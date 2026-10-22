# Scalar block elimination screen

Prepared for Cinna Davis with OpenAI assistance.

`discover.py` examines 618 maximal constant-frame scalar blocks in the current helper-warp word. It forms exact rational matrices, requires acyclic off-diagonal dependencies and dyadic-unit diagonal entries, and tries topological row synthesis. A candidate must eliminate a role with an identity row and column and use at most twice the original gate count.

No candidate meets these conditions. `RESULT.json` records this bounded negative result. It is not a barrier to arbitrary circuit synthesis, nonconstant frames, cyclic elimination, or larger replacement circuits. No kappa improvement is claimed.

Run `python -B research/scalar-block-elimination/discover.py` to regenerate the result. The source is the published helper-warp word at commit 7197831b13c8f5715055a608a148fbfde7b38b7d; its native lineage and credits are retained.

## Open next questions

Relaxing the acyclic dependency condition may permit a cheaper exact factorization. Screen the complete bridge invoice before investing in physical certification.
