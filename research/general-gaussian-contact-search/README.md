# Costed non-nested Gaussian contact search

**Exact rank/invoice model and optional constructive search; no new kappa.**
This extends contact retiming beyond monotone climbs. Every former zero edge is
represented, every changed native warp is charged at its actual Gaussian rank,
and a helper's target rank is its whole relative Clifford rank. Both helper
boundaries may move. The unchanged main, adapter and owned interfaces are frozen.

The positive calibration independently rediscovers #4672's 49-contact / 13-helper
change on its older #4610 word and reproduces its entire paid/helper invoice.
That result and its kappa belong to the predecessor. Bounded searches on the
stronger round-three word have not found a profitable candidate. No exponent,
new physical supplier or universal negative result is claimed here.

## Changed search model

At a node with old subspace U choose either U or U intersect M, where M is the
common kernel of the supplied nonzero nine-bit functionals. A scalar contact
uses one common actual gauge for all operands. Main endpoints, explicit adapter
boundaries and all contacts involving owned C stay at their original gauges.

For canonical gauges C_U and C_V, the actual child C_V C_U^-1 has Fourier rank

    r(U,V) = dim U + dim V - 2 dim(U intersect V).

This applies to downward and non-nested edges. Dimension difference alone is
wrong outside ascending chains. An old zero edge U->U may become a positive
rank child when only one endpoint moves. For a native map K_G transporting the
source chart U to G(U), the changed physical warp is charged at r(G(U),V),
rather than being declared monomial. Whole helper jobs use r(U_start,U_final).
Every helper must remain strictly productive in the searched switch model.

`model.py` derives these ranks from explicit nine-bit subspace sets. It retains
all chronological contacts and previously zero transitions. Its baseline must
reproduce the source paid list exactly. Changed shared G matrices are outside
scope: the maps remain the same, while their changed physical implementations
may require Gaussian children of positive rank.

The formulas are the canonical zero-form case of Dugongue's #4654 Lagrangian
chart grammar. If U subset V and intersecting with M removes alpha and beta
dimensions respectively, the paid four-state table is

    (r, r+alpha, r+2alpha-beta, r+alpha-beta),  r=dim V-dim U,

ordered (00,10,01,11). Thus the mixed state 01 must not silently be assigned
r-beta. Native warp tables are computed from their actual mapped subspaces.
The verifier compares the general rank formula with the exact Clifford B-block
on all 285 ordered subspace pairs in dimensions one through three.

## Discovery and acceptance

`discover.py` converts each exact rank table into its rank-power energy at the
recorded test saving. Full paid energy minus full productive helper energy is
retained. In two-state coordinates any table is

    E00 + A*x + B*y + W*abs(x-y).

Physical edge costs are submodular; moving both helper endpoints can add
negative cut weights. A signed-cut mixed-integer model handles those terms.
The contact switches are binary; auxiliary cut variables can be continuous,
using the lower XOR envelope for positive weights and upper envelope for
negative weights. These envelopes give the exact table for binary endpoints.
The emitted switch list is repriced from the complete exact rank invoice and
must agree with the floating objective.

This is discovery only. Floating solver optimality is not an exact ceiling;
a timeout is not a rejection certificate. A useful candidate still needs exact
moment inequalities, an emitted physical word, all-column and absolute-phase
checks, complete compiler/ordinary/outer admission and the inherited analytic,
precision and execution contracts. No such new candidate is supplied here.

Optional discovery requires installed NumPy/SciPy; it is not installed by the
package and is not needed for the registered replay. For example:

```sh
python3 research/general-gaussian-contact-search/discover.py \
  --functionals 1,2 --seconds 30 --output /tmp/contact-candidate.json
```

Use `--source .../inputs/round2-word.json.gz --functionals 1
--fixed-helper-side exit` to rediscover the known positive calibration. It
finds the predecessor profile on the tested environment; no claim of a fixed
solver path or platform-independent discovery output is made.

## Exact replay and results

```sh
python3.12 -B scripts/research_package.py --package research/general-gaussian-contact-search
python3.12 -I -O -B research/general-gaussian-contact-search/verify.py
```

The standard-library replay verifies 285 actual Clifford ranks, the complete
source invoices, frozen-boundary rejection, new charges at previously zero
edges and the non-nested-rank counterexample. The fixed 62-node positive
calibration gives paid `{1:2183,2:416,3:507,4:135,5:40,8:8}` and helpers
`{4:28,7:5,8:38,9:337}`, matching #4672. Its strict local gain is certified
with rational logarithm and alternating-exponential bounds, independently of
the optimizer. This is a positive calibration of the model, not a new saving.

The current source has paid `{1:2201,2:412,3:510,4:127,5:40,8:8}` and helpers
`{4:28,7:7,8:47,9:326}`. `SEARCH.json` retains bounded floating experiments,
including uncompleted older product-linearized models explicitly labelled as
timeouts. They establish no theorem. The selected conditional kappa stays
0.00302015 at canonical base b58ad9ef4d4e861b0eaa5dba41742bdc072dca51.

## Open next questions

Apply the model to changed native words or compound different common kernels,
then reprice every old and new edge before further native implementation. A
negative verified energy is the first stopping/expansion gate; solver status
alone is insufficient. The actual physical witness and its complete supplier
admission remain the blocker. This package supplies the search and invoice
mechanism, not an assertion that broader search will yield a breakthrough.

## Sources and credit

Both exact #4610 input words are retained with original commit/path/blob
provenance. The round-two payload is the input used by #4672; round three is
its stronger published successor at 1eb8da6cfb35512c0cc2533413e5ca42f48e13c6.
The optional solver is separate from the independent registered verifier.

Credit Cao Yifan/#4610 for the native words; Cinna Davis/#4672 for coordinated
contact cuts and the positive calibration; Dugongue/#4654 for the exact chart
rank grammar; Cinna Davis/#4470 and its controller lineage; zxv, Jacob Alan
Sussman and all retained E8/scalar/Clifford/native/compiler contributors. Prepared
by Cinna Davis with substantial OpenAI Codex assistance; Apache-2.0. Classical
signed-cut and linearization formulas are not claimed as new mathematics.
