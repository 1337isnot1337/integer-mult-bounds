# Compact supplied programs on five tapes

This is an author-written proof. Independent human and formal proof-kernel review are unclaimed. The mathematical statement is for every finite program. The executable admits at most 4,096 wires and 200,000 program symbols.

## Contract and machine model

Let A>=1, G>=0 and Q>=1. A topological AND/XOR circuit has constants numbered 0 and 1, A input wires numbered 2 through A+1, gate j at c_j=A+2+j, and Q ordered output wire indices w_t. Each gate operand a_j,b_j is smaller than c_j. Put B=A+G+2 and H=ceil(log2 B). Let h(w)=max(1,bit_length(w)).

The supplied immutable program is `^`, then the G gate rows, then the Q output rows, then `$`. A gate row is opcode A or X followed by two operand fields. An output row is opcode O followed by one operand field. A field is the canonical least-significant-bit-first binary encoding of its index followed by `#`. Zero is `0#`. The last bit of any longer field is 1. Its complete length is

    L = 2 + sum_j [3+h(a_j)+h(b_j)] + sum_t [2+h(w_t)].

The five tapes are program P, borrowed address X, private wire values W, private binary counter C and returned header Y. X initially contains `^`, its A bits in physical MSB order, then `$`. P and X start at their first symbols. W, C and Y start blank. The allocated extents are exactly

    P: L,  X: A+2,  W: B+2,  C: H+3,  Y: Q+3.

One read, write or unit head move costs one primitive. The finite alphabet is the fixed union of program opcodes, bits, markers and blank. Finite state holds the current opcode, at most two Boolean operands and a Boolean zero-test flag. It never holds a numerical wire index. The Python list backs a tape; executed accesses use only Tape.read/write/move at its head. Host admission, binary encoding, allocation, instrumentation and final observation are outside this primitive invoice. Host loop bounds are safety guards derived from allocated extents. The successful control path terminates on tape markers and counter zero, so it does not use those bounds as an uncharged address oracle.

This is a sequential machine-model implementation, not a lowering into the repository's production tape library. Host admission checks the complete input before constructing tapes. There is no rollback promise for interruption, external mutation or an injected fault after execution starts. Private storage is initially blank rather than arbitrary dirty workspace.

## Binary access lemma

To fetch wire w, load its h=h(w) supplied bits into C between `^` and `$`, returning C's head to its origin and advancing P past `#`. W starts at its origin. Move W once to constant-zero position. Test C for zero by scanning all h bits to `$` and returning to `^`. If nonzero, subtract one with a low-to-high borrow ripple, return C to `^`, and move W one cell right. Repeat until zero. Read the wire bit, return W to `^`, and erase the complete C prefix including its markers.

After k decrements, C represents w-k in exactly h cells and W is at position k+1. Ordinary binary subtraction proves this invariant. The process stops after exactly w decrements and w+1 zero tests. Thus it reads precisely wire w, returns W's head, blanks C and returns its head. Every access is finite. The last accessible wire has position B, with an additional blank cell at B+1. The counter's largest written position is h+1, followed by a blank cell at h+2. Both fit their allocated extents.

The exact costs, counting each terminating marker read, are:

| Part | Exact primitives |
|---|---:|
| Load P field, including `#` and advance | 2h+2 |
| Construct and return C after load | 4h+6 |
| Each full zero test, including return | 4h+5 |
| Decrement positive integer k, including return | 5v2(k)+6 |
| Move W to w, read, return | 3w+5 |
| Erase C, including markers and head return | 5h+11 |

For the decrement row, if t=v2(k), there are t zero bits before the first 1. The decrement uses 2t+3 reads, t+1 writes and 2t+2 moves. For any nonblank prefix consisting of `^` and n following symbols, erase uses 2n+3 reads, n+1 writes and 2n+2 moves, or 5n+6 primitives. Substitute n=h+1 for C.

The elementary identity sum_(k=1)^w v2(k)=w-popcount(w), including w=0, follows by counting multiples of 2,4,8,... or by the binary expansion of w. Adding all rows therefore gives the access bill

    F(w) = 15h(w)+29 + w[4h(w)+19] - 5popcount(w).

No constant-time binary subtraction is assumed. Every tested/decremented bit and every return traversal is charged.

