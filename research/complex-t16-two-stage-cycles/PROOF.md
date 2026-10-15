# Why the owner map is admissible and strictly cheaper

## Domain

This argument is the same as PR1407's (`research/astra-ultra-hosting-20261013/PROOF.md`
at `d8640f5b`). Relative to the selected PR1094 map, only the physical owner,
port and slice offset of whole helper roles change. The local gauge44 provider (480 whole helpers per call), the 144
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

The search (global class-level repack, ejection cycles, CP-SAT neighbourhood
re-assignments and the final min-diff re-assignment) only proposes a final
owner table. Intermediate states
are not executed; the controller only ever sees the final table. So it is
enough to check the final map, and this package checks it three independent
times:

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
weights `H(r)` over the idle remainders. Rank mass (1,041,408) and deficit
(5,120) are unchanged. Against the selected PR1094 map, the idle remainder
profile changes by

```
{1:+70, 2:+3, 3:-223, 5:+9, 7:+29, 8:+2, 16:+7, 28:+1, 39:+1, 40:+1, 41:+2, 44:+41, 48:-37}
```

with equal residual totals (237,024 on both sides). Unlike the previous
versions of this package, the new residual vector does **not** majorize the
old one: 37 bins that were completely idle (residual 48) now host a few small
helpers (41 residuals 44, two 41, one each of 40, 39 and 28), while many
residuals 3 elsewhere merge into residuals 7 and 16 or close completely.
Sorted, the first 4,829 entries agree (48), and the next 37 are 44s in the new
vector against 48s in the old one, so the partial sums of the new vector fall
below the old ones there. Karamata's inequality alone therefore does not give
the sign, and no hand argument is offered for it.

The decrease is established by the exact engines instead. The pinned exact
engines (moment, base-two moment, outer) price the new profile; the native
complex lower endpoint is `1675857962565178858949/10^24` (selected:
`1675462676808103522925/10^24`). The bit lower
endpoint is unchanged at `1733427039589844234749/10^24`. The complex supplier
is binding, so κ = `1673054161426948/10^18` = 0.001673054161426948. With the
conservative bit surcharge, κ = 0.001673054158574889. The unchanged strict
verifier's own moment engines and outer assembly reach the same κ, and the
PR1069 sweep independently certifies the endpoint, the deficit identity
`W - 64N`, halving, the PR589 bit record, and that κ equals both the record and
the title value. The search used the surrogate `Σ f ln f` over idle fragments
only to rank candidates; only the final profile matters for κ.

## What is not claimed

There is no optimality claim: the κ search is a finite heuristic (global
repack plus LNS) that was still finding gains when it was stopped, and the
min-diff step is a finite MIP/LNS whose relocation count is not proven minimal
over all maps with this profile. There is no new supplier,
interface or mechanism. There is no fresh cold rebuild of the native ancestry,
and no unconditional theorem. All PR1094 inherited assumptions remain.
