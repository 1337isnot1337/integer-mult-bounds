# Label-field census: rank-k labels and other lattices do not beat E8 (no κ claim)

Rohan Guliani (@Rohansguliani), 2026-10-13. Apache-2.0. Prepared with substantial AI assistance (Mux agent); every
number below comes from `census.py` and the certified roots of `research/format-limits-corrected`.

**This package makes no κ claim and ships no word.** It tests one structural change: replacing the rational E8 label
geometry with a label field of higher rank per port. It finds that this change does not help, and records where it fails.

## Question

The selected result has κ = 0.001635527380375392. Two observations about where that number comes from:

1. **The outer assembly is already saturated.** With the binding complex supplier
   a = 65528268492323474503/4·10²², the exact value a/(1+a) equals the selected κ to a relative 1.4·10⁻¹⁶.
   a/(1+a) is the balance of `min(1−ε, εq)` ([assembly-domain audit](../../docs/research/assembly-domain-audit.md)).
   Changing the ring, the transform length, the Gaussian resampling or the Fürer / Schönhage–Strassen /
   Harvey–van der Hoeven outer layer acts only through this conversion. It can therefore raise κ by at most a factor
   1+a ≈ 1.0016. A meaningful factor has to come from the supplier saving a.
2. **Inside the B_K format the saving is capped by the unit.** Section A of
   [format-limits-corrected](../format-limits-corrected/README.md) proves a ≤ X(s, h/k, x/k): the ceiling depends only
   on the stage count s, the window per label rank w = h/k, and the copy cost per port and label rank x/k. On the realised
   units this gives κ ≤ 5.16·10⁻³, so κ > 0.01 needs a unit with a smaller w or x.

A structural lever that the format theorem leaves open is the **label field**. E8 also carries a Z[ω]-lattice structure
(the 40-line Witting configuration in Q(ω)⁴) and a Hurwitz structure (10 quaternionic lines in H²). Labels over those fields
are rational labels of rank k = 2 and k = 4 inside the same 8-dimensional window, so w drops from 8 to 4 or 2. At w = 4 the
ceiling clears 1/99 whenever x/k ≲ 0.624 (s = 5, float bisection), while the frontier units have x ≈ 0.57. On these window numbers alone
the change looks like a factor of two.

## What fails

The copy floor rises faster than the window falls. For a coordinate-total decoder, N_TS ≠ 0 exactly on non-orthogonal
pairs. Requiring B_TT = 1 and B_TS = 0 there forces B[K, K] = I on every clique K of pairwise non-orthogonal lines inside
a total. So each total costs at least the largest such clique in its support, and x ≥ x_lb = Σ cliques / v. The
census computes these quantities exactly and feeds x_lb to the certified ceiling `skel.X`. Because X is non-increasing
in x, the X column is an upper bound for every decoder of that type.

| configuration | field, k | v | n = h/k | ω (max non-orth clique) | support cliques | x_lb | certified ceiling X |
|---|---|---:|---:|---:|---|---|---|
| E8 root lines, Hamming frame | Q, 1 | 120 | 8 | 8 | 8 × 8 | 8/15 | ≤ 8.009·10⁻³ (s = 3) |
| E7 root lines | Q, 1 | 63 | 7 | 7 | 7 × 7 | 7/9 | ≤ 1.847·10⁻³ (s = 11) |
| D4 root lines | Q, 1 | 12 | 4 | 3 | 4 × 3 | 1 | no positive saving |
| F4 root lines | Q, 1 | 24 | 4 | 5 | 4 × 5 | 5/6 | ≤ 2.155·10⁻³ (s = 13) |
| **Eisenstein E8 (Witting)** | Q(ω), 2 | 40 | 4 | **7** | 4 × 7 | 7/10 | **≤ 6.335·10⁻³** (s = 7) |
| **Hurwitz E8** | H, 4 | 10 | 2 | 5 | 2 × 5 | 1 | **no positive saving** |

