# Check independent dirty endpoints before pricing a supplier

This verifier keeps each entrance normalization `T_E^-1` distinct when replaying
the actual old response, main word and cleanup. It detects cross-helper dirty
responses that an ordinary scalar identity check can miss. It is an additional
finite interface check, not a full supplier or all-size theorem verifier.

The included regressions establish:

- An admitted PR416 plus entrance-956 word passes both orientations.
- The supplied original PR419 word and our entrance-956 extension pass ordinary
  scalar replay, but fail the independent-helper endpoint after normalization.
- The failures are instantiated with exact Gaussian operators. In the forward
  direction, dirty helper 255 contributes `(I - T_[48]^-1)/4` to helper 244.
  A basis input at address zero gives an unexpected `(1+i)/8` at address zero.
- The issue is already present before our entrance upgrade. No improved numerical
  bound is claimed by this package.

This concerns the proposed assembly into independently normalized residual banks.
A different coupled-bank construction would need its own endpoint, routing and
cost proof. The result does not disprove such a construction or an unconditional
multiplication theorem. See [PROOF.md](PROOF.md).

Run the source closure and regression suite, using Python 3.11 or later:

```sh
python -B research/e8-dirty-chart-audit/verify.py
```

Audit an emitted program with the same scalar/event schema:

```sh
python -B research/e8-dirty-chart-audit/chart_audit.py candidate.json \
  --programs LOCAL-PROGRAMS.json.gz --output new-result.json
```

For the bundled PR419 bracket, use `--emitter419` in place of `--programs`.
Successful formal or exact Gaussian endpoint checks exit zero. An actual
mismatch exits one. Different formal tags alone are not treated as a Gaussian
counterexample: the verifier evaluates all address columns of every distinct
coefficient operator, stopping at the first exact nonzero entry. If every column
vanishes, it reports `PASS_EXACT_GAUSSIAN_ENDPOINT`. It caches operators and the
current address column, without retaining whole dense matrices.

The regression suite also includes a three-axis operator combination that is
zero on address zero but nonzero on address one. Testing only the first address
would miss this mismatch. Another test resolves different tags that represent
the same exact operator. These checks concern the emitted endpoint only.

The fixtures are finite words from pinned research runs. PR419 event streams are
regenerated with its byte-identical emitter. The admitted control uses a retained
emitted-program fixture. This package does not rerun the upstream word searches,
phase verification, banks or pricing. [SOURCES.json](SOURCES.json) records exact
provenance; [VALIDATION.md](VALIDATION.md) records what was executed.
