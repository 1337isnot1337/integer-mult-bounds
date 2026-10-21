# A generic logarithmic bound for weakly separated mixed units

The logarithmic compiler argument extends beyond the particular paid-rank
ratio below 2 used by the preceding native constructions. It applies to
every complete mixed-unit contract with a nonempty paid word,

```math
1\leq r_j\leq q:=\min k<m:=\max k,\qquad q\geq2,
```

provided at least one paid rank is strictly below `q` and a fixed rational
`0<t<1` has positive mixed surplus. All constants and the final sufficient
rank can be selected by terminating integer and rational searches.

The conclusion is about the ordinary paid-leaf count of the finite
compiler. A native implementation and its analytic transfer remain
separate requirements. In particular, a favorable rank histogram does
not supply arbitrary independent inputs, permitted adapters, or a native
operator identity.

## 1. Statement and complete contract

Let `W_k` be the positive integer multiplicities of the productive target
ranks. Let `(r_j,owner_j)` be a finite, nonempty chronological paid word.
Define

```math
T_a=\sum_k W_k k^a,\qquad P_a=\sum_j r_j^a.
```

Retain the complete contract in the source
[finite-precompilation argument](https://github.com/zxv/integer-mult-bounds/blob/da637c87c89482bc4c86be36bd0071b3d400dbed/research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md):
arbitrary independent productive fields; an all-column native word;
disjoint splitting that preserves complete spectators; permitted,
explicitly priced whole-job adapters; named physical owners for every
paid call; initialized and erased owned storage without productive
credit; and finite-program closure with the same scalar, restoration
and precision interface. Repeated paid ranks retain their multiplicities.
Paid calls on owned storage remain in `P_a`.

Assume

```math
2\leq q<m,\quad 1\leq r_j\leq q\text{ for every }j,
\quad r_j<q\text{ for at least one }j,
\quad 0<t<1,\quad T_t>P_t,
```

where `t` is fixed and rational. Use the checked
[weak interface](../kappa-4359-weak-compiler/verify.py) and the unchanged
source integer compiler. Let `L(n)` denote paid rank-one leaves per
productive full-rank array. Set `L(0)=0`; the ordinary base has `L(n)=n`
for `1<=n<m`.

**Theorem.** Explicit constants `n_0>=m`, `gamma>=1` and
`A=n_0^(1-t)` exist such that

```math
L(n)\leq A n^t\max(1,\log n)^\gamma\qquad(n\geq1).
```

For every fixed rational `z` with `t<z<1`, the construction below produces
integers `H,J` and a specified finite uniform supplier at `N=2^H` with

```math
L(N)=P_N/B_N<N^z.
```

Each fixed exponent and gap has its own finite program, physical cost
constants and eventual threshold. The theorem does not assert a bound
at `z=t`, a practical template size, or an unconditional multiplication
bound.

## 2. Exact flow facts under weak separation

For an integer `n>=m`, put `G=floor(log_q(n/m))`. A class at depth `d`
has dilation `rho`, the product of its first `d` paid ranks. Its units
have target multi-indices of degree `G-d`, with the multinomial
multiplicities in the source construction.

The weak inequality `r_j<=q` suffices for every parent-to-child fit:
replacing one target factor `k` by a paid rank changes the ambient
requirement by the factor `r_j/k<=1`. The exact Pascal identity then
consumes every parent job. Equality does not create a dependency cycle:
the child class completes one chronological round before the suspended
parents advance to the next round.

Every paid path of length `d<=G` has a nonempty class, since
`m*rho*q^(G-d)<=m*q^G<=n`. At depth `G`, the only multi-index is zero
and its multiplicity is one. Thus every ordered sequence of `G+1` paid
rounds contributes exactly one exit. For every real `a`, the complete
unnormalized exit moment is exactly

```math
E_a=P_a^{G+1}.
```

Every exit is at most `q^(G+1)<=qn/m<n`. Root sources exceed `n/m`
because a further target factor would have degree `G+1` and cannot fit.
In a nonroot class, a fresh source of rank `s` occurs only when the
corresponding parent unit does not fit. This implies
`m*s/r_j>n`, hence `s>n/m`. All sources also have `s<=n`.

Write `c_s` for source counts, `d_e` for exit counts, `S_0=sum c_s`, and
`S_a=sum c_s*s^a`. There is at least one root source, so `S_0>0`.
Canceling every internally matched job gives the exact identity

```math
S_a-E_a=(T_a-P_a)\sum_{\text{units }v}c(v)^a,
```

where `c(v)` is the unit's positive integral column count. In particular,
`S_t>E_t>0`; the final positivity uses the nonempty paid word. Clearing
each chronological batch denominator yields the exact leaf recurrence

```math
S_0L(n)=\sum_s c_sL(n-s)+\sum_e d_eL(e).
```

Every recursive rank is strictly smaller than `n`. Zero complements
vanish. The same integer batching, owned-field allocation and whole-job
adapter obligations as in the source proof remain charged.

## 3. Two useful bounds from the hypotheses

First, the rank-one surplus is automatically positive:

```math
T_1\geq q^{1-t}T_t>q^{1-t}P_t\geq P_1.
```

The recurrence and `E_1<=S_1` therefore give `L(n)<=n` for every `n` by
strong induction. This covers the entire finite range below the later
threshold `n_0`; it is not restricted to the compiler's original base.

Second, put

```math
R_t=\frac{P_{t+1}}{P_t},\qquad u=\frac{P_2}{P_1}.
```

Both denominators are positive, and `1<=u<q`. Indeed,
`P_2-qP_1=sum_j r_j(r_j-q)<0`. The rational number `u` uniformly bounds
`R_t` for `t<=1`. To see this, group equal paid ranks with counts `p_i`:

```math
P_2P_t-P_1P_{t+1}
=\sum_{i<j}p_ip_jr_ir_j(r_i-r_j)
  \bigl(r_j^{t-1}-r_i^{t-1}\bigr)\geq0.
```

The last inequality follows because `x^(t-1)` is nonincreasing. Thus
`R_t<=u<q`; no transcendental evaluation of the tilted mean is needed.

## 4. Entirely rational choices for the logarithmic estimate

Find the first integer `h>=2` with

```math
u^h<q^{h-1},
\qquad \alpha=1-\frac1h,
\qquad \theta=1-\frac1{2h}.
```

This search terminates because `(q/u)^h` tends to infinity. In particular,
`u<q^alpha` and `3/4<=theta<1`. Set `eta_0=t/m`; choose the first positive
integer `gamma` for which `theta^gamma<eta_0/2`. This search terminates
because `0<theta<1` and `eta_0>0`. Finally, set

```math
D=\left\lfloor\frac{2u}{\eta_0}\right\rfloor+1,
\qquad n_0=\max\bigl(m,16,D^{2h}\bigr).
```

Call an exit high when `e>n^theta`, and write `E_t^high` for its
unnormalized `t`-moment. The exact exit identity gives

```math
\begin{aligned}
\frac{E_t^{\rm high}}{S_t}
&\leq n^{-\theta}\frac{E_{t+1}}{E_t}
 =n^{-\theta}R_t^{G+1}\\
&\leq u\,m^{-\alpha}n^{-1/(2h)}
 \leq u\,n^{-1/(2h)}
 \leq\frac{u}{D}<\frac{\eta_0}{2}
 \qquad(n\geq n_0).
\end{aligned}
```

Let `psi(n)=max(1,log n)^gamma`. For `n>=n_0`, we have
`theta*log(n)>1`, since `n_0>=16`, `theta>=3/4`, and `log 2>1/2`.
This also covers a low exit of rank one. Every low exit satisfies
`psi(e)<=theta^gamma*psi(n)`, and every high exit satisfies
`psi(e)<=psi(n)`, since every exit is smaller than `n`. Consequently,

```math
\sum_e d_ee^t\psi(e)
\leq\psi(n)\bigl(\theta^\gamma E_t+E_t^{\rm high}\bigr)
<\eta_0S_t\psi(n).
```

The coarse sum of low and high bounds is sufficient; optimizing their
convex combination is not needed for this generic theorem.

## 5. Strong induction, including all small ranks

For `n/m<s<=n`, concavity gives

```math
n^t-(n-s)^t\geq t n^{t-1}s
\geq \eta s^t,
\qquad\eta=t m^{t-1}>\eta_0>0.
```

For `1<=n<n_0`, the earlier rank-one bound gives
`L(n)<=n<=n_0^(1-t)*n^t*psi(n)`. Set `A=n_0^(1-t)` and induct on
integer `n>=n_0`. Monotonicity of `psi` bounds every nonzero complement
using `psi(n)`. The exact recurrence, complement inequality and exit
estimate then imply

```math
\begin{aligned}
S_0L(n)
&\leq A\psi(n)\bigl(S_0n^t-\eta S_t+\eta_0 S_t\bigr)\\
&\leq A S_0 n^t\psi(n).
\end{aligned}
```

The rank-zero convention removes the only undefined logarithm. This
proves the global logarithmic estimate without replacing the actual
finite-range compiler by a different algorithm.

## 6. A terminating sufficient uniform-rank search

Let `b` be the binary bit length of `n_0`, so `n_0<2^b`. For the fixed
rational gap `delta=z-t>0`, try successive integers `J=1,2,...` and put

```math
H=\max\left(b,2^{J-1},
\left\lfloor\frac{b(1-t)+\gamma J}{\delta}\right\rfloor+1\right).
```

Accept when `H<2^J`. This test terminates: the third term grows linearly
in `J`, the first is fixed, and `2^J` eventually exceeds both. No fixed
cap on `J` is used. Since `H>=b>=5`, `log(2^H)>1`, and `log 2<1` gives

```math
A\bigl(\log(2^H)\bigr)^\gamma
<2^{b(1-t)+\gamma J}<2^{H(z-t)}.
```

Thus `N=2^H` is sufficient. The finite compiler defines its complete
integer word, even though this certificate does not materialize that
word.

The positive mixed hypothesis is also effectively certifiable for
rational `t=a/b_t`. Each `k^t` is the positive `b_t`-th root of the
integer `k^a`. Integer bisection gives directed dyadic intervals, which
can be refined until the strictly positive mixed margin is separated.
The companion checker includes this unbounded refinement. Termination
is asserted on the theorem's positive-margin inputs; the procedure is
not advertised as a total classifier for arbitrary equality cases.

## 7. A nontrivial exact instance

Take productive ranks `(9,16)`, paid ranks `(1,4,9)`, `t=1/2`, and
`z=3/4`. This formal complete-role example is not asserted to be a
native transform. Its exact parameters are

| Quantity | Value |
| --- | ---: |
| `q,m` | `9,16` |
| `T_t-P_t` | `1` |
| `T_1-P_1` | `11` |
| `R_t,u` | `6,7` |
| `h,theta` | `9,17/18` |
| `eta_0,gamma,D` | `1/32,73,449` |
| `n_0,b` | `449^18,159` |
| `A` | `449^9` |
| `H,J` | `3823,12` |
| `H(z-t)-b(1-t)-gamma*J` | `1/4` |

Here `r_max=q` and `R_t=6>2`, so the example exercises a regime outside
the earlier concrete tail bound. The checker verifies one actual
two-generation source/exit graph at rank `1296`, including an owned
paid field. All relevant square-root potentials are exact integers.
It compares the exit histogram against all ordered paid products and
checks the full source/exit cancellation at exponents `1/2`, `1`, and
`2`. The selected sufficient rank remains a mathematical specification.

## 8. Boundaries and verification

The assumption that some paid rank is below `q` has real force for the
literal compiler's global estimate. The companion
[boundary argument](BOUNDARY.md) considers productive ranks `(2,3)` and
two paid rank-2 calls. It has positive mixed `1/2`-surplus but
`L(2^k)>=phi^k`, where `phi=(1+sqrt(5))/2>sqrt(2)`. Thus no constants
`A,gamma` give this compiler the claimed global
`A*n^(1/2)*max(1,log n)^gamma` estimate. This is not a lower bound on
multiplication or an obstruction to every other supplier construction.

Other excluded cases have separate reasons. An empty paid word makes
the ratios undefined and is not accepted by the current compiler
interface. A target minimum of one makes its lattice enumeration
nonterminating. Paid ranks above `q` can fail the Pascal fitting step.
The boundary `q=m=r_max` can produce an exit of the current ambient
rank. The endpoints `t=0,1` are outside the stated positive-saving
argument. The theorem makes no necessity claim for every one of these
conditions; another construction can require different hypotheses.

```sh
python3 -B research/kappa-4359-generic-weak/verify.py \
  --source-root /absolute/path/to/pr4359-checkout --check
python3 -B research/kappa-4359-generic-weak/boundary_check.py \
  --source-root /absolute/path/to/pr4359-checkout --check
```

The standard-library checkers authenticate the frozen source compiler
and the weak interface. Their receipts bind the companion proofs and
discriminating arithmetic and rank-boundary controls. The universal
claim follows from the written flow, inequalities and termination
arguments, rather than from finitely many examples.

The source is PR
[#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359), pinned
at `da637c87c89482bc4c86be36bd0071b3d400dbed`. Its integer mixed flow uses
Jacob Alan Sussman's Theorem 1G in
[#4268](https://github.com/CrocSwap/integer-mult-bounds/pull/4268).
The preceding [weak-separation proof](../kappa-4359-weak-separation/PROOF.md)
introduced the exact paid-product exit identity and weighted-tail
argument used here. This package broadens that argument with a rational
mean bound, explicit generic constants and a delimited boundary.
New material is Apache-2.0.
