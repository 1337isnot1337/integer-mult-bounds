# Cycle 11 task card

- **Track / selector card:** `recursive-interfaces` / `centre-path-sharing`
- **Accepted seed:** `10d3ef274e33f1db0aaecb961566139c`
- **Priority revision / catalogue SHA-256:** 3 / `6686ad58f1fbdbc87134a78901b60fd53a20d3984355e91defbbebc9e9fa8075`
- **Exact base:** `0b1cccf86e2f5132ed286a26ef0a681a495740ea`
- **Selected-record SHA-256:** `10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32`
- **Scope status:** changed. The initial three-frame screen showed that the selected centres are distinct carriers; a common frame intersection alone does not establish one shared call. The bounded experiment now changes PR1708's identical-source premise by one explicit source-side rank-one deviation.

## Object and question

Let `L : F_2^n -> F_2^m` be one fixed exact linear centre map, `v` a fixed source direction, and `alpha` an arbitrary scalar. Two arbitrary-dirty target panels request

```text
y0 += L(x)
y1 += L(x + alpha*v).
```

Can one complete broadcast of `L(x)` to both targets plus a separately charged rank-one correction `alpha*(L(v))` produce exactly these outputs while preserving `x`, `alpha`, both arbitrary target values, and any private dirty state? The second source panel differs from the first only in the one-dimensional `v` direction.

This is source-side delta correction. It differs from PR1707's identical-source broadcast and from the active rank-one output-panel difference claim in Discussion #1166 comment 18922942.

## Fully charged budget screen

The baseline pays two rank-8 map calls and two target updates. The candidate pays one rank-8 broadcast, one rank-one correction, and the same two target updates. The correction must be fused into the second target's existing accumulation; a third target pass is charged as extra overhead `Delta`.

Ignoring only `Delta`, the rank-mass saving is `8^(1-a)-1`. At the selected complex endpoint `a = 67018507072324140917/40000000000000000000000`, this is about **6.972176283896** rank-mass units. Therefore all coefficient preparation, source-delta access, extra output arithmetic, dispatch, frame, hosting, restoration and precision costs must total less than 6.972176283896 units for this pair to improve the moment. If the correction cannot be integrated into one target pass, include that extra pass and stop if the completed screen fails.

This is a local interface screen only. The selected bit supplier, full recursive moment, eligible selected occurrence, and complete frontier remain separate obligations. No kappa is claimed.

## Bounded method and stopping rule

Use the smallest nontrivial exact instance: `n=m=3`, an invertible binary `L`, `v=e_0`, and arbitrary `x`, `alpha`, `y0`, `y1`. Prove the general identity `L(x+alpha*v)=L(x)+alpha*L(v)` and implement the fused output accumulation. Exhaust all `2^12` dirty/input states. Require positive controls and negative controls for an omitted correction, stale `alpha`, and incorrect `L(v)`.

Price the fused output and source access completely against two ordinary complete calls. Stop if the full bill does not beat the baseline or if a correction requires a separate target pass above the 6.972-unit allowance. Do not search other operators or panel counts in this cycle.

## Pins and nearest work

- Selected record, certificate, review, source manifest and reproduction are resolved from the current `certificates/selected-result.json`: `docs/research/community-batch1099-review.md`, `research/community-frontier1094-audit/SELECTED-SOURCE.json`, `research/community-frontier1094-audit/ASSEMBLY.json`, `make frontier1094-verify`.
- PR #1707, head `3d2e634e046ac4fbf07ddbfb0e59da4cf9907f4e`, packages charged common-A broadcast readout on identical source values.
- PR #1708/#1748 and #1791 cover identical-source two-panel centre sharing and its profile budget.
- Discussion #1166 comment 18922942 concerns a rank-one difference between output tensors; the present object is a rank-one difference between source panels.
- Fresh complete overlap refresh at 2026-10-14 12:59 UTC covered 536 open PRs and 516 Discussions; no direct hit for `rank-one source delta`, `source-panel difference`, or `input-panel correction`.

## Deliverable

One exact local construction or a bounded, reproducible obstruction, with literal source/output schedule, complete cost, positive and negative controls, source pins, reproduction command, open next questions, attribution, and explicit statement that selected-supplier admission and kappa remain unproved. Substantial OpenAI Codex assistance will be disclosed.
