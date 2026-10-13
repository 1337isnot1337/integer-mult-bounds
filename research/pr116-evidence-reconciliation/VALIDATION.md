# Validation and limitations

Local validation on 2026-10-13, macOS arm64; CPython 3.14.6 and system CPython
3.9.6. Only standard-library code is used by the new checker.

Completed before submission:

- Ordinary and isolated optimized replay match all fields of `RESULT.json`.
- `test_package.py`: 28 tests pass normally and under `-I -O -B`; 26 reject
  specific transport/parser/evidence corruptions, with two positive controls.
- An offline copy outside the repository passes the checker and all 28 tests
  on Python 3.9.6 from an unrelated working directory, with no changed bytes.
- Rebuilding `CERTIFICATE.json` from the retained Git objects and downloaded
  input snapshots produces byte-identical JSON. The rebuilt capsule passes.
- `python3 -I -B scripts/verify_selected_result.py`: selected PR942 record passes.
- `python3 -I -B -m unittest discover -s tests -p test_selected_result.py`: five
  tests pass.
- `python3 -I -B -m unittest discover -s tests -p test_pr_reconciliation.py`:
  14 tests pass.
- `python3 -I -B scripts/verify_pr_reconciliation.py`: the complete 642-entry
  base ledger and all explicit family/evidence/closure checks pass.
- Only PR116's remaining question and companion pointer changed in the ledger;
  all other rows, heads, attribution, dispositions and counts are retained.
- `git diff --check` passes. The selected certificate and `upstream/` have no
  changes from this contribution.

This is a new offline source/evidence check. The 42 successful checks and three
focused verifier executions are recovered historical GitHub results, not new
CI or a fresh execution of the original package. The author's standalone
full-suite archive was not recovered. No full `make verify`, supplier cold
replay or Lean compilation was run. No mathematical assertion was weakened or
old input rewritten to make a replay pass.

Final integration check: rebased onto
`2921874911956718fcaaaf9396fe8267b3cfa9f0`. The original research base remains
`8bddbee377e2f3ce1f1247196c4b290d55767d20`; all consumed historical objects,
PR116's upstream head and the selected result are unchanged. On rebased
implementation `b5d7e5150f3f25c68107403c6ed035a5c8253c4a`, the optimized 28-test
package, complete result replay, byte-identical capsule regeneration, five
selected tests, 14 ledger tests, selected-record checker and complete 642-entry
ledger checker all pass again. Subsequent changes are documentation only.
The open queue was refreshed through PR1003; no competing PR116 reconciliation
was found. The PR279 work that prompted the pivot has now merged separately.
`codex` and `codex-automation` labels are unavailable in the upstream repository.
