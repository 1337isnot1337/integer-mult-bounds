# Exact rank-cap floor for a κ = 0.1 target

**Scoped negative budget result. No supplier or κ improvement is claimed.** The selected conditional result remains κ = 0.001672660197076918.

## Result

The retained transfer is `κ = a/(1+a)`, so κ = 1/10 corresponds to the primitive target `a = 1/9`. For any charged child of rank `r < m`, its moment contribution per unit rank mass at that target is

\[
\frac{(r/m)^{8/9}}{r}=m^{-8/9}r^{-1/9},
\]

which decreases with `r`. If all child ranks are at most `R`, total paid rank mass is `P`, and `w` families are served per call, every histogram therefore has moment at least

\[
F=\frac{P}{Rw}\left(\frac Rm\right)^{8/9}.
\]

Under the current coverage law `P = (m-u)w + c`, write `S=P/w=m-u+c/w`. Then `F^9 = S^9/(R m^8)`, so the strict comparison with one reduces to exact rational arithmetic. We also check the more favorable case `c=0`, which deletes the positive centre/copy mass entirely.

At the largest rank admitted by the current depth envelopes, even the centre-free, one-unpaid-coordinate lower bound exceeds one on both suppliers:

| Supplier | `m` | Current maximum `R` | Exact lower-bound comparison at `a=1/9` | Approx. `F` |
|---|---:|---:|---|---:|
| Bit | 64 | 53 (depth 4) | `63^9 > 53·64^8` | 1.005219793354 |
| Complex | 73 | 51 (depth 2) | `72^9 > 51·73^8` | 1.026397274382 |

Because this is already the cheapest histogram allowed by the aggregate law and cap, every actual histogram in that model costs at least this much. The moment increases with `a`, so neither supplier can support `a ≥ 1/9`, and hence neither can support κ > 0.1, while retaining one unpaid coordinate and these maximum child ranks. Keeping the existing centre charge only raises the floors to approximately 1.015407831801 (bit) and 1.035561535761 (complex).

The closest finite two-unpaid complex candidate in the local archive is the paired-plane identity fit: it reports `u=2`, centre charge `c=112`, `m=73`, `w=896/9`, and idle cap 51. At the 0.1 target its exact lower-bound parameter is `S=577/8`, with `(S^9)/(51·73^8)>1` and `F≈1.028179214095`. Thus even granting that local endpoint and then moving *all* mass to rank 51 cannot reach κ>0.1; the aggregate floor with `c=112` needs at least four unpaid coordinates. The paired-plane package itself reports only a favorable local ceiling `a≈0.00408`, and leaves routing, restoration, precision and the bit side open.

The exact threshold screens identify what could reopen the budget:

| Supplier | Current cap; centre kept | Minimum unpaid coordinates for the *ideal floor* to drop below 1 | With one unpaid coordinate, minimum rank after deleting centre | Halving-guard depth first allowing that rank |
|---|---|---:|---:|---:|
| Bit | `R=53`, `c=63` | 2 | 56 | 6 |
| Complex | `R=51`, `c=64` | 4 | 65 | 6 |

If the centre/copy charge is also removed, the minimum unpaid counts become 2 (bit) and 3 (complex). If it stays, the one-unpaid rank requirements rise to 61 and 70, requiring halving depths 15 and 17, respectively. Every rank and depth boundary is checked with exact integer or rational comparisons in [verify.py](verify.py).

These passing threshold rows are **necessary budget openings only**. They place all paid rank mass at the maximum rank, which is an intentionally generous relaxation and not a decodable local word. The deeper guard depths have not been shown to fit their row-coefficient invoices. No second unpaid coordinate, high-rank local consumer, physical endpoint, dirty-state restoration, bit/complex composition, or complete supplier has been constructed here. The result is scoped to the two current coverage identities and their rank/depth envelopes; a different outer algorithm remains open.

## Fixed bit word with two unpaid coordinates

The all-mass-at-cap row can hide a large local-profile gap. I also evaluated the source-bound selected bit histogram `{1:1323, 2:1342, 3:79, 4:44, 5:102, 6:11, 7:19}` (rank mass 5,129) under the hypothetical `u=2` coverage law, with the best admitted idle cap `R=53`. At `a=1/9` its exact outward-rational moment is **1.365696** with the existing centre charge `c=63`, or **1.355508** after deleting that charge. So changing coverage alone does not rescue the selected bit word.

