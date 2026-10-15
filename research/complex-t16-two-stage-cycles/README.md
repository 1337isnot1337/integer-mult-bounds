# T16 owner map from a global class-level repack on the selected supplier

On the unchanged selected PR1094 supplier, this owner map admits conditional
**κ = 0.001673054161426948** (conservative surcharge 0.001673054158574889).
That is **+2.3553e-4 relative** (+3.940e-7) over the selected record
0.001672660197076918 and +3.733e-7 over open PR1407 (0.001672680818492982).
Against this PR's earlier versions it is +3.697e-7 over the first
(0.001672684510394236) and +3.512e-7 (+2.0996e-4 relative) over the second
(0.001672702955495933). The local gauge44 word, helper widths, 144-call order,
windows, physical stock, native supplier and PR589 bit supplier are unchanged.
The unchanged PR1087 strict replay passes.

**Scope.** This is a conditional T16 packing on the same supplier, with no new
mechanism. The map is stated and verified **only against the merged selected
PR1094 map**: `DIFF-vs-selected.json` changes 1,661 of its 69,120 rows
(1,435 helpers move to another bin; 226 more rows only change their slice
offset). It depends on no open PR. It claims no packing optimum and no
unconditional multiplication theorem.

## Versions of this PR

1. κ 0.001672684510394236: two-stage ejection cycles on PR1407's map (a
   23-row successor of PR1407).
2. κ 0.001672702955495933: depth-8 ejection cycles alternated with CP-SAT
   large-neighbourhood re-assignments, then a min-diff re-assignment to 70
   changed rows against the selected map.
3. This version, κ 0.001673054161426948: a global class-level repack followed
   by the same cycle/LNS loop, then a new min-diff re-assignment. The idle
   profile is now far from the selected one, so the diff is much larger than
   version 2's 70 rows.

## Construction

A bin is `(owner replica, idle child, port)`. Its capacity and borrowing window
come from the selected PR1094 plan. A placement puts one whole helper role of
one call into a bin. It must fit the free capacity, the call must lie strictly
inside the bin's window, and the bin's physical family must be unused by every
other helper in that call. No helper is split and no call is reordered.
Helpers of the same call and width are interchangeable under these rules.

### Why a global repack

Version 2's loop (ejection cycles plus CP-SAT LNS) had slowed to steps of about
1e-9 in κ. Three observations led to a global model instead:

* κ is, to good accuracy, a linear function of the surrogate `Σ f ln f` over
  the idle fragments (free capacities `f`), so the surrogate is a usable
  objective for a global model; only the exact engines decide acceptance.
* Inside one physical family the bins' windows never overlap. So the family
  rule (R4) reduces to "at most one helper per bin per call", and two bins with
  the same capacity and the same set of allowed calls (a *class*: 144 classes
  of 224 bins each) are interchangeable.
* The problem therefore becomes a class-level pattern/flow model: how many bins
  of each class get each width pattern, and how many helpers of each
  (call, width) each class hosts.

### κ search (`search/`, `SEARCH.json`)

Starting from version 2's raw search output (content `a7e8f0ca…`):

1. **Stage 1** (`glob.py`): CP-SAT over pattern counts and flows per class,
   with per-(class, call) Hall constraints (a call can use at most as many bins
   of a class as there are bins whose pattern holds the widths it needs) and
   Gale–Ryser-style constraints for several helpers of one width in a bin
   (they need distinct calls), maximising the surrogate. Best stage 1:
   906,706 surrogate units (the start map had 905,605).
2. **Stage 2** (`glob5.py`): per class and width, a max-flow from calls to
   bins realises the stage-1 solution with distinct calls per bin. Stage 1 is a
   relaxation, so 80 helpers stayed unplaced; they were inserted greedily where
   they cost the least surrogate. The realised map had κ 0.001672432283943020,
   lower than the start but with a very different profile.
3. **Loop** (`loopx.sh`): chain2 ejection cycles alternated with CP-SAT LNS
   plateau steps (`lns.py`, now with a worker-count setting `NW` and an `f3`
   neighbourhood mode), keeping the best map by exact κ. Strict-replayed
   checkpoints: κ 0.001672894024167899 and 0.001673054161426948.

The search was **stopped while still improving**. It is a finite heuristic, not
an optimum.

**Heuristic ceiling (not a proof).** `winbound.py` groups bins by class and
drops the per-bin constraints. In the session, this relaxation gave an
optimistic ceiling of about 908.1k surrogate units, which by the near-linear
κ–surrogate relation corresponds to roughly κ ≈ 0.0016741. This number is
**not certified**: the κ–surrogate relation is only approximate, and a rerun
of the shipped script for this package (one CP-SAT worker, 900 s) did not
close its bound (it stopped at 983k). It is reported only as a rough sense of
how much room the surrogate may leave; `aggbound.py` is a coarser variant that
ignores calls and windows entirely.

