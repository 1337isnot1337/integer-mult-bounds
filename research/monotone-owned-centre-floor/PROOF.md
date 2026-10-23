# Sharp owned-wire floor with native and helper boundaries free

Cinna Davis / 1337isnot1337, substantial OpenAI Codex assistance; Apache-2.0.
Written scoped proof and exact finite witnesses; no new multiplication theorem.

## Statement and source

Use the exact persistent-field incidence, scalar opcode/coefficient/order and
owned lifetimes of Cao Yifan's round-three word in `SOURCES.json`, separately
in either orientation. Each scalar event has one common frame subspace in
F2^9 for its persistent operands. On each persistent L field, spaces increase
by containment between consecutive contacts with no intervening native warp.
Fix the main entrance and exit spaces. Free both helper boundaries, all contact
spaces and all native boundaries. Discard every relation across a native warp.

Then the following bounds are sharp:

1. Each of the eight high owned contacts has dimension at least eight. This
   first conclusion needs only the fixed main entrances.
2. Even if every scatter/gather contact moves and the owned C wire takes
   arbitrary intermediate subspace charts, each block pays Fourier rank mass
   at least eight, provided each owned transition is paid at its actual relative
   Clifford B-block rank. This includes nonnested canonical charts. It also
   includes general intermediate Clifford charts with the projected-subspace
   convention stated below. The conclusion requires fixed main exits as well.
3. The eight owned lifetimes therefore pay rank mass at least 64 and moment
   at least 8 times 8^t for every 0 < t <= 1. The original eight rank-eight
   jobs simultaneously attain these bounds.

No new CLEAR, COPY or borrowed scratch can be inserted into an owned lifetime
for free: the scalar word and its owned lifetimes are fixed. Every owned move
is charged. These statements do not optimize the remaining persistent paid
jobs or productive helper credits and prove no full-invoice optimum.

Matarener's [PR5060](https://github.com/CrocSwap/integer-mult-bounds/pull/5060),
`research/owned-centre-wire-floor/PROOF.md`, already gives forward/backward
interval propagation and the nested owned-path argument for #4470 with fixed
native and helper boundaries. Those lemmas and the original complete nested
floor are prior work. This package extends coverage to the newer round-three
word, removes all native relations and helper boundaries, and permits nonnested
owned moves through the projection-rank inequality. The canonical Gaussian
rank grammar is credited to Dugongue / PR4654 and its retained exact
implementation in `research/general-gaussian-contact-search`. This is an
extension of those results, not a claim to invent their elementary invariants.

## Entrance and exit path lemmas

Make one vertex for each persistent entrance, scalar contact and main exit.
Along each persistent field draw an edge from its previous entrance/contact
to its next scalar contact, and from its last contact to its main exit if
applicable. Both operands of a scalar ADD use the same contact vertex.
At every native warp cut the chain: its output is an independent new vertex,
and no edge crosses the warp. No helper exit or productive-target edge is
needed. Owned C transitions are not edges of this persistent graph.

Along a directed path every earlier space is contained in every later space.
Thus a vector at a fixed main entrance lies in every contact it can reach.
Eight independent such vectors force a contact's dimension to be at least
eight. Conversely a path from a contact to fixed main exit E forces that
contact into E. A linear functional annihilating E annihilates the contact.

These assertions use induction on the path length. No equation for a native
map or helper endpoint is involved. Physical frame incidence survives data
cancellation; a zero logical coefficient does not remove a common scalar
contact. Splitting the operand gauges requires a different paid scalar
interface and is outside the hypothesis.

## Relative rank and the owned-path bound

For a Clifford chart C, define its inverse zero Lagrangian as
L_C = C^(-1) Z, where Z = {(0,z)} in the binary symplectic space F2^(2n).
Write U_C for the projection of L_C onto its first n coordinates. This is the
subspace convention used by the retained contact/Lagrangian grammar. In
particular the canonical chart labelled U has projected subspace U.
The relative operator C_B C_A^(-1) has B-block rank

    r(A,B) = n - dim(L_A intersect L_B).

To see this, the kernel of its B-block consists of vertical vectors mapped
to vertical vectors. Applying C_A^(-1) identifies that kernel with
L_A intersect L_B. Rank-nullity gives the displayed identity. It also shows
that adjoint transitions have the same rank.

The vertical kernel of a Lagrangian with projection U is U-perp: isotropy
implies inclusion, and both have dimension n-dim U. Projection of
L_A intersect L_B is contained in U_A intersect U_B; its vertical kernel is
contained in (U_A+U_B)-perp. Therefore

    dim(L_A intersect L_B)
        <= dim(U_A intersect U_B) + n - dim(U_A + U_B),

and consequently

    r(A,B) >= dim U_A + dim U_B - 2 dim(U_A intersect U_B).

