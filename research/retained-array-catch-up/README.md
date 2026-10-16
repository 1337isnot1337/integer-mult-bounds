# Retained-array catch-up: what a retained array costs per call in the transport moment

**Audit: a scoped interface lemma and a priced decision. No new κ, no supplier, and the
selected frontier is unchanged.**

This package answers [#1166 c18956869](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-18956869)
from Philippe Van Velzen. The question is how to price an array that is retained across calls
but read by none of them. He offered two conventions:

- **(S):** 1 paid unit per array-call.
- **(C):** one rank-8 copy plus 8 units per array-call.

## Statement

All of the following hold in the scalar common-frame transport model of
[PR1664](../dirty-host-cutrank-audit/PROOF.md). [PROOF.md](PROOF.md) gives the statements and
proofs.

1. **Storage is free in the moment (Lemma 2).** Holding an array at a fixed frame for any
   number of calls adds no paid mass. So (S) is not a consequence of the moment. Physical
   storage is a separate premise, and it remains **UNKNOWN**.
2. **Catch-up is charged exactly (Proposition 3).** Take records R at height h_r and
   partners P at height h_p, with R ∩ P = 0. To deliver O ⊆ R ⊕ P at the consumer height
   h_c, the minimum paid mass is
   `min_L ρ_r|L−h_r| + ρ_p|L−h_p| + ρ_o|L−h_c|`:
   - ρ_r is what only the records supply, ρ_p is what only the partners supply, and ρ_o = dim O;
   - the minimum is attained at the median level, and it equals the sum of the
     [PR1664](../dirty-host-cutrank-audit/PROOF.md) cut deficits;
   - so the bound covers both directions: the record climbs, or the partners descend. The
     consumer level is an explicit premise.
3. **Eight coordinates per level in the selected template (Fact T and Corollary 4).** The
   pinned #1094 template moves every pair through nine levels of eight coordinates each. A
   level is advanced either by the pair's own call or by an idle sweep. A record consumed at
   its source family's current frame therefore pays **8 × (levels advanced) per independent
   row**. That is at least 8 per later data incidence.
4. **The law matches neither convention in general (Proposition 5).**
   - It equals (C)'s mass when the family advances one level per call of the lifetime.
   - It is **0** for a record of a pair-3 Y stream held across six calls, before anything acts
     on that stream; no residual is hosted there either. (S) charges 6 and (C) charges 48 for
     that record.
   - It exceeds (C) for a record of a deferred family: 48 against 24 for a pair-0 X stream
     captured after stage 5.
   - (S) under-prices current-frame consumers by 8×. For example, PR2540 costs 16 under (S),
     but the law forces 128, and PR2540 attains it.

## Priced decisions

Each row uses the pinned [`ceiling.py`](../complex-local-word-ceiling/ceiling.py) with
C = 0 and a free controller, unless stated otherwise.

| Route | Law (units/replica) | Verdict |
|---|---:|---|
| (a) INIT64 + d_A final-record contract (fork `9fcd3d89`), under P_final and P_rank | **3,648** | **Rejected** in the stated model. ≥ 896 leaves no positive saving at all, under either convention. |
| (a) d_A records alone | 960 | Also ≥ 896. |
| (a) cheapest 62 of the 88 stated captures (#2074 Theorem B lower bound) | 1,952 | Also ≥ 896. |
| (b) gap-1 shared-source centre sharing (the f0→f2 class) | ≥ 64 per shared set, equal to the 64 saved | **Rejected** for two independent reasons. First, the prior information obstructions: PR2199 rank 16, plus #2391/#2461 for the adjacent class. Second, catch-up across B1. |
| (c) QQ16 retained caller #2540/#2651, retention row | exactly 128 = its 16 H8 | One charge, not two; it is proved under ρ = 16 and attained. In the moment it is dominated by zero-retention #2707 (pending; author-reported invoice): 112 − 16·8^(1−a) < 0. Storage is UNKNOWN. **Narrow** further retention work. |

The routes depend on these premises:

- **P_final.** The decoded inputs are consumed at the final frame.
- **P_rank.** Each stated array is rank-necessary at the cuts it crosses. The support is
  finite-model evidence, not a proof on the actual cover.
- **ρ = 16 for PR2540.** This is PR2511's interface bound.
- **P4.** The inherited words have no slack, as the coverage identity 72W + 64N indicates.

The two published conventions compare with the law as follows:

- (C) as published charges 8 × 464 = 3,712.
- The law equals (C) with uniform lifetimes, 8 × 456 = 3,648. The price gate counts bank 0's
  d_A as live for 8 calls. Under the convention it uses for INIT, the count is 7. No verdict
  changes.

Break-even catch-up mass per replica, below which the route still gains:

| Comparison point | κ | Idle-priced | Rank-8-priced |
|---|---:|---:|---:|
| Selected record | 0.001672660197076918 | 579 | 576 |
| PR2474 (pending) | 0.001703676387993676 | 573 | 568 |
| #2843 / #2848 (pending) | 0.00171865827784172 / …850830493 | 570 | 568 |
| PR589 bit endpoint | 0.001733427039589844 | 568 | 560 |

No-saving threshold: **896** units per replica (one unpaid coordinate for each of the 896
families). This is exact; see the proof in PROOF.md §7.2.

## What is new

- **Philippe Van Velzen's price gate and #1166 request** assume (S) or (C). This package
  derives which price the transport model actually forces, and reprices both #1166 routes.
- **PR2540, PR2197 and PR2678** each pay one concrete frame charge. They are reproduced here as
  controls of a single law. The F_L → F_U1 upgrades in PR2492/PR2512 are the same one-level
  climb, but they are not recomputed separately.
- **PR2480** counts information only. The [centre-sharing overhead budget](../centre-sharing-overhead-budget/README.md)
  treats ΔH abstractly.
- **Precursor.** Philippe Van Velzen's sibling-helpers note says, for helper time-sharing,
  "the bill is coordinate advances, not storage". The note is at fork `b5ce9d22`,
  `research/complex-budget-law/closures-2/sibling-helpers`, and its author marks it LOCAL-ONLY.
  It is concurrent with this package and credited as a precursor.

## Reproduce

Run from the repository root; only the standard library is needed. Local runs used CPython
3.14.4. The registered replay in [VERIFY.json](VERIFY.json) uses Python 3.12.

```sh
python3 -I -B research/retained-array-catch-up/verify.py              # ~20 s
python3 -I -B research/retained-array-catch-up/independent_check.py   # ~1 s
python3 scripts/research_package.py --package research/retained-array-catch-up --check-only
```

Expected output:

```text
PASS_RETAINED_ARRAY_CATCH_UP pr2540=128 init64_dA=3648 dA_only=960 cheapest62=1952 array_calls=464/456 no_saving=896 breakeven_S=573 breakeven_C=71 zero_witness_calls=6 frame_instances=10748/4044 negative_controls=12 no_new_kappa
PASS_RETAINED_ARRAY_CATCH_UP_INDEPENDENT pr2540=128 init64_dA=3648 dA_only=960 cheapest62=1952 zero_witness_calls=6 breakeven_S=573 breakeven_C=71 no_saving=896 echelon_dijkstra_instances=2432 controls_rejected=2
```

`verify.py --write` regenerates [RESULT.json](RESULT.json). It refuses to replace a differing
file unless `--force` is also given.

### What `verify.py` checks

1. **Source pins.** 14 source pins, two archive-member pins and 24 verbatim premise lines.
2. **Level timeline.** It replays the selected template's level timeline. The hosted and base
   schedules are equal; the base idle children have rank 8 per level; hosted residuals never
   exceed that. It also checks the hosting side conditions:
   - 4,173 residuals hosted before a route capture all belong to levels already reached;
   - the witness streams host nothing in the window;
   - pair 3's X streams host 160 residuals in that window.
3. **The law and routes.** It computes the law, the controls (PR2540 128, PR2197 144, PR2678
   1,792/3,696, centre path 576) and the routes.
4. **Pricing.** With the pinned `ceiling.py` it checks the 896 threshold, reproduces the #1166
   break-evens 573 and 71, and computes the targets above.
5. **Frame model.** A breadth-first minimum is compared with Lemma 1 and the meeting formula:
   - 10,748 record/partner instances where opt = Σ deficits = min_L f. GF(2)² and GF(3)² are
     complete; GF(2)³ uses 24 sampled (R, P) pairs from `random.Random(59)`.
   - 4,044 general instances where the bound is sound. The bound is tight on 3,999 of them;
     PROOF.md §2 gives the smallest non-tight case.
6. **Tensor toy.** A two-call rational toy runs 25 trials. Adding a record without catch-up
   gives a wrong output every time. The paid catch-up, or a partner descent, repairs it.

### Negative controls that must fail

There are 12 in total.

- A mutated idle `to_level`.
- PR2540 priced with 15 rows, or with two incidences.
- INIT bank 1 captured at level −1.
- The zero-witness window extended past the first touch of pair 3.
- The witness window stretched into pair-3 Y hosting.
- 464 array-calls under uniform lifetimes.
- A positive saving claimed to vanish at 895.
- A break-even at 574.
- An upward-only cut bound.
- Omitted catch-up, and catch-up on the wrong axis, in the tensor toy.

### What `independent_check.py` does differently

It shares no code with `verify.py` and does not import `ceiling.py`.

- **Different source and representation.** It uses the base template from the PR2346-pinned
  #1042 archive. Frames are explicit coordinate sets, built from idle child **ranks**; the
  declared level fields are only cross-checked.
- **Different arithmetic.** It evaluates moments with `decimal` at 80 digits, and checks the
  896 threshold with exact rationals.
- **Different solver.** It runs Dijkstra over reduced echelon bases on 2,432 instances, plus
  two rejecting controls.
- **Witness re-check.** It re-checks the hosted-template witness window by first-touch times.

## Scope, inherited assumptions and UNKNOWN obligations

- **Physical storage, tape movement and hosting windows** for retained arrays lie outside the
  moment and stay UNKNOWN.
- **P_final, P_rank, PR2540's ρ = 16, and P4** are premises. P4 says the inherited words have
  no slack, as the coverage identity indicates. PROOF.md §8 lists them all.
- **Forward histories.** Philippe Van Velzen's derived decoders use the forward histories f2,
  f4 and f6. They are not in the 464 array-calls. If they are retained separately, they add at
  most 768. The rejection does not depend on them.
- **Frames.** Only nested frames are modelled. Gauge terms, such as PR2678's signed-line 1,904
  row, are quoted rather than derived.
- **Prices.** They are ideal-packing ceilings, not attained exponents.
- **Finite checks.** These cover the stated domains only. The general statements are the
  written proofs, which no human or formal kernel has checked.

## Open next questions

The same questions appear, structured, in [TASK.json](TASK.json).

1. **Is there a final-record contract with late captures?**
   - *Why it matters.* The law limits the information captured per replica: its
     catch-up-weighted sum must stay below about 570 units. Roughly, 62 arrays must be captured
     within one level of their consumer.
   - *First step.* Find, per bank, the latest cut at which the lost information is still
     readable.
   - *Blocked by.* No actual-cover witness of when each bank's information is destroyed.
2. **Does the forward-history retention make any QQ16 decoder worse?**
   - *First step.* Price f2, f4 and f6 with Corollary 4 for #2540-style and final-record callers.
3. **What does physical storage cost?** This is the UNKNOWN that the moment cannot settle.
   - *First step.* Bind one caller's 16 early arrays (#2651) to concrete streams and tape
     positions across B1, and price that against #2707's surplus of 192 wrappers, 256 maps and
     8,368 scalars.
4. **Candidate 3: where does F_U1 output go?** Name the consumer, and its frame, for the 224
   F_U1 outputs of #2540/#2707. Proposition 3 needs this premise. Handoff thread: #2657.
5. **A per-record-class schedule search.** Can idle sweeps be re-timed so that records sit in
   zero-catch-up windows? PR1012 shows restoration deferral is mass-neutral, so this is a real
   question. It was dropped from this session and is not attempted.

## Credit

The full list is in PROOF.md §9.

- **The model, the lemma and the lineage.** an664 (PR1664) and ctoth (#1516, #1587), PR1012,
  and the idle-axis-hosting / #434 lineage.
- **The native frames and tariffs.** ywz65 (PR2540, PR2707, #2461), petalas (PR2678) and
  1337isnot1337 (PR2197).
- **The conventions and the census.** Philippe Van Velzen.
- **The information obstructions.** navinor (#2391) and our PR2199.
- **Others.** Ross Richardson (PR2480), alephnan (PR2346), commdata2338 (PR2174, PR2651) and
  Ali Romman's QQ16 lineage.

Fork data from `philippeVV/integer-mult-bounds@9fcd3d89` (`price_gate.py`, `PRICE-GATE.json`)
was read as data and never executed. Its numbers are reproduced independently here.

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5).
Apache-2.0.
