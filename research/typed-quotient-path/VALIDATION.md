# Validation

Executed on Linux with CPython 3.12.15:

- Registered `scripts/research_package.py --package research/typed-quotient-path`: PASS.
- Isolated optimized `python3.12 -I -O -B research/typed-quotient-path/verify.py`: PASS.
- Exact original Git-blob/SHA256 inputs, both paid rank counts and 520-helper census: PASS.
- Both Laurent B normalizations and five sign/orientation/Q controls: PASS.
- All 2,504 complete split/support invoices through p=4: PASS.
- Rational derivative certificate stronger than 1980/7: PASS.

The all-p/all-C assertion is the written monotonicity proof, not extrapolation
from these finite cases. The supplied PR4654 typed native theorem is a premise.
Its 632-row, absolute-phase and all-width proof was not re-audited here.
No selected cold replay, changed native word, higher K or proof-kernel
acceptance is claimed. Hosted checks are separate from local replay.
