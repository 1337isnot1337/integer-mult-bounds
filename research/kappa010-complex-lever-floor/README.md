# Joint-lever floor for a κ = 0.1 target

**Scoped budget screen; no κ improvement or supplier is claimed.** The selected conditional result remains κ = 0.001672660197076918. This checks what the already explored two-output anchor, centre removal, rank-16 repacking and a changed coverage law would need to accomplish at `κ=1/10`.

## Result

The retained transfer `κ = a/(1+a)` maps `κ=1/10` to the exact target `a=1/9`. We use the certified outward-rational interval engine in `complex-local-word-ceiling/ceiling.py` and the pinned selected profile and two-output-anchor receipt.

The selected complex word still fails badly at the target after deleting its eight rank-8 centre children and all 64 units of centre charge. Its largest feasible unpaid count with that fixed local profile is `u=17`; the exact interval moment there is approximately **1.151904798395**, above one. Since increasing `u` only reduces the idle remainder and this is already the largest feasible `u`, no coverage change alone can rescue the fixed selected profile in this relaxed model.

We next grant the strongest combination from the local two-output-anchor exploration:

1. Seven hypothetical 112-port blocks replace 332 rank-one children with 112 children per block.
2. The 112 affine additions in each block are charged as 112 rank-one-equivalent units, giving rank-one profile count 1,656.
3. The complete centre path is deleted, including its 64-unit charge and eight rank-8 children.
4. All remaining paid local rank mass, exactly 4,766, is fractionally repacked into rank-16 children.
5. All source alignment, dirty-state handling, routing, frame, precision, restoration and physical costs are waived.

Even this combined relaxation has target moment **1.077445412079** with four unpaid coordinates. Its exact unpaid-coordinate boundary is:

| Model at `a=1/9` | Previous integer | Moment | First passing integer | Moment |
|---|---:|---:|---:|---:|
| Seven anchors, centre free, original local ranks | `u=23` | 1.007064932212 | `u=24` | 0.992809414512 |
| Seven anchors, centre free, all mass at rank 16 | `u=9` | 1.006167823580 | `u=10` | 0.991912305880 |
| Same rank-16 model, centre charge retained | `u=10` | 1.001076567258 | `u=11` | 0.986821049559 |

The inequalities are decided by exact rational interval endpoints; decimals are for orientation. The positive control reproduces a passing moment at the repository's smaller planning target `a=1/99` with the same ideal rank-16 profile and only one unpaid coordinate.

There is also a concrete five-plane P112 decoder in the local archive with a reported `u=5` endpoint. Its pinned profile is `{1:2412, 2:418, 3:432, 4:142, 5:82, 7:10, 8:6}`. Using the exact same selected replay archive as the present checkpoint, its moment at `a=1/9`, `u=5`, and centre charge 64 is **1.336180761792**. More strongly, its paid local terms alone contribute at least **1.165241830803**, before any idle remainder is added. Therefore no change to `u`, centre charge or idle packing can make this *fixed local profile* reach the 0.1 target. This is scoped to its profile, not to the P112 endpoint family or other decoders.

Even replacing that whole profile with fractional rank-16 children and deleting the centre leaves moment **1.080393847328** at `u=5`; the first passing counts are `u=11` centre-free and `u=12` with the centre charge. With `u=5` held fixed, every 5,640 units would instead need a uniform local rank of at least 37 centre-free or 41 with the centre. The existing decoder's paid terms have ranks 7 and 8. The exact threshold checker reuses its pinned profile and source manifest; it does not replay that decoder's algebra.

There is a clear exchange rate between the two remaining structural levers. Keep the same 4,766 units of local mass, place it fractionally at one uniform rank `r`, and leave only the idle remainder at rank 51. The first passing `u` is:

| Assumed local rank `r` for all 4,766 units | First passing `u`, centre free | First passing `u`, centre retained |
|---:|---:|---:|
| 16 | 10 | 11 |
| 32 | 6 | 7 |
| 48 | 4 | 4 |
| 51 | 3 | 4 |

