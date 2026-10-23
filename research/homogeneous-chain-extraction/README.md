# Optimal two-call extraction from odd homogeneous chains

**Conditional operator theorem, author-checked; no new kappa or native supplier.**
For every odd n=2m+1>=3, a homogeneous chain U_n=I+Q J_n and its actual raw
inverse transpose can deliver n-1 independent Q jobs and restore one arbitrary
spectator with two calls. Every boundary uses only scalar mixing and the global
monomial P=Q^2. The explicit reversible circuit uses 5m-2 scalar ADDs, m swaps
and 3m signed-P scales, as field macros. For n=5 this is four Q jobs from two
calls, with eight ADDs, two swaps and six scales across all boundaries.

This extends the three-field conditional identity in Cinna Davis's
[PR4698](https://github.com/CrocSwap/integer-mult-bounds/pull/4698), whose frozen
source/proof are pinned in [SOURCES.json](SOURCES.json). The proof also shows
that no two-call word in the scalar/global-P ring can produce more than n-1
independent Q jobs, even with arbitrary restored dirty workspace. The count
must be even, giving only an upper bound n-2 for even n. This bound excludes
broader physical monomial/address operations and does not apply to every
isolated small tensor width. The identity itself holds at every positive width.

[PROOF.md](PROOF.md) gives the all-length construction, the restricted optimality
proof, its width qualification and the complete conditional moment ledger.
[verify.py](verify.py) checks all independent inputs symbolically over
Z[q]/(q^4-1) for odd lengths 3 through 31, every boundary count, six semantic
mutations, 256 finite dirty-workspace rank fixtures, and the tensor-width
qualification. These finite checks supplement the written proof; they do not
prove physical realizability or certify a multiplication algorithm.

## Budget and expansion decision

With n transverse rank-b main fields per provider, autonomous helper moment H_t
and complete paid moment P_t, the two-call surplus is

    2 H_t + (n-1)(2b+1)^t + (2b)^t - 2 P_t.

Writing E=P_1-H_1-nb, the C=0 rank surplus is (n-1)-2E. A new physical offer
therefore needs E<(n-1)/2 merely to pass this necessary rank test. Directly
building the chain from its n-1 unary queries loses at least n-1 moment units
for every 0<=t<=1 with b>=1. Longer chains alone do not repair that bill.

**Decision: retain the proved module; stop direct unary synthesis.** No native
expansion is warranted until a named changed provider has a complete favorable
budget. The retained-center source has heterogeneous charts and incoming helper
noise, as recorded in [Discussion4840](https://github.com/CrocSwap/integer-mult-bounds/discussions/4840).
No native homogeneous offer is obtained from its scalar Jordan chains.
Acquisition, actual chart maps, dirty restoration and independent helper targets
are unknown for the proposed longer chain. Physical movement/precision,
completion, compiler, BIT and outer recovery remain unrun and unpriced.

## Reproduce

From the repository root, using only the Python standard library:

```sh
python3.12 -I -B research/homogeneous-chain-extraction/verify.py
python3.12 -I -O -B research/homogeneous-chain-extraction/verify.py
python3.12 -B scripts/research_package.py --package research/homogeneous-chain-extraction
```

[RESULT.json](RESULT.json) is deterministic and must match replay. No Lean,
Docker, all-history suite or selected-frontier replay is required for this
scoped theorem. The selected conditional kappa remains 0.00302015. See
[TASK.json](TASK.json) for the exact base, original assignment, overlap boundary,
claim, and explicit expansion gate. Upstream and frozen predecessors are unchanged.

## Open next questions

- Can an actual changed native provider supply even one five-field homogeneous
  chain with excess E<2, arbitrary spectator/helper restoration and a positive
  full moment? Begin with its literal source/target chart contract and complete
  two-orientation invoice; stop on an unfavorable optimistic bill. No provider
  meeting this allowance is identified here.
- Is the even-n upper bound n-2 attained by two full calls to the same even
  chain in this ring? Begin with n=4 and arbitrary free middle boundaries.
  The odd-chain construction and the upper bound do not answer that question.

## Credit and scope

Cinna Davis / 1337isnot1337 supplies PR4694's coupled retained-center extension,
PR4698's helper normalization and conditional three-chain consumer, and the
PR4440/4470 controller lineage. Retain Cao Yifan / intqwq, zxv, Jacob Alan
Sussman, Ryanson Jonathan and all cited native/compiler/precision predecessors.
Their actual native construction is not replayed or modified here. The new
contribution is the longer odd-chain proof/circuit, restricted workspace bound,
and explicit acquisition allowance. Prepared for Cinna Davis with substantial
OpenAI Codex assistance. Apache-2.0. No independent human or proof-kernel
acceptance is claimed.
