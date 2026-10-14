# Two-stage ejection cycles on PR1407's T16 owner map

On the unchanged selected PR1094 supplier, this owner map admits conditional
**κ = 0.001672684510394236** (conservative surcharge
0.001672684507542306). That is **+3.69e-9** over open PR1407
(0.001672680818492982) and **+1.4536e-5 relative** (+2.43e-8) over the selected
record 0.001672660197076918. The local gauge44 word, helper widths, 144-call
order, windows, physical stock, native supplier and PR589 bit supplier are
unchanged. The unchanged PR1087 strict replay passes.

**Scope.** This is a conditional T16 packing on the same supplier, with no new
mechanism. It is a successor search on PR1407's map, so it **depends on open PR1407**
(head `d8640f5b`). If PR1407 is rejected for a reason that applies to its moves,
this candidate falls with it. It claims no global packing optimum and no
unconditional multiplication theorem.

## Construction

A bin is `(owner replica, idle child, port)`. Its capacity and borrowing window
come from the selected PR1094 plan. A move re-owns one whole helper role of one
call into another bin. It must fit the free capacity, the call must lie strictly
inside the bin's window, and the bin's physical family must be unused by every
other helper in that call. No helper is split and no call is reordered.

An *ejection cycle* starts at a bin X. It lifts one helper out of X, places it
into a bin that ejects another helper, and so on, until the last ejected helper
returns to X. The *two-stage* search first applies a cycle with zero surrogate
gain that raises the free capacity of X. It then looks for a second cycle through
the same X that turns that capacity into a strict gain. Free capacity `3` would
otherwise sit at the wrong place for any single improving cycle.

Starting from PR1407's map (idle `{1:2277, 3:377, 16:3, 48:4866}`):

* **Stage A** has two cycles through X = (12,4,0), each 7→7→7→4→4 in helper
  widths. The first moves the free 3 of bin (0,0,103) into X with zero gain. The
  second adds the free 3 of bin (0,0,104), so X has free 6. Idle becomes
  `{1:2277, 3:375, 6:1, …}`.
* **Stage B** has one 7-move cycle starting at X' = (6,0,36). It passes through
  X, where a width-9 helper replaces a width-4 one. The free capacities
  3 + 3 + 6 in bins (0,0,105), (0,0,58), (12,4,0) become 8 + 1 + 3 in bins
  (0,0,58), (12,4,0), (6,0,36).

There are 16 placements in total. Row 431 leaves its bin and returns, so 14 rows
are relocated net, and 23 serialized rows change after prefix compaction
(`DIFF-vs-pr1407.json`). Against the selected PR1094 map, PR1407's moves
together with these give 37 relocated rows and 70 changed rows
(`DIFF-vs-selected.json`). `SEARCH.json` lists every move.

## Exact profile change

| | idle remainder profile | κ |
|---|---|---|
| selected PR1094 | `{1:2276, 3:377, 7:7, 48:4866}` | 0.001672660197076918 |
| PR1407 | `{1:2277, 3:377, 16:3, 48:4866}` | 0.001672680818492982 |
| this package | `{1:2278, 3:374, 8:1, 16:3, 48:4866}` | 0.001672684510394236 |

Compared with PR1407, the paid profile changes by `{1:+1, 3:-3, 8:+1}`. In
effect, residuals 3+3+3 become 8+1, and rank mass is conserved. The full paid
profile is `{1:349606, 2:60192, 3:62582, 4:20448, 5:11808, 8:1153, 16:3, 48:4866}`.
Rank mass is still 1,041,408 and the deficit is still 5,120. Cross-replica
helper roles go from 57,481 to 57,482. `PROOF.md` gives the concavity argument.

`SPEC.expected.actual_73column_sigmas` is **10000** (selected: 10002). This
value is not a tuning knob. The strict audit counts the distinct orthogonal
73-column charts that the realized owner chronology uses. `assemble.py` pins
that count against SPEC exactly, and an `understated_actual_chart_types` mutation
control guards it. With the inherited 10002, assembly fails with
`SPEC MISMATCH expected.actual_73column_sigmas: expected 10002 got 10000`.
PR1407's map already has 10000, and these cycles leave the count unchanged.

## Reproduce

Run from a complete checkout at or after base `0fdd7d82`, with Python 3.12 and
the standard library only:

