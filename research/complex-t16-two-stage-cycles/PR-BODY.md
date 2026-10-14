# Record candidate: two-stage ejection cycles on PR1407's T16 owner map (κ=0.001672684510394236)

## Contribution

This PR adds `research/complex-t16-two-stage-cycles`, a registered research
package. It is a conditional T16 owner map on the **unchanged selected PR1094
supplier**, with no new mechanism.

- **κ = 0.001672684510394236** (conservative 0.001672684507542306).
- That is +3.69e-9 over open PR1407 (0.001672680818492982) and +1.4536e-5
  relative over the selected record (0.001672660197076918).
- Idle remainders go from `{1:2277, 3:377, 16:3, 48:4866}` (PR1407) to
  `{1:2278, 3:374, 8:1, 16:3, 48:4866}`. In effect, residuals 3+3+3 become
  8+1, with rank mass 1,041,408 and deficit 5,120 unchanged.
- The search ran in two stages on PR1407's map:
  1. Two ejection cycles through bin (12,4,0). The first is neutral and moves a
     free 3 into the bin. The second merges another free 3 into it.
  2. One 7-move cycle that turns free 3+3+6 into 8+1+3.

  That is 16 whole-helper placements and 14 net relocated rows. Widths, call
  order, windows and the local and bit suppliers are unchanged.
- The unchanged PR1087 strict replay passes all 11 stages, with controls
  69/12/6/15.
- The seed67 owner auditor passes R1–R7, X1, X2 and its 11 controls. Pricing
  with the pinned exact engines and the PR1069 sweep agree with the replay.
- `SPEC.expected.actual_73column_sigmas` is 10000, the same as PR1407. It is
  the chart count the strict audit recomputes and `assemble.py` pins; it is not
  a free setting. The README explains it.

It claims no packing optimum and no unconditional theorem. All PR1094 inherited
assumptions remain.

## Dependency on PR1407

This candidate **builds on open PR1407** (pai-scaffolde, head
`d8640f5b7ae99b43f5d56146cb94ca62b8b3835d`). The package does not need PR1407
merged:

- It ships the complete map and verifies it against the merged selected PR1094
  archive.
- `DEPENDENCY-PR1407.json` pins PR1407's head commit, data blobs and SHA256s.
  `verify.py` undoes this package's 23 rows and requires the result to equal
  PR1407's owner content hash.

If PR1407 is rejected for a reason that applies to its moves, this candidate
falls with it. If PR1407 changes its map, this package needs a rebase.

PR2077 (lydakis) is an **alternative**, not an ancestor. Its vacancy-chain idea
inspired the cycles, but none of its four moves compose with PR1407: all 15
subsets are illegal on PR1407's map, because PR1407 already moved row 34306
out of bin (11,8,103).

## Provenance

- **Chooser:** this work was not drawn by `scripts/choose_research_task.py`. It
  was self-selected as the review-and-compose task: a review of PR1407 and
  PR2077, a test of whether they compose, and then a search on the stronger
  map. `TASK.json` records it under the closest card, `selected-packing`, with
  `scope_status: changed` and this reason.
- **Base:** `0fdd7d82`. The 287 pinned inputs are listed in `INPUTS.json` and
  `SOURCES.json`.
- **Credit:**
  - pai-scaffolde (PR1407): direct parent.
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

The full replay takes about 50 s and uses only the standard library. The
search is optional and needs numpy; the README gives the commands. Each stage
takes about 15 s and reproduces `data/OWNERS.json.gz` exactly.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
