# Guard windows under #4100's position-mod-K coloring

**Claim type: a scoped proof audit with a counterexample to the literal text,
plus a census of #4174's actual production descriptors. No new κ.** This
does not accept #4100 and changes nothing in it.

## Object

Cinna Davis's [CRT.md](../unconditional-batched-crt/CRT.md) §4, at #4100 head
`337d04939571a637aeab54a0f58f54fde811663a`, says three things:

- the good predicate requires "a margin 2B from both ends of each K-bit
  guard";
- the bad density is at most `r[2/B + 8B/2^K]`;
- "Color targets by current position modulo K, so guard intervals are
  disjoint."

Three open audits take this disjoint-guard premise as given:

- #4321 (unpaidmoon) assumes "the `K`-bit guards are pairwise disjoint" and
  notes that no audit decides that hypothesis.
- #4328's exact `r`-target density needs disjoint windows.
- #4174 (kumagi) supplies the actual placement descriptors; this package
  checks them.

## Results

### 1. Lemma

Let one macro's active targets all share a color, that is, a residue of their
`y`-significance position mod `K`.

- With `(K−1)`-bit guards (the `K−1` bits above each target), the guards are
  pairwise disjoint and contain no active target, for every descriptor.
  Distinct same-color targets differ by a nonzero multiple of `K`, hence by
  at least `K`.
- With `K`-bit guards, they are still pairwise disjoint, but a guard contains
  another active target exactly when two same-color targets are `K` apart.

This is checked exhaustively on 3,266 small position sets.

### 2. The literal `K`-bit reading fails on #4100's own gadget

In #4100's `check_batched_crt.py`, `good(…, guard=g)` reads `g−1` window bits.
Its two-target fixture places the targets at positions 0 and 6, exactly
`K = 6` apart. Running every one of the `2^20` addresses:

| Source | Window bits | Good addresses | `S ≠ T` on good addresses | `T` leaves the good set |
| --- | --- | --- | --- | --- |
| #4100's `source_pair` | 5 (`K−1`) | 82,944 | 0 | 0 |
| #4100's `source_pair` | 6 (`K`) | 186,624 | **3,888** | **31,104** |
| second pair | 5 (`K−1`) | 82,944 | 0 | 0 |
| second pair | 6 (`K`) | 186,624 | **2,388** | **15,552** |

Example: `(u,t,y) = (0,1,1086)` goes to `(0,5,1087)` instead of
`(0,1,1087)`. A carry inside target 0's 6-bit window flips target 1 before
target 1 is read, so the control field is not restored.

**Consequence.** The premise must read "**`(K−1)`-bit guards**, free of active
targets". The equivalent alternative is `K`-bit guards with coloring mod
`K+1`. This matches the code, and it matches the density term `8B/2^K`,
which counts `4B` bad values in `K−1` bits. A `K`-bit window would give
`4B/2^K`. This is a presentational correction to CRT.md's "K-bit guard" and
to #4321's hypothesis wording. No bound changes.

### 3. #4174's production descriptors

The layout is #4174's own production census: `d = 65,536`, `ell = 24`,
widths alternating 24/23, `p = 6L`. That gives:

| `L` | `G` | `K` | `r_max` | `H` | `y` bits |
| --- | --- | --- | --- | --- | --- |
| 1,540,096 | 3,072 | 196,608 | 5 | 15,360 | 1,494,016 |

The census covers all 104,864 plans, 524,288 active-axis visits and 524,314
fragments:

- **Every active axis lies in `y`** after the three exchanges.
- **No two active axes of any plan can ever share a color, for any Beneš bit
  schedule.** For every pair of fragments, the range of position differences
  contains no nonzero multiple of `K`. This holds even though pairs reach
  1,463,286 bits apart. The aligned schedule (bit `m` on every axis wider
  than `m`) confirms it over 12,304,384 target visits: maximum color
  multiplicity 1, and no exact-`K` pair.
- **So at production parameters the disjoint-guard premise holds
  vacuously,** and each compact macro handles one target. The multi-target
  cancellation, and #4328's `r ≥ 2` density, are not exercised there. The
  `O(K)`-colors-per-layer tariff covers this.
- **The last-`K` branch carries a material share.** 16,225 plans (15.5%) have
  active axes in the top `K−1` bits of `y`. Under the aligned schedule,
  388,466 plan-layers contain exceptions, up to all 5 targets. At these sizes
  `K/|y| ≈ 13%`. #4187 audits that branch at `O(VK)`.

## Evidence

`verify.py` uses only the standard library and takes about 18 seconds. It
also checks the source bindings: SHA256 pins of CRT.md and
`check_batched_crt.py`, 3 exact CRT.md phrases, `good()`'s `guard−1` window
expression, and the byte hash of the vendored allocator.

## Not covered

- Other production layouts. Only #4174's own pattern is censused here.
  Other mixed-width patterns or larger `ell` could, in principle, create
  same-color pairs; the lemma still covers them with `(K−1)`-bit guards.
- The elementary last-`K` branch's correctness (#4187).
- The control-function supports (#4169, #4174).
- There is no proof-kernel check.

## Reproduce

```sh
python3 scripts/research_package.py --package research/pr4100-guard-coloring --check-only
python3.12 scripts/research_package.py --package research/pr4100-guard-coloring
python3.12 -B research/pr4100-guard-coloring/verify.py
```

The verifier prints `PASS_PR4100_GUARD_COLORING_FINITE`.

## Open next questions

1. **Price macros per occupied color, not per residue.**
   - *Why it matters:* at production every color is a singleton, so a layer
     uses at most `r_max` macros per batch rather than `K`. The tariff could
     be stated per occupied color.
   - *First step:* bound occupied colors per batch by `r_max` in the CRT §4
     cost line.
   - *Blocked by:* nothing.
2. **Census other admitted width patterns.**
   - *Why it matters:* the vacuity finding is pattern-specific.
   - *First step:* run the census on blocked and random `ell`/`ell−1`
     patterns at `d = 65,536`.
   - *Blocked by:* nothing; about 20 seconds per pattern.

## Credit

The construction and audited text are Cinna Davis's #4100 (OpenAI Codex
assistance). The placement descriptors are Hiroki KUMAZAKI's (@kumagi) #4174,
vendored unmodified; see [vendor/NOTICE.md](vendor/NOTICE.md). #4321
(unpaidmoon) states the guard hypothesis this package decides. Prepared by
Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5) assistance.
Apache-2.0.