Conversely, with only four unpaid coordinates, the local consumer must place all this mass at rank at least 42 if the centre is removed, or rank at least 47 if it remains. These are exact boundaries in the relaxed profile model. They suggest the concrete alternatives for further construction work: prove substantially more unpaid coverage, or build a consumer close to the maximum admitted idle rank. Neither exists at the selected provider boundary today.

The target also leaves little room for a complete anchor invoice. With all 4,766 units placed at rank 16, the largest integer per-block rank-one-equivalent fee is `e=170` at `u=10` with the centre removed; `e=171` fails. The known 112 affine additions use 112 of that allowance, leaving at most 58 units per block for every other interface cost under the same tariff. If the centre charge remains and coverage rises to `u=11`, the boundary is `e=207` passing versus `e=208` failing, leaving 95 units beyond the 112 affine additions. These are exact moment boundaries, not realized physical prices.

This gives a concrete target-scale requirement for this bundle: even after granting all its local and consumer costs for free, it needs **ten unpaid coordinates per live family** if the centre is actually removed, or eleven if the centre charge remains. The existing selected contract has one. The local anchor result does not realize any replacement coverage identity, and fractional rank-16 repacking is not a decoder.

## Tensorized paired-plane endpoint: additive composition still misses

I checked a more aggressive escape using the exact [block-valued paired-plane endpoint](../paired-plane-block-rank/README.md) and its [49-support scalar fit](../paired-plane-minrank-bracket-audit/README.md). The fixed fit partitions the 112 ports into supports of sizes `{1: 2, 2: 31, 3: 16}`. Under the full port-space charge used by PR2203, a support of size `s` touches `s` mutually orthogonal nondegenerate planes and costs rank `2s`. Its exact copy profile is therefore `{2: 2, 4: 31, 6: 16}`, with mass **224 per payload copy**. Tensoring the fit by `d` copies gives unpaid count `u=2d` and multiplies this profile by `d`; the all-size block-rank receipt confirms the fixed mask has normalized query rank `49d`.

Now combine those `d` copies with the seven-anchor profile. After replacing seven groups of 332 rank-one children by 112 children, the non-centre base mass is 3,982. I grant the strongest allowed idle/consumer relaxation by placing all of it at rank 51, and charge only the unavoidable dirty-output affine updates: each of the 110 arbitrary dirty destinations must receive a nonzero product-dependent correction, and one `ADD` changes one destination, so every 112-output block needs at least `q−2 = 110` additions. This is more favorable than the anchor's actual 112-add schedule. If the centre remains, its eight rank-8 children are restored to the profile along with its 64-unit charge.

| Payload copies `d` | Unpaid `u=2d` | Target moment at the minimum 110 additions, centre-free / retained | Maximum affordable additions per block, centre-free / retained |
|---:|---:|---:|---:|
| 1 | 2 | 1.082289 / 1.093548 | none; it fails with zero additions |
| 2 | 4 | 1.063520 / 1.074779 | none; it fails with zero additions |
| 3 | 6 | 1.044752 / 1.056010 | 28 / 8 |
| 4 | 8 | 1.025983 / 1.037241 | 62 / 42 |
| 5 | 10 | 1.007214 / 1.018473 | 96 / 76 |

The entries are certified outward-rational intervals; decimals are only for reading. Thus every `d≤5` fails even after allowing all remaining mass to use rank-51 children and reducing the anchor to its 110-update lower bound. For `d≥6`, the same minimum invoice already exceeds the coverage mass: at `d=6` it is over by exactly `208/9`, and each extra copy increases the excess by `3808/9`. Keeping the centre adds its charge and children equally on the two sides of this mass comparison, so it does not repair the excess.

This closes only the **tensorized paired-plane fit plus additive seven-anchor map** under the selected coverage law and the one-target `ADD` contract. It does not price a changed support mask or a recursive child that jointly updates multiple dirty destinations. Such a child would have to reduce the 110-update floor by at least 14 (centre-free) or 34 (centre-retained) in the best `d=5` row, while also supplying the endpoint identity and full source/restoration contract. The fitted matrix alone does not do that. No supplier or κ improvement is claimed.

