# Retained-array catch-up in the transport moment: the forced price and the #1166 INIT64 + d_A decision

**Research note: a scoped lemma and a conditional negative result. No new κ, no supplier, and the
selected frontier is unchanged.**

Base commit `de880ca1fa4540472ee8461d400914a60fc9dd41`. Every pinned input has the same git blob on
main `304c32e6f11a1b024012ae6a61b155bfe13142ce` (checked through the GitHub API on 2026-10-16).

- **Stakes.** [#1166 c18956869](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-18956869)
  (Philippe Van Velzen) asks how to price an array that is retained across calls but read by none
  of them. The answer decides his INIT64 + d_A final-record route:
  - under storage pricing (S) his price gate reports a complex κ ceiling of 0.00228, or 0.00221
    with PR2468-style read invoices. We reproduce the 0.00228 value exactly; the 0.00221 value is
    quoted. The bit endpoint (0.0017334) caps either in practice;
  - under centre-like pricing (C) it has no saving.
- **Result.** The answer holds in PR1664's scalar common-frame transport moment.
  - Holding an array costs nothing.
  - The consumer must bring the record to a common frame with its partners. That costs **8
    coordinates per level the source pair advances, for each record row that is independent of
    the rows the consumer's contract lets it combine** (Corollary 4).
  - For the stated contract this is (C)'s mass, up to a one-call lifetime off-by-one.
  - INIT64 + d_A costs **3,648 units per replica** with the stated end-of-replica decoder.
  - Decoding each bank as soon as its observed field is final still costs at least **2,496**.
  - A relaxation that lower-bounds every current-frame timing gives **1,344**.
  - The all-initial variant costs 3,456, 2,304 and 1,152 under the same three timings.
  - All are at least the exact **896-unit no-saving threshold**, so the (S) escape closes in this
    model.
- **Premises.** The rejection is conditional on the following, each defined under
  [Premises](#premises):
  - the stated observation contract (P_obs);
  - P_rank, which has finite-model evidence only, with uncompressed delivery as published;
  - P4: no slack in the inherited words;
  - current-frame consumers.

  Physical storage stays **UNKNOWN**. It can only add cost.
- **Without P_rank.** philippeVV's Theorem B still rejects the route when every bank decodes at
  one level. At earlier timings, where banks decode at different levels, it needs an extra
  own-bank premise.

The two conventions Philippe Van Velzen offered are:

- **(S):** 1 paid unit per array-call.
- **(C):** one rank-8 copy plus 8 units per array-call.

**Terms used below.**

- **The law** means Corollary 4.
- **Idle-priced:** extra mass packed as ideal rank-51 idle children.
- **Rank-8-priced:** extra mass as rank-8 children, which is (C)'s shape.
- **Units** are paid coordinates per replica.
- **Data incidence:** a later local call of the record's own pair.

## Statement

[PROOF.md](PROOF.md) gives the statements and proofs.

- Items 1 and 2 are theorems of the scalar common-frame transport model of
  [PR1664](../dirty-host-cutrank-audit/PROOF.md).
- Item 3 also uses Fact T (the pinned template) and P4.
- Item 4's statements about the #1166 records also use P_obs and P_rank.

1. **Storage is free in the moment (Lemma 2).**
   - Holding an array at a fixed frame for any number of calls adds no paid mass.
   - So (S) is not a consequence of the moment. Physical storage is a separate premise, and it
     remains **UNKNOWN**.
2. **Catch-up is charged exactly (Proposition 3).**
   - Take records R at height h_r and partners P at height h_p, with R ∩ P = 0.
   - Delivering O ⊆ R ⊕ P at the consumer height h_c costs exactly
     `min_L ρ_r|L−h_r| + ρ_p|L−h_p| + ρ_o|L−h_c|`.
   - ρ_r is what only the records supply, ρ_p is what only the partners supply, and ρ_o = dim O.
     Each rank is taken modulo the rows the consumer may combine.
   - The minimum is attained at the median level, and it equals the sum of the
     [PR1664](../dirty-host-cutrank-audit/PROOF.md) cut deficits. So the record may climb or the
     partners may descend; the bound covers both.
   - The consumer level is an explicit premise.
3. **Eight coordinates per level in the selected template (Fact T and Corollary 4, under P4).**
   - The pinned #1094 template moves every pair through nine levels of eight coordinates each.
   - A level is advanced either by the pair's own call or by an idle sweep.
   - Between two level-boundary instants, a record consumed at its pair's current frame pays
     **8 × ρ_r × (levels advanced)**. That is at least 8 ρ_r per later data incidence.
   - Hosted residuals put some idle families between declared levels at other instants. Every
     instant used below is checked to lie on a level boundary, in all 16 replicas.
4. **How the law compares with (S) and (C) (Proposition 5).**
   - (C) is a special case: ρ_r equals the number of rows and the pair advances one level per
     call. Under P_obs and P_rank every route (a) record satisfies this, so the (C) verdicts for
     route (a) are derived here rather than assumed.
   - (S) is not a moment price. As a stand-in for catch-up it under-prices current-frame
     consumers by 8×. PR2540 costs 16 under (S), but the law forces 128 under PR2511's ρ = 16,
     and PR2540 attains it.
   - The law counts levels advanced by the source pair, not calls. In replica 0 (and in 12 of
     the 16 replicas), pair 3's Y streams are untouched across six calls. A record of them costs 0
     under the law whatever ρ_r is, against 48 under (C) and 6 under (S). That record merely copies
     an untouched stream, so the example only shows which variable the law counts.

An earlier draft's "48 against (C)'s 24" lagging-pair example was withdrawn in review: its record
duplicates a row the contract observes, so the law charges 0 (PROOF.md §6(c); `verify.py` checks
the schedule fact).

## Priced decisions

Each row uses the pinned [`ceiling.py`](../complex-local-word-ceiling/ceiling.py) with
C = 0 and a free controller. Route (a) has three consumer timings, defined under
[Premises](#premises): P_final (stated), P_Y (earliest the observed fields allow) and P_early (a
relaxation).

| Route | Law (units/replica) | Verdict |
|---|---:|---|
| (a) INIT64 + d_A final-record contract, stated end-of-replica decoder (P_final) | **3,648** | **Rejected** in the stated model. Anything ≥ 896 leaves no positive saving, and any non-negative storage price only adds. |
| (a) the same, each bank decoded as soon as its observed field Y_(k,U) is final (P_Y) | ≥ **2,496** | Also ≥ 896. A lower bound for every timing P_obs admits. |
| (a) the same, early relaxation (P_early) | ≥ **1,344** = 8 per later data incidence | Also ≥ 896. A lower bound for every current-frame timing. |
| (a) all-initial variant (#2074 c18950926: d_A swapped for reads of the initial X_(1..3,U)) | 3,456 (P_final) / ≥ 2,304 (P_Y) / ≥ 1,152 (P_early) | Also ≥ 896. Its reads cost 0 at P_early, so INIT64's catch-up is the binding term. |
| (a) d_A records alone (P_final) | 960 | Also ≥ 896. |
| (a) Theorem B in place of P_rank, one consumer level (P_final) | 1,952 (original) / 1,824 (all-initial) | Also ≥ 896: **rejected without P_rank**. |
| (a) Theorem B in place of P_rank, with the own-bank premise | 1,344 / 1,216 (P_Y); 800 / 608 (P_early) | P_Y: ≥ 896. P_early: the best case, 608, caps κ at 0.0015234 idle-priced (0.0015144 rank-8-priced), below the selected 0.001672660197076918. |
| (a) Theorem B's count alone at P_Y / P_early | deliveries that meet the count (if the captures are independent) cost 608 / 544 (P_Y) and 112 / 0 (P_early) | **Not decided** by the count alone: the caps at 544, 112 and 0 exceed the selected κ. |
| (b) gap-1 shared-source centre sharing (the f0→f2 class) | ≥ 64 per shared set, equal to the 64 saved | **No moment gain** under the stated premises, by catch-up alone. The f0→f2 information question remains **open** (PR2199 open question 2). #2391/#2461 cover only the adjacent f0→b1 class. |
| (c) QQ16 retained caller #2540/#2651, retention row | exactly 128 = its 16 H8 | **Clarification only:** one charge, not two. It is proved under ρ = 16 with an F_U1 consumer, and PR2540 attains it. The moment comparison with zero-retention #2707 is #2707's own result: it wins for 0 ≤ a ≤ 1/16, because 8^15 > 7^16. It is now incorporated and reviewed. Storage is UNKNOWN. |

### Premises

The route (a) rows depend on these premises; PROOF.md §7.2 states each one.

- **P_obs (observation contract).**
  - The consumer may combine only:
    - the contract observations (final selected fields, final completed-X fields Y_(k,U), the
      forward histories);
    - the stated records and reads, at their stated capture times.
  - Other endpoint rows, such as the former-Y ordinary endpoints, and transient stream contents
    are excluded by the contract. This exclusion is a premise of the QQ16 observation contract
    (qq16-final-record-obstruction §1), not a consequence of the transport moment.
  - Without P_obs a record row may lie in the span of level-8 endpoint rows, which the moment
    lets the consumer combine for free. The obstruction's kernel family is visible exactly
    there.
- **P_rank.**
  - The stated arrays below each cut are independent modulo everything P_obs allows above it.
  - The contract delivers each needed array uncompressed to the decoder that uses it, as the
    published contract does ("Every retained array stays live until the final decode"). Lemma 1
    counts ranks, so compression before the climb would be a different contract.
  - The evidence is philippeVV's finite-model census and derived decoders. It is not a proof on
    the actual cover.
- **Capture times.** As stated in the price gate: INIT just before each bank's first call, and
  d_A right after its backward call.
  - Local calls overwrite X_U, and no bridge writes X_(k,U) before bank k's first call. So the
    stated INIT capture is the latest one that needs no other read.
- **Consumer timing.** Current-frame consumers.
  - **P_final** is the stated contract: every bank decodes at the end, level 8.
  - **P_Y** decodes bank k as soon as its observed field Y_(k,U) = −final X_(k,U) is final.
    X_(k,U) is last written at event 6 for bank 0 (level 2) and by bridges 27, 26 and 25 for
    banks 1–3, which run at level 8. Other observations can only delay a decoder, so P_Y is a
    lower bound for every timing P_obs admits.
  - **P_early** decodes each bank right after its last local call (levels 2, 4, 6, 8). For banks
    1 and 2 it ignores the last-write constraint, so P_obs does not allow it. It is kept as a
    relaxation: catch-up only grows with the consumer level, so P_early lower-bounds every
    current-frame timing. It also assumes, in the route's favour, that the decoded fields ride
    the inherited idle sweep for free.
  - A consumer whose outputs must return to the bank's frame is covered automatically.
- **P4.** The inherited words have no slack, as the coverage identity 72W + 64N indicates.
- **ρ = 16 for PR2540.** This is PR2511's interface bound.
- **Own-bank premise** (the Theorem B rows at P_Y and P_early only). Each bank's rows come only
  from the captures its derived decoder uses, independent modulo everything else that decoder may
  combine; the 62 rows split freely over the banks. It is ours, not part of Theorem B.
- **Equal levels share a frame (P_glob).** Every bridge in the schedule joins two pairs at equal
  levels. P_glob is used only to show that some costs are 0 and that the count-only deliveries
  are attained. No lower bound, and so no rejection, depends on it.

### Comparison with the published conventions

- (C) as published charges 8 × 464 = 3,712.
- The law equals (C) with uniform lifetimes, 8 × 456 = 3,648.
- The price gate counts bank 0's d_A as live for 8 calls. Under the convention it uses for INIT,
  the count is 7. No verdict changes.
- The (S)-priced 464 array-calls reproduce PRICE-GATE.json's storage ceiling
  2285992139/1002285992139 (0.0022808 idle-priced) exactly.

### Break-even catch-up mass

Break-even catch-up mass per replica, below which a route still gains:

| Comparison point | κ | Idle-priced | Rank-8-priced |
|---|---:|---:|---:|
| Selected record (#1094) | 0.001672660197076918 | 579 | 576 |
| PR2474 (pending) | 0.001703676387993676 | 573 | 568 |
| #2843 (pending) | 0.00171865827784172 | 570 | 568 |
| #2848 (pending) | 0.00171865850830493 | 570 | 568 |
| #2857 (pending; opened after the base) | 0.00172009662868483 | 570 | 568 |
| PR589 bit endpoint | 0.001733427039589844 | 568 | 560 |

- The pending rows reflect open PRs at review time.
- Break-even mass does not increase with κ, and `verify.py` checks this across the table. So any
  claim between the selected record and the bit endpoint, such as #2853 or #2856, has its
  break-even in [568, 579] idle-priced or [560, 576] rank-8-priced.
- **No-saving threshold: 896** units per replica, one unpaid coordinate for each of the 896
  families. It is exact; PROOF.md §7.2 gives the proof.
  - Our PR2470 found the same threshold under the assumed centre-like convention: its C = 0 limit
    of 111 coordinate-calls with any positive saving is 888 units, and 896 = 8 × 112.
    `verify.py` checks the pinned row against it.

## What is new

- **The price, derived.** Philippe Van Velzen's price gate and the #1166 request assume (S) or
  (C). This package derives which price the transport moment actually forces, and states the
  observation premise it needs. It reprices both published variants of the #1166 route at three
  consumer timings.
- **Theorem B's reach, made explicit.** Its global count of 62 rejects the route without P_rank
  when every bank decodes at one level. At multi-level timings the count alone does not decide.
- **Controls of a single law.** PR2540, PR2197 and PR2678 each pay one concrete frame charge.
  They are reproduced here as controls of the law. The F_L → F_U1 upgrades in PR2492/PR2512 are
  the same one-level climb, but they are not recomputed separately.
- **Earlier treatments.**
  - PR2480 counts information only.
  - The [centre-sharing overhead budget](../centre-sharing-overhead-budget/README.md) treats ΔH
    abstractly.
  - Our PR2470 ([qq16-cut-retention-census](../qq16-cut-retention-census/README.md)) priced
    PR2443's retained copies under an assumed centre-like convention. Corollary 4 now derives
    that convention for current-frame consumers under P4. PR2470 also noted that reading the
    whole post-B1 state needs no copy, which is the endpoint-read lever below.
- **Precursor.** Philippe Van Velzen's sibling-helpers note says, for helper time-sharing, "the
  bill is coordinate advances, not storage".
  - It lives at `philippeVV/integer-mult-bounds@b5ce9d223feeed73d07e2a07321f7a025bd5865e`,
    `research/complex-budget-law/closures-2/sibling-helpers/README.md`.
  - Its author marks it LOCAL-ONLY. It is concurrent with this package and is credited as a
    precursor.

## Reproduce

Run from the repository root. Only the standard library is needed. Local runs used CPython 3.14.4;
the registered replay in [VERIFY.json](VERIFY.json) uses Python 3.12, which was not available
locally.

```sh
python3 -I -B research/retained-array-catch-up/verify.py              # ~40 s
python3 -I -B research/retained-array-catch-up/independent_check.py   # ~2 s
python3 scripts/research_package.py --package research/retained-array-catch-up --check-only
```

Expected output:

```text
PASS_RETAINED_ARRAY_CATCH_UP pr2540=128 init64_dA=3648/2496/1344 all_initial=3456/2304/1152 dA_only=960 thmB_one_level=1952/1824 thmB_own_bank=1344/1216/800/608 thmB_count_only=608/544/112/0 array_calls=464/456 no_saving=896 breakeven_S=573 breakeven_C=71 zero_advance_calls=6 hosted_instants=21 frame_instances=34454/4044 negative_controls=16 no_new_kappa
PASS_RETAINED_ARRAY_CATCH_UP_INDEPENDENT pr2540=128 init64_dA=3648/2496/1344 all_initial=3456/2304/1152 dA_only=960 thmB_one_level=1952/1824 thmB_own_bank=1344/1216/800/608 thmB_count_only=608/544/112/0 zero_advance_calls=6 zero_advance_replicas=12/16 hosted_route_instants=21x16 breakeven_S=573 breakeven_C=71 no_saving=896 echelon_dijkstra_instances=2432 controls_rejected=2
```

How to read the tokens:

- `init64_dA` and `all_initial` are P_final / P_Y / P_early.
- `thmB_one_level` is original / all-initial at P_final.
- `thmB_own_bank` and `thmB_count_only` are original / all-initial at P_Y, then at P_early.

`verify.py --write` regenerates [RESULT.json](RESULT.json). It refuses to replace a differing
file unless `--force` is also given.

### What `verify.py` checks

1. **Source pins.** It checks:
   - 16 file pins and two archive-member pins;
   - 36 verbatim premise lines, including the bridge and terminal semantics, the observation
     list, the X_U updates of the local words, PR2199's open f0→f2 question and PR2470's
     centre-like limit.
2. **Level timeline.** It replays the selected template's level timeline.
   - The hosted and base schedules are equal.
   - The base idle children have rank 8 per level, and hosted residuals never exceed that.
   - Every bridge joins two pairs at equal levels.
   - X_(k,U) is last written at events 6, 27, 26 and 25, and bridges 25–27 run with every pair at
     level 8.
   - **Hosting, replica 0, both directions.** It uses 21 instants: the seven route captures, the
     four P_early consumers, the three all-initial reads with their consumers, and the four P_Y
     consumers.
     - No overshoot: every residual hosted on the pair by then belongs to a sweep that has already
       reached the stated level. That is 14,290 slot checks over 3,644 distinct residual slots,
       4,173 of them at the seven captures.
     - No undershoot: every residual of such a sweep has landed. That is 9,280 checks of slots
       that have not landed yet.
   - The window streams host nothing; pair 3's X streams host 160 residuals in that window.
3. **The law and routes.** It computes:
   - the controls: PR2540 128, PR2197 144, PR2678 1,792 and 3,696, centre path 576;
   - both variants of route (a) at P_final, P_Y and P_early;
   - the Theorem B floors: the one-level cut sum, the own-bank floor and the count-only delivery
     at each timing;
   - the forward-history add-on;
   - the withdrawn example's schedule fact.
4. **Pricing.** With the pinned `ceiling.py` it checks:
   - the 896 threshold, which agrees with PR2470's centre-like limit of 111 coordinate-calls;
   - the #1166 break-evens 573 and 71, and the PRICE-GATE.json storage ceiling;
   - the comparison table, including that break-even mass does not increase with κ;
   - which route rows have no saving, which stay below the selected κ, and that the count-only
     deliveries at 544, 112 and 0 stay above it.
5. **Frame model.** A breadth-first minimum is compared with Lemma 1 and the meeting formula.
   - There are 34,454 record/partner instances, and in all of them opt = Σ deficits = min_L f.
     They cover GF(2)² with 4 levels (2,432), GF(3)² with 3 levels (2,106) and GF(2)³ with 3
     levels (29,916), each domain complete.
   - On 4,044 general instances the bound is sound, and it is tight on 3,999. PROOF.md §2 gives
     the smallest non-tight case.
6. **Tensor toy.** A two-call rational toy runs 25 trials.
   - Adding a record without catch-up gives a wrong output every time.
   - The paid catch-up, or a partner descent, repairs it.

### Negative controls that must fail

There are 16 in total. Each of the 13 explicit ones must fail with its stated message, and
`verify.py` asserts the message:

- a mutated idle `to_level`;
- PR2540 priced with 15 rows (120), or with two incidences (256);
- INIT bank 1 captured at level −1 (4,032);
- the window extended past the first touch of pair 3 (48);
- the window stretched into pair-3 Y hosting;
- a pair-1 residual of sweep 2 delayed to time 25 (undershoot);
- 464 array-calls under uniform lifetimes (456);
- a positive saving claimed to vanish at 895;
- a break-even at 574;
- the all-initial read barred from bank 0's consumer level (1,216);
- bridge 27 reversed so that it writes X_(0,U) (last write 27);
- Theorem B at P_early without the own-bank premise (112, not 800).

The other three are an upward-only cut bound, which fails on 14,426 instances, and, in the tensor
toy, omitted catch-up and catch-up on the wrong axis.

### What `independent_check.py` does differently

It shares no code with `verify.py` and does not import `ceiling.py`. The independence lies in the
representation and the algorithms. Its base template is a byte-identical copy (same sha256) of the
same member, read from the PR2346-pinned #1042 archive.

- **Coordinate sets.** Frames are explicit coordinate sets built from idle child **ranks**. The
  declared level fields are only cross-checked. It recomputes every route value at all three
  timings, and the last writes of X_(k,U).
- **Theorem B by enumeration.** It enumerates every split of the 62 rows over the banks for the
  own-bank floor, takes nearest-consumer deliveries for the count-only value, and runs a direct
  cut loop for the one-level sum.
- **Per-family hosted heights, all 16 replicas.** It replays the hosted template family by family:
  local call +8, idle child +remaining rank, pooled slot +width at its own time.
  - It does this under both conventions for equal times.
  - It requires one uniform height on all 224 families of the pair at the 21 route instants, in
    every replica.
  - It finds that the zero-advance window holds in exactly 12 replicas, all except 4, 5, 6 and 11.
- **Different arithmetic.** It evaluates moments with `decimal` at 80 digits, and checks the 896
  threshold with exact rationals.
- **Different solver.** It runs Dijkstra over reduced echelon bases on 2,432 instances, plus two
  controls. Each control must be rejected for its stated reason, and the count is enforced.

## Scope, inherited assumptions and UNKNOWN obligations

- **Physical storage, tape movement and hosting windows** for retained arrays lie outside the
  moment and stay UNKNOWN.
- **Endpoint reads.** Any read of an endpoint row at the consumer frame pays no catch-up in the
  moment. Its price is a question for the read and observation contract, outside the moment.
- **Premises.** P_obs, P_rank, the capture times, the consumer timing, P4 and PR2540's ρ = 16 are
  all premises. PROOF.md §8 lists them.
- **Theorem B.** It is a posted claim of #2074 that has not been reviewed. Our per-cut
  application of it is written out in PROOF.md §7.2. Alone it rejects only at P_final; the
  own-bank premise it needs at P_Y and P_early is ours.
- **Forward histories.** The derived decoders use f2, f4 and f6, which are not in the 464
  array-calls.
  - If each is retained as one 8-row array, captured at its forward call's output or input
    level, the law adds 768–960 under P_final, or 0–192 under P_early.
  - These only add, so the rejection does not depend on them.
- **Frames.** Only nested frames are modelled. Gauge terms, such as PR2678's signed-line 1,904
  row, are quoted rather than derived.
- **Prices.** They are ideal-packing ceilings, not attained exponents.
- **Finite checks.** These cover the stated domains only. The general statements are the
  written proofs, which no human or formal kernel has checked.

## Open next questions

The same questions appear, structured, in [TASK.json](TASK.json).

1. **Can the INIT information be captured late or read at the consumer frame?**
   - *Why it matters.* INIT64's catch-up is the binding term of both variants: 1,920 at P_Y and
     1,152 at the P_early relaxation. A gain needs the catch-up-weighted retention under about
     570 units per replica.
   - *First step.* Per bank, find the latest cut at which the initial query information can
     still be rebuilt from rows a contract may read. Then price that read with the law, and
     separately as a read contract.
   - *Blocked by.* No priced observation contract for endpoint or ordinary reads, and no
     actual-cover proof of P_rank.
2. **Does the forward-history retention make any QQ16 decoder worse?**
   - *First step.* Determine whether f2, f4 and f6 are kept in data ports or in separate arrays,
     then apply the law.
3. **What does physical storage cost?** This is the UNKNOWN that the moment cannot settle.
   - *First step.* Bind one caller's 16 early arrays (#2651) to concrete streams and tape
     positions across B1. Price that against #2707's surplus of 192 wrappers, 256 maps and 8,368
     scalars.
4. **Where do the F_U1 outputs go?** Name the consumer, and its frame, for the 224 F_U1 outputs
   of #2540/#2707. Proposition 3 needs this premise. Handoff thread: #2657.
5. **A per-record-class schedule search.** Can idle sweeps be re-timed so that records sit in
   zero-advance windows?
   - PR1012 shows that restoration deferral is mass-neutral, so this is a real question.
   - It was not attempted in this session.

## Credit

The full list is in PROOF.md §9.

- **The model, the lemma and the lineage.** Andrey Mas (an664, PR1664), ctoth (#1516, #1587),
  PR1012, and the idle-axis-hosting / #434 lineage.
- **The native frames, interfaces and tariffs.**
  - ywz65: PR2511, the source of ρ = 16; PR2540; #2707; #2461.
  - Arham Tahir: PR2681, the zero-retention lineage that #2707 refines.
  - petalas (PR2678) and 1337isnot1337 (PR2197).
- **The conventions, census, price gate, decoders and Theorem B.** Philippe Van Velzen.
- **The information results.** navinor (#2391), ywz65 (#2461) and our PR2199.
- **The earlier retention screen.** Our PR2470.
- **Others.**
  - Ross Richardson (PR2480);
  - alephnan (PR2346);
  - commdata2338 (PR2174, PR2651);
  - Ali Romman's QQ16 lineage;
  - the maintainers' combined review of #2707.

### External sources, read as data

These were read as data and never executed. Their pinned numbers are reproduced independently
here.

- `philippeVV/integer-mult-bounds@9fcd3d899cc5bad2e27ab1d3d64d241cbfe30793`,
  `research/joint-query-first-pair-catalogue/final-record/`:
  - `price_gate.py`, sha256 `d4c2c077…cb39`;
  - `PRICE-GATE.json`, sha256 `78eed8a0…53d0`;
  - `README.md`.
- Discussion posts: #2074 c18940190 (Theorem B, fork `680d0997621a2cecfef2186ab143377658687825`),
  c18950410 and c18950926 (the decoders and the all-initial variant).

[SOURCES.json](SOURCES.json) records the full hashes.

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5).
Review so far consists of AI review passes in the same automated loop. There has been no human or
formal-kernel review. Apache-2.0.
