# The subsequent block-four claims do not close the paid schedule

This addendum reviews PR4818 at fd29d065bbe12f5be5af02fdf5a8b4d86dda3381
and PR4819 at a7b42c2f8ffe5a18d305ca4dda5729d2f1d72ea8. Both are by hexapode.
It is an independent source audit plus an exact conditioning counterexample,
not a proof that their advertised call counts are impossible.

## Source pins and missing execution

- https://github.com/hexapode/integer-mult-bounds/blob/fd29d065bbe12f5be5af02fdf5a8b4d86dda3381/research/complex-block4-three-in-ten/verify_schedule.py
  Git blob: 8f9a2ef3cdba4c83be7a4d931c1070fef73ba896.
- https://github.com/hexapode/integer-mult-bounds/blob/a7b42c2f8ffe5a18d305ca4dda5729d2f1d72ea8/research/complex-block4-thirteen-in-fortyone/verify_schedule.py
  Git blob: e22dd9afd88837705cba14195f6c9acb4a97c6e7.

PR4818 sets three couplers to one-half XOR permutations (lines 131-133),
computes the target vectors, then constructs the observations directly from
those targets and E*x (lines 369-383). PR4819 similarly chooses thirteen
half-XOR couplers at line 158, defines E=K*G at line 167, computes Y_true=K*X
at line 369, and constructs V_obs using those target vectors at lines 377-379.

These are consistency checks of an explicitly assembled linear system and its
solver, not execution of ten or forty-one native paid calls. In particular,
solving 3*n3+4*n4=41 and n3+n4=13 (PR4819 lines 295-303) gives a numerical
partition, not the eleven missing three-call target-bearing ports. The source
must still implement the observations with the claimed grammar and bill.
Using a target oracle to construct test observations is not an error by itself;
it is insufficient when it replaces the entire paid construction being claimed.

Consequently the quoted 0.1315 and 0.1714 exponent values are not established
by these checks. A kept-subspace lower bound is not an attaining construction.

## Exact counterexample to the claimed whole-cycle conditioning bound

For the actual selected couplers, write G_k=(1/2)P_k, with P_k an XOR
permutation of sixteen coordinates. Their normalized cycle is

    (M y)_k = y_k + G_k y_(k+1 mod w).

Every P_k fixes the all-ones vector u. Thus the subspace y_k=c_k*u is invariant.
On all-positive coefficients c_k=1, the squared norm quotient is 9/4.
For odd w and alternating coefficients c_k=(-1)^k, the first w-1 output
coefficients have magnitude 1/2, while the wraparound output is 3/2. Its
squared norm quotient is (w+8)/(4w).

The largest singular value squared is at least the first quotient and the
smallest is at most the second. Therefore

    cond_2(M)^2 >= 9w/(w+8).

For the actual w=3 masks [1,2,4], this is 27/11, strictly larger than the
claimed (9/7)^2. For w=13 masks [1,...,13], this is 39/7, strictly larger than
the claimed (8193/8191)^2. The checker verifies both strict comparisons over
rational numbers using the literal XOR masks, with no floating-point tolerance.

The small loop gain does bound the condition number of the final Schur block
I +/- product(G_k). It does NOT give that same condition number for the whole
coupled matrix. This is the mistaken implication under review. Indeed,
M=I+(1/2)U for a block permutation U, so cond_2(M)<=3 remains a valid bound.
The counterexample rejects the advertised near-identity bound, not bounded
conditioning itself. It does not solve or obstruct the paid-decoder problem.

## Reproduction and next step

Run `python3 -I -B research/pr4813-decoder-audit/verify_cycle_control.py` and
repeat with `-O`. Both certificates are included in CYCLE-CHECKS.json.
No source scripts from the reviewed PRs are executed. Native ports, paid
schedules, all-width transfer, recursive costs and precision admission remain
unverified. The next useful deliverable is an actual emitted paid word, not a
larger invertible observation system.

Prepared for Cinna Davis with substantial OpenAI assistance. Credit the
reviewed authors and their cited predecessors; no independent human review
or claim of global novelty. Apache-2.0 under the repository license.

## Same missing implication in the subsequent block-five claim

PR4826 at d7b53d3992e658f0dd49d0207ba33bbc39272bac advertises 0.3174.
Its source is
https://github.com/hexapode/integer-mult-bounds/blob/d7b53d3992e658f0dd49d0207ba33bbc39272bac/research/complex-block5-three-in-nine/verify_schedule.py
(Git blob ea1511ae49f4e9b9d58033d7d69056227bf4b53f).
Lines 171-173 choose the same half-XOR masks [1,2,4], now in dimension 32.
Lines 262-270 compute K*x and use it directly to construct the primary
observations. Line 287 again applies K to recovered inputs. There is still no
execution of nine paid calls that produces those observations. The corresponding
whole-cycle condition claim is again 9/7 (line 224), and the same invariant
all-ones subspace gives cond_2(M)^2 >= 27/11. The checker now includes that
32-coordinate instance. Increasing the finite matrix dimension does not repair
the missing paid construction or all-width cost proof.
