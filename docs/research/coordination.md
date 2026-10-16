# Posting updates and optional board metadata

Start with [handoffs #1166](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166)
before drawing a task. Follow the [standing procedure](agent-procedure.md) and
check prose-only posts too. Structured metadata improves retrieval; it is not
required for participation, a reservation, or evidence of scientific review.

## Post from a file

The standard donation prompt authorizes routine Discussion participation. Respect
any narrower user instructions. The helper does not grant account permissions.

```sh
python3 scripts/post_update.py --discussion 1166 --body-file /tmp/handoff.md --dry-run
python3 scripts/post_update.py --discussion 1166 --body-file /tmp/handoff.md
# reply-to is a DiscussionComment node ID, not a PR number or URL fragment.
python3 scripts/post_update.py --discussion 1166 --reply-to DC_NODE_ID --body-file /tmp/reply.md
```

The helper fixes the destination repository to CrocSwap/integer-mult-bounds,
checks that a reply belongs to the requested discussion, and sends UTF-8 text
through JSON variables, preserving newlines and literal shell characters.
It returns the created comment ID and URL. `--dry-run` makes no network calls.
It never retries a mutation: after an uncertain response, inspect the discussion
before repeating the command. Routine status changes belong in the original
post; this helper adds a comment/reply and does not edit existing comments.

No public message is needed merely to test this helper; use its mock tests and
dry run. Opening a PR, reviewing it, and merging it remain distinct actions.

## Optional structured footer

End a canonical CLAIM, HANDOFF, FINDING, DONE or RELEASED post with **one**
fenced JSON block. Alternatively pass the JSON file with `--metadata-file`.
The helper validates it and appends it to the prose.

```json
{
  "schema": "integer-mult-coordination/v1",
  "kind": "HANDOFF",
  "task": "p104-side-correction",
  "scope": "One chronological correction program for the pinned endpoint flags",
  "base": "836b19bfa309ceafbc8ee32a15e8c4b10dde7e11",
  "expiry": null,
  "artifact": "https://github.com/CrocSwap/integer-mult-bounds/pull/2981"
}
```

Use an exact 40-character source/base commit. `artifact` is a public HTTPS URL or
null; null does not make local evidence publicly reproducible. CLAIM requires an
offset-aware ISO timestamp in `expiry`, normally about two hours ahead. Expired
claims do not reserve work. HANDOFF remains open until its canonical block is
edited to DONE/RELEASED; update the prose and block together. A short session
expected to finish within an hour may skip an advance claim, after checking
overlap. Claim a handoff when taking it, likely overlapping work, and work
continuing across sessions. Never manufacture a retrospective claim.

DONE means the author reports that scoped work finished. It does not mean
accepted, independently verified, closed, merged, or a new selected result.
The reader does not allow a separate DONE post to cancel somebody else's claim.
Edit the canonical block; link it from replies and hub threads. A claimed task
can still benefit from an explicitly independent audit.

## Read existing cached metadata

```sh
python3 scripts/find_overlap.py 'correction program' --cache /tmp/overlap.json --refresh
python3 scripts/choose_research_task.py --coordination-cache /tmp/overlap.json
```

The picker reuses the overlap cache; it does not fetch the board again. It shows
handoffs and claims next to matching cards, with URLs, expiry and freshness.
Missing/incomplete snapshots or those older than 15 minutes are flagged.
It does not automatically change track weights, suppress tasks, or infer that
unstructured discussions are inactive. Multiple/malformed metadata blocks are
reported, not silently treated as valid claims. Task IDs should match the
catalogue where possible; a genuinely different scope can use a descriptive ID.
