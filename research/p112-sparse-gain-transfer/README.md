# Two-port queries cannot beat the P112 full-group invoice

For the fixed P112 full-group mask, **every rational strict fit costs at least
334 if all source queries touch at most two scalar ports**. The same floor
holds if all reader rows touch at most two ports. There is no restriction on
the fit's rank, number of terms, query dependence, or equality of readers.
Only one factor family needs to satisfy the uniform sparsity condition.

The proof changes the rational query gains to a characteristic-two field and
recovers each actual reader within its old support. The new endpoint may
change permitted free entries, but preserves every diagonal and forbidden
zero. Every strict fit on this physical mask expands to I334, which yields
the invoice floor. See [PROOF.md](PROOF.md) and
[the independent proof audit](INDEPENDENT-PROOF.md).

This is a structural exclusion, not an unrestricted 334 floor or a new upper
bound. A decoder reaching 296 must have at least one query touching three or
more ports **and** at least one such reader; these need not be the same term.
Those conditions are necessary, not sufficient. The selected bound is unchanged.

## What the package establishes

| Result | Hypothesis | Conclusion |
|---|---|---|
| Strict-fit transfer | Every query has at most two literal ports; arbitrary rational strict fit | Same source supports and shrinking actual reader supports over a characteristic-two field; free endpoint entries may change; invoice at least 334. The transpose gives the reader-sparse result. |
| Common group gauge | One invertible within-group similarity makes either entire factor family two-sparse | Original complete-group invoice is unchanged, so the same floor applies. Independent per-term gauges are not allowed. |
| [Common recovery](COMMON-RECOVERY.md) | Literal two-port queries; disjoint indicator marks recoverable inside the intersection of their actual reader supports | Preserves the exact indicator endpoint, with unchanged source supports and shrinking reader supports. This extra premise is unnecessary for the main cost floor. |
| [Coefficient-space transfer](SCALAR-DEMAND-AND-BRIDGE.md) | Each query combines at most two complete canonical indicator columns | Preserves the exact canonical endpoint even with dependent queries and arbitrary copy-asymmetric readers; invoice at least 334. Literal query supports can exceed two ports. |
| Seven-query bridge | Two declared triangles plus one paired bridge, with any exact rational reader matrix | Local invoice at least 18, including extra zero-target reader columns. No attainability or optimum for earlier sample invoices is claimed. |

The main theorem also gives a necessary budget test. Split every dense query
into pieces of at most two ports, keeping its reader. The sum of the extra
physical charges must be at least `334-C` for an original invoice C. Reaching
296 therefore requires at least **38 units of splitting overhead for every
such partition**. The proof does not optimize partitions or supply a saving.

The canonical residual query has three ports. For a sparse local completion
it is refined into its ordinary pair and residual unit, keeping the same
reader and exact endpoint. Their verified charges are 6+1=7. This avoids
silently applying the two-port theorem to an unsplit residual query.

## Exact scope and reproducibility

The physical cover and labels are pinned through the two inputs in
[SOURCES.json](SOURCES.json). The mask fixes a common nonzero diagonal,
forbids off-diagonal entries between nonorthogonal complete physical groups,
and leaves the remaining entries free. A common diagonal is normalized to
one without changing supports. The tariff is binary pairing rank of complete
source and reader group closures; all conclusions retain this model.

From the repository root, with Python 3.12 or later and the standard library:

```sh
python3 -I -O -Werror -B research/p112-sparse-gain-transfer/verify.py
python3 -I -O -Werror -B research/p112-sparse-gain-transfer/independent.py
python3 -B scripts/research_package.py --package research/p112-sparse-gain-transfer
```

Both scientific commands authenticate their inputs directly, import no
project or scratch code, compare against committed receipts, and leave files
unchanged. `--write-receipt` is explicit maintenance. The separate arithmetic
implementations check:

- All 111,556 entries of the literal I334 expansion and all symbolic strict-fit
  expansion positions, including 28 free group pairs and 420 free scalar entries.
- All 57 target marks, their `3 H3 + 53 H6 + H7` invoice, the three singletons,
  and the residual-bearing mark `{9,39,55}` with its 6+1 sparse refinement.
- An exact three-copy GF4 gauge that succeeds where an ungauged tree fails,
  unit-grounded singleton recovery, and a failed common-reader intersection.
- Strict-fit controls that deliberately change free entries, and the complete
  bridge kernel/particular-reader identities governing every reader matrix.

The main graph proof and common vertex-gauge proof are quantified written
arguments reviewed by separate AI agents. The finite scripts check their
premises and controls; they are not a proof-assistant formalization or an
independent human review. No coefficient or geometry sweep is performed.
A sufficiently large finite characteristic-two field can replace the formal
field by specialization, but no efficient field-size or native implementation
claim is made.

A scalar tariff result does not supply native routes, dirty-state restoration,
storage, precision, an all-size compiler or a complete multiplication supplier.
Those obligations remain open, and no selected frontier file changes.

## Provenance, overlap and credit

Scientific base: canonical main `12fa8c5c844be21bfefb38a19503fbd867a11244`,
priority revision 7. The donor's assigned decoder goal takes precedence over
a new task draw; `TASK.json` records the changed scope. The 20 October public
API snapshot covered all 354 open PRs. Discussion coverage remained unavailable
after persistent HTTP406, so this is not a novelty certificate.

Nearby retained work has different premises: `p112-regular-query-floor` treats
projectively totally-unimodular queries for a fixed canonical target in the
plane model; `p112-graphic-query-transfer` treats finite two-terminal
replacements at one query interface; and `p112-two-port-transfer-classification`
classifies 30 non-Fano placements and coherent boundary maps. This package
instead allows the fitting matrix's free entries and rank to change, and
covers an entire literal two-sparse factor family. No prior result is claimed
as a new deduction here.

The cover, canonical targets and original invoice are retained from
flyingviper's [p112-rational-decoder-gate](../p112-rational-decoder-gate/README.md),
including Cinna Davis's P112 cover lineage, Sagar Thakrar's scalar-mask and
full-group audits, Adam Gall's mask obstruction, ctoth and Philippe Van
Velzen's endpoint/pricing framework, and Hanson Sun's projection work.
Physical labels retain the attribution in the adaptive-kernel-demotion source.

Signed-incidence ranks, switching and circuits are standard; see Thomas
Zaslavsky, [Signed Graphs and Geometry](https://people.math.binghamton.edu/zaslav/Tpapers/sggm.pdf),
Theorems 3.1 and 3.5-3.6. The package proves the needed arbitrary-gain facts
itself and does not attribute its transfer theorem to that signed-only survey.
The strict-mask relaxation, common vertex gauge, support-intersection transfer,
and invoice applications are deductions in this investigation. Prepared by
flyingviper with substantial OpenAI Codex assistance and separate AI-agent
mathematical checks. Apache-2.0.

## Open next questions

- Can a genuinely multiport source/reader interaction lower the full-group
  invoice? A proposed mechanism must have both dense queries and dense readers,
  evade the common-group-gauge obstruction, and provide a fully priced exact
  endpoint. Merely adding one three-port vector does not imply a saving.
- Can the sparse-splitting inequality give a concise rejection certificate for
  a specific dense candidate? Start with one explicit partition and its exact
  tariffs. A low-overhead partition rules out a claimed saving; large overhead
  alone is not a construction.
- Is there a useful structural test for a common group gauge making one whole
  factor family two-sparse? One invertible groupwise similarity must work for
  all terms; separate gauges chosen per term do not meet the corollary.
