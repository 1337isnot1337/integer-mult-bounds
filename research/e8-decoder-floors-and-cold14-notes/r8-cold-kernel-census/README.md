# Helper-donor cold kernels: exhaustive census on the four-kernel words (negative result, no new κ)

Scope: the two local provider words of PR1297 (pivots 531/543/555/567 already applied), which are byte-identical
to the words used by PR1319's T74 exact-fill construction (current valid κ head 0.001676855229071321; #1377/#1424
only refine the outer grid). PR1305/PR1324 were withdrawn by their author (idle-overlay invalid), so their idle
reassignment step is not used here.

## What a helper-donor cold kernel is

A *cold pivot* q is a register whose value is still its start value (start frame `start_extra[q]`, here usually a
rank-one frame such as `[24]` or `[30]`) when it is read by some early B gates `t += k*q` ("early uses", before
q's first B write). A kernel deletes a set D of those early uses and restores the scalar program with *shocks*:

* **cut** `h += a*q` inserted in B (PR1274/PR1297: right after an early output read of helper h), undone by
  `h -= a*q` at the end of early cleanup;
* **hook** `s += c*q` / `s -= c*q` around an early gate `t += k*s` (the donor s is already at q's frame).

Exactness is the rational equation `d = Σ coeff_i · response_i`, where `d` is the change of q's final column
caused by deleting D and each response is the backward column of the shocked register. Admissibility is then:
scalar map unchanged (mod p check of B + early tails + prepends), the cone caps (`audit_local` inverse-row and
dirt-column cones as end-of-B caps), and a feasible frame annotation; the profile is the exact optimum of the
#1186 frame solver (integer duality certificate). Widths, ports, centres and entrances are unchanged, so any
admitted kernel would reuse the owners/dispatch unchanged.

Why the four kernels pay: per-register climb diff of pivot 555 on the PR1286 word
(`tools/climbs.py`): `(187,1)-2, (187,2)+1, (483,1)-1, (483,2)-1, (483,3)+1`. Deleting the rank-one early reads
of q into 187/483 merges two consecutive climbs of those targets into one larger climb; the new gates land on
registers (donor 620, helper 383) that are already at the needed frame. Paid profile H1 −3, H3 +1, cost −11676.

## Census (all exact)

| Family | Generator | (pivot, D) jobs | candidates | priced: ok / infeasible / inexact | gains |
|---|---|---|---|---|---|
| PR1297 family, D = all early uses | `relations.py full` | 376 | 254 (48 pivots) | 99 (all Δ=0) / 80 / 75 | 0 |
| G: cut after any read of any h (or B start), hook around any early add, 1- or 2-shock cut+hook, all subsets D | `relations2.py subsets` | 1952 | 9916 (248 pivots) | 1435 (1311 Δ=0, 124 Δ=+4913) / 7287 / 1194 | 0 |
| K2: any two shocks (cut+cut, hook+hook), all subsets D, beyond G | `relations3.py 2 subsets` | 1952 | 15507 | 13402 priced: 4346 (4169 Δ=0, 177 Δ=+4913) / 8808 / 248; 2105 unpriced (time budget; 38 pivots, 1547 hook+hook, 557 cut+cut, 1 hook+cut) | 0 |
| 3-shock spot check (pivots 554, 448) | `relations3.py 3 full` | 2 | 12 | 0 / 12 / 0 | 0 |

Controls: on the PR1286 input word, `relations.py` restricted to 531/543/555/567 recovers exactly PR1297's
5 + 5 relations, all priced −11676 (= its SEARCH-RESULT.json); `relations2.py` contains all ten and finds two more
(same pivots). So the generators and the pricer reproduce the published kernels.

Per pivot (family G): 376 registers have early uses; 128 admit no exact dyadic relation at all; of the 248 with
relations, the best outcome is Δ=0 for 171, Δ=+4913 for 6, infeasible for 67, inexact for 4.
Main infeasibility reason: `L not inside U at mutable vertex` (3566 at the early-cleanup restore of a cut, the
rest at end-of-B cone caps) — the restore `h -= a*q` or the hook pair forces a register below its cone.

Cold-pivot inventory on the final base word: 192 registers have start frames; 152 have early uses
(rank-one start: 24 with 1 use, 12 with 2, 5 with 3, 53 with 4, 2 with 5; rank 4: 44 with 3; rank 5: 12 with 3).
The (out, out, helper) three-use pattern of the four kernels occurs only at 531/543/555/567, which are spent.

## Conclusion

On the current four-kernel words there is **no further admissible helper-donor cold kernel with negative cost**
in families PR1297 ⊂ G (fully priced) and in the 13402 priced members of K2 (all subsets of early uses, any single or paired cut/hook shocks). PR1297's
four kernels are the only positive ones in this neighbourhood. Not covered: three or more shocks in general
(cost ~4 CPU-min per pivot; only spot-checked), cuts at gaps not adjacent to a read, and gate reordering.
Only the base provider word was priced exhaustively. The extra word has the identical scalar program (same 1844 B gates; it differs only in frames, report and one start_extra entrance group), so the census produces the identical 9916 / 23139 candidate sets; its pricing was started and paused for CPU and is not claimed. 2105 K2 candidates on base remain unpriced (resume: `TMO=30 price_all.py words/base.json.gz cands/K2-base-new.json cands/K2-base-new-price.json`, it skips priced keys).

## Reproduce

```sh
export IMB_ROOT=<checkout with research/gauge44-frames-x and complex-k492-owner-repair>   # #1186 toolkit roots
python build_word.py --base vendor/pr1297/inputs/base.json.gz --recipe vendor/pr1297/RECIPE-base.json.gz --out words/base.json.gz
python -B scripts/relations2.py words/base.json.gz cands/G-base-sub.json subsets
python -B scripts/price_all.py  words/base.json.gz cands/G-base-sub.json cands/G-base-sub-price.json 10
python -B scripts/relations3.py words/base.json.gz cands/K2-base-sub.json 2 subsets
```
`price_all.py` imports the #1186 exact frame toolkit (`harness.Pricer`).
