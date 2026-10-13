# Coverage-law relief thresholds for the selected complex local word

**Scoped obstruction and exact threshold table under the optimistic relaxation.
No new kappa, no supplier admission; the selected record is unchanged.**

## Scope

Card `complex-new-helper-inventory` (complex-mechanisms track, chooser nonce
`6ddf1b6647d8c5131033b16d30f0045b`), scope **refined** to the card's first
experiment: the complete optimistic child histogram, used to reject interface
routes without headroom. The card asks for a new physically realizable helper
inventory; this package instead quantifies the screen itself on **changed
coverage-law interfaces**, answering the coverage-law half of
https://github.com/CrocSwap/integer-mult-bounds/pull/1240's open question. The
full task card is in [TASK-CARD.md](TASK-CARD.md); structured scope metadata is
in [TASK.json](TASK.json).

## Model and object

The hosted nine-stage coverage law of the selected line (semantics follow
CrocSwap/integer-mult-bounds#1012's coverage identity and
CrocSwap/integer-mult-bounds#1240's moment model; the arithmetic here is
written independently):

- width `m = 73`; per call `w = families/stages = 896/9` live data families;
- coverage identity: paid rank mass + idle mass = `(m − unpaid)·w + centre`
  (selected line: `unpaid = 1`, `centre = 64`); deficit `D = unpaid·w − centre`;
- the selected CrocSwap/integer-mult-bounds#1094 local word per call is
  `{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}` (paid mass 5586), recorded at
  `research/gauge44-slots-t16/README.md`;
- idle/remainder children have rank at most `R = 51` (halving guard `m² > 2R²`);
  the optimistic relaxation allows fractional counts and puts all idle mass at `R`.

Total mass per call is 7232 (idle 1646), reproduced exactly. The relaxation
moment `relax(a)` is increasing in the saving `a`; the packing ceiling `a*`
solves `relax(a*) = 1`. A failing relaxation (moment above one at a target)
falsifies **every** construction with those interface parameters; a passing one
is optimistic only.

Two targets:

- **T1 (headline):** `a = 1/99`, equivalently `κ = 0.01` under the retained
  transfer `κ = a/(1+a)`.
- **T2 (unbinding):** `a = κ_bit/(1 − κ_bit)` with `κ_bit =
  1733427039589844234749/10^24`, the bit saving pinned by
  `scripts/research_baseline.py` at the base commit. This is where the complex
  side would stop binding over that bit supplier. The incumbent ceiling
  `a* = 0.001690054109088696` (κ ≈ 0.00168720) is below T2, so **pure repacking
  of the selected word cannot unbind the complex side**; an interface change is
  required even for the near target.

## Results (all brackets certified with exact rational intervals)

Positive control: `a* = 0.001690054109088696` reproduces
https://github.com/CrocSwap/integer-mult-bounds/pull/1240's grid ceiling
`a < 0.001690054109089` to within one 1e-15 grid step.

| Lever (others at the selected line) | T2: unbinding (`a = 0.001736437026484097`) | T1: `a = 1/99` |
|---|---|---|
| unpaid coordinates per family `u` | `u* ∈ (1.009826689, 1.009826689)`; least integer 2 | `u* ∈ (2.804078009, 2.804078010)`; least integer 3 |
| centre charge `c` (from 64) | `c* ∈ (63.021698514, 63.021698515)`: met iff `c ≤ c*` | **impossible**: sup `a* = 0.004711142955614` at `c = 0` |
| families per replica `F` (stages 9) | least met `F = 906` (905 fails) | least met `F = 3093` (3092 fails) |
| paid-word count scale `s` | met iff `s ≤ 0.969437086` | met iff `s ≤ 0.049110034` |

Pair points at `F = 896`:

- `(u=2, c=0)`: `a* = 0.009357801683738 < 1/99`. So unpaid relief up to 2
  combined with **any** centre charge fails T1 (the sup over `c ∈ [0, 64]` is at
  `c = 0`; `relax` is strictly decreasing in `u` and strictly increasing in `c`).
- `(u=3, c=64)`: `a* = 0.011001994530886 > 1/99`. Keeping three unpaid
  coordinates per family optimistically suffices at the unchanged centre charge.

Reading the T1 column as an interface budget: the headline target needs one of
three large changes — every live family keeping at least 2.804 unpaid
coordinates (integer 3 at `c = 64`), or a 3.45× larger template (3093 families
per replica at 9 stages), or a paid word at most 4.911% of its current counts
(a 95.1% reduction, consistent with CrocSwap/integer-mult-bounds#1240's
independently derived "about 95% lower fully priced local excess spend").
Centre-charge relief alone cannot reach T1 at any `c ≥ 0`. T2 is much nearer:
about 1% more unpaid coordinates, or one unit off the 64 centre charge, or 906
families, or a 3.06% paid-count cut.

## D/E diagnostic

`a* < D/E` holds strictly (convexity: `(r/m)^(1-a) ≥ (r/m)(1 + a ln(m/r))`),
checked at four points:

| Point | `D` | `E = Σ n_r r ln(m/r)` | `D/E` | `a*` |
|---|---|---|---|---|
| incumbent | `320/9` | `20973.176117977` | 0.001695287130359 | 0.001690054109089 |
| `u=2, c=0` | `1792/9` | `20914.519566200` | 0.009520233562185 | 0.009357801683738 |
| `u=3, c=64` | `704/3` | `20901.768141900` | 0.011227120360035 | 0.011001994530886 |
| `c=0` | `896/9` | `20950.223554238` | 0.004752004449872 | 0.004711142955614 |

The diagnostic tracks the exact ceiling within 0.4% here, but the exact moment
is the acceptance test.

## What this does and does not establish

