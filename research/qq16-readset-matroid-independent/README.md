# QQ16 optimal read sets: independent check of the 45-set classification and rank 66

**Status: independent verification. No new κ, no supplier, no construction.**

This package rechecks the finite claims of
[PR2389](https://github.com/CrocSwap/integer-mult-bounds/pull/2389) (head
`aed06c8f8d60ce97b7eb3a7c6c17ad12cbe1e863`) and the rank premise of
[PR2354](https://github.com/CrocSwap/integer-mult-bounds/pull/2354) (head
`308ebc7405303bb7ed91b012bb705949c6091a16`) for the QQ16 common-first-axis
hidden-input family. It reads only main's pinned sources and uses different
methods from both PRs. Every compared claim is reproduced and **no discrepancy
was found**. The package also contains a written audit of PR2389's adaptive
transcript-fiber argument (section 4).

| claim (source) | this check |
|---|---|
| 47 first-axis groups; axis-2 group C has 30 ports and rank 8; all other groups have independent columns; rank L = 74 (PR2354) | reproduced |
| dim V = 96 - rank R_U = 88; R_U R_U^T = 48 I; R_A R_A^T = 4 I | reproduced |
| rank(H\|V) = 66 and ker(H\|V) = K = ker R_C, dim 22 (PR2354/PR2389) | reproduced by a **different certificate** (section 3) |
| exactly 45 optimal 66-port read sets (PR2389) | reproduced by the **complement classification** (section 2) |
| 22 mandatory ports 1-5, 93-109 | reproduced |
| 29 nuisance coordinates C - {77}; 77 is the only coloop of R_C | reproduced |
| port 77 swaps for exactly 44 ports; the 45 omissions listed in PR2389 RESULT | reproduced (same list) |
| dual vector w = (-1,0,1,0,1,0,1,0) up to sign, w r_77 = -4, alpha_p in {±1/2} on 44 ports | reproduced |

## Reproduce

From the repository root (Python 3.10+, standard library only; ~10 s):

```sh
python3 -I -B research/qq16-readset-matroid-independent/verify.py
```

Expected output (the run also checks byte-equality with `RESULT.json`):

```text
PASS_QQ16_READSET_INDEPENDENT rank_H_V=66 optimal_sets=45 mandatory=22 nuisance=29 swaps77=44 owner_minor=47x47 controls=10 no_new_kappa
```

Tests: `python3 -B -m unittest research/qq16-readset-matroid-independent/test_verify.py`
(5 tests: positive replay, receipt invariants, tampered receipt, tampered
source bytes, wrong claims). Metadata: `python3 -B scripts/research_package.py
--package research/qq16-readset-matroid-independent --check-only`.
It was run locally with Python 3.14.4. The generic Python 3.12 hook was not run
because no 3.12 interpreter was available.

## Sources and independence

Live inputs, pinned by SHA256 in [SOURCES.json](SOURCES.json) and in `verify.py`:

* `research/joint-query/certificate.json.gz`
  (`a5ed85fa…49f7`): `R_rows` (8×112, integral), `A_ports`, `T_ports`,
  `U_ports`, and `map_registry` (`owner_right_matrix_columns`, 1408 distinct
  non-identity owners).
* `research/community-frontier1042-audit/selected-replay.tar.gz`
  (`22c3f4dc…b754`), member
  `t16/global/base/work/complex-nine-native/DATA-PHASES.json`
  (`c5916ff3…51fa`): per-port chart `idle_children[0].orthogonal_axes`.
  The first axis b_p is entry 0.

Base commit: `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2` (priority revision 4).
No code from PR2354 or PR2389 is imported, copied or executed. Their READMEs and
RESULT files were read to state the audited claims (the `CLAIMS` constant in
`verify.py`, used only for comparison) and to locate the source members and
the owner-column convention. Rank is computed by fraction-free Bareiss
elimination over Z. Kernels use exact `Fraction` reduced row echelon form.

## 1. Family and objects (as defined by PR2389, not re-derived)

V = ker R_U ⊂ Q^96. For an owner d in the cover group G, f_b(d) = bit_0(d b),
where d acts on the bit vector b through its GF(2) column list. Then
H(c)(d) = Σ_{p∈U} r_p c_p f_{b_p}(d) = Σ_b f_b(d) L_b(c), with
L_b(c) = R_{C_b} c_{C_b} for the first-axis groups C_b. As a source-binding
check, all 96×8 = 768 common-axis routes are present in the packet registry.
For every ordinary port p and stage s = 1..8, a registered owner maps p's
8-axis chart (first axis first) onto e_{9+8(s-1)+i}.

