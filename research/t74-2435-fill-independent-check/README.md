# Independent check of PR2435's T74 words, owner map and complex endpoint

**Independent verification; no κ claim.** [PR2435](https://github.com/CrocSwap/integer-mult-bounds/pull/2435)
(Jeremy Kothe, head `324d7d35`) claims conditional κ = 0.0016985113436976293… It raises the entrance frames of
24 copy-buffer helpers per word from dimension 1 to 2 (width 8 → 7) on PR2322's handoff construction, and adds
an exact owner fill. This package re-checks the words, the owner map and the complex endpoint with code
written independently of PR2435. The checkers are this author's own earlier tools, used unchanged as
libraries: PR2387's `fill_check80.py` and PR2315's `words_check.py`.

**Result: everything checked reproduces.**

| object | check | result |
|---|---|---|
| both BORROW-WORDs | frame-climb recount (two implementations) | profile {1:2359, 2:632, 3:330, 4:120, 5:38, 8:8}, inventory {4:33, 5:9, 7:62, 8:90, 9:240}, 434 helpers, 78 zero buffers, equal to the reports |
| both BORROW-WORDs | 46 warps (G invertible, G·span U = span E, K_G symplectic, Fourier rank 0); nested frames; **exact replay over ℚ⟨F⟩, forward and dual, all 658 inputs arbitrary (dirty)** | Y += X; everything else and the 78 zero buffers restored; a flipped coefficient is rejected |
| OWNERS.json.gz (289,044 roles) | R-a..R-e, with 1,332 windows rebuilt from 2,220 GLOBAL-TEMPLATE events and equal to PR2435's PLAN windows | PASS; 276,407 cross-replica roles; 123,882 of 149,184 bins occupied |
| recount vs PR2435 SPEC, PROFILE and PR body | idle, global profile, roles, rank mass | idle `{1:20824, 3:6695, 5:1, 48:25302}`, profile `{1:1591918, 2:420912, 3:226475, 4:79920, 5:25309, 8:5328, 48:25302}`, mass 4,816,512 (deficit 23,680), all equal |
| R-f namespace | PR2322 rule vs PR2435's charged stock | 66,748 = 66304 + 434 + 8 + 2 with the buffers in the reserved tableau; PR2435 charges them separately: 66,748 + 78 = **66,826**, equal to its SPEC |
| R-g | X2 pending-axis disjointness; distinct 73-column charts | 2,016 checks pass; **9,129** charts, equal to SPEC `actual_73column_sigmas` |
| complex endpoint | root of the recounted global profile, 800-bit enclosures | certified within ±1e-15 of the claimed κ |
| negative controls | fill_check80's 16 mutations, adapted to these words, plus a flipped word coefficient | all rejected, each by the intended rule |

A companion audit, [PR2442](https://github.com/CrocSwap/integer-mult-bounds/pull/2442), shows that this fill is
not the pattern-integer optimum for these words. The optimum, with idle `{1:20822, 3:6694, 5:2, 48:25302}`,
would add up to +5.8e-10 if a legal owner map realizes it. That does not affect the correctness verified here.

## Scope (what is not checked)

- **Raised entrances.** Their scalar correctness is checked: the exact replay of the whole word passes with
  arbitrary dirty inputs. Their frame legality is checked as nested frame climbs. Not checked: whether the
  parent hosting actually delivers each raised copy buffer at its two-dimensional entrance frame. That is a
  native and recursive-hosting obligation, which PR2435 audits with its own native tooling and tamper
  controls.
- Native lowering, phases and wrappers, the invoice, precision tapes, outer ledger, bit supplier and
  admission are not re-run.
- The root check confirms the complex endpoint of the recounted profile. κ = C − 1/F − B is PR2435's outer
  formula and is not re-derived.

## Reproduce

From the repository root, standard library only:

```sh
python3 -I -B research/t74-2435-fill-independent-check/check_2435.py --fetch    # ~20 s
```

`--fetch` fetches `refs/pull/2435/head` if commit 324d7d35 is absent. All 13 PR2435 inputs are blob- and
sha256-pinned. The template's DATA-PHASES file is read pinned at PR2269 b479fc55 (fetch
`refs/pull/2269/head` if absent).

Expected final line:
`PASS_T74_2435_FILL_INDEPENDENT roles=289044 idle={"1":20824,"3":6695,"48":25302,"5":1} physical=66826 charts=9129 controls=16 root=kappa_2435+-1e-15`

All results were run on CPython 3.14.4; the registered Python 3.12 replay was not run locally.

## Open next questions

- **The pattern optimum.** Does a legal owner map attain PR2442's optimum for these words, adding up to
  +5.8e-10? First step: starting from OWNERS.json.gz, re-pattern the bins listed in PR2442's receipt and run
  this checker.
- **Entrance delivery.** What exactly justifies the two-dimensional entrance of a copy buffer in the parent
  hosting? First step: locate the parent recipe event that delivers copy-buffer content and check its frame
  rank.

## Credits and licence

- PR2435 / PR2374 / PR2349 (Jeremy Kothe) and PR2363 (mason-hale): the audited construction and fill line.
- PR2322 (Vlado Vojdanovski): the handoff construction.
- PR2269 (Jeremy Kothe): template and borrow words.
- PR2226 (Cinna Davis): anticipatory borrowing.
- PR2309 (Dugongue) / PR2315 (this author): buffer stock accounting.
- PR2387 / PR2315 (this author): the vendored checkers, pinned.

Prepared with substantial AI assistance (Claude Code, Anthropic, Claude Opus 5.5). An adversarial AI reviewer
was used; no independent human review is claimed. Apache-2.0.
