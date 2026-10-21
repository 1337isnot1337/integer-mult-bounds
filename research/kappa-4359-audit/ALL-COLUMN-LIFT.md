# Independent audit of the native column lift

The logical complex replay in PR #4359 supports the claimed column lift.
It does not use a matrix-sum identity that is silently tensor-powered.
This conclusion depends on the pinned physical frame and normalizer
identities. It is a mathematical review of that implication, not a formal
verification of the Clifford compiler or the full multiplication theorem.

The reviewed source is PR #4359 at
`da637c87c89482bc4c86be36bd0071b3d400dbed`.
The native word, free-word interpreter, phase certificates and original
closure argument belong to that PR and its attributed predecessors.
This audit adds the following explicit interpretation. New text is
Apache-2.0.

## Decoded coordinates

For an address frame `a`, write its physical invertible operator at column
multiplicity `f` as `E_(a,f)`. Interpret the current physical array in role
`r` as

```math
x_r=E_{a,f}y_r.
```

A paid frame transition from `a` to `b` applies
`E_(b,f) E_(a,f)^(-1)`, leaving the decoded array `y_r` unchanged.
This is why the interpreter updates the frame tag and paid histogram
without inserting a symbolic warp into the decoded array.

An ADD is accepted only when its source and destination have the same
frame. Therefore

```math
x_d\leftarrow x_d+\lambda x_s
\quad\Longrightarrow\quad
y_d\leftarrow y_d+\lambda y_s.
```

The coefficient `lambda` remains the same rational scalar for every `f`.
The role-level scalar circuit is not tensor-powered. COPY and CLEAR retain
their owned-storage restrictions and their explicit execution costs.

## The algebra actually used by the checker

The interpreter in
`research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py`
represents a decoded row as a finite rational linear combination of pairs
`(original input role, operator word)`. Its `warp()` prepends a signed
generator and cancels only an adjacent inverse of that same generator.
Backward, inverse-transpose warps use a disjoint generator family.

There is no commutation rule between distinct warp generators, no
idempotent-projector relation, and no rule replacing a sum of physical
operators by a new tensor-powered symbol. Equality of these reduced
free-group-algebra rows is valid after assigning arbitrary invertible
linear operators to the generators. In particular, assign the correct
`f`-column lift to each generator and its actual inverse to the negative
generator.

The full-identity reconstruction uses this checker in both directions.
It also runs a separate literal endpoint implementation on all 632
persistent input columns. The arbitrary helper inputs are represented by
their own original input variables. They are not initialized to zero.
An owned center is the only storage discarded by CLEAR, and it receives
no productive-output credit.

The underlying physical identity for a warp has the form

```math
V=E_b W E_a^{-1}.
```

Taking tensor powers preserves this product identity and the inverse
relation. The decoded scalar circuit then evaluates its unchanged linear
combinations at `W_f`. This is the relevant operation; the invalid formula
`(U+V)^(tensor f)=U^(tensor f)+V^(tensor f)` is never needed.

## Rank-zero maps and absolute phase

For a native monomial normalizer on one column,

```math
|x\rangle\longmapsto i^{a+q(x)}|Mx+b\rangle,
```

the lift acts separately on each of the `f` column blocks. Its phase is

```math
af+\sum_{j=1}^{f}q(x_j)\pmod4.
```

The constant phase is multiplied by `f`. Dropping it would invalidate
odd-column cases. PR #4359's closure note states this factor explicitly;
the recorded one-column recipes retain their absolute phases, and exact
product identities lift with these phases included. The fixed binary
address matrix becomes its block lift. Untouched blocks remain complete
spectator fields.

The same reasoning sends a rank-`r` paid transform to rank `rf`. The
uniform compiler's final rank-one calls therefore become rank-`f`
ordinary children. Remainder axes are completed separately and preserved
as spectators by the full endpoint.

## BIT qualification

The BIT lift uses rational projector identities over the future common
cover, rather than this free-warp implementation. Its statements are
polynomial product identities: projector idempotence, nested transition
relations, conjugacy and the product of a source projector job with its
complement. Replacing each head matrix by its tensor product with `I_f`
preserves those identities. The reversed tail pairing is retained.

The common external weight must remain independent of every fresh role
and cover field of the whole compiled invocation. A route changes only
those fresh fields, so it commutes with that weight. A weight depending
on the current fresh cover coordinate does not satisfy the premise.
The original delayed-cover audit includes a negative control for that
failure. Neither this review nor the new count census weakens that
condition.

## Limits

This argument extends authenticated local operator identities to all
positive column multiplicities. It does not establish native movement
costs, the semantic-precision recurrence, the outer analytic reduction,
or the primitive implementation of every permitted frame map. Those
remain the explicit inherited hypotheses of the conditional claim.
