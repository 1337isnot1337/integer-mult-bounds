# Proof: priced width screen for the staged544 fixed-T360 ideal

All numbers are printed by `verify.py`. Units are per owner replica; one
"helper-call" is one helper in one of the nine calls.

## 1. Model and sign lemma

Inventory per replica (PR3734 head `fa041037`, PR3815 head `77ffbf28`): `9 s_w`
helper-calls of hosted width `w`, with `s = {4:26,5:2,6:18,7:53,8:96,9:213}`;
idle bins `B = {8:672,16:448,32:448,48:448}`; local per-call profile
`n = {1:2440,2:725,3:224,4:102,5:20,8:8}`; 896 live rank-73 families. A
packing puts each helper-call into one bin; a bin pattern `p` (counts `p_w`) of
capacity `c` leaves `l_p = c - sum_w w p_w >= 0`, paid as one rank-`l_p` child
when `l_p > 0`. With `h(l) = l^(1-a)` and `h(0) = 0`,

`F(a) = 9 sum_r n_r h(r) + sum_p y_p h(l_p) - 896 h(73)`.

As in PR3815, `F(a) = 73^(-a) (sum n_r r (73/r)^a - 65408)` and every paid rank
is below 73, so `F` has one root and "root < a" iff `F(a) > 0`. This holds for
every inventory and local profile below (all paid ranks stay at most 48), for
integer or fractional `y`, and for any clock: the clock only restricts `y`.

`V(s', a) = min sum_p y_p h(l_p)` over `y >= 0` with `sum_p y_p p_w = 9 s'_w`
for every width and `sum_{p in c} y_p = B_c`. The ideal ceiling of an
inventory `s'` and profile `n'` is the root of
`9 sum n'_r h(r) + V(s', a) - 896 h(73)`.

`h` is enclosed outwardly (`h_lo <= h <= h_hi`, width below 1e-85): `ln l`
from the `atanh` series with a geometric tail bound, `exp(-u)` from alternating
partial sums, and outward rounding to 1e-90.

## 2. Staged544 ceiling bracket

The ten patterns found by HiGHS equal PR3815's basis. Their exact primal is
`y >= 0`; the smallest entry is 7. With `h_hi`, `F(a_lo) <= -1.31e-19` at
`a_lo = 0.001730578437266246818740`. Solving the same basis for `(pi, mu)` with
`h_lo` at `a_hi = 0.001730578437266246818741` gives `F(a_hi) >= 5.28e-20`.
This reproduces PR3815's bracket with an independent enclosure. It is not a
new result.

## 3. Theorem (weak duality with monotone prices)

Let `pi_w` (w = 1..9) and `mu_c` satisfy

(D) `sum_w pi_w p_w + mu_c <= h_lo(l_p)` for **every** pattern of widths 1..9
in every bin (318,840 patterns).

Then for any inventory `s'` over widths 1..9 (fractional or not) and any
local profile `n'`, every packing satisfies

`F'(a_hi) >= 9 sum_r n'_r h_lo(r) + 9 sum_w pi_w s'_w + sum_c mu_c B_c - 896 h_hi(73).`   (*)

Proof: multiply (D) by `y_p >= 0`, sum, and use the two equality constraints.

**Reductions.** Let `s'` arise from `s` by moving `z_{w->v} >= 0`
helper-calls from width `w` to any `v < w` (`v >= 1`). The right side of (*)
equals the staged544 bound plus `sum z_{w->v} (pi_v - pi_w)` plus
`9 sum (n'_r - n_r) h_lo(r)`. If `pi` is nonincreasing in width, every
reduction term is nonnegative.

`verify.py` takes `pi_4..pi_9` and `mu` from the basis. It sets `pi_1, pi_2,
pi_3` to the largest values that keep (D) feasible, maximizing `pi_3` first
(with `pi_1 = pi_2 = pi_3`), then `pi_2`, then `pi_1`. It then checks the
following:

- (D) holds on all 318,840 patterns. The minimum reduced cost is exactly 0.
  An unbounded-knapsack recursion over used volume gives the same minimum.
- `pi_1 >= pi_2 >= ... >= pi_9`, and every `pi_w <= 0`. Hence unhosting a
  helper (width 0) is also never improving.
- the staged544 bound is `F(a_hi) >= 5.28e-20 > 0`.

**Corollary (free reductions).** If the local profile is unchanged, no reduction
of any hosted widths raises the ideal ceiling above `a_hi`. This covers any
amount, any widths and widths down to 1 or unhosting, at zero entrance cost.
Each reduction unit costs at least `pi_v - pi_w` in `F`:

