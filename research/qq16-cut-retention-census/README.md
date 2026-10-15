# In-place availability of PR2443's two-cut QQ16 observations

**Negative result (scoped screen). No kappa claim, no supplier, no controller.**
[PR2443](https://github.com/CrocSwap/integer-mult-bounds/pull/2443) (starship-s,
head `545c05e17243c962b112b91e7f84b4c1a41de7b8`) decodes all pair-0 inputs of
the conserved `F0/B_1_2` pair from 224 observed port arrays at two cuts. It
grants the retention of those arrays. This package checks which of them are
still held by a live field at a decode point of the pinned 19-event QQ16 recipe.

| item (cut) | arrays | live at d1 (after `B_1_2`) | live at d18 (after terminal) | first overwrite event |
|---|---:|---:|---:|---|
| `x1_A` (after F0) | 8 | 0 | 0 | 1 (`B_1_2`) |
| `x1_T` (after F0) | 8 | 0 | 0 | 1 (`B_1_2`) |
| `y1_A` (after F0) | 8 | 0 | 0 | 1 (`B_1_2`) |
| `y1_T` (after F0) | 8 | 0 | 0 | 1 (`B_1_2`) |
| `x1_S` (after F0) | 88 | 0 | 0 | 1 (`B_1_2`) |
| `y2_A` (after B1) | 8 | 8 (same field) | 0 | 3 (`F2`) |
| `C=x2_U` (after B1) | 96 | 96 (same field) | 0 | 2 (bridge `1->0`); 3 (`F2`) if pairs 1-3 are zero |
| **total copies needed** | 224 | **120** | **224** | |

"Live" means equal, as a linear map of all 896 initial port arrays, to some
field of the four bank pairs at that point. The zero entries also hold under
three relaxations. The array is not a nonzero scalar multiple of any live
field. It is not in the span of the two fields `X_(k,p)`, `Y_(k,p)` at any one
port of any pair. Neither statement changes if a cover map `M(g,delta)` is
applied (see "Model" below). The counts do not change if the terminal also
exchanges selected fields, or if pairs 1-3 start at zero.

Per owner per replica, the contract therefore needs these retained copies:

- **d1:** 120 copies (all F0-cut arrays), each held across one call (`B_1_2`),
  so 120 coordinate-calls.
- **d18:** all 224 copies. The 120 F0-cut arrays are held for 8 calls and the
  104 B1-cut arrays for 7 calls, so 1688 coordinate-calls.

### Comparison with the #2074 pricing (inherited, unreviewed)

philippeVV's four-bank finding (#2074, fork `680d0997`) says that with
`C = 0` the route "pays only for in-place or single-call storage". `price.py`
re-implements the `price3.py` convention (5F+4B QQ16 profile, rank-8 child
plus 8 mass per coordinate-call for centre-like storage, 72 mass per new live
family). It uses the pinned `ceiling.py`. Before transferring anything, it
reproduces three committed values of `price3.json` exactly: the selected
ceiling and the C=0 centre rows for 62 and 64 coordinates. The results are in
[PRICE.json](PRICE.json):

| convention | max coordinate-calls/replica with any positive saving | max still beating the selected ceiling | census demand d1 / d18 |
|---|---:|---:|---|
| C=0, centre-like copy | 111 | 71 | 120 / 1688: no saving at either |
| C=0, new live family | 12 | 8 | 120 / 1688: no saving at either |
| C=64, centre-like copy | 39 | 0 | none beats selected |
| C=64, new live family | 4 | 0 | none beats selected |

The literal PR2443 contract needs copies at both decode points. Even the
favourable d1 point, with single-call storage, needs 120 coordinate-calls. That
is above the C=0 positive-saving break-even of 111, and above 71 for beating
the selected ceiling. **Within this convention, the literal contract fails the
stated C=0 condition.** It also exceeds #2074 Theorem B's floor of 62, which
is consistent with that theorem. This screens one contract under one inherited
price convention. It is not an impossibility theorem for QQ16 controllers.

### Recomputation leads (not in-place availability)

Two exact identities follow from CONSERVED-QQ16 (1) and (3). The checker also
verifies both in the model.

- **L1.** F0, B1 and F2 conserve the 16 selected pair sums `X_V+Y_V=x_V+y_V`.
  Nothing writes them afterwards, so they are live two-field sums at d1 and at
  d18 (identity selected terminal). PR2443's last step `y_V=x1_V+y1_V-x_V`
  only needs these sums.
- **L2.** At d1, `x1_U = X2_U + Y2_U - K_(1,U) ell_(1,T) x1_T`. So the 88
  `x1_S` copies could be replaced by one same-port two-field read plus an
  8-coordinate driver record. Because `B_1_2` is invertible, a decoder that may
  read the whole post-B1 state of pair 0 needs no copy at d1. PR2443 excludes
  `y2_U` from its reads, so that is a different contract.

So the census prices the literal contract, not the information need. The
compressed variant is listed below as an open question.

## Model, exactness and scope

- **Maps:** CONSERVED-QQ16 equations (1) and (3). The checker binds them to the
  packet's `F_contract`/`B_contract` strings. Pins: `R`, `K=R^T/4`, the
  A/T/U96 sets and the Grams (U:48, A:4, T:4).
- **Recipe:** the literal 19-event `GLOBAL-TEMPLATE.json.gz` recipe (archive
  member sha256 `a179dad8...`). Its local pairs are `0,0,0,1,1,2,2,3,3`.
