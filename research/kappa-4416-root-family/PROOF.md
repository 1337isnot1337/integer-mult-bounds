# The strict p7 root family and its precise mixed-moment limit

This note gives a constructive conditional result for **every fixed rational
`0 < kappa < C_star`**, where the raw p7 root satisfies

```text
0.002686489048851021139378940762
    < C_star <
0.002686489048851021139378940763.
```

The resulting integer-multiplication bit bound is
`T(n)=O(n*(log n)^(1-kappa))`, under the inherited premises below.

The construction retains the native p7 word in
[PR #4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416), at
`e9058860b5c850760fdf970e796a96aefcdb1d98`. It uses fully paid target
completion, paid-job splitting, the exact integer compiler, and the
complete inherited outer consumer. Every parameter and finite program is
fixed before the eventual multiplication input varies.

The root is also the supremum of the positive mixed-moment certificates
obtainable from this fixed raw invoice by the tensor, completion and
splitting operations specified below. This is a limit on that certificate
family. It does not lower-bound the performance of every algorithm using
the supplier, or exclude a different analysis, controller or native word.

The earlier statement of this raw root and infinite-power headroom in
[PR #4420](https://github.com/CrocSwap/integer-mult-bounds/pull/4420), by
pinterbanget at `64b4f5457613ada7f0e3f2f4d26f9978d19cdfa7`, is acknowledged.
No priority claim is made for the root or headroom. The additional result
here is the quantified construction, uniform exact tail bound, complete
outer family, and precise closure argument for the allowed operations.

## 1. Authenticated native input and inherited premises

The checker first authenticates and replays both new companion packages:

- [Logarithmic uniform compilation](../kappa-4416-log-template/PROOF.md).
- [Paid floor 17 and the concrete endpoint](../kappa-4416-padding-endpoint/PROOF.md).

Their immutable digests bind all 41 files of the source contribution. The
full native, tensor, moment and outer source receipt is recomputed before
its invoice is used. The two exact raw profiles are

```text
T = {5:420, 6:270, 7:840, 8:1395, 9:3195,
     25:448, 41:448, 57:448, 121:224},
P = {1:37305, 2:10695, 3:3360, 4:1530, 5:300,
     8:1464, 16:448, 32:448, 48:448}.
```

The ambient rank is 121, the productive field count is `B=7688`, and the
number of paid calls is 55,998. The first moments are `T_1=131723` and
`P_1=131115`. Their positive difference is 608.

This is an invoice of the authenticated chronological word. It is not a
replacement for its owner, phase, spectator or whole-job contracts. In
particular, each paid position at column count `f` requires one native
rank-`r*f` child. Separate scalar copies do not supply that contract.
The all-column, physical movement, finite precision, owned storage,
analytic, fixed-tape and exact-recovery premises remain conditional.

## 2. One raw root throughout the full exponent interval

For `0 <= t <= 1`, write

```math
M_t=T_t-P_t=\sum_r(T_r-P_r)r^t,
\qquad C=1-t.
```

After common ranks are netted, its exact decomposition is

```math
\begin{aligned}
M_t={}&120\,5^t+270\,6^t+840\,7^t+3126\,9^t+224\,121^t\\
 &-37305-10695\,2^t-3360\,3^t-1530\,4^t\\
 &+69(9^t-8^t)\\
 &+448\bigl((25^t-16^t)+(41^t-32^t)+(57^t-48^t)\bigr).
\end{aligned}
```

Divide by `5^t`. Each remaining positive monomial has base at least one.
Each remaining negative monomial has base strictly less than one, so its
negative increases strictly with `t`. For any paired bases `1<a<b`,
`b^t-a^t` also increases strictly for `t>=0`: its derivative is
`b^t log(b)-a^t log(a)>0`, since `x^t log(x)` increases in `x>=1`.
Therefore `M_t/5^t` is strictly increasing for all `t>=0`.

The integer endpoint values are `M_0=-48310` and `M_1=608`. Continuity
gives exactly one zero `t_star` in `(0,1)`. Define `C_star=1-t_star`.
It follows on the entire interval `0<C<1` that

```math
T_{1-C}>P_{1-C}\quad\Longleftrightarrow\quad C<C_\star.
```

The checker proves the two strict signs in the displayed root enclosure
using directed rational logarithms and exponentials. As an independent
local check, it also bounds the derivative of `M_(1-C)` on
`0<=C<=C_cap=0.00268649` by

```math
\frac{d}{dC}M_{1-C}
\le \sum_r P_r r\log r
   -\sum_r T_r r^{1-C_{\rm cap}}\log r
<-223288.
```

The global uniqueness claim uses the exact decomposition, rather than
extrapolating this local derivative estimate.

## 3. A single paid-tail bound for the whole relevant range

For a fixed `0<C<C_star`, put `t=1-C` and

```math
\alpha=\frac{P_t}{T_t},\qquad
\beta=\frac{131115}{10^C T_t},\qquad
\delta=\frac{7688\cdot17}{10^C T_t}.
```

These `beta` and `delta` are paid-tail ratios, unrelated to the outer
group parameter. Let

```math
D(C)=10^C T_{1-C}
     =\sum_r T_r r\exp\!\left(C\log\frac{10}{r}\right).
```

This is convex. Its tangent gives `D(C)>=131723+C D'(0)`. Directed
logarithm intervals prove `D'(0)>-138300`. Thus, uniformly for
`0<=C<=C_cap`,

```math
D(C)\ge131723-138300C_{\rm cap},
```

and the entirely rational comparison is

```math
\frac{999}{1000}(131723-138300C_{\rm cap})-131115
=105.106974567>0.
```

Also `7688*17=130696<131115`. Consequently

```math
0<\delta<\beta<\frac{999}{1000}<1
```

throughout the whole root-below range. The exact integer comparison
`2*999^693<1000^693` supplies one uniform decay block.

## 4. An effective strict mixed rule for any fixed root-below saving

Because `C<C_star`, choose a positive rational `epsilon` with
`alpha<=1-epsilon`. Such a number can be certified by successively
refining the elementary-function intervals; no fixed precision is
assumed in this existence statement.

Choose

```math
\ell=\max\left(4,\left\lceil\frac{1}{693\epsilon}\right\rceil\right),
\qquad v=693\ell.
```

Take the admitted chronological tensor product of `v` raw units. If a
role's complete endpoint is `L_j F_K R_j`, apply `R_j^-1` to its
original arbitrary input, run the entire tensor word, and then apply
`L_j^-1` to its output. This gives `F_K` before completion; it does not
assume that the two matchers are inverses of one another. Every input
and output adapter remains charged. Now complete each rank `K<17^v`
to `17^v` by a paid positive transform on unused disjoint axes of that
same field. Retain any required external whole-job matchers. Split
every original and completion paid job into
consecutive disjoint pieces of rank at most `10^v`.

The source tensor/padding proof charges the complete paid moment by

```math
\frac{P_{\rm complete,t}}{T_t^v}
\le\alpha^v+2\beta^v+2\delta^v
<\frac{1}{1+v\epsilon}+\frac{4}{2^\ell}
\le\frac34<1.
```

Here Bernoulli's inequality gives the first term, `v epsilon>=1`, and
`ell>=4` controls the second. The new target moment is at least `T_t^v`.
Every completion and every split job has been paid; the positive
rank-one surplus remains `131723^v-131115^v`. The finite rule satisfies

```math
m=121^v,\qquad q=17^v,\qquad r_{\max}\le10^v<q<m.
```

No additional productive owner or free center is introduced. This rule
fits the exact strict compiler of the companion proof.

## 5. Explicit logarithmic compilation without enormous integer powers

Use `theta=61/75`, supported by `10^75<17^61`. Let

```math
b=7v,\qquad K=\left\lceil1+bC\right\rceil,\qquad \gamma=4K.
```

Since `121<2^7`, the ambient rank satisfies `m<2^b` without computing
the integer `121^v`. Also `1-C>1/2` and

```math
\eta=(1-C)m^{-C}>2^{-(1+bC)}\ge2^{-K}.
```

The small integer comparison `2*61^4<75^4` gives
`theta^gamma<2^-K<=eta`. The rank-one exit guard follows from
`theta>1/2` and `m>=121>16`. The companion's complete recurrence,
including every source complement and paid owned-bank call, therefore
has

```math
L(n)\le m^C n^{1-C}\max(1,\log n)^\gamma.
```

For any fixed rational `U<C`, select integers `H,J` with

```math
H\ge\max(b,2),\qquad H<2^J,\qquad H(C-U)>bC+\gamma J.
```

Then `N=2^H` has `L(N)<N^(1-U)`. The companion's increasing search
over `J` terminates, since its threshold for `H` is affine in `J` while
`2^J` grows exponentially. Only the encodings of `m,q,N` are needed.
The deliberately generous generic bounds do not claim an optimal
tensor power, potential, template rank or expanded word size.

## 6. The complete outer family and its quantifiers

The paid-floor companion already certifies the fixed point
`kappa_0=0.002686488`. For `0<kappa<=kappa_0`, that same fixed program
gives the weaker requested bound. Its historical comparison with an
earlier incumbent need not be asserted for the smaller requested
exponent.

For `kappa_0<kappa<C_star`, choose a rational `C` with
`kappa<C<C_star`. An effective choice examines
`C_j=kappa+2^-j`: whenever `C_j<C_cap`, compute a directed mixed
interval at precision increasing with `j`, and accept the first
strictly positive lower bound. Since `C_j` tends to `kappa` and
`M_(1-kappa)>0`, this search terminates. An inconclusive interval is
skipped; it does not freeze the search at a possible equality point.

Set `d=(C-kappa)/7` and retain the exact source family

```text
U=kappa+6*d, b_outer=kappa+5*d, a=kappa+4*d, q_outer=kappa+3*d,
epsilon_outer=1-d, beta_outer=1-3*d,
r0=d/10, stop=d, layout=d, ordinary_BIT_saving=0.0027.
```

The template constructed above funds precisely this `U`. The source
ledger supplies all nine outer cost savings, all 54 named strict
predicates, and all three additional functional guards.

The universal verification is symbolic, not a sampling argument. Write
`x=kappa-kappa_0` and expand that unchanged ledger over the polynomial
ring `Q[x,d]`. The actual cofinal triangle is contained in

```math
0\le x\le C_{\rm cap}-\kappa_0,\qquad
0<d\le(C_{\rm cap}-\kappa_0)/7.
```

The retained ledger has `sigma-tau=-d<0`, so its only symbolic
`max(sigma-tau,0)` branch is exactly zero.

For each of the 57 predicates, remove its common power of `d`. The
remaining polynomial has a strictly positive rational lower bound on
this rectangle. The checker computes that bound by retaining its
constant coefficient, discarding other positive terms, and replacing
each negative monomial by its value at both upper endpoints. Since
`d>0`, every original predicate is strictly positive. This includes the
historical comparison for the actual cofinal construction.

For example, the main cost exceeds `kappa` by `d(3-q_outer)`, the
global router by `4d`, the fused Gaussian cost by `d(4-3q_outer)`, and
the group BIT router by `d(5-3a)`. The checker records every polynomial
and lower bound, and checks the nine cost rows against their named
predicates. Thus the result is a full conditional outer range, rather
than a local supplier exponent.

Every resulting finite word has fresh constants: if `U_raw` is its
number of actual raw p7 invocations, allocate and charge `O=U_raw`
separately named centers. Let `W` be its productive width, `P` its final
paid rank-one count, and `R` every nonscalar native record and whole-job
route, including completion and splitting. Retain the source scalar
allowance and use

```text
G=2490856*U_raw+8*R, Z=W+O,
E=64*(Z+N+P+G+1)^3, B_constant=P+E,
C0=32*N*B_constant^2.
```

Actual coordinate movement is paid separately. These constants and
the template are fixed before the eventual input varies. The inherited
storage, precision, physical and analytic hypotheses remain premises.

The checker executes the generic construction at the further explicit
final point `kappa=0.002686489`:

| Parameter | Certified value |
| --- | --- |
| Tested saving `C` | `kappa+2^-35` |
| Raw ratio gap `epsilon` | `2^-35` |
| Tensor power `v` | 34,359,739,029 |
| Potential exponent `gamma` | 2,584,597,740 |
| Uniform saving `U` | `kappa+6/(7*2^35)` |
| Uniform rank `N` | `2^47400257013113900919251` |
| Rank-selection integer `J` | 76 |
| Strict final power gap | `42467/234881024000000000` |

Every one of its 57 outer predicates is checked again numerically over
the rationals. This very generous generic member demonstrates the
quantified construction. It does not claim a competitive template
rank; a tuned finite-power choice can be much smaller.

## 7. A precise ceiling for these mixed-moment certificates

Fix any `0<t<1` for which the raw mixed moment is nonpositive.
For every positive integer `v`,

```math
T_t^v-P_t^v\le0.
```

Completing a productive rank `K` by paying for `D>0` unused axes
changes the complete mixed moment by

```math
(K+D)^t-K^t-D^t<0.
```

The inequality is strict for positive `K,D`. Splitting a paid rank
`R=sum_i r_i` into positive pieces changes it by

```math
R^t-\sum_i r_i^t\le0.
```

Both facts follow from strict subadditivity of `x^t` for `0<t<1`.
Consequently no finite sequence of these paid completions and paid
splittings, after a tensor power of this fixed raw rule, restores a
positive complete mixed moment. The same sign argument permits
further tensor products of intermediate rules whose moments remain
nonpositive.

Section 2 proves that this obstruction holds for every
`C_star<=C<1`. At `C=C_star`, completing an actual all-five tensor
target from `5^v` to `17^v` already makes the moment strictly negative.
Such a target exists because the raw word has 420 rank-five productive
roles. Together with Sections 3–6, this identifies `C_star` as the
supremum of the strictly admitted outer savings in this particular
positive-moment certificate family. The endpoint is not attained by
the stated recipe. This says nothing stronger about other analyses
of the supplier or about integer multiplication in general.

## 8. Reproduction and attribution

With the exact #4416 contribution available in a separate source
checkout, run from this repository:

```bash
python3 research/kappa-4416-root-family/verify.py --source-root /path/to/pr4416 --check
```

The checker uses Python's standard library only. Every deciding
operation is rational or integer. Its elementary interval precision
can increase without a fixed cap. It replays the authenticated
companions, the raw sign enclosure, global signed decomposition,
uniform tangent and decay bounds, all 57 symbolic outer predicates,
and one explicit constructive family member. No tensor word or
astronomical ambient power is materialized.

The native supplier originates in zxv's #4359; the all-fresh p7 word,
chronological tensor and paid padding are retained from
1337isnot1337's #4416 and its #4412/#4414 predecessors. The exact
lockstep compiler is Jacob Alan Sussman's Theorem 1G. The outer
ledger retains #4405's attribution. Related logarithmic-potential
work in zxv's #4411 and the raw-root headroom in #4420 are credited
without priority claims. New material is Apache-2.0.

## 9. Open next questions

**Can a different raw native invoice exceed this root?** The relevant
first step is one exact controller factorization and complete native
invoice with positive mixed moment at `C=0.00268649`. A new candidate
must then pass the literal owner, phase, spectator and chronological
checks. The ceiling above rules out improving the fixed raw invoice by
the specified paid completion and splitting alone; it does not search
different native words. Admitting the retained all-column and physical
contracts remains a separate blocker.

**Can the same final saving use a smaller complete finite program?** A
feasible first step is to replace the deliberately coarse generic power
by a tuned finite power with both paid tails checked exactly, then
reselect the logarithmic template and recompute all outer constants.
Cutoff and target-floor choices should be assessed together. A reduction
in `H` alone does not control productive width, total instructions,
storage or movement, so those full-word counts remain part of the work.
