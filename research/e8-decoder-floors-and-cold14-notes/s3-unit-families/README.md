# Beyond E8 (no κ claim): ADE screen erratum, certified triple-family and Lorentzian ceilings, and a helper-adjusted ranking

These notes follow up #620 (GamingPuzzled). They make **no κ claim** and ship no word.

Status labels:

- **checked**: `verify.sh` recomputes the item; it is exact or certified unless marked *model*.
- **argued**: a proof written in this README.
- **model**: an estimate. It is not a bound.

```sh
sh verify.sh /path/to/integer-mult-bounds-main /fresh/out     # PY=python3.11 ...; about 40 min, steps in parallel
```

Requirements: Python ≥ 3.11 with numpy, networkx and python-sat. The scripts import #595's `skel.py`, `cert.py`, `minrank_sat.py` and
`e8units.py` from `research/format-limits/scripts` of main. `check.py` compares every recomputed field with
`expected.json`:

- integers, fractions and certified interval ends must be equal;
- model floats must agree to a relative 10⁻⁹.

SAT answers come from CaDiCaL through python-sat, **without proof logs**.

Conventions are those of #595 (§A):

- a unit is v lines with a Gram matrix G and window h (k = 1);
- decoder pattern over F2: B_TT = 1, and B_TS = 0 wherever G_TS ≠ 0;
- c is the number of totals;
- star cost cst = Σ_j β_j, where β_j is the dimension of the gathered span (the copy drops f = V → 0);
- x = cst/v;
- X* is the certified root of skel.X, maximised over odd s ∈ [3, 15].

## 1. Erratum to #620's ADE screen (`ade_screen_fixed.py`, checked)

#630 (vectorsss) is right: #620's `E6()` took the complement of two **orthogonal** roots. That gives 30 lines of type D6.
E6 is the complement of an A2 (a·b = 1), which has 36 lines. Recomputing the whole table found two more problems with #620's
screen.

- #620's column "c" was rank_F2(J + G) of one decoder. That is only an **upper** bound on the minrank. The column is now
  the exact F2 minrank, with asymmetric decoders allowed: SAT from the clique bound ω upwards, under the GL(c) gauge on the clique.
- #620 charged every total the full window (x = c·h/v). The table now also gives the star cost that label decoders on
  the B0 labels actually attain, cst_lab: a matroid-greedy minimum over bases of F2^c of Σ dim span(gathered set). It is
  an upper bound on cst_min.

