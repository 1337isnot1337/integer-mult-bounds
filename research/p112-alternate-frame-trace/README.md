# Three rectangle caps exclude a P112 common frame

For the explicit asymmetric rank-eight anchor on physical groups
`[1,2,27,28]`, the common source/reader frame selected by anchor axes
`[6,1,11]` cannot be extended to groups 3 and 4 while satisfying all
mandatory complete-group rectangle ranks. This holds for every rational
split of that frame, including degenerate cases and unrestricted coefficients.

Three caps suffice. They force an exact trace to be both zero and minus four:

```
trace((W-I)Q) + 7 det(S4) - 2 det(I3-Q[:3,:3]) = -4.
```

The cap and projector premises force all three terms on the left to vanish.
The proof uses formal polynomial identities, without coefficient samples,
parameter grids or a computer algebra solver. See [PROOF.md](PROOF.md) and
[the independent derivation](INDEPENDENT-PROOF.md).

## Exact scope and relevance

The fixed anchor, common annihilators and physical labels are fully specified.
The verifier reconstructs the rank factorization, checks all 225 nonempty
anchor rectangle inequalities, regenerates the saturated flags and derives
the complete normal form `P=diag(1,Q,0)` for rank-two idempotent `Q`.
The necessary caps are masks 34, 22 and 28 in group order
`[1,2,27,28,3,4]`, with physical ranks 4, 6 and 7 respectively.

The earlier local fixture passed the first two caps. This result excludes
all rational alternatives in its common frame, not just that one fixture.
Other common frames and other anchors are outside the claim. In particular,
this proves neither a global 334 floor nor a decoder of cost 296. The latter
is the first integer target below the optimistic threshold `2672/9`; an
improved selected bound requires a stronger complete invoice and supplier.
No selected result changes.

`FIXTURE.json` is new explicit local research data. Its old local receipt
hashes record provenance, not accessible Git dependencies or accepted proofs.
The primary verifier recomputes every property needed from those records,
including equality of the saved and regenerated flag spaces. Runtime geometry
comes from the two exact source inputs declared in `SOURCES.json` and
`VERIFY.json`. Frozen predecessor files remain unchanged.

## Reproduce

From the repository root, using Python 3.12 or later and the standard library:

```sh
python3 -I -O -Werror -B research/p112-alternate-frame-trace/verify.py
python3 -I -O -Werror -B research/p112-alternate-frame-trace/independent.py
python3 -B scripts/research_package.py --package research/p112-alternate-frame-trace
```

Both scientific commands compare their exact recomputations with committed
receipts and leave all files unchanged. `--write-receipt` is an explicit
maintenance option. The two implementations share literal input data, but
not arithmetic or polynomial code. Their identities use sixteen free entries
of `Q` and six variables for the complete rank-at-most-one parameterization.
The primary detects a changed physical compression coefficient and a reversed
certificate sign. The independent implementation retains a two-cap positive
fixture showing why the third cap matters.

These are exact arithmetic and written proof checks, not a proof-assistant
kernel or independent human review. No full multiplication cold replay is
relevant to this isolated negative result. Native routes, scalar execution,
owned/borrowed state, dirty restoration, storage, precision, all-size compiler
and complete supplier admission remain unproved; their cost is not zero.

## Provenance, overlap and credit

Based on canonical main `12fa8c5c844be21bfefb38a19503fbd867a11244`, priority
revision 7. The donor's existing decoder assignment takes precedence over a
new task draw; `TASK.json` records that scope change. The 20 October 2026 public
API scan covered all 354 open PRs. Nearby work included #4219 (actual-basis
C1 invoices), #3604 (tetrad co-delivery), and #4204 (paid helper return), with
different premises. Fresh Discussion coverage was unavailable after a
persistent HTTP406, so this is not a novelty certificate.

The fixed cover and canonical decoder are from flyingviper's
[p112-rational-decoder-gate](../p112-rational-decoder-gate/README.md), retaining
Cinna Davis's P112 cover lineage, Sagar Thakrar's scalar-mask/full-group audits,
Adam Gall's mask obstruction, ctoth and Philippe Van Velzen's endpoint and
whole-space pricing framework, and Hanson Sun's excess-rank/projection work.
The selected physical labels are retained through the adaptive-kernel-demotion
source and its upstream contributor notices. The current proof does not claim
those predecessor results as new.

The new contribution is the complete selected-frame normal form and the
three-cap trace contradiction, with separate implementations. Prepared by
flyingviper with substantial OpenAI Codex assistance and separate AI-agent
mathematical checks. Apache-2.0.

## Open next questions

- Classify the remaining common frames by anchor-preserving invariants. Start
  with the general flag incidences and nondegenerate source/reader pairing;
  an all-cap extension or an all-frame obstruction is still missing.
- For the constructive route, give one sparse characteristic-dependent
  endpoint whose complete physical bill saves. A scalar identity alone does
  not supply the omitted native and supplier obligations.

`TASK.json` records the first steps, relevance and blockers explicitly.
