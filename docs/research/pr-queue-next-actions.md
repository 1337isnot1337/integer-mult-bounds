# PR queue: next actions

Snapshot after the twenty-fifth intake: **101 non-draft PRs remain open**. Twenty-eight contributions were archived this round, including 25 separately reviewed manual workflow configurations. Scientific claims remain unvalidated by intake; selected κ is unchanged.

| Lane | Open non-draft PRs |
| --- | ---: |
| new head | 1 |
| shared code or docs | 31 |
| research plus attributes | 1 |
| held known correctness | 14 |
| held known correctness or integrity | 48 |
| held intake errors | 3 |
| held unreviewed stack | 2 |
| held unmerged dependencies | 1 |

## Efficient next pass

Refresh live heads and compare to the [exact queue snapshot](../../research/community-efficient2500-audit/QUEUE-final.json). Skip unchanged revision holds. Prioritize shared-code changes with affected-consumer tests; #2958 addresses replay-inventory omissions and is a useful next target. #2957 adds a research package plus root attributes and needs its own source/attribute intake.

CI configuration for 25 proposals is now manual-only. No jobs were dispatched. #1699 shares the copied evidence-manifest mismatch, and #732 conflicts with the frozen global-star package; both remain open.

The [previous grouped integrity report](../../research/community-efficient2400-audit/manifest-issues.json) records the 36 related revision holds and one separate hash mismatch. The #1699 copy adds another instance. Resolve the common provenance question once without silently rewriting frozen evidence. Known proof objections and stacked dependencies retain their exact obligations in the central ledger.
