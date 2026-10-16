# Retained-array catch-up in the scalar common-frame transport model

This note answers [#1166 c18956869](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-18956869)
within one stated model. It proves no new κ and no supplier. Section 7 gives the priced
decisions. Section 8 lists every premise that is not proved here.

**The question.** An array is retained across calls but no call reads it. Philippe Van
Velzen proposed two per-call prices for it:

- **(S):** one paid unit per array per call.
- **(C):** one rank-8 copy plus 8 units per array per call.

Which price, if either, does the selected model use?

**The short answer.** Neither is a primitive of the transport moment.

- Holding an array at a fixed frame costs nothing in the moment (Lemma 2).
- The moment charges **catch-up** instead: the frame transport the consumer needs to combine
  the record with its partners. Its exact value for independent record and partner rows is a
  minimum over the meeting level, in both directions (Proposition 3).
- In the selected nine-stage template, every pair passes through nine levels of eight
  coordinates each. A level is advanced either by the pair's own call or by an idle sweep
  (Fact T). So a record consumed at its source family's current frame pays **8 × (levels
  advanced between capture and consumption)** per independent row (Corollary 4).

How the law compares with the two conventions:

| Situation | Law | (C) | (S) |
|---|---|---|---|
| Source family advances one level per call of the lifetime, consumer at the current frame | equals (C)'s mass | 8 per call | under-prices 8× |
| Record of a family that nothing touches during the lifetime (pair 3, six calls) | 0 | over-prices | over-prices |
| Record of a deferred family (pair 0 after stage 5) | 48 per array | 24 per array | — |

For the two #1166 routes with an end-of-replica decoder, the law agrees with (C), up to one
lifetime off-by-one. Their verdicts are therefore those that (C) gives, but here they are
derived rather than assumed. An earlier decoder lowers the INIT64 + d_A charge to 1,344 units
per replica, which is still above the 896-unit no-saving threshold.

## 1. Model and premises

**P1. The transport model.** This is the scalar common-frame transport model of
[PR1664](../dirty-host-cutrank-audit/PROOF.md) §4.1, and we use its rules 1–4 unchanged:

1. Scalar copy, add, scale and clear at a common frame are free.
2. A transport moves one register's logical row from frame A to frame B and costs at least
   |ν(A) − ν(B)|.
3. No uncharged cross-frame or multi-payload moves are allowed.
4. Any pre-existing side information belongs to the entry state.

Rows are vectors over a field K.

**P2. Nested chain.** The frames of one data family form a nested chain. Height means the
number of applied coordinates.

- PR1664's frame formula gives d(A, B) = dim A + dim B − 2 dim(A ∩ B), which is at least
  |dim A − dim B|. For nested frames the two are equal.
- The selected frames are nested. [PR2540](../qq16-complete-native-decoder/PROOF.md) §1 gives
  F_L = ∏_{j=0..8} C_(d e_j) (9 axes) and F_U1 with U1 = ⟨e0,…,e16⟩ (17 axes).
- A direct move from height a to height b costs at least |a − b|. That is the number of unit
  cuts it crosses, so unit moves lose nothing.

**P3. The region and its entry state are fixed.** Lower bounds hold for a stated region and
its complete entry configuration (PR1664 rule 4).

**P4. The inherited words have no slack.** Sometimes the region contains the unchanged
inherited calls: F0, B1, the idle sweeps and so on. Their transports are then taken to cross
each cut exactly as often as the rank of the rows they must deliver above it. Those rows are
their own data endpoints and restored hosts.

This is what the coverage identity says. Paid mass equals 72W + 64N exactly, so each family
crosses each of its 72 cuts once. PR1664 §5 shows the 64-per-call centre path is tight in this
model. So the extra mass of a region equals M minus the inherited mass, and is at least
Σ_j(δ_j⁺ + δ_j⁻) minus the inherited demand.

This premise blocks one escape. A record cannot ride an inherited crossing "for free" by
being added into an inherited register. The demanded endpoint row must still reach the top,
so one extra independent row must cross. A construction that exhibits real slack in an
inherited word would escape P4. It would have to show that slack explicitly.

