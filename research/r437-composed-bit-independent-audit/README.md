# Independent audit of PR #3647's composed R437 bit word, hosting and price

PR #3647 composes two helper deletions on the selected #589 bit word. The
helper464 deletion re-synthesizes one D4 node with a ten-gate GL block. The
helper470 deletion comes from #1043 and replaces a carrier with a late read of
SOURCE77. This package checks the resulting 659-input R437 word, its local-call
records, its hosted template and its price. The interpreter, controls and
price engine are written separately for this audit, and the word is checked
against both single-change controls. **At head `36ff4414` every check
passes**:

- **Word.** Over F2 the word maps every input `(x, y, h)` to `(x, y + x, h)`.
  Here `x` is the 111 SOURCEs, `y` the 111 targets and `h` the 437 helpers
  with arbitrary dirty contents. The two edits compose with no interaction
  beyond the single-change controls. The SOURCE77 read at frame 186 is in
  chronological order, and the literal word gives the claimed local profile.
- **Records and hosting.** The PR's 27,132-record stream is byte-identical to
  an independent lowering of the word. The hosted template's 125,856 helper
  placements satisfy the selected chain's idle-hosting rule.
- **Price.** The whole paid profile and the invoice's precision fields follow
  from these. The price root gives
  **c = 868314126713557740143/5·10^23 = 0.001736628253427115480286**, and the
  next 10^-24 grid point fails.
- **Controls.** The same price engine reproduces the selected #589 value
  `0.001733427039589844234749` from main-only inputs, and #1043's
  `0.001734176288479865766692`.

This is a finite, exact, **independent check of one local bit supplier**,
under the selected chain's inherited semantics: word format, hosting rule,
invoice formula and price equation. It makes no κ claim and changes no
frontier, and it does not admit PR #3647. Physical-owner, native-transport and
all-size assumptions stay as inherited (see Scope). The selected record stays
`0.001672660197076918`. The complex side binds today.

Reproduce from the repository root (standard library only, about 10 s):

```sh
python3 -I -B research/r437-composed-bit-independent-audit/verify.py
```

Expected output: `PASS_INDEPENDENT_R437_WORD_AUDIT cpu <seconds>`. The command
recomputes everything and requires byte equality with the committed
[RESULT.json](RESULT.json). `--write` regenerates it.

## Why it matters, and to whom

The selected #589 bit supplier caps the retained balanced transfer at
a/(1+a) = 0.0017304274698236. The pending complex chain of PR #3653 and
PR #3682 claims κ = 0.0017304189, which is 8.57e-9 below that cap. **If that
chain is admitted, the bit primitive binds**, and further gains need an
admitted better bit supplier. PR #3647 makes the highest open bit claim, with
cap c/(1+c) = 0.0017336176. Before this package it had author checks only.
PR #3668 (jwr404) checks the histogram-to-c arithmetic on the *published*
histogram. Here that histogram is rederived from the word and the template.

## What was audited

