# Smaller finite overcharge from source-basis ordering

A three-line source-minor ordering change reduces the finite coefficient of
the pinned [PR433](https://github.com/CrocSwap/integer-mult-bounds/pull/433)
bit construction from 223 to 192 bits, and its two-level coefficient from
483 to 420 bits. It adds 32 local XOR additions, which are fully charged.
The saving comes from a lower cancellation-free prefix bound.

**The supplier caps and multiplication exponent are unchanged.** This is a
finite-accounting improvement, not a practical speed benchmark or a claim to
the current numerical lead. Newer supplier proposals report higher exponents.

The selected change is `basis-order.patch`; PROOF.md proves equivalence of the
nine copied forms and explains the cost comparison. It preserves every frame,
rank, helper count and surrounding scalar operation. Five deterministic
minor/order choices were screened; global basis optimality is not claimed.

Run the self-contained standard-library audit:

```sh
python3 -B research/e8-bit-basis-order/verify.py
```

It checks package/source bindings, both literal 998-column orientations,
inverse/dirty-compensator rejection, exact prefix growth, all finite invoice
terms, and the retained five-stage verification receipts. It does not rerun
the global construction or Gaussian phases.

The actual changed-component run used the unmodified pinned exporter, global
checker, independent audit, price engine and combined certifier. All five
stages passed. The complex component receipts were reused from the completed
source replay. That run and the independent audit retain all source/output
hashes, stage logs and exact coefficients.

The source package is pinned to commit
`6d9244518175caf9e0089f92486959bc2c317273` in
[`icekylinx/integer-mult-bounds`](https://github.com/icekylinx/integer-mult-bounds/tree/6d9244518175caf9e0089f92486959bc2c317273/research/split-centres-global).
`reproduce.py --source /path/to/that/package --check-inputs` validates the
portable reconstruction inputs without rerunning the scientific stages.
Use `--output /absolute/path/to/new/output` instead to reconstruct the candidate
and replay the five changed-bit stages. Original package bytes are preserved.
The portable wrapper has input-only validation; the completed scientific run
used the separately retained driver described in VALIDATION.json.

All conditional supplier/compiler/common-grid/precision/analytic interfaces
remain assumptions. Transferring this choice to later reset/kernel words
requires fresh reconstruction and verification, not replacement of a hash.
Original contribution notices and licenses are preserved.

## Reusable postprocessing after reset and kernel stages

`postprocess.py` now derives the copied forms from the actual input word and
constructs the reordered basis. It does not contain a hardcoded PR433 basis.
For a compatible word with an explicitly delimited, full-frame source basis:

```sh
python3 -B research/e8-bit-basis-order/postprocess.py original.json candidate.json
python3 -B research/e8-bit-basis-order/test_postprocess.py
```

The output must be a new file. The tool checks the original literal inverse,
source-only operations, independent copied forms, and the set of source rows
entering the full frame. It preserves its input. Its output is a candidate;
run the supplier's unchanged local, reflected, global, pricing and invoice
checks before using it. This ordering is not guaranteed to improve every word.

The `port438` evidence applies this tool **after** the original reset and
kernel checks in [PR438](https://github.com/CrocSwap/integer-mult-bounds/pull/438),
pinned at `e3b56de7869f6af88d48ac0ab1d7959c4c9e6176`. Their original selection
hashes and receipt remain intact. A separate basis-stage receipt binds the
new word. All nine changed-bit stages passed in one execution, including the
original global checks and combined certifier.

| Pinned construction | Finite coefficient bits | Two-level coefficient bits | Extra local additions |
| --- | ---: | ---: | ---: |
| PR433 R758 | 223 to 192 | 483 to 420 | 32 |
| PR438 R747 after resets/kernel | 226 to 193 | 488 to 423 | 32 |

For PR438, both supplier caps and κ = 45340333148791/40000000000000000 remain
unchanged. The candidate invoice comes from fresh emitted-program checks.
The baseline cost is reconstructed from its literally replayed word and the
unchanged geometry/schedule; its full global pipeline was not rerun.
Completed PR433 complex-component evidence is reused with explicit source,
canonical-word and recipe bindings. No new complex or phase replay is claimed.

The default `verify.py` also audits this port, the original/new word identities,
both 987-column orientations, actual prefix growth, complete finite invoice,
source pins, stage logs, and retained controls. `port438/adapter` preserves the
exact executed scripts and their original temporary paths as evidence; it is
not a portable CLI. The standalone postprocessor and audit commands above are
portable. `port438/VALIDATION.json` records these validation boundaries.
