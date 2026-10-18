# Fitting rank for odd binary types

I first use the standard binary dot product on V=F2^d, with d=5 or 6. Write
O={x:x dot x=1} and j=(1,...,1). An admissible type is a pair (q,w) in
O times O with w dot q=1. A port list may contain any finite multiplicities
of these types. For its v distinct port positions I define the binary mask

    B_st = w_s dot q_t.

I call a v-by-v matrix N over a field K fitting if N_ss is nonzero and
N_st=0 whenever s is different from t and B_st=1. I interpret the binary
entries as zero or one in K. I make no assumption that N is symmetric,
positive, integral, or has a prescribed factorization.

I prove, over every coefficient field K,

    d=6: rank_K N >= ceil(3v/32),
    d=5: rank_K N >= ceil(17v/105).

These statements require the odd-type representation above. They are not
bounds for arbitrary binary matrices of rank five or six.
Section 5 gives the general even-dimensional bound and an odd baseline.
Section 6 proves the stronger odd-dimensional theorem using two flags.

## 1. A triangular selector

Let a=e_0 and let W be the odd vectors with coordinate zero equal to zero.
For d=6, order W as follows, using binary integers for vectors:

    2,4,8,14,16,22,26,28,32,38,42,44,50,52,56,62.

For d=5 use its first eight entries. Equivalently, take e_1 plus the
subsets of (e_1+e_2,...,e_1+e_(d-1)), in binary subset order. For the
ordered sinks w_0,...,w_(2^(d-2)-1), select the types

    S_k = {(q,w_k): q in O, q dot w_i=1 for every i<=k}.

List the blocks S_k in increasing k, with any fixed order inside a block.
For d=5 append the type (j,j). Call the resulting ordered selector S.

For a row from block i and a column from block k>=i, their mask entry is
one by construction. Within each block all mask entries are one. The
appended d=5 column also has mask entry one against each preceding row,
because those sinks are odd. A fitting principal matrix on S is therefore
lower triangular with nonzero diagonal.

The same conclusion holds when I include every port occurrence of each
selected type. Distinct copies force zero cross entries because their
mask entry is one. Thus, if n_t is the multiplicity of type t,

    rank N >= sum_(t in S) n_t.                         (1)

The prefix sink ranks are 1,2,3,3,4,4,4,4,5,...,5. The vector j is
independent of their span: a dot j=1 while a annihilates W. The equations
q dot j=1 and q dot w_i=1 therefore have rank r+1 for a prefix of rank r.
They are consistent: each linear relation among the odd w_i uses an even
number of them, so the prescribed right sides satisfy that relation.
Independent linear forms give every remaining right side. Each block
therefore has 2^(d-r-1) labels q. I obtain:

| d | Prefix block sizes | Added type | Total |
|---|---|---|---:|
| 6 | 16,8,4,4,2,2,2,2,1,1,1,1,1,1,1,1 | none | 48 |
| 5 | 8,4,2,2,1,1,1,1 | (31,31) | 21 |

I count diagonal types (2,2),(14,14),(62,62) in d=6. In d=5 I count
(2,2),(14,14),(31,31). The executable certificates check these lists,
the complete selector and every triangular mask entry.

## 2. Symmetry and multiplicities

Binary isometries act on both components of a type. I also allow the
exchange (q,w) -> (w,q). Isometries preserve B; exchange transposes B.
The image of S therefore gives either a lower- or an upper-triangular
fitting principal matrix. Inequality (1) holds for each such image.

For d=6, the isometry group is transitive on the 32 odd vectors. To see
this, fix an odd q. Its orthogonal complement has characteristic vector
j+q of norm one; the orthogonal complement of that vector inside q-perp
is a nondegenerate alternating four-space. Choosing a symplectic basis
there gives the same orthogonal decomposition for any odd q. The
stabilizer of q acts transitively on the 15 nonzero vectors in that
alternating space. Every distinct odd w with q dot w=1 has the form
w=q+x for one of those 15 vectors. Thus admissible types have two orbits:
32 diagonal types and 480 cross types. S contains three and 45 respectively.

