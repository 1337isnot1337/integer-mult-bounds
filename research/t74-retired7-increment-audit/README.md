# Independent audit of #2802's increment over #2751 (T74 retired7), extended to #2818

**Status: independent verification (no κ). No defect found in the increment: all 26 named rules pass and all 15
negative controls are rejected by their named rules. A pass is necessary but not sufficient for #2802/#2818.
The inherited T74/#1319 supplier admission, native lowering and PR1673 outer proof are still required. No selected
frontier is changed.**

## Statement

PR #2802 (Marius-Paul Dumitrean, head `17b2ee6ef3cf1468e78a6267f0ecbc9a0e6f60dd`, `research/t74-joint-twelve-retired7/`)
turns PR #2751's two T74 BORROW-WORDs (Tekalign, head `4cfbb0cc8314d7fb4e8e754545a49a42eb590a69`) into new words through
seven declared stages: `refit5 → alias5 → refit5c → refit7 → hostmove2 → alias7 → refit7c`. These stages contain:
- seven retired-lender aliases: 606←550, 635←551, 637←552, 638←553, 639←562, 667←401 and 669←403;
- two hostee moves: warp 30 from 401 to 564, and warp 31 from 403 to 565;
- the refit frames.

#2802 then drops the seven followers' roles from PR #2751's owner fill. It claims κ = C − 10⁻⁴⁶ − 10⁻⁷⁰ with
C = 0.001717794984118634663827, which is +5.38×10⁻⁷ over #2766/#2767.

Fresh standard-library code checked the following on both words (`base`/`gauge44` and `extra`). PR code was read
only as pinned data and never imported or executed. All arithmetic is exact. The matrix realisation in item 3 is a
randomized second method; the free-algebra replay is the exact one:

1. **S1 event diff.** Every difference between W2751 and W2802 is one of the declared stage edits, and nothing
   else differs. Exactly 63 B gates are relabelled: 35 from `alias5`, 14 from `hostmove2` and 14 from `alias7`. They
   sit at exactly the positions of the 63 declared delete/insert pairs. Exactly 62 frames change: 26 from `refit5`,
   32 from `refit5c`, 2 from `refit7` and 2 from `refit7c`, all present at their declared final value. Warps 30/31
   are replaced in place, warps 66–72 are appended, `removed` gains the seven followers, and `start_extra` loses only
   them. Every other field is unchanged (equal as parsed JSON). This covers `ports`, `centers`, `center_frames`,
   `target_levels`, `precondition`, `compensation`, `initial_corrections`, `prelude_events`, `helper_final` and `cut`.
   A, restore and B keep their lengths and gates up to these relabels. Separately, our own application of the 14
   stage files to W2751 rebuilds W2802 exactly, cleanup included. Every intermediate state passes the frame chain,
   its declared profile and inventory, and both replays. Profiles (helpers, mass) per state:
   - `refit5` 415, 5223;
   - `alias5`, `refit5c`, `refit7` and `hostmove2` 410, 5198;
   - `alias7` and `refit7c` 408, 5188.
2. **S2 occupancy timeline.** Each register's forward event list (corrections, wrapper, A, cut, B, restore) is split
   at that register's warps. On the final word, all 704 resulting segments are exactly one parent role each, with the
   same events and gates up to the declared relabel, in time order. For the new warps:

   | follower ← lender (warp) | lender's last own event | warp before | follower's first event |
   |---|---|---|---|
   | 606 ← 550 (66) | B901 | B947 | B947 |
   | 635 ← 551 (67) | B902 | B1024 | B1024 |
   | 637 ← 552 (68) | B909 | B1027 | B1027 |
   | 638 ← 553 (69) | B910 | B1030 | B1030 |
   | 639 ← 562 (70) | B903 | B1033 | B1033 |
   | 667 ← 401 (71) | **A3175** (27 A + 54 compensation events) | B259 | B259 |
   | 669 ← 403 (72) | **A3174** (26 A + 60 compensation events) | B262 | B262 |
   | hostee of warp 30 → 564 | B911 | B941 (was B941 on 401) | B941 |
   | hostee of warp 31 → 565 | B912 | B944 (was B941 on 403) | B944 |

   No lender has a restore event. No follower has an event before its warp. The old lenders 401/403 keep no hostee
   event. The cleanup is the exact inverse-reverse of the recorded program: it is re-derived and equals the shipped
   4,547 items. Within each register's cleanup the order is therefore mirrored: follower, inverse warp, lender. The
   dual orientation applies g⁻ᵀ item by item in the same order, and each g⁻ᵀ touches the same registers as g. So the
   timeline, and this check, are the same in both orientations.
