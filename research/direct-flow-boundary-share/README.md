# #4436's direct-exponent gate reduces to a uniform boundary-exit share

**Claim type:** a written conditional lemma plus numerical evidence. **No new κ, and no proof of the
uniform bound.** It addresses zxv's [#4436](https://github.com/CrocSwap/integer-mult-bounds/pull/4436)
open exponent gate. #4436 notes that its direct flow for overlapping ranks creates *boundary exits*
of rank greater than `k_min·n/m`, "near the upper boundary", which "cannot be assigned the old bound".

## Lemma (conditional)

The setting is #4436's direct flow at top rank `n ≥ m`, with an exponent `t` above the unit's mixed
root and `z0 = t + δ`. Assume:

- **(A) Potential.** `Σ_e x_e e^t ≤ Σ_s w_s s^t` over all exits. This holds because matched jobs
  cancel and each unit's paid `t`-potential is at most its target potential.
- **(B) Ranks.** Sources satisfy `n/m < s ≤ n`. Boundary exits satisfy `e ≤ r_max·n/m`. Leaf exits
  satisfy `e ≤ E(n) = r_max(n/m)^θ`.
- **(C) Boundary share.** `Σ_boundary x_e e^t ≤ β Σ_s w_s s^t`, uniformly in `n`.

Then the exit coefficient obeys

    κ(n) = Σ_e x_e e^(z0) / Σ_s w_s s^(z0)  ≤  β·r_max^δ + (m E(n)/n)^δ.

**Proof.** Boundary part:
`Σ_b x_e e^(z0) ≤ (r_max n/m)^δ Σ_b x_e e^t ≤ (r_max n/m)^δ β Σ w_s s^t ≤ β r_max^δ Σ w_s s^(z0)`,
using `s > n/m`. Leaf part: `Σ_l x_e e^(z0) ≤ E^δ Σ_l x_e e^t ≤ E^δ Σ w_s s^t ≤ (mE/n)^δ Σ w_s s^(z0)`,
using (A). ∎

#4405's refined induction needs only `κ(n) ≤ η = z0·m^(z0−1)` for all `n` beyond an explicit
threshold. Since `(mE/n)^δ → 0`, the induction closes if `β·r_max^δ < η`, and the direct flow then
attains every saving below the unit's root, with an explicit finite rank. For raw p7, `m = 121`,
`r_max = 48` and `η ≈ 0.984`, so the condition is roughly `β < 0.98`.

So the gate reduces to proving a **uniform boundary-exit share bound** (C) with `β < η·r_max^{−δ}`.

## Evidence for (C) on raw p7

`verify.py` uses an independent implementation of #4436's flow, the same as in my #4456. It scans
3,394 ranks: every `N` from 121 to 3,000, plus a 1% geometric grid up to 495,968. At each rank it
checks exactly that exits are at most `r_max·N/m`, that leaf exits are at most `r_max^(G+1)`, and the
rank-one potential identity. It then computes `β(N)` at `t = 1 − 0.0026865`:

| | value |
| --- | --- |
| maximum `β(N)` | **0.1545**, at `N = 1089` |
| typical `β(N)` for `N ≥ 10⁴` | 0.075–0.11 |
| maximum `exit/N` | 0.39669 = 48/121, the bound attained |

The observed `β` sits far below the roughly 0.98 that the lemma needs. These are finite floating-point
measurements, not a proof.

## Not covered

- **A proof of (C)**, which needs counting the omitted Pascal terms at the top boundary.
- **The explicit rank and outer ledger** for a direct-flow endpoint.
- **Native premises.**

## Reproduce

```sh
python3.12 -B scripts/research_package.py --package research/direct-flow-boundary-share --check-only
python3.12 -B scripts/research_package.py --package research/direct-flow-boundary-share
```

The verifier prints `PASS_DIRECT_FLOW_BOUNDARY_SHARE` in about 50 seconds, using only the standard
library.

## Open next questions

1. **Prove a uniform bound on the boundary-exit `t`-potential share.**
   - *Why it matters:* it would close #4436's exponent gate, giving the direct saving without
     tensoring.
   - *First step:* boundary exits occur at points `b` with `m·ρ·r·c(b)/k > n` for some `k`. Bound
     their `u(b)`-weighted potential by the multinomial mass of the last layer.

## Credit

- The direct flow and the gate are zxv's (#4436).
- The refined induction is 1337isnot1337's (#4405).
- The lockstep construction is Jacob Alan Sussman's Theorem 1G.

Prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
Apache-2.0.
