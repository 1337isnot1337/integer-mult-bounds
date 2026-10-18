# P104 fixed-cover support cut: hypothesis review and a sharper criterion

**Statement.** PR3259's path-embedding argument is a **valid** necessary support
test under its fixed-cover contract, taken in its pooled form (K1-K7 in
[PROOF-REVIEW.md](PROOF-REVIEW.md)). That contract is closed by a much larger
obstruction than one coefficient: **2,682 of the 4,992 required entries of
`C = I - G/2` are unsupported**, with at least one in every row and every
column.

The 2,682 count rests on two sound tests that agree on all 10,816
source/target pairs:

- PR3427's one-recombined-helper lemma, re-proved here in every dimension
  case. It keeps the fact that PR3259's test discards: the frames along a
  dependency path are nested.
- PR3252's full-memory recurrence, whose proof is reviewed valid here,
  implemented anew over the whole pool. It is multi-hop and does not assume
  the lemma.

For the pooled untimed relaxation the lemma is exact: no sound untimed test
can exclude more pairs. The supported pairs have a simple form. They are the
2,309 compatible slot pairs read as port pairs, plus one extra pair, so
`2,682 = 4,992 - 2,309 - 1`. PR3259's single missing entry,
`C[71,102] = -1/2`, belongs to its looser relaxation. Applied to all 104
columns, PR3427's source-preconditioner bound rises from `rank(U-I) >= 4` to
**`rank(U-I) >= 17`** under PR3427's own contract.

This is an author-checked, AI-assisted audit: a scoped proof review, a finite
certificate and small-domain checks. Four AI review passes in the same loop
(reproducibility, mathematics, provenance, referee) checked the first
version, and this revision addresses their findings. No independent human or
formal-kernel review has been done. The audit constructs nothing and is not a
complete multiplication theorem. It proves no P104 impossibility outside the
stated contract, and κ and the selected frontier are unchanged.

## Results

| Item | Result |
|---|---|
| PR3259 embedding argument, checklist a-h | Valid. Two implicit sentences are recorded as clarifications. See [PROOF-REVIEW.md](PROOF-REVIEW.md). |
| PR3252 PROOF.md (memory relaxation) | Valid for its recurrence and contract. |
| What PR3427 consumes | Its own one-helper lemma and PR3252's full-memory operations, not PR3259's recurrence. Both are justified. |
| Channel word, exact run | Every Y increment is exactly `G/2` in the sorted port order, with all helper dirt cancelled; every channel add is at equal frames. |
| Control: PR3259 layered test, rebuilt | Missing set `{(71,102)}`. Forward counts `16,25,52,365,1725,2283,2285,2297`. Backward cone 37, disjoint. |
| Sharp criterion: one criterion in two loop orders, plus PR3252's multi-hop recurrence | All three computations agree on every pair. 2,310 supported pairs, against 10,815 for PR3259's test. 2,682 required entries unsupported: 1,801 at `-1/2` and 881 at `+1/2`. 8,506 pairs unsupported in all. |
| Shape of the sharp support | Exactly the 2,309 compatible slot pairs `(a,b)` read as (target `b//2`, source `a//2`), all distinct and all required, plus `(73,83)`. All supported pairs are off-diagonal required entries. PR3259's test grants 2,681 of the 2,682 missing entries, all 5,720 zero off-diagonal pairs and all 104 diagonal pairs. |
| Cross-check with PR3427 | The four published per-source masks (sources 0-3) are reproduced exactly. |
| Consequence for PR3427 | A 19-by-18 rectangle of unsupported pairs has `rank C[R,S] = 17`, giving `rank(U-I) >= 17`. A 17-by-17 minor has `det(8C) = 2^43`. |
| Small domains, pooled | 4,500 seeded `F_2^3`/`F_2^4` instances. On every one, an exhaustive untimed reachability, which does not assume the lemma, equals the one-helper test. Its 4,264 helper-only pairs are each realized by an explicit program in the checked interpreter. PR3259's test is strictly looser on 54 instances (75 pairs), and the exhaustive search confirms those pairs unreachable. |
| Small domains, unpooled | 4,500 instances with six rigid types. The exhaustive support lies inside PR3259's test every time, and 8,978 helper-only pairs are realized. 33 pairs on 26 instances lie outside the one-helper test, each realized by a legal program: the lemma needs pooling. |
| Random programs | 18,000 seeded checked programs with exact `Fraction` coefficients, two per instance; all lie inside the exhaustive support. Pooled: 1,043 nonzero coefficients counted per program, 604 of them on pairs whose X and Y chains share no frame, and 633 (13 + 620) passed between helpers of different types. Unpooled: 1,887 coefficients. The random programs found none of the 33 unpooled escapes, so they are a soundness sample, not the evidence for the lemma. |

