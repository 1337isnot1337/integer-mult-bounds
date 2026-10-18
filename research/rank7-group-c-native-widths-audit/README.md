# Group C's native residual widths through the shipped T74 fill

**Finite native/interface audit; no new kappa or supplier admission.**

Both literal PR2979 providers pass the entering-residual check for group C.
Helpers 452, 453, 532 and 533 enter at `[30]` and end at
`W = [256,128,64,32,19,11,6]`. Their emitted residual width is **six**, not
the terminal dimension seven. Exact native identities include global phase and
both orientations. These widths bind to all 2,664 group-C placements in the
shipped T74 allocation. Adapter and `LOCAL-CHECKS` hashes match the retained
`FULL-NATIVE-RECEIPT.json`. The four helpers share one residual pair
`115:262`.

This package deliberately does **not** headline the already-registered guide
margins `+17170` / single-helper negatives from `#2979`
`STAGE-PRICES.json`. The contribution here is the native residual / wrapper
binding for group C, in the style of leave-alone #3411 (group B) and the
group-A entrance audit.

### Existing coverage and the added check

`research/rank7-group-a-entrance-audit/` binds group A
(`331/450/451/508/509`, `W_A`). Leave-alone #3411
`research/rank7-group-b-native-widths-audit/` binds group B
(`299/448/449/484/485`, `W_B`). Group C is outside both packages.

## Exact native statement and source binding

The source is [PR2979][2979] at
`be191346391661f4d35fc0d1508d0a6029572576`; the base is canonical main
`6f100d4bb5083f8c35d96fd95a539811c62f245c`, priority revision 6
(κ = `0.001672660197076918`). [SOURCES.json](SOURCES.json) records exact Git
blobs and SHA256 hashes. The native producer, exact kernel and retained
emitter are authenticated before execution. No frozen predecessor is modified.

For entrance `E` and terminal `U`, write the native residual as
`S(E,U) = T_U T_E^-1`. The source compiler produces `S = L F_w R`, where
`F_w` is the retained coordinate Fourier primitive on the first `w` address
axes. A separate exact Gaussian-integer kernel checks all 512 columns of
that identity, and the emitted inverse wrappers satisfy

```text
L^-1 S(E,U) R^-1 = F_w,
w = dim(U) - dim(E).
```

| Helper(s) | Entrance | Parent terminal dimension | Parent width | Joint/final width |
|---|---|---:|---:|---:|
| 452, 453, 532, 533 | span(30) | 8 | 7 | 6 |

Here `30 = 19 xor 11 xor 6` lies in the span of `W`. Treating an entering
helper as cold would select width seven and break the shipped packing. The
parent right wrapper (width seven) is not interchangeable with the joint
width-six recipe: the all-column check rejects that substitution. A different
contained line, `[10]`, has the same dimension but also fails with the actual
`[30]` recipe. The same-width group-B terminal span
`⟨256,128,64,34,17,11,4⟩` likewise fails against the group-C recipe.

The verifier regenerates both complete emitted programs with the unchanged
transport/emitter and reconstructs the full serialized adapter file using
the original generation convention. The uncompressed `LOCAL-CHECKS.json`
and `RESIDUAL-ADAPTERS.json` hashes match PR2979's retained native receipt.
Both regenerated event streams also match the counts and canonical event
digests inside that pinned receipt.

## Reproduction

```sh
python3 -I -B research/rank7-group-c-native-widths-audit/verify.py
python3 -I -O -B research/rank7-group-c-native-widths-audit/verify.py
python3 -I -B research/rank7-group-c-native-widths-audit/test_verify.py -v
python3 -I -B scripts/research_package.py --package research/rank7-group-c-native-widths-audit --check-only
python3 -I -B scripts/research_package.py --package research/rank7-group-c-native-widths-audit
```

Expected verify line:

```text
PASS_GROUP_C_NATIVE_WIDTHS providers=2 helpers=4 residual_widths=6,6,6,6 pairs=452:115:262,453:115:262,532:115:262,533:115:262 placements=2664 adapter_pinned both_orientations no_new_kappa
```

## Open next questions

1. Can the checked group-C direct paths and endpoints be joined to the
   complete native dependency closure of their private cleanup?
2. Do the complete physical, precision/tape and outer obligations admit the
   unchanged PR2979 source after independent review?
3. Do group D helpers `{454,455,556,557}` under
   `W=⟨256,128,64,37,21,8,3⟩` admit the same native residual / T74 join?

## Credit

Builds on #2979 (Dugongue / mdumitrean), the DreamingOfClouds / PR458 emitter
lineage, Sagar Thakrar's exact kernel, Nick Petalas's group-A entrance native
audit, and leave-alone #3411 group-B native widths. New check by Wentao Li.
Apache-2.0.

Prepared by Wentao Li with substantial AI assistance.

[2979]: https://github.com/CrocSwap/integer-mult-bounds/pull/2979
