# A smaller fixed template for PR #4416

The conditional saving in [PR #4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416)
is `kappa = 0.00268647`. This note preserves that saving and every native,
tensor, completion, splitting and outer parameter. It changes the bound
used to select the final uniform rank.

| Quantity | PR #4416 | This note |
| --- | ---: | ---: |
| Tested complex saving `C` | 0.00268648 | 0.00268648 |
| Uniform complex saving `U` | 376107/140000000 | 376107/140000000 |
| Final conditional saving `kappa` | 0.00268647 | 0.00268647 |
| Tensor power | 6,240 | 6,240 |
| Target floor | `11^6240` | `11^6240` |
| Paid cutoff | `10^6240` | `10^6240` |
| Sufficient uniform rank `N` | `2^16201843136005340321` | `2^66091190261265` |

The reduction is about 245,143.8 in `log2(N)`. It is not a bound on the
ratio of expanded instruction counts or running times. Both programs
remain far beyond materialization.

The exact dependency is commit
[`e9058860b5c850760fdf970e796a96aefcdb1d98`](https://github.com/1337isnot1337/integer-mult-bounds/tree/e9058860b5c850760fdf970e796a96aefcdb1d98/research/pr4359-p7-padding)
of `1337isnot1337/integer-mult-bounds`. Its p7 native construction and
paid target completion are retained in full. Its finite compiler comes
from zxv's PR #4359 and Jacob Alan Sussman's mixed lockstep construction,
Theorem 1G in PR #4268. The outer parameter family is retained from
PR #4405. Related [PR #4411](https://github.com/CrocSwap/integer-mult-bounds/pull/4411)
uses a logarithmic potential for the original PR #4359 suppliers. The
present contribution applies that method to the much larger tensor rule
in PR #4416, with a new exact rank certificate. New material is under
Apache-2.0.

## 1. What the source replay establishes

The checker authenticates all 41 files added by the pinned PR #4416. It
then executes its complete verifier and reproduces its saved result. This
reconstructs the p7 native invoice, checks its Laurent factorization and
physical contacts, checks both charged tensor tails, and reevaluates the
current outer ledger. Authentication occurs before any source is imported.

The raw p7 rule has ambient rank 121, 7,688 productive fields and 55,998
paid calls. Its rank-one moments are 131,723 and 131,115. Its minimum
target is five and its maximum paid rank is 48. Thus the strict compiler
does not apply directly to this raw rule. The completion and splitting
steps in PR #4416 remain necessary for the argument given here.

There is a concrete obstruction to merely relaxing the raw compiler's
rank guard. At `n=121*5=605`, its deepest target generation is one.
The root class has 420 units at the rank-five target point. Any rank-eight
paid round emits a rank-40 job, but its next class has dilation eight and
`floor(605/(121*8))=0`. That class has no target point and cannot consume
the incoming jobs. This is a failure of that literal routing recipe;
it does not rule out another native compilation method.

The pinned chronological tensor construction takes `v=6240` copies,
completes every target below `11^v` on disjoint axes of its existing
arbitrary owner, and splits every paid job at `10^v`. This includes the
extra paid completion jobs. Completion runs after the entire tensor word.
No center bank or copied input receives productive output credit.

For `t=1-C`, the source proves that the complete paid moment, divided by
the raw tensor target moment, is less than

```math
\frac{1}{1+6240/10^8}+\frac{4}{2^{16}}
 =\frac{10240625039}{10240638976}<1.
```

The new target moment is at least the raw tensor target moment. Hence
the completed and split finite rule has strict positive mixed `t`-moment.
Its rank-one surplus is `131723^6240-131115^6240>0`, because completion
adds equal paid and productive rank, and splitting preserves paid rank.
Its ranks satisfy

```math
m=121^{6240},\qquad q=11^{6240},\qquad 1\le r_{\max}\le10^{6240}<q<m.
```

These exact finite checks retain substantive native premises. They do
not formally verify arbitrary column multiplicity, complete spectators,
whole-job adapters, tape implementations, semantic precision, or analytic
recovery. The tensor product acts on distinct physical owners at each
fixed paid position. It requires the stated all-column native contract;
repetition of scalar rank-one copies would not provide that contract.

## 2. The exact finite compiler recurrence

Consider any admitted finite mixed rule with integer ranks
`1 <= r_max < q <= m`. Assume the all-column, whole-job, spectator,
owned-storage and finite-composition hypotheses in the pinned
[finite precompilation proof](https://github.com/1337isnot1337/integer-mult-bounds/blob/e9058860b5c850760fdf970e796a96aefcdb1d98/research/pr4359-p7-padding/source/research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md).
Let `0<t<1` and suppose its complete mixed `t`-moment is strictly positive.

At integer rank `n`, let `L(n)=P_n/B_n` be its final paid rank-one calls
per productive array, after the compiler has cleared all batch
denominators. Set `L(0)=0`; for `1<=n<m`, choose the ordinary program
`L(n)=n`.

For `n>=m`, first consider the unreplicated finite integer flow. Let `S_s`
be its number of sources of rank `s`, and set `S=sum_s S_s`. Let `E_e`
be its complete exit count at rank `e`, including paid calls on owned
storage. Write

```math
w_s=S_s/S,\qquad x_e=E_e/S.
```

The denominator-clearing factor `a` gives productive width `B_n=a*S`.
It multiplies the whole paid bill by the same factor. Each source array
first receives its disjoint complement. Every chronological exit batch
then receives its smaller uniform program before the suspended parent
resumes. Thus the exact normalized recurrence is

```math
L(n)=\sum_s w_sL(n-s)+\sum_e x_eL(e),\qquad \sum_s w_s=1.
```

Every source satisfies `n/m<s<=n`. Summing the strict mixed balance over
all actual units, and canceling every matched internal job, gives

```math
\sum_e x_e e^t\le\sum_s w_s s^t.
```

The finite chronological job flow supplies this inequality. A favorable
histogram without its physical interpretation is insufficient. No scalar
pass or array route has been converted into free productive work.

## 3. A strict logarithmic majorant

Choose `0<theta<1` with `r_max<q^theta`. For the integer compiler,
`G=floor(log_q(n/m))` is the deepest target generation. Every exit rank
is at most `r_max^(G+1)`. Therefore

```math
e\le r_{\max}^{G+1}
 <q^{\theta(G+1)}
 \le\left(\frac{q}{m}n\right)^\theta
 \le n^\theta<n.
```

There is no multiplicative prefactor in this exit bound. Source
complements also have smaller rank than `n`.

Assume `theta*log(m)>1`. Choose a positive integer `g` for which

```math
\theta^g<\eta,\qquad \eta=t\,m^{t-1}.
```

For positive integers define

```math
\psi(n)=\max(1,\log n)^g,\qquad A=m^{1-t}.
```

All logarithms are natural. The maximum includes rank-one exits. For
`n>=m`, the exit bound and the assumption on `theta*log(m)` imply

```math
\psi(e)\le\theta^g\psi(n).
```

For a source with `u=s/n>1/m`, concavity gives

```math
1-(1-u)^t\ge tu\ge t m^{t-1}u^t=\eta u^t.
```

Consequently

```math
n^t-\sum_s w_s(n-s)^t\ge\eta\sum_s w_s s^t.
```

Strong induction now proves, for every positive integer `n`,

```math
L(n)\le A n^t\psi(n).
```

For `n<m`, use `L(n)=n`, `n^(1-t)<=m^(1-t)` and `psi(n)>=1`. For
`n>=m`, substitute the induction hypothesis in the complete recurrence:

```math
\begin{aligned}
L(n)
&\le A\psi(n)\left(\sum_s w_s(n-s)^t+
                    \theta^g\sum_e x_e e^t\right)\\
&\le A\psi(n)\left(n^t-(\eta-\theta^g)\sum_s w_s s^t\right)\\
&\le A n^t\psi(n).
\end{aligned}
```

Zero-rank complements vanish. This argument uses monotonicity of `psi`,
not concavity of its exponent. In particular, `g` can exceed one. That
distinction matters here: the large tensor dimension makes `eta` very
small, so a potential suitable for the original small p3 rule would fail.

## 4. Exact constants for the pinned tensor rule

The integer inequality `10^26<11^25` supplies `theta=25/26`. Also
`m>=121>16` and `theta>1/2`. The elementary bound `log(2)>1/2`
therefore gives `theta*log(m)>1`.

Put `C=0.00268648`. The desired potential comparison is equivalent to

```math
g\log(26/25)>6240C\log(121)-\log(1-C).
```

The verifier encloses every logarithm by rational arithmetic. To compute
`log(x)`, first write `x=2^k y` with `1<=y<2`. For
`z=(y-1)/(y+1)`, use

```math
\log y=2\sum_{j=0}^{M-1}\frac{z^{2j+1}}{2j+1}+R_M,
\quad 0\le R_M\le
\frac{2z^{2M+1}}{(2M+1)(1-z^2)}.
```

The same formula at `y=2` encloses `log(2)`. Signed multiplication by
`k` preserves the appropriate interval endpoints. The present case uses
128 terms; no floating-point number decides a condition.

The integer `g=2050` gives a certified logarithmic margin greater than
`0.00488866717`. The checker also proves that `g=2049` fails this same
potential comparison. This is a check of the stated sufficient method,
not an optimality claim about templates.

Computing the bit length of the exact integer `121^6240` gives

```math
2^{43173}\le m<2^{43174}.
```

Set `b=43174`. Here `b` is the binary ambient bound; it is unrelated to
the outer parameter also named `b` in the retained ledger.

## 5. An explicit uniform rank and finite search

Let `U<C` be a fixed desired uniform saving and `d=C-U>0`. If positive
integers `H,J` satisfy

```math
H\ge\max(b,2),\qquad H<2^J,\qquad Hd>bC+gJ,
```

then `N=2^H>=m` has

```math
A\psi(N)=m^C(H\log2)^g
 <2^{bC+gJ}<N^{C-U}.
```

Thus `L(N)<N^(1-U)`. One terminating selection rule is to increase `J`
through the positive integers and set

```math
H_J=\max\left(b,2,2^{J-1},
              \left\lfloor\frac{bC+gJ}{C-U}\right\rfloor+1\right).
```

Accept the first `J` with `H_J<2^J`. The nonexponential entries grow at
most linearly in `J`, so the search terminates. It has no fixed iteration
cap. Every input and program is fixed before the eventual multiplication
input varies; this does not allow `U` to approach `C` with that input.

For the unchanged PR #4416 point,

```math
U=\frac{376107}{140000000},\qquad C-U=\frac1{700000000},
\qquad J=46,\quad H=66091190261265.
```

The strict power margin is exactly

```math
H(C-U)-43174C-2050\cdot46=\frac1{700000000}.
```

The previous integer `H-1` gives equality and fails the strict test.
The previous logarithmic bin `J=45` also fails the stated selection rule.
These controls do not show that no other potential or template is smaller.

## 6. The same outer endpoint with fresh full-word constants

The uniform supplier still has the same strict saving `U`. Therefore
the source outer family is unchanged:

```math
\begin{gathered}
\kappa=0.00268647,\quad d=(C-\kappa)/7=1/700000000,\\
U=\kappa+6d,\quad b_{\rm outer}=\kappa+5d,\quad
a=\kappa+4d,\quad q_{\rm outer}=\kappa+3d,\\
\epsilon=1-d,\quad\beta=1-3d,\quad r_0=d/10,\quad
\operatorname{stop}=\operatorname{layout}=d.
\end{gathered}
```

The ordinary BIT saving remains `0.0027`. Full replay reevaluates all
nine cost rows, all 54 strict predicates and all three functional
predicates. The least final cost margin above `kappa` remains
`524529867/122500000000000000>0`. This gives the same proposed conditional
bound `T(n)=O(n (log n)^(1-kappa))` under the inherited premises.

Choosing a new uniform rank changes the expanded word. Its constants
must be defined from that new word. Expand the exact tensor, completion,
splitting and denominator-cleared compiler recipes at this note's `N`.
Let `U_raw` count all raw p7 instances, and allocate `O=U_raw` distinct
owned center banks. Let `W` be final productive width, `P` final rank-one
paid count, and `R` the full nonscalar record and normalizer count.
Retain each center until its actual unit clears it. Counting product
macros alone would undercount owned banks.

With the authenticated raw scalar allowance `S_raw=2490856`, the source
envelope formulas become

```math
\begin{gathered}
G=S_{\rm raw}U_{\rm raw}+8R,\qquad Z=W+O,\\
E=64(Z+N+P+G+1)^3,\qquad B_{\rm cost}=P+E,\qquad
C_0=32N B_{\rm cost}^{2}.
\end{gathered}
```

All coordinate movement and actual routes are paid separately. The
completed-child recurrence retains
`A(e)<=A(floor(e/N))+P*floor(e/N)+E`, giving
`A(e)<=2*B_cost*e` as in the source precision argument. No numerical
constant for the older, larger uniform word is silently reused. The new
finite widths, denominators, coefficient envelopes and prefix norms are
absorbed using the unchanged strict outer margins and inherited native,
precision, analytic, fixed-tape and recovery premises.

The checker certifies the finite recipe and inequalities. It does not
materialize `N`, the tensor word or the final compiled word, and it does
not formally prove the full multiplication theorem. The lower bound on
the saving remains conditional in exactly the sense stated by PR #4416.

## 7. Reproduction and reusable functions

This focused package does not duplicate PR #4416's 41 added files.
Provide a checkout of its pinned head, or the same repository-shaped
export, as the external source root:

```sh
python3 -I -O -B research/kappa-4416-log-template/verify.py \
  --source-root /absolute/path/to/pr4416-checkout --check
```

For a separate fresh receipt, replace `--check` with
`--out /absolute/path/to/new-certificate.json`. The default source root
is the enclosing repository. Missing or altered dependency files fail
before import. The checker also binds this proof and its own source.
It uses the Python standard library only.

`authenticated_source(source_root)` authenticates and replays the full
source result. `build(source_root)` includes that result under
`source_replay`. The reusable `derive_template` function accepts the
ambient base, target floor, paid cutoff, tensor power, tested and uniform
savings, and a rational exit exponent. It proves its own separation,
logarithmic and rank inequalities. It does not supply a changed native
moment or physical construction: a future caller must separately certify
those inputs before using the general theorem.
