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

## Verify

```text
python3 -B research/three-short-row-units/verify.py
```

The check takes about 13 s and uses the standard library only.

## Limitations

- **Finite range only.** This is exact evidence for m ≤ 13, not a proof for every m.
- **Inherited model.** The row model and its converse are inherited from #4280.
- **Not claimed.** Call counts and κ.

## Open next questions

- **A uniform three-row construction for units, for every m ≥ 6.** First step: extract minimal witnesses for m = 6 to 13 and fit a template, as #4622 does for two rows: λ = (L₁, L₂, L₃) with one coordinate adjusted from the two-row construction.

Credit: petalas (Nick Petalas) for #4600 and #4280. Prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
