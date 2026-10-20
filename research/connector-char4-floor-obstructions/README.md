# Characteristic-four connector floor obstructions

For the unsigned dirty connector of
[PR #4231](https://github.com/CrocSwap/integer-mult-bounds/pull/4231), let
N(c) be the largest source count k at which every source operator and every
nonzero binary-mask output operator can be called exactly c times while
restoring the arbitrarily dirty connector. The complete-call floor is
c(k + 2^k - 1).
[PR #4248](https://github.com/CrocSwap/integer-mult-bounds/pull/4248)
attains nine sources in characteristic four and supplies the deletion lemma.
[PR #4255](https://github.com/CrocSwap/integer-mult-bounds/pull/4255)
proves N(4) <= 20.

This package establishes:

- **9 <= N(4) <= 18.** A translated-binary-cube argument excludes every
  nineteen-source floor walk. It bounds the obtainable binary masks,
  including zero, by 512,526, strictly below 524,288.
- **The maximum depth-two source count is four.** More sharply, a balanced
  five-source block serves at most 28 of the 31 nonzero masks using two
  prefix readouts. Exactly four words, up to source relabelling, attain 28.
- An all-ones readout normal form has eight possible source inventories
  across four gaps. It gives 19,448 inventory-type count vectors at k = 10,
  while leaving internal event orders to search.

The upper bound is a scoped written proof with bounded controls. The
five-source maximum and catalog are exhaustive finite results. They do not
exclude ten sources in a general depth-four walk. There is no new κ,
selected-frontier change or complete multiplication theorem.

## Interface and necessary conditions

A characteristic-four floor walk has length 4k and uses each immutable source
exactly four times. Every nonzero binary mask m must be a sum of four
possibly repeated boundary prefix vectors modulo four. This is #4231/#4248's
prefix criterion. Zero is obtained by reading the zero boundary four times.

Modulo two, a four-readout multiset reduces to an even subset of at most four
parity prefixes. Repeated parity-prefix values can be identified without
changing that set of parity sums. The full mod-four condition also constrains
how many prefixes can lie in a translate of the binary cube.

## 1. A translated-cube intersection bound

Let w have length L=4k, each source occurring four times. Let q_t be its
prefix in (Z/4)^k, with cyclic boundaries t=0,...,L-1. Let u_t=q_t mod2 and
let r=L-|{u_t}| be the number of repeated parity-prefix occurrences.

For any a in (Z/4)^k define V={t:q_t+a lies in {0,1}^k}, and s=|V|.
Put

    S0=min(k, floor((r+1)/2)),
    H(k,r)=k+S0+floor((k-S0)/4).

Then s<=H(k,r). In particular s<=2k.

Proof. If V is empty there is nothing to prove. Rotate the cycle to begin at
a boundary in V. This does not change r. In each coordinate, the four source
increments go once around Z/4. Relative to the allowed values {0,1}, exactly
one edge is internal, 0->1. The other three edges form a bad arc
1->2->3->0. All three edges of a source's bad arc belong to one connected
component of the portion of the cycle outside V.

An outside component is a maximal path with endpoints in V and interior
outside V. For such a path, let d be the number of source bad arcs it contains
and h the number of internal 0->1 source edges that occur while some other
coordinate is outside {0,1}. Then d>=1 and its length is exactly 3d+h.
Across all outside components, sum d=k. Write I=sum h and let R be the
number of outside components. Exactly k-I edges have both endpoints in V.
Each vertex of V is either preceded by one of these edges or by an entry
from an outside component, so

    s=k-I+R.

Call a component small if h=0 and d<=3, and write S for their number. A small
component has 3d+1 boundary vertices, and its parity prefixes vary in at most
d coordinates. Thus it has at least 3d+1-2^d repeated parity occurrences,
which is at least two for d=1,2,3.

Charge each repeated occurrence to its later position within the component.
No component's first position is charged, so these charges are disjoint even
when consecutive outside components share their endpoint. All are among the
r globally repeated positions, except possibly the final position L that
was identified with position zero. Consequently 2S<=r+1.

Components with h>=1 contribute 1-h<=0 to R-I. Every non-small component
with h=0 consumes at least four source bad arcs. The S small components
consume at least S bad arcs. Therefore

    R-I <= S+floor((k-S)/4).

The right side is nondecreasing in S, and S<=min(k,floor((r+1)/2))=S0.
Combining these inequalities proves the bound.

## 2. Four-boundary sums

Fix three distinct boundaries. The possible fourth boundaries giving a
binary sum are the intersection with a translate of {0,1}^k. There are at
most H(k,r) of them. Every valid four-element boundary set is counted four
times by its three-element subsets. Hence the number of valid four-element
sets is at most

    floor(C(4k,3)*H(k,r)/4).

A four-boundary multiset with a repeated index has an even parity support
of size at most two. Since a binary mask equals its parity vector, all such
readouts together give at most 1+C(4k,2) distinct masks, including zero.
It follows that the number of binary masks obtainable by four readouts is
at most

    floor(C(4k,3)*H(k,r)/4)+C(4k,2)+1.

Separately, identifying repeated parity prefixes gives the elementary bound

    1+C(4k-r,2)+C(4k-r,4),

with binomial coefficients zero when their lower argument exceeds the upper.

## 3. Evaluation at k=19

For r<=15, S0<=8, so H(19,r)<=19+8+floor(11/4)=29. Thus the number of
obtainable binary masks, including zero, is at most

    C(76,3)*29/4+C(76,2)+1
      =509675+2850+1
      =512526 < 524288=2^19.

For r>=16, there are at most 60 distinct parity prefixes. The elementary
even-subset bound is at most

    1+C(60,2)+C(60,4)=489406 < 524288.

Every case excludes a characteristic-four floor walk at nineteen sources.
The cited deletion lemma then gives N(4)<=18. With the cited nine-source
certificate the interval becomes 9<=N(4)<=18.

## A normal form for future construction searches

Take four readout boundaries for the all-ones mask and rotate the source walk
to begin at the first. Every prefix is translated by the same vector, so each
four-prefix sum changes by four times that vector, which vanishes modulo four.
The four cyclic gaps partition the source events.

For each source, its gap inventory (a, b, c, d) has total four and satisfies
3a + 2b + c = 1 modulo four. Exactly eight of the 35 weak compositions satisfy
this equation: the cyclic rotations of (3, 0, 0, 1) and (0, 2, 1, 1).
Every source misses at least one gap. Repeated readouts give empty gaps and
remain allowed.

Up to source relabelling, the inventory-type counts have C(k+7, 7)
possibilities, giving 19,448 at k = 10. This counts inventories, not event
orders. Each gap's prescribed multiset still needs an internal ordering.
When labels are fixed by inventory type, first-occurrence symmetry can be
imposed only within equal-type classes. No ten-source exclusion follows.

## Sharp depth-two obstruction

A block has depth at most two if every binary mask is a sum of at most two
of its prefix-count vectors modulo four. Boundary zero pads shorter reads.
Two concatenated two-source depth-one blocks from #4248 attain four sources.

The complete first-occurrence-canonical census at five sources accounts for
all 20! / ((4!)^5 * 5!) = 2,546,168,625 words. None reaches 30 masks including
zero, and exactly four reach 29. [MAXIMIZERS.json](MAXIMIZERS.json) lists those
four words, their missing nonzero masks and their four-permutation structure.
Each is checked directly. The count of four plus four distinct valid canonical
witnesses proves catalog completeness up to source relabelling only.
Rotation and reversal are not quotiented out.

[DEPTH2.md](DEPTH2.md) gives the safe future-cut relaxation, exact subtree
accounting and replay details. The threshold-30 census visits 8,462,068 nodes
and prunes 6,451,947 subtrees. The threshold-29 census visits 8,715,495 nodes
and prunes 6,632,616 subtrees. Both account for the complete canonical family.
Source deletion preserves depth at most two, so failure at five sources
excludes every larger depth-two block. This closes the concatenation route
using two five-source depth-two blocks, while allowing coupled depth-four
searches.

## Reproduction

From the repository root with CPython 3.12:

```sh
~/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/connector-char4-floor-obstructions/verify.py
~/git/integer-mult-bounds/.venv/bin/python3.12 -W error -B research/connector-char4-floor-obstructions/independent_check.py
~/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/connector-char4-floor-obstructions
~/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/connector-char4-floor-obstructions --check-source-history
```

Expected main marker:
`PASS_CONNECTOR_CHAR4_FLOOR_OBSTRUCTIONS N4<=18 depth2_max=4 depth2_k5_coverage=28`.
Both registered checkers also run with optimized Python and explicit checks.
The main verifier recomputes [CERTIFICATE.json](CERTIFICATE.json), including
all 76 duplicate-count cases, the inventory enumeration, full-coverage
controls, the sharp depth-two censuses and the maximizer catalog. Certificate
regeneration is available through `verify.py --write-certificate`.
Each checker prints a generated receipt bound to all package files.

The main cube control checks all 70 labelled two-source words at all 16
translations and all 34,650 labelled three-source words at all 64 translations,
for 2,218,720 translations. It also checks 4,000 deterministic larger words
at 100 translations each. The separately written component checker uses
literal coordinate states on 21,120 cases, directly checking the outside
components, disjoint repeated-parity charges and arithmetic table. It also
checks every maximizer independently.

The depth-two Python replay checks its future-cut tables directly and compares
with an unpruned coordinate evaluator through three sources at every mask
threshold. A separately written iterative C engine agrees with every field
of both sharp five-source censuses and accounts for all 2,627,625 four-source
canonical words with negative feasibility pruning disabled, finding 421
full-cover solutions. Already-satisfied prefixes may still aggregate their
canonical completions. Its opt-in
commands are in DEPTH2.md; it is not a registered CI obligation.
Predecessor constructions and exclusions are cited dependencies, not new
audit deliverables. Their exact heads and README hashes are recorded as
citations in [SOURCES.json](SOURCES.json).

## Limitations

N(4) remains open within 9 <= N(4) <= 18. There is no ten-source witness and
no exclusion of ten through eighteen sources. The translated-cube proof
alone leaves too many possibilities at eighteen sources. Moreover, the
72-event finite witness in [CUBE-SHARPNESS.json](CUBE-SHARPNESS.json) has
72 distinct parity prefixes and 22 prefixes in the unshifted binary cube.
Thus H(18,0)=22 is attained, so that uniform intersection cap cannot be
lowered at this corner. This is not a floor-attainment witness. The depth-two
census concerns only that block depth and characteristic four.

The interface has immutable sources, unsigned calls and every nonzero binary
mask output. No physical caller, primitive tariff, admission, dispatch or
precision obligation is instantiated. Independent human and formal
proof-kernel review are unclaimed.

The Python checkers allocate bounded integers and temporary collections.
In depth_two.py, walk_tables and inspect_state use preallocated tables and
an explicit 21-frame stack for k <= 5, with no recursion. CPython allocation
is a managed-runtime deviation from fixed-allocation operation. Fixed
dimensions, explicit iteration bounds, capacity checks and normal/optimized
replays bound and check the live state. A strict allocation-free consumer
would require the native fixed-array implementation instead of widening
this Python contract. No unbounded input or concurrent mutation is accepted.

## Open next questions

Structured first steps and blockers are in [TASK.json](TASK.json).

1. Find a ten-source floor walk in the eight-inventory normal form, or prove
   ten sources fail. The four maximizing depth-two blocks give a complete
   small seed catalog for coupled searches; concatenation alone cannot work.
2. Improve the translated-cube count at eighteen sources, possibly by
   controlling several cube intersections together rather than their maximum.
3. Identify a concrete characteristic-four caller and price its complete
   interface before using a larger abstract batch in a recursive supplier.

## Credit

This package was produced by Nick Petalas. The interface and floor are
#4231's. The nine-source lower bound and deletion lemma are #4248's;
the deletion argument extends #4232's characteristic-three version.
The parity-boundary counting approach builds on #4255. The connector
interface and prefix criterion originate in Ross Richardson's #943/#934
lineage. Independent human and formal proof-kernel review are unclaimed.
Apache-2.0.
