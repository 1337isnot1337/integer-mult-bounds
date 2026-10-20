# Rational FFT circuits on fixed Hadamard stages

I connect PR4205's actual rational FFT and stored adjoint to the retained
six-H/seven-diagonal words and Beneš routing. I preserve the source stage
counts, complete inactive pairs and account for normalization from raw
Hadamard $H$ to $H_0=H/2$. I execute the resulting arithmetic with
rounded diagonal coefficients and rounding after each primitive stage.

The old `gateword('fft',w)` produces $H\operatorname{diag}(1,w)$.
Our unitary rational butterfly is instead

\[
\begin{pmatrix}a&bw\\b&-aw\end{pmatrix},\qquad
a^2+b^2=|w|^2=1.
\]

I bind it through the existing nonzero-shear helper without increasing
the six-H word count. I lower the original stored adjoint separately;
I do not identify it with the inverse of a quantized expanded word.

For a dyadic field of size $N$, arbitrary ordered active FFT wires,
Euclidean input bound $R\ge1$, target $2^{-t}$ and incoming grid
$F_0$, I give an explicit allocation with online widths

\[
O(F_0+t+\log N+\log R).
\]

I prove an exact prefix/inverse-prefix bound $K=2^{14}$ independent
of the number of completed FFT layers. I use it to pay coefficient
perturbations and all data-rounding sites, including inactive words.
Under the retained certified phase contract, I obtain error below
$3\cdot2^{-t}/4$ against the normalized DFT or its adjoint.
[PROOF.md](PROOF.md) states the domain, counts, allocation, word widths
and a separate allowance for a future physical native-call error.

## Source and scope

I start from canonical main
`12fa8c5c844be21bfefb38a19503fbd867a11244`, priority 7.
I retain the producer at PR4205 head
`78c72e563173f3822fcb4efed9ceeccf05630258` unchanged, with
[original provenance](vendor/PROVENANCE.json). I pin its local archive
at `e417b66e1106da6c44088a1aa63105fd776c9949` for exported source history.
[SOURCES.json](SOURCES.json) binds the actual input bytes.

I extract nine unchanged functions from `check_tensor_compiler.py`,
substitute exact scalar arithmetic for the needed SymPy scalar operations,
and retain source assertions under optimized Python. I preserve oriented
wire ownership, the complete matching, routing direction and distinct
rounding sites. I authenticate input files before parsing or executing them.

I execute mathematical $H_0$ arithmetic, followed by the declared grid
rounding. I do not invoke a physical T74 supplier or certify full-stream
tensor admission, coefficient delivery, tape movement or the outer theorem.
The rounded forward and adjoint programs generally are not exact inverses.

## Verification

Use CPython 3.12 and its standard library:

```sh
python3.12 -B scripts/research_package.py --package research/rational-fft-fixed-h
```

I declare normal and optimized replays, each with a 120-second limit.
Thirteen cases cover fields through 64 wires, nontrivial wire order,
partial active fields, both directions, a large input radius, singleton
programs and a 512-bit incoming spectator. I execute 2,525 primitive
stages and 73,104 complex roundings. I compare complete exact native and
retained FFT outputs, complete basis matrices through field size eight,
and direct Fourier interval formulas.

I also check sixteen standalone butterfly words and all 1,456 nonempty
contiguous segments and their inverses. Twenty-three controls cover
normalization, orientation, idle words, source assertions, precision,
source corruption and typed receipts. The inactive-word fixture has
nonzero spectator error, which I include in the total rounding budget.

The complete [RESULT.json](RESULT.json) digest is
`d735321b0bf6457ad884779b5854ff201e18f79e4bf8df8b32da6f91477b4c9d`.
The Fourier formula shares the declared phase backend; I claim no
independent transcendental implementation. I observe mathematical
component temporaries, not every internal `Fraction` operation.
The finite checks do not establish the quantified proof by themselves.

## Overlap and attribution

I refreshed 359 open PR bodies and 3,071 Discussion records with complete
pagination, inspected all fourteen phrase matches and checked eight newer
PR records and 5/900 hub comments. I found our PR4178 tensor precision
protocol and PR4205 producer as relevant predecessors. The other named
matches concern different matrix or connector problems. Broader closed
history, arbitrary diffs and unpublished work remain outside the search.
[Discussion4202](https://github.com/CrocSwap/integer-mult-bounds/discussions/4202)
records the scoped claim and obligation ledger.

I considered the global core/halo connection as an alternative. The
retained rad20 reports already prove the row-Neumann locality lemma;
that next task needs current-reference and output-ownership binding.
I chose this connection to resolve the rational gate's mismatch with
the existing fixed-H compiler while preserving its stage count.

I credit Vlado Vojdanovski for the source words, Beneš routing and FFT
schedule; Chafik Boukhalfa/PR628 for certified rational phases; and
Cinna Davis for the later Gaussian caller. I retain the classical
Fourier, LDU and perturbation lineage. Our earlier PR4178 supplies a
distinct rounded tensor-scan protocol with its own caller hypotheses.
I add the rational gate binding and complete fixed-grid FFT contract.

Jose Manuel (`jmbarrancoml`), with substantial OpenAI Codex assistance in
mathematics, source analysis, implementation and writing. Internal agents
belong to the author process. I claim no independent human or proof-kernel
acceptance, worldwide mathematical priority or selected-frontier change.
Apache-2.0.

## Open next questions

- Connect these coefficient bounds and stage signatures to the actual
  physical tensor caller, including its unit-disk, complete-record,
  normalization and spectator requirements.
- Bind the completed rounded Gaussian core to global halo ownership and
  carry the analytic-reference error through the outer computation.

I keep the exact next steps and remaining costs in [TASK.json](TASK.json).
