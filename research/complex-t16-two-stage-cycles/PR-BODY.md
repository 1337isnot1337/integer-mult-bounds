# Record candidate: T16 owner map from a global class-level repack on the selected supplier (κ=0.001673054161426948)

## Contribution

This PR adds `research/complex-t16-two-stage-cycles`, a registered research
package. It is a conditional T16 owner map on the **unchanged selected PR1094
supplier**, with no new mechanism.

- **κ = 0.001673054161426948** (conservative 0.001673054158574889).
- That is **+2.3553e-4 relative** (+3.940e-7) over the selected record
  (0.001672660197076918) and +3.733e-7 over open PR1407
  (0.001672680818492982). Over this PR's earlier versions it is +3.697e-7
  (first version, 0.001672684510394236) and +2.0996e-4 relative, +3.512e-7
  (second version, 0.001672702955495933).
- Idle remainders go from `{1:2276, 3:377, 7:7, 48:4866}` (selected) to
  `{1:2346, 2:3, 3:154, 5:9, 7:36, 8:2, 16:7, 28:1, 39:1, 40:1, 41:2, 44:41, 48:4829}`.
  Rank mass 1,041,408 and deficit 5,120 are unchanged. The new residual vector
  does not majorize the old one, so the decrease of the complex moment rests on
  the pinned exact engines and the strict replay, not on a concavity argument.
- **Standalone diff against the selected map:** `DIFF-vs-selected.json`
  changes 1,661 of 69,120 rows: 1,435 helpers move to another bin and 226 rows
  only change their slice offset. Widths, call order, windows and the local and
  bit suppliers are unchanged. No open PR is needed.
- The unchanged PR1087 strict replay passes all 11 stages, with controls
  69/12/6/15. `actual_73column_sigmas` is 10055: the strict audit recomputes
  this chart count for the realized map and `assemble.py` pins it.
- The seed67 owner auditor passes R1–R7, X1, X2 and its 11 controls. Pricing
  with the pinned exact engines and the PR1069 sweep agree with the replay.

Packing ceiling: with the PR1240 local-word ceiling endpoint
a_hi = 0.001690054109089, this map realises 2.709% of the complex endpoint gap
(second version: 0.294%; first version: 0.167%; PR1407: 0.142%).

It claims no packing optimum and no unconditional theorem. All PR1094
inherited assumptions remain.

## How the map was found

The second version's loop (ejection cycles plus CP-SAT LNS) had slowed to
steps of about 1e-9. Two observations changed the approach: κ is close to
linear in the surrogate `Σ f ln f` over idle fragments, and inside a physical
family the bins' windows never overlap, so the family rule reduces to at most
one helper per bin per call. Bins with the same capacity and the same allowed
calls are then interchangeable, and the problem becomes a class-level
pattern/flow model.

1. **Global repack.** Stage 1 (`search/glob.py`): CP-SAT over pattern counts
   and flows per (capacity, window) class, with per-call Hall constraints and
   Gale–Ryser-style distinct-call constraints (best: 906,706 surrogate units
   against 905,605 at the start). Stage 2 (`search/glob5.py`): per-width
   max-flow realisation on concrete bins; 80 helpers that stage 2 could not
   place were inserted greedily.
2. **Cycle/LNS loop** (`search/loopx.sh`): depth-8 ejection cycles
   (`search/chain2.py`) alternated with CP-SAT LNS plateau steps
   (`search/lns.py`, now with `NW` and an `f3` mode). It was **stopped while
   still improving**. Strict-replayed checkpoints: 0.001672894024167899 and
   0.001673054161426948.
3. **Min-diff re-assignment** at the same idle profile, hence the same κ. The
   raw map relocates 61,985 rows against the selected map. The same class
   structure gives a two-stage min-diff: a class-level MIP that keeps as much
   of the selected map's class flows as the target profile allows, a per-class
   realisation that keeps as many of its placements as possible, then an LNS
   polish (`search/mindiff_cls1.py`, `search/mindiff_cls2.py`,
   `search/mindiff_lns.py`, `search/realize.py`): 61,985 → 1,440 → 1,435
   relocations, i.e. 1,661 changed rows of which 226 are offset-only. Stage 1
   is a relaxation; five classes it changed could not be realised and were
   kept as in the selected map. The class-level relaxation, solved by HiGHS,
   implies at least 853 relocations for any legal map with this profile (a
   solver-reported bound, not a checked certificate); the shipped map is not
   proven minimal.

A class-level relaxation (`search/winbound.py`) gave, in the session, an
optimistic surrogate ceiling of about 908.1k units (roughly κ ≈ 0.0016741). It
is **not** a certified bound: the κ–surrogate relation is approximate, and a
900 s single-worker rerun here did not close the relaxation's own bound.

`SEARCH.json` records the checkpoints and the commands.

## Earlier versions of this PR

- **First version**, κ 0.001672684510394236: two-stage ejection cycles on
  PR1407's map, a 23-row successor of PR1407, with the ancestry checked by
  content.
- **Second version**, κ 0.001672702955495933: a longer cycle/LNS search, then
  a min-diff re-assignment to 70 changed rows (55 relocations) against the
  selected map; the PR1407 ancestry check was dropped.

This third version replaces the map, the diff and the search record. PR1407
(pai-scaffolde) remains the starting point of the search line and the source of
the whole-helper semantics and all-input argument; PR2077 (lydakis) remains the
origin of the vacancy-chain idea. Their four literal moves still do not compose
(`search/compose.py`).

## Provenance

- **Chooser:** this work was not drawn by `scripts/choose_research_task.py`. It
  was self-selected as the review-and-compose task: a review of PR1407 and
  PR2077, a test of whether they compose, and then a search on the stronger
  map. `TASK.json` records it under the closest card, `selected-packing`, with
  `scope_status: changed` and this reason.
- **Base:** `0fdd7d82`. The 287 pinned inputs are listed in `INPUTS.json` and
  `SOURCES.json`.
- **Credit:**
  - pai-scaffolde (PR1407): starting map of the search line, whole-helper
    semantics and all-input argument.
  - George Lydakis (lydakis, PR2077): the vacancy-chain idea.
  - Rohan Arun and Jeremy Kothe: the PR1050–PR1094 line and the selected
    supplier and map.
  - Josie Elliston: the seed67 auditor, PR1091.
  - Sagar Thakrar: the independent pricing sweep, PR1069.
- **Prepared by** Philippe Van Velzen with substantial Claude Code (Claude
  Opus 5.5) assistance. No independent human review is claimed.

## Reproduce

```sh
python3 scripts/research_package.py --package research/complex-t16-two-stage-cycles --check-only
python3.12 scripts/research_package.py --package research/complex-t16-two-stage-cycles
```

The full replay takes about 60 s and uses only the standard library. The
search is optional and needs numpy, ortools, scipy and highspy; the README and
`SEARCH.json` give the commands.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
