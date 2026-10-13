# Lorentzian unit I_{11,1}: punctures, E8 skeleton features, and the helper budget (no κ claim)

This note follows up S3 (`e8-decoder-floors-and-cold14-notes/s3-unit-families`). That package found I_{11,1} to be the best non-E8 unit lead:

- v 220, window h 11, minrank 11;
- label decoder cost 110, so x = 1/2;
- certified ceiling X* 7.1715·10⁻³;
- but the helper-adjusted model puts it below E8 unless it reaches ≤ 2.66 (abs) / 3.34 (rel) helpers per port. E8 ships 3.95.

This package asks three questions:

1. Can punctures (the analogue of E8's 120 → 111) lower x or raise X*?
2. Which E8 geometry sets E8's helper count, and does I_{11,1} have it?
3. What does the calibrated model say for the best punctured unit?

**Answers, in short:**

1. **No improving puncture.**
   - For the centre (label) decoder, no puncture of any size improves x. This is an exact certificate for I_{11,1} and I_{13,1}.
   - For every label decoder, the same holds up to 8 (I_{11,1}) or 10 (I_{13,1}) punctures.
   - No puncture of ≤ 19 lines lowers the minrank to 10 (SAT).
   - The E8 mechanism exists here: puncturing a line makes its own label functional one unit cheaper. But that functional starts at h, not h − 1, so it only ties the centres.
2. **The E8 skeleton features carry over, but the count lands at or above break-even.**
   - Carried over: cell cover number 3, orthogonal 4-frames with F₂ parity, and a "design" obstruction for triple sources.
   - Not carried over: a partition into such frames is impossible (55 pairs is odd), and each needer must sum 56–70 lines against E8's 30.
   - The transferred skeleton counts 3.33–3.58 helpers per port.
   - Within the cell architecture, carriers alone are exactly 2 per port. Reaching ≤ 3 would need a middle network that costs less than ⅔ of E8's per cell while carrying about twice E8's demand per needer (argued; not a theorem over all designs).
3. **The model gives no gain over E8.** The best unit is the unpunctured one. At the transferred-skeleton intensity the model gives 1.58·10⁻³ (abs) / 1.73·10⁻³ (rel), against E8's 1.806·10⁻³. Only the optimistic variant (pair sources on two non-cell branches, rel scaling) touches E8: 1.811·10⁻³, which is +0.3% and inside model error.

Status labels:

- **checked**: `verify.sh` recomputes it. Exact rational arithmetic, or a CP-SAT/SAT optimum or UNSAT as stated.
- **argued**: a proof written here.
- **model**: an estimate, not a bound.

SAT answers come from CaDiCaL 1.5.3 (python-sat) without proof logs. CP-SAT optima are reported only when the status is OPTIMAL.

```sh
PY=/path/to/python3.11 sh verify.sh /path/to/integer-mult-bounds-main /fresh/out   # ~30-40 min, 10 cores
```

Requirements: numpy, sympy, networkx, python-sat, ortools. The scripts import #595's `skel.py`/`cert.py` (main, `research/format-limits/scripts`) and S3's `units.py`, `est_model.py` and `rank.py`, which are copied unchanged into `scripts/`. `check.py` compares every log with `expected/`; it ignores run times and allows a relative difference of 1e-9 on model floats.

Conventions follow #595 §A and S3:

- **Pattern.** The decoder pattern is B_TT = 1, with B_TS = 0 where G_TS ≠ 0.
- **Labels.** The labels are S3's I_{n,1} labels (a 3-set, or the complement of a pair).
- **Reader set.** R(p) = {t : ⟨u_t, p⟩ = 1}.
- **Star cost.** A label total p costs dim_Q span(R(p) ∩ live).
- **Optimal label decoder.** It is the minimum-weight basis of the live label space (matroid greedy, exact).

## 1. Reader census (`census.py`, checked)

| n | functional weight k | readers | span | Gram rank |
|---|---|---|---|---|
| 11 | 1 (the 11 centres e_i) | 90 (45 triples ∋ i, 45 pairs ∌ i) | **10** | 10 |
| 11 | 2 … 11 | 90 … 220 | **11** | 11 |
| 13 | 1 (centres) | 132 | **12** | 12 |
| 13 | 2 … 13 | 132 … 364 | **13** | 13 |

Only the centres span h − 1, so the unpunctured label decoder is forced to be the centre decoder: 11 × 10 = 110 and 13 × 12 = 156. The Theorem C pairing floor (#446) of every centre equals its span, so on the unpunctured unit Theorem C = star.

## 2. Punctures (Q1)

### 2.1 The centre decoder never improves (`partition.py`, checked certificate + argued)

**Theorem P1.** For every live set L of I_{11,1}: Σ_i rank(R(e_i) ∩ L) ≥ |L|/2. For I_{13,1}: Σ_i rank(R(e_i) ∩ L) ≥ (3/7)|L|.

**Proof (I_{11,1}).**

- `partition.py` partitions the 220 lines into 22 sets I_{i,1}, I_{i,2}, each linearly independent and contained in R(e_i). Exact ranks are verified; every set has size 10.
- Then 2·rank(R(e_i) ∩ L) ≥ |L ∩ I_{i,1}| + |L ∩ I_{i,2}|. Summing over i gives the claim.

**Proof (I_{13,1}).** Take three copies of each of the 364 lines. They split into 91 independent sets, 7 inside each R(e_i), each of size 12. ∎

**Consequence.** For the centre decoder, x(P) ≥ 1/2 (resp. ≥ 3/7) for every puncture P, so the unpunctured ratio is never beaten.

**Scope.**

- Costs are span ranks. This is the right measure for live sets with a nondegenerate span.
- A degenerate live set (a radical appears, e.g. the E8 sub-configuration) is dominated by its quotient unit (#595 Lemma Q). It is a different unit with a smaller window; see §2.4.

### 2.2 All label decoders, small punctures (`packbases.py`, checked + argued)

`packbases.py` treats each functional orbit (Hamming weight k, under S_n). It strips coloops (lines outside the span of the rest of R(p)) and packs q disjoint bases into the rest. The packings are verified exactly.

**The E8 mechanism, here.** For k = 3 (triple labels) and k = n − 2 (pair labels), the coloop is the line itself:

- R(u_t) = {t} ∪ (readers of t);
- the readers of t span only h − 1.

So puncturing t makes its own label functional drop from h to h − 1. That is exactly E8's 8 → 7. Here, however, h − 1 is what the centres already cost.

**Theorem P2.** Every label decoder has x ≥ 1/2 on I_{11,1} for |P| ≤ 8, and x ≥ 3/7 on I_{13,1} for |P| ≤ 10.

**Proof.**

1. **Disjoint bases protect rank.** If R(p) minus its coloops holds q disjoint bases, deleting P costs that rest at most ⌊|P|/q⌋ rank.
2. **Every non-centre functional keeps cost ≥ h − 1.** The binding orbits are:
   - n = 11: k = 9, rest rank 10, q = 9, so |P| ≤ 8;
   - n = 13: k = 11, rest rank 12, q = 11, so |P| ≤ 10.

   The full table is in `packbases*.log`; for n = 11 the other orbits allow 10–39 deletions.
3. **The live space is unchanged.** The weight-n functional holds 20 (resp. 28) disjoint bases, so the live span and window stay h.
4. **Combine with P1.** Let S be the set of centres in an optimal basis. Then W ≥ Σ_{i∈S} r_i + (h − 1)(n − |S|) ≥ Σ_i r_i ≥ |L|/2 (resp. (3/7)|L|), because r_i ≤ h − 1. ∎

**First cheap non-centre total (`example_pairlabel.py`, checked).**

- **Puncture.** Delete the pair {0,1} and the 9 triples {0,1,x}, 10 lines in all. The pair-label functional then drops to 9: star 109/210 = 0.519, X* 6.3495·10⁻³ (s = 3).
- **Ratio.** One cost unit costs 10 punctures, while improving x needs more than 1 unit per 2 punctures.
- **Theorem C.** The floor here is 108 (X* at 108/210 = 6.5549·10⁻³), still below the unpunctured unit.

### 2.3 Fewer totals after puncturing? (`clique_orbits.py`, `punct_sat.py`, checked by SAT)

The maximum pairwise non-orthogonal cliques of I_{11,1} (the #595 pattern's identity blocks) are 38,786 cliques of size 10, in 5 S_11-orbits. The orbit sizes are:

| orbit size | composition |
|---|---|
| 27,720 | 8 triples + 2 pairs |
| 9,240 | 7 triples + 3 pairs |
| 495 | 8 triples + 2 pairs |
| 1,320 | 3 triples + 7 pairs |
| 11 | 10 pairs |

(#634's 10,395 sets Cl(a, M) are pairwise *orthogonal*. They belong to #634's knowing graph, not to this pattern.)

**Gauge argument.**

- A line lies in at most 1,784 of these cliques. So any ≤ 21 punctures leave a maximum clique alive (`survival_bound`, checked).
- The clique gauge U_K = W_K = [I | 0] on one representative per orbit, forced live, is therefore without loss of generality for k ≤ 21.

**Result: the minrank stays 11 for every puncture of ≤ 19 lines.** With c = 10 and k = 19, the SAT instance is UNSAT for all 5 orbits (`sat19_o*.log`). Runs at k = 0, 4 and 8 (orbit 0) were UNSAT in under 6 s.

**Consequence.** A 10-total decoder needs ≥ 20 punctures. If its totals cost 10 each, that gives x ≥ 100/200 = 1/2.

**Scope.** General (non-label) 11-total decoders with totals cheaper than 10 are not excluded. The same open item, the non-star decoder, holds for E8 (#595 F.2, #631).

### 2.4 Window-lowering sub-units (`punct.py`, checked)

These keep the lines avoiding a set of coordinates. Labels are inherited from I_{11,1}; Theorem C is the greedy Gram-rank floor.

| live lines | v | h | star (x) | X* | Theorem C (X*) |
|---|---|---|---|---|---|
| all | 220 | 11 | 110 (1/2) | **7.1715·10⁻³** (s 3) | 110 |
| avoid coordinate 10 (I_{10,1}-type) | 165 | 10 | 99 (3/5) | 4.0462·10⁻³ (s 5) | 88 (6.3329·10⁻³) |
| avoid 9, 10 (the E8 lines; radical 1) | 120 | 8 | 80 (2/3) | 3.4352·10⁻³ | 80 |
| avoid 8, 9, 10 | 84 | 8 | 63 (3/4) | 1.9850·10⁻³ | 63 |

The inherited labels are not minimal on sub-units. E8's own labels give 72, not 80 (#595 C.6). So these rows are upper bounds on those units' cost. The E8 rows are the known E8 unit, and the I_{10,1}-type unit loses even at its Theorem C floor.

### 2.5 Heuristic search (`anneal.py`, exploratory; logs in `data/`)

The search used two objectives:

- x, 3 seeds × 4000 moves;
- an X* proxy (2 − 3x)/h that also rewards lowering h, 1 seed.

Each run used float ranks and exact greedy bases. Every run ended at the unpunctured unit. This is evidence only.

## 3. Helpers (Q2)

### 3.1 What sets E8's 3.95 helpers per port

The shipped word is #555 (= `research/e8-bit-p111`, R = 439 at v = 111). It sits on #543's L3 skeleton (`research/e8-bit-r420`, itself on #493's `e8-bit-carrier-skeleton` partition):

| component | count | per port (v = 111) | geometric reason |
|---|---|---|---|
| carriers | 240 | 2.16 | 3 branches per source, at the three cells {s, e} of its 4-frame. 3 is the minimum: s⊥ = E7 is a spherical 4-design, so no 2 hyperplane sections cover it (#463). Checked here as "no nonzero quadratic form vanishes on the 63 readers" (`twocover.py 8`). |
| empty cell registers | 180 | 1.62 | 30 orthogonal 4-frames × 6 cells; **3 registers per cell** (#493/#543 family bound): 2 line branches + 1 register that delivers the cell sum to the two quads (D4 frames of 6 cells from 6 blocks) and keeps a line |
| totals | 9 | 0.08 | F₂ minrank 9 |
| extra carriers (puncture) | 10 | 0.09 | #545 pseudo-target mini-nodes |

**E8 features this rests on:**

- **(a) Good 4-frames.** The 120 lines partition into 30 orthogonal 4-frames whose half-sum is a lattice vector (F₂ parity).
- **(b) Free inclusion–exclusion on the target side.** By (a), every reader s of t meets 1 or 3 of t's frame-mates.
  - So t's three needers at the D6 frames {t, e}⊥ count every reader an odd number of times.
  - The exceptions are t's 3 frame-mates, which are fixed by single "d-line" reads.
- **(c) Small, well-shared needer sums.** {t, e}⊥ holds 30 lines. Each is assembled from two quad outputs plus one Q-delivery, and each quad output serves 6 needers.
- **(d) Block nodes.** D4 blocks in complementary pairs supply the Q-deliveries.

### 3.2 What I_{11,1} (and I_{13,1}) has (`cellcover.py`, `twocover.py`, `frames.py`, checked; parity argued)

| feature | E8 | I_{11,1} | I_{13,1} |
|---|---|---|---|
| readers per source | 63 | 115 (triple), 129 (pair) | 183, 231 |
| cell cover number (branches into 2-dim cells {s, e}) | 3 | **3** (both types; CP-SAT OPTIMAL; attained by pairwise-orthogonal e's) | **3** (both types) |
| 2 branches of *any* frame dimension possible? | no (quadratic forms vanishing on readers: dim 0) | **triple: no (dim 0)**; pair: not excluded (dim 1; S3 has a 2-cover certificate) | triple: no; pair: not excluded |
| good 4-frames (orthogonal, F₂ parity) | 9,450 | **20,790**: 6,930 of type (pair, pair, triple, triple), 13,860 of type (triple)⁴ | not computed |
| partition into good 4-frames | yes (30) | **impossible**: every good frame holds 0 or 2 pairs, and 55 is odd | – |
| lines in a cell-perp (needer demand) | 30 | **56–70** | – |
| needers per port | 1.5 | 1.5 (3 per target, each shared by 2 targets) | 1.5 |

**Parity (argued).** For example, {e₀−e₁, e₂−e₃, t_{401}, t_{423}} has half-sum e₀ + e₂ + e₄ + e₁₂ ∈ Z^{11,1} ∩ w⊥. For every integral line s, the sum of s's products with the frame is then even, so (b) holds verbatim, including the d-line correction. `frames.py` checks the parity condition directly on all 1,926,540 orthogonal 4-sets.

### 3.3 A concrete skeleton sketch (argued count) and the ≤ 3 obstruction

**Sketch: the E8 cell architecture transferred.**

- Cover the lines by good 4-frames: 54 frames plus one frame reused for the odd pair, about 6 extra registers.
- Sources branch into their 3 cells: 2 carriers per source, 440.
- Each of the 330 cells holds 3 registers, adding 1 empty register per cell (330).
- Targets read 3 needers at {t, e}⊥ plus the d-lines.
- 11 totals.

| variant | helpers | **per port** |
|---|---|---|
| all sources on cells | 440 + 330 + 11 + 6 = **787** | **3.58** |
| pair sources on their 2-cover (2 non-cell branches) | 385 + 330 + 11 + 6 = **732** | **3.33** |

Not constructed:

- the middle network (quad and block-node analogues);
- the d-line reads, cleanup, hosting.

**The count assumes a middle as cheap per cell as E8's, while each needer must collect 56–70 lines instead of 30.**

**Obstruction to ≤ 3 helpers per port (argued, conditional on the architecture).**

- **Cell-branch designs.** Sources branch only into 2-dim cells and carriers are pure, as in #493/#543/#555. Then carriers are **exactly ≥ 2 per port**, because the cell cover number is 3 for both line types (checked).
- **Remaining budget.** ≤ 3 per port leaves ≤ 1 − 11/220 = 0.95 per port for the whole middle, i.e. ≤ 0.63 empty registers per cell.
- **Comparison with E8.** E8 needs 1 per cell (#493's family bound of 3 per cell) for half the demand per needer.
- **Any design with pure carriers.** Triple sources need ≥ 3 branches whatever the frame dimension (exact: no quadratic form vanishes on their 115 readers, the analogue of E8's design-strength carrier bound). So carriers are ≥ (2·165 + 55)/220 = **1.75 per port**, leaving ≤ 1.2 per port for the middle and totals.
- **Design-free floors.** S3 §4's floors (cover numbers 2–3, about 1 per port) remain the only bounds that hold for every design, so this is **not** a theorem excluding ≤ 3.
- **What it says.** A ≤ 3 skeleton must abandon E8's "3 registers per cell" middle, or share registers across sources (mixing carriers) far more than #555 does.

## 4. Calibrated model on the best unit (Q3; `model3.py`, model)

The best punctured unit is the unpunctured 220/110 (§2). S3's calibrated helper model (`est_model.py`, unchanged; bit calibration 1.0032 against #555) gives E8's target a = 1.8058·10⁻³ (#555 at ρ = 439/111):

| unit | ρ* abs / rel | a_est at ρ = 3.577 (cells) | at 3.327 (pairs on 2 branches) | at 3.955 (E8's) | at 3.0 | at ρ_dim 5.207 |
|---|---|---|---|---|---|---|
| I_{11,1} 220/110 | 2.66 / 3.34 | 1.580 / 1.730 ·10⁻³ | 1.654 / **1.811**·10⁻³ | 1.480 / 1.620 | 1.716 / 1.875 | 1.225 / 1.339 |
| I_{11,1} 210/109 | 2.38 / 2.84 | 1.495 / 1.638 | 1.566 / 1.715 | 1.401 / 1.534 | 1.625 / 1.775 | 1.165 / 1.267 |

(Pairs are abs / rel; the unit is 10⁻³.)

Reading:

- The transferred-skeleton intensity is 3.33–3.58 against break-even 2.66 / 3.34.
- Only the optimistic corner (rel scaling, pair 2-branch variant, a middle as cheap as E8's) reaches E8, at +0.3%. That is inside model error and rests on the unbuilt middle.
- Clearing E8 robustly (rel) needs ρ ≈ 3.0, i.e. the ≤ 0.63-per-cell middle of §3.3.

## 5. Not done / open

- **Exact rank-loss thresholds.** δ_d for the non-centre functionals: the MIP in a first draft was too slow and was dropped. These would extend P2 beyond 8 / 10 punctures (the 10-line example shows the first sub-10 total appears at exactly 10 for pair labels, and it is not an improvement).
- **Non-label decoders.** Non-label 11-total decoders on punctured I_{11,1}; Theorem C floors are listed for comparison.
- **The middle network.** Constructing a middle network for I_{11,1} with ≤ 0.63 empty registers per cell, or proving a family bound for it. D4 blocks and complementary pairs (E8 feature (d)) were not searched.
- **I_{13,1} frames.** Good-frame and frame-partition data for I_{13,1}.
- **Overlap check.** #920 (complex shared-parity frame dimensions), #912 (Hurwitz adaptive routing) and #907 (abelian Cayley metric scope) do not touch Lorentzian units, punctures or bit carrier skeletons.

## Files

- `scripts/census.py`: §1.
- `scripts/partition.py`: P1.
- `scripts/packbases.py`: P2.
- `scripts/punct.py`: exact star and Theorem C evaluation, §2.4.
- `scripts/example_pairlabel.py`: the 10-line puncture example of §2.2.
- `scripts/clique_orbits.py`, `scripts/punct_sat.py`: §2.3.
- `scripts/anneal.py`: §2.5, not in `verify.sh`.
- `scripts/cellcover.py`, `scripts/twocover.py`, `scripts/frames.py`: §3.
- `scripts/model3.py`: §4.
- Copied unchanged from S3: `units.py`, `est_model.py`, `rank.py`, `cover.py`.
- `scripts/check.py`, `expected/`, `verify.sh`; `data/` holds the anneal logs.

## Credits

This note builds on:

- DreamingOfClouds: #595 (skel/cert, §A/§D/§F, Lemma Q), #446 Theorem C, #463's carrier bound, #545's punctured star;
- ShikeChen01: #634, the Lorentzian family;
- Chi Zhao: #631, the puncture-threshold method;
- eumemic: #493, #543 and the E8 bit skeletons;
- #555;
- S3 (GamingPuzzled).

Prepared by Joel Pulikkan (GamingPuzzled) with Claude Opus 5.5 (Anthropic) via Claude Code. Apache-2.0.
