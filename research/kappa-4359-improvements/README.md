# Conditional kappa 0.00231284 from the productive jobs in PR #4359

Under the inherited native and outer-transfer hypotheses of
[PR #4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359), the
proved native modification and finite compiler extension in this
contribution support

```math
T(n)=O\bigl(n(\log n)^{1-0.00231284}\bigr).
```

This improves the predecessor's stated saving `0.0023` by `0.00001284`.
The construction first deletes 102 rank-one topups and retains the
corresponding fresh outputs at their native rank five. It then repacks
38 idle owners to use the changed rank interface more efficiently. A new
weighted-exit proof permits equality between maximum paid rank and minimum
productive target rank. An exact finite-rank certificate and rational
outer parameters complete the conditional implication.

The predecessor is pinned to
`da637c87c89482bc4c86be36bd0071b3d400dbed`. This contribution is based on
canonical main `12fa8c5c844be21bfefb38a19503fbd867a11244`; its checkers
accept a separate checkout of the pending predecessor. The inherited
analytic, native movement, precision, and fixed-tape conditions remain
part of the claim. The selected result on canonical main is a separate
record and is unchanged.

## Results and their evidence

| Result | Evidence | Scope |
| --- | --- | --- |
| Detailed review of the predecessor | [Audit](../kappa-4359-audit/README.md) | All 23 fresh replay stages and all 59 scientific artifact comparisons pass; 45 artifacts are byte-identical |
| Native topup removal | [Native deletion proof](../kappa-4359-native-five/README.md) | Exactly 102 authenticated, disjoint sixth-axis topups are removed, with lower endpoint promises and all complement costs retained |
| Further native packing gain | [Packing proof](../kappa-4359-native-packing/README.md) | 38 literal idle owners receive a better helper partition, with full coordinate maps, inventories, normalizers and paid chronology reconstructed |
| Equal-rank finite compilation | [WeakRule interface](../kappa-4359-weak-compiler/README.md) and [weighted-exit proof](../kappa-4359-weak-separation/PROOF.md) | Finite chronological integer batching with `r_max <= k_min < m` and `k_min >= 2` |
| Specified successful finite rank | [Packed-tail proof](../kappa-4359-packed-tail/PROOF.md) | Uniform saving `0.002312848` at `N=2^756938551` |
| Final integer-multiplication exponent | [Outer proof](../kappa-4359-native-packing/OUTER.md) | All nine cost rows strictly support `kappa=0.00231284`, with authenticated native and compiler dependencies |
| Entire strict endpoint range | [Packed-tail theorem](../kappa-4359-packed-tail/PROOF.md) | Every fixed rational `0<kappa<C_*`, where `C_*` is the final mixed root, with a finite template chosen for that kappa |
| Smaller templates for the original tariff | [Logarithmic potential proof](../kappa-4359-log-potential/PROOF.md) | A separate improvement preserving the predecessor's original native invoice |

The audit found no blocking error in the predecessor's conditional
source/exit argument, chronological ownership, native composition, or
all-column extension. The retained receipts distinguish exact byte
agreement from the explicitly declared timing and hash normalization.
Finite replay does not establish all inherited operator and analytic
premises, and it does not materialize the enormous winning templates.

## The native change and its complete accounting

The revised productive and paid ranks are:

| Rank | Productive jobs | Paid calls |
| ---: | ---: | ---: |
| 1 | 0 | 17,559 |
| 2 | 0 | 5,027 |
| 3 | 0 | 1,738 |
| 4 | 0 | 714 |
| 5 | 140 | 254 |
| 6 | 52 | 0 |
| 7 | 56 | 0 |
| 8 | 93 | 0 |
| 9 | 1,229 | 0 |
| 25 | 448 | 0 |
| 57 | 224 | 0 |

There are still 2,242 independent productive fields and one uncredited
owned center. The rank surplus is still 224. The retained conservative
scalar allowance is still 1,147,304 real primitives.

For `0<t<1`, the initial topup deletion improves the target-minus-paid
mixed moment by exactly

```math
102\bigl(1+5^t-6^t\bigr)>0.
```

Each of the two rank-16 idle families originally uses 19 helper pairs
`(5,9)`, leaving a rank-two remainder. The further change replaces these
with 18 pairs `(6,9)` and one pair `(9,6)`, leaving rank-one remainders.
The literal helper inventories fit. All other window patterns remain:
93 pairs `(8,8)`, 56 pairs `(7,9)`, 56 pairs `(9,7)`, and the two
rank-eight middle families. This adds the strict moment improvement

```math
38\bigl(2^t+5^t-1-6^t\bigr)>0.
```

Both inequalities follow from strict concavity. The second uses
`2^t-1>6^t-5^t`. Full completion accounting is preserved at each step:

| Rank-one base bill at ambient rank 57 | Original | Topups removed | Repacked |
| --- | ---: | ---: | ---: |
| Productive target rank mass | 37,317 | 37,215 | 37,177 |
| Paid rank mass | 37,093 | 36,991 | 36,953 |
| Source complement rank mass | 90,477 | 90,579 | 90,617 |
| Total full-completion leaves | 127,570 | 127,570 | 127,570 |

The gain arises in the mixed hierarchy, whose recurrence pays all of
those complements. The packing certificate reconstructs every fresh
field and actual helper binding, including their full invertible
coordinate maps. Its complete oriented normalizer multiset and scalar
controller are unchanged; its changed coordinate moves receive their
own finite movement constants.

Exact rational intervals place the new mixed saving root strictly in

```text
(0.002312854665364207351198238279,
 0.002312854665364207351198238280).
```

The original compiler's strict rank-separation constructor rejects the
new invoice because both extreme ranks equal five. The explicit new
interface and theorem are therefore necessary parts of this result.

## Why the equal-rank compiler closes

Write `t=1-C`, `m=57`, and `q=5`. The integer source/exit matching only
needs each paid rank to be at most each productive rank. Its deepest
exits satisfy `e <= (q/m)n < n`, so the recursive program terminates.
Source complements also have smaller rank.

For `G=floor(log_q(n/m))`, the exact unnormalized exit moment is
`E_a=P_a^(G+1)`, where `P_a` is the complete paid-call moment. A weighted
tail estimate controls the potential of exits above `n^(3/4)`. At the
tested saving, `P_(t+1)/P_t<2`, and the large-exit fraction is less than
`1/8` at every `n>=57`.

This yields the global paid-leaf bound

```math
L(n)\leq 57^C n^{1-C}\max(1,\log n)^{1/20}.
```

The proof closes with a rational bound on the entire weighted exit
term, including the large exits. It also retains all source complements
and ordered paid calls, including paid calls on owned storage.

For the concrete choices

```text
C   = 0.00231285
C_u = 0.002312848
H   = 756938551
J   = 30,
```

the certificate verifies `H<2^J` and the strict sufficient inequality

```math
H(C-C_u)-6C-J/20=1/500000000>0.
```

Consequently the fully specified finite supplier at `N=2^H` has
`L(N)<N^(1-C_u)`. The finite algorithm specifies its replication factors
and complete word; these huge objects are not materialized here.

## Exact outer instance

The rational parameter family has spacing `d=(C-kappa)/5`. The chosen
instance is:

| Quantity | Exact value |
| --- | ---: |
| Tested complete mixed saving `C` | `0.00231285` |
| Uniform supplier saving `C_u` | `0.002312848` |
| Selected complex saving `b` | `0.002312846` |
| Effective common saving `a` | `0.002312844` |
| Outer transform parameter `q_outer` | `0.002312842` |
| Claimed `kappa` | `0.00231284` |
| `d` | `0.000000002` |
| `epsilon` | `0.999999998` |
| `beta` | `0.999999994` |
| Main-transform saving | `0.002312841995374316` |

The main-transform saving exceeds the claim by
`0.000000001995374316`. All nine outer cost rows strictly clear the
claim. The verifier checks the direct inequalities and the inherited
ledger, and replays the native deletion, weak compiler, and finite-rank
certificates, including the actual new paid-owner integration, before
accepting the final exponent.

Every template-dependent scalar, routing, storage, precision, and reserve
constant must be the constant of the new fixed compiled word. Earlier
numerical caps are not reused. The very large finite constants are
absorbed only in the eventual asymptotic bounds under the inherited
transfer hypotheses.

## The complete strict endpoint range

The [packed-tail theorem](../kappa-4359-packed-tail/PROOF.md)
proves that every fixed rational `0<kappa<C_*` is admitted under the same
conditional interfaces, where `C_*` is the new mixed root enclosed above.
This statement chooses a finite template for each strict kappa; it does
not assert attainment of `C_*` itself.

The weighted-exit estimate holds uniformly across this range. For every
`t<=1`, the complete paid invoice satisfies

```math
P_{t+1}-2P_t\leq P_2-2P_1=71083-2(36953)=-2823<0.
```

The rank-one term is constant, the rank-two coefficient is zero, and
every higher-rank term has a positive coefficient and increases with
`t`. The complement margin also remains strictly above `4047/4096`
through the convenient rational upper bound `C=0.00232`, which exceeds
`C_*`. Thus the same `gamma=1/20` proof covers every mixed saving below
the root. The unbounded finite-rank search in the endpoint package
then supplies a template for every required positive rational gap.

## Completed intermediate improvements

The first native continuation, before repacking, supports
`kappa=0.00231165` and every strict saving below its own mixed root
`0.002311660492818048695136925339...`. Its native word, weak compiler,
concrete rank certificate and full endpoint corollary remain separately
frozen in `kappa-4359-native-five/`, `kappa-4359-weak-compiler/`, and
`kappa-4359-weak-separation/`.

The final packing raises the mixed root itself. Its stronger outer point
uses the new uniform saving and complete paid-owner contract; the earlier
template cannot simply be relabeled with the larger exponent.

## A separate improvement preserving the original native invoice

The first part of this contribution proved a logarithmic paid-leaf bound
under the predecessor's strict separation. Together with the rational
outer family, it supports `kappa=0.00230508` using the unchanged native
tariff. The proof and deterministic certificates remain separately
reproducible in `kappa-4359-log-potential/` and
`kappa-4359-outer-endpoint/`.

At the predecessor's original uniform savings, it gives:

| Family | Uniform saving | PR #4359 | Related PR #4405 | Logarithmic bound here |
| --- | ---: | ---: | ---: | ---: |
| Complex | `0.002304` | `2^276540184361` | `2^1546084442` | `2^2458275` |
| BIT before the cover | `0.002760` | `2^6552928412` | `2^42843607` | `2^463652` |

These are comparisons of sufficient ambient ranks. The expanded words,
batch multiplicities, and constants remain enormous. A smaller
sufficient rank does not by itself give a practical runtime measurement.

## Related contributions found in the final overlap check

[PR #4405](https://github.com/CrocSwap/integer-mult-bounds/pull/4405), at
head `873d1b3c96a83b701a5c0bba8e37a861e6672fef`, proves a strict outer
family below the unchanged mixed root and checks the point
`kappa=0.00230509`. It also tightens the original intermediate-power
argument by using the actual complement coefficient. Its sufficient ranks
at the original supplier savings appear in the comparison above.

The original-tariff outer-family conclusion in this contribution overlaps
that related result. No priority claim is made for that conclusion, and
the retained `0.00230508` point is not an improvement over #4405's
`0.00230509` point. The logarithmic paid-leaf bound gives the distinct
smaller sufficient ranks shown above. The later weak-separation, topup
deletion and literal repacking change the native tariff and raise its
mixed root beyond both unchanged-tariff results.

[PR #4404](https://github.com/CrocSwap/integer-mult-bounds/pull/4404), at
head `77f20afb7c24286937c75cb65a7f19e24e7a567f`, independently checks the
original explicit-rank argument and 19,895 aggregate lockstep flows. Its
stated scope excludes the native word, denominator clearing, delayed BIT
cover and outer transfer. The review retained here records its own
broader source/ownership/operator scope and reproduction limits.

These related public contributions were located during the final
2026-10-21 overlap check. The search is not an exhaustive novelty audit;
Discussion coverage was unavailable. Both PR heads and stated scopes
were recorded, and #4405's endpoint and template proofs were read.
Their different claims remain separate from the new native result.

## Reproduction

Use a separate checkout of the pinned predecessor as the source root.
One way to obtain it is:

```sh
git init /tmp/integer-mult-pr4359-source
git -C /tmp/integer-mult-pr4359-source remote add origin https://github.com/zxv/integer-mult-bounds.git
git -C /tmp/integer-mult-pr4359-source fetch --depth 1 origin da637c87c89482bc4c86be36bd0071b3d400dbed
git -C /tmp/integer-mult-pr4359-source checkout --detach FETCH_HEAD
```

Run the following commands from this contribution's checkout:

```sh
python3 -B research/kappa-4359-log-potential/verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-outer-endpoint/verify.py --source-root /tmp/integer-mult-pr4359-source --check-only
python3 -B research/kappa-4359-weak-compiler/verify.py --source-root /tmp/integer-mult-pr4359-source
python3 -B research/kappa-4359-native-five/verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-weak-separation/verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-native-five/outer_verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-weak-separation/endpoint_verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-weak-compiler/native_five.py --source-root /tmp/integer-mult-pr4359-source
python3 -B research/kappa-4359-audit/count_multilevel.py --source-root /tmp/integer-mult-pr4359-source
python3 -B research/kappa-4359-native-packing/verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-native-packing/compiler_check.py --source-root /tmp/integer-mult-pr4359-source
python3 -B research/kappa-4359-packed-tail/verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-native-packing/outer_verify.py --source-root /tmp/integer-mult-pr4359-source --check
```

The checkers use the Python standard library. They authenticate fixed
source hashes and compare deterministic certificates. The outer
checkers also replay their required rank certificates and cross-check all
nine cost rows against the inherited ledger. No floating-point result
decides acceptance. The audit directory documents the additional count,
ownership, comparison-control, and original replay checks.

The predecessor's separate full replay is:

```sh
python3 -B /tmp/integer-mult-pr4359-source/research/kappa-0023-productive-jobs/verify.py --out /tmp/pr4359-fresh-replay
```

The output directory must not already exist. That replay checks the
predecessor's native artifacts; the new arithmetic checks do not replace
its operator and ownership obligations.

## Provenance and open next questions

The p3 native word, complete invoice, delayed BIT cover, and original
finite-template closure are from zxv's PR #4359. The mixed-job lockstep
construction builds on Jacob Alan Sussman's Theorem 1G in PR #4268.
The outer formulas and their earlier contributors remain credited in
the pinned predecessor and the proof packages. New material is under
Apache-2.0.

The width-five change resolves the initial investigation of topups used
only for strict separation, and the new owner assignment completes one
further packing improvement under that interface. Global optimality of
the packing is not claimed. The retained rank-eight windows already use
all available helpers of width at most eight, so a further improvement
needs a different complete packing, controller, native contract or proved
compiler interface. Every candidate must reconstruct its integral owner
assignment and preserve all chronological endpoints, arbitrary inputs,
movement charges and cleanup operations. A tighter exit estimate may also
reduce finite template sizes; it cannot by itself raise the local mixed
root.
