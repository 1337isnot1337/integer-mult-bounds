# Working evidence

I have completed source reproduction, native replay and finite compilation.
The new whole-call physical interpreter and its root theorem remain unfinished.
I have not registered this draft as a completed replay package or opened a PR.

I reconstructed the exact PR2979 source through its pinned predecessor chain.
I fetched missing PR2894 commit18d03c447886895ef9abf888398178e0428533ca;
I changed no predecessor files in the repository. The637-file derived source
matches manifest751b46364742cbb947f7db07c130ff09085b38b52c520d3b47f2dadc1e21ba80.

I ran the retained sparse native driver on both changed words with Python3.12.13,
numpy2.2.6 and one BLAS thread. Each provider passed transport, ledgers,
local replay, wrappers and exact phase/warp checks. Base took28.003seconds;
extra took26.941seconds. These source checks retain their authors' scope.

I ran the new compiler under `-I -O -Werror -B`. Each orientation/provider
contains22,748source events and29,782compiled instructions. Each has3517
positive children, with profile

    {1:2445,2:706,3:232,4:108,5:18,8:8}.

I retain91explicit zero-buffer releases and107zero operations (including
the centre starts/ends). The compiled instruction digests are:

| Provider | Orientation | SHA256 |
|---|---|---|
| base | forward | `0d134143fbea5abaac24a1ea1ee575a4657de87835f6563cff92186d681d0263` |
| base | backward | `3b024792bf684ff05c88fa9caf998b8fefa77716ab7509e2fce73ee8f62d0921` |
| extra | forward | `d468032f5d78732be593f3d0f72386be2613e5ac3ff3509b54a3e56aaa9c0a87` |
| extra | backward | `ff23ef17c3ae31a31dbd77eda8478d4a5eaafaf628bf2fdfbe133c07a922e7b4` |

The combined scalar vocabulary has36literals, maximum absolute numerator8
and maximum denominator8. I have not bound its physical scalar microprogram
or recomputed its complete numerical-prefix allowance yet.

The exact layer-budget check gives the conditional bound in
[LAYER-BOUND.md](LAYER-BOUND.md). I have not converted that favorable budget
into a completed physical-layer or integer-multiplication claim.

I checked a possible backward-phase ambiguity before reuse. PR2287's same-label
contract and T74's free-warp endpoint proof permit the same directed native
recipes in both orientations. A source-analysis agent also executed one
PR3385 backward column modulo65537 and obtained its required endpoint.
That check covers one column, not the entire physical matrix. I found no
backward defect and made no change to PR3385.

I used substantial OpenAI Codex assistance, including source-analysis agents.
No independent human or formal-kernel review has occurred.
