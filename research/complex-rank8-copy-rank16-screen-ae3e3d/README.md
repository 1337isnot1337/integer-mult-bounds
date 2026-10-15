# Rank-8 copy children regrouped as rank-16: exact screen

This is a bounded negative result for one rank-shape mechanism. The selected
per-call word has eight rank-8 private-temporary copy children, contributing 64
of its 5,586 paid local mass. Pairing them into four rank-16 block children
preserves that mass. Even under a zero-overhead relaxation, the exact packing
ceiling gain is only about **0.211321%**, below the catalogue's 5% screen. No
decoder identity was synthesized, and no broader rank-shape impossibility is
claimed.

## Candidate and exact budget

The pinned selected profile is
`{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}`. The candidate changes it to
`{1:2412, 2:418, 3:432, 4:142, 5:82, 16:4}`. Both have paid mass 5,586.
The model remains at 73 ports, 896 families, 9 stages, one unpaid coordinate
per family, the existing 64-per-call centre charge and the existing halving
guard. The candidate is charged zero new gathering, copy, frame, restoration,
hosting or precision cost. This is deliberately more favorable than any
physical implementation of this copy-only regrouping at the unchanged model.

The pinned `ceiling.ceiling()` engine returns these certified brackets:

| Profile | Ceiling bracket |
| --- | --- |
| Selected baseline | `[1690054109/10^12, 169005411/10^11]` |
| Eight rank-8 children changed to four rank-16 children | `[1693625547/10^12, 423406387/250000000000]` |

Using the candidate's upper endpoint and the baseline's lower endpoint gives
the conservative relative-gain upper bound
`3571439/1690054109 < 1/20`. The full gain interval is
`[1190479/563351370, 3571439/1690054109]`. Therefore this copy-only block
cannot meet the task's 5% threshold even before charging any implementation
overhead.

The baseline and candidate keep every other paid child, all 64 centre charge,
all coverage inputs and the outer guard unchanged. Any realization that needs
additional copies, frame transitions, restoration, hosting or precision can
only reduce the candidate's ceiling further. The result does not cover moving
rank-1 through rank-5 mass, another block identity, a changed coverage law or a
different word.

## Controls

The verifier has an ideal-only positive budget control that moves all 5,586
mass to fractional rank-16 children; this clears 5%. It is the existing
one-lever relaxation and is explicitly not a construction. A second sensitivity
profile moves only the rank-1 mass and reports its budget without claiming an
identity. The negative accounting control adds the four rank-16 children
without removing the old rank-8 children; its mass rises to 5,650 and its
ceiling falls. This catches an undercharged profile edit.

## Provenance and overlap

- Track/card: `complex-mechanisms / complex-rank-shape-decoder`; priority
  revision 4; seed `ae3e3db974aea7693960685554d84d39`.
- Base: `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`.
- Catalogue SHA-256:
  `d46eb6d5b3e279428753d770653663fbdf1063e55c255ea073d768f344927ef7`.
- Selected-record SHA-256:
  `10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32`.
- Selected review, source manifest and assembly are pinned in `SOURCES.json`.
- The exact ceiling code is pinned as a live input at SHA-256
  `86a1432870b3b21d8454106ec9162fddc0471472d9214c590a1420f2426cedfc`.
- Related open work: [PR #2277](https://github.com/CrocSwap/integer-mult-bounds/pull/2277),
  head `ca7f99921f03398d303bba90245d3ee2e38e95c3`, establishes scoped algebraic
  copy floors; this package evaluates a different, layout-level paid-profile
  change. [PR #2237](https://github.com/CrocSwap/integer-mult-bounds/pull/2237),
  head `bc63155a531d814dd8fa98993d84dc287756ad47`, treats a p=25 root-pair
  boundary.
- Related rank-shape discussions #1952, #1693 and #2003 concern a cyclic
  rank-three masked child, released rank-one-to-rank-two retiming, and a P112
  paired-tetrad support model, respectively. They do not test the eight
  rank-8-copy regrouping screened here.
- The selected T16 whole-helper repacking package
  `research/complex-t16-rare-pattern-exchanges/` keeps the local word and paid
  profile unchanged; its T16 refers to replica count, not rank-16 children.
- No advance claim was posted. Report this completed first-step budget screen
  as a `FINDING`/`DONE` result. It makes no new `kappa` claim.

## Reproduce

From the repository root, run the registered package check and replay with
Python 3.12:

```sh
python3.12 scripts/research_package.py --package research/complex-rank8-copy-rank16-screen-ae3e3d --check-only
python3.12 scripts/research_package.py --package research/complex-rank8-copy-rank16-screen-ae3e3d
```

The verifier checks the pinned ceiling engine, exact base/candidate/ideal
brackets, mass preservation, the 5% comparison and both controls. The selected
record, task catalogue, priority log and related packages are pinned to the
base commit as provenance. In this environment Python 3.12 is unavailable;
the manifest-equivalent optimized isolated replay was run with Python 3.14.7.

## Open next questions

Can an explicit block-frame identity reorganize a substantial part of the
rank-1 through rank-5 mass into larger-rank children while preserving the
selected local operator? It matters because the copy-only block changes too
little mass, while the all-mass ideal relaxation has room to exceed the 5%
gate. For a fresh investigation, name one chronological block, its source and
target frames, every copied direction and each restoration, then screen its
complete profile before synthesis. This screen contains no identity for the
rank-1 through rank-5 portions.

## Credit

The selected profile and ceiling model are attributed to the existing
`complex-local-word-ceiling` and selected-word packages. This package was
prepared with substantial OpenAI Codex assistance; no independent human review
is claimed.
