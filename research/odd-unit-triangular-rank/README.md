# Odd-unit rank bounds and the orbit-77 assembly gate

I prove a new source-bound constraint for the paused h=5/6 odd-type unit
search. For any finite port multiset and any fitting scalar matrix N over
any field, I obtain

    h=6: rank N >= ceil(3v/32),
    h=5: rank N >= ceil(17v/105).

I require both binary labels of each port to have odd norm and pair to
one in the standard five- or six-dimensional binary space. I allow
repeated types, nonsymmetric N and arbitrary nonzero diagonal entries.
[PROOF.md](PROOF.md) states the complete hypotheses and the stronger
maximum of two weighted flag inequalities.

For the proposed h=6 orbit-77 completion, I derive two consequences:

- A unit whose nonzero copy charges are at least five has C/v>=15/32=.46875,
  above the source's .45 screen.
- Rank-16 totals need aggregate rank at least 3v/2. In particular, full
  rank-16 idempotents cannot sum to I_v over characteristic zero, even
  with independent gauges and arbitrary port multiplicities.

I retain the author's individual rank-16 projector. The new obstruction
concerns its completion to a unit. Mixtures containing lower-charge
terms, lower-rank totals and sufficiently non-additive constructions
remain open.

## Evidence and reproduction

I construct a 48-type triangular minor in dimension six. It occupies
3/32 of each of the two type orbits, so averaging gives the bound for
arbitrary multiplicities. In odd dimensions I balance a hyperbolic-pair
flag and a Lagrangian-first flag. Both include every special port; I also
prove exact rank addition when removing those ports. At h=5 each flag
has 48 types, and their high-flag weight is 3/7.

One flag checker uses symplectic Gram-Schmidt in the ambient binary
space. The other uses abstract symplectic coordinates and an explicit
ambient isometry. They share only source authentication. I retain the
earlier hyperplane selectors as baseline checks.

I also extend the same proof to general ambient dimensions. For even
d>=2 I obtain `rank N>=ceil(d v/2^d)`. For odd d>=3, put
`t=2^(d-2)`, `n=2t-1`, and `rho=((d-3)t+1)/(n(t-1))`. If p port
occurrences have either label equal to the all-ones vector, I prove

    rank N >= p + ceil(rho (v-p)).

The weighted maximum of the two flag bounds can be stronger. Section 6
handles the coincident flags at d=3. The dimension-five copy-cost floor
for charges at least five is 17/21, above the source's .7275 scouting
screen; this comparison does not price a complete supplier.

For a dimension-five literal identity sum of rank-15 and rank-1
idempotents over characteristic zero, I also derive the necessary count
`44 J_1>=75 J_15`. I use the trace and the bound above; I do not
construct such a mixture or price its native copies.

The checkers verify the complete finite selectors and type orbits,
nonuniform multiplicities, repeated-port minors over Q/F2/F3/F5, the
retained projector's exact factor identity, and fourteen failure controls.
The controls distinguish a local projector from a complete unit and
retain the identity hypothesis in the idempotent trace corollary.

With Python 3.12 and the standard library:

```sh
python3.12 -B scripts/research_package.py --package research/odd-unit-triangular-rank
python3.12 -B scripts/check_research_commit.py --package research/odd-unit-triangular-rank --check-source-history
```

The six registered commands include `odd_flags.py` and
`odd_flags_independent.py` alongside the baseline and boundary checks.
They read immutable source bytes and use exceptions that remain active
under optimized Python. The source archive includes its license and
requires no unmerged foreign Git objects. I do not execute the
predecessor's large orbit search or its unpublished LP drivers.

## Source, decision and limits

I answer the explicit reopening question in Philippe Van Velzen's
[small-unit note](https://github.com/philippeVV/integer-mult-bounds/tree/b5ce9d223feeed73d07e2a07321f7a025bd5865e/research/complex-budget-law/closures-3/small-units-lp).
The author already used Hadamard and acyclic rank bounds. I use those
standard methods with new selectors and multiplicity averaging to
strengthen the recorded v<=17h_b and v<=16h_b pair rows. For h_b<=5,
the respective limits become 53 and 30 ports. A fitting unit still
needs its actual bit-copy factorization and complete physical costs.

I retain Philippe's existing acyclic-minor method and distinguish
DreamingOfClouds/PR2244's Lagrangian averaging, which allows nonsymmetric
decoders under a symmetric support majorant. Independent odd source/sink labels here can
give directed masks. [NOTICE.md](NOTICE.md) links those exact comparisons;
the earlier bound can be stronger on its restricted mask class.

I retain the original scientific pins at
`6f100d4bb5083f8c35d96fd95a539811c62f245c`. I prepared this strengthening
from canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority
revision 6, after archival intake of PR3512. The intake ledger still
marks that predecessor partially reviewed. I coordinate
in [Discussion2278](https://github.com/CrocSwap/integer-mult-bounds/discussions/2278#discussioncomment-19010715).
I preserve the selected frontier and supply no new integer exponent.
I claim no independent human review, formal-kernel proof or complete
supplier admission. [NOTICE.md](NOTICE.md) retains source credit and
substantial AI disclosure.

## Open next questions

Can a mixture of charges or lower-rank totals meet a complete paired
budget after imposing these new rank rows? First add the certified rows
to an explicit integer unit model and retain its actual support-rank
histograms on both sides. The unpublished LP drivers and the missing
physical producer/consumer invoice prevent a stronger conclusion here.
The beta-five-only rank-additive assembly does not justify another
construction round under the retained fitting contract.
