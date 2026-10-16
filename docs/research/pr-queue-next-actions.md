# PR queue: next actions after archival intake

Snapshot against main `6e1bbb4a489cb7d05bf592a043d5d353eb767e4a`; **171 non-draft PRs open**. This is triage, not a statement that the scientific reviews are complete. The selected result is unchanged. New arrivals after this snapshot require a refresh.

| Lane | PRs | Next action |
| --- | ---: | --- |
| new head | 1 | Collect exact-head metadata and source inventory. |
| research plus attributes | 74 | Review narrowly scoped attributes and reconcile research-package versions; this category is not merge approval. |
| shared code or docs | 30 | Review the actual shared behavior or claims and affected callers. |
| held known correctness | 20 | Resolve the recorded counterexample, invalid inference, scope overclaim or engine defect before acceptance. |
| research plus ci | 27 | Review workflow permissions, triggers, resource limits and research-source overlap. |
| research versions or new files | 16 | Reconcile overlapping package versions and retain exact original sources; check prior substantive holds. |
| held intake errors | 2 | Repair source/manifest disagreement without weakening immutable pins. |
| held unmerged dependencies | 1 | Resolve or separate inherited shared-code changes before archive-only integration. |

The large attributes lane contains historical supplier revisions, often sharing package paths. A `.gitattributes`-only difference outside `research/` does not establish that all research files are new or mutually compatible. Preserve the current selected supplier and frozen sources while reconciling these versions.

The [exact-head queue](../../research/community-efficient2200-audit/QUEUE-NEXT.json) retains each PR’s remaining scientific question and differing paths. Source-only archive merges stay partially reviewed in the [central ledger](pr-ledger.md). No heavy replay is justified merely to repeat unchanged evidence.