Canonical zero-form charts attain equality, as in the retained Gaussian
contact model. Arbitrary phase forms or other intermediate Clifford charts
cannot lower this projection bound. The bound concerns the actual B-block
rank; it does not declare a new all-column implementation free.

Let the projected subspaces on the owned itinerary be G_0,...,G_N, starting
at the high contact. Reverse the itinerary in the backward orientation, which
preserves each paid rank. Set I_j = G_0 intersect ... intersect G_j. Then

    dim I_j - dim I_(j+1)
        <= dim G_j - dim(G_j intersect G_(j+1))
        <= r_j.

The first inequality is the injection of the lost intersection quotient into
the lost part of G_j; the second follows from the projection-rank inequality.
Summing gives total paid rank at least dim G_0 - dim I_N. This includes any
number of paid intermediate moves and does not assume nested C spaces.

The exit witnesses below force the intersection of the visited low contact
spaces to zero, hence I_N = 0. The entrance witnesses give dim G_0 >= 8.
Each block therefore pays at least eight. Subadditivity of x^t for
0 < t <= 1 gives sum_j r_j^t >= (sum_j r_j)^t >= 8^t. Apply this separately
to the eight owned lifetimes. A free reset after the last consumer does not
remove any of the required visits within its lifetime.

## Exact witnesses

The source has 632 persistent fields: 224 main and 408 arbitrary helpers.
Raw event ordinals omit `climb` events and start at zero. There are 31,630
distinct scalar-contact edges and 224 terminal main-exit edges per orientation.
All 240 native events per orientation are cut. All owned contact spaces are
free in the argument. Only main entrances and exits supply boundary witnesses.

| Role | Forward high event | Backward high event | Original frame | Eight independent entrance vectors |
| --- | ---: | ---: | ---: | --- |
| 92 | 10344 | 10367 | 254 | 276, 351, 266, 74, 44, 193, 247, 14 |
| 57 | 10370 | 10393 | 274 | 304, 379, 259, 67, 37, 131, 254, 14 |
| 81 | 10396 | 10419 | 619 | 471, 386, 73, 506, 164, 194, 254, 388 |
| 224 | 10422 | 10445 | 279 | 471, 386, 73, 506, 164, 194, 304, 74 |
| 11 | 10448 | 10471 | 621 | 268, 274, 164, 194, 146, 289, 67, 388 |
| 240 | 10474 | 10497 | 280 | 268, 274, 146, 289, 304, 379, 164, 247 |
| 9 | 10500 | 10523 | 624 | 268, 274, 146, 289, 471, 386, 67, 14 |
| 256 | 10526 | 10549 | 281 | 247, 145, 290, 196, 268, 274, 471, 304 |

Each integer encodes a nine-bit vector. `WITNESSES.json` records 128 entrance
paths with 2,204 links. For every high contact, their vectors are independent
and span its actual source eight-dimensional frame. This proves the first
bound without enumerating candidate subspaces.

Each block also has 22 low owned scatter/gather contacts. The artifact records
nine independent terminal annihilators for each block, each with a path from
one actual low contact to an actual fixed main exit. There are 144 outgoing
paths with 2,516 links. A vector in every visited low contact space must be
annihilated by all nine independent functionals, so it is zero. This proves
the premise I_N=0 for the owned-path bound. No frozen native input or helper
exit supplies a cap.

The verifier checks seeds, chronological links, main terminal annihilators,
target identities, both actual owned macro boundaries and all binary ranks.
It also checks 300 corruption, missing-normal, rank-seven-hyperplane and
warp-cut controls. A separate finite calibration enumerates every Lagrangian
in dimensions one through three (3,15,135 respectively) and checks all 18,459
ordered pairs against the projection-rank inequality. The universal proof is
the dimension argument above; this finite calibration checks the conventions.

The full source paid histogram is
`{1:2201,2:412,3:510,4:127,5:40,8:8}` and its productive-helper histogram is
`{4:28,7:7,8:47,9:326}` in both directions. Reconstructing these is a baseline
control, not a new invoice. No solver or floating tolerance enters the proof.

## Consequence and limits

The high-side-only independent/shared-map proposal cannot shrink its eight
center inputs. Moving both sides, permitting multiple C transitions, or moving
both helper boundaries also cannot lower the owned-wire moment under the
stated persistent monotonicity and scalar/main-boundary hypotheses. No MILP
is needed to decide that owned-wire reduction.

Other persistent bridges or helper credits might improve without lowering the
owned charge. Nonmonotone L itineraries, changed scalar incidence/order,
independent operand gauges with paid cross-frame ADDs, changed main boundaries
and additional paid observations are outside the theorem. In particular the
older common-kernel prototype allowed nonmonotone L edges and is not excluded.

Native all-column realization, movement, precision, owned erasure, compilation
and the outer integer-recovery theorem remain separate obligations. The
selected conditional kappa remains 0.00302015.
