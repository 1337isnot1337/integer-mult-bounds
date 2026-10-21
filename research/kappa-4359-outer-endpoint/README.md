# Strict outer savings approaching the unchanged p3 mixed root

This result is conditional on the finite compiler, native adapters, delayed
BIT cover, finite-template closure, and outer analytic and tape hypotheses
of PR #4359. It does not change the local productive word or its invoice.

The outer parameters in #4359 leave a gap between the complex mixed root
and its stated multiplication saving. That gap can be made arbitrarily
small while keeping every required inequality strict. The root itself is
not attained by this argument.

## Result

Let `C` be the saving root of the unchanged complex p3 invoice:

```
targets = {6:192, 7:56, 8:93, 9:1229, 25:448, 57:224}
paid    = {1:17623, 2:5065, 3:1738, 4:714, 5:254}.
```

Subject to the named hypotheses of #4359, every rational

```
0 < kappa < C = 0.002305090194876170622919094755...
```

is an admissible outer saving. The finite program and its constants depend
on the chosen strict saving. This does not assert one program attaining `C`.

The root is unique. For `R(t)=sum_paid r^t / sum_targets W_k*k^t`,
the logarithmic derivative is at most `log(5)-log(6)<0` because every
paid rank is at most 5 and every productive rank is at least 6.
Also `R(0)=25394/2242>1` and `R(1)=37093/37317<1`.
Thus `C=1-t_root` is well defined, and the strict mixed moment is
positive at every saving below `C`.

A concrete instance is

```
kappa = 0.00230508,
T(n) = O(n (log n)^(1-kappa)).
```

This exceeds `0.0023` by `0.00000508`. The minimum outer saving is
`0.002305081995389836`, giving exact positive slack
`498847459/250000000000000000`.

The supplier is recompiled at uniform saving `0.002305088` and the fixed
rank `N=2^1729137493`. The separate
[logarithmic-potential proof](../kappa-4359-log-potential/PROOF.md) and
its exact certificate establish that sufficient rank. The outer verifier
replays the rank verifier and checks the exact tested saving, uniform
saving, and rank. The old `0.002304` template is not used for this point.
The generic formulas in `FINITE-TEMPLATE-CLOSURE.md` use the new template's
finite counts, including every owned bank and scalar or routing operation.
Those enormous counts and instruction lists are not materialized.

## An explicit rational parameter family

Let `B` be an admitted ordinary BIT saving. Choose rationals satisfying

```
0 < kappa < c < min(C, B, 1/32),
d = (c-kappa)/5.
```

The #4359 BIT construction admits `B=0.0027`, which exceeds `C`.
Set

| Parameter | Choice |
| --- | --- |
| Tested mixed saving | `c` |
| Compiled complex uniform saving `U` | `c-d` |
| Selected complex saving `b` | `c-2d` |
| Effective common saving `a` | `c-3d` |
| Outer transform saving parameter `q` | `c-4d` |
| Global dimension exponent `epsilon` | `1-d` |
| Group exponent `beta` | `1-3d` |
| Stopping exponent | `d` |
| Precision spare power `r0` | `d/4` |
| Layout slack | `d/4` |
| `lambda` | `1-(q+a)/2` |
| `lambda_prime` | `1-q` |
| Boundary matrix exponent | `45/16` |
| Boundary cap `xi` | `(1-d)(1+q)-3/32+d/4` |

Keep `theta_power=2`, `halo_power=48`, and `core_power=128`.
All these quantities are fixed before the input length varies.

### Supplier and stopping inequalities

The strict mixed test at `c` gives a finite uniform supplier at `U<c`,
under the unchanged compiler theorem. The differences `c-U`, `U-b`,
`b-a`, and `a-q` all equal `d>0`. Also `B>a`.

For the stopped recurrence, `sigma=1-b<tau=1-a`, so the internal exponent
is exactly `tau`. The stopped leaf saving is

```
(1-d)b = a+d(1-b) > a.
```

The chosen `lambda` is `tau+d/2`. The chosen `lambda_prime` exceeds it
by `d/2` and exceeds the leaf exponent by `d(2-b)`. All the strict
stopping inequalities therefore hold.

### Every outer cost

Substitution in the unchanged nine outer formulas gives:

| Cost | Saving |
| --- | --- |
| Main transform | `(1-d)q` |
| Global coordinate routing | `a` |
| Fused Gaussian work | `q+d(1-3q)` |
| Group BIT routing | `a+d(1-3a)` |
| Group scans | `1-2d` |
| Boundary matrix work | `(1-d)q+d/4` |
| Sparse union movement | `(1-d)q+d/4+13/32` |
| Polynomial products | `1-d` |
| Microbox face corrections | `77+4d` |

