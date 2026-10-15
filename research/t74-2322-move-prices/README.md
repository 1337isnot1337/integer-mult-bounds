# Exact move prices and owner-fill headroom on the T74 PR2322 words

**Research note; no κ claim.** This note gives exact local-move prices and a certified packing cap for the
words of [PR2322](https://github.com/CrocSwap/integer-mult-bounds/pull/2322) (Vlado Vojdanovski). Those
words underlie the current open T74 line: #2349, #2363 and #2374, whose claim is
κ = 0.0016971949509. It answers one planning question: after owner fills, where can the next gain on
these words come from, and how large can it be?

| finding | value |
|---|---|
| **certified cap, any legal whole-helper owner fill of the PR2322 words** | **b < 0.001697195759** |
| headroom above PR2374's claim | ≤ 8.1e-10 |
| one more PR2322-type handoff (same reshapes) | +4.27e-8 each, linear up to 12 (+5.13e-7) |
| one PR2339-type low alias | −1.91e-7 |
| one PR2339-type high alias | exactly 0 |
| one (1,1)→(2) merge of two rank-1 climbs (no width change) | +1.13e-7 |
| the 26 such target merges that come with PR2339's low aliases, on their own | +2.94e-6 |

All prices are LP-ceiling differences on the PR2322 words, both providers, at a = PR2374's κ.

**Owner fills on these words are finished.** The width-aware bin-pattern LP of
[PR2387](https://github.com/CrocSwap/integer-mult-bounds/pull/2387) /
[PR2360](https://github.com/CrocSwap/integer-mult-bounds/pull/2360) is certified with an exact rational
dual and 800-bit enclosures. It caps every legal whole-helper fill of these words at b < 0.001697195759,
with a W·mu margin of 1.85e-7 and zero dual repair. The certificate does not reject PR2374's claimed
point. PR2374 therefore sits within 8.1e-10 of the cap, and further owner relocations on these words can
add at most that much.

## Mechanism

Under the frame-climb rule, a climb of d dimensions on a register pays one recursive child of rank d.
Local mass equals 1856 plus the sum of helper widths, and the total rank mass is fixed. So a move changes
b only through the **shape** of the children and through the helper widths, which act via the bin
patterns.

`move_prices.py` recounts which register pays each child in the pinned words. It checks every recount
against the word's own reported profile and width inventory, then decomposes the realized changes
exactly; the reshapes add up to the profile change with nothing left over.

- **PR2312 → PR2322.** The four handoffs are:
  - remove helpers 619/621/622/623, each (1,1,1,1);
  - X lenders 1/4/6/12 go (5,1,1,1)→(2,1,1,1,1,1,1);
  - partners 616/617/618/620 go (4,1,1,1,1)→(3,2,1,1,1).

  The local change is {1:−2, 2:+2, 3:+1, 4:−1, 5:−1} with one fewer width-4 helper: a net −1.23e-5 per
  call in 66304·mu, a small gain. The LP predicts a +1.96e-7 ceiling gain from PR2312 to PR2322; the
  realized claims gained +1.69e-7. The underlying prices, LP-ceiling differences, are what this note
  reports.
- **PR2269 → PR2339.**
  - A low alias's lender takes over the removed helper's climb: (3,2,1,1,1) is removed and the lender
    goes (1,1,1,1)→(2,1,1,1,1,1,1,1). The net local change is −h(3), but the width change costs
    +0.04137 per call through the bins, a loss of 5.5e-5 per call. Successive low aliases cost more,
    because the LP is convex; this is why all 32 cost −9.8e-6 (PR2387).
  - A high alias is exactly price-neutral: its local −h(5) equals its bin cost.
  - The 26 targets whose climbs changed each gain exactly one (1,1)→(2) merge. That merge has no width
    effect and is worth +1.13e-7 by itself.

The independent recount (`independent_recount.py`) was written by a separate AI reviewer subagent
from a plain statement of the frame rules, with its own GF(2) code and no shared code. It reproduces
both providers' profiles, the exact PR2312→PR2322 change set and the site lists below.

## Untried sites (leads, not constructions)

- 33 helpers of the PR2322 words still climb (1,1,1,1). These are the 32 PR2226 low lenders 273..394
  plus 653.
- 12 X registers, 31 33 49 55 68 74 80 83 85 88 98 101, still climb (5,1,1,1) and lend no warp.
  These are the shapes of PR2322's four lenders before the handoff.
- Block 53 (registers 648–655) has exactly PR2322's pre-handoff pattern: helper 653 (1,1,1,1) next to
  four (4,1,1,1,1) partners 648/649/650/652. Its other three slots were already removed. PR2374 notes
  that alias 653 was dropped when 651 moved to lender 530.
- The other blocks pair (1,1,1,1) helpers with (4,1,1,1,1,1) mates.

If each extra handoff reproduced PR2322's reshapes, k handoffs would add k × 4.27e-8, up to 12 by the
lender count. Whether any of them admits a coherent rank-zero handoff (frame availability, lifetimes,
warp images, native lowering) is **not checked here**.

## Reproduce

From the repository root, standard library only:

```sh
python3 -I -B research/t74-2322-move-prices/move_prices.py --fetch          # ~16 s
python3 -I -B research/t74-2322-move-prices/independent_recount.py          # ~10 s
```

`--fetch` fetches `refs/pull/{2312,2322,2269,2339}/head` from the canonical repository if the pinned
commits are absent. The pinned commits are fb76f799, 002304ef, b479fc55 and bf1742ae; each word file
is blob- and sha256-pinned.

Expected final lines:
- `PASS_T74_MOVE_PRICES cap=0.001697195759 handoff_db=+4.272e-08 low_alias_db=-1.906e-07 high_alias_net=0 sites=33/12`
- `PASS_T74_INDEPENDENT_RECOUNT`

`vendor/pr2387/` holds byte copies of this author's PR2387 `ceiling_lp.py` and `fill_check80.py` and the
iteration-3 enclosure code, all pinned. `move_prices.py` patches one line of `local_recount` at load time,
to record the register that pays each child. All results were run on CPython 3.14.4; the registered
Python 3.12 replay was not run locally.

## Scope and limits

This is a pricing screen on fixed, pinned words:

- Moves are priced only by their per-register climb reshapes and width change, through the bin-pattern
  LP. Windows, families and ports are dropped, so prices are ceiling differences, not realized gains.
- The cap is a certified relaxation ceiling for unsplit helpers on the unchanged PR2269 bin stock, not
  a κ.
- No new handoff or merge is constructed.
- Prices are first-order in the sense that they are measured at the PR2322 operating point. The low-
  alias row shows that the LP is convex, so large moves need a re-solve, which the script does for the
  ladder.

## Open next questions

- **Block 53 handoff.** Does helper 653 admit a PR2322-type coherent handoff to a free (5,1,1,1) X
  register, with partners 648/649/650/652? The first step is to rerun PR2322's handoff generator with
  653 as the target role. Its price is +4.27e-8. PR2374 dropped alias 653, so its lender conflict is the
  blocker to check.
- **Target merges without low aliases.** The +2.94e-6 from the 26 (1,1)→(2) target merges dwarfs the
  owner-fill race. Can those merges be obtained without the width-9 low-lender inventory change? The
  first step is to identify which B-gate frames changed on those targets in the PR2339 words, and
  whether the anticipatory initial corrections (PR2394 lowers their prefix natively) can be kept with
  the original helpers. Note that #1995/#2013 bound frame freedom inside a fixed scalar word, so this
  needs a changed premise.
- **More handoff patterns.** Which X shapes other than (5,1,1,1), and which partner shapes, give
  positive prices? The first step is to tabulate prices for every (lender shape, partner shape) pair
  that occurs in the words.

## Credits and licence

- PR2322 (Vlado Vojdanovski): handoffs and words.
- PR2312 and PR2269 (Jeremy Kothe): width exchange and borrow43 words.
- PR2374 and PR2349 (jeremykothe2) and PR2363 (mason-hale): owner fills on PR2322's words.
- PR2226 (Cinna Davis / 1337isnot1337): anticipatory borrowing.
- PR2339 and PR2387 (this author).
- PR2360 (Jeremy Diviney) and PR1129 (Ali Romman): pattern-dual relaxation.
- PR2394 (commdata2338): native anticipatory prefix.
- PR1995 and PR2013: fixed-word frame bounds.
- PR1319 and PR1297: T74 lineage.

Prepared with substantial AI assistance (Claude Code, Anthropic, Claude Opus 5.5). The independent
recount was written by an AI subagent; no independent human review is claimed. Apache-2.0.
