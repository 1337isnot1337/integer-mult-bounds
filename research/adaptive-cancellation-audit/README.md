# Independent sharp-cancellation audit

Assignment D audits one quantified implication of zxv's adaptive compiler, not its already-covered finite parameter arithmetic. PROOF.md proves the exact contraction implication for all real admissible potentials and characterises its sharp universal threshold using explicit extremisers. It agrees with PR4483 Section 4. It supplies no new kappa or lower uniform rank and does not claim a compiler bug.

The exact dual-slack identity is

    (1-beta)(eta I-B-F)
      = (eta-beta)A-(1-eta)F+(1-eta)(beta I-B),

under I=B+F+A. At fixed A,F the worst possible exit fraction is (beta A+F)/(A+F). Necessity is for a guarantee over all allowed boundary masses, not for every individual flow. Zero mass is handled separately without division. Two explicit rejected controls show why omitting roots or leaves invalidates weaker arguments.

## Reproduce

Python 3.12, standard library only:

```sh
python -B scripts/research_package.py --package research/adaptive-cancellation-audit
python -I -O -B research/adaptive-cancellation-audit/verify.py --self-test
```

Local normal and optimised runs pass 6,120 rational cases, 1,800 extremiser checks, 120 zero-mass checks and the listed controls. The hosted registered run additionally authenticates the exact source proof. No predecessor acceptance function, approximate logarithm or solver is imported. The universal conclusion comes from the written algebra, not extrapolation of this finite grid.

## Sources, scope and overlap

Canonical scientific base f9f85c1e4fa1e955ff39f10fca447e3e2a4e4adc; source research/rank-convergence/PROOF.md, Git blob 75f451837204bd141f357e7f5e5d6c6f42e1423e. VERIFY.json declares that live input and verify.py rejects a changed blob before reporting source-bound success. SOURCES.json retains the original card and selected record as historical provenance. Priority revision 7. The user-assigned proof-audit scope is recorded as changed from independent-moment. The historical baseline helper was not executed.

PR4529 independently checks numerical gates but excludes the theorem. PR4532 proves broader gate-existence statements, and PR4533 retunes witnesses without a new kappa. This audit intentionally isolates the scalar cancellation inference rather than repeating those results. Targeted live PR searches and bounded Discussion reading are not exhaustive overlap coverage or proof of novelty.

## Open next questions

Can actual flow correlations improve the mirror/leaf bound beyond the information used in the sharp scalar inference? Start with a source-bound joint boundary/leaf occupation statement, not a lower threshold contradicted by the extremisers. Separately audit one Chernoff occupation or root bound before treating the full adaptive compiler as independently verified. No particular claim that these are unclaimed is made without a fresh overlap check.

## Credit

Credit zxv for PR4483's argument, Jacob Alan Sussman for mixed-target recursion, Ryanson Jonathan for mirror/gate work, Dillon for the broader gate-existence follow-up, and the retained Cinna Davis/native/outer lineage. Prepared for Chris R / Clear1nsight with substantial OpenAI assistance, Apache-2.0. This is one separately implemented workstream, not independent human or proof-kernel acceptance.
