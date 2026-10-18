# Staged544 width-lever screen: exact width prices for the fixed-T360 ideal

**Scoped exact result about the clock-free fixed-bin ideal. It makes no kappa
claim, is not a construction and is not a complete multiplication theorem.**

## Statement

The model is PR3815's fixed-inventory ideal of the staged544 T360 template
(PR3734). Per owner replica there are 9 calls of 408 helpers with hosted widths
`{4:26,5:2,6:18,7:53,8:96,9:213}`, idle bins `{8:672,16:448,32:448,48:448}`,
local profile `{1:2440,2:725,3:224,4:102,5:20,8:8}` and 896 live rank-73
families. Packings may be fractional and any clock is allowed. Details are in
[PROOF.md](PROOF.md).

1. **Priced screen (exact, proved).** One dual `(pi, mu)` is feasible on **all
   318,840** bin patterns with widths 1..9, with exact minimum reduced cost 0.
   Its helper prices are nonincreasing in width and nonpositive. By weak
   duality, every changed inventory `s'` over widths 1..9 with these bins and
   any changed local profile `n'` satisfies

   `F(a_hi) >= 9 sum n'_r h(r) + 9 sum pi_w s'_w + sum mu_c B_c - 896 h(73)`   (*)

   at `a_hi = 0.001730578437266246818741`. The staged544 inventory gives
   `F(a_hi) >= 5.28e-20 > 0`.
2. **Theorem (free reductions; proved negative result).** No reduction of the
   hosted widths of any helpers, by any amount and down to width 1 or
   unhosting, at zero entrance cost, raises the ideal ceiling above
   `0.001730578437266246818741`. This holds when the local profile is
   unchanged. The ceiling itself lies in
   `[0.001730578437266246818740, 0.001730578437266246818741]`, which
   reproduces PR3815.
3. **Exact width-unit prices** in `F` units per helper-call, at `a_hi`:

   | move | price | exact range on the basis |
   |---|---|---|
   | 9->8, 8->7, 7->6, 6->5 | 0.987736781185353068089966 | 28 / 30 / 28 / 28 helper-calls |
   | 5->4 | 1 exactly | 18 |
   | 4->3 | >= 0.991791369039984911721564 | not established (HiGHS attains it to 3e-12) |

   By convexity each price is a lower bound for every further unit.
4. **Theorem 2 does not bound real staging.** The paid rank sum is the same on
   all three pinned T360 profiles: PR3682 finite, PR3734 finite and PR3815 clock
   fill all give `sum n_r r = 23,431,680 = (896*73 - 320)*360`. This identity
   is observed, not proved. Where it holds, a free reduction is not realizable.
   A literal staging unit must remove one unit of local paid rank, which saves
   up to `h(1) = 1`. With such single-child compensation, a unit can gain at most:
   - **0.012263218814646931910033** per helper-call for widths 6..9. This is
     exact within the ranges above when the compensation deletes a rank-1 child.
   - **0** for 5->4. Single-child-compensated 5->4 staging never raises the
     ceiling, in any amount.
   - **0.008208630960015088278435** for 4->3.
5. **PR3682 -> staged544, exact at `a_hi`.** All four corners share one optimal
   basis, so the interaction term is exactly 0.
   - Width part (one 8->7 per call): `+8.889631030668177612809695088162`.
   - Local part: `-8.919009734220261337601597266358`, a saving of
     0.991001081580029037511288 per call.
   - Net: `-0.029378703552083724791902178195`.

   Neither single change is realizable under the identity. Width-only moves
   the ideal root to about 0.0016821 and local-only to about 0.0017788 (HiGHS,
   float). PR3734's ideal gain of 0.003264300394675969421322 per call is the
   margin of its local saving over the exact price. Its local change gives up
   0.008998918419970962488711 per call (about 73% of the 0.012263 available)
   to reshaping: `{1:+4,2:+1,3:-2}` has zero rank change and a positive cost.

To first order, `dF/da ~ 184132` at the ceiling (floating point). Staging one
more width-6..9 helper in all nine calls with rank-1-deletion compensation would
raise the ideal ceiling by about 6.0e-7. PR3734 realized about 1.6e-7.

## Decision informed