**Fact T. Template levels.** These are read from the pinned selected #1094 hosted
`GLOBAL-TEMPLATE` (replica 0). Its 30-event schedule equals the base split-centres template's
schedule.

- **Pair binding.** The local calls at stages 0–8 use pairs 0,0,0,1,1,2,2,3,3. Even stages
  are forward calls; odd stages are backward calls.
- **Levels.** Each pair starts at level −1 and ends at level 8.
- **Local calls.** A local call at stage s moves its pair from level s−1 to level s. It applies
  the call's eight data coordinates.
  - The QQ16 frames show this directly: F0 outputs F_L (9 axes) and B1 outputs F_U1 (17 axes);
    see PR2540 §1.
  - It also agrees with the coverage partition 8·k_f + 1 + hosted_f + idle_f = 73
    (ctoth, #1587).
- **Idle sweeps.** An idle sweep moves an idle pair from its current level to `to_level`.
  - In the base template, its two children have rank 8 × (levels advanced).
  - The hosted template replaces part of an idle child by hosted helper residuals.
    [idle-axis-hosting](../idle-axis-hosting/PROOF.md) §2 shows that this leaves the product
    unchanged, so the frame after the sweep is unchanged.
  - A hosted residual acts at its helper's invocation time, inside the idle window. So part of
    an idle family's next block can be applied **before** its sweep. `verify.py` checks every
    one of the 4,173 residuals hosted on a route record's source pair before its capture: each
    belongs to a sweep that has already reached the capture level. The route capture levels
    below are therefore exact.

So one level is eight coordinates, and the nine levels are the 72 paid coordinates of each
family.

**Level timeline** (pairs 0–3, after each event):

| Event | Description | Pair levels |
|---|---|---|
| entry | — | −1 −1 −1 −1 |
| 0 | F0 | 0 −1 −1 −1 |
| 1 | B1 | 1 −1 −1 −1 |
| 2 | idle sweep, pair 1 | 1 1 −1 −1 |
| 4 | F2 | 2 1 −1 −1 |
| 5 | idle sweep, pair 1 | 2 2 −1 −1 |
| 7 | B3 | 2 3 −1 −1 |
| 8 | idle sweep, pair 2 | 2 3 3 −1 |
| 10 | F4 | 2 4 3 −1 |
| 11 | idle sweep, pair 2 | 2 4 4 −1 |
| 13 | B5 | 2 4 5 −1 |
| 14 | idle sweep, pair 3 | 2 4 5 5 |
| 16 | F6 | 2 4 6 5 |
| 17 | idle sweep, pair 3 | 2 4 6 6 |
| 19 | B7 | 2 4 6 7 |
| 20 | F8 | 2 4 6 8 |
| 21–23 | final idle sweeps, pairs 0–2 | 8 8 8 8 |

Bridges are omitted from the table; they do not change levels. `verify.py` reads this table
from the schedule. `independent_check.py` recomputes it from explicit coordinate sets, using
the idle child ranks and not the declared levels.

**Definitions.**

- An **entry configuration** is a finite list of (row, height) pairs.
- A **demand** is a finite list of (row, height) pairs that must each be held, at some time
  in the region, by a register at that height.
- For a cut j (between heights j−1 and j), let E_j⁺ and E_j⁻ be the spans of the entry rows
  at heights ≥ j and < j. Let D_j⁺ and D_j⁻ be the spans of the demanded rows on each side.
- The **deficits** are δ_j⁺ = dim(E_j⁺ + D_j⁺) − dim E_j⁺ and δ_j⁻ = dim(E_j⁻ + D_j⁻) − dim E_j⁻.

## 2. Lemma 1 (PR1664's cut-rank bound, for one nested chain)

Every program in P1–P3 that meets the demand has paid mass

M ≥ Σ_j (δ_j⁺ + δ_j⁻).

**Proof.** This is PR1664 (C-down), its symmetric (C-up), and (A), applied with Q_j equal to
the demanded rows on each side.

- Each high-to-low transport across cut j adds at most one direction to the retained span of
  low rows.
- Common-frame operations, upward moves and clears add none.
- A move between heights a and b crosses |a − b| cuts.

Summing over the cuts gives the bound. ∎

**The bound is not always attained.** The frame model in `verify.py` finds 45 non-tight cases
among 4,044 general instances. The smallest has the same row v at heights 0 and 2 and demands
v at height 1. Every cut deficit is 0, but one transport is needed. Proposition 3's
independence hypothesis excludes such duplicates.

## 3. Lemma 2 (storage neutrality)

In P1–P3, keeping a register at a fixed frame for any number of calls contributes nothing to
M. Adding duplicates of entry rows at their own heights changes neither the per-cut bound nor
the minimum M.

**Proof.**

- M counts transports only (rule 2).
- Spans do not change when duplicates are added.
- A same-frame copy is free (rule 1). So each configuration can reach the other at zero cost.

∎

**Consequences.**

- No per-array-call storage price follows from the moment. (S) is an extra physical premise.
  The question of physical storage is real but lies outside the moment: tape, banks, hosting
  windows, and the stream that holds an extra array.
- The selected record keeps helper residuals across calls on existing idle data streams, with
  no per-call charge (idle-axis hosting §2), and its hosted template has no helper banks.
  This shows that the selected accounting puts no moment price on retention by an existing
  stream. It does **not** show that new arrays are physically free.

## 4. Proposition 3 (record, partner and consumer: exact both-direction minimum)

**Setting.**

- Records R sit at height h_r and partners P at height h_p, with span R ∩ span P = 0.
- The demand is a row set O ⊆ span(R ⊕ P) at height h_c. Optionally P must also stay at h_p.
- Let ρ_r = dim(P + O) − dim P. This is the part of O that only the records can supply.
- Let ρ_p = dim(R + O) − dim R. This is the part only the partners can supply.
- Let ρ_o = dim O.

**Claim.** The minimum paid mass equals

min_L f(L), where f(L) = ρ_r |L − h_r| + ρ_p |L − h_p| + ρ_o |L − h_c|.

The minimum is attained at L = median(h_r, h_p, h_c), and it equals the sum of the cut deficits.

**Lower bound.** Fix a cut j. A side is "high" if it lies at heights ≥ j.

- **Consumer on the high side.** The upward deficit is:
  - 0 if R and P are both high;
  - ρ_r if only P is high;
  - ρ_p if only R is high;
  - ρ_o if neither is high.
- **Consumer on the low side.** The downward deficit is the mirror image.
- **Partner demand.** It never adds a deficit, because P is in the entry span on its own side.

**Matching f.** At cut j, f(L) is charged with the weights of those points of
{h_r (weight ρ_r), h_p (weight ρ_p), h_c (weight ρ_o)} that lie on the other side from L.

- If L lies on the **majority** side, the other side holds at most one point. Its weight is
  exactly the deficit in the case list above.
- Putting L on the minority side instead costs at least as much, by three inequalities:
  - ρ_r ≤ ρ_o, because ρ_r = dim(P+O) − dim P ≤ dim O;
  - likewise ρ_p ≤ ρ_o;
  - ρ_o ≤ ρ_r + ρ_p, because o ↦ (a(o), b(o)) below embeds O into A ⊕ B.

The median of {h_r, h_p, h_c} lies on the majority side of every cut. Hence

f(median) = min_L f(L) = Σ_j (δ_j⁺ + δ_j⁻) ≤ M,

where the last inequality is Lemma 1.

**Construction.**

1. Write each o ∈ O uniquely as a(o) + b(o) with a(o) ∈ span R and b(o) ∈ span P.
   - A = {a(o)} is the projection of O along P. Its kernel is O ∩ P, so
     dim A = dim O − dim(O ∩ P) = ρ_r.
   - Likewise B = {b(o)} has dim B = ρ_p.
2. Copy and move a basis of A from h_r to L, at cost ρ_r |L − h_r|.
3. Copy and move a basis of B from h_p to L, at cost ρ_p |L − h_p|. The partners stay at h_p.
4. At L, O lies in A + B, so form a basis of O there for free.
5. Move that basis to h_c, at cost ρ_o |L − h_c|.

The total cost is f(L). ∎

**Special cases.**

- (i) h_c = h_p ≥ h_r: the record **climbs**, at cost ρ_r (h_p − h_r).
- (ii) h_c = h_r ≤ h_p: the partners **descend**, at cost ρ_p (h_p − h_r).
- (iii) h_c = h_r = h_p: the cost is 0.

The consumer level is a premise of the caller. Proposition 3 prices every choice of it; it
does not choose one.

**Finite checks.**

- **Primary, by exhaustive search.** `verify.py` runs a breadth-first search over per-level
  spans. It checks opt = Σ deficits = min_L f on 10,748 instances:
  - GF(2)², 4 levels, complete;
  - GF(3)², 3 levels, complete;
  - GF(2)³, 3 levels, 24 independent (R, P) pairs drawn with `random.Random(59)`.
- **Independent.** `independent_check.py` runs Dijkstra over reduced echelon bases on 2,432
  GF(2)² instances, and checks opt = min_L f.
- **Negative controls.** An upward-only bound fails on 4,516 instances. A formula without the
  output term fails as well.

## 5. Corollary 4 (eight coordinates per level)

Under Fact T and P4, take a record of pair k captured at time t, when the pair is at level ℓ(t).
Suppose it is consumed at its pair's current frame at time t′, so h_c = h_p.

- Its catch-up is exactly 8 ρ_r (ℓ(t′) − ℓ(t)).
- Each later local call of the pair raises ℓ by one, so this is **at least
  8 ρ_r × (later data incidences before t′)**.
- Idle sweeps raise ℓ further.

**Child shape.** The law fixes the transported **mass**, not the shape of the children.

- One child of rank 8Δℓ per independent row realizes it. So do rank-8 children, one per level.
- Per unit of mass, larger children cost less in the moment when a > 0.
- So convention (C)'s "rank-8 copy per call" shape is sufficient but not forced.

## 6. Proposition 5: (S) and (C) compared with the law

**(a) When (C) is a special case of the law.** (C)'s mass is 8 per array-call. The law's mass
(current-frame consumer, ρ_r = number of rows) is 8 per level advanced. They are equal exactly
when the source family advances one level per counted call of the lifetime.

The #1166 records satisfy this:

- **INIT records** are captured just before their bank's first call, at levels −1, 2, 4 and 6.
  Since the levels are the global stage index minus one, the lifetimes are 9, 6, 4 and 2.
- **d_A records** are captured right after the backward call, at levels 1, 3 and 5. The
  lifetimes are 7, 5 and 3.

Philippe Van Velzen's price gate uses 8 for bank 0's d_A. Under the convention he uses for
INIT (calls after the capture point), the count is 7. The law therefore gives 8 × 456 = 3,648.
(C) as published gives 8 × 464 = 3,712. No decision changes.

**(b) Zero-catch-up witness.** Take pair 3's Y streams in replica 0 (families 784–895).
Nothing acts on them from entry until event 14 (time 40):

- no local call (stages 0–5 are on pairs 0–2);
- no idle sweep (the sweeps at events 2, 5, 8 and 11 are on pairs 1 and 2);
- no bridge (bridges at events 3, 6, 9 and 12 join pairs 0–1 and 1–2; event 15 is the first
  bridge that touches pair 3);
- no hosted residual. Their sweep from level −1 to level 5 is an unhosted rank-48 child, and
  no pooled slot lands on them before time 40.

A record of such a stream captured at entry and consumed at its current frame before event 14
therefore pays 0 under the law, over six calls. For each such array, (S) charges 6 and (C)
charges 48.

Pair 3's **X** streams host 160 helper residuals in the same window, so their frames do change.
That is the selected record's own use of this window shape ("nothing touches F between ι and
τ", idle-axis hosting §2). The witness uses the Y streams. It shows that the law is not (S)
and not (C).

**(c) A deferred family.** Pair 0's X streams (families 0–111) stay at level 2 from event 4
until the sweep from level 2 to level 8 at event 21. That sweep is an unhosted rank-48 child,
and no residual is hosted on these streams by time 40. Take a record captured after B5
(event 13, time 40) and consumed at the end.

- The law charges 48 per array (six levels).
- (C) charges 24 (three calls).

So (C) can also under-price.

**(d) (S).** Storage is not a moment price (Lemma 2). As a stand-in for catch-up, (S)
under-prices current-frame consumers by 8×. Example: PR2540's 16 early records over one call
cost 16 under (S), but the law gives 128, which is both forced and attained (§7.1).

## 7. Applications and decisions

### 7.1 Controls

| Control | Law | Source value |
|---|---|---|
| PR2540: 16 early records, F_L → F_U1 (one level) | 16 × 8 = 128 | its 16 rank-8 upgrades (PR2540 §2) |
| PR2197: 8 Y_A arrays moved 18 frame terms to private frame I | 8 × 18 = 144 | 144-line floor |
| PR2678: 224 outputs, F_U1 → F_L | 224 × 8 = 1,792 | 224 H8 |
| PR2678: 224 outputs, F_U1 → (C_q, I), heights 17 → 1 and 17 → 0 | 112 × 16 + 112 × 17 = 3,696 | 112 H16 + 112 H17 |
| Selected centre path: 8 centres per call descend 8 → 0 (PR1664 §5.2 / ctoth's tree lemma) | 64 per call, 576 per replica | eight rank-8 copies, C = 64 |
| #1166 price gate against PR2474 | break-evens 573 (S) and 71 (C) | reproduced with `ceiling.py` and with Decimal |

Notes on the controls:

- **PR2540.** It attains Proposition 3(i), assuming ρ_r = 16. That value is PR2511's rank-16
  bound for its compressed observation interface, as quoted in PR2540's README.
- **PR2678 F0-gauge row (1,904).** It adds one signed-line gauge per Y. That is outside the
  height model and is quoted from PR2678.
- **Centre path.** It is the law's descend direction.

### 7.2 Route (a): the INIT64 + d_A final-record contract (philippeVV, fork 9fcd3d89)

**Premises.**

- **Consumer timing (explicit).** The consumer works at each bank's **current** frame
  (h_c = h_p in Proposition 3). Two timings bracket the possibilities:
  - **P_final**, the stated contract: decode at the end, level 8, where the final records and
    the replica's data endpoint live.
  - **P_early**, the most favourable: decode each bank at its own frame right after its last
    local call (levels 2, 4, 6, 8). The corrected fields then ride the inherited idle sweep to
    level 8 at no extra cost.

  Any later timing advances the partners further, so it only adds catch-up. A consumer below
  the partners' frame would need its outputs moved back up, which Proposition 3 charges in
  full; it is not priced here.
- **P_rank (joint).** At every cut j, the stated arrays captured below j are linearly independent
  modulo all rows available at or above j. Those rows are the final records, plus any stated
  record captured above j. So the deficit at cut j is the number of stated arrays below j that
  the decoder needs.
  - Support: the finite-model census and the derived decoders.
  - Not proved on the actual cover.
- **Capture times.** As stated: INIT just before the bank's first call, and d_A right after
  the bank's backward call.

**Catch-up per replica.**

| Records | Capture levels | Levels climbed (P_final) | Units (P_final) | Levels climbed (P_early) | Units (P_early) |
|---|---|---|---|---|---|
| INIT, banks 0–3 (16 arrays each) | −1, 2, 4, 6 | 9, 6, 4, 2 | 1,152 + 768 + 512 + 256 | 3, 2, 2, 2 | 384 + 256 + 256 + 256 |
| d_A, banks 0–2 (8 arrays each) | 1, 3, 5 | 7, 5, 3 | 448 + 320 + 192 | 1, 1, 1 | 64 + 64 + 64 |
| **Total** | | | **3,648** | | **1,344** |

The P_early total is exactly 8 per later data incidence. Under P_final the idle sweeps add the
rest.

**Price.** With C = 0 and the controller free, a paid mass of at least 896 units per replica
leaves no positive saving, whatever the packing. The reason:

- At a = 0, every child costs r/m. The moment is then total/(m·w) = (72w + u/9)/(73w), which
  is at least 1 exactly when u ≥ 896 (one unpaid coordinate for each of the 896 families).
- For a ≥ 0, every child cost (r/m)^(1−a) is at least r/m.

Both `ceiling.py` (at 895 and 896) and the exact rational check agree.

**Decision: rejected in the stated model, under either convention and either consumer
timing.** Both 3,648 and 1,344 are at least 896. Adding a storage price can only raise the cost.

**Robustness.**

- d_A alone costs 960 under P_final, which is ≥ 896.
- Theorem B in #2074 c18940190 (philippeVV) says any repair needs at least 62 coordinates per
  owner per replica. It is a posted claim, with fork `680d0997`, and has not been reviewed.
  - If the needed information lies in the stated captures, any 62 of the 88 cost at least
    1,952 under P_final. This needs only Theorem B, not the joint P_rank.
  - The weakest combination considered is P_early with only the 62 cheapest stated captures.
    It costs 800, giving a κ ceiling of 0.000509, far below the selected 0.0016727. So even
    there the route gains nothing over the selected record or any pending claim.
- **Sufficiency.** Whether INIT64 + d_A is actually sufficient (finite models; derived
  decoders, #2074 c18950926) does not affect the rejection. A contract that is not sufficient
  fails anyway, and one that is sufficient costs at least the amounts above.

**What could revive the route.** A contract whose catch-up-weighted retention stays below the
break-evens:

- 573 idle-priced or 568 rank-8 units against PR2474;
- 570 idle-priced or 568 rank-8 units against #2843 and #2848;
- 568 idle-priced or 560 rank-8 units against the bit endpoint (PR589).

For example, 62 arrays would need an average climb under about 9.2 coordinates. Each array
would have to be captured within about one level of its consumer frame. The stated INIT
captures are 2 to 9 levels below it.

### 7.3 Route (b): shared-source centre sharing over a one-call gap

**Which pairs.** PR2199 lists six classes of same-replica shared-data pairs: f0→b1, b1→f2,
b3→f4, b5→f6, b7→f8 and f0→f2.

- f0→f2 is the only class with a one-call gap: B1 lies between the two calls. So 16 eligible
  pairs exist, one per replica.
- The other five classes are adjacent.

**Prior information obstructions.** These apply whatever the retention convention.

- **PR2199.** Every one of the 1,539 dependent pairs, f0→f2 included, has formal pair rank 16
  in its calls-only projection. The "8 rows" figure is the roles-0..111 restriction. For
  f0→b1, it is certified not to survive once the helper roles stay formal.
- **#2391 and #2461 (PR2391, PR2461).** These treat the adjacent f0→b1 class (calls 0 and 4):
  a native non-lift, and 104 owner-local coordinates per owner.

**The law adds an independent reason.** Suppose the information were present, and the sharing
is realized as #1166 prices it: the 8 rows are retained across B1 and consumed at pair 0's
current frame in f2. Suppose also that they are independent modulo the rows available there.

- B1 is a data incidence of the source pair between capture and reuse. So Corollary 4 charges
  at least 8 per row, which is at least 64 per shared 8-row set.
- That equals the per-call centre charge the sharing would save. The net moment gain is
  therefore at most 0, which is (C)'s ×1.000.
- (S)'s ×1.787 leaves out this catch-up.

**Decision: rejected.** The information obstruction comes from the predecessors; the
catch-up argument is new here. The two reasons are independent.

### 7.4 Route (c): QQ16 retained caller #2540/#2651 against the zero-retention #2707

These are the gate rows for #2617.

**Retention in the moment.**

- It is exactly 128, which is PR2540's 16 H8. Under ρ_r = 16 and the F_U1 consumer this is a
  proved lower bound, and PR2540 attains it.
- So the "16 H8" row and the "retention" row are one charge, not two.
- Holding the records at F_L across B1 is free in the moment (Lemma 2).

**Physical storage.** Storing 16 arrays across B1 is UNKNOWN, because it lies outside the
moment. #2651 coalesces these arrays into output banks.

**The zero-retention decoder #2707.** This is a pending PR at head `efa51a6c`. ywz65 reports an
invoice of 336 H1 children, against PR2540's 224 H1 + 16 H8; we have not re-derived that
invoice.

- The difference in child moment has the sign of 112 − 16·8^(1−a).
- This is negative for 0 ≤ a ≤ 1/16, since 8^15 > 7^16. The check is exact in `verify.py`.
- So, on the reported invoice, #2707's whole added child moment is below the retained
  caller's, and #2707 needs no retention at all.

**Child shape.** The 128 cannot be realized more cheaply in the moment. Each of the 16
independent rows must cross 8 cuts, and rule 3 allows one row per transport. So at most one
child of rank 8 is available per row, and rank-8 children are the cheapest per unit of mass.

**Decision for the gate.**

- In the moment, the retained-record caller is dominated by #2707 (on its reported invoice).
- The law shows that its retention row cannot fall below 16 H8 for this interface.
- Therefore the retained caller can only win on costs outside the moment:
  - #2707's extra 192 wrappers, 256 maps and 8,368 scalars;
  - against the retained caller's UNKNOWN cost of 16 stored arrays.
- **Recommendation: narrow.** Stop optimizing retention for the retained caller, and compare
  physical (non-moment) caller costs with #2707 as the moment baseline.
- The precision rows (PR2603 and the #2692 chain), travel (#2794), allocation (#2709) and the
  output consumer (UNKNOWN) are unaffected.

## 8. Scope and unresolved obligations

- **Physical storage, tape and hosting windows of retained arrays** lie outside the moment and
  are UNKNOWN. Lemma 2 neither prices nor dismisses them.
- **P_rank for INIT64 + d_A** rests on finite-model evidence only.
- **The consumer timing** is a premise, not a theorem. It is bracketed by P_early and P_final;
  a consumer below the partners' frame is not priced.
- **P4 (no slack in inherited words)** is supported by the coverage identity and PR1664 §5. It
  is not re-derived event by event here. Slack exhibited in an inherited word would reduce the
  forced catch-up by at most that slack.
- **Forward histories.** The derived decoders use f2, f4 and f6, which are themselves retained
  arrays. They are not counted in the 464 array-calls. If they are retained separately, the
  law charges 8 per level, at most 768 more. The rejection does not need them.
- **Non-nested frames.** Only nested chains are treated. For non-nested frames, d ≥ |Δh| still
  gives a lower bound. Gauges such as signed lines can add more (PR2678's 1,904).
- **Prices.** Break-evens are given for ideal idle packing (rank 51) and for rank-8 children.
  The prices are ceilings, not attained exponents.
- **Frame-model checks** cover the stated finite domains only. Proposition 3 is proved in
  general above.
- **No new κ, no supplier, no change to the selected frontier.**

## 9. Credit

- The transport model and cut lemma are an664's (PR1664), with the GPT-6 Pro review it
  records.
- The tree lemma and the coverage partition are ctoth's (#1516, #1587).
- The coverage identity is PR1012's. Idle-axis hosting comes from the #434 lineage.
- The native frames are from ywz65 (PR2540, PR2707); the tariff from petalas (PR2678); the
  private d_A floor from 1337isnot1337 (PR2197).
- The census and price gate are Philippe Van Velzen's.
- Philippe Van Velzen's sibling-helpers note anticipates Lemma 2 and Corollary 4. On helper
  time-sharing it says "the bill is coordinate advances, not storage". The note is at fork
  `b5ce9d22`, `research/complex-budget-law/closures-2/sibling-helpers/README.md`; its author
  marks it LOCAL-ONLY, and here it was read as data only.
- The information obstructions are from navinor (#2391) and ywz65 (#2461), and our PR2199.
- Also credited: Ross Richardson (PR2480), alephnan (PR2346), commdata2338 (PR2174, PR2651),
  and the QQ16 lineage of Ali Romman.

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5).
No human or formal-kernel review. Apache-2.0.
