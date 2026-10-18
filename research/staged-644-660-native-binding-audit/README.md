# Staged helpers 644/660: native entrance residual under a separate kernel

**Finite native/interface audit; no new kappa, supplier admission or frontier change.**

PR3605 lowers helpers 644 and 660 from width 8 to width 7 by letting them enter
at `span(429,30)` instead of `span(30)`. Its consumers reuse those STAGED
words: #3624, #3626, #3630, #3633 and #3638. PR3687 checked the words as exact
free-operator identities. It left one question open: do the **native phases** of
the paired `span(429,30)` entrance hold, checked without the `bw_*` lineage code?
This package answers that question for both providers and both orientations.
The answer is **yes**.

- **The width-7 residual is exact.** The emitted recipe for `span(429,30) -> FULL`
  satisfies `R · F_7 · L = T_E^-1 · T_FULL` on all 512 Gaussian columns,
  including global phase. Its wrapped form `L^-1 T_E^-1 T_FULL R^-1 = F_7` and
  inverse-transpose form also hold. The check uses Sagar Thakrar's separately
  written kernel `research/frontier1094-recipes-exact-seed76/clifford.py`,
  which imports no repository code. No `bw_*` module takes part in it.
- **The emitted program uses exactly this recipe for 644 and 660.** The
  unchanged producer emits one `pre`/`post` residual wrapper pair at frame
  `[429,30]`, with no terminal field. There is one ordinary `new_to_old` exit
  adapter at FULL and no private buffer, in both orientations. The climbs are
  `[2,1,2,1,1]` for 644 and `[2,2,1,1,1]` for 660. Both sum to 7, and each of
  the ten distinct climb recipes also passes the separate kernel. All 17 direct
  scalar clocks per helper match the source word, including the 8 FULL-frame
  cleanup gates.
- **Only this residual changes.** As a single-change control, the parent PR3133
  words go through the same producer. There, 644/660 enter at `span(30)` with
  width 8, and their first climb is 3 instead of 2; the later climbs are
  identical. Across all 408 helpers, only 644 and 660 change their
  entrance/terminal pair. The residual classes go from 57 to 58, and the new
  class is `([429,30], FULL)`.

Expected verifier line:

```text
PASS_STAGED_644_660_NATIVE_BINDING providers=2 helpers=644,660 entrance=span(429,30) terminal=FULL residual_width=7 parent_width=8 shared_key=137 climb_recipes=10 controls=7x2 single_change=2 both_orientations no_new_kappa
```

## What the check does

For entrance `E` and terminal `U`, the native residual is `S(E,U) = T_U T_E^-1`.
The source compiler factors it as `S = L F_w R`, where `F_w` is the coordinate
Fourier primitive on the first `w` axes, and `w = dim U - dim E`. Here
`E = [429,30]`, `U = FULL` and `w = 7`; the other two axes are spectators.

