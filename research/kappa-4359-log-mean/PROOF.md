# A smaller finite template from the mean logarithmic exit rank

The repacked native construction admits the same uniform saving
$U=0.002312848$ at the smaller specified ambient rank

$$
N=2^{206938551}.
$$

The previous weighted-tail certificate used $2^{756938551}$ at this
same saving. The new estimate preserves the entire native invoice,
actual paid owners, source complements and conditional outer hypotheses.
It changes the sufficient finite template and therefore uses the complete
constants of that new fixed compiled word.

With the unchanged rational outer parameters, it still supports
$T(n)=O(n(\log n)^{1-0.00231284})$ under the inherited hypotheses.
The local mixed root remains the root already certified by the
[native packing](../kappa-4359-native-packing/README.md). This note
improves the uniformization estimate; it adds no productive credit.
New material is Apache-2.0.

## 1. Authenticated source and exit recurrence

Use the native word, actual weak compiler and exact source/exit identity
authenticated and replayed by the frozen
[packed-tail package](../kappa-4359-packed-tail/PROOF.md). The predecessor
is PR #4359 at da637c87c89482bc4c86be36bd0071b3d400dbed.
The complete invoice is

    targets = {5:140, 6:52, 7:56, 8:93, 9:1229, 25:448, 57:224}
    paid    = {1:17559, 2:5027, 3:1738, 4:714, 5:254}.

Write $m=57$, $q=5$, $t=1-C$, with a positive strict mixed test
$0<C<C_*$, and

$$
P_a=\sum_r p_r r^a,\qquad
G=\left\lfloor\log_5(n/57)\right\rfloor.
$$

For $n\ge57$, every source has rank $s$ in $(n/57,n]$ and every exit
has rank $e<n$. All ordered paid paths occur, with full multiplicity,
including calls on the uncredited owned center. Their exact exit
moment is

$$
E_a=\sum_e E_e e^a=P_a^{G+1}.
$$

If $W_t=\sum_s S_s s^t$ is the complete source potential, cancellation
and the strict mixed inequality give $E_t\le W_t$. The paid-leaf
recurrence includes both all exits and the complementary job of rank
$n-s$ for every source. This note does not change that recurrence.
Write $B_n=\sum_s S_s$ for this unreplicated source count. Clearing
integer batch denominators scales the source width and its complete
leaf bill together; all flow counts in the induction below use the
unreplicated normalization.

## 2. Two applications of concavity

Set $\ell(n)=1+\log n$ for $n\ge1$, and choose $0<\gamma\le1$.
Normalize the exit weights by $E_t$. The exact paid-product identity
gives their mean logarithmic rank:

$$
\frac{\sum_e E_e e^t\log e}{E_t}
=(G+1)\mu_t,\qquad
\mu_t=\frac{\sum_r p_r r^t\log r}{P_t}.
$$

This follows either by differentiating the finite moment identity or
by summing the logarithms over each ordered paid path. Jensen's
inequality for the concave function $x^\gamma$ now gives

$$
\sum_e E_e e^t\ell(e)^\gamma
\le E_t\left(1+(G+1)\mu_t\right)^\gamma.                 \tag{1}
$$

Jensen's inequality for $\log$ separately gives

$$
\mu_t\le\log\frac{P_{t+1}}{P_t}.
$$

The complete paid invoice has the uniform exact inequality

$$
\begin{aligned}
P_{t+1}-2P_t
&=-17559+1738\,3^t+1428\,4^t+762\,5^t\\
&\le-17559+5214+5712+3810=-2823<0
\end{aligned}
$$

for every $0<t\le1$. Thus $\mu_t<\log2$. Rank-one exits cause no
exception: their logarithm is zero and their value of $\ell$ is one.

Take $\theta=7/16$. The integer comparison $2^{16}<5^7$ proves
$\log2/\log5<\theta$. Also $\log2<3/4$ and $\log57>3$, so

$$
1+\log2<7/4<\theta(1+\log57).
$$

For every $n\ge57$, the nonnegative quantity $\log(n/57)$ then gives

$$
\begin{aligned}
1+(G+1)\mu_t
&<1+\log2+\frac{\log2}{\log5}\log(n/57)\\
&<\theta(1+\log57)+\theta\log(n/57)
=\theta\ell(n).
\end{aligned}
$$

Together with (1) and $E_t\le W_t$, this proves the complete exit
estimate