- **Object.** [PR #3647](https://github.com/CrocSwap/integer-mult-bounds/pull/3647)
  (ai-nanachi), head `36ff441479ff9c7e70d83f0becccd44da50effb8`, package
  `research/bit-p111-r437-gl464-470-20261018`. [inputs/](inputs/) holds
  vendored copies, each pinned by Git blob and SHA256 in
  [SOURCES.json](SOURCES.json):
  - the R437 word (`data/r0042/R437-COMPOSED-WORD.json.gz`);
  - its R438 helper464-only ancestor (`data/r0028/FINAL-R438-WORD.json.gz`);
  - the R437 record stream (`data/r0042/R437-RECORDS.bin`, stored gzipped);
  - the hosted template (`generated/GLOBAL-TEMPLATE.json.gz`). Its canonical
    content SHA256 `2e868ff4…` equals the PR's EXPECTED value.
- **Reference word.** The selected #589 word on main:
  `research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz`. The PR's
  `data/SELECTED589.json.gz` is byte-identical to it.
- **helper470 control.** #1043 (Ali Romman), archive-merged on main as
  `research/bit-boundary-persistence/`. The control is rebuilt here from the
  edit in its PROOF.md, then compared with its `FRAME-PATHS.json` and
  `CERTIFICATE.json`.
- **Semantics.** All of it is taken from the selected chain on main:
  - word format: `research/e8-bit-p111-tuned/code/xcheck_p.py` and
    `code/pwordl.py`;
  - record and event layout, parent recipe, idle ranks and prefix bound: the
    nine-stage caller `vendor/pr510/…/global_k.py`;
  - invoice coefficient formula: `vendor/pr510/e8-r480-nine-stage/code/assemble9.py`;
  - idle-hosting rule: `research/e8-bit-carrier-skeleton/code/hub/idle-axis-hosting/hosting_core.py`;
  - price equation: `…/e8-r740-replica32/code/engines/moment.py`.

  **No code from PR #3647, #1043 or main is imported or run.** Each rule is
  reimplemented here from its source text.

## The two edits, in #589 numbering

| Edit | Removed | Added |
|---|---|---|
| E464 (PR #3647 ancestry) | `A[224] = [56, h464, [x54]]`; the three-gate D4 node `A[1986..1988]` at frame 506, two of whose gates read h464 | ten gates at frame 506 on h340, h241 and h349, which read x6, x56, h233, h319, h322, h462 and h463 (25 operands) |
| E470 (#1043) | `A[230] = [79, h470, [x77]]` and `A[1993] = [79, h444, [h470]]` | `[186, h444, [x77]]` in place of `A[1993]` |

In both edits the deleted helper is removed, higher ids are renumbered, D0 is
rebuilt from the raw word, and C is rebuilt as the literal reverse of every A/B
gate whose destination is a source or helper, at the full frame.

## Results (all exact; numbers from RESULT.json)

| Word | Inputs | Gates D/A/B/C | Scalar ADDs | Local profile | Mass |
|---|---:|---|---:|---|---:|
| selected #589 | 661 | 111/2075/712/2574 | 24,305 | {1:1323, 2:1342, 3:79, 4:44, 5:102, 6:11, 7:19} | 5,129 |
| #589 + E464 (= PR R438) | 660 | 111/2081/712/2580 | 24,265 | {1:1322, 2:1342, 3:78, 4:43, 5:102, 6:11, 7:19} | 5,121 |
| #589 + E470 (#1043 R438, rebuilt) | 660 | 111/2074/712/2573 | 24,248 | {1:1321, 2:1344, 3:78, 4:44, 5:102, 6:11, 7:18} | 5,121 |
| **R437 (PR #3647)** | **659** | 111/2080/712/2579 | **24,208** | **{1:1320, 2:1344, 3:77, 4:43, 5:102, 6:11, 7:18}** | **5,113** |

### Word level

1. **Identity, two methods.** The primary method is a forward replay. Register
   `r` starts as the column bitset `1 << r`, so one pass covers every input
   column over F2. Every operand makes a strictly increasing, nested climb to
   the gate's frame. Dimensions and nesting are computed from the E8 line
   vectors over Q. The final frames are FULL for sources and helpers and t-perp
   for targets. The second method is a reverse pull-back, the transpose action
   with gates in reverse order. It yields, for each input, the set of outputs
   that depend on it. For all four words both methods give `(x, y + x, h)`, and
   they agree on every entry of the 659 × 659 matrix (660², 661² for the
   controls). The replay is symbolic on a basis and every gate is F2-linear, so
   this proves the identity for all input values. It is not a sample. The
   literal reverse orientation also passes: gates are reversed, and frames
   descend, which is a climb of the orthogonal complement. Over F2 it is implied
   by the forward check. All 636 frames are closed in the live lines
   (70,596 memberships). The finite hypotheses H1–H5 of the selected
   interleaved lemma and its U/J conclusions hold. D0 and C are equal to the
   rebuilt ones.
2. **Composition.** Applying E464 and E470 literally to #589 and rebuilding D0
   and C gives the PR's R437 word. All fields are equal; only the `stats`
   metadata differs (`extra_carriers` 10 → 8). E464 alone gives the PR's R438
   word. E470 alone reproduces #1043's published results:
   - every frame path in its `FRAME-PATHS.json` (660 candidate and 661 baseline
     paths);
   - its D0 change from 18,085 to 18,030 ADDs;
   - its 2,573-gate C;
   - its profile table.
3. **No interaction.** Traces are aligned gate by gate across about 5,350
   common gates per comparison. The deleted helpers' columns are projected
   away, and survivors are renamed.
   - **E470** changes no value at all.
   - **E464** changes no clean (x or y) column anywhere. It changes only helper
     340's arbitrary-dirt column, at four A gates of #589: `A[2044]` (h340),
     `A[2047]` (h241), and `A[2068]` and `A[2070]`, which write the retained
     totals h477 and h478. The same column also changes at the four literal
     inverses of these gates in C.
   - **Composed word.** Its trace equals the E464 control's trace with h470's
     column deleted, at all 5,369 aligned gates. It equals the E470 control's
     trace with h464's column deleted, except at exactly those eight gates.
   - **Profile deltas** add exactly: E464 gives −e1−e3−e4, E470 gives
     −2e1+2e2−e3−e7, and R437 − #589 = −3e1+2e2−2e3−e4−e7. R437 − R438(E464)
     is −2e1+2e2−e3−e7 (mass −8), as the PR states.
   - **Compensation.** R437's D0 is the E464 control's D0 with column h470
     deleted. For E464 alone, D0 is **not** a column deletion of #589's D0,
     because the h340 dirt reaches two COPY sources.
4. **SOURCE boundaries and chronology.**
   - **Source writes.** There are A0/B483/C483 source writes. All 966
     source-write gates hold, before and after, the same full rows as in #589,
     with the deleted dirt columns projected away.
   - **Climbs.** Every one of the 111 SOURCEs climbs through the same frames as
     in #589, between the same unchanged gates.
   - **Access histories** differ only at the edits. x54 loses its read at
     `A[224]`. x77 loses its read at frame 79 at `A[230]` and gains the frame-186
     read. The x6 and x56 reads move inside the re-synthesized node's window.
   - **The new read.** At the frame-186 read (lines {33, 77}, rational dimension
     2), x77 holds exactly its input column, with no dirt. It reached frame 186
     at `A[426]`, as in #589. Its later climbs, at B289, B525, B636 and the C
     inverse of B525, are unchanged. The receiver's path is
     0 → 186 → 509 → 392 → 513 → FULL, where #589 has 0 → 79 → 509 → ….

### Records, hosting, invoice and price

5. **Records.** The PR's stream has 27,132 records (651,168 bytes, SHA256
   `caeb2eb0…de13cb`). It equals byte for byte a lowering written here from the
   word semantics: lazy climbs, one ADD per operand, one COPY/ADD/ERASE episode
   per retained total, then the final climbs. The stream is replayed in both
   orientations with the selected caller's record semantics. Both pass all 659
   columns with 24,208 ADDs, 9 rank-7 COPYs and the local profile. The
   cancellation-free row bounds are 49,347 forward (16 bits) and 1,113,998
   reverse (21 bits). The template's forward and reverse local programs equal
   the events derived from this stream.
6. **Hosting.**
   - **Schedule and windows.** The template's parent schedule equals the one
     derived here from main's nine-stage recipe, including idle ranks
     14, 7, 28, 7, 42, 7, 42, 28, 14 and 0. Under the selected rule, its nine
     idle windows are recomputed and equal the template's. The rule: a stage
     may use a pair's idle child only if it runs strictly after the pair's last
     local or bridge touch and is not on that pair.
   - **Slots.** Each replica has 3,933 slots. Each (stage, helper) occurrence
     appears exactly once, with width 8 as the word requires. Its stage lies in
     its window, and its offsets are disjoint inside the child's rank.
   - **Remainders.** They equal the template's, giving the per-replica idle
     children `{2:431, 4:444, 6:444, 7:666, 34:2, 42:11}`.
   - **Owners.** All 288 calls (9 stages × 32 replicas) match the slots and the
     selected data route. The data families form the call's pair block, with
     the sides swapped in reverse sweeps. Each hosted helper sits in a
     different pair's idle child at its slot. In total 125,856 occurrences are
     hosted, with 0 banks and 7,814,016 local events.
7. **Whole paid profile and invoice.** 288 × the local profile plus 32 × the
   idle children gives
   `{1:380160, 2:400864, 3:22176, 4:26592, 5:29376, 6:17376, 7:26496, 34:64, 42:352}`.
   That is 903,456 children of rank mass 1,808,352 = 64·28,416 − 10,272,
   exactly as published. The invoice precision fields are recomputed with the
   selected formulas, as an envelope over every non-prefix term:
   - prefix 2^18 · 49,347^5 · 1,113,998^4 has 177 bits, charged 192;
   - the coefficient has 177 bits;
   - the two-level coefficient has 393 bits, charged 512;
   - halving depth 2, with 2·42² = 3,528 < 4,096;
   - ROW = 2·(64² + 1) + 9,909 + 252 = 18,355 < 20,161.

   The ROW constants 9,909 and 252 are inherited.
8. **Price.** The equation is
   `Σ r·n_r/(m·W) (m/r)^a + 32·m·N/(10^16·W) m^a = 1` with m = 64 and
   W = 28,416, including the inherited bad-class fallback. It is solved with
   separate rational log/exp enclosures. At a = c the moment is < 1, and at
   c + 10^-24 it is > 1, for
   c = **0.001736628253427115480286**. The same engine gives two positive
   controls:
   - **Selected #589.** The value is built from main only: the #589 word gives
     the local profile, `selection9-p111.json` the hosting patterns, and main's
     recipe the windows. Its idle children are `{2:435, 4:444, 6:444, 7:666, 42:9}`.
     It reproduces the selected bit value 0.001733427039589844234749 exactly at
     the 10^-24 grid.
   - **#1043.** Its certificate profile splits exactly over the rebuilt E470
     local profile, and the engine reproduces its c, 0.001734176288479865766692.

### Mutants and controls (each must be rejected; one positive control must pass)

| Mutant | Outcome |
|---|---|
| D0 dropped | identity fails on 111 columns |
| C dropped | identity fails on 545 columns |
| #589's D0 reused (deleted helpers dropped, renamed) | identity fails on 54 columns |
| #589's C reused (same projection) | identity fails on 3 columns |
| replacement read at frame 79 | illegal climb: x77 would descend from 186 to 79 |
| replacement read moved early, to the removed birth | **F2 identity and frame legality still pass**; rejected only by the SOURCE chronology check (x77 reaches 186 before `A[426]`) |
| replacement read dropped | identity fails on 55 columns |
| naive helper464 deletion (old node, h464 operands dropped) | identity fails on 54 columns |
| each of the ten GL gates dropped in turn | identity fails on 53–63 columns |
| a slot moved to a window outside its stage | window, disjointness, remainder, owner and profile checks fail |
| two slots made to overlap | disjointness and owner checks fail |
| a slot dropped | occurrence, remainder, owner and profile checks fail |
| one idle rank changed | window, remainder and profile checks fail |
| one rank-2 child per replica relabelled as rank 3 in the whole profile | the c bracket fails |
| the composed word itself (positive control) | accepted |

The early-read row shows that the identity check alone does not enforce SOURCE
chronology. The chronology comparison with #589 is a separate, load-bearing
check. In the price bracket, each next grid point acts as a built-in negative
control.

## Scope, inherited assumptions and unresolved obligations

These results are checked:

- the local F2 identity and frame legality of the literal R437 word and both
  controls;
- deletion composition at gate and trace level;
- SOURCE write boundaries and chronology against #589;
- the local profile and ADD counts;
- the byte binding of the records and the template's local programs to the
  word;
- the hosting slot assignment under the selected idle rule;
- the whole paid profile, the invoice precision fields and the price root.

These are **not** checked:

- **Physical semantics.** Owner routes are checked against the selected rule
  and route formulas, not against a physical register machine. The private
  centre reserve (physical = 28,416 + 9) and the cover classes are not
  checked.
- **Native transport.** The rational projector identities (D_F, P_A P_B) that
  PR #3647's R437-LOCAL proof states are not checked beyond the frame
  nesting/dimension model.
- **Inherited formulas.** The invoice formula, the 10^-16 fallback, the ROW
  constants and the price equation are used as stated in the selected sources,
  not re-derived.
- **Route factors.** The geometry's `max_route_factors` term is covered only by
  the envelope; any value below 2^40 gives the same bit lengths.
- **Inherited assumptions.** These are unchanged from selected #589: the
  all-size bit/Gaussian compiler, the common-label, mutable-SOURCE and
  target-label realization, whole-call correlated hosting, tape and
  precision, the analytic H1–H5 lemma (only its finite hypotheses are
  evaluated here, not its proof) and the cited outer assembly.

This is a finite certificate for one local supplier instance and its hosted
invoice. It is not a scoped all-size proof or a multiplication theorem, and it
does not admit PR #3647. It also makes no κ claim. Today the complex primitive
binds. The bit side would bind only if the pending complex chain
(PR #3653/PR #3682) were admitted.

## Open next questions

[TASK.json](TASK.json) structures these.

1. **Is the dirt-only change to two COPY sources contract-neutral?** E464
   changes the arbitrary-dirt content of the retained totals h477 and h478 (two
   rank-7 captures) by helper 340's column, while their clean rows are
   unchanged. The question is whether the inherited capture contract (one paid
   transform plus linear private-stream discard) is provably independent of
   the dirt pattern of a captured total. First step: state the native capture
   lemma's hypotheses as used by selected #589, and check them on these two
   captures.
2. **Do the native projector identities hold for the changed paths?** The paths
   are receiver 444 (0 → 186 → 509) and the GL node at frame 506. First step:
   build the exact rational projectors of frames 0, 79, 186, 506 and 509 from
   the E8 lines, and check P_A P_B = P_A and D_(B−A) D_A = D_B on these
   transitions.
3. **Which admission dependencies remain?** For PR #3647 to supply the bit side,
   the complex chain PR #3653/PR #3682 must first make the bit side binding.
   After that, maintainers must accept the inherited interfaces. First step:
   reconcile this package's checks with the PR #3653/#3682 review state when
   that chain is reviewed.

## Predecessors and credit

- **PR #3647** (ai-nanachi; substantial OpenAI Codex assistance per its
  README): the R437 composition, the helper464 GL edit, the records, the
  hosted template and the claimed c, all audited here.
- **#1043** (Ali Romman): the helper470 deletion and its source-boundary proof
  on main. Its other replays (PR #1302, PR #2971, PR #2653) cover helper470
  alone and are cited, not redone.
- **Selected #589 chain** (eumemic, DreamingOfClouds, DaysSky's #442 hosting,
  #510/#463 nine-stage caller and invoice, and the credited chain in their
  NOTICEs): every semantic rule used here.
- **PR #3668** (jwr404): histogram-to-c arithmetic on the published
  histogram. This package rederives the histogram instead.
- This loop's earlier audit, PR #3687, supplied the audit pattern only. It
  covered a different, complex supplier.

## Provenance

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). Base commit
`20ecf2891d80b5acf18d980b2164fb44ea7faa90`. The checks are finite exact
computations in Python 3 (standard library). No human or formal-kernel review
is claimed. Apache-2.0.
