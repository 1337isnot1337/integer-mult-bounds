# The fixed L/2 firing set at n = 5 beyond length 16

**Claim type: a scoped proof for L ≥ 26, plus an independent census through
L = 22. No new κ.** It answers most of #4322's open question 1. The selected
conditional κ stays `0.001672660197076918`.

## Object

[PR #4322](https://github.com/CrocSwap/integer-mult-bounds/pull/4322)
(unpaidmoon) shows that the fixed `L/2` substitution's firing set is not
monotone in length at `n = 4`: it is empty at `L = 14, 16` by a flat-excess
cap. At `n = 5` it found the firing set still monotone through `L = 16`.

Its open question 1 asks: **for n = 5, which even length first makes every
functional sound?**

The model is #4322's:

- canonical first-occurrence words;
- simple restored prefix walks on `F_2^n`, universal when the difference set
  of the prefix states is all of `F_2^n`;
- a nonzero mask fires when `base < excess ≤ base + d²`, with
  `base = (L/2)(L/2−1) − (2^(n−1) − 1)`.

## Results

**1. Soundness from L = 26 (proof).** At `n = 5` a level set is an affine
4-flat. By enumerating all `2^16` subsets of `F_2^4`, the maximum excess of a
`k`-subset is:

| k | 0–3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| max excess | 0 | 3 | 3 | 8 | 14 | 21 | 21 | 30 | 40 | 51 | 63 | 76 | 90 | 105 |

A split `(s, t)` therefore has excess at most `e(s) + e(t)`. This cap is at
most `base(5, L)` for every split exactly from `L = 26`. So every functional
is sound on **every** 26-, 28-, 30- or 32-point subset, not only on walks. At
`L = 24` the cap leaves only the `(8, 16)` split. A firing word there must
contain an entire level set of its mask.

**2. Census through L = 22.**

| L | closed | universal | false prunes | firing masks |
|---:|---:|---:|---:|---|
| 12 | 3,695 | 828 | 2,856 | 24 |
| 14 | 33,922 | 24,787 | 56,686 | 25 (all of weight ≤ 3) |
| 16 | 267,890 | 263,140 | 447,912 | 25 |
| 18 | 1,737,048 | 1,737,048 | 1,812,996 | **28**: adds `27, 29, 30` (weight 4) |
| 20 | 9,019,738 | 9,019,738 | 5,357,220 | **30**: adds `15, 23` |
| 22 | 35,938,056 | 35,938,056 | 11,569,998 | **30**: every mask but `31` |

- **No n = 4-style collapse.** The `n = 5` firing set stays nested through
  `L = 22`, and the all-ones mask `31` never fires.
- **Answer.** The first length at which every functional is sound is
  **24 or 26**. Only the `L = 24` census, restricted to the `(8, 16)` split,
  remains.

**Agreement with the predecessors.** The census reproduces the published
per-mask rows exactly: #3699's `(4,8)`, `(4,10)` and `(5,12)`, #3733's
`(4,12)` and `(5,14)`, both on main, and #4322's new `(5,16)` row. It also
confirms #4322's `n = 4` silence at `L = 14, 16`.

## Method and independence

Nothing is imported from #4322.

- **`verify.py`**, standard library, rebuilds the 16-point flat caps, and
  reruns the census itself for every `n = 4` case and for `n = 5` at
  `L = 12, 14, 16`. That includes #4322's full `(5,16)` row, in about 50
  seconds.
- **`census.c`** is a separate C enumerator for the lengths Python cannot
  reach. Its recorded runs in `evidence/CENSUS-RUNS.txt` are bound to the
  source by SHA256. They match every published row and the Python census at
  `(5,16)`, and give the new lengths 18, 20 and 22.
- **The C runs are local evidence.** CI reads them and does not recompile.
  `(5,22)` took about 17 minutes.
- **Vendored file.** #4322's `verify.py` is vendored byte-identically only
  for its literal `EXPECTED_5_16` row, which is read with `ast.literal_eval`
  and never run.

## Not covered

- `L = 24`. A plain census would take about two hours here. The cap reduces
  it to walks containing a full level set.
- `(7, 18)` and `(7, 20)`, and `n ≥ 6`.
- Any change to a retained seven-label exclusion.

## Reproduce

```sh
python3.12 -B research/f7-firing-n5-length-census/verify.py
cc -O2 -o census research/f7-firing-n5-length-census/census.c && ./census 5 22
```

The first prints `PASS_F7_FIRING_N5_LENGTH_CENSUS` in about a minute.

## Open next questions

1. **Does any mask fire at `(5, 24)`?**
   - *Why it matters:* it decides #4322's open question 1 between 24 and 26.
   - *First step:* enumerate only universal simple closed walks of length 24
     that contain a full level set of some mask (the cap's surviving
     `(8, 16)` split).
   - *Blocked by:* about two hours for a plain census on this machine.

## Credit

The model, the `n = 4` theorem and the open question are unpaidmoon's (#4322),
building on Nick Petalas's #3699 and #3733, Nicholas Stone's #2973 and the
PR943 walk. Prepared by Ryanson Jonathan with substantial Claude Code (Claude
Opus 5.5) assistance. Apache-2.0.
