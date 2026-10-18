# complex-halving-degree-invoice: the largest admissible halving degree for the selected complex invoice

**Scoped finite statement, conditional on inherited hypotheses; an optimistic opening only.
No new κ, no supplier, no frontier change.**

## Statement

Every complex ceiling screen fixes the idle child rank at R ≤ 51. That cap comes from the
halving guard 73^t > 2R^t at t = 2. At t = 2 the selected #1094 finite invoice charges
the row coefficient 2·2642 + 9909 + 252 + 1024 = 16469, where S = 2642 is its stock bits.
Hypothesis H1 in [PROOF.md](PROOF.md) is the lineage's degree-t ledger. Under it, the
charge at degree t is

Row(t, S) = t·S + 9909 + 252 + prefix(t).

Under hypotheses H1–H4, the degree t is limited only by this row contract:

| Row contract | prefix(t) | t_max | Largest admissible R | Rank-56 idle bin | R = 72 |
|---|---|---|---|---|---|
| A: retained 20161 is binding (Row < 20161) | 1024 (fixed) | **3** (row 19111) | **57** | admissible | no |
| A | 512·t | **3** (row 19623) | **57** | admissible | no |
| B: only the bridge binds (Row < 490196) | 1024 | **181** (row 489387) | **72** | admissible | yes (t ≥ 51) |
| B | 512·t | **152** (row 489569) | **72** | admissible | yes |

Reading B keeps the bridge reserve 10^6 and the factor 51/25 fixed and re-chooses the
retained coefficient up to ⌊(25·10^6 − 1)/51⌋ = 490196. At that cap the bridge gap is
4/25 > 0.

A child rank R is admissible exactly when t_min(R) ≤ t_max, where t_min(R) is the least
t with 73^t > 2R^t. Examples: t_min(51) = 2, t_min(57) = 3, t_min(58) = 4, t_min(71) = 25,
t_min(72) = 51. R = 73 is never admissible. For general stock, (R, S) is admissible
exactly when S ≤ ⌊(cap − 1 − 10161 − prefix(t))/t⌋ with t = t_min(R); RESULT.json
tabulates this for R ∈ {48, 51, 52, 56, 57, 58, 64, 68, 71, 72}.

**Ideal ceilings.** Colkitt's packing relaxation of the selected local word, with idle
ranks allowed up to R, gives the values below. The κ column uses Colkitt's conversion,
which holds while the complex side binds. For R ≥ 71 the bit side may bind instead.

| R | t_min | a_ceiling (certified to a 10^−15 grid cell) | κ ≤ a/(1+a) | gain over R = 51 |
|---|---|---|---|---|
| 51 | 2 | 0.001690054109089 (published value, reproduced) | 0.001687202645325402 | — |
| 57 | 3 | 0.001704851516268 | 0.001701949944324806 | +0.875558% |
| 72 | 51 | 0.001736778936705 | 0.001733767765368969 | +2.76469% |

The full table for R = 51..72 is in RESULT.json and increases strictly with R. **R = 71
(t_min = 25) is the least rank whose ceiling cell lies above the selected bit endpoint
0.001733427039589844234749.** The ceiling at R = 70 is 0.001732866531911.

What this decides:

- Under reading A (and H1–H4), R = 51 is not forced by the invoice: degree 3 is admissible. But the
  whole depth lever is +0.875558% (R ≤ 57). The complex ceiling stays below the current
  bit endpoint, so in this relaxation the complex supplier still binds.
- Under reading B (or C, below), R = 72 is admissible. The ideal lever is +2.76469%, and
  for R ≥ 71 this relaxation no longer forces the complex side to bind.
- In both readings the lever is small next to the local rank-shape lever priced in
  #3701 and #3811.

## What is new compared with predecessors

