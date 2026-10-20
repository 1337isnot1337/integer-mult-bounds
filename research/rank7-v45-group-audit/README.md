# Independent audit of #2979 group V45

**Partial frame-surrogate certificate. No new κ.** Selected κ stays
`0.001672660197076918`. PR #2979's conditional κ ≈ 0.001729 is not selected
and is not re-certified here.

On both PR #2942 parent words, the four restored helpers 249, 251, 265 and 267
share one rank-7 end frame

```text
W = ⟨256, 128, 64, 35, 16, 11, 5⟩ = E_7 ∩ E_42 = E_7 ∩ E_42 ∩ E_45
```

because `7 ⊕ 42 = 45`. Lowering any proper subset of those four end frames, after
the 61 gate frames that land only in `W`, loses money under #2979's published
integer frame weights. Lowering all four gains **22,972** surrogate units.
The shared gate-frame overhead is **78,512** units, and each added helper then
saves exactly one rank-1 climb, `c_1 = 2,116,671`.

## What was checked

The parents are `research/rank7-joint-endframes/data/PARENT-base.json.gz` and
`PARENT-extra.json.gz`, with the stage-1 record
`STAGE1-FRAME-EDITS.json`. Group V45 owns the 61 edits whose new frame is
contained in `W` and in no other declared group frame (20 in `B`, 41 in
`restore`). No `A` gate moves. Scalars, operators and the cleanup list are
unchanged, and the private-buffer count stays 86.

The paid profile is recomputed by a separate transcription of the inherited
climb rules (monotone subspace climbs, warp resets, centre and target cuts,
final climb to the live end frame). It is not imported from
`rank7-joint-endframes/producer.py` or from `STAGE-PRICES.json`. Calibration:
both stored parent profiles and width inventories are reproduced before any
edit. Weights are the published surrogate

```text
c = (2116671, 4228346, 6338140, 8446713, 10554378, 12661320, 14767661, 16873488, 18978865)
```

at the recorded base saving, and the break-even charge for one freed width is
`c_1 - 25371 = 2091300`. This package does not re-derive `c_r` from the moment
engines.

For a subset of `k` helpers, with those end frames set to `W` and all 61 gate
frames applied, the margin is `-Δ - k·2091300`. Both providers give the same
margins:

| k | subsets | margin |
|---:|---:|---:|
| 0 | 1 | −78,512 |
| 1 | 4 | −53,141 |
| 2 | 6 | −27,770 |
| 3 | 4 | −2,399 |
| 4 | 1 | **+22,972** |

The `k = 4` profile delta is `−8,388,172`, and the width inventory moves four
units from width 8 to width 7. The identity

```text
4·25371 − 78512 = 22972
```

is the whole joint margin: partner frames are paid once, and each helper
returns `c_1` against a break-even of `c_1 - 25371`. Every one-helper control
loses. Omitting the first helper-touching edit, or putting that gate's old
frame back, makes the word nonmonotone.

## What this does not establish

Groups A–D, the five paired extractions, the fourteen rewrites, the T74
allocation, idle packing, native admission and both supplier caps are
unchecked. A positive local margin in this surrogate is not a multiplication
exponent. `research/rank7-joint-endframes-restore-edit` starts from the #2979
words and does not replace this group check. PR #3585 records archive blobs
only.

## Reproduce

Python 3.12, standard library, from the repository root:

```sh
python3 -B research/rank7-v45-group-audit/verify.py
python3 -B scripts/research_package.py --package research/rank7-v45-group-audit
```

Expected first line:

```text
PASS_RANK7_V45_GROUP_AUDIT providers=2 edits=61 sections=20+41 joint_delta=-8388172 joint_margin=22972 single_margin=-53141 pair_margin=-27770 triple_margin=-2399 frame_only_margin=-78512 overhead=78512 width_8_to_7=4 buffers=86 cleanup_unchanged=yes controls=omit-edit,stale-frame
```

The direct verifier finished in about 6 seconds on the recorded host.

## Open next questions

1. Isolate groups A, B, C and D by the same containment rule and test whether
   each added helper saves exactly `c_1` after one shared overhead. That is the
   same finite check; it was not run here.
2. Enclose `c_r` independently at `b = 0.001703676387993676` and price this
   profile delta through the idle-width cap. Until that is done, the unit
   margin does not move κ. The frame-domain-ceiling engines are the blocker.

## Credit

Marius-Paul Dumitrean (Dugongue / mdumitrean), PR #2979, for the words, the
V45 claim and the published weights under audit. The parent words descend from
Mason Hale's PR #2917 and the PR #2942 extractions; frame climb rules are
Jeremy Kothe's, from the PR #2894 lineage. Jeremy Diviney's paired-extraction
method and Dugongue's PR #2969 comparator sit behind that claim and are not
rechecked here. Archive disposition PR #3585 is separate.

Prepared by unpaidmoon with substantial AI assistance (Cursor Grok). No
independent human or formal-kernel review is claimed. Apache-2.0.