For d=5, j has norm one and V is the orthogonal sum of span(j) and a
nondegenerate alternating four-space H. Write q=j+x and w=j+y. The
admissibility equation is x dot y=0. Symplectic basis extension and
source/sink exchange give the following four orbits:

| Orbit | Description | Size | Selected |
|---|---|---:|---:|
| special | x=y=0 | 1 | 1 |
| one-special | exactly one of x,y is zero | 30 | 8 |
| diagonal | x=y nonzero | 15 | 2 |
| cross | x,y nonzero and distinct, x dot y=0 | 90 | 10 |

For the last row, each of 15 nonzero x has six nonzero orthogonal choices
y different from x. Any such pair extends to a symplectic basis. The
finite checkers also reconstruct these orbits from explicit isometries,
using different generator families.

Average (1) over the finite symmetry group. A type in an orbit A occurs
in a uniformly chosen image with probability |A intersect S|/|A|. I average
integer cardinalities as rational numbers, not matrices over K, so the
argument also covers fields whose characteristic divides the group order.
For d=6 both fractions equal 3/32. Hence rank N>=3v/32.

For the baseline d=5 selector, write v_special, v_one, v_diagonal and v_cross for occurrence
counts, including repetitions. I obtain the stronger inequality

    rank N >= v_special + (4/15)v_one
              + (2/15)v_diagonal + (1/9)v_cross.        (2)

Every coefficient in (2) is at least 1/9. This gives a baseline bound;
the two flags in section 6 improve it. Taking ceilings is valid because
rank is an integer.

## 3. Copy terms and linear rank slack

In the retained unit model, write N=sum_(l=1)^J r_l a_l^T. Define

    X_l = diag(r_l) B_lift diag(a_l),
    beta_l = rank_F2 B[supp(r_l),supp(a_l)],
    C = sum_l beta_l.

A term of charge zero has an all-zero mask rectangle, so its X_l is
zero. I may remove such terms and form a new fitting N from the remaining
terms. The new N still has rank at most their number J. I apply the rank
bound to this N; free terms cannot inflate the count needed below.

If every remaining beta_l is at least five, then in dimension six

    J >= ceil(3v/32),
    C >= 5 ceil(3v/32) >= (15/32)v.

The ratio 15/32=.46875 exceeds the source's .45 screen by 3/160. This is
a lower bound under the declared additive support-rank tariff. Mixtures
with lower charges need their own invoice; I do not close the complete
small-unit lane.

If each X_l has rational rank 16, the total rank satisfies

    sum_l rank X_l = 16J >= 16 ceil(3v/32) >= 3v/2.    (3)

Thus such a complete unit needs at least v/2 aggregate rank slack. This
conclusion does not assume that the totals are idempotent. It uses the
fitting mask; it is not an extension of the predecessor's invalid
homogeneous per-total trace rows.

For the proposed literal identity sum of rank-16 idempotents over a
characteristic-zero field, taking traces gives v=16J. This contradicts
(3) for v>0. Hence full-rank orbit-77 projectors alone cannot resolve I_v,
even with independent diagonal gauges, repetitions, either orientation
and arbitrary port multiplicities. The same contradiction applies to an
explicitly rank-additive assembly over any field.

Identity is essential to the trace corollary. A general fitting unit has
B_lift .* N=D with an arbitrary nonzero diagonal D. Row normalization
preserves fitting rank and support costs, but it may destroy individual
idempotency. I do not use it to convert an arbitrary idempotent sum D into
the identity case. The cost and rank-slack bounds themselves require only
the nonzero fitting diagonal.

## 4. Paired windows and remaining scope

For a bit twin whose actual window is h_b=rank_Q N, section 6 gives
17v<=105h_b in dimension five, while 3v<=32h_b holds in dimension six.
In particular, h_b<=5 permits at most 30 and 53 ports respectively.
The weighted flag maximum can tighten the first restriction. The previous
source rows were v<=16h_b and v<=17h_b.
I do not replace the bit twin's copy invoice by the complex invoice.

