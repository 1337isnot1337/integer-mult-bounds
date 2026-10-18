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
shows that those terms cannot serve as `rho`. It then reads the merged
selected complex layer to settle how its callees get their stock: the layer's
only row stock is its own divisor, so `S_leaf = 1` and `rho = 0`. This holds
conditionally on that chain. All fourteen recorded stage guards pass either
way.

```sh
python3 -I -B research/selected-stock-rho-ledger/verify.py
```

Expected:

```text
PASS_SELECTED_STOCK_RHO_LEDGER B=2642 ledger=16469 9909=367*27 252=9*28 1024=2*512 bit_row=18355=8194+9909+252 implicit_rho_3113=11185 rho_a=0 sigma_a<=4362.14 rho_b=8194 sigma_b<=12556.14 L_bits=2642 S_leaf=1 guard=16,17<=6562783 stages=14 H_min=6562783 lean_row=6308 qadic_bit_row>=655356>20161 controls=16 checks=62
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
6. **The selected complex layer's only row stock is its own divisor.** Jose
   Manuel's PR2287 (`selected-complex-layer-closure/PROOF.md`) is the written
   all-size m=73 layer. PR3385 implements it physically; that archive has had
   intake checks only, with no scientific verifier run. PR2287 sets
   `W = 14336` and `L = W·|O(73,2)|`. Its only row stock is `L^D0(d)`, taken
   from a prefix of `q0 = ceil(log2 L)·D0(d)` chunks. A child receives `U`
   with `L^D0(e') | U`, and "a completed child restores its own row labels".
   - **Peeled axes and stopped leaves.** The layer processes the
     `e mod 73` leftmost axes individually, and "the leaves require only the
     elementary C kernel". These calls have no callee and need no stock.
   - **Compact fields.** The root also reserves `qF + qB` chunks for three
     H-bit compact fields (`H = dG`, `G = 4⌈log2 p⌉ + 6`). They may start
     dirty, and the adapters restore them. "No compact-field bit enters this
     selector", so they are not row stock and lie outside A, B and `rho`.
   - **Ordinary/BIT calls.** The only ones sit inside PR2250's compact
     adapters, which run them on `(f-1)G`-bit pieces of the compact fields.
     PR2287 says its bound uses "an ordinary binary chunk interchange …
     PR2234 proposes that contract". PR2250 grants that callee "no external
     row stock or ancestor access". PR3385 binds it to B1/C0 (L17–19).
   - **The callee's own stock.** PR2234 §8 (realized physically as B1 in
     PR2899) chooses its own stock `S=K(w)^D(e)` with `log_q K <= 4097w`. It
     borrows `k=ceil(log_q S)` leading digits of its own chunk, so inside the
     compact-field piece it was given. Below the fitted range it falls back to
     elementary interchanges. With halving
     depth 2 that stock is exactly PR2084's `8194` coefficient.
   - **The divisor matches B.** `ceil(log2(14336·Γ)) = 2642`, the same as
     #3113's B. The divisor is w-free, consistent with #3421's `A = 0`.

## What follows for `rho`

- #3113's conditional readings sigma ≈ 16469 or 15555 put the external-ledger
  constants `9909 + 252 + 1024 = 11185` into the borrowed-stock envelope. The
  verifier reproduces `15555 − ⌈43·2642/26⌉ = 11185`. Those constants are
  w-free degrees of an external reserve, and 9909 belongs to a historical
  family. So the ledger does not supply a source-bound `rho`. The control
  `ledger_constant_as_rho` rejects 9909 as a w-free bound on the w-shaped BIT
  term, because `9909 < 8194·w` for every `w >= 2`.
- **Reading (a), completed callees, is what the selected layer does.** Every
  callee inside an m=73 node is either elementary or a completed ordinary call
  that borrows internally and restores (fact 6). So `S_leaf = 1`, as
  `selected-coarse-depth-stock/PROOF.md` already allowed conditionally. Then
  `rho = 0` and, at native stage 1,
  `sigma <= (43/26)(1-s)·2642 ≈ 4362.14`, with `ceil(log2(8·sigma)) = 16`.
- **Reading (b), the parent reserving the BIT factor, is kept only as a
  counterfactual.** An earlier version cited `structured-bulk-assembly.tex`'s
  "Both factors are reserved simultaneously" for it. That sentence concerns
  fixed-wire *external* factors (`W_b,W_c<2^{43}`, bounded in `p^{108000}`),
  the kind the selected ledger pays as 9909. It is not the w-shaped BIT
  stock. If a parent did reserve that stock, `rho` would have to dominate
  PR2084's 8194. That gives `sigma <= 12556.14` with guard 17, which still
  passes.
- **All fourteen recorded stages pass both values.** That is native stages
  1–7 and conservative stages 1–7, each with its branch's own `s` and its own
  headroom. For each stage record, the verifier re-derives
  `H_j = floor(L_j·gap_j/2) − 4` from the recorded `L_j` and gap. It checks
  that the gap is the least of the four recorded gaps, that the stock gap is
  `1 − s`, and PR1965's premises (`L ≥ 2`, `L·gap² ≥ 36`,
  `0 < gap ≤ 1 − s`). The tightest stage is stage 1
  in both branches, at `H = 6,562,783`. The guards are only 16 and 17.

## What the 9909 and 252 slots pay for

The selected certificate charges the complex row
`2·2642 + 9909 + 252 + 1024 = 16469`. Separately, it charges the BIT row
`8194 + 9909 + 252 = 18355`. Both are checked against one cap, 20161
(`assemble.py` L159, L173, L204).

