# census-prune-source-impact

**Draft; no new bound claimed.**

## Scope and evidence

Original card: `census-pruning-audit`. Complete [TASK.json](TASK.json), including any scope
change and its connection to the bottleneck. Explain the result and limitations here.
Source commits, Git blobs and SHA256 pins are in [SOURCES.json](SOURCES.json).
The selected record and catalogue are historical provenance, so later priority
updates do not invalidate this package. Explicit --source files are live inputs
and must match their pins. Full Git history is needed to resolve provenance.

## Reproduce

After completing the verifier and marking VERIFY.json ready, from repo root:

```sh
python3 scripts/research_package.py --package research/census-prune-source-impact --check-only
python3.12 scripts/research_package.py --package research/census-prune-source-impact
```

Declare all external inputs and pinned dependencies in VERIFY.json. The generic
hook is bounded; native/Lean or long replays need an explicit dedicated workflow.

## Open next questions

Complete the structured `open_questions` list in TASK.json and explain it here:
the question, why it matters, a feasible first step and any blocker. If no next
question is justified, say so rather than inventing one.

## Credit

Prepared by JoyboyBrian. Retain predecessor attribution and source-specific notices.
New work is Apache-2.0. Disclose substantial AI assistance in TASK.json.
