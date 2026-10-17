# Class-C 4-flat covering-config census: an independent table audit (no kappa claim)

**Status:** author-checked, not independently reviewed. **Priority revision 6.**
Base canonical main `463113d675af7410ac91d53a4fed51ec6494eb9a`.

This package audits the *published tables* of the class-C help package for
Discussion #2954. It does **not** re-derive any E8/P112 geometry, does **not**
verify the kill criterion (Lemma B), and does **not** verify relative root
counting (RRC), which that help post itself marks as under audit. No kappa,
decoder floor, residue exclusion, supplier or frontier claim is made here.

## What this establishes

### First: the cover relation is dominance closure, not literal CSV incidence

This was **not** obvious from the CSV and is the load-bearing correction in
this package. #2954 publishes per-config totals -- "6554 covers 62 of the 70
rows, 5555 27, 6544 40, 5554 23, 6543 16" -- and those five numbers are
reproduced **exactly** by *dominance closure* (a config may serve any row of a
config it dominates coordinatewise) and **not at all** by literal incidence:

| config | literal incidence | dominance closure | published in #2954 |
|---|---:|---:|---:|
| 6554 | 39 | **62** | 62 |
| 5555 | 21 | **27** | 27 |
| 6544 | 36 | **40** | 40 |
| 5554 | 22 | **23** | 23 |
| 6543 | 16 | **16** | 16 |

`6554 = (6,5,5,4)` dominates `5544`, `6444`, `6544` and `6543` coordinatewise, so
its true reach is 62 rows, not the 39 the CSV lists for it. Rows 13 and 62 list
`5544` but omit `6554`, which is consistent with the author listing only the
*minimal* generator of each cover rather than every config that can serve it.

An earlier version of this package read the relation as literal incidence. That
was wrong and overstated the required campaign; the correction is below.

### Two findings about *compute allocation*

**1. The advertised cheapest campaign is redundant by dominance, so it cannot
help.** #2954 prices five configs and singles out `(6,5,4,3)` = `6543` as by far
the cheapest: 2.6e7 pairs against 1.1e8-3.3e8 for the others, ETA about 4e4
CPU-h against about 3e5. It is the only target that looked plausibly
affordable, and it is where the route-B acceleration work (tekuuu's PR2975,
PR3000) was pointed.

But `6543 = (6,5,4,3)` is **dominated by `6554 = (6,5,5,4)`**, so everything it
can serve, `6554` can serve too. Independently of that, `6543` appears only on
rows that relative root counting already kills and covers none of the 17 rows in
`rows17.csv`. Either way it adds nothing, and ~4e4 CPU-h on it cannot advance
the hard problem.

**2. A two-config campaign suffices.** The exact minimum set of configs covering
the 16 config-coverable rows of the 17 is

```
{5555, 6554}
```

`5544`, `5554`, `6444` and `6544` are redundant, and the same two configs also
cover all 64 config-coverable rows of the whole 70-row census. For the full
table, 11 of the 13 configs are redundant -- only `5555` and `6554` survive.
`5555` survives because `6554` does not dominate it: `5555 = (5,5,5,5)` is
narrower than `6554` in its largest dimension.

Using only the README's own pair counts, dropping redundant `5554` (3.3e8) and
`6544` (1.1e8) removes **4.4e8 enumerated pairs** before any closure runs, and
also dropping `6543` (2.6e7) brings the full-census figure to **4.66e8**.
`5544` and `6444` have no published pair count, so both figures are **lower
bounds**.

**Supporting consistency checks, all passing.** These matter because the
redundancy claim rests on the table being well-formed:

* dominance closure reproduces all five published per-config totals, and
  literal incidence does not (table above);
* every listed config satisfies the `sum g <= 52` admissibility bound, and
  `6554` = `(6,5,5,4)` saturates it *exactly* at 52, so it is the unique
  largest admissible 4-flat budget in the table;
* `rows17.csv` is exactly `rows70.csv` minus the 53 `RRC-killed` rows
  (symmetric difference empty), and the kill count is the published 53;
* every shared row's `d`, `s`, `weights`, `e` and config list agrees between
  the two tables;
* independently, the 6 rows with no config at all are `3, 12, 24, 37, 54, 61`,
  confirming the post's "6 rows have no 4-flat candidate". Row 37 is the only
  one of the 17.

## What this does *not* establish

* **Completeness of the config list is not checked.** The audit verifies that
  each listed config is admissible (`sum g <= 52`), not that the packing
  predicate admits no further config. That predicate is only sketched in #2954,
  so the redundancy result is a statement about the published list.
* **The dominance relation is recovered from published totals, not proved from
  the geometry.** That `6554` can substitute for a dominated config in the
  actual span computation is a *source-semantic* premise, not something this
  table audit establishes. It is exactly the question taken up independently in
  the follow-up claim on #2954; treat the two-config campaign as the *planning*
  conclusion pending that lemma.
* The kill criterion, the span bound `span H <= d-1`, and RRC are untouched.
* Pair counts and CPU-hour ETAs are reused verbatim from the help README and
  were not re-measured.
* No row is excluded. A redundant *config* is not a disproved *row*; see the
  card's own `scope_change_trigger`.