1. The verifier runs the pinned `bw_transport.py` and `bw_emit.py` (byte-identical
   to the copies used by the #2979 group audits) on PR3605's two STAGED words.
   It then binds every emitted event of helpers 644/660 to the source word. It
   checks the wrapper entrance, the climb chain from `[429,30]` to FULL, the one
   exit adapter, the event order (wrapper, climbs, exit, cleanup, wrapper) and
   every direct scalar clock.
2. It rebuilds the serialized residual-adapter file with the source compiler,
   and the separate kernel then checks the shared recipe (key `137`) and every
   climb recipe.
3. It runs the parent PR3133 words through the same producer as the
   single-change control above, and checks the parent's width-8 recipe too.
4. It rejects seven residual controls per provider. Three fail at the
   all-column operator check: a global-phase change, the parent's right wrapper
   substituted, and the same-dimension wrong plane `[429,18]`. Four fail at the
   width check: no entrance, the contained line `[429]`, the old entrance `[30]`
   and the parent recipe at the new entrance.

`test_verify.py` adds corruptions that must fail through the same code paths.
These include a missing `post` wrapper, a wrong wrapper frame, a restored-helper
terminal field, a deleted or mis-ranked climb, and an entry adapter in place of
the exit adapter. They also cover a moved exit adapter, an added private
buffer, a sign-flipped scalar and the wrong orientation. Word, recipe and
source-pin corruptions are covered as well. One finding came from a wrong test
expectation: `[30,429]`, the same plane with its basis reordered, passes the
identity. So the kernel checks the subspace, not the order of its basis. The
same-plane case is not a control here.

## Sources

The base is canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority
revision 6 (κ = `0.001672660197076918`). [SOURCES.json](SOURCES.json) pins every
input by Git blob and SHA-256.

- **Staged words.** `inputs/STAGED644-660-{base,extra}.json.gz` are byte copies
  of `research/staged-644-660-width-reduction/STAGED644-660-*.json.gz` at PR3605
  head `3efbb5de06a49ffeea6684482f2d3fe48cdca3fb`. The repository's `head:` pin
  must name the live path, so these copies are pinned as provenance rows under
  their original path. The verifier checks the copies' bytes against those pins.
  The hashes also match PR3605's `ARTIFACTS.json`.
- **Parent words.** These are PR3133's `edits/FINAL-WORD-{base,extra}.json.gz`
  on main.
- **Producer and compiler.** These are the retained t74-native-fast
  `bw_transport.py`, `bw_emit.py` and `vendor/clifford/clifford_exact.py`. They
  are producers, not independent evidence.

The author's own checks are PR3605's full native chain and `check_residual.py`.
Both use the `bw_gauss` lineage kernel (`bw_adapters.py`, `bw_gauss.py`). They
check one abstract `(E,U)` pair and do not bind the emitted helper events.

**Local-only cross-check (not part of the registered replay).** The producer's
own `bw_adapters.py` needs numpy. Under Python 3.13.1 and numpy 2.2.2 (not
PR3605's declared numpy 2.5.4), it wrote a `RESIDUAL-ADAPTERS.json` for each
provider. The LF-normalized bytes equal this package's reconstruction:
`a19e744f…` (base) and `c4ddd4db…` (extra). So the recipe checked here is the
one the native chain serializes. On Windows, `bw_adapters.py` writes CRLF
through `write_text`.

## Reproduction

```sh
python3 -I -B research/staged-644-660-native-binding-audit/verify.py
python3 -I -B research/staged-644-660-native-binding-audit/test_verify.py -v
python3 -B scripts/research_package.py --package research/staged-644-660-native-binding-audit --check-only
python3.12 -Werror -B scripts/research_package.py --package research/staged-644-660-native-binding-audit
```

These use only the Python 3.12 standard library, and take about 30 seconds
and 7 seconds on a Windows 11 laptop. PR3605's commit must be present for the
provenance pins (for example
`git fetch origin refs/pull/3605/head`).

## Scope and unchecked obligations

This checks the native entrance of the two changed helpers. It does not check:

- the native phases of the other 57 residual classes, the 240 warps or the
  scalar macros under an independent kernel;
- the retimed or delayed consumer words;
- owner journals, physical stock, prefix, precision and tape;
- the T740 or consumer releases;
- the inherited all-size compiler, analytic transfer and BIT hypotheses.

A passing finite audit does not admit a supplier or change the selected record.

## Open next questions

The structured list is in [TASK.json](TASK.json).

1. **Do the retimed (#3642/#3653) and delayed (#3682) words keep this entrance
   residual?** If their 644/660 entrance/terminal pairs and recipe are
   unchanged, this check covers those consumers too. First step: vendor those
   words and run `native.provider()` on each, with the STAGED words as the
   control.
2. **Do all 58 residual classes and 240 warps pass the separate kernel?**
   Loop `check_recipe` over every reconstructed adapter key, and check each
   warp record as a monomial identity.
3. **Is the complete emitted 644/660 lane phase-exact under an independent
   simulator?** This would need an emitted-event interpreter for the scalar
   macros and warps, compared with PR3687's free-operator endpoint.

## Credit

- **Construction:** Ross Richardson's PR3605.
- **Parent words:** dcharb78's PR3133, with the word lineage credited there.
- **Open question:** Sagar Thakrar's PR3687 posed the question answered here.
- **Separate kernel:** Sagar Thakrar's, from frontier1094-recipes-exact-seed76.
- **Producer lineage:** DreamingOfClouds/PR458, retained t74-native-fast
  (PR2226 notices).
- **Method and code:** adapted from Wentao Li's
  `research/rank7-group-d-native-widths-audit/`, which in turn adapts the
  group A–C audits.

Prepared by Mainzu with substantial assistance from Claude Code (Anthropic,
Claude Opus 5.5). No independent human or formal-kernel review is claimed.
Apache-2.0.
