# Why the R8 census missed the pivot-566 / signed-554 kernels, and an extended census on the current T74 supplier (no new κ)

Words: the current supplier words carried by PR1800 / PR1839 (`new/{gauge44,extra}-word-566.json.gz`, git blobs
76c01583… / e86142b3…, byte-identical to PR1672 and to PR1957's inputs). Exact frame pricing (PR1186 toolkit)
reproduces their local paid profiles: gauge44 {1:2348,2:500,3:416,4:130,5:82}, extra {1:2340,2:508,3:420,4:126,5:82}.
PR1672's EDITS-1 (pivot-554 kernel) on the step-0 word prices at Δ = −1850 (ok), same as published.

## 1. The missed mechanism

R8's families (PR1297 ⊂ G ⊂ K2) were built from two shock types, both paired:
* cut `h += a·q` right after a read of h, undone by `h −= a·q` at the **end** of early cleanup;
* hook `s ± c·q` around **one** existing gate;
with at most two shocks per relation.

The pivot-566 (PR1625) and pivot-554 (PR1672/PR1718) kernels are 5–7-term relations that lie outside this:
* **unpaired direct reads** `x += c·q` anywhere q still holds its start value; never undone (response `col_p[x]`,
  neither the cut form `col − e` nor the hook form);
* **windows closed in early cleanup right after q's own restoration** (q holds ±q0 again there: the "signed restore"
  of PR1718 is a read at a position where q's holder coefficient is −1), not at the end of cleanup;
* donor windows spanning many gates.

The common description: every term is a read `x += λ·y` at a position where some register y holds a multiple of the
deleted read's source value (a "holder window", in B or in early-cleanup tails), and the relation is the full linear
span of these responses. This is PR1957's `gencomp2` family. Positive controls (this run):
* PR1297/#1319 gauge44 word, delete B755 (`494 −= 566`): gencomp2 and our `gencomp3` find the 5-term kernel
  `98+=q@1963(tail), 98−=q@866, 210−=q@514, 150+=q@484, 146+=q@480`, Δ = −1850 ok;
* step-0 word, delete B342 (`482 −= 554`): 5-term kernel with signed tail `74 −= q`, Δ = −1850 ok.
So R8's families were too narrow (paired shocks, ≤2 terms, restore only at the end, only `+q0` value).

## 2. Extended census on the current supplier word (gauge44)

PR1957 (open) already ran gencomp2 on these words for 101 single-read deletions (budget −Δdel−1), and single-gate
commuting moves at 4461 positions: 0 gains. The extensions here:

| Ext | Family | Jobs | Result |
|---|---|---|---|
| E1 | same-value **multi-deletion** subsets (pairs–quads within 172 value groups of gain-carrying reads), gencomp2, ≤8 terms | 128 / 330 run (stopped for CPU cap) | 0 solutions (74 shape-infeasible, rest CP-infeasible) |
| E2 | relaxed oracle budget (+4913; the frame-cost oracle is not additive) on 24 small-gain reads: 16 one-split (−4913), 783/802 (−6763), 822/840/858/876 (−6100; 858/876 not in PR1957), 857/875 (−3050) | 24 / 24 | 0 gains: only the trivial "read moved one slot" (Δ 0), else infeasible / shape-infeasible |
| E3 | commuting-window retiming of **every** B add to its earliest/latest slot | 3074 / 3074 priced exactly | 2068 ok (all Δ 0), 1006 infeasible, 0 gains |
| E4 | NEW **two-value holder** family (`gencomp3.py`): reads of registers holding v + u, with u cancelled by other holders of u (incl. pure-u registers); matrix-valued exactness on (input, output) entries + B-only target rows; chain exclusion; holder values taken in the deleted program | 144 / 1002 single deletions: all 24 small-gain reads (−3050…−9826 band complete: 54 of the −9567/−9826 reads) + 90 largest-gain reads (−22039…−26389) | 126 shape-infeasible, 18 CP-infeasible, 0 gains |

E4 control: on the #1319 word it recovers the 566 kernel and new exact two-value variants (e.g. `210 += ½·676 @293`,
`210 −= ½·676 @237` replacing `210 −= q`), all Δ = −1850. So the family is strictly larger and still prices
correctly. On the current word: 144 single deletions done (smallest-gain first, and largest-gain first in parallel):
all 24 small-gain reads (−3050…−6763) are shape-infeasible or CP-infeasible within budget −Δdel−1 even with
two-value holders (e.g. 783/802: 1857 candidates, 4 two-value classes, INFEASIBLE; one-split reads 1/3: ~2400
candidates, 8–11 classes, INFEASIBLE). All large-gain delivery reads finished so far are shape-infeasible:
some effect row has no candidate under the budget.

## 3. Conclusion

The R8 negative was an artifact of a too-narrow relation family, not of the words. With the right family
(holder-window spans, PR1957) and two further generalizations (multi-deletion, two-value holders), plus relaxed
oracle budgets and full retiming, the current pivot-566+554 T74 supplier word has **no admissible negative-cost
kernel in the covered sets**. Not covered: the remaining E1/E4 jobs (CPU budget), three-or-more-value holders,
cross-value multi-deletions, A-section edits (see PR1957 §5), and the extra word (it has the same scalar program,
so it yields the same candidate sets, but frames differ).

## Reproduce
```sh
export IMB_ROOT=<checkout with the PR1186 roots>  OPENBLAS_NUM_THREADS=1
python scripts/ext3.py words/gauge44.json.gz E4-jobs.json out/E4 10 4 40 0 3      # two-value census
python scripts/ext.py  words/gauge44.json.gz E1-jobs.json out/E1 8 4 30 0 3       # multi-deletion (gencomp2)
python scripts/ext.py  words/gauge44.json.gz E2-jobs.json out/E2 10 6 40 4913 2   # relaxed budget
python scripts/retime.py words/gauge44.json.gz retime.json && python scripts/price_all.py words/gauge44.json.gz retime.json out.json 6
```
`gencomp3.py` imports PR1957's `fc3.solve`, `costorc.CostOracle` and the vendored PR1186 toolkit.
