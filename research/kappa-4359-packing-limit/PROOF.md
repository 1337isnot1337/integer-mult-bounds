# An exact limit for the fixed native window packing class

The construction in `../kappa-4359-native-packing/` maximizes the mixed root
within the class defined below. Its root lies strictly between

\[
0.002312854665364207351198238279
\quad\hbox{and}\quad
0.002312854665364207351198238280.
\]

The proof is an exact dual certificate for a finite packing problem. It
does not use an optimizer, an optimality status from a solver, or a
rounded comparison at one guessed root. The checker proves every dual
inequality throughout this entire closed interval and compares the
profiles at the true root inside it.

This is a limit for the specified native inventories, windows, and
residual completion rule. It is not a limit for other controller words,
other native programs, or all integer multiplication constructions. It
does not strengthen the inherited physical or analytic hypotheses of
the published conditional bound.

## 1. Exact class being compared

Fix the authenticated PR4359 source at commit
`da637c87c89482bc4c86be36bd0071b3d400dbed` and the native rank-five
endpoint convention certified by `../kappa-4359-native-packing/`.
Keep the seven native local words, their complete paid invoices, their
main productive endpoints, the owned center, and the four existing
idle-window families. Each native stage has the following helper stock.

| Native helper width | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|
| Available roles per stage | 28 | 18 | 56 | 93 | 213 |

The existing families have these exact stage slots and capacities.

| Family | Native stages | Owners in the family | Window capacity |
|---|---|---:|---:|
| 0 | 0, 1 | 224 | 16 |
| 1 | 2 | 224 | 8 |
| 2 | 4 | 224 | 8 |
| 3 | 5, 6 | 224 | 16 |

The stage sets are disjoint. Stage 3 has no such window. The window
axes, their owners, their stages, and the surrounding controller
chronology are fixed. Different families may be packed independently;
there is no symmetry requirement between their assignments.

An admitted packing may use at most one actual native helper in each
stage slot of each window. Hosted helper slices must be disjoint and
must lie inside the original window. A helper role may be used only
once at its native stage. All unhosted helpers become independent
fresh productive fields at their native widths. Their names and their
number may change as the packing changes. A width-five helper stays
width five; it receives no free sixth axis.

Every remaining window dimension uses the same canonical completion
rule: split its residual dimension into as many rank-five paid calls
as possible, followed by one call for a nonzero remainder. The native
local paid word and main endpoints remain fixed. The one owned center
remains outside the productive credit.

This class allows all ordered cross-stage choices inside these windows,
all exchanges of available native roles within their actual stages,
all choices of owner for an admissible slot, and every resulting
change to the fresh owner set. It is not restricted to the symmetric
pool used to display the published construction. We use an upper
bound on the width-count relaxation of this class, so extra physical
restrictions can only reduce the admissible set.

The class excludes changing the native words or inventories, adding or
moving idle windows, hosting two helpers in one stage slot, borrowing
axes outside a window, combining unused helpers into other kinds of
fresh programs, changing the productive endpoint convention, or using
a different residual completion rule. No claim about those changes is
made here.

## 2. The exact mixed invoice

Write \(t=1-C\), \(h_r=r^t\) for \(r\geq1\), and \(h_0=0\) for an
empty helper slot. For a residual dimension \(d\), define

\[
s_d=\lfloor d/5\rfloor h_5+h_{d\bmod5}.
\]

If every helper is initially fresh and every window is paid in full,
the productive profile is

\[
T_0=196h_5+126h_6+392h_7+651h_8+1491h_9
    +448h_{25}+224h_{57}.
\]

The complete local paid word has the same rank counts in each of the
seven stages, in its required orientation:

\[
P_{\rm local}=2487h_1+713h_2+232h_3+102h_4+28h_5.
\]

Thus the baseline mixed moment is

\[
M_0=T_0-7P_{\rm local}-448s_{16}-448s_8.
\]

Hosting widths \(a,b\) in a rank-16 window changes this moment by

\[
g_{16}(a,b)=s_{16}-s_{16-a-b}-h_a-h_b.
\]

The terms \(-h_a-h_b\) remove the corresponding fresh output credits.
The residual term pays every unhosted axis. This change applies to
every ordered pair

\[
(a,b)\in\{0,5,6,7,8,9\}^2,\qquad a+b\leq16.
\]

There are exactly 33 such ordered pairs. A rank-eight window has the
analogous one-slot gain

\[
g_8(a)=s_8-s_{8-a}-h_a,
\qquad a\in\{0,5,6,7,8\}.
\]

## 3. A dual bound for each rank-16 family

Use the following symbolic prices:

\[
\begin{aligned}
\lambda&=g_{16}(6,9)=3h_5-h_6-h_9,\\
\alpha_7&=g_{16}(7,9)-\lambda=1+h_6-h_7,\\
\alpha_8&=\frac{g_{16}(8,8)-\lambda}{2}
          =\frac{1+h_6+h_9-2h_8}{2}.
\end{aligned}
\]

The checker proves that all three prices are strictly positive
throughout the certified root interval. For every one of the 33
ordered patterns, it also proves

\[
g_{16}(a,b)\leq
\lambda+\alpha_7\bigl(\mathbf1_{a=7}+\mathbf1_{b=7}\bigr)
        +\alpha_8\bigl(\mathbf1_{a=8}+\mathbf1_{b=8}\bigr).
\tag{1}
\]

Five patterns are identically tight:
\((6,9),(9,6),(7,9),(9,7),(8,8)\).
The other 28 have strictly positive dual gaps throughout the interval.
Identically zero polynomials are cancelled symbolically before any
interval evaluation.

