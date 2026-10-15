# Research notes (no κ claim): E8 decoder floors and #615/#617 cold-end levers

Negative results and one open lead, recorded so others don't repeat them. Scripts are included as they were run (paths reference a local scratch dir and `~/imb-src` pinned sources; Python 3.11 with numpy, scipy, sympy, python-sat, ortools). SAT results come from CaDiCaL via python-sat **without proof logs**. Nothing here is packaged with a verify.sh.

## 1. Unit screen (`ade_screen.py`; **superseded by `s3-unit-families/` §1**)

> **Erratum.** As #630 (vectorsss) points out, the "E6" row was D6 (30 lines). True E6 (the complement of an A2: v 36, h 6) has exact F2 minrank 7 and label copy cost 35 (x = 35/36), so X ≤ 5.69e-5: it is still useless. The c column here was rank_F2(J+G), which is only an upper bound; the exact minranks are in `s3-unit-families/`. E7 and E8 are unchanged.

Real ADE root systems as units (v lines, window h = rank, c = F2 rank of (J+G) mod 2, proxy x = c·h/v, ceiling via #595's `skel.X`): only E8 gives a useful ceiling. E7 (v 63, h 7, c 7) reaches X* ≈ 1.84e-3; A_n, D_n and E6 have x ≥ 1 and give no saving. X scales roughly as 1/h, consistent with the Leech (#598) and Niemeier (#606) losses.

## 2. E8 decoder floors (`s2-decoder/`, details in `REPORT.md`)
- **P111 (shipped bit puncture 39,52,57,71,76,78,103,109,114):** the 9-total F2 decoder is unique (= B0 on the live lines); 8 totals is UNSAT (`uniq.py`).
- **#446 Theorem C floor = star floor** on all realised units checked: P120 bit 72 (all 511 reader sets span Q^8, `t1.py`); P111 bit 63 (exact SAT over all label-decoder decompositions: cost ≤ 62 UNSAT, 63 SAT; `run62.py`, `dec9sat.py`, `p111c.py`); P112 complex frame decoder 64 (`cxp.py`). Decoders differing from B0 off-pattern (rank ≥ 10) are not covered.
- Where slack would have to come from: a total whose readers lie in a hyperplane orthogonal to a punctured line can drop to that line (cost 6 for orthogonal punctured pairs). It does not get P111 below 63.
- Deeper punctures (annealing, 9–26 lines removed), sub-root-system units (D8, E7+A1, A8, …) and mixed units with non-root ports (≥ 14 lines must be removed; best x ≥ 0.67) are all worse. Search results, not exhaustive. Exact W(E8) hyperplane orbit counts: E7 120, D7 1080, E6+A1 3360, A7 8640 (`hyper.py`).
- Asymmetric sinks on P112: 0 of 28,560 target/sink pairs relax for free (floating-point rank, `asym.py`); one extra copy unit frees 2 sinks (matches #595 C.6). Pricing (argued): ≤ 2 × 4.4 helpers × 0.143% ≈ 1.3% b < 2.82% per copy unit, so net negative.

## 3. Levers on #615 / #617 (`r1-cold14/`, details in `REPORT.md`)
Measured on #615's words (#615 re-verified locally: κ 0.001626010676080313):
- **"e2" entering ends are infeasible** at all three Lean (E,U) pairs of #593: the row-cone left-nullity equals the number of helpers already ended (12/24/12) on jp8 and atm3. Cold-mixing directions (542/543/554/555, 566/567/578/579) have no column-cone solution (`nulls.py`, `broad2.py`, `probe2.py`).
- Extra cold dim-8 hyperplane ends all lose (best −5.67e-9 b per call). E1 partners 438/440 can't be replaced by already-lifted registers.
- No PR583-type frame coalescences on jp8, with or without commuting gate moves (the same scan finds #583's six on atm3) (`coal*.py`, `movecoal.py`).
- #615's owner map + dispatch equals the aggregate LP optimum over {jp8, atm3}, even with unlimited windows (`aglp.py`).

**Open lead on #617 (κ 0.001635183729255778):** #617's owner solve stopped at its time limit with remainders {1:24, 2:2, 3:2, 7:2}. The aggregate LP bound (`aglp617.py`) is **+119.3e-9 b** above #617's map at fractional dispatch jp8 60.9 / atm3 11.1. An integer packing at jp8×61 / atm3×11 that meets the bound would give about **+1.1e-7 κ**. `mip617.py` (free-dispatch MIP with Hall constraints) and `expand617.py` (to OWNERS/PLAN) are included; the integer packing is not yet solved or verified.

## Credits
Builds on jeremykothe2 (#591–#601, #607–#617), DreamingOfClouds (#595 format limits, #604, #610), chafreaky (#583, #616), #446 (Theorems A–C), eumemic (#543) and the contributors listed in those PRs. Prepared by Joel Pulikkan (GamingPuzzled) with Claude Opus 5.5 (Anthropic) via Claude Code. Apache-2.0.

## 4. E8 over extension rings and K12 (`s1-extension-rings/`, details in `REPORT.md`)
On the bit side ranks are counted over Q, so a K-line unit is a rank-k unit with k = [K:Q] and h = k·w_K (argued). Exact F2 minrank of the decoder pattern, asymmetric decoders allowed (SAT, no proof logs):

| view | lines v | w | largest non-orthogonal set | minrank | v/w |
|---|---|---|---|---|---|
| Gaussian E8 | 60 | 4 | 12 | 15 (13, 14 UNSAT) | 15 |
| Eisenstein E8 (Witting) | 40 | 4 | 7 | 10 (7–9 UNSAT) | 10 |
| Hurwitz E8 | 10 | 2 | 5 | 5 | 5 |

- In every extension view, minrank = v/w. Real E8's cross-field gain (minrank 9 < 120/8) disappears. Under the full-rank-totals premise that #595 uses for E8's 72, x_K = 1.0, so D ≤ 0: no saving.
- Copy-cost searches (CP-SAT, 900 s, not proven optimal): Gaussian best 60 (proven lower bound only x_K ≥ 0.15); Eisenstein best 40 (x_K ≥ 0.225). Hurwitz symmetric decoders: optimum 10 (x_K = 1). Hurwitz asymmetric decoders: open.
- **Open question:** a structural lower bound Σ_j dim span A_j ≥ ~0.71·v for these units (the threshold to beat bit E8's ceiling at w = 4, float screen). This has the same open status as E8's 72.
- G34 / Coxeter–Todd K12: 126 lines, w = 6, largest non-orthogonal set 15, so x_K ≥ 0.714 even at minrank 15; it loses.
- Complex side (argued): F4-Hermitian (Eisenstein) labels give an alternating F2 trace form, so there are no odd-norm residuals and the phase calculus fails. Gaussian labels reduce mod (1+i) to F2, so they bring no extension.
- Side finding (float screen only, not certified): the paper's original triple family has a higher X* than E8 (~7.4e-3 bit, ~7.2e-3 complex at h = 24, s = 3), but 630 orthogonal neighbours per target (vs 63 for E8) makes its helper cost the issue. X* alone does not rank unit families.

## 5. Beyond E8: triple and Lorentzian families (`s3-unit-families/`, own README and `verify.sh`, 114 PASS)
- Certified ceilings above E8's: the paper's triple family T_h (bit cst h(h−1), max X* 7.7735e-3 at h = 21; complex cst h², max 7.4444e-3 at h = 22) and the Lorentzian units of #634: I_{11,1} (minrank exactly 11, cst 110, x = 1/2, X* 7.1715e-3) and I_{13,1} (cst 156, x = 3/7, X* 8.6247e-3).
- Helper-adjusted (model, calibrated to #555 within 0.3%, not a bound): no candidate reaches E8's estimate, even at E8's 3.95 helpers per port. To break even, a design would need ≤ 2.6–3.4 helpers per port for I_{n,1} (≤ 2.5 for bit triples). The best lead is I_{11,1}; next steps are its punctures (the analogue of E8's 120 → 111) and a real helper design.
- #595 §D helper floors don't separate the families: the triple family has cover number 2 (exact certificates up to h = 24).

## 6. Dispatch and cold-end pricing on the #639 lineage (`r2-dispatch/`, details in `REPORT.md`)
- Exact prices at concentrated idle (PR568 `moment.certify`): #639 b = 0.0016391439889600812; 72×jp8 b = 0.0016392558 (not admissible, since the global controls need two dispatched providers); 71 jp8 + 1 st2 (#635's jp8 word as the second provider) b = 0.0016392519, i.e. **+1.08e-7 b** from removing the forced ck call. #643 (jeremykothe2) later realised this twin dispatch independently.
- Exact sub-MIP obstruction: with jp8 at t = 5 and every window not touching t ≤ 7 held fixed, the optimum leaves 64 idle-3 owners, so no perfect packing exists in that neighbourhood. Once ck's 9+7 pairs are gone, the early windows are the tight ones.
- Mass-neutral V pricing per end per call (V639.json): u4-type premix-only dim-8 ends ({1:+2, 2:−1, 4:+1, 5:−1}, width −1) ≈ −0.025, essentially neutral, consistent with #637's 23 LP-negative candidates. **Dim-7 factored end pairs (#627 type) ≈ +2.25 per pair: the positive direction.** This should carry over to the gauge44 lineage (#645 onward) and was not searched here.

## 7. I_{11,1} / I_{13,1}: punctures and helper structure (`s4-lorentzian-helpers/`)
Status: `expected/` is frozen from the complete run1 (all steps finished; the k = 19 SAT runs take ~2 h). No second fresh run has been done yet.
- **Punctures never help the centre decoder** (exact matroid-partition certificate). The 220 lines of I_{11,1} split into 22 independent sets, 2 inside each centre reader set, so the cost is ≥ |L|/2 for every live set L. For I_{13,1}, three copies of the lines split into 91 sets, giving ≥ (3/7)|L|. Every label decoder satisfies x ≥ 1/2 for |P| ≤ 8 (x ≥ 3/7 for |P| ≤ 10 on I_{13,1}).
- **Minrank stays 11** after ≤ 19 punctures for **all 5** maximum-clique S_11-orbits (SAT, no proof logs; orbit 0 UNSAT in 7,484 s). So any 10-total decoder needs ≥ 20 punctures. The 38,786 maximum cliques fall into 5 orbits, and a union bound shows any ≤ 21 punctures leave one alive.
- **Helpers.** E8's R = 439 is 240 carriers (3 branches per source, forced by E7 being a 4-design) + 180 cell registers + 9 totals + 10 puncture carriers. In I_{11,1}:
  - triple sources also need ≥ 3 branches in any frame design (exact quadratic-form nullspace);
  - the cell cover number is 3;
  - 20,790 good 4-frames exist, but **no partition into good 4-frames exists**: every good frame holds 0 or 2 pairs, and there are 55 pairs.
  - Needers cover 56–70 lines, against 30 in E8.
  - The transferred cell skeleton has 787 helpers (3.58 per port), or 732 (3.33 per port) with 2-branch pairs. The calibrated model gives a_est 1.58–1.81e-3, against E8's 1.806e-3: no robust gain without a new middle network.

## 8. Why "no new kappa" construction savings cannot move κ (R5 triage, 2026-10-13)
κ depends only on (i) the complex paid rank profile H = calls × local_paid + idle and the live stock W (b is the moment root of Σ_r r·n_r·(73/r)^b = 73W), and (ii) the bit profile (c). Primitive, ADD and XOR counts enter only finite admission checks, all with large slack: local_primitive_bound < 2^48, prefix < payload, row < 20161, and so on. The outer row gap also uses the fixed 20161.
- #883, #916, #901, #917, #919, #922, #882, #932, #937 and #945 each leave the paid children, helper widths and phase events unchanged, so the gain is exactly 0. Several act on historical CK/JP8/X4 words rather than the selected U8 word.
- Bit savings (#914, #915, #908, #904, #891, #713, #884, #936, #941) leave c unchanged. c = 0.0017334 > b ≈ 0.0016647, so the bit side doesn't bind anyway.
- #892 (rank-8 coded helper) does change the local profile, but it is excluded by its own packing obstruction on the old word.
- The only path from these savings to κ is a lower local prefix bound, which allows more replicas. Raising the charged payload does that directly: row slack 3,692 allows payload up to ~2,350, which is what T37 (#942) uses.
- **Next real lever:** dim-7 factored end pairs (#627 type, local {1:+2, 2:+2, 5:−2}, width −4) on the U8 word. Priced at ideal packing, each is worth about **+1.7e-7 b per pair per call**, about 60× the T37 gain.

## 9. Exhaustive local-rewrite search on the fused X54 words (`r7-fusion-search/`, 2026-10-13)
**Search target:** the composed words of #1239/#1218: #1193's mixed T37 construction with #1195's source-holder fusions and #1130's X54 slot. JFX is the joint-entrance provider and D4FX its group-627 variant. Prices are exact, from #1186's frame toolkit (b = #1094 cost units): X54 = −1,788 and the two fusions = −4,338 on the joint word.

**Frames:** the exact frame optimum of both words equals their published profiles, so frame changes have no slack left.

| family | candidates per word | feasible | gains |
|---|---|---|---|
| every read fusion × {B-after, B-before-next, tail, prepend} restores × {none, single/pair swaps, full exchange} (#1186 `repair.py`) | 2,238 fusions / 2,850 pricings | 969 | **0** |
| standalone SW4 read-set exchanges (all non-empty subsets per copy pair) | 50 | 0 (cone cap "L not inside U" at end-of-B target vertices) | 0 |
| #1186 `joint.py` triangle-hybrid family | 161 (JFX/D4FX); 259 on the fusions-only word | 24 | 0 |
| `joint2.py`: generalised slots over all donation/restore gap classes, with keep/swap/fuse per movable read (reproduces X54 exactly in 120 equivalent variants), non-target holders | 3,924 | 0 | 0 |
| a fusion analogue at the X54 site (in place of the slot) | 45 touching 54/589 | 4 | 0 (best +956, worse than the slot) |
| `joint2` with target holders (+2,940 per word) and `fusion2.py` (10,603 generalised fusions on JFX) | — | **partial**: stopped before completion | none found |

**Conclusion (scoped):** on these words, no further width-neutral source-holder fusion, read exchange or triangle slot of the searched families gains. The remaining κ gains in the lineage come from other mechanisms, notably #1274's helper-donor cold kernels. (**Correction, 2026-10-13:** an earlier version also cited the idle-overlay exchanges of #1268/#1280. The author has since closed #1268, #1280, #1305 and #1324 as invalid, because those moves shift axes between idle children of different (pair, side) families whose DATA-PHASES fix the Z4 multiplier; see #1286. The valid frontier is #1319/#1424.) Scripts `joint2.py` and `fusion2.py` extend #1186's exact-frame toolkit (credit mdumitrean #1186/#1195), which is not re-vendored here.

## 10. Extension-ring E8: copy-cost floors over every decoder (`s5-extension-ring-floors/`, `verify.sh` ALL MATCH)
This follows up §4, where S1 obtained x_K = 1 only under the full-rank-totals premise. Here every F2 decoder on the orthogonality pattern is covered: any number of totals, asymmetric pairings, no star premise. Costs are #446 Theorem C costs Σ_j β_j.
- **Eisenstein / Witting (40 lines, w = 4): Σβ ≥ 40 = v for every decoder, so it is excluded** (checked plus proof).
  - Sum-rank step: Σβ ≥ rank(G∘N), where N counts the totals covering each pair.
  - If every line lattice span(T) ∩ E8 has odd determinant, G∘N reduces mod 2 to an invertible block-diagonal matrix. The Witting line lattices are A2 (det 3); the Hermitian diagonal 2+ω is a unit at the inert prime 2.
  - Real E8 escapes this because its line lattices are √2·Z (det 2). That is consistent with 72 < 120.
- **Hurwitz (10 lines, w = 2): minimum over all decoders = 10 = v, so it is excluded** (checked plus a König/rank proof). The reduced SAT is UNSAT at cost ≤ 9, and the frame decoder attains 10.
- **Gaussian (60 lines, w = 4): Σβ ≥ 40 for every decoder (x_K ≥ 2/3, checked).** Not yet excluded: the float screen says x = 42/60 would still beat bit E8's ceiling (X* 6.33e-3), while 43/60 would not (5.66e-3).
  - How the 40 is proved: 640 twelve-line cliques each force B[C,C] = I₁₂, and hits ≤ 192·rank holds on all 2271² flat pairs.
  - The 2-adic method caps at 12, and an LP over clique families stays at 40.
  - The best known decoder costs 60. A decoder at ≤ 42 would need ≥ 16 totals with at most 10 of full rank.
  - **Open:** close the window 40–42. A pending SAT (`gauss_c15.py`) would show that every 15-total decoder costs exactly 60.

## 11. Helper-donor cold-kernel census on #1319's word (**scope limited; see §12**) (`r8-cold-kernel-census/`, 2026-10-13)
**Base:** #1297/#1319's four-kernel base word (byte-identical to the one #1319 uses), κ 0.001676855229071321. #1305 and #1324 were withdrawn as invalid (#1286), so the idle-axis overlay is not used.

**What a kernel is:** a cold pivot q (still at its rank-one start frame) has early B reads `t += k·q`. A kernel deletes them and repairs exactness with one or two shocks: a cut (`h += a·q`, undone in early cleanup) or a hook (`s ± c·q` around a donor read). The coefficients come from an exact rational equation.

**Admissibility:** the scalar map is unchanged mod p, the cone caps hold, and #1186's exact frame solver finds feasible frames.

**Why kernel 555 gains:** deleting reads merges the consecutive climbs of targets 187 and 483 (H1 −3, H3 +1, cost −11,676).

**Control:** restricted to pivots 531/543/555/567 on the #1286 word, the census recovers exactly #1297's 5 + 5 relations, each −11,676.

| family | candidates | admissible | gains |
|---|---|---|---|
| #1297's family, all 376 pivots with early uses | 254 | 99 (all Δ0) | **0** |
| G: cuts after any read or at B start, hooks around any early add gate, 1–2 shocks, every subset of early uses | 9,916 at 248 pivots | 1,435 (Δ0 or +4,913) | **0** |
| K2: two shocks of the same type, 15,507 new (**13,402 priced**) | 13,402 | 4,346 (Δ0 or +4,913) | **0** |
| 3-shock spot check (pivots 554, 448) | 12 | 0 | 0 |

The dominant failure is "L not inside U", at the early-cleanup restore or at the end-of-B cone caps. The (output, output, helper) three-read pattern that the four kernels use occurs only at 531/543/555/567, which are already spent.

**Not done:** 2,105 K2 candidates, pricing on the extra word, a full 3-shock census, and 3,066 gate-retiming candidates (generated by `retime.py`, unpriced; they target the same climb-merging mechanism directly).

## 12. Supplier census on the current pivot-566 + 554 T74 word, and why §11 missed those kernels (`r9-supplier-census/`, 2026-10-14)
**Why this matters:** at #1800's ε → 1 outer point, κ ≈ the complex supplier endpoint b, so only supplier gains move κ.

**Word and controls.** The words are #1800's `new/{gauge44,extra}-word-566.json.gz`, identical to #1672/#1957. Our pricer reproduces their profiles, gauge44 {1:2348, 2:500, 3:416, 4:130, 5:82} and extra {1:2340, 2:508, 3:420, 4:126, 5:82}, and prices #1672's k554 edit at Δ −1,850.

**Correction to §11.** Its families G and K2 allowed only paired shocks, at most two per relation: a cut restored at the end of early cleanup, or a hook around one gate. The 566 and signed-554 kernels are 5–7-term relations built from three things those families lacked:
- unpaired direct reads `x += c·q` that are never undone;
- windows closed in early cleanup right after q's own restoration (the "signed restore" reads q while it holds −q0);
- donor windows spanning many gates.

The right family is the span of reads `x += λ·y` wherever y holds a multiple of the deleted value; this is #1957's gencomp2. Positive controls: it recovers 566 (delete B755 on the #1319 word) and signed 554 (delete B342 on step 0), each at −1,850.

#1957 (rohanarun) already ran that family on the current word, with 0 gains. The extensions here also find nothing:

| run | coverage | gains |
|---|---|---|
| E1: several reads of the same value deleted together | 128 / 330 | 0 (all infeasible) |
| E2: relaxed frame-cost budget (+4,913) on 24 small-gain reads, incl. 858/876 not in #1957 | 24 / 24 | 0 (only trivial Δ0 slot moves) |
| E3: retime every B add to both ends of its commuting window | 3,074 / 3,074 | 0 (2,068 ok at Δ0, 1,006 infeasible) |
| E4: new two-value holder family (`gencomp3.py`; reads of holders of v+u with u cancelled, exactness on matrix entries, no insert feeding a later insert) | 144 / 1,002 (small-gain, mid and largest-gain bands) | 0 (126 shape-infeasible, 18 CP-infeasible) |

E4's control recovers 566 plus new exact two-value variants at −1,850. A reversed-constraint bug in gencomp3 was found and fixed mid-run, and the affected results were rerun.

**Not covered:** the rest of E1 and E4, three-value holders, multi-deletions across different values, A-section edits, and the extra word. The negative results suggest further supplier gains need changes outside B-local kernels, such as the A-section or the parent/centre interface.

## 13. Gaussian E8: every 15-total decoder costs exactly 60 (`s6-gaussian-c15/`, 2026-10-14)
This answers §10's open question G2.

**Reduction (argued).** Take a valid 15-total decoder B = W·Uᵀ over F2. If supp(Wx) lies in a 3-flat H for some x ≠ 0, then on O = the lines outside H we get W[O]x = 0. So B[O,O] has rank ≤ 14 and still obeys the decoder pattern. It therefore suffices to show that the induced pattern on O has F2 minrank ≥ 15 for every 3-flat H; the U side follows by transposition. Then every total spans K⁴, so β_j = 4 and the cost is 60.

**Symmetry (checked).** The 60 complex reflections preserve the lines and their non-orthogonality, and generate a group of order **11,520**. The 1,500 3-flats fall into **3 orbits**: 60 of size 15, 480 of size 6 and 960 of size 4.

**SAT (checked, no proof logs).** On the complement of each orbit representative (45, 54 and 56 lines), c = 14 is **UNSAT** with all three of CaDiCaL 1.5.3, Glucose 4 and MapleChrono, in 5–123 s. Calibrations: c = 15 is SAT on every O, and on all 60 lines c = 14 is UNSAT and c = 15 is SAT. The previous monolithic encoding ran for 18 h without an answer.

**Group-free cross-check** (every 3-flat individually, no symmetry used): **complete: all 1,500 UNSAT** ("ALL AS EXPECTED", `logs/prove_all.log`).

**Side lemma (argued).** For a c-total decoder and any family of flats, at most c − minrank(pattern on the complement of their union) totals have R_j inside the union (and likewise for A_j).

**Consequence:** a Gaussian decoder costing ≤ 42, which would beat real E8, needs **≥ 16 totals**. The lower bound of 40 from §10 is unchanged. The 16-total case is being checked with this multi-flat argument.

## 14. Gaussian E8: no 16-total decoder costs ≤ 42 (`s7-gaussian-c16/`, `verify.sh` reproduces `expected.txt`, 2026-10-14)
Together with §13, a Gaussian E8 decoder that beats real E8 (cost ≤ 42) needs **≥ 17 totals**.

**Proof chain** (k = number of cheap totals, β_j < 4):
1. **Cost types (argued).** β_j = dim X − dim(X ∩ Y^⊥). The cheap types are:
   - *a*: a side of dim ≤ 2 (β ≥ 0);
   - *p*: a (3,3) "dumbbell" with β = 2;
   - *q*: everything else (β ≥ 3).

   Cost ≤ 42 at c = 16 forces **3a + p ≥ 22 − k**.
2. **Multi-flat rank drop (argued; generalises §13).** Choose one legal 3-flat per cheap total. Then for every subset J, the minrank of the pattern on the complement of their union is ≤ 16 − |J| (a "level-k" set).
3. **Level tables (checked; orbit reps under the order-11,520 group).**

   | k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   | reps | 3 | 28 | 120 | 368 | 498 | 464 | 315 | 206 | 124 | 74 | 32 | 24 | 10 | 6 | 1 | **0** |

4. **(A) checked:** *a* = 0 whenever k ≥ 5.
5. **(B) checked:** the most jointly valid dumbbells are p* = 5, 4, 3, 2, 1 for k = 11..15, against the 11, 10, 9, 8, 7 needed.
6. **Arithmetic.** For k ≤ 4, 3a + p ≤ 3k < 22 − k. For 5 ≤ k ≤ 10, p ≤ k < 22 − k. For 11 ≤ k ≤ 15, p ≤ p* < 22 − k. For k = 16, no level-16 set exists.

**Checks.**
- All 200 UNSAT prunings were re-solved with Glucose 4: 0 mismatches.
- The fast canonicaliser matches the slow one on levels 2–4.
- A from-scratch `verify.sh` matches exactly; `CROSS=1` adds the Glucose re-solve.
- Calibrations: c = 16 without a cost cap is SAT, and the decoder found prices at 64; c = 15 reproduces §13.
- Side result: at most 2 totals can have a side of dim ≤ 2.
- Related scoped results: #767, #2066.

**Caveat (found in §15):** the fast canonical key in `levels2.py` can overflow int64 for k > 10, so in principle a pruning could be wrong. No mismatch was observed, and §15's Theorem 1 re-proves the c = 16 result independently (cost ≥ 44) without level tables or SAT.

## 15. Gaussian E8 for every c: cost ≥ max(40, 60 − c), and c = 18 excluded (`s8-gaussian-all-c/`; `verify.sh` about 6 min, exact arithmetic)
- **Theorem 1 (checked).**
  - On all 2271² flat pairs, the maximum clique hits by rank are 0, 192, 384, 512 and 640 for ranks 0–4. Their concave envelope has two facets: h ≤ 192·R and **h ≤ 128·R + 128**.
  - Summing the second facet over the c totals: 7680 ≤ 128·cost + 128·c, so **cost ≥ 60 − c**.
  - Hence every decoder with c ≤ 17 costs ≥ 43. This **settles c = 17** and re-proves §14 (c = 16 gives ≥ 44) without SAT.
- **Theorem 2 (checked): c = 18 is excluded.**
  - At c = 18 and cost ≤ 42, every clique is hit exactly 12 times and every total is tight.
  - All 1,081 tight flat pairs miss exactly the cliques M·x_t, where x_t is a set of pairwise-orthogonal lines.
  - So Mμ = 6·**1** with μ integral. M is the 640×60 clique/line incidence matrix, of exact rank 60, so μ = ½·**1**: a contradiction.
- **Theorem 3 (checked): the tight face cost = 60 − c never occurs.** It would need μ = (c − 12)/12. Hence c = 19 requires cost ≥ 42 (only cost = 42 is open) and c = 20 requires cost ≥ 41.
- **Facts for all c (argued).**
  - Cost-0 totals can be dropped, so WLOG c ≤ 42.
  - At most 3 totals are full rank and at most 6 have β ≥ 3.
  - At most 2(c − 18) totals have rank 1.
- **Why counting alone stops here.**
  - The LP over cliques of every size, lines, flat complements and a free c-term gives exactly max(40, 60 − c).
  - An **integral** cover exists from c = 21: 21 dumbbells (ℓ^⊥, m^⊥) with ℓ ⊥ m, of total cost 42, hit every clique 12–16 times (checked).
  - So excluding c ≥ 21 needs the F2 decoder pattern itself, not counting.
  - CP-SAT covering ILPs for c = 19 and c = 20 returned UNKNOWN.

**Status of the Gaussian question.** A Gaussian E8 decoder that beats real E8 (cost ≤ 42) needs **19 ≤ c ≤ 42** totals of nonzero cost. At c = 19 only cost exactly 42 is open, and at c = 20 only 41–42.

## 16. Gaussian E8: c = 19 excluded; c = 20 partial (`s9-gaussian-c19/`, 2026-10-15)
- **μ-packing theorem (checked: HiGHS exact-optimal, and CP-SAT for capacities 7 and 8).** Tight totals miss exactly the cliques M·x_t (§15). Over μ ∈ ℤ≥0^60 with Mμ ≤ cap, the maximum |μ| for cap = 6..12 is **28, 32, 36, 42, 48, 52, 60**; the LP allows 5·cap. Consequences:
  - an all-tight decoder costs ≥ 44 for every c ≤ 20;
  - at c = 21 the requirement equals the maximum (42), which is exactly S8's 21-dumbbell cover.
- **c = 19 is excluded (checked, HiGHS MIP dual bounds; floating point, not exact certificates).** Non-tight totals are handled by a case split over the 27 rank-maximal type orbits with deficit ≤ 256. All 20 lifted cases are excluded: each best value is ≤ 32 with a dual bound ≤ 33, against the 34 needed. **Hence no 19-total decoder costs ≤ 42.**
- **c = 20 is partial.**
  - At cost ≤ 41: 6 cases are excluded and cases 6 and 9 timed out.
  - At cost ≤ 42: cases −1 and 21 are excluded; cases 19, 22 and 23 timed out, and the heavy cases (20k–54k columns) were not run.
- **c ≥ 21 (argued, partly checked).** Counting is exhausted. However, the c = 21 covers that counting allows are **F2-infeasible** (0.1 s SAT). The minimal core is a non-orthogonal pair {a, b}: one total covers both diagonal entries while another gives only an off-diagonal entry. S9 classified the exact 2×2 support lemma into 17 minimal feasible patterns; `pair_ilp.py` (all-dumbbell plus the lemma) is written but not run.

**Status of the Gaussian question:** a decoder that beats real E8 needs **20 ≤ c ≤ 42**. c = 20 is partly excluded, and c ≥ 21 has a candidate F2 route.
