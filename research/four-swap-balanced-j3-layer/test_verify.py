#!/usr/bin/env python3
"""Independent pins for verify.py of research/four-swap-balanced-j3-layer.

The algebraic expectations here were derived by hand (2x2 matrix products over
F2 and the expansion of ([a]+1)([b]+1)([a]+1)) before verify.py existed, so a
failure indicates a bug in the checker, not in the expectation. Stdlib only.
"""
import importlib.util
import itertools
import pathlib
import random
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("j3verify", HERE / "verify.py")
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)


class AlgebraPins(unittest.TestCase):
    def setUp(self):
        V.build()

    def test_involution_squares_vanish(self):
        for g in (V.A, V.B, V.S):
            x = V.gplus(g)
            self.assertEqual(V.rmul(x, x), 0)

    def test_one_swap_word_at_r1(self):
        # The three-call word aba at r=1 (N = [1]) equals [s] exactly:
        # each factor I + ([g]+1) collapses to [g] in dimension one.
        labels = (V.A, V.B, V.A)
        word = V.word_value(1, labels, (V.idem(1, 1, 1),) * 3)
        self.assertEqual(word, (1 << V.idx(V.S),))

    def test_xyx_pin(self):
        # Hand expansion: ([a]+1)([b]+1)([a]+1) = [aba] + [ab] + [ba] + [b]
        # with NO identity term (the two [1] summands cancel over F2).
        x, y = V.gplus(V.A), V.gplus(V.B)
        got = V.rmul(V.rmul(x, y), x)
        ab = V.idx(V.mm2(V.A, V.B))
        ba = V.idx(V.mm2(V.B, V.A))
        want = (1 << V.idx(V.S)) ^ (1 << ab) ^ (1 << ba) ^ (1 << V.idx(V.B))
        self.assertEqual(got, want)

    def test_layer_expansion_identity(self):
        # prod(1+eps_i) == 1 + sum eps_i + sum_{i<j} eps_i eps_j  (mod J^3),
        # in the exact quotient for seeded random words.
        rng = random.Random(20261014)
        idems = V.rank_one_idempotents(4)
        lab = (V.A, V.B)
        for _ in range(50):
            q = rng.randrange(1, 8)
            labels = tuple(lab[rng.randrange(2)] for _ in range(q))
            mats = tuple(rng.choice(idems) for _ in range(q))
            self.assertTrue(V.layer_expansion_holds(4, labels, mats))


class WordControls(unittest.TestCase):
    def setUp(self):
        V.build()

    def test_direct_words_hit_targets(self):
        for r, labels, mats, k in V.direct_control_words():
            self.assertEqual(V.word_value(r, labels, mats), V.target(r, k),
                             "direct word must realize the target")

    def test_mutated_words_fail(self):
        for r, labels, mats, k, mut in V.mutation_controls():
            self.assertNotEqual(V.word_value(r, labels, mats), V.target(r, k),
                                "mutation control must fail: " + mut)

    def test_conjugation_closure(self):
        rng = random.Random(7)
        idems = V.rank_one_idempotents(4)
        gl = V.gl_elements(4)
        for _ in range(50):
            n = rng.choice(idems)
            u = rng.choice(gl)
            c = V.conjugate(4, u, n)
            self.assertIn(c, idems)


class SearchControls(unittest.TestCase):
    def setUp(self):
        V.build()

    def test_search_finds_known_small_instances(self):
        # Smallest falsifying instances first: where a balanced word is known
        # to exist, the search must actually find one.
        r1 = V.search(1, 3, 1, 1, samples=2000, seed=11)
        self.assertIsNotNone(r1["full_witness"], "r=1, q=3, 1a2b must find bab")
        r2 = V.search(2, 6, 3, 2, samples=20000, seed=12)
        self.assertIsNotNone(r2["full_witness"], "r=2, q=6, 3a3b must find aba|bab")

    def test_layer_is_a_strict_relaxation(self):
        # Honesty control: a word that passes the J^3 layer check but fails
        # full formal equality must exist at a known-solvable instance.
        r2 = V.search(2, 6, 3, 2, samples=20000, seed=12)
        self.assertGreater(r2["layer_hits"], 0)
        self.assertIsNotNone(r2["layer_only_witness"])
        labels, mats = r2["layer_only_witness"]
        self.assertTrue(V.layer_value_ok(2, labels, mats, 2))
        self.assertNotEqual(V.word_value(2, labels, mats), V.target(2, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
