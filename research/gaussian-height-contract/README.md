# Incoming-height repair for the mixed-provider Gaussian caller

I identify an omitted incoming-height term in PR4100's literal common-grid
allocation and give an exact constant-vector witness. I also derive an
explicit conditional reserve from the four mixed providers' eight emitted
programs, including corrections, dual-center flushes, cleanup and the
complete bridge multiplicity.

For root input height \(t_0\), I replace the stated fractional/integer
allocation by \(P+t_0+Bh\) and \(t_0+Bh+2\) bits. I prove
\(A(h)\le Bh\) by strong induction under the stated native endpoint
contracts, and reserve \((B+4)h\) for the Gaussian caller's raw-H
conversion and restoration. The caller can retain \(O(p)\) words if
it establishes \(t_0=o(p)\) and \(h=O(p^\beta)\), \(\beta<1\).
I do not exhibit a failing Gaussian execution or reject the claimed exponent.

In [PROOF.md](PROOF.md), I distinguish the literal supplier-contract
omission from the remaining Gaussian entrance-height obligation.
I credit the earlier generic prefix, divisibility and shift analysis;
my new scope binds the actual mixed programs and caller.

## Evidence

I regenerated all eight programs through the authenticated emitter and
matched their complete retained digests. Before emission I reconstructed
the canonical construction fields from all four original words.
I obtained maximum scalar-height charge 30,349, maximum scalar shift 3,
and 725,760 bridge ADDs per cover. With the retained rank mass,
\[
 S=23{,}431{,}680\Gamma,\quad E=99{,}056{,}520\Gamma+73,\quad
 B=\max(2,\lceil(S+E)/25\rceil).
\]
I use a conservative sum, without dividing height by the time recurrence's
payload factor. The resulting constant has 2,650 bits; I claim an
asymptotic existence bound, not a useful numerical precision constant.

The exact finite controls cover 4,394 scalar ADD cases using all 26 emitted
coefficients, 338 C/inverse-C cases, 54 incoming-height witnesses through
six dimensions, H0/raw-H identities and shift boundaries. I reject source
corruption, omitted cleanup and an altered emitted scalar direction.
The finite checks accompany the quantified argument; I do not extrapolate
that argument from them.

I preserve the native endpoint, complete free-algebra, hosting/stock and
Gaussian error premises. I have not run the native engine, Lean, a complete
Gaussian trace or a multiplication recovery test for this audit.
Author checks and substantial AI assistance do not constitute independent
human or formal-kernel acceptance.

## Reproduce

From the repository root, using standard-library Python 3.12:

```sh
python3.12 scripts/research_package.py --package research/gaussian-height-contract
```

The two registered commands compare the complete [RESULT.json](RESULT.json)
under ordinary and optimized audit interpreters. I preserve assertions in
the authenticated source adapters. Default replay writes no artifacts.
For receipt generation, `verify.py --emit NEW_PATH` refuses overwrite.
The source manifest binds 32 live inputs and two historical provenance files.

## Open next questions

1. Bind each actual Gaussian raw-H entrance to its base grid and a uniform
   \(t_*(p)=o(p)\), including denominator growth and rounding sites. Begin
   with `GAUSSIAN.md:120–126` and the dense interior call sites. The complete
   numerical circuit specification remains a prerequisite.
2. Check the lifted native endpoints and ordinary/outer admission for the
   four-provider dispatch. Begin with the complete original-word,
   canonical, emitted and recipe correspondence. This arithmetic audit
   retains those endpoint and hosting obligations.

I record the assignment and source pins in [TASK.json](TASK.json) and
[SOURCES.json](SOURCES.json). I coordinate in
[Discussion4175](https://github.com/CrocSwap/integer-mult-bounds/discussions/4175).

## Attribution

Jose Manuel (`jmbarrancoml`), with substantial OpenAI Codex assistance,
including source-analysis agents. Apache-2.0.

I credit Cinna Davis for PR4100/4088 and the borrowing/provider construction;
AAAmirinu for the earlier PR2287 primitive-prefix and shift audit; Gareth
Davidson for earlier Horner/prefix analysis; and the retained native
lineage, including icekylinx, DreamingOfClouds, Tekalign, Ali Romman and
Charles Bethin. I use the unmodified predecessor emitter and transport
construction prefix through source adapters. The original authors retain
their source notices, including
`staged544-mixed-fourth-entry/NOTICE.md` and
`native/NATIVE-LINEAGE-NOTICE`. I claim no new selected bound.