## 2. Complement classification (replaces PR2389's 67 kernel-rank checks)

Let S ⊂ U be a read set with |S| = 66 and T = U - S (|T| = 30). Write
K_S = V ∩ {c_S = 0}. Then **K_S = ι_T(ker R_T)** because c_S = 0 leaves exactly
R_T c_T = 0. By section 4, S is a possible terminal read set iff
K_S ⊆ ker(H|V) = K. Since dim K_S ≥ 22 = dim K, this means K_S = K. Hence:

1. K ⊆ ι_T(ker R_T) forces supp(K) ⊆ T. The verifier computes supp(K) =
   C - {77} (29 ports). For each of these ports it records a kernel-basis vector
   that is nonzero there and checks that deleting the column keeps rank 8.
   Column 77 is a coloop: deleting it drops rank R_C to 7.
2. |T| = 30 = 29 + 1 forces T = (C - {77}) ∪ {x} with x among the 67
   ports of J = U - (C - {77}).
3. K ⊆ ι_T(ker R_T) now holds, so equality ⇔ dim ker R_T = 22 ⇔
   rank R_T = 8 ⇔ r_x ∉ span R_{C-{77}} (rank 7) ⇔ w·r_x ≠ 0, where w spans
   the one-dimensional left kernel of R_{C-{77}}.

The verifier runs both tests for all 67 x and requires agreement: Bareiss rank
of the 8×30 R_T and w·r_x ≠ 0. The valid x are 77 and 44 ports of U - C, so
there are **45** sets S_x = J - {x}. The 22 ports with w·r_x = 0 have
rank R_T = 7. They are in every S_x (mandatory). The 29 ports of C - {77} are
in none. Sets of other sizes are not classified. Read sets of size < 66 are
impossible by the threshold. Normalising, the relation w R_U c = 0 is
c_77 + Σ α_p c_p = 0 with α_p = (w r_p)/(w r_77). The support of α is exactly
the 44-port swap set. All of this uses the 8-row matrix R only, with no
88-dimensional kernel basis.

## 3. rank(H|V) = 66 through owner-function independence

Let F be the 0/1 matrix F[d][b] = f_b(d) over owners d and the 47 distinct
first axes b. If some 47 owners D give an invertible F_D, then H(c)|_D = 0
implies L_b(c) = 0 for every b (apply F_D^{-1} ⊗ I_8). Hence
ker(H|V) ⊆ ker L. Conversely H factors through L on every owner, so
ker L ⊆ ker(H|V). Also ker L ⊆ V because R_U c = Σ_b L_b(c). Every group
except C has independent columns, so ker L = ker R_C ⊕ 0 = K with dim 22.
Therefore ker(H|V) = K and rank(H|V) = 88 - 22 = 66 on the whole owner array.

The certificate is a 47×47 0/1 minor with **determinant 2^62 =
4611686018427387904**. Its rows are the identity owner and registered owners
`m1 … m185`, all listed in `RESULT.json`. The rows were chosen by an exact
greedy pass over the registry in index order, and the determinant was recomputed
fraction-free. The predecessors instead use evaluation minors on the same 17
owners (identity and rho_1(p), p = 0..15): PR2354 a rank-74 certificate on
Q^96, PR2389 a 66×66 minor on V. Neither uses independence of the bit functions.

Observations (recorded in `RESULT.json`, not used for the claim):

* On the 768 **route owners alone** the f_b have rank only **44**, and 45 with
  the identity. Route owners therefore cannot certify full bit-function
  independence. The certificate needs other registered owners: 29 of its 46
  non-identity rows are not routes. That does not contradict the predecessors'
  route-owner minors. They only need F_D ⊗ I_8 to be injective on the
  74-dimensional image of L (PR2354) or on L(V) (PR2389), which is weaker
  than full bit-function independence.
* Under the transposed action convention, bit_0(d^T b) = parity(d e_0 ∧ b),
  the rank is still 47. The certificate does not depend on that convention
  choice.

## 4. Written audit of PR2389's adaptive argument

Statement audited: README "Transcript-fiber theorem", "Zero-error
randomization" and "All 45 optimal terminal sets" at head `aed06c8f`.
Verdict: **the argument is correct as written**, given the inputs below. This
is a written check, not a formal proof.

* (A1) Each port read returns h_p = c_p f_{b_p}, which is linear in c with a
  ≤1-dimensional answer space. Reads on c and c + v agree whenever v_p = 0.
  The fiber argument only needs this. The bound |S| ≥ rank(Q_S|V) needs the
  answer for each port to be one scalar's worth, which holds. The upper bound
  (a decoder reads c_p back from h_p) needs f_{b_p} ≠ 0 at some owner. That is
  implied by section 3, since every column of an invertible F_D is nonzero.
