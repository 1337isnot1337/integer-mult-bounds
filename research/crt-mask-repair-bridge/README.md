# One-target CRT repair bridge: produced mask -> direct keys -> sparse radix reinsertion

**Claim type: a joined, executable contract at the actual #4100 five-layer Beneš caller, with
one explicitly unpaid arithmetic premise. No new κ, no theorem, no tape evaluator.**

## Question

`research/pr4100-crt-repair-tariff` (#4328) ends with: *compose the hole mask, key evaluator and
repair into one fixed-tape program; their ownership and erasure contracts have not been joined.*
#4377 counts the key evaluator but its compiler is array-based. Each piece existed with its own
inputs: #4208/#4201 produce a mask on tapes, #4169 gives current-state reverse keys on host
arrays, #4328 builds its `MASK` from a host `good` list and takes keys from `T[inv_S[x]]`.

## What is joined (and run)

For each of the ten repaired layers of the actual caller (`check_compact_crt.py`: five Beneš
layers for padded moduli 3 and 5 over all 4096 labeled payloads, then the five reversed):

1. the **unchanged** #4208 `producer.py` builds the stencil from six unary geometry words
   `G,H,K,Y,J,B = 2,2,6,8,j,0` (exact `33H+25K+38Y-6G-J+12B+335` invoice asserted);
2. the **unchanged** #4201 `machine.transduce` scans it into the owned BAD mask
   (exact `8ML+15M+13L+18` invoice asserted; mask equals the source `good` predicate);
3. `bridge.py` consumes **that mask tape in place** — never a host good list: split by mask,
   key evaluated at marked addresses only, `L = 12` stable full-key radix passes over
   (payload, key) blocks, mask-driven reinsertion comparing the sorted key to the counter,
   physical erasure of mask, stencil, counter, good/bad streams and both buckets, head return;
4. recycled physical tapes must be blank with head at `LEFT` before the next layer
   (producer private roles are reused as good/bad/bucket roles).

Label 780 reaches address 777 after layer 5 and returns to 780 after the inverse five.
Every layer is also checked equal to the pinned table-based `check_compact_crt.layer`.

## The unpaid point

`bridge.evaluate_key` pays the tape actions that read the address cells and write the 12 key
bits. The mapping address -> `T(S^-1(q))` is `key_subroutine.ReverseWordKey`: the ten compact
shears run in reverse at the current `y` (kumagi's #4169), then the ideal switch. It is plain
Python integer arithmetic, called once per marked address, with no inverse table, no address loop
and no good-set test; the verifier compares it with #4169's `Word.run(inverse=True)` on every
address of every layer. **It is not a literal tape evaluator and its cost is not charged**; that
cost is CRT.md §4's premise `E(p,ell)` (counted in #4377). Everything else in the repair is a
read/write/one-cell-move program whose branching is finite control on read symbols; an AST
guardrail (review aid only) rejects host arithmetic, indexing, length primitives and observer
reads outside `evaluate_key`.

## Evidence

`PROOF.md` proves the composition for every geometry satisfying the predecessors' facts and
the key premise. `verify.py --part caller` replays the 10 layers (also receipts
`RESULT-caller.json`); `--part controls` runs the negative controls (`RESULT-controls.json`):
wrong keys (`ideal_of_current`, `inverse_only`, `stale_source`, `guarded_identity`) fed
through the real program on the actual layer and on a callable-source fixture; a mode whose key
equals the correct key at every hole of a fixture is reported as equivalent there, not as detected,
and each mode must be discriminated on at least one fixture; zeroed mask (zero key calls, wrong records); one hole unmarked;
truncated mask; over-marked good address (output right, one good key evaluation counted);
key evaluation on every good address; skipped sort; skipped clear of each of mask, stencil,
good, bad, counter, buckets; omitted head return; producer geometry mutants through the real
scanner; damaged source bytes rejected before execution. A skipped clear does not change that
layer's payloads (marker-driven reads) and is caught by the physical-blank gate; the README
and PROOF say so rather than claim the payload check catches it.

Exact per-phase action counts and the 12-bit-record weighted meter are in the receipts.

Author execution in the declared Python 3.12.14 environment passed the ten-layer caller
and all semantic controls. Across the ten layers: 29,440 marked-key calls, zero good-address
key evaluations, 133,110,830 repair actions and 226,260,150 record-bit-weighted repair
actions. The producer uses 8,422 actions and the scanner 4,548,300. The 2,266,880 key-interface
actions are included in the repair total, not added twice. Key arithmetic is excluded.

The control receipt contains 24 detected violations and two distinct non-rejection outcomes:
the key-identical stale-source case and the correctly repaired but overcharged extra mark.
The callable parity source makes the stale-source mutant fail the actual hole-key check.

An independent OpenAI-family verifier reviewed the Anthropic implementation and ran both
isolated optimized replay commands, comparing the existing receipts. The parent then ran
the complete registered package, which reported `PASS_REGISTERED_RESEARCH_PACKAGE` with
`outcome=partial`. Partial refers to the explicitly unpaid tape-evaluator and macro premises,
not to an incomplete execution of this package's two commands.

## Not covered

The macro `S` and the raw post-macro stream are host-built oracle inputs. One target per layer,
unary one-target geometry only; no many-target ordering, binary or transported geometry; no
`E(p,ell)` tape evaluator; no asymptotic `O(V)` claim here (the key premise and `L = Θ(p)`
calibration are CRT.md's).

## Reproduce

```sh
python3 scripts/research_package.py --package research/crt-mask-repair-bridge --check-only
python3.12 -I -B research/crt-mask-repair-bridge/verify.py --part caller
python3.12 -I -B research/crt-mask-repair-bridge/verify.py --part controls
python3.12 -I -B research/crt-mask-repair-bridge/verify.py --probe   # one layer, quick
```

Write receipts with `--write` (once). Standard library only.

## Open next questions

1. **Replace the key premise by a literal tape program.** *Why:* it is the only unpaid
   arithmetic here. *First step:* the ten reversed shears on the counter role for this geometry,
   plugged into `evaluate_key` and metered. *Blocked by:* a literal CRT-data evaluator (#4192 follow-up).
2. **Macro, many targets and transported geometry.** *Why:* the raw stream and layer hand-off
   are host-built. *First step:* the literal macro on the same data role. *Blocked by:* no pinned
   tape macro or many-target producer.

## Credit and AI disclosure

Cinna Davis (#4100/#4088, CRT.md and the caller); Hiroki KUMAZAKI (@kumagi, #4169/#4174, reverse
keys); ToikY (#4195/#4201/#4208, scanner, producer); Jose Manuel (@jmbarrancoml, PR2250, sparse
repair); Ryanson Jonathan (@pinterbanget, #4311/#4328/#4329, tariff and handoff); unpaidmoon
(#4377, evaluator bound); Douglas Colkitt/OpenAI and the NOTICE lineage. This
package joins their contracts. Prepared for codyw912 with substantial Anthropic Claude
implementation and OpenAI coordination/verification assistance; no human or formal-kernel
review. Apache-2.0.
