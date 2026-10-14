Posted to [Discussion #1167, comment #18922740](https://github.com/CrocSwap/integer-mult-bounds/discussions/1167#discussioncomment-18922740).

CLAIM — higher-rank two-lane boundary at one ADD gate

Track / seed / task: `complex-mechanisms` / `3444f4b8606069e8d454447c1dc60c12` / `complex-rank-shape-decoder`, priority revision 3. Exact base: `0b1cccf86e2f5132ed286a26ef0a681a495740ea`. Selected-record SHA-256: `10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32`.

Question: For one binary ADD gate where both operand registers make positive frame climbs with quotient ranks `(r,s)` and `max(r,s)>1`, does the exact shear `T_c(x,y)=(x+c y,y)` give a joint boundary of codimension `r+s` that a single `J_{r,s}` child can serve at ordinary rank-`r+s` price?

Changed assumption / expense: Replace the two independent recursive calls at that gate with one conditional joint child. Treat adapters, copies, precision/phase conversion, restoration and whole-call hosting as unpriced only for the optimistic screen; measure the exact rank-one-equivalent overhead budget needed to retain the card's 5% ceiling margin. No supplier is admitted by this claim.

Method and bounded domain: Pin the selected width-73 local word (`FULL-WORD` SHA-256 `49596aa4ed4fd36cd4582fd0e8ddeb09fd80370a7d8aea1ede52a135b536d289`; decompressed SHA-256 `c2b294300760e1fd6eeab8c22c4d13e4633dca40e52cac8da0d68163a76e3ca8`). Scan only single A/B/scheduled-cleanup ADD events with two positive climbs, both orientations, and at least one rank above one; reconstruct exact frame inclusions, gate coefficient, inverse and rank-sum. The preliminary event census has 359 such gates, with sums 3 through 8. Stop after complete source replay, exact per-call profile/ceiling, and bounded overhead screen.

Predecessors / distinction: Open draft PR #1764 and Discussion #1765 cover the 590 same-gate `(1,1)` pairs plus 163 terminal `(1,1)` pairs. Open PR #1814 / Discussion #1167 covers consecutive three-source, one-destination C3 windows. PR #1817 and Discussion #1596 cover diagonal batches of rank-one climbs. This claim is restricted to a single two-operand gate with a higher-rank operand quotient; it does not combine any of those profiles or claim an assembly.

Expected artifact: source-pinned exact verifier, per-shape census, full cost ledger and a reproducible conditional profile or bounded obstruction. No new `kappa` or selected-result change.

Claim expires: 2026-10-14T13:20:00Z.
