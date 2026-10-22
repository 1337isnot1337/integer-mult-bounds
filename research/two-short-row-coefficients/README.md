# Which coefficients admit exactly two short rows?

**Task:** independent-moment (a partial answer to #4600's open question 1). **Base:** canonical main `f626db5c`. **No κ is claimed.**

## Background

petalas's #4600 (head `44640c4a`, open) works in #4280's row model of balanced unsigned depth-four dirty chain words with modulus m. It proves that two short rows realizing c ≠ 0 force **m | cL** for each short length L. Unit coefficients therefore need at least three short rows. It also gives the family m = 8t, c = 4t. Its open question 1 asks which nonzero coefficients admit exactly two short rows, noting that the annihilator condition is not known to be sufficient.

The model is the following. Profiles λ (row lengths L_q), ρ and β each have m nonincreasing entries in [0, m], with B(L) = β₁ + … + β_L. A triple is correct exactly when

```text
Σ L_q = Σ ρ_q = Σ β_p = 0,   Σ ρ_q L_q = Σ B(L_q) = 0,   Σ ρ_q B(L_q) = −c   (mod m).
```

## Results

### Theorem: gcd(c, m) = 2 is impossible, with a written proof

If exactly two short rows realize c ≠ 0, then **gcd(c, m) ≥ 3**.

**Proof.** Let g = gcd(c, m). By #4600, m/g divides L₁ and L₂, and L₁ + L₂ = m. If g = 2, then L₁ = L₂ = m/2, and the congruences become

```text
(r₁ − r₂)·m/2 ≡ 0,   2·B(m/2) ≡ 0,   c ≡ −(r₁ + r₂)·B(m/2)   (mod m).
```

The first makes r₁ − r₂ even, so r₁ + r₂ is even too. The second gives B(m/2) ∈ {0, m/2}. Hence c ≡ 0 (mod m), a contradiction. ∎

### Exact enumeration for every m ≤ 12

The enumeration ranges over all nonincreasing ρ and β, and every placement of the two short rows after the full rows. It shows that **the achievable nonzero c are exactly {c : gcd(c, m) ≥ 3}**:

| m | achievable c | allowed by m \| cL but not achievable |
|---|---|---|
| 4 | — | 2 |
| 6 | 3 | 2, 4 |
| 8 | 4 | 2, 6 |
| 9 | 3, 6 | — |
| 10 | 5 | 2, 4, 6, 8 |
| 12 | 3, 4, 6, 8, 9 | 2, 10 |
| 2, 3, 5, 7, 11 | — | — |

- **The annihilator condition alone is not sufficient.**
- **The strengthened condition is exactly right for m ≤ 12.**
- **Family check.** #4600's family m = 8t, c = 4t is checked directly for t = 1, …, 64: valid profiles, all congruences, exactly two short rows and c = 4t. This agrees with the table, since gcd(4t, 8t) = 4t ≥ 4.

## Verify

```text
python3 -B research/two-short-row-coefficients/verify.py
```

The check takes about 3 s and uses the standard library only.

## Limitations

- **Sufficiency is shown only for m ≤ 12.** Whether every c with gcd(c, m) ≥ 3 admits two short rows for all m is open.
- **Inherited assumptions.** The row model and its converse (every correct triple comes from a balanced word) are inherited from #4280 and are not re-proved here.
- **Not claimed.** A call-count claim beyond #4600's, a physical caller, a supplier or κ.

## Open next questions

- **Is gcd(c, m) ≥ 3 sufficient for every m?** First step: construct profiles for c = m/g·k with g ≥ 3 from #4600's m = 8t template. The candidates are L₁ = m − m/g, L₂ = m/g and ρ = (·, g′, 0, …), extending the 6t/2t split.

Credit: petalas (Nick Petalas) for #4600 and #4280 (row model). Prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
