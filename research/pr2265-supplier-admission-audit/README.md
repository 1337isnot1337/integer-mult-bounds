# Supplier-admission audit of the #2265 substitution, traced into PR2260

**Status: adversarial audit / research note. No new kappa, no construction.**
No FALSE or MISSING-PROOF premise was found. The finite premises were checked here
with independent code. The remaining premises are interface hypotheses located in
the sources but not provable from shipped data.

## Question

PR #2265 (DreamingOfClouds, head `49ce38fe`) applies the PR1673 capped phase-cell
fusion outer to the PR2260 selective-borrowing supplier (Dugongue, head `fde6b107`).
Its README marks three substitution items as "inherited from PR2260; not
re-derived": the completed-call/dirty-borrowing premise, the semantic guard, and
the equal-chunk bit interchange. The PR asks for an independent check. This audit
asks whether each supplier-admission premise of the substitution has a supporting
statement or data check in PR2260, and whether it holds on the shipped data at
#2265's final point. The audit covers four groups:

- (A) Borrowing stays inside the call and is restored.
- (B) The guard, C_0 and row constants.
- (C) The retained bit endpoint and the interchange premise.
- (D) The numeric substitution facts.

The stop-parameter relations are already #2265 ledger rows and were audited for
T74 in #2286, so they are excluded.

## Result

[INVENTORY.json](INVENTORY.json) lists 15 premises with file:line pins and one
class each:

