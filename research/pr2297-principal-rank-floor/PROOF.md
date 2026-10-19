# Principal-rank floor for scalar decoders on the PR2297 cover

All statements concern the exact PR2297 five-frame cover authenticated by
`verify.py`. The cover has 112 ports in 23 groups. Twenty-two groups are
orthonormal five-frames `E_g` in `F_2^9`, each carried by five ports. One
orthonormal pair `E_22` is carried by two ports. The pairing is the dot
product on `F_2^9`. Every port carries its group's **whole** space (the
full-port tariff of PR #2879 and PR #2532).

## Theorem

Let `F` be any field (in particular `Q`), `c in F` nonzero, and

    c I_112 = A diag(c_t) B^T,      c_t != 0,

any finite factorization over `F`. For term `t` let `L_t` (`R_t`) be the sum of
the port spaces on which column `t` of `A` (`B`) is nonzero. Let
`rho_t = rank_F2(pairing on L_t x R_t)` and `C = sum_t rho_t`. Then

    C >= 554,

and the direct decoder (one term per port) attains 554. No restriction is placed
on the number of terms, supports, span matching, signs or denominators.

**Corollary.** The zero-saving bound `C <= 492` is unreachable. With unpaid
budget `(8/9) * 554 = 4432/9`, every scalar decoder has deficit at most
`4432/9 - 554 = -554/9`. On this cover the u=5 coverage lever row has no
positive saving under the scalar contract.

## 1. Principal-rank count

The mask has no free pair. The verifier checks that every two distinct group
spaces have a nonzero pairing. Distinct ports of one group share a
nondegenerate space. So the scalar contract forces `K = c I_112`.

For a set `S` of groups, write `ports(S)` and `f(S) = |ports(S)| = sum_{g in S} d_g`.
Say term `t` **hits** `S` when both `A[ports(S), t]` and `B[ports(S), t]` are
nonzero.

**Lemma 1.** `h(S) := #{t : t hits S} >= f(S)` for every nonempty `S`.

*Proof.* `K[S,S] = c I_{f(S)}` equals `sum_t c_t A[ports(S),t] B[ports(S),t]^T`.
Only terms that hit `S` survive. A sum of `h(S)` matrices of rank at most one
has rank at most `h(S)`, so `h(S) >= f(S)`. ∎

This is a statement about ranks over `F`. It needs no reduction modulo 2, so
denominators play no role. It is false when a principal block has free entries
(control 6 in `verify.py`).

## 2. Group supports and flats

Let `P_t` (`Q_t`) be the set of groups containing a port where column `t` of `A`
(`B`) is nonzero. Then `L_t = E_{P_t} := sum_{g in P_t} E_g`, likewise
`R_t = E_{Q_t}`, so `rho_t = rho(E_{P_t}, E_{Q_t})`. Term `t` hits `S` exactly when
`S` meets both `P_t` and `Q_t`.

A **flat** is a subspace `E_P` for a nonempty group set `P`. Its closed group
set is `cl(E_P) = {g : E_g ⊆ E_P}`. It contains `P` and spans `E_P`. This cover
has exactly 107 flats. The verifier finds them in two independent ways.
(a) A breadth-first closure of the single-group spans under adding one group.
(b) The canonical reduced-echelon spans of all group subsets of size at most
five. It then checks that family (b) contains every single group and is closed
under adding any group. Hence (b) contains every flat.

## 3. Dual certificate

**Lemma 2.** Let `y_S >= 0` be weights on a finite family of group sets such that,
for every ordered pair of flats `(F, F')`,

    sum { y_S : S meets cl(F) and S meets cl(F') } <= rho(F, F').      (*)

Then every decoder of the theorem satisfies `C >= sum_S y_S f(S)`.

*Proof.* Discard terms with a zero column (they cost nothing and hit nothing).
For term `t` put `F = E_{P_t}` and `F' = E_{Q_t}`. Any `S` hit by `t` meets
`P_t ⊆ cl(F)` and `Q_t ⊆ cl(F')`. By (*), `sum_{S hit by t} y_S <= rho(F,F') = rho_t`.
Summing over `t`, exchanging the sums and applying Lemma 1 gives

    C >= sum_S y_S h(S) >= sum_S y_S f(S). ∎

This is LP duality for the relaxation that keeps only Lemma 1's
principal-rank constraints. The relaxation is exact on this cover: the
certificate below comes within `0.0036` of the direct cost 554.

## 4. The certificate and the floor

`CERTIFICATE.json` lists 88 group sets with positive integer numerators over
`10^6`. The verifier checks (*) exactly in integers for all `107^2 = 11449`
ordered flat pairs. The minimum slack is `6/10^6`. The value is
`sum_S y_S f(S) = 553996479/1000000 > 553`. `C` is a sum of integer ranks,
so `C >= 554`. Both pairing-rank methods give the same `rho(F,F')`: packed
elimination of the Gram matrix, and the count `dim F - dim(F ∩ F'^perp)` over all
512 vectors.

The certificate's shape explains the floor. Each five-frame lies in total
weight 5, and the residual pair in total weight 2. These are the constraints
`(E_g, E_g)`, which cost `d_g`. The total weight is `449997/50000 < 9`. This is
the constraint `(F_2^9, F_2^9)`: a term meeting every group on both sides costs
9 and hits every set. Sets have sizes 4 to 20. By (*) on single-group flats,
two groups whose pairing has rank `r` lie together in total weight at most `r`.
This is how the certificate charges the off-block corrections that a cheap
shared term creates.

## 5. Scope

- Complete for scalar decoders of this exact mask and full-port tariff, over
  any field. It contains PR #2879's equal-span floor and the 2-integral floor
  (philippeVV, Discussion #1587 Theorem 1, applied in PR #2532) for this cover.
  It settles the open unmatched-span, even-denominator class: PR #2879 §4 showed
  a saving would need at least 16 unmatched-span terms with credit at least 62.
  No such decoder exists.
- It does not apply to masks with free pairs. There a principal block need not
  be `c I` and Lemma 1 can fail. Examples are the PR2041 triad cover and the
  plane and line masks of Discussion #1587, where E8-type savings exist. This
  agrees with philippeVV's follow-up 4: bounds that also hold for line ports
  cap at 128 on plane covers. Lemma 1 does not hold for line masks with free
  pairs.
- It prices no native frame, restoration, hosting, precision, consumer, other
  cover or other `u`. No supplier or κ follows.
