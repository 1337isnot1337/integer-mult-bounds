# OR-Tools found a rank-only T740 gain; exact operator replay rejects it

A global CP-SAT allocation improves the rank-moment surrogate and would give a hypothetical
κ about `0.001734807085759196013190…`, above PR #3200's conditional headline. That allocation
**does not preserve the exact eight-stream operator**, so its κ is inadmissible. This package
claims **no new κ**.

## What the solver found

The search starts from the byte-pinned PR #3200 T740 fill and runs CP-SAT over 2,328 distinct
`(port, child-usage)` patterns and 82,880 groups. It considers 139,038 one-axis transfer
candidates, requires unique source axes, forbids a child from both donating and receiving, enforces
pairwise orthogonality at receivers and caps ranks at 51. OR-Tools 9.11.4210 (Python 3.10, seed 0,
eight workers) found a `FEASIBLE`, not `OPTIMAL`, rank profile in 119.327 seconds.

The hypothetical profile shifts 40 children from rank 45 to 44 and 40 from rank 50 to 51 while
preserving rank mass. The old PR #3200 verifier accepts its commuting/hosting rules and brackets
the corresponding numerical root. The source-bound exact operator replay does not.

## Exact rejection witness

For owner replica 0, port 0, the pinned initial pattern is
`[[4,31],[6,31],[8,0],[10,0],[12,0],[13,0],[14,31],[15,31]]`. The six rank-only transfers
change ranks of children 8, 10, 12, 14 and 15. This extends beyond the four-unhosted-child
assignment screen in [PR #3199](https://github.com/CrocSwap/integer-mult-bounds/pull/3199):
two of the proposed donors (14 and 15) are partially hosted.

The exact replay first fails at coordinate character `2^53`. Three Gaussian-integer matrix entries
change:

| Entry | Baseline | Rank-only overlay |
|---|---|---|
| `(1,1)` | `[0,1]` | `[1,0]` |
| `(3,1)` | `[0,0]` | `[1,-1]` |
| `(6,6)` | `[0,1]` | `[-1,0]` |

The unmodified operator passes the source package's 147-mode positive control. `verify.py` rebuilds
the owner-zero context from authenticated PR3148 fill/journal inputs, confirms it matches the
pinned PR #3200 BINS, applies all six moves, and reproduces the exact mismatch. This is a concrete
false positive of the rank-only objective; it is not a theorem that every possible exchange fails.

## Fixed-word ceiling and limits

For PR #3200's local profile `{1:2433, 2:724, 3:228, 4:102, 5:20, 8:8}`,
`complex-local-word-ceiling/ceiling.py:ceiling(local, 73, 896, 9, 64)` gives
`a∈[0.001756446675046, 0.001756446675047]`, hence the scoped relaxation
`κ<0.0017533669794458152` under `κ<a/(1+a)`. The rank-only profile would realize about
98.9415% of that ceiling numerically, but the candidate fails physical-operator equality; its
valid realized fraction is therefore **not established**.

The result is conditional on PR #3200's source stack. It neither validates the PR #3200 baseline
nor discharges its supplier, controller, native-admission or outer-release obligations. The
selected record remains unchanged. The cached overlap scan covered 275 open PRs and 2,050
discussions (complete pagination at 2026-10-17 18:40 UTC). The nearest related work includes
[PR #3199](https://github.com/CrocSwap/integer-mult-bounds/pull/3199), whose exact-coordinate
CP-SAT screen covers rank changes among four idle children, [PR #3204](https://github.com/CrocSwap/integer-mult-bounds/pull/3204),
which states a broader four-site rigidity result, and [PR #3220](https://github.com/CrocSwap/integer-mult-bounds/pull/3220),
which prices additive phase-child repairs. This package contributes one concrete global rank-only
incumbent using partially hosted donors (children 14 and 15) and its exact operator counterexample;
it does not duplicate or replace those broader results. A later overlap refresh could not reach
GitHub, so these counts are a dated snapshot, not a novelty certificate.

## Reproduce

The frozen rank-only result and exact rejection use standard-library replay; no OR-Tools dependency
is needed for verification:

```sh
python3.12 -B research/t740-joint-axis-optimization/verify.py
python3 scripts/research_package.py --package research/t740-joint-axis-optimization --check-only
python3.12 scripts/research_package.py --package research/t740-joint-axis-optimization
```

To rerun the rank-only discovery search, install `ortools==9.11.4210` under Python 3.10 and run:

```sh
python3.10 -m pip install -r research/t740-joint-axis-optimization/requirements-search.txt
python3.10 research/t740-joint-axis-optimization/search.py \
  --seconds 120 --workers 8 --seed 0 --output-dir /tmp/t740-joint-axis-search
```

The parallel CP-SAT search may return the baseline or another feasible profile. Its output is a ranking surrogate;
only the independent exact replay determines whether a move list preserves the operator.

## Open next questions

- **Can operator-preserving exchanges involving partially hosted donors create a net rank gain?**
  First derive exact per-character constraints for the whole eight-child T740 port pattern and
  screen a small source-bound domain before another moment optimization. Blocker: the current
  CP-SAT model checks only rank/commutation/orthogonality, while the physical identity couples
  all streams.
- **Can a global rank-only search be made cheaper once exact operator constraints are added?**
  First incorporate the operator-derived phase tables on the four fully idle children and one
  partially hosted donor in a single representative group. Blocker: the current joint model is
  large, and the previous long multiworker attempt was terminated before writing a result.

## Credit

The T740 baseline BINS, moves and exact verifier are preserved byte-for-byte from PR #3200; source
blobs and hashes are recorded in the source archive. The physical operator replay comes from the
merged `idle-star-paired-axis-census` package, with its source lineage and notices retained there.
PR #3199's broader four-child screen is acknowledged as the nearest overlap; this package adds a
concrete rank-only candidate that also uses partially hosted donors and an exact operator
counterexample for that candidate. New work is Apache-2.0 and uses substantial OpenAI Codex
assistance under the user's research direction.
