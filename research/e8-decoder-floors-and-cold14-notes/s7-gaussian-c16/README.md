# S7 — Gaussian E8: no decoder with exactly 16 totals costs ≤ 42

Context: #620 §10 (`s5-extension-ring-floors/`) and §13 (S6, every 15-total decoder costs exactly 60).
- The setting is the Gaussian view of E8: 60 Q(i)-lines in K⁴ with the F2 decoder pattern (B_TT = 1, and B_TS = 0 on K-non-orthogonal pairs). The minrank is 15.
- Theorem-C cost is Σβ_j, where β_j is the K-rank of the pairing span(R_j) × span(A_j).
- Proven floor: 40 for every decoder (S5).
- To beat real E8 a decoder needs Σβ ≤ 42. By S5 and S6, such a decoder needs at least 16 totals.

## Result

**Theorem (S7).** Every Gaussian-E8 decoder with exactly 16 totals has Σβ_j ≥ 43.

So a Gaussian decoder that beats real E8 needs at least 17 totals.

## Definitions

- **Level-k set.** A set of k distinct 3-flats Z_1..Z_k such that every subset J of it satisfies
  minrank(pattern on O_J) ≤ 16 − |J|, where O_J is the set of lines outside ∪_{i∈J} Z_i.
- **Cheap total.** Total j is cheap when β_j < 4, and k is the number of cheap totals.

## Proof

### 1. [argued] Cost by type
The form is Hermitian definite on K⁴. With X = span R_j and Y = span A_j, β_j = dim X − dim(X ∩ Y^⊥) ≥ dim X + dim Y − 4.
- If neither side is proper, β_j = 4.
- Otherwise β_j < 4, and a side lies in a proper flat, hence in a 3-flat spanned by lines.

Cheap totals fall into three types:
- **a**: one side has dim ≤ 2, so it lies in a 2-flat Z. **Every** 3-flat through Z is a legal 3-flat for this total. β ≥ 0.
- **p**: dims (3,3) with β = 2. Then X ≠ Y, and both X and Y are legal 3-flats (a "dumbbell").
- **q**: everything else. Here β ≥ 3: either (3,4), or (3,3) with β = 3.

With f = 16 − k full totals:
- cost ≥ 4f + 2p + 3q.
- So cost ≤ 42 forces **3a + p ≥ 22 − k**.

### 2. [argued] Rank drop over several flats (extends the S6 lemma)
Pick one legal 3-flat Z_j for each cheap total j.
- For any subset J, the columns j ∈ J of W (or U) vanish on O_J. So B[O_J, O_J] has rank ≤ 16 − |J| and obeys the induced pattern.
- Hence **every** legal choice gives a level-k set.
- The flats are distinct. If one 3-flat H were legal for two totals, then rank B[O,O] ≤ 14 on O = the lines outside H, but S6 proved minrank 15 there.

### 3. [checked] Level tables up to the line group (order 11520, from S6 `orbits.py`)
- `levels2.py` / `levels3.py` compute all orbit representatives of level-k sets, k = 1..16. The run uses these steps:
  - extend each level-(k−1) rep by one 3-flat;
  - canonicalise (least image under the group);
  - keep the set only if all of its (k−1)-subsets are level-(k−1) sets;
  - SAT-test the whole union at rank ≤ 16 − k. The SAT encoding is S6's clique-gauge encoding.
- Rep counts by level:

  | k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | reps | 3 | 28 | 120 | 368 | 498 | 464 | 315 | 206 | 124 | 74 | 32 | 24 | 10 | 6 | 1 | 0 |

- Level 2: 28 of the 178 pair orbits pass.
- From level 7 on, subset closure does all of the pruning.
- Consistency check: the slow canonicaliser (`levels.py`) and the fast one (`levels2.py`/`levels3.py`) agree on levels 2–4.
- **Cross-check.** Every UNSAT pruning (levels 2–6, 200 instances) was re-solved with Glucose 4: see `logs/cross_glucose.log`. Only UNSAT verdicts remove configurations; a wrong SAT verdict would only keep more.

### 4. [checked] (A): a = 0 whenever k ≥ 5
A member of a level-k rep is *a-capable* if some 2-flat Z inside it has the following property: substituting each 3-flat through Z still gives a level-k set (6, 12 or 14 substitutions, depending on the 2-flat's size).
- Reps with an a-capable member: 3, 19, 18 and 3 at k = 1..4, and **0 for every k ≥ 5**.
- So a decoder with k ≥ 5 cheap totals has no total with a side of dim ≤ 2.
- The case of a line side is covered too: the line lies in a 2-flat inside the chosen 3-flat, and every 3-flat through that 2-flat contains the line.

### 5. [checked] (B): few dumbbells
- β between 3-flats is computed for all 1500² pairs: β = 2 on 102180 ordered pairs and 3 on the rest. The method is SVD of products of orthonormal bases; an assert checks that no singular value is ambiguous.
- p* is the largest number of members of a level-k rep that can be doubled at once. Doubling means each chosen member gets a partner Y with β = 2, and **all 2^p** transversals are level-k sets.
- Results for k = 11..15: p* = 5, 4, 3, 2, 1. The requirement 22 − k is 11, 10, 9, 8, 7.

### 6. Arithmetic
| k | why 3a + p ≥ 22 − k fails |
|---|---|
| ≤ 4 | 3a + p ≤ 3k < 22 − k |
| 5..10 | a = 0, so p ≤ k < 22 − k |
| 11..15 | p ≤ p* < 22 − k |
| 16 | no level-16 set exists |

The 2-flat search (`lev_c16_d2`) is not needed for the theorem. It shows that at most 2 totals can have a side of dim ≤ 2, for any k.

## Calibrations
- c = 16 decoders exist (SAT in 0.1 s, `calib.log`). A SAT-found c = 16 decoder is priced in `logs/price16.log`: all β_j = 4, sum 64.
- Level 1 at c = 15 is empty (rank ≤ 14 on each 3-flat complement is UNSAT), which reproduces S6.
- The direct monolithic encoding (`direct.py`: 16 columns, 9 of them confined to flats, no gauge) gave no answer in 20 min per instance. The orbit and level route is what made the problem tractable.

## Related hub work (cited; no overlap)
- #767 (cbethin, planar and incidence obstructions) and #2066 (adamgall, whole-hyperplane reciprocity ≥ 180, symmetric B) are scoped subclass bounds.
- #738 and #770/#868 are about the clique-LP floor of 40.
- None of these treats 16-total decoders.

## Reproduce
`PATH=$SP/venv/bin:$PATH sh verify.sh` uses 8 processes. It rebuilds the level tables from scratch (about 15 min), runs `prove_c16.py` (about 13 min), `price16.py` and the c = 15 calibration. Compare the output with `expected.txt`. A from-scratch run reproduced `expected.txt`, and the rebuilt tables are identical to `data/lev_c16_d3_hi.pkl`. `CROSS=1` adds the Glucose cross-check (about 45 min).

## Notes
- `scripts/sub_minrank.py` is S6's encoder with one change: isolated lines are added to the clique graph, so a line set with no non-orthogonal pair still gets a 1-clique gauge.
- `refine.py`, `acap_sanity.py` and `dumbbell.py` are the exploratory forms of (A) and (B). `prove_c16.py` is the consolidated check.
