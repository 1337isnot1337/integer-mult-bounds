# Validation and scope

Exact runtime: Python3.12.14, NumPy2.3.5, isolated/optimized/no-bytecode mode.
On Ross's Mac the tested interpreter is
`/Users/ross/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

```sh
python3 -I -O -B research/h6-compensation-network/verify.py
python3 -I -O -B research/h6-compensation-network/gate/replay.py
make selected-record-check
git ls-remote origin refs/heads/main
```

The unified receipt is `RESULT.json`, with eleven step logs in `checks/`.
The relocation/corruption receipt is `gate/RESULT.json`. It records the
tested implementation/specification hashes, exact inherited Git-blob pins,
semantic controls, environment and elapsed time. New checks are explicit
exceptions and stay active under `-O`; the pinned lowerer's legacy asserts
are disabled, while the independent wrapper guards remain active.

The final selected-record check passed for
`836330098538459/500000000000000000`. Remote main remained
`0b1cccf86e2f5132ed286a26ef0a681a495740ea`. That check is separate from
package replay and does not cold-replay the selected supplier.

Coverage includes the complete polynomial identity and actual feature
binding; complete bucket census and cap-span witnesses; emitted8/32-port
edge and bucket K+compensation words with every arbitrary source, target,
center and ordinary-helper column in both orientations; three stored
whole-target partial routes; rank/tableau/exact-state/global-phase physical
checks; universal endpoint completion family; every used signed dyadic
coefficient's cleared stream; finite exact-child grid ledger; bank/pad/stock
and rational nominal invoices. Negative controls detect changed coefficients,
missing dirt cancellation/restoration, illegal frames/lifetimes, mispriced
stock/pads/private C/scalar work/movements, wrong physical phase/rank,
understated grid and changed inherited sources.

Ten specialists covered contract, lifecycle, route structure, invoices,
explicit K, bank/compiler provenance, independent replay, universal physical
recipes, adversarial synthesis and clean-export gates. The root joined and
reviewed their work. These are machine-assisted checks, not human peer review.

One real replay issue was corrected during integration: `-I` removes implicit
sibling imports, so the stored-route checker now inserts its own directory
explicitly before importing its independent scalar/frame interpreter. The
full optimized replay was rerun after the fix. Earlier identified count,
exception-handler and movement-ledger presentation issues were also corrected
before the final snapshot.

Unrun/unproved: executing the entire billion-event stream, integrated immutable
physical bank/controller/pad/tape program, approximate-child error propagation,
all-size precision/common-grid and bit-supplier admission, outer analytic
transfer, general `make verify`, hosted CI, theorem/frontier admission. The
prior exhaustive958,521,600-entry pairing receipt is retained immutable
input evidence. Nominal planning roots and exact-child finite-grid closure
are not promoted to those stronger obligations.

All changes are confined to this new package. Prior audit, frozen H6/PR606,
`upstream/`, selected certificate and imported exact lowerer remain unchanged.
No Discussion post, PR, merge or remote publication was performed.