### Which hypotheses carry the obstruction

Each row relaxes one hypothesis and is checked at support level with the sharp
criterion. The rows are unpriced and give no coefficient or dirty restoration.

| Relaxed hypothesis | Reaches `(71,102)` | Reopens, of 2,682 |
|---|---|---:|
| Cross-layer nesting, as PR3259's proof drops it (a proof relaxation, not a contract change) | no | 2,681 |
| K5, correction-only Y relay, keeping each target's write-before-read order (R1) | no | 0 |
| R1 without that order (R1u; a looser test, since no program reads content before it is written) | yes | 2,682 |
| K5, the channel's own Y content readable, including target feedback (R1c) | yes, by feedback on Y71 at dimension 5 | 2,682 |
| K1, free nested flags: helpers not tied to `L/A/B/H` (R2) | yes, one free flag from X102's dimension-1 frame to Y71's dimension-8 frame | 2,682 |
| K6, reads of old channel-helper state (R3) | yes, one equal-frame add from `D11` at dimension 5 | 2,682 |

The sharp criterion and the rows relax the relative timing of different
registers but keep the order of operations along one dependency path; that
order is what makes path frames nested. R1 applies it at a target used as a
relay. Content written into `Y_u` at one of its frames can be read only at
that frame or a later one, because `Y_u`'s frames ascend in time. Every program obeys this. With it,
correction content reaches targets at their final caps (2,310 arrivals) and at
55 frames of dimension 5 or 6 (31 and 24). A cap can feed only itself, since
the 104 caps are distinct, and the 55 lower arrivals relay nothing new, so R1
reopens nothing. R1u drops the order and reopens everything. R1's zero rests
on that order.

R1c and R3 use the channel's actual coefficients, recorded from the exact run
of its 4,058 events. The channel first puts `X102` into `Y71` at event 3378,
with coefficient `1/2`, from `D11` at dimension 5; both channel witnesses use
that state. R1c and R3 reopen everything because the channel's state already
carries the support of `G/2`, which contains every off-diagonal required
entry. Reading that state is not a correction: its coefficients, restoration
and cost are unknown.

Among the rows computed here, two hypotheses each reopen every entry: the
fixed cover (K1) and the exclusion of the channel's source-dependent state
(K6, with its exposure through Y). The rows are not a complete map. Not
computed at P104: frame descent (K2), cross-frame mixing (K3), changed source
or target frame paths and source mutation (K4, K5), dependent dirt (K7) and
extra correlated storage. The small-domain controls show that descent,
cross-frame mixing, off-cover flags and correlated old state can each escape
both tests. Under PR3427's preconditioner contract, which relaxes K4, a source
preconditioner needs `rank(U-I) >= 17`. Any reopening must change at least one
of K1-K7, or add storage, and must cover all 2,682 entries with a full bill.

The 2,682 count binds only corrections that keep the fixed cover, the frozen X
and Y frame paths and the untouched channel state. Routes that change any of
these, including the channel-state and present-head work listed below, must be
judged at coefficient and restoration level.

Cited, not recomputed:

- PR3013: component/containment pooling reaches all 4,992 entries.
- PR3427: a one-H2 source shear removes only the `(71,102)` requirement.

### Concurrent pending work on the same card

These open PRs are not reviewed here. The corrections they construct or bound
change something K1-K7 freeze, so they lie outside this contract and do not
conflict with its closure.

- Wentao Li (VictorLiwentao) prices single-entry and whole-row `I - G/2`
  corrections on the published word: #3601 (`26394881f0a183ca0df3d986ec58aa56900ada6c`),
  #3610 (`4352496b3aa56ad17446ddbd1d78931f3d392996`) and #3618
  (`0c4b73507ba7ed7b992e47b17f2cbcb6e362466b`). Their words lift a target's
  frame (changes the frozen Y path, outside K5), detour a source (changes the
  frozen X path, outside K4), add a private-copy lifetime (extra storage,
  outside K6) or build on a repaired channel update (outside K6). #3618's
  T48 corrects all 48 entries of row 23 on one target lift for +2 rank mass.
  #3532 (`8fecbf7df7b48c9004bd10a0da6a81f33d455737`) repairs a channel
  update, which changes the channel (outside K6). #3614
  (`a6c3ae20abe0a15d781ee952e717d489552c9c66`) and #3621
  (`b37f6aef686c940a7613db3e04c6234e472399cf`) give non-private +2 lower
  bounds for present-head entries in those correction classes. #3669
  (`84288150fcaa8e3fecb128ef1feeb8ac1c63ccc6`) audits flag 0's
  dirty-restoration chronology on the published word.
