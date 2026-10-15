# Selected BIT caller: fixed roles, parked banks and finite returns

I give a source-level fixed-tape lowering of the all-size p=1 caller in
[David Arias's PR2753](https://github.com/CrocSwap/integer-mult-bounds/pull/2753).
The construction uses permanent stream roles, two shared numerical banks, one
parking stack and a serialized finite return label. Under the pinned caller's
input and root-coupling hypotheses, I prove an O_q(V_root)+F_q physical reserve
and retain its O_q(V(n+w)) local toll. See [PROOF.md](PROOF.md).

The executable contribution includes:

* The actual PR2753 Frame integration with one bank pair, including child grants,
  matched restoration and cleanup after constructor/deeper-child failure.
* Stream-role serialization on the same PR2635 parking tape, a finite residual
  return cursor and a protected result port through 1500 nested returns.
* A complete 9216-address GL2 recursive payload check using shared numerical banks.

I specify the whole caller as a finite macroprogram and prove its source
refinement. I have not generated a whole-caller transition table or executed the
complete selected GL64 payload through that controller. The GL2 check retains
the logical payload scheduler. The code checks therefore support distinct parts
of the construction; they are not a formal verification of the full theorem.

I retain p=1, the stronger H2 primitive obligations and the outer borrowing
wrapper boundary. I make no exponent improvement or supplier-admission claim.
I leave the selected frontier unchanged.

## Reproduce

Use Python 3.12 and the standard library, from the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/selected-bit-physical-caller
```

The registered suites authenticate the complete frozen source inventory and
its transitive repository inputs before execution. They run the new controls
with normal and optimized Python, then run the complete small recursive payload.
See [VALIDATION.md](VALIDATION.md) for scope, commands and observations.

## Attribution and overlap

Jose Manuel (`jmbarrancoml`) contributed this lowering and integration, with
substantial OpenAI Codex assistance in mathematics, code and verification. I
claim no independent human or proof-assistant review.

David Arias supplied the all-size logical caller, stock/endpoint induction,
linear-sign repair and complete logical reserve in PR2753. I reuse my numerical
codec from [PR2769](https://github.com/CrocSwap/integer-mult-bounds/pull/2769).
ywz65 supplied the finite two-tape parking controller in
[PR2635](https://github.com/CrocSwap/integer-mult-bounds/pull/2635).
[SNAPSHOTS.json](SNAPSHOTS.json) pins the 97 unchanged exported files and their
original Git paths. Those exports retain predecessor notices, including the
earlier routing, directory, residual-lifetime and selected-source work.

I coordinated this scope in
[Discussion2319](https://github.com/CrocSwap/integer-mult-bounds/discussions/2319#discussioncomment-18958887).
The numerical lifetime audits in PR2781/2796/2801, the ordered-shear machine in
PR2776 and the separately claimed outer wrapper address complementary boundaries.
I do not incorporate their pending claims as proof dependencies.

## Open next questions

* Generate the complete controller from the finite block specification and run
  a small payload through it. Start by assigning the canonical ports in PROOF
  sections 2–6; the current executable GL2 replay still uses logical generators.
* Replace the retained O(wV) route/leaf routines with the required H2 primitives.
  Price the actual source-bound coefficient and movement paths; the present
  physical lowering retains the p=1 baseline.
* Join the physical reserve with the outer stock wrapper. Coordinate with its
  active author and track all padding, restoration and preparation charges.

The structured scope, overlap checkpoint and next steps appear in
[TASK.json](TASK.json). This contribution follows the repository's Apache-2.0
license and preserves the frozen sources' notices.
