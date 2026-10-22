# PR4633: unsupported supplier claim and boundary repair obstruction

Reviewed PR4633 head: `b390d64abfcdba1a3816b86fc763cbc95d43c12c`.
Review date: 2026-10-22. Local evidence; no GitHub review, comment, or PR posted.
Prepared with substantial OpenAI Codex assistance. Apache-2.0.

The claimed improvement cannot be retained by quotienting the submitted frames
and adding per-port boundary adapters. This is a scoped obstruction to that
repair, not an impossibility theorem for new suppliers or joint circuit rewrites.
No new kappa is established. Frozen predecessor files are unchanged.

The PR description still advertises the earlier one-dimensional value
0.012401086416. The reviewed commit's actual artifact uses
`span{150,102,255}` and claims BIT kappa 0.032249423394893. The findings below
apply to those committed bytes.

## Blocking findings

1. **Rational E8 frames are changed into binary subspaces without preserving the
   port split.** `bit-ambient-quotient/build.py:47-54,121` reduces the annihilator
   rows modulo 2. The source exporter explicitly defines these as rational
   bases and annihilators. All 111 source entrance lines avoid their terminal
   hyperplanes over Q. After the builder's field change, before any quotient,
   103 entrance lines lie inside their terminal hyperplanes. For port 8,
   entrance frame 10 has basis `u=(0,1,1,0,1,0,0,1)` and terminal frame 533 has
   normal `u`. The dot product is 4 over Q and 0 over F2. Thus `u` changes from
   outside to inside the terminal. Equal individual frame dimensions do not
   preserve this incidence. Every subsequent linear quotient preserves
   containment, and the full-image padding also preserves it. A different
   kernel alone cannot restore the required disjointness on those ports.

2. **The invoice credits a different operator.**
   `bit-ambient-quotient/verify.py:84-94,150-163,185-194` uses block 7 and one
   central rank on every main output without requiring the corresponding
   endpoints. At the reviewed head all 111 ports fail the necessary interface.
   Main widths are `{4:103,7:70,8:49}`; only 70 of 222 are width 7. Restoring
   helper finals to dimension 8 does not restore this main interface.
   The local saving of 287 consists of 260 missing main ranks and 27 missing
   COPY ranks. The stacked complex artifact also fails the priced block-8
   interface on every port: 56 ports have a complementary rank-1 entrance and
   rank-7 terminal, hence block 7; the remaining 56 have rank-8 terminals
   containing the entrance. These are artifact endpoint checks, not a fresh
   replay or physical lowering of the complex dependency.

3. **The verifier trusts paid ranks and does not bind logical replay to the
   physical endpoint.** `bit-ambient-quotient/verify.py:105-111` does not derive
   a MOVE's rank from its frame bases or check containment. Setting every MOVE
   rank to zero still passes both logical replays, including all 661 arbitrary
   columns and endpoints, and lowers the reported local mass from 4842 to 36.
   The new `check_transports` guard rejects this mutation. The new
   `require_supplier` guard rejects the actual artifact's endpoints. These
   are necessary checks; passing them would not establish full admission.

The proof's assertion that no MOVE is lengthened is also false after padding:
557 MOVEs grow, adding 1618 ranks on those records. For example, source record
21373 (zero based), on role 457, grows from rank 2 to rank 5. The net paid mass
still falls; this finding corrects the proof's monotonicity claim.

## Repair attempted and exact obstruction

Give the construction its most favorable binary preimage-frame interpretation.
Allow each port to choose **any** new entrance line P' and terminal hyperplane
H' with `P' intersection H' = 0`. Keep X's full endpoint, Y's zero entrance and
all helpers. This is more permissive than requiring the original charts or
proving the exact representatives give the controller's common stage operator.
Only per-port frame adapters are allowed; joint scalar rewrites are outside
this calculation.

For preimage frames U,V the physical transition rank is
`d(U,V)=dim(U)+dim(V)-2dim(U intersection V)`; see
`notes/general-clifford-frames.tex`. Any chain of transitions has total rank
at least this distance. For each integer cap c its cost is at least
`min(d(U,V),c)` as well. The current port types and optimal adapters are:

