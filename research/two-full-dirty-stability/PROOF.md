# Restored identity scratch does not rescue two native FULLs

This is a scoped obstruction, not a new multiplier, native caller, or kappa
improvement. It extends the full-monomial **two-owner** Fourier-grade theorem
of [PR4920](https://github.com/CrocSwap/integer-mult-bounds/pull/4920) to
arbitrarily many independent dirty scratch owners returned unchanged. The
additional argument uses the intermediate grades, then regular-module rank.
It answers the identity-scratch question released in
[Discussion4902 comment19144315](https://github.com/CrocSwap/integer-mult-bounds/discussions/4902#discussioncomment-19144315).

The source interface, grade facts, and all-width separation lemma are inherited
from PR4920. The finite regular-module method and the warning against silently
combining different resource scopes are credited to
[PR4928](https://github.com/CrocSwap/integer-mult-bounds/pull/4928).
Native operators and raw phase conventions are credited to the upstream
contributors. The new argument is the forced main/scratch decoupling below.

## Exact algebra and endpoint

Let G be a fixed finite-phase, one-column Clifford group on 17 address axes,
Z its scalar subgroup, and H its **full monomial subgroup**, containing Z.
In particular, H includes monomial central/fresh coordinate mixing and
controlled quadratic phases; it is not the separated subgroup in PR4928.
At column width f, let A_f be the central-character twisted group algebra
on G/Z, specializing z=ζI to ζ^f over a characteristic-zero splitting field K.
Let B_f be its subgroup algebra on H/Z. No domain assumption is made.

Fourier grade is unchanged by left or right monomial multiplication. Thus
projection onto any chosen set of grades is a B_f-bimodule map. Products of
pure words satisfy grade(uv) <= grade(u)+grade(v). These are exactly the grade
facts used by PR4920; scalar cocycles change coefficients, not grades.

There are two main owners and s>=0 further independent arbitrary dirty
scratch owners. The real native helper jobs remain autonomous, unchanged,
and unavailable for mixing. On these 2+s owners the two calls have form

    T1 = diag(A1,A2,I_s) E_{u,v}(q1),
    T2 = diag(B1,B2,I_s) E_{x,y}(q2),
    E_{i,j}(q) = I + e_i q e_j^T,

where {u,v}={x,y}={1,2}. Products act on columns from right to left.
Each Ai and Bi is a pure Clifford group unit of Fourier grade eight,
including the role-dependent raw translations and phases. The query letters
q1,q2 may differ and need not commute with each other or any diagonal factor.
Their signs and inverses are retained. This is the source factor order
`diag(D) E`; no D factor is absorbed into a free control.

Allow arbitrary L,W,R in GL_{2+s}(B_f). They may mix main and scratch owners,
and their entries may be sums of monomial words, not just pure words or
owner permutations. Suppose

    L T2 W T1 R = J = diag(g1,g2,I_s),

where each gi is one pure Clifford group word of grade 17, up to arbitrary
monomial boundaries and with its actual phase. We prove this impossible.

## Intermediate grades force the interstage control to decouple

Put rho=pi_{1,...,16}. Since rho(J)=0, the bimodule property and invertibility
of L,R imply

    rho(M)=0,  where M=T2 W T1.                         (1)

This retains the grade-zero scratch endpoint. It does **not** make the
incorrect inference pi_{<=16}(M)=0 while scratch is present.

Write c=u for the main input column untouched by the first shear, c'=v for
the other main column; write r=y for the main output row untouched by the
second shear, r'=x for the other main row. The four orientations are:

| First shear | Second shear | Untouched column c | Untouched row r |
| --- | --- | --- | --- |
| E12 | E12 | 1 | 2 |
| E12 | E21 | 1 | 1 |
| E21 | E12 | 2 | 2 |
| E21 | E21 | 2 | 1 |

For every scratch index a, direct multiplication in the declared order gives

    M[a,c] = W[a,c] A_c,
    M[r,a] = B_r W[r,a].                               (2)

Each entry is supported wholly in grade eight: W entries lie in B_f and
monomial multiplication preserves grade. Consequently rho is the identity
on these entries. By (1) they vanish. Ai,Bi are group units, so

    W[a,c]=W[r,a]=0.                                   (3)

Before using (3), the other two entries are exactly

    M[a,c'] = W[a,c'] A_c' + W[a,c] A_c q1,
    M[r',a] = B_r' (W[r',a] + q2 W[r,a]).              (4)

The query terms vanish by (3), without moving a query through any D factor.
The remaining terms are again entirely grade eight, so (1) implies

    W[a,c']=W[r',a]=0.                                 (5)

Equations (3),(5), for all a, say

    W=diag(Wm,Ws),       M=diag(Mm,Ws),
    Mm=T2_main Wm T1_main.                             (6)

Both Wm and Ws are invertible over B_f. Indeed, multiplying a two-sided
inverse of the block diagonal W on either side gives a two-sided inverse
for each diagonal block. This works for every finite s, including s=0.

## The scratch block already uses the entire projected rank

Let Pi=pi_{0,...,16} and P=diag(0,0,I_s). The endpoint equation gives

    Pi(M) = L^-1 P R^-1.                               (7)

The right side lies in Mat_{2+s}(B_f). Independently, (1) implies
Pi(Mm)=pi_0(Mm), so the left side of (7) also lies in that matrix algebra.
Thus the following rank comparison is on B_f^{2+s}, rather than an
unjustified restriction of an A_f-valued map to B_f.

Put d=dim_K(B_f). Act by left multiplication on columns in the right regular
module B_f^{2+s}; its K-dimension is (2+s)d. L and R are invertible on that
space. The right side of (7) therefore has K-rank sd. By (6), its left side is

    diag(Pi(Mm), Ws).

The invertible Ws block already has rank sd. Rank additivity for this block
diagonal K-linear map forces Pi(Mm) to have rank zero on B_f^2. Left regular
multiplication is faithful: a nonzero entry acts nontrivially on the column
having 1 in its input position. Consequently

    Pi(Mm)=0                                          (8)

as an algebra element. This is not an accidental small-width operator
identity, and it does not use an integral-domain or division-ring property.

## Apply the two-owner zero-column implication

Use the same c,r as above. Directly,

    Mm[r,c] = B_r Wm[r,c] A_c.

Every word here has grade at most 8+0+8=16. Hence it is its own Pi projection;
(8) makes it zero and the group-unit factors give Wm[r,c]=0. The other entry
of the same input column is

    Mm[r',c] = B_r' (Wm[r',c] + q2 Wm[r,c]) A_c
             = B_r' Wm[r',c] A_c.

The same grade bound and (8) give Wm[r',c]=0. Thus Wm has a zero column,
contradicting invertibility. This is precisely PR4920's direct zero-column
step. It needs no reduced outer main-only L/R, and presumes no such reduced
matrices invertible. All four shear orientation pairs were retained.

## Why this is an all-width obstruction

The argument above holds in A_f for every central character. To pass from
literal tensor operators to A_f, use PR4920/PR4928's separating-polynomial
lemma, recalled here to make the hypothesis explicit. Choose one matrix
representative v_t per projective class G/Z, and put m=|G/Z|. For each t and
u!=t, choose a linear functional that vanishes on v_u and not on v_t. Their
product isolates v_t in degree m-1. Multiplication by powers of a functional
nonzero on v_t extends this to every degree f>=m-1. Applied to tensor powers,
these functionals prove the v_t^{tensor f} linearly independent for every
such f. The central-character tensor representation of A_f is then injective.

Therefore a literal endpoint at every positive column width would give the
forbidden algebra identity at every sufficiently large width. Coefficients,
controls, query choices, and the finite scratch count may depend on f within
the same fixed finite one-column alphabet. The argument is applied separately
at each sufficiently large f, so width-dependent coefficients do not help.
The finite checker corroborates formulas and grade supports; it does not
replace this all-width proof by a width-one matrix experiment.

## Exact advance and remaining boundary

PR4920's full-monomial grade theorem had exactly two owners and explicitly
excluded scratch mixing. PR4928 allowed identity scratch and simultaneously
transformed helper jobs, but only in a separated central/transverse algebra.
Neither result alone establishes this full-monomial identity-scratch extension.
The new ingredient is (2)-(5), forcing decoupling via grades 1 through 16,
followed by the rank budget (7)-(8).

The theorem includes arbitrary main/scratch owner mixing by L,W,R, all full
monomial central/fresh routes, all shear orientations, role-dependent rank-eight
raw factors, and arbitrary restored identity scratch. It excludes mixing the
productive native helper operations, native prefixes, altered FULLs, additional
paid nonmonomial calls, discarded main-dependent garbage, noninvertible global
owner controls without a reversible restored extension, and non-columnwise or
arbitrary width-specific address operations outside the fixed finite alphabet.
Already transformed helper input/output contracts cannot be replaced by the
identity-scratch contract without justification.

No new endpoint, invoice improvement, kappa, complete compiler replay, formal
proof-kernel verification, or independent human review is claimed.
