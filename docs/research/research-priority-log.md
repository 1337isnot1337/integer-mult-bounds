# Research priority decisions

This log records allocation decisions, not mathematical frontier changes.
The active machine-readable portfolio is [agent-task-catalog.json](agent-task-catalog.json).
Follow [the director review procedure](../../autoresearch.md#6-maintainerdirector-priority-review)
when changing it. Preserve old entries so later agents can see why a route was
prioritized, narrowed or retired.

## Revision 1 — 2026-10-13: initial diversified portfolio

**Evidence base:** `ce7ad1b6ab09452c3478723a2e96ed5ff212dc08`, the selected #1094
record and [batch-1099 review](community-batch1099-review.md). The onboarding
portfolio was introduced in `c0e3631dc24e3c24a861f7d3d79e0608481cccec`; discussion
breadcrumbs followed in `e208d5e77a204252f92b395aae271679cc3a56f0`.

**Allocation:** bit mechanisms 20%, complex mechanisms 20%, recursive interfaces
15%, adversarial audit 15%, independent verification 10%, verifier engineering
10%, consolidation 5%, incumbent optimization 5%. This establishes the initial
repository-owned allocation; this entry does not change its weights.

**Reasoning:** local scalar improvements can leave the paid recursive profile
unchanged, and incumbent packing improvements alone have not established a
large-jump mechanism. The selected construction is complex-limited, but a large
improvement also needs the bit supplier to advance. Allocate substantial effort
to mechanisms on both sides and changed interfaces, while keeping verification
and useful incremental work represented. Existing evidence includes the
[scoped decoder bound](../../research/complex-decoder-field-extension-seed44/README.md),
[frozen provider-catalogue bound](../../research/heterogeneous-owner-assembly/README.md)
and [helper-contract gap](../../research/r439-bsection-stars-seed01/README.md).

**Limits:** weights are research judgment, not measured success probabilities.
The listed obstructions have restricted hypotheses. No universal barrier, new
supplier, or stronger κ is established by this allocation. No systematic
post-launch yield measurement is available yet.

**Next experiments:** use the catalogue cards to identify a changed premise,
price a favorable complete budget, and run a bounded falsification or construction
test. Independent work should target specific proof or verification obligations.

**Next review trigger:** a reviewed frontier/bottleneck change, a new decisive
obstruction, the next substantial PR reconciliation, or evidence of duplicate
assignments on the live board. In an active influx, review roughly daily.

## Revision 2 — 2026-10-13: reduce entry costs and expose scope changes

**Evidence base:** `1b59b624d21924f8e3537cdc1ac52d3be6eda2fe`, retaining the same
#1094 selected mathematical record. A maintainer-supplied first-agent report
described successful onboarding but costly manual overlap checks, a move toward
a self-contained side result, unclear next questions, and scope drift from
changing an alphabet to increasing its source count. The report's corresponding
PR was not independently audited in this onboarding pass. Direct inspection
confirmed the task card's alphabet-change premise and the missing workflow
helpers. This is one field report, not a measured population trend.

**Decision: actionable workflow repair; no portfolio reweighting.** Keep the
revision-1 weights. Add a concrete bottleneck brief and glossary, source-bound
first steps, causal bottleneck links, bounded next experiments, allowed
variations and scope-change triggers to every card. Make the one-hour budget a
default and the orientation fraction flexible. A substantive handoff can finish
a session without a PR.

**Implementation:** cached overlap search covers open PR titles/bodies, live
discussion messages, package notes/metadata and the ledger, reporting freshness
and limits. A minimal package generator captures exact provenance and live input
pins. Explicit metadata requires an actual scope, a reason for changes and
structured next questions; it does not certify mathematical relevance. A bounded
opt-in CI hook replaces any suggestion to execute every historical verifier.
Frozen predecessor packages remain untouched.

**Coordination:** the donation prompt explicitly authorizes routine board posts
and focused PRs once, avoiding repeated permission questions. Optional feedback
goes in a PR or [discussion #1200](https://github.com/CrocSwap/integer-mult-bounds/discussions/1200);
director decisions belong here. A repository file cannot override a donor's
narrower restrictions or grant missing account access.

**Next experiments:** observe whether new sessions reach the card's intended
premise, whether the first command works, and whether the overlap report saves
orientation effort. Record actual scope changes, actionable central handoffs and
useful side contributions separately. Evaluate the metadata/replay hook on new
packages before extending its environment presets.

**Next review trigger:** several additional session reports, a substantive
helper failure, the next PR reconciliation, or a new mathematical bottleneck.
If drift persists, narrow assignments or rebalance effort using evidence; a
single report is insufficient reason to retire the mechanism tracks.

## Revision 3 — 2026-10-13: aim complex and interface effort at the structural levers

**Exact base and selected source record:** `dadfea6e8a78ff6ba901705f87532a71c6f5bbb8`, unchanged #1094
record (`certificates/selected-result.json`, κ 0.001672660197076918, complex side binding).

**Evidence links and verification status.** The maintainer independently replayed #1240
(`1e136b8c4a552050820334ad113628775182f08c`) and #1264
(`1be64e9ef79fe11f24f05b62b0fd7d70be0b7b4c`), including all 14 pinned census blobs.
The monotone-cost relaxation and rational enclosures were reviewed within their stated model.
This accepts scoped arithmetic and the screening argument, not any pending construction or the full
multiplication theorem. Original sources, attribution and conditional coverage-law assumptions remain explicit.

- [#1240](https://github.com/CrocSwap/integer-mult-bounds/pull/1240) (`research/complex-local-word-ceiling`):
  under PR1012's coverage identity (also open) and the halving guard, any hosting, owner or idle repacking of
  the selected local word has a < 0.001690054109089, so κ < 0.001687203 (+0.869%). At a = 1/99, the word's
  excess spend is 20.4 times the per-call budget. `levers.py` gives the one-at-a-time ideal budgets: centre
  path free 2.80×, shared by two calls 1.90×, rank-16 children 2.31×, two unpaid coordinates per family
  3.77×, centre free plus rank-16 6.51× (κ cap 0.0109).
- [#1264](https://github.com/CrocSwap/integer-mult-bounds/pull/1264): 14 of the 30 open claims above the
  selected κ (pinned by blob) use nine distinct paid local profiles. Within the stated model all have κ < 0.001687314840. The leading
  #1148 line sits on words whose caps are 0.17–0.21% *below* the selected word's, and reports a larger fraction of its own relaxation cap. A comparison of caps alone does not compare attainable optima.
  16 claims could not be screened.
- The October 13 census snapshot lists 30 nearby κ claims; similar titles do not establish duplicate
  mechanisms. [One agent's feedback](https://github.com/CrocSwap/integer-mult-bounds/discussions/1200#discussioncomment-18909265)
  reports a crowded queue and scattered supplier anatomy, and requests profile-based grouping.
  More quantitative task cards are a maintainer response to this evidence, not a demonstrated population-wide cause of duplication.

**Current bottleneck; what changed.** The binding complex budget is about D/E. D is about 35.6 unpaid of
7,232 paid coordinates per call, and the 64-per-call centre path consumes about 64% of the raw deficit. E has
an effective child rank of about 3.9. Revision 1 diagnosed this qualitatively ("a large jump needs a changed
mechanism"). The new evidence quantifies it: packing headroom on every screened word is under 0.9%, while the
structural levers are worth integer multiples. This motivates more quantitative cards; it does not establish why contributors chose particular routes.

**Track/card decisions.**

- *Complex mechanisms:* **replace** `complex-masked-decoder` with `complex-rank-shape-decoder` (larger-rank
  delivery; masked and overcomplete supports remain allowed methods). **Narrow** `complex-new-helper-inventory`
  with a ceiling screen. Weight unchanged at 20.
- *Recursive interfaces:* **expand** with `centre-path-sharing` and `coverage-law-change`. Keep
  `persistent-boundary` and `connector-alphabet-change`. Weight 15 → 20.
- *Incumbent optimization:* **narrow**. Claims must report their packing cap and realized fraction. Weight 5 → 2.
- *Verifier engineering:* **continue** at reduced weight, 10 → 8.
- Bit mechanisms, adversarial audit, independent verification and consolidation are **unchanged**.
- `autoresearch.md` asks claims within this model to report their packing cap; claims outside it must identify the changed hypothesis and a replacement bound.

**Old allocation → new allocation:**

| Track | Old | New |
|---|---:|---:|
| Bit mechanisms | 20 | 20 |
| Complex mechanisms | 20 | 20 |
| Recursive interfaces | 15 | 20 |
| Adversarial audit | 15 | 15 |
| Independent verification | 10 | 10 |
| Verifier engineering | 10 | 8 |
| Consolidation | 5 | 5 |
| Incumbent optimization | 5 | 2 |

**Paused scope and evidence that would reopen it.**

- No track is paused. `complex-masked-decoder` is retired as a separate card, and its methods continue
  under the rank-shape card. Reopen it if a masked decoder is found to help through a route other than child
  rank (for example, deficit).
- Incumbent optimization returns to 5 or more if #1240 or #1264 fails review, or if a reviewed word is found
  whose cap is well above its realized packing.

**Next bounded experiments and stop rules.**

- *Centre path:* a fully charged relaxation of sharing one centre path across two calls. Stop the card if the
  ideal (1.90×) shrinks below a 10% gain once restoration and hosting are charged.
- *Rank shape:* one exact small identity with block frame climbs, screened with `ceiling.ceiling()`. Stop a
  candidate whose ideal ceiling does not beat the selected word's by 5%.
- *Coverage law:* explain the source of the single unpaid coordinate per family. Stop if it is forced by the
  data endpoint contract, and record that as an obstruction.

**Uncertainties and useful work preserved.**

- The lever multipliers are one-at-a-time favorable relaxations. They omit the cost of realizing each lever.
- The ceiling assumes PR1012's coverage law and the stated template/guard. The checked profiles satisfy that identity, but this review does not establish it for changed interfaces or complete the separate PR1012 review.
- Equal paid profiles do not establish equal circuits. Upper bounds on different profiles do not order attainable optima.
- The task-card thresholds are research allocation choices; the ideal multipliers are not success probabilities.
- If review finds an error in #1240 or #1264, revert to the revision-2 cards.
- The bit side is unchanged and must advance too before κ > .01. Its levers are not quantified in this revision.
- Packing results remain valuable as realizability evidence. They are now labelled relative to their cap.

**Next review trigger:**

- a correction to #1240/#1264, completion of the separate PR1012 review, or a materially different paid profile;
- the first fully charged centre-path or rank-shape result, positive or negative;
- or several sessions on the new cards.

Until then, review roughly daily during the influx.

## Template for the next decision

```text
Revision / UTC date:
Exact base and selected source record:
Evidence links and verification status:
Current bottleneck; what changed:
Track/card decisions (continue / narrow / expand / pause / replace):
Old allocation -> new allocation:
Paused scope and evidence that would reopen it:
Next bounded experiment and stop rule:
Uncertainties and useful work preserved:
Next review trigger:
```

Prepared by Douglas Colkitt with OpenAI Codex assistance. Apache-2.0.
