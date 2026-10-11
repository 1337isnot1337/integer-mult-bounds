"""Exercise the complete offline assembly package in the existing test matrix."""
from pathlib import Path
import os
import subprocess
import sys
import unittest


class FiniteAssemblyPackageTest(unittest.TestCase):
    def test_pinned_supplier_evidence_and_finite_frontier(self):
        root = Path(__file__).resolve().parents[1]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONOPTIMIZE', None)
        result = subprocess.run(
            [sys.executable, '-B', str(root/'research/finite-assembly-frontier/verify.py')],
            cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main()
