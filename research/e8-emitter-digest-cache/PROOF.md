# Exact byte preservation

The pinned emitter produces integer lists of four forms: op0 and op1 contain
six fields; op2 and op3 contain seven. For op0 it hashes the JSON array
`[op, owner(x), *z[2:]]`. Otherwise it hashes
`[op, owner(x), owner(y), *z[3:]]`, with the existing private-owner descriptor
when y is at or beyond LOCAL. Both tails are nonempty. The encoder checks this
schema before compiling a stream and checks operand indices during encoding.

With `json.dumps(..., separators=(',',':'))`, a list is an opening bracket,
the JSON encodings of its elements separated by commas, and a closing bracket.
Replacing an owner element by its cached encoding therefore preserves its
bytes. Each integer tail is encoded by the same JSON function once, with only
its opening bracket removed; its closing bracket is retained. The opcode is
an integer 0..3, whose decimal encoding equals JSON's encoding. Concatenating
these pieces with the same separators and final newline reproduces the exact
original record. Nested owner syntax and string escaping remain the JSON
encoder's responsibility. No rank-only or digest-only substitute is used.

The original emitter constructs its local streams before ownership expansion.
Those streams stay unchanged throughout the loop, and each invocation builds
a new owners list which is not mutated while consumed. Thus cached values are
valid for their full lifetimes. The helper recreates the owner/private cache
for every invocation; it does not reuse an earlier call's owner descriptors.

The patch strictly zips the original events with their encoded records. It
preserves the original paid-rank increments and event counter. Since the same
bytes enter the hash in the same order, the complete digest is identical.
Normalizing only the added helper import, compilation assignment and changed
hashing loop yields an AST identical to the entire original emitter. All other
ownership, restoration, scalar, geometry and invoice checks are retained.

The offline audit extracts the exact original and patched loops from their
pinned source ASTs; it never imports either supplier module. It compares every
actual record byte and independent aggregate digests on all 144 calls of two
source-bound completed fixtures. It also compares event counts and the loop's
paid local-instruction profile. That profile does not include later idle-child
or global-invoice additions; those unchanged statements lie outside the patch.

The setup-inclusive benchmark validates the same digests, counts and profiles
on every trial. Its speedup is an implementation result for this extracted
hashing loop and these workloads. It establishes no whole-wrapper speedup,
new mathematical supplier admission, numerical exponent improvement or reduction
in the mathematical finite-cost coefficient.
