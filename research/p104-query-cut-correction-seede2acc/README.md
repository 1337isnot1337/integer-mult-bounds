# p104-query-cut-correction-seede2acc

**Finite side-correction construction; no new kappa or admitted supplier claimed.**

## Scope and evidence

This package completes the exact finite P104 channel `Y <- Y + (G/2)X` from
PR1972 with its missing `I-G/2` side correction at the terminal source/target
cut. The original eight query registers are dirty at the earlier query-live
cut, so the shared-query candidate is invalid and is not used. At the terminal
cut all sources are in F9, targets are in their rank-8 hyperplanes, and all
helpers have been restored. For each target, the exact sparse correction has
48 coefficients `-G[t,s]/2 = +/-1/2`; lift the target to F9, add those source
terms, and return it to the same hyperplane. Together with G/2 this yields
`Y_t + X_t` on arbitrary inputs.

The correction adds 4,992 scalar ADDs and 208 rank-one frame transitions. It
adds no helper, query, copy or restoration role. The exact profile becomes
`{1:1282,2:58,3:86,4:104,5:48,6:24,7:8,8:8}`, rank mass 2,576. Under the
selected nine-stage coverage-law relaxation, its optimistic local ceiling is
`a = 0.003246394165033..`; at the selected saving parameter the relaxation is
`0.9976261887..`. This is a favorable profile screen only: it assumes the same
coverage law and optimally packed idle mass, and does not establish a physical
global owner assignment, all-size lift, recursive precision, a supplier or a
new kappa.

At this terminal cut, 208 is also the exact transition-rank floor for this
direct scatter. Every nonzero source term needs the common rank-9 frame; each
of the 104 target registers begins and ends in a rank-8 hyperplane. A nested
path must therefore climb at least one rank and descend at least one rank per
target. The construction attains that floor with one rank-one transition in
each direction.

The exact predecessor pins and dependency hashes are in [SOURCES.json](SOURCES.json).
Scientific inputs stay pinned to the accepted assignment base 7c1e781; the
submission branch was refreshed onto canonical main 0fdd7d82 after checking
that the selected record, catalogue and P104 priority were unchanged.
The final live overlap check found an earlier active claim for this exact
terminal cut and bill at [Discussion #1167](https://github.com/CrocSwap/integer-mult-bounds/discussions/1167#discussioncomment-18931718).
The mathematical construction is therefore handed off from the public branch
linked in that thread instead of being submitted as a duplicate PR.
The independent verifier reconstructs the P104 roots and Gram matrix, checks
all arbitrary input rows and frames through the appended correction, validates
the native rank-one transition recipes including phase, and rejects a malformed
coefficient, missing target descent and mutated native phase.

## Reproduce

From repo root:

```sh
python3 scripts/research_package.py --package research/p104-query-cut-correction-seede2acc --check-only
python3.12 scripts/research_package.py --package research/p104-query-cut-correction-seede2acc
```

Declare all external inputs and pinned dependencies in VERIFY.json. The generic
hook is bounded; native/Lean or long replays need an explicit dedicated workflow.

## Open next questions

The next obligation is the global chronology/owner assignment, precision and
all-size lift inherited from PR1972. The first step is a complete corrected-word
owner invoice; the current package only resolves the finite local correction.
The structured next question is recorded in [TASK.json](TASK.json).

## Credit

The G/2 channel and dirty-helper cancellation are Rohan Arun's PR1972; the
32-chain schedule is Adam Gall's PR1940; the P104 fixture is Josie Elliston's
PR1071 lineage; the exact native compiler and interpreter retain the attribution
in `research/p104-native-channel/SOURCES.json`. The sparse correction and replay
were prepared with substantial OpenAI Codex assistance. No independent human
review is claimed. New work is Apache-2.0.
