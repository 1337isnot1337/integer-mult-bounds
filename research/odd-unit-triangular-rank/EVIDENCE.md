# Verification evidence

I used CPython 3.12.13 and its standard library. I passed the primary
replay under `-I -O -Werror -B`, the independent vector-coordinate replay
under `-I -Werror -B`, and the fourteen-control replay under optimized Python.
I also passed the registered replay and metadata/source-pin
validation. I record committed-byte/history and hosted status in the PR.

The retained baseline engines reconstruct 136 and 512 admissible
types, and hyperplane selectors of 21 and 48 types. They agree on these canonical
selector SHA256 values:

```text
h5 96726988127c29a14030b175bada688bfc3eb574dcb5fed32ad973abe01f423f
h6 7422ceb1f7f0332c25ebaea83c18cf98bda5056536a73373b27ecde3c32d60be
```

I checked all 1,407 upper-triangular seed-selector positions and their
transposed reverse-order selectors. The primary
engine also checks repeated-port minors of orders 28 and 64 over Q,
F2, F3 and F5. Both engines check nonuniform multiplicities, including
missing types. The primary weighted fixtures have 342 and 1,282 port
occurrences; the independent fixtures have 395 and 1,470.

I reconstructed the retained 256-port rank-16 projector through its
16-by-32/32-by-16 exact factor identity after clearing denominator eight.
Its scalar factor fails the complete fitting condition, as expected.
I did not execute the original FLINT search or claim that a single
projector completes a unit.

The baseline controls reject zero fitting diagonals, collapsed duplicate ports,
invalid multiplicities/types and a broken triangular selector. They also
exhibit the missing h5 special orbit, the failure of idempotency after
normalizing a nonidentity diagonal, correct removal of a zero-charge
term, and rejection of an altered archive by the actual optimized CLI.

For the stronger odd theorem, I checked both flags in dimensions three,
five and seven: 624 selected type occurrences across six flag cases and
2,226 admissible types. I checked 68,216 triangular seed positions and
their transposed reverse-order controls. The ambient Gram-Schmidt engine
and the separate abstract symplectic engine agree on all six digests.
The dimension-five digests are:

```text
low  0cf9d4433f4388d5d03aa7954b23f547d70fa5c64ea4586377c1a4287c7e5e54
high 9003b127e3ea12b62271165f4038c65c8b1eab99d084b1998fb85425d9a2bbc3
```

I checked nonuniform populations where either flag improves the balanced
bound, exact high weights 3/7 and 9/31, and the d3 coincident-flag case.
For 44 rank-15 terms, I checked the necessary mixed-rank count at
74, 75 and 76 rank-1 terms. The first fails; 75 attains the arithmetic
boundary. I claim no construction attaining that boundary.
I reject equal weights and a mislabeled flag. An unreversed source/sink
exchange fails the checker's upper-one mask convention; reversing its
order restores that convention. I also distinguish the lifted binary bit
from the wrong integer expression. Singular-core
fixtures establish the exact special-port rank addition over Q/F2/F3/F5/F7,
including repeated special ports and nonidentity diagonal values. A
separate full d3 fitting matrix attains the weighted rank-eight bound.
Both actual optimized baseline and flag CLIs reject changed source bytes.

For the triangular-selector limit, I ran a subset dynamic program over
explicit annihilators, without using the written prefix-rank upper bound.
At dimensions three and five, I checked 8 and 32,768 sink subsets, with
12 and 245,760 transitions, respectively. These states cover all 3!
and 15! orders of the nonzero sinks. I obtained maximum regular selector
sizes 1 and 17 and reconstructed triangular witnesses. I prove the
all-dimensional limit in PROOF.md; I claim no optimal fitting matrix.

The arbitrary-multiplicity and field quantifiers follow from PROOF.md.
Finite replays do not exhaust those domains. Source-analysis agents
checked the proof and its scope separately during this AI-assisted
session; I claim no independent human or formal-kernel review.

For the retained general baseline, I checked every admissible type,
selector entry and generated orbit for dimensions two through eight:
10,964 types and 451 selected types across those seven fixtures. The
uniform fractions are 1/2, 1/3, 1/4, 1/9, 3/32, 11/270 and 1/32. I also
checked exact odd-fraction comparisons through dimension 49. These are
finite corroboration; the affine-flag and symplectic arguments prove the
baseline formulas. The stronger odd coefficients are 1/3, 17/105 and
43/651 at d3/d5/d7. Their all-dimension statement follows from the written
flag radical counts and orbit mixture. The old baseline and the new flag
implementations remain separate checks.

I ran the card's existing ceiling control separately and obtained
`PASS_COMPLEX_LOCAL_WORD_CEILING`. It only orients the selected-word
baseline. I did not run the full selected supplier replay or change its
frontier. The new unit bound uses its own declared fitting/copy model.
