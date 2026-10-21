# Larger paid target floors and a higher conditional p7 endpoint

This contribution continues the source-bound logarithmic template proof in
[the companion package](../kappa-4416-log-template/PROOF.md), applied to
[PR #4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416) at
`e9058860b5c850760fdf970e796a96aefcdb1d98`. It proves two changes:

| Case | Tested mixed saving | Final conditional kappa | Tensor power | Target floor | Paid cutoff | Sufficient uniform rank |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Larger target floor, same endpoint | `0.00268648` | `0.00268647` | 6240 | `17^6240` | `10^6240` | `2^12185590261265` |
| Higher endpoint | `0.002686489` | `0.002686488` | 8970 | `17^8970` | `10^8970` | `2^190671120967650` |

The first point preserves #4416's native word, tensor power, cutoff and
outer parameters. It changes the paid target completion and the final
uniform template. The second point raises the final multiplication
saving by `0.000000018`. Both remain conditional on the stated native,
all-column, whole-job routing, precision, storage, analytic, fixed-tape
and exact-recovery premises. The astronomical words are specified by
finite recipes and are not materialized.

## 1. Complete source contract

The raw p7/keep232127 controller and its native invoice are unchanged:

```text
T = {5:420, 6:270, 7:840, 8:1395, 9:3195,
     25:448, 41:448, 57:448, 121:224},
P = {1:37305, 2:10695, 3:3360, 4:1530, 5:300,
     8:1464, 16:448, 32:448, 48:448}.
```

There are `B=7688` independent productive fields and 55,998 paid calls.
The ambient rank is 121. The rank-one target and paid moments are
`T_1=131723` and `P_1=131115`, leaving surplus 608. The companion
verifier authenticates all 41 files of the pinned #4416 contribution
and reproduces its complete native, moment and outer receipt before
this continuation uses the invoice.

Native chronology, phases, helper independence, endpoint maps and owned
centers are inherited from that checked finite construction. They are
not inferred from these two histograms. The all-column contract
requires one rank-`r*f` child for each paid position at column count `f`;
replacing it by `f` scalar copies does not satisfy the contract.

## 2. Complete targets to a larger floor

Use the chronological native product of `v` copies. It has `B^v`
independent productive fields, target moment `T_t^v`, paid moment
`P_t^v` and ambient rank `121^v`. Take `t=1-C`, with `0<C<1`.

Conjugate the entire product word by the permitted per-role whole-job
normalizers: apply each role's inverse normalizer to its input, run the
whole product, then apply the corresponding output normalizer. Its
productive endpoint of rank `K` is now in canonical coordinates.
Only after that complete word finishes, for `K<17^v`, pay a positive
transform on `17^v-K` unused, disjoint axes of that same arbitrary
input field. Restore the external matchers when required. Endpoints
now have rank `max(K,17^v)`. No additional productive field or owned
center is credited. Since `17<121`, each completion fits the complete
ambient array.

Split every original and additional paid job at `J=10^v` into
consecutive disjoint blocks, retaining its whole-job normalizers.
For `R=qJ+r`, `0<=r<J`, this costs

```math
qJ^t+r^t\le R J^{-C}+J^t.
```

The zero remainder is omitted. Keeping the original small-call moment
as an overcount bounds all original paid jobs by
`P_t^v+2P_1^v/J^C`. A completion of rank `D<17^v` costs less than
`2*17^v/J^C`, also when `D<J`. Thus the complete paid moment divided
by the original target moment is at most

```math
\alpha^v+2\beta^v+2\delta^v,\qquad
\alpha=P_t/T_t,\quad
\beta=P_1/(10^C T_t),\quad
\delta=B\,17/(10^C T_t).
```

Here `beta` names a paid-tail ratio, not the outer group parameter.
The decisive integer comparison is

```math
B\,17=130696<131115=P_1.
```

Consequently `delta<beta`. Increasing the floor from `11^v` to
`17^v` leaves the same conservative two-tail bound available:

```math
\alpha^v+2\beta^v+2\delta^v < \alpha^v+4\beta^v.
```

This charges every completion. It is not a free enlargement of the
productive endpoints. Completion adds equal target and paid rank-one
mass, and splitting preserves rank-one mass, so the positive surplus
remains `131723^v-131115^v`.

## 3. Two exact finite powers

Independent directed rational logarithm/exponential engines verify
the complete raw moments at both tested savings.

At `C=0.00268648` the original bounds remain

```math
\alpha<1-10^{-8},\qquad \beta<4991/5000.
```

Since `(4991/5000)^390<1/2`, choose `v=6240=16*390`. Bernoulli's
inequality then gives the same strict upper bound as #4416:

```math
\alpha^v+4\beta^v
 <\frac1{1+6240/10^8}+\frac4{2^{16}}<1.
```

At the higher tested saving `C=0.002686489`, the directed interval
checks prove

```math
\alpha<1-\frac8{10^{11}},\qquad \beta<4991/5000.
```

Choose `v=8970=23*390`. The complete normalized paid moment is below

```math
\frac1{1+8970(8/10^{11})}+\frac4{2^{23}}
=\frac{2621441250000897}{2621441881145344}<1.
```

The exact gap is
`631144447/2621441881145344`. With the stated envelope, 22 decay
blocks fail this sufficient comparison; the chosen power is not
claimed to be the smallest possible native power.

The nearby tested point `C=0.00268649` has a strictly negative raw
target-minus-paid moment. It therefore fails this raw-moment
criterion. This is a limitation of this certificate and raw invoice,
not a global upper bound for multiplication.

## 4. Logarithmic uniformization

The completed unit has

```math
m=121^v,\qquad q=17^v,\qquad r_{\max}\le10^v<q.
```

The exact integer inequality `10^75<17^61` allows
`theta=61/75`. The companion proof, retaining the exact integer
compiler and every source complement, gives

```math
L(n)\le m^C n^{1-C}\max(1,\log n)^\gamma
```

whenever `theta^gamma<eta=(1-C)m^{-C}`. The exit estimate has no
additional factor: from `G=floor(log_q(n/m))` and the literal tree,
`e<=r_max^(G+1)<n^theta`. Also `theta*log(m)>1`, which covers
rank-one exits in the logarithmic potential.

Let `b=bit_length(121^v)`. Then `m<2^b`. Since `1-C>1/2`,

```math
\eta>2^{-(1+bC)}\ge2^{-K}
```

for any integer `K>=1+bC`. The following tests use integers and
fractions only:

| Case | `b` | `K` | `gamma` | Verified contraction |
| --- | ---: | ---: | ---: | --- |
| Same endpoint | 43174 | 117 | 393 | `(61/75)^393<2^-117` |
| Higher endpoint | 62063 | 168 | 564 | `(61/75)^564<2^-168` |

For a desired uniform saving `U<C`, choose integers `H,J` with
`H>=b`, `H<2^J` and

```math
H(C-U)>bC+\gamma J.
```

At `N=2^H`, `log(2)<1` implies
`m^C(max(1,log N))^gamma < N^(C-U)`, so
`L(N)<N^(1-U)`. The exact choices are:

| Case | `U` | `H` | `J` | Strict final power gap |
| --- | --- | ---: | ---: | --- |
| Same endpoint | `376107/140000000` | 12185590261265 | 44 | `1/700000000` |
| Higher endpoint | `9402711/3500000000` | 190671120967650 | 48 | `1/7000000000` |

The search for `H,J` is unbounded and terminates for every positive
fixed rational gap. These are sufficient template ranks, not minimal
ranks or bounds on the complete program size. In particular, template
width and instruction counts need not decrease by the rank ratio.

## 5. Complete consumer and replacement constants

For each row, let `kappa` be its claimed final point and set
`d=(C-kappa)/7`. Use #4416's complete outer family:

```text
U=kappa+6*d, b_outer=kappa+5*d, a=kappa+4*d, q_outer=kappa+3*d,
epsilon=1-d, beta_outer=1-3*d, r0=d/10, stop=d, layout=d.
```

Retain ordinary BIT saving `0.0027` and the inherited atom, Strassen,
halo, core and physical transfer parameters. The unchanged ledger
recomputes all nine cost savings, all 54 strict predicates and all
three functional guards at each point. Every saving exceeds its
claimed `kappa`. The higher point is therefore a complete conditional
outer point, not just a local mixed root.

For the new expanded word, let `U_raw` count actual raw p7 invocations,
including those introduced inside products and uniform compilation.
Allocate one separately identified, initialized and erased center for
each invocation. Write `O=U_raw`, `W` for final productive width,
`P` for final paid rank-one count and `R` for every nonscalar native
record and whole-job route, including the new completion/split routes.
Retain the authenticated raw scalar allowance `S=2490856` and define

```text
G=S*U_raw+8*R, Z=W+O,
E=64*(Z+N+P+G+1)^3, B_constant=P+E,
C0=32*N*B_constant^2.
```

Actual coordinate movement is paid separately. The completed-child
recurrence and inherited finite-precision, parking and borrowed-stock
arguments use these new fixed-word counts. All are finite before the
eventual multiplication input varies. No old numerical cap is
substituted for the newly compiled template.

## 6. Provenance and open next questions

The local native supplier and controller are from zxv's
[#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359),
`da637c87c89482bc4c86be36bd0071b3d400dbed`. The source-bound all-fresh
p7 composition and paid-padding construction are retained from
1337isnot1337's #4416 and its #4412/#4414 predecessors. The mixed
lockstep compiler is Jacob Alan Sussman's Theorem 1G. The #4405 outer
ledger and its earlier contributor attribution remain in the pinned
source. The parallel logarithmic-majorant contribution
[#4411](https://github.com/CrocSwap/integer-mult-bounds/pull/4411),
by zxv at `ec2c9505d863c7f5f2a5f08628e8ee6fb740c0a7`, is acknowledged;
no priority claim is made for that idea. New material is Apache-2.0.

This continuation changes the paid padding, supplies exact complete
moment and finite-rank certificates, and reprices the full consumer.
The baseline source package remains immutable and is provided as a
separate exact checkout for replay.

Better kappa beyond this narrow raw root requires a changed controller,
local native word or another admitted operation improvement. Hosting
independent fresh helpers inside an otherwise whole idle of rank `R`,
with widths `w_i` and remainder `d`, changes the mixed surplus by
`R^t-d^t-sum_i(w_i^t)<=0`. Such repacking alone cannot improve this
all-fresh/full-idle invoice. This observation does not exclude changed
native contracts or controller words.

Useful remaining questions are reducing the tensor power with sharper
paid-tail estimates, optimizing the complete uniform word rather than
its ambient rank alone, and independently admitting the retained
all-column, physical movement, precision and outer analytic premises.
No global optimum, unconditional theorem, practical implementation or
selected-frontier promotion is claimed.
