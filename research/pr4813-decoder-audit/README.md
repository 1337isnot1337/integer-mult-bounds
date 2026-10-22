# PR4813: invertible observations are not a paid target decoder

## Result and scope

This is a scoped proof and independent exact rank control for PR4813 at
`9e33ecf009d36118f49ac86e9a0ee36e38dca44f`. It identifies a missing implication
in the advertised five-input/fourteen-call construction. It does not prove
that such a construction is impossible and does not change kappa.

Source: https://github.com/hexapode/integer-mult-bounds/blob/9e33ecf009d36118f49ac86e9a0ee36e38dca44f/research/complex-block3-five-in-fourteen/verify_schedule.py

### 1. The rank certificate survives deleting every coupled observation

Lines 371-378 append five independent blocks `t_k = A x_k`, with `A=C0`.
Here `C0=((1+i)I+(1-i)X0)/2`. On the two eigenspaces of the involution X0,
its eigenvalues are 1 and i. Consequently A is invertible (indeed unitary).
The bottom 40 rows of the claimed 80-by-40 observation matrix are therefore
`diag(A,A,A,A,A)`, an invertible matrix.

Thus the matrix has rank 40 regardless of its upper 40 rows. In particular,
replace every v1,...,v4,w5 observation row by zero: the same full-rank claim
still holds. This proves input recoverability, not the stated paid cost of
five target outputs. Our independent checker reproduces this exact control.
Removing the fifth retained A block instead lowers the rank to 32.

### 2. The recovery check applies the target after recovering the inputs

The source solves the observation system by Gaussian elimination, groups the
recovered input coordinates at line 447, and then explicitly computes
`recovered_targets = [mv(K, recovered_x[k]) for k in range(5)]` at line 450.
The expected answer uses the same target operator at line 411.

An expected-value oracle may of course use K. The missing element here is a
separate admitted decoder whose *actual outputs* are compared with that
oracle. The code provides no operation-level cost accounting for the
elimination or for the final K application. At one eight-coordinate example,
dense matrix multiplication cannot establish a cost-preserving algorithm at
all positive tensor widths. Rank and conditioning alone do not fill this gap.

### 3. The modeled observations are not a chronological five-bank replay

Lines 413-433 directly form K*x_k + E*x_(k+1), F*x5, and A*x_k from the original
input vectors. They do not execute fourteen primitive calls against a mutable
five-bank state. The stated ports overlap inputs. A valid construction must
show how each required original input or transformed view remains available,
with all temporary storage and restoration accounted for.

The cancellation used to motivate v_k is also stated under a swap-eigenspace
promise. Testing three choices of sector signs is not a proof that arbitrary
inputs enter these sectors, or that both sector executions can be composed
within the same fourteen-call bill. We do not claim a sector counterexample;
we identify the absent all-input admission argument.

## Reproduction and boundaries

Run `python3 -I -B research/pr4813-decoder-audit/verify.py` and repeat with `-O`.
The checker uses exact Gaussian rational arithmetic and explicit exceptions.
It independently reconstructs C0, checks A* A=I, and performs the rank controls.
It does not import or execute the reviewed PR's verifier. No native schedule,
all-width decoder, full supplier, precision proof or selected cold replay is
claimed. The source review and mathematical proof are distinct from the finite
rank corroboration. The main checkout is pinned at 624de9dc66858af0945e5f8a0942488d62280d43.

## Open next questions

- Emit the literal fourteen-call mutable-state word and its workspace contract.
- Supply a decoder in the admitted free/paid grammar, retaining the exact target
  application and all-width costs instead of only an unrestricted inverse.
- Remove the sector promise or price the required sector handling.

The first check should compare the emitted word's actual outputs with diag(K)
on independent input columns. A numerical left inverse is not this deliverable.

## Credit and review coverage

PR4813 is by hexapode, drawing on Dugongue's PR4743 native ports, Yiyang's PR4710
prefix/deficit analysis and Jacob Alan Sussman's PR4628 bound. None of those
predecessor results is independently rejected here. Prepared for Cinna Davis
with substantial OpenAI assistance; no independent human review is claimed.
PR4813's discussion had no returned comments at the inspection checkpoint.
No public comment was posted and no broader novelty search is claimed.
Apache-2.0, under the repository's license.

The source-pinned follow-up in BLOCK4-ADDENDUM.md addresses PR4818/4819,
including independent exact counterexamples to their whole-cycle condition bounds.
