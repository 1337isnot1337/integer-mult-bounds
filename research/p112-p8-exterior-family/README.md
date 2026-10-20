# A P8 exterior family cannot improve this three-mark invoice

For the fixed P112 target pairs `{0,67}`, `{7,64}`, `{1,75}`, the prescribed
six-query P8-extension family has **full-group invoice at least 18** whenever
the rational exterior direction h satisfies `rank[c0,c1,c2,h]=4`. Equality
is attained within the family. The three original canonical terms also cost 18. This family cannot contribute a saving toward
the decoder-cost target of 296.

The queries are `h`, `c1+c2+2h`, `c0+c2+h`, `c0+c1+h`, `2c0+c1+c2`, and `c0+h`.
Readers are arbitrary rational vectors and the two copies of each target may
use different formulas. The theorem allows h anywhere on the 112 scalar
ports. It fixes the six queries, the marking, the physical embedding and the
exact canonical endpoint. Extra readers arising when the coordinate rank is
only three are outside the theorem.

[PROOF.md](PROOF.md) reduces all rational h to 324 complete source zero patterns
while retaining the reader equations forced by rank four. Exact minimal-reader
recovery gives 32,400 support choices per pattern. The primary verifier solves
160 distinct tariff tables using valid monotone lower bounds; the independent
checker exhausts all 10,497,600 cells without pruning. Both reconstruct every
physical tariff and obtain the same digest of all 324 exact minima.

| Result | Exact value |
|---|---:|
| Original exterior `h=c0_left-c0_right` | 21 |
| Support-dominating exterior `h=-c0_right` | 18 |
| Minimum over the complete rank-four exterior family | 18 |
| Rank-four finite source strata attaining 18 | 6 |

An equality witness is `c0=q5-q0`, `c1=q3-q5`, `c2=q2-q5`. Its complete-group
term charges are `[3,0,6,6,0,3]`. The two dense P8-specific queries are unused
in this witness. The selected multiplication bound is unchanged; no global
334 floor, new native schedule, or complete supplier is claimed.

## Reproduce

From the repository root, using Python 3.12 or later and its standard library:

```sh
python3 -I -O -Werror -B research/p112-p8-exterior-family/verify.py
python3 -I -O -Werror -B research/p112-p8-exterior-family/independent_check.py
python3 -B scripts/research_package.py --package research/p112-p8-exterior-family
```

The standalone checks use only the two declared, authenticated scientific
inputs in [SOURCES.json](SOURCES.json). They import no producer/scratch code,
need no network or Git metadata, and compare compact committed receipts
without writing files. `--write-receipt` explicitly regenerates a receipt.
Each replay takes a few seconds; registered timeouts are 30 seconds each.

The receipts include complete coverage counts, the canonical digest of all
source-stratum minima, and attaining fixtures. All rows are regenerated before
checking the digest. Exact controls retain the missing half-root cancellation,
source deletion with rank collapse, the extra rank-three reader freedom,
and underpriced/corrupted reader rejection. The independent checker also
checks both fixed witnesses on all 112 squared endpoint entries.

The rational-family reduction is a written mathematical proof reviewed by
separate AI agents. The finite coverage and optimization steps are exact
computations, not a proof-assistant formalization or independent human review.

## Provenance and credit

Base: canonical main `12fa8c5c844be21bfefb38a19503fbd867a11244`, priority
revision 7. The donor assigned the continuing rational-decoder goal;
[TASK.json](TASK.json) records the changed scope from the retained card.
The parent investigation refreshes upstream and checks public overlap;
this package makes no novelty claim from an absence of matches.

Choe, Oxley, Sokal and Wagner give the P8 representation in
[Homogeneous Multivariate Polynomials with the Half-Plane Property](https://www.math.lsu.edu/~oxley/ycjoasdw.pdf),
Example 11.8, equation (11.6), and Appendix A.4, equation (A.1). We use its literal
rational entries, mark three basis columns, and append the specified point
`c0+h`. The classical representation and its characteristic obstruction are
not new findings here. The earlier five-query P8 restriction is already covered
by [p112-triad-matroid-boundary](../p112-triad-matroid-boundary/README.md).
This package closes the exterior choices for this one six-query extension.

The canonical targets and original invoice come from flyingviper's
[p112-rational-decoder-gate](../p112-rational-decoder-gate/README.md), retaining
Cinna Davis's P112 cover lineage, Sagar Thakrar's scalar-mask/full-group audits,
Adam Gall's mask obstruction, ctoth and Philippe Van Velzen's endpoint/pricing
framework, and Hanson Sun's projection work. Physical labels retain the
adaptive-kernel-demotion source attribution. Frozen predecessor files are
unchanged. Prepared by flyingviper with substantial OpenAI Codex assistance
and separate AI-agent mathematical and implementation checks. Apache-2.0.

## Open next questions

- Can the genuinely rank-three exterior cases be covered by a separate reader
  reduction or an existing transfer theorem? Their extra reader freedom is a
  precise gap in this result. Start from the effective three-row query matrix;
  the inherited four-coordinate reader constraints cannot establish that claim.
- Can a different, structurally chosen added point produce a local saving?
  This family is closed, so another round needs a reason its source/reader
  interaction changes the invoice. Derive its complete affine zero patterns
  and reader demands before pricing one justified marking. No alternate point
  or placement is established as promising by this package.

Neither question supplies the remaining global saving budget, compatible
placement count, native routing/restoration, or all-size multiplication proof.
