"""Run the hosted bit contract regressions in the existing Python matrix."""
from pathlib import Path
import subprocess
import sys
import unittest


class HostedBitContractTest(unittest.TestCase):
    def test_source_bound_positive_and_regression_audit(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, '-B', str(root/'research/e8-hosted-bit-contract/verify.py')],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main()
