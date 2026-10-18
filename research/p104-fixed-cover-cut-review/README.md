# P104 fixed-cover support cut: hypothesis review and a sharper criterion

**Statement.** PR3259's path-embedding argument is a **valid** necessary support
test under its stated fixed-cover contract. That contract is closed, by a much
larger obstruction than one coefficient. The test discards one fact true of every
legal dependency path: its frames are nested across dimensions. Keeping that
fact gives a valid criterion, **one recombined helper per path**. This lemma is
stated in PR3427 and re-proved here in every dimension case. It is exact for
untimed support. Under it, **2,682 of the 4,992 required entries of
`C = I - G/2` are unsupported**, with at least one in every row and every
column. PR3259's single missing entry, `C[71,102] = -1/2`, is a property of its
looser relaxation.

PR3427 states the lemma, but it has not been evaluated beyond PR3427's four
source columns. Applied to all 104 columns, it raises PR3427's source-preconditioner bound
from `rank(U-I) >= 4` to **`rank(U-I) >= 17`**, under PR3427's own contract.

This is an audit: a scoped proof review, a finite certificate and small-domain
controls. It constructs nothing and is not a complete multiplication theorem.
It proves no P104 impossibility outside the stated contract, and κ and the
selected frontier are unchanged.

## Results

| Item | Result |
|---|---|
| PR3259 embedding argument, checklist a-h | Valid. Two implicit sentences are recorded as clarifications. See [PROOF-REVIEW.md](PROOF-REVIEW.md). |
| PR3252 PROOF.md (memory relaxation) | Valid for its recurrence and contract. |
| What PR3427 consumes | Its own one-helper lemma and PR3252's full-memory operations, not PR3259's recurrence. Both are justified. |
| Control: PR3259 layered test, rebuilt | Missing set `{(71,102)}`. Forward counts `16,25,52,365,1725,2283,2285,2297`. Backward cone 37, disjoint. |
| Sharp criterion (two loop orders) | 2,682 required entries unsupported: 1,801 at `-1/2` and 881 at `+1/2`. 2,310 supported pairs, against 10,815 for PR3259's test. |
| Cross-check with PR3427 | The four published per-source masks (sources 0-3) are reproduced exactly. |
| Consequence for PR3427 | A 19-by-18 rectangle of unsupported pairs has `rank C[R,S] = 17`, giving `rank(U-I) >= 17`. A 17-by-17 minor has `det(8C) = 2^43`. |
| Oracle, coefficient level | 4,500 seeded legal programs over `F_2^3` and `F_2^4`, with exact `Fraction` coefficients. 269 nonzero helper-path coefficients, 107 of them for pairs with no common snapshot. None lies outside the sharp test. |

### Which hypotheses carry the obstruction

Each row relaxes one hypothesis and is checked at support level with the sharp
criterion. The rows are unpriced and give no coefficient, chronology or dirty
restoration.

| Relaxed hypothesis | Reaches `(71,102)` | Reopens, of 2,682 |
|---|---|---:|
| Cross-layer nesting, as PR3259's proof relaxation drops it | no | 2,681 |
| Unread Y, correction-only relay (R1) | no | 0 |
| Unread Y, with the channel's own Y content readable (R1c) | yes, by feedback on Y71 at dimension 5 | 2,682 |
| Fixed cover: helpers not forced through `L/A/B/H` (R2) | yes, one helper through `L_102 <= H_71` | 2,682 |
| No reads of old channel-helper state (R3) | yes, one equal-frame add from `D11` at dimension 5 | 2,682 |

Among the rows computed here, two hypotheses each reopen every entry. One is
the fixed cover. The other excludes the channel's source-dependent state,
whether held in its helpers or exposed by reading targets after the channel
has written them. That state already carries
the support of `G/2`, which contains every off-diagonal requirement. At P104,
correction-only Y relay reopens nothing, although an `F_2^3` program shows it
can matter in principle. Frame descent and cross-frame mixing also break the
argument; the small-domain negative controls show this. They are not priced or
counted at P104 here. Cited, not recomputed:

- PR3013: component/containment pooling reaches all 4,992 entries.
- PR3427: a one-H2 source shear removes only the `(71,102)` requirement.

## Reproduce

From the repository root, with the standard library (about 20 s):

```sh
python3 -I -O -Werror -B research/p104-fixed-cover-cut-review/verify.py
python3 -I -O -Werror -B research/p104-fixed-cover-cut-review/test_verify.py
```

The verifier prints one JSON receipt. Its last line is

```
PASS_P104_FIXED_COVER_CUT_REVIEW layered_missing=1 sharp_missing=2682 of 4992 pr3427_masks=4 rank_U_minus_I>=17 rows=4 oracle_programs=4500 no_kappa
```

