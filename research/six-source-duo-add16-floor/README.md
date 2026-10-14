# Six-source DUO: 14 calls are necessary at the 16-add budget

In the inherited six-source dirty-connector model, a universal restored source
word with at most **16 source adds needs at least 14 calls**. Aaron Wang/Navinor's
[PR2128](https://github.com/CrocSwap/integer-mult-bounds/pull/2128) supplies the
attaining `(14,16)` word. The new result is its lower bound, not that word.

The core exclusion is exact: a `(13,16)` word covers at most **63 of 64 binary
masks**, with an attaining near miss. A `(12,16)` word would split into a
forbidden `(13,16)` word. The two 14-add cells left open by PR2128 follow from
the inherited singleton census. At the all-63-output batch's minimum **142
adds**, the root-query minimum is **140**. Higher-add tradeoffs remain open.
No physical supplier, selected-frontier change or new kappa is claimed.

Literature checkpoint: Gavrylkiv, *Bases in Dihedral and Boolean Groups*,
[JIS 20 (2017), Table 3](https://cs.uwaterloo.ca/journals/JIS/VOL20/Gavrylkiv/gav4.pdf),
reports the stronger unrestricted value `r[(C2)^6]=14`. Thus the lower bound
itself is not a new group-theoretic result. The present restricted census is
a reproducible independent check with source-add and complete-batch accounting.
The wider prefix-set reduction and its independent enumeration are a separate
follow-up; do not read the open cells below as a claim against that published value.

## Model and inherited reduction

Keep [the five-source DUO model](../duo-toggle-connector/README.md), extending
Ross Richardson's [dirty connector](../universal-connector-boundary/README.md):
six read-only sources, arbitrary dirty targets, one arbitrary dirty connector z,
and complete F2-linear calls with fixed generic maps:

```
B_j:       z += B_j x_j
DUO_{j,l}: z += B_j x_j + B_l x_l       (j != l)
A_i:       y_i += A_i z.
```

No extra connectors, source mutations, combined readouts or reads inside a DUO
are allowed. Restore z and all scratch. A source word has k calls and W
source-map applications: a singleton contributes one to W, a DUO two.
The inherited price is one overhead o per call and one marginal p per add.

Write q_t for the source-parity prefix. Restoration forces q_k=0, with every
used source appearing a positive even number of times. Two output readouts
give q_s XOR q_t. Paired universality is exactly `D={q_s XOR q_t}=F2^6`.
Necessity follows from independent scalar dirty inputs; sufficiency holds for
arbitrary A_i and B_j without commutativity. This reduction is inherited.

## Exhaustive expansion reduction

A `(13,16)` word has ten singletons and three DUOs. Expand each DUO into its
two singleton applications in either order. The resulting 16-step restored
word has six positive even multiplicities, hence exactly one of

```
(6,2,2,2,2,2)       or       (4,4,2,2,2,2).
```

The original word sees every expanded prefix except the three internal DUO
midpoints. These are pairwise nonadjacent cyclic vertices, each merging two
distinct labels. Conversely every such hidden triple gives a legal `(13,16)`
word. Cyclic shifts translate all prefixes and preserve D. Repeated prefixes
are retained. Expanded internal boundaries are bookkeeping, never actual
DUO readout opportunities.

If the visible prefixes cover all masks, their expanded superset does too.
It therefore suffices to enumerate every full-cover 16-step singleton word
and every legal hidden triple. Renaming labels by first occurrence preserves
D. The exact canonical counts are

```
16! / (6! * (2!)^5 * 5!)                 =  7,567,560
16! / ((4!)^2 * (2!)^4 * 2! * 4!)       = 47,297,250
total                                   = 54,864,810.
```

Two code-disjoint enumerators agree on both counts and the **same complete
7,480 full-cover words**, byte for byte:

- `enumerate_rgs.cpp` uses restricted-growth words, a parity-feasibility bound
  and incremental pair differences. Its hidden-vertex screen requires each
  single deletion to preserve coverage, necessary for any successful triple.
- `enumerate_partitions.cpp` partitions positions into even blocks, placing
  the least unassigned position in the next block. Each partition gives one
  normalized word. A dual bitset-translation test computes coverage. It uses
  neither the first recursion nor the hidden-vertex screen.

All 7,480 full covers have multiplicity `(4,4,2,2,2,2)`. [FULL-COVERS.bin](FULL-COVERS.bin)
contains their sorted little-endian uint64 codes: sixteen 3-bit labels per
word, earliest in the least significant bits, 59,840 bytes total. SHA256:

```
251100fa9f200ddb24cefac8a6b8255cfa43d1f3bd7e4bc3f45120d4f3aa7262
```

The Python audit checks every word literally. Normalized rotation/reversal
partitions the table into **251 orbits**: one of size 8, 33 of size 16 and
217 of size 32. Every orbit is present in full and the orbits are disjoint.
Rotation, reversal and source permutation preserve the hidden-midpoint
conditions and retained coverage.

For each representative, the audit checks all 352 cyclic nonadjacent triples
whose merges have distinct labels: **86,900 legal cases** in total, without
the native individual-removability prune. None covers all 64 masks; the
maximum is 63. These are orbit/deletion pairs, not distinct charged programs.
Non-full-cover expansions already have retained coverage at most 63, so the
complete `(13,16)` domain has maximum 63.

[RESULT.json](RESULT.json) binds counts, orbits, the audited histogram and a
sharp near miss. Both enumerators also reproduce the predecessor's 945 /
10,395 / 945,945 singleton controls, with maxima 31/32, 49/64 and 59/64.
No timeout or heuristic search failure is used as an exclusion.

## Consequences and full abstract bill

Any k<=13 word with W=16 can split DUOs until k=13, exposing prefixes without
losing coverage. It is therefore excluded. For W<16, expansion would give
a universal singleton word of the same W, contradicting the inherited
singleton minimum 16. This settles `(12,16)` and explicitly excludes
`(12,14)` and `(13,14)` by the old 14-step bound.

PR2128's attaining word is

```
2,16,8,16,1,4,48,4,3,4,32,8,4,16.
```

It has 14 calls, 16 adds, restoration and full coverage. Its construction is
credited to the predecessor; the new result proves optimality for W<=16.

Each of 63 dirty outputs needs at least two readouts. A mask absent from D
needs at least four. Source restoration requires even W>=12. At W=12,
expansion misses at least 15 nonzero masks, so total adds are at least
`12+126+30=168`; at W=14 the floor is `14+126+10=150`; at W>=18 it is at least
`18+126=144`. A batch at the minimum **142 adds** must therefore have W=16
and exactly 126 paired readouts. It needs at least 14 source calls, hence
**140 queries**, attained by the predecessor at cost `140o+142p`. This is a
certified Pareto point, not the entire frontier or every weighted optimum.

The sharp near miss has steps

```
2,1,4,1,2,9,20,8,32,8,16,8,33
```

and misses only mask 12. Boundaries 0,1,2,6 XOR to 12; four readouts repair
it. That batch costs 141 queries and 144 adds, worse than the incumbent in
both quantities. Almost-full coverage is not an unpriced improvement.

## Reproduce and limits

Full replay needs **Python 3.12 and a C++17 compiler** (g++ or clang++).
Tested: Ubuntu 24.04, CPython 3.12.3, g++ 13.3.0. Set CXX to the compiler
executable if c++ is unavailable. Nothing is downloaded. The verifier fails
clearly without a compiler, builds in temporary storage, re-enumerates both
complete domains, compares their full tables and runs the literal audit:

```sh
python3 -I -O -B research/six-source-duo-add16-floor/verify.py
python3.12 scripts/research_package.py --package research/six-source-duo-add16-floor
```

The first full replay including compilation took 10.34 seconds and 120,352
KiB peak RSS on one CPU. The initial three-CPU search finished in about three
seconds; no limit fired. `--out NEW_PATH` creates a receipt exclusively.
Default replay compares RESULT and leaves the package unchanged.
The registered Ubuntu replay passed in 10.53 seconds (120,104 KiB peak RSS).
Ten additional isolated source-export checks passed: a complete Git-free
replay, optimized portable audit, missing/drifted input rejection, table and
count-preserving receipt corruption, a false theorem receipt, absent compiler,
and exclusive output creation/rejection. Default replay did not change inputs.

The portable command also runs on Windows without a compiler. It checks the
table, all orbits/deletions, the near miss and arbitrary-input positive replay.
**It does not itself re-establish the table's 54-million-word completeness**:

```sh
python3 -I -O -B research/six-source-duo-add16-floor/audit.py
```

The positive control checks all 70, 140 and 210 independent input columns at
dimensions 1, 2 and 3, with noncommuting maps at dimensions 2 and 3.
Dropped/moved readouts, a shrunk DUO and a dropped source call reject. The
full verifier rejects a deadline-truncated census. Both native implementations
and the Python audit have the same author/assistant; no independent human or
formal-kernel review is claimed. No physical supplier, tape/compiler
integration, frame/owner admission, precision proof, global moment or outer
exponent is supplied.

## Open next questions

Higher-add cells such as `(13,18)` or `(12,18)` remain open here. A witness
would trade source-map work for dispatches and needs a full batch bill.
A bounded search plus complete dirty replay is a feasible first step; a
timeout must remain a search limit. More consequential is whether a physical
supplier can admit DUO after frame, access, restoration and precision costs.
There is still no admitted selected-supplier instance. Structured scope,
source pins and handoffs are in [TASK.json](TASK.json).

## Credit

Ross Richardson / PR943 and PR934 supplies the interface and prefix reduction;
Navinor / PR1531 the DUO alphabet, five-source result and prices;
Aaron Wang/Navinor / PR2128 at `697369a971eed02c0fbcd75ebefec9f59945f08e`
the six-source `(14,16)` word and open cells; Douglas Colkitt / PR1185 and
Hanson Sun / PR1215 the singleton result. PR2134 and PR2146 concern one-TRIO
censuses in a different alphabet and are not claimed here.

Prepared for Tairitsu-Aya with substantial OpenAI Codex assistance in
mathematics, implementation, source reading, verification and prose.
Apache-2.0. Frozen predecessors and the selected result are unchanged.
This continues a released handoff, not a new operation family or fresh draw.
