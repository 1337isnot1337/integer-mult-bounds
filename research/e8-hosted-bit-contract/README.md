# Preserve the parent contract in the hosted bit audit

This package adds a guard for the bit-side idle-axis-hosting audit from
[PR442](https://github.com/CrocSwap/integer-mult-bounds/pull/442), pinned at
`4e16d001d505d4f21dd2bcfc44591f9be4c279bd`.

The original generator preserves the parent scalar schedule. Its independent
hosting audit checks ownership and paid profiles but does not enforce that
schedule preservation. Removing the terminal exchange or zeroing a bridge
coefficient leaves its reported paid profile unchanged and is accepted by the
original audit, although the scalar program is incorrect.

`require_hosted_bit_contract(hosted, parent)` closes this verification gap. It
checks all eight scalar columns, legal level progression, nine local stages,
nine bridges, and the terminal exchange. It then requires exact preservation
of the parent schedule, invocation headers and inherited template fields.
Only the added, consecutive idle indices and the generator's documented
hosting fields are allowed to differ. In particular, the guard does not strip
unknown metadata or ignore changed bridge signs.

Use the guard before the existing ownership/profile audit:

```python
from schedule_guard import require_hosted_bit_contract
require_hosted_bit_contract(hosted, parent)
profile, hosted_count = audit_bit(hosted, parent, widths)
```

`hosting-audit.patch` supplies this integration against the pinned original
`audit.py`; place `schedule_guard.py` beside that file. The standalone check
also accepts plain JSON or gzip input:

```sh
python3 -B schedule_guard.py parent.json.gz hosted.json.gz
python3 -B verify.py
```

The parent must be source-bound and independently admitted. The new guard
supplements the ownership, hosting-window, paid-profile and finite-invoice
checks. It does not replace them. This package covers the bit template only;
the complex generator has different permitted schedule edits.

This is a verification improvement. The demonstrated mutations are deliberate
regressions, not the actual published construction. No invalidity of PR442's
bound, new exponent, or new hosting method is claimed. The original numerical
result retains its conditional supplier and analytic assumptions.

## Validation and evidence

The positive fixture is the actual PR442 bit template, payload SHA256
`dd7833dcaff8c84b258847f4c4d65b6402c702700ae37d2c464083ee37b24126`,
matching the immutable upstream EXPECTED.json. Its parent template also matches
the committed parent receipt. A seven-stage, 4.43-second reconstruction reused
an exact previously verified reset word, then ran the original 110-entry
kernel, exporter, integer source-span checker, global emitter, parent audit,
and frozen bit hosting generator. The parent kernel's three controls and its
audit's eight controls passed. No complex, phase, pricing or assembly run was
performed; this is fixture reconstruction, not a new bound admission.

On that authentic hosted output, the original audit accepts both regressions
with the same profile and 39,568 hosted residuals. Scalar replay finds eight
wrong columns after exchange removal and three after zeroing the bridge.
The new guard accepts the intact output and rejects both, plus changes to
bridge signs, levels, invocation headers, idle indices and inherited fields.

The offline verifier checks the exact source/Git bindings, upstream payload
hashes, completion and stage-log bindings, retained dependency reuse, and all
four focused test contracts. It executes the proposed integration patch in
memory against the original audit and checks its positive and negative cases.
`evidence/adapter` retains the executed driver's original temporary paths and
source hash inventory, not a portable reconstruction CLI. The guard, patch and
offline verifier are portable and require only Python's standard library.
