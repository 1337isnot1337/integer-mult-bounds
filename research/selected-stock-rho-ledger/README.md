# Selected m=73 row ledger: the non-complex terms do not bind `rho`

**Card `selected-stock-envelope`, scope refined. Partial. No new κ.**
[#3113](https://github.com/CrocSwap/integer-mult-bounds/pull/3113) and
[#3421](https://github.com/CrocSwap/integer-mult-bounds/pull/3421) bound `B`
and `A` for the selected m=73 complex producer:

```text
sigma <= (43/26)*(1-s)*(A+B) + rho,    A = 0,  B = 2642
```

That leaves `rho`, the leaf reserve, as the only unbound term. This package
traces every non-complex term of the selected row ledger to its source. It
shows that those terms cannot serve as `rho`, and reduces `rho` to a named
two-way missing lemma. Both branches pass the native stage-1 fit guard.

```sh
python3 -I -B research/selected-stock-rho-ledger/verify.py
```

Expected:

```text
PASS_SELECTED_STOCK_RHO_LEDGER B=2642 ledger=16469 9909=367*27 252=9*28 1024=2*512 bit_row=18355=8194+9909+252 implicit_rho_3113=11185 rho_a=0 sigma_a<=4362.14 rho_b=8194 sigma_b<=12556.14 guard=16,17<=6562783 controls=10 checks=42
```

Python 3.12 standard library, under one second. The verifier authenticates
every live input listed in [SOURCES.json](SOURCES.json). It reads three
members of the pinned PR1087 tarball in memory; its `code/assemble.py` hash is
the one `selected-bootstrap-stock-audit` pins. Every constant is parsed from
source text, not typed in. Nothing from the repository is imported or executed.

## Source facts

1. **The selected ledger.** Frozen PR1087 `code/assemble.py` asserts the
   ledger `2*stock.bit_length()+9909+252+1024`, which gives 16469. It also
   asserts the retained cap `20161` and the external degree gap
   `10^6 - (51/25)*20161`. That gap is the selected `ASSEMBLY.json`
   `outer.row_product_gap = 23971789/25`.
2. **9909 and 252 are historical family charges.**
   `notes/partial-gauge-assembly.tex` gives the "coarse bit, ordinary leaf and
   complex families" the (halving degree, wire bits) pairs `(367,27)`,
   `(9,28)` and `(200,28)`. Hence `9909 = 367·27` and `252 = 9·28`. Later
   assembly notes carry them forward unchanged as "conservative previous bit
   and ordinary-leaf reserves" (`58344+9909+252`, `10284+9909+252`). The
   367-level coarse-bit family is not the selected PR589 BIT producer, whose
   halving depth is 2.
3. **1024 is the prefix term.** `invoice_allcold.py` sets
   `row_prefix_extra = 2*payload`, and `charged_prefix_bits = 512`.
4. **The selected BIT ledger stacks the same constants.** PR510's
   `assemble9.py` computes `row = DEPTH*(m*m+1)+9909+252 = 18355`. With
   PR589's `nine.bit` record (m=64, maximum child 42, 28,425 physical roles,
   halving depth 2), the BIT family's own term is `2·(64²+1) = 8194`. That is
   the coefficient
   [PR2084](https://github.com/CrocSwap/integer-mult-bounds/pull/2084)
   (`research/selected-bit-parent-reserve`) proves conditionally. PR2084
   already reads this formula and argues that the other outer allowances do
   not enter the BIT sigma. That BIT-side observation is not new here.
5. **The two stocks have different units.** The assembly notes define a row
   coefficient as the degree of a **fixed external polynomial reserve**:
   `log2 Q <= (51/25)·K·log2 p`, and `p^(10^6)` for the selected assembly.
   They state that the width-dependent q-adic selector stock is "supplied by
   the separate internal borrowing proof, rather than multiplied into this
   external polynomial stock". H3,
   `log_q S(e,w) <= sigma·w·(1+log2 e)` with `k < e/2`, constrains that
   internal borrowed stock.

## What follows for `rho`

- #3113's conditional readings sigma ≈ 16469 or 15555 put the external-ledger
  constants `9909 + 252 + 1024 = 11185` into the borrowed-stock envelope. The
  verifier reproduces `15555 − ⌈43·2642/26⌉ = 11185`. Those constants are
  w-free degrees of an external reserve, and 9909 belongs to a historical
  family. So the ledger does not supply a source-bound `rho`. The control
  `ledger_constant_as_rho` rejects 9909 as a w-free bound on the w-shaped BIT
  term, because `9909 < 8194·w` for every `w >= 2`.
- **Reading (a): completed leaves.** If every BIT/ordinary callee inside an
  m=73 node is a completed call that borrows internally and restores (PR2084
  hypothesis 4, the reviewed PR185 contract), then the external `S_leaf = 1`.
  `selected-coarse-depth-stock/PROOF.md` already allows this conditionally.
  Then `rho = 0` and, at native stage 1,
  `sigma <= (43/26)(1-s)·2642 ≈ 4362.14`, with `ceil(log2(8·sigma)) = 16`.
- **Reading (b): the parent reserves the BIT factor.** This is the mode
  `structured-bulk-assembly.tex` describes: "Both factors are reserved
  simultaneously". Then `rho` must dominate the BIT stock's w-shaped
  coefficient. Conditionally on PR2084 that gives `rho = 8194` and
  `sigma <= 12556.14`, with guard 17. Sequential callees reuse restored rows,
  and PR2084's envelope is monotone in `e` and `w`, so the maximum over
  callees suffices. This composition is stated, not independently proved.
- Both branches sit far below the stage-1 sufficient guard `H_1 = 6,562,783`.
  So the open obligation is which reading the selected construction actually
  realizes, not headroom.

## Controls

Each of these must be rejected:

1. A flipped byte in a pinned input.
2. A ledger constant changed to 9908.
3. The family wire bits changed to 28.
4. `Sp(70,2)` in place of `Sp(72,2)`.
5. A prefix extra of 2048.
6. The eleven-stage BIT record.
7. A tampered `row_product_gap`.
8. 9909 used as a w-free `rho`.
9. The `S_leaf=1` premise removed.
10. A guard set below sigma.

## Not claimed

No supplier, κ, cutoff, frontier or selected-record change. Only native
stage 1 is checked. Neither reading is shown to be the one the selected
lowering realizes. The PR2084 coefficient is used as that package's
conditional result, not re-derived. The composition in reading (b) is a
stated argument, not a proved lemma. This is a finite source-bound audit,
not a supplier replay or a multiplication theorem. Overlap was checked
against open and closed PRs, package READMEs and Discussion titles; I didn't
search Discussion bodies.

## Open next questions

The structured versions are in [TASK.json](TASK.json).

1. **Which reading holds?** Inside selected m=73 nodes, is each BIT callee a
   completed call, or does the parent reserve its factor? This decides
   between `rho = 0` and `rho >= sigma_BIT`. First step: classify the
   adapter and peeled-atom call sites in the PR1094 source manifest. Blocked
   by: no pinned sentence names the reservation mode for selected m=73
   adapters.
2. **All fourteen stages.** Repeat the guard comparison for native stages
   2–7 and the conservative branch, using each stage's own `s` and headroom.
   This is bounded arithmetic once question 1 is settled.
3. **Is the external ledger still source-bound?** The term 9909 was derived
   for a fixed-wire historical family. If the selected BIT digit tower had to
   sit in the external reserve, that term would not be bound to the selected
   producer. First step: trace where the selected assembler routes PR589's
   q-adic selector stock.

## Credit

- Aaron Wang (#3113, `selected-stock-envelope-m73`) bound `B = 2642` and
  stated the missing `A, B, rho` lemma.
- Wentao Li (#3421, `selected-stock-shape-a-zero`) proved `A = 0`.
- Sricharan Vagvala (#2105, `selected-coarse-depth-stock`) supplied the
  `43/26` depth rate, the composition formula and the conditional
  `S_leaf = 1` sentence.
- Adam Gall (PR2084, `selected-bit-parent-reserve`) supplied the conditional
  BIT coefficient 8194, its completed-leaf hypothesis and the BIT-side reading
  of the 18355 formula.
- Josie Elliston (PR1965) and ToikY (`selected-bootstrap-stock-audit`)
  supplied the stage receipt and guard.
- Jeremy Kothe (PR1087) and Rohan Arun (PR1094) supplied the selected
  assembler and invoice. The partial-gauge, three-stage, paired-cube and
  structured-bulk assembly notes keep their original attribution.

Prepared by Mainzu, with substantial Claude Code (Anthropic) assistance. No
independent human review is claimed. Apache-2.0.