- Clear Insight (Clear1nsight), #3609
  (`13f974dae4af66027afb01f3ab42df9e830c2e90`), completes the omitted P104
  section at the word's entrance with sources moved and Y temporarily
  writable (outside K4 and K5).
- James Reed (jwr404), #3580 (`c867e61e2ea790738474025b6200bf8475e56957`),
  indexes the #3259 replay for the
  [live support map](../../docs/research/p104-live-support-map.md).

## Reproduce

From the repository root, with the standard library (about 2.5 minutes in all):

```sh
python3 -I -O -Werror -B research/p104-fixed-cover-cut-review/verify.py
python3 -I -O -Werror -B research/p104-fixed-cover-cut-review/test_verify.py
```

The verifier prints one JSON receipt with every count quoted above. Its last
line is

```
PASS_P104_FIXED_COVER_CUT_REVIEW layered_missing=1 sharp_missing=2682 of 4992 pr3427_masks=4 rank_U_minus_I>=17 rows=5 oracle_instances=9000 oracle_programs=18000 no_kappa
```

The registered replay is
`python3.12 -B scripts/research_package.py --package research/p104-fixed-cover-cut-review`.
Every check raises `SystemExit("FAIL: ...")`, so checks stay active under `-O`.

**Negative controls that must fail.** `test_verify.py` checks seven:

- a tampered input hash is rejected;
- an unsound "shared snapshot only" test is rejected by the oracle;
- an exhaustive search that never switches helper type is rejected, because
  it misses the fixed unpooled two-type relay;
- dropping the shared-helper-type requirement changes PR3427's masks;
- dropping containment `V <= W` is unsound on a fixed `F_2^4` instance (at
  P104 containment is never decisive, which `verify.py` asserts);
- a wrong rank rectangle is rejected;
- the fixed Y-relay program is a real escape.

Inside `verify.py`, five contract violations must each produce a coefficient
outside both tests. They are a Y read (a fixed four-operation `F_2^3` program
run in the checked interpreter with only that rule relaxed), frame descent,
cross-frame mixing, an off-cover flag and correlated old state. A sixth
control, a fixed unpooled two-type relay over `F_2^4`, must lie outside the
one-helper test and inside PR3259's test.

## Method and independence

The code shares nothing with PR3182, PR3252, PR3259 or PR3427. Frames are
canonical reduced-echelon keys over `F_2^9`. E8 ports are enumerated
independently and sorted.

- An exact `Fraction` run of the channel word binds the port order and `C` to
  the channel itself, and records the channel's actual coefficients per
  register and frame for rows R1c and R3.
- The layered control hosts every d-flat of each interval literally, then
  takes one read-first step per layer.
- The sharp support is computed three times. Two computations evaluate the
  one-helper criterion in different loop orders: echelon keys with
  helper-type masks, and point-set bitmaps looped per helper type. The third
  is PR3252's full-memory recurrence (carry, admitted reads, relay of old
  memories `S + L(h,d) + L(w,d)`, minimal-memory pruning), rewritten over
  all 2,309 types and 104 sources. It is multi-hop and does not assume the
  lemma.
- The rank bound uses a deterministic greedy. For each seed column it
  repeatedly adds the column that maximizes `min(|R'|, |S|+1)`, then `|R'|`,
  with ties to the smallest index, where `R'` is the set of rows still
  unsupported. It stops when `min(|R|,|S|)` stops growing and keeps the
  rectangle of largest rank. Exact `Fraction` elimination gives the rank, and
  an independent integer Bareiss determinant confirms it. The greedy is not
  optimal, so 17 is a lower bound.
- The small-domain oracle draws seeded random instances (seed `20261018`):
  3,000 over `F_2^3` and 1,500 over `F_2^4` in each family. Coverage is these
  instances, not every instance.
  - *Pooled* instances mirror P104. Departure chains fix the low dimensions,
    arrival chains fix the high ones, and the types are every compatible
    pair. *Unpooled* instances use six random rigid flags as types.
  - Each instance gets an exhaustive untimed reachability over frames: a
    helper of one type moves up between two nested frames its type admits,
    and helpers mix at equal frames. Every reachable helper-only pair is
    then turned into an explicit program, one helper per step, and run in
    the checked interpreter.
  - Each instance also runs two random programs. One chooses uniformly among
    the operations legal at each moment, for 120 operations; the other
    follows a random path through one to three relays. Direct X-to-Y adds
    are omitted from them, so every coefficient travels through helpers.
  - The interpreter checks flags of the right type, ascending transports,
    and equal-frame reads, adds and writes.
