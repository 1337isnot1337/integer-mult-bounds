# Joined mask / key / repair contract: statement and proof

Scope: one repaired switch layer of Cinna Davis's #4100 `CRT.md` §4, one target. This proves
the *composition* (representation, ownership, erasure, correctness of the sparse reinsertion)
under an explicit key premise. It does not prove or execute the key arithmetic on tapes.

## Setting

Address space `A = {0,1}^L`, `L = 12`, `x = (u:2, t:2, y:8)`, MSB first. `S` is the literal
compact macro (ten shears), `T` the ideal controlled switch `y -> y xor (f(y) << j)`,
`good` the #4100 predicate (digits `u,t != 3`, the `K-1 = 5` bits above target `j` lie in
`[8,24)`). Facts used from predecessors (not re-proved here):

* (F1) `S` and `T` are bijections of `A` preserving `good`, and `S = T` on `good`
  (#4100 `check_compact_crt.py`; universal argument #4169 PROOF.md for a source `f` omitting
  its targets).
* (F2) `S^-1` is computed at the CURRENT `y` by running the ten shears in reverse with negated
  offsets (#4169). Hence `T o S^-1` is computable at one address without a table.
* (F3) The unchanged #4201 scanner outputs `mask[q] = 1` iff `q` is bad, from the stencil
  produced by the unchanged #4208 producer, with exact invoices
  `T_prod = 33H+25K+38Y-6G-J+12B+335` and `T_scan = 8ML+15M+13L+18`.

Let `raw` be the stream after the macro: `raw[S(x)] = payload(x)`. Goal: `final[T(x)] = payload(x)`.

## Contract of `bridge.repair`

Tapes (fixed roles): `stencil, mask, counter, data, good, bad, b0, b1`. Inputs: `stencil` and
`mask` are the producer/scanner's own output tapes, `data` holds `raw` as `LEFT, (R,v)^M, END`,
`counter, good, bad, b0, b1` are physically blank (`LEFT` then `BLANK`). Key premise
(K): `key_function(addr)` returns `T(S^-1(addr))` as `L` bits for every `addr`.

Postcondition: `data = final` (same length); `mask, stencil, counter, good, bad, b0, b1` are
physically blank apart from permanent `LEFT`; all heads at `LEFT`; the key function was
called once per marked address and on no other.

## Proof

**Counter.** `init_counter` writes `0^L END` (one `0` per stencil atom, so `L` is carried by the
stencil, never by a host integer). `advance` runs to `END` and applies the scanner's own
carry; it returns "wrapped" exactly after `2^L` increments, and the program raises if
"wrapped" disagrees with the mask `END`. So at the k-th loop iteration the counter spells
`k` (MSB first) and the mask cell read is `mask[k]` (mask and address space have equal length).

**Split.** For `k` with `mask[k]=0` the record of `data[k]` is appended to `good` and no key is
read. For `mask[k]=1` the record and then `key_function(k)` (the address read off the counter
cells) are appended to `bad` as a block `R, key^L`. No other path touches `key_function`.
Hence `good` is the subsequence of `raw` at good addresses, `bad` the blocks at bad addresses
in address order, each carrying `key_k = T(S^-1(k))`.

**Keys permute the holes.** By (F1), `S^-1` and `T` both preserve bad = complement of good, so
`k -> key_k` is a bijection of the bad set onto itself (also: `raw[k]` is the payload whose
ideal destination is `key_k`, because `payload(x)` sits at `S(x)` and `x = S^-1(k)`).

**Radix.** One pass moves each block, stable, to `b0` or `b1` by the LAST key bit, rotating that
bit to the front of the key, then concatenates `b0 b1` into `bad`. After pass `i` the blocks are
stably ordered by original bits `b_0..b_{i-1}` (LSB first) and the key is the rotation of the
original by `i` places. This is the textbook LSD argument with the dropped bit re-attached.
After `L` passes the keys have their original orientation and the blocks are ordered by the full
key, with all keys distinct (keys are a permutation of the holes). The stencil is the pass
counter (`L` atoms), not a host integer.

**Reinsertion.** The `r`-th smallest key is the `r`-th smallest bad address (the keys are
exactly the bad set). Walking addresses in order with the counter, a bad address takes the next
sorted block and the program compares its key bits with the counter bits, raising on any
difference; a good address takes the next `good` record. Thus `final[k] = payload(x)` where
`T(x) = k` for bad `k` (the block whose key is `k`), and for good `k` the record
`raw[k] = payload(S^-1(k))` with `T(S^-1 k) = k` by (F1) (`S = T` on good and `S^-1(k)` good).
Both streams end together or the program raises. So `final = T`-image of the payloads. QED.

The reinsertion key check is necessary but NOT sufficient for correct keys: any bijection of
the holes passes it (`ideal_of_current`, `inverse_only`, `stale_source`, `guarded_identity`
keys all pass or fail it without the payloads being right). Correctness of the repair therefore
rests on premise (K); the verifier exercises these four wrong keys, counting a mode as detected only where it changes
some hole key (equivalent fixtures are recorded as such).

**Ownership/erasure.** `erase` reads to `END`, blanks every cell including the allocated `END`,
and rewinds. `repair` ends by erasing `mask` (consumed), `stencil` (consumed), `good`, `bad`,
`counter`, and each pass erases `b0, b1`. Each role is then physically `LEFT, BLANK*`, so the
next layer's producer/scanner/repair reuses the same physical tapes; the verifier asserts
blankness before every reuse. `data` is overwritten in place cell by cell (no extra length).

**What a skipped clear costs.** Marker-driven reads stop at `END`, so stale cells beyond a
rewritten marker are not read by the next layer; skipping a clear is therefore a *state/
ownership* defect that does not change that layer's output, and it is caught by the physical
blank gate, not by the payload comparison. The verifier states this and detects it by the gate.

## Cost (explicit model)

One action = one read, write, or one-cell move of the finite-alphabet cell/head model; a record
cell additionally counts `R = 12` bit-widths in the observer bit meter. With `M = 2^L`, `N` holes:

* producer `T_prod` and scanner `T_scan` exactly as in (F3), unchanged;
* init `O(L)`; split `O(M L + N L)` (counter advance and address read are `O(L)` each) plus
  `N` key-call interfaces of `O(L)` actions each;
* sort: `L` passes, each `O(N L)` actions (each block is scanned, its last key bit fetched and
  the block rewritten), i.e. `O(N L^2)`; erase of buckets `O(N L)` per pass;
* reinsertion `O(M L + N L)`; final erasure `O(M + N (L+1) + L)`.

The verifier reports exact observed counts per phase and per layer. Key ARITHMETIC (the body of
`key_function`: ten shears, a Beneš table lookup, an ideal switch, over `E(p, ell)`-bounded data
in #4377) is not charged and not on tapes; only the interface actions are. This is the
"explicit paid key subroutine" premise: its cost is `E` per call from #4377's counting proof.

## Limits

* Macro `S`, and the raw stream/ideal layout used as oracles, are host-built; only the repair
  (and, upstream, producer and scanner) is a tape program.
* The geometry is the unary one-target family of #4208 with the fixed `u2,t2,y8`; many-target
  ordering and binary/transported geometry are not covered.
* `key_function` is not a tape program (stated above). The AST guardrail is a review aid.
* The 4096-payload runs are finite evidence for the actual caller; the algebraic statement is
  the proof above, for every `(L, f)` satisfying (F1)-(F3) and (K).
