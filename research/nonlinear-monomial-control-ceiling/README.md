# Nonlinear weighted-monomial control ceiling

This is a new support-partition extension of [PR #5160](https://github.com/CrocSwap/integer-mult-bounds/pull/5160),
not a repetition of its Clifford alphabet. For the released four-control endpoint,
**arbitrary nonlinear weighted monomial** one-column controls still force
`t0_f=0` at every sufficiently large width, provided the program has a fixed
finite set of complete one-column operator products independent of width.
Thus no all-width invertible family exists in this declared class.

The outer scalar owner coefficients may depend on width. **A finite generating
alphabet alone is insufficient:** weighted generators can produce infinitely
many projective products as word lengths vary with width. Such unbounded
width-dependent products, growing complete-product supports, noncolumnwise
routing, extra paid calls/axes, changed codes and altered productive targets
are outside the theorem. This distinction was found during independent review;
the rejected first draft is retained unchanged.

## Written theorem and source binding

The unchanged [final proof](evidence/proof-review/frozen/REVIEWED-PROOF.md),
SHA256 `76bea47531ed557c0c9cb210c4324d6000c74415bf13e5747b7036567853f6ef`,
passes the separate [independent written review](evidence/proof-review/REVIEW.md).
The author's original status text still says review pending; this README records
the subsequent final review without altering those original bytes.

The argument uses complete support blocks. A weighted monomial intertwiner
must send support-partition blocks to blocks; no phase or Clifford
classification is assumed. The transported letter preserves the W and q+W
coset partitions. It therefore cannot carry a direction with a nonzero U
component into a direction contained in q+W. In the actual source endpoint,
monomiality forces `s=j`; the source coefficient is then `A[j,j]=0`.
Uniform tensor separation of a fixed finite set of complete operator products
supplies the sufficiently-large-width conclusion. Cancellation cannot create
a monomial class absent from every surviving source term.

The scientific source remains `4c0a359d88f22f05189d51f48387750b801a45d4`,
`research/coded-native-caller`, on q+U8+W8 (17 axes,112 owners).
The released endpoint is `E=Q^-1 C3 t C1 Q^-1`, `t=D3 t0 D3^-1`.
The predecessor is #5160 head `7800589ce99d932bdb063aafca1f501f1a38626d`;
#5126 head `0e8a13c251a9be1029114cda8b4194f05f3a23ec` is context, not
an executable free dictionary. Publication base is
`ec2780e8aeb1c88acaf5e9e470ef8c68e7fbbb6c`.

The proof-review packet retains the exact raw CODE/NORMALIZERS/PHYSICAL
captures, predecessor proof/source manifest/checker, final proof and rejected
first draft. [SOURCES.json](SOURCES.json) binds reachable Git blobs;
[EVIDENCE.json](EVIDENCE.json) authenticates the unchanged original packets.
CRLF source bytes are preserved with local `evidence/** -text` attributes.
Actual112/17 source facts remain inherited from the pinned predecessor;
this package does not reexecute its native source or all-port evaluator.

## What the finite checker establishes

The unchanged [checker](evidence/finite-check/check_support.py) uses exact
Gaussian-rational16x16 matrices on q,u1,u2,w. It checks three examples:
weighted nonlinear Toffoli on q or w, and CCZ(q,w,u1). Its108 terminal
sandwiches are nonmonomial. The exact controls demonstrate that dropping
join preservation or the nonzero-U condition changes the answer; transported
CCZ need not preserve central q-cosets; reversing D conjugation or omitting
its inverse changes literal matrices. Gaussian C squared is X, not identity.
Both RESULT and complete MATRICES regenerate byte-for-byte in normal/O modes.

This is finite support calibration, **not** an all-width theorem checker,
17-axis source fixture, rank lower bound or physical absolute-phase campaign.
The independently reviewed written proof carries the uniform theorem.
No t0 search, native/emitter/compiler/Lean replay or complete κ claim is made.

## Reproduce

```sh
python3 -I -W error -B research/nonlinear-monomial-control-ceiling/verify.py
python3 -I -O -W error -B research/nonlinear-monomial-control-ceiling/verify.py
python3 -B scripts/research_package.py --package research/nonlinear-monomial-control-ceiling --check-only
python3 -B scripts/research_package.py --package research/nonlinear-monomial-control-ceiling
python3 scripts/check_research_commit.py --package research/nonlinear-monomial-control-ceiling --ref HEAD --check-source-history
```

CPython3.12, standard library only; direct runs take about1second. The wrapper
authenticates every original packet manifest and runs an unchanged checker
copy in private scratch with the original four source paths. The author checker
writes RESULT/MATRICES next to itself, so direct execution against its frozen
evidence directory would mutate it: use the registered wrapper. Package and
exported source bytes stay read-only. Complete RESULT/MATRICES, not just
compact summaries or container hashes, determine equality.

```sh
python3 scripts/export_research_package.py export --package research/nonlinear-monomial-control-ceiling --ref HEAD --output /tmp/nonlinear-monomial-control-ceiling.tar.gz
python3 scripts/export_research_package.py check /tmp/nonlinear-monomial-control-ceiling.tar.gz
```

## Open next questions

A constructive continuation must change a named premise: actual noncolumnwise
control, growing complete-product support, an affordable paid control, or a
changed observation/endpoint with exact arbitrary-input ownership and source
access. No such supplier is supplied here. Retained native/helper observations
remain with their existing investigators. Unknown finite costs, precision,
restoration, compiler reserve and outer admission are not zero.

## Credit

Root support-partition derivation and separate independent proof review;
finite nonlinear discriminator and its author review; Chris R/Clear1nsight
packaging, all with substantial OpenAI Codex assistance. Retain Dillon's
released equations, Dugongue/mdumitrean's source A and normalizers, Cinna
Davis/1337isnot1337, Cao Yifan/intqwq, zxv, Jacob Alan Sussman, Ryanson
Jonathan and the native/helper/Clifford/compiler lineage. Original Apache-2.0
LICENSE/NOTICE and source notice remain included. No published-paper novelty,
independent human acceptance or proof-kernel verification is claimed.
