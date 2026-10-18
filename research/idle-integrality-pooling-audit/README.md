# Audit: averaging idle mass does not preserve integer multiplicities

**A domain correction to PR3729's planning ceiling. No physical packing,
supplier admission, new multiplication exponent or selected-frontier change.**

[PR3729](https://github.com/CrocSwap/integer-mult-bounds/pull/3729), head
`c7c68f89e020f9e62f38514afdfc99dda01430d4`, correctly prices the best integer
idle histogram **within each isolated mass-1646 call**. Its stronger claim about
the existing aggregate packing relaxation needs an additional lemma. The
selected ledger has 237024 units of idle mass over 144 calls; division by 144
does not require each normalized multiplicity to be integer.

This package checks that missing implication rather than repeating the DP.
The pooled histogram `{51:4647,27:1}`, already proved optimal by
[Penguin for Maximus Putnam / PR1685](../idle-packing-stability/README.md), has
integer counts, the correct total mass and the same rank cap. At `a=0.001689`:

| Complete normalized moment | Certified enclosure |
| --- | --- |
| Repeated per-call optimum `{51:4608,14:144}` | `[1.000001152479605767560524,1.000001152479605767560525]` |
| Aggregate optimum `{51:4647,27:1}` | `[0.999996966877034959759759,0.999996966877034959759760]` |

The first rejects the saving and the second accepts it. The correct
**fixed-144-call aggregate integer** ceiling lies between
`0.001690044548222` and `0.001690044548223`, rather than the per-call
`0.001688603446527`. This is a necessary bound in a relaxation, not a
construction attaining it. A stronger physical bound might still follow
from owner constraints; the aggregate arithmetic alone does not establish it.

The literal selected owner ledger also has shared bins. One capacity-32 bin
receives widths 9,4,9,9 from calls 9,11,13,15 before its single rank-1 remainder
is charged. The independent recount covers all 69120 selected allocations,
recovers the selected idle histogram and finds 17217 used bins shared by
multiple calls. It establishes the capacity accounting interface, not native
semantics or a physical realization of the pooled optimum.

Two short normalization checks clarify the scope further. In a coverage-only
relaxation permitting replica counts to vary, 153 calls give integer histogram
`{51:4938}`, exactly equal to the original fractional relaxation after
normalization. Seventeen complete selected cohorts likewise have zero
aggregate remainder. And the two-unpaid-coordinate lever's average idle mass
`13918/9` has an integer total over nine calls; its fractional average alone
does not prove infeasibility. Neither is a physical construction or admission
of a changed template/coverage law. See [PROOF.md](PROOF.md).

## Reproduce and inspect

Standard library, Python 3.12 or later, from the repository root:

```sh
python3.12 -I -B research/idle-integrality-pooling-audit/verify.py
python3.12 -I -O -B research/idle-integrality-pooling-audit/test_verify.py
python3.12 -B scripts/research_package.py --package research/idle-integrality-pooling-audit
```

The verifier uses its own positive-binomial rational enclosures, with directed
integer rounding and a geometric tail bound. It imports or executes no
predecessor implementation. It confirms both signs of PR3729's per-call root
bracket as a positive control, both signs of the pooled root bracket, the
separating moment, exact replication identities and the literal selected
capacity ledger. [RESULT.json](RESULT.json) retains exact fractions and outward
decimal displays. Default verification preserves input bytes; `--write`
explicitly regenerates that receipt.

Eight test groups include exact square/cube price calibrations, exhaustive
small partitions, invalid histogram rejection, missing-factor/normalization
controls, five real owner-ledger corruptions and retained/main-source
corruption rejection. They remain active under `-O`.

Main inputs are pinned at canonical main
`20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority revision 6, in
[SOURCES.json](SOURCES.json). PR3729's README, implementation and receipt are
retained byte-for-byte with original Git blobs and SHA256 in
[UPSTREAM.json](UPSTREAM.json). They are authenticated for review and data
binding, never imported. A clean replay needs no foreign PR Git object or
network access. [VALIDATION.md](VALIDATION.md) records the executed checks,
source availability and bounded coverage.

## Task and overlap

The `independent-moment` card is refined to the fresh ceiling claim's unchecked
domain implication. Its suggested baseline command passed. Entry overlap
reported complete pagination for 444 open PRs and 2495 Discussion records,
without warnings; a targeted cached query also covered local package notes.
This is bounded title/body/board coverage, not a novelty guarantee.

PR3737 checks the same per-call histogram's arithmetic. PR3701 changes paid
local rank caps. PR1685 already supplies the unrestricted pooled optimum and
concavity proof. This audit adds the separating domain counterexample, correct
fixed-N repricing, replication identities and source-bound shared-bin check.
[TASK.json](TASK.json) records scope, checkpoints and remaining obligations.
The claim is [the reply to the ceiling finding](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19022496).

## Open next questions

* **Repair the public ceiling's scope or justify a stronger physical bound.**
  First state whether idle partitions are aggregate, per replica or per call.
  If per-call isolation is intended, prove the source/owner decomposition or
  a direct physical lower bound. Unknown owner/hosting restrictions cannot be
  replaced by the per-call mass average. This controls which packing proposals
  can legitimately be screened out.
* **Which aggregate-optimal histograms survive the physical owner interface?**
  This is PR1685's existing question, retained with credit. Start from the
  authenticated bin capacities and eligible-call sets and formulate the legal
  grouping constraints. The current audit supplies no owner assignment for
  rank-51 children, no cost claim and no mandate for another packing search.

The structured questions and blockers are in TASK.json. The expansion decision
is **finish this bounded audit and hand off**; no dependent construction round
is authorized by this package.

## Credit and limits

Credit Nick Petalas / PR3729 for the per-call integer DP and question; Penguin
(OpenAI) for Maximus Putnam / PR1685 for the pooled optimum and proof; Douglas
Colkitt with Claude assistance for the fractional ceiling; PR1012 for coverage;
Ali Romman for catalogue-mixture boundaries; and Rohan Arun, Jeremy Kothe,
Hao Yan and the selected #1094/#1087, #589/#555 predecessor chain for the
construction and owner interface. Exact source notices are retained; see
[NOTICE.md](NOTICE.md).

New audit by Arham-Tahir64 with substantial OpenAI Codex assistance in research,
implementation, checking and writing. Apache-2.0. This is author-executed
independent implementation, with no independent human or formal-kernel review.
No full selected cold replay, native/frame/tape admission, all-size theorem,
physical optimum, new kappa or selected-record change is claimed.
