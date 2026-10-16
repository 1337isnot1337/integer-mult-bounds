# Independent V45 frame and invoice audit for PR #2979

**Result: partial positive audit of one local group, the profile-bearing word stages, and the literal T74 owner allocation, plus an exact negative screen of the audited profile at κ=0.1. It does not independently validate the full supplier or select a new κ.**

The selected conditional result remains κ = 0.001672660197076918. [PR #2979](https://github.com/CrocSwap/integer-mult-bounds/pull/2979) claims κ ≈ 0.0017290339826465135, about `0.0000563737855695955` above the selected value. It merged into `main` on 2026-10-16, but the selected record still names #1094; this audit does not admit the candidate or change the frontier. It independently reconstructs the V45 rank-7 frame group from the pinned parent words using explicit XOR-span closure, then rebuilds the profile-bearing word sections through the five extraction transforms and fourteen literal rewrites for both providers. It also independently checks the T74 owner allocation, in addition to the published aggregate arithmetic. It does not replay the full admission chain.

For V45, all 61 edited gate frames are hyperplanes of their old frames, each lies in the shared rank-7 subspace, and every gate touching a lowered helper stays in that subspace. Both parent providers give the same result. The coordinated four-helper lowering changes the exact weighted local profile price by −8,388,172 units and leaves +22,972 after paying for four freed width units. The single-helper control loses: its price delta is −2,038,159 and its margin is −53,141. The five-group positive control independently reproduces all 139 stage-1 edits, the declared stage-1 local profile and the changed width inventory.

The source replay reproduces the stage-2 profile `{1:2449, 2:710, 3:236, 4:102, 5:18, 8:8}` and the final profile `{1:2445, 2:706, 3:232, 4:108, 5:18, 8:8}`, with the claimed width inventory, for both providers. Its exact weighted stage deltas are −46,150,994, −10,523,403, and −52,350 units, summing to −56,726,747. A missing stage-2 frame change, stale rewrite preimage, and unshifted phase warp are rejected by negative controls.

The independent T74 owner replay reconstructs all 1,332 replica/child windows from the pinned nine-stage template and the literal `ORDER.json`, then checks every one of the 271,728 `FILL.json.gz` roles against its source window, provider width, family capacity, and bin coordinates. It verifies that repeated rank-level windows sharing one `(replica, pair, side, port)` family are time-disjoint; all 408 helper identities occur exactly once per call; and both dispatched providers reproduce the same 408-width inventory and paid profile. The resulting idle profile is `{1:17310, 3:4956, 5:1728, 48:28190}` and the full profile closes the exact rank-mass identity at 4,816,512. The physical count reconciles as `896×74 + 408 helpers + 8 centres + 91 private cleanup buffers + 2 inherited coefficient guards = 66,813`. These are source-bound finite allocation and stock-count checks, not a recertification of the global native/outer admission.

A separate 90-digit Decimal evaluation places the full-profile root at approximately `0.00172903398264651351771759`, consistent with the conservative value in the claim and above the selected κ. This is a numerical cross-check, not a new exact root certificate.

The independently reconstructed #2979 local profile and the newer six-skip profile from [PR #3042](https://github.com/CrocSwap/integer-mult-bounds/pull/3042) both fail the requested `κ=0.1` target under the inherited `m=73`, `w=896/9` recursive moment. The PR #3042 claim is pinned at its exact head in [SOURCES.json](SOURCES.json); [PR #3054](https://github.com/CrocSwap/integer-mult-bounds/pull/3054) reports composing that same six-skip word with a larger T740 allocation, which changes its idle profile but leaves the local profile unchanged. At `κ=1/10`, the retained transfer requires `a=1/9`, and the local child term is `(r/73)^(8/9)`. Integer ninth-root brackets, checked by exact integer powers, give

```text
(PR #2979) (1/w) Σ n_r (r/73)^(8/9) ≥ 48304277901/44800000000 > 1.
(PR #3042) (1/w) Σ n_r (r/73)^(8/9) ≥ 48295445607/44800000000 > 1.
```

Both left sides count only paid local children. They omit idle children and the centre path, whose costs are nonnegative, so no packing, extra unpaid coverage, or centre deletion can bring either **fixed profile** to `κ≥0.1` under that transfer. A different local profile, coverage law, or outer transfer could escape this scoped result; none is supplied here. The verifier checks the #2979 profile from its pinned words, reads the PR #3042 profile from its exact pinned claim, and checks rank-by-rank rational floors and both aggregate inequalities.

## Reproduce

From the repository root:

```sh
python3.12 scripts/research_package.py --package research/rank7-v45-profile-audit --check-only
python3.12 scripts/research_package.py --package research/rank7-v45-profile-audit
```

The verifier uses only standard-library arithmetic and JSON/gzip inputs pinned in [SOURCES.json](SOURCES.json). Its target screen uses exact integer ninth-root brackets, not floating-point powers.

## Limits

The stage-2/3 replay reconstructs only sections that determine the paid profile; it does not independently prove the extraction or rewrite operator identities, or reconstruct compensation and cleanup semantics. The owner replay checks literal finite rank windows, offsets and the stated stock count, but not the underlying binary frame transitions, global stock/precision/hosting premises, fresh native admission or outer release. The `κ=0.1` screen applies only to the audited local profile and inherited moment/transfer. Consequently, the audit does not certify the complete κ claim or update the selected frontier.

## Open next questions

The exact target screens show that the #2979 profile and its newer six-skip successor both need a substantial local-profile change (or a changed coverage/outer transfer) before their other open obligations could matter to `κ≥0.1`. For #2979, the next validation step remains a code-disjoint symbolic replay of the extraction/rewrite identities, compensation updates and inverse cleanup on all 632 independent inputs; a separate complete-stock/native/outer review is needed for its reported κ. See the structured questions in [TASK.json](TASK.json). Do not start another lowering census until those obligations are closed or explicitly handed off.

## Credit

The audited construction and its predecessor chain remain credited in `research/rank7-joint-endframes/NOTICE` and its README: Dugongue / Marius-Paul Dumitrean for PR #2979, Jeremy Kothe for the PR #2957 rewrites, and all listed predecessor contributors. This small audit does not replace or absorb those contributions. Prepared with substantial AI assistance by OpenAI Codex; Apache-2.0.
