# Record candidate: T16 owner map from ejection cycles and CP-SAT LNS on the selected supplier (κ=0.001672702955495933)

## Contribution

This PR adds `research/complex-t16-two-stage-cycles`, a registered research
package. It is a conditional T16 owner map on the **unchanged selected PR1094
supplier**, with no new mechanism.

- **κ = 0.001672702955495933** (conservative 0.001672702952644).
- That is **+2.5563e-5 relative** (+4.276e-8) over the selected record
  (0.001672660197076918), +2.214e-8 over open PR1407 (0.001672680818492982)
  and +1.845e-8 over this PR's first version (0.001672684510394236).
- Idle remainders go from `{1:2276, 3:377, 7:7, 48:4866}` (selected) to
  `{1:2280, 2:1, 3:363, 7:3, 16:4, 48:4866}`. Residuals totalling 70 are
  regrouped into fewer, larger ones; rank mass 1,041,408 and deficit 5,120 are
  unchanged.
- **Standalone diff against the selected map:** `DIFF-vs-selected.json`
  changes 70 of 69,120 rows: 55 helpers move to another bin and 15 rows
  only change their slice offset. Widths, call order, windows and the local and
  bit suppliers are unchanged. No open PR is needed.
- The unchanged PR1087 strict replay passes all 11 stages, with controls
  69/12/6/15. `actual_73column_sigmas` is 10000: the strict audit recomputes
  this chart count for the realized map and `assemble.py` pins it.
- The seed67 owner auditor passes R1–R7, X1, X2 and its 11 controls. Pricing
  with the pinned exact engines and the PR1069 sweep agree with the replay.

Packing ceiling: with the PR1240 local-word ceiling endpoint
a_hi = 0.001690054109089, this map realises 0.294% of the complex endpoint gap
(first version: 0.167%; PR1407: 0.142%).

It claims no packing optimum and no unconditional theorem. All PR1094
inherited assumptions remain.

## How the map was found

1. **κ search** from this PR's first version (PR1407's map plus two-stage
   ejection cycles): depth-8 ejection cycles (`search/chain2.py`) alternating
   with CP-SAT large-neighbourhood re-assignments (`search/lns.py`,
   `search/loop3.sh`). It is a finite search and was **stopped while still
   improving**. Its raw output differs from the selected map in 30,039 rows,
   mostly from random plateau moves.
2. **Min-diff re-assignment** at the same idle profile, hence the same κ:
   HiGHS MIPs and two LNS passes (`search/mindiff_mip.py`,
   `search/mindiff_lns.py`, `search/mindiff_lns2.py`, `search/realize.py`) that
   keep as many of the selected map's placements as they can:
   2,062 → 182 → 94 → 55 relocations. This is not proven minimal.

`SEARCH.json` records the checkpoints (three were strict-replayed during the
session) and the exact min-diff commands.

## Change from the first version of this PR

The first version (κ 0.001672684510394236) was a 23-row successor of open
PR1407 and checked that ancestry by content (`DEPENDENCY-PR1407.json`). After
the min-diff re-assignment, PR1407's map is no longer an ancestor (of the 23
placements PR1407 changes, the new map shares 2), so that check and
`DIFF-vs-pr1407.json` are removed. The package now depends only on merged
inputs. PR1407 (pai-scaffolde) remains the starting point of the search and
the source of the whole-helper semantics and all-input argument; PR2077
(lydakis) remains the origin of the vacancy-chain idea. Their four literal
moves still do not compose (`search/compose.py`).

## Provenance

- **Chooser:** this work was not drawn by `scripts/choose_research_task.py`. It
  was self-selected as the review-and-compose task: a review of PR1407 and
  PR2077, a test of whether they compose, and then a search on the stronger
  map. `TASK.json` records it under the closest card, `selected-packing`, with
  `scope_status: changed` and this reason.
- **Base:** `0fdd7d82`. The 287 pinned inputs are listed in `INPUTS.json` and
  `SOURCES.json`.
- **Credit:**
  - pai-scaffolde (PR1407): starting map of the search, whole-helper semantics
    and all-input argument.
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
