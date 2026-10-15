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

The search (ejection cycles, CP-SAT neighbourhood re-assignments and the final
min-diff re-assignment) only proposes a final owner table. Intermediate states
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
PR1407 and PR2077 arguments, `H(r) = r^p` with `0 < p < 1`. Against the selected
PR1094 map, the idle remainder profile changes by
`{1:+4, 2:+1, 3:-14, 7:-4, 16:+4}`: fourteen residuals 3 and four residuals 7
(total 70) become four residuals 16, one 2 and four 1 (total 70), and nine bins
fill up completely. Padded with zeros and sorted,

```
new: 16 16 16 16 2 1 1 1 1 0 0 0 0 0 0 0 0 0
old:  7  7  7  7 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```

the partial sums of the new vector (16, 32, 48, 64, 66, 67, 68, 69, 70, …, 70)
dominate those of the old one (7, 14, 21, 28, 31, …, 67, 70), with equal totals.
So the new residual vector majorizes the old one, and by Karamata's inequality
for strictly concave `H`,

```
4 H(16) + H(2) + 4 H(1) < 4 H(7) + 14 H(3)
```

(for example 21.41 < 34.83 at `p = 1/2`). The complex moment strictly decreases
while rank mass (1,041,408) and deficit (5,120) are unchanged. The search used
the surrogate `f ln f` on free capacity only to rank candidates; only the final
profile matters for κ.

The exact value comes from the pinned exact engines (moment, base-two moment,
outer) and is not computed by hand. The native complex lower endpoint is
`1675505578629257024283/10^24`. The bit lower endpoint is unchanged at
`1733427039589844234749/10^24`. The complex supplier is binding, so
κ = `1672702955495933/10^18` = 0.001672702955495933. With the conservative
bit surcharge, κ = 0.001672702952644. The PR1069 sweep independently
certifies the endpoint, the deficit identity `W - 64N`, halving, the PR589 bit
record, and that κ equals both the record and the title value.

## What is not claimed

There is no optimality claim: the κ search is a finite LNS that was still
finding gains when it was stopped, and the min-diff step is a finite MIP/LNS
whose relocation count is not proven minimal over all maps with this profile. There is no new supplier,
interface or mechanism. There is no fresh cold rebuild of the native ancestry,
and no unconditional theorem. All PR1094 inherited assumptions remain.
