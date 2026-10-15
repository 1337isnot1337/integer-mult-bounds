# S9 — Gaussian E8: integral clique packing closes c = 19 (and part of c = 20); c ≥ 21 needs F2 structure

Context: #620 §13–§15 (S6, S7, S8). Setting: the Gaussian view of E8, 60 Q(i)-lines in K⁴, F2 decoder pattern
(B_TT = 1, B_TS = 0 on K-non-orthogonal pairs), minrank 15, line group of order 11520, Theorem-C cost Σβ_j.
Beating real E8 needs Σβ ≤ 42. Before S9: cost ≥ max(40, 60 − c); c ≤ 18 excluded; c = 19 open only at cost 42;
c = 20 open at 41–42; c ≥ 21 open (and S8 found an integral clique cover at c = 21, so counting alone cannot close c ≥ 21).

Labels: **checked** = recomputed by `verify.sh` (exact integers / certified ranks for the data; HiGHS MIP and CP-SAT for
the integer programs, see "Trust" below); **argued** = proof in this README.

## Status (PARTIAL — written 2026-10-15 01:40 EDT, solver jobs still running)
- **Proven (checked):** the μ-packing lemma (§1) and its corollary: a decoder whose totals are all tight costs ≥ 44 at c = 18–20 and ≥ 42 at c = 21.
- **c = 19, cost 42: 17 of 20 cases excluded. Three cases are still running:** orbits 17, 18 and 20. Their logs are  (HiGHS, optimisation form) and  (CP-SAT on case 20). The 10 cases that went to the time limit in optimisation form all had dual bounds ≤ 33 < 34, and analogous cases gave dual bound 33 within 1200 s. **c = 19 is NOT yet closed.**
- **c = 20:** cost 41 has cases −1 and 2 excluded; cases 4, 5 and 6 are running (), and cases 9 and 11–23 were never run. Cost 42 has cases −1 and 21 excluded; case 22 is running (, sequential −1, 21, 22, 23, 19, 20). The heavy cases at cost 42 (orbits 1, 2, 4–6 and 9–18, 20k–54k columns) were never run; they look out of reach without a better formulation.
- **c ≥ 21:** counting is exhausted (proven). The F2 pattern is what fails on the counting covers (2×2 support lemma, §3). This is not a proof for any c ≥ 21.

## 1. The μ-packing lemma (checked: `mu_ilp.py` HiGHS optimal, `mu_cpsat.py` CP-SAT cross-check)
M = 640 × 60 clique/line incidence (the 640 twelve-cliques of pairwise non-orthogonal lines; each line lies in 128).

  f(k) := max { |μ| : μ ∈ Z≥0⁶⁰, Mμ ≤ k·1 } = 28, 32, 36, 42, 48, 52, 60 for k = 6, …, 12,

while the LP value is 5k (μ = k/12·1). CP-SAT independently: k = 7, |μ| ≥ 33 INFEASIBLE; k = 8, |μ| ≥ 37 INFEASIBLE.
The integrality gap (3 at k = 7, 4 at k = 8) is what S8's linear counting could not see.

**Corollary (all-tight decoders; argued).** S8: a tight total t misses exactly the cliques M·x_t with x_t pairwise
orthogonal lines and gain g_t = 4 − β_t = |x_t|. N_C ≥ 12 gives Σ_j M x_j ≤ (c − 12)·1, so Σ g ≤ f(c − 12):
cost ≥ 4c − f(c − 12) = 44 (c = 18), 44 (c = 19), 44 (c = 20), 42 (c = 21). The c = 21 value is attained by
S8's 21-dumbbell cover, so counting is exactly exhausted there.

## 2. Lifted packing relaxation for all decoders (argued; data checked)
For a decoder with c totals and cost ≤ cm:
1. **WLOG β_j ≥ 1** (S8: a cost-0 total can be dropped; c − 1 is already excluded at the same cost).
2. **Types.** Replace total j by a rank-maximal enlargement t of its span pair (X_j, Y_j): certified rank R_t ≤ β_j,
   its miss set m_t (cliques not met on both sides) ⊆ the total's miss set, and e_t = 128R_t + 128 − hits_t ≤ e_j.
   All rank-maximal types with 1 ≤ R ≤ 3 have e ≤ 132; deduplicated by (R, miss set) there are **58,340**, in **27 orbits**
   under the line group (`types_e.py`, `dom.py`).
3. **Packing.** N_C ≥ 12 ⇔ Σ_j m_j ≤ (c − 12)·1. Cost ≤ cm ⇔ Σ_j g_j ≥ 4c − cm with g = 4 − β ≤ g_t.
   Identity (E) of S8: Σ_j e_j + E = 128(cm + c) − 7680 =: slack, so Σ_j e_t(j) ≤ slack.
