"""Behavioral boundaries of the finite target constructor."""
import unittest
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys

from assembly import INITIAL, ceiling, construct, greatest_grid_target


class FiniteAssemblyTests(unittest.TestCase):
    def test_targets_across_both_binding_regimes(self):
        caps = [INITIAL*Q(1001, 1000), Q(1, 1000), Q(1, 100), Q(1, 33)]
        for bit in caps:
            for complex_ in caps:
                for fraction in [Q(1, 100), Q(1, 2), 1-Q(1, 10**30)]:
                    with self.subTest(bit=bit, complex_=complex_, fraction=fraction):
                        target = ceiling(bit, complex_)*fraction
                        result = construct(bit, complex_, target, coefficient_bits=30000)
                        seed = result['seed']
                        self.assertLess(seed, bit)
                        self.assertLess(seed, (1-result['beta'])*complex_)
                        self.assertGreater(result['eta'], 0)
                        self.assertGreater(result['beta'], 0)
                        self.assertEqual(len(result['strict_constraints']), 47)
                        self.assertTrue(all(v > 0 for v in result['strict_constraints'].values()))
                        self.assertGreater(result['minimum_margin'], target)
                        for j, value in enumerate(result['bootstrap_chain']):
                            self.assertEqual(value, seed-(seed-INITIAL)*seed**j)
                        for entry in result['cutoffs']:
                            length, gap = entry['cutoff_log2'], entry['gap']
                            self.assertIsInstance(length, int)
                            self.assertGreaterEqual(length*gap**2, 36)
                            self.assertGreaterEqual(length*gap, 2*(4+30000))

    def test_grid_maximality_including_exact_endpoint(self):
        bit = complex_ = Q(1, 99)  # Supremum is exactly 1/100.
        for grid in [Q(1, 10000), Q(3, 10000), Q(1, 10**100)]:
            target = greatest_grid_target(bit, complex_, grid)
            self.assertEqual((target/grid).denominator, 1)
            self.assertLess(target, Q(1, 100))
            self.assertGreaterEqual(target+grid, Q(1, 100))
            self.assertGreater(construct(bit, complex_, target)['minimum_margin'], target)

    def test_no_bootstrap_needed_below_inherited_bound(self):
        result = construct(Q(1, 100), Q(1, 50), INITIAL/4)
        self.assertEqual(result['bootstrap_chain'], [INITIAL])
        self.assertEqual(result['cutoffs'], [])

    def test_cli_exports_fine_grid_witness(self):
        grid = Q(1, 10**100)
        completed = subprocess.run(
            [sys.executable, '-B', str(Path(__file__).with_name('assembly.py')),
             '--bit', '1/99', '--complex', '1/99', '--grid', str(grid)],
            check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = json.loads(completed.stdout)
        self.assertEqual(result['target'], str(greatest_grid_target(Q(1, 99), Q(1, 99), grid)))
        self.assertEqual(len(result['strict_constraints']), 47)
        # Inspect the serialized signs without reparsing huge decimal strings
        # into integers under this test process's own conversion guard.
        self.assertTrue(all(value[0] in '123456789' for value in result['strict_constraints'].values()))
        self.assertGreater(max(map(len, result['strict_constraints'].values())), 4300)

    def test_unattainable_targets_and_invalid_premises_rejected(self):
        for target in [Q(0), Q(-1), Q(1, 100), Q(1, 99)]:
            with self.subTest(target=target), self.assertRaises(ValueError):
                construct(Q(1, 99), Q(1, 99), target)
        for bit, complex_ in [(INITIAL, Q(1, 100)), (Q(1, 100), Q(1, 32))]:
            with self.subTest(bit=bit, complex_=complex_), self.assertRaises(ValueError):
                construct(bit, complex_, Q(1, 100000))
        for charge in [0, -1, True, Q(3, 2)]:
            with self.subTest(charge=charge), self.assertRaises(ValueError):
                construct(Q(1, 99), Q(1, 99), Q(1, 1000), coefficient_bits=charge)
        for grid in [0, -1, Q(1, 100)]:
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                greatest_grid_target(Q(1, 99), Q(1, 99), grid)


if __name__ == '__main__':
    unittest.main()