There is a stronger fixed-word bound: the local histogram by itself, normalized by the pinned `w=296/3` families per call, has exact outward-rational moment **1.195680** at `a=1/9`. This omits the centre and every idle child. Any change that retains this local histogram and `w` can only add nonnegative child costs, so changing the unpaid-coordinate coverage law alone cannot make this selected word pass. This is specific to the pinned bit word and call width; a different local word or changed `w` remains open.

For comparison, the necessary all-mass-at-cap floor with `u=2` and `c=63` is only **0.999452**. Holding the selected local rank mass at 5,129 and fractionally repacking it at one uniform local rank, the first passing rank is **53** with the centre retained; rank 52 gives 1.001209. If the centre is deleted, rank 48 first passes (0.998447), while rank 47 gives 1.000411. This quantifies the missing mechanism: a bit-side endpoint must both leave a second coordinate unpaid and replace the selected low-rank local profile with children near the maximum admitted rank. It is a scoped profile screen, not a universal obstruction or a constructed supplier.

## Reproduction

```sh
python3.12 -I -B research/kappa010-rank-cap-floor/verify.py
python3.12 scripts/research_package.py --package research/kappa010-rank-cap-floor --check-only
python3.12 scripts/research_package.py --package research/kappa010-rank-cap-floor
```

The verifier uses only the standard library. It binds the selected record and the bit/complex budget receipts listed in [SOURCES.json](SOURCES.json). Its exact acceptance decision is the sign of `S^9/(R m^8)-1`; displayed decimal moments are orientation only.

## Open next questions

1. **Can two unpaid coordinates be carried through one complete dirty-input endpoint on the bit side?** This is the least aggregate change that opens the bit floor at `R=53`, but the actual word must preserve both coordinates and pay the consumer, frame, and restoration costs. First step: trace a named two-coordinate candidate through one full selected call. Blocker: the current endpoint contract and cost invoice have not been changed.
2. **Can the complex supplier leave four coordinates unpaid while retaining the current centre charge?** Four is the exact optimistic threshold at `R=51`; it does not follow from a local two-output anchor. First step: derive the replacement coverage identity for one full outer family, including delivery and restoration. Blocker: the anchor source columns are dirty and the centre consumer is still paid.
3. **Can the outer row invoice admit depth six, or a different construction with equivalent high-rank children?** Depth six is only the guard threshold with the centre removed and one unpaid coordinate. First step: evaluate the exact row coefficient and all non-rank charges at that depth. Blocker: no such invoice is currently available, and passing the guard alone does not construct a supplier.

## Scope, overlap and credit

This refines the `coverage-law-change` card for the user-set target κ > 0.1. It tests the cheapest possible aggregate moment under the pinned coverage laws before searching for a mechanism. It does not prove that changing coverage or depth is impossible, and it does not replace the card's complete-instance acceptance gate. Local overlap surfaced the earlier `kappa01-complex-target-screen`, several paired-plane coverage-law packages, and the concrete paired-plane identity fit; this result contributes the exact shared rank-cap floor and strict threshold table for the new 0.1 target.

The bit-side predecessor is Sagar Thakrar's `bit-revision3-levers-seed03`, building on DreamingOfClouds' PR589 / `format-limits`, eumemic's PR555, and the PR510 / PR442 template lineage. The complex predecessor is Douglas Colkitt's `complex-local-word-ceiling`, building on PR1012, the selected #1094 construction, and the credited frame/ownership chain. No predecessor artifacts were modified. The task began on `d8e0f83f00191df62174b641e9fff055c357f641`; canonical main was refreshed at `18aacb215fc3717b06be8ceb9fca62aeca0d3e99` (priority revision 6) on 2026-10-17. The P104 precision-map pointer remains the only earlier relevant change. Before this update, `origin/main` advanced to `997e6a9ca7b4f95d50e366f61412fd640d72a88a`; its relevant changes add sparse-checkout/path-cache notes and record exact-head PR intake including concurrent PR3107, without changing the selected record, priority, family status or quantitative inputs. The κ conversion is unchanged.

The overlap helper refreshed open PRs on 2026-10-17 at 02:03:00 UTC (237 records) and discussions at 02:03:33 UTC (1,872 records), both with complete pagination. It surfaced extensive possible overlap, including PR #3093's fixed-profile screens and the broader target work; the helper searches PR bodies and discussion claims, not arbitrary code diffs. Earlier checks also surfaced PRs #3064 and #3097 and Discussions #1163, #1166 and #1167. This fixed-bit-profile result extends the package's own aggregate screen; no novelty is claimed. Recheck relevant heads before opening another research round.

Prepared by Codex with OpenAI assistance. New work is Apache-2.0.
