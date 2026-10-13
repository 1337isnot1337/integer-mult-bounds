# Spectral split residuals: an exact interface with an unfavorable boundary cost

Research note and scoped negative result. Douglas R. Colkitt, with substantial
OpenAI Codex assistance. Apache-2.0. No new multiplication exponent.

An explicit encoder can put the complex residual `C_(9f)` into two separate
streams acted on by `C_(4f)` and `C_(5f)`, for every integer `f >= 1`.
Zero workspace returns to zero. Arbitrary dirty workspace can also be restored
by one explicitly described phase pass. This changes the interface behind the
earlier split-residual obstruction: it uses payload transforms and a phase
correction, not just a routing conjugation.

The proposed implementation nevertheless fails its favorable cost screen.
Its literal recursive profile is `2 C_(9f) + 3 C_(4f) + 3 C_(5f)`, on the
original per-stream volume. Even granting the two owner kernels for free
leaves `2 C_(9f) + 2 C_(4f) + 2 C_(5f)`. An obvious algebraic simplification
removes the owner sandwiches and leaves two width-9f transforms. Recognizing
the entire remaining operator simply recovers the original `C_(9f)` call.
This supplies no saving, even before movement, precision and workspace costs.

The result is an algebraically feasible alternative interface and an exact
accounting diagnostic for this encoder. It is **not** an impossibility theorem
for encoded hosting, a repair of #448's priced word, or a new supplier.

## Reproduce

From the repository root, with Python 3.10 or later and no external packages:

```sh
python3 -B research/clean-residual-dilation/verify.py
```

Expected output starts with
`PASS_EXACT_DILATION_AND_UNFAVORABLE_BOUNDARY_BUDGET`. The command checks source
pins, recomputes the certificate and compares every field with
[CERTIFICATE.json](CERTIFICATE.json). `--write /tmp/dilation.json` writes the
same deterministic result separately. It also works with `python3 -I -O`;
admission checks do not use Python `assert`.