Since `kappa=q-d`, the main margin is exactly

```
(1-d)q-kappa = d(1-q) > 0.
```

Global routing exceeds the main row by `d(1+q)`. The Gaussian row exceeds
the main row by `d(1-2q)>0`. Group BIT routing exceeds the Gaussian row
by `d(1-3d)>0`. The boundary and sparse-union rows have the displayed
positive extra terms. Since `q<c<1/32` and `d<c/5<1/160`, the remaining
three rows are larger than the main row. Thus the main row is binding.

### Functional precision, support, stock, and layout conditions

The parameter gaps used to absorb the changed finite constants are

```
1-epsilon = d > 0,
1-beta = 3d > 0,
epsilon-beta = 2d > 0,
1-epsilon-r0 = 3d/4 > 0,
1-beta-2(1-epsilon) = d > 0.
```

The boundary cap satisfies

```
epsilon-xi = 3/32-(1-d)q-d/4 > 39/640 > 0,
xi-1/2 = 13/32+q-d(3/4+q) > 0.
```

The fine-prime group guard is

```
1-(2xi-2)-r0-beta = 3/16-2q+d(17/4+2q) > 1/8.
```

The BIT atom exponent remains `3/1000`. Consequently the changed row
stock is sublinear in the active group, since
`beta*(1-3/1000)>0`. The fixed halo metadata inequality has margin
`128-48-epsilon-beta-1>77`. The unchanged integer comparison
`7^16<2^45` supports the selected boundary exponent.

These positive powers remain valid even when `d` is very small. They
increase the eventual input threshold; they do not permit omission of
the new finite-template constants or native movement costs. Every other
retained scalar inequality is recomputed by the accompanying certificate
and cross-checked against the unchanged inherited ledger function. Its
63 positive predicates are checked at the concrete point; historical
`improvement_over_*` predicates are not assertions about every smaller
rational `kappa` in the general theorem.

## The concrete point

Choose `c=0.00230509` and `kappa=0.00230508`. Then `d=0.000000002`:

| Parameter | Exact decimal |
| --- | ---: |
| Uniform complex saving `U` | 0.002305088 |
| Selected complex saving `b` | 0.002305086 |
| Effective saving `a` | 0.002305084 |
| Outer parameter `q` | 0.002305082 |
| `epsilon` | 0.999999998 |
| `beta` | 0.999999994 |
| Stopping exponent | 0.000000002 |
| `r0` and layout slack | 0.0000000005 |

Independent directed rational arithmetic encloses the complete local
moment surplus at the tested `c` around
`0.0000188554472952932126952022696385`, strictly above zero.
It rejects the nearby unsupported saving `0.002306` and the zero-gap
choice `kappa=c`.

## Scope and provenance

The local p3 word, invoice, mixed root, BIT saving, and all native and
analytic interfaces come from #4359 at commit
`da637c87c89482bc4c86be36bd0071b3d400dbed`. The outer equations retain
the work credited there, including PR #1673, #1758, and #1786.

The new result is the strict parameter family and its quantified stronger
outer point. It does not advance the local mixed root. Source hashes,
directed rational intervals, all strict inequalities, and agreement with
the inherited ledger are recorded by `verify.py`.

## Reproduction and open next questions

Check the committed certificates against a checkout containing the pinned
#4359 source files:

```sh
python3 -B research/kappa-4359-outer-endpoint/verify.py --source-root /path/to/pr4359 --check-only
```

The `--source-root` argument keeps the pending predecessor explicit.
It defaults to the current project root when those files are present.
To emit a fresh certificate, replace `--check-only` with
`--out /tmp/outer-endpoint-certificate.json`. Immutable SHA-256 pins are
checked before reading the invoice or executing the inherited ledger.
The replay rejects a changed inherited source before execution, a saving
above the local mixed root, and a zero-gap outer choice.

The main remaining source of exponent improvement is the local complex
invoice. Parameter retuning can approach its root but cannot cross it.
A further improvement requires a new complete native invoice or a stronger
compiler theorem with different cost accounting. Any such result must
preserve arbitrary productive inputs, charge owned-center calls, and
retain the native scalar, phase, movement, and cleanup costs.

The logarithmic-potential rank bound can also be tightened at a fixed
uniform saving. The useful first calculation is an exact optimization of
its concavity parameter against the final integer rank condition; this
changes finite constants and template size rather than the mixed root.

Apache-2.0 for the new material; inherited notices remain applicable.
