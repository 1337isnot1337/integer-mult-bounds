#!/usr/bin/env python3
"""Negative controls: each deliberate defect must make verify.py fail."""

import unittest
from pathlib import Path
from unittest import mock

import runpy

V = runpy.run_path(str(Path(__file__).resolve().parent / "verify.py"))


def fails(fn, *args):
    try:
        fn(*args)
    except SystemExit as exc:
        return str(exc).startswith("FAIL")
    return False


class Controls(unittest.TestCase):
    def test_tampered_input_hash(self):
        bad = {k: "0" * 64 for k in V["INPUTS"]}
        with mock.patch.dict(V["load"].__globals__["INPUTS"], bad):
            self.assertTrue(fails(V["load"]))

    def test_oracle_rejects_an_unsound_test(self):
        # A test that grants only shared snapshots misses helper paths.
        g = V["oracle"].__globals__
        with mock.patch.dict(g, {"small_sharp": lambda inst: {
                (t, s) for s, xc in enumerate(inst[1])
                for t, yc in enumerate(inst[2]) if set(xc) & set(yc)}}):
            self.assertTrue(fails(V["oracle"], 7, ((3, 400),), 120))

    def test_dropping_nesting_breaks_pr3427_masks(self):
        g = V["sharp_by_frames"].__globals__
        r = V["p104"]()
        loose = [0] * 104
        geo, paths = r["geo"], r["paths"]
        masks = V["endpoint_masks"](geo)
        frames = {f for k in "XY" for i in range(104)
                  for f in paths[k + str(i)]}
        adm = {f: V["admit_mask"](geo, masks, f) for f in frames}
        for t in range(104):
            for s in range(104):
                if any(adm[v] and adm[w] for v in paths["X%d" % s]
                       for w in paths["Y%d" % t]):
                    loose[t] |= 1 << s
        got = [sum(1 << t for t in range(104) if loose[t] >> s & 1)
               for s in range(4)]
        self.assertNotEqual(tuple(got), g["PR3427_SOURCE_MASKS"])

    def test_wrong_rectangle_is_rejected(self):
        g = V["rank_consequence"].__globals__
        r = V["p104"]()
        with mock.patch.dict(g, {"RANK_ROWS": g["RANK_ROWS"] + (71,)}):
            self.assertTrue(fails(V["rank_consequence"], r))

    def test_y_relay_counterexample_is_a_real_escape(self):
        self.assertEqual(V["y_relay_counterexample"](), (1, True))


if __name__ == "__main__":
    unittest.main()