* (A2) The induction is over the reader's deterministic query and stop rule,
  which depend only on the transcript. At a leaf with read set S, every
  v ∈ K_S leaves the transcript unchanged. Exactness on c and c + v then gives
  H(v) = 0. This needs c + v in the domain where exactness is promised.
  PR2389 states this for all of V over Q. Remark (ours): integer points also
  suffice. If the reader is exact on every point of V ∩ Z^96, then
  K_S ∩ Z^96 spans K_S over Q, so H(K_S) = 0 still follows. As PR2389 notes,
  bounded coefficient boxes are *not* covered.
* (A3) Randomized case: the seed law is independent of the input, and for each
  c the event "terminates with H(c)" is measurable and has probability 1.
  Countably many c (Q, or the integer points) give a common full-measure seed
  set. The fiber theorem then applies per seed. Bounded-error readers are not
  covered.
* (A4) Classification at |S| = 66 uses ker(H|V) = K exactly. Section 3 gives
  this independently. Section 2 then gives the 45 sets.
* (A5) **Inherited, not checked here**: the equivalence "recovering the
  original selected A defect ⇔ recovering H(c)" (X_A = -P_{0,A} H(c)). Only the
  R_A R_A^T = 4I Gram identity is rechecked. Also inherited from
  PR2093/PR2326/PR2354 and not replayed: the ordered F0/B1 maps, the retained
  tail and the zero observations. So are B_s h = 0 beyond the existence of the
  768 registered routes, and the semantics that registered
  `owner_right_matrix_columns` are elements of G in the same representation as
  d in f_b(d).

## Negative controls (all rejected; reasons are in `RESULT.json`)

1. R entry (row 0, port 1) +1: port 1 becomes swappable, giving the wrong set
   count (46).
2. R entry (row 3, port 77) +1: the classification is unchanged and only the
   Gram identity detects it. It is kept to show what the classification alone
   does not see.
3. First axes of ports 77 and 6 swapped: the group census changes and the
   coloop moves.
4. Identity owner only (empty registry): owner-function independence fails.
5. Coloop claimed at 78. 6. Set count 46. 7. Unique optimal set. 8. 65-read
   threshold. 9. Mandatory port 109 dropped. 10. Omission 77 replaced by 76.

## Scope, inherited assumptions, unresolved obligations

* Finite exact replay on one fixed 96-port family. It does not formalize the
  adaptive theorem and is not a full QQ16, supplier or multiplication theorem.
  No κ change. The selected frontier is untouched.
* Inherited: the definitions of H, f_b and the observation contract from
  PR2389/PR2354, and the items in (A5).
* Unresolved: an independent check of the P_{0,A} equivalence and of the full
  ordered native schedule (PR2354/PR2389 do not replay it either). A Python
  3.12 run of the generic hook is also outstanding.

## Open next questions

Structured versions are in [TASK.json](TASK.json).

1. **Do the 29 nuisance ports C - {77} carry a second hidden family that
   defeats all 45 sets?** All optimal sets omit the same 29 ports. First step:
   search ker R_U for vectors supported on C - {77} plus a second axis group
   that survive the ordered F0/B1 maps. PR2384's second-axis witness is the
   template. Blocker: native ordered maps beyond this family.
2. **Which structured owner class certifies bit-function independence?** Route
   owners reach rank 44 only. Identify the non-route registered maps that
   supply the missing 3 directions, and explain the determinant 2^62. This is
   a small exact computation with no blocker.
3. **Bounded-error or bounded-box readers.** The fiber argument needs exactness
   on an unbounded lattice or space. First fix a coefficient box and an input
   law, and bound a reduced instance. Blocker: no agreed QQ16 input
   distribution.

## Credit

Audited and built on: **commdata2338**, PR2389 and PR2326/PR2384 (adaptive
theorem, classification, coordinate-access contract). **kyzer1023**, PR2354
(rank 74/66, fixed-set threshold). **Adam Gall**, PR2093 (common-axis
bit-function family). **Ali Romman**, PR1969 (QQ16 packet, routes, frame
conventions). **EdDiboi**, the parallel parity-subspace threshold claim in
#2205. **Cinna Davis**, PR2216/PR2268 (shear/tap question). Retain the QQ16
[NOTICE.md](../joint-query/NOTICE.md).

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic,
Claude Opus 5.5). Apache-2.0.
