"""Run the source-bound emitter byte contract in the existing Python matrix."""
from pathlib import Path
import subprocess
import sys
import unittest


class EmitterDigestCacheTest(unittest.TestCase):
    def test_complete_source_bound_byte_contract(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, '-B', str(root/'research/e8-emitter-digest-cache/verify.py')],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main()