$$
\sum_e E_e e^t\ell(e)^\gamma
<W_t\theta^\gamma\ell(n)^\gamma.                       \tag{2}
$$

Both concavity steps have their stated range. In particular, this
argument does not extend Jensen's $x^\gamma$ step to $\gamma>1$.

## 3. Source complements and the global induction

For each source rank $s>n/57$, concavity gives

$$
n^t-(n-s)^t\ge t n^{t-1}s
\ge \eta s^t,\qquad \eta=t57^{t-1}.
$$

Use the rational cap $\overline C=0.00232>C_*$. Since
$\log57<81/20$ and $e^{-x}\ge1-x$,

$$
\eta=(1-C)57^{-C}>
\eta_0=(1-\overline C)(1-(81/20)\overline C)
=\frac{3088455621}{3125000000}>0.
$$

The exact rational comparison

$$
\eta_0^{70}>\frac7{16}
$$

therefore permits $\gamma=1/70$, with
$\theta^\gamma<\eta_0<\eta$, uniformly for every strict mixed test
$0<C<C_*$. The verifier compares these rational powers directly.

Let $A=57^C$. For $1\le n<57$, the ordinary scalar base
$L(n)=n$ satisfies $L(n)\le A n^t\ell(n)^\gamma$.
Set $L(0)=0$, so a zero source complement contributes zero.
For the strong-induction step, every child rank is smaller than $n$.
Bound the complement logarithms by $\ell(n)$ and apply (2) to the exits.
The complete normalized recurrence then gives

$$
\begin{aligned}
B_n L(n)
&\le A\ell(n)^\gamma
\left(\sum_s S_s(n-s)^t+\theta^\gamma W_t\right)\\
&\le A\ell(n)^\gamma
\left(B_n n^t-(\eta-\theta^\gamma)W_t\right)
\le A B_n n^t\ell(n)^\gamma.
\end{aligned}
$$

Consequently

$$
\boxed{L(n)\le57^C n^{1-C}(1+\log n)^{1/70}
\quad(n\ge1).}
$$

Every source complement and owned-field paid call is still charged.
The finite integer compiler and its chronological batching are unchanged.

## 4. Explicit rank and the outer ledger

For $N=2^H$ with $H\ge6$, $\log2<3/4$ gives
$1+\log N<H$. Also $57<2^6$. If $H<2^J$, it suffices that

$$
H(C-U)>6C+J/70.
$$

At $C=0.00231285$ and $U=0.002312848$, take

$$
H=206938551,\qquad J=28.
$$

The exact checks are

$$
H<2^{28},\qquad
H(C-U)-6C-\frac{28}{70}=\frac1{500000000}>0.
$$

Thus $L(N)<N^{1-U}$ for the specified smaller template.
For every fixed rational $0<U<C<C_*$, the same proof admits the
unbounded search

$$
H=\max\left(6,2^{J-1},
\left\lfloor\frac{6C+J/70}{C-U}\right\rfloor+1\right),
\qquad H<2^J.
$$

Try successive positive integers $J$. Exponential growth dominates the
linear numerator, so the search terminates for every fixed positive gap.

The outer parameters still use $\kappa=0.00231284$,
$d=(C-\kappa)/5=0.000000002$, $U=C-d$,
$b=C-2d$, $a=C-3d$, $q_{\rm outer}=C-4d$,
$\epsilon=1-d$, and $\beta=1-3d$.
The checker recomputes all direct inequalities, all 63 inherited
predicates and all nine outer cost rows. The limiting main saving is
0.002312841995374316, with positive slack 0.000000001995374316.

The newly specified word needs its own full scalar, movement, storage,
precision and row-stock constants in the inherited generic formulas.
Those constants are finite and fixed before input length varies; the
earlier numerical caps are not substituted. The hypotheses of the
original native/all-column, analytic, fixed-tape and exact-recovery
interfaces remain in force. The huge winning word is specified by the
finite algorithm and is not materialized. No practical runtime or
attainment of $C_*$ is claimed.

## Reproduction

From the contribution checkout, with the pinned predecessor available
separately:

    python3 -B research/kappa-4359-log-mean/verify.py --source-root /path/to/pinned-pr4359 --check

The checker authenticates and replays the frozen packed-tail package,
including its actual native and compiler dependencies, before applying
the new exact logarithmic inequalities and outer cross-check.