## Circuit correctness and return

Initialization writes the two constants and the borrowed input into W. Its nonblank prefix is `^` followed by the A+2 initial wire values. Induct on j. Before gate j, all earlier wires have their circuit values, and all heads used by fetch are at their origins. The access lemma returns a_j and b_j. Finite-state AND/XOR computes the right bit. Scanning to the first blank appends it at c_j+1, then returns W's head. This proves the invariant for the next gate. Each output access then returns its designated circuit bit, appended to Y in order. The final program marker writes Y's `$` and returns Y's head.

After all outputs, W has exactly B bits after `^`; erasing that prefix blanks every W cell. C is blank after every access. P is rewound after its final `$`. X was never written and was rewound during initialization. P was never written. Therefore the result is exactly the circuit output, both borrowed tapes are preserved byte for byte with their heads at zero, both private tapes are wholly blank with heads at zero, and the output head is zero. The finite verification includes constants, repeated operands/outputs, no-gate programs and nontrivial borrow chains; induction supplies the universal claim.

## Complete invoice

Initialization costs 8A+18. Appending gate j after its two accesses costs 4c_j+9, including its opcode read/advance. Each output costs F(w_t)+4, including its opcode read/advance and bit write/advance. Interpreter setup, terminal-marker handling and output return contribute 2Q+8 outside those rows. Final W erasure costs 5B+6, and final P return costs 2L-1. Hence total executed primitives are exactly

    T = 8A+2Q+5B+2L+31
        +sum_j [4c_j+9+F(a_j)+F(b_j)]
        +sum_t [4+F(w_t)].

All allocated finite-alphabet tape cells, including borrowed program and address, output, markers and spare blanks, total exactly

    C_total = L+A+B+Q+H+10.

Since w<B and h(w)<=H, F(w)=O(B log(B+1)). Thus

    T = O((G+Q+1) B log(B+1)+A),
    C_total = O(A+B+Q+(G+Q+1)log(B+1)).

These bounds do not include an accumulated output stream. Reusing the machine for many headers still requires a charged address producer and consumer. Input encoding is supplied; this proof does not execute a compiler from shape descriptors or claim that compiler's cost is zero.

## Synthetic exponent specialization and boundary

The three authenticated canonical inputs in SOURCES.json are actual runtime or mathematical premises. The retained circuit.py supplies the topological AND/XOR circuit. Its PROOF.md derives the physical named-slot order and combined exponent from the retained transform source and proves its exact circuit/gate bounds. We use that all-size theorem as a premise, rather than inferring it from finite evaluations here.

For ell>=2, each axis has ell or ell-1 address bits. In round h, the circuit has A=sum_i a_i inputs and Q=ell+1 outputs. When h>=1 and d_h>0, G=d_h(6h+5), plus 3(h+1) in the forward direction. When h=0 or d_h=0, G=0. Its output encodes the source combined exponent modulo 2^(ell+1), with the opposite sign in the opposite direction. The general theorem above executes those exact outputs. Under d*ell=O(p), A,B,G,Q=O(p), so this is an executed O(p² log(p+2)) primitive, O(p log(p+2)) cell implementation for a supplied compact program and physical address.

PR3534 used a supplied unary-index program with O(p²) program/cell storage and O(p²) primitives. The changed binary format restores the compact storage bound in PR3522's written scan simulation, using five fixed roles and paying a logarithmic time factor. This is a local control-storage improvement, not a universal strict decrease for every tiny circuit or a new algorithmic asymptotic bound. The exact comparison sources are retained separately in comparisons/ and COMPARISONS.json. They are not proof premises or runtime imports of this machine.

For fixed 0<epsilon<1, positive a_r,b_d, d<=b_d*p^epsilon and r>=2^(a_r*p/d), r dominates every fixed power of p. The polynomial header bound fits O(rp) eventually under those source comparison bands, with no explicit numerical cutoff supplied. This conditional absorption is not the complete caller cost.

Encoded shape/topology production, enumeration of physical addresses, movement and consumption of header packets, signed data/layer composition, complete spectator/buffer/head costs, native/root/ordinary refinement, outer recovery and all supplier/theorem obligations remain open. No selected frontier or kappa change follows.
