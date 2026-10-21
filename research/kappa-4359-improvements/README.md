# Improvements to the productive-job construction in PR #4359

Conditional on the native compiler and outer interfaces of
[PR #4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359), the
unchanged complex p3 invoice supports

```math
T(n)=O\bigl(n(\log n)^{1-0.00230508}\bigr).
```

This exceeds the predecessor's stated saving `0.0023` by `0.00000508`.
The change has two parts: a logarithmic bound on the finite compiler's
paid-leaf count, and an exact outer parameter family approaching the
unchanged mixed root. No new local native word is needed for this result.

The dependency is pinned to
`da637c87c89482bc4c86be36bd0071b3d400dbed`. It is pending research, with
the inherited analytic, native movement, precision, and fixed-tape
conditions retained. The selected result on canonical main is a separate
record and is not changed by this contribution.

## Results and their scope

| Result | Location | What it establishes |
| --- | --- | --- |
| Smaller finite templates | [Logarithmic potential proof](../kappa-4359-log-potential/PROOF.md) | A new bound on paid rank-one leaves, including source complements and all exits |
| Stronger outer saving | [Outer parameter proof](../kappa-4359-outer-endpoint/README.md) | Every strict rational saving below the unchanged complex mixed root, with an explicit instance at `0.00230508` |
| Exact finite-rank witness | [Rank certificate](../kappa-4359-log-potential/CERTIFICATE.json) | Complex uniform saving `0.002305088` at the specified rank `2^1729137493` |

At the predecessor's original uniform savings, the new bound gives:

| Family | Uniform saving | Predecessor sufficient rank | New sufficient rank |
| --- | ---: | ---: | ---: |
| Complex | `0.002304` | `2^276540184361` | `2^2458275` |
| BIT before the cover | `0.002760` | `2^6552928412` | `2^463652` |

These comparisons concern the ambient rank. The expanded words, their
batch multiplicities, and their constants remain enormous and are not
materialized. A smaller ambient rank alone is not a practical running-time
measurement.

## Why the stronger exponent follows

For the exact finite compiler recurrence, the logarithmic potential gives

```math
L(n)\leq m^{1-t}n^t\max(1,\log n)^\gamma.
```

The proof keeps the same integer routing and paid source complements.
Its exact inequalities specify a successful finite rank for a chosen
uniform saving. This replaces the predecessor's more expensive argument
through an intermediate power exponent.

The concrete outer instance tests the mixed tariff at `0.00230509` and
compiles a complex supplier at `0.002305088`. The old `0.002304` supplier
would be insufficient. The parameter certificate binds the stronger rank
certificate before checking the outer claim.

All nine outer costs have savings strictly greater than `0.00230508`.
The limiting main-transform saving is `0.002305081995389836`, with exact
positive margin `498847459/250000000000000000`.

The complete parameter family proves that any rational
`0<kappa<C`, where
`C=0.002305090194876170622919094755...` is the unchanged complex mixed
root, can be approached with a fixed finite program. It does not prove
attainment of the endpoint `C`.

## Reproduction

Use a separate checkout of the pinned predecessor as the source root.
One way to obtain it is:

```sh
git init /tmp/integer-mult-pr4359-source
git -C /tmp/integer-mult-pr4359-source remote add origin https://github.com/zxv/integer-mult-bounds.git
git -C /tmp/integer-mult-pr4359-source fetch --depth 1 origin da637c87c89482bc4c86be36bd0071b3d400dbed
git -C /tmp/integer-mult-pr4359-source checkout --detach FETCH_HEAD
```

Run the following commands from this contribution's checkout:

```sh
python3 -B research/kappa-4359-log-potential/verify.py --source-root /tmp/integer-mult-pr4359-source --check
python3 -B research/kappa-4359-outer-endpoint/verify.py --source-root /tmp/integer-mult-pr4359-source --check-only
```

Both checkers use the Python standard library. They authenticate fixed
source hashes and compare deterministic certificates. The outer checker
also replays the rank certificate and cross-checks all nine cost rows
against the inherited ledger. No floating-point result decides acceptance.

The predecessor's separate full replay is:

```sh
python3 -B /tmp/integer-mult-pr4359-source/research/kappa-0023-productive-jobs/verify.py --out /tmp/pr4359-fresh-replay
```

The output directory must not already exist. That replay checks the
predecessor's native artifacts; the new arithmetic checks do not replace
its operator and ownership obligations.

## Provenance and open next questions

The p3 native word, complete invoice, delayed BIT cover, and original
finite-template closure are from zxv's PR #4359. The mixed-job lockstep
construction builds on Jacob Alan Sussman's Theorem 1G in PR #4268.
The outer formulas and their earlier contributors remain credited in
the pinned predecessor and the two proof packages. New material is under
Apache-2.0.

The local complex mixed root still bounds the unchanged tariff. A further
exponent gain requires a changed complete native invoice or a justified
extension of the compiler's hypotheses. The next investigation examines
the explicit helper topups used only to enforce strict rank separation.
Any deletion must preserve arbitrary-input endpoints and replace that
separation hypothesis with a proved terminating integer compiler.
