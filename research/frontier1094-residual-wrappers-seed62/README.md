# The selected frontier1094 word's 36 residual wrappers are exact

**Supplier-boundary audit: an independent, byte-bound check. No new κ, and no existing check is changed.**

- Track: 60–74 (adversarial audit), assignment seed 62, drawn with the OS CSPRNG via Python `secrets`.
- Card: `supplier-boundary-audit`, with the scope **refined** in [TASK.json](TASK.json).
- Base: `179089e4`. The selected record frontier1094 is unchanged.

## The obligation and where its acceptance came from

Lemma A's exact part (`research/e8-lemma-a-lean`, `research/e8-lemma-g-lean/PROOF.md` §4) concerns every helper that enters at a nonzero frame E or ends below FULL at a hyperplane U. Each such helper needs a stored wrapper (L, R) with

`L ∘ (C_[w] ⊗ I) ∘ R = T_end ∘ T_E⁻¹`,  w = dim end − dim E,

where end is FULL, or U for a hyperplane end. For the selected gauge44 provider these are the 36 records in `RESIDUAL-ADAPTERS.json`, raw sha256 `383f40aa`.

The selected chain binds that file through the owner audit's `source_artifacts`, but it does not check that the records are exact:
- **The chain's own audit checks structure only.** `gauge44-slots-t16/code/audit_allcold.py` (lines 56–61) checks only each wrapper's `frame`, `terminal`, `vectors`, `terminal_vectors` and ranks.
- **Exactness rests on a receipt the chain does not pin.** The only statement of exactness is the producer's own `WRAPPER-CHECKS.json` (`PASS_RESIDUAL_WRAPPERS_ARE_EXACT`, sha256 `0ae753d6`). The producer wrote it with its own Clifford code, and the owner audit does **not** pin it.
- **Later re-runs are not independent.** Re-runs such as #1646 and `selected-replay-fastpath` execute that same producer code.
- **#1781 (ours) left these records out** of its independent check. It covered the 2,896 child records and 224 endpoint adapters.

## What this package checks

### Binding
- It reuses the merged #1781 binding, which our package imports with its digests pinned. The chain runs: selected record → frontier1094 certificate → capsule → owner audit → gauge44 word and programs.
- `RESIDUAL-ADAPTERS.json` must match the owner audit's own digest.
- The `split-centres` decoy, which has the same basename, differs by digest.
- The global8 twin is byte-identical. This is informational only.

### Inventory
- **The keys.** The 36 keys are exactly the word's entering helpers ending at FULL (key = start) together with its hyperplane-ending helpers (key = start:final). That gives:
  - 22 FULL-ended records;
  - 12 cold hyperplane-end records (`0:U`);
  - 2 entering hyperplane-end records (`2:999` and `3:998`).
- **The records.** Every record's frames, vectors and ranks match the word, and all 72 monomials are well formed.
- **The program events.** In both programs, each of the 240 wrapped helpers has exactly one `pre` and one `post` residual event, with the right key. Its first event is the `pre` and its last is the `post`. Our open #1964, from another session, checks this placement as part of Lemma G's H1. Each orientation has 480 events, with widths {4: 112, 5: 64, 7: 60, 8: 244}.

### Two kernels
- **Kernel B** ([closed_form.py](closed_form.py), new, standard library only) computes amplitudes directly from closed forms:
  - the frame operator from its closed formula;
  - the monomial records from their closed forms;
  - F_w from the √X product.

  It works on sparse exact columns and evaluates no gate list.
- **Kernel A** is #1781's packed Gaussian-integer evaluator (`clifford.py`).

Both must find every identity exact on all 512 columns, with the global phase included.

### Calibration of kernel B
Before any record is judged, kernel B must reproduce:
- #702's 14 frame-kernel digests;
- #1415's three operator digests of T_U ∘ T_E⁻¹, which exercise the adjoint.

Separately, records `3:998` and `2:999` are field-for-field Exact.lean's pair 2 and pair 3. Their identities are Lean-proved.

## Results ([RESULT.json](RESULT.json))

| | Records | Exact (kernel B) | Exact (kernel A) | K (C gates per identity) |
|---|---|---|---|---|
| FULL-ended | 22 | 22 | 22 | 9 |
| Cold hyperplane-end `0:U` | 12 | 12 | 12 | 4 (8 records), 8 (4 records) |
| Entering hyperplane-end | 2 | 2 | 2 | 8 |

