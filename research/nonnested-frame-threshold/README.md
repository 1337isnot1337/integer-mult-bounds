# Small nonnested rewrites cannot improve this invoice

Prepared for Cinna Davis with OpenAI assistance. Apache-2.0.

## Scoped theorem

Fix arbitrary-input helper interfaces and all main endpoints. Fix the owned-center jobs and their charges. Allow exact dimension-preserving free transports and changes to scalar contacts. Suppose the old ordinary frame trajectories are monotone. If the new trajectories have at most 33 charged ordinary bridges and contain any nonnested or descending bridge, their paid moment is strictly larger for every exponent t=1-kappa with 0 < kappa <= 1/330.

Count all new bridges on the affected trajectories, including any repair or cleanup bridge. Unaffected trajectories cancel. A cut must preserve its endpoint frames, not merely its dimensions. Helper credit must be unchanged. These hypotheses exclude changed helper inventories, new consumer contracts, free non-dimension-preserving maps, and unfunded endpoints.

## Proof

Use the sufficient arbitrary-frame primitive in Dugongue's PR4635, head 898b0c8e2ca23897c312230988515c2553154f30:

    r(U,V) = dim(U) + dim(V) - 2 dim(U intersection V).

For subspaces of F2^9, 0 <= r <= 9. Write

    r(U,V) = dim(V) - dim(U) + 2[dim(U) - dim(U intersection V)].

Summing over each trajectory telescopes. Free transports preserve dimension. The old monotone rank mass M is the sum of endpoint dimension differences. Any descending or nonnested edge makes the bracket positive, hence the new rank mass is at least M+2.

For integers 1 <= r <= 9, exp(-x) >= 1-x gives

    r - r^(1-kappa) <= r*kappa*log(r) < 9*kappa*(11/5) <= 3/50.

Here log(9) < 11/5, verified by an exact positive Taylor lower bound for exp(11/5). Therefore the new moment exceeds its rank mass minus 33*(3/50). The old moment is at most M. The new minus old moment is strictly greater than

    2 - 99/50 = 1/50.

This is a paid-moment obstruction, not a barrier to arbitrary new constructions. It explains why allowing a few nonnested contacts cannot exploit the new primitive near the current exponent. A genuinely nonmonotone improvement must affect at least 34 paid bridges, or change another hypothesis. Thirty-four is necessary, not sufficient.

## Reproduction and sources

Run `python -B research/nonnested-frame-threshold/verify.py`. It checks the rational numerical inequalities and enumerates all subspaces of F2^3 to verify the rank-mass decomposition. That finite test corroborates, but does not replace, the displayed dimension argument.

The frame primitive and constructive phase-aware realization are credited to PR4635's ARBITRARY-FRAME-BRIDGES.md and its retained canonical Clifford sources. This package does not independently rerun their absolute-phase lowering. The threshold argument is derived here. No new kappa or universal optimality is claimed.

## Open next questions

Search coordinated windows with at least 34 affected bridges, or change helper endpoints and price their actual relative operators. Favor a favorable exact rank invoice before implementing a large physical candidate. Small monotone changes remain possible and are not ruled out by this theorem.
