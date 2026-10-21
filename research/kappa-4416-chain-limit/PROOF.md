# An all-p limit for the declared two-chain invoice family

The balanced p7 invoice in [PR #4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416)
has the largest mixed-moment root among **all** the invoice formulas defined
below, for every integer `p>=1` and every split of the two chains. Its root is

```text
0.002686489048851021139378940762
    < C_star <
0.002686489048851021139378940763.
```

Thus increasing `p`, or unbalancing these two chains, cannot raise the
positive-moment endpoint of this particular family. This extends the source's
finite arithmetic screen over `2<=p<=20` to every `p`; it is not an exhaustive
controller or idle-mask theorem. No new native word is admitted here. The
bound remains valid even if native admission is granted to every declared
invoice.

The p7 member is already admitted under the source's inherited premises. The
[strict root-family companion](../kappa-4416-root-family/PROOF.md) supplies a
conditional program for every fixed rational `0<kappa<C_star`. Consequently
the ceiling below is sharp for this family of positive-moment certificates.
It is neither an unconditional multiplication theorem nor a lower bound on
all algorithms that use the supplier.

## 1. The complete declared invoices

We retain the exact formula in the pinned source
[scan.py](https://github.com/1337isnot1337/integer-mult-bounds/blob/e9058860b5c850760fdf970e796a96aefcdb1d98/research/pr4359-p7-padding/scan.py).
Its local productive and paid counts are

```text
H = {5:28, 6:18, 7:56, 8:93, 9:213},
N = {1:2487, 2:713, 3:224, 4:102, 5:20, 8:8}.
```

These counts come from the authenticated native local receipt. Both local
orientations have the same paid profile. The declared parameters are
integers `p>=1`, `0<=a<=p-1`, and `b=p-1-a`.

The targets consist of `(2p+1)` copies of `H`, 224 targets of rank `16p+9`,
and, for each chain length `l` in `(a,b)`, 224 targets at every rank
`16j+25`, `0<=j<l`. The paid bill consists of `(2p+1)` copies of `N`,
224 calls of rank 8 for each of the `p-1` middle windows, and 224 calls
at every rank `16j+16`, `0<=j<l`, for each chain. No paid window is omitted.

The source associates this formula with all retained middle windows, the
first `a` initial windows, and the last `b` terminal windows. At `(p,a,b)=(7,3,3)`
the mask is 232127 and both complete profiles exactly equal the native p7
invoice. Elsewhere we study the formula without assuming a physical word.
The source's screen starts at `p=2`; its same algebraic formula is also
well-defined at `p=1`, where both chains are empty.

For `0<t<1`, set

```math
\begin{aligned}
D_t&=\sum_r(H_r-N_r)r^t,\\
f_t(j)&=(16j+25)^t-(16j+16)^t,\\
F_t(l)&=\sum_{j=0}^{l-1}f_t(j),\qquad F_t(0)=0.
\end{aligned}
```

The complete target-minus-paid moment is exactly

```math
M_{p,a}(t)=(2p+1)D_t+
224\bigl[(16p+9)^t+F_t(a)+F_t(p-1-a)-(p-1)8^t\bigr]. \tag{1}
```

In particular, `D_0=-3146` and `D_1=-1856`.

## 2. Balancing and strict discrete concavity in p

For fixed `0<t<1`, the function `x^t` is strictly concave on `x>0`.
Therefore `f_t(j)`, an increment of length 9, strictly decreases with `j`.
If `a>=b+2`, moving one term from the longer chain to the shorter changes
`F_t(a)+F_t(b)` by `f_t(b)-f_t(a-1)>0`. Hence a balanced split maximizes
(1), uniquely up to interchanging the two chain lengths.

Write the balanced value as

```math
B_p(t)=M_{p,\lfloor(p-1)/2\rfloor}(t).
```

When `p` increases by one, one term is added to a shorter chain. Thus

```math
\begin{aligned}
B_{p+1}(t)-B_p(t)=2D_t+224\bigl[&
(16p+25)^t-(16p+9)^t\\
&+f_t(\lfloor(p-1)/2\rfloor)-8^t\bigr]. \tag{2}
\end{aligned}
```

The first difference inside the brackets is an increment of length 16
whose starting point increases with `p`, so it decreases strictly. The
`f_t` term is nonincreasing, including when the floor does not change.
Consequently the increments in (2) decrease strictly for every integer
`p>=1`. This proves strict discrete concavity over the entire unbounded
sequence; no finite-range extrapolation is used.

## 3. Two exact neighbor signs settle the unbounded sequence

Let `t_star=1-C_star`, using the unique p7 root proved in the frozen
root-family companion. Its balanced moment is `B_7(t_star)=0`.

The checker encloses each neighbor difference over the **entire** displayed
rational interval for `C_star`. The strict rational bounds are

```math
1.253606978240 < B_7(1-C)-B_6(1-C) < 1.253606978241,
```

```math
1.427475680484 < B_7(1-C)-B_8(1-C) < 1.427475680485.
```

They hold for every `C` in the closed root enclosure. Each rank power is
bounded at the two appropriate endpoints before mixed signs are summed.
No floating-point value or pointwise approximation to the root decides a
comparison.

At `t_star`, (2) is positive for `p=6` and negative for `p=7`. Its strict
decrease implies positive increments for all `p<=6` and negative increments
for all `p>=7`. Therefore `B_7(t_star)` is the unique global maximum among
all integers `p>=1`. Balancing gives

```math
M_{p,a}(t_\star)\le B_p(t_\star)\le B_7(t_\star)=0, \tag{3}
```

with equality only for `p=7,a=b=3`.

In particular, even a native realization of the balanced p8 formula would
have moment less than `-1.427475680484` at the p7 root. Merely adding its
two fresh local stages does not improve this invoice.

## 4. The ceiling holds for every larger saving

We must also exclude a profile whose moment becomes positive again after
`C_star`. The following exact sign structure rules this out for the full
range `0<C<1`.

After the local counts and middle windows are combined, the coefficients
at ranks 1 through 9 are

| Rank | Net coefficient |
| --- | --- |
| 1 | `-2487(2p+1)` |
| 2 | `-713(2p+1)` |
| 3 | `-224(2p+1)` |
| 4 | `-102(2p+1)` |
| 5 | `8(2p+1)` |
| 6 | `18(2p+1)` |
| 7 | `56(2p+1)` |
| 8 | `309-54p` |
| 9 | `213(2p+1)` |

For `p<=5`, the rank-8 coefficient is nonnegative. For `p>=6`, pair its
negative part with the same number of rank-9 terms:

```math
(54p-309)(9^t-8^t).
```

The remaining rank-9 coefficient is `372p+522>0`. Every chain term is
also a positive multiple of `(16j+25)^t-(16j+16)^t`, and the central
term has positive rank `16p+9`.

Divide the resulting expression by `5^t`. All unpaired negative terms
have bases strictly below one, so their negatives increase strictly with
`t`. All unpaired positive terms have bases at least one. In every paired
difference the scaled bases satisfy `1<x<y`, and `y^t-x^t` increases
strictly for `t>=0`, since `z^t log z` increases with `z>=1`.
Thus `M_{p,a}(t)/5^t` is strictly increasing for every fixed declared
profile throughout `t>=0`.

Its exact endpoint values are

```math
M_{p,a}(0)=-6516p-2698<0,\qquad
M_{p,a}(1)=96p-64>0.
```

Each profile therefore has one root in `0<t<1`. Combining the strict
increase with (3) proves

```math
M_{p,a}(1-C)\le0
\quad\text{for every }C_\star\le C<1,\ p\ge1,\ 0\le a<p.
```

The inequality is strict unless `C=C_star,p=7,a=3`.

## 5. Consequences and scope

At a fixed `0<t<1`, tensoring profiles with `T_t<=P_t` preserves that
inequality, even when the factors use different `p` or chain splits.
Paid completion from rank `K` to `K+D` changes the mixed moment by
`(K+D)^t-K^t-D^t<0` when `D>0`. Splitting a paid rank into positive parts
also cannot increase the mixed moment. These are the same fully charged
operations analyzed in the root-family companion.

Hence the declared chain family, followed by these operations, cannot
give a positive complete mixed moment at or above `C_star`. The companion's
p7 construction supplies every strict root-below conditional exponent.

The theorem does not classify arbitrary idle masks, exclude a different
controller word, prove that every formula has a native realization, or
rule out an analysis that does not use this positive-moment condition.
All native, all-column, whole-job, movement, storage, precision, analytic,
fixed-tape and exact-recovery premises of the constructive result remain
inherited.

## 6. Reproduction

The checker authenticates and fully replays the frozen root-family
companion and its native dependency chain. It authenticates the original
`scan.py` and local receipt, compares the declared profile with that
source, and independently verifies the two neighbor signs using directed
rational intervals. All acceptance decisions use Python integers and
fractions. The balancing, discrete-concavity and scaled-monotonicity
arguments above establish the unbounded quantifiers.

From a checkout containing these companion packages, with the exact
PR #4416 export at `SOURCE_ROOT/research/pr4359-p7-padding`, run

```bash
python3 -I -O -B research/kappa-4416-chain-limit/verify.py \
  --source-root SOURCE_ROOT --check
```

The source commit is `e9058860b5c850760fdf970e796a96aefcdb1d98`.
The source export is an external dependency; a changed source is rejected.

## 7. Attribution and open next questions

The native supplier comes from zxv's [PR #4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359).
The p7 native word, declared chain formulas and finite scan come from
1337isnot1337's #4416. The constructive companion retains Jacob Alan
Sussman's Theorem 1G compiler and the source outer ledger's #4405 lineage.
Related logarithmic work in zxv's #4411 and the raw-root observation in
pinterbanget's #4420 remain credited in that companion. The new all-p
argument, verifier and receipt are Apache-2.0.

Two questions remain useful after this scoped limit.

- Can a different idle-mask family or controller word yield an exact
  Laurent factorization with a better complete moment? A candidate needs
  exact factorization and then its own owner, phase, spectator and
  chronological admission. This theorem does not settle those masks.
- Can a change to the local supplier lower its complete paid bill while
  retaining the needed productive fields? Equation (1) gives a direct
  way to assess an admitted new local invoice. The present all-p limit
  only uses the fixed `H` and `N` displayed above.
