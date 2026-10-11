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

## Transfer after a frozen upstream selection

The same argument holds when the source-basis block follows earlier resets or
kernel transformations. Let T be the explicitly delimited source-only suffix
of A, and require that B begins with its literal inverse. Recover each copied
form by applying T to formal unit source rows. The new basis T' realizes those
same forms in the same copy order. Therefore T', copy, T'^-1 induces the same
source-to-target linear transformation as T, copy, T^-1 for every state
entering the block, including states correlated with dirty helpers.

The postprocessor uses the actual input block and its copied forms. It requires
all basis operations at the existing full frame and preserves the set of
source rows touched by the block. Thus each affected source reaches the same
full frame, with the same rank increment; subsequent full-frame operations
add no paid frame move. Each selected copy is checked to occupy that frame.
The surrounding word, retained-form order, scatter, helper state, frame data,
and start/final labels are untouched. This algebraic argument does not replace
the supplier's legality, integer-span, ownership, or finite-invoice checks.

PR438's 11 resets and 118 kernel entries were first reconstructed with their
original input/output hashes and controls. The postprocessor then produced
word 2be5d42a53e367648f4dd33fd4a368c61e1565f0cf7c48bfe887ca953a735063
from the original post-kernel word cc6242d90ccdd8477521ea16f35ee2667dbe6c48cc60c6e4e9bcf6460497b233.
The unchanged integer-span replay gave the same local paid histogram; both
literal orientations restore all 987 columns. The original kernel receipt
continues to identify its original output, and BASIS-STAGE.json binds the
separate transformation. No upstream selection or receipt was repinned.

The fresh emitted-program verification measures prefix maxima 352,915 and
1,686,810, versus 4,749,873 and 18,976,454 from the original word. Both words
have the same 727 banks per stage, 14,223 live and 14,232 physical families,
328,536 paid calls, rank deficit 2,496, and row coefficient 18,355. The local
addition counts are 14,725 and 14,757. With all extra additions charged, the
candidate coefficient is

    C = 11618636861972555523343873296287586172648663760810665400081.

Its 193-bit coefficient and 423-bit two-level coefficient strictly improve the
algebraically reconstructed baseline's 226 and 488 bits. The baseline uses the
same verified schedule/geometry and its own literal prefix and addition count;
there was no second baseline global run. The fresh candidate's unchanged
combined certifier passes both moment engines, all 47 strict inequalities,
eight bank controls and four outer controls. The 256/512 conservative charges
and κ are unchanged. The completed PR433 complex receipts are reused as a
separate component: compared scientific sources match except the phase guard
and receipt representation, whose actual canonical gzip/payload and recipe
hashes satisfy both versions. This is not a fresh PR438 complex replay.
