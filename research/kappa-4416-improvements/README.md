# A constructive p7 saving family with smaller finite templates

The source-bound p7 controller from
[PR #4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416)
supports a finite conditional construction for every fixed rational
`0 < kappa < C_star`, where

```math
0.002686489048851021139378940762
< C_\star <
0.002686489048851021139378940763.
```

The resulting bound is `T(n)=O(n(log n)^(1-kappa))` under the retained
premises. An explicit, separately checked recipe gives
`kappa=0.002686489`, an increase of `0.000000019` over #4416's stated
final saving. A logarithmic compiler bound and a larger fully paid
target floor also substantially reduce its sufficient uniform template
rank. The quantified construction reaches every strictly smaller
saving than the raw root, including `kappa=0.002686489`.

| Construction | Final conditional kappa | Tensor power | Target floor base | Sufficient uniform rank |
| --- | ---: | ---: | ---: | --- |
| Pinned PR #4416 | `0.00268647` | 6240 | 11 | `2^16201843136005340321` |
| Logarithmic bound, unchanged source recipe | `0.00268647` | 6240 | 11 | `2^66091190261265` |
| Larger paid target floor | `0.00268647` | 6240 | 17 | `2^12185590261265` |
| Higher conditional endpoint | `0.002686488` | 8970 | 17 | `2^190671120967650` |
| Closer-to-root finite endpoint | `0.002686489` | 9750 | 17 | `2^5670914876226139` |

All rows use paid cutoff base 10 and raw ambient rank 121. A base in
the table is raised to the row's tensor power. The floor-17 construction
at `kappa=0.00268647` makes `log2(N)` smaller by a factor exceeding
1.3 million compared
with #4416's specified bound. These are bounds on sufficient ambient
rank. The complete words remain astronomical, and their instruction
counts and productive widths need not decrease by the same ratio.

The result retains the native all-column, spectator, whole-job routing,
precision, storage, analytic, fixed-tape and exact-recovery hypotheses.
No full multiplication theorem is formally verified or winning template
materialized. The selected result on canonical main is unchanged.

## Review and finite-template improvements

The dependency is the exact #4416 head
`e9058860b5c850760fdf970e796a96aefcdb1d98`, in
`1337isnot1337/integer-mult-bounds`. All 41 files in its contribution
are authenticated by byte length, SHA-256 and original Git blob before
any source is imported. Its integrated verifier reconstructs the
native controller and complete invoice, then reproduces its saved
tensor, padding and outer certificate.

Independent proof reviews found no blocking error in the retained
chronological tensor construction, owned centers, paid source
complements, complete tail bills or stated conditional outer transfer.
The native review covered actual contact maps and inverses, phases,
main endpoints, independent helper roles and full idle owners. This
review does not remove the inherited universal physical and analytic
premises.

The first change is the [logarithmic paid-leaf bound](../kappa-4416-log-template/PROOF.md):

```math
L(n)\le m^C n^{1-C}\max(1,\log n)^\gamma.
```

Here `L(n)` is the fully compiled paid rank-one count per productive
array. The proof retains its exact source/exit recurrence and all
integer batch clearing. It avoids the intermediate power used in the
previous template estimate. Unlike a concave-power mean estimate, it
permits the integer exponent `gamma=2050` needed by the large tensor
dimension.

The second change is [fully paid completion to a larger target floor](../kappa-4416-padding-endpoint/PROOF.md).
There are `B=7688` productive fields and raw paid rank mass `P1=131115`.
The integer inequality

```math
B\cdot17=130696<P1
```

shows that the added completion tail is smaller than the original
paid-splitting tail. Both can therefore use the same conservative
envelope. Increasing the floor from `11^v` to `17^v` improves the
exit contraction while preserving complete payment. The construction
uses input and output whole-job conjugation around the entire product,
then pays the missing disjoint axes on each existing productive owner.

At tested saving `C=0.002686489`, tensor power `v=8970` and fully
charged completion/splitting have normalized paid moment below

```math
\frac{2621441250000897}{2621441881145344}<1.
```

The resulting uniform supplier has saving
`U=9402711/3500000000` at `N=2^190671120967650`. The complete consumer
uses the original seven-gap parameter family at `kappa=0.002686488`.
All nine cost savings exceed that point; all 54 strict inequalities
and three functional guards pass. Its minimum outer slack is exactly
`20981194581/49000000000000000000`.

A [further finite point](../kappa-4416-efficient-root-point/PROOF.md)
uses `C=0.00268648904`, `v=9750` and final `kappa=0.002686489`.
Both directed moment engines certify its raw gap and complete paid
tails. The complete normalized paid-moment bound is

```math
\frac{6710887200000117}{6710887381467136}<1.
```

Using the actual logarithmic contraction gives `gamma=608`,
`U=470135581/175000000000` and `N=2^5670914876226139`. All nine
costs and 57 outer predicates pass; the minimum outer slack is
`262264932211/15312500000000000000000`. The explicit sufficient rank
has a smaller exponent than #4416's specified rank by more than
2,857 times, while also increasing the final saving.

Each new expanded word receives its own scalar, coordinate movement,
storage, precision and reserve constants. The p7 raw scalar allowance
is retained only per actual raw invocation. Product macros are not
counted as single raw invocations or single owned centers.

## Every fixed saving below the raw root

The [constructive root-family proof](../kappa-4416-root-family/PROOF.md)
establishes the full strict range. This extends the earlier qualitative
raw-root headroom in #4420 with a finite constructor and the complete
outer consumer.

Write `T_t` and `P_t` for the two exact raw rank moments and
`t=1-C`. An exact signed-rank decomposition proves that
`(T_t-P_t)/5^t` is strictly increasing throughout `t>=0`.
The unscaled moment `T_t-P_t` equals `-48310` at `t=0` and `608` at
`t=1`. Directed rational intervals then enclose the unique saving
root by the two numbers above.

The construction has a uniform paid-tail estimate:

```math
\frac{131115}{10^C T_{1-C}}<\frac{999}{1000},
\qquad
\frac{7688\cdot17}{10^C T_{1-C}}
<
\frac{131115}{10^C T_{1-C}}.
```

These inequalities hold across the entire interval containing the
root. Given any fixed positive raw moment, an increasing-precision
rational calculation certifies `P_t/T_t<=1-epsilon` for some
`epsilon>0`. A finite tensor power then makes the complete normalized
paid bill smaller than `3/4`. The larger-floor construction, strict
integer compiler and logarithmic template bound apply to that fully
paid rule.

The outer step is proved for a continuum of parameters: the checker
executes the unchanged source ledger over `Q[x,d]` and supplies a
strict rational positivity witness for each of its **54 strict
predicates and three functional guards**. All nine actual cost rows
are matched to their corresponding witnesses. Smaller requested
savings use the already certified fixed program and weaken its bound.
This avoids confusing a historical incumbent-comparison check with
a mathematical restriction on the requested saving.

The generic constructor is deliberately generous. Its saved example
at `kappa=0.002686489` has tensor power `34359739029` and sufficient
rank `2^47400257013113900919251`. These numbers exercise the
quantified construction. The tuned finite point in the table proves
the same saving with a reduction in `log2(N)` exceeding 8.35 million.
The large ambient powers and tensor words
are represented symbolically, without materializing them.

The same proof gives a precise limit for this certificate family.
When the raw mixed moment is nonpositive, tensoring preserves that
sign. Paid target completion changes the moment by
`(K+D)^t-K^t-D^t<0`, and paid splitting also cannot increase it.
Consequently those operations cannot yield a positive complete mixed
moment at or above `C_star`. This is a ceiling for the specified
positive-moment certificates. It does not exclude a better raw
controller, a different analysis of the supplier, or a different
multiplication algorithm.

## A ceiling for every declared two-chain profile

The [all-p chain limit](../kappa-4416-chain-limit/PROOF.md) extends
#4416's finite formula screen over `2<=p<=20`. Among every integer
`p>=1` and every split of the two chains in that exact declared
invoice family, the balanced `p=7` member has the largest raw
mixed-moment root.

For fixed `0<t<1`, the successive chain contributions are
`f_t(j)=(16j+25)^t-(16j+16)^t`. Strict concavity makes them decrease
with `j`, so balanced chains maximize the moment at each `p`.
The successive differences of those balanced maxima then decrease
strictly with `p`. Two exact rational comparisons at the full p7
root enclosure settle the whole unbounded sequence:

```math
1.253606978240 < M_7-M_6 < 1.253606978241,
\qquad
1.427475680484 < M_7-M_8 < 1.427475680485.
```

Here each `M_p` denotes the balanced moment evaluated at the same
point in the root enclosure. At the p7 root, its moment is zero
and every other declared profile has a negative moment. An exact
rank-8/rank-9 pairing proves that each profile's moment divided by
`5^t` increases strictly with `t`, so none becomes positive again
at a larger saving.

This ceiling also survives tensor products of different declared
profiles, paid target completion and paid splitting. It does not
classify arbitrary idle masks or admit a physical controller for
every formula. Even granting all those declared formulas native
admission would not improve their raw endpoint beyond the p7 root.

## Reproduction

Use Python 3.12 or newer with the standard library. Provide a separate
checkout of the exact #4416 source commit; it need not have merged.
For a focused source checkout:

```sh
git init /tmp/pr4416-source
git -C /tmp/pr4416-source remote add origin https://github.com/1337isnot1337/integer-mult-bounds.git
git -C /tmp/pr4416-source fetch --depth 1 --filter=blob:none origin e9058860b5c850760fdf970e796a96aefcdb1d98
git -C /tmp/pr4416-source sparse-checkout set research/pr4359-p7-padding
git -C /tmp/pr4416-source checkout --detach FETCH_HEAD
```

From this contribution's checkout:

```sh
python3 -I -O -B research/kappa-4416-log-template/verify.py --source-root /tmp/pr4416-source --check
python3 -I -O -B research/kappa-4416-padding-endpoint/verify.py --source-root /tmp/pr4416-source --check
python3 -I -O -B research/kappa-4416-root-family/verify.py --source-root /tmp/pr4416-source --check
python3 -I -O -B research/kappa-4416-efficient-root-point/verify.py --source-root /tmp/pr4416-source --check
python3 -I -O -B research/kappa-4416-chain-limit/verify.py --source-root /tmp/pr4416-source --check
```

The second command authenticates and replays the first package, including
the entire source verifier. The third replays both companions before
checking the full strict root family. The fourth independently
recomputes the tuned finite point; the frozen root-family receipt
serves only as its historical rank comparison. The fifth replays the
full root family and checks the declared-profile identities and
neighbor signs used by the unbounded proof. All packages compare deterministic
saved receipts. New acceptance decisions use exact rational or integer
arithmetic. Two separately implemented directed moment engines check
the changed mixed points and both complete paid tails.

Controls reject changed source bytes, equal paid/target bases, an
insufficient logarithmic exponent, a closed uniform gap, one fewer
declared decay block, a target floor of base 18 under this tail
criterion, the nearby failing raw test `C=0.00268649`, and unfunded
outer parameters. A separate exact two-class obstruction explains why
the unpadded raw rule cannot simply bypass the literal compiler's
rank separation.

The initial log-template and padding-endpoint packages also passed an isolated, optimized
replay under Python 3.12.14. A fresh Pyroam workspace downloaded all
41 pinned source files and seven contribution files from GitHub,
checked every Git blob, and reproduced the same receipts under
Python 3.12.13. That independent execution used contribution commit
`806d491bcd31caae35e3cf5f8e97cbce40b452e3` and completed in 35.53
seconds. It did not depend on the earlier p3 exploration workspace.

The root-family package separately passed an isolated optimized
deterministic replay under Python 3.12.14, with only the nine new
proof, generator and receipt files beside the separate pinned source.
Independent reviews also compared all 57 symbolic predicates and
nine cost slacks with the literal rational ledger at boundary and
interior parameter points.

The tuned `kappa=0.002686489` package also passed an isolated
optimized deterministic replay under Python 3.12.14. Its proof and
checker were independently reviewed; a separate rational logarithm
calculation confirmed `gamma=608`, the rejected preceding exponent,
the exact finite rank and the full outer funding.

The all-p chain-limit package passed an isolated optimized
deterministic replay under Python 3.12.14, including the full
root-family dependency chain. Its whole-root-enclosure neighbor
comparisons were also independently reproduced with a separate
rational interval calculation.

## Context, attribution and remaining questions

This builds on the stronger native lineage, rather than presenting
the earlier p3 point as the current best saving:

| PR | Exact reviewed or referenced head | Stated final conditional kappa |
| --- | --- | ---: |
| [#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359) | `da637c87c89482bc4c86be36bd0071b3d400dbed` | `0.0023` |
| [#4412](https://github.com/CrocSwap/integer-mult-bounds/pull/4412) | `9f0df9bf6f49942faf5f31389e7e387fdfe511b3` | `0.00247755` |
| [#4414](https://github.com/CrocSwap/integer-mult-bounds/pull/4414) | `90da4b0ab894350ca12cac9110cc6da2225d18af` | `0.00267987` |
| [#4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416) | `e9058860b5c850760fdf970e796a96aefcdb1d98` | `0.00268647` |

The native supplier and controller are zxv's #4359 work. The all-fresh
composition and paid-target-padding lineage is retained from
1337isnot1337's #4412, #4414 and #4416. The integer mixed flow is Jacob
Alan Sussman's Theorem 1G in #4268. The outer family comes from #4405,
with its earlier contributors retained in the pinned source notices.
New material is under Apache-2.0.

Parallel [#4411](https://github.com/CrocSwap/integer-mult-bounds/pull/4411),
by zxv at `ec2c9505d863c7f5f2a5f08628e8ee6fb740c0a7`, proves a
logarithmic majorant for the original suppliers. No priority claim is
made for that idea. [#4420](https://github.com/CrocSwap/integer-mult-bounds/pull/4420),
by Ryanson Jonathan at `64b4f5457613ada7f0e3f2f4d26f9978d19cdfa7`,
independently checks the original p7 moment/tail arithmetic and reports
its narrow remaining raw-root headroom. Its scope excludes the native
word and full consumer; its source description and checker were read.
The new contribution here includes the changed paid padding, complete
finite templates, complete outer points, constructive full strict
range, scoped certificate ceiling and all-p declared-chain limit.

The later [#4426](https://github.com/CrocSwap/integer-mult-bounds/pull/4426),
at `6f918e2658c727007611d98ffb8d3c7336e2290c`, independently rebuilds
the selected p7 Laurent word and invoice.
[#4428](https://github.com/CrocSwap/integer-mult-bounds/pull/4428), at
`ba0efeaac4e62d1757d7a9be6fd8aaf8f9bd35dc`, checks the original
paid-completion proof and arithmetic and gives further fixed-recipe
improvements under the earlier power induction. Both explicitly state
no new final kappa. Their primary descriptions and #4428's checker
were read during the final overlap refresh. They do not supply the
constructive full outer range or the all-p declared-chain theorem here.

This focused branch starts from canonical main
`12fa8c5c844be21bfefb38a19503fbd867a11244`. Source heads were checked
against the live PR queue before publication. The overlap search is
not exhaustive, and Discussion coverage was unavailable. The final
queue refresh through #4429 at 18:13 UTC on 2026-10-21 found no larger
stated final kappa than `0.002686489` in the checked entries.

## Open next questions

A stronger raw controller or admitted native operation could move the
mixed-moment root. The all-p result rules out achieving that merely
by increasing `p` or changing the split in the declared two-chain
formula. A feasible first step is an exact controller factorization
and complete invoice outside that formula. A candidate
must retain the chronological word, arbitrary input fields, helper
owners and complete paid calls before its numerical moment is useful.
The root-family ceiling does not settle this broader search.

Sharper finite parameters can reduce the very large sufficient
templates. The next step is to compare tighter complete splitting
and paid-tail bounds across cutoff and tensor-power choices, then
rerun the full outer consumer and charge the actual width and movement.
An improvement in ambient rank alone does not establish a comparable
reduction in productive width or expanded instruction count.

Full productive width, program size and the inherited universal
physical and analytic premises remain separate questions. A first
step is to extend the charged native-record inventory to an explicit
width and movement formula for the new word. Finite invoice replay
does not resolve those universal premises.
