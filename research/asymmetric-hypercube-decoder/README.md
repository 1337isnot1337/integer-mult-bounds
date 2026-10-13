# Asymmetric stars do not evade the hypercube parity obstruction

**Scoped negative result; no new κ.** The symmetric-coefficient result in
[PR #231](https://github.com/CrocSwap/integer-mult-bounds/pull/231), by
Joel Pulikkan / GamingPuzzled, extends to arbitrary target-dependent coefficients
on **all stars of degree less than k, including off-target stars**. For the
smaller target-local star family, the exact minimum number of deleted ports
needed to decode one retained target at a power-of-two k is **2(p − k) + 1**.

The first result closes an algebraic escape route: asymmetric reweighting or
off-target proper stars cannot rescue an unpunctured 4- or 8-dimensional paired
hypercube decoder. The second quantifies how fragile that obstruction can be
under puncturing, without claiming a construction for all remaining targets.

## Model and predecessor

Let p ≥ k ≥ 2. The coordinates are p disjoint pairs. A port is a k-element set
containing one coordinate from each of k distinct pairs. Write P for all
2^k binom(p,k) ports. The independent input symbols x_S take values in F₂.
For a surviving family F ⊆ P containing a fixed target T, define

```text
star_L(F) = sum_{S in F, L subset S} x_S
C_j(T,F) = sum_{S in F, |S intersect T| = j} x_S.
```

All sums and coefficients below are in F₂. A global proper-star decoder has
the form

```text
x_T = sum_{L: 0 < |L| < k} a_(T,L) star_L(F)
      + sum_{j=1}^{k-1} b_(T,j) C_j(T,F).                 (1)
```

Here L may use any coordinates; sets containing both coordinates of a pair
give a zero star and can be omitted. Coefficients may depend independently on
T and L. Within each correction C_j, the same coefficient applies to every
source of that intersection size. The target-local family additionally
requires L ⊂ T. Degree-k stars and the j=0 and j=k correction classes are
excluded. A degree-k star would directly supply x_T; the j=k correction would
do the same. Allowing an empty-set star does not change the unpunctured
obstruction below.

[The retained #231 note](../hypercube-decoder-parity/README.md) restricts to
target-local stars with a_(T,L) = a_|L| and establishes existence exactly when
k is not a power of two. We retain that result and attribution. The new points
are the larger coefficient/support class in Theorem 1 and the sharp local
puncture threshold in Theorem 2. This is not a repeat of #231's coefficient
enumeration. Pending [#631](https://github.com/CrocSwap/integer-mult-bounds/pull/631)
studies E8 root-line punctures, a different port geometry.

## Theorem 1: arbitrary global proper stars, full port family

For F=P, a decoder of form (1) exists if and only if k is not a power of two.

**Necessity, without a symmetry assumption.** Fix T. Let Q_T be the 2^k ports
obtained by independently flipping the chosen coordinate in each of T's k
pairs. XOR the coefficient equations of (1) for all source ports S ∈ Q_T.

For a star_L with |L|<k, the number of such ports containing L is either zero
(if L uses an outside pair or incompatible coordinates) or 2^(k−|L|). Thus
every allowed star contributes zero to the summed equation. The same holds
for the empty star. The correction C_j contributes binom(k,j), since exactly
that many sign-flip ports intersect T in j coordinates.

If k is a power of two, every binom(k,j), 0<j<k, is even. The right side
therefore sums to zero, whereas the desired coefficient vector of x_T sums
to one: **0=1**. This is an explicit binary linear inconsistency certificate,
not an argument that averages coefficients over symmetries.

**Sufficiency, inherited from #231.** If k is not a power of two, choose
0<l<k with binom(k,l) odd. Set all local size-l star coefficients to one and
other star coefficients to zero; set b_(T,j)=binom(j,l) mod 2. For a source
with j<k intersections, the two coefficients cancel (and j=0 contributes
zero); at S=T the coefficient is binom(k,l)=1.

For completeness, the binomial parity criterion follows in F₂[z] from
(1+z)^k = product_{r: bit_r(k)=1}(1+z^(2^r)). With one set bit there are no
interior terms. With at least two set bits, the least set bit gives an odd
interior coefficient. The proof applies to every p≥k, not only checked sizes.

## Theorem 2: sharp puncture threshold for target-local stars

Let k≥2 be a power of two, p≥k, and retain a specified T. Restrict to
0<|L|<k with L⊂T in (1). The smallest possible deletion set D⊆P\{T} for
which T admits a decoder on F=P\D has size

```text
min |D| = 1 + 2(p-k).                                  (2)
```

Both stars and corrections are defined over the surviving family F. This
statement does **not** cover off-target stars after puncturing.

**Cell sizes.** For J⊂T, |J|=j<k, let P_J be the ports with S∩T=J. Put
d=k−j and q=p−k. To complete J to such a port, select a of the remaining d
target pairs (using their opposite coordinates), then d−a outside pairs,
with two signs each. With out-of-range binomial coefficients taken as zero,

```text
|P_J| = N_j = sum_{a=0}^d binom(d,a) binom(q,d-a) 2^(d-a)
            = sum_{u=0}^d binom(d,u) binom(q,u) 2^u.
```

For every nonempty proper J, d≥1. The u=0 and u=1 terms give
N_j≥1+2dq≥1+2q, with equality at j=k−1. Thus fewer than 1+2q deletions
leave at least one representative in every nonempty proper intersection cell.

**Why surviving cells force local symmetry.** For each such J, the coefficient
equation is

```text
sum_{empty != L subset J} a_(T,L) = b_(T,|J|).          (3)
```

Induction on |J| forces a_(T,J) to depend only on |J|: singletons all equal
b_(T,1); thereafter (3) expresses a_(T,J) as b_(T,|J|) plus the already
level-constant contributions of proper subsets of J. Write the resulting
coefficients a_l. The target coefficient must then be
sum_{l=1}^{k-1} binom(k,l)a_l=0, contradicting the required value one.
This proves the lower bound in (2). It also shows that any successful local
puncture must empty at least one entire nonempty proper intersection cell.

In fact, emptying **any** such cell P_J suffices for local decoding of T:
use the sum of star_L over J⊆L⊊T. Its source coefficient is one precisely
when S∩T is J or T. For J⊆K⊊T this follows from
sum_{J⊆L⊆K}1=2^(|K|−|J|); at K=T the excluded term L=T changes the parity
to one. With P_J deleted this is x_T. Thus the cell criterion characterizes
local feasibility; a smallest deletion set uses |J|=k−1.

**Sharpness.** Choose a fixed (k−1)-subset J⊂T and delete exactly P_J. These
are the 1+2(p−k) ports other than T that contain J. Among surviving ports,
star_J(F)=x_T. Use that single star with coefficient one and set every other
coefficient to zero. This attains (2).

For comparison, on the full family the same induction proves that all local
decoders are level-constant at each target. For a non-power-of-two k, the
k−1 level coefficients satisfy one nonzero binary equation, so there are
exactly 2^(k−2) local decoders per target. The correction coefficients are
then determined. This count does not apply to the larger global-star class.

## Verification

Run from the repository root, using only the Python 3.10+ standard library:

```sh
python3 -B research/asymmetric-hypercube-decoder/verify.py --negative-controls --write /tmp/asymmetric-hypercube.json
cmp research/asymmetric-hypercube-decoder/results.json /tmp/asymmetric-hypercube.json
```

The expected result is a PASS message and an identical deterministic receipt.
The committed receipt covers 9 compressed coefficient systems, 11 actual port
families, all 131,336 coefficient vectors in its three small cases, all 3,413
deletion sets in its four bounded puncture cases, and five negative-control
categories. Fresh runs on Python 3.11.13 and 3.14.5, including Python 3.14.5
with `-O`, produced identical receipts; no check relies on Python assertions.
The checker generates actual ports independently of the cell-count formula,
forms unrestricted target-local coefficient systems, and performs exact F₂
elimination. It also checks the global-star XOR certificate directly on
actual sign-flip cubes. Finite coverage and negative controls are enumerated
in [results.json](results.json); they support the written all-parameter proofs
above and are not a formal proof of the multiplication theorem.

The experiment domain and stopping rule are fixed by the verifier's case lists:
complete finite cases, no heuristic search or time-dependent stopping. Seed 48
selects the structural track and focuses on k=4 and k=8; the verifier records
its deterministic target choices. Source pins and the starting accepted
construction are in [SOURCES.json](SOURCES.json), with the sprint scope in
[CLAIM.json](CLAIM.json). Neither the selected certificate nor `upstream/` is
changed. The full supplier cold replay is outside this standalone decoder
result; no new supplier profile is asserted.

## Interpretation and limits

- For the full paired-port family at power-of-two k, arbitrary asymmetric
  proper-star preparation already fails at the scalar identity. Giving every
  helper, copy, source read, frame change, restoration and recursive child
  zero cost cannot repair that failure. There is therefore no positive
  complete-cost candidate to price or claim as a κ improvement here.
- The local puncture upper bound decodes only one specified target. Its
  isolated-star witness says nothing about simultaneously decoding all live
  ports, restoring arbitrary scratch inputs or improving copied-information
  cost. It supplies neither a paid recursive profile nor an assembly bound.
- After puncturing, arbitrary off-target stars are outside Theorem 2. Other
  correction classes, source-dependent coefficients within a class, degree-k
  totals, nonlinear mechanisms and different port geometries are outside the
  obstruction as stated. In particular this is not an E8 decoder ceiling.
- The selected construction at the base commit has conditional
  κ=51110230636731/31250000000000000. Its compiler, physical realization,
  hosting, precision/tape and analytic assumptions are neither used to prove
  these finite algebraic statements nor discharged by them.

## Attribution and license

Prepared by Sam Sung (@the-missionary-company), with substantial OpenAI Codex
assistance in the proofs, implementation and independent review. The prior
symmetric obstruction and parity criterion are Joel Pulikkan / GamingPuzzled's
#231 contribution, building on icekylinx's #144 paired-cube work and eumemic's
paired-cube bit identity. The repository preserves those predecessor notices.
The selected-frontier context credits Chafik Boukhalfa's #626, Jeremy Kothe's
#622/#623 and eumemic's #543, with the cumulative lineage in its maintainer
review; this note does not independently re-certify that construction.

New files are licensed under the repository's Apache-2.0 license.
