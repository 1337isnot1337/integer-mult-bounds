# E8 over extension rings: copy-cost floors under the #595 format (no κ claim)

This package follows up #620 §4 (S1). It asks whether E8, viewed as a unit over a larger ring, can beat real E8 under the #595 format:

- over Z[i]: 60 Gaussian lines, w = 4;
- over Z[ω]: the 40 Witting lines, w = 4;
- over the Hurwitz quaternions: 10 lines, w = 2.

The quantity that decides it is x_K = Σ_j β_j / v. Here β_j is the #446 Theorem C pairing-rank cost of total j, counted in K-ranks, and the minimum runs over **every** F2 decoder on the K-orthogonality pattern: any number of totals, asymmetric W ≠ U allowed, and no star premise.

To beat the bit E8 ceiling X* = 6.0005e-3, a w = 4 view needs x_K < ~0.708, so Σβ ≤ 42 for the Gaussian view. A w = 2 view needs x_K < ~0.86. These thresholds come from S1's float screen `fx.py`, which uses skel.X's profile with float roots. They are not certified here.

Labels used below:
- **checked**: `verify.sh` recomputes the claim with exact arithmetic, or with SAT where stated (CaDiCaL via python-sat, no proof logs).
- **argued**: the proof is in this README.
- **recorded**: a run whose log is shipped; `verify.sh` does not repeat it.

## Results

| view | v | w | floor proven here | best decoder known | excluded? |
|---|---|---|---|---|---|
| Eisenstein (Witting) | 40 | 4 | **Σβ ≥ 40 for every decoder** (x_K ≥ 1) | 40 (frames) | **yes** |
| Hurwitz | 10 | 2 | **Σβ ≥ 10 for every decoder** (x_K ≥ 1) | 10 (frames) | **yes** |
| Gaussian | 60 | 4 | **Σβ ≥ 40 for every decoder** (x_K ≥ 2/3); Σβ = 60 for 15-total decoders (pending; see G2) | 60 (frames) | **no**: the window 40–42 is open |

**Theorem (Eisenstein and Hurwitz).** Viewed over Z[ω] or over the Hurwitz order, E8 cannot beat real E8 in the #595 format. Under #446 Theorem C, every decoder of the K-orthogonality pattern pays Σ_j β_j ≥ v. This covers any number of totals, asymmetric pairings and non-star copy trees. So x_K ≥ 1, D_s/k = (s − 1)·v − s·x_K·v < 0 at every s, and there is no saving at all. **Gaussian E8 is not settled.** The floor proven here is 40 and exclusion needs 43.

## Model (as in #595 C.6 and #446 Theorem C)

- **Decoder.** B = Σ_j w_j u_j^T over F2, with readers R_j = supp w_j and sources A_j = supp u_j.
- **Pattern.** B_TT = 1, and B_TS = 0 whenever the lines T and S are K-non-orthogonal. B_TS is free on orthogonal pairs.
- **Cost.** By Theorem C, β_j/k ≥ rk(span A_j × span R_j), the rank of the real pairing divided by k = dim_Q K. For K-subspaces this is the K-rank of the Gram block G[R_j, A_j]. Since the form is positive definite, rk(X × Y) = dim Y − dim(Y ∩ X^⊥).
- **Cost-0 totals.** A total of cost 0 has R_j × A_j made only of orthogonal pairs. It touches only free entries and can be dropped. Every total that is kept costs ≥ 1.
- **Construction (checked).** `lines.py` builds the three views exactly from the 240 roots in doubled coordinates. The Gaussian view uses J = left multiplication by i on H². The Eisenstein view uses a fixed-point-free order-3 element ρ of W(E8), the product of the Coxeter elements of 4 orthogonal A2's. The Hurwitz view uses left multiplication by i, j, k.

## E. Eisenstein: Σβ ≥ 40 for every decoder (argued; every ingredient checked by `eisen_floor.py`)

