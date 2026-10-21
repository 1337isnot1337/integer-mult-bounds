# Every strict saving below the changed native mixed root

Under the native and analytic hypotheses retained from PR #4359, the
width-five native word supports every rational multiplication saving

```math
0<\kappa<C_*,\qquad
C_*=0.002311660492818048695136925339\ldots.
```

The corresponding bound is

```math
T(n)=O\!\left(n(\log n)^{1-\kappa}\right).
```

The fixed program and its constants depend on the selected strict saving.
The endpoint itself is not attained by this argument.

This is a corollary of the frozen [weighted-tail proof](PROOF.md),
the [native deletion certificate](../kappa-4359-native-five/README.md),
and the [strict outer parameter family](../kappa-4359-outer-endpoint/README.md).
It extends the concrete point `kappa=0.00231165` without modifying the
frozen concrete proof or its numerical certificate.

## 1. The changed mixed root is unique

Use the complete native tariff

```text
productive targets: {5:102, 6:90, 7:56, 8:93, 9:1229, 25:448, 57:224}
paid calls:         {1:17521, 2:5065, 3:1738, 4:714, 5:254}.
```

Write

```math
M(C)=\sum_k W_k k^{1-C}-\sum_r p_r r^{1-C}.
```

Every target rank is at least 5 and every paid rank is at most 5.
For `t=1-C`, define

```math
F(t)=\sum_k W_k(k/5)^t-\sum_r p_r(r/5)^t.
```

Every term of `F` is nondecreasing in `t`. Terms with target rank above
5 are strictly increasing; terms with paid rank below 5 also increase
strictly after their minus sign is included. Hence `F` is continuous and
strictly increasing. Exact endpoint values are

```math
F(0)=2242-25292=-23050<0,\qquad F(1)=\frac{224}{5}>0.
```

There is therefore exactly one zero `t_*` in `(0,1)`. Set `C_*=1-t_*`.
Since `M(C)=5^(1-C) F(1-C)`, the complete mixed surplus is positive at
every `0<C<C_*` and negative at every `C_*<C<1`.

Directed rational evaluation gives the strict bracket

```math
0.002311660492818048695136925339
 < C_* <
0.002311660492818048695136925340.
```

Both bracket signs are recomputed independently by the endpoint checker.
In particular, `C_*<0.002312<0.0027`, where `0.0027` is the admitted
ordinary BIT saving retained from the predecessor.

## 2. The exit-tail estimate holds uniformly below the root

The weighted-tail proof requires `P_(t+1)/P_t<2`, where
`P_a=sum_r p_r r^a`. This inequality holds uniformly for `0<t<=1`.
Its proof uses only the paid invoice:

```math
\begin{aligned}
P_{t+1}-2P_t
 &= -17521+\sum_{r=3}^5 p_r(r-2)r^t\\
 &\leq -17521+1738\cdot3+714\cdot2\cdot4+254\cdot3\cdot5\\
 &= -2785<0.
\end{aligned}
```

The rank-two coefficient is zero. Every remaining positive term is
bounded using `r^t<=r`. Equivalently, the integer check at `t=1` is
`P_2-2P_1=71197-2*36991=-2785`.

All structural constants in the tail proof are independent of `C`:

```math
q=5,\quad m=57,\quad \theta=\frac34,\quad
\gamma=\frac1{20},\quad 2^2<5,\quad 57^3>16^4.
```

The exact exit identity `E_a=P_a^(G+1)`, with
`G=floor(log_5(n/57))`, therefore gives the same high-exit fraction
strictly below `1/8` at every `n>=57`. The low/high convex combination
is strictly below `4047/4096`, as in the concrete proof.

It remains to make the complement margin uniform. Put `C_bar=0.002312`.
For `0<C<C_*<C_bar`, the two positive factors in

```math
(1-C)\left(1-\frac{81}{20}C\right)
```

both exceed their values at `C_bar`. The exact comparison is

```math
(1-C_{\rm bar})\left(1-\frac{81}{20}C_{\rm bar}\right)
 -\frac{4047}{4096}
 =\frac{1544696341}{5000000000000}>0.
```

Since `log(57)<81/20`, the actual margin
`eta=(1-C)57^(-C)` exceeds this rational lower bound. Thus every strict
mixed saving below `C_*` satisfies the same logarithmic induction:

