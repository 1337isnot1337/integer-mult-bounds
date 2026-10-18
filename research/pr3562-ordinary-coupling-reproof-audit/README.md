# Independent reproof of the arithmetic layer of PR3562's ordinary-rate theorem (no κ)

**Result.** I reproved the arithmetic layer of the all-size ordinary-rate theorem in
[PR3562](https://github.com/CrocSwap/integer-mult-bounds/pull/3562) (Jose Manuel,
`jmbarrancoml`, head `abb93be8b9ceca07a2b17f3a97db7bb6b074271d`) from its stated
premises. Every audited arithmetic step holds:

- (a) the two moment certificates;
- (b) the C0 majorant;
- (c) the e ≥ 2^20 selector fit;
- (d) the composed bound `T_B(e) <= 4283584 C V e^(1-a)` with `a = 576/332929`;
- (e) the Consequence arithmetic.

The audit is conditional on PR3562's line-154 physical bound, called P5 here:
`T_B(e)/V <= C(801n + 4000000 n^(1-c) w + k + w + 1)`. P5 is PR3562's own derivation
step (lines 141-154), which I take as a premise. Its coefficients are one line of
arithmetic: two reversed C0 calls, each on padded volume below 2V, times majorant (1),
plus the wrapper bill. That gives 801 = 2·2·200 + 1 and 4000000 = 2·2·10^6. The physical
claims behind that line are not audited here (see Inherited assumptions).

I found one **exposition gap** and no mathematical gap. Line 156 lists `n <= e^(1-c)`,
`w <= 2e^c` and the bound `n^(1-c) w <= 2^c e^(1-a)` of line 158. Line 158 is stated
without derivation, and the two bounds listed beside it do not imply it. An exact
witness exceeds it by the ratio 2^(1-c). The inequality `n <= e/w`, which follows from
the selector definition `n = floor((e-k)/w)` on line 117, does imply it. So line 158
and `4283584` hold as written. Deriving line 158 from the two line-156 bounds alone
would give only a factor of 2 and the coefficient `8033584`, with the same O-bound.

