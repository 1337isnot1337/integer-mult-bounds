# Independent audit of PR3605's staged 644/660 words

**All four audited claims of PR3605 hold at head `3efbb5de` for both providers.**
A new standard-library interpreter, which does not import the inherited auditor,
confirms the following. The changed `base` and `extra` words are exact
arbitrary-dirty identities in both orientations, with 632 independent inputs and
91 private buffers. Their cleanup is the literal inverse cleanup. Their chronological
binary frames give the local profile
`{1:2433,2:724,3:228,4:102,5:20,8:8} -> {1:2439,2:726,3:224,4:102,5:20,8:8}`
and the helper widths `8:99 -> 97`, `7:50 -> 52`. The published complex-root
brackets of PR3605 and PR3148 also hold. An exact rational interval engine
checks them, and a 70-digit decimal engine cross-checks the result.

This is a finite exact **audit** of one local supplier change. It makes no κ
claim and no frontier change. It does not check native Gaussian phases, the
owner journal, complete admission or the inherited all-size hypotheses (see
Scope). The selected record stays `0.001672660197076918`.

## What was audited

Audited object: RossRichardson's
[PR3605](https://github.com/CrocSwap/integer-mult-bounds/pull/3605), head
`3efbb5de06a49ffeea6684482f2d3fe48cdca3fb`, package
`research/staged-644-660-width-reduction`. In its two words, eight early raw
helper-to-target writes (old `B184..187` for helper 644, `B216..219` for 660)
are replaced by four donor releases at `span(429,30)`: `640 += 2*644` and
`496 -= 2*644` before old B599, and `656 -= 660` and `520 -= 2*660` before
old B647. Helpers 644 and 660 then enter at `span(429,30)` instead of `span(30)`
and keep FULL terminals. The single-change control is dcharb78's unchanged
[PR3133](https://github.com/CrocSwap/integer-mult-bounds/pull/3133) parent words
(`51eb9c4e`, byte-identical on main). The root control is Jeremy Diviney's merged
[PR3148](https://github.com/CrocSwap/integer-mult-bounds/pull/3148) (`f2927a4b`).

The open staged-width κ>0.00173 chain (#3624, #3626, #3633, #3638 and the #3630
successor) reuses these words unchanged. On 2026-10-18 the GitHub API showed
byte-identical copies at these heads: #3624 `515a7c44`, #3626 `659fd5e7` and
#3633 `72c268f1` add word blobs `dc6d321b`/`78e7b2bb` and record blobs
`042dbc69`/`67f04ae3`. The same blobs sit inside #3638 `d62e1acd`'s vendored
`PR3624-SOURCE.tar.gz` and #3630 `bcac7fe0`'s `PR3605-SOURCES.tar.gz`.
PR3605's own semantic check runs the pinned inherited interpreter
(`audit_local.py`). This package supplies a separately implemented check of
those exact words. It does not check those PRs' own owner journals or roots
and does not admit any of them.

| Quantity (each provider) | PR3133 parent (control) | PR3605 changed word |
|---|---|---|
| Local profile | `1:2433, 2:724, 3:228, 4:102, 5:20, 8:8` | `1:2439, 2:726, 3:224, 4:102, 5:20, 8:8` |
| Helper widths | `4:26, 5:2, 6:18, 7:50, 8:99, 9:213` | `4:26, 5:2, 6:18, 7:52, 8:97, 9:213` |
| Inputs / private buffers | 632 / 91 | 632 / 91 |
| Forward (dirty buffers), dual, reverse pull-back | PASS | PASS |
| Cleanup equals the literal inverse | yes | yes |

The profile delta is `+6 H1 + 2 H2 - 4 H3` (local rank mass −2 per call). It is
confined to exactly six registers, and each change equals PROOF.md's written
invoice: pivots 644/660 `+H2 - H3`, first donors 640/656 `+H1 + H2 - H3`,
second donors 496/520 `+2 H1 - H2`. Applying either helper's edit alone keeps
the identity and moves the profile by `+3 H1 + H2 - 2 H3`. The two helpers'
shares are therefore separable and additive.

## Method and independence

The registered verifiers (`audit_core.py`, `verify.py`, `root.py`) import only
the standard library. The word format and contract were read from PR3133/PR3605
and the inherited `audit_local.py`. No code was imported or copied from them or
from the earlier `coupled-carrier-independent-audit` (Arham Tahir). The optional
cross-check below is the only exception: it imports the inherited auditor on
purpose.

- **Identity, algorithm 1 (forward values).** Each register's value is
  propagated as exact rational combinations of `(input, reduced free-group word)`.
  Warps are independent invertible free symbols. All 632 live inputs **and the
  91 private buffers** are independent symbols, so the buffers are dirty. The
  check requires `y_t -> y_t + x_t` with every other live input restored, and no
  buffer contribution in any live register. With dirty buffers, every buffer is
  returned unchanged in both orientations. At the cleanup boundary, targets
  are sheared and the 91 restored helpers equal their own inputs and are read
  nowhere else.
- **Dual.** The contragredient circuit is run separately with independent `K^-T`
  symbols and must give `x_s -> x_s - y_s` with clean buffers.
- **Identity, algorithm 2 (reverse pull-back).** The program is processed
  backwards on covectors, with words growing on the right. The resulting
  723 × 723 symbolic matrix at return must equal algorithm 1 entry for entry.
  A separate pull-back of the pre-cleanup program must satisfy the same
  boundary contract.
- **Frames.** Subspaces of `F_2^9` are stored as 512-point masks. Each gate's
  frame must contain the current frame of every register it touches. The checks
  also cover warp frame maps and the lifted Lagrangian action of all 72 warps,
  centre descents, target levels and end frames. The profile and widths are derived from these frame
  chains; report fields are compared only afterwards. The inherited structural
  rules are also checked: dyadic scalars, power-of-two scales, and wrapper and
  correction access.
- **Reconstruction.** Each changed word is rebuilt from the parent using only
  PROOF.md's prose. Every field except cleanup must equal the shipped word, and
  cleanup must equal the independently derived literal inverse. Canonical and
  compressed digests must match PR3605's records, and the declared edit record
  must equal the prose.
- **Second method (written argument).** Two parts of PROOF.md are checked
  symbolically. First, `P_new = P_old S1 S2` holds on **every register** at
  the boundary after the old-B647 releases. The S matrices change exactly
  the four donors and the eight tabled targets. Second, the two four-row target
  tables hold exactly at old B599 and B647, every other target has zero
  columns, and each table kills its `v`. A per-register frame invoice is also
  computed and compared with PROOF.md's written per-pivot histograms.
- **Contract fidelity (optional; not in the registered replay).**
  `crosscheck_inherited.py SEED TRIALS` compares this package's forward and dual
  verdicts with the pinned inherited interpreter on random mutants of the
  `base` word. The mutants flip, drop or swap B gates, change coefficients,
  flip or drop cleanup gates, drop or flip corrections, and shift warps. Seeds
  `3605 40` and `44 60` gave 200 of 200 agreeing verdicts. This script imports
  the inherited auditor, so it checks that the contract was read correctly. It
  is not independent evidence.

## Required-failing mutants (19 per provider, all as predicted)

| Mutant | Outcome |
|---|---|
| Omit one of the four releases (cleanup regenerated) | identity fails at targets: 644→640 `135,162`; 644→496 `135,220`; 660→656 `141,196`; 660→520 `141,171` |
| Flip one release sign, or both signs of one helper | identity fails at targets |
| Add releases but keep the raw target writes | frame containment fails at B184; identity fails at `162,171,196,220` |
| Entrance `span(429,30)` alone on the parent | frame containment fails at B184 (helper 644) |
| Releases at frame `[30]` | frame containment fails at the first release |
| Parent cleanup on the changed word / one cleanup gate removed | identity fails (donors 496,520,640,656 left dirty / helpers dirty) |
| Keep the old `[30]` entrance | identity holds; profile `+2 H1`, widths back to `8:99, 7:50` |
| Drop the restore-210 frame edit | identity and bill unchanged (that edit is bill-neutral) |
| 644-only or 660-only edit | identity holds; profile `{1:2436,2:725,3:226,…}`, widths `7:51, 8:98` |

The old-entrance mutant shows that, within these words, the entire rank-mass
saving of 2 comes from the entrance frame. With the old entrance, the staged
releases leave local rank mass unchanged. The physical legitimacy of the
`span(429,30)` entrance therefore rests on the native wrapper identity
`L^-1 T_F T_P^-1 R^-1 = C_[7] ⊗ I_[2]` (PR3605 `check_residual.py`). That
identity is shared by every downstream PR and is not independently checked here
(open question 2).

## Root brackets and attribution

`root.py` uses `M(b) = Σ_r r·H[r]·(73/r)^b / (73·663040)` (PR3605 DERIVATION.md)
on the published complete histograms. Its primary engine is outward-rounded
exact rational interval arithmetic: atanh/Taylor series with explicit
remainders on a `2^-320` grid. The second engine is 70-digit decimal Newton
iteration. During preparation, python-flint 0.9.0 arb at 400 bits reproduced
both `M(C)-1` and `M(D)-1` to all printed digits. That third check is not
part of the shipped replay.

| Histogram | Published bracket | Confirmed 30-digit bracket |
|---|---|---|
| PR3605 | `[0.001730006549538841847005, …006]` | `[0.001730006549538841847005854305, …306]` |
| PR3148 | `[0.0017297774946785970118869, …870]` | `[0.001729777494678597011886903656, …657]` |

The root delta is `+2.29054860244835118950648e-7` to `…650e-7`. Both
histograms have the same rank mass, `48,165,120 = 65088·740`. The
decomposition is `H = 6660·L + I`, with the local change `+6H1+2H2−4H3` per
call and the idle change `{1:+996, 3:−617, 4:+1, 5:−3083, 6:+3, 48:+616}`.
Swapping one component at a time does not conserve mass and moves the root by
about ±9.7e-5. Those hybrids (0.0018266 and 0.0016331) are arithmetic
counterfactuals, not realized journals. **The net gain is a 0.2% residual of
two opposite mass shifts.** A single rank-48 idle child moves the PR3605 root by
`∓3.498e-7`, more than the whole gain over PR3148. A rank-1 child moves it by
`∓7.34e-9`. So the claimed gain over PR3148 also depends on every idle count
being exact.

`root.py` also recounts PR3605's published aggregate integer witness
(`owners/AGGREGATE-INTEGER-FLOW.json.gz`, vendored). Over its 1,491,840 bins,
`idle = capacity − pattern width` reproduces `I` exactly. Its role flow meets
the per-call demand `20 × {4:26, 5:2, 6:18, 7:52, 8:97, 9:213}` (the audited
widths) for all 333 macro-calls. The capacity balance
`35,804,160 = mass(I) + 6660·3279` holds. Three controls are rejected: the
parent widths, a deleted pattern record and a deleted role-flow record. The
witness's source windows are taken as published. The literal 2,717,280-row
journal and its chronology are not re-derived here; they remain the
load-bearing unaudited input to the root.

## Scope, inherited assumptions and unrun obligations

Checked here: the finite free-operator identity for arbitrary independent inputs
in which warps are free invertible symbols, the binary-frame chronology and bill,
the cleanup, the PROOF.md factorization, tables and invoice, and arithmetic
on two published histograms. The free-operator proof uses inverse cancellation
only, so it applies to the actual invertible warps.

Not checked:

- native Gaussian/Clifford phases and the rank-7 residual `C_[7]⊗I_[2]` on 512 columns;
- the owner source windows and the literal T740 owner journal (the idle profile is recounted only from the aggregate witness);
- the PR3605 conditional release and full fresh-bootstrap wrapper replay requested in Ross's #1166 handoff;
- physical/prefix/outer release, precision, H1–H5 and the formal kernel.

The binary-frame contract is taken from the inherited format. It is not
derived from first principles. Gzip streams are not compared; payloads and
pinned byte digests are.

## Reproduce

From the repository root, with Python 3.12 or later and the standard library only:

```sh
python3 -I -B research/staged-644-660-independent-audit/verify.py
python3 -I -B research/staged-644-660-independent-audit/root.py
```

Expected output is `PASS_INDEPENDENT_STAGED_644_660_WORD_AUDIT` (after two
`CHECKED` lines, about 35 s) and `PASS_EXACT_MOMENT_BRACKETS` (about 31 s). Both
compare against the committed receipts `RESULT.json` and `ROOT-RESULT.json`; `--write`
regenerates a receipt deliberately. Failures raise explicit exceptions, also
under `-O`. Both commands passed directly on CPython 3.14.4 under `-I -B` and
`-I -O -B`, and `research_package.py --check-only` passed. The generic runner
(`python3.12 scripts/research_package.py --package
research/staged-644-660-independent-audit`) needs Python 3.12. That version
was not available here, so the runner has not been executed.

## Sources

Base main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority revision 6.
PR3605 is unmerged, so its two words, two edit records, its conditional-release
`CLAIM.json` and its aggregate owner witness are byte-preserved in `inputs/`.
[SOURCES.json](SOURCES.json) records their source path, commit, Git blob and SHA256, which `verify.py`
checks. The PR3133 parent words and PR3148 `CLAIM.json` are read from main;
their blobs equal those at the predecessor heads. The PR3605 files that were
read but not executed (PROOF.md, staged_pair.py, check_scope.py, verify.py,
DERIVATION.md) are pinned the same way.

## Open next questions

The structured list is in [TASK.json](TASK.json).

1. **Are PR3605's owner windows and literal journal legal?** The root gain
   over PR3148 is smaller than one rank-48 idle child. The arithmetic from the
   aggregate witness to
   `I={1:174156,3:48334,4:1,5:10792,6:3,48:283185}` is reproduced here, so the
   decisive remaining check is the witness's 333 source windows and the
   2,717,280-row chronological expansion. First step: derive the window classes
   from the T37 source template without the retained `owner.windows` routine,
   and compare them with the witness's `groups`.
2. **Do the native phases of the paired `span(429,30)` entrance hold?** This
   needs an independent check of the rank-7 residual on all 512 Gaussian
   columns, without the `bw_*` lineage code.
3. **Is the restore-210 frame edit needed?** It is bill- and identity-neutral
   here. Does any native stage require it?

## Credit and provenance

The construction is RossRichardson's PR3605. The parent words and coupled folds
are dcharb78's PR3133, and the T740 owner/cap root control is Jeremy Diviney's
PR3148. The word lineage retains its credited predecessors (PR2857, PR2908/2917,
Marius-Paul Dumitrean's PR2979, Jeremy Kothe's PR3015, PR3042) as recorded in
those packages. Arham Tahir's `coupled-carrier-independent-audit` gave
orientation on the contract; no code was taken from it. The PR3531 arithmetic
lineage is credited for the root model in PR3605.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). No human or formal-kernel review is claimed.
Apache-2.0.