### Min-diff re-assignment

Given the selected map A and the search output F, find a legal map with F's
idle profile (hence F's κ) that keeps as many placements of A as possible. A
placement is `(bin, call, width)`, since helpers of one call and width are
interchangeable. Version 2's tools (`mindiff_mip.py`, `mindiff_lns.py`) start
from F's per-bin fills; here F shares only 8,426 of A's 69,120 placements
(61,985 rows relocated), and those models could not get close (the fill-fixed
MIP's root bound alone allowed at most about 44.7k kept placements). The class
structure gives a better route:

1. `mindiff_cls1.py` (HiGHS): a class-level MIP over the same pattern counts
   and flows as the repack, with the idle profile fixed to F's, maximising the
   flow of A's (class, call, width) placements that stays in place. HiGHS
   solved it to optimality: 68,236 placements' worth of flow (884
   relocations) at the tie-broken optimum. Since every legal map with F's
   profile is feasible for this relaxation, the reported dual bound implies at
   least 853 relocations for any such map once the tie-break weight is
   discounted. That is a solver-reported bound, not an independently checked
   certificate.
2. `mindiff_cls2.py` (CP-SAT pass, then HiGHS pass, per changed class):
   realise each class's stage-1 solution on its 224 bins, keeping as many of
   A's placements as possible; unchanged classes keep A. Stage 1 is a
   relaxation, so a few classes could not be realised (4, 9, 88 and 133 in the
   first round; 94, proven infeasible, in the second). Those classes were fixed
   to A (`FIX`) and stage 1 re-solved; in the last round all other classes kept
   the previous stage-1 values except the changed ones (`KEEP`/`FREE`), and 34
   of 47 class results were reused (`mindiff_reuse.py`). Result: 1,440
   relocations.
3. `mindiff_lns.py` (version 2's LNS, with the stage-2 map as F): 1,435
   relocations. Three iterations of `mindiff_lns2.py` found nothing more and
   were stopped.
4. `realize.py` keeps A's helper labels and offsets where possible:
   **1,435 relocations and 226 offset-only changes (1,661 changed rows)**,
   against 61,985 relocations in the raw search output.

This is a heuristic too. The relocation count is not proven minimal.

## Exact profile change

| | idle remainder profile | κ |
|---|---|---|
| selected PR1094 | `{1:2276, 3:377, 7:7, 48:4866}` | 0.001672660197076918 |
| PR1407 | `{1:2277, 3:377, 16:3, 48:4866}` | 0.001672680818492982 |
| version 1 of this PR | `{1:2278, 3:374, 8:1, 16:3, 48:4866}` | 0.001672684510394236 |
| version 2 of this PR | `{1:2280, 2:1, 3:363, 7:3, 16:4, 48:4866}` | 0.001672702955495933 |
| this package | `{1:2346, 2:3, 3:154, 5:9, 7:36, 8:2, 16:7, 28:1, 39:1, 40:1, 41:2, 44:41, 48:4829}` | 0.001673054161426948 |

Compared with the selected map, the idle profile changes by
`{1:+70, 2:+3, 3:-223, 5:+9, 7:+29, 8:+2, 16:+7, 28:+1, 39:+1, 40:+1, 41:+2, 44:+41, 48:-37}`.
37 bins that were completely idle now host small helpers, and many residuals 3
elsewhere merge into larger ones or close. The full paid profile is
`{1:349674, 2:60195, 3:62362, 4:20448, 5:11817, 7:36, 8:1154, 16:7, 28:1, 39:1, 40:1, 41:2, 44:41, 48:4829}`.
Rank mass is still 1,041,408 and the deficit is still 5,120. Cross-replica
helper roles go from 57,480 to 57,456. Unlike versions 1 and 2, the new residual
vector does not majorize the old one, so the cost decrease rests on the exact
engines, not on a concavity argument (`PROOF.md`).

`SPEC.expected.actual_73column_sigmas` is **10055** (selected: 10002; the raw
search output had 10614). This value is not a tuning knob. The strict audit
counts the distinct orthogonal 73-column charts that the realized owner
chronology uses. `assemble.py` pins that count against SPEC exactly, and an
`understated_actual_chart_types` mutation control guards it. It depends on the
map, so the strict verifier recomputes it on every replay.

Packing ceiling: with the PR1240 local-word ceiling endpoint
a_hi = 0.001690054109089, this map realises **2.709%** of the complex endpoint
gap (version 2: 0.294%; version 1: 0.167%; PR1407: 0.142%).

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
   relocated rows, recomputes the idle histogram with its own packing checker,
   and regenerates `PLAN.json` and `SPEC.json` byte for byte.
   `OWNERS.json.gz` is compared on its decoded payload.
3. It restores the PR1087 archive (`upstream1087.tar.gz`), checks all 179
   archived files, overlays only the three data files, and extracts the selected
   R480 gauge44 provider from `selected-replay.tar.gz` (`LOCAL-PINS.json`). It
   then runs the unchanged `verify_t16.py`, which covers all 11 stages and
   69/12/6/15 rejecting controls, and requires `actual_73_axis_charts` = 10055.
4. It runs `check.py`, an independent check adapted from the session's
   `checkmap.py`. That check uses the seed67 owner auditor (R1–R7, X1, X2 and
   11 controls) on both the selected and the candidate map. It also prices with
   the pinned exact engines and runs the PR1069 sweep on the strict replay's
   lowers. The conservative κ is compared as a decimal, because the native
   assembler drops trailing zeros.

The full replay takes about 60 s and stays under 1 GB of RAM. `evidence/`
holds the receipts of the local run.

The search needs third-party packages and proves nothing; `SEARCH.json` records
the commands and checkpoints. Solver time limits are wall clock and some seeds
came from bash `$RANDOM`, so a rerun can land on a different map of similar
quality. The min-diff step, from the search output F (content SHA256 in
`SEARCH.json`), ran as follows:

```sh
S=research/complex-t16-two-stage-cycles/search; W=<work dir>; F=<search output F>
PY="uv run -q --no-project --python 3.12"; HI="--with scipy --with highspy"
stage2() {   # stage-1 json, cache dir; the two halves ran in parallel
  for h in 0/2 1/2; do
    $PY --with ortools python -I $S/mindiff_cls2.py $S $1 $2 60 150 $h cp
    $PY $HI python -I $S/mindiff_cls2.py $S $1 $2 60 150 $h hi
  done; }
$PY $HI python -I $S/mindiff_cls1.py $S $F $W/c1.json 1500 $F           # optimal, 981 s
stage2 $W/c1.json $W/cache                                              # classes 4, 9, 88, 133 unrealised
FIX='[4,9,88,133]' $PY $HI python -I $S/mindiff_cls1.py $S $F $W/c1b.json 330
stage2 $W/c1b.json $W/cache2                                            # class 94 infeasible
FIX='[4,9,88,133,94]' KEEP=$W/c1b.json FREE='<changed classes of c1b.json except 94>' \
  $PY $HI python -I $S/mindiff_cls1.py $S $F $W/c1c.json 300
python3 $S/mindiff_reuse.py $W/c1b.json $W/c1c.json $W/cache2 $W/cache3   # 34 of 47 reused
stage2 $W/c1c.json $W/cache3
$PY python -I $S/mindiff_cls2.py $S $W/c1c.json $W/cache3 $W/cls.json merge   # 1,440 relocations
$PY python -I $S/realize.py $S $W/cls.json $W/R1440.OWNERS.json.gz
$PY $HI python -I $S/mindiff_lns.py $S $W/R1440.OWNERS.json.gz $W/cls.json $W/lns.json 40 1 300 30   # 1,435
$PY python -I $S/realize.py $S $W/lns.json $W/OWNERS.json.gz
$PY python -I $S/buildcand.py $S $W/OWNERS.json.gz $W/pkg 10055
```

## Assumptions retained

The all-size compiler, common-label/mutable-source realization, whole-call
hosting, precision/tape, exact recovery, analytic transfer and PR589 bit H1–H5
assumptions of the selected PR1094 record remain. The native local receipts are
reused with source binding; the ancestry is not rebuilt cold. Hosted CI and
maintainer acceptance are separate.

## Credit

- **pai-scaffolde, PR1407**: the search line started from its owner map
  (through the first version of this package), and this package reuses its
  whole-helper neutral-path semantics and all-input argument. The final map is
  no longer a row-for-row descendant of PR1407's map, but the line of work is
  its.
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
  is to rerun `search/loopx.sh` from `data/OWNERS.json.gz` under a memory cap
  (or a new global repack from it), strict-replay each new best, and rerun the
  min-diff step on the result.
- **A certified packing bound.** The class-level relaxation (`winbound.py`)
  gives only an uncertified surrogate ceiling. A bound stated directly in the
  exact cost (or a proven κ–surrogate inequality) would show how much κ owner
  packing can still give on this supplier.
- **A smaller diff.** The min-diff map is not proven minimal for its profile.
  A stage 1 that also penalises pattern changes, or longer stage-2 and LNS
  runs, may shrink it.
