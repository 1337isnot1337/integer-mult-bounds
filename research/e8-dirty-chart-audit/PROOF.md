# Required dirty endpoint and the missed conjugation

Let `u` be the vector of independent dirty helper inputs in their old charts.
Let `H` be the scalar helper-to-helper map of the main word. The prewhitening
bracket uses `P = H^-1` before entrance normalization. Let

```
D = diag(T_E^-1)
```

where an ungauged helper has the identity entry. Scalars commute with address
operators, but mixing helpers does not generally commute with their distinct
normalizations.

The original [PR390 proof](https://github.com/Dugongue/integer-mult-bounds/blob/0e790f2dfb64e17bdee154aee151bb0c1dddb28e/research/e8-prefix-restoration/PROOF.md)
performs the preconditioning at a common initial frame. Its pinned prefix word
has no entrance gauges and every helper starts at frame zero. That argument
does not establish commutation with later, distinct nontrivial entrance charts.
PR419's README inherits two-sided residual normalization and bank routes while
explicitly reopening phase and invoice work; its supplied proof does not give
a replacement coupled-bank invariant for this interaction.

Ordinary scalar replay sets all entries of `D` to identity and checks `HP = I`.
The normalized dirty endpoint of this bracket is instead `HDP`. The proposed
independent-helper residual assembly requires `D`. Therefore that assembly needs

```
H D H^-1 = D, equivalently D H^-1 = H^-1 D.
```

Zero clean-input content in a sink is not this condition. It does not establish
that the sink's dirty helper row is its own identity row, or that inverse helper
cleanup may be omitted there.

The checker first executes the supplied old response on independent scalar
columns. At `ad0`, it left-multiplies each gauged helper row by its `T_E^-1` tag.
It then executes the actual main and cleanup scalar events and compares against
the required normalized helper endpoints and prescribed target update. Clears,
copies, and private erasure are included. The existing phase/lifetime/geometry
checks are separate requirements; passing this endpoint check alone does not
establish them.

The replay uses formal tags as a sufficient identity test. A failed formal test
does not by itself imply an operator mismatch, because frame operators can be
linearly dependent. For a counterexample, the tool substitutes the pinned exact
Gaussian matrices and evaluates address basis vectors in order. A single nonzero
entry proves a mismatch. If all `2^h` columns of every coefficient operator
vanish, linearity proves that the emitted endpoint agrees on every input vector.
Repeated coefficient operators are checked once. This resolves formal
cancellations without assuming that distinct tags are independent.

For example, on three address axes the exact operator

```
T_[1,4]^-1 - T_[1,6]^-1 - T_[2,4]^-1 + T_[2,5]^-1
```

annihilates the basis vector at address zero. On address one it instead gives
`i*|4> - |6>`. Thus a zero result on the first address alone cannot certify
operator equality. The focused regression uses these actual canonical frames.

For both supplied PR419 words, the forward off-diagonal coefficient from dirty
helper 255 to helper 244 is `(I - T_[48]^-1)/4`. On the basis vector at address
zero, its component at address zero is `(1+i)/8`, which is nonzero. The backward
word has coefficient `(T_[3]^-1 - I)/2` from helper 420 to helper 246, with
component `-(1+i)/4` at address zero. These coefficients must be zero under the
required independent-helper endpoint contract.

Independent invertible input and output chart changes cannot remove a nonzero
off-diagonal coefficient: `L_i A_ij R_j = 0` implies `A_ij = 0`. This explains why
checking additional per-helper boundary adapters does not repair the discovered
gap. It does not exclude a different construction with explicit coupling between
helpers or banks and a separately proved route, phase, padding and cost model.

The retained admitted PR416+956 event stream passes the same chart-sensitive
replay in both orientations. Both failing fixtures pass the same replay with all
entrance operators collapsed to identity. These controls distinguish the missed
chart interaction from an ordinary scalar failure or an event-format mismatch.
