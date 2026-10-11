"""Run the source-bound scalar address cache contract in the existing matrix."""
from pathlib import Path
import subprocess
import sys
import unittest


class ScalarAddressCacheTest(unittest.TestCase):
    def test_exact_source_replay_and_boundary_controls(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, '-B', str(root/'research/e8-scalar-address-cache/verify.py')],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main()
