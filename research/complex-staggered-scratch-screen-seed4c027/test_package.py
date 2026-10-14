#!/usr/bin/env python3
"""Focused exact controls for the interval and moment screen."""
from __future__ import annotations

import itertools
import unittest

import verify


def brute_max(intervals, capacity):
    best = 0
    for mask in range(1 << len(intervals)):
        chosen = [intervals[i] for i in range(len(intervals)) if mask >> i & 1]
        try:
            verify.check_capacity(chosen, capacity)
        except ValueError:
            continue
        best = max(best, len(chosen))
    return best


class IntervalControls(unittest.TestCase):
    def test_exhaustive_small_interval_families(self):
        universe = [(a, b, "A", i, 0)
                    for i, (a, b) in enumerate(itertools.combinations(range(4), 2))]
        for mask in range(1 << len(universe)):
            intervals = [universe[i] for i in range(len(universe)) if mask >> i & 1]
            for capacity in (1, 2, 3):
                selected = verify.maximum_interval_schedule(intervals, capacity)
                self.assertEqual(len(selected), brute_max(intervals, capacity))

    def test_empty_capacity_and_invalid_interval(self):
        intervals = [(0, 2, "A", 1, 0), (1, 3, "A", 2, 0)]
        self.assertEqual(verify.maximum_interval_schedule(intervals, 0), [])
        self.assertEqual(len(verify.maximum_interval_schedule(intervals, 1)), 1)
        with self.assertRaises(ValueError):
            verify.maximum_interval_schedule([(2, 2, "A", 1, 0)], 1)

    def test_inclusive_collision_control(self):
        with self.assertRaises(ValueError):
            verify.check_capacity([(0, 2, "A", 1, 0), (2, 4, "B", 2, 0)], 1)


class CostControls(unittest.TestCase):
    def test_batch_replacement_preserves_paid_mass(self):
        baseline_mass = sum(r * n for r, n in verify.BASE_PROFILE.items())
        for count in (0, 1, 85, 369):
            profile = verify.profile_for_batches(count)
            self.assertEqual(sum(r * n for r, n in profile.items()), baseline_mass)
            self.assertEqual(profile[1], verify.BASE_PROFILE[1] - 3 * count)
            self.assertEqual(profile[3], verify.BASE_PROFILE[3] + count)
        with self.assertRaises(ValueError):
            verify.profile_for_batches(-1)

    def test_source_pinned_screen_stops_below_five_percent(self):
        result = verify.compute()
        self.assertEqual(result["candidate_triples"], 369)
        self.assertEqual(result["capacities"][-1]["simultaneous_packets"], 5)
        self.assertEqual(result["capacities"][-1]["scratch_arrays"], 15)
        self.assertEqual(result["capacities"][-1]["selected_triples"], 85)
        self.assertEqual(result["capacities"][-1]["ceiling_grid_bracket"],
                         ["107/62500", "1713/1000000"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