- Necessity holds inside the stated model: any construction on this local word,
  template and outer recipe whose interface parameters miss every threshold
  fails the moment, however it packs, hosts or repacks.
- Sufficiency is **optimistic-relaxation only**: fractional idle, all idle at the
  cheapest admissible rank, no added charges. No physical realizability, owner
  map, finite invoice or cold replay is claimed. The card's acceptance gate (a
  new physically realizable contract) is **not** met by this package.
- The `u`, `c` and pair thresholds are at `F = 896` families; the `F` and `s`
  thresholds are at the selected `u = 1, c = 64`. Changing several levers at once
  can meet a target below each single-lever threshold (see open questions).
- `u > 1` and any `c ≠ 64` are what-if coverage laws.
  CrocSwap/integer-mult-bounds#1012's identity is re-checked only at the
  selected point; a realized `u ≥ 3` would itself be a changed interface
  contract needing its own admission.
- `κ = a/(1+a)` is the retained planning transfer, not a theorem; T2 uses the
  bit supplier pinned at the base commit, and any bit-side improvement moves it.
- All inherited all-size/compiler, common-label/mutable-source, whole-call
  hosting, precision/tape, analytic-transfer and bit H1–H5 assumptions remain.
  This is not a full Lean multiplication theorem.

## Boundary with existing work

- https://github.com/CrocSwap/integer-mult-bounds/pull/1240 (Douglas Colkitt)
  derives the coverage-law moment model and the fixed-word packing ceiling, and
  names the coverage-law change as open. This package answers that question with
  independently written, code-disjoint exact interval arithmetic; its `unpaid`
  what-if parameter is used here as a search lever.
- The pending stacked branches of
  https://github.com/CrocSwap/integer-mult-bounds/pull/1240 and
  https://github.com/CrocSwap/integer-mult-bounds/pull/1272 carry a `levers.py`
  ideal-budget table (first-order multiples per lever) that
  CrocSwap/integer-mult-bounds#1272's proposed `centre-path-sharing` and
  `coverage-law-change` cards cite. This package is complementary: it certifies
  exact threshold brackets (not first-order multiples) at two targets, adds the
  families and paid-word-scaling levers, least-integer thresholds, the
  `(u=2, c=0)` pair obstruction and the `a* < D/E` convexity margins, and ships
  as a package on the base commit.
- https://github.com/CrocSwap/integer-mult-bounds/pull/1264 screens 14 open
  claims at the **unchanged** coverage law; nothing there varies the interface.
- https://github.com/CrocSwap/integer-mult-bounds/pull/1272 (pending) narrows
  this card with a ceiling screen; this package is that screen applied to
  changed interfaces.
- Ali Romman's `research/heterogeneous-owner-assembly/` bounds every mixture of
  the frozen catalogue's 25 cost interfaces and explicitly excludes new
  helper-inventory interfaces such as the R489/R480 interfaces of
  CrocSwap/integer-mult-bounds#1004 and CrocSwap/integer-mult-bounds#1005. The
  thresholds here price what such a new interface would have to deliver.
- Distinct from
  https://github.com/CrocSwap/integer-mult-bounds/discussions/1265 (within-group
  idle repartitions at a fixed coverage law) and
  https://github.com/CrocSwap/integer-mult-bounds/discussions/1315 (X2
  acceptance boundary for the selected owner map).

## Reproduce

Python 3.11+, standard library only, from the repository root:

```sh
python3 -I -B research/complex-coverage-law-relief/verify.py
python3 scripts/research_package.py --package research/complex-coverage-law-relief --check-only
python3.12 scripts/research_package.py --package research/complex-coverage-law-relief
```

Expected final line:

```text
PASS_COMPLEX_COVERAGE_LAW_RELIEF
```

Add `--out /new/file.json` for the complete certificate (model, targets, every
threshold bracket as exact fractions, pair points, D/E diagnostics, check log).
Failure controls: `unpaid = 0`, halving-guard `R = 52`, a negative centre charge
and an over-paid word are rejected; one extra rank-1 child lowers the ceiling;
nine extra families raise it.

## Open next questions

See [TASK.json](TASK.json) for the structured list:

1. **Can any physically realizable helper inventory move a lever past a
   threshold?** First step: map the R489/R480 interfaces of
   CrocSwap/integer-mult-bounds#1004 and CrocSwap/integer-mult-bounds#1005 onto
   `(u, c, F, s)` and price them here. Blocked on an admission proof that a
   known interface change corresponds to a coverage-identity change rather than
   a repacking.
2. **Thresholds for the CrocSwap/integer-mult-bounds#1148 joint-entrance words**
   (whose packing caps are 0.17–0.21% below the selected word's). First step:
   pin one joint-entrance profile from
   https://github.com/CrocSwap/integer-mult-bounds/pull/1264's `SNAPSHOT.json`
   and rerun the table. Blocked on the profile not being in the base tree.
3. **The exact combined `(u, c)` and `(F, s)` Pareto surface at 1/99.** First
   step: a certified 2D grid in `verify.py`; not blocked, cheap.

## Credit

Contributor: **Navinor**, with help from opencode. Apache-2.0.

Predecessors: CrocSwap/integer-mult-bounds#1012's coverage identity;
https://github.com/CrocSwap/integer-mult-bounds/pull/1240 and
https://github.com/CrocSwap/integer-mult-bounds/pull/1264 (Douglas Colkitt) for
the moment model, the fixed-word ceiling and the open question; the selected
local word and its lineage (see `certificates/selected-result.json` and
`research/gauge44-slots-t16/README.md`); Ali Romman's
`research/heterogeneous-owner-assembly/` for the frozen-catalogue boundary. All
construction credit for the selected line stays with the authors listed in the
selected record's review. No human review or full formal verification is claimed
for this package.
