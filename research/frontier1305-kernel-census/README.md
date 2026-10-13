# Helper-donor kernel census on the #1297/#1305/#1324 words (no new κ)

**Scoped negative result.** The highest open claims share two local words: #1324 (κ = 0.001677380107853623) and #1305 (κ = 0.001677162029073474). Both use #1297's words byte-identically, with the same owners and dispatch. On these words, neither the #1274/#1297 two-shock helper-donor family nor exact re-timing of early reads improves the exactly optimal frames. The search covers **all 306 helper pivots read before their first B write**: #1297 searched four. #1305's idle overlay is also **exactly optimal** within the donor-star class its own verifier admits. #1324 then gained by enlarging that class to simultaneous axis swaps. No construction is proposed and no selected-record change is suggested.

Coordination: [discussion #1314](https://github.com/CrocSwap/integer-mult-bounds/discussions/1314) (claim and results).

## Starting point (validated)

- **#1305 head `a96a5d95`** (jeremykothe2): its `verify.py` was run locally from a fresh checkout. It covers fresh native replays of both words, local controls, literal owner construction and strict global admission with the idle overlay. Result: `PASS_GLOBAL_MIXED_X54_IDLE_EXCHANGES_NATIVE_AND_STRICT_ADMISSION 0.001677162029073474` (127 s, macOS/Python 3.14, no Boost).
- **#1324 head `43c19465`** (jeremykothe2, posted 22:40Z while this census ran): its `verify.py` was also run locally from a fresh checkout, with fresh native replays and strict admission. Result: `PASS_GLOBAL_MIXED_X54_IDLE_EXCHANGES_NATIVE_AND_STRICT_ADMISSION 0.001677380107853623` (156 s). The #1186 pricer reproduces this κ exactly from #1324's profile: H39=1530, H42=244, H45=1477, H48=1568, H51=6555 replace #1305's idle part.
- **Independent pricing:** the #1186 `kappa.kappa(H, 37)` pricer reproduces 0.001677162029073474 from #1305's profile, and 0.001676854978651125 (#1297) without the overlay.
- **Words:** `inputs/BASE-WORD.json.gz` (125 calls) and `inputs/EXTRA-WORD.json.gz` (208 calls) are #1297's `gauge44-word.json.gz` / `extra-word.json.gz`, which are the same blobs in #1305. `inputs/CONTROL-WORD.json.gz` is #1297's input base word, before pivots 555/567 were given kernels. Pins are in [inputs/PINS.json](inputs/PINS.json).

## Searched families and results

Pricing uses the #1186 exact frame harness (PR #1186):
- an exact program-map screen;
- recomputed cone caps, tail-mutable optimal frames and cut equality;
- per-rank weights at b = 0.001679979627113687, which is #1305's certified complex lower endpoint.

Repricing the 61 + 292 + 803 base-word candidates at #1324's endpoint, 0.001680198439292940, gives identical verdicts and profiles. `ok` means certified optimal (integer duality gap 0). A screen rejection is exact: a dyadic map that differs modulo an odd prime differs over Q. `infeasible` means there is no legal frame assignment in the model. Both words give identical tallies.

| Family (per word) | Pivots with matches | Candidates | Exactly neutral | Frame-infeasible | Inexact | Gains |
|---|---:|---:|---:|---:|---:|---:|
| #1297 two-shock relation, restore at end of early cleanup (`--restore tail`, the #1297 rule) | 25 | 61 | 32 | 8 | 21 | **0** |
| Same relation, helper restored just before the pivot's first write (`--restore first`, exact by construction) | 43 | 292 | 52 | 240 | 0 | **0** |
| Exact re-timing of early reads within the target's suffix segment (single moves to three slots plus the joint move per pivot; the 152 pivots with a positive deletion price) | — | 803 | 635 | 168 | 0 | **0** |

**Positive control.** On the control word, `census.py` reproduces #1297's five hooks for each of pivots 555 and 567, including its committed donors 620 and 628 with partners 383 and 399. Every hook is priced at −11,707 units, which is H1 −3, H3 +1: the realized #1297 kernel, worth 2.616e-7 κ over 333 calls.

**Deletion screen, a heuristic and not a bound.** `deletion.py` prices the word with every early read of one pivot deleted and no compensation. 152 pivots have a positive price. The largest are:

| Pivots | Price (units) | Notes |
|---|---:|---|
| 439, 444 | −67,944 | the X=439/444 slot sites of #1195's fusions |
| 438, 440 | −62,316 | |
| 230, 238, 226, 228, 231, 232, 236, 434, 436, 446 | −51,648 each | read early by two helpers and one output |
| 12 further pivots | −44,075 each | |

Under exact pricing, a −51,648 profile change (H1 −12, H2 +4, H3 −4, H4 +4 per call) would be worth +1.16e-6 κ.

This is **not** an upper bound on kernels. On the control word the uncompensated deletion of 555 or 567 is frame-infeasible, yet the exact kernels are feasible and gain. Deletion changes the map-derived constraints that compensation restores. Use the screen only to choose where richer compensations are worth attempting.

**Idle overlay of #1305.** `idle_optimum.py` reruns #1305's group enumeration over 3,687 (replica, port) groups and 11,374 eligible children. Each group has at most four completely idle rank-48 non-owner children. Unlike #1305's builder, it picks axis triples by exact backtracking rather than greedily. The optimum equals #1305's selection in every group: 3,251 donors and 5,025 receivers. No size-4 group admits one donor serving three receivers, and 963 groups admit no exchange. A further idle gain therefore needed a larger class, not a better selection. #1324 supplies one: simultaneous axis reassignments inside each group, with its own operator check. Its 4-child groups reach (51,51,51,39), so this part is superseded as a frontier statement and remains a closure statement for #1305's class.

## What is and is not established

- **Established:** finite exhaustive results for the families above, on these two fixed words, in #1186's exact frame model. Census replays are exact rational arithmetic, standard library only.
- **Not established:**
  - anything about other compensation families: three or more shocks, window donors on helper readers, or cleanup-side corrections;
  - other words, other owner maps or hosting changes;
  - any impossibility theorem.
- **Not run, since nothing is admitted:** native replay and strict admission of candidates.
- The idle statement holds only inside `verify_idle_overlay.py`'s admitted class.

## Reproduce

Standard-library check, about 30 s. It replays every census exactly, binds every priced record to a census match, recounts all evidence against [RESULT.json](RESULT.json), runs the positive control, and checks that four failure controls are rejected:

```sh
python3 -B research/frontier1305-kernel-census/verify.py
python3 scripts/research_package.py --package research/frontier1305-kernel-census
```

To regenerate all 16 evidence files and compare them byte for byte you need PR #1186's toolkit; this takes about 4 minutes with 14 workers:

```sh
python3 -B research/frontier1305-kernel-census/regenerate.py \
  --toolkit <checkout of PR #1186>/research/exact-frame-toolkit --out /absolute/new/dir --workers 14 \
  [--idle-run <#1305 verify work dir> --idle-owners <#1305 package>/OWNERS.json.gz]
```

## Open next questions

- **Do three-shock or window-donor relations exist for the high-screen pivots** (438/440 and the ten −51,648 pivots)?
  - *Why it matters:* their screens are four to five times a realized kernel. The two-shock family is now exhausted on these words.
  - *First step:* extend `census.py`'s dictionary from output-read donor pairs to windows `x += c·q … x −= c·q` on any register x, closing before the pivot's first write. Solve d as a sparse dyadic combination of at most three terms, then price with `price.py`.
  - *Blocker:* each pivot has roughly 2,500 distinct suffix vectors, so the search needs support-guided enumeration rather than all triples.
#1324 has since answered the idle question that was here: a larger simultaneous-swap class does admit (51,51,51,39) groups.

## Credit

The words, relation rule and edit format are from rohanarun's #1297 (`search_relations.py`), built on Jeremy Kothe's #1274 helper-donor kernel mechanism. Jeremy Kothe's #1305 and #1324 contribute the idle overlay compositions and strict packages, after Gonzalo-Mier's #1252 idle exchanges. The lineage also includes #1218/#1193/#1148/#1195. Prior saturation sweeps on the #1218 words are Wronskode's #1288, and the idle ceiling on #1094 is PatatePatatePatate's #1276. The pricing harness is #1186. See [NOTICE.md](NOTICE.md).

Prepared by Marius-Paul Dumitrean with substantial AI assistance (Anthropic Claude, via Claude Code). Apache-2.0.
