# PR queue: next actions

Snapshot after the twenty-fourth intake: **125 non-draft PRs remain open**. Nineteen contributions were archived this round; source archival acceptance does not validate their scientific claims. The selected result is unchanged.

| Lane | Open non-draft PRs |
| --- | ---: |
| new head | 2 |
| shared code or docs | 30 |
| held known correctness | 14 |
| research plus ci | 27 |
| held known correctness or integrity | 10 |
| held intake errors | 39 |
| held unreviewed stack | 2 |
| held unmerged dependencies | 1 |

## Efficient next pass

Refresh live heads and compare to the [exact queue snapshot](../../research/community-efficient2400-audit/QUEUE-final.json). Skip unchanged holds. Review the 27 CI proposals by common trigger, permissions and resource policy; do not enable heavy automatic workloads merely to archive research. Shared-code changes need affected-consumer checks.

The [grouped integrity report](../../research/community-efficient2400-audit/manifest-issues.json) identifies 36 revisions sharing one copied evidence-manifest disagreement and one separate revision. Resolve the source/provenance discrepancy once per identical input before considering the dependent revisions; do not rewrite frozen author evidence to manufacture matching hashes.

Known correctness issues, stacked dependencies and unrelated integrity failures retain their exact outstanding obligations in the central ledger. Remaining general research questions are not settled by an archive merge.
