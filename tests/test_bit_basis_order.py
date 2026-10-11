"""Run the complete source-basis finite-cost evidence audit in existing CI."""
from pathlib import Path
import subprocess
import sys
import unittest


class BitBasisOrderTest(unittest.TestCase):
    def run_package_script(self, name):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, '-B', str(root/'research/e8-bit-basis-order'/name)],
            cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_literal_equivalence_prefix_and_complete_invoice(self):
        self.run_package_script('verify.py')

    def test_postprocessor_contracts_and_cli(self):
        self.run_package_script('test_postprocess.py')


if __name__ == '__main__':
    unittest.main()
