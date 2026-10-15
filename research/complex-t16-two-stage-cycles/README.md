# T16 owner map from ejection cycles and CP-SAT LNS on the selected supplier

On the unchanged selected PR1094 supplier, this owner map admits conditional
**κ = 0.001672702955495933** (conservative surcharge 0.001672702952644).
That is **+2.5563e-5 relative** (+4.276e-8) over the selected record
0.001672660197076918, +2.214e-8 over open PR1407 (0.001672680818492982), and
+1.845e-8 over this PR's first version (0.001672684510394236). The local
gauge44 word, helper widths, 144-call order, windows, physical stock, native
supplier and PR589 bit supplier are unchanged. The unchanged PR1087 strict
replay passes.

**Scope.** This is a conditional T16 packing on the same supplier, with no new
mechanism. The map is stated and verified **only against the merged selected
PR1094 map**: `DIFF-vs-selected.json` changes 70 of its 69,120 rows
(55 helpers move to another bin; 15 more rows only change their slice
offset). It depends on no open PR. It claims no packing optimum and no
unconditional multiplication theorem.

## What changed since the first version of this PR

The first version applied two-stage ejection cycles to PR1407's map
(κ 0.001672684510394236) and checked that undoing them reproduced PR1407's
owner table. This version:

1. ran a longer finite search from that map (depth-8 ejection cycles
   alternating with CP-SAT large-neighbourhood re-assignments), which raised κ
   to 0.001672702955495933. Its raw output differed from the selected map in
   30,039 rows (17,173 relocations), mostly because of random plateau moves;
2. replaced that output by an equivalent map at the **same idle profile, hence
   the same κ**, that is as close as the min-diff search could make it to the
   selected map (55 relocations, 70 changed rows);
3. dropped the PR1407 ancestry check (`DEPENDENCY-PR1407.json`,
   `DIFF-vs-pr1407.json`). After the re-assignment, PR1407's map is no longer
   an ancestor: of the 23 (bin, call, width) placements PR1407 changes, the
   new map shares 2. PR1407 and PR2077 remain lineage and credit (see Credit).

## Construction

A bin is `(owner replica, idle child, port)`. Its capacity and borrowing window
come from the selected PR1094 plan. A placement puts one whole helper role of
one call into a bin. It must fit the free capacity, the call must lie strictly
inside the bin's window, and the bin's physical family must be unused by every
other helper in that call. No helper is split and no call is reordered.
Helpers of the same call and width are interchangeable under these rules.

**κ search** (`search/`, `SEARCH.json`). Starting from the first version's map:

* `chain2.py` searches one- and two-stage ejection cycles (a cycle lifts a
  helper out of a bin, places it where it ejects another one, and so on until
  the last one returns), up to depth 8, ranked by the surrogate `Σ f ln f` over
  free capacities and accepted only if the exact κ rises.
* `lns.py` frees a neighbourhood (a set of calls or physical families) and
  re-assigns all its helpers with CP-SAT, maximising the same surrogate. On a
  plateau (`DIV=1`) it keeps the surrogate and randomly maximises relocations
  to escape.
* `loop3.sh` alternates the two. Strict-replayed checkpoints:
  κ 0.001672686708686457, 0.001672699106899519 and 0.001672702955495933.

The search was **stopped while still improving** (its last 45-minute run
still added +3.8e-9). It is a finite heuristic, not an optimum.

**Min-diff re-assignment.** Given the selected map A and the search output F,
find a legal map with F's idle profile that keeps as many placements of A as
possible. A placement is `(bin, call, width)`, since helpers of one call and
width are interchangeable:

1. `mindiff_mip.py fill`: HiGHS MIP with every bin's fill fixed to F's and
   candidates = placements of A or F. Proven optimal: 2,062 relocations.
2. `mindiff_lns.py`: LNS where each bin's fill may be A's or F's, with the
   number of bins per idle value preserved inside each neighbourhood: 182.
