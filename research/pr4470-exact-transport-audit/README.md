# Exact physical transport audit of PR4470

This is an in-progress, source-bound audit of all 423 declared transport/helper-boundary pairs in PR4470 at b9a13c1673e0e9697de410de16e8bbf3207a7363. It claims no new kappa. The selected result and frozen predecessor files are unchanged.

The separately written checker reconstructs the reference frame catalogue and compares every entry of each 512 by 512 lowered matrix against the literal Gaussian-dyadic reference operator, in both orientations. It uses int64 Gaussian numerators and explicit powers-of-two denominators, not floating-point tolerances, predecessor interpreters, Clifford tableaux, or a zero-column-only phase comparison. A 28-Gaussian-gate cap keeps all arithmetic and squared magnitudes within int64.

## Verification state

Local Python 3.13.5 / NumPy 2.3.5 self-tests pass with 196 positive checks, seven rejection controls, and a two-column tensor-phase test. The complete source-bound replay has not yet completed at the initial draft commit. Its status must be read from the focused CI job and subsequent handoff, not inferred from the presence of this code.

Install numpy==2.2.6 on Python 3.12, then run:

```sh
python -B research/pr4470-exact-transport-audit/verify.py --self-test
python -B research/pr4470-exact-transport-audit/verify.py --out /tmp/pr4470-exact-transport-result.json
```

The output path must not already exist. Git-free replay is supported by the four committed, authenticated source exports. The focused workflow runs this audit alone with a 600-second scientific timeout; it does not replace or waive shared repository CI. Registration and the final source manifest will be completed after the first full-source replay.

## Scope boundaries

Even a passing full replay only verifies the listed physical normal forms and their declared ranks/phases. It does not independently prove that the 423-pair list is exhaustive for the chronological word, replay the 632 persistent-field endpoint, admit the p16 controller, price physical movement, or establish precision, storage, and the outer multiplication theorem. Tensoring a checked operator identity preserves that identity for each positive column multiplicity; it does not by itself price the lifted implementation.

## Task and overlap

Base is canonical main 2a13eb1827784206202db90e5dc8327cf8a250db, priority revision 7. The assigned PR4470 native audit refines independent-moment to actual physical operators rather than invoice arithmetic. PR4478's current README covers the compiler and outer rows. PR4457 audits predecessor operators, not PR4470's changed 423-pair set. PR4464/4466 cover stage-zero commutation. Live PR4470 mentions and the public handoff thread were checked; this is bounded coverage, not a claim of exhaustive novelty. The newer compiler work in PR4483 does not discharge this physical audit.

## Open next questions

The smallest useful follow-up is to reconstruct the changed chronological word and prove that every transport and helper endpoint is represented in the audited pair set, then replay all 632 arbitrary persistent inputs and the owned centre. Pin the same head and start from native_joint.py's source-to-patch mapping, without importing its evaluator. A separate follow-up audits the p16 controller. Neither is closed by the matrix checks here.

## Credit

Prepared for Chris / Clear1nsight with substantial OpenAI assistance. This is a separately implemented AI-assisted check, not independent human or proof-kernel verification. Apache-2.0. The source construction and mathematical reference conventions belong to the contributors in vendor/NOTICE.md. In particular, credit Cinna Davis for PR4470, zxv for the native/compiler lineage, Jacob Alan Sussman for mixed-target recursion, Mark / Matarener for PR4457, and Ryanson Jonathan for PR4478.
