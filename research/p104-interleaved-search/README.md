# P104 interleaved schedule search checkpoint

**No complete P104 schedule or improved κ was found in this bounded follow-up.**
This package preserves exact partial constructions and their remaining costs.
It does not promote a local fragment, an oracle-assisted identity, or an
optimistic packing bound into a multiplication supplier.

The starting point is canonical main
`0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`. The selected result remains
κ = `836330098538459/500000000000000000`. The requested objective was a
significant, fully verified gain; the working search threshold was a 1%
relative improvement. That objective is **not achieved**.

## What is retained

1. **Conditional dirty-register surgery.** `scalar_surgery.py` replays the
   selected 112-port word on all 704 independent input columns. It converts
   eight source/target pairs into sixteen arbitrary dirty helper roles and
   derives a 104-port identity, including actual compensation and restoration
   gates. Its replacement cut reads eight explicitly hypothetical pure-source
   queries. The checker reports the cut's incompatible survivor reads; it is
   not a frame-legal implementation of those queries.
2. **An interleaved two-query delivery channel.** `delivery.py` checks the supplied
   coefficient schedules against the selected scalar B word, propagates changed
   frames through the later tail, and accounts for changed helper endpoints and
   query-residual cancellation. These change the frame paths that were frozen
   in the temporal-cut obstruction. Each fragment has an explicit external
   query-input contract. It also replays both queries together: 30 contacts,
   two simultaneous private copies, and zero remaining query perturbation in
   every other register after cleanup. The two supplied query registers incur
   two rank-one boundary moves, reported separately from the public-profile
   deltas. This does not establish an
   eight-query schedule, query construction, or concurrent native admission.
3. **A conditional cost screening tool.** `budget.py` uses exact rational interval
   arithmetic in the pinned packing-ceiling engine. It distinguishes helper
   boundary work that replaces an idle/remainder invoice from genuinely extra
   transport work. Every reported candidate κ is an optimistic **upper bound**
   under the stated retained template, not an achieved saving.

The native fixture maps to removed selected port positions
`3, 14, 21, 34, 39, 61, 76, 93`. This differs from the puncture chosen in the
selected-port adapter package; the coordinate map and puncture are checked
directly, rather than conflating the two fixtures.
Both constructions use the same decoder orientation. For the two retained
delivery pairs, the supplied query must equal the scalar surgery's raw source
query divided by eight; the aggregate checker binds this normalization. This
agreement does not construct the queries or assemble the missing six terms.

The selected contract already allocates **eight distinct private-centre
families**, separately from its ordinary helper families. The two simultaneous
private copies fit that stock; their overlap does not imply that ambient width
`m=73` must increase. The checker binds this count through the selected source
manifest to `complex-t16-rare-pattern-exchanges/data/SPEC.json`. The old emitter
still assumes sequential centre lifetimes, and the two external public query
registers need their own actual placement and construction. Physical private
stock sufficiency alone does not close those obligations.

## Reproduce

From the repository root, with Python 3.12 and the standard library:

```sh
python3 -I -O -B research/p104-interleaved-search/verify.py
python3 scripts/research_package.py --package research/p104-interleaved-search
```

The registered command is read-only. It checks source hashes, recomputes the
exact receipt, compares it with `RESULT.json`, and runs rejecting controls.
The receipt separates the conditional scalar identity, delivery contracts,
and favorable cost models. It contains no admitted exponent claim.

Validation on October 14, 2026 on macOS arm64 passed the registered replay with Python 3.12.14
and a separate Python 3.14.7 replay from a read-only export containing only the
ten package files and eight declared inputs. The export replay ran outside the
checkout with `-I -O -B`; its file set and hashes were unchanged afterwards.
Four scalar-error controls, three delivery-error controls, and the cost
accounting checks all passed. No complete supplier or outer-theorem replay was
run, because this checkpoint does not supply their missing inputs.

Discovery also explored persistent helper routes, changed packet timing,
alternative decoders, and constrained delivery-chain searches. Finite-field
and numerical optimization screens were used only to nominate candidates;
they are not evidence of rational identities or impossibility. Only the exact
replays retained here are acceptance evidence. Failure to find the other
chains is not a universal lower bound.
The final source-storage probe also found that simply dropping the punctured
source roles' old reads loses live-input transfers. Those roles carry selected
word intermediates; using them as query banks requires a replacement prefix,
not just new compensation for dirty inputs.

## Remaining admission obligations

The eight queries must be constructed from the actual source values at legal
chronological frames while preserving arbitrary dirty state. The remaining
six delivery terms must be scheduled, and all eight must coexist with query
construction and each other. Their combined frame changes, helper entrances,
cleanup and residual widths must be recomputed; separate profile deltas cannot
simply be added as a substitute for combined replay.

A completed local word would still need its backward interface, native phase
recipes, chronological whole-call hosting, residual/idle children, precision
and reserve accounting, two exact moment checks, and the retained outer
inequalities. None of those missing obligations is waived here. With the
selected bit supplier unchanged, even a successful complex replacement remains
subject to the bit-side cap recorded by the budget checker.

## Open next questions

- **Can the source packet prefix produce the four non-coordinate queries
  within the remaining budget?** This is necessary before a delivery fragment
  can become a supplier. The first experiment should change the packet prefix
  or later packet routing and replay its full dirty-state matrix; reusing a
  register must also remove or preserve its existing lifetime. A scalar span
  calculation alone does not supply storage or frame availability.
- **Can the remaining delivery terms share one legal chronological schedule?**
  Start with the two exact fragments, add one term, then propagate every frame
  through the tail and cleanup before pricing it. The blocker is the combined
  lifetime and frame contract, not the decoder identity.
- **Does a completed candidate survive the full supplier invoice?** Only after
  the first two questions are closed should whole-call hosting and the outer
  certificate be rebuilt. An optimistic ceiling leaves unpriced obligations;
  it cannot be used as a lower bound on κ.

## Provenance and scope

This follows the native P104 channel in PR1991 (Chafik Boukhalfa), the scalar
channel in PR1972 (Rohan Arun), and the chronological gather schedule in PR1940
(Adam Gall). The P104 geometry and decoder work originate in PR1071 (Josie
Elliston), PR1125 (Ali Romman), PR717 and PR968. The selected scalar architecture
and Hamming packet construction retain their predecessor attribution, including
icekylinx's frame-sa504 work and the selected PR1042/PR1094 lineage. The packing
ceiling engine is Douglas Colkitt's existing work, not a new theorem here.

The earlier temporal-cut result in PR2082 concerns a frozen native schedule;
this search explicitly changes that hypothesis. The live overlap check also
found the independent cut work in PR2090 and terminal-correction work in
PR2083/PR2089. Those results are not recast here as a new gain. Exact source
blobs, hashes and the local task record are in `SOURCES.json` and `TASK.json`.

Prepared for David Arias with substantial OpenAI Codex assistance, including
parallel construction and checking. Apache-2.0. No formal proof assistant or
human independent review is claimed.
