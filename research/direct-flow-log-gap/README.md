# The refined-induction ceiling on #4436's direct flow grows with the lockstep depth

**Claim type:** a first-order argument plus finite floating-point evidence. **No new κ.** It follows
my correction of [#4459](https://github.com/CrocSwap/integer-mult-bounds/pull/4459). There, leaf exits
turned out to dominate, so the question becomes what the total exit coefficient of zxv's
[#4436](https://github.com/CrocSwap/integer-mult-bounds/pull/4436) direct flow can certify under
#4405's refined induction (`κ(N, z0) ≤ η = z0·m^{z0−1}`).

## First-order picture

- **Balance at the root.** At the unit root `t*`, where `Σ_k W_k k^t = Σ_r P_r r^t` (raw p7 gives
  `t* = 0.9973135`, `s* = 0.0026865`), exits and sources carry equal `t*`-potential. The verifier
  checks this to `10⁻⁹` at every rank.
- **The log-gap.** Define `g(N) = E_S[ln s] − E_X[ln e]`, with `t*`-potential weights. To first order:

      κ(N, z0) ≈ exp(−(z0 − t*)·g),      η(z0) ≈ exp(−(1 − z0)(1 + ln m)).

- **The ceiling.** The test therefore certifies savings up to about

      cap(N) = s*·g / (g + 1 + ln m),     with 1 + ln 121 = 5.796.

  The first-order formula matches the exact κ to `3·10⁻⁵` across the grid.

## Measurements (raw p7)

`g` is a sawtooth in `N`: it drops each time the lockstep depth `G` increases. Its per-level minima
nevertheless rise steadily, by about 0.23 per level, which is a factor of about 5 in `N`.

| G | rank of minimum | min g | cap at minimum |
| --- | --- | --- | --- |
| 1 | 1,000 | 1.977 | 0.000683 |
| 2 | 3,071 | 2.204 | 0.000740 |
| 3 | 16,135 | 2.538 | 0.000818 |
| 4 | 76,886 | 2.751 | 0.000865 |
| 5 | 384,675 | 2.954 | 0.000907 |
| 6 | 1,924,603 | 3.207 | 0.000958 (local run) |
| 7 | 9,629,156 | 3.373 | 0.000990 (local run) |

Rows 1–5 rerun in the verifier, in about 7 seconds. Rows 6–7 come from
`evidence/gap_large.py 2e7`, whose output is `evidence/LOGGAP-LARGE.txt`, through `N = 1.73·10⁷`.

Consistency checks:

- In the verifier, saving 0.0008 passes at every grid rank `N ≥ 3·10⁵`, and saving 0.001 still
  fails at some.
- #4456's effective savings (0.000634 at 10³, 0.000835 at 3·10⁴) sit just under these caps.

## Reading

- **The ceiling is not bounded away from `s*`.** If `g` keeps growing by about 0.23 per level, the
  cap tends to `s*`, so #4436's direct exponent gate plausibly closes in the limit.
- **But extremely slowly.** A saving `s` needs `g ≥ s(1 + ln m)/(s* − s)`. Saving 0.001 needs
  `g ≈ 3.44`, about level 8 (`N ~ 5·10⁷`). The selected 0.0023 would need `g ≈ 34.5`, roughly 135
  more levels, `N ~ 10^{100}`. This is a heuristic extrapolation, not a bound.
- **The tensor/padding route is not superseded.** The direct flow is not a practical substitute for
  it at κ near 0.0023, unless the induction itself is improved, for example by using several steps
  of exits.

## Not covered

- A proof that `g → ∞`, or a rate for it.
- Second-order terms beyond the measured `3·10⁻⁵`.
- Native premises.

## Reproduce

```sh
python3.12 -B scripts/research_package.py --package research/direct-flow-log-gap --check-only
python3.12 -B scripts/research_package.py --package research/direct-flow-log-gap
cd research/direct-flow-log-gap && python3.12 -B evidence/gap_large.py 2e7   # ~2 min, rows 6-7
```

The verifier prints `PASS_DIRECT_FLOW_LOG_GAP`, using only the standard library.

## Open next questions

1. **Why does `g` grow by about 0.23 per level, and does it grow without bound?**
   - *Why it matters:* it decides whether #4436's direct saving approaches the root, and how fast.
   - *First step:* express the leaf exits' `t*`-potential through the mirror base measure of #4459,
     and compute the per-level drift of its log-mean.
2. **Can a multi-step exit test beat the single-step ceiling?**
   - *First step:* substitute the exits' own flows once, giving a two-step coefficient, and remeasure.

## Credit

- The direct flow and the gate are zxv's (#4436).
- The refined induction is 1337isnot1337's (#4405).
- The lockstep construction is Jacob Alan Sussman's Theorem 1G.

Prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
Apache-2.0.