The retained rank-16 projector remains valid as a local example. Its
rank-one scalar factor does not fit the complete unit mask. The checker
verifies its exact factor identity and rejects that attempted promotion.

I leave lower-rank totals, mixed charges, sufficiently non-additive
assemblies and changed label/mask contracts open. I supply no native
producer, complete supplier, selected-frontier update or new multiplication
exponent. The proof uses the explicit finite geometry above for a theorem
over arbitrary finite multiplicities; the bounded replays corroborate its
finite ingredients and failure controls rather than exhaust its quantifiers.

## 5. General ambient dimension

I now take any integer d>=2 and retain the same odd-type and fitting
conditions. I use the ordered affine flag from section 1 in the odd
hyperplane e_0-perp. The first sink contributes 2^(d-2) types. For each
prefix rank r=2,...,d-1, I have 2^(r-2) sinks, each contributing
2^(d-r-1) types. Thus the prefix selector has d*2^(d-3) types. For d=2
this expression equals one and there are no higher-rank prefixes.

For completeness, write the subset index as m. The sink w_m has low
coordinate 1+wt(m) modulo two and higher coordinates m. To select its
diagonal type, its pairing with w_0 forces wt(m) even. Pairing with all
earlier sinks then requires every bit through the highest bit of m to
be one. Hence m=2^(2t)-1, including m=0. I obtain d/2 diagonal types
when d is even and (d-1)/2 when d is odd.

For even d, the odd-vector stabilizer uses a nondegenerate alternating
space of dimension d-2, as in section 2. The admissible type orbits have
the following sizes and selector counts:

| Orbit | Size | Selected |
|---|---:|---:|
| diagonal | 2^(d-1) | d/2 |
| cross | 2^(d-1)(2^(d-2)-1) | (d/2)(2^(d-2)-1) |

At d=2 I omit the empty cross orbit. Both nonempty orbit fractions equal
d/2^d. The same multiplicity argument proves, over any coefficient field,

    d even, d>=2: rank N >= ceil((d/2^d) v).            (4)

For odd d, I append (j,j) and use the alternating space j-perp of
dimension d-1. Put t=2^(d-2) and n=2t-1. The four-orbit table becomes:

| Orbit | Size | Selected |
|---|---:|---:|
| special | 1 | 1 |
| one-special | 2n | t |
| other diagonal | n | (d-1)/2 |
| cross | n(t-2) | ((d-2)t-(d-1))/2 |

I count the one-special entries by taking q=j for each of the t prefix
sinks. At d=3 the cross orbit is empty and the other fractions give
rank N>=ceil(v/3). For this baseline selector at odd d>=5 the cross fraction is

    rho_d = ((d-2)t-(d-1)) / (2n(t-2)).

I have t>d-1 for d>=5: it holds at d=5, and increasing d by two
multiplies t by four while increasing d-1 by two. Direct comparison
then gives rho_d <= (d-1)/(2n) <= t/(2n) <= 1. Thus

    d odd, d>=5: rank N >= ceil(rho_d v).               (5)

Its weighted bound uses the four individual orbit fractions.
Equations (4) and (5) give 3/32 and the baseline 1/9. They concern
the same odd-type fitting model; no new native-cost or supplier conclusion
follows from changing the ambient dimension alone. `general.py` checks
the finite geometry for d=2,...,8 and the formula's edge cases. The
general proof uses the affine ranks and symplectic decompositions above,
not extrapolation from that replay.

Writing rho for the applicable uniform coefficient, the same rank-one
factorization argument gives J>=ceil(rho v). Constant-charge beta terms
therefore cost at least beta*ceil(rho v). Constant-rank R masked totals
need aggregate rank at least R*ceil(rho v). A literal identity sum of
rank-R idempotents over characteristic zero can exist only if R*rho<=1.
Section 6 strengthens the odd-dimensional coefficient. These remain
necessary tests under the fitting model, not constructions or complete
supplier prices.

## 6. Stronger odd-dimensional flags

