# Stage-local address caching for E8 scalar replay

The [pinned PR447 emitter](https://github.com/rohanarun/integer-mult-bounds/blob/43e5aa3a2fb6701b1facf542f7f3dee0fbb33c3e/research/e8-eleven-hosting-selected/code/emit.py)
recomputes the same local-to-global address mapping for each instruction operand.
`ADDRESS-MAP.patch` constructs that mapping once per local stage and replaces
the two function calls with indexed lookups. It includes the private scratch
index and retains every original scientific check.

On two retained local-word workloads, the exact scalar-replay section measured
**1.74x and 1.73x faster**, respectively, in three alternating trials:

| Retained local word | Original median | Cached median | Ratio |
| --- | ---: | ---: | ---: |
| Completed PR438 post-basis bit word | 35.984 ms | 20.728 ms | 1.736x |
| Authentic PR442 hosted bit template's local word | 35.774 ms | 20.676 ms | 1.730x |

The timings include table construction, dirty-basis initialization, all eleven
scalar stages, stage/private/terminal restoration assertions, and 24 integer
bridge omission controls. They exclude template loading, AST extraction,
geometry, hosting, compression and the remaining supplier wrapper. Measurements
used Python 3.14.8 on macOS arm64. This is a scalar-replay microbenchmark, not a
whole-emitter speedup. The cache adds O(LOCAL) storage per active stage.

Both versions independently reproduce identical complete values, levels,
schedules, stage receipts and controls. Each workload checks 9,417 basis
columns and all 11 stages. The operand contract checks 648,692 mapped operands
across both workloads, including both reflections and the private endpoint.
The two workloads use source-bound, completed PR438/PR442 local words in the
pinned eleven-stage recipe. They do not constitute a new full PR447 admission.
No numerical bound or mathematical finite coefficient changes.

The [proof](PROOF.md) states the exact valid-index and stage-immutability
preconditions. AST normalization verifies that the only source edits are table
construction and the two lookups. The retained digest-cache patch also composes
cleanly in either order to identical source; the two independently measured
speedups must not be multiplied into a whole-emitter claim.

To apply the optimization in the pinned upstream checkout:

```sh
git apply --directory=research/e8-eleven-hosting-selected /path/to/ADDRESS-MAP.patch
```

The offline verifier needs Python 3.11+ and only the standard library:

```sh
python3 -B research/e8-scalar-address-cache/verify.py
```

It checks original Git/SHA/license/receipt bindings, patch scope and composition,
all operand and complete replay results, and two focused contract tests for
address boundaries, cache freshness, invalid operands and a missing private
endpoint. Default validation does not repeat timing or any full supplier run.
Add `--benchmark` for a new measurement of the extracted section, optionally
with `--output /absolute/path/to/new-result.json`.

The exact measured driver is preserved under `evidence/adapter`, including its
original temporary input paths. It is an execution record; the portable verifier
uses the bundled source and fixtures. Original notices and license are retained.