**Lemma (sum-rank).** Let M_j = P_{R_j} G P_{A_j}, padded to v × v. Then Σ_j β_j ≥ Σ_j rank M_j ≥ rank(Σ_j M_j) = rank(G ∘ N), where N_TS = #{j : T ∈ R_j, S ∈ A_j} is an integer matrix. Because N ≡ B (mod 2), N_TT is odd and N_TS is even on every non-orthogonal pair.

**Lemma (odd line lattices).** For every line T, pick a Z-basis of span(T) ∩ E8. Suppose every such line lattice has **odd** determinant. Then the real Gram G̃ on these bases is integral, its diagonal blocks are invertible mod 2, and its off-diagonal blocks vanish on orthogonal pairs. So G̃ ∘ (N ⊗ J) ≡ diag(G̃_TT) (mod 2), which has full rank. Hence rank_Q ≥ Σ_T dim T, that is, Σ_j β_j ≥ v in K-units.

- **Eisenstein satisfies it.** Each line lattice is ⟨r, ρr⟩ ≅ A2, with Gram [[2, −1], [−1, 2]] and det 3 (checked for all 40 lines).
- **Complex form of the same proof.** Let h_E(x, y) = (⟨x,y⟩ − ω⟨x, ρy⟩)/4. It is Z[ω]-valued and sesquilinear (checked), and its K-ranks equal the Theorem C ranks (checked on 200 random blocks). Its diagonal is 2 + ω, of norm 3, so a unit at the inert prime 2. Hence (h_E ∘ N) mod 2 is (2+ω)·I over F4, of rank 40 (checked on random admissible N as a sanity test).
- **Why real E8 itself escapes.** Its line lattices are √2·Z (det 2), so the lemma does not apply. This is consistent with the shipped 72 < 120.
- **The other two views.** The Gaussian line lattices are √2·Z[i] (det 4) and the Hurwitz ones are D4 (det 4), so neither is covered.

## H. Hurwitz: min Σβ = 10 exactly (argued; checked by `hurwitz_floor.py`, plus a direct SAT)

**Structure (checked).** There are 10 lines and w = 2. Each line is orthogonal to exactly one other, so the orthogonal pairs form a perfect matching. Any two distinct lines span H².

**Cost formula.** Because of that structure, a total costs one of three amounts:
- 0 if R × A has no equal-or-non-orthogonal pair;
- 2 if |R| ≥ 2 and |A| ≥ 2;
- 1 otherwise.

This follows from rk = dim Y − dim(Y ∩ X^⊥) and is checked exactly on all 3,025 pairs with |R|, |A| ≤ 2. Larger sets add nothing, because their span is already H².

**Proof that every decoder costs ≥ 10.**
1. Drop the cost-0 totals.
2. Let X be the sum of the cost-2 totals, so they cost 2g ≥ 2·rank X. Let ρ be the rows of the single-row totals and γ the columns of the single-column totals; these cost ≥ |ρ| + |γ|.
3. B + X vanishes outside the rows ρ and the columns γ. So on ρ' × γ' (the complements), X agrees with the pattern.
4. Let C = ρ' ∩ γ'. The C × C part of X is block-diagonal, with blocks [1] or [[1, *], [*, 1]], because non-orthogonal entries are 0. So rank X ≥ |C|/2.
5. Hence cost ≥ |C| + (10 − |ρ'|) + (10 − |γ'|) ≥ 10, using |ρ'| + |γ'| ≤ 10 + |C|.

The 5 orthogonal pairs, used as frames, attain 10.

**Checks.**
- The reduced form (2g + |ρ| + |γ| ≤ 9, for g = 0..4) is UNSAT.
- This closes S1's open item 2. A direct SAT run with S1-style encoding (`hurwitz_direct.py C`: arbitrary totals, exact cost formula, cost cap C) gives:
  - C = 10: SAT (calibration).
  - C = 9: see `logs/hurwitz_direct.log` (**recorded** if present).

## G. Gaussian (not settled)

