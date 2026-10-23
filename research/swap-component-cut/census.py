#!/usr/bin/env python3
"""Exact additivity census at n = 3, R = 2 (about four minutes).

For every pair (g, h) in GL_3(F2) x GL_3(F2), with word lengths l(g), l(h)
in coordinate CNOTs, search for a formal word of length <= min(l(g)+l(h)-1, 5)
realizing diag([g], [h]). None exists, so the formal cost is at least
min(l(g)+l(h), 6), and equals l(g)+l(h) whenever that sum is at most six.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE))

import formal  # noqa: E402


def main() -> None:
    model = formal.Model(3, 2)
    forward = model.layers(model.diagonal([]), 3)
    lengths = formal.word_lengths(3)
    if sorted(lengths.values()).count(6) != 2 or len(lengths) != 168:
        raise SystemExit("FAIL: GL_3 word lengths")
    checked = 0
    for g, h in itertools.product(lengths, lengths):
        total = lengths[g] + lengths[h]
        if total <= 1:
            continue
        budget = min(total - 1, 5)
        target = model.diagonal([g, h])
        best = model.shortest(target, forward, max(0, budget - 3)) if budget > 3 else forward.get(target)
        if best is not None and best <= budget:
            raise SystemExit(f"FAIL: shorter word for {g}, {h}: {best} < {total}")
        checked += 1
    if checked != 168 * 168 - 13:
        raise SystemExit("FAIL: census size")
    print(f"PASS_SWAP_COMPONENT_CENSUS pairs={checked} no_shorter_word")


if __name__ == "__main__":
    main()
