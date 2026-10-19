# PR2297 principal-rank floor: every scalar decoder costs at least 554

**Result: a scoped proof plus an exact finite certificate. No κ claim and no supplier.**

On the exact PR2297 five-frame cover, take any finite factorization
`c I_112 = A diag(c_t) B^T` over `Q`, or over any field. Under the full-port
tariff `rho_t = rank_F2(pairing on L_t x R_t)`, its cost is

    C = sum_t rho_t >= 554.

The direct one-term-per-port decoder attains 554, so the bound is sharp. The
zero-saving bound `C <= 492` is therefore unreachable. The unpaid budget is
`4432/9`, so every scalar decoder has deficit at most `-554/9`. **On this cover
the u=5 coverage lever row has no positive saving under the scalar contract.**
That holds for every number of terms, every support pattern (matched or
unmatched spans), every sign and every denominator.

The proof is in [PROOF.md](PROOF.md). It has two parts.

1. **Lemma 1 (principal-rank count).** For a set `S` of groups, `K[S,S] = c I`.
   Hence at least `f(S) = sum_{g in S} d_g` terms must be nonzero on `S` on both
   sides. This is a rank statement over the base field. It needs no reduction
   modulo 2, so even denominators do not matter.
2. **Lemma 2 (LP duality over flats).** Give nonnegative weights `y_S` to group
   sets. Suppose that for every pair of flats `(F, F')`, the sets meeting both
   closed group sets have total weight at most `rho(F,F')`. Then
   `C >= sum_S y_S f(S)`. A flat is the span of a nonempty group set. This
   cover has 107 of them.

[CERTIFICATE.json](CERTIFICATE.json) holds 88 sets with integer weights over
`10^6`. It satisfies all 11,449 ordered flat-pair constraints exactly, with
minimum slack `6/10^6`. Its value is `553996479/1000000 > 553`, and `C` is an
integer, so `C >= 554`.

## What is new

- **Predecessors.** PR #2879 (Arham Tahir, `research/support-balanced-port-floor`)
  proved 554 only for terms with equal complete spans. For the general case it
  gave a necessary condition: at least 16 unmatched-span terms with credit at
  least 62. philippeVV's Theorem 1 (Discussion #1587, applied to this cover in
  PR #2532) proved 554 only for 2-integral decoders. The general
  unmatched-span, even-denominator class was the open question of both packages.
- **This package** closes that class. It does so by counting ranks over the base
  field, not by a 2-adic argument. The counting constraints are weighted by an
  exact dual certificate over the cover's flats. The relaxation is tight here:
  its value is within `0.0036` of the direct cost. This also answers PR #2532's
  open question "even-denominator gain for k=5": that gain is zero.
- **Why Lemma 1 is available here.** The mask has no free pair, so every
  principal block is `c I`. On masks with free pairs, Lemma 1 holds only for
  group sets that contain no free pair. Examples are the PR2041 triad cover and
  the plane and line masks of Discussion #1587, where E8-type savings exist. This agrees with philippeVV's follow-up 4: bounds
  that also hold for line ports cap at 128 on plane covers.

## Reproduce

From the repository root, with Python 3.12 or later and the standard library
only (about 2 s and 35 MB):

```sh
python3 -B research/pr2297-principal-rank-floor/verify.py
```

The expected final line is `PASS_PR2297_PRINCIPAL_RANK_FLOOR`. The printed JSON
includes:

    "flats": 107, "flat_pairs": 11449, "certificate_sets": 88,
    "certificate_value": "553996479/1000000", "min_slack_numerator": 6,
    "floor": 554, "direct_decoder_cost": 554, "unpaid_budget": "4432/9",
    "exact_instance_cost": 691

The generic hook is
`python3.12 scripts/research_package.py --package research/pr2297-principal-rank-floor`.

### What the verifier checks

1. **Inputs.** It authenticates both pinned inputs (SHA256 and Git blob), the
   selected-replay member (SHA256) and the 112 labels.
2. **Cover.** There are 22 orthonormal five-frames and one orthonormal pair, and
   no orthogonal group pair. This is the premise `K = c I_112`.
3. **Flats.** It finds the 107 flats twice: by breadth-first closure, and from
   all group subsets of size at most five plus a closedness check.
4. **Pairing ranks.** It computes `rho(F,F')` for all flat pairs twice: by
   packed Gram elimination, and as `dim F - dim(F ∩ F'^perp)` by vector
   counting.
5. **Certificate.** It checks the dual constraint (*) for all 11,449 ordered
   flat pairs in exact integers, and computes the exact value.
6. **Sharpness.** The direct decoder costs 554.
7. **Non-closed supports.** It tries 2,000 seeded random support pairs `(P, Q)`
   that are not closed. Each satisfies (*) with ranks computed directly. This is
   a second check of the closure reduction.
8. **Exact instance.** It builds a random exact rational decoder with
   denominators 2, 4 and 8: a unit-triangular `A` with up to 160 cross entries,
   and `B^T = c0 diag(c)^{-1} A^{-1}`. It checks `K = c0 I_112` entrywise and
   checks the chain `C = 691 >= sum y_S h(S) >= sum y_S f(S)`.

**Negative controls**, each of which must be rejected:

- one certificate weight inflated by 1;
- `rho(F_2^9, F_2^9)` replaced by 8, as if the ambient pairing were degenerate;
- the line-label tariff (cost 1 per single-group pair) instead of the full-port
  tariff;
- the doubled certificate;
- a flat family missing the ambient space;
- a toy mask with free pairs (three orthogonal lines), which fails the premise
  `K = c I`.

