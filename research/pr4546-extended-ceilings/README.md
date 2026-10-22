# #4546's zero shear headroom, recomputed independently and extended to six-shear words

**Task:** independent-moment. **Base:** canonical main `f626db5c`. **No new κ.**

Clear1nsight's #4546 (head `55b8d34c`) certifies **zero optimistic headroom** at C = 0.00302015 in the first twelve #4470 phase-B receiver windows. The candidates are every word of at most **four** unit shears on the same three persistent fields, with the same exact endpoint and fixed entrance/exit frames. Its open question asks to change the length cap before reopening the domain.

This package recomputes #4546 with separately written code and **extends the cap to five and six shears**. Nothing is imported from #4546. The windows are extracted by this package's own code from the canonical #4470 constructor in main (`research/joint-helper-lattice/native_joint.py`, run isolated on its pinned inputs). #4546's `RESULT.json` (blob `f2f41100`) is vendored only for cross-checking.

## Results

1. **Reproduction at length ≤ 4.** All twelve windows match #4546 exactly:
   - index, roles, coefficients, phase, start/exit dimensions and old paid profile;
   - 22,621 words with 84 endpoint matches each;
   - relaxed-profile counts of 1, or 4 for windows 10575 and 10579;
   - a best optimistic gain of exactly 0.
2. **Lengths 5 and 6.** These add 248,832 and 2,985,984 words, with matches found by meet in the middle over exact integer matrices. Every window then has 272 matching words (≤ 5) and **3,812** (≤ 6), and every one is admitted by the dimension screen. **The relaxed-profile set is unchanged in every window, and the best optimistic gain stays exactly 0.**

| window | old paid | relaxed profiles (≤4 / ≤5 / ≤6) | best gain |
|---|---|---|---|
| 10554, 10555 | {2:1} | 1 / 1 / 1 | 0 |
| 10557, 10560, 10561, 10563 | {1:3} | 1 / 1 / 1 | 0 |
| 10558 | {1:2} | 1 / 1 / 1 | 0 |
| 10564 | {1:1} | 1 / 1 / 1 | 0 |
| 10575, 10579 | {1:1, 2:1, 3:1} | 4 / 4 / 4 | 0 |
| 10577, 10581 | {1:2, 2:1} | 1 / 1 / 1 | 0 |

**Why it does not move.** In this relaxation, every contact frame lies between the forward sum of the operands' current lower bounds and the backward intersection of their exits. For these windows those bounds already pin each field's admissible rank steps. For example, in the `{1:3}` windows a field climbing `0 → 2` has every contact capped at an exit intersection of dimension 1. Longer words only add contacts under the same caps, so they cannot merge the two rank-1 payments. This explains the observed invariance but is **not** proved here for all lengths; the checked statement is lengths ≤ 6.

**Model** (re-implemented from #4546's README):
- each shear acts in one common binary frame, and frames only grow along a field's path;
- forward mandatory spans and backward permissible intersections bound every contact;
- integer contact dimensions are enumerated, and every positive gap, exit gaps included, is charged;
- ranks are priced `r^(1−C)` with certified rational enclosures.

The relaxation contains every actual monotone path, so a zero ceiling rules out gains from any word in the class.

## Verify

```text
python3 -B research/pr4546-extended-ceilings/verify.py
```

This runs in about 3 s with the standard library only.

## Limitations

- **Coverage.** Only the first twelve of the 128 eligible windows are covered, as in #4546. Only unit coefficients, the same three fields and fixed boundaries are allowed.
- **Lengths.** Lengths above 6 are not checked, and the structural explanation above is not a proof for all lengths.
- **Overlap.** Individual window results must not be summed across overlapping windows.

## Open next questions

- Prove the length-independence: show that the relaxed-profile set of a window is determined by its start and exit frames. First step: characterise the reachable contact dimensions from the pairwise exit intersections and start sums alone.
- Apply the same computation to the other 116 eligible windows, with a structural reason to expect headroom first, as #4546 asks.

Credit: Clear1nsight (#4546), Cinna Davis (#4470), and zxv's receiver-sharing and helper work. Prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