For calibration, the same engine gives 6.000·10⁻³ for the realised bit unit (h = 8, x = 63/111) and 5.186·10⁻³ for the
realised complex unit (h = 9, x = 64/112). The complex-side analogue of Witting is worse: its F₄ window is at least ω = 7,
and at x ≥ 7/10 it gives at most 3.274·10⁻³.

Reading of the table:

- **Witting.** The window halves (w = 4), but 7 of the 40 lines are pairwise non-orthogonal inside each coordinate support.
  E8 has 8 such lines in 8 dimensions; Witting has 7 in 4. Compared lower bound against lower bound, Witting
  (6.33·10⁻³) is below E8 (8.01·10⁻³). It is only 5.6% above the realised E8 bit unit, and only if its decoder attains
  the clique bound. The realised E8 decoder does not: P120 costs 72 against its clique bound of 64.
- **Hurwitz.** Every line is orthogonal to exactly one other, so the non-orthogonality cliques cover the ports. Then x ≥ 1
  and D_s = (s−1)k − s·x < 0: there is no saving at any s.
- **Rational alternatives (D4, F4, E7)** are all worse than E8. E8 is the only configuration here whose non-orthogonal
  clique does not exceed its dimension, and that is why it is the best unit.
- **κ > 0.01 is out of reach for this decoder type.** Even E8 with a coordinate-total decoder at its clique bound
  (x = 8/15) has ceiling 8.01·10⁻³ < 1/99. Section A.7 of format-limits records the copy charge as the largest single
  multiplier (×6.9). This census adds that choosing another lattice or label field does not lower it.

## Consequence for the stretch goal

Under the current format, a different lattice or label field does not give the factor of six needed for κ > 0.01.
What remains open is the scope this census excludes. It is the same list the format theorem leaves uncovered:

1. **Decoders without coordinate totals.** Totals whose reader and source sets avoid large non-orthogonal cliques could
   escape the clique bound. #446 Theorem C's pairing-rank floor then still applies.
2. **Non-B_K schedules**, which change (Sch) and (Dfc).
3. **A different deficit identity (P)**, for example networks whose endpoint is not a two-bank exchange.

A useful next target is a quantitative version of item 1: a lower bound on Σ_j rank B[R_j, A_j] over all
decompositions N = Σ_j r_j a_jᵀ with the E8 pattern. If that bound is at least 0.476·v at h = 9 or 0.499·v at h = 8
(the copy ratios at which the ceiling reaches 1/99, from the same `skel.profile`), then units with those windows cannot
reach κ > 0.01 in this format.

## Scope and verification

- The Witting rays are generated in Z[ω]⁴. The script asserts Hermitian norm 3 on all 40 rays and |⟨u, w⟩|² ∈ {0, 3}.
  Each ray is orthogonal to exactly 12 others, which matches the Witting configuration.
- The Hurwitz lines are H(1,0), H(0,1) and H(1, y) for y ∈ {±1, ±i, ±j, ±k}, with the Hermitian form a c̄ + b d̄.
- Cliques are exact (exhaustive search with `e8units.first_clique`). Ceilings are rational-interval roots from
  `skel.X`, maximised over s ∈ {3, 5, …, 13}. The census does not evaluate the s ≥ 15 tail. The format-limits tail
  bound shows that X decreases there for the realised units, but this census does not re-prove it for these units.
- x_lb is a bound only for coordinate-total decoders in the stated orthogonal frame (lattice lines that are mutually
  orthogonal). Other frames or decoders are not covered. The clique bound uses only B_TT = 1 and B_TS = 0 on
  N_TS ≠ 0. It does not use the window rank, so it is weaker than the SAT floors of format-limits for E8.
- It is not checked here whether the bit contract's rational address shears and the complex binary phase frames can be
  carried over Q(ω) or H. The negative result does not need this: even if both transfer, the ceiling is too low.

```sh
python3 -B research/label-field-census/census.py --json /tmp/label-field-census.json
# compare with research/label-field-census/RESULT.json (about 2 minutes; numpy only)
```

Builds on DreamingOfClouds' #446 (Theorems B and C) and the format-limits packages and their contributors
(`research/format-limits-corrected`). It reuses their `skel`, `cert` and `e8units` modules unchanged.