`find_certificate.py` is a provenance helper and **not** part of verification.
It shows how the certificate was found: the HiGHS LP over 3,252 distinct
candidate sets against all flat pairs. The candidates are all 23 singletons, all
253 pairs, the full set and seeded random sets. The weights are rounded down to
`10^-6` and shrunk by 2 ppm. It needs numpy 2.5.4 and scipy 1.18.1, which are not
verifier requirements. With those pins it reproduced the shipped certificate
byte for byte. Any feasible certificate with value above 553 proves the same
floor.

## Sources and pins

- **Base commit:** `20ecf2891d80b5acf18d980b2164fb44ea7faa90` (priority revision 6).
- **Live inputs** (also in [SOURCES.json](SOURCES.json) and `VERIFY.json`):
  - `research/community-frontier1094-audit/selected-replay.tar.gz`,
    sha256 `f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6`.
    Its member `candidate/strict/global/base/work/complex-nine-native/DATA-PHASES.json`
    has sha256 `c5916ff312678f12aba403847643fbbc29f643acec60bdf836fa56cd3e8251fa`.
  - `research/kport-group-scalar-endpoint-audit/fixtures/PR2297-CANDIDATE.json`,
    sha256 `5b69c7a873f19a64ed73a1c1281d20398d2675b3281fd4fa259aed9cf91a86c0`.
    This is Cinna Davis's PR2297 cover as retained by PR #2532.
- **Certificate:** `CERTIFICATE.json`, sha256 `7c8005882d34aeef545bd3256e6da2d3cb5aa881dc70ff97363111a80adcc525`.

## Scope, inherited assumptions and obligations

- **Scope.** The exact PR2297 cover, the scalar-decoder contract and the
  full-port tariff, as defined in PR #2532 and PR #2879. This is a scoped proof
  plus a finite certificate. It is not a complete multiplication theorem.
- **Inherited assumptions.** The tariff charges each touched port's complete
  group space. The planning law is the portwise, nine-stage law of PR #2879 §3,
  which gives the unpaid budget `(8/9) sum d_i`. Both are taken as given; this
  package does not re-derive them.
- **Unresolved obligations.**
  - Lemmas 1 and 2 are elementary and written out, but have not been checked
    by a proof assistant.
  - Native frames, restoration, hosting, precision and the complete consumer
    are unpriced. They are moot for this row only because no decoder saves.
  - Other covers, other `u` values and masks with free pairs are not covered.
- **No change** to the selected result or κ.

## Open next questions

The structured versions are in [TASK.json](TASK.json).

1. **Clique-restricted principal-rank LP on the PR2041 triad cover.** Lemma 1
   still holds for group sets that contain no free (orthogonal) pair.
   - *Why it matters:* PR #2879's floor of 297 does not exclude the
     uniform-three completion, whose budget is `896/3 ≈ 298.67`. A clique LP
     value of 299 or more would close that row too.
   - *First step:* run `find_certificate.py`'s LP with the candidate sets
     restricted to orthogonal-pair-free group sets of the PR2041 cover.
2. **Free-pair masks.** Is there a principal-rank analogue for masks with free
   pairs, using only cliques of the nonorthogonality graph, that is not also
   valid for line ports?
   - *Why it matters:* philippeVV's follow-up 4 shows that line-valid bounds
     cap at 128 on plane covers, so any useful version must be plane-specific.
   - *First step:* compute the clique-restricted LP on philippeVV's a23 plane
     assignment and compare it with 128.
3. **Changed contracts.** The u=5 row on PR2297 is now closed for scalar
   decoders. Any k-port coverage saving must therefore change the mask (free
   pairs), the tariff or the cover.
   - *Why it matters:* this marks which contract change still has room.
   - *First step:* state which of these a proposed k-port contract changes
     before pricing a decoder.

## Credit and provenance

- **Arham Tahir (Arham-Tahir64).** PR #2879, head
  `17183900660480a4e8f031f117f04d79474cf63d`,
  `research/support-balanced-port-floor`. Matching lemma, equal-span floor,
  asymmetry budget and the exact cover analysis this package extends.
- **Philippe Van Velzen (philippeVV).** Discussion #1587, comments 18927273
  (Theorem 1, top-layer lemma), 18932906 (Smith lemma) and 18942562 (follow-up 4
  barriers). The full-port pricing and the 2-adic route this package bypasses.
- **Sagar Thakrar (thakrarsagar).** PR #2532, `research/kport-group-scalar-endpoint-audit`,
  commit `bcb6f278503bd2a6b3ffb9bdcfcda9f36c18d2f4`. The k-port masks, the
  2-integral floor and the retained PR2297 fixture.
- **Cinna Davis (1337isnot1337).** PR2297 cover, commit
  `49f9c1a08bf1fe67a62bd6d2825aa0d03e1b1518`.
- **Adam Gall (adamgall).** PR1889 mask and tariff foundations.
- **Tekalign (tekuuu).** PR2782, the Gram denominator gate, commit
  `002a9983079a3244c10221b4e16d0cff7e70da40`.
- **ywz65.** PR #2528, the mixed-cover weighted unpaid dimension `554/112 = 277/56`.
  It agrees with the budget `(8/9) * 554 = 4432/9`, whose integer part 492 is the
  zero-saving threshold used here.

The proof, certificate and verifier are new. The cross-checks are an
independent flat enumeration, a second rank method, random non-closed supports
and an exact rational instance. They were run by the same AI-assisted session.
There has been no human review.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). Apache-2.0.
