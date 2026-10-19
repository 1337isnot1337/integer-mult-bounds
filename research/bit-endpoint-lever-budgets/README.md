# Bit-lever budgets at the +10% bit endpoint, on the actual PR589 histogram

**Planning bound and scoped proof (bit supplier). No construction, no κ claim, not a multiplication theorem.**
The selected record is unchanged: κ = 0.001672660197076918 (#1094), complex-bound.

- Track: bit (weight 20). Card: `bit-helper-contract`, scope **changed** to lever pricing (see [TASK.json](TASK.json)).
  Consuming decision: `centre-path-sharing`.
- Base: canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90` (priority revision 6). Pins: [SOURCES.json](SOURCES.json).

## Statement

[centre-sharing-overhead-budget](../centre-sharing-overhead-budget/README.md) (PR1791) showed that two-call centre
sharing makes the complex side stop binding. A **+10%** whole-bound κ then needs the bit endpoint
**c\* = 921658892752012102303/5·10²³ ≈ 0.0018433178** (1.0634× the selected bit endpoint). On the cited PR589 bit
histogram that is a net saving of **649 rank-1 children** (648 fails). Its open question 1 asks whether any bit lever
supplies that. This package prices each catalogued revision-3 bit lever **on the actual histogram** (deficit 10,272,
m = 64, W = 28,416, T = 32 replicas, 288 stage calls, nine rank-7 copies per call, halving depth 2). The surcharge is
recomputed from each histogram's child count. Every count below is a **sharp integer at c\***: the stated count
passes the exact moment test and one less fails (one more, for budgets). The same signs hold at c\* + 10⁻²⁴.

| Lever (one premise changed on the actual histogram) | Admitted today? | Net saving at c\* (rank-1 units) | Sharp size that clears 649 |
|---|---|---:|---|
| (a) Halving depth 3 / 4 (idle cap 45 → 50 / 53) | yes (r740 row bound) | **0 exactly** | none: the cap is slack |
| (a′) Width-8 re-hosting inside the actual idle windows | yes | **0 exactly** (record is optimal) | none |
| (b1) Rank-8 copy carriage, 9 copies per call (cst 63 → 72) | in (Bat) window | **−2,577.6** | none (makes things worse) |
| (b2) Fewer rank-7 copies | no (new decoder contract) | +2,008.8 for one fewer per call | **93 copies** record-wide (92 fails), i.e. one per call |
| (b3) Bit centre path shared by two calls (cst 31.5) | no (unconstructed) | **+9,039.5** | passes with overhead ≤ **8,391 rank-1 / 1,203 rank-7 / 201 rank-42** children (29.1–29.3 units per call) |
| (c) Second unpaid coordinate on F families | no (coverage-law change) | ≤ F | **F ≥ 649** of 28,416 (2.28%), necessary |
| (d) Pure helper deletion, most favorable (8 rank-1 climbs each), optimal width-8 re-hosting | no (PR1250: one removable helper) | +658.5 at d = 40 | **d = 40 per call** (39 fails for every hosting) |
| (d) Helper deletion, PR1043's measured delta | no | ≤ +169.8 | none: the model runs out of rank-7 climbs at d ≤ 19 |
| (e) Ideal in-window local shapes (single rank-7 data climbs, single rank-8 helper climbs) | no (no such word) | +3,647.6 in all 288 calls | **52 of 288 calls** (51 fails) |

**Conclusion.** No admitted bit lever nets anything at c\*. The admitted levers are the halving-depth cap raise,
width-8 re-hosting and rank-8 copy carriage. Their nets are 0, 0 and −2,578, so any combination of them also fails.
Every lever that clears 649 changes the word, the decoder or the coverage law. The cheapest stated sizes are one
fewer rank-7 copy per call, 40 pure helper deletions per call (9.3% of 430) or the ideal local shapes in 52 calls.

**Consequence for `centre-path-sharing`.** The catalogued route to +10% through two-call sharing is to share the
centre path **on both suppliers**. The bit-side copy of the same mechanism (row b3) has about 14× the needed saving.
Its overhead budget is ≈ 29.1–29.3 paid-mass units per call. With the complex side at c\* + 10⁻²⁴ and the bit side
at c\*, κ is still ≥ 1.1× selected (checked). The complex side's two-call overhead budget **at c\*** is
≤ 4,079 rank-1 or 511 rank-8 children in total: **≈ 28.3–28.4 units per call**. That is tighter than the
30.5–30.8 that PR1791 gives at the selected bit endpoint, which is the right figure only for the +3.45% cap. Without
a bit-side mechanism of one of the stated sizes, the card's stop rule holds for the catalogued lever set.

## Why the admitted levers give exactly zero (proof)

**Windows.** The nine-stage recipe (`global_k.py`, PR #463/#510 lineage, K = 4 pairs) creates nine idle events per
replica: ranks 14, 28, 42 for s = 1, 3, 5, then 7, 7, 7 for s = 2, 4, 6, then 42, 28, 14 (and one rank-0 event) at
s = 8. Each event covers 2v = 222 coordinates. Per replica that gives windows {7: 666, 14: 444, 28: 444, 42: 444}.
`verify.py` derives this from the recipe rules and checks that the record's idle part (profile minus 288 shipped
words) equals T × {2: 435, 4: 444, 6: 444, 7: 666, 42: 9}, the remainder left after hosting 9 × 439 width-8 helpers
per replica.

**(a) The cap is slack.** HD = 2 caps children at 45, since 2r² < 64² ⇔ r ≤ 45. HD = 3 and 4 raise the cap to 50
and 53. But every idle child is a window remainder, at most the largest window 7(2K − 2) = 42, and every local
child has rank ≤ 7. So the record's max child is 42 < 45, and raising the halving depth admits no histogram the
fixed windows can produce. Its net saving is exactly 0. Longer windows need a different recipe. In
[bit589-recipe-floor](../bit589-recipe-floor/README.md) (PR1487)'s whole class of nine-stage recipes, that package
reports the longest advance as 2(K − 1) = 6 levels, i.e. a window of 42, so the cap is slack there too.

**(a′) Width-8 re-hosting cannot help.** A rank-r window holds at most ⌊r/8⌋ width-8 helpers. 8 divides no window
rank, so every window keeps exactly one nonzero remainder child, and the child count (hence the surcharge) is fixed.
Write φ(x) = x(m/x)^a, which is concave. A window with base remainder ρ = r − 8⌊r/8⌋ and u unused slots costs
φ(ρ + 8u), so its extra cost g_ρ(u) = φ(ρ + 8u) − φ(ρ) is concave in u with g_ρ(0) = 0. Hence
g_ρ(u) ≥ u·g_ρ(cap)/cap. Each replica has exactly 3,996 − 3,951 = 45 unused slots. So the total extra cost is
at least 45·min over ρ of g_ρ(cap)/cap.

At c\* the per-slot costs are certified as 7.94284 (rank-42 window) < 7.94625 (rank 28) < 7.95184 (rank 14) rank-1
units. So the minimum is 45·g_2(5)/5, which the record attains by leaving 9 rank-42 windows empty. The record's
hosting therefore minimizes the bill over all width-8 hostings of the actual windows, even with the per-stage window
constraints relaxed. The same bound holds record-wide (1,440 unused slots), so pooling across replicas does not
help either. This re-certifies, at c\*, what our merged
[bit589-width-packing](../bit589-width-packing/README.md) (#1023) proved at the selected endpoint.

**(b1) Copy carriage.** The decoder constant is the sum of the copy ranks: format-limits' T(2Kv − L·cst). With whole
copies, rank-8 carriage of the nine copies raises cst to 72 and the paid mass by 2,592. That increases the bill.
PR1334's "rank-8 carriage" row kept cst = 63 with 63/8 fractional copies, which is the fewer-copies lever (b2).

**(c) One unit of rank mass is worth at most one rank-1 child.** Trimming a rank-r child to r − 1 saves
φ(r) − φ(r − 1) < φ(1), certified for r = 2..42 at c\*. Removing a rank-1 child also removes its surcharge. So F
doubly-unpaid families save at most F rank-1 children, and F ≥ 649 is necessary.

**(d) Deletion bounds.** For d deletions per call, the 45 + 9d unused slots per replica are priced two ways:
- from below, by the concavity bound (all at the rank-42 per-slot cost, fractional);
- from above, by an explicit hosting (⌊(45 + 9d)/5⌋ empty rank-42 windows plus one partly used rank-42 window).

In the most favorable pure-deletion model each deleted helper removes 8 rank-1 climbs, the most a mass-8 removal can
save. There the lower bound fails at d = 39 and the explicit hosting passes at d = 40. So 40 is sharp in the
stage-relaxed slot model, and d ≤ 39 fails for every pure-deletion word. Deltas that also merge other climbs belong
to lever (e); the [bit-deletion-ladder](../bit-deletion-ladder/README.md) (PR2465) notes that they can beat RANK1
at equal mass.

Linearity makes every budget sharp. f(a) = (1/(mW)) Σ n_r r (m/r)^a + c_s m^a with c_s = 32mN/(10¹⁶W) is affine in
the counts, so each one-parameter family is monotone and the boundary is a single integer.

## Second method

[independent.py](independent.py) rebuilds every boundary histogram from the pinned PR589 and #1094 records with its
own code, requires byte-identical histograms, and recomputes all **40 signs**: 16 bit rows and 4 complex rows, each
at c\* and at c\* + 10⁻²⁴. It uses the separate interval arithmetic of our merged
[bit-revision3-levers-seed03/levers.py](../bit-revision3-levers-seed03/levers.py) (PR1334): ln by atanh prime chains,
exp by Taylor with a remainder bound, outward dyadic rounding. It also re-checks the re-hosting order and the
trimming lemma. The primary [verify.py](verify.py) uses the D/E-diagnostic engine (PR1293, Navinor). The two
methods agree on every sign.

## Reproduce

From the repository root (standard library and `git`; about 15 s):

```sh
python3 -I -B research/bit-endpoint-lever-budgets/verify.py && python3 -I -B research/bit-endpoint-lever-budgets/independent.py
```

Expected output:

```text
PASS_BIT_ENDPOINT_LEVER_BUDGETS need_rank1=649 admitted_levers_max_net=0 copies_sharp=93 deletions_per_call=RANK1:40/TEMPLATE:None ideal_shape_calls=52 no_new_kappa
PASS_BIT_ENDPOINT_LEVER_BUDGETS_INDEPENDENT signs=40 at c* and c*+1e-24 (levers.py interval arithmetic)
```

`verify.py` regenerates [RESULT.json](RESULT.json) and requires byte equality (`--write` rewrites it). It refuses
to run under `-O`.

**Controls in `verify.py`:**
- its bill equals the pinned engine's on the record;
- the selected bit endpoint is accepted and its next grid point rejected;
- the selected κ is recomputed;
- c\* is the least grid point with κ ≥ 1.1× selected (and c\* − 10⁻²⁴ is not);
- the record fails at c\*;
- the 649/648 rank-1 and 16 rank-42 requirements are re-derived.

**Negative controls that must fail:** every "one less" boundary row (648 rank-1, 92 copies, 39 deletions,
51 reshaped calls) and every "one more" overhead row. [test_package.py](test_package.py) checks that tampering is
rejected by the independent method:
- off-by-one counts;
- a flipped verdict;
- an edited histogram;
- an edited complex verdict.

```sh
python3 -I -B -m unittest discover -s research/bit-endpoint-lever-budgets -p test_package.py
```

## Scope, inherited assumptions and unresolved obligations

- **Inherited:**
  - the fixed-histogram bill and surcharge law of the selected record;
  - the coverage identity D = T(2Kv − L·cst) at fixed m, W;
  - PR1791's endpoint model, with the complex side at 3/1000 under two-call sharing;
  - the PR589 H1–H5, all-size/compiler, precision and analytic obligations, unchanged.
- **Scope of each row:**
  - (a) and (a′) hold for the PR589 nine-stage windows and width-8 helpers. (a′) also holds with stage windows
    relaxed. No banks are used.
  - (b2), (b3), (c), (d) and (e) are pricing passes for hypothetical words or decoders.
    - (d)'s d = 40 pass is in the stage-relaxed slot model; its d ≤ 39 fail holds for every hosting.
    - (e) is the in-window ideal relaxation of PR1334, applied call by call.
- **Unpaid obligations of every passing row:** the word or decoder itself, then:
  - the dirty-input endpoint and restoration;
  - hosting under the real stage windows;
  - the row-coefficient invoice;
  - the recomputed surcharge (included here);
  - the native precision/tape;
  - admission.

  For (b3) add the bit analogue of PR1748's ownership/sink blocker. Overhead that changes the windows, the coverage
  law or the outer recipe is outside the model.
- Run on Linux with CPython 3.14.4. The registered replay
  (`python3.12 scripts/research_package.py --package research/bit-endpoint-lever-budgets`) also passed with CPython
  3.12.15: `PASS_REGISTERED_RESEARCH_PACKAGE`.

## Open next questions

1. **Can the bit centre path be shared by two calls within ≈ 29 units of overhead per call?**
   - *Why it matters:* it is the only catalogued route on which centre sharing reaches +10%. The complex half must
     also stay within ≈ 28.3 units per call at c\*.
   - *First step:* write the bit analogue of PR1748's two-call reverse phase for the nine rank-7 copies of one
     replica, and price its restoration/hosting children.
   - *Blocked by:* no bit sharing word exists, and PR1748's ownership/sink blocker has no bit analogue yet.
2. **Is there a decoder contract with eight retained totals (cst ≤ 56)?**
   - *Why it matters:* one fewer copy per call nets ≈ 2,009 units, 3.1× the requirement.
   - *First step:* test whether one of the nine retained totals of the v = 111 word can be recomputed instead of
     copied, and price the extra climbs.
   - *Blocked by:* a replacement contract for the decoder's copied totals (the `centre-path-sharing` card's
     scope-change trigger).
3. **Which bit word reaches the 52-call reshaping or the 40-deletion size?**
   - *Why it matters:* these are the non-sharing alternatives.
   - *First step:* measure the best per-call delta of PR1043-style deletions combined with climb merges.
   - *Blocked by:* PR1250 found only one removable helper in the fixed word.

## Credit and provenance

- **Requirement, endpoint and sharp-removal method:** rtyu193-rgb, `centre-sharing-overhead-budget` (PR1791, head
  `00d05a648985`).
- **Moment enclosures:** Navinor, `selected-suppliers-de-diagnostic` (PR1293, head `85a361233431`).
- **Bootstrap/outer formulas:** Wronskode, `frontier1042-invoice-audit-seed81`.
- **Independent arithmetic:** our merged `bit-revision3-levers-seed03` (PR1334, head `5ad74a4a04d1`).
- **Re-hosting optimality at the selected endpoint and the slot model:** our merged `bit589-width-packing` (#1023).
- **Deletion models:** our merged `bit-deletion-ladder` (PR2465, head `9494fc4e2ecd`), from Ali Romman's PR1043 delta.
- **Recipe class:** ianlibanio, `bit589-recipe-floor` (PR1487).
- **Halving-depth admission:** the r740 elementary-cover row bound authors.
- **Bit supplier:** DreamingOfClouds (PR589) and eumemic (PR555), with the PR510/PR463/PR442 template and hosting
  lineage.
- **Selected construction:** Rohan Arun (#1094).

All are loaded unchanged as pinned Git blobs. Predecessor code is reused without modification.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5). The
question was scoped, and the code and prose written, in one session of an automated research loop. Before submission
it is checked only by AI review passes in the same loop; there is no independent human review. Apache-2.0.
