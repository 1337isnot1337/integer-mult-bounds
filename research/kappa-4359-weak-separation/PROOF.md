# Finite compilation when a paid rank equals the smallest target

The strict separation condition in PR #4359 is sufficient, but its
pointwise bound on the largest exit is stronger than this construction
needs. A bound on the weighted fraction of large exits allows the
smallest target rank and largest paid rank both to equal 5.

This permits removal of all 102 rank-one completions that promoted fresh
width-five productive helpers to rank six. Their native endpoints already
compute rank-five jobs. The complete resulting tariff is

```text
productive targets: {5:102, 6:90, 7:56, 8:93, 9:1229, 25:448, 57:224}
paid calls:         {1:17521, 2:5065, 3:1738, 4:714, 5:254}
```

The native deletion is authenticated separately in
`../kappa-4359-native-five/CERTIFICATE.json`. This note proves a finite
compiler theorem applicable to that tariff. Its exact certificate uses
mixed saving `C=0.00231166` and certifies uniform saving `0.002311658`
at the fixed rank

```math
N=2^{756934981}.
```

This is a conditional native supplier statement. The separate outer
transfer determines the resulting integer-multiplication saving.

The source construction is zxv's PR
[#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359), pinned
at `da637c87c89482bc4c86be36bd0071b3d400dbed`. Its integer flow derives
from Jacob Alan Sussman's Theorem 1G in
[#4268](https://github.com/CrocSwap/integer-mult-bounds/pull/4268).
The logarithmic paid-leaf argument in `../kappa-4359-log-potential/`
supplies the quantitative method used here. New material is Apache-2.0.

## 1. The finite flow still exists and terminates

Let `m` be the largest productive target rank and `q` the smallest.
Assume

```math
1\leq r_j\leq q,\qquad 2\leq q<m.
```

The chronological unit, arbitrary productive inputs, complete spectators,
permitted whole-job adapters and owned-storage contracts are unchanged.
Only the strict inequality between `r_j` and `q` is weakened. In the
present native word, `q=5` and `m=57`.

At top rank `n>=m`, the target lattice has

```math
G=\left\lfloor\log_q(n/m)\right\rfloor
```

generations. The original Pascal matching remains valid. A parent unit
at lattice point `b` fits when `m*rho*c(b)<=n`. For a child fed by paid
rank `r_j` and target type `k`,

```math
m\rho r_j c(b-e_k)
   =m\rho c(b)\frac{r_j}{k}\leq n.
```

The proof requires `r_j<=k`, so equality is allowed. The child still has
one less target generation. Its other inputs are distinct fresh sources.
Round labels retain the same lockstep execution order; jobs from a later
round are never used to satisfy an earlier suspended round.

All sources retain the band `n/m<s<=n`. Every exit satisfies

```math
e\leq q^{G+1}\leq\frac qm n<n.
```

Every source complement has rank below `n` as well. Consequently the
denominator-cleared compiler still terminates by strong induction on
the integer rank. Its normalized paid-leaf count obeys the same exact
recurrence, including all source complements and exits:

```math
L(n)=\sum_s w_sL(n-s)+\sum_e x_eL(e),\qquad\sum_s w_s=1.
```

The frozen executable in PR #4359 rejects `r_max=k_min` at its entry
guard. This extension does not claim that the old executable accepts
the new rule unchanged. The scoped adapter and finite scheduling checks
in `../kappa-4359-weak-compiler/` supply the changed admissibility guard.
The native word, adapters and every remaining paid call have their
separate source-bound audit.

## 2. Exact exit moments

Write

```math
P_a=\sum_j r_j^a
```

for the moment of the complete paid-call list. Repeated calls count
with their actual multiplicities.

Every paid-round path of length `G` occurs. Indeed, its dilation obeys
`rho<=q^G<=n/m`; the degree-zero lattice point therefore fits. At that
depth, it is the only point and its multinomial multiplicity is one.
Thus the unnormalized exit moment is exactly

```math
E_a=P_a^{G+1}.
```

There is no missing branch factor. The sequence of paid rounds identifies
the class, and the final paid round identifies its exit.

Choose `t=1-C` such that the native mixed tariff satisfies

```math
P_t<\sum_k W_k k^t.
```

Cancellation of every internal matched job gives source moment
`S_t>=E_t`. Dividing source and exit counts by the number of source arrays
then gives

```math
\sum_e x_e e^t\leq\sum_s w_s s^t.
```

## 3. A uniform bound on the large-exit fraction

For this tariff, exact directed rational evaluation proves

```math
\frac{P_{t+1}}{P_t}<2,\qquad 2^2<5=q.
```

Take `theta=3/4`. Markov's inequality, applied to the exit moment itself,
gives

```math
\begin{aligned}
\frac{\sum_{e>n^\theta} x_e e^t}{\sum_s w_s s^t}
&\leq\frac{n^{-\theta} E_{t+1}}{E_t}\\
&=n^{-3/4}\left(\frac{P_{t+1}}{P_t}\right)^{G+1}\\
&<n^{-3/4}2^{G+1}\\
&\leq 2m^{-1/2}n^{-1/4}\\
&\leq 2m^{-3/4}<\frac18.
\end{aligned}
```

The penultimate inequalities use `2^G<=q^(G/2)<=sqrt(n/m)` and `n>=m`.
The last strict inequality is the integer comparison
`57^3>16^4`. Retaining the factor from `m` makes the bound valid at every
rank `n>=57`; no large additional cutoff is required.

This argument controls the fraction of exit potential carried by large
exits. The largest exit itself need not be bounded by a sublinear power
of `n`. The strict ratio `q/m<1` already ensures that every recursive
exit is smaller than its parent.

## 4. Logarithmic induction with low and high exits

Set

```math
\gamma=\frac1{20},\qquad
\psi(n)=\max(1,\log n)^\gamma,\qquad
A=m^{1-t}.
```

For `n>=m`, `theta*log(n)>1`. A low exit `e<=n^theta` therefore satisfies
`psi(e)<=v*psi(n)`, where `v=theta^gamma`. This includes `e=1` because
of the maximum with 1. Every high exit satisfies `psi(e)<=psi(n)`,
since `e<n`.

Let `beta` be the large-exit `t`-potential divided by source
`t`-potential. The preceding section gives `beta<1/8`. Using the total
exit potential bound as well, the full weighted exit term satisfies

```math
\sum_e x_e e^t\psi(e)
\leq\psi(n)\,[v+(1-v)\beta]\sum_s w_s s^t.
```

The coefficient is a convex combination. Counting the high-exit
potential twice would produce a needlessly weaker estimate.

The following integer-power comparison proves a sufficient upper bound
on `v`:

```math
\frac34<\left(\frac{505}{512}\right)^{20}.
```

Hence

```math
v+(1-v)\beta
 <\frac78\frac{505}{512}+\frac18
 =\frac{4047}{4096}.
```

The source complement inequality is unchanged:

```math
n^t-\sum_s w_s(n-s)^t
\geq\eta\sum_s w_s s^t,
\qquad \eta=t m^{t-1}.
```

For `C=0.00231166`, the exact logarithm bound `log(57)<81/20` and
`exp(-x)>=1-x` give

```math
\eta>(1-C)\left(1-\frac{81}{20}C\right)
 >\frac{4047}{4096}.
```

The exit term fits within the complement margin. Strong induction in
the exact leaf recurrence therefore proves

```math
L(n)\leq m^C n^{1-C}\max(1,\log n)^{1/20}
```

for every positive integer `n`. For `n<m`, this follows from the
ordinary base program `L(n)=n`. Terms with zero complementary rank
vanish. For `n>=m`, both recursive kinds have smaller rank and the
preceding inequalities close the induction.

## 5. A specified rank for the improved uniform saving

Choose `C_u=0.002311658`, so `d=C-C_u=1/500000000`.
Put `N=2^H`. Since `m<2^6`, `H<2^J`, and `log(2)<1`, it is sufficient
to require

```math
Hd>6C+\frac J{20}.
```

The exact choices

```math
H=756934981,\qquad J=30
```

satisfy `H<2^J`, `H>=6`, and

```math
Hd-6C-\frac J{20}=\frac1{500000000}>0.
```

It follows that `L(N)<N^(1-C_u)`. The uniform compiler at this exact
rank is a finite integer program with complete productive outputs and
only rank-one paid children. Its entire word, replication factors and
constants are specified by the finite algorithm. They are not
materialized here and remain impractical in size.

The scalar, routing, owned-storage, row-reserve and precision constants
must all be those of this new fixed compiled word. The change in rank
and native tariff does not authorize reusing a previous numerical cap.

## 6. Reproduction and audit scope

Keep the pinned PR #4359 checkout separate from these new packages.
Each checker accepts its path with `--source-root`. The native and
compiler receipts are independently replayed before this theorem's
receipt is checked:

```sh
python3 -B research/kappa-4359-native-five/verify.py \
  --source-root /absolute/path/to/pr4359-checkout --check
python3 -B research/kappa-4359-weak-compiler/verify.py \
  --source-root /absolute/path/to/pr4359-checkout
python3 -B research/kappa-4359-weak-separation/verify.py \
  --source-root /absolute/path/to/pr4359-checkout --check
```

The final checker authenticates both companion receipts, independently
recounts the changed native tariff, and verifies the moment ratio,
large-exit bound, complement margin and sufficient rank. Its arithmetic
uses exact fractions with directed logarithm and exponential enclosures.
Use `--out /absolute/path/to/new-certificate.json` to generate a separate
receipt. No source package is modified by a check.

The exact finite tests cover named field ownership, ordered batching,
equal-rank scheduling, the rank-one-lattice rejection and the literal
native deletion. They do not formally verify all inherited native,
fixed-tape or outer analytic hypotheses. The general weak-separation
claim is the written argument above. The numerical certificate checks
its sufficient conditions for this concrete source-bound rule.

## Open next questions

1. Determine whether a different split threshold or fractional moment
   gives smaller sufficient templates. The first exact test is
   `P_(t+alpha)/P_t` at rational `alpha`; the proof must retain both the
   source denominator and all chronological exit multiplicities.
2. Test weaker rank separation beyond this case. The present theorem
   requires `r_j<=k_min<m` for exact Pascal matching and decreasing
   recursive ranks. It does not cover arbitrary overlapping rank ranges.
3. Improve the remaining native tariff. Removing the width-five
   completions changes the endpoint root; improving this tail estimate
   alone changes template sizes and does not raise that root.
