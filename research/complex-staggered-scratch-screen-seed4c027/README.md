# Staggered same-register rank-three packets miss the selected-word gate

**Scoped negative result. No construction or new κ is claimed.**

## Question and result

The selected PR1094 gauge44 local word has many rank-one frame climbs on the same `(phase, register)`, at different program positions. Could one rank-three child replace three such climbs if three product outputs are held in temporary arrays until their respective use positions?

The pinned source has 369 disjoint candidate triples in the forward `A`/`B` phases. I give the changed interface up to five simultaneous packet windows, requiring 15 additional scalar scratch arrays. An exact integral min-cost flow on the event line selects at most 85 compatible triples at capacity five. Replacing each selected triple by one rank-three child preserves paid mass. This creates the optimistic profile:

```text
{1: 2157, 2: 418, 3: 517, 4: 142, 5: 82, 8: 8}
```

Every scratch-array cost is set to zero: no initialization, input access, frame transitions, arbitrary dirty-state closure, restoration, hosting, precision, or controller costs are charged. Even this favorable profile has an exact packing-ceiling bracket `[107/62500, 1713/1000000]`, i.e. at most `0.001713`. The 5% acceptance target is `35491136290869/20000000000000000`, approximately `0.00177456`. Therefore this inventory cap fails before construction. Smaller packet capacities cannot select more windows.

The calculation does not show that any selected triple has a realizable rank-three endpoint. It only shows that this bounded inventory cannot pass the declared screen even if every selected replacement works perfectly.

## Scope and source pins

Assignment seed: `4c02737e0fc701ea05e30cbadaa396a9`; complex-mechanisms / `complex-new-helper-inventory`; priority revision 3. Base commit: `0b1cccf86e2f5132ed286a26ef0a681a495740ea`. Selected-record SHA256: `10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32`.

The selected replay archive SHA256 is `f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6`. The checked member is `candidate/strict/global/base/providers/gauge44/LOCAL-PROGRAMS.json.gz`, compressed SHA256 `241fde27d4e43f5a9cb6b128f9f76c5131a53d09f0371676163f914d0b0fef3a`. `SOURCES.json` pins the archive, selected source manifest, current ceiling engine, selected result, catalogue, and record. The data source and predecessor credits remain unchanged.

The 8-array late-output block optimum covers any finite scalar program within its declared contract. The present scope changes that contract by adding at most 15 scratch arrays. Nearby work in PR1836 studies two positive operand climbs at one ADD; Discussion #1167 comment 18920760 studies a batch on distinct destination registers; PR1814 studies distinct-destination C3 gather windows. The object here is a capacity-limited schedule of time-staggered same-register triples.

## Reproduce

From the repository root, Python 3.12 or later and the standard library:

```sh
python3 -B research/complex-staggered-scratch-screen-seed4c027/verify.py
python3 -B research/complex-staggered-scratch-screen-seed4c027/test_package.py
python3 scripts/research_package.py --package research/complex-staggered-scratch-screen-seed4c027 --check-only
```

Expected summary:

```text
PASS_STAGGERED_SCRATCH_SCREEN triples=369 K1=17 K3=51 K5=85 arrays5=15 ceiling5<=0.001713 gate=FAIL
```

The flow is integral min-cost flow on the interval time line: each candidate window is an edge of capacity one and cost minus one, each adjacent time edge has capacity `K`, and `K` units of flow select a maximum-cardinality feasible packet set. `test_package.py` exhaustively compares the solver to brute force on every subset of the six intervals over four time points for capacities one through three; it also checks inclusive endpoint collisions and paid-mass preservation.

The moment check reuses the pinned exact engine `research/complex-local-word-ceiling/ceiling.py`. Its `1e-6` rational grid bracket is already separated from the 5% gate by more than `6e-5`.

## Limits and handoff

The exact domain is the 369 triple windows formed by partitioning each selected `(phase, register)` rank-one climb stream into successive groups of three, with packet capacity `K=1,3,5`. The two orientations share the same climb itinerary. This is not a full temporal scheduler, a proof that a packet endpoint exists, or an impossibility theorem for more scratch arrays, different packet widths, or another profile. The experiment stopped because the best allowed zero-cost profile fails the repository card's 5% gate; charging scratch costs could only lower its ceiling.

No next experiment is justified within this seed and inventory cap: increasing the buffer count changes the bounded question and would need a new favorable screen before any construction work.

## Open next questions

No open question remains within the declared `K≤5` inventory: its favorable exact screen already fails the acceptance gate. A larger inventory is outside this seed's stopped domain and is not asserted to be impossible.

The claim and release are recorded at [Discussion #1163, comment 18923240](https://github.com/CrocSwap/integer-mult-bounds/discussions/1163#discussioncomment-18923240). No PR was justified. The local package is a reproducible handoff; maintainers can use its selected-interval hash and exact ceiling check if a separately motivated larger-inventory construction is proposed.

## Credit

Prepared by OpenAI Codex for Cinna Davis with substantial autonomous assistance in task triage, exact interval optimization, implementation, verification, and writing. No independent human review is claimed. New material is Apache-2.0.