## Reproduce

```sh
python3 -B research/k2-class-c-config-audit/verify.py
```

Python 3.12, standard library only, runs in under a second. Expect
`PASS_K2_CLASS_C_CONFIG_AUDIT` and exit 0. `RESULT.json` is written next to the
verifier with every derived quantity. The verifier asserts the sha256 of both
inputs, runs the 8 structural checks, and then runs **4 rejecting mutants** that
must each be caught:

| mutant | rejected by |
|---|---|
| inject inadmissible config `6555` (`sum g = 56`) | admissibility + cross-table agreement |
| drop row 62 from `rows17.csv` | row count + rows17-vs-rows70 identity |
| flip one RRC status (kill count 53 -> 52) | rows17 identity + kill count |
| edit row 35's configs in `rows17.csv` only | cross-table agreement |
| add `6554` to row 3 (dominance total 62 -> 63) | published-total reproduction |

## Sources and inputs

* Audited help package: `research/k2-class-c-help` on
  `DreamingOfClouds/integer-mult-bounds`, branch `research/k2-class-c-help`,
  help-package source commit `1b25759bff5486293a9083ebbe0097b5f6642e08`.
* `inputs/rows70.csv` sha256 `c0eb6bb88498bf39a8b2020b1d0d600181f6e13eb9dd6a6e5f90794f0895754a`
* `inputs/rows17.csv` sha256 `9ebe7fc1ecd74148e7bdefa1f6bb2ed00551884b1a4a6558d7f129f7eef4efd5`
* `g(1..7) = 1,2,4,8,12,20,36`, `sum g <= 52`, and the pair counts are quoted
  from Discussion #2954 and the same README, and restated in `verify.py`.

These two CSVs are **not Git objects in this repository**, so they cannot carry
a `git_blob`/`pin` row in `SOURCES.json`. They are vendored under `inputs/`,
declared as live inputs in `VERIFY.json`, and the verifier re-checks their
sha256 on every run as the byte-equality receipt.

## Overlap tooling limitation

`python3 scripts/find_overlap.py --task ... --refresh` could not refresh its
remote corpus in the session environment: its remote refresh shells out to
`gh`, which is not installed, so it reported `open_prs: null, discussions: null`
and fell back to local notes. The overlap check was instead done with
authenticated API reads of #2954, #1166 and #3156 and API searches across open
and closed PR bodies. This is **not** an arbitrary-diff or unpublished-work
census, and no match would not by itself have proved novelty.

## Open next questions

0. **Does the dominance substitution preserve the span threshold?** Every
   conclusion here assumes that if `6554` dominates a config then `6554` serves
   its rows at the same target `T`. That is a source-semantic premise this audit
   cannot prove; it is the one thing standing between this and a two-config
   campaign being *correct* rather than merely *plausible*. *First step:* fix a
   single `(V1..V4)` instance and a target `T`, and check both the dominated and
   dominating config against the real span computation. *Blocked by:* needs the
   E8/P112 geometry and `s4z`.
1. **Is the admissible config list complete?** *Why it matters:* completeness is
   what makes the redundancy a real saving; a missing config would enlarge the
   minimal cover. *First step:* obtain the exact weight-multiset-to-config
   packing predicate from the help author, regenerate the config sets
   independently and diff them against `inputs/rows70.csv`. *Blocked by:* the
   predicate is unpublished; `s4z.c` encodes it only implicitly.
2. **Rows 37, 3, 12, 24, 54, 61 admit no 4-flat config.** *Why it matters:* they
   are unreachable by every advertised config, so no amount of 4-flat closure
   compute closes them. *First step:* test whether a 5-flat or an explicit
   two-free-piece cover exists for row 37 within `sum g <= 52`, or prove none
   does. *Blocked by:* needs the E8/P112 flat geometry and the unpublished RRC
   scenario list.
3. **Do the 3 redundant configs matter for the wider residue chains?** *Why it
   matters:* the redundancy is proved only relative to these 70 rows, while
   PR2985/PR3049 reuse the same config vocabulary. *First step:* run this audit
   unchanged against their residue tables after pinning their heads. *Blocked
   by:* those tables are not vendored here and their heads are unpinned.

## Predecessor credit

* **DreamingOfClouds** - the class-C help package, the `s4z`/`s3z` engines, the
  `data88.txt` direction list, the `g`-table, the `sum g <= 52` bound and both
  CSV tables that are the entire object of this audit. Their results retain all
  credit; nothing here disputes them.
* **tekuuu** - PR2975 (33x requirement enumeration) and PR3000 (9.31x four-flat
  maximal-mask filtering). Those accelerate work *inside* a config; this
  removes whole configs from the campaign, and composes with them.
* **Nick Petalas** and the retained **#2816 / #2826 / #2862** E8/P112 lineage,
  and the RRC residue chain of **PR2985 / PR3049** that this census belongs to.
* **Douglas Colkitt**, the selected result and the retained source lineage.

Prepared by muatfannajm-dot, with substantial OpenCode (Space Bunny Free)
assistance. Apache-2.0. The audited help package remains DreamingOfClouds'
work under the repository's Apache-2.0 licence.