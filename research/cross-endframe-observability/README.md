# Cross-endframe observability in the PR2979 word

**Claim: no κ improvement.** This package finds an exact eligible linear form only by pooling outputs from incomparable rank-seven terminal subspaces. It does not identify a consumer, realize a new helper, provide a complete invoice, or change the selected result.

## Result

The pinned `WORD-base` and `WORD-extra` providers from [the joint-endframes package](../rank7-joint-endframes/README.md) each have 49 observed rank-seven endpoint classes (104 terminal registers) and 126 rank-eight classes (336 registers). An independent exact reverse-adjoint checker examines every rank-seven class individually, every pair whose join has rank eight (413 pairs), every triple whose join has rank eight (2,571 triples), and every rank-eight endpoint class individually.

No single rank-seven or rank-eight endpoint exposes an eligible input form. Exactly one pair of rank-seven classes has a nonzero eligible readout among all 413 rank-eight joins. Exactly one of the 2,571 triples does too; it is the same pair plus a third class whose coefficients are zero. The unique readout is

```text
-out[7] - out[232] + out[236] + out[238]
 = 1/2 * (-h224 + h227 - h229 - h231 - h232 + h233
         -h234 + h235 + h236 - h237 + h238 - h239 - h276 - h292).
```

All 497 protected initial columns and every nonempty formal warp word cancel exactly. The result has support on 14 eligible initial coordinates. Removing any one of the four terminal readouts removes the eligible signal. The identity and the bounded census agree on both word orientations.

The effect lies outside the fixed-single-endpoint scope of [PR #3172](https://github.com/CrocSwap/integer-mult-bounds/pull/3172): pooling the two incomparable rank-seven spaces reveals a form that either space hides alone. It is also distinct from [PR #3178](https://github.com/CrocSwap/integer-mult-bounds/pull/3178)'s fixed-U12 screen. These scoped statements do not imply a general endpoint or architecture barrier.

## Reproduce

The checker uses only the Python standard library. From the repository root:

```sh
python3 -B research/cross-endframe-observability/verify.py
python3 scripts/research_package.py --package research/cross-endframe-observability --check-only
python3.12 scripts/research_package.py --package research/cross-endframe-observability
```

The two compressed word inputs are hash-pinned in `SOURCES.json`. `verify.py` independently reconstructs the frame census and the non-target formal-polynomial maps; it does not import the predecessor producer or verifier. Its exact checks include the pair/triple search, orientation agreement, the complete witness coefficients, and four controls that delete each readout in turn.

## What remains before κ can change

This identity is an information result, not a supplier. A caller must accept the 14-coordinate linear form; the circuit must deliver it with an actual register or a direct readout contract; and the full synthesis, rank-eight storage, restoration, physical and recursive costs must be charged. Without that work, the rank histogram and κ remain unchanged. The current selected κ is still 0.001672660197076918. The conditional 0.0017290339826465… claim in the predecessor package is not selected, and this result does not exceed it.

## Open next questions

1. Can a named downstream caller consume the four-register readout directly as one helper? First write its exact input/output and dirty-state contract, then price synthesis, storage, restoration and the recursive profile. The blocker is that no current caller accepts this linear form.
2. Do sparse rank-nine pools expose more useful directions at tolerable cost? First search the exact nuisance kernel while minimizing register and endpoint support and recording the join rank. The blocker is that no complete cost model prices a rank-nine pool.

## Credit

This scoped follow-up uses the two PR2979 word providers and preserves their attribution in the predecessor package. New analysis and checker prepared by OpenAI Codex with substantial AI assistance; no independent human or formal-kernel review is claimed. Apache-2.0.
