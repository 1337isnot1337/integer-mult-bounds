# All-length cost floor for the 128 PR4470 receiver windows

For each of the **128 adjacent receiver windows** extracted from the pinned
PR4470 constructor, the incumbent minimizes the paid rank cost among **all
finite shear words on the same three persistent fields**, with the same scalar
endpoint and monotone fixed entrance/exit frames. There is **no length or
rational-coefficient cap**. The conclusion holds for every price `r^p`,
`0 < p < 1`, hence every saving `0 < C < 1` with `p = 1-C`.

This is a computer-assisted, scoped cost-floor proof, not a new kappa,
physical supplier, global optimum, or selected-frontier change. The finite part
has **1,303 reachable states and 239 window/profile pairs**, checked with exact
integers. All seven constructor inputs are SHA256-pinned at canonical main
`f626db5c3a3d781d8f7695038776c621651f75e1`. Every boundary, incumbent and terminal
rank partition is in [RESULT.json](RESULT.json). The written reduction below
is essential: a finite calculation alone does not establish an all-length result.

## Delta and coordination

Clear1nsight's [#4546](https://github.com/CrocSwap/integer-mult-bounds/pull/4546)
at `55b8d34c82fc4df6499c5037e156db6e990b96fe` tested words through four unit
shears in twelve windows. Ryanson Jonathan's
[#4567](https://github.com/CrocSwap/integer-mult-bounds/pull/4567) at
`50fedd98cda709707e4291c542e20ead96bcc786` extends the census to all 128 windows,
length six and bounded nonunit alphabets; its README explicitly asks for a
length-independence proof. This package answers the **cost-floor** part with a
different relaxation: directed potential source dependence and frame dimensions.
It imports neither predecessor's search/checking code and does not assume their
finite results. It reuses Cinna Davis's credited #4470 constructor for native data.
Separate implementation does not mean independent human or formal review.

The `independent-moment` card is refined from its older named suppliers to this
live handoff. Closing an unbounded search direction in a fixed invoice model
identifies which premises must change before further construction searches.
[Discussion #4577](https://github.com/CrocSwap/integer-mult-bounds/discussions/4577)
is the canonical investigation thread.

**Concurrent work.** The submission refresh discovered
[#4573](https://github.com/CrocSwap/integer-mult-bounds/discussions/4573) and
[#4574](https://github.com/CrocSwap/integer-mult-bounds/discussions/4574), posted
after the initial overlap snapshot, investigating the same all-length question.
#4573 also proposes a dimension/temporal-contact relaxation; #4574 proposes
mandatory-contact bounds. This package is an **independent certificate
implementation and corroborating proof**, not a claim of priority or an
exclusive new question. Its specific evidence is the complete integer
capped-rank comparison for every concave price, with geometric and
premise-removal controls. Coordination updates were posted in both threads.

## Model and theorem

Label the persistent fields `a,b,x` by `0,1,2`. Their arbitrary initial scalar
values are independent formal variables. The required scalar endpoint is

```
a <- a + ca*x,   b <- b + cb*x,   x <- x,
```

where the source windows have `ca,cb` in `{+1,-1}`. A replacement is any finite
word `y_i <- y_i + c*y_j`, `i != j`, with rational coefficients and that exact
endpoint. Both operands of every gate have one common binary frame in `F2^9`.
Each field's frames grow by inclusion from fixed `S_i` to fixed `E_i`. Every
positive dimension increment, including the exit gap, is charged by its rank.
No extra/owned field, frame decrease, free transport or changed boundary is
allowed. Scalar-height charges are omitted in the replacement's favor; adding
nonnegative charges cannot defeat the lower bound. The common moment
normalization does not affect this local comparison.

**Theorem.** In each extracted window, every replacement in this model costs
at least the incumbent under `r^p` for every `0<p<1`. The incumbent has the
required endpoint and a legal monotone path, so the minimum equals its cost.
Windows are considered individually: no overlapping gains may be summed.

### 1. A finite relaxation contains every legal word

The state is `(d_0,d_1,d_2,M)`, with current dimensions and a three-bit mask.
Initially `d_i=dim S_i` and `M=100` (binary). At a gate with destination `i`
and source `j`, update

```
M' = M union {i if j is in M}.
```

Inductively, any field with a nonzero exact coefficient of initial `x` belongs
to `M`: a shear cannot create it unless it was present in its destination or
source. Cancellation can only make the mask overestimate dependence. The
required endpoint has nonzero `x` coefficients in both receivers, so valid
termination requires `M=111`. Ignoring the exact coefficients and the other
initial variables enlarges the candidate set. There is no coefficient bound.

The common frame `F` at a contact necessarily satisfies

```
S_i + S_j <= F <= E_i intersection E_j.
```

Exclude a pair if either start is outside the other exit. Otherwise enumerate
every integer common dimension

```
max(d_i, d_j, dim(S_i+S_j)) <= h <= dim(E_i intersection E_j).
```

Set both dimensions to `h`, update `M`, and append positive ranks `h-d_i` and
`h-d_j`. Actual intermediate subspaces and tighter chronological bounds are
forgotten. Every legal common frame maps to such a transition; the converse
is not asserted.

At any state with `M=111`, termination appends every positive rank
`dim E_i-d_i`. If an implementation splits a climb, aggregate increments
between consecutive contacts on that field, or between its last contact and
exit. For concave `f` with `f(0)=0`, concavity gives
`f(u+v) <= f(u)+f(v)`. Thus aggregation can only reduce cost. Every actual
word maps to a relaxed path with cost no greater than its actual bill.

### 2. The enumeration has no hidden length cutoff

Every dimension and dependency bit is nondecreasing. An edge that leaves the
state unchanged adds no positive rank. Removing it preserves all future
transitions and terminal options **in this relaxation**; this is not a claim
that its shear can be deleted from the actual scalar word.

Every other edge strictly increases
`Phi=d_0+d_1+d_2+popcount(M)`. The reduced graph is therefore a DAG, with at
most `sum_i(dim E_i-dim S_i)+2 <= 29` nontrivial edges on a path and at most
`4*product_i(dim E_i-dim S_i+1)` states. The `x` bit always stays set.

`relaxed_profiles` explores every allowed edge and unions its appended ranks
with every suffix partition, also including every permitted terminal option.
Induction on remaining `Phi` proves it enumerates all relaxed terminal
partitions. Removed self-loops add no ranks. Every terminal partition has
telescoping mass `sum_i(dim E_i-dim S_i)`, which the code checks explicitly.

### 3. Integer dominance proves every concave-price comparison

For a partition `v`, set `B_k(v)=sum_{r in v} min(r,k)` for `k=1,...,9`.
For every terminal `v` and incumbent `u`, the replay checks

```
sum(u) = sum(v),     B_k(u) <= B_k(v) for k=1,...,9.
```

These inequalities are a discrete majorization certificate. For completeness,
put `delta_k=f(k)-f(k-1)`. Concavity makes these deltas nonincreasing. For
integer `0<=r<=9`, telescoping yields

```
f(r) = delta_9*r
       + sum_{k=1}^8 (delta_k-delta_{k+1})*min(r,k).
```

The mass term cancels; every remaining coefficient is nonnegative. Hence
`sum f(u)<=sum f(v)` for every concave `f` on these ranks with `f(0)=0`, in
particular `r^p`, `0<p<1`. No floating point, logarithm, root enclosure or
rounding is used. Combining the three steps proves the theorem.

## Source binding and evidence

The pinned `native_joint.construct()` runs in an isolated child Python with a
fresh private bytecode cache. No unmerged Git object or predecessor verifier
is needed. The new extractor scans the forward program with climb events
omitted, retaining each persistent field's last frame. It selects consecutive
ADDs in `B` or `cleanup_tail` with a common source, distinct receivers and unit
coefficients. Each exit is its field's next scalar/warp entrance or final frame.
The two original contacts and every exit gap determine the incumbent; their
inclusions are checked exactly.

| Evidence | Result |
|---|---:|
| Eligible windows | 128: 123 B, 5 cleanup_tail |
| Reachable states, summed over windows | 1,303 |
| Terminal window/profile pairs | 239 |
| Incumbent admitted and dominating every profile | All 128 windows |
| Profile-count distribution | 93x1, 9x2, 6x3, 2x4, 13x5, 4x7, 1x9 |
| Exact unit-shear endpoint words through length 4 in a control fixture | 84 |
| Legal `F2^2` common-frame paths for those words inside the relaxation | 2,868 |

The small geometric fixture tests the abstraction on concrete paths; it does
not prove its universal soundness. Three weakened-model controls expose strict
false savings for every `0<p<1`:

| Removed premise | Window | Incumbent | Falsely admitted |
|---|---:|---|---|
| Directed source-dependence requirement | 10557 | `(1,1,1)` | `(2,1)` |
| Exit-intersection dimension cap | 11078 | `(1,1,1,1)` | `(2,2)` |
| Terminal exit charges | 10554 | `(2)` | empty |

The normal model excludes each false gain. Dimension mass or uncharged cleanup
alone therefore cannot establish the floor.

## Reproduce

Python 3.12, standard library only, from the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/receiver-window-all-length-floor
python3.12 -I -O -B research/receiver-window-all-length-floor/verify.py
```

Both recompute and compare the complete `RESULT.json` receipt, without
rewriting it. `--write` explicitly authors the receipt. Windows/CPython 3.12.0
takes about three seconds. All acceptance checks remain active under `-O`.
The PR records publication and export checks. Full supplier/native/physical
and selected-frontier replays are outside scope. The historical baseline was
attempted in the sparse checkout but stopped at a missing selected-package
file; no baseline success is claimed.

## Overlap and limitations

Initial overlap covered 355 open PRs and 3,470 Discussion records with complete
remote pagination around 2026-10-22 07:48–07:50 UTC. Local search was sparse,
7/5,860 note paths; relevant main inputs and live #4546/#4567 material were read
directly. This is not a novelty guarantee. The selected result remains
`23/10000`. The central ledger labels #4470 partially reviewed; this result
does not upgrade its admission status.

At the submission refresh main remained `f626db5c3a3d781d8f7695038776c621651f75e1`.
#4567 had advanced to `5ac594d1bc1e6d91f20ef8157f38bb9b29768bfd`, adding 88
nonadjacent pairs and a whole-word single-contact retiming check. Those newer
scopes are outside this package; none of its runtime inputs come from #4567.

The theorem covers pinned **forward adjacent windows with fixed boundaries**.
It does not assert equality of #4546's whole relaxed-profile set at every
length, exact scalar realizability of every state path, or geometric
attainability of every partition. These stronger statements are unnecessary
for the lower bound. Extra/owned fields, nonmonotone frames, new operations,
nonadjacent or jointly overlapping windows and changed producer/consumer
contracts are outside scope. Native correctness, physical lowering, precision,
stock, hosting, reverse admission and all-size multiplication remain separate.

## Open next questions

1. **Change a boundary premise before searching again.** Extra fields or
   nonmonotone transports could escape the DAG. First name one actual window
   and specify all entrance, exit and restoration costs of the changed model,
   then derive its optimistic graph. The missing complete cost contract is
   the blocker; unknown costs cannot be zero.
2. **Independently review the all-length reduction.** Check the dependency
   induction, state-edge deletion and concave aggregation against the exact
   caller, then replay the integer certificate. Finite tests alone cannot
   establish that reduction. No independent human or formal review is claimed.
   No further length/coefficient census is justified inside the proved model.

## Credit and license

Credit Chris R / Clear1nsight (#4546's model and finite ceilings), Ryanson
Jonathan (#4567's census and explicit all-length question), Cinna Davis
(#4470's constructor), zxv (productive-helper and receiver-sharing work),
Jacob Alan Sussman, and the native/Clifford/geometry/outer contributors credited
in the source packages. Prepared for mihir-s-05 with substantial OpenAI Codex
assistance. Apache-2.0. Predecessor packages and frozen evidence are unchanged.
The concurrent mihir-s-05/Codex investigations #4573 and #4574 are acknowledged
above; no independent human review is implied by their separate sessions.