Let d=2k+1>=3, j=(1,...,1), and H=j-perp. The binary form on H is
nondegenerate and alternating, with dimension 2k. Write q=j+x and w=j+y
for x,y in H. Admissible types satisfy x dot y=0. For port positions s,t,

    B_st = 1 + y_s dot x_t  in F2.

I lift the resulting bit, not the integer expression 1+y_s dot x_t,
into the coefficient field. This distinction matters when the binary
pairing is one.

Put t=2^(d-2), n=2t-1, and L=(d-3)t+1. There are four type orbits under
symplectic isometries of H and source/sink exchange: the special type
(x,y)=(0,0); 2n one-special types; n other diagonal types; and n(t-2)
cross types. The last orbit is empty at d=3.

### Exact removal of special ports

A port with w=j has an isolated nonzero row in N. A port with q=j has
an isolated nonzero column. Let p count all occurrences of such ports,
including repetitions, counting each occurrence once. The row-special
class has w=j and q!=j; the column-special class has q=j and w!=j;
the special class has q=w=j. Order these as row-special, regular,
column-special, and special. The fitting matrix has block form

    [ D_B  0   0   0 ]
    [ E    M   0   0 ]
    [ F    G   D_A 0 ]
    [ 0    0   0   D_S ],

where the D blocks are invertible diagonal matrices. Row and column
elimination remove E,F,G without changing M. Therefore, over any field,

    rank N = p + rank M.                              (6)

Thus these ports contribute one rank each, rather than a fractional
contribution. The regular port counts below are v_D for other diagonal
types and v_C for cross types; v=p+v_D+v_C.

### Two complete flags

Choose a symplectic basis e_1,f_1,...,e_k,f_k of H. I use two orders:

    low:  e_1,f_1,e_2,f_2,...,e_k,f_k,
    high: e_1,...,e_k,f_1,...,f_k.

For either order, enumerate all y in binary subset order, starting at
zero. At y_i, include every x orthogonal to the span of y_0,...,y_i.
Every selected mask entry from an earlier row to a later column is one,
so this again gives a triangular fitting principal matrix. Each flag
contains every special and one-special type.

Let P_r be the span of the first r basis vectors. Binary subset order
has 2^(r-1) new sinks in P_r outside P_(r-1). Each allows 2^(2k-r)
labels. The rank-zero block contributes 2^(2k)=2t, and each rank
r=1,...,2k contributes t. Thus each selector has (d+1)t types, of which
4t-1 are special or one-special. Its regular count is L.

A regular diagonal selection at level r is a vector in
rad(P_r) outside P_(r-1). In low order the radical has one new vector
at each odd r and none at even r, giving k diagonal selections. In high
order the first k prefix spaces are isotropic and contribute
1+2+...+2^(k-1)=2^k-1. Later radicals lie inside the previous prefix,
so they contribute no new diagonal selection. Write

    D_low=k,       D_high=2^k-1.

For d>=5, average each flag over the finite symmetry group. The two
weighted rank bounds are

    R_D = p + (D/n) v_D + ((L-D)/(n(t-2))) v_C,
    rank N >= ceil(max(R_low,R_high)).                 (7)

Every type occurrence contributes separately. I average integer counts
over the rationals, so no group-order inverse is needed in the
coefficient field.

### Balanced coefficient and scope

Put D_star=L/(t-1). For k>=2,

    D_star = 2k-2 + (2k-1)/(t-1),
    k < D_star < 2^k-1.

The lower inequality follows from 2k-2>=k, with a positive remainder.
For the upper one, t>2k holds at k=2 and persists as k increases; it
implies D_star<2k-1<=2^k-1. Hence the high-flag
weight alpha=(D_star-k)/(2^k-1-k) lies strictly between zero and one.
This mixture equalizes the two regular orbit densities at

    rho_d = L/(n(t-1)).

As an orbit density, rho_d lies in (0,1]. I obtain the conclusions

    rank N >= p + ceil(rho_d (v-p)) >= ceil(rho_d v).  (8)