```sh
python3 scripts/research_package.py --package research/complex-t16-two-stage-cycles --check-only
python3.12 scripts/research_package.py --package research/complex-t16-two-stage-cycles
# or directly, keeping the work tree:
python3.12 -I -B research/complex-t16-two-stage-cycles/verify.py --work /abs/fresh/dir
```

`verify.py` follows the PR2077 package (`research/complex-t16-vacancy-chain`):

1. It checks the 287 pinned inputs (`INPUTS.json`) and the package inventory
   (`MANIFEST.json`).
2. `build.py` applies `DIFF-vs-selected.json` to the merged selected PR1094
   map. It checks that only owner fields change, recomputes the idle histogram
   with its own packing checker, and regenerates `PLAN.json` and `SPEC.json`
   byte for byte. `OWNERS.json.gz` is compared on its decoded payload.
3. It undoes the 23 rows of `DIFF-vs-pr1407.json` and requires the result to
   equal PR1407's pinned owner content hash (`DEPENDENCY-PR1407.json`).
4. It restores the PR1087 archive (`upstream1087.tar.gz`), checks all 179
   archived files, overlays only the three data files, and extracts the selected
   R480 gauge44 provider from `selected-replay.tar.gz` (`LOCAL-PINS.json`). It
   then runs the unchanged `verify_t16.py`, which covers all 11 stages and
   69/12/6/15 rejecting controls.
5. It runs `check.py`, an independent check adapted from the session's
   `checkmap.py`. That check uses the seed67 owner auditor (R1–R7, X1, X2 and
   11 controls) on both the selected and the candidate map. It also prices with
   the pinned exact engines and runs the PR1069 sweep on the strict replay's
   lowers.

The full replay takes about 50 s and stays under 1 GB of RAM. `evidence/` holds
the receipts of the local run.

To reproduce the search (it needs numpy and does not prove anything):

```sh
python3.12 research/complex-t16-two-stage-cycles/search/chain2.py \
  research/complex-t16-two-stage-cycles/search <PR1407 data/OWNERS.json.gz> /tmp/s1 6
python3.12 research/complex-t16-two-stage-cycles/search/chain2.py \
  research/complex-t16-two-stage-cycles/search /tmp/s1.OWNERS.json.gz /tmp/s2 6
python3.12 research/complex-t16-two-stage-cycles/search/buildcand.py \
  research/complex-t16-two-stage-cycles/search /tmp/s2.OWNERS.json.gz /tmp/pkg 10000
```

Each search stage takes about 15 s. The `/tmp/s2` map equals `data/OWNERS.json.gz`
in content. `search/compose.py` shows that PR2077's moves do not compose with
PR1407 (see Credit).

## Assumptions retained

The all-size compiler, common-label/mutable-source realization, whole-call
hosting, precision/tape, exact recovery, analytic transfer and PR589 bit H1–H5
assumptions of the selected PR1094 record remain. The native local receipts are
reused with source binding; the ancestry is not rebuilt cold. Hosted CI and
maintainer acceptance are separate.

## Credit

- **pai-scaffolde, PR1407** is the direct parent. This package starts from its
  owner map and reuses its whole-helper neutral-path semantics and
  all-input argument.
- **George Lydakis (lydakis), PR2077** contributed the vacancy-chain idea of
  propagating free capacity through occupied bins, which is the ancestor of
  these cycles. Its four moves do **not** compose with PR1407. PR1407 already
  moved row 34306 out of bin (11,8,103), and all 15 subsets of PR2077's moves
  are illegal on PR1407's map. The two gains are alternatives.
- **Rohan Arun and Jeremy Kothe**: the PR1050–PR1094 owner-packing line and the
  selected PR1094 supplier and map.
- **Josie Elliston**: the seed67 owner auditor (PR1091), used in `check.py` and
  in the search's legality oracle.
- **Sagar Thakrar**: the independent pricing sweep (PR1069), used in `check.py`.
- The strict verifier, exact engines and their predecessors keep their original
  authors and notices, which are unchanged.

Prepared by Philippe Van Velzen with substantial Claude Code (Claude Opus 5.5)
assistance. No independent human review is claimed. New material is Apache-2.0.

## Open next questions

The structured versions are in `TASK.json`:

- **Longer or three-stage cycles.** Bounded depth-6 passes of both searches on
  this map find no improving cycle (`SEARCH.json`). That is a search limit, not
  an optimum. The first step is to rerun `search/chain2.py` at depth 8 under a
  memory cap.
- **A certified packing bound.** An LP relaxation over bins with the
  family-per-call constraint would show how much κ owner packing can still give
  on this supplier.