| dim X entrance | dim Y terminal | intersection dimension | ports | added child ranks per port |
| ---: | ---: | ---: | ---: | --- |
| 0 | 4 | 0 | 41 | 1 and 3 |
| 1 | 4 | 1 | 62 | 5 |
| 1 | 8 | 1 | 8 | 1 |

The verifier enumerates all 255 nonzero hyperplane normals. For each hyperplane
it minimizes X's adapter over every entrance line avoiding that hyperplane.
This exhausts all 32640 complementary pairs for each port. The table minimizes
every capped rank moment, not merely the sum of ranks. Its aggregate extra
profile is `{1:49,3:41,5:62}`, with rank mass **482**. Therefore:

```
submitted local paid mass:       4842
minimum boundary adapter mass:   482
repaired local paid mass:        5324  (source: 5129)
global rank surplus:             5919 - 18*482 = -2757
```

Negative rank surplus alone would not settle every noninteger moment. Here
the stronger condition is checked exactly: for every integer cap `c=1..127`,

```
sum_paid count(r)*min(r,c) - sum_target count(r)*min(r,c) >= 2757.
```

Every increasing concave function on these integer ranks, with f(0)=0, is a
nonnegative linear combination of the capped functions `min(r,c)`. For
`f(r)=r^t`, `0<t<=1`, write `s_i=i^t-(i-1)^t`; then
`f(r)=s_127*r + sum_{i=1}^{126}(s_i-s_(i+1))*min(r,i)`.
All coefficients are nonnegative and sum to 1. Consequently the repaired paid
moment exceeds the target moment by at least 2757 for every `t=1-kappa` in
`(0,1]`. The first screen inequality fails throughout `0<kappa<1`; changing
the tail cutoff or admission literals cannot repair this invoice.

This exhausts endpoint adapters in the stated relaxation. It does not rule out
changing the internal word, applying operations jointly across ports, or
proving another controller and paying for its actual endpoints.

## Reproduce

```
python3 -B research/pr4633-kappa-audit/verify.py
python3 -B research/pr4633-kappa-audit/verify.py --require-supplier
```

The first command takes about one second and reports
`PASS_AUDIT_REJECTS_UNSUPPORTED_KAPPA`. The second intentionally exits nonzero
because the submitted supplier fails the endpoint guard. `--write` regenerates
only this audit's `RESULT.json`. The verifier authenticates all eight inputs by
SHA256, replays the source and submitted BIT word in both directions, checks
every submitted MOVE's nesting and dimension tariff, exercises the false-rank
control, and proves the finite capped-moment inequalities with integer arithmetic.
It never calls either predecessor's artifact-writing `main` function.

The subject's input pins, exact endpoint census, adapter profile and all 127
cap gaps are in `RESULT.json`. No Lean check, selected-frontier replay, hosted
CI, or new physical lowering is claimed. The selected record on canonical main
at `fbc9ea0249746acca4f504d4fda2b84e0e36cf0d` remains the conditional
`60403/20000000 = 0.00302015`; this audit does not change it.

## Open next questions

- Can a genuine representation of the E8 frame incidences support a cheaper
  internal word with all original physical endpoints pinned? Start with the
  port-8 field-change counterexample and require a representation proof before
  pricing. The modulo-2 conversion is not such a proof.
- Can a joint rewrite avoid the independently paid boundary adapters? It must
  supply the actual port operator, common stage transform, central shear and
  full recursive invoice. The obstruction here addresses endpoint adapters.

## Attribution and sources

DaysSky's PR4633 supplies the quotient and claimed invoice. Its BIT source is
DreamingOfClouds' PR589 E8 word and the credited eumemic/PR555/PR543 lineage.
Its complex source is Cinna Davis's PR4470 chain. The endpoint concern was raised
by pinterbanget in PR4604, studied for the complex kernel family by Nick Petalas
in PR4627, and developed in Rohan Arun's PR4633 audit comment
<https://github.com/CrocSwap/integer-mult-bounds/pull/4633#issuecomment-6341849407>.
This audit extends that concern to the current three-dimensional head, supplies
the rational-to-binary counterexample and false-rank control, and checks the
boundary repair cost and all concave rank moments exactly.