For the consumers [PR3576](https://github.com/CrocSwap/integer-mult-bounds/pull/3576)
(Hiroki KUMAZAKI, `kumagi`) and [PR3690](https://github.com/CrocSwap/integer-mult-bounds/pull/3690)
(`zxv`): the arithmetic layer they inherit holds, including 4283584, conditional on P5
and PR3562's other retained premises. This narrows, and does not lift, PR3576's stated
limit that the all-size PR3562 theorem is not independently reproved. Still unaudited
are lines 141-154 (the physical composition behind P5), lines 84-104 (history,
preparation and reserve), lines 172-174 (binary transfer) and lines 20-25 (space
bound, borrowed-input restoration and ownership). PR3690's R437 moments are not
checked here.

**Scope.** This is an independent check of a scoped all-size arithmetic implication,
P1-P5 ⇒ (2) and the Consequence. It assumes PR3562's retained source/refinement and
physical-cost premises and does not admit them. It is not a κ, not a frontier change
and not a complete multiplication theorem.

## What is checked, and how

[PROOF.md](PROOF.md) has the written reproof, the gap classification and the ceiling
remark. [verify.py](verify.py) is stdlib-only, uses exact `Fraction` arithmetic, takes
about 5 s and stays under 40 MB RSS.

- **Two exact engines** for the moments μ_t = (Σ_r H_r (r/64)^t + εF(1/64)^t)/W.
  Both use the same two methods PR3562 says it used (lines 64-72), but I implemented
  them independently without reading PR3562's code:
  - E1, integer-root bisection: z^q·64^p ≤ r^p·Q^q < (z+1)^q·64^p, at Q = 2^128
    (PR3562 uses 2^160);
  - E2, a rational interval series: atanh-based logarithms and a Horner exp with a
    Lagrange tail, using outward dyadic rounding.

  μ_1 = 2874298095721977/2890625000000000 < 199/200. Both engines enclose μ_(576/577)
  as 0.999998938581682162866772413602788… (the verifier prints widths 9.358e-38 for E1
  and 1.695e-77 for E2). Both enclosures lie inside PR3562's stated 10^-30 enclosure,
  and 10^6(1-μ) = 1.0614 > 1.
- **Source binding to main.**
  - H and W are the selected bit supplier's "nine" profile and live count in
    `research/e8-bit-p111-tuned/tune/EXPECTED.json`. Its `bit_lower` equals the selected
    `ASSEMBLY.json` endpoint.
  - εF/W is the literal in `research/lean-bit-moment-discharge/lean/Selected.lean`.
  - The selected certificate hash is checked through `certificates/selected-result.json`.
  - E2 shows that the selected `bit_saving` 0.001733427039589844234749 is the
    fallback-inclusive root truncated to 24 digits. The fallback-free root lies about
    2.0e-12 higher; that figure comes from decimal cross-checks in the review passes,
    and verify.py certifies only that it lies above b_sel + 10^-24. E1 brackets the root
    in (10/5769, 9/5192).
- **Steps (b)-(d) parametric** in rational c ∈ (17/10000, 1/512). Lemma B covers any
  histogram whose moments satisfy A(1-μ_1) ≥ 1 and M(1-μ_t) ≥ 1. At c = 1/576 with
  M = 10^6 (PR3690's choice), the (c)-(d) arithmetic also gives 4283584. This holds
  provided PR3690 keeps the same selector and stock definitions (D with child rank 42,
  K), the same P5 composition and A = 200.
- **Line-158 witness.** At e = 2^q with c = p/q, the values n = e^(1-c) and w = 2e^c
  satisfy both line-156 bounds with equality. They exceed line 158's bound by exactly
  2^(1-c) > 17/16. They also violate n ≤ e/w and w = ceil(e^c) (line 18), so the
  selector excludes them. The verifier checks this exponent arithmetic. The
  classification as an exposition gap rests on the written argument in PROOF.md.

## Reproduce

From the repository root, on base `20ecf2891d80b5acf18d980b2164fb44ea7faa90`:

```sh
python3 -B research/pr3562-ordinary-coupling-reproof-audit/verify.py
```

Expected last line:

```text
PASS_PR3562_REPROOF_AUDIT: audited arithmetic steps (a)-(e) hold from P1-P5; line-156 bounds alone give factor 2, n <= e/w from line 117 gives 2^c; coefficient 4283584 justified
```

To also check PR3562's exact bytes and literals, run:

```sh
git fetch origin pull/3562/head
git show abb93be8b9ceca07a2b17f3a97db7bb6b074271d:research/retuned-ordinary-coupling/PROOF.md > /tmp/pr3562-PROOF.md
python3 -B research/pr3562-ordinary-coupling-reproof-audit/verify.py --pr3562-proof /tmp/pr3562-PROOF.md
```

The expected PROOF.md sha256 is `3e554832c38b4b801f55b20868679f3283bc90cd5a9d8ce1960f828ed2655f22`.
That file is not vendored, because the package pin format accepts only same-path head pins.

**Negative controls.** These seven run through the same `audit()` function and must
each be rejected; the verifier fails if any is accepted:

| control | rejected at |
|---|---|
| c = 9/5192, just above b | (a) μ not below 1 |
| c = 10/5769 with M = 10^6 | (a)/(b) M too small |
| H_7 + 1 | source binding |
| fallback term dropped | (a) outside PR3562's enclosure |
| reciprocal j = 576 | (e) |
| reciprocal j = 578 | (e) |
| factor 2 instead of 2^c | (d) 8033584 ≠ 4283584 |

The "fallback dropped" control fails only against PR3562's stated enclosure. At
c = 1/577 the fallback-free moment would still satisfy 10^6(1-μ) > 1. The need for the
fallback term comes from the G(f) term in Lemma B's written proof, not from this control.

I froze the code before the single control sweep (verify.py sha256 recorded in VERIFY.json).

## Ceiling remark (proof shape only)

The c(1-c) shape needs μ_(1-c) < 1, which means c < b. So on the selected bit program
its exponent has supremum b(1-b) = 0.0017304222702882630233…, which is not attained.

PR2979, PR3633, PR3642 and PR3653 state κ = X − 10^-46 − 10^-70 under the modern outer,
so I compare against their primitive complex lower bounds X. This is primitive against
primitive. It avoids the mixed a/(1+a)-versus-modern-κ comparison that the sibling PR3700
withdrew.

- The reciprocal a = 576/332929 exceeds X for PR2979 (+1.0646e-6) and PR3633 (+2.246e-9).
- It falls short of X for PR3642 (−2.958e-7) and PR3653 (−3.203e-7).
- The supremum b(1-b) exceeds PR3653's X by 3.371e-9, so only a narrow window of
  non-reciprocal c just below b clears PR3653 (example in PROOF.md).
- On a different supplier, pending PR3690 (R437, c = 1/576) reports a = 575/331776. That
  exceeds every X here, by at least +2.678e-6 (PR3653). So this ceiling matters only if
  R437 is not admitted. R437's moments are not checked here.

These are statements about the proof shape, not a claimed endpoint.

## Inherited assumptions and unresolved obligations

- P5 is assumed, not audited. It rests on these physical claims (PR3562 lines 141-154):
  - there are exactly two reversed C0 calls;
  - each call's padded volume is below 2V;
  - each call costs its padded volume times the normalized time T at the same n;
  - the wrapper bill CV(n+k+w+1) is complete.
  Also assumed: the retained PR2753/PR2809/PR2899/PR2808 inventory, history and
  wrapper arguments.
- Not audited: history, preparation and reserve (lines 84-104), the bit-wrapper
  transfer to binary width E (lines 172-174), and the O_q(V)+F_q space bound with its
  borrowed-input restoration and ownership claims (lines 20-25).
- The elementary branch is read as costing at most C·V·e. PR3562 names the "elementary
  fallback coefficient" on line 142 and uses it on lines 165-166, but does not write
  that form explicitly.
- PR3562's code, EVIDENCE.md and factory are not reviewed. They were deliberately not
  read, to keep this reproof independent.
- Not re-audited: PR3576's T74 step, and PR3690's R437 source binding and moments.

## Open next questions

The structured form (question, why_it_matters, first_step, blocked_by) is in
[TASK.json](TASK.json).

1. **Derive line 158 in PR3562?** Citing `n <= e/w` (line 117) at lines 156-158 makes
   the written derivation match the stated bound. This is the author's call. First
   step: a one-line edit to PR3562 PROOF.md.
2. **Audit the physical inputs behind P5.** Its arithmetic is checked here. The
   remaining trust lies in four claims: exactly two calls, padded volume below 2V per
   call, cost scaling with padded volume at the same n, and a complete wrapper bill,
   plus the elementary cost ≤ C·V·e and setup absorbed into C. First step: trace them in
   PR2899/PR2808's wrapper bill.
3. **Decoupled width exponent.** With w = ceil(e^γ) and γ < c, the shape's saving
   becomes c(1-γ), not c(1-c). The retained PR2753 history estimates need
   γ ≥ 17/10000. Does a decoupled γ raise the reach to about b(1 − 17/10000)? First
   step: redo (d) with separate γ and recheck lines 86-97.
4. **Recheck PR3690's R437 moments at c = 1/576.** PR3690 reports its own two-engine
   enclosure. Still open: an independent recheck with this package's engines, and
   binding of its R437 histogram to source. Blocked by: not reading PR3690's pipeline
   in this audit.

## Credit and provenance

- Object: PR3562 by Jose Manuel (`jmbarrancoml`), head `abb93be8b9ceca07a2b17f3a97db7bb6b074271d`.
  It builds on David Arias's PR2753 (`DavidAriasC`), Jose Manuel's PR2809 and PR2899,
  and Nick Petalas's PR2808 (`petalas`), as credited there.
- Consumers named, not re-audited:
  - PR3576, Hiroki KUMAZAKI (`kumagi`), head `1630afea0fc1083717b5b2799b8de7a819a6ea02`;
  - PR3690, `zxv`, head `03c141ef1fd372cf42951488767537e55675c072`.
- Endpoints cited:
  - PR2979, `mdumitrean`, merged archive, head `be191346391661f4d35fc0d1508d0a6029572576`;
  - PR3633, Pierre-Loic Doulcet (`hexapode`), head `2969dce9739c4043330ddf76f395ca0dd3a90baa`;
  - PR3642, `roger-sato`, head `6568db75adbb61437190545f6fef1534c70e91e5`;
  - PR3653, `rohanarun`, head `607a09ff441c79b215a8127a81f4cc70021d0d9b`.
- Convention note: PR3700 (this account's sibling loop, head `aa0bd9fbc8700506b1fafcc55bca9bd32aced7d9`).
- Selected bit supplier and moment literal: `research/e8-bit-p111-tuned` and
  `research/lean-bit-moment-discharge` on main, credited in their own packages.

The verifier and proof were reviewed by four independent AI review passes in the same
loop: reproducibility, adversarial mathematics, provenance and referee. This is not
human review, and none is claimed. Source pins are in [SOURCES.json](SOURCES.json).

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from Claude
(Anthropic, Claude Opus 5.5). Apache-2.0.
