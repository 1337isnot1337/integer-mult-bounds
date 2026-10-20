# Executed evidence and limits

Scientific base: `12fa8c5c844be21bfefb38a19503fbd867a11244`.
Task: `supplier-boundary-audit`, priority revision 7, refined to the exact
PR4088/PR4165 four-provider admission handoff. The assignment and experiments
are deterministic; there was no randomized task lottery.

## Baseline and bounded evidence

The inexpensive `python3 -B scripts/research_baseline.py` passed
`PASS_RESEARCH_BASELINE_BINDINGS_ONLY`. This checks source bindings, not
mathematical acceptance.

The retained PR4085 source preflight was executed freshly, redirecting only its
output location into a private external work directory. Its three independent
terminal, staged-entry and receiver reviews passed. It reconstructed exactly
676 source files, manifest SHA256
`4116ef61479e509811b60b5fd4e84db8811dae079092f2f83bdcc2c80052c0da`,
and admission engine SHA256
`e69184d235d8790a3c520977dd44dcfb73a99d56989825485f922ff61059c8b1`.
All 95 non-source archive inputs matched their retained inventory.

An unmodified inherited owner reconstruction on the real PR4085 THREE control
reproduced its old invoice, including idle
`{3:22842,5:1890,48:138438}`. The independent mixed scan and the new binding
then reproduced the distinct PR4088 invoice in the README. PR4165's existing
five rejection controls also passed; its idle finding is predecessor credit.

Both FOUR native sources were freshly executed through all five stages:
`native`, `ledgers`, `local-replay`, `wrappers`, `phases`. Initial executions
took 63.145 and 68.423 seconds. These are observed wall times, not a speedup
claim. Unchanged THREE and parent-admission evidence is explicitly authenticated
reuse, not a fresh cold replay of the entire historical ancestry.

Executed bounded commands:

```sh
python3 -B scripts/research_package.py --package research/mixed-provider-admission
python3 -O -B research/mixed-provider-admission/independent_ledger.py --controls
python3 -B research/mixed-provider-admission/challenge.py --work REPLAY_WORK --preflight PREFLIGHT
python3 -O -B research/mixed-provider-admission/challenge.py --work REPLAY_WORK --preflight PREFLIGHT
```

`REPLAY_WORK` and `PREFLIGHT` above denote the actual external output directories,
not repository dependencies. The registered command passed the 192 live pins,
14 semantic test methods, all 1,321,920 real rows, the optimized unit controls
and the independent event/span checker. The independent checker also passed
separately under `-O`, with an identical result object.

The public actual-output challenges passed 18 cases in normal and optimized
Python. They include all four providers, changed phase with coherently rebound
references, skipped native stage, equivalent serialization/timing positives,
and a changed predecessor engine with its completion receipt rebound.

`python3 -O -B research/mixed-provider-admission/replay.py --work NEW_DIRECTORY`
was rejected before creating the directory, with
`inherited admission requires assertions`. An optimized full release is not
reported as passing.

## Development failures and corrections

The first mixed wrapper attempt reached the new rebind gate and failed because
the inherited reconstructor serializes dispatch rows chronologically, while the
literal input table has a different row order. The correction compares the
table as a sorted relation while separately requiring a bijection and checking
every chronological call, program, orientation and width. A permutation
positive control and changed-selector negative controls cover this distinction.
No owner or accounting predicate was removed.

A separate adversarial AI context demonstrated two draft reuse gaps: an
unbound cached admission driver and native output phases authenticated only by
successful flags. The fixed engine commitment and fixed scientific output
commitments close those demonstrated gaps. That context's 17 bounded follow-up
cases passed before the public four-provider challenge script was added.
These were defects in this unpublished draft, not new allegations about
predecessor mathematics.

A preliminary metadata-only check rejected the draft outcome string
`in-progress`; it was corrected to the schema's `partial` state. The registered
metadata and pin checks then passed.

## Full release

The development replay has passed complete discovery, both outer ledger
checks, native/Lemma-G bindings and the ordinary source-review chain. The
strict and final outer release are still running at this development checkpoint.
No final admission is claimed from those intermediate stages. The final
publication gate additionally requires a fresh replay from a committed,
Git-free source export and inspected release receipts.

## Review and overlap scope

The 2026-10-20 08:19 UTC refresh still found canonical main at the scientific
base and priority revision 7. The helper covered all 294 open/draft PRs and
2,693 Discussion records with complete pagination and no warnings. The latest
50 updated PRs were also inspected for merged successors.

PR4170's pooled-ceiling transfer and PR4171's independent moment/paid-power
arithmetic are complementary to this actual caller/ordinary/outer integration.
PR4169 audits a PR4100 CRT repair implication. No equivalent admission
successor or active claim was found in that coverage. This is an overlap check,
not a proof of novelty. Coordination remained local-only.

## Checks outside this result

No repository-wide historical suite, selected #1094 cold replay, Lean proof,
reference dense native backend, Windows execution, or hosted CI was run.
The selected construction is not changed. No complete all-size theorem,
independent human review or maintainer acceptance is established.

The numerical environment is CPython 3.12.14 on Linux, NumPy 2.3.5,
SciPy 1.17.0, SymPy 1.14.0 and mpmath 1.3.0, all already installed.
The full driver checks these dependency versions before running.
The registered regression itself uses the Python standard library.

Prepared for yssite with substantial OpenAI Codex assistance. Apache-2.0;
all predecessor credits and source-specific notices remain applicable.
