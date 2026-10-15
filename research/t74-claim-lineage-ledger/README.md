# T74 handoff line: pinned κ ledger, stated-comparison check, and independent-check map

**Research consolidation; no κ claim.** The T74 handoff line has twelve open conditional-κ PRs with interlocking
"exceeds PR#### by X" statements. This package pins each PR's own claim file and recomputes every stated
comparison. It flags the ones that do not match, and maps which claims have independent checks.

## Ledger (pinned claim files, exact heads; `PINS.json`)

| PR | author | κ (pinned claim file) | + over previous row | construction step (from the PR) |
|---|---|---|---|---|
| 2269 | jeremykothe2 | 0.0016962471390584742207 | | capped phase-cell fusion outer on the T74 borrow43 supplier |
| 2288 | jeremykothe2 | 0.0016963109504150503355 | +6.381136e-8 | exact frame refit of the borrowed gauge44 word |
| 2302 | jeremykothe2 | 0.0016963957667360813401 | +8.481632e-8 | pivot-518/506 helper-donor kernels |
| 2309 | Dugongue | 0.0016965151242727336160 | +1.193575e-7 | 44th dirty alias with owner repacking |
| 2312 | jeremykothe2 | 0.0016968910672416183217 | +3.759430e-7 | helper width exchange |
| 2322 | Vlado-V | 0.001697060296258836 | +1.692290e-7 | four coherent helper handoffs |
| 2349 | jeremykothe2 | 0.0016970659941088806668 | +5.697850e-9 | owner relocations on PR2322's words |
| 2363 | mason-hale | 0.001697147064845350 | +8.107074e-8 | whole-role augmenting paths (owner map) |
| 2374 | jeremykothe2 | 0.0016971949509017704265 | +4.788606e-8 | exact owner fill on PR2322's words |
| 2435 | jeremykothe2 | 0.0016985113436976293290 | +1.316393e-6 | entrance raise of 24 copy buffers |
| 2447 | jeremykothe2 | 0.0016985119240027614377 | +5.803051e-10 | pattern-optimal owner fill (PR2442) |
| 2462 | jeremykothe2 | 0.0017035523129795943854 | +5.040389e-6 | optimal owner fill for PR2436's aliases on the entrance-raised words |

## Stated comparisons re-checked (`COMPARISONS.json`, transcribed verbatim)

Nine of twelve are consistent to their printed precision. **Three are mismatches.** In each, the stated number is
the difference to a different PR than the one named. The κ values themselves are not affected.

| PR body says | true difference | the stated number is actually | suggested text |
|---|---|---|---|
| PR2302: "exceeds PR2288 … and PR2269 by 8.48163E-8" | vs PR2269: 1.486277E-7 | the difference to PR2288 | "exceeds PR2288 by 8.48163E-8 and PR2269 by 1.48628E-7" |
| PR2374: "… and PR2312 by 1.28957E-7" | vs PR2312: 3.038837E-7 | the difference to PR2349 | "… PR2349 by 1.28957E-7 (PR2312 by 3.03884E-7)" |
| PR2435: "… and PR2312 by 1.31639E-6" | vs PR2312: 1.620276E-6 | the difference to PR2374 | "… PR2312 by 1.62028E-6" |

There is also a **README mislabel in PR2435**. `research/gmx-t74-borrow43-handoff/README.md` says "exceeds PR2374 (our
previous package, kappa 0.0016985113436976293…)". That value is PR2435's own κ. PR2374's pinned κ is
0.0016971949509017704….

## Independent checks per claim (as of this package)

- **PR2269:** words, fill and root independently reproduced by PR2315. Its outer side conditions were audited in
  PR2286, on the PR2044 lineage.
- **PR2322 words:**
  - PR2402 certifies that every owner fill has b < 0.001697195759.
  - PR2442 shows PR2374's fill is the unique exact pattern optimum, so PR2349 and PR2363 are dominated owner maps
    on the same words.
- **PR2435:**
  - PR2446 independently reproduces the words, the 289,044-role owner map and the root. It also finds that the
    change is frame-only, with entrance delivery left unchecked.
  - PR2453 prices the mechanism.
- **PR2447:** PR2466 independently checks it and shows it is exactly the PR2442 optimum, so the fill is provably
  optimal for those words.
- **PR2462:** no independent check yet. Its claim rests on PR2436 (tekuuu, four aliases plus 24 entrance raises).

## Reproduce

From the repository root, standard library only:

```sh
python3 -I -B research/t74-claim-lineage-ledger/ledger.py --fetch
```

`--fetch` fetches each `refs/pull/N/head` whose pinned head is absent.

Expected final line:
`PASS_T74_CLAIM_LEDGER prs=12 comparisons=12 consistent=9 mismatches=2302->2269,2374->2312,2435->2312 readme_2435_mislabel=1`

The expected mismatch set is asserted, so a corrected PR text or a moved head makes the check fail deliberately.
All results were run on CPython 3.14.4; the registered Python 3.12 replay was not run locally.

## Scope and limits

- **What is checked.** Only the stated numbers in PR bodies and one README sentence. The κ values are read from
  each PR's own claim file. No κ, outer ledger or construction is re-derived here.
- **Unpinned baselines.** Comparisons against PR2265 and PR2436 are not included, because their claim files are
  not in the standard place.
- **Snapshot.** Heads are pinned as of 2026-10-15; later edits are not reflected.

## Open next questions

- **PR2462.** Is PR2462's owner fill exactly optimal for its words, and do its words recount to its report? First
  step: run PR2442's `owner_optimum.py` and PR2446's checker on PR2462's pinned files.

## Credits and licence

- PR authors as listed: Jeremy Kothe, Dugongue, Vlado Vojdanovski, mason-hale, tekuuu (PR2436).
- PR2315 / PR2402 / PR2442 / PR2446 / PR2453 / PR2466 (this author): the independent checks referenced.

Prepared with substantial AI assistance (Claude Code, Anthropic, Claude Opus 5.5). No independent human review is
claimed. Apache-2.0.