4. **Lifting.** Z_t = lines all of whose 128 cliques are missed by t; x_t = a maximum pairwise-orthogonal subset (α_t = |x_t|).
   A clique contains at most one line of x_t, so M x_t ≤ m_t. If α_t ≥ g_t ("non-deficient") replace t by x_t (fewer
   misses, gain ≥ g_t): these totals only enter through μ = Σ x_t ∈ Z≥0⁶⁰. "Deficient" types (δ_t = g_t − α_t > 0) keep their
   exact miss set. Every deficient type has e_t ≥ 16 (`lift_prep.py`; table below).
5. **Case split (symmetry).** No deficient total: Σ g ≤ f(c − 12). Otherwise apply a group element so that the
   deficient total of **largest e** is its orbit representative t₁; every other deficient total then has
   e ≤ min(e₁, slack − e₁). Each case is the ILP  M μ + m_{t₁} + Σ n_t m_t ≤ (c−12)·1,  Σ n_t e_t ≤ slack − e₁,
   |μ| + g_{t₁} + Σ n_t g_t ≥ 4c − cm  (μ, n integer) — `branch1.py` (HiGHS; "feas" adds the last row as a
   constraint, "opt" maximises the left side and reports the dual bound).

**Theorem 1 (c = 19), partial.** Cases −1, 2, 4, 5, 6, 9–16, 19, 21, 22 and 23 are excluded: HiGHS proved them infeasible, or the optimisation form gave a dual bound ≤ 33 < 34. Cases 17, 18 and 20 are still running. If they are excluded, then no 19-total decoder costs ≤ 42 (logs: ).

**Theorem 2 (c = 20), partial.** Cost ≤ 41: cases −1 and 2 are excluded. Cost ≤ 42: cases −1 and 21 are excluded. Everything else is open or running (see Status).

Single-deficient diagnostics (`vsingle.py`, c = 19): with one deficient total fixed to each orbit representative,
max(|μ| + g) ≤ 33 < 34 for every orbit, i.e. deficient totals always cost more clique capacity than they gain.

| orbit | R | e | α | δ | size |  | orbit | R | e | α | δ | size |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 128 | 3 | 0 | 60 |  14 | 2 | 84 | 0 | 2 | 5760 |
| 1 | 1 | 132 | 2 | 1 | 2880 |  15 | 2 | 70 | 0 | 2 | 5760 |
| 2 | 1 | 100 | 2 | 1 | 1440 |  16 | 2 | 70 | 0 | 2 | 5760 |
| 3 | 2 | 128 | 2 | 0 | 360 |  17 | 2 | 76 | 1 | 1 | 2880 |
| 4 | 1 | 84 | 1 | 2 | 1920 |  18 | 3 | 76 | 0 | 1 | 960 |
| 5 | 1 | 76 | 2 | 1 | 960 |  19 | 2 | 24 | 0 | 2 | 720 |
| 6 | 2 | 76 | 1 | 1 | 320 |  20 | 2 | 34 | 0 | 2 | 5760 |
| 7 | 1 | 64 | 3 | 0 | 180 |  21 | 2 | 16 | 0 | 2 | 1440 |
| 8 | 2 | 64 | 2 | 0 | 30 |  22 | 2 | 20 | 1 | 1 | 2880 |
| 9 | 2 | 108 | 0 | 2 | 2880 |  23 | 3 | 20 | 0 | 1 | 480 |
| 10 | 2 | 114 | 0 | 2 | 5760 |  24 | 2 | 0 | 2 | 0 | 90 |
| 11 | 2 | 112 | 0 | 2 | 2880 |  25 | 2 | 0 | 2 | 0 | 360 |
| 12 | 2 | 112 | 0 | 2 | 2880 |  26 | 3 | 0 | 1 | 0 | 60 |
| 13 | 2 | 112 | 0 | 2 | 2880 |  | | | | | |

## 3. c ≥ 21: counting is exhausted; the F2 pattern is what fails (checked: `f2check.py`, `try_cand.py`, `core.py`, `tight_diag.py`)
- For c ≥ 21 the lifted relaxation is feasible already with μ alone (f(9) = 42 = 4·21 − 42, f(10) = 48 ≥ 46, …): no counting
  argument of this kind can exclude c ≥ 21.
- `f2check.py` solves the actual F2 problem with every total confined to given line sets (R_j ⊆ X_j, A_j ⊆ Y_j, optional
  alternatives such as both orientations of a dumbbell). Calibration: the identity decoder (60 singleton totals) is SAT and
  re-checks as a valid decoder.
