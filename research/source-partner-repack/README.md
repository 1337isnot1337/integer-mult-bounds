# Repacked owner fill on PR2530's source-partner words: conditional κ = 0.0017137844912361143

**Credit first: PR2530 (zxv, with OpenAI Codex).** The eight source-partner aliases, the 422-helper words, the diagonal call order and windows, and the whole native/global/outer pipeline are PR2530's (`research/source-partner-lifetimes`). They rest on PR2462 and its lineage (Jeremy Kothe and the authors credited there). This package changes **only the owner fill**, which was PR2530's first open question.

## Result

Conditional **κ = 0.0017137844912361143131449999999999999999999998999999999999999999999999**. The exact rational is in [CLAIM.json](CLAIM.json).

- Exceeds PR2530 (0.0017137379215475043467…) by **4.656969e-08**.
- The certified complex endpoint is 342756898247222862629/200000000000000000000000, at the same 1e-24 endpoint grid and outer settings as PR2530.

## What changed

PR2530's fill leaves idle `{1:21976, 3:6662, 5:440, 8:114, 16:172, 32:3, 48:26488}`. Most of the expensive part sits at the start of the diagonal order:

- the rank-16 window (replica 0, child 0) is completely empty;
- (1, 2) is half empty;
- a rank-8 window is empty.

These first windows can draw only on the first few calls, so the shortfall cannot be fixed inside them alone. The repacking moves single 9s into some of those bins (rank-16 → remainder 7). It pays for them by emptying (9,9,9)+5 rank-32 bins and re-concentrating idle elsewhere, so the moment drops.

- New idle: **`{1:21987, 3:6659, 5:423, 7:81, 8:102, 14:2, 16:90, 32:25, 48:26492}`**.
- Local profile and width inventory per call are unchanged: `{1:2369, 2:632, 3:320, 4:118, 5:26, 7:8}` and `{4:33, 5:9, 7:62, 8:78, 9:240}`.
- Rank mass, live stock, deficit, call order and windows are unchanged.
- Global profile: [PROFILE.json](PROFILE.json).

**Method** (offline; only the result is shipped and verified literally). I used large-neighbourhood search with an exact CP-SAT subproblem (OR-tools 9.15):

- Each step frees every role in about 80 bins: holes plus donor bins of time-overlapping windows.
- It re-solves their placement exactly under the package's own owner rules: each role inside its window, bin capacity and prefix packing, and one role per call and physical family.
- It minimises the idle moment weight at fixed a.
- A step is applied only on strict improvement. The search starts from PR2530's own fill.

The pattern LP of PR2387/PR2442 (thakrarsagar) caps any whole-helper fill of these words at b < 0.0017142284. Further repacking or a different order may still help.

## Reproduction

```sh
python3 -B research/source-partner-repack/verify.py            # bounded: build, literal owners, controls, bindings
python3 -B research/source-partner-repack/full_replay.py --work /fresh/absolute/dir
```

`build.py` runs PR2530's unchanged `build.py`, including its own word regeneration and checks. It then substitutes `evidence/repack-fill.json.gz` and re-runs the package's own `reconstruct.py` and `lift_parent.py`.

`full_replay.py` runs the same stages as PR2530's: retained parent, natives, rebind, discovery, strict global admission, geometry controls, exact outer ledger, independent balance and the nineteen outer evidence replays. It can reuse a completed retained-parent directory and native directories, each status- and hash-checked; the defaults are fresh.

Receipts are in `receipts/`: the full replay and its stages, and the bounded run.

## Open next questions

- **How much of the remaining relaxed gap is forced by the diagonal windows?** The window-free pattern LP (b < 0.0017142284) ignores time windows. Adding per-width interval (Hall) cuts for these windows would give a window-aware ceiling to compare with this fill.
- **Can a different call order remove the start-of-order holes?** Most of the remaining idle cost sits in the first rank-16 and rank-8 windows of the diagonal order. Screening order variants needs a fast fill heuristic per order, then a literal fill and a full replay.

## Scope

This is a conditional finite construction, exactly as PR2530. These obligations remain: all-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape, exact recovery, analytic transfer, the PR559 recurrence correction and PR589 bit H1–H5. No unconditional theorem, independent human review or global packing optimality is claimed.

## Credits

- PR2530 (zxv): source-partner lifetimes, the diagonal order and the whole package this one builds on.
- PR2462, PR2447, PR2435 and the T74 line (Jeremy Kothe).
- PR2436 (tekuuu).
- PR2322 (Vlado Vojdanovski).
- PR2226 (Cinna Davis).
- PR2387, PR2442 and PR2466 (thakrarsagar): the pattern-LP ceiling and owner-optimality method.
- Everyone credited in the source package's READMEs and notices.

New here: the repacked fill and this wrapper, by Rohan Arun with AI assistance (Claude). Apache-2.0.
