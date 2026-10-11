# Byte-identical caching for the E8 emitter's digest loop

The pinned [PR447 emitter](https://github.com/rohanarun/integer-mult-bounds/blob/43e5aa3a2fb6701b1facf542f7f3dee0fbb33c3e/research/e8-eleven-hosting-selected/code/emit.py)
serializes the same owner descriptors and instruction tails repeatedly while
hashing each renamed local invocation. This package caches each fixed integer
tail once per orientation and each owner descriptor once per call. Every
instruction still enters the digest in its original order.

On two retained workloads comprising **2,742,552 records and 144 calls**, the
exact source-extracted hashing loop took a median **3.206 seconds** before and
**0.587 seconds** after this change, about **5.47x faster**. These three trials
include tail compilation and owner-cache setup and alternate execution order.
They ran on macOS arm64 with Python 3.14.8. Template loading, geometry checks,
file compression and the rest of the supplier wrapper are outside this timing.
This is a hashing-loop microbenchmark, not an end-to-end speedup claim.

The comparison checks every record byte, the full independent digests, event
counts and paid local-instruction profiles. Both orientations, all four
opcodes, signed operands and private-owner references are covered. The fixture
bytes come from completed PR438 and authentic PR442 runs; this is not a fresh
PR447 supplier replay. The pinned PR447 producer uses the same checked event
schema. PROOF.md gives the byte-preservation argument for that schema.

`EMITTER.patch` changes only the helper import, one-time tail compilation and
the hashing loop. An AST comparison verifies that every other source statement,
including all original ownership and scientific checks, stays unchanged. To
apply it to the pinned source checkout, copy `digest_encoder.py` beside its
`code/emit.py`, then apply the patch with the appropriate package directory:

```sh
git apply --directory=research/e8-eleven-hosting-selected /path/to/EMITTER.patch
```

Streams and owner descriptors must remain unchanged during each encoding pass,
as they do in the pinned emitter. Unsupported event shapes are rejected.
The original source notices and license are retained in this package.

Run the portable offline validation with Python 3.11+ and the standard library:

```sh
python3 -B research/e8-emitter-digest-cache/verify.py
```

This checks source/Git/fixture/receipt bindings, the full byte contract, exact
patch scope, and two focused test contracts for JSON escaping, integer tails,
per-call owner-cache freshness, malformed shapes and invalid operand indices.
It does not rerun the benchmark or any supplier stage. To measure the same
extracted loops on your machine, add `--benchmark`; optionally save its report
with `--output /absolute/path/to/new-report.json`.

The recorded measurement used the exact frozen adapter under `evidence/adapter`.
Its original temporary input paths are retained as execution evidence; the
portable verifier uses the bundled fixtures. All inherited mathematical
interfaces, numerical bounds, finite coefficients and emitted bytes are unchanged.
