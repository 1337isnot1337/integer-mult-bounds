# Three short rows realize every unit coefficient for 6 ≤ m ≤ 13

**Task:** independent-moment (exact evidence for #4600's open question 2). **Base:** canonical main `f626db5c`. **No κ is claimed.**

## Background

petalas's #4600 proves, in #4280's row model of balanced depth-four dirty chain words with modulus m, that a unit coefficient needs at least three short rows. Its open question 2 asks whether three short rows realize every unit for every m ≥ 6. My #4622 settles the two-short-row case completely: two short rows realize c ≠ 0 exactly when gcd(c, m) ≥ 3.

## Result

The verifier enumerates the model exactly:

- every nonincreasing ρ and β with m entries in [0, m];
- every λ with exactly three short rows L₁ ≥ L₂ ≥ L₃ summing to 0 (mod m), placed after f full rows.

It finds the following.

| m | coefficients realized with exactly three short rows |
|---|---|
| 2 to 5 | none |
| 6 | 1, 2, 4, 5 |
| 7 to 13 | every nonzero c |

- **The answer to #4600's open question 2 is yes for 6 ≤ m ≤ 13.** Every unit is realized with three short rows.
- **The threshold m ≥ 6 is sharp.** For m ≤ 5, no nonzero coefficient is realized with three short rows.
- **Two vs three rows at m = 6.** The coefficient 3 needs two rows rather than three, consistent with #4622.

## Fixed-shape evidence up to m = 30

A single shape suffices well beyond the exhaustive range:

```text
λ = (m−1, m−2, 3, 0, …),   ρ = (m, a, b, padding ≤ b, …).
```

For each target only (a, b) changes, and β is decided exactly by a dynamic programme. This shape realizes every unit for 7 ≤ m ≤ 30. At m = 6 the unit 5 needs a different shape, which the exhaustive run finds.

## Explicit construction for every c ≢ −1 (written, checked to m = 200)

Take λ = (m−1, m−2, 3, 0, …) and ρ = (m, 3, 2, 1^(m−5), 0, 0). For 1 ≤ u ≤ m−2, take

```text
β = (balanced first block of sum u + 2m,  balanced middle of length m−5 and sum S,  u,  0),
```

where S is the least value ≥ (m−5)u with S ≡ −2(u + 2m) (mod m).

- **Partial sums.** B(3) ≡ u, B(m−2) ≡ −u and B(m−1) ≡ B(m) ≡ 0.
- **Congruences.** Every congruence holds, and the coefficient is −(3B(m−2) + 2B(3)) ≡ u.
- **Monotonicity.** This needs S ≤ (m−5)·⌊(u+2m)/3⌋, which holds for all u ≤ m−2.

The verifier checks the construction for every 10 ≤ m ≤ 200. **So three short rows realize every c ≢ −1 (mod m) for all m ≥ 10, in a uniform way.** Only c = −1 still needs a uniform rule. It is covered exactly for m ≤ 13 and by the fixed-shape search for m ≤ 30, using other ρ = (m, a, b, …) with a ≡ 3t and b ≡ 2t for a unit t, for example.

## Verify

```text
python3 -B research/three-short-row-units/verify.py
```

The check takes about 20 s and uses the standard library only.

## Limitations

- **Finite range only.** This is exact evidence for m ≤ 13, not a proof for every m.
- **Inherited model.** The row model and its converse are inherited from #4280.
- **Not claimed.** Call counts and κ.

## Open next questions

- **A uniform three-row rule for c = −1.** The construction above covers every other c for m ≥ 10. First step: use ρ = (m, 3t, 2t, …) with a unit t such that 3t mod m ≥ 2t mod m, and X ≡ −t⁻¹.

Credit: petalas (Nick Petalas) for #4600 and #4280. Prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