Each family has 224 windows and, across its two actual stages, at most
112 width-seven roles and 186 width-eight roles. Summing (1), with no
assumption on how the ordered patterns are distributed, bounds its
total gain by

\[
G_{16}\leq224\lambda+112\alpha_7+186\alpha_8.
\tag{2}
\]

The nonnegative prices make these inventory upper bounds legitimate.
Widths five, six, and nine have zero inventory price; ignoring their
stock constraints in this upper bound is a relaxation. Those stock
constraints still apply to the attaining construction.

The published assignment attains (2) exactly:

| Ordered widths | Number of windows per rank-16 family |
|---|---:|
| (8, 8) | 93 |
| (7, 9) | 56 |
| (9, 7) | 56 |
| (6, 9) | 18 |
| (9, 6) | 1 |

It uses all 56 width-seven and all 93 width-eight roles at each stage.
Its width-six usage is 18 in the first stage and 1 in the second;
its width-nine usage is 57 and 74, respectively. All fit the actual
per-stage stock. Every used pattern is tight in (1), so the upper
bound and attained gain agree as symbolic polynomials, not just at
the root.

The full maps, phases, normalizers, owner chronology, rebuilt fresh
fields, and ordered paid word for this assignment are checked in the
separate frozen native certificate. The present checker authenticates
and reproduces that certificate before using it.

## 4. The rank-eight families

For one-slot windows,

\[
g_8(0)=g_8(5)=0
\]

identically. The checker proves \(g_8(6),g_8(7),g_8(8)>0\) throughout
the root interval. Every family therefore has gain at most

\[
G_8\leq18g_8(6)+56g_8(7)+93g_8(8).
\tag{3}
\]

The current assignment uses all these positive-gain roles. It also
hosts the 28 width-five roles and leaves 29 windows empty. The 195
eligible roles fit within 224 owners, so it attains (3). Leaving some
width-five roles fresh instead would give the same mixed moment,
because their one-slot gain is zero.

## 5. Full-profile bound and true-root comparison

The four families use disjoint native stage inventories. Add two
copies of (2) and two copies of (3) to \(M_0\). Exact symbolic
cancellation gives the published mixed polynomial:

\[
\begin{aligned}
M_*(t)={}&224h_{57}+448h_{25}+1229h_9+93h_8+56h_7+52h_6\\
        &-114h_5-714h_4-1738h_3-5027h_2-17559h_1.
\end{aligned}
\]

The coefficient \(-114\) combines 140 productive rank-five fields
with 254 paid rank-five calls. Every admitted packing \(P\) obeys

\[
M_P(1-C)\leq M_*(1-C)
\tag{4}
\]

throughout the entire certified saving interval. The same inequality
also bounds the fractional width-count relaxation. It does not rely
on a solver or on any symmetry of \(P\).

For completeness, every admitted profile has a unique mixed root in
\(0<C<1\). All productive ranks are at least five, all paid ranks are
at most five, and the 224 productive rank-57 fields remain present.
Consequently

\[
\frac{M_P(t)}{5^t}
=\sum_k b_k(k/5)^t-\sum_r p_r(r/5)^t
\]

is strictly increasing in \(t\): every term has a nonnegative
derivative, and the fixed rank-57 terms have strictly positive
derivatives. At \(t=1\), its unscaled moment is 224. Hosting a
width-\(w\) helper removes both \(w\) productive rank units and
\(w\) paid rank units, so this surplus is the same for every admitted
packing. At \(t=0\), there are at most 3,528 productive fields and
at least 24,934 unchanged local paid calls, so the moment is negative.
Continuity and strict monotonicity give exactly one root.

Let \(C_*\) be the true root of the published profile. Exact endpoint
signs put \(C_*\) inside the displayed interval, and hence (4) applies
at \(C_*\), giving

\[
M_P(1-C_*)\leq M_*(1-C_*)=0.
\]

Strict increase in \(t\) means that the root for \(P\) has
\(t_P\geq1-C_*\), equivalently \(C_P\leq C_*\). The published,
physically checked packing attains equality. This proves the claimed
maximum mixed root for the stated class, without claiming uniqueness
of the attaining packing or attainment of an outer exponent at that
strict endpoint.

## 6. Exact verification and reproduction

`verify.py` checks immutable SHA-256 bindings for the frozen native
producer, its receipt, and the existing directed rational interval
engine in `../kappa-4359-outer-endpoint/verify.py`. The native producer
authenticates the PR4359 input bytes before executing source-derived
code. Its full receipt is replayed and compared. The local paid words,
per-stage helper stock, original window stages and capacities, native
profile, and root bracket are all checked against these inputs.

For each power \(r^{1-C}\), monotonicity in \(C\) gives a simultaneous
enclosure over the whole root interval. The checker evaluates the
lower endpoint of that power interval at the upper saving endpoint,
and the upper endpoint at the lower saving endpoint. All polynomial
coefficients are exact rational numbers. Signed sums use directed
endpoints, and every nonzero dual gap must have a strictly positive
rational lower bound. Decimal strings in the receipt are displays;
they never decide acceptance.

No optimizer or floating-point arithmetic is needed. The certificate
records all 33 wide inequalities, the five middle choices, the three
dual prices, the symbolic full-profile identity, endpoint signs,
source hashes, and hashes of this proof and its verifier.

From this contribution checkout, with a separate snapshot of the
pinned pending PR4359 dependencies:

```bash
python3 -B research/kappa-4359-packing-limit/verify.py \
  --source-root /path/to/pr4359-da637c87-checkout --check
```

The default source root is the current project root. `--out PATH`
writes a freshly generated receipt. The default action and `--check`
replay the proof and require byte-for-byte agreement with the
committed `CERTIFICATE.json`.