This informs expansion-gate point 4 for the staged-entrance family (#3606), the
engine of #3605 and #3734. It also partly answers PR3815's open question 1.

- Free width reduction is not a lever.
- 5->4 staging is closed under single-child compensation.
- Staging width-6..9 (and 4->3) helpers remains open in the ideal. The test for
  a candidate is now one exact inequality: its local saving must exceed the
  price above.
- The cheapest identified improvement is to avoid PR3734-type reshaping (up to
  0.008999 per call).
- Bin changes are priced by `mu`. The local word is priced by `h(r)`.

## Reproduce

```
python3.12 -B scripts/research_package.py --package research/staged544-width-lever-screen
```

The verifier is standard-library only and runs in about 6 s. It can also be run
directly as `python3 -B research/staged544-width-lever-screen/verify.py`. The
expected last line is `PASS_STAGED544_WIDTH_LEVER_SCREEN`, preceded by a JSON
report with every number above. The output was identical under Python 3.12.15
and 3.14.4.

**Negative controls (each must fail; the verifier asserts they do):**

- `pi_9 + 1e-30` makes the dual infeasible.
- `granularity_raised_pi3_infeasible_on_1_to_9`: raising `pi_1..pi_3` 1e-30
  above the tight extension leaves the prices monotone and feasible on the
  2,551 width-4..9 patterns, but infeasible on widths 1..9. This is why the
  318,840-pattern check is needed.
- A non-monotone extension is rejected.
- The dual bound at `a_lo` is not positive.
- One 8->9 widening per call drops the bound to `<= 0` (widening is priced as a
  gain).
- A +1 change to a profile breaks the paid-rank identity.

**Second, independent method (floating point):** `crosscheck_highs.py` used
Python 3.14.4, numpy 2.5.4 and scipy 1.18.1 HiGHS. It generates patterns as
integer partitions, uses explicit reduction columns instead of dual
monotonicity, and bisects the root. Its recorded output is
`evidence/HIGHS.json`:

- Fixed staged544 root 0.0017305784372662612.
- Free reductions over 318,840 patterns: 0.0017305784372661503. This is not
  higher; the 1.1e-16 difference is float noise.
- The stage-move variant matches the fixed root.
- PR3682 ideal root 0.0017304188997660508.
- Single-unit prices 0.9877367811860 (8->7), 1.0 (5->4) and 0.9917913690369 (4->3).

It is not part of the registered replay.

## What is new

PR3815 certified the fixed staged544 inventory on 2,551 patterns. The
async505 inventory wall, PR3630 and PR3638 priced other inventories with fixed
widths. The following are new here:

- the dual extension to all widths 1..9 with monotone prices;
- the general priced screen (*);
- exact width-unit prices and their ranges;
- the single-child staging bounds;
- the observed paid-rank identity and its consequence that free reductions do
  not bound real staging (this corrects the premise of this package's task card);
- the exact PR3682 -> staged544 decomposition.

## Sources

The base is canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`. The
inputs are numbers transcribed into `verify.py` and `CERTIFICATE.json` from
unmerged PR heads. These heads are not reachable from main, so they are recorded
here by sha256 and not as `SOURCES.json` pins. The verifier cannot byte-check
them. This is a stated gap.

| PR | head | file | sha256 |
|---|---|---|---|
| #3734 (dataisfire) | `fa041037a3374eaa08feeca0b26a5d6893194147` | `research/staged544-producer-return/PROOF.md` (inventory, local profile) | `be5fa8e381da957d52d02b154e2420f4459d7c8b30e23e82e245c11c978e3b62` |
| #3734 | same | `research/staged544-producer-return/inputs/PROFILE.json` | `06b4e2abe8d56b49bad3bdc8f8504082404b40609d548fa8de2618eb7373fd48` |
| #3815 (ChaloupeMusic) | `77ffbf287b6ca198b4a31e3835db3bae60718b93` | `research/staged544-clock-ceiling/ceiling_certificate.py` (model, bins, bracket) | `2276f1c5d341db63dcf511f6398733b1efbe9d09e2e9aa86b50d7a160a0f7d03` |
| #3815 | same | `research/staged544-clock-ceiling/inputs/PROFILE.json` | `9686df0d8e710c2e94aef3887f4bf130a05b64215faeae702cccb59e95a469d5` |
| #3682 (zxv) | `431e6c6023ef352c41696469de7fb614cd4ded8c` | `research/staged-donor-release/PROOF.md` (inventory, local profile) | `89ce2b0aa2dcf84ebcab04aedc451420815bc48af25c69998594910e9976a31b` |
| #3682 | same | `research/staged-donor-release/LEAD1-PRICE.json` (finite profile) | `217dfc6b0c243d5387f50b23d0a5a389754df702ea1d810aea46a6f3d81617bc` |

## Scope, inherited assumptions and unresolved obligations

- **Model.** This is the clock-free fractional ideal with fixed idle bins and
  PR3815's payment rule (one rank-`l` child per remainder). Template, stock and
  clock effects are out of scope. PR3815 traced PR3734's shortfall from its
  ideal to the clock.
- **Paid-rank identity.** It was observed on three pinned profiles and is not
  derived. The statements in item 4 that depend on it are conditional on it.
- **Admission costs not priced.** All admission costs of a changed inventory are
  unknown and are not zero. These include physical stock, coverage law and
  template checks, literal staging identities and clock feasibility.
- **Ranges.** Exact prices hold within the stated ranges of one basis. Outside
  them they are lower bounds. The 4->3 value is a lower bound only.
- **Floating-point values.** `dF/da`, the ceiling conversions and the HiGHS
  values are floating point.
- **No kappa.** No kappa, frontier or selected-result change is claimed.

## Open next questions

- **Does the paid-rank identity `sum n_r r = 65088 T` hold for every literal
  construction of this template?** If it does, items 4 and 5 become
  unconditional. First step: derive it from the owner and frame accounting in
  PR3734's `owner_audit.py`, or find a construction that violates it.
- **Can a width-6..9 helper be staged with rank-1-deletion compensation and no
  reshaping?** Each such helper is worth up to 0.110369 in `F` (about 6e-7 of
  ceiling) within the ranges. First step: list PR3734's helpers with a rank-1
  entrance and price their literal staging local deltas with the screen (*).
- **What does the template lever (bins) offer?** `mu` gives exact bin prices
  (`mu_48 = 47.679502755263063473958379`). First step: write a candidate
  template's bin counts and evaluate the screen (*). Re-solve the LP for changes
  outside the basis ranges.

## Credit

The model, bins, payment rule and basis are from PR3815 (ChaloupeMusic, head
`77ffbf28`). The staged544 inventory and local profile are from PR3734
(dataisfire, head `fa041037`). The predecessor inventory is from PR3682 (zxv,
head `431e6c60`). The staged-entrance mechanism is from PR3605 (RossRichardson),
with lineage through PR3795/PR3802 (hexapode). The width-price method follows
`research/experiment-log/negative-searches/async505-inventory-wall` (Rohan
Arun), PR3630 (RossRichardson) and PR3638 (zxv).
No predecessor code is copied. `verify.py`'s enclosures, enumeration, knapsack
check and LP algebra are new.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). Checked by AI review passes in the same
loop. No human or formal-kernel verification is claimed. Apache-2.0.
