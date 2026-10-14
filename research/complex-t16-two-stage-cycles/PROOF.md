# Why the two-stage cycles are admissible and strictly cheaper

## Domain

This argument is the same as PR1407's (`research/astra-ultra-hosting-20261013/PROOF.md`
at `d8640f5b`). Only the physical owner, port and slice offset of whole helper
roles change. The local gauge44 provider (480 whole helpers per call), the 144
complete calls and their order, orientations, source events, endpoint adapters,
global bridges and terminal corrections all stay fixed. `build.py` asserts that
every changed row keeps `stage`, `replica`, `time`, `helper` and `width`.

The bin `(o, c, p)` is owner replica `o`, idle child `c` and port `p`. Its
capacity is the rank of `c`. Its borrowing interval is the original idle
transition: after the owner's last source-event touch and before its idle
deadline, with all 144 bridges included. A placement of helper `h` of call `k`
into `(o, c, p)` is legal under four conditions:

1. **Capacity.** The widths assigned to the bin fit its rank, and the slices
   are a prefix `0..used-1`.
2. **Window.** The call position lies strictly inside the bin's interval.
3. **Family.** The physical family `o*F + (2*pair+side)*V + p` is used by no
   other helper of the same call.
4. **Integrity.** `copy = 112*o + p`, each helper appears once per call, and no
   helper is split.

An ejection cycle is a sequence of such placements whose *final* state meets
1–4. Intermediate states are not executed. The controller only ever sees the
final owner table. So it is enough to check the final map, and this package
checks it three independent times:

- `build.py`'s own packing checker covers 1, 3 and 4 and the window
  membership of 2 against `PLAN.windows`.
- The seed67 auditor (Josie Elliston, PR1091) checks R1–R7, X1 and X2 and
  rejects its 11 mutations. `check.py` also confirms that every role lies
  strictly inside its window and that each helper appears once per call.
- The unchanged PR1087 strict verifier re-emits every affected chart. Its
  controller audit, finite invoice, independent T16 replay and 69 + 12 + 6 + 15
  rejecting controls all pass.

## All-input operator argument (inherited)

Inside one borrowed bin, the owner has no data touch between the interval's
opening event and its deadline. Each complete invocation applies its declared
data shear whatever the incoming helper values are. It also applies its
residual Clifford operator to the borrowed axes. Distinct slices partition the
bin's original `c` axes, and the exact Gaussian-dyadic factors commute. So at the
deadline the assigned slices together with the unused suffix act as the
original idle child. The owner's value is the original one whenever the
controller reads it. This is PR1407's argument, applied to a different legal
final assignment; it needs no new step. It inherits the common-label and
mutable-source realization assumptions; it does not prove them anew.

## Strict cost improvement

The paid recursive moment depends on the profile through a sum of per-residual
weights `H(r)` that are strictly concave in the rank `r` with `H(0) = 0`. In the
PR1407 and PR2077 arguments, `H(r) = r^p` with `0 < p < 1`. Against PR1407, the
idle multiset changes from `{3, 3, 3}` to `{8, 1, 0}`, with the same total of 9.
Sorted, `(8, 1, 0)` majorizes `(3, 3, 3)`: the partial sums are 8 ≥ 3, 9 ≥ 6 and
9 = 9. By Karamata's inequality for strictly concave `H`,

```
H(8) + H(1) + H(0) < 3 H(3),   e.g.  8^p + 1 < 3 * 3^p  for 0 < p < 1,
```

so the complex moment strictly decreases while rank mass (1,041,408) and
deficit (5,120) are unchanged. The two stages behave differently under the
search's surrogate `f ln f` on free capacity. Stage A's first cycle is neutral:
it only moves a free 3. Stage A's second cycle merges 3 + 3 into 6, a gain of
`6 ln 2`. Stage B turns 3 + 3 + 6 into 8 + 1 + 3. Only the final profile matters
for κ.

The exact value comes from the pinned exact engines (moment, base-two moment,
outer) and is not computed by hand. The native complex lower endpoint is
`209435883958297284563/125000000000000000000000`. The bit lower endpoint is
unchanged at `1733427039589844234749/10^24`. The complex supplier is binding, so
κ = `418171127598559/250000000000000000` = 0.001672684510394236. With the
conservative bit surcharge, κ = 0.001672684507542306. The PR1069 sweep
independently certifies the endpoint, the deficit identity `W - 64N`, halving,
the PR589 bit record, and that κ equals both the record and the title value.

## What is not claimed

There is no optimality claim: bounded depth-6 one- and two-stage passes on the
final map find nothing, which is a search limit. There is no new supplier,
interface or mechanism. There is no fresh cold rebuild of the native ancestry,
and no unconditional theorem. All PR1094 inherited assumptions remain.
