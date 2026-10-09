import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import docker_inventory as inv

class InventoryTests(unittest.TestCase):
    def test_offline_only_collects_definitions(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'Dockerfile').write_text('FROM alpine\n')
            (p/'compose.yaml').write_text('services: {}\n')
            (p/'.env').write_text('MY_PASSWORD=secret\n')
            (p/'README.txt').write_text('hi')
            result,truncated=inv.offline_files(p)
            self.assertFalse(truncated)
            self.assertEqual({x['path'] for x in result}, {'Dockerfile','compose.yaml'})
            self.assertNotIn('secret',json.dumps(result))
    def test_default_has_no_live_commands(self):
        ns=inv.parse_args([])
        self.assertFalse(ns.live)
        data=inv.build_inventory(ns)
        self.assertEqual(data['collection_mode'],'offline')
        self.assertEqual(data['services'],[])
    def test_environment_validation(self):
        ns=inv.parse_args(['--environment','homolog'])
        self.assertEqual(ns.environment,'homolog')

if __name__ == '__main__':
    unittest.main()

class LiveScopeTests(unittest.TestCase):
    def test_live_requires_context_and_project(self):
        with self.assertRaises(SystemExit):
            inv.parse_args(['--live'])
        ns=inv.parse_args(['--live','--project','my-app','--expected-context','default'])
        self.assertEqual(ns.project,'my-app')
        self.assertEqual(ns.expected_context,'default')
