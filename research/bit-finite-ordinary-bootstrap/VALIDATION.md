# Author-side verification

Scientific commit: `db3856719bdf2b913f9662ec348e39c2c7c65242`.
Base: `624de9dc66858af0945e5f8a0942488d62280d43`.
Environment: Windows, CPython 3.12.14, standard library only.

- Registered package metadata/source pins: PASS.
- Both registered commands, normal mode: PASS. This includes the source-identical
  PR4760 native/caller/all-RAW replay, the tighter rank compiler and all three
  ordinary stages, and the separate census/positive-series arithmetic engine.
- Committed-byte/source-history preflight: PASS, 43 source inputs and 53 total
  exported scientific files. No predecessor file was changed.
- Export creation and archive integrity: PASS.
- Fresh Git-free extraction, empty PATH, both direct commands under
  `python -I -O -B`: PASS. Source/native, deterministic primary/independent
  certificates and negative controls pass from that extraction.

Reproduce the registered checks with the README command. Direct export commands
are `verify.py` and `independent.py`. The portable replay uses no network calls;
the environment did not impose a network-denial policy. Later documentation
and publication-identity commits do not change the verified scientific code,
parameters or input bytes; their committed bytes are checked separately.

Separate internal AI checks independently derived the exact tails, H0/H1,
prime allowance and three stages, and read the completed arbitrary-width,
spectator and nested ROW contracts. These are author-side assisted checks,
not external human review or formal-kernel verification. The completed backend
and underlying implementation premises remain those identified in PROOF.md.
The enormous uniform program and fixed machine/precision constants are
algorithm-defined, not materialized or empirically timed here.
