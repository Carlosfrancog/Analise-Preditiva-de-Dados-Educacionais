import importlib.util
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'tools/inventory_laravel.py'
spec = importlib.util.spec_from_file_location('inventory_laravel', TOOL)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InventoryTests(unittest.TestCase):
    def test_laravel_files_and_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            migration = base / 'database/migrations/2026_01_01_create_records.php'
            migration.parent.mkdir(parents=True)
            migration.write_text("<?php\nSchema::create('records', function () {});\n", encoding='utf-8')
            model = base / 'app/Models/Record.php'
            model.parent.mkdir(parents=True)
            model.write_text("<?php\nclass Record extends Model {\n  return $this->belongsTo(User::class);\n}", encoding='utf-8')
            report = module.inventory(base)
            kinds = [x['kind'] for x in report['findings']]
            self.assertIn('migration_create', kinds)
            self.assertIn('eloquent_model', kinds)
            self.assertIn('eloquent_relation', kinds)
            refs = {ev['id'] for ev in report['evidence']}
            self.assertTrue(all(set(f['evidence_refs']) <= refs for f in report['findings']))
            self.assertEqual(report['evidence'][0]['line'], 2)

    def test_skip_sensitive_and_vendor_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / '.env').write_text('SECRET=do-not-read\nSchema::create("secret",1)', encoding='utf-8')
            vendor = base / 'vendor/package/File.php'
            vendor.parent.mkdir(parents=True)
            vendor.write_text('Schema::create("fake", 1)', encoding='utf-8')
            report = module.inventory(base)
            self.assertEqual(report['evidence'], [])
            self.assertNotIn('SECRET', str(report))

    def test_reject_bad_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                module.inventory(Path(tmp), max_files=0)

    def test_max_files_truncation(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / 'app';base.mkdir()
            for i in range(4):
                (base / f'C{i}.php').write_text('class Record extends Model {}', encoding='utf-8')
            report = module.inventory(Path(tmp), max_files=2)
            self.assertEqual(len(report['findings']), 2)
            self.assertTrue(any('inventário parcial' in gap for gap in report['gaps']))

if __name__ == '__main__':
    unittest.main()