At d=3 both flags coincide, the cross orbit is empty, and the same
conclusion holds with rho_3=1/3. I do not divide by the vanished mixing
denominator. The exact d=5 and d=7 coefficients are 17/105 and 43/651;
the high-flag weights are 3/7 and 9/31.

Equation (7) retains more information than (8). In fact

    R_high-R_low = ((2^k-1-k)/n)(v_D-v_C/(t-2)).

The weighted maximum improves the balanced expression unless
v_C=(t-2)v_D, although integer ceilings can erase that gain. I claim no
optimal fitting matrix. Below I prove the precise limit of convex
averaging of triangular principal-minor bounds on the regular types.

For an actual bit window h_b=rank_Q N, (8) gives

    v <= p + floor((h_b-p)/rho_d).

At d=5, h_b<=5 permits at most 30 ports. After zero-charge terms are
removed, if every remaining copy charge is at least b, section 3 gives
C>=b ceil(max(R_low,R_high))>=b rho_d v. In particular, the d=5 floor
for charges at least five is 17/21, above the source's .7275 scouting
screen. That comparison does not certify a supplier or its bit-copy bill.

The rank-slack and literal-idempotent conclusions also use the stronger
rho_d. For constant masked-total rank r, aggregate rank is at least
r ceil(rho_d v). A rank-additive assembly, or a literal identity sum of
rank-r idempotents over characteristic zero, is impossible if r rho_d>1.
For mixed ranks in a rank-additive unit, I combine J>=rho_d v with
sum_l rank X_l=v to obtain mean masked-total rank v/J<=1/rho_d.
For a literal identity sum of idempotents over characteristic zero,
I obtain the same equality by taking traces, without a commutativity
assumption. At d=5, if J_15 terms have rank 15 and J_1 have rank one,

    17(15 J_15+J_1) <= 105(J_15+J_1),
    44 J_1 >= 75 J_15.                              (9)

I obtain equality in this integer count condition only at
(J_15,J_1)=(44m,75m). I do not construct an attaining assembly or
derive its native copy invoice. I retain the literal identity and
characteristic-zero hypotheses for the trace argument from section 3.
I leave lower-charge mixtures, lower-rank totals, sufficiently
non-additive assemblies and changed fitting masks open.

### Optimal uniform coefficient from triangular selectors

Take one occurrence of each regular type (x,y), with x,y nonzero and
x dot y=0, in H of dimension m=2k. Consider any ordered triangular
selector, including selectors outside the two flag families. Order its
distinct sinks y_i by first occurrence and let r_i be their prefix rank.
Every selected source at sink y_i is orthogonal to y_1,...,y_i: its
position follows their first occurrences, and its own type is admissible.
There are at most f(r_i)=2^(m-r_i)-1 such nonzero sources. Distinct types
with this sink have distinct sources, so the selector has size at most
sum_i f(r_i).

Let A_r count the distinct sinks whose prefix rank is at most r. They
lie in a subspace of dimension at most r, so A_r<=2^r-1. Since f(m)=0,
I sum by parts to obtain

    sum_i f(r_i)
      = sum_(r=1)^(m-1) A_r (f(r)-f(r+1))
      <= sum_(r=1)^(m-1) (2^r-1) 2^(m-r-1)
      = (m-2) 2^(m-1)+1 = L.                        (10)

Either complete flag attains L regular types. Thus I obtain the exact
maximum over triangular selectors for this uniform, distinct-type
population. I use that population as a test of any proposed universal
linear coefficient from convex averages of these minor-size bounds.
It has n(t-1) regular types, while each minor and each convex average
has value at most L. No such average gives a coefficient greater than
rho_d=L/(n(t-1)); the balanced flags attain rho_d for arbitrary
multiplicities. Repeated occurrences do not invalidate this limitation,
because the distinct-type population is one allowed multiset.

I restrict this optimality claim to convex averages of triangular
principal-minor size bounds. I leave stronger fitting-rank inequalities,
nontriangular minors and more general combinations of rank information
open. I do not infer that a fitting matrix of rank L exists at d>=5.
