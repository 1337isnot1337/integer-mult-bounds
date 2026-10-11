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
