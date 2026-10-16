# Case 30: the remaining sixteen-term profile is impossible

This note excludes exactly the following profile: a rational factorization
of `I15` into sixteen nonzero rank-one terms, two with whole-group charge 1
and fourteen with charge 3. It covers all 21 cheap-pair branches of that
profile. It does **not** combine earlier solver receipts into a claim about
other term counts, other profiles, or the global P112 decoder.

The five ordered physical triads, with names A, B, C, D, E, have ports

```
A [10,18,93]   B [6,36,74]   C [13,23,102]
D [41,73,88]   E [30,50,87].
```

Every pair of these triads has nonzero physical pairing, so the strict
endpoint on their three payload coordinates each is exactly `I15`.
All prices below charge the complete physical triad spaces touched by a
factor, regardless of its active payload coordinates.
A common nonzero rational scalar multiplying `I15` is equivalent after
rescaling one factor family, which preserves every group support and price.

## 1. A restricted rational bilinear lift

Let `E_g` be the three authenticated binary labels of group g. Form the
15-by-15 rational matrix `H` whose `(g,h)` block is the literal binary dot
pairing between the labels of `E_g` and `E_h`, interpreted as rational zeros
and ones. Replace each off-diagonal block between two different groups in
`{A,C,D}` by `J3/3`. Those original blocks are all `J3`. Leave every other
entry unchanged. In particular `H_gg=I3`.

For masks `s,t` in 1..31, write `h(s,t)=rank_Q H[s,t]` and let `rho(s,t)` be
the actual binary whole-group tariff. The exact replay checks all 961
ordered rectangles and establishes these limited domination facts:

* There are 14 rectangles with tariff 1, and all satisfy `h<=1`.
* There are 273 rectangles with tariff 3. Of these, 165 have `s&t != 0`,
  and all 165 satisfy `h<=3`.

No domination claim is made for arbitrary other rectangles. Indeed this
matrix is deliberately **not** a universal lift for the five-group module.

Given a payload factor `u v^T`, form its 45-by-45 lift with `(g,h)` block

```
(u_g v_h^T) tensor H_gh.
```

If the exact nonzero group supports are `(s,t)`, this equals
`D_u H[s,t] D_v^T`, where each diagonal block of `D_u` is `u_g tensor I3`
and similarly for `D_v`. Every such block has full column rank 3. Thus the
lifted factor has rank exactly `h(s,t)`. The lift of an `I15` endpoint is
`I45`, including arbitrary mixtures of the three payload coordinates.

## 2. The complementary projector restricts the disjoint types

Write a proposed factorization as `UV^T=I15`, where U, V each have 16
columns. Then

```
P=I16-V^T U
```

is an idempotent rank-one matrix of trace 1. If a term's source and reader
group supports are disjoint, its ordinary trace is zero, hence `P_tt=1`.
Every tariff 1 type is disjoint.

Two indices with nonzero diagonal entries in a rank-one matrix have
nonzero entries in both cross positions. Therefore their source/reader
types `(a,b)` and `(c,d)` must satisfy `a&d != 0` and `c&b != 0`.
In particular the two cheap types are distinct: two copies of a disjoint
type fail this cross condition. Thus the initial unordered domain has
`binomial(14,2)=91` pairs.

The two cheap terms already contribute 2 to `trace(P)`. Among the fourteen
other terms there must be a common-footprint term with nonzero projector
diagonal: otherwise their diagonal contributions would each be either 0
(common footprint) or 1 (disjoint footprint), and could not sum to -1.
Such a common-footprint term must cross both cheap types. Enumerating the
fourteen tariff 1 types with these two necessary conditions gives exactly
21 unordered cheap-pair branches, with no coefficient restriction.

Every disjoint tariff 3 term also has projector diagonal 1 and must cross
both cheap types. The replay enumerates precisely that finite set in each
of the 21 branches. For 17 branches all permitted regular types satisfy
`h<=3`. Four branches have one exceptional permitted type each:

| Cheap pair | Exceptional `(source,reader)` masks | Lift rank | Tariff |
|---|---:|---:|---:|
| `(1,12), (8,5)` | `(20,9)` | 4 | 3 |
| `(4,9), (8,5)` | `(17,12)` | 4 | 3 |
| `(5,8), (9,4)` | `(12,17)` | 4 | 3 |
| `(5,8), (12,1)` | `(9,20)` | 4 | 3 |

All four exceptional types are disjoint. There cannot be two terms of
one such type: their entire 2-by-2 reverse-product block in `V^T U` would
be zero, giving an `I2` principal block in the rank-one matrix P.
Thus each branch contains at most one exceptional term.

## 3. Rank equality excludes the four exceptional branches

If no exceptional term occurs, the sum of the lifted term ranks is at
most `2*1+14*3=44`. Their sum is `I45`, a contradiction.

If one exceptional term occurs, the rank sum is at most 45 and hence
exactly 45. The following elementary equality lemma applies.

**Rank-sum equality lemma.** If `I_n=sum A_t` and
`sum rank(A_t)=n`, then every `A_t` is idempotent. To see this, choose rank
factorizations `A_t=X_t Y_t`, concatenate the X blocks into the square
matrix X and stack the Y blocks into Y. Since `XY=I_n`, also `YX=I_n`.
Its diagonal blocks give `Y_t X_t=I`, so `A_t^2=A_t`.

The exceptional lifted term is nonzero of rank 4. But its source and
reader group supports are disjoint, so its square is zero. It cannot be
idempotent. This contradiction closes the four remaining branches.

Therefore all 21 branches of the stated sixteen-term price profile are
impossible over Q. The proof also works over any characteristic-zero
field containing the coefficients, using the same finite rank premises.

## Replay and attribution

Run `verify.py` with Python 3.12 using
`-I -O -B`. It uses only the standard library, authenticates the retained
candidate/archive/label hashes, rebuilds all prices and rational ranks,
and prints a receipt without writing files. It imports no search, producer,
solver, or sibling verifier. `independent.py` separately rebuilds the matrix
as the integer matrix 3H, uses primitive integer elimination and reverse-order support
enumeration, and checks all 91 possible cheap-type pairs.

Controls include the literal direct-copy `I45` lift, an exact rational
sixteen-term redundant frame, factorwise injective-rank checks, all four
rank 4 square-zero types, a nonorthogonal rank-tight idempotent fixture,
the duplicate-type rank 2 projector contradiction, and mutations showing
that the division by 3 and the own identity blocks are material.

The custom five-triad candidate and its complete type census are included
in this package; no unpublished search receipt is a replay dependency.
Earlier support relaxations and gauge searches motivated the investigation
but are not premises. Separate AI agents reviewed the proof and independently
implemented the Fraction and primitive-integer replays. This is AI-assisted
research, not scientific admission or a new decoder construction.
