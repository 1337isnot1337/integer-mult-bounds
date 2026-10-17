# T16 owner-packing improvement from an OR-Tools evacuation neighbourhood

This package records a **conditional packing gain**, not a new word, supplier,
mechanism, or multiplication theorem. On the same selected PR1094 T16 word and
both unchanged suppliers, a finite OR-Tools CP-SAT large-neighbourhood search
found an owner map with exact **κ = 0.001673618490895016**. The immediately
preceding map had κ = 0.001673614205725695, so the increase is
**4.285169321 × 10⁻⁹** (0.0002560428% relative). The map changes 163 rows of its
predecessor: 142 helper relocations and 21 offset-only edits.

The exact selected-word ceiling from `complex-local-word-ceiling/ceiling.py` is
`a_hi = 0.001690054109089`, giving `κ < a_hi/(1+a_hi) =
0.001687202645325402…`. This candidate realizes **99.194871%** of that κ
ceiling. The gain closes 6.589632% of the κ gap from the selected PR1094 map to
this ceiling. These are ceilings for the fixed word, template,
coverage law, and halving guard. They do not bound other words or changed
mechanisms.

The inherited exact packing certificate still proves at most 4,887 empty
capacity-48 bins and `Σ f ln(f) ≤ 908,139.013`; this candidate has 4,880 such
bins and `Σ f ln(f) = 907,279.723`. That surrogate certificate is not a κ
optimality proof. The CP-SAT run ended `FEASIBLE` with objective 10,463,952 and
solver bound 10,540,812. Exact κ and legality came from independent replay and
pricing, not from the solver objective. Later evacuation, relocation-cost,
single-call, and time-window neighbourhood rounds did not improve the exact κ.
The finite search does not establish an optimum.

## Verification

The verifier reconstructs the candidate from the predecessor's compressed
owner rows plus `DIFF-vs-predecessor.json`, regenerates `OWNERS`, `PLAN`, and
`SPEC` through the existing builder, then runs the unchanged strict T16 replay.
It also runs the independent seed67 owner audit, prices both suppliers with the
pinned engines and PR1069 sweep, calls the exact word-ceiling routine, and runs
the exact-integer packing-ceiling checker. The strict replay recomputes the
73-column chart count as 10,008.

From the repository root, run:

```sh
python3.12 scripts/research_package.py --package research/complex-t16-evacuation-increment --check-only
python3.12 scripts/research_package.py --package research/complex-t16-evacuation-increment
```

The search used OR-Tools 9.11.4210 with Python 3.10.12. Reproducing the search
itself requires the pinned research environment described in `SEARCH.json`;
the registered verifier deliberately replays and audits the candidate without
running an optimizer.

## Search overlap

The most recent complete local PR/discussion overlap snapshot was fetched on
2026-10-17 at 19:54 UTC (310 open PRs and 2,095 discussions). It showed no
matching open T16 owner-map/selected-packing PR; nearby open work concerned
T740 or T16 audit tooling. Network/DNS failures prevented a newer live refresh
during packaging, so this snapshot is evidence of the check performed, not a
claim that overlap is impossible. See `SEARCH.json` and rerun the live overlap
check before relying on novelty.

## Open next questions

The structured questions are in `TASK.json`. The most direct OR-Tools follow-up
is to price residual bins with the exact supplier engines and use those prices
to guide adaptive CP-SAT neighbourhoods. This candidate improved exact κ even
though its `Σ f ln(f)` surrogate is higher than its predecessor's, so the
surrogate can mis-rank nearby maps. First derive stable scaled marginal costs
for the residual profile, then compare those neighborhoods against the current
best using strict replay. A proof-quality bound on the remaining κ gap is still
open.

## Credit

The predecessor packing, builder, exact checkers, strict replay, and proof
retain their original authorship and notices. This incremental map and search
record were prepared by OpenAI Codex at the user's direction with substantial
AI assistance. No independent human review is claimed. New package material is
Apache-2.0.
