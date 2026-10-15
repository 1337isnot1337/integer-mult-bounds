# Record candidate: T16 owner map from a global class-level repack and evacuation LNS on the selected supplier (κ=0.001673341928508063)

## Contribution

This PR adds `research/complex-t16-two-stage-cycles`, a registered research
package. It is a conditional T16 owner map on the **unchanged selected PR1094
supplier**, with no new mechanism.

- **κ = 0.001673341928508063** (conservative 0.001673341925655596).
- That is **+4.0757e-4 relative** (+6.817e-7) over the selected record
  (0.001672660197076918) and +6.611e-7 over open PR1407
  (0.001672680818492982). Over this PR's earlier versions it is +6.574e-7
  (first version, 0.001672684510394236), +6.390e-7 (second version,
  0.001672702955495933) and +1.7200e-4 relative, +2.878e-7 (third version,
  0.001673054161426948).
- Idle remainders go from `{1:2276, 3:377, 7:7, 48:4866}` (selected) to
  `{1:2355, 2:2, 3:172, 7:3, 16:11, 48:4874}`. Rank mass 1,041,408 and deficit
  5,120 are unchanged. The new residual vector majorizes the selected one
  (equal totals 237,024; `check.py` asserts the partial-sum comparison), so by
  Karamata's inequality the complex moment strictly decreases for any strictly
  concave per-residual weight. The value of κ comes from the pinned exact
  engines and the strict replay.
- **Standalone diff against the selected map:** `DIFF-vs-selected.json`
  changes 1,638 of 69,120 rows: 1,415 helpers move to another bin and 223
  rows only change their slice offset. Widths, call order, windows and the
  local and bit suppliers are unchanged. No open PR is needed.
- The unchanged PR1087 strict replay passes all 11 stages, with controls
  69/12/6/15. `actual_73column_sigmas` is 10006: the strict audit recomputes
  this chart count for the realized map and `assemble.py` pins it.
- The seed67 owner auditor passes R1–R7, X1, X2 and its 11 controls. Pricing
  with the pinned exact engines and the PR1069 sweep agree with the replay.

Packing ceiling: with the PR1240 local-word ceiling endpoint
a_hi = 0.001690054109089, this map realises 4.688% of the complex endpoint gap
(third version: 2.709%; second: 0.294%; first: 0.167%; PR1407: 0.142%).

It claims no packing optimum and no unconditional theorem. All PR1094
inherited assumptions remain.

## How the map was found

Inside a physical family the bins' windows never overlap, so the family rule
reduces to at most one helper per bin per call, and bins with the same
capacity and the same allowed calls are interchangeable. κ is close to linear
in the surrogate `Σ f ln f` over idle fragments, which the search uses as its
objective; only the exact engines decide acceptance.

1. **Global repack** (third version). Stage 1 (`search/glob.py`): CP-SAT over
   pattern counts and flows per (capacity, window) class, with per-call Hall
   constraints and Gale–Ryser-style distinct-call constraints. Stage 2
   (`search/glob5.py`): per-width max-flow realisation on concrete bins. Then
   depth-8 ejection cycles (`search/chain2.py`) alternated with CP-SAT LNS
   plateau steps (`search/lns.py`, `search/loopx.sh`), up to κ
   0.001673054161426948.
2. **Evacuation neighbourhood** (new). Many cap-48 bins held only a few small
   helpers. The `evac` mode of `search/lns.py` picks 1–3 such stranded bins
   (used ≤ 20), bins with spare room and full bins whose windows contain some
   of the stranded helpers' calls, and a few empty bins, frees all their
   helpers and re-packs them exactly with CP-SAT. One 102-bin solve emptied
   35 cap-48 bins (+291 surrogate units, κ 0.001673213119136600). The
   cycle/LNS loop with `evac` in its mode mix (`search/loopy.sh`) gave the
   rest. It was **stopped while still improving**. Strict-replayed
   checkpoints: 0.001673213119136600, 0.001673243717212927,
   0.001673272876788591, 0.001673312438393585, 0.001673322090452138 and
   0.001673341928508063.
3. **Min-diff re-assignment** at the same idle profile, hence the same κ. The
   raw map relocates 62,678 rows against the selected map. The third
   version's class-level min-diff tools (`search/mindiff_cls1.py`,
   `search/mindiff_cls2.py`, `search/mindiff_lns.py`, `search/mindiff_lns2.py`,
   `search/realize.py`) give 62,678 → 1,518 → 1,415 relocations, i.e. 1,638
   changed rows of which 223 are offset-only. Stage 1 is a relaxation; one
   class's stage-1 pattern could not be realised and is now excluded with a
   new `BAN` option. The LNS polish was stopped at a two-hour budget while
   still improving. The
   class-level relaxation, solved by HiGHS, implies at least 1,002
   relocations for any legal map with this profile (a solver-reported bound,
   not a checked certificate); the shipped map is not proven minimal.

A class-level relaxation (`search/winbound.py`) gave, in the session, an
optimistic surrogate ceiling of about 908.1k units (roughly κ ≈ 0.0016741);
this map is at 906.8k. It is **not** a certified bound: the κ–surrogate
relation is approximate, and a 900 s single-worker rerun did not close the
relaxation's own bound.

The session's loop compared κ strings in one place, where trailing zeros
(`0.0016732131191366` vs `0.001673213119136600`) can mislead; `lns.py`,
`loopy.sh`, `check.py` and `verify.py` compare κ as `Decimal`.

`SEARCH.json` records the checkpoints and the commands.

## Earlier versions of this PR

- **First version**, κ 0.001672684510394236: two-stage ejection cycles on
  PR1407's map, a 23-row successor of PR1407, with the ancestry checked by
  content.
- **Second version**, κ 0.001672702955495933: a longer cycle/LNS search, then
  a min-diff re-assignment to 70 changed rows (55 relocations) against the
  selected map; the PR1407 ancestry check was dropped.
- **Third version**, κ 0.001673054161426948: a global class-level repack and
  the cycle/LNS loop, then a class-level min-diff re-assignment to 1,661
  changed rows (1,435 relocations). Its idle profile did not majorize the
  selected one, so it relied on the exact engines alone for the sign.

This fourth version replaces the map, the diff and the search record. PR1407
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