- The verifier also checks the roles in the original channel word: X is
  never written and Y is never read, so K4 and K5 hold for the channel.

## Scope, inherited assumptions and open obligations

Inherited:

- PR2981's covers and the native channel frame paths, through their pinned
  JSON inputs;
- the ordered E8 ports with the fixture's 16 removed roots, bound to the
  channel by the exact run;
- the contract K1-K7 in [PROOF-REVIEW.md](PROOF-REVIEW.md). K1 is PR3259's
  pooled relaxation of its matching contract, so every exclusion here holds a
  fortiori for each single matching.

The rows and the rank bound apply only under those contracts.

Open and not addressed here:

- cross-register chronology and acquisition order;
- coefficient delivery and dirty restoration;
- native lowering, precision and physical hosting;
- consumer cost and supplier admission;
- every changed-cover or changed-path construction;
- a timed refinement of the sharp criterion.

The selected cold replay is unchanged and was not rerun.

## Open next questions

1. *Is 17 the true rank bound?* A min-rank completion of `-C` on all 8,506
   unsupported pairs may force a rank well above 17. A larger rank would
   further constrain any joint native source preparation under PR3427's
   contract. A first step is an exact lower bound by larger or overlapping
   rectangles, or by a min-rank argument. It needs no new matching search.
2. *Which changed contract reopens all 2,682 entries at least cost?* An entry
   is supported when one helper type admits a source frame and a nested
   target frame. Under the present cover that happens only through the
   entry's own compatible slot pair, apart from `(73,83)`, which goes through
   X83's dimension-4 frame. A changed cover must supply such a type for every
   missing entry; relaxing the cover (R2) does this at support level. The first priced data
   point is pending #3618's T48, which corrects a whole target row on one
   target lift for +2 rank mass by changing the target's path rather than
   the cover. Coefficients, dirt and every cost of a complete reopening
   remain unknown.
3. *Is there a non-trivial use of channel state?* R1c and R3 reopen everything
   only because the channel already carries `G/2`. One would need a
   coefficient-level construction that reads channel state and restores it,
   with an explicit list of the changed channel obligations.

## Predecessors and credit

- Nick Petalas (petalas):
  - PR2981 `3d24b92d8ba057b57cb2d480170ec407520e6882` (covers and flags);
  - PR3252 `4784b71d2e0833537c9ae1e8be05ad2a6b334d92` (memory soundness);
  - PR3259 `b572b0c25569898579041200e95731c5a43c9189` (pooled cut and
    embedding argument);
  - PR3013 `504dc9a15f7a874a47564cdf3ae6857bbbc8d000` (component pooling).
- dcharb78: PR3182 `ad848966cd62e13de5ad8d4b5169c221d74d2fcd` (the cut and its
  1,725/37 cones).
- commdata2338: PR3214 `faa6323371db1c5fbb43ab04c6e00715d2328bc6` (output
  repair).
- Jose Manuel (jmbarrancoml): PR3427 `344774ba08a73fc3a85fdcb93fb319927bde3ea2`
  (the one-helper lemma and the rank-four theorem extended here).
- James Reed (jwr404): the merged #3497-#3519 series (heads
  `a8804afd46ee63b202291ab3bcebd1eb2b83ecfc` through
  `d8928dd94a3450c5145a847507e7fb466dbc5c00`) already reproduced the X102
  cone counts 16, 25, 52 and 365 and showed that the literal recurrence
  misses the same pair.
- Wentao Li (VictorLiwentao) for the chronology audit
  (`p104-channel-touch-restoration-audit`), which is not redone here.
- The [live support map](../../docs/research/p104-live-support-map.md), which
  asks for this review before the fixed-cover route is treated as closed.
- The native/compiler lineage credited in the pinned inputs: Rohan Arun/1972,
  Chafik Boukhalfa/1991, Adam Gall/1940, Josie Elliston/1071 and
  Ali Romman/1125.

Base: canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority
revision 6. [SOURCES.json](SOURCES.json) pins the three live inputs by Git blob
and SHA256.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). Apache-2.0.
