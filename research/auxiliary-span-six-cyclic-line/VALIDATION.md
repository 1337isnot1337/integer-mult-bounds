# Validation record

Environment: macOS, CPython 3.12.2, standard library only. No installed solver,
network service, Lean, Docker, native compiler or historical heavy replay used.

## Executed development checks

- `python3.12 -B scripts/research_package.py --package research/auxiliary-span-six-cyclic-line`
  passed both declared science commands and source/metadata checks in under two
  seconds. An initial metadata check rejected the unrecognized outcome label
  `obstruction`; it was corrected to `negative-result` before this pass.
- Direct optimized science command also passed. Acceptance uses explicit
  exceptions, not Python assertions.
- `git diff --check` passed before publication preparation.

Science result: 120 projectors from two implementations; 12 cyclic projectors
in three groups of four; 300 pairwise symbolic projection checks; 12 ordered
eight-factor checks; final common-J two-run Laurent identities; nine-call
positive endpoint; five meaningful failure controls.

The program does not enumerate rational frame assignments, verify every
augmentation-quotient step of PR468 §5.1, or supply a physical implementation.
The proof explicitly depends on that written common-J lemma. Independent
human/proof-kernel acceptance, hosted CI and full selected cold replay are
not claimed.

Publication-source/export checks and independent review will be recorded in
the final handoff against their exact committed heads. The science program is
self-contained; its two predecessor README inputs are retained for source-bound
mathematical provenance and included by the official exporter.
