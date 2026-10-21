# Keep the 102 fresh width-five outputs at width five

PR #4359 adds a rank-one call to every fresh native width-five helper so
that all productive target ranks exceed every paid rank. Its new finite
compiler requires that strict separation. The topups are a compiler
interface cost, not part of the helpers' autonomous native endpoints.

There are 102 such calls in the actual p3 word. Deleting those calls and
retaining their native rank-five outputs gives the following complete
local invoice:

| Rank | Productive jobs | Paid calls |
| ---: | ---: | ---: |
| 1 | 0 | 17,521 |
| 2 | 0 | 5,065 |
| 3 | 0 | 1,738 |
| 4 | 0 | 714 |
| 5 | 102 | 254 |
| 6 | 90 | 0 |
| 7 | 56 | 0 |
| 8 | 93 | 0 |
| 9 | 1,229 | 0 |
| 25 | 448 | 0 |
| 57 | 224 | 0 |

The local mixed saving root lies strictly between

```
0.002311660492818048695136925339
0.002311660492818048695136925340.
```

This is an improvement to the local word. An integer-multiplication
claim requires the separate weak-separation compiler and outer transfer.
The original strict-separation theorem cannot be invoked directly,
because the new maximum paid rank and minimum target rank both equal 5.

## Literal change to the native word

The predecessor is #4359 at commit
`da637c87c89482bc4c86be36bd0071b3d400dbed`. The exact source is
`research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz`, with its
source-bound generator `p3_native_cover.py` and independent native audit.

For every fresh helper, the original generator sets
`target=max(6,width)`. It embeds the helper's native output on its first
`width` canonical axes. It then emits standalone paid residual calls on
the remaining axes up to `target`. For native width five, that is exactly
one rank-one call on the sixth canonical axis.

The derivative program has this finite specification:

1. Start with the complete pinned native p3 word, including all its
   whole-call helper normalizers and its full main-field boundary maps.
2. Delete exactly the 102 residual records listed in `CERTIFICATE.json`.
3. Change only those 102 fresh-field endpoint promises from rank six to
   rank five.

`rewrite_cover` in `verify.py` constructs this exact change. It leaves
every other residual in its original order. It also preserves every
helper binding, coordinate map, idle owner, and owned-storage entry.

The removed calls have the following distribution:

| Stage | Removed rank-one topups |
| ---: | ---: |
| 0 | 9 |
| 1 | 28 |
| 3 | 28 |
| 5 | 9 |
| 6 | 28 |
| Total | 102 |

Each native local word has 28 width-five helper roles. Some of those
roles are hosted in idle main fields; others are fresh. The count for
one local word therefore does not give the count for all seven stages.
The 102 count comes from the complete native ownership artifact.

## Why the changed endpoints are correct

Fix one of the listed fresh fields `Gstage:role`. The source-bound native
helper certificate gives an autonomous completed rank-five endpoint for
that field's arbitrary input. Its physical binding is on the five axes
`[1,2,4,8,16]`. Its complete 57-dimensional embedding and inverse are
identity coordinate maps.

The existing whole-call normalizers give the canonical positive rank-five
job. They retain their actual direction, scalar phase, and native role.
The original additional rank-one call acts on axis `[32]` after that
stage. This sixth axis is disjoint from the helper's five output axes.
Thus the original endpoint is the product of the completed five-axis job
and one independent sixth-axis job. Deleting the second factor leaves
the canonical five-axis job and identity on all remaining axes.

The field has exactly one global helper binding, and its only external
residual call is this topup. It owns no main idle window. Its owner name
identifies a fresh arbitrary input field, not the copied center or any
main field. No later controller stage or other outer residual consumes
the extra sixth-axis result. Deletion therefore has no downstream
effect on another field. Internal uses inside the one local call are
already covered by the unchanged autonomous native endpoint identity.

This is an operator argument for arbitrary input and spectator contents.
It does not assume zeros in the fresh field or its spectator axes.
Column lifting preserves the same split into five coordinate blocks and
one independent sixth block, so the argument holds at every positive
column multiplicity admitted by the original native word.

