# The sparse exception repair tariff of #4100's CRT.md §4

**Claim type: a scoped proof audit (per-step accounting with explicit
constants and exact absorption at #4100's parameters), checked against a
literal tape run of the repair around #4100's own compact fixture. No new
κ.** This does not accept #4100 and changes nothing in it.

## Object and gap

The object is the repair step of Cinna Davis's
[CRT.md](../unconditional-batched-crt/CRT.md) §4, #4100 head
`337d04939571a637aeab54a0f58f54fde811663a`. It reads: "On the bad holes,
apply the correction key `T(S^-1(x))`, sort those holes by this full key on
fixed tapes, and merge them back … It does not sort the full input." It then
says that "bad-key evaluation, O(p)-bit keys, radix passes, counters and
clearing all fit O(V)".

**Every existing CRT audit leaves this tariff out:**
- #4169 lists "sequential head movement/sorting costs";
- #4174 lists the "sorting tariff";
- #4187 lists the repair integration;
- #4201 and #4208 list "exception extraction, inverse keys, sorting, payload
  routing, reinsertion";
- #4321 lists "bad-key repair".

**Why PR2250's tariff does not carry over.** The mechanism comes from
jmbarrancoml's merged PR2250
([PROOF §3–4](../selected-complex-compact-adapters/PROOF.md)): extraction,
inverse destination keys, two-bucket stable binary radix passes, keyed
reinsertion and erasure. Its cost is `O(V + M A³ + δ M A(R+A))`, absorbed
only because PR2250's records are superpolynomial (`A^C/R → 0`). In CRT.md,
`R` and `A = L` are both `Θ(p)`, so `M A³ = Θ(p²)·V`. CRT.md itself says not
to import that tariff unchanged. Its replacements are:
- the linear `O(ML)` guard scan (#4201) for the hole mask;
- `E(p,ell)`-cost keys evaluated only at holes;
- key comparisons only at holes.

Nobody had checked that combination.

**Outcome: the tariff holds.** Per color, the repair costs `O(V)` dense work
plus a sparse part that is `o(V)` with an enormous margin at every `p`.

## Results

Write `M = 2^L` records of `R` cells, `N` holes, and `δ = N/M`.

**1. Dense part: `≤ 9MR + 5M` cells.**
- Read the guard scan's hole mask once.
- Split good records onto a good stream.
- Reinsertion overwrites the data region from cell 0 and consumes the good
  stream and the mask in order.
- Erase both.
- No key, inverse or arithmetic work touches a good record.

**2. Sparse part: `≤ N(L+R)(9L+6)` cells, plus `N` key evaluations.**
- At each hole, copy the `L`-bit address, evaluate `T(S^-1(x))` (cost
  `E(p,ell)`, CRT.md's premise), and append key and record.
- Run `L` stable two-bucket LSD passes, each nine sweeps of the keyed holes:
  read, bucket write, two rewinds, bucket read, concatenation write, a
  two-sweep erase, and the next rewind.
- Reinsertion reads one sorted keyed hole per hole bit, then erases.

**3. Counter: `≤ 8M + 4LN + 4L`.** This is two amortized binary-counter
scans plus address reads at holes only.

**4. Correctness.** `T∘S^-1` permutes the bad set, because both maps
preserve it. So the `k`-th smallest key is the `k`-th hole address, and
reinsertion sends the record at `x` to `T(S^-1(x))`. This is PR2250's
argument, and it holds unchanged at these record widths.

**Caution.** The reinsertion check "key equals current address" only proves
that the keys *permute the holes*. Keys `S^-1(x)` without `T` also permute
them and pass the check, while misplacing every hole record (control below).
Correct keys therefore rest on the inverse evaluator: #4169's literal reverse
word, composed with `T`.

**5. Absorption at #4100's parameters.** CRT.md sets
`G = 64(ell + ⌈log₂(p+2)⌉)`, `B = 2^G`, `K = 64G` and `r ≤ L/(100G)`.
The bad density is `δ ≤ r(2/B + 8B/2^K)`, which the fixtures check exactly
at `r = 1`.

- **Sparse moves:** `δ(1+L/R)(9L+6) + δ·4L/R`. Since
  `2^-G ≤ 2^-64ell (p+2)^-64`, this is below `p³(p+2)^-64` for `L ≤ p` and
  `R ≥ p/8`. So it is absorbed at **every** `p`, not just eventually. The
  exact values range from `2^-640` (`p = 16`) to `2^-37,326` (`p = 2^64`).
- **Key evaluations:** `δ·E/R`, where `2^-G·2^(4ell)(p+2)^16 ≤
  2^(-60ell)(p+2)^(-48)` holds exactly. This is CRT.md's displayed line; the
  constant `C` in `E ≤ C·2^(4ell)(p+2)^16` remains CRT.md §2's.

## Evidence

`verify.py` uses only the standard library and takes about 6 seconds.

- **Fixtures.** The macro `S` and the ideal switch `T` come from #4100's
  pinned `check_batched_crt.py` (`compact`, `good`). There are five fixtures,
  with `B ∈ {4, 8, 16}`, guard 6 or 8, three source functions and
  `M = 1,024` to `65,536`.
- **Correctness.** Each fixture checks that `S` and `T` are bijections, that
  both preserve the good set, and that `S = T` on good addresses. The repair
  then realizes `T` on every record.
- **Density.** The measured density never exceeds `2/B + 8B/2^K`.

| `B`, guard, `M` | Holes | Dense / `MR` | Sorted / (holes·`L(L+R)`) |
| --- | --- | --- | --- |
| 4, 6, 1,024 | 736 | 5.91 | 9.50 |
| 4, 6, 16,384 | 11,776 | 5.76 | 9.36 |
| 8, 8, 16,384 | 6,976 | 7.23 | 9.36 |
| 8, 8, 65,536 | 27,904 | 7.18 | 9.31 |
| 16, 8, 65,536 | 36,736 | 6.51 | 9.31 |

Toy `B` makes holes dense here. At #4100's `G`, `δ ≈ 2^-G` (item 5).

**Controls,** each of which must fail:
- **Full-input sort.** It evaluates 16,384 keys, not 11,776, and moves
  262·`MR`, which is `Θ(L)·V`. This is why CRT.md avoids it.
- **Keys `S^-1(x)`.** 5,888 records are misplaced, undetected by the
  reinsertion check.
- **No repair.** 2,048 records are wrong.

**Source binding:** SHA256 pins of CRT.md, `check_batched_crt.py` and
PR2250's PROOF.md, with 9 exact phrases.

## Not covered

- The cost of the `E(p,ell)` evaluator itself; #4192 covers its Beneš part.
- The guard scan that produces the hole mask (#4201, #4208).
- The macro `S`'s ordinary interchanges, the last-`K` branch (#4187), and
  reservoir placement (#4174).
- The fixtures have one target. CRT.md's `r`-target density is the union
  bound, checked here only at `r = 1`.
- There is no proof-kernel check.

## Reproduce

```sh
python3 scripts/research_package.py --package research/pr4100-crt-repair-tariff --check-only
python3.12 scripts/research_package.py --package research/pr4100-crt-repair-tariff
python3.12 -B research/pr4100-crt-repair-tariff/verify.py
```

The verifier prints `PASS_PR4100_CRT_REPAIR_TARIFF_FINITE`.

## Open next questions

1. **Compose the hole mask, key evaluator and repair into one fixed-tape
   program.**
   - *Why it matters:* the three pieces (#4201/#4208, #4192/#4169, this
     package) are each audited with separate inputs and outputs. Their
     ownership and erasure contracts have not been joined.
   - *First step:* feed #4208's produced mask and #4169's reverse-word keys
     into this repair on one shared fixture.
   - *Blocked by:* the full `E(p,ell)` evaluator from CRT data (#4192's
     follow-up).
2. **Check multi-target density exactly.**
   - *Why it matters:* the `r`-target bound is a union bound over targets
     with disjoint guards.
   - *First step:* enumerate a two-target fixture (`positions=(0,6)`, 12 `y`
     bits) through the same repair.
   - *Blocked by:* nothing; it costs `2^20` records.

## Credit

The construction and audited claims are Cinna Davis's #4100 (OpenAI Codex
assistance). The repair mechanism (extraction, keys, two-bucket radix passes,
keyed reinsertion) is jmbarrancoml's PR2250, building on Douglas Colkitt's
compact-control construction. kumagi's #4169 supplies the reverse-word keys,
and ToikY's #4201/#4208 the hole mask. This independent tariff audit was
prepared by Ryanson Jonathan with substantial Claude Code (Claude Opus 5.5)
assistance. Apache-2.0.
