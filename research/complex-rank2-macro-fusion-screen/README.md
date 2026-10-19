# Selected complex rank-two macro-fusion screen

**A source-bound negative screen for direct pair fusion. No new supplier or κ claim.**

## Result

The selected complex trace has 2,412 rank-one child climbs per orientation. A direct pair-to-rank-two macro would be attractive in the recursive cost model: if it preserved the exact operator, replacing two rank-one calls by one rank-two call would multiply that pair's recursive charge by `2^-a`, for the provider saving exponent `a > 0`.

This screen checks the narrowest concrete version of that idea against the pinned selected source. It walks each register's climb history and looks for two successive rank-one climbs whose combined endpoint transition also has an exact rank-two child recipe. Each orientation has 1,441 such rank-one successor links, of which 35 have a matching direct rank-two recipe. **All 35 candidates are interrupted by scalar operations on the same register**: 20 have five such touches, five have two, and ten have one. No candidate can be substituted directly while preserving the recorded scalar schedule.

This is a negative result for direct local pair replacement, not an impossibility theorem for macrocircuit fusion. A rank-two recipe with the same endpoint frames does not by itself prove equality with the two rank-one child maps plus intervening scalar work. Linearity suggests moving the post-add climb to its add operand so the target uses the rank-two endpoint recipe. We checked all 100 candidate/add-operand instances: none of those source registers already receives the exact same rank-one frame transition anywhere in the trace. Thus this simple call-reuse route also has no selected call to absorb the moved work. A larger synthesizer could find an equivalent transition in another basis, absorb multiple scalar operations, change neighboring registers, or choose another intermediate frame; this screen does not test those options. The selected κ remains `0.001672660197076918`.

## Task and overlap

Base: canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`. The original task is `complex-rank-shape-decoder`; this package narrows it to direct fusion of two rank-one frame climbs into an available rank-two endpoint recipe in the selected complex schedule. It does not satisfy the task's construction or five-percent acceptance gate.

The overlap refresh covered 677 open PRs and 2,578 Discussions with complete pagination and found no direct match for selected-source rank-two pair fusion. The local [two-invocation stage-pair audit](../../docs/research/stage-pair-audit.md) studies a different bit-side graph and a bounded family of joint frame changes; it is relevant boundary guidance, not the same source-level test. The overlap report is not a novelty certificate. Exact source and member pins are in `SOURCES.json`.

## Reproduction

From the repository root:

```sh
python3 scripts/research_package.py --package research/complex-rank2-macro-fusion-screen --check-only
python3.12 scripts/research_package.py --package research/complex-rank2-macro-fusion-screen
```

The registered normal and optimized replays pin the selected trace, canonical word and child recipes; replay climb and scalar-frame legality in both orientations; enumerate direct endpoint-recipe candidates; test whether any add operand already receives the same frame transition; and run wrong-rank and source-removal controls. No candidate is treated as an equivalent macro, and no full supplier replay is claimed.

## Open next questions

The exact next experiment starts with the forward phase-B candidate on register 195: event indices 12806 and 13402 climb `0→2→252`, with the sole same-register touch `add L195, L521`. Reconstruct that complete intervening region and both left/right child maps, then test whether a joint rank-two macro implements the same operator and price all changed registers and restoration. The blocker is that the selected rank-two recipe authenticates only its own endpoint transition; it does not certify equality with the composition being replaced. `TASK.json` records this question and its stopping rule.

## Credit

Credit the selected PR #1094 provider lineage and its pinned source audit. Prepared by Gonzalo Mier with substantial OpenAI Codex assistance. Apache-2.0; no independent human review claimed.