## Starting point and scope selection

Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`. At this base the selected
conditional result is #626/#623/#622 with #543,
`kappa = 51110230636731/31250000000000000`. The
[selected review](../../docs/research/community-k492-review.md) and its actual
construction were read. The complex supplier binds. This note does not adopt
larger numbers from pending PRs.

The OS-generated assignment seed was **51**, assigning the recursive-interface
track. Among deferred helper cleanup, encoded residual hosting, and native bit
query fusion, hosting was selected. Cold-end/cleanup work is already extensive;
#521 has an exact native bit fusion primitive. The seed picks the split
`a = 1 + (51 mod 8) = 4`, `b = 9-a = 5`. Width 9 is motivated by the complex
helper geometry, not by treating a pending record as accepted. In particular,
the selected global profile already hosts whole helpers and has no width-9
child to which this note claims to apply a saving.

There was no pinned coordination issue. The local [claim](CLAIM.json) records
the three candidates, overlap checks, scope and time allocation. Exact source
and PR heads are in [SOURCE-PINS.json](SOURCE-PINS.json).

## What changes relative to the prior obstruction

Chafik Boukhalfa's [#451 trace obstruction](https://github.com/CrocSwap/integer-mult-bounds/blob/f3a38153678b55063fc005901cc968266166507d/research/cross-family-residual-obstruction/README.md)
shows that `C_(a+b) direct-sum I` and `C_a direct-sum C_b` have different traces.
They cannot be conjugate by an invertible linear map on the two complete
streams. The later [#448 discussion](https://github.com/CrocSwap/integer-mult-bounds/pull/448#issuecomment-6113842081)
also acknowledges the missing single-register, multi-stream realization.
Those findings remain valid.

Here a clean-input embedding leaves a complementary operator `B`, not `I`, on
the workspace. An additional `B^-1` phase pass then restores dirty workspace.
Thus the full program is not merely a similarity between the two operators
in #451. The proof below constructs the encoder and exposes its expense.
It does not rerun the already closed coordinate-routing search.

The [earlier Fourier boundary diagnostic](../fourier-boundary-fusion/REPORT.md)
already charged entrance and exit transforms in a copied-center scatter and
proved a scoped coordinate-cut inequality. This note credits that warning;
its new object is a direct sum of two separately acted-on streams, its changed
assumption is a spectral embedding with a complementary workspace action, and
its evidence includes exact dirty restoration. It does not claim a new
coordinate-only lower bound.

## Exact operator and all-f embedding

Work over the Gaussian rationals. Let

```text
C = (1/2) [[1+i, 1-i], [1-i, 1+i]],
H =       [[1,   1  ], [1,   -1 ]].
```

On an `N = 2^e` coefficient stream, `C_k` and `H_k` act on the low `k`
address coordinates and leave the others as spectators. Here `e = 9f`.
`H_k^-1 = 2^-k H_k`, and

```text
H_k C_k H_k^-1 = Delta_k,
Delta_k[x,x] = i^(popcount(x mod 2^k)).
```

The multiplicity of `i^j` in `C_k` is

```text
d_j(k;e) = 2^(e-k) sum_{t = j mod 4} binom(k,t),   j=0,1,2,3.
```

An injective intertwiner from `C_e` into `D = C_(4f) direct-sum C_(5f)`
exists exactly when each source eigenspace fits into its corresponding host
eigenspace. Necessity follows because an injective intertwiner maps each
eigenspace injectively to the same eigenvalue; sufficiency follows by choosing
such injections. All operators are diagonalizable since their fourth power
is the identity over a characteristic-zero field containing `i`.

At `f=1`, the exact dimensions are:

| Operator on one or two 512-coefficient streams | 1 | i | -1 | -i |
|---|---:|---:|---:|---:|
| source `C_9` | 136 | 136 | 120 | 120 |
| first host `C_4` | 64 | 128 | 192 | 128 |
| second host `C_5` | 96 | 96 | 160 | 160 |
| total host | 160 | 224 | 352 | 288 |
| workspace complement | 24 | 88 | 232 | 168 |

For completeness, this is not just a favorable finite example. Put
`p_j(k) = 2^-k sum_{t=j mod 4} binom(k,t)`. Pascal's identity gives

```text
p_j(k+1) = (p_j(k) + p_(j-1 mod 4)(k))/2.
```

Consequently `min_j p_j(k)` is nondecreasing and `max_j p_j(k)` is
nonincreasing. The exact rows at 4, 5 and 9 give

```text
min p(4) = 1/8,  min p(5) = 3/16,  max p(9) = 17/64.
```

For every `f>=1` and every `j`, the host capacity minus source demand,
divided by `N`, is therefore at least

```text
1/8 + 3/16 - 17/64 = 3/64 > 0.
```

This is a written proof for all `f`; the checker additionally compares
binomial and independent dynamic-programming counts through width 288 and
checks the proposed dilations for `f=1,...,32`. Those finite counts are not
presented as the proof of the universal statement.

## A literal encoder and its dirty restoration

Enumerate source addresses in increasing order. Send each source address to
the first unused host coordinate with the same phase eigenvalue, first
through host A and then host B. Complete this injection to a permutation `P`
by mapping the workspace addresses, in increasing order, to the unused host
slots, also in increasing order. This specifies a full permutation of `2N`
coordinates, not a copy or a many-to-one map.

Define

```text
E = (H_(4f)^-1 direct-sum H_(5f)^-1) P (H_e direct-sum I).
```

All factors are invertible. Let `B` be the diagonal phase on the workspace
whose `j`th entry is the host phase at `P[N+j]`. Direct conjugation gives

```text
E^-1 D E = C_e direct-sum B,
(I direct-sum B^-1) E^-1 D E = C_e direct-sum I.
```

The first identity implements `(h,0) -> (C_e h,0)`. The second implements
`(h,z) -> (C_e h,z)` for arbitrary dirty `h,z`. `B^-1` is an address-dependent
unit phase, not another recursive transform. It must still be computed and
applied. At `f=1`, scratch basis column 63 acquires phase `-i` if this repair
is omitted. The trace has not disappeared: it is carried by `B` and changed
by the explicitly added correction.

This is a standalone residual primitive. During `E` both streams contain
linear combinations of their inputs. No unchanged local scalar word is
allowed to read a supposedly single helper at an intermediate point. A port
to actual owner windows would have to provide exclusive use of both full
streams and compatible intervening operations. No such port is supplied.

## Complete recurrence and favorable cost screen

Let `T(k,N,p)` be the cost of the inherited `C_k` primitive on **N original
coefficient positions**, with coefficient bit budget `p`. In a parent at
width `mf`, all children below have the same `N=V/W` logical coefficient
volume. The workspace is another physical stream, not a second independent
copy of the requested input and not permission to replace `N` by `N/2`.

The inherited exact identity, also tested here, is

```text
H_k = (1-i)^k S_k C_k S_k,
H_k^-1 = 2^-k (1-i)^k S_k C_k S_k,
S_k[x,x] = i^(popcount(x mod 2^k)).
```

Each Walsh boundary therefore costs one width-k child plus two coefficient
passes, with its exact scalar combined into the second pass. There are six
Walsh boundaries and two owner calls. With `e=9f`, the full local bill is

```text
R(e,N,p) <= 2 T(e,N,p') + 3 T(4f,N,p') + 3 T(5f,N,p')
           + 12 Scan(N,p') + Scan(N,p')
           + 2 Route(2N,e,p') + Prep(e,p').
```

`Scan` pays a full coefficient pass, including its specified unit phase and
Gaussian-dyadic scalar multiplication. The thirteenth pass is dirty
restoration. `Route` includes reading, moving and writing both streams; it
includes creating and clearing private keys and sorting buffers. `Prep` includes the multiplicity
table, route descriptors and scalar preparation. For the clean variant,
replace the final repair pass by a paid initialization pass unless zero
workspace is explicitly supplied. No additional source copy is used. The
borrowed dirty variant restores its entire extra stream at return.

These terms can be bounded without a unit-cost wide-address assumption.
Binomial prefix counts rank and unrank the four phase classes. Binary search
in the count of unused slots handles the completed workspace permutation.
With `L=ceil(log2(2N))` and `Q=p+e+L+1`, quadratic integer arithmetic and
sequential merge routing give the conservative combined nonrecursive bound
`O(N Q^4 + Q^5)`, and `O(N Q + Q^4)` temporary bits, including route records.
For example there are `O(e^2)` prefix-count table entries of `O(e)` bits;
ranking uses `O(e)` such operations, and workspace unranking at most another
`O(e)` bisections. Routing sorts `2N` keyed records in `O(L)` merge passes.
This generous bound is only a complete upper invoice, not a transfer into
the repository's tight fixed-tape overhead allowance.

The coefficients are exact Gaussian dyadics. Every layer introduces only
`O(e)` numerator or denominator bits: the program has a fixed number of
transforms, their scalars have `O(e)` bits, and a butterfly sums at most four
integer components. Thus `p'=p+O(e)` suffices for this exact arithmetic
description. This does not establish the inherited numerical rounding or
precision guard for a new all-size supplier. Granting `p'=p` only makes the
following rejection more favorable.

In a conditional parent recurrence, replacing a single width-9f child by the
literal interface changes its term from

```text
(9/m)^sigma / W
```

to

```text
[2 (9/m)^sigma + 3 (4/m)^sigma + 3 (5/m)^sigma] / W.
```

For `0<sigma<=1` its ratio to the original term is at least
`2 + 3*(4/9) + 3*(5/9) = 5`. Even with both owner calls already paid by
someone else, the ratio is at least `4`. Each required source boundary
already has the entire original volume and width. Helpers, routing,
normalization, scratch preparation/restoration and precision can only add
expense; there is no uncharged recursion child.

There is also an obvious simplification that a fair screen must include.
The two `H_k C_k H_k^-1` host sandwiches can each be replaced by their
diagonal phase, eliminating their three recursive calls. The remaining
program uses `H_e`, phases/permutation and `H_e^-1`, for recursive ratio
`2`. Then `P^-1 (Delta_(4f) direct-sum Delta_(5f)) P = Delta_e direct-sum B`
allows the whole program to collapse to `C_e direct-sum I`: exactly the
starting implementation, ratio `1`, with no hosting saving. The checker
replays the partially collapsed program as well. The ratio-5 and ratio-4
figures describe the literal interface, not an optimality claim for its
algebraic operator.

If one tries to use this encoder as the recursion rule for its own width e,
the two source boundaries are same-width children, so it is not even a
strictly decreasing recursion. Used inside a larger parent it is a valid
priced substitution, but has the unfavorable moments above. The experiment
stops here. Since it fails even its optimistic complete budget, no owner
search, supplier replay or new assembly/kappa calculation is warranted.

## Exact evidence and limits

The checker constructs the actual 1024-position permutation and executes
the full dyadic circuit at `f=1`. It tests every one of the 512 complex basis
columns for the source and each of the 512 workspace columns, before and
after dirty restoration. Complex linearity covers arbitrary real and
imaginary coefficients. A separate tensor-entry formula checks `C_9` without
using the encoder or its butterfly routine. All source columns also check
both directions of the one-child Walsh reduction. The collapsed program is
checked on all 1024 columns. No floating point, random numerical tolerance,
or imported supplier verifier is used.

Eight controls reject: the genuinely infeasible `C_2` into `C_1 direct-sum
C_1` embedding (missing eigenvalue -1); an eigenvalue-mismatched route;
omitted source boundaries; omitted host entrance; omitted owner kernels;
omitted inverse normalization; unrestored dirty workspace; and the wrong
sign in dirty repair. These are concrete failures of identities or capacity,
not unsuccessful searches.

There is no optimization search. The seed selects one split; the deterministic
stopping rule was to stop after exact capacity, full `f=1` replay and complete
cost accounting. The certificate records completed finite coverage. It does
not certify a whole E8 word, ownership schedule, all-size physical compiler,
numerical precision contract, common tape, analytic transfer, or the full
integer-multiplication theorem. Those inherited assumptions remain with their
existing constructions. Neither the selected frontier nor `upstream/` changes.

## Attribution

The residual/Clifford frame interface and paid Walsh identity come from
icekylinx's frame construction and the repository's cumulative compiler work;
the selected #622/#623/#626 complex construction is credited to Jeremy Kothe
and Chafik Boukhalfa, with eumemic's #543 bit supplier and the predecessors
listed in its review. The unequal-width recurrence comes from the retained
[complex batching note](../../notes/batched-complex-rows.tex).

The split-hosting proposal is Sreekanth Nair / higherbeing's #448; the trace
obstruction is Chafik Boukhalfa's #451. The separate single-stream audit in
#448 is credited to hipotures / RaD with Claude assistance. Their observations
motivate the changed interface here; no endorsement or incorporation of their
pending packages is implied. Douglas Colkitt's earlier Fourier-boundary note,
also developed with Codex, supplies the prior warning about unpaid boundaries.
This encoder, exact checker and scoped accounting were developed by Douglas
R. Colkitt with substantial OpenAI Codex assistance, under Apache-2.0.
