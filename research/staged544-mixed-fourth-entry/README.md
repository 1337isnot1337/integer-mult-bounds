# A mixed fourth staged entry improves the conditional bound

**Local, author-checked finite construction; not maintainer-reviewed.** The complete
moment root is in

**[0.001730978305075885693430, 0.001730978305075885693431].**

Under the retained outer-transfer hypotheses and padding convention, take

`κ = 0.001730978305075885693430 − 10^-46 − 10^-70`.

This exceeds [PR4085](https://github.com/CrocSwap/integer-mult-bounds/pull/4085)'s
certified upper endpoint by more than **7.885876721990690 × 10^-9**, approximately
**0.000455576%**. No selected-frontier update or unconditional multiplication
exponent is asserted. The full inherited ordinary/outer release engine has not
been rerun with the four-provider dispatch; that integration remains open.

## Construction

PR4076 stages helpers 600, 608 and 609 in every call. Its rejection of a uniform
fourth entry does not exclude using that entry in only some calls. Here helper
601 is staged in exactly **1,080 of 3,240 calls**, those at chronological times
`t ≡ 0 (mod 3)` in the retained T360 order. The other 2,160 calls use the exact
PR4085 receiver-sharing words. Both original orientations have an explicit fourth-entry variant.

The receiver-sharing rewrite is inherited from PR4085 at
`c5854c77620723aae6914c32122870519a6f820d`. It acts on different helpers;
the four-entry words include it explicitly and are rechecked in full.

For helper 601, replace entrance `[45]` by `[127,45]`, remove its four early
`+1/4` target reads, and insert `602 -= 601` and `123 += 601/2`. The complete
scalar words, exact frames and derived cleanup are retained. Literal records
reconstruct the new words from the pinned predecessors without a solver.

| Quantity | Three entries, PR4085 | Four entries |
|---|---|---|
| Local profile | `{1:2487,2:713,3:224,4:102,5:20,8:8}` | `{1:2489,2:713,3:227,4:99,5:20,8:8}` |
| Widths 5 / 6 / 7 / 8 / 9 | 28 / 18 / 56 / 93 / 213 | 28 / 18 / 57 / 92 / 213 |
| Calls used | 2,160 | 1,080 |

The new literal fill covers all **1,321,920 roles in 725,760 bins**. It checks
every time window, helper identity, family, compact offset and capacity.
The exact operator replay additionally checks productive-data nonaliasing, every
original phase-axis cell, strict scalar-observation windows, and 10,416 Z4
phase identities over all 112 ports and all positive tensor multiplicities.
Its idle profile is `{3:22785,5:1625,16:1,32:2,48:138490}`. The complete paid
profile is

`{1:8060040,2:2310120,3:751785,4:327240,5:66425,8:25920,16:1,32:2,48:138490}`.

The improvement survives the actual integer fill. Neither a fractional packing
nor a solver's objective is used as the certificate.

## Replay

From the repository root, standard-library CPython 3.12:

```sh
python3.12 -B scripts/research_package.py --package research/staged544-mixed-fourth-entry
```

The registered commands freshly verify all four words on 723 independent formal
inputs, forward and dual semantics, reverse pullback, both cleanup boundaries,
91 arbitrary dirty buffers, independent binary-frame ledgers, the full owner
fill, and rational moment signs. Controls reject omitted or flipped releases,
the old entrance, wrong source, bad owner timing/family/offset, omitted fourth
provider, an extra unpaid rank-one term and unsupported root endpoints.

Both composed four-entry words also passed fresh five-stage native runs on CPython 3.12.14.
The default replay authenticates those receipts and their full native source
closure. To rerun the native phases, NumPy is additionally required; use a fresh
external output path for each command:

```sh
python3.12 -B research/staged544-mixed-fourth-entry/native/run_native.py research/staged544-mixed-fourth-entry/inputs/FOUR-base.json.gz /tmp/mixed-four-native-base
python3.12 -B research/staged544-mixed-fourth-entry/native/run_native.py research/staged544-mixed-fourth-entry/inputs/FOUR-extra.json.gz /tmp/mixed-four-native-extra
```

`PROOF.md` states the composition and cost argument. `RESULT.json` contains the
exact rational endpoints and moment intervals. `EXPORTED-SOURCES.json` pins
predecessor exports; `MANIFEST.json` pins this package's replay files. Discovery
used PR3815's class/Hall model with varying per-call supplies, exact integer
pattern counts, and a call-wide augmenting matching. The frozen fill is the
replayable witness; no optimization software is required to validate it.

## Scope

The finite words, fresh native runs, literal chronological fill, exact phase operator and exact moment
are checked. Uniform source generation, physical hosting/tape/precision/recovery,
analytic and BIT transfer assumptions are inherited from the PR3945/4076/4085 line.
The new finite selector and common-interface composition are explicit in the
proof. No human or formal-kernel review is claimed.

## Open next questions

1. Rebind the ordinary/outer admission engine to all four providers and the new
   dispatch. The first step is a provider-registry extension on the pinned source
   closure, preserving every admission predicate and mutation control.
2. Optimize which calls receive the fourth entry. A periodic one-third schedule
   is sufficient but is not proved optimal; a complete candidate must again
   produce a literal fill and pass every owner constraint.
3. Improve integer packing without changing the words. The ideal mixed screen
   is slightly stronger than this fill; the rank-16 and rank-32 residual bins
   identify a concrete place to investigate, with no assumed free repacking.

## Attribution

Prepared by Cinna Davis with substantial OpenAI Codex assistance. Apache-2.0.
The mixed dispatch and its literal fill are new here. The staged-entry mechanism,
source words, frame solver, audit engines, native machinery, owner model and
rational arithmetic are credited in `NOTICE.md`; they are not new inventions
of this package.