- **philippeVV**, Discussion #2278 ([comment](https://github.com/CrocSwap/integer-mult-bounds/discussions/2278#discussioncomment-18960261),
  2026-10-15, local-only and unreviewed), stated that the guard is a convention, that
  "the retained bridge degree 10^6 already admits t ≤ 181", and that the effect on this
  word's ceiling is "≤ +2.8%". This package:
  - binds every term of the t = 2 ledger, and the scaling of the stock term with t, to
    pinned source text and to the selected invoice bytes. How the prefix scales with t
    stays open (H2);
  - separates reading A (t_max = 3) from reading B;
  - adds the prefix-scaling case (152 instead of 181);
  - gives the exact (R, S) region;
  - certifies the ceilings at every R = 51..72 by two methods. This confirms his
    figure: +2.76469% at R = 72, under reading B only.
  - finds the bit-endpoint crossing at R = 71.
- **Gonzalo-Mier**, `research/kappa010-rank-cap-floor`, open question 3, asks whether
  deeper guard depths fit the row invoice. For the complex invoice, every depth
  4 ≤ t ≤ 152 fits under B, including the depth 17 that their complex rank-70 row needs.
  No depth above 3 fits under A. The bit invoice is not evaluated here.
- **Douglas Colkitt**, `research/complex-local-word-ceiling`: the relaxation and its
  rational enclosure primitives are reused unmodified, as a cross-check. The guard check
  is not called for R > 51.
- **petalas**, #3701/#3729/#3754/#3805/#3811: ceilings and integer packings for caps up
  to the guard cap 51. This package extends only the idle cap past 51, and does not
  re-tabulate their cap tables.

## Reproduce

From the repository root, with the standard library only. This was tested locally with
Python 3.14. `VERIFY.json` targets 3.12, which was not available locally, so the
runner's 3.12 replay was not run here.

```sh
python3 -I -B research/complex-halving-degree-invoice/verify.py
```

Expected output, in under 10 s:

```
PASS_COMPLEX_HALVING_DEGREE_INVOICE_SCOPED {'A_retained/fixed': 3, 'A_retained/per_level': 3, 'B_bridge/fixed': 181, 'B_bridge/per_level': 152} {'51': '0.001690054109089', '57': '0.001704851516268', '72': '0.001736778936705'} 11 controls
```

The verifier recomputes everything and requires byte equality with
[RESULT.json](RESULT.json). `--write` regenerates the file. It checks:

1. 27 literal source bindings in the pinned assembler code and notes, plus the
   precedent arithmetic 4·2571 = 10284 and 24·2431 = 58344.
2. The selected invoice member SHA256. It recomputes S from physical roles × group(36),
   and the row, router, literal and C0 bit lengths from the invoice's own fields.
3. Guard thresholds for every R = 1..72, by integer power search and by the exact
   coarse recurrence n ↦ R·⌊n/73⌋ (two methods).
4. t_max for each reading and prefix, by direct scan, as an initial-segment property.
5. The (R, S) region.
6. The ceilings by the package's own decimal interval bisection, which uses correctly
   rounded ln/exp with one-ulp widening and directed rounding. At both bracket
   endpoints they are cross-checked against Colkitt's unmodified rational `child_cost`
   enclosures. At R = 51 the bracket must equal the unmodified `ceiling.ceiling()` and
   the published `RESULT.json`.

**Negative controls.** These 11 inputs run through the main check functions and must
fail; each did:

| Control | Why it fails |
|---|---|
| t = 4 under A, fixed prefix | row 21753 ≥ 20161 |
| t = 4 under A, 512·t prefix | row 22777 ≥ 20161 |
| R = 58 at t = 3 | guard 390224 > 389017 |
| R = 72 at t = 50 | guard fails |
| R = 73 at t = 200 | guard can never hold for R ≥ 73 |
| t = 182 under B, fixed prefix | row exceeds the bridge cap |
| t = 153 under B, 512·t prefix | row exceeds the bridge cap |
| bridge cap + 1 (490197) | degree gap not positive |
| `row_prefix_extra` set to 0 | invoice row identity fails |
| stock bits + 1 | invoice stock identity fails |
| physical roles doubled | invoice stock identity fails |

Three controls were run outside the verifier, and each fails as it should:

- running with `-O` exits non-zero, because the assertions are the checks;
- an unknown argument is rejected;
- a one-digit edit of RESULT.json fails the byte comparison.

## Scope, inherited assumptions and unresolved obligations

