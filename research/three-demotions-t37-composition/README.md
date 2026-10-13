# Joint entrance choices with T37 whole-owner packing

The updated draft composes PR1148's joint entrance choices (head f1d8dc59288dcab77cae713c450d14069e7eec05) with a new exact T37 owner flow on PR1131's wave order. The candidate conditional price is **κ = 0.001675568675201533**, **0.0004611994%** above that PR1148 head at 0.001675560947524449.

**Verification pending:** the 159,840 literal whole-helper roles in 333 calls, exact integer flow equations, bipartite matching decomposition, and two-engine rational profile price pass. Full native replay and strict T37 admission are in progress. This draft is not yet a verified new frontier.

The local paid profile is `{1:2364,2:498,3:412,4:130,5:82,8:8}`. The new flow has idle profile `{1:834,48:11374}` and targets the fixed-word grid upper value from PR1148. An upper relaxation alone does not establish physical realization; the draft supplies a concrete owner map for full admission.

Package: `research/three-demotions-t37-composition/`. Reconstruct the owner map without an optimizer using:

```sh
python -B construct.py --flow PATTERN-FLOW.json --plan PLAN.json --out NEW_OUTPUT
```

A standalone full verification wrapper and receipts will be added after verification. The package directory name is retained from the initial three-demotion composition; its latest payload uses joint entrance groups 603, 611 and 635.

Credit: Thomas DiFiore/Codex and PR1148's full local ancestry; seslly/shipstuff PR1111's group-635 lead; Ali Romman/Codex PR1129's integer flow, matching decomposition and T37 audit; PR1131's wave order; PR1074/1018, Rohan Arun's PR987, PR1030, PR864, Hao Yan/FanPUYen's PR858, PR870, Chafik Boukhalfa's PR795/890 duals, PR942, PR1091, and the unchanged PR589 bit supplier. New composition by Rohan Arun with substantial OpenAI Codex assistance, Apache-2.0. Original notices retained.

All-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape, exact recovery, analytic transfer, PR559 recurrence correction and bit H1-H5 obligations remain. No unconditional multiplication theorem, full formalization, general sphere-packing optimality or runtime improvement is claimed.
