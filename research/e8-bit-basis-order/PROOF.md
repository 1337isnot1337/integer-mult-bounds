# Source-basis order and the finite coefficient

The parent is PR433 at 6d9244518175caf9e0089f92486959bc2c317273. This changes
only the choice and order of an invertible source minor in its R758 bit word.
It does not change a supplier saving, rank profile, helper count or exponent.

## The nine copied forms are identical

The original constructor replaces nine retained helpers with nine independent
binary forms in the 120 original source rows. It completes these forms to an
invertible source basis, emits a sequence T of elementary XOR additions,
copies the nine selected rows sequentially, and applies the literal inverse
T^-1 before the remaining program.

The three-line patch performs high-pivot elimination and assigns the nine
forms to the resulting pivot indices in descending order. Elimination still
proves that the completed 120-by-120 matrix is invertible. Its elementary row
operations realize exactly the selected matrix, and their reversed sequence
is its inverse over F2. The retained forms, in copy order, are exactly the
same nine forms as before. Only their source row names change.

Every changed scalar operation has the existing full frame. Each copy has the
same rank eight, gather/child/scatter lifetime and decoded target contribution.
No source changes during a copy episode. After T^-1, all source rows return to
their original values. The surrounding A prefix, B suffix, entire D and C
words, scatter lists, helper rows, frames and start/final labels are unchanged.
Thus the parent's arbitrary-helper compensator and cleanup remain valid.

The independent verifier checks these identities literally, reconstructs the
nine forms, and replays all 998 independent source/target/helper columns in
both orders. Removing the inverse or the dirty compensator is rejected. The
unchanged exporter and global checker also replayed the actual reflected
COPY/ERASE events with their private-work lifetimes. The source changes add
no geometric frame or phase pair; complex evidence is reused explicitly.

## Account for the complete finite cost

The forward basis has 575 additions instead of 559. Including its inverse,
the local word increases from 14,510 to 14,542 additions. This is not an
operation-count reduction. Both source orientations and all 72 invocations
retain their paid child profiles and stock.

The cancellation-free bound follows each emitted addition by
N[dst] <- N[dst] + abs(coefficient)*N[src], starting each live row at one.
Private copies inherit their source bound and erase it at the end of the
episode. The actual forward/reverse maxima change from 3,885,147/15,348,208
to 352,811/1,303,186. The verifier independently reproduces those values from
the literal words; the emitted-program checker also measured them afresh.

The nine-stage bound is P=2^18*forward^5*reverse^4. The 18 unchanged bridge
shears account for 2^18. Thus its bit length falls from 223 to 192.
All other scalar, selector, compiler, route, copy and stock terms are charged
as in the unchanged combined certifier. In particular, the 32 additional
local additions contribute 72*32 extra units; they are not omitted.

Recomputing the complete coefficient gives

    C = 4133102071585442738602693393898919077364732015670619884057.

With E=321480 paid calls, the two-level coefficient (C+1)^2*(E+1)^2 has
420 bits, down from 483. The final assembly conservatively retains its
256-bit payload and 512-bit two-level charges. The row coefficient remains
18,355 < 20,161. Both rational moments, all 47 outer inequalities, bootstrap
cutoffs and invalid-parameter controls are unchanged and pass.

This is a strict improvement to a finite overcharge on a pinned construction.
It is not evidence of a practical runtime speedup or a new numerical frontier.
The five tested minor/order choices establish no global optimality of this
basis. Newer reset/kernel words need their own reconstruction and validation
before this choice can be transferred. All inherited compiler, dirty-bank,
common-grid, restored-work, precision and analytic assumptions remain premises.
