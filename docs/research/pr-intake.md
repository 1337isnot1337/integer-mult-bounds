# Maintainer queue intake: review changes, not the backlog

This is the default for authorized PR maintenance, including after compaction or
handoff. It takes precedence over historical batch recipes and generated generic
priority lists. It changes scheduling, not the standard of scientific evidence.
The review ledger remains authoritative for acceptance and attribution;
[pr-intake-state.json](pr-intake-state.json) is only a persistent scheduling cache.

## Start here every session

```sh
python3 scripts/pr_intake.py plan --refresh --output /tmp/pr-intake-plan.json
```

This fetches canonical main, reads open PR metadata once, compares exact heads and
watched source/dependency identities, and selects at most 100 actionable entries.
It never reads full PR bodies, executes contribution code, merges, closes, posts,
or changes the cache. Use the canonical integration checkout; preserve unrelated
user work. `--live-json` supports offline diagnostics but is explicitly not fresh
GitHub evidence. Recheck the live head before publication or closure.

Read the summary and **selected** entries first, not the entire ledger. Within
the selected chunk, handle ready integrations together, group shared dependencies,
and review each changed mechanism once. New/changed heads receive priority over
unfinished older review; pending review stays visible until explicitly resolved
or deferred. A changed head invalidates reuse, but does not require rerunning
unchanged scientific inputs whose exact coverage remains valid.

## What wakes an old entry

- A different PR head.
- A changed or removed watched main file/directory or review evidence blob.
- A watched PR head change or its departure from the open queue (not proof it merged).
- A scheduling policy-version change.
- `--wake PR_NUMBER` after new relevant external evidence or explicit direction.

The planner does not read Discussion/comment bodies. A revision supplied only in
comments must be explicitly woken. Watch actual scientific dependencies as well as
shared production paths when they can resolve a hold. The whole main commit,
queue length, passage of time, unrelated CI activity and compaction are **not**
reasons to repeat a review. Increment `POLICY_VERSION` only when existing cached
scheduling decisions genuinely require reconsideration.

## Persist each changed decision once

Use `record` after reviewing the exact head; it checks the live head by default:

```sh
python3 scripts/pr_intake.py record --number 123 --head FULL_REVIEWED_SHA \
  --status waiting_revision --reason 'Concrete failure and required repair' \
  --evidence docs/research/EXISTING-REVIEW.json \
  --watch-path scripts/RELEVANT_SOURCE.py --watch-pr 122
```

Use real existing evidence and paths at the selected base; omit irrelevant watch
arguments. Commit the updated cache with the actual review/integration evidence.
Do not repeatedly record unchanged entries. `record` does not update the ledger,
authorize a merge, or certify tests. Status meanings:

| Status | Next action |
| --- | --- |
| `ready_to_integrate` | Finish explicit acceptance gates, source retention, attribution and publication. |
| `pending_review` | Unfinished substantive work; remains actionable. |
| `waiting_revision` | Concrete correctness/integrity or migration repair needed; dormant until woken. |
| `deferred_replay` | Explicitly scheduled separately or resource-stopped execution; dormant, obligations remain open. |

A generic “not yet reviewed” is not a revision request. Do not mark pending work
as blocked merely to shrink the queue. Leaving the open queue does not certify
incorporation; reconcile actual GitHub state and retained sources separately.

## Time and inference budget

- Reconcile the **whole queue cheaply**, then work in chunks of **up to 100 actual
  decisions**. Never pad a chunk by rereading dormant PRs.
- Carry forward unchanged review evidence by reference. Record only new decisions
  and receipts. Do not create another 100-entry audit directory, copy old source
  packets, or rewrite old reports for an unchanged batch.
- Bulk archive eligible isolated research after source/integrity intake, preserving
  authors and explicit unverified scientific obligations. Shared tooling and known
  correctness failures cannot enter through the archive lane.
- Group related construction chains; review the strongest relevant descendant and
  each unique delta, retaining predecessor credit. This is not automatic approval
  or closure of ancestors.
- Run relevant checks once per changed source/dependency/environment obligation.
  Reuse exact-source receipts with explicit coverage; keep expensive frontier
  verification separate from archive intake.
- No automatic Lean, Docker, all-history suites, or parallel heavy jobs. Current
  local replay limits remain serial, sampled 1 GiB descendant memory, and explicit
  timeouts. A resource stop stays deferred until the execution plan changes.
- For hosted CI, record run ID and source SHA. Poll that same run; a transient
  observation failure is not permission to restart it. Do useful independent work
  while it runs. Scope workflow triggers to avoid unrelated automatic workloads.
- Summaries report **new integrations, new holds, pending actionable work and
  separately deferred replays**. Reconciled entry count is not completed reviews.

## Handoff and completion

Keep the current scheduling cache, exact-head ledger and a short checkpoint with
any live run IDs, integration branches and next commands. A new session should
resume that checkpoint, not reconstruct all earlier batches. The initial durable
checkpoint is [pr-intake-checkpoint.json](pr-intake-checkpoint.json).

“All caught up” requires a fresh queue read, all actionable work resolved and
all remaining revision/deferred obligations accurately reported. It does not mean
all PRs have been scientifically verified. If the user's goal requires outstanding
replays, keep that goal incomplete until they are actually resolved.

Test scheduling changes with `python3 -B tests/test_pr_intake.py`; this is a cheap
metadata test and intentionally launches no contribution workloads.
