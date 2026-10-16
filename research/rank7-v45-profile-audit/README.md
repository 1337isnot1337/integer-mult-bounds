# Independent V45 frame and invoice audit for PR #2979

**Result: partial positive audit of one local group and the aggregate profile. It does not independently validate the full supplier or select a new κ.**

The selected conditional result remains κ = 0.001672660197076918. PR #2979 claims κ ≈ 0.0017290339826465135, about `0.0000563737855695955` above the selected value, but its status remains an unadmitted source archive. This audit independently reconstructs its V45 rank-7 frame group from the pinned parent words using explicit XOR-span closure, then checks the published final words and T74 aggregate arithmetic. It does not replay the full admission chain.

For V45, all 61 edited gate frames are hyperplanes of their old frames, each lies in the shared rank-7 subspace, and every gate touching a lowered helper stays in that subspace. Both parent providers give the same result. The coordinated four-helper lowering changes the exact weighted local profile price by −8,388,172 units and leaves +22,972 after paying for four freed width units. The single-helper control loses: its price delta is −2,038,159 and its margin is −53,141. The five-group positive control independently reproduces all 139 stage-1 edits, the declared stage-1 local profile and the changed width inventory.

Profiling the pinned final words directly reproduces `{1:2445, 2:706, 3:232, 4:108, 5:18, 8:8}` and `{4:26, 5:2, 6:16, 7:52, 8:99, 9:213}` for both providers. Their exact weighted change from the parent is −56,726,747 units, equal to the sum of the three published stage deltas. The T74 allocation profile pays all 666 local calls, leaves idle profile `{1:17310, 3:4956, 5:1728, 48:28190}`, and closes the exact rank-mass identity at 4,816,512. A separate 90-digit Decimal evaluation places the full-profile root at approximately `0.00172903398264651351771759`, consistent with the conservative value in the claim and above the selected κ. This is a numerical cross-check, not a new exact root certificate.

## Reproduce

From the repository root:

```sh
python3.12 scripts/research_package.py --package research/rank7-v45-profile-audit --check-only
python3.12 scripts/research_package.py --package research/rank7-v45-profile-audit
```

The verifier reads only standard-library JSON/gzip inputs pinned in [SOURCES.json](SOURCES.json).

## Limits

Stages 2 and 3 are not independently rebuilt from the five extraction records and fourteen rewrite records; the final words are read as pinned inputs. The T74 owner schedule and physical allocation chronology, fresh native admission, and outer release are also not independently checked here. Consequently, the audit supports the V45 local cost mechanism but does not certify the complete κ claim or update the selected frontier.

## Open next questions

The next useful test is a source-bound reconstruction of the changed local profile through stages 2 and 3, followed by one independent check of T74 ownership chronology and the supplier cap. See the structured questions in [TASK.json](TASK.json). Do not start another lowering census until those obligations are closed or explicitly handed off.

## Credit

The audited construction and its predecessor chain remain credited in `research/rank7-joint-endframes/NOTICE` and its README: Dugongue / Marius-Paul Dumitrean for PR #2979, Jeremy Kothe for the PR #2957 rewrites, and all listed predecessor contributors. This small audit does not replace or absorb those contributions. Prepared with substantial AI assistance by OpenAI Codex; Apache-2.0.
