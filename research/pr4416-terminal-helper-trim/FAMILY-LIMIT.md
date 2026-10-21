# Exact limit of the declared prefix/suffix family

The terminal helper change raises the local mixed-moment frontier. Increasing
the pair count in the same controller family does not provide another gain:
`p = 7` is the unique best integer pair count at each of the four test
exponents below. The result holds for every positive pair count, rather
than only the finite range screened in PR4416.

| Local supplier | Positive p7 test | Negative test for every pair count and split |
| --- | ---: | ---: |
| Original THREE-base invoice | `0.00268648` | `0.00268649` |
| Terminal helper trim | `0.00269635` | `0.002696357` |

These are statements about the declared mixed moments. A positive test does
not itself establish the native supplier, strict hierarchy, rounded
implementation, or outer multiplication endpoint. Those obligations are
handled elsewhere in this package and its attributed predecessors.

The negative test also constrains the existing rank-based completion and
strictification operations, as explained below. It is not a universal
limit on other masks, controllers, native words, geometries, or integer
multiplication algorithms.

## The exact invoices

For `0 < t < 1`, let `H_t` and `P_t` be the productive helper and paid-child
moments of one local call. The original unsplit THREE-base invoice is

```text
H = {5:28, 6:18, 7:56, 8:93, 9:213}
P = {1:2487, 2:713, 3:224, 4:102, 5:20, 8:8}.
```

The terminal helper change deletes twenty-two rank-one children and reduces
twenty-two helper targets from rank five to rank four:

```text
H = {4:22, 5:6, 6:18, 7:56, 8:93, 9:213}
P = {1:2465, 2:713, 3:224, 4:102, 5:20, 8:8}.
```

Thus the local difference `H_t-P_t` increases by

\[
22\bigl(1+4^t-5^t\bigr)>0.
\]

The total rank-one difference is unchanged. The gain comes from the strict
concavity of the power function, rather than additional rank mass.
`native_trim.py` and `NATIVE-TRIM.md` bind this change to the actual word;
this note supplies an independent arithmetic and infinite-family argument.

## Every split is bounded by a balanced split

The family has `p >= 1` pairs, all middle idles, an initial prefix of
length `a`, and a terminal suffix of length `b`, where `a+b=p-1`. It uses
`2p+1` local calls. Write

\[
h(x)=x^t,\qquad g(j)=h(16j+25)-h(16j+16).
\]

The exact target-minus-paid moment is

\[
\begin{aligned}
F(p,a,b)={}&(2p+1)(H_t-P_t)\\
&+224\left[h(16p+9)+\sum_{0\le j<a}g(j)
                      +\sum_{0\le j<b}g(j)
                      -(p-1)h(8)\right].
\end{aligned}
\]

The function `g` is strictly decreasing because `h` is strictly concave.
If one chain is at least two longer than the other, transferring its last
term to the shorter chain increases `F`. Consequently, at each fixed `p`,
the maximum is achieved by

\[
a=\left\lfloor\frac{p-1}{2}\right\rfloor,\qquad
b=\left\lceil\frac{p-1}{2}\right\rceil,
\]

up to exchanging the two chains. Denote this balanced maximum by `F(p)`.

## Discrete concavity controls all positive pair counts

The exact successive difference is

\[
\begin{aligned}
F(p+1)-F(p)={}&2(H_t-P_t)\\
&+224\left[h(16p+25)-h(16p+9)
 +g\left(\left\lfloor\frac{p-1}{2}\right\rfloor\right)-h(8)\right].
\end{aligned}
\]

The first variable term decreases strictly with `p`, again by concavity.
The `g` term never increases. Therefore the successive difference is
strictly decreasing for all integers `p >= 1`. This conclusion is
independent of which of the two local invoices is used: the local
contribution is constant in the successive difference.

It follows that `F(7)>F(6)` and `F(7)>F(8)` prove that `p=7` is the unique
global maximum. Three exact evaluations therefore suffice to establish
the result for the infinite family.

## Exact finite comparisons

At `t=1-C`, the independent rational verifier gives the following outward
intervals. The table shortens the output intervals; the script prints
thirty digits with rigorous outward rounding.

| Supplier | C | p | Strict enclosing interval for F(p) |
| --- | ---: | ---: | --- |
| Original | `0.00268649` | 6 | `(-1.253787662584492, -1.253787662584491)` |
| Original | `0.00268649` | 7 | `(-0.000214004461231, -0.000214004461230)` |
| Original | `0.00268649` | 8 | `(-1.427723940471097, -1.427723940471096)` |
| Trimmed | `0.002696357` | 6 | `(-1.204142700102404, -1.204142700102403)` |
| Trimmed | `0.002696357` | 7 | `(-0.000218270385070, -0.000218270385069)` |
| Trimmed | `0.002696357` | 8 | `(-1.487080618144224, -1.487080618144223)` |

In both cases, the adjacent inequalities hold strictly and the global
maximum is negative. Hence `F(p,a,b)<0` for every legal `p,a,b` at the
respective negative test.

The same adjacent comparisons hold at the positive tests. The p7 moment
lies in `(0.002035952908284, 0.002035952908285)` for the original invoice,
and in `(0.001350885109719, 0.001350885109720)` for the trimmed invoice.

## Why tail tuning cannot cross this limit

Fix one supplier and its negative test, and write its target and paid
moments as `T` and `P`. Every block in the stated family has `T<P`.
The following operations cannot turn that inequality into a favorable
moment at the same test exponent:

- A disjoint union adds target and paid moments separately.
- A tensor product of such blocks multiplies the two moments separately.
- Matching and canceling identical whole jobs subtracts equal terms.
- Completing a target of rank `K` by a paid transform on `D` unused axes
  changes the difference by `(K+D)^t-K^t-D^t <= 0`.
- Splitting a paid child of rank `r+s` into ranks `r,s` increases its paid
  moment, since `(r+s)^t <= r^t+s^t`.

A higher-moment tail estimate can prove that a positive raw moment
survives a finite strictification more efficiently. It does not change
the raw moment or reverse these inequalities.

This also excludes a larger saving for a recipe obtained by these
operations and completed to a strict hierarchy. To see this, let `L` be
the smallest completed target rank, so every paid rank is below `L`.
After dividing by `L^t`, the target moment is nondecreasing in `t`, while
the paid moment is decreasing. Positivity at a larger saving, which has
a smaller `t`, would imply positivity at the negative test. That
contradicts the preserved nonpositive moment there.

The argument leaves open a changed native invoice, other controller
families, and genuine operator cancellations that the listed rank
operations do not express. Those are appropriate places to seek the
next substantial improvement.

## Reproduction and attribution

From the repository root, run:

```sh
python3 -I -B research/pr4416-terminal-helper-trim/family_limit.py
```

The script is read-only and uses only the Python standard library.
It independently bounds logarithms by sixty terms of the positive
`atanh` series with an explicit geometric remainder. It bounds the
small positive exponential arguments by forty Taylor terms and an
explicit tail. Rational arithmetic and reciprocation then enclose
`r^(1-C)`. It compares independently assembled literal and formula
histograms, checks the complete rank-one surplus `96p-64`, verifies the
twenty-two changes, and proves all twelve finite moment comparisons.
The extension to all pair counts is the concavity proof above.

Sources are PR4416's `FOLLOWUP.md`, `scan.py`, and exported original
THREE-base invoice, plus this package's native trim. Controller and
native construction: zxv. Productive padding and this extension:
Cinna Davis / 1337isnot1337, with OpenAI assistance. The mixed-target
framework builds on Jacob Alan Sussman's work. Apache-2.0.