| move | exact price at a_hi | range on the basis (helper-calls) |
|---|---|---|
| 9->8, 8->7, 7->6, 6->5 | 0.987736781185353068089966 | 28, 30, 28, 28 |
| 5->4 | 1 (exactly: `[9,9,9,5]` and `[9,9,9,4]` are both basic) | 18 |
| 4->3 | >= 0.991791369039984911721564 (dual bound) | n/a |

The value `V` is convex in the right-hand side, so a price is a lower bound for
every further unit in that direction. Inside the listed range the same basis
stays primal-feasible, and the price is the exact change. HiGHS gives
0.9877367811860, 1.0 and 0.9917913690369 for single units of 8->7, 5->4
and 4->3. The 4->3 dual bound is therefore attained to about 3e-12 in floating
point; exact attainment is not claimed.

**Why monotonicity is not automatic.** A narrower helper fits gaps that wider
ones cannot. The limiting patterns of the tight extension are exact fills:
`48 = 3 + 5*9` limits `pi_3`, `48 = 2 + 5*9` (leftover 1) limits `pi_2`, and
`32 = 1 + 4 + 3*9` limits `pi_1`. So the width-4..9 dual (2,551 patterns) does
not by itself give a monotone feasible extension. The control
`granularity_raised_pi3_infeasible_on_1_to_9` raises `pi_1..pi_3` by 1e-30 above
the tight value. The prices stay monotone and feasible on all 2,551 width-4..9
patterns, but some width-1..9 pattern becomes infeasible.

## 4. Paid-rank identity and what the corollary does not cover

On three pinned T360 profiles, `sum_r n_r r = (896*73 - 320) T = 23,431,680`:

- PR3682's finite profile (LEAD1-PRICE.json);
- PR3734's finite profile (inputs/PROFILE.json);
- PR3815's clock fill (inputs/PROFILE.json).

The identity was observed on these three profiles; it is not proved here. If it
holds for every literal construction of this template, a free reduction is
not realizable. It adds `w - v` units of paid leftover with no offsetting local
change. A real staging move must then remove `w - v` units of local paid rank.
PR3734's change does exactly this: width 8->7 together with local
`{1:+3, 2:+1, 3:-2}`, a rank-sum change of -1 per call. So the corollary in
section 3 is **not** an upper relaxation of real staging. The correct screen is (*)
with the actual `n'`.

**Staging screen.** Suppose one unit `w -> w-1` is paid by removing one unit
from a single local child (`r -> r-1`). That saves `h(r) - h(r-1) <= h(1) = 1`
by concavity, with equality when a rank-1 child is deleted. By (*), the change
in `F` is at least `price - 1`. The ceiling can therefore rise only if the
price is below 1:

- w in {6..9}: gain at most 0.012263218814646931910033 per helper-call. This is
  exact within the ranges above for a rank-1 deletion.
- w = 5: gain at most 0. Single-child-compensated 5->4 staging never raises
  the ceiling, in any amount.
- w = 4: gain at most 0.008208630960015088278435.

Local rewrites that also merge or split children are priced exactly by
`9 sum (n'_r - n_r) h(r)` in (*). They are a separate local-word lever.

## 5. PR3682 -> staged544 decomposition (exact at a_hi)

All four corners have the same optimal basis. Each primal is `y >= 0` with
dual feasibility on 2,551 patterns, and each enclosure gap is below 1e-70.
Because `(pi, mu)` depends only on `a`, the interaction term is exactly 0. The
four corners are PR3682 (inventory `{...,7:52,8:97,...}`, local
`{1:2437,2:724,3:226,...}`), width-only, local-only and staged544:

- width part (one 8->7 per call): +8.889631030668177612809695088162
  = 9 x 0.987736781185353068089966...;
- local part: -8.919009734220261337601597266358, a saving of
  0.991001081580029037511288 per call;
- total -0.029378703552083724791902178195, or 0.003264300394675969421322
  per call.

Under the identity neither single change is realizable. The width-only change
moves the ideal root down to about 0.0016821 and the local-only change moves it
up to about 0.0017788 (HiGHS, float). PR3734's gain is the margin of its local
saving over the exact width-unit price. Against the single-child reference, its
local change gives up 0.008998918419970962488711 per call to reshaping:
`{1:+4,2:+1,3:-2}` has zero rank change and a positive cost. That is about 73%
of the 0.012263 available.

## 6. Scope

This is a clock-free, fractional relaxation with fixed idle bins. Sections 3 and 4
are exact statements about it. Template, stock and clock (chronological)
effects are not modeled. The paid-rank identity is observed, not derived. The
first-order conversion `dF/da ~ 184132` is floating point. No kappa,
supplier or admission claim is made.
