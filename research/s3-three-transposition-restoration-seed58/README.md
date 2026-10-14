# Three-transposition S3 boundary: a four-child restoration carry

**Result type:** scoped typed-interface construction; no new kappa and no
selected-supplier admission.

## Exact result

Let the six workspace coordinates be indexed by the elements of S3, with
generators a=(12), b=(23), and c=(13). For a transposition h, one call applies
the right-regular row permutation R_h: g maps to gh. It computes and emits the
trivial-character reader L(W)=sum_g W_g from the incoming workspace W. This
reader costs one COPY and five ADD operations, and it is invariant under every
row permutation. The COPY initializes the designated output register, so it
does not leave an unpriced temporary or output move.

Define two typed call groups:

- A consists of the child sequence a,b,a. It emits three copies of L(W) and
  exits in frame R_c, since aba=c.
- B consists of the child c. It emits L(W) and exits in frame R_c.

For every h, L(R_h W)=sum_g W_{gh}=sum_g W_g because g maps to gh is a
bijection. Also aba=c and c²=e. Thus A and B each end in R_c, while their
composition returns every W exactly; the invariant makes all intermediate
reader outputs equal too.

Each elementary h-child has the exact typed endpoint W -> R_h W and emits
L(W) from the incoming dirty workspace. Its descendant cost Q_h(n) covers the
full recursive implementation below this boundary; it must preserve that
endpoint and observable contract. The frame update only permutes the six
workspace rows, so it needs no scratch helper or restoration copy.

The pair A;B returns the workspace to its exact incoming order because c²=e.
The inverse-order pair B;A does too. The sequence is noncommuting: a and b
do not commute, and the intermediate prefixes of a,b,a,c are all nonidentity.