```math
L(n)\leq57^C n^{1-C}\max(1,\log n)^{1/20}
\qquad(n\geq1).
```

The source complements, arbitrary productive fields, owned-center calls,
chronological batching, all-column interpretation and native adapters
remain exactly those required in the core proof. The uniform inequality
does not remove any of those obligations.

## 3. Every strict uniform saving has an effectively specified template

Fix rational `0<U<C<C_*`. Let `d=C-U>0`. It suffices to choose integers
`H>=6` and `J` such that

```math
H<2^J,\qquad Hd>6C+\frac J{20}.
```

Then `N=2^H` satisfies `L(N)<N^(1-U)`. An explicit search tries successive
positive integers `J`, defines

```math
H=\max\left(6,\ 2^{J-1},
\left\lfloor\frac{6C+J/20}{d}\right\rfloor+1\right),
```

and stops once `H<2^J`. The search has no fixed upper bound on `J`.
It terminates because `2^J d` eventually exceeds the displayed linear
function of `J`. This matters for savings chosen arbitrarily close to
the root: a finite search cap is sufficient for the concrete receipt,
but cannot establish the entire strict family.

The denominator-cleared compiler at the selected rank defines a finite
program. Its actual replication, leaf, scalar, movement and owned-storage
counts determine its own precision and layout constants. Those constants
are fixed before the input length varies; they are not replaced by caps
from an earlier template.

## 4. Apply the strict outer parameter family

For any rational `0<kappa<C_*`, choose a rational `c` with
`kappa<c<C_*`. Set `d=(c-kappa)/5` and use

| Parameter | Exact choice |
| --- | --- |
| Tested native mixed saving | `c` |
| Compiled complex uniform saving | `U=c-d` |
| Selected complex saving | `b=c-2d` |
| Effective common saving | `a=c-3d` |
| Outer transform parameter | `q_outer=c-4d` |
| Global dimension exponent | `epsilon=1-d` |
| Group exponent | `beta=1-3d` |
| Stopping exponent | `d` |
| Precision spare power and layout slack | `d/4` |

The preceding section supplies the required uniform program at `U`.
The ordinary BIT saving exceeds `c`, and `c<1/32`. These are exactly
the supplier inputs of the previously proved outer parameter family.
Its strict supplier differences all equal `d`; its minimum outer saving
has margin

```math
(1-d)q_{\rm outer}-\kappa=d(1-q_{\rm outer})>0.
```

Every other retained outer cost is larger. The positive precision powers
`1-epsilon=d`, `1-beta=3d`, and `1-epsilon-d/4=3d/4` absorb the constants
of the newly selected finite template after increasing the eventual
input threshold. This establishes the claimed strict saving for each
fixed rational `kappa<C_*`.

The implicit constant in the bound and its eventual input threshold may
depend on that fixed `kappa`. All parameters remain fixed as `n` tends
to infinity.

This corollary preserves all source-bound native and outer analytic
hypotheses. It does not assert an unconditional multiplication theorem,
formal verification of the inherited premises, one program attaining
`C_*`, or practical sizes for the fixed templates.

## Reproduction and provenance

```sh
python3 -B research/kappa-4359-weak-separation/endpoint_verify.py \
  --source-root /absolute/path/to/pr4359-checkout --check
```

The checker authenticates the frozen concrete proof and receipt, the
native deletion and weak interface, and the earlier outer-family source.
It replays the concrete arithmetic, verifies both endpoint signs, and
checks the uniform integer inequalities above. It also compares literal
equality-case exit histograms with all ordered paid-round products at
generation depths zero through four. The general quantified conclusion
uses the written monotonicity, induction, unbounded-search and outer-family
arguments; finite numerical tests alone are not a proof of that conclusion.

The predecessor is PR
[#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359), commit
`da637c87c89482bc4c86be36bd0071b3d400dbed`. The finite mixed flow derives
from Jacob Alan Sussman's Theorem 1G in
[#4268](https://github.com/CrocSwap/integer-mult-bounds/pull/4268).
The native word and outer equations retain the contributor notices of
their respective source packages. New material is Apache-2.0.

The next route to a higher exponent is a further complete native tariff
improvement. Tightening the same exit-tail or rank inequalities can reduce
finite template sizes, but does not move this tariff's unique mixed root.
