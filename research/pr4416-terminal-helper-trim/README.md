# Terminal helper trimming: conditional κ = 0.00269635

The p7 native construction in [PR4416](https://github.com/CrocSwap/integer-mult-bounds/pull/4416)
pays for 22 rank-one helper transforms per local call after those helpers'
last interaction with another field. Removing those transforms changes their
productive ranks from 5 to 4 and strictly improves the mixed moment. With all 15
local calls changed, the complete conditional multiplication endpoint increases
from **κ=0.00268647 to κ=0.00269635**. The absolute gain is **0.00000988**,
approximately **0.368%** relative to PR4416. This is a modest structural gain;
it does not establish a large new multiplication improvement or a global optimum.

The new local word is replayed on all 632 arbitrary persistent inputs in both
orientations, and every changed helper receives a new exact Clifford normal
form including its absolute phase. The unchanged p7 controller is regenerated
and its actual main contacts, endpoint phases and whole idle jobs are replayed.
The new profile then passes charged tensor strictification and all 54 outer
predicates, all 3 functional predicates, and all 9 cost rows.

This is a **conditional research contribution awaiting independent review**.
The selected result is unchanged. Native all-column lift, allowed physical
operations, analytic decomposition, precision, storage, fixed-tape execution and
exact recovery remain the stated premises of PR4359 and its successors. A finite
certificate is not a formal verification of the complete multiplication theorem.

## 1. What changes in the actual native word

[NATIVE-TRIM.md](NATIVE-TRIM.md) gives the word transformation and phase proof.
The changed helpers remain distinct arbitrary original inputs. No initialized
center, copy or correlated replacement is credited as an independent input.

For each eligible helper, remove its final rank-one climb, retag later scalar
scalings at its rank-four frame, and replace its old whole-call helper adapters
with the freshly decoded rank-four adapters. There is no later cross-field
read or write. All other native instructions and every owned center lifetime
are retained. The source interpreter checks the full input-to-output operator;
the constructor does not infer correctness from an invoice alone.

The local target and paid inventories are derived from the changed literal
word and endpoint frames. In the paid inventory, each of the 8 source center
paths is charged as its exact whole rank-eight transform, as in PR4416.

| Local inventory | Before | After |
| --- | --- | --- |
| Helper targets | `{5:28,6:18,7:56,8:93,9:213}` | `{4:22,5:6,6:18,7:56,8:93,9:213}` |
| Paid jobs | `{1:2487,2:713,3:224,4:102,5:20,8:8}` | `{1:2465,2:713,3:224,4:102,5:20,8:8}` |

The p7 controller still has 15 local invocations, 1,568 main fields, 6,120 fresh
helper fields and 7,688 total productive fields in ambient rank 121. Its main
operator,8-dimensional fresh stage blocks, whole idles and constant Laurent
factor remain those of the pinned p7 construction. Replacing its 15 local
invoices gives exactly

```text
T = {4:330,5:90,6:270,7:840,8:1395,9:3195,
     25:448,41:448,57:448,121:224}
P = {1:36975,2:10695,3:3360,4:1530,5:300,
     8:1464,16:448,32:448,48:448}.
```

The rank-one masses fall from 131,723 and 131,115 to 131,393 and 130,785.
Their positive difference remains 608. For every exponent 0<t<1, the exact
improvement in target-minus-paid moment is

\[
330\bigl(1+4^t-5^t\bigr)>0.
\]

This follows from strict subadditivity of x^t. Losing the rank-five productive
credit is therefore fully charged: the saving in paid work is worth more than
the loss in productive moment. Keeping the old productive rank would be false
accounting, and a physical negative control rejects it.

At the exact tested saving **C=0.002696355**, t=1−C, outward rational intervals
give

```text
0.000230059751406022474982393905 < T_t−P_t
                                      < 0.000230059751406022474982393906.
```

The same exact arithmetic rejects the original invoice at C and rejects the
new invoice at 0.002696357. Thus the new continuous moment has a zero in the
stated sign-change interval; a floating-point screen puts that zero near
0.002696356026296. The conditional endpoint is supported by the exact lower
test and complete consumer below, not by that floating-point estimate.

## 2. Complete charged strictification

The raw paid ranks extend to 48 while the productive ranks extend down to 4.
The strict mixed compiler cannot be invoked directly from their raw moment.
We use PR4416's chronological product, paid completion and disjoint splitting,
together with [PR4433's higher-moment tail](../higher-moment-strictification/README.md).
The new constants are checked in [strictification.py](strictification.py).

For two native units U,V, run one U copy for each distinct productive role of V.
At each chronological paid position of U, use a V invocation on the distinct
current owners to supply the requested jobs. Finish V and restore every whole-job
matcher before resuming U. Allocate separate owned centers for every raw local
invocation. Arbitrary-input correctness allows correlated values in distinct
slots; it does not manufacture extra independent inputs. This finite acyclic
substitution multiplies both productive and paid moments at each iteration.

After v factors, ambient rank is m^v=121^v and the productive field count is
B^v=7688^v. On each actual productive owner with target rank K<L=b^v, pay for
the positive transform on L−K disjoint axes after the whole product has finished.
Use the permitted complete-job normalizers at both input and output. Targets
become max(K,L). Every added transform is paid and no new field receives credit.
Then split every paid job into disjoint pieces of rank at most J=c^v.
Keep the original whole-job normalizers around the entire replacement.

For t=1−C, choose u>=C. If an original paid rank R>J is split as R=qJ+r,
0<=r<J, then

\[
qJ^t+r^t\le 2R J^{-C}
           \le 2R^{t+u}J^{-u}.
\]

The last inequality uses t+u>=1. Overcounting unsplit original jobs by P_t^v
therefore bounds their full charge by P_t^v+2P_(t+u)^v/J^u. A completion
D=L−K<L has split charge at most 2L/J^C, also when D<J. There are at most B^v
completions, and completion only increases productive t-moment. The complete
normalized paid moment is consequently bounded by

\[
\alpha^v+2\gamma^v+2\delta^v,\qquad
\alpha=\frac{P_t}{T_t},\quad
\gamma=\frac{P_{t+u}}{c^uT_t},\quad
\delta=\frac{Bb}{c^CT_t}.
\]

For **v=180,c=10,b=15,u=3/10**, exact outward intervals give:

| Ratio | Certified interval, shortened | Rational upper bound |
| --- | --- | --- |
| α | `(0.999999998233169239687568538396,0.999999998233169239687568538397)` | `1−10^−9` |
| γ | `(0.904996283324825045276686108578,0.904996283324825045276686108579)` | `181/200` |
| δ | `(0.880161938698256950864260386893,0.880161938698256950864260386894)` | `881/1000` |

Bernoulli's inequality and an exact comparison of rational integers prove

\[
\frac1{1+180/10^9}
 +2(181/200)^{180}+2(881/1000)^{180}<1.
\]

The certified strict gap exceeds 0.000000148289558798340001944730. All final
paid ranks are at most 10^180, all final target ranks are at least 15^180, and
the ambient rank is 121^180. Product, completion and splitting preserve a
strict rank-one surplus 131393^180−130785^180. The actual integer inventories
are defined by finite products, per-owner completion and integer division.
They have not been materialized. The same rounded certificate rejects v=160;
no minimum tensor power is asserted. The older rank-one-tail estimate also
fails at v=180, which is why PR4433's stronger tail is used.

## 3. Explicit uniform rank and outer endpoint

We retain the finite integer source/exit compiler and use PR4433's logarithmic
majorant. Its hypotheses and proof are pinned, and the constants here are
recomputed for the changed native word. Write m=121^180 and t=1−C. Take
theta_bar=6/7 and logarithm power p=16. The exact inequalities are

```text
10^7 < 15^6,
2*(10^180)^7 <= (121^180)^6,
eta = t*m^(t−1) > 0.097265815379458638502878125384 > (6/7)^16,
m^C < 10.253382867446957567464386012415 < 2^16.
```

The source complement capacity then exceeds the exit charge for the majorant
L(n)<=n^t(1+log2(n))^16, where L is normalized rank-one leaf count. This is a
bound on the specified finite compiler, not a physical runtime estimate.

Let κ=0.00269635 and d=(C−κ)/7=1/1400000000. The desired complex uniform
saving is C−d. With **H=890400000000,N=2^H**, the exact integer comparison

```text
890400000001^16 < 2^636
```

proves L(N)<N^(1−(C−d)). The preceding multiple of 1400000000 fails the same
comparison. The enormous final uniform word is specified algorithmically,
not emitted or claimed practical.

[endpoint.py](endpoint.py) reuses the unchanged PR4405/PR4416 outer ledger
with exact parameters

```text
complex_uniform_saving = κ+6d = C−d,
b = κ+5d, a = κ+4d, q = κ+3d,
BIT_saving = 0.0027,
epsilon = 1−d, beta = 1−3d,
r0 = d/10, stop = d, layout = d.
```

All 54 strict predicates, 3 functional predicates and 9 cost rows pass. The
smallest cost-row margin above κ is exactly
4196225107/1960000000000000000. Closing epsilon, closing the uniform gap,
claiming the unfunded tested saving as κ, or reverting BIT to 0.0023 is rejected.
The unchanged ordinary BIT saving is checked against its source admission.

The full expanded program includes each new helper normalizer, every local
scalar, every whole-job route and each owned center. As in the source finite
closure prescription, choose operation, height, amplification, error and stock
constants from that entire finite expansion before choosing sufficient input
size. The new normalizers consist only of permitted finite monomial operations;
they add no recursive Fourier calls. The source all-size/precision argument is
retained with newly defined finite constants. No numerical full-program stock,
condition number or practical input threshold is supplied here.

## 4. Reproduce and inspect

Standard library, Python 3.12. From the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/pr4416-terminal-helper-trim --check-only
python3.12 -B scripts/research_package.py --package research/pr4416-terminal-helper-trim
```

The normal verifier is read-only. It authenticates every declared live source,
rebuilds the local trim and the unchanged p7 geometry, computes the complete new
invoice, verifies both tail and compiler inequalities, replays the outer ledger,
and compares all proof-relevant output with [RESULT.json](RESULT.json).
An independently written rational atanh/Taylor engine cross-checks the raw
moment and its alpha bound. Regeneration is explicit:

```sh
python3.12 -B research/pr4416-terminal-helper-trim/verify.py --write-result
```

[SOURCES.json](SOURCES.json) pins original repository files at the exact base
commit. [VERIFY.json](VERIFY.json) declares the complete live input closure.
No predecessor source is modified or copied merely for provenance.
Metadata validation authenticates bindings; it does not establish the mathematics.

## Open next questions

The proof in [FAMILY-LIMIT.md](FAMILY-LIMIT.md) extends the old finite pair-count
screen to every positive pair count in the declared balanced prefix/suffix
family. Concavity makes p7 its unique best pair count at the exact test points.
The original family fails at 0.00268649 and the trimmed family fails at
0.002696357. These are limits of the stated native invoices and controller
family. They do not bound integer multiplication or other native constructions.
The same failure persists under unions and chronological products of failing
blocks, paid target completion, whole-job matching and disjoint splitting.
This identifies why tuning tensor powers or adding more pairs cannot produce
a substantial next gain within that family.

The structured continuation is in [TASK.json](TASK.json). A larger gain requires
a new native invoice or controller. Current candidates include using the missing
orthogonal E8 frame to extend 112 ports to 120, or a controller for retained center
inputs. Their scalar matrix identities alone do not prove free physical routes:
the cross-field phase interfaces and the complete paid bill must be reconstructed.
The present PR makes no larger claim from those exploratory identities.

The ordinary BIT admission 0.0027 will become binding if the complex supplier
advances far beyond this endpoint. Whole-idle BIT composition is a plausible
source of headroom, but a raw moment alone does not close that caller's admission.

## Credit

Native supplier, original controller and Clifford/source interfaces: @zxv,
PR4359 and retained predecessors. p7 productive padding: @1337isnot1337,
PR4416. Higher-moment tail, outward interval engine and generalized logarithmic
majorant: @zxv, PR4433, building on PR4411. Integer mixed compiler: Jacob Alan
Sussman, Theorem 1G. All original source notices and attribution remain intact.
The terminal trim, its native replay, revised endpoint and this integration
were prepared for @1337isnot1337 with substantial OpenAI Codex assistance.
New work is Apache-2.0.