Every transposition acts on the six regular rows as three disjoint logical
coordinate swaps. Each logical swap is realized in the integer operation
alphabet by `x += y; y -= x; x += y; NEG(y)`, which maps `(x,y)` to `(y,x)`
using exactly three signed ADDs and one NEG, with no scratch register. Thus a
forward frame change costs 9 ADD + 3 NEG. Returning either macro call to
canonical order costs the same. This is a minimum in the row-swap model: a
permutation on six rows with c cycles has exact swap distance 6-c, since one
swap changes cycle count by at most one and each cycle can be split into fixed
points with length minus one swaps. The operation word is also used in the
independent order-four paired-cycle work of [PR #1391](https://github.com/CrocSwap/integer-mult-bounds/pull/1391); this package rederives and replays its exact two-coordinate action. For arbitrary legal child sizes
n_1,...,n_4, let Q_h(n_j) be the full descendant cost below an elementary h
call, excluding its displayed local reader, row action and dispatch. Then
U_A=Q_a(n_1)+Q_b(n_2)+Q_a(n_3), and U_B=Q_c(n_4). With unit leaf, macro and
parent dispatch charges d_leaf, d_macro and d_root, the complete recurrence is:

    T_A = U_A + 3(1 COPY + 14 ADD + 3 NEG + d_leaf) + d_macro
    T_B = U_B +   (1 COPY + 14 ADD + 3 NEG + d_leaf) + d_macro
    T_eager(A,B) = d_root + T_A + T_B + 18 ADD + 6 NEG
    T_carried(A,B) = d_root + T_A + T_B

The finite fixture sets U_A=U_B=0 and d_leaf=d_macro=d_root=1. Its paired
vector invoice is 4 COPY + 74 ADD + 18 NEG + 7 dispatch = 103 eager, versus
4 COPY + 56 ADD + 12 NEG + 7 dispatch = 79 carried. The 24-primitive saving
is exactly the two redundant R_c restorations (18 ADD + 6 NEG). For the
complete two-direction echo A,B,B,A, all four macro exits would pay twelve
eager frame changes; the carried word has product c⁴=e and pays none:

    T_eager_echo = d_root + 2 T_A + 2 T_B + 36 ADD + 12 NEG
    T_carried_echo = d_root + 2 T_A + 2 T_B

With no descendants, the complete echo vector invoice is 8 COPY + 148 ADD +
36 NEG + 13 dispatch = 205 eager, versus 8 COPY + 112 ADD + 24 NEG + 13
dispatch = 157 carried. Its 48-primitive saving is 36 ADD + 12 NEG.
This is a local boundary result, not a multiplication recurrence or a
contraction claim. U_A and U_B remain explicit; no child cost is treated as
free. The fixture defines the reader, frame changes, output writes, leaf, macro
and parent dispatches, and restoration alphabet completely. It does not
identify a physical integer-multiplication supplier that implements these call
types. All component counts price COPY, signed ADD, NEG and dispatch as one
primitive each; no unit-cost SWAP is assumed.

## Exact audit and controls

The checker builds all six group elements and all right-regular actions, and
checks each emitted row-swap program against the direct permutation on basis
columns.
It examines all 45 reduced words of lengths one through four over the three
transpositions. There are no nontrivial reduced identity words of lengths one
through three and 12 at length four; all 12 use all three generators, and
a,b,a,c is one shortest witness. A parity
argument rules out odd lengths, and the length-two reduced words are products
of distinct transpositions.

The group and invariant-sum identities prove the all-integer endpoint and
observable statements. The replay also checks both pair orders and both echo
directions on all 729 workspace vectors in {-1,0,1}^6. Controls show that a single-coordinate
reader changes under the first transposition, the sign-character reader
changes sign, and replacing B by an identity-frame call leaves a nonzero
terminal repair costing 9 ADD + 3 NEG rather than a free restoration.

## Reproduce

From the repository root, using only the Python standard library:

~~~sh
python3 -I -O -B research/s3-three-transposition-restoration-seed58/verify.py
~~~

Expected final line:

~~~text
PASS_S3_THREE_TRANSPOSITION_BOUNDARY reduced_words=45 length4_relations=12 pair=103_vs79 echo=205_vs157 saved=24_and_48 workspace_vectors=729 no_new_kappa
~~~

The registered replay is:

~~~sh
python3.12 scripts/research_package.py --package research/s3-three-transposition-restoration-seed58
~~~

It also checks metadata and all source pins. [Local validation and limits](VALIDATION.md)
record the available Python version and unrun full replay. The selected record,
source manifest, assembly, review, integration receipt and catalogue background
are pinned in SOURCES.json. Base commit:
bce54fb3f895cbe5cd4c0eb477c3afeed100190f.

## Scope, predecessors and limits

The selected conditional result remains kappa=0.001672660197076918 from #1094
([selected record](../../certificates/selected-result.json), [source manifest](../community-frontier1094-audit/SELECTED-SOURCE.json),
[assembly](../community-frontier1094-audit/ASSEMBLY.json), [review](../../docs/research/community-batch1099-review.md),
[integration receipt](../../docs/research/community-batch1099-integration.json)).
The selected record still inherits the reviewed complex and bit supplier
interfaces; this result neither changes nor verifies them. The full selected
cold replay was not run for this separate abstract interface contribution.

This is distinct from the claimed [two-generator S3 sign-character word in
discussion #1381](https://github.com/CrocSwap/integer-mult-bounds/discussions/1381):
the present object uses all three transpositions, the shortest reduced
four-step relation, and the fully invariant trivial character. It is also
distinct from [PR #1391's order-four paired-cycle workspace](https://github.com/CrocSwap/integer-mult-bounds/pull/1391), which independently gives the exact 3-ADD/1-NEG coordinate-swap word reused and replayed here.
The refreshed pre-submission scan also found [PR #1410](https://github.com/CrocSwap/integer-mult-bounds/pull/1410), which carries PR #1391's order-four frame across two same-source root echoes. It shares the persistence objective but uses a different cyclic frame and schedule. This package adds an independent regular-S3 instance, a different trivial-character reader, the complete reduced-word census through length four, and reader/frame negative controls.
The general read-free/composable restoration condition in [PR #1155](https://github.com/CrocSwap/integer-mult-bounds/pull/1155),
the cancelling-reader cuts in [PR #1199](https://github.com/CrocSwap/integer-mult-bounds/pull/1199),
noncommuting reader wrapper in [PR #1203](https://github.com/CrocSwap/integer-mult-bounds/pull/1203),
invariant/nonzero reader criterion in [PR #1205](https://github.com/CrocSwap/integer-mult-bounds/pull/1205),
fixed-reader sign output in [PR #1227](https://github.com/CrocSwap/integer-mult-bounds/pull/1227),
and cyclic-output construction in [PR #1287](https://github.com/CrocSwap/integer-mult-bounds/pull/1287)
are predecessor context, not new claims here. This package adds a separately
checkable regular-S3 instance, complete boundary invoice and exact short-word
census. See CLAIM.md for candidate selection and overlap details.

## Open next questions

- **Can a selected supplier realize this typed invariant-reader pair?**
  This would be needed before the local restoration saving can alter a paid
  recursive profile. First step: pin one candidate supplier's ordered call
  trace, extract its six-row frame maps, reader and full child invoice, then
  check the A/B endpoint identities. Blocker: this package identifies no
  supplier call family with the required contract.

Prepared by Cinna Davis with substantial OpenAI Codex assistance. No
independent human review is claimed. New work is Apache-2.0.
