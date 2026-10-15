# Validation scope

I use Python 3.12.15 on macOS arm64. Each registered command authenticates the
97 frozen files and PR2753's transitive repository inputs before execution.
The verifier compares a SHA256 receipt over the complete canonical JSON result
of each suite, including event counts, restoration outcomes and operation meters.
I retain the expected receipts in RESULT.json.

| Suite | Evidence |
| --- | --- |
| frame | Actual selected IDLE source 27825, widths 256→168→84, two repeated frozen-prefix records, exact projected extents, same Word objects/slots/bytes/heads after return. Controlled 23-bit bodies. |
| frame failures | Constructor failure after PARK and a deeper child failure; initiating error and parent state survive cleanup. |
| continuation | 36 good/fallback traces, 16362 compared events and 180 reconstructed return cursors. Width quotients 1,2,3,63,64,65,127,128,129. |
| role parking | 1500 nested frames, four permanent stream roles, three allocated index slots, 1501 protected output symbols. Exact composed table charge 1051500 steps. |
| controls | Nine complete-result transfers; short/out-of-range/overlong finite-control records and a dirty child role reject. |
| nested | Complete 9216-address GL2 payload, 12 shared-bank child calls/returns, 156 residuals, 12 root-stock and 144 child-stock checks. Independent address provenance oracle. |

I completed all five registered commands with exit code 0 on 2026-10-15. The
launcher reported `PASS_REGISTERED_RESEARCH_PACKAGE`; the complete nested
payload took 150.31 seconds under Python 3.12.15. The frame and continuation
commands also passed with `-O`; their acceptance checks use explicit exceptions.
I ran the pinned GL2 oracle with ordinary Python.

I then fast-forwarded the isolated branch to canonical main
`28f54620ff770dd051d5df35882bd84303d13c6f` and authenticated the complete source
inventory again. The registered runner, declared runtime inputs, guidance and
selected record had no changes. I did not repeat the unchanged payload suite
after that refresh. The source selection/provenance base remains
`31452ecd309f32a97e2e84214719b21297a59018`.

The whole-caller lowering in PROOF.md is a source-level construction. I have not
generated its full transition table or replayed a selected GL64 payload. The
complete GL2 payload still uses the predecessor's logical scheduler. The 1500-
frame test instead executes a finite iterative controller with encoded depth,
which tests checkpoint composition without exercising the selected arithmetic.
The GL2 fixture uses one family, cutoff 2 and coordinate projectors at its root;
its internal children execute all twelve conjugated GL2 good/fallback forms.
It does not instantiate the selected dimension-64 source or its stock multiple.

I ran the task card's historical owner-boundary positive control and the current
baseline binding check. Those checks establish orientation and source bindings;
they are not new mathematical results or the selected complete cold replay.
This package changes no selected construction file, parameter or certificate.
