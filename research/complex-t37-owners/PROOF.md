# The T37 owner composition

## What changes, and what does not

The complex local supplier (PR869/PR870 U8 word: paid profile
`{1:2548,2:338,3:446,4:162,5:72,8:8}`, helper widths
`{4:80,5:32,7:54,8:122,9:216}`), the PR589 bit supplier, both rational moment
engines and the seven-step outer recipe are PR890's, unchanged. Only the
replica count, the whole-owner map and one charged finite constant change.

## Why PR890's bound stops at T21

PR890's exhaustive relaxation (PR795 signed dual) is stated for
`T <= 22`, because the retained prefix charge is `113+18T < 512`. The 512 is
the *charged* global prefix payload. In the inherited finite invoice it is
paid in exactly two places: the prefix reserve `prefix < payload` and the
physical row coefficient `row = 2*bitlen(stock)+9909+252+2*payload < 20161`;
the outer bootstrap additionally checks finite cutoffs `cut*gap >= 2*(4+payload)`.
None of the moment, deficit or 47 outer inequalities depends on it (the outer
row gap uses the retained bound 20161, not the actual row). Charging
`payload = 1024` costs `row = 17495 < 20161` and leaves every other inequality
unchanged; the bootstrap cutoffs are recomputed at `2*(4+1024)`. The retained
PR531 invoice is still required to have been charged at 512 and its allowance
is retained in full, as before. Precedent: earlier packages raised other
charged allocations (192 -> 256) after recomputing their reserves.

## The relaxed optimum over all T

Running PR890's own relaxation without the `T <= 22` cap (same dual, same
price table): per replica the excess over all-48 is mass `30 (mod 48)` and
signed credit `150`. Rank-one remainders have the best credit per cost
(credit 925). Six rank-one remainders give credit `5550 = 150*37` and mass
`6 = 30*37 (mod 48)`, so T37 with idle `{48:11086, 1:6}` meets the dual with
equality and is the unique-shape normalized optimum for every T (multiples of
37 repeat it). Its normalized penalty `6c(1)/37` is below T21's
`(3c(1)+c(3))/21`.

## Construction

1. PR890's T21 map (PR858 T16 + literal T5 + nine edits) is rebuilt by its own
   unchanged constructor; its own independent checker is rerun on it.
2. PR858's T16 map is rebuilt unchanged and relabelled into replicas 21..36
   (replica, owner, copy and family offsets `+21`, `+21*112`, `+21*896`).
3. The 189 T21 calls and 144 T16 calls are merged by the key `(i+1)/189`
   versus `(j+1)/144` (ties: T21 first). Each component keeps its own order,
   so every component role keeps its window.
4. Before the trade the idle profile is `{48:11085,44:1,3:1,2:1,1:5}`, which
   is worse than T21. Eight frozen edits (`data/EDITS.json`) apply the
   credit-neutral trade `(44,3,2) -> (48,1)`:
   - the lone width-4 role of the cap-48 bin (owner 29, child 8, port 0)
     moves into a full bin of owner 20; the width-4 role it displaces (a later
     T21 call) moves on to bin (20,14,111);
   - bins (20,14,111) and (27,15,0) (fills 29 and 30) are repacked as
     `{8,4,4,4,4,4,4} = 32` and `{9,9,9,4} = 31`, moving one width-9 role
     (T21 call) into owner 27 and two width-4 roles (second-T16 calls) into
     owner 20.
   All moves are cross-component, so no moved role is hosted by its own
   replica. The result is `{48:11086, 1:6}`.

## Checks

The independent checker (PR858/PR890 code, `T = 37`, payload 1024) checks all
`333*504 = 167832` roles against the actual source-event windows, families,
per-call distinctness, whole widths, contiguous slices, all 73-axis charts,
exact per-replica projections, idle profile, deficit `320*37 = 11840`,
prefix `72+37+333+333+4 = 779 < 1024`, row `17495 < 20161` and halving.
Every omitted edit is rejected, and so is the same map under the sequential
(non-interleaved) schedule. The partial bank envelope 8+8+8+8+5 is audited
literally with eight mutations. The PR870 controller chain (bind, emit,
asynchronous audit with mutations, invoice, assembly, 69 admission and 12 bit
controls) runs with cardinality edits and the payload edits listed in
`data/ADAPTER-EDITS.json`.

## Price

Live `33152`, rank mass `73*33152-11840 = 2408256`. Both engines certify

```
b = 1664727258740678855772 / 10^24
```

(accept at b, reject b+10^-24); bit `c` unchanged. The outer recipe gives

```
kappa = 1661960547713947 / 10^18 = 0.001661960547713947
```

which is `2.773066918e-9` above PR890.

## Scope

Inherited hypotheses are unchanged (all-size compiler, common-label/mutable
source realization, whole-call hosting, precision/tape, analytic transfer, bit
H1-H5). The new explicit premise is that the charged global prefix payload is
a finite constant priced only through the reserves listed above.