All 36 wrappers are exact.

### Controls
Each mutation below is rejected on every record it applies to:
- global phase +1;
- input character (`linear_Z4 += 2`);
- a CZ term in Q;
- an offset translation;
- swapped wrappers;
- width ±1;
- a transposed matrix (36/36 each);
- hyperplane-end records evaluated against FULL (14/14);
- a FULL-ended wrapper reused for a hyperplane end (2/2);
- another basis of the same span (2/2, while the same rows reordered pass);
- kernel B's own phase and width mutants (8/8).

The tests also reject the decoy, a flipped archive byte, a dropped `pre` event, an event read with the wrong key, and a wrong record vector. [test_package.py](test_package.py) has 15 tests.

## Overlap

- **Lean pairs.** `2:999` and `3:998` were already Lean-proved as Exact.lean pairs 3 and 2 (#593). Their semantic binding is #1415's.
- **Cold rank-4 records.** The eight cold rank-4 records `0:124`…`0:327` are byte-identical to records in earlier provider files, for example `research/community-k492-audit`. #702 checked the cold wrappers of that family by amplitudes, for PR626.
- **What is new.** The other 26 records (the 22 FULL-ended ones and `0:1000`…`0:1003`) had only producer evidence. All 36 are now checked for the **selected** word, from its bound bytes, by two kernels.

## What this does not show

- **The executor bridge.** It does not show that the emitted program applies these records with exactly these semantics (Lemma G's H1 and the label bridge; see #1964).
- **Other recipes.** The child and endpoint records are #1781's, and the identity adapters are not checked.
- **Lean.** There is no Lean proof for the 34 records outside the Exact.lean pairs.
- **κ.** There is no new κ.

## Reproduce

```sh
python3 -I -B research/frontier1094-residual-wrappers-seed62/verify.py        # about 40 s; PASS_FRONTIER1094_RESIDUAL_WRAPPERS_EXACT
python3 -I -B -m unittest discover -s research/frontier1094-residual-wrappers-seed62 -p test_package.py
python3 scripts/research_package.py --package research/frontier1094-residual-wrappers-seed62 --check-only
python3.12 scripts/research_package.py --package research/frontier1094-residual-wrappers-seed62
```

Requires standard-library Python 3.10 or later. It was run on Python 3.12.15 and 3.14.8 (macOS 26.5, arm64).

## Open next questions

1. **Does the emitted executor apply the child, endpoint and residual records with exactly these semantics?**
   - Why it matters: record-level exactness, here and in #1781, still needs the bridge rec(A, B) = record circuit.
   - First step: replay one helper's full event sequence (`pre` wrapper, climbs, `post` wrapper) through an independent statevector executor and compare the result with C_[w] ⊗ I.
   - Blocked by: an independent executor for the emitted program format.
2. **Should `WRAPPER-CHECKS.json`, or this package's receipt, be bound by the owner audit?**
   - Why it matters: the chain pins the records but not the producer's exactness receipt.
   - First step: propose the binding at the next maintainer integration of frontier1094.
   - Blocked by: a maintainer decision.
3. **Can Lean's `Clifford.check` kernel-check the 36 packed identities for this instance?**
   - Why it matters: two of them are already Lean-proved, so the rest would turn this replay into a formal result.
   - First step: emit the 22 FULL-ended identities as Lean `check` terms and time `lake build`.
   - Blocked by: a Lean toolchain, which is not installed here.

## Credit

- **Lemma A and Lemma G Lean packages, and the HPE wrapper tool:** DreamingOfClouds (#484/#509), following PR #458 (chafreaky).
- **`HyperplaneEnd/Exact.lean`:** jeremykothe2 (#593).
- **Calibration sources:** #1415 (commdata2338) and #702 (BigCactusLabs).
- **The producer:** `phases_full.py`/`clifford_exact.py` (icekylinx, from PR425).
- **The packed kernel and binding:** our #1781.
- **Related checks:** #1697 (navinor; the cold hyperplane operators), #1611 (bbMisk; binding helper 450's wrapper pair), and #1964 (ours, open; Lemma G H1 extended labels).

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from Claude (Anthropic) via Claude Code.
- Parallel read-only scout and judge subagents selected the obligation and traced the producer-only evidence.
- The closed-form kernel, the verifier and the controls were then written fresh.

No claim was posted to Discussions. New material is Apache-2.0.
