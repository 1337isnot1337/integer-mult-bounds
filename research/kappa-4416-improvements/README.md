# Conditional kappa 0.002686488 with smaller p7 templates

The source-bound p7 controller from
[PR #4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416)
supports the improved conditional point

```math
T(n)=O\!\left(n(\log n)^{1-0.002686488}\right).
```

The increase over #4416's stated final saving is `0.000000018`.
A logarithmic compiler bound and a larger fully paid target floor
also substantially reduce its sufficient uniform template rank.

| Construction | Final conditional kappa | Tensor power | Target floor base | Sufficient uniform rank |
| --- | ---: | ---: | ---: | --- |
| Pinned PR #4416 | `0.00268647` | 6240 | 11 | `2^16201843136005340321` |
| Logarithmic bound, unchanged source recipe | `0.00268647` | 6240 | 11 | `2^66091190261265` |
| Larger paid target floor | `0.00268647` | 6240 | 17 | `2^12185590261265` |
| Higher conditional endpoint | `0.002686488` | 8970 | 17 | `2^190671120967650` |

All rows use paid cutoff base 10 and raw ambient rank 121. A base in
the table is raised to the row's tensor power. The unchanged-endpoint
improvement reduces `log2(N)` by more than 1.3 million times compared
with #4416's specified bound. These are bounds on sufficient ambient
rank. The complete words remain astronomical, and their instruction
counts and productive widths need not decrease by the same ratio.

The result retains the native all-column, spectator, whole-job routing,
precision, storage, analytic, fixed-tape and exact-recovery hypotheses.
No full multiplication theorem is formally verified or winning template
materialized. The selected result on canonical main is unchanged.

## Review and the two changes

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

Each new expanded word receives its own scalar, coordinate movement,
storage, precision and reserve constants. The p7 raw scalar allowance
is retained only per actual raw invocation. Product macros are not
counted as single raw invocations or single owned centers.

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
```

The second command authenticates and replays the first package, including
the entire source verifier. Both packages compare deterministic saved
receipts. New acceptance decisions use exact rational or integer
arithmetic. Two separately implemented directed moment engines check
the changed mixed points and both complete paid tails.

Controls reject changed source bytes, equal paid/target bases, an
insufficient logarithmic exponent, a closed uniform gap, one fewer
declared decay block, a target floor of base 18 under this tail
criterion, the nearby failing raw test `C=0.00268649`, and unfunded
outer parameters. A separate exact two-class obstruction explains why
the unpadded raw rule cannot simply bypass the literal compiler's
rank separation.

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
finite templates and complete outer points.

This focused branch starts from canonical main
`12fa8c5c844be21bfefb38a19503fbd867a11244`. Source heads were checked
against the live PR queue before publication. The overlap search is
not exhaustive, and Discussion coverage was unavailable.

Further work should connect a stronger raw controller or admitted
native operation to a complete paid invoice, sharpen the uniform
tail-to-template construction, bound full productive width and program
size, and independently resolve the retained universal native and
analytic premises. The nearby failed raw test and any bounded
controller search do not establish a global barrier.