## Scope and next step

The result rejects only the fixed selected profile and the stated seven-anchor/centre-free/rank-16 relaxation. It is not a theorem about other local words, suppliers, recursion widths or multiplication algorithms. It also does not independently reprove the predecessor anchor's local bilinear map.

The next decisive experiment must change the endpoint or the recursive consumer together: the additive d-fold plane decoder cannot fit beside even the minimum dirty-output updates, while d≥6 also violates the paid-mass envelope. A bounded follow-up should start with one complete dirty-input block whose child output writes more than one dirty destination, then price that changed contract against the d=5 target row. The blocker is that no such multi-target recursive child or selected-provider placement is currently source-bound. Further searches over the same scalar support fit or anchor schedule cannot change this decision.

## Reproduction

From the repository root:

```sh
python3 -B research/kappa010-complex-lever-floor/verify.py
python3 scripts/research_package.py --package research/kappa010-complex-lever-floor --check-only
python3.12 scripts/research_package.py --package research/kappa010-complex-lever-floor
```

The verifier binds the selected record, current local ceiling model, two-output-anchor result, and paired-plane fit receipts in [SOURCES.json](SOURCES.json). It checks the exact `a=1/9` interval boundaries `u=23/24`, `u=9/10` and `u=10/11`, the rank/unpaid and fee frontiers, the 49-support full port-space profile, every tensor multiplicity `d=1..5` at its minimum dirty-update count, the `d≥6` mass excess, and the lower `a=1/99` positive control.

## Predecessors and credit

This is a target refinement of the `coverage-law-change` question, motivated by the donor-set target κ > 0.1. The local two-output temporary-sum map and its seven-block hypothesis are Cinna / commdata2338's [two-output anchor](../complex-two-output-sum-anchor-seed65ce19/README.md); retain its predecessor attributions. The paired-plane construction retains the credits in its own README, including thakrarsagar's 49-support fit, ywz65's block-rank extension, Adam Gall's strict mask, and the PR1825 matching and PR2203 native payload accounting. The interval ceiling and selected profile are credited in [complex-local-word-ceiling](../complex-local-word-ceiling/README.md). This package adds only target-specific combined-lever budgets. Prepared by Codex with substantial OpenAI assistance; no independent human review is claimed. New work is Apache-2.0.

A fresh overlap refresh on 2026-10-17 covered 259 open PRs and 1,866 discussions (complete pagination). Open PR #3093 checks two fixed local profiles (#2979 and #3042) at the same target. This package instead evaluates the selected profile, the pinned five-plane profile and the seven-anchor/centre/rank-16 relaxation, including exact unpaid-coordinate and per-block-fee boundaries; the scopes are complementary. Local matches include the earlier `kappa01-complex-target-screen`, the P112 five-plane decoder and prior coverage-law packages, so novelty is not claimed. Relevant PRs #3064 and #3097 and Discussions #1163, #1166, #1167 and #2838 were also checked. Canonical main was refreshed at `18aacb215fc3717b06be8ceb9fca62aeca0d3e99` (priority revision 6); the selected record and quantitative predecessor receipts are unchanged.

## Open next questions

1. **Can a complete dirty-input endpoint leave ten coordinates unpaid?** It matters because ten is the first passing boundary even after granting a rank-16 consumer and centre removal. First step: bind one named block to a selected-provider trace and prove its entry/exit map, coefficient delivery and restoration. Blocker: no source locations or changed coverage identity are supplied.
2. **Can the selected provider realize a rank-16 consumer for the remaining 4,766 units?** The fractional profile passes at `u=10`, but it does not give a physical decoder. First step: exhibit an exact local decoder and its frames, then run the full cost through the selected word. Blocker: the anchor package has no selected-provider rank-16 consumer.
3. **Can seven two-output anchors be placed within the target budget of `e≤170` per block?** The 112 affine additions leave at most 58 rank-one-equivalent units for every other interface cost. First step: find one source-bound occurrence with the two clean required outputs and price its acquisition, routing, frame and cleanup. Blocker: no selected trace alignment has been established.