These hypotheses are inherited (see PROOF.md). They are evidenced from source but not
proved here:

- **H1.** The finite-cover transfer can be instantiated at degree t with ledger
  t·S + 10161 + prefix(t). The lineage's notes do this at t = 4 and t = 24 with the same
  9909 + 252. The degree-genericity of the written transfer proof behind this particular
  assembler is not re-proved.
- **H2.** The prefix is either fixed or 512·t; source does not settle which.
- **H3.** Whether the retained 20161 binds (reading A) or only the bridge binds
  (reading B). This is a contract question that this package does not decide.
  - There is a third reading, C, recorded but not used for any number: the reserve
    exponent is itself chosen per assembly. The pinned notes use 70000, 108000 and
    160000, and the selected invoice uses 10^6. Under C the row invoice gives no finite
    cap.
- **H4.** The other finite checks do not depend on t. The square in router and literal
  is the W² exchange count of a W-role permutation, and the degree-24 precedent keeps it.

The following costs are unknown, not zero:

- physical hosting of idle children of rank > 48 (#3805 leaves 49–51 open);
- stock and coarse-depth repricing for children of higher rank (#3113 records only the
  selected m = 73 envelope and its missing shape lemma; the coarse depth per halving
  grows like 1/log2(73/R));
- native admission;
- any change to the staged544 template.

The ceilings are relaxations: they bound what repacking this local word could reach,
and they are not achievable values. This package admits nothing and does not change the
selected frontier.

## Open next questions

1. **Does the retained row coefficient 20161 bind, or only the bridge (reading A versus
   B or C)?** If only the bridge binds, R up to 72 is open (+2.76469% ideal). If 20161
   binds, R ≤ 57 (+0.875558%). First step: have a maintainer or the lineage author say
   whether `retained_row_coefficient == 20161` is a contract of the transfer proof or a
   bookkeeping constant. Blocker: this is a contract decision, not a computation.
2. **Is `row_prefix_extra` fixed or proportional to t?** It changes t_max under B from
   181 to 152, but not the R = 72 conclusion. First step: trace `2*payload` to the
   PR582 plain-joint-prefix construction.
3. **Can idle children of rank 71 or 72 be hosted, and what does the coarse-depth stock
   cost at t_min = 25 or 51?** This is the first step at which the bit side could bind.
   First step: reprice the selected-coarse-depth-stock bill with the depth coefficient
   1/log2(73/R). Blocked by #3805 (physical hosting) and #3113 (shape lemma).
4. **Bit-side analogue.** Does the bit invoice (m = 64) admit the depths that the
   kappa010 bit rows need (t = 15 for rank 61)? First step: bind the bit row ledger the
   same way.

## Sources and credit

- Base commit `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority revision 6. Exact Git
  blobs and SHA256 values of every input are in [SOURCES.json](SOURCES.json).
- The selected invoice is the tar member above, SHA256 `212cf4ee3b16081bf66f300fa18b4070d25c17210c21c78c2967892c91870d12`.
- The ledger formula is in the finite-invoice assembler lineage vendored at
  `research/complex-571-hpem46c/code/` (reviewed archive; the selected record's source
  chain includes PR1087 by jeremykothe2).
- Precedents: `notes/paired-cube-assembly.tex`, `notes/three-stage-cover-assembly.tex`,
  `notes/three-stage-cover-rows.tex`, `notes/structured-bulk-assembly.tex`. DaysSky's
  closed PR375 is an earlier package with a halving degree above 2.
- Predecessors:
  - philippeVV: the halving-guard note in Discussion #2278.
  - Gonzalo-Mier: kappa010-rank-cap-floor, open question 3.
  - Sricharan Vagvala (@theon199): selected-coarse-depth-stock.
  - Douglas Colkitt: complex-local-word-ceiling, and the review that vendored the
    assembler.
  - navinor: #3113.
  - petalas: #3701/#3729/#3754/#3805/#3811.

No predecessor file was modified.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from Claude
(Anthropic, Claude Opus 5.5). Claude chose the method, wrote verify.py and drafted this
README and PROOF.md. No human has reviewed it independently. Apache-2.0.