| unit | v | h | rank_F2(J+G) | ω | **minrank** | x_proxy = c·h/v | cst_lab (x_lab) | X* (proxy / lab) |
|---|---|---|---|---|---|---|---|---|
| A4 | 10 | 4 | 5 | 4 | 5 | 2 | 15 (3/2) | – / – |
| A5 | 15 | 5 | 5 | 5 | 5 | 5/3 | 20 (4/3) | – / – |
| A6 | 21 | 6 | 7 | 6 | 7 | 2 | 35 (5/3) | – / – |
| A7 | 28 | 7 | 7 | 7 | 7 | 7/4 | 42 (3/2) | – / – |
| A8 | 36 | 8 | 9 | 8 | 8..9 (c = 8 timed out after 600 s) | ≥ 16/9 | 63 (7/4) | – / – |
| D4 | 12 | 4 | 3 | 3 | 3 | 1 | 12 (1) | – / – |
| D5 | 20 | 5 | 5 | 4 | 5 | 5/4 | 20 (1) | – / – |
| D6 | 30 | 6 | 5 | 5 | 5 | 1 | 30 (1) | – / – |
| D7 | 42 | 7 | 7 | 6 | 7 | 7/6 | 42 (1) | – / – |
| D8 | 56 | 8 | 7 | 7 | 7 | 1 | 56 (1) | – / – |
| D9 | 72 | 9 | 9 | 8 | 8..9 (timeout) | ≥ 1 (c ≥ 8: 8·9/72) | 72 (1) | – / – |
| D10 | 90 | 10 | 9 | 9 | 9 | 1 | 90 (1) | – / – |
| D12 | 132 | 12 | 11 | 11 | 11 | 1 | 132 (1) | – / – |
| D6 (#620's "E6") | 30 | 6 | 5 | 5 | 5 | 1 | 30 (1) | – / – |
| **E6 (corrected)** | 36 | 6 | 7 | 5 | **7** (5 and 6 UNSAT) | 7/6 | **35 (35/36)** | – / ≤ 5.69·10⁻⁵ (see below) |
| E7 | 63 | 7 | 7 | 7 | 7 | 7/9 | 49 (7/9) | 1.8468·10⁻³ (s = 11) |
| E8 | 120 | 8 | 9 | 8 | 9 | 3/5 | 72 (3/5) | 5.1598·10⁻³ (s = 5) |

("–" means D_s = (s − 1) − s·x ≤ 0 for every s ≤ 15.)

Findings:

- **E6 (corrected).**
  - The minrank is 7. ω = 5 (c = 5 and 6 are UNSAT), and #630's rank_F2(J+G) = 7 is attained.
  - The proxy deficit is negative, as #630 says.
  - The attainable label-decoder cost is 35 < 36, though: one total spans only 5 dimensions. That makes x = 35/36 < 1, so D_s > 0 for
    s > 36.
  - The ceiling there is negligible. max over odd s ≤ 801 of D_s/Cost_s is 5.69·10⁻⁵ (at s = 81), and D_s/Cost_s is an upper
    bound on X (#595 §A.2).
  - So the conclusion "E6 gives no useful saving" stands, but the reason is the tiny D_s/Cost_s, not D ≤ 0 at every s.
- **A_n and D_n.** x ≥ 1 under both the proxy (at the lower end of the minrank) and the attained label cost, so there is no saving
  in this screen. The D_n label decoders attain exactly x = 1 (D = −1).
- **E7 and E8.** These rows are unchanged from #620: X* = 1.8468·10⁻³ (E7) and 5.1598·10⁻³ (E8 120/72).
- **Scope.** The cst_lab column is an attained upper bound for label decoders on the B0 labels. A lower bound over
  all decoders is proved only for E8 (#595 C.6, S2). The "no saving" verdicts for A_n, D_n and E6 rest on #620's
  full-rank-totals premise; this table only recomputes them.

## 2. The triple family T_h (`triple.py`, checked)

This is the upstream Alon-type unit (`upstream/build/sections/03-motifs.tex`).

**Bit side.** Lines t_T, T ∈ C([h], 3), with the form I − J/9, so G_ST = |S∩T| − 1.

- The pattern requires B_TS = 0 where |S∩T| ∈ {0, 2}.
- The paper's centre decoder C_i is B0 = M Mᵀ mod 2, with c = h totals.

**Complex side.** Labels are t_T ∈ F2^h with the dot product.

- The pattern requires B_TS = 0 where |S∩T| = 1.
- The decoder is the h + 1 centres C_i and C_*, with B_ST = (|S∩T| − 1)/2 over ℚ(i).

**Copy cost (derived, not a proxy).** Total C_i gathers the C(h−1, 2) lines T ∋ i, and its readers are the same set.

| | bit | complex |
|---|---|---|
| span of a centre C_i | dimension h − 1 over ℚ (the functional 2x_i − Σ_{j≠i} x_j vanishes on it) | V_i = {x : Σ_{j≠i} x_j = 0}, dimension h − 1 over F2 |
| #446 Theorem C pairing rank of C_i | h − 1 (computed) | h − 1 for even h; h − 2 for odd h, because 1 + e_i ∈ V_i ∩ V_i^⊥ |
| C_* | – | costs h |
| **cst, attained** | **h(h − 1)** | **h²** |
| cst, Theorem C floor of the centre decoder | h(h − 1) | h² for even h; h(h − 1) for odd h |

**Minrank (bit).**

- For 8 ≤ h ≤ 11 the minrank is h (SAT).
- For h ≡ 0 (mod 4) it is h by the clique argument: ⌊h/4⌋ disjoint 4-sets give 4⌊h/4⌋ pairwise even-intersection triples.
- h = 6 and 7 give 6.
- Label decoders on the B0 labels have every gathered span of dimension ≥ h − 1 (`lab_min`, checked for h ≤ 11). So the centre decoder is
  optimal among them.

Certified ceilings (selected; every h from 6 to 32 is in `triple.json`):

| h | v | bit x = 6/(h−2) | **bit X*** | complex x = h²/C(h,3) | **complex X*** |
|---|---|---|---|---|---|
| 9 | 84 | 6/7 (window 8: the form is degenerate at h = 9) | 7.2457·10⁻⁴ (s = 15) | 27/28 | – (Theorem C floor: 6.358·10⁻⁴) |
| 12 | 220 | 3/5 | 3.3282·10⁻³ | 36/55 | 2.4187·10⁻³ |
| 15 | 455 | 6/13 | 6.4061·10⁻³ | 0.4945 | 5.3738·10⁻³ |
| 16 | 560 | 3/7 | 6.9611·10⁻³ | 0.4571 | 6.1233·10⁻³ |
| 18 | 816 | 3/8 | 7.5613·10⁻³ | 0.3971 | 6.9874·10⁻³ |
| 20 | 1140 | 1/3 | 7.7612·10⁻³ | 0.3509 | 7.3512·10⁻³ |
| **21** | 1330 | 6/19 | **7.7735·10⁻³ (max)** | 0.3316 | 7.4224·10⁻³ |
| **22** | 1540 | 3/10 | 7.7474·10⁻³ | 0.3143 | **7.4444·10⁻³ (max)** |
| 24 | 2024 | 3/11 | 7.6184·10⁻³ | 0.2846 | 7.3882·10⁻³ |
| 30 | 4060 | 3/14 | 6.9743·10⁻³ | 0.2217 | 6.8600·10⁻³ |

All maxima are at s = 3.

- **Bit side.** The triple family's ceiling exceeds E8's realised bit unit (6.0005·10⁻³) for every h from 15 to 32.
- **Complex side.** It exceeds E8's realised complex unit (5.1863·10⁻³) for every h from 15 to 32. At the
  attained cost the odd-h rows are slightly lower; at their Theorem C floor they equal the bit values.
- **S1's float screen.** It gave 7.4 / 7.2·10⁻³ at h = 24 with the proxy cst = h² / h(h+1). The derived cst is h(h−1) / h², and
  the certified values are 7.6184 / 7.3882·10⁻³.

## 3. Lorentzian I_{n,1} (`lorentz.py`, `lorentz_minrank.py`, checked)

The units are #634's triples e_A + e_{n+1} and pairs e_i − e_j, n odd.

- The binary labels (the 3-set, or the complement of the pair) fit the #595 pattern exactly: ⟨u_S, u_T⟩ = 1 + G_ST mod 2 (checked).
- The window is the Lorentz Gram rank n. #634 note 3 proves that n − 1 is impossible for n = 11, 13.

| unit | v | h | c (minrank) | ω | readers z per line | cst_lab (per total) | x | **X*** |
|---|---|---|---|---|---|---|---|---|
| I_{9,1} = E8 (control, quotient by the isotropic w) | 120 | 8 | 9 | 8 | 63 | 72 (8 each) | 3/5 | 5.1598·10⁻³ |
| I_{11,1} | 220 | 11 | **11** (10 UNSAT) | 10 | 115 (triples), 129 (pairs) | **110 (10 each)** | 1/2 | **7.1715·10⁻³** (s = 3) |
| I_{13,1} | 364 | 13 | ≤ 13 (ω = 12) | 12 | 183, 231 | **156 (12 each)** | 3/7 | **8.6247·10⁻³** (s = 3) |

Unlike E8, each total spans only h − 1 dimensions. That is where x < 3/5 comes from. Both ceilings exceed E8's.

## 4. Helper floors: the #595 §D method (`cover.py`, checked; one bound argued)

The method computes cover numbers at the source end: the fewest proper hyperplane sections of a source's readers T(s) that cover T(s).

| unit | readers | rank | cover number | evidence |
|---|---|---|---|---|
| E8 bit (control) | 63 | 7 | 3 | no 2-cover; best pair union 52; 3-cover found (= #595 D1) |
| T_h, h = 8 … 24 | 3·C(h−3, 2) | h − 1 | **2** | exact certificate: two rank-(h−2) subsets with union T(s) |
| I_{11,1} / I_{13,1}, pair-type sources | 129 / 231 | h − 1 | 2 | certificate |
| I_{11,1} / I_{13,1}, triple-type sources | 115 / 183 | h − 1 | ≤ 3 (no 2-cover found in sampling) | 3-cover certificate |

**Triple family, max section (argued; matches the search for h = 10, 12, 16, 20, 24).**

- **Setup.** For S = {1, 2, 3} and O = [h] \ S (n′ = h − 3), a section is {(a, {x, y}) : c_a + c_x + c_y = 0} for a functional c.
- **Constant c on O.** At most two of the three a-classes are covered, so the section has ≤ 2C(n′, 2) readers. If all three were
  covered, c would vanish on T(s).
- **Non-constant c on O.** Each a-class meets a "sum graph" with at most C(n′−1, 2) edges (n′ ≥ 6). That gives ≤ 3C(h−4, 2) readers,
  and c = e_z attains it.
- **Result.** For h ≥ 9 the max section is 3C(h−4, 2), the leftover is 3(h − 4), and the #595 floors are:
  - sink-only: R ≥ v − ⌊v/(3(h−4))⌋, about 0.98–0.99 helpers per port;
  - strict: 0.
- **Comparison.** E8 bit has 212 / 138, which is 1.91 / 1.24 per port.

**Conclusion of §4.** The design-free floors do **not** penalise these families; they are lower per port than E8's.
The §D method cannot rank them. Their helper cost is in the work per port: 630 readers per source for T_24 bit, against 63
for E8.

## 5. Helper-adjusted ranking (`est_model.py`, `rank.py`; model)

**Model.**

- **Base.** #595's per-port slot profile at window h.
- **Data runs.** Cut with the shipped run histograms: #555 x/y for bit, #569 four-cold for complex (#595 a4).
- **Helpers.**
  - ρ = R/v helpers per port, each climbing h per stage.
  - Cut with the shipped helper-run histograms (#555; #568 implied).
  - Hosted into the largest B_K idle slots first. A hosted slot of rank r leaves a remainder of rank r/a, as in #555's 42/28/14 → 6/4/2.
  - Mass beyond the hostable idle mass stays as extra children.
- **Root.** The same pressure root, at m = 1 + s(h−1) and D = (s−1) − s·x, with the best s.
- **Calibration.**
  - Bit: the model reproduces #555 to 0.3% (factor 1.0032).
  - Complex: the factor is 1.129, because #568's hosting is better than the rule above.
- **Piece-size scaling to larger h.**
  - abs: shipped absolute ranks (pessimistic).
  - rel: ranks scale with the window (optimistic).
- **Loss-chain factors.** #634's a ≈ (1/m)(D/W)/L_ent is reported per candidate in `rank.json`. It matches the root to < 1% at E8.

**Columns.**

- **ρ\*** is the break-even helpers per port: the ρ at which a candidate's estimate equals the E8 word of the same side in the same
  model (bit 1.8058·10⁻³ at ρ = 439/111 = 3.95; complex 1.6108·10⁻³ at ρ = 496/112 = 4.43).
- **ρ_dim** transfers E8's shipped intensity per reader per window dimension: ρ_E8 · (z/(h−1)) / (z_E8/(h_E8−1)).

| candidate | h | v | x | readers z | X* (certified) | **ρ\*** abs / rel | ρ_dim | a_est at ρ = ρ_E8, abs / rel | **a_est at ρ_dim**, abs / rel |
|---|---|---|---|---|---|---|---|---|---|
| E8 bit 111/63 (#555) | 8 | 111 | 0.5676 | 63 | 6.0005e-3 | 3.95 (ref) | 3.95 | 1.806e-3 | **1.806e-3** |
| E8 complex 112/64 (#568) | 9 | 112 | 0.5714 | 52 | 5.1863e-3 | 4.43 (ref) | 4.43 | 1.611e-3 | **1.611e-3** |
| **I_{11,1} bit** | 11 | 220 | 0.5000 | 118.5 | 7.1715e-3 | 2.66 / 3.34 | 5.21 | 1.480e-3 / 1.620e-3 | **1.225e-3 / 1.339e-3** |
| I_{13,1} bit | 13 | 364 | 0.4286 | 193.3 | 8.6247e-3 | 2.64 / 3.43 | 7.08 | 1.438e-3 / 1.647e-3 | 0.942e-3 / 1.079e-3 |
| T_13 bit | 13 | 286 | 0.5455 | 135 | 4.3818e-3 | 1.03 / 1.75 | 4.94 | 1.046e-3 / 1.198e-3 | 0.904e-3 / 1.026e-3 |
| T_12 bit | 12 | 220 | 0.6000 | 108 | 3.3282e-3 | 0.55 / 0.98 | 4.31 | 0.954e-3 / 1.070e-3 | 0.900e-3 / 1.009e-3 |
| T_14 bit | 14 | 364 | 0.5000 | 165 | 5.5852e-3 | 1.27 / 2.08 | 5.58 | 1.092e-3 / 1.275e-3 | 0.866e-3 / 1.001e-3 |
| T_16 bit | 16 | 560 | 0.4286 | 234 | 6.9611e-3 | 1.46 / 2.41 | 6.86 | 1.109e-3 / 1.340e-3 | 0.745e-3 / 0.898e-3 |
| T_20 bit | 20 | 1140 | 0.3333 | 408 | 7.7612e-3 | 1.20 / 2.43 | 9.44 | 1.029e-3 / 1.326e-3 | 0.533e-3 / 0.679e-3 |
| T_24 bit | 24 | 2024 | 0.2727 | 630 | 7.6184e-3 | 0.80 / 2.19 | 12.04 | 0.918e-3 / 1.248e-3 | 0.387e-3 / 0.517e-3 |
| T_16 complex | 16 | 560 | 0.4571 | 325 | 6.1233e-3 | 2.14 / 2.92 | 14.76 | 1.087e-3 / 1.270e-3 | 0.424e-3 / 0.490e-3 |
| T_22 complex | 22 | 1540 | 0.3143 | 1026 | 7.4444e-3 | 1.92 / 3.07 | 33.29 | 0.995e-3 / 1.265e-3 | 0.182e-3 / 0.229e-3 |
| T_24 complex | 24 | 2024 | 0.2846 | 1393 | 7.3882e-3 | 1.67 / 2.93 | 41.26 | 0.943e-3 / 1.230e-3 | 0.141e-3 / 0.181e-3 |

The full list (T_10 … T_30, both sides) is in `rank.json`.

**Answer to "is there a family that beats E8 on both the ceiling and the helper-adjusted estimate?" — no candidate in
this screen does.**

- **The ceiling.** Many candidates beat E8's ceiling: T_h for h ≥ 15 on both sides, I_{11,1} and I_{13,1}.
- **The helper-adjusted estimate.** Even at E8's own helper intensity per port (3.95), every candidate stays below E8:
  - the best is I_{13,1} rel at 1.647·10⁻³, against 1.806·10⁻³;
  - the break-even ρ\* is 2.6–3.4 helpers per port for I_{n,1} and ≤ 2.5 for the bit triples.
- **Why the break-even is implausible.** These units have 1.3–1.9× (I_{n,1}) and up to 3× (T_24) more readers per window
  dimension than E8, which ships 3.95.
- **Loss-chain view (#634).**
  - 1/m falls from 1/50 (E8, s = 7) to 1/91 (I_{11,1}, s = 9) and 1/162 (T_24 bit, s = 7).
  - L_ent rises from 3.19 to 3.79–4.46.
  - The smaller copy share x improves D/W by at most about 1.5×.
- **Ranking by a_est at ρ_dim.**
  1. I_{11,1}: 1.23–1.34·10⁻³
  2. I_{13,1}: 0.94–1.08·10⁻³
  3. T_12–T_14 bit: about 0.9–1.0·10⁻³
  4. larger triples, falling as 1/h
  5. complex triples: their readers grow like h³
- **Closest lead.** I_{11,1} beats E8 only if a design reaches ≤ 2.7–3.3 helpers per port on 118 readers per line. If
  its minrank had been 10, cst would have been 100 and X* 9.14·10⁻³. The minrank is 11 (c = 10 UNSAT).

**Model caveats.**

- The helper piece statistics and hosting rule are transferred from the E8 words.
- ρ for a new family is unknown; ρ\* is the honest output.
- s is free on both sides.
- None of this bounds κ.

## 6. Not done

- **Q3: a rigorous lower bound on the copy cost for the Gaussian and Eisenstein E8 views.** Not attempted beyond observing that the
  counting bounds available here are weak:
  - covering lines by flats gives 4;
  - the minrank gives 15 ≤ 0.25v;
  - the clique-matroid argument gives 12.
  S1's question (Σ_j dim span A_j ≥ 0.71v?) stays open.
- The exact minrank of A8 and D9 (SAT timeouts at c = 8). Not needed: x ≥ 1 either way.
- Exact max section and cover number for the triple-type sources of I_{n,1}.
- Punctures of I_{n,1}, which might help as 120 → 111 did for E8.

## Files

- `scripts/units.py`: exact line systems and ranks, the clique bound, and the time-limited gauged minrank SAT.
- `scripts/ade_screen_fixed.py`: §1; it replaces #620's `ade_screen.py`.
- `scripts/triple.py`: §2.
- `scripts/lorentz.py`, `scripts/lorentz_minrank.py`: §3.
- `scripts/cover.py`: §4.
- `scripts/est_model.py`, `scripts/rank.py`: §5.
- `scripts/check.py`, `expected.json`, `verify.sh`: recomputation.

## Credits

Builds on:

- DreamingOfClouds: #595 format limits (skel/cert/minrank_sat, §A, §D, a4 histograms) and #446 Theorems A–C;
- vectorsss: #630, the E6 correction;
- ShikeChen01: #634, the Lorentzian family and the loss chain;
- the upstream paper (03-motifs);
- jeremykothe2: #568;
- #555 and #569, whose shipped statistics are used;
- #620 (GamingPuzzled).

Prepared by Joel Pulikkan (GamingPuzzled) with Claude Opus 5.5 (Anthropic) via Claude Code. Apache-2.0.
