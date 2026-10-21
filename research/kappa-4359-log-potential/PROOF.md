# Smaller fixed templates from a logarithmic superpotential

This note replaces the quantitative rank argument in PR #4359. It retains
the same finite integer compiler, native words, productive jobs and paid
calls. At the original uniform savings, it reduces the specified ranks to

| Family | Uniform saving | Previous rank | New sufficient rank |
| --- | ---: | ---: | ---: |
| Complex | 0.002304 | `2^276540184361` | `2^2458275` |
| BIT, before covering | 0.002760 | `2^6552928412` | `2^463652` |

The new argument also certifies complex uniform saving `0.002305088` at
rank `2^1729137493`. The separate outer package uses this stronger uniform
saving. This note alone does not assert an integer-multiplication exponent.

The conditional dependency is PR
[#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359), commit
`da637c87c89482bc4c86be36bd0071b3d400dbed`, by zxv. Its finite compiler builds
on Jacob Alan Sussman's mixed lockstep construction, Theorem 1G in
[#4268](https://github.com/CrocSwap/integer-mult-bounds/pull/4268). Those
contributions supply the job construction and its native interfaces. The
change here is a sharper quantitative induction for its paid-leaf count.
New material is under Apache-2.0.

## 1. The exact compiler interface

Let `L(n)=P_n/B_n` be the number of paid rank-one calls per productive array
in the denominator-cleared uniform compiler. Set `L(0)=0`. For `n<m`, use
the ordinary program, so `L(n)=n`. Here `m` is the largest productive rank.
The other native ranks satisfy `1 <= r_max < k_min <= m`.

At each `n>=m`, the compiler supplies source weights `w_s`, exit counts
`x_e`, and the exact recurrence

```math
L(n)=\sum_s w_sL(n-s)+\sum_e x_eL(e),\qquad \sum_s w_s=1.
```

Every source is a distinct arbitrary array. Its complementary job is paid
in the first sum. Every exit, including a call on owned storage, is paid
in the second sum. Ordered integer batching changes the counts and source
width by the same factor. It does not change this recurrence.

For a rational exponent `0<t<1`, suppose the complete mixed tariff obeys

```math
\sum_j r_j^t<\sum_k W_k k^t.
```

Cancel every matched internal job in the finite flow. This gives

```math
\sum_e x_e e^t\leq\sum_s w_s s^t,\qquad n/m<s\leq n.
```

This implication uses the actual chronological job flow. A favorable
histogram alone does not establish the native operator contract. The
present proof retains that contract as a pinned dependency.

## 2. The exit bound has no extra multiplicative factor

Choose rational `theta` with `0<theta<1` and
`r_max < k_min^theta`. The integer checker verifies this by raising both
sides to the denominator of `theta`.

Let `G` be the deepest target generation in the compiler at rank `n`.
Then `m*k_min^G<=n`, and every exit has rank at most `r_max^(G+1)`. Thus

```math
e\leq r_{\max}^{G+1}
  <\left(k_{\min}^{G+1}\right)^\theta
  \leq\left(\frac{k_{\min}}m n\right)^\theta
  \leq n^\theta.
```

In particular, every exit is smaller than `n`. This bound follows directly
from the integer tree. It needs no asymptotic estimate of the largest
exit and introduces no prefactor such as 16.

## 3. Logarithmic superpotential

Choose rational `gamma>0` such that

```math
\theta^\gamma<\eta,
\qquad \eta=t\,m^{t-1}.
```

For positive integers, define

```math
\psi(n)=\max(1,\log n)^\gamma,
\qquad A=m^{1-t}.
```

All logarithms are natural. Assume `theta*log(m)>1`, as in the three
certified cases. At `n>=m`, the exit bound gives

```math
\max(1,\log e)\leq\theta\log n,
\qquad \psi(e)\leq\theta^\gamma\psi(n).
```

The maximum with 1 is necessary. It includes rank-one exits, whose
logarithm is zero. Every nonzero source complement satisfies
`psi(n-s)<=psi(n)`. Rank-zero terms vanish because `L(0)=0`.

For `u=s/n>=1/m`, concavity gives

```math
1-(1-u)^t\geq tu\geq t m^{t-1}u^t=\eta u^t.
```

Therefore the source complements leave a definite margin:

```math
n^t-\sum_s w_s(n-s)^t\geq\eta\sum_s w_s s^t.
```

Strong induction now proves the uniform bound

```math
L(n)\leq A n^t\psi(n).
```

For `1<=n<m`, this follows from `L(n)=n`, `n^(1-t)<=m^(1-t)`, and
`psi(n)>=1`. For `n>=m`, substitute the induction hypothesis in the exact
recurrence and use the preceding inequalities:

```math
\begin{aligned}
L(n)
&\leq A\psi(n)\left(
   \sum_s w_s(n-s)^t+\theta^\gamma\sum_e x_e e^t\right)\\
&\leq A\psi(n)\left(
   n^t-(\eta-\theta^\gamma)\sum_s w_s s^t\right)\\
&\leq A n^t\psi(n).
\end{aligned}
```

No free passes or scalar costs have been removed. The quantity being
bounded is the paid-leaf count of one fixed finite template. Its complete
scalar word, routing, owned-storage allocation and precision constants
remain part of the native supplier, as in PR #4359. They are fixed before
the eventual multiplication input grows.

## 4. Rational checks for the potential

Write `C=1-t`. For any proved rational upper bound `ell>log(m)`,
the inequality `exp(-x)>=1-x` gives

```math
\eta=(1-C)\exp(-C\log m)>(1-C)(1-C\ell)=\eta_{\rm low}.
```

The three cases use the following exact choices.

| Case | `C` | Uniform saving | `theta` | `gamma` | `ell` |
| --- | ---: | ---: | ---: | ---: | ---: |
| Complex, incumbent saving | 0.002305 | 0.002304 | 9/10 | 1/9 | 81/20 |
| BIT, incumbent saving | 0.002769 | 0.002760 | 15/16 | 7/32 | 4 |
| Complex, improved outer saving | 0.00230509 | 0.002305088 | 9/10 | 1/9 | 81/20 |

The checker encloses each logarithm with the positive atanh series. It
then verifies `theta^gamma<eta_low` using integer powers of rational
numbers. No floating-point comparison decides a certificate condition.
It also independently checks the mixed moments from the authenticated
native tariffs, using directed logarithm and exponential enclosures.

All cases have `m>=16` and `theta>1/2`. Since `log(2)>1/2`, they satisfy
`theta*log(m)>1`. This supplies the small-exit condition used above.

## 5. One explicit successful rank

Let `C_u<C` be the desired uniform saving and put `d=C-C_u>0`.
Choose positive integers `H,J,b` with `H>=b` and

```math
m<2^b,\qquad H<2^J,\qquad Hd>bC+\gamma J.
```

Set `N=2^H`. Since `m>=16`, the condition `H>=b` ensures `log(N)>1`,
so the maximum in `psi(N)` equals `log(N)`. Because `log(2)<1`,

```math
A\psi(N)=m^C(H\log2)^\gamma
 <2^{bC+\gamma J}
 <2^{Hd}=N^{C-C_u}.
```

Consequently

```math
\frac{P_N}{B_N}=L(N)<N^{1-C_u}.
```

The proof is effective. It selects an explicit integer `N` and invokes
the same finite, ordered, denominator-cleared compiler at that rank.
It does not wait for an unperformed search for the first successful word.

The certificate uses `b=6` in all cases:

| Case | `H` | `J` | Exact gap `Hd-bC-gamma*J` |
| --- | ---: | ---: | ---: |
| Complex, incumbent saving | 2,458,275 | 22 | 1/1,800,000 |
| BIT, incumbent saving | 463,652 | 19 | 1/250,000 |
| Complex, improved outer saving | 1,729,137,493 | 31 | 7/4,500,000,000 |

These are sufficient ranks, without a claim of optimality. The reductions
apply to `log2(N)`: approximately 112,493.6 times for the incumbent complex
saving and 14,133.3 times for the incumbent BIT saving. The full words
remain astronomically large. No instruction count, role count, owned
allocation or practical running time is inferred from these ratios.

## 6. Scope and reproduction

`verify.py` accepts `--source-root` pointing to a checkout of the pinned
PR #4359 source. It checks exact SHA-256 values before reading the tariffs.
The dependency is pending research, and it is not bundled into this
focused package. A missing or changed dependency fails the replay.

```sh
python3 -B research/kappa-4359-log-potential/verify.py \
  --source-root /absolute/path/to/pr4359-checkout --check
```

To regenerate a separate receipt, replace `--check` with
`--out /absolute/path/to/new-certificate.json`. The committed receipt also
binds this proof and its generator. The checker uses the Python standard
library only.

The inherited conditions remain substantive: arbitrary-input native
endpoints, complete spectators, permitted whole-job adapters, finite
chronological composition, restored owned storage, the delayed BIT cover,
and the outer movement, precision and analytic interfaces. This proof
does not independently establish them and is not a formal verification
of the multiplication theorem.

## Open next questions

1. Improve the sufficient rank without changing the native tariff. Start
   with the exact minimum of the complement ratio, then tighten `gamma`
   and the binary bound on `log(H)`. The present inequalities are enough
   for existence and are deliberately simple.
2. Reduce the actual compiled program size. Start by counting the merged
   source and exit flow at moderate ranks, preserving chronological
   batches. A smaller ambient rank alone does not bound the replication
   factor or the fully expanded word.
3. Strengthen the complex mixed tariff. Its root still limits the outer
   saving. A larger BIT saving alone cannot remove that constraint; a
   changed complex word needs a new native endpoint and ownership audit.