- **Bridges and terminal:** semantics follow PR2346 section 1 (alephnan, head
  `653520d7`). A bridge does `X_j,U += c X_i,U; Y_i,U -= c Y_j,U`. The
  terminal does `(X_U,Y_U) -> (Y_U,-X_U)`; the selected terminal is identity or
  the same exchange (variant).
- **Exactness:** every field is an exact rational linear form in the 896
  initial port arrays of four pairs. The executable instance is the
  owner/payload-constant subspace, where every cover map
  `M(g,delta)f(d,z)=f(d*g, z XOR d*delta)` is the identity. Any actual
  equality, even up to a scalar or a cover map, restricts to an equality
  there. So every "not live" entry is an exact counterexample for the actual
  routed maps. The only "live" entries are the post-B1 arrays at d1, where no
  event intervenes. The support argument proves them, and every survival claim
  is checked against the symbolic write sets.
- **Consistency check:** in this model, PR2443's ordered decoder recovers all
  224 pair-0 inputs exactly, including `C=-y_U` and the two-sided `R_J`
  inverse. This was implemented independently; no predecessor code is imported.
- **Not covered:** physical idle cover sweeps, terminal Y translations,
  bank padding and phase adapters. These are invertible frame changes in the
  inherited logical convention. They cannot make an overwritten logical value
  live again. Also not covered: native read legality, read and chart-map cost,
  cleanup, hosting, precision, and other contracts or schedules.

## Negative controls (all must be rejected or change the receipt)

1. Claiming `x1_A` survives B1 in place is rejected.
2. Dropping F2 (event 3) changes the d18 census to 216 copies. Eight arrays
   are then live in place, and 104 are scalar multiples of live fields.
3. Dropping B1 (event 1) changes the d1 census to 0 copies.
4. Claiming `C=+y_U` is rejected.
5. A corrupted centre coefficient fails the Gram/source checks.
6. A wrong sign of the future logger `E_t` breaks PR2443's decoder.

A wrong `11a -> 12a` coefficient in the backward `Y_T` output was also tried.
It does **not** break the decoder, because PR2443 never reads `y2_T`. That
mutation was therefore not used as a control.

## Reproduce

From the repository root (stdlib only; about 65 s and 50 s on one core):

```sh
python3 -I -B research/qq16-cut-retention-census/verify.py
python3 -I -B research/qq16-cut-retention-census/price.py
```

Expected last lines: `PASS_NEGATIVE_CONTROLS 6`, `PASS_QQ16_CUT_RETENTION_CENSUS`,
then `PASS_QQ16_CUT_RETENTION_PRICE_TRANSFER`. Each script recomputes its JSON
and requires it to equal the committed [RESULT.json](RESULT.json) (receipt
`8c57f8f5...`) and [PRICE.json](PRICE.json). Per-array rows are in
[CENSUS-ROWS.json](CENSUS-ROWS.json). Registered replay:
`python3.12 scripts/research_package.py --package research/qq16-cut-retention-census`.
The checks were run with Python 3.14.4, since 3.12 was not installed locally.

Base commit `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`. Input pins are in
[SOURCES.json](SOURCES.json). External, read-only pins: PR2443 `545c05e1`,
PR2346 `653520d7`, PR2174 `f79470a7`, and philippeVV `price3.py` sha256
`1c2ca9a4...` (fork `680d0997`).

## Open next questions

1. **What is the smallest retained record for a final-only (d18) decode with
   PR2443's read set plus legal final reads?**
   - *Why it matters:* the literal contract needs 1688 coordinate-calls, while
     the C=0 break-even is 71. A compressed record set must also respect
     #2074 Theorem B's floor of 62.
   - *First step:* replace `x1_S` by the driver record (L2) and the selected
     records by the conserved sums (L1), then rerun this census.
   - *Blocker:* the legal native read types for former-Y endpoints and
     `X+Y` sums.
2. **Can a controller use the d1 decode point at all?**
   - *Why it matters:* the demand there is only 120, and with full post-B1
     reads it is 0, since `B_1_2` is invertible. But a mid-schedule decode
     must restore what it reads before F2.
   - *First step:* price the CONSERVED-QQ16 inverse of B (`H_s`, `E_t`) as
     reads plus restoration.
   - *Blocker:* no priced read of `y2_U`/`X2_T` at the completed-X type.
3. **Which centre charge applies to QQ16, C=0 or C=64?** This is the
   maintainers' open question in #2074. Under C=64 no positive retention
   budget beats the selected ceiling.

## Credit

The observation contract and decoder are from PR2443 (starship-s). The local
maps, packet and cover semantics are from Ali Romman (PR1969,
`research/joint-query`). The bridge/terminal semantics and the 19-event
binding are from alephnan (PR2346). The two-query recovery contract is from
commdata2338 (PR2174; also PR2153, PR2376). The unread basis and 88-port
threshold are from Gareth Davidson / bitplane (PR2432). The C=64 screen and
the `y2_A` pricing are from 1337isnot1337 (PR2079, PR2197). Theorem B and the
price3 convention are from Philippe Van Velzen (#2074, fork `680d0997`). The
trace method is from Ross Richardson (PR2104). The ceiling model is
`research/complex-local-word-ceiling`. ywz65's concurrent PR2443 operator
audit is independent of this storage census.

Prepared by thakrarsagar with substantial AI assistance from Claude
(Anthropic, Claude Opus 5.5). No independent human review is claimed.
Apache-2.0.
