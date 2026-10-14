# S6 — Gaussian E8: every decoder with exactly 15 totals costs exactly 60 (question G2 of §10 closed)

Context: `s5-extension-ring-floors/` (#620 §10). The Gaussian view of E8 has 60 Q(i)-lines in K^4. Its F2 decoder pattern has
minrank 15 (S1: c = 14 UNSAT). S5 proved that every decoder costs >= 40. Excluding the Gaussian view needs 43; beating real E8 needs <= 42.
S5 left question G2 open (`gauss_c15.py`, a monolithic CaDiCaL run stopped after 18 h without an answer). The question was:
can a 15-total decoder have a column-space vector `W x` (or `U x`) supported inside a 3-flat? A "no" means every 15-total
decoder costs exactly 15 * 4 = 60.

## Result
**G2 is UNSAT. Every Gaussian-E8 decoder with exactly 15 totals has Theorem-C cost exactly 60** (x_K = 1). The cheap
decoders that remain possible (cost 40..42) must have >= 16 totals.

## Proof
1. **[argued] Reduction to small minrank instances.** Let B = W U^T be valid (B_TT = 1, B_TS = 0 on K-non-orthogonal pairs), with W, U in F2^{60x15}.
   Suppose x != 0 and supp(W x) lies in a 3-flat H. Put O = the lines outside H.
   - Then W[O] x = 0, so rank W[O] <= 14.
   - So B[O,O] = W[O] U[O]^T has rank <= 14, and it obeys the decoder pattern induced on O.
   - So if minrank(pattern on O) >= 15 for every 3-flat H, no such x exists. The same holds for U by transposition.
   - Coverage: every proper flat lies in a 3-flat spanned by lines (extend by lines one at a time). W has full column rank, so W x != 0.
   - Once no such x exists, every total has span(R_j) = span(A_j) = K^4. The Hermitian form is definite, so beta_j = 4 and the sum is 60 (S5 Theorem-C argument).
2. **[checked] Symmetry.**
   - `orbits.py` builds the 60 complex reflections s_r s_{Jr}. Each is exact, preserves E8 and commutes with J, and each is checked to preserve the line set and the non-orthogonality relation.
   - Closing them gives a permutation group of order 11520 on the lines (G31 modulo scalars).
   - The 1500 3-flats form 3 orbits: 60 of size 15, 480 of size 6 and 960 of size 4.
   - minrank(pattern on O) is invariant under the group, so one H per orbit is enough.
3. **[checked] SAT.** `prove_c15.py orbits` runs on each orbit representative's complement O (45, 54 and 56 lines).
   - The encoding is S1's clique gauge: a 12-clique of O gets W = U = [I_12 0]. This is valid for any clique size <= c.
   - c = 14 is **UNSAT** with each of three independent solvers: CaDiCaL 1.5.3, Glucose 4 and MapleChrono (5-120 s each).
   - Calibrations: c = 15 is SAT on every O, and on all 60 lines c = 14 is UNSAT and c = 15 is SAT. So the encoding is not trivially infeasible.
4. **[in progress, group-free] All 1500 3-flats.** `prove_c15.py all` repeats the c = 14 test on every 3-flat complement, without using the group. Status: 700/1500 UNSAT so far and no SAT. The log is at s6/prove_all.log, and the advisor will append the final count.
5. **[script provided, not yet run] Sanity.** `price_c15.py` takes a SAT-found 15-total decoder and prices it, expecting every beta_j = 4 and a sum of 60. It was not run, to stay under the 3-process cap while the sweep runs.

What made it tractable: S5's encoding asked for a decoder together with a witness x and a selector over 1500 flats in a single instance, and it ran 18 h or more without an answer. The rank-drop reformulation turns this into 3 orbit instances, each a 45-56-line minrank test that is UNSAT in about 5 s.

## Side lemma (argued, from the same runs; possible input for the >= 43 question)
Take any decoder with c totals and any 3-flat H. At most c - 15 totals have R_j inside H, and the same holds for A_j.
- Proof: those columns vanish on O, so B[O,O] has rank <= c - #.
- More generally, for any family of 3-flats H_1..H_m: #{j : R_j inside some H_i} <= c - minrank(pattern on the complement of the union of the H_i).

## Reproduce
`PATH=$SP/venv/bin:$PATH sh verify.sh` takes about 3-5 min and uses 3 processes. `FULL=1` adds the 1500-flat sweep, which takes about 45 min. Compare the output with `expected.txt`.
Logs from the original runs are in `logs/` (`prove_orbits.log`; `prove_all.log` is still running in s6/).