The main fields, their physical frames, copied-center calls, and owned
center initialization and erasure are unchanged. The prior conservative
scalar allowance of 1,147,304 real primitives remains valid. No scalar,
route, or cleanup operation receives an additional discount.

## Exact invoice and moment improvement

The source has 192 rank-six productive fields. Exactly 102 have native
width five; the other 90 have native width six. Removing the listed calls
therefore changes the source invoice by

```
targets[5] += 102
targets[6] -= 102
paid[1]   -= 102.
```

There are still 2,242 productive fields and one uncredited owned center.
The rank surplus remains 224, since both productive and paid rank totals
fall by 102.

The omitted sixth axes still need completion when this mixed unit is
turned into a full-rank supplier. At ambient rank 57, the exact bill is:

| Rank-one base bill | Original | Width-five version |
| --- | ---: | ---: |
| Productive target rank mass | 37,317 | 37,215 |
| Paid rank mass | 37,093 | 36,991 |
| Source complement rank mass | 90,477 | 90,579 |
| Total full-completion leaves | 127,570 | 127,570 |

Thus the 102 deleted topups reappear as 102 extra complementary axes at
depth zero. The verifier checks this equality. A single full rank-57
completion receives no free saving. The improvement arises from the
strictly concave mixed moment and the subsequent integer hierarchy,
whose source complements must remain fully charged.

At a saving `C` with `0<C<1`, write `t=1-C`. The new target-minus-paid
moment exceeds the old moment by exactly

```
102 * (1 + 5^t - 6^t) > 0.
```

The inequality follows from strict concavity: `6^t-5^t<1^t-0^t=1`.
The improvement therefore does not rely on rounding a numerical root.
The accompanying directed-rational computation encloses the new root,
and separately verifies a positive complete moment at `C=0.00231166`.

The new root is unique. Every paid rank is at most 5 and every target
rank is at least 5. Positive paid mass has rank below 5, so the
logarithmic derivative of the paid-to-target moment ratio is strictly
negative as a function of `t`. At `t=0` that ratio exceeds one, and at
`t=1` it is below one because the rank surplus is positive.

## Verification and remaining obligations

Run the deterministic check from this project:

```sh
python3 -B research/kappa-4359-native-five/verify.py --source-root /path/to/pr4359 --check
```

Use `--out /tmp/native-five.json` to emit a fresh certificate. The source
root defaults to the project root when the pending predecessor is
present. The verifier checks immutable source hashes before reading the
native artifact, and authenticates every source listed by that artifact.
It binds the actual helper boundary records, exact axes, chronological
owners, copied-center exclusion, retained scalar allowance, and complete
invoice. Negative controls reject an unearned rank-six endpoint, an
unpaid rank-five call, and duplicate deletion credit.

The verifier reuses the independently reviewed rational interval engine
from `kappa-4359-outer-endpoint/verify.py` after authenticating that source.
It does not import or change the original native generator.

The weak-separation extension must supply finite, acyclic integer batching
when paid and target ranks can both equal 5. It must also control the
weighted exit tail; the prior worst-exit contraction estimate does not
apply with equal extreme ranks. A multiplication bound further needs
the resulting finite uniform template, its replacement constants, and
the inherited BIT, native movement, analytic, and tape hypotheses.

The finite certificates are not a formal verification of all those
operator and analytic premises. This package makes no standalone kappa
claim.

## Open next questions

The previous owner packing was chosen with a minimum target rank of six.
Once width-five targets are admitted, the complete idle-owner packing
can be optimized again using the changed moment. A useful next search
keeps paid ranks at most five and reconstructs its exact integral owner
assignment before comparing roots. That search must preserve the same
chronology and every native endpoint, movement, and cleanup cost.

The coefficient bound in the weak exit-tail argument may also permit a
smaller fixed template. Such a reduction changes the finite constants;
it does not by itself change the local mixed root.

Apache-2.0 for the new material. The unchanged native controller and
source notices retain the predecessor attribution in PR #4359.
