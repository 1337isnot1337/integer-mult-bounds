# Rank-one source-delta fanout

**Exact local construction; no selected-supplier admission or new kappa.**

## Construction

Let `L : F_2^n -> F_2^m` be linear, let `v` be a fixed source direction, and let `alpha` be a scalar bit. The two dirty target panels request

```text
y0 += L(x)
y1 += L(x + alpha*v).
```

Linearity gives `L(x + alpha*v) = L(x) + alpha*L(v)`. The candidate evaluates the common value `L(x)` once and broadcasts it to both targets. During the ordinary second-target accumulation, it adds the charged correction `alpha*L(v)` into the same output update. Sources, targets, and private dirty state are preserved; each target receives one output update. The correction cannot be treated as free coefficient work: source access, coefficient preparation for `L(v)`, its rank-one child, dispatch, hosting, restoration, frames, and precision belong in the complete bill.

The verifier uses the invertible matrix with row masks `(0b011, 0b110, 0b111)`, direction `v=0b001`, and `L(v)=0b101`. It emits literal CNOT circuits with one arbitrary dirty scratch bit `t`; each output parity is computed into `t`, applied, uncomputed, and the arbitrary entry value of `t` is cancelled from the target. A second private dirty bit is untouched. It compares the separate and fused schedules on all 4,096 states of `x`, `alpha`, both arbitrary targets, and both dirty bits. The explicit invoice is **44 CNOTs** for separate calls and **28 CNOTs** for the fused schedule, a saving of 16; the two correction CNOTs are included. Three controls reject an omitted correction, stale `alpha`, and incorrect `L(v)`.

For output row `j`, let `w_j` be its Hamming weight and `d_j` its dot product with `v`. The dirty-scratch schedule costs `4w_j+2d_j+4` CNOTs for two separate calls and `2w_j+d_j+4` for the fused call. Summing the pinned fixture's rows gives 44 and 28. Each target's desired parity is applied once, then the same target toggles cancel the arbitrary entry value of `t`; correction CNOTs are added only where `d_j=1`.

## Cost screen and scope

For two rank-8 calls versus one rank-8 broadcast plus a rank-one correction, the favorable recursive moment changes from `2*(8/73)^(1-a)` to `(8/73)^(1-a)+(1/73)^(1-a)`, before any extra cost `Delta`. At the selected complex endpoint `a = 67018507072324140917/40000000000000000000000`, the rank-mass margin is approximately **6.972176283896**. A construction improves this local moment only if the complete extra source, coefficient, dispatch, frame, hosting, restoration, precision, and output-fusion bill is smaller. A separate third target pass must be charged and can close the margin. The finite CNOT invoice is a separate microcircuit result; it does not certify the recursive child prices.

The finite fixture establishes an exact interface identity, not that any selected T16 pair has this source relation. PR1707 (Cinna Davis, head `3d2e634e046ac4fbf07ddbfb0e59da4cf9907f4e`) supplies the predecessor common-A broadcast construction for identical source values. The current rank-one output-panel difference claim in Discussion #1166 comment 18922942 changes the output tensors; this package changes the source panels. The separate three-frame screen and its rejected shared-call assumption are recorded in [PIVOT.md](PIVOT.md).

Selected-record provenance is pinned in [SOURCES.json](SOURCES.json), and the review/certificate/reproduction pointers are checked by the verifier. The selected result remains unchanged. No native supplier, selected occurrence, complete outer composition, or new `kappa` is claimed.

## Reproduce

From the repository root:

```sh
python3 -B research/centre-rank1-source-delta-seed10d3/verify.py
python3 scripts/research_package.py --package research/centre-rank1-source-delta-seed10d3 --check-only
python3.12 scripts/research_package.py --package research/centre-rank1-source-delta-seed10d3
```

Expected direct result:
`PASS_SOURCE_DELTA_FANOUT states=4096 controls=3 rank=3 source_delta_rank=1 selected_complex_rank_mass_margin~6.972176283896`.

## Open next questions

- **Does a selected T16 pair satisfy the one-dimensional source relation?** This decides whether the interface can change the selected paid profile. A feasible first step is to trace the source rows for one exact pair of complete centre calls in the pinned local program. The blocker is the missing source, owner, and host receipt, plus native precision and tape pricing.
- **What is the complete break-even bill for a rank-one correction?** It determines which source deltas can improve the recursive moment. A feasible first step is to price the fused second-target accumulation and coefficient access in one selected provider environment. The blocker is that this package supplies only a finite binary interface fixture.

## Credit

The common-A broadcast predecessor is Cinna Davis's PR1707. Prepared by Cinna Davis with substantial OpenAI Codex assistance in scoping, construction, verifier implementation, exact enumeration, cost screening, and writing. New work is Apache-2.0. The construction remains conditional on an actual supplier interface and its complete charges.
