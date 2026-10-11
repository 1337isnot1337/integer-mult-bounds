"""Endpoint contracts, exact regressions and malformed chronology."""
from pathlib import Path
import copy
import unittest

from fractions import Fraction as Q
from chart_audit import audit, gaussian_witness, programs419, read, replay

ROOT = Path(__file__).resolve().parent


class ChartTests(unittest.TestCase):
    def test_admitted_word_retains_each_dirty_input(self):
        candidate = read(ROOT/'inputs/admitted416-candidate.json.gz')
        programs = read(ROOT/'inputs/admitted416-programs.json.gz')['local_programs']
        result = audit(candidate, programs)
        self.assertEqual(result['status'], 'PASS_REQUIRED_ENDPOINT')
        for orientation in result['orientations'].values():
            self.assertEqual(orientation['chart_sensitive_bad_registers'], 0)

    def test_prewhitening_counterexample_survives_entrance_upgrade(self):
        for name in ('original419', 'changed419'):
            candidate = read(ROOT/f'inputs/{name}-candidate.json.gz')
            result = audit(candidate, programs419(candidate))
            self.assertEqual(result['status'], 'ENDPOINT_NOT_ESTABLISHED')
            for ori, count, output, source, real, imaginary in (
                    ('forward', 430, 244, 255, '1/8', '1/8'),
                    ('backward', 483, 246, 420, '-1/4', '-1/4')):
                r = result['orientations'][ori]
                self.assertEqual(r['status'], 'FAIL_EXACT_GAUSSIAN_ENDPOINT')
                self.assertEqual(r['ordinary_scalar_bad_registers'], 0)
                self.assertEqual(r['chart_sensitive_bad_registers'], count)
                self.assertEqual(r['chart_sensitive_bad_targets'], 0)
                witness = r['exact_witness']
                self.assertEqual((witness['output_register'], witness['dirty_source']), (output, source))
                self.assertTrue(witness['off_diagonal'])
                self.assertEqual(witness['first_nonzero'],
                                 dict(address=0, real=real, imaginary=imaginary))

    def test_normalization_phase_cannot_be_omitted(self):
        candidate = read(ROOT/'inputs/admitted416-candidate.json.gz')
        programs = read(ROOT/'inputs/admitted416-programs.json.gz')['local_programs']
        events = copy.deepcopy(programs['forward'])
        events.remove(['phase', 'ad0'])
        with self.assertRaisesRegex(AssertionError, 'Unexpected phase order'):
            replay(candidate, events, 'forward', charts=True)

    def test_formal_tokens_alone_do_not_establish_a_counterexample(self):
        # Frame zero and I are different formal tags but the same operator.
        self.assertIsNone(gaussian_witness({'h':1, 'frames':[[]]},
                                          {0:{(1,-1):Q(1), (1,0):Q(-1)}}))


if __name__ == '__main__':
    unittest.main()
