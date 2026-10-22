# A sharp 32-channel algebraic hull for one physical head

Prepared for Cinna Davis with OpenAI assistance. Apache-2.0. Uses the credited native H factorization and phase-corrected head data from the repository. No physical decoder or new kappa is claimed.

## Distinguish two channel models

The earlier h-boundary-commutator result requires 112 channels for a fixed scalar response space invariant under every individual head character. That result remains correct. A frequency-dependent space for ONE complete tensor head has a different answer: at most 32 channels, and this bound is sharp for the pinned H response matrix.

Let U have the eight response columns of H-I. In simultaneous Fourier coordinates, the complete f-column head acts on port p by

    D(Y)[p,p] = i^(sum_j parity(q_p dot y_j)).

Thus D(Y) has at most four distinct eigenvalues. Let P_r(Y) project onto ports with phase i^r. The least D(Y)-invariant subspace containing the columns of U is

    direct sum over r=0,1,2,3 of image(P_r(Y) U).

Its dimension is exactly the sum of the four restricted matrix ranks, and is at most 4*8=32. To prove minimality, each P_r is a degree-three polynomial in D, so every invariant space containing U also contains P_r U. Conversely the displayed sum is invariant. This proof applies at every f and every frequency. The channel basis may depend on Y.

For one column, exact rational enumeration of all 512 frequencies gives minimum-channel counts: 8 at two frequencies, 15 at sixteen frequencies, and 16 at 494 frequencies. Therefore merely allowing frequency-dependent bases does not rescue an eight-channel invariant-space decoder.

For three columns, RESULT.json gives a literal frequency tuple where all four restricted matrices have rank eight. This proves the upper bound 32 is sharp in this model. It is not an extrapolation from a random sample: the universal upper bound is proved above, and the exact witness attains it.

## Physical obligation remains open

The spectral projectors depend on the port and Fourier address. An algebraic channel basis does not provide a free native extraction or injection. Fourier conversion, spectral filtering, arbitrary-input cleanup and restoration must be priced. The result also does not assert that different stage-owner conjugates share one 32-channel space. It is not a query-complexity lower bound and does not exclude non-invariant intermediate-state algorithms.

An explicit generating family is W(Y)=[P_0 U, P_1 U, P_2 U, P_3 U], satisfying D W = W diag(I,iI,-I,-iI). This supplies a concrete algebraic target for a physical construction, not a cost certificate.

## Replay

Run `python -B research/h-frequency-channel-rank/search.py --check`. It reconstructs the source geometry and phases, enumerates the one-column ranks and verifies the three-column witness with rational elimination. The source tree is required. Assertions must remain enabled. Without --check, the result is regenerated.

## Open next questions

Can the 32 projector-weighted response channels be extracted and restored below the full H boundary budget? Can several stage owners share channels without destroying the original target ranks? Answer those questions with actual native operators and complete charges before claiming an exponent improvement.
