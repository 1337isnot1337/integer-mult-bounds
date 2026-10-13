# X54 on the three-demotion k8 word, with #1148's T16 owners

```text
kappa = 0.001675161536733127
```

That is **+3.98889e-8 over #1148** (0.001675121647789207, the current best open result). The complex side binds; the
PR589 bit supplier is unchanged.

## Change

The eighth triangle-hybrid slot **X54/E589** (Jeremy Kothe's #1130 recipe) is applied to Thomas DiFiore's
three-demotion k8 word (#1148, `research/k8-three-demotions/FULL-WORD.json.gz`).

- `RECIPE-X54-dem.json` is #1130's `RECIPE-X54-ends7.json` with **identical edits and frames**: 5 B deletes and
  5 inserts, a FULL restore of holder 335 and an early restore of holder 367. Only the base and result pins and the
  profile change.
- NewBArch's unchanged `build_tri.py` gives word content `bffd102a…`.
- The slot is width-neutral. Widths `{4:44, 5:44, 7:38, 8:114, 9:240}`, entrances, start/end frames, local prefixes
  and the owner interface are unchanged. #1148's T16 owner map (`research/k8-three-demotions/OWNERS.json.gz`) is used
  unchanged, so the idle stays `{1:360, 24:1, 48:4918}`.
- Local profile `{1:2372, 2:494, 3:412, 4:130, 5:82, 8:8}` → `{1:2372, 2:494, 3:414, 4:126, 5:84, 8:8}`.
- Global profile: `{1:341928, 2:71136, 3:59616, 4:18144, 5:12096, 8:1152, 24:1, 48:4918}`.

## Verification

```sh
python -B research/k8-dem-x54/verify.py --base /abs/seven-slot-k8-word.json.gz --work /abs/new-dir
# optional reuse: --parent-from <completed research/k8-eight-ends-t16/verify.py work dir> --native-from <native dir>
# PASS_X54_ON_THREE_DEMOTIONS_COMPLETE_ADMISSION 0.001675161536733127
```

The steps are:

1. Rebuild #1148's parent geometry (`research/k8-eight-ends-t16/verify.py`), pinned by #1148's `PARENT-PINS.json`.
2. Build the word.
3. Run the independent `audit_local`: exact forward/dual endpoints, frames, entrances and cones.
4. Run NewBArch's unchanged `run_controls.py`. That is 10 outcomes: C0, the recipe, and drop_restore / restore_full /
   drop_preread / donation_after, both globally and for X=54.
5. Run PR635's native chain (`research/k8-eight-ends/replay_native.py`).
6. Check the rebound plan identities.
7. Run **#1148's unchanged `run_global.py`** strict T16 admission. It covers bind, emit, the controller audit with 15
   mutations, the invoice (prefix < 512, row < 20,161), assembly with all 47 outer inequalities, 69 admission and 12
   bit-supplier controls, and the six independent T16 controls.

`data/PLAN.json.gz` is #1148's plan with its provider identities rebound to the new locals: semantic artifact ids,
the LOCAL-CHECKS pin and both program hashes, plus the paid and global profiles. `data/SPEC.json` was re-frozen by the
unchanged `run_global.py --discover` and `freeze_spec.py`. Receipts are in `evidence/` (Linux, Python 3.13).

## Credits

- **Thomas DiFiore** (#1148): the three-demotion word, the T16 owners and the admission runner.
- **Jeremy Kothe**: the X54 slot recipe (#1130), the seven-slot k8 word (#1018/#1074) and the leaver chain (#1005).
- **NewBArch**: the triangle-hybrid move, plus the unchanged builder and controls.
- **Alexander Schwartzman** (#1030): rank-seven ends.
- **Rohan Arun** (#987): the slot search behind the k8 slots.
- **Hao Yan**: the T16 machinery.
- Every contributor credited in the retained notices.

Composition by Rohan Arun with Claude (Anthropic), Apache-2.0.
