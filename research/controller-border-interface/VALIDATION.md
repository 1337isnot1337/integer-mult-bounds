# Executed validation and limits

Prepared by Dillon with substantial OpenAI Codex assistance, 2026-10-22.
Environment: macOS ARM64, Python 3.12.15 for the registered replay and
Python 3.14.7 for the second isolated optimized replay. Standard library only.
Scientific base: canonical main `f626db5c3a3d781d8f7695038776c621651f75e1`.

## Scientific checks completed

```sh
python3.12 -B scripts/research_package.py --package research/controller-border-interface --check-only
python3.12 -B scripts/research_package.py --package research/controller-border-interface
python3.12 -I -O -B research/controller-border-interface/verify.py
python3 -I -O -B research/controller-border-interface/verify.py
git diff --check
```

All pass. The registered replay reports
`PASS_REGISTERED_RESEARCH_PACKAGE ... outcome=partial`. A metadata pass alone
does not verify mathematics; the separate scientific command actually executes
the checkers and compares the exact receipt. The explicit authoring `--write`
command was used once to create RESULT.json before normal comparison runs.
Floating-point discovery roots are intentionally excluded from that receipt.

The checks cover all Laurent coefficients for p=1..8, including orientations,
filtration degree and exact decoder matrices; exact integer-power enclosures
for the all-p budget certificates; independent rational event execution on 24
p2/p3 instances and all columns; 48 wrong-weight controls; four actual
polynomial degree-growth examples; and nine exact conditioning examples.
The written proofs, rather than finite extrapolation, establish the all-p
claims. Repeated-evaluation checks credit fresh independent helpers correctly.
Omitted thin queries and duplicated main credit demonstrate invalid invoices
that would reverse the decision. They are fault controls, not new candidates.

A separate author-side AI worker reviewed the proofs and wrote the independent
rational implementation without importing either controller implementation.
Three temporary-source mutations of that independent checker were rejected in
optimized Python 3.12: wrong p2 X coupling, wrong reverse wrapper, and omission
of the conditioning term in the precision budget. REVIEW.md records coverage
and corrections made during review. This is not independent human review or
a formal-kernel proof.

The selected-baseline helper separately passed source/metadata orientation.
No selected native cold replay, whole historical suite, Lean build or Docker
run was needed or performed. Existing native, physical, ordinary BIT, analytic
and recovery premises are inherited, not recertified by these checks.

## Publication checks

Committed-byte, source-history, archive integrity and isolated exported replay
results are recorded below after the scientific files are committed. Until
then, the scientific results above are local author-executed evidence.

## Research decision and remaining obligations

The hour began at 09:56:24 UTC. Guidance was read from refreshed upstream at
09:59:29, and selection followed at 10:05 after comparing several major avenues.
The original greater-than-.01 target is rejected within the proved fixed
inventory and output contract. The exact formal construction remains a partial
interface result; no new supplier, kappa or frontier update is reported.

The raw complex norm specialization is conditional on explicitly stated
completed-operation norm bounds. A numerical implementation must still bind
oracle errors, coefficient heights, movement, input magnitudes and runtime.
A chronological amplified/recursive word needs its own global bound. BIT
needs an explicit scalar-extension representation and complete return cost.
The scoped recovery obstructions leave shared internal queries, cross-port
schemes, changed native words and changed output contracts open.

Apache-2.0. Retain the predecessor attribution in README.md and SOURCES.json.
