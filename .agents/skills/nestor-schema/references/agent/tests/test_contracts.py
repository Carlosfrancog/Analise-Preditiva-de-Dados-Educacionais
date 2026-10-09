import json
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1]
try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:
    Draft202012Validator = None
    ValidationError = None


@unittest.skipUnless(Draft202012Validator, 'Instalar jsonschema para verificar contratos')
class SchemaTests(unittest.TestCase):
    def test_examples_validate(self):
        for path in sorted((BASE / 'schemas').glob('*.schema.json')):
            with self.subTest(path=path.name):
                schema = json.loads(path.read_text(encoding='utf-8'))
                Draft202012Validator.check_schema(schema)
                example_path = BASE / 'examples' / path.name.replace('.schema.json', '.example.json')
                example = json.loads(example_path.read_text(encoding='utf-8'))
                Draft202012Validator(schema).validate(example)

    def test_reject_database_executed(self):
        path = BASE / 'schemas/migration-plan.schema.json'
        schema = json.loads(path.read_text(encoding='utf-8'))
        example = json.loads((BASE / 'examples/migration-plan.example.json').read_text(encoding='utf-8'))
        example['execution']['executed'] = True
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(example)

    def test_reject_invented_fact_label(self):
        path = BASE / 'schemas/reader-inventory.schema.json'
        schema = json.loads(path.read_text(encoding='utf-8'))
        example = json.loads((BASE / 'examples/reader-inventory.example.json').read_text(encoding='utf-8'))
        example['evidence'][0]['label'] = 'CERTAINLY_TRUE'
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(example)

if __name__ == '__main__':
    unittest.main()