**G1. Floor of 40 for every decoder (checked, `gauss_bound40.py`).**
- **Counting step.** Take each of the 640 twelve-line sets C of pairwise K-non-orthogonal lines. The pattern forces B[C, C] = I₁₂, and every total contributes a rank-1 F2 matrix there. So ≥ 12 totals hit C on both sides.
- **Reduction to flats.** For fixed spans, hit(R, A) is largest at R = lines(X) and A = lines(Y).
- **The inequality.** The script checks hit(X, Y) ≤ 192·rk(X, Y) on all 2271² flat pairs. Hits are exact integers. Ranks are certified lower bounds: integer pairing matrices, rank mod 2³¹ − 1.
- **Conclusion.** Σβ ≥ 12·640/192 = **40**.
- **Binding pair.** X is a 6-line 2-flat through ℓ and Y is the 15-line hyperplane ℓ^⊥: pairing rank 1, 192 hits.
- **Trying to improve it.** An LP over uniform orbit weights added every maximal clique size (7, 8, 10, 11, 12), the singletons, the non-orthogonal pairs and the whole set (minrank 15). It stays at 40 (`gauss_lp3.py` in the work dir; float LP, **recorded**).

**G2. Decoders with exactly minrank = 15 totals.**
- **Why every total then costs 4.** With n = rank B = 15, W and U have full column rank. If every nonzero vector of col W and of col U has a support that spans K⁴, then each total pairs K⁴ with K⁴ at rank 4, and Σβ = 60.
- **The SAT question.** `gauss_c15.py` asks whether a valid 15-total decoder exists together with x ≠ 0 such that supp(Wx) lies in one of the 1500 three-dimensional flats. The calibration without the flat constraint is SAT in 1 s. The main run is **pending** (see `logs/gauss_c15.log`). If it comes back UNSAT, every 15-total decoder costs exactly 60. That would be the Gaussian analogue of #595's "9 totals × 8" premise, but without the star assumption.

**G3. What the 2-adic method can give (checked, `gauss_pi.py`).**
- The Gaussian diagonal is 2 = −i·π². The off-diagonal entries are units on 32 pairs per line and π·unit on 12 pairs per line.
- The mod-π reduction of G ∘ N/2 is I plus free entries on the unit pairs.
- The unit graph splits into 12 five-cliques, so this method can certify at most 12.
- No per-line 2-adic rescaling helps either. Write p_T, q_T for the 2-adic valuations of the determinants of the row and column rescalings of line T. One needs p_T + q_T = −2 on every line and p_T + q_S ≥ 0 on every unit pair (argued). Adding the two pair inequalities for a unit pair (T, S) gives 0 ≤ (p_T + q_T) + (p_S + q_S) = −4, a contradiction.

**Open (Gaussian).**
- A decoder with Σβ ≤ 42 would need ≥ 16 totals, most of them with a support confined to a hyperplane flat. By counting, n_full ≤ 10 totals of cost 4.
- The obvious next step is an LP with new kinds of Z-sets: rectangles C₁ × C₂ with a known minrank, or sets that the cheap (6-line 2-flat, ℓ^⊥) totals rarely hit on both sides.
- Alternatively, an exact SAT with sub-spanning totals.

## Files (`scripts/`)

| file | what |
|---|---|
| `lines.py` | exact E8 roots, the three views, K-ranks, pairing ranks, Hermitian Gram matrices |
| `flats.py` | all flats of a view (Gaussian: 2271) |
| `eisen_floor.py` | §E checks |
| `hurwitz_floor.py`, `hurwitz_direct.py` | §H checks; the direct SAT with a cost cap |
| `gauss_bound40.py`, `gauss_pi.py`, `gauss_c15.py` | §G1, G3, G2 |
| `verify.sh`, `expected.txt` | runs the checked items and compares the PASS/RESULT lines with the frozen output |

```sh
PY=/path/to/python3.11 sh verify.sh     # numpy, scipy, networkx, python-sat; ~3-6 min
```

Credits: builds on S1 (#620 §4), #595 (DreamingOfClouds, format limits) and #446 (Theorems A–C). Prepared with Claude Opus 5.5 via Claude Code.
