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
re-assignments including the evacuation neighbourhood, and the final min-diff
re-assignment) only proposes a final
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
weights `H(r)` that are strictly concave in the rank `r` with `H(0) = 0`. In the
PR1407 and PR2077 arguments, `H(r) = r^p` with `0 < p < 1`. Rank mass
(1,041,408) and deficit (5,120) are unchanged. Against the selected PR1094 map,
the idle remainder profile changes by

```
{1:+79, 2:+2, 3:-205, 7:-4, 16:+11, 48:+8}
```

selected: `{1:2276, 3:377, 7:7, 48:4866}`; this map:
`{1:2355, 2:2, 3:172, 7:3, 16:11, 48:4874}`. The residual totals are equal
(237,024 on both sides). Sorted in decreasing order and padded with zeros to
the common number of bins,

```
new: 48 x 4874, 16 x 11, 7 x 3, 3 x 172, 2 x 2, 1 x 2355, 0 ...
old: 48 x 4866,          7 x 7, 3 x 377,         1 x 2276, 0 ...
```

The partial sums of the new vector are never below those of the old one.
They agree for the first 4,866 entries (all 48), the new vector leads from
entry 4,867 on (by 332 after 4,874 entries), and the old vector never catches
up before both reach 237,024 (after 4,874 + 11 + 3 + 172 + 2 + 2,355 = 7,417
and 4,866 + 7 + 377 + 2,276 = 7,526 entries). So the new residual vector
majorizes the old one, strictly. In words: 205 residuals 3 and four residuals
7 are gone, and their residual capacity (643) reappears as eight more
completely idle bins (384), eleven residuals 16 (176) and 79 more residuals 1
plus two residuals 2 (83). `check.py` checks this mechanically: it sorts and
pads both audited idle vectors, asserts equal totals and that every partial sum of
the candidate vector is at least the selected one's, with strict inequality
somewhere, and records the result as `majorization` in `CHECK.json`;
`verify.py` requires it. By Karamata's inequality for strictly concave `H`,

```
4874 H(48) + 11 H(16) + 3 H(7) + 172 H(3) + 2 H(2) + 2355 H(1)
  < 4866 H(48) + 7 H(7) + 377 H(3) + 2276 H(1)
```

(for example 36,475.7 < 36,660.1 at `p = 1/2`). The complex moment strictly
decreases while rank mass and deficit are unchanged. (Version 3 of this package
did not have this property and relied on the exact engines alone.)

The sign argument gives the direction only. The value of κ comes from the
pinned exact engines (moment, base-two moment, outer) and the strict replay,
not from a hand computation. The native complex lower endpoint is
`1676146695051222742471/10^24` (selected: `1675462676808103522925/10^24`). The
bit lower endpoint is unchanged at `1733427039589844234749/10^24`. The complex
supplier is binding, so κ = `1673341928508063/10^18` = 0.001673341928508063.
With the conservative bit surcharge, κ = 0.001673341925655596. The unchanged
strict verifier's own moment engines and outer assembly reach the same κ, and
the PR1069 sweep independently certifies the endpoint, the deficit identity
`W - 64N`, halving, the PR589 bit record, and that κ equals both the record and
the title value. The search used the surrogate `Σ f ln f` over idle fragments
only to rank candidates; only the final profile matters for κ.

## What is not claimed

There is no optimality claim: the κ search is a finite heuristic (global
repack plus LNS, including the evacuation neighbourhood) that was still finding
gains when it was stopped, and the min-diff step is a finite MIP/LNS whose
relocation count is not proven minimal over all maps with this profile. The
majorization argument shows only that this map is strictly cheaper than the
selected one; it says nothing about how far from optimal either is. There is no
new supplier, interface or mechanism. There is no fresh cold rebuild of the
native ancestry, and no unconditional theorem. All PR1094 inherited
assumptions remain.