3. **S2 replay.** An exact replay over ℚ⟨free group⟩ treats all 632 live registers as independent dirty symbols and
   the 72 private zero buffers as zero. It passes forward (Yᵢ ← Yᵢ + Xᵢ) and dual (Xᵢ ← Xᵢ − Yᵢ). The dual treats K⁻ᵀ
   as new free letters. Before cleanup, each restored helper is its own input and is read by no other register. A
   second, independent method realises every K_op as a random invertible 4×4 matrix over GF(2⁶¹−1), with K⁻ᵀ the
   actual inverse transpose. That realisation also passes forward and dual, for 2 seeds.
4. **S3 frames.** The check covers 72 B warps and 24 prelude warp items. For each, G is invertible over GF(2), dim U =
   dim E, G(U) = E and G⁻ᵀ(U^⊥) = E^⊥. The binary-symplectic image of K_G is symplectic and maps L_U onto L_E. Each B
   warp's U equals the lender's **actual propagated frame**, from our own literal frame chain. The new and moved warps
   are 30, 31 and 66–70 (dim 5) and 71–72 (dim 4). Every gate climbs monotonically.

   Refit exactness, measured against the propagated floor (the join of the incident registers' pre-gate frames):

   | stage | frames at the floor |
   |---|---|
   | `refit5` | 26/26 |
   | `refit7` | 2/2: B911/B912, dim 6→5 |
   | `refit7c` | 2/2: B1170/B1171, dim 6→5 |
   | `refit5c` | 25/32 |

   The 7 `refit5c` frames above the floor are B771, B773, B776, B778, B783 and B788 (dim 5, floor 4) and restore60
   (dim 8, floor 6). These lie inside the frame refit #2802 credits to PR2766. `refit5c` claims "certified optimal",
   not "floor". These frames are legal, and the recount below charges them. Optimality was not checked.
5. **S4 profile.** Our recount gives the local profile `{1:2382,2:648,3:268,4:128,5:26,8:8}` (mass 5188) on both words.
   It equals the word reports and both providers' `actual_paid_profile`. A second frame chain, which represents
   subspaces by canonical reduced bases instead of element sets, gives the same profile and inventory. It confirms
   every warp's U and G(U) = E, and it reproduces the parent's profile. The width inventory is
   `{4:26,5:2,7:62,8:78,9:240}` = 408 helpers. The ordered widths dim(end) − dim(entrance) equal the providers' `widths`.
6. **S5 fill with word-derived R.** R = 408 and the per-helper widths are derived **from the words**, not from the
   providers. The fill's 271,728 = 666 × 408 roles cover each call's helper set exactly once. Each role lies strictly
   inside its window; we rebuilt the 1,332 windows from GLOBAL-TEMPLATE and ORDER. No family hosts two helpers in one
   call. Bins are disjoint, within capacity and prefix-compact, and the idle remainders are
   `{1:17316,3:6594,5:9878,32:1,48:26558}`. Independently, FILL equals FILL2751 minus exactly the 4,662 = 666 × 7
   roles of the seven followers, with every bin and in-bin order preserved over 122,625 bins.
7. **S6 price (repeat check).** The complete profile is `{1:1603728,2:431568,3:185082,4:85248,5:27194,8:5328,32:1,48:26558}`.
   Its mass is 4,816,512 = 2·73·33,152 − 2·11,840. With directed-rounding decimal evaluation and an explicit error
   slack, f(C) < 66,304 < f(C + 10⁻²⁴), where f(z) = Σ nᵣ (r/73)^(1−z). Also κ = C − 10⁻⁴⁶ − 10⁻⁷⁰ exactly. The margins are:
   - over #2751: `326698885104162859/500000000000000000000000`;
   - over #2766: `538010651632355557/1000000000000000000000000`;
   - over #2767: 5.380106516323555560552…×10⁻⁷.
8. **#2818 (Jeremy Kothe, head `175822aee7a1858ec653f7f92d7a750aec2c2795`).** Its words
   (`new/borrow/words/BORROW-WORD-43{base,extra}.json.gz`), `new/borrow-fill/FILL.json.gz`, `ORDER.json` and
   `new/BORROW-PROVIDERS.json` are byte-identical to #2802's. Its DISPATCH is the same map. Every field of its
   `retired7_43{base,extra}.json` patch equals #2802's final word. The verdict above therefore covers #2818's
   construction. Its 10⁻³⁰⁰⁰ endpoint certificate is not checked here.

A positive control runs the same code on the #2751 parent. It reproduces that profile `{1:2366,2:646,3:297,4:120,5:26,8:8}`
(415 helpers), both replays, and the parent fill of 276,390 roles with R = 415, whose complete profile equals #2751's claim.

## Separating the new construction from its ancestors

The PR #2802 κ composes three increments over #2751. Each one is priced here with the same code and bracketed with
the same root evaluator:

| increment | check | endpoint C (root in [C, C + 10⁻²⁴]) | gain |
|---|---|---|---|
| PR2766-credited frames: A0–A11, B771/773/776/778/783/788, B1151, restore60 (via PR2733) | Applied alone to W2751, these 20 `refit5c` frames give the per-call change H1 −2, H2 +1. That yields exactly PR2766's claimed complete profile. | 0.001717256973467002308270 | (PR2766's claim) |
| retired5: `refit5`, `alias5` and the other 12 `refit5c` frames (B941–946, B950, B1148–1150, B1168–1169); unpublished | Rebuilt as the `refit5c` state. Its fill is FILL2751 minus the five followers, re-tiled. Local `{1:2386,2:642,3:274,4:128,5:26,8:8}`, idle `{1:17316,3:6594,5:8546,32:1,48:26558}`. | 0.001717409316335491643448 | +1.52342868489335178×10⁻⁷ over PR2766 |
| **retired7 (new in #2802)**: `refit7`, `hostmove2`, `alias7`, `refit7c` | All rules above | 0.001717794984118634663827 | **+385667783143020379/10²⁴ ≈ 3.857×10⁻⁷ over retired5** |

The retired5 fill is our reconstruction by the same compaction rule that #2802 uses for its own fill (S5), because
retired5 is unpublished.

## The two acceptance checks #2802 changed

**R read from the providers.** `independent_owners.check` sets R to the length of the providers' widths, which are
themselves under test. We found that this is **not an open gap**. #2802's `verify.py` `compact()` requires the new
provider widths to equal the parent widths re-indexed by the word-derived live set. The inherited
ENTRANCE-WIDTH-BINDING stage of `new/rebuild_borrow.py` binds the word-derived widths to the providers; its code is
present both in #2802's overlay and in #2818. #2802's recorded release logs show `ENTRANCE-WIDTH-BINDING ... bound
True` for both words (author-recorded; not re-run here). Our S5 makes the binding explicit and independent. Control C8 keeps follower
667 live: providers and fill still say 408, but the words say 409. Control C11 adds helper index 408. Both are
rejected by `S5-FILL-WORD-DERIVED-R`.

**The A-retired-lender control.** For `alias7`, #2802 replaced "warp before lender retirement" with "warp after the
follower's first gate", because 401/403 retire in A. Only 401/403 retire in A. Lenders 550–553/562 retire in B
(B901–B910), so they keep the original control. The replacement control moves the warp *later*. It does not test a
lender event *after* the warp. Our controls show this matters for what the scalar replay can see. In C4a, 401's last
A gate (`add 401 += 41` at A3175) is moved into B right after warp 71. In C4b, it is moved to the end of restore.
**Both the free-algebra replay and the matrix realisation accept both mutants**: that gate's effect reaches only the
zero-response follower and the derived cleanup. Only frame monotonicity after the warp and the occupancy timeline
reject them. C4a fails with `frame not monotone: register 401 at B259`. C4b fails with `final segment of 401 after
warp 71 is not exactly follower 667`. We read the pinned PR2679 auditor's source but did not run it. Its monotone
`climb` applies to every B and restore gate, so #2802's own auditor should reject C4a/C4b for the same frame reason.
For the A-retired lenders 401/403, no shipped control exercises this case. For the B-retired lenders, the retired5
control "warp before lender retirement" does. #2818's retired7 stage controls do not restore it. Those controls are: sign
flipped, coefficient doubled, gate dropped, `warps.pop(0)` (an inherited warp, not a new one) and target frame
changed.

## Reproduce

From the repository root, with Python ≥ 3.10 (standard library only) and `git`, in about 80 s and under 0.6 GB RSS:

```sh
python3 -I -B research/t74-retired7-increment-audit/verify.py --fetch
```

`--fetch` downloads `refs/pull/{2802,2751,2818}/head` only when a pinned commit is absent, and writes only
`FETCH_HEAD`. Every input is checked against its sha256 pin in `increment_audit.py` (`PINS`). Expected last line:

```text
PASS_T74_RETIRED7_INCREMENT_AUDIT rules=26/26 controls=15/15 commit2802=17b2ee6ef3cf commit2818=175822aee7a1
```

`--out RECEIPT.json` rewrites the deterministic receipt shipped here. It records every rule's details and every
control's failing rules. The registered hook (`VERIFY.json`) runs the same command.

## Negative controls (each must be rejected by the named rule)

The cleanup of every word mutant is re-derived from its own forward program, so a stale cleanup is never the reason
for a rejection. Each mutant is re-checked by every rule except the parent positive control and the stage-chain and
attribution rules. Those rebuild or reprice unmutated parents and run once on the pinned inputs.

| control | rule | reason recorded |
|---|---|---|
| C1 `refit7` B911 undone (dim 6) | S3S4-FRAMES-PROFILE | warp frame mismatch: op 30 lender 564 |
| C2 hostee move 401→564 reverted | OCC-TIMELINE | follower 667 outlives the segment (401 would host 667 and hostee 30 at once) |
| C3 warp 66 placed before lender 550's last gate B901 | OCC-TIMELINE | lender 550 has an own event at/after its alias warp |
| C4a 401's last A gate moved into B after warp 71 | S3S4-FRAMES-PROFILE | frame not monotone: register 401 at B259 (replays accept) |
| C4b 401's last A gate moved to the end of restore | OCC-TIMELINE | final segment of 401 after warp 71 is not exactly follower 667 (replays accept) |
| C5 warp 71 after follower 667's first gate | OCC-TIMELINE | follower 667 has an event before alias warp 71 |
| C6 wrong G on warp 71 | S3S4-FRAMES-PROFILE | G(U) != E |
| C7 consistent (U′, G(U′)) on warp 71, U′ ≠ propagated frame | S3S4-FRAMES-PROFILE | warp frame mismatch: op 71 lender 401 |
| C8 removed follower 667 kept live | S5-FILL-WORD-DERIVED-R | role count 271728 != 666 × word-derived 409 |
| C9 lenders of warps 71/72 swapped | OCC-TIMELINE | alias warp 71 is not on lender 401 |
| C10 first restore gate dropped | S2-REPLAY-FREE | restored helper 572 not its own input |
| C11 fill inflated to R + 1 helper indices | S5-FILL-WORD-DERIVED-R | role count 272394 != 666 × 408 |
| C12 one hostee-30 gate left on 401 | S1-DIFF | B941 is not the declared relabel |
| C13 undeclared frame raise (B1500 → FULL) | S1-DIFF | undeclared frame changes |
| C14 #2818 base word altered by one sign | X-2818-SAME-CONSTRUCTION | words differ |

## Scope, inherited assumptions and unresolved obligations

- **Model.** We check the finite BORROW-WORD model as written in PR2226 `PROOF.md` and the PR2679/PR2751 lineage
  (frames, rank-zero K_G warps, COPY charges, derived cleanup and windows). The model itself is not validated. Its
  conventions are taken as the specification: free warps, free cleanup at FULL, idle children priced by remainder, and
  the window rule rebuilt from the template.
- **Not re-derived here.** PR #2751's twelve-source recovery, its 4(H8−H7−H1) delta and the PR2720 reconciliation.
  A sibling session claimed these in #2612. We use W2751 as a pinned parent and check that #2802's copies are
  byte-identical to #2751's own files.
- **Not checked here; inherited and still open.** Native K_op lowering and the exact Clifford phases of the new
  warps. Precision and row reserve, native providers, and physical hosting and routing. The strict outer inequalities
  and the PR1673 capped phase-cell fusion outer. The T74/#1319 supplier admission and the all-size compiler. The physical
  stock identity 66,794 = 66,304 + 408 + 8 + 72 + 2, whose components R = 408 and 72 buffers = |helper_final| agree
  with the words. The "at most two aliases" census and philippeVV's 670/671 pigeonhole in #2802. #2818's 10⁻³⁰⁰⁰
  endpoint.
- **Claim strength.** This is a finite exact check of one construction, not a proof of the multiplication theorem.
  A pass removes no inherited obligation.

## Open next questions

1. **Ship an occupancy control in the stage suites.** *Why:* the scalar replays accept a lender event moved past an
   alias warp (C4a/C4b), so only frame monotonicity protects that semantics. *First step:* add C4a/C4b-style mutants
   (a lender gate moved after the warp) for the A-retired lenders 401/403 to `retired7_controls.py` and #2818's
   `stage_controls`, expecting `frame not monotone`. *Blocked by:* author action.
2. **Is `refit5c`'s "certified optimal" claim true?** *Why:* 7 of its frames sit above the propagated floor. They are
   legal and charged, but optimality is only asserted. *First step:* re-solve those 7 gates' frames with an
   independent exact optimiser under the same moment cost. *Blocked by:* a written objective for "optimal".
3. **Admission of the new warps at the native level.** *Why:* warps 30, 31 and 66–72 are checked only up to their
   binary-symplectic image. *First step:* the exact Clifford/Gaussian lift of each new K_G, in both orientations.
   *Blocked by:* the native lowering inputs, which ship only in the full release.

## Credits and provenance

- **Checked work.**
  - Marius-Paul Dumitrean (PR #2802): the retired5/retired7 stages and the census.
  - Jeremy Kothe (PR #2818, which repackages #2802 with a finer endpoint; concurrent work; also the PR2673/#2745
    lineage and the gmx-t74-borrow43 machinery).
  - Tekalign (PR #2751): the parent words, fill transform and independent checkers.
  - Philippe Van Velzen (PR #2679/#2559): the retired-lender alias and pre-life hostings.
  - Cinna Davis (PR #2226): anticipatory dirty borrowing and the free-operator replay idea.
  - Mason Hale (PR #2696).
  - DavidAriasC (PR #2766): it composes the PR2733 frame refit (mdumitrean) with #2751's words.
  - zxv (PR #2530).
  - The commdata2338 audits.
- **Related work by the same account (disclosed).** The merged `research/t74-borrow43-independent-check` was used as
  a semantic reference for the BORROW-WORD model; no code was copied. Sibling PR #2804 audits #2530's words and the
  #2679 order/windows. The concurrent sibling #2612 claim covers #2751's twelve-source recovery. The pinned PR2679
  auditor and #2802/#2818 scripts were read as data only.
- **Base and assignment.** Base `544a7e82810e30cab61c297cb2e2ea86127fe944` (priority revision 5). Sprint track
  60–74 (adversarial audit), OS seed 71. Claim: Discussion #1163 comment 18961174. Canonical thread: Discussion #2612.
- **AI assistance.** Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5).
  One session wrote and ran the code and these notes. No human has checked the findings by hand. Apache-2.0.
