# Product application review — 2026-10-15

Scope: two applications of the actual clean six-tape multiplication table, not a faster multiplication algorithm. No Jev was used.

## Checked result and limits

`IntegerMultiplicationProductApplications20261015.lean` adds nine theorems and two definitions. A fresh Lean 4.34.1 process checked its mechanically namespace-renamed scratch against the checked public bootstrap, with no diagnostics. Canonical SHA-256: `4a08d972a97b14e2ae3d12b61b424a6e047f8388d6e30f063664e3b129982809`; source/scratch hashes and compiler exit are in the retained local evidence ledger. Whole-package transitive-axiom auditing remains the release owner's responsibility.

1. `commonWidth a b = max a.size b.size` is proved to be the least width satisfying both operand inequalities, including zero width. Literal input-cell equalities identify each word as `Nat.bits ++ replicate padding false`; `minimal_width_product` gives an actual cleanMachine run and genuine halt for every pair of naturals.
2. `zmod_product` runs that same machine on the canonical natural representatives of arbitrary elements of `ZMod (2^n)`. Its physical output is the exact double-width natural product. Its ring label is the ring product; decoding the low n bits gives the canonical product residue. There is no physical truncation pass. `signed_residue_label` identifies signed integer input labels with Euclidean remainders, including negative inputs, and `signed_residue_product` proves the actual run's output label is the integer product cast to ZMod. No signed integer parser or free conversion procedure is claimed.

The statements use the verified conservative bound `280*n^2+322*n+122`. They do not establish the campaign's proposed tighter bound.

## Actual source comparison and attribution

The shared fresh PR inventory contains 1,898 PRs updated since October 14, through #2767. Main was refreshed to `8e22a9d9f621c72ab5b299061c2be4c7f638fd3c`. This is bounded freshness, not an exhaustive semantic novelty search.

- Current main's `formal/lean` tree was queried at that exact commit (40 entries, untruncated). The actual `README.md` and `KappaCheck.lean` were fetched and read. That project formalizes parameter/certificate arithmetic, frame/address/layout algebra and recurrence consequences, and explicitly leaves fixed-tape execution outside its scope. It is useful existing formalization, not an implementation of this six-tape multiplication interface. This inspection does not cover every main research package.
- PR #2235 at `e5a5d0651003e8774e98121250203b35c236b02b`: the actual `BinaryMultiplicationOriginABI.lean` was fetched and its input/output theorems read. `quadratic_origin_product` already supplies padded-operand multiplication with an origin MSB output. This campaign directly reuses that machine and arithmetic proof lineage. The product applications only select the least common width and specialize residue meanings after the campaign's cleanup extension; the basic multiplication result is not new here.
- PR #2439 at `4bbcd5ec320eff1deb0240fcc8a12e5919564741`: actual `PaidBinaryIncrement.lean` and `WidenedSourceDyadicAddition.lean` were fetched. Their `outputWord`, `output_value`, `output_length`, `machine_result`, `exponent_width` and `time_bound` implement paid overflow widening and dyadic half-source addition. This overlaps binary representation, exact halting and width accounting. Our minimum input width and ZMod labels do not implement that widening or replace its paid transitions.
- PR #2636 at `c1e173b7af38603bc7660a8829e75006e93645d3`: actual `tapes.py` was fetched and the counter/tape/scan operations read. It physically pads or restricts five-coordinate aggregates, meters cell operations, and restores heads and owned work. Our literal zero padding is an initial input ABI equality. It supplies no competing physical padding implementation or aggregate complexity result.
- Mathlib `Nat.size_le`, `Nat.size_eq_bits_len`, `Nat.bits_append_bit`, `ZMod.natCast_zmod_val`, `ZMod.val_mul` and `ZMod.val_intCast` provide the reused standard representation/residue facts. The short `bitsValue_nat_bits` proof follows Nat.binaryRec' and the existing project binary-power pattern. No claim of mathematical novelty is made for these elementary facts.

Fetched PR source paths, exact raw commit URLs, Git blob IDs and SHA-256 hashes are retained in the retained local evidence ledger; current-main source bytes and the exact tree response are retained beside it. Sources were inspected, not independently replayed. Credit the existing package's arithmetic/compiler/serializer authors and retained upstream/Mathlib attribution. No new kappa, selected-frontier change, subquadratic bound, or completeness for TI = TI_SL follows.


Final package verification supersedes these preliminary per-worker checks; see VALIDATION.json.
