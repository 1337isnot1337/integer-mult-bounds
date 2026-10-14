Fixed-tape proof toolkit, 2026-10-13. New work is Apache-2.0.

New theorem implementations, the finite compiler and scheduler, dirty-frame
proofs, examples and replay infrastructure were prepared with substantial
OpenAI Codex assistance, including three parallel Codex agents. No submitting
user's name, email or private machine paths are included.

Mathlib supplies its Turing tape/TM2 and asymptotic vocabulary and retains its
own upstream licensing and attribution. No Mathlib source tree is vendored.
The toolkit's finite absolute-coordinate convention was compared against
platypii/integer-mult-bounds-lean, Machine.lean at
4f270864a297374cae8e443c520c6225b625c0d5. Lean PR1 and PR2 supplied inspected
statement, adapter and heterogeneous-host context; their proof implementations
are not imported or copied into this package.

CrocSwap/integer-mult-bounds PR1379 by commdata2338 supplied the motivating
recursive parking boundary and named open Lean frame/composition work, building
on rfu08's PR64 transfer lineage. Its stream implementation is not vendored or
claimed proved here. PR1608 and the earlier PR893 audit lineage motivated exact
declaration/report coverage; their audit implementations are not imported.
Original selected construction and upstream contributors retain their credit.

The package proves its displayed universal sufficient machine/transfer results.
It changes no supplier, selected record or kappa and does not represent a
formal verification of the full fast multiplication theorem. Local kernel
checks, hosted CI, public submission and external human review are distinct.
