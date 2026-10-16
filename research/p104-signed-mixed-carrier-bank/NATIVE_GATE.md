# Native realization gate: direct E8 root-line adapter fails

The prior schematic signed mixed-carrier bank places new scalar values on binary labels \(u_i+u_j\). This is a valid **formal vector-space** line but not an existing E8 **root line**.

In the standard P104 label realization \(u_r=(\mathrm{rootBits}(r),1)\in\mathbb F_2^9\), every root-line label has ninth coordinate 1, whereas a sum of two root-line labels has ninth coordinate 0. Hence no two-root sum equals any root-line label. This applies to all 120 E8 root lines, not just one selected decoder.

`root_line_gate.py` reconstructs the exact 120-by-120 mod-2 pairing signatures from 240 doubled-coordinate E8 roots and checks all 7,140 distinct pairs. No XOR of two root signatures equals another root signature. This is independent of the selected P104 frame.

**Implication:** a proposed implementation cannot simply relabel a mixed sum as another primitive root-line carrier. One must exhibit a legal generalized frame/phase and scalar word, or another encoding. The result does **not** rule out all arbitrary one-dimensional subspaces of the nine-dimensional label space, nor block generalized-frame constructions.

Required next gate: specify permissible registers, phase conversions, and source/copy/erase/restore primitives; compile an exact signed example; count the extra child ranks and cleanup operations; then compare the full paid moment with current selected frontier. Until then, the 30.8% ADD and 41% frame-rank savings are schematic rather than multiplication bounds.
