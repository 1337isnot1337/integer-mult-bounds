# PR4633: endpoint failures and attempted repairs

**The submitted quotient does not support a new kappa.** This audit covers
PR4633 head `b390d64abfcdba1a3816b86fc763cbc95d43c12c`, including its latest
three-dimensional BIT kernel. The two original packages remain unchanged.
[RESULT.json](RESULT.json) records `supported_new_kappa: null`; its passing
status means the counterexamples pass.

## Findings

1. **The BIT builder changes the scalar field of the frame geometry.** PR589
   stores rational E8 subspaces with form `<x,y>/2`. Reducing annihilator entries
   modulo two preserves individual dimensions but identifies distinct subspaces:
   636 source frames become 157 binary spaces before any quotient. More
   decisively, 103 of 111 source ports lose the complementary entrance-line and
   terminal-hyperplane split under this binary reinterpretation alone. All 111
   original rational ports pass the corresponding exact checks.
2. **The submitted BIT map has no rational linear lift.** Its three-dimensional
   kernel erases 41 rational entrance lines spanning all eight dimensions.
   Ports `[8,9,10,11,46,47,59,60]` give an exact independent witness. A rational
   linear map annihilating those lines would be zero, so it cannot be the claimed
   rank-five quotient. Already the two source lines at ports 8 and 9,
   `(0,1,1,0,1,0,0,1)` and `(0,1,1,0,1,0,0,-1)`, are independent over Q but are
   identified by the binary reduction.
3. **The invoice credits operators absent from the endpoints.** The controller
   requires a central entrance line P, a terminal hyperplane H with
   `P direct-sum H = ambient`, and equal stage widths on both mains. Logical
   replay checks its own declared final frames instead of this caller contract.
   Neither submitted supplier has a valid port at its invoiced block size.
4. **BIT replay trusts the emitted MOVE charge.** Setting every stored MOVE
   charge to zero leaves the full author verifier passing and reporting kappa
   `0.25`, its search ceiling. Comparing charges with the actual endpoint
   dimension differences independently detects 2,184 mismatches. The committed
   artifact's original MOVE charges do match its own dimensions; this mutation
   demonstrates the missing check rather than a false charge in that artifact.

The exact endpoint table follows. Each tuple is
`(X entrance dim, X final dim, Y entrance dim, Y final dim)`.

| Word | Required | Actual dimensions and counts |
| --- | --- | --- |
| Rational BIT source | (1,8,0,7) | (1,8,0,7): 111, all complementary |
| Submitted BIT | (1,8,0,7) | (0,8,0,4): 41; (1,8,0,4): 62; (1,8,0,8): 8 |
| Complex source | (1,9,0,8) | (1,9,0,8): 112, all complementary |
| Submitted complex | (1,9,0,8) | (1,8,0,7): 56; (1,8,0,8): 56 |

## Repair checks

Re-padding helpers restores helper dimensions, but does not restore the main
operators. The submitted BIT mains have total width 1,294 instead of 1,554.
Their lost 260 ranks, plus 27 ranks removed from the nine COPY-related episodes,
explain **all** of the 287-rank local paid reduction:

```
source:   paid 5129 - helper 3512 - main 1554 = 63 = 9*7
quotient: paid 4842 - helper 3512 - main 1294 = 36 = 9*4
surplus gain = 18 * (260 + 27) = 5919 - 753 = 5166
```

Restoring those required rank contributions removes the entire rank-surplus
increase. This identity alone does not prove equality of moment profiles for
every possible different implementation. Restoring the original source word
restores its original BIT screen value `0.003464248972023964`.

I also tested pricing the smaller block implied by the quotient width, retaining
the submitted local paid/helper invoices. BIT block 4 has surplus `-6069`;
complex block 7 has surplus `-256`. Neither has a passing point in the author's
screen search on `[1e-7,0.25]`. These remain diagnostic invoices, not valid
repaired suppliers: the BIT has varying central ranks, and only 56 of 112 complex
ports satisfy the block-7 split. The other 56 have the X entrance contained in
the Y terminal and central rank zero.

An exact obstruction also rules out choosing a different global quotient while
preserving every source port. Suppose `V = P direct-sum H`, `dim P = 1`, and a
quotient with kernel K preserves a nonzero image P complementary to image H.
Dimension counting forces `K subset H`:

```
codim(image H) = 1 - dim K + dim(K intersect H) = 1.
```

For all ports this requires `K subset intersection_p H_p`. The BIT terminal
normals have rational rank 8 and the complex terminal normals have binary rank
9, so both intersections are zero. A nontrivial global quotient cannot preserve
all these splits. This excludes that source-compatible quotient repair. It does
not exclude a new caller, a different port set, independently constructed frames,
or a fully priced non-quotient circuit. Helper re-padding changes the proposed
map, and must separately satisfy the endpoint checks; the submitted versions do
not.

## Verification and scope

Both author verifiers were run under CPython 3.12.15 and reproduced their claimed
screens. This audit checks exact dimensions and annihilator/basis agreement for
all 636 rational BIT frames, both source contracts, both quotient contracts,
both BIT replay directions, the full-verifier undercharge mutation, independent
MOVE ranks, lost-work identities and repaired-block invoices. Endpoint and rank
counterexamples use exact integer/rational arithmetic. Screen roots and sampled
screen searches retain the author's floating arithmetic.

The selected record at live main `fbc9ea0249746acca4f504d4fda2b84e0e36cf0d`
was `0.00302015` when checked. The PR's older selected-record provenance remains
pinned as history. This audit changes neither the selected result nor admission
constants, and proves no multiplication theorem.

From repository root:

```sh
python3.12 scripts/research_package.py --package research/pr4633-kappa-repair-audit
python3.12 -I -O -B research/pr4633-kappa-repair-audit/verify.py
```

All declared sources are bound by Git blob and SHA-256 in
[SOURCES.json](SOURCES.json). The registered replay also checks those pins.

## Open next questions

A replacement must first specify valid complementary per-port endpoints and
implement them in the source's actual scalar field. Only then can a changed
consumer or port selection be priced, including central transports, endpoint
conversion and admission. The first useful test is an independent per-port
operator check against the caller, followed by a complete paid invoice. No such
replacement is supplied here. Changing admission literals cannot repair the
current endpoint failure.

## Credit

Prepared by Cinna Davis with substantial OpenAI Codex assistance, Apache-2.0.
Credit DaysSky for PR4633 and its experiments; pinterbanget/PR4604 for the
endpoint-frame question; petalas/PR4627 for the kernel census; and Rohan Arun's
[per-port audit](https://github.com/CrocSwap/integer-mult-bounds/pull/4633#issuecomment-6341849407).
Retain PR589's E8 contributors and the complete PR4470/native/helper-boundary
lineage in the pinned predecessor packages. This latest-head audit adds the
three-dimensional rational rank-eight counterexample, exact lost-work accounting,
the independent MOVE-rank control and the scoped quotient obstruction.
