# Validation

The original diagnostic was run on 2026-10-11 under Python 3.14. It checked the
admitted PR416+956 control and both the original and extended PR419 fixtures.
The control passed in both orientations. Both PR419 fixtures passed ordinary
scalar replay and produced the exact chart-sensitive witnesses in PROOF.md.
Ody independently repeated this regression and obtained the same results; the
source-bound discovery and independent-review receipts are retained in inputs/.

The portable package checks its complete manifest, exact vendored source hashes,
fixture bytes, and six focused tests: admitted endpoints, the original/extended
counterexamples, required normalization chronology, and a formal-token mismatch
that correctly does not establish an actual Gaussian counterexample, a mismatch
first appearing at address one, and an end-to-end exact cancellation that
resolves a failed formal-tag comparison.

The checker has standard-library-only dependencies. No compiler, installation,
network request, numerical optimizer, full phase replay or full supplier replay
is required. Its negative fixtures are intentional expected results. Passing the
regression suite means the checker detects the contract gap; it does not mean
those candidate suppliers are admitted. The witness search now examines every
address column when necessary. The new address-one regression was run against the previously published checker and
failed because it returned no witness, then passed after the change. All six
focused tests pass under Python 3.14. Exact cancellation is admitted only after
all address columns vanish; the original concrete witnesses remain unchanged.

The broader changed-419 component run separately passed both scalar orientations,
14 source mutation controls, coefficient expansion, 6,480 exact Gaussian phase
operators, and 43 residual charts. A later entrance-chart check found the endpoint
obstruction before global execution. Those successful component checks are not
represented as complete supplier admission, and no new κ is claimed.