3. `mindiff_mip.py two`: the same two-fill model solved globally, warm-started
   from step 2: 94 (time limit; that model's dual bound is 92).
4. `mindiff_lns2.py`: LNS on the remaining region with any fill and every
   legal placement of the rows involved, plus sampled extra bins: 55. A second
   round found nothing in 7 iterations.
5. `realize.py` keeps A's helper label wherever A's placement is kept and
   orders each bin's slices to keep as many of A's offsets as possible:
   55 relocations and 15 offset-only changes.

This is a heuristic too: no lower bound below the two-fill model's 92 is
known, and a smaller diff with the same profile may exist.

## Exact profile change

| | idle remainder profile | κ |
|---|---|---|
| selected PR1094 | `{1:2276, 3:377, 7:7, 48:4866}` | 0.001672660197076918 |
| PR1407 | `{1:2277, 3:377, 16:3, 48:4866}` | 0.001672680818492982 |
| first version of this PR | `{1:2278, 3:374, 8:1, 16:3, 48:4866}` | 0.001672684510394236 |
| this package | `{1:2280, 2:1, 3:363, 7:3, 16:4, 48:4866}` | 0.001672702955495933 |

Compared with the selected map, the idle profile changes by
`{1:+4, 2:+1, 3:-14, 7:-4, 16:+4}`: residuals totalling 70 are regrouped into
fewer, larger ones, and rank mass is conserved. The full paid profile is
`{1:349608, 2:60193, 3:62571, 4:20448, 5:11808, 7:3, 8:1152, 16:4, 48:4866}`.
Rank mass is still 1,041,408 and the deficit is still 5,120. Cross-replica
helper roles go from 57,480 to 57,481. `PROOF.md` gives the majorization
argument.

`SPEC.expected.actual_73column_sigmas` is **10000** (selected: 10002; the raw
search output had 10466). This
value is not a tuning knob. The strict audit counts the distinct orthogonal
73-column charts that the realized owner chronology uses. `assemble.py` pins
that count against SPEC exactly, and an `understated_actual_chart_types`
mutation control guards it. It depends on the map, so the strict verifier
recomputes it on every replay.

Packing ceiling: with the PR1240 local-word ceiling endpoint
a_hi = 0.001690054109089, this map realises **0.294%** of the complex endpoint
gap (first version of this PR: 0.167%; PR1407: 0.142%).

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
   map. It checks that only owner fields change, counts the changed and
   relocated rows, recomputes the idle histogram with its own packing checker
   (expected `{1:2280, 2:1, 3:363, 7:3, 16:4, 48:4866}`), and regenerates
   `PLAN.json` and `SPEC.json` byte for byte. `OWNERS.json.gz` is compared on
   its decoded payload.
3. It restores the PR1087 archive (`upstream1087.tar.gz`), checks all 179
   archived files, overlays only the three data files, and extracts the selected
   R480 gauge44 provider from `selected-replay.tar.gz` (`LOCAL-PINS.json`). It
   then runs the unchanged `verify_t16.py`, which covers all 11 stages and
   69/12/6/15 rejecting controls, and requires `actual_73_axis_charts` = 10000.
4. It runs `check.py`, an independent check adapted from the session's
   `checkmap.py`. That check uses the seed67 owner auditor (R1–R7, X1, X2 and
   11 controls) on both the selected and the candidate map. It also prices with
   the pinned exact engines and runs the PR1069 sweep on the strict replay's
   lowers. The conservative κ is compared as a decimal, because the native
   assembler drops trailing zeros.

The full replay takes about 60 s and stays under 1 GB of RAM. `evidence/`
holds the receipts of the local run.

The search needs third-party packages and proves nothing; `SEARCH.json` records
the commands and checkpoints. The min-diff step, from the search output F
(content SHA256 in `SEARCH.json`), ran as follows. HiGHS time limits are wall
clock, so a rerun can land on a different map of similar size:

```sh
cd <repo root>; S=research/complex-t16-two-stage-cycles/search
uv run -q --no-project --python 3.12 --with scipy --with highspy python -I $S/mindiff_mip.py $S F.OWNERS.json.gz /tmp/fill.json fill 900 -
uv run -q --no-project --python 3.12 --with scipy --with highspy python -I $S/mindiff_lns.py $S F.OWNERS.json.gz /tmp/fill.json /tmp/lns.json 60 1 300 60
uv run -q --no-project --python 3.12 --with scipy --with highspy python -I $S/mindiff_mip.py $S F.OWNERS.json.gz /tmp/two.json two 2400 /tmp/lns.json
uv run -q --no-project --python 3.12 --with scipy --with highspy python -I $S/mindiff_lns2.py $S /tmp/two.json /tmp/any.json 15 11 80 90
python3.12 -I $S/realize.py $S /tmp/any.json /tmp/OWNERS.json.gz
python3.12 -I $S/buildcand.py $S /tmp/OWNERS.json.gz /tmp/pkg 10000
```

## Assumptions retained

The all-size compiler, common-label/mutable-source realization, whole-call
hosting, precision/tape, exact recovery, analytic transfer and PR589 bit H1–H5
assumptions of the selected PR1094 record remain. The native local receipts are
reused with source binding; the ancestry is not rebuilt cold. Hosted CI and
maintainer acceptance are separate.

## Credit

- **pai-scaffolde, PR1407**: the search started from its owner map (through
  the first version of this package), and this package reuses its whole-helper
  neutral-path semantics and all-input argument. The final map is no longer a
  row-for-row descendant of PR1407's map, but the line of work is its.
- **George Lydakis (lydakis), PR2077** contributed the vacancy-chain idea of
  propagating free capacity through occupied bins, the ancestor of the
  ejection cycles. Its four literal moves do not compose with PR1407 (all 15
  subsets are illegal on PR1407's map; `search/compose.py`).
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

- **Continue the κ search.** It stopped while still improving. The first step
  is to rerun `search/loop3.sh` from `data/OWNERS.json.gz` under a memory cap,
  strict-replay each new best, and rerun the min-diff step on the result.
- **A certified packing bound.** An LP or Lagrangian relaxation over bins with
  the family-per-call constraint would show how much κ owner packing can still
  give on this supplier.
- **A smaller diff.** The min-diff map is not proven minimal for its profile.
  Widening the candidate placements, or a longer two-fill MIP, may shrink it.
