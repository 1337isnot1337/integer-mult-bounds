# PR2374's owner fill is optimal over all whole-helper fills of the PR2322 T74 words

**Audit / independent check; no κ claim.** [PR2374](https://github.com/CrocSwap/integer-mult-bounds/pull/2374)
(Jeremy Kothe) claims κ = 0.001697194950901770… from "an exact window-free-optimal owner fill" on
[PR2322](https://github.com/CrocSwap/integer-mult-bounds/pull/2322)'s words. Its published leftover idle ranks
are `{1:21978, 3:8592, 5:2552, 32:1, 48:24560}`. This package checks the optimality claim by a different
method, over a strictly larger class of fills.

**Result.**
- Every legal whole-helper owner fill of the PR2322 words on the unchanged T74 template has complex root
  **b ≤ κ₂₃₇₄ + 10⁻¹⁵**.
- PR2374's idle multiset is the **only** one whose root exceeds κ₂₃₇₄ − 10⁻¹².
- The window-free optimality claim is therefore confirmed, and strengthened to optimality among all legal
  whole-helper fills. Owner-map work on these words cannot gain more than 10⁻¹⁵. The earlier cap in
  [PR2402](https://github.com/CrocSwap/integer-mult-bounds/pull/2402) allowed up to 8.1e-10.

## Method (`owner_optimum.py`)

1. **The relaxation.** A legal fill places every helper role whole into one idle bin. The bins have ranks
   8/16/32/48 and counts 49,728 / 33,152 / 33,152 / 33,152. So the fill's idle remainders come from an
   integer pattern-count vector x ≥ 0 over the 1,163 width patterns, with the bin and width-inventory row
   sums fixed (PR2387 / PR2360 relaxation, after PR1129). Windows, families and ports are dropped. That
   makes this a relaxation of every legal fill, and the moment is linear in x.
2. **Root check.** The PR2322 local profile (recounted in PR2402) plus PR2374's idle multiset has its root
   certified within ±10⁻¹⁵ of the claimed κ, using 800-bit enclosures. Its rank mass equals 73·66304 − 23680.
3. **Exact dual.** At a₀ = κ₂₃₇₄ + 10⁻¹⁵, a float simplex dual is repaired to an exact rational dual. It is
   feasible against 800-bit lower enclosures of h(r) = (r/73)^(1−a₀) on all 1,163 patterns. Every integer
   x then satisfies

       66304·μₓ(a₀) ≥ L_loc + D + Σ_p rc_p xₚ,   rc_p ≥ 0 exact,

   and if Σ rc_p xₚ ≥ T := 66304 − L_loc − D, then bₓ ≤ a₀. Here T ≈ 1.5475e-4.
4. **Enumeration.** Every integer x with Σ rc_p xₚ < T is enumerated exactly.
   - Only 9 basic and 7 non-basic patterns have rc < T.
   - The 2 degenerate patterns, (32: 7,8,8,9) and (32: 7,7,9,9), are checked to swap only zero-remainder
     patterns, so they never change the idle multiset. Their basis representation is integral, so their
     counts never affect integrality.
   - Any solution using them therefore maps to a count-0 representative with the same idle multiset and the
     same Σ rc. That representative is checked to be nonnegative for every candidate combination, so the
     sweep is complete.
   - The other 5 have reduced costs 5.5e-5 … 1.5e-4, which allows counts ≤ 2.
   - Basic variables are solved in exact rationals.
5. **Result at a₀:** zero integer survivors, so every fill has b ≤ a₀.
6. **Control at κ₂₃₇₄ − 10⁻¹²:** the same procedure must let PR2374's own fill survive, and it does. The 25
   survivors there are degenerate copies of one fill, a single empty 32-bin, and all carry PR2374's idle
   multiset. That gives the uniqueness statement.

An adversarial AI reviewer tried to refute the argument and found it **not refuted**. Using its own code
(Decimal at 90 digits), it:
- reproduced PR2374's root to 60 digits;
- confirmed with a Gomory group-relaxation shortest path that the only correction within the budget is one
  empty 32-bin;
- ran local search over more than 48,000 exchanges of up to 4 bins without finding any improvement.

Its runner-up fill, `{1:21978, 3:8591, 5:2553, 30:1, 48:24560}`, has a root 5.0e-10 below PR2374's. Its
two wording issues are fixed here: the nonnegativity argument for the degenerate sweep, and the
degenerate-copy count.

## Reproduce

From the repository root, standard library only. It needs no network, since all inputs are vendored and
pinned.

```sh
python3 -I -B research/t74-2374-owner-optimality/owner_optimum.py     # < 1 s
```

Expected final line:
`PASS_T74_2374_OWNER_OPTIMUM survivors_above=0 bound=kappa_2374+1e-15 idle_multisets_within_1e-12=1 no_new_kappa`

All results were run on CPython 3.14.4; the registered Python 3.12 replay was not run locally.

## Scope and limits

- **What is not re-checked.** PR2374's realization of its fill (windows, families, ports, admission, outer)
  is its own claim and is not re-run here. Only its published idle multiset and claimed κ are used.
- **What the statement covers.** It is about owner fills of the fixed PR2322 words, the 249/417 dispatch
  and the unchanged PR2269 bin stock. Changed words, inventories or templates are outside it; see PR2402
  and PR2429 for those levers.
- **Exactness.** The enumeration is exact (integer and rational), with an exact dual and enclosures. The
  only floating-point step is the simplex that proposes the dual, and its repair is exact.

## Open next questions

- **Other inventories.** Do the same exact integer-optimality certificates hold for PR2312's and PR2269's
  inventories? That would show whether every recent owner-fill PR on the T74 line was already at the
  integer optimum. First step: run `owner_optimum.py` with their inventories and published idle
  multisets.
- **Recursive-interface levers.** Since packing on these words is exhausted, which word-level move is
  cheapest to realize? Candidates are a block-53 handoff (+4.3e-8, PR2402) and cold-restoring one
  end-climb-3 helper (+1.46e-6, PR2429). First step: attempt the PR601-style commutation test on the 64
  end-climb-3 helpers.

## Credits and licence

- PR2374 / PR2349 (Jeremy Kothe) and PR2363 (mason-hale): the audited fills.
- PR2322 (Vlado Vojdanovski): the words.
- PR2360 (Jeremy Diviney) and PR1129 (Ali Romman): the pattern-dual relaxation.
- PR2387 / PR2402 (this author): the LP and recount tools, vendored with pins.

Prepared with substantial AI assistance (Claude Code, Anthropic, Claude Opus 5.5). An adversarial AI
reviewer was used; no independent human review is claimed. Apache-2.0.
