# Validation record

Scientific local commit: 7d4f7d5c8663e674f690fe254c80ebfbe135e982.

- All six commands in the registered package replay passed, outcome partial.
- Committed-byte and source-history check passed for 44 package/input files,
  retaining public base b58ad9ef4d4e861b0eaa5dba41742bdc072dca51.
- Export and archive inventory/hash checks passed. The exporter writes an
  uncompressed POSIX tar regardless of a filename suffix.
- Both new verifiers, rectangular_native.py and state_minimum.py, passed from
  a fresh Git-free extracted export under Python isolated mode (-I -B).
  The native check reproduced both complete words and all 632-column endpoints.
- Assertions are required; optimized (-O) execution is deliberately rejected.
- PR4698 was fetched at 0e2ecf8a60b61bf43d3978633776f08a2f9eab39 and its proof
  was read for overlap. Its related eight-helper normalization is credited.

No new phase-pair enumeration, selected scientific cold replay, global
recursive controller, rounding/compiler proof, outer transfer or independent
human review is claimed. No improved kappa is claimed. Later metadata-only
edits describe the expanded scope and do not change the tested payloads.
