# S8 — Gaussian E8: no decoder with at most 18 totals costs ≤ 42

Context: #620 §10 (S5: Σβ ≥ 40 for every decoder), §13 (S6: every 15-total decoder costs 60) and §14 (S7: no 16-total decoder costs ≤ 42).
- The setting is the Gaussian view of E8: 60 Q(i)-lines in K⁴, with the F2 decoder pattern (B_TT = 1, and B_TS = 0 on K-non-orthogonal pairs).
- The cost is the Theorem-C cost Σ_j β_j.
- To beat real E8 a decoder needs Σβ ≤ 42.

Labels:
- **checked**: `verify.sh` recomputes the claim, with exact integers and certified rank lower bounds.
- **argued**: the proof is in this README.

## Results

**Theorem 1 (two counting facets; argued + checked).** Every Gaussian-E8 decoder with c totals has

  Σβ ≥ max(40, 60 − c).

So every decoder with c ≤ 17 totals costs ≥ 43. This re-proves §14 (c = 16) with the stronger bound 44, and settles **c = 17**. No level tables or SAT are needed.

**Theorem 2 (c = 18; argued + checked).** No 18-total decoder costs ≤ 42.

**Theorem 3 (tight face).** A decoder with Σβ = 60 − c exists for no c: for 15 ≤ c ≤ 20, μ = (c − 12)/12 is non-integral, and c ≤ 14 or c ≥ 21 is impossible (minrank 15; cost ≥ 40). In particular:
- c = 19 needs cost ≥ 42, so the only value open there is cost exactly 42;
- c = 20 needs cost ≥ 41.

**Corollary.**
- A total of cost 0 touches only free entries, so it can be dropped. That gives a decoder with fewer totals and the same cost.
- Therefore a Gaussian decoder that beats real E8 has **between 19 and 42 totals of nonzero cost**.
- The upper end holds because each such total costs ≥ 1.
- **The all-c theorem is NOT proved. The open range is 19 ≤ c ≤ 42.** See "Gap" below.

## Proof

### 0. Data (checked: `hits_table.py`, which is S5's `gauss_bound40.py` plus a pickle dump)
For all 2271² pairs of flats (X, Y), the table holds:
- the exact clique hits h(X, Y): the number of the 640 twelve-line cliques of pairwise non-orthogonal lines that meet both X and Y;
- a certified lower bound R(X, Y) on the K-rank of the pairing, computed as an exact integer rank mod 2³¹ − 1.

### 1. Theorem 1
**Per clique (S5, argued).** On a clique C the pattern forces B[C, C] = I₁₂. A total contributes to this block only if it *hits* C, meaning R_j ∩ C ≠ ∅ and A_j ∩ C ≠ ∅, and then it contributes a rank-1 matrix. So N_C, the number of totals hitting C, satisfies N_C ≥ 12. Summing over the 640 cliques gives Σ_j hit_j ≥ 7680.

**Per total (checked, `facets.py`).** Let X_j, Y_j be the spans of the two sides of total j. Then
- hit_j ≤ h(X_j, Y_j), and β_j ≥ R(X_j, Y_j);
- by rank, the largest h is 0, 192, 384, 512, 640 for R = 0, 1, 2, 3, 4;
- the upper concave envelope of these values has two facets, so on **every** flat pair

  h ≤ 192·R  and  h ≤ 128·R + 128.

Summing over totals gives 7680 ≤ 192·Σβ and 7680 ≤ 128·Σβ + 128·c. ∎

The two facets give two slack identities, each term of which is ≥ 0:
- (D) Σ_j d_j + E = 192·cost − 7680, where d_j = 192β_j − hit_j;
- (E) Σ_j e_j + E = 128·(cost + c) − 7680, where e_j = 128β_j + 128 − hit_j;
- in both, E = Σ_C (N_C − 12).

### 2. Theorem 2 (`c18.py`)
1. **Tightness.** At c = 18 and cost ≤ 42, the right side of (E) is ≤ 0. Hence cost = 42, E = 0 (every clique is hit **exactly** 12 times), and every e_j = 0.
2. **The span pair is tight.** hit_j ≤ h(X_j, Y_j) ≤ 128·R + 128 ≤ 128β_j + 128 = hit_j, so (X_j, Y_j) is a *tight* flat pair, and total j hits exactly the cliques that its span pair hits.
3. **The tight pairs (checked).** There are 1081 of them, and they are exactly:
   - (ℓ^⊥, m^⊥) with ℓ ⊥ m, β = 2;
   - (ℓ^⊥, ℓ^⊥), β = 3;
   - (ℓ^⊥, K⁴) and (K⁴, ℓ^⊥), β = 3;
   - (K⁴, K⁴), β = 4.

   Here ℓ^⊥ is a 15-line 3-flat. For each tight pair t, the set of cliques it **misses** is exactly {C : C meets x_t}, where x_t is a set of pairwise orthogonal lines ({ℓ, m}, {ℓ} or ∅). In matrix form, 1 − h_t = M·x_t, where M is the 640 × 60 clique/line incidence matrix.
