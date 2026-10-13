# No improvement by two frozen-domain PR589 transports

**Complete finite exclusion, independently replayed; no improved construction
or new kappa.** On the exact PR589 input, no legal sequence of at most two
transports improves the surcharge-inclusive reference root in the domain below.
This replaces another sampled scan with a complete, explicitly limited result.

Both implementations agree on every single-operation domain, the full pair
candidate transcript, all 93 pair-profile deltas and their occurrence counts.
Every independent price enclosure lies inside the primary enclosure. The
complete primary pair scan took 372.174 seconds; the separate integer-geometry
and rational-series replay took 125.896 seconds. No paid service was used.

| Census | Quantity |
| --- | ---: |
| Elementary A/B operation identities | 3,064 |
| All literal legal single transports | 1,452,893 |
| Single exact ties / strictly worse | 1,227,676 / 225,217 |
| All distinct overlapping ordered operation pairs | 59,998 |
| Pair-specific projected first states | 327,963 |
| Final second-move frame/touch representatives | 1,379,084 |
| Pair representative exact ties / strictly worse | 1,282,055 / 97,029 |
| Better / unresolved results in either census | 0 / 0 |

Repeated-operation pairs reduce to singles. Register-disjoint pairs reduce to
the sum of two legal baseline single deltas. For each remaining pair, the exact
projection retains **all** operations touching either mover's registers in both
sections. Thus it preserves the other mover's private-register ordering, which
the original immediate-best/own-touch shortcut does not preserve. The
[proof](PROOF.md) covers all 9,388,096 ordered choices of two operation identities;
these are not literal move-path counts.

## Exact domain and remaining scope

A move stays inside its A or B section, crosses only commuting elementary ADDs,
preserves frame nesting and the original retained COPY frames, and chooses a
frame from the original **636-frame catalogue plus the current slot's own
rational lower-bound closure**. The catalogue does not accumulate closures
from unrelated earlier slots. Both intermediate words must be legal. The
independent checker confirms all 636 original masks are exact span closures.

This settles that frozen two-transport class. It does not settle three or more
moves, a growing frame catalogue, arbitrary subspaces, Steinberg/Boolean circuit
identities, simultaneous changes through illegal intermediates, or a global
circuit optimum. The source word is historical PR589, not a claim about every
newer bit word. No native/physical admission, precision result, selected-supplier
change or complete multiplication-theorem verification is supplied.

## Reproduction

From the repository root, using Python 3 and only its standard library:

```sh
python3 -I -O -B research/pr1048-complete-feasibility/singles.py --engine primary --out /tmp/pr1048-primary-singles.json
python3 -I -O -B research/pr1048-complete-feasibility/singles.py --engine independent --out /tmp/pr1048-independent-singles.json
python3 -I -O -B research/pr1048-complete-feasibility/pairs.py --full --time-budget 900 --output /tmp/pr1048-primary-pairs.json
python3 -I -O -B research/pr1048-complete-feasibility/independent_pairs.py --full --time-budget 1200 --output /tmp/pr1048-independent-pairs.json
```

The caps are resource stops, not completeness assumptions: a capped run reports
`INCOMPLETE`. Require `COMPLETE`, all 59,998 pairs, no better/unresolved outcome,
and the exact transcript digest
`b39d6d23210ab7eee24c04e165b078e39ea00053e4be4b523f7c793e24b79679`.
The two single receipts must have identical `domains`; their delta/count/status
triples must match. Pair `totals`, `candidate_digest` and delta/count/status
triples must also match; the independent rational intervals must be enclosed
by the primary intervals. Timing and implementation-specific metadata differ.

Saved results are [primary pairs](complete-pairs.json),
[independent pairs](independent-complete-pairs.json), both single receipts,
and the [independent comparison](independent-comparison.json), which binds all
four receipt hashes. [REVIEW.md](REVIEW.md) records the separate Astra review.
The pilot files are runtime observations, not the basis of the exclusion.
The synthetic control demonstrates a strictly improving continuation lost by
the unsafe first-state quotient; it is not an improving PR589 witness.

## What this adds and who supplied what

The preserved [certified repair](../pr1048-certified-repair/README.md), local
commit `ce0b65fd4acf1d9326a586dade3fc6ad2f4d8370`, reproduces Douglas Colkitt/the
maintainers' existing root-ordering counterexample and woklerx PR1182's false
brackets. Neither finding is claimed as ours. It retains flemhhh's original
PR1048 code and woklerx's bracket repair unchanged with their notices, and adds
reference-root pricing and a bounded coverage diagnosis. This continuation
reuses those checkers and closes the precisely stated two-transport domain.

Live overlap checks through PR1230 found PR1048 and PR1182 unchanged at their
pinned heads. PR1143 concerns fixed frame slots on the different R480 word;
PR1208/1221 are fixed-profile Boolean reductions. See [OVERLAP.json](OVERLAP.json)
for the bounded search record. No general priority claim is made for commuting
search, pair projection or interval arithmetic.

Prepared by Brian Ross with substantial OpenAI Codex assistance, including
independent GPT-6 Astra work at xhigh reasoning. Credit DreamingOfClouds and the
retained supplier lineage, flemhhh's original search, the maintainers'
counterexamples and woklerx's bracket repair. The Krenn independent-verifier and
semantic-corruption methodology and ThetaTwist exact-arithmetic discipline are
credited to Brian Ross with exact source links in [PROOF.md](PROOF.md). These are
methodological adaptations, not copied code. New material is Apache-2.0; no
independent human review or proof-assistant verification is claimed.

Only this new directory is added. The completed K492/PR1162 checkout and the
earlier certified-repair package are unchanged. Nothing was pushed or published.