The registered replay is
`python3.12 -B scripts/research_package.py --package research/p104-fixed-cover-cut-review`.
Every check raises `SystemExit("FAIL: ...")`, so checks stay active under `-O`.

**Negative controls that must fail:**

- `test_verify.py` rejects a tampered input hash.
- It rejects an unsound "shared snapshot only" test inside the oracle.
- It rejects a wrong rectangle.
- It shows that dropping nesting changes PR3427's masks.
- Inside `verify.py`, five contract violations must each produce a coefficient
  outside both tests. They are Y read (a fixed four-operation `F_2^3` program),
  frame descent, cross-frame mixing, an off-cover flag and correlated old
  state.

## Method and independence

The code shares nothing with PR3182, PR3252, PR3259 or PR3427. Frames are
canonical reduced-echelon keys over `F_2^9`. E8 ports are enumerated
independently and sorted.

- The layered control hosts every d-flat of each interval literally, then
  takes one read-first step per layer.
- The sharp criterion is computed twice. One method uses echelon keys with
  helper-type masks. The other uses point-set bitmaps, looped per helper type.
- The rank bound uses a deterministic greedy over 104 seed columns. Each
  step adds the column that most increases `min(|R|,|S|)`, ties to the
  smallest index. Exact `Fraction` elimination gives the rank, and an
  independent integer Bareiss determinant confirms it. The greedy is not
  optimal, so 17 is a lower bound.
- Oracle programs choose uniformly among the operations legal at each moment.
  Direct X-to-Y adds are omitted so that every coefficient travels through
  helpers. Seed `20261018`, 120 operations per program, 3,000 programs over
  `F_2^3` and 1,500 over `F_2^4`. This is a bounded randomized family, not an
  exhaustive enumeration.
- Before this review, the original channel word was checked for its roles:
  X is never written and Y is never read, so K4 and K5 hold for the channel.

## Scope, inherited assumptions and open obligations

Inherited:

- PR2981's covers and the native channel frame paths, through their pinned
  JSON inputs;
- the ordered E8 ports, with the fixture's 16 removed roots;
- the contract K1-K7 in [PROOF-REVIEW.md](PROOF-REVIEW.md).

The rows and rank bound apply only under those contracts. R1c and R3 use
structural, no-cancellation dependence of the channel registers.

Open and not addressed here:

- chronology and acquisition order;
- coefficient delivery and dirty restoration;
- native lowering, precision and physical hosting;
- consumer cost and supplier admission;
- every changed-cover construction;
- a timed refinement of the sharp criterion.

No independent human or formal-kernel review has been done. The selected
cold replay is unchanged and was not rerun.

## Open next questions

1. *Is 17 the true rank bound?* A min-rank completion of `-C` on all 8,506
   unsupported pairs may force a rank well above 17. A larger rank would
   further constrain any joint native source preparation under PR3427's
   contract. A first step is an exact lower bound by larger or overlapping
   rectangles, or by a min-rank argument. It needs no new matching search.
2. *Can a changed cover reopen all 2,682 entries cheaply?* Relaxing the fixed
   cover (R2) reopens every entry at support level. The open question is the
   smallest set of off-cover helper flags that covers all 2,682 pairs, with
   its full bill. Coefficients, dirt and every cost remain unknown.
3. *Is there a non-trivial use of channel state?* R1c and R3 reopen everything
   only because the channel already carries `G/2`. One would need a
   coefficient-level construction that reads channel state and restores it,
   with an explicit list of the changed channel obligations.

## Predecessors and credit

- Nick Petalas (GitHub petalas):
  - PR2981 `3d24b92d8ba057b57cb2d480170ec407520e6882` (covers and flags);
  - PR3252 `4784b71d2e0833537c9ae1e8be05ad2a6b334d92` (memory soundness);
  - PR3259 `b572b0c25569898579041200e95731c5a43c9189` (pooled cut and
    embedding argument);
  - PR3013 (component pooling).
- dcharb78: PR3182 `ad848966cd62e13de5ad8d4b5169c221d74d2fcd` (the cut and its
  1,725/37 cones).
- commdata2338: PR3214 `faa6323371db1c5fbb43ab04c6e00715d2328bc6` (output
  repair).
- jmbarrancoml: PR3427 `344774ba08a73fc3a85fdcb93fb319927bde3ea2` (the
  one-helper lemma and the rank-four theorem extended here).
- Wentao Li for the chronology audit, which is not redone here.
- The native/compiler lineage credited in the pinned inputs: Rohan Arun/1972,
  Chafik Boukhalfa/1991, Adam Gall/1940, Josie Elliston/1071 and
  Ali Romman/1125.

Base: canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority
revision 6. [SOURCES.json](SOURCES.json) pins the three live inputs by Git blob
and SHA256.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). Apache-2.0.