4. **Equation.** So 12·**1** = N = Σ_j h_j = 18·**1** − M·μ, with μ = Σ_j x_{t(j)} ∈ Z₊⁶⁰. That is, Mμ = 6·**1**.
5. **Contradiction.** M has exact rank 60 (checked, sympy), and M·(½·**1**) = 6·**1** because every clique has 12 lines. So μ = ½·**1**, which is not integral. ∎

**Theorem 3.** The same argument applies whenever cost = 60 − c. That case needs (E) = 0, and with cost ≥ 40 it forces c ≤ 20. Then Mμ = (c − 12)·**1**, so μ = (c − 12)/12. For c = 19, 20 this is 7/12 and 2/3, neither integral.

### 3. Consequences for 19 ≤ c ≤ 42 (argued)
- From (D), a total with β ≥ 3 has d ≥ 64 and a full total has d = 128 (checked: the smallest d at R = 3 is 64, at R = 4 it is 128). So there are at most 3 full totals and at most 6 totals with β ≥ 3, **for every c**.
- From (E), a rank-1 total has e ≥ 64. So there are at most 2(c − 18) rank-1 totals, while cost ≤ 42 needs at least 2c − 42 of them.
- At c = 19 with cost 42, the slack in (E) is only 128.

## Gap: what is not proved, and why
- **Linear counting cannot go further.** `lp2.py` is an LP over uniform orbit weights. It uses cliques of every size (7, 8, 10, 11, 12), single lines, complements of all flats (minrank 15), the whole set, and a free c-term μ·c. Its value is exactly max(40, 60 − c) (float LP, recorded). So linear counting with these sets is exhausted; what goes further must be integrality, as in Theorem 2, or F2 structure.
- **Level tables do not scale.** The S7 level-table route does not reach c ≥ 19. Every multiset of at most c − 15 three-flats is trivially a level set, so the bottom levels alone have about 1500^(c−15)/11520 orbits. The hyperplane-only version at c = 18 grew as 1, 5, 21, 129, 921, 7917 reps at levels 1–6.
- **Integer counting is not enough either from c = 21 on (checked).**
  - `tight_ilp.py 21` (CP-SAT) found 21 dumbbell totals (ℓ^⊥, m^⊥) with ℓ ⊥ m. They cost 42 in total, and they hit every 12-clique at least 12 times (between 12 and 16 times).
  - `check_c21cover.py` re-checks this exactly; see `logs/check_c21cover.log`.
  - So clique counting, even with integrality, cannot exclude c ≥ 21. That range needs the F2 pattern itself, for example S7-style rank-drop or level arguments on the dumbbell hyperplanes, or a SAT search.
- **c = 19 and 20 are open.**
  - c = 19: cost exactly 42 with (E)-slack 128.
  - c = 20: cost 41 or 42.
  - CP-SAT returned UNKNOWN within its time limit on two runs:
    - the full covering ILP over 124,841 rank-maximal types (`types.py`, `cover_ilp.py`, all c, 900 s);
    - the tight-types-only version (`tight_ilp.py 19/20`, 300 s each).

  See `logs/`.

## Validation
- c = 15: Theorem 1 gives ≥ 45, consistent with §13's exact 60.
- c = 16: it gives ≥ 44, consistent with §14's ≥ 43.
- The identity decoder (60 single-line totals, cost 60) meets 7680 = Σ hits exactly, with 128 hits per total, and satisfies both facets.
- §14's machinery was rerun from scratch with a multiset-aware level search (`levels_ms.py` in the work dir, exact multi-key canonical form). It reproduced S7's level counts 3, 28, 120, 368 for k = 1–4; the run was stopped after that because it is superseded.
- **Caveat on S7 (not affecting any S8 claim).** S7's `levels2.keys` packs ids 6, 7, … into one int64 with 12-bit shifts. That overflows for k > 10, so the canonical form there is a min over a truncated key. False prunes would need two distinct images to tie on the truncated key. None were observed, but none were excluded either. Theorem 1 re-proves §14 without the tables.
- No new SAT/UNSAT verdicts are used, so no Glucose cross-check is needed. All checks are exact integer computations, plus a sympy rank.

## Files (`scripts/`)
| file | what |
|---|---|
| `lines.py`, `flats.py` | S5's exact construction of the lines and flats |
| `hits_table.py` | S5's `gauss_bound40.py`, which also dumps `hits_table.pkl` |
| `facets.py` | Theorem 1: both facets on all flat pairs; the tight pairs |
| `c18.py` | Theorems 2 and 3: tight-pair miss sets equal M·x_t; rank M = 60; the parity contradiction |
| `lp2.py` | the LP showing linear counting stops at max(40, 60 − c) |
| `types.py`, `cover_ilp.py`, `tight_ilp.py` | integer clique-covering relaxations (exploratory; CP-SAT) |
| `check_c21cover.py` | exact check of the c = 21, cost-42 integral cover |

```sh
PATH=$SP/venv/bin:$PATH sh verify.sh     # ~6 min, 1 process; compare with expected.txt
```
