# The selected complex word cannot reach κ = 0.1 by repacking

**Exact target-scale rejection for one frozen local word. No new supplier or κ claim.**

The user-set target κ > 0.1 is far beyond the selected result. Under the
retained planning transfer κ = a/(1+a), it requires primitive saving
a > 1/9. At a = 1/9, the selected complex word's paid local work already has
normalized moment strictly above one, even after assigning **zero cost** to
every idle child, hosting operation and centre path. Therefore no change to
packing, idle hosting or coverage law can bring this same local word to the
target. The word or the outer transfer must change.

The source-bound per-call profile from
[`complex-local-word-ceiling/levers.py`](../complex-local-word-ceiling/levers.py)
is

```text
H = {1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}
width = 73; live families per call = 896/9
```

The exact lower bound is

```text
(9/896) * Σ_r H[r] * (r/73)^(8/9) > 1.155558328185663 > 1.
```

Each fractional power is enclosed by integer inequalities. For scale
`S = 10^30`, the checker finds integers `l_r, u_r` satisfying

```text
l_r^9 * 73^8 <= r^8 * S^9 <= u_r^9 * 73^8,
```

so `l_r/S <= (r/73)^(8/9) <= u_r/S`. The complete rational lower endpoint,
upper endpoint and per-rank witnesses are in [`RESULT.json`](RESULT.json).
The proof does not use floating point; decimals are only for display.

There is also a word-independent screen for the retained width, template and
halving guard. The largest permitted child rank is 51 (`2·51² < 73² ≤ 2·52²`).
For a fixed coverage mass, rank 51 minimizes the moment per unit rank mass,
because the cost per unit mass is proportional to `r^(-1/9)`. Even this
fractional all-at-rank-51 relaxation costs **1.035561535760803** at the
selected coverage law (one unpaid coordinate and centre mass 64). Thus the
current coverage law cannot reach the target with any local word in this
template, even if the local word itself were free.

The exact relaxation brackets also locate the next structural threshold:

| Unpaid coordinates | Centre mass | Ideal all-rank-51 bill | Meaning |
|---:|---:|---:|---|
| 1 | 64 | 1.035562 | Selected law fails, even with a free local word |
| 2 | 0 | 1.012142 | Still fails after removing the centre charge |
| 3 | 0 | 0.997886 | Ideal relaxation passes; no construction follows |
| 3 | 64 | 1.007051 | Fails with the selected centre charge |
| 4 | 64 | 0.992795 | Ideal relaxation passes; no construction follows |

So even the relaxed format requires at least three unpaid coordinates if the
centre is free, or four if the selected centre charge remains. Those are only
necessary budget thresholds: the current word's local-only bill is 1.155558,
so changing coverage alone still cannot work. The two ideal passes have less
than 0.22% and 0.73% headroom before any actual lower-rank work is charged.

The same exact relaxation gives the minimum maximum-child rank needed for each
coverage choice. With the selected law, even a free local word needs rank cap
70; the selected halving guard allows only 51. Removing the centre charge
lowers the requirement to 65, and allowing two unpaid coordinates with no
centre lowers it to 57. The two relaxed combinations that fit under rank 51
are three unpaid coordinates with no centre, or four with the selected centre
charge:

| Unpaid coordinates | Centre mass | Minimum rank cap | Allowed by current guard? |
|---:|---:|---:|:---:|
| 1 | 64 | 70 | no |
| 1 | 0 | 65 | no |
| 2 | 0 | 57 | no |
| 3 | 0 | 51 | yes, at the boundary |
| 3 | 64 | 55 | no |
| 4 | 64 | 48 | yes |

Every rank-cap threshold has a strict adjacent-integer certificate. A rank cap
above 51 would require a different outer halving argument; the table does not
show that such an argument exists.

This is a scoped result about the selected #1094 complex local word and, for
the all-rank-51 relaxation, its width, family count and halving guard. It does
not bound a redesigned template or rank cap, a changed operation alphabet or
supplier, a different outer reduction, or the newer unreviewed candidate
packages. It does not change the selected frontier or certify the full
multiplication theorem. In particular, this is not an independent review of
open PRs #3051 or #3054.

## Reproduce

From the repository root, Python 3.12 and the standard library are enough:

```sh
python3 -I -B research/kappa01-complex-target-screen/verify.py
python3.12 scripts/research_package.py --package research/kappa01-complex-target-screen --check-only
python3.12 scripts/research_package.py --package research/kappa01-complex-target-screen
```

Expected direct marker:

```text
PASS_KAPPA01_SELECTED_COMPLEX_WORD_FLOOR bill_lower=1.155558328185663
```

The interval source inputs and base commit are pinned in
[`SOURCES.json`](SOURCES.json); the replay command and its 120-second timeout
are registered in [`VERIFY.json`](VERIFY.json).

## Open next questions

- What changed complex local identity can bring its paid-word term below one at
  `a = 1/9`? This must precede any packing optimization. A feasible first step
  is one explicit replacement profile with all new decoder, frame, dirty-state
  and restoration costs included. The blocker is a new identity and supplier
  contract; the current word is already 15.55% over budget before hosting.
- Can a source-bound outer transfer improve enough that the current local
  profile's admissible `a` maps to κ > 0.1? This matters only if the new transfer
  changes the proved conversion, rather than just its numerical backoff; the
  first step is an exact derivation against the selected assembly and its
  all-size premises. The blocker is that the current selected reduction is
  source-bound and strictly reserved.

## Credit

The selected complex profile and its packing-ceiling context retain Rohan
Arun's #1094 construction and Douglas Colkitt's #1240 analysis. This package
adds only the target-`0.1` local-word floor and its integer-root replay; it does
not modify predecessor sources. Prepared by OpenAI Codex with substantial
assistance in the calculation, verifier and write-up. New material is covered
by the repository's Apache-2.0 license.
