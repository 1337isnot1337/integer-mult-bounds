"""Rejection controls for research/even-target-cnot-census/verify.py."""

import json
import random
import unittest
from pathlib import Path

import verify as v


class PackageTests(unittest.TestCase):
    def test_attaining_words_are_exact(self):
        for r in (1, 2, 3):
            w = v.word_even(r)
            self.assertTrue(v.formal_is_target(v.formal_word_value(w, r), r))
            self.assertTrue(v.layer_ok_even_target(w, r))

    def test_drop_one_rejected(self):
        r = 3
        w = v.word_even(r)
        for drop in range(len(w)):
            mut = w[:drop] + w[drop + 1:]
            self.assertFalse(v.formal_is_target(v.formal_word_value(mut, r), r))

    def test_wrong_label_rejected(self):
        r = 2
        w = v.word_even(r)
        bad = list(w)
        gi, vv, pp = bad[0]
        bad[0] = (v.B_IDX, vv, pp)
        self.assertFalse(v.formal_is_target(v.formal_word_value(bad, r), r))

    def test_layer_system_rejects_wrong_target_word(self):
        # a word that hits [c] cannot satisfy the SWAP-target layer system
        self.assertFalse(v.layer_ok_swap_target(v.word_even(2), 2))
        self.assertTrue(v.layer_ok_swap_target(v.word_swap(2), 2))

    def test_parity_and_or_confusion_control(self):
        # the natural target transform is F_2 addition: 1+1 = 0 (a row of
        # two equal bits must cancel).  Regression for a | / ^ confusion.
        r = 2
        v.set_r(r)
        s = (0b11 << 0) | (0b11 << (v.ROWSZ * 1))  # rows 0 and 1 = (1,1)
        got = v.nat_right_target(s, v.MAT_C, r)
        # rho(c) = [[0,1],[1,1]]; a row (1,1) maps to (1^1, 1^1) = (1,0)
        row0 = (got >> 0) & 0b11
        row1 = (got >> v.ROWSZ) & 0b11
        self.assertEqual(row0, 0b01)
        self.assertEqual(row1, 0b01)

    def test_receipt_rejects_mutation(self):
        here = Path(__file__).resolve().parent
        stored = json.loads((here / "RECEIPT.json").read_text(encoding="utf-8"))
        fresh = json.loads(json.dumps(v.run(fast=True), default=str))
        for key in ("t1r1", "small_minima", "swap_t2r2"):
            self.assertEqual(stored.get(key), fresh.get(key))
        tampered = json.loads(json.dumps(stored))
        tampered["main_t4r4"]["q"]["6"] = 99
        self.assertNotEqual(tampered["main_t4r4"]["q"], fresh["main_t4r4"].get("q", {}))

    def test_random_words_do_not_hit_target(self):
        rng = random.Random(99)
        r = 2
        v.set_r(r)
        gens = v.make_gens(r)
        for _ in range(30):
            n = rng.randrange(1, 6)
            s = v.nat_identity()
            for _k in range(n):
                s = v.nat_right_mul(s, gens[rng.randrange(len(gens))])
            self.assertNotEqual(s, v.nat_right_target(v.nat_identity(), v.MAT_C, r))


if __name__ == "__main__":
    unittest.main()
