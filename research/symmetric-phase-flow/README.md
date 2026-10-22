# Exact phase-form rigidity and paid phase-flow screens

Prepared for Cinna Davis with OpenAI assistance. Apache-2.0. The phase-form and graph-cut mechanisms are credited to Dugongue's PR4654, head dca175fed8ebde8980635fd3b4508b8cba89a1b0, specifically PHASE-FORM-GRAMMAR.md and PHASE-CUT.md. Canonical frames, native maps, scalar words and helper contracts retain their original repository credits.

## Exact finite result

For the published helper-warp word, frozen main endpoints, frozen owned-center contacts, fixed native maps and unchanged paid ranks, the full symmetric-form linear system has 10,165 variables, 43,890 equations and rank 10,165 over F2. Thus only the zero form assignment survives. This is not just a rank-one search. Both helper entrances and exits are allowed to vary, subject to shared scalar-contact and transport constraints.

The graph has 4,162 frame nodes, collapsed to 1,059 shared-contact nodes. Two elimination implementations with opposite pivot orders agree on full rank. Actual native warp images are checked against their source/target spans. The compressed source word is hash-pinned. This finite rigidity statement applies only to the displayed fixed word, boundaries and no-extra-rank equations.

Run `python -B research/symmetric-phase-flow/search.py --check` for an immutable receipt check. Assertions must remain enabled. Without --check, the script regenerates RESULT.json. The source tree is required.

## Paid discovery screens

`cuts.py` tests all 511 nonzero ambient rank-one forms with each of two helper-boundary modes, for 1,022 min-cut searches. `general_cuts.py` tests 229 more fixed forms in each mode: 36 elementary alternating forms, identity, 96 deterministic random symmetric forms and 96 sums of two rank-one forms. All 458 additional searches return the empty cut with zero energy.

These are bounded discovery results. Capacities are rounded to a 10^-6 grid and selected cuts are reevaluated with floating-point moments. No exact global minimum or universal phase obstruction follows. No candidate with a strict negative cost was found, so no physical candidate or new kappa is claimed.

`defects.py` permits arbitrary symmetric forms while removing the equality constraints for one paid edge at a time. An exact basis-coordinate calculation finds only four nonzero single-edge defects. None changes any helper's productive form. Edges containing no selected independent constraint cannot lower the full rank when removed. This covers all individual paid edges, but not multiple simultaneous defects. DEFECTS.json retains the four exceptions.

## Open next questions

Frozen owned-center gauges are a genuine restriction. The adjacent owned-center-phase-flow package explores them with explicit center-rank accounting. Multiple paid defects and simultaneous moving subspaces remain outside these tests. A profitable proposal must undergo exact moment, phase, all-column, compiler and outer admission checks.
