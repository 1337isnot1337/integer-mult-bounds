# Physical applications: checked scope and source comparison

The canonical source is the canonical development source. Its mechanical public translation passed Lean 4.34.1 with `-j1 -DmaxHeartbeats=4000000`, exit 0 and no diagnostics. This is a preliminary module check against the hash-bound bootstrap imports; the final independent whole-package audit remains the root worker's responsibility.

## Exact applications

1. `EndpointAdapters.fixes_designated` proves that any fixed physical tape permutation fixing a designated tape retains its entire head/cell endpoint. In the multiplication specialization, `outputPermutation` is the accumulator/sumReverse swap, fixing both multiplier and multiplicand indices. `unchanged_input` proves equality with the original complete `cleanInput`, using the original blank work tapes. The input operands are preserved by this adapter; the actual multiplication computation itself consumes them, as its original clean contract specifies.
2. `EndpointAdapters.lift_iterate` obtains exact executable Option-iterate transport from `TapeEmbedding.lift_step` and Mathlib's existing `Function.Semiconj.iterate_right`. `accumulator_product` applies the existing actual clean multiplication execution to the statically compiled table. It accepts the literal unchanged input, halts genuinely, and returns the padded MSB product at accumulator origin. The other five tapes are globally blank. Actual endpoints are retained: the former accumulator's head at minus twice the width is now on sumReverse; it is not reset for free. The currently stated bound is the already checked conservative `280*n^2+322*n+122`.

The permutation compiles a fixed finite transition table before execution. It is not a runtime tape-data swap with zero claimed charge. No unknown arithmetic routine is assumed.

## Reuse and overlap

Mathlib's [Function/Iterate.lean](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Logic/Function/Iterate.lean) already proves `Function.Semiconj.iterate_right`; the pinned local Mathlib source was inspected and that exact theorem is applied. Credit Yury Kudryashov (2020), Apache-2.0. Neither semiconjugacy nor iteration transport is claimed as new mathematics. The project `TapeEmbedding` supplies the one-step tape compilation and generic run/halt preservation; this file specializes those existing results rather than replacing their proofs.

Fresh API metadata, complete changed-file lists, and actual raw sources were fetched with verified TLS using `node --use-system-ca`, without configuration changes. Inspected comparisons:

- [PR2418](https://github.com/CrocSwap/integer-mult-bounds/pull/2418), head `ddaf7234581133ec0c15496f4dfc65570aef401c`: the actual `PositionalMetadataReturn.return_exact` and `PaidPairedTrackAcquisition.machine_result/time_eq` prove paid symbol traversals, source preservation and return in a paired-symbol zipper model. Credit James Chang with OpenAI assistance and the retained prerequisite chain. These are substantial endpoint/return suppliers. This application performs static table renaming and no runtime home-return operation; it does not replace or improve those traversals.
- [PR2438](https://github.com/CrocSwap/integer-mult-bounds/pull/2438), head `3e4399b276d663f8716b17c7758b597f96503675`: actual `ReusableDyadicOutput.machine_exact`, `machine_result`, and `output_representation` compose charged output extraction and sign separation while retaining the prior dyadic endpoint. That is concrete arithmetic output adaptation, so generic output-adapter novelty would be false. Its datatype, marked numerator/exponent ABI, and executed copy/split phases differ from this fixed six-tape multiplication permutation. Its source header/prerequisite attribution remains authoritative; no source was copied here.
- Recent [PR2635](https://github.com/CrocSwap/integer-mult-bounds/pull/2635), head `1662dda699d9ea57b3fb13a23873b087d765149f`: actual `machine.py` has a 10-state, two-tape finite controller whose table selects only from state/scanned symbols; `PROOF.md` proves properly nested packet parking and restoration with charged unit moves. Credit ywz65 with OpenAI Codex, Apache-2.0. This is strong overlapping finite-table/physical-endpoint infrastructure. Our application does not implement parking, borrowing, dynamic tape routing, or arbitrary in-place permutations.

Root refreshed upstream main to `8e22a9d9f621c72ab5b299061c2be4c7f638fd3c` and retained 1,898 recently updated PR metadata records. The three comparisons above inspect actual sources, not only titles. Coverage remains bounded; no claim that nobody has applied these techniques, no complete semantic search, and no priority claim follows. This physical review does not independently rebuild the older PR environments.


Final package verification supersedes these preliminary per-worker checks; see VALIDATION.json.