- **The counting covers are F2-infeasible.** S8's 21-dumbbell cover (fixed orientation: UNSAT immediately — some line has
  no total covering its diagonal) and the cover found by `tight_diag.py` (21 dumbbells satisfying clique counting AND
  diagonal coverage; free orientation per dumbbell): UNSAT in 0.1 s.
- **Minimal reason** (`core.py`, UNSAT core over per-line assumptions + deletion): a single non-orthogonal pair {23, 26}.
  On it the decoder needs B[{a,b},{a,b}] = I₂. Exactly one total covers both diagonals, and the only other total hitting the pair
  can give just one off-diagonal entry. Counting is satisfied (2 totals hit the pair), but I₂ − e_a e_bᵀ has rank 2.
- **Exact 2×2 support lemma** (`pairkinds.py`): classify each total on a non-orthogonal pair {a,b} by its kind
  (X∩{a,b}, Y∩{a,b}). I₂ is reachable iff the multiset of kinds contains one of **17 minimal patterns**:
  16 two-element patterns (two totals that can supply the two diagonal entries) and the triple
  {(ab,ab), (a→b), (b→a)}. This is a local F2 constraint that counting (N_K ≥ |K|) does not capture.

## Remaining open cases
- c = 19 (cost 42): cases 17, 18 and 20 (running).
- c = 20, cost 41: cases 4, 5 and 6 (running), and 9, 11–23 (not run).
- c = 20, cost 42: every case except −1 and 21. Case 22 is running.
- 21 ≤ c ≤ 42: everything. Suggested next step: a cut loop that adds the exact 2×2 lemma constraints (, written but not run) plus F2 cores to the type ILP.

## Trust and validation
- Inputs are exact (lines, flats, cliques, hits) with certified rank lower bounds (S5/S8 `hits_table.py`). The relaxation
  only uses R as a lower bound on β and hits as upper bounds, so every step is in the safe direction.
- The integer programs are solved in floating point by HiGHS (scipy 1.x `milp`) and have no proof certificates. The μ optima
  were cross-checked with CP-SAT. The case ILPs have not been cross-checked independently; one CP-SAT run () is in progress.
- Calibrations (must be feasible, are feasible): c = 21, cost ≤ 42, case "no deficient" (μ = 42); c = 19, cost ≤ 44,
  same case. The F2 checker accepts the identity decoder.
- Not used: level tables (S7), the S6 sweep.

## Files (`scripts/`)
| file | role |
|---|---|
| `lines.py`, `flats.py`, `hits_table.py`, `orbits.py` | S5/S6/S8 exact data: lines, 2271 flats, 640 cliques, hits, certified ranks, the order-11520 group |
| `mu_ilp.py`, `mu_cpsat.py` | μ-packing optima f(k) (HiGHS) and CP-SAT cross-check |
| `types_e.py`, `dom.py`, `lift_prep.py` | type catalog (58,340), orbits (27) and dominance, lifting data (x_t, δ_t) |
| `branch1.py` | one case ILP of the lifted relaxation (`feas` / optimisation form) |
| `vsingle.py` | single-deficient diagnostics |
| `f2check.py`, `try_cand.py`, `core.py`, `tight_diag.py`, `pairkinds.py`, `check_c21cover.py` | F2 confinement SAT, UNSAT cores, tight covering ILP with diagonal coverage, 2×2 lemma, S8's c = 21 cover |

```sh
PATH=$SP/venv/bin:$PATH sh verify.sh            # data + μ lemma + calibrations + F2 checks (~15 min)
FULL=1 PAR=6 PATH=$SP/venv/bin:$PATH sh verify.sh   # + every case ILP of Theorems 1-2 (hours)
```

## Addendum (2026-10-15, after the agent stopped): final case results
- **c = 19: all 20 lifted cases EXCLUDED.** The last three (cases 17, 18 and 20, 11,280 columns each) finished in the optimisation form with a HiGHS MIP dual bound of 33 < 34 needed, with best incumbents 31, 31 and 30, at about 2,400 s each (`logs/cases_19_42_opt2.log`). CP-SAT on case 20 returned UNKNOWN (`logs/cp_19_20.log`); the HiGHS bound is the one used. **Hence no 19-total Gaussian decoder costs ≤ 42.** HiGHS dual bounds are floating-point MIP bounds; they are not exact certificates.
- **c = 20, partial.**
  - At cost ≤ 41: cases −1, 2, 10, 11, 12 and 13 are EXCLUDED. Cases 6 and 9 hit the time limit (OPEN).
  - At cost ≤ 42: cases −1 and 21 are EXCLUDED. Cases 19, 22 and 23 hit the time limit (OPEN).
  - The remaining heavy cases were not run. See `logs/cases_20_41.log` and `logs/cases_20_42_light.log`.
- `verify.sh` has not been rerun from scratch.