| Class | Count | Premises |
|---|---:|---|
| COVERED (checked by #2265 or a PR2260 check it reruns; independently re-confirmed here) | 6 | A3 hosting 72x436, C1 bit endpoint, D1 73²>2·48², D2 W/mass/deficit, D3 q<a_eff<b<c, D4 endpoint and kappa |
| TRUE-unencoded (true under an independent exact check; not a #2265 ledger row) | 4 | A1 call closure, A2 restoration replay, B2 C_0<2^210000, B3 row 16467<20161 |
| INHERITED-traced (statement located; interface premise not checkable from finite data here) | 5 | A4 serialization windows, B1 semantic guard units, C2 equal-chunk interchange, C3 C_1=1, D5 surcharge portability |
| MISSING-PROOF / FALSE | 0 | none |

What the independent checks establish:

- **A1, call closure.** Both orientations of the literal local word were checked: 21,065 forward and 21,381 backward events. Every event touches only the call's 660 public arrays (224 data, 436 helpers) and 76 owned private arrays. No event references any of the 44 removed aliases.
  - All 44 borrowed sources are public inputs of the same call. Handoffs occur exactly at those sources, with paid rank 0.
  - All 31,392 owner rows lie in inherited pending children of the same hosted parent. Within each child the rows form disjoint exact prefixes, and no row uses an active data family of its own call.
- **A2, restoration.** An exact replay over a free group of reference-change symbols with rational coefficients was written for this audit. It starts every public array as an independent label, so arbitrary dirty contents are covered.
  - In both orientations, all 660 columns end at the declared normalized shear and all private arrays end at zero.
  - The paid profile is {1:2424,2:418,3:429,4:141,5:42,8:8}.
  - This is a third replay of PR2260's event model, not a different model; see Scope.
- **A3/D2, owner recount.** The pending children were reconstructed from the hosted parent's pooled blocks plus its idle residuals: 16,128 children with rank mass 387,072. The new owners host 254,088, leaving 132,984.
  - The residual histogram {1:1724,3:20,5:1469,6:18,7:494,32:11,39:7,48:2493} reproduces PR2260's EXPECTED and its PROOF.md partition.
  - 72·local + residual equals the SPEC profile, with mass 520,704 and deficit 2,560.
- **B2/B3, finite constants.** The values were recomputed from the retained formulas: 7745 physical families, stock bit length 2641, row 16467 < 20161, and 200012 required C_0 bits. The |O(2k+1,2)| formula was checked by brute force for n = 3 and 5.
- **C1, bit endpoint.** c equals PR2260 BIT-EXPECTED, which is byte-identical to the base `research/e8-bit-p111-tuned/tune/EXPECTED.json`. The conservative bit moment at c is 1 − 1.599e-24.
- **D3/D4, endpoint and ordering.** The moments were evaluated with 320-digit correctly rounded decimal ln/exp, with error below 1e-316:
  - native moment at C: 1 − 8.387e-12;
  - conservative moment at C: 1 − 2.884e-200;
  - conservative moment at C + 1e-200: 1 + 3.157e-202.

  In exact rationals: a − q = 5e-281, b − a = 1.5e-280, c − b = 5.0014e-5, and kappa = C − 1e-246 − 1e-222.

### New observations (not defects)

1. **One borrowed source is a data input.** 43 of the 44 borrowed sources are helper inputs. The other is register 73, the X-side data input, borrowed for removed alias 653. Prose in both PRs speaks of dirty *helper* borrowing.
   - This stays inside the call.
   - In the forward orientation it is returned to its input.
   - In the backward orientation it ends as the declared shear column X_73 − Y_185.
   - So the "completed call" premise holds for this word, but a reader should not take "borrowed = helper" literally.
2. **Unit question for the guard (B1).** In the selected lineage the prefix allowance is a *fixed* 512-bit count, compared with a lambda-free prefix (`docs/research/community-batch952-review.md:51`, `scripts/verify_frontier1094.py:94`, `direct-delivery504-global/code/invoice_final.py:238-241`). PR2260 instead declares the 512 payload a *per-lambda* coefficient, with guard 244·lambda (`finite-invoice.json` precision_units).
   - Under the fixed-bit reading, 244·lambda < 512 only for lambda ≤ 2.
   - Under PR2260's per-lambda reading, its row formula `2*stock_bits + 9909 + 252 + 2*payload` still counts `2*payload = 1024` as fixed. If that term scaled, row < 20161 would need lambda ≤ 4.
   - Neither PR defines lambda here or says how the row allowance scales with it.
   - For #2265 the PR1673 outer needs only an O(g) supplier guard constant (review, lines 73–78). The question bears mainly on PR2260's own balanced-prefix outer, whose degree gap uses 20161. It is an open interface question, not a counterexample.
3. **Identical invoice fields are explained, not copied.** PR2260's physical_stock_bits 2641, row 16467 and required_C0_bits 200012 equal direct-delivery504's exactly. The reason is that both stocks (7682 and 7745 families) have the same bit length after multiplying by |O(73,2)|, and the C_0 field is dominated by 2^100000.
4. **Surcharge portability.** The conservative surcharge used by #2265's endpoint comes from the vendored `moment.py`. Its own comment calls the envelope "only conditionally portable to the new cover". Neither PR proves that portability; it is inherited.

## Reproduce

From the repository root, after `git fetch origin pull/2260/head pull/2265/head`.
The verifier attempts this fetch itself if the pinned heads are absent.

```sh
python3 -B research/pr2265-supplier-admission-audit/verify.py
```

Expected output, in about 3 seconds with stdlib only (Python ≥ 3.11):

```
PASS_PR2265_SUPPLIER_ADMISSION_AUDIT controls_rejected 13 of 13
```

The full receipt is compared with [EXPECTED.json](EXPECTED.json). Use `--write` to regenerate it.

### Negative controls

Each control must be rejected by the named check:

- **Borrowed source.** Moved to a removed alias, or to register 2000 outside the call.
- **Events.** One ADD reads a removed alias.
- **Replay.** One logical monomial warp is dropped, or one helper ADD coefficient is doubled.
- **Owner rows.** One row overlaps the previous block, or one row is placed on its call's active data family.
- **Halving guard.** A mass-preserving child rank 52 (48 + 4 → 52) is introduced.
- **Row guard.** The payload is scaled by lambda = 5.
- **Endpoint.** It is raised by one 1e-200 grid step.
- **Kappa.** It is raised by 1e-240.
- **Bit endpoint.** It is set equal to b, or raised by 1e-18.

## Sources and pins

- Base commit: `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`. Base-tree inputs are pinned in [SOURCES.json](SOURCES.json):
  - `research/e8-bit-p111-tuned/tune/EXPECTED.json` (sha256 `b9f0e5ca…`);
  - `research/direct-delivery504-global/evidence/audit/PREFIX-AND-INVOICE.json` (sha256 `ce1bfa49…`).
- PR2260 head `fde6b107e26a14da5bac5b66913c914708ea6901` and PR2265 head `49ce38fee91f33edb54645724e7be9530f5631f6`. The 18 blobs read from these heads are SHA-256 pinned in `verify.py` (`PINS`). Examples: forward trace `a9d513bc…`, OWNERS `892b49f9…`, HOSTED-PARENT `f713f8e6…`, ENDPOINT `aefecb3b…`, LEDGER `df357ddc…`.
- No code from either PR is imported or executed. The vendored copy of PR2260 inside #2265 is byte-identical to PR2260's head, verified with `diff -r` during the audit.

## Scope, inherited assumptions, unresolved obligations

- This is a finite data audit at one point: #2265's final point and PR2260's shipped word. It is not a proof of the capped-fusion theorem, of the all-size compiler, or of any multiplication theorem. #2284's "modern outer" point was not audited.
- The replay is limited to PR2260's event model:
  - It checks the literal events under PR2260's documented semantics: free reference-change symbols, GF(2) frames, destructive COPY/CLEAR. It was written after reading PR2260's description and its row interpreter, so it is an independent *implementation* of the same model, not an independent model.
  - The native Clifford lowering, phases, the lambda-fold lift and the physical charts are not rechecked.
- The 63-bit ideal local bound is taken from PR2260's precision receipts and is not recomputed. The 160 time windows (A4) are not re-derived.
- All INHERITED-traced items remain open obligations of PR2260 and PR1673: the all-size fixed-tape/route realization, the exact completed-child interface, the C_1 = 1 semantic guard, the equal-chunk interchange, and surcharge portability.
- The #2265 conclusion stays exactly as conditional as PR2260 and PR1673. This audit removes no hypothesis; it confirms that the finite supplier premises hold on the shipped data.

## Open next questions

1. **Guard units (B1).**
   - *Question:* is the retained row allowance 20161 per-lambda or absolute, given PR2260's per-lambda payload?
   - *Why it matters:* under the lineage's fixed-bit reading, PR2260's 244·lambda guard fits 512 only for lambda ≤ 2. Under a per-lambda reading of `2*payload`, the row guard holds only for lambda ≤ 4.
   - *First step:* locate the retained interface's definition of lambda and of the row coefficient in the selected lineage (direct-delivery504 / PR523 invoice notes), then restate PR2260's row in matching units.
   - *Blocker:* the definition of lambda in the all-size compiler is spread over historical notes.
2. **Surcharge portability (D5).**
   - *Question:* does the bad-residue surcharge envelope "32 m ΣH / 10^16 W" port to the PR2260 cover?
   - *Why it matters:* #2265's endpoint C is certified against the conservative moment, so C depends on this envelope.
   - *First step:* find the derivation of the envelope in `research/frame-domain-ceiling` and list its cover-specific hypotheses.
   - *Blocker:* the derivation may only be in older PR discussions.
3. **Data-input borrow.**
   - *Question:* should PR2260's prose state that one alias borrows the public X_73 input?
   - *Why it matters:* the outer's interface sentence speaks of dirty helper/spectator coordinates only. Data borrowing is invisible at the call boundary, but the prose should match the data.
   - *First step:* a one-line note in PR2260's PROOF-LOCAL.
   - *Blocker:* none.

## Credit

The audited and predecessor work is by:

- PR #2265: DreamingOfClouds, the outer retune.
- PR #2260 and #2284: Dugongue, the selective-borrowing supplier and owners.
- PR #2226: Cinna Davis / 1337isnot1337, the borrowing architecture.
- PR #1673: Vlado-V, the capped phase-cell fusion outer and its substitution review.
- PR #2220: jeremykothe2, the retune ledger.
- PR #2180 / #2161: dataisfire.
- PR #1786 and #1758.
- The e8-bit-p111-tuned and direct-delivery504 packages.

Concurrent related audit: #2286, which covers the T74 side-condition inventory and states that supplier admission was not checked there.

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5). Apache-2.0.
