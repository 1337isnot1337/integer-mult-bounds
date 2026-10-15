# Clean six-tape multiplication and eight checked applications

One fixed finite six-tape machine multiplies every pair `a,b < 2^n`, including
width zero, and genuinely halts in at most **280n² + 278n + 68** physical
transitions. The input is two separately supplied padded LSB stack words at
head zero. The output is the literal padded `2n`-bit MSB product at origin zero
on `sumReverse`; all other five tapes are globally blank. Actual terminal heads
are specified, with no free return to origin. The operands are consumed.

`IntegerMultiplicationCompilerApplications.clean_product_tight` proves this
bound for `IntegerMultiplicationEngine.cleanMachine`. Its six setup phases take
exactly **40n + 30** physical transitions. The complete polynomial is an upper
bound, not an exact running time or an optimality claim. The earlier checked
`280n² + 322n + 122` theorem remains available.

The release adds eight reusable applications to the existing toolkit:

1. Explicit closed tape windows suffice for an actual completed run; every
   arbitrary dirty exterior cell is preserved literally.
2. Independent origins relocate both entire tapes and heads of the same actual
   multiplication table. This changes supplied coordinates, not execution cost.
3. Exact six-phase setup invoices tighten the complete clean multiplication bound.
4. Any fixed injective alphabet encoding compiles the finite table with unchanged
   exact transition count and genuine halt on encoded configurations.
5. `max a.size b.size` is the least common operand width; input cells equal
   literal `Nat.bits` followed by false padding.
6. Actual multiplication specializes to `ZMod (2^n)`, including signed integer
   residue labels. Output is the full exact double-width natural product.
7. Fixed tape permutations fixing designated operands preserve their head/cell
   endpoints as adapters; this does not say the multiplication retains operands.
8. A statically permuted multiplication table returns output on `accumulator`
   with literally unchanged input ABI, same time bound and genuine halt.

The window, width/residue and accumulator application statements retain the
conservative `280n² + 322n + 122` bound. The tighter theorem and encoded-alphabet
specialization use `280n² + 278n + 68`.

All imports are pinned Mathlib/Lean or bundled public modules. The prior compiler,
caller, finite tape embedding, dirty-frame, marker lifecycle, serializer and
Problem1.8 arithmetic closure remain included. No personal project is required.
Literal input padding and signed residue labels are supplied input conventions;
there is no claimed paid parser, physical truncation pass or fast recursion.
This is an explicit quadratic machine result and changes no selected kappa.

## Verification

Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` are pinned.
From this directory:

```sh
python3 -I -B verify.py
python3 -I -B replay.py --out /absolute/new/check --cache-project /path/to/pinned/cache --lean /path/to/lean
```

`verify.py` checks exact immutable sources, operational controls and rejection of
corrupted reports; it does not run Lean. `replay.py` rebuilds all 74 bundled
modules in a fresh external output directory and audits every owned declaration,
including private/global/generated helpers. It checks transitive axioms, admits
only `propext`, `Classical.choice`, `Quot.sound`, and rejects package axioms even
when unused. Real Lean negative fixtures test the audit boundaries.
The dependency cache supplies pinned Mathlib/Lean binaries; those external
libraries are not independently rebuilt by this package. No prebuilt toolkit
artifact can satisfy the fresh package build. Hosted CI and human review are
separate from local verification. `VALIDATION.json` binds the checked sources;
`MANIFEST.json` binds all shipped files. The final distribution receipt is kept
outside the package to avoid a self-referential manifest.

## Reuse and overlap

`API.md`, `PROOF.md`, `PORTING.json`, `REUSE.json` and `NOTICE.md` record contracts,
assembly and attribution. `FRONTIER.md` and `reviews/` compare actual relevant
sources after refreshing main and recent PR metadata. Prior alphabet transport,
physical padding, output adapters and multiplication proofs are substantial
related work. No first-use, exhaustive novelty or improved-exponent claim is made.
Substantial OpenAI Codex assistance included one root and three parallel agents;
no Jev service was used.

## Open next questions

- Implement a paid serialized/signed input parser into this exact two-stack ABI.
  Start with explicit cell/head contracts; literal initial padding is not a parser.
- Adapt the clean arithmetic endpoint to the marked arbitrary-bank caller ABI.
  Alphabet transport alone does not supply physical marking, routing or buffer placement.
- Assemble charged dynamic recursion and routing for a fast multiplier. The fixed
  quadratic table and its adapters provide concrete leaves, not that algorithm.
