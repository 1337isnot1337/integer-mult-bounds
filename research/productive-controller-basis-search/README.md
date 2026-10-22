# Changing the controller basis does not remove the smallest idle bill

**Scoped finite search; no new supplier or kappa.** We searched outside the
selected path controller: every call may act on arbitrary binary linear
combinations of four main fields, with arbitrary constant changes of basis
between calls and at both boundaries. For five query-bearing calls, three to
five of them full native calls with independent fresh multipliers, none of the
controllers without idle calls produces four independent Fourier jobs.

The search includes 1,680 conjugated native maps and 105 thin-query maps,
rather than only coordinate-pair calls or the existing path's bridge choices.
It uses safe finite-field rank pruning, then a separate exact polynomial
replay. All **12,480** surviving query cancellations fail the complete output
factorization: their coefficient-rank sums are at least six instead of four.
[PROOF.md](PROOF.md) defines the alphabet, proves the pruning/factorization
criteria and states precisely what the finite exclusion covers.

The motivating target is the productive-helper controller's large idle bill.
The selected #4470 construction is conditional kappa 0.00302015. Its local
helper/paid profiles and query-only interface are retained unchanged. This
experiment changes the controller topology/basis instead of optimizing another
fixed scalar contact. It is a negative checkpoint, not the requested larger K.

## Reproduce

Python 3.12+ and a C++17 compiler (`g++` or `clang++`) are required; no Python
packages or network access are needed. All binaries and search streams live
in a temporary directory. Run from the repository root:

```sh
python3 -B scripts/research_package.py --package research/productive-controller-basis-search
```

The hook recompiles and reruns all 16 masks and compares the exact receipt.
It checks all gate relations, a working six-call example, a wrong-query
control, a genuine five-call query cancellation that fails factorization,
and the false positive obtained by collapsing all fresh multipliers to one.
`--write` regenerates the receipt and is only an authoring option.

This does not run the selected cold supplier replay or an outer ledger:
no changed supplier passed the algebraic gate. There is no native admission,
formal-kernel acceptance, independent human review, new exponent or claim of
an all-length lower bound. In particular this binary exclusion is not silently
transferred to arbitrary complex dyadic boundary changes.

## Open next questions

1. Does a larger branching controller admit independent monomial outputs with
   fewer paid idle transforms? This four-field, five-call census does not
   answer it. First give the complete word and test coefficient ranks.
2. Can a changed output interface retain a rank-five/six coefficient pencil at
   a funded recovery price? Query cancellation alone earns no output credit.
3. Can a native local family make multiple ports share a query line, or reduce
   the copied-center debt? That changes a premise outside this enumeration.

Credit Cinna Davis's #4440/#4470 controller/helper work, zxv's productive
native/compiler construction, Jacob Alan Sussman's mixed-target recursion,
and the retained BIT, Clifford, precision and outer contributors. The current
#4602/#4603 diagnosis motivated changing topology rather than repeating a
fixed-window rewrite; #4623 studies a different border endpoint and recovery
model. New algebra, code and writing by Cinna Davis / 1337isnot1337 with
substantial OpenAI Codex assistance. No subagents. Apache-2.0.