- **No selected family has the 9909 or 252 parameters.** The selected BIT
  is halving depth 2 with `64²+1` bits, giving 8194. The selected complex
  layer's peeled axes and leaves are elementary C kernels (fact 6). The pairs
  `(367,27)` and `(9,28)` are historical families.
- **In the selected layer, the two slots pay for nothing.** Its only row
  stock is `L^D0(d)`, and its BIT callee borrows internally. Without the
  slots, the complex row is `2·2642 + 1024 = 6308`, so they are inherited
  slack. Dropping them would not change κ: the physical row only has to stay
  below the retained 20161, and only that retained cap enters the outer
  assembly, through the strict degree-gap constraint.
- **The BIT's 8194 here is a binary model.** The certificate's 8194 is
  PR510's model of the BIT, with `m²+1` bits per level. In that model, 8194
  would fit in the 9909 slot (`6308 + 8194 + 252 = 14754 < 20161`), so the
  cap check alone decides nothing about how the BIT gets its stock.
- **The BIT the adapters call is q-adic, and its stock cannot fit the
  cap.** The adapters call PR2234's BIT, which has `q > 2^80`. Its level
  divisor has at least `4096·80 − 2` bits, because
  `|GL_64(F_q)| ≥ q^4096/2`. In the certificate's own row convention
  (halving depth × bits per level), that gives a row term of at least
  `2·(4096·80 − 2) = 655,356` at `w = 1`. That is over 32 times the 20161
  cap, and it grows with `w`. So the row ledger cannot be holding that
  stock. It is borrowed inside the call, as fact 6 says, and this is the
  same w-shape point as fact 5 and the `ledger_constant_as_rho` control.

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
11. PR2250's adapter callee given external row stock.
12. PR2234's per-level stock coefficient changed to 4098.
13. PR2287's leaves given a BIT reserve.
14. PR2287's divisor family count doubled.
15. A tampered headroom on the last conservative stage.
16. PR2234's prime bound lowered to `q > 2^2`.

## Not claimed

- No supplier, κ, cutoff, frontier or selected-record change.
- The stage records are the `selected-bootstrap-stock-audit` receipt. Their
  cutoffs and gaps are taken as recorded, not recomputed from the selected
  savings.
- `rho = 0` rests on PR2287, PR2250, PR2234 and PR2899. The PR ledger
  (`docs/research/pr-ledger.json`) records all four as `incorporated` after
  a scoped review of written constructions with passing replays. None is an
  executed GL64 or O(73,2) machine or a formal proof. PR2234 itself says
  "Independent mathematical review remains necessary" (PROOF.md L432).
- PR3385, the physical controller, is only `partially_reviewed`: source-only
  archival intake with no scientific verifier run. So are #3113 (B) and
  #3421 (`A = 0`).
- No physical O(73,2)/GL64 payload has been run by those sources or by this
  package.
- The PR2084 coefficient is used as that package's conditional result, not
  re-derived.
- This is a finite source-bound audit, not a supplier replay or a
  multiplication theorem.
- Overlap covered open and closed PRs and package READMEs. It also covered
  Discussion search for the terms in TASK.json, Discussions #2238 and #2319
  in full, and the latest 100 comments of #1166.

## Open next questions

The structured versions are in [TASK.json](TASK.json). The earlier first
question, which reading the selected layer realizes, is answered by fact 6.
The earlier second question, covering all fourteen stages, is answered in
"What follows for `rho`". The earlier third question, about the external
ledger, is answered in "What the 9909 and 252 slots pay for".

1. **A source-bound replay of PR3385.** `rho = 0` uses written constructions
   that have had a scoped review: PR2287's layer and the PR2234/PR2899 B1
   callee. PR3385 is the physical controller that binds the compact
   adapters to B1/C0, and its ledger entry still asks for "independent
   scientific review and source-bound replay". First step: run its
   registered replay (Python 3.12). Then check B1's borrowing fit `k < e/2`
   at the compact-field widths where PR3385's adapters call it.
2. **Does an H3 envelope apply to the complex layer at all?** PR2287 takes
   its rows from its own prefix of `q0` chunks, not from bootstrap borrowing.
   The bootstrap's stopped producer is the PR589 BIT
   (`docs/research/selected-bootstrap-scope-map.md`). If the complex layer
   never enters a bootstrap fit, the m=73 sigma is a consistency bound
   rather than an obligation. If an H3 fit did apply, it would also have to
   count the three H-bit compact fields, about `3dG/K` axes (PR3385
   L177–178). That amount does not have the `sigma·w·(1+log2 e)` shape.
   First step: find any selected composition that bootstraps the complex
   layer.
3. **The 1024 prefix term.** It is bound here only to the invoice
   (`2·512`). This package does not trace which construction step uses it.

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
- Jose Manuel supplied the selected complex layer and its physical
  controller (PR2287, PR3385), the compact adapters (PR2250, which retains
  Douglas Colkitt's compact-control method), the selected BIT interchange
  (PR2234) and the physical ordinary wrapper B1 (PR2899, around Nick
  Petalas's PR2808 wrapper). Fact 6 reads them; it adds no construction.
- Jeremy Kothe (PR1087) and Rohan Arun (PR1094) supplied the selected
  assembler and invoice. The partial-gauge, three-stage, paired-cube and
  structured-bulk assembly notes keep their original attribution.

Prepared by Mainzu, with substantial Claude Code (Anthropic) assistance. No
independent human review is claimed. Apache-2.0.
