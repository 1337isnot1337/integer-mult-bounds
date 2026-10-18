# The two-hub literal actual-reader tariff minimum is exactly 54

PR3583 proved that the two-hub `K3,2` marked support-transfer certificate has
no characteristic-two realization, built one exact rational literal
factorization for it, measured nine rectangular complete-plane charges
totalling **54** against a baseline of **42**, and wrote:

> Neither the bill nor this construction is claimed optimal.

This package closes that question. It computes the exact minimum of the same
literal actual-reader row model and finds

```text
row units      27   (21 rows, six of them forced to two units)
minimum charge 54
baseline       42   unattainable
forced excess  12
```

The retained PR3583 witness attains 54, so **the retained witness is already
optimal** and **no literal actual-reader factorization of this certificate can
do better**. The twelve-unit excess is forced by the six reader rows
`dxy`, `dzw`, `gtxy` for each mark, whose premise sets force the mark to be
carried by two mark-bearing queries at once.

This is an exact finite optimum for one fixed row model over one fixed
certificate. It is **not** a graph classification, not a literal tariff for the
wider coverage identity, not a physical or supplier cost, and **not** a kappa
or selected-frontier statement. It does not lift the 42-port factorization to
other graphs and it does not revisit the characteristic-two impossibility,
which is a statement about a different object.

[PROOF.md](PROOF.md) gives the model, the two-step lower bound and the
attainment. [RESULT.json](RESULT.json) holds the per-row minima, the attaining
reader support and evaluator kill set for every row, and the nine measured
charges. [ORIGINS.json](ORIGINS.json) pins the three retained PR3583 files by
origin commit, path, Git blob and SHA256.

## Evidence

- **Before:** the only known charge for this certificate was the measured 54 of
  one witness, explicitly not claimed optimal.
  **After:** two independently written exact searches both return 27 row units
  and 54 as the minimum, and the retained witness attains it.
- `verify.py` searches the whole row model by exact rational linear
  feasibility: for every row it enumerates every admissible reader support and,
  for each, the largest set of its queries that one admissible evaluator can
  simultaneously kill. It replays the twenty-one premises themselves, checks
  the retained witness row by row, and checks all 1,764 entries of
  `a a^T + b b^T = sum_i u_i q_i^T` over the 42 ports.
- `independent.py` shares no code and uses only integers and fraction-free
  elimination. It obtains the seven source-row minima from the universal bound
  `phi_p(mark(p)) = 1 = sum_i u_i^(p) phi_p(Q_i)` and recomputes all fourteen
  reader-row minima from an explicit span table. It also recomputes the nine
  plane charges from the retained witness bytes.
- The search in `verify.py` is conservative in the safe direction: it relaxes a
  reader-row evaluator to *every* functional with `phi(mark) = 1` and
  `phi(other mark) = 0`, which is a strict superset of the admissible set, and
  relaxes a source-row reader from PR3583's default `ghx`/`ghy` to all seven
  reader premise sets of that mark. Both relaxations can only lower the
  searched minimum, and the relaxed search still returns 54.
- Ten actual mutation groups are rejected by both programs: two altered query
  rows, swapped marks, a dropped premise, a broken evaluator, a broken reader,
  altered retained predecessor bytes, an understated minimum, a hidden extra
  row unit, and inflated witness charges. Twenty rejecting runs plus three
  positive runs pass, and the receipt bytes are unchanged across them.

## A correction recorded against the retained predecessor

PR3583's `PROOF.md` says "There are twelve E rows and nine F rows" and
"partitioned into binary Gram-I groups of sizes 24 and 18". Its own retained
`WITNESS.json` has **eleven** mark-`E` rows (four source plus seven reader) and
**ten** mark-`F` rows (three source plus seven reader), so the 24/18 split is
not a description of that witness.

This does not change any mathematical claim. The port total of 42 follows from
21 rows times two, all nine charges are reproduced from the retained bytes,
and the 1764-entry identity check passes. The predecessor text is retained
verbatim and is **not** edited; the discrepancy is recorded in
[ORIGINS.json](ORIGINS.json) instead, for the PR3583 author to resolve in the
source package.

## Reproduction

CPython 3.12 and the standard library suffice, from the repository root:

```sh
python3.12 -W error -B scripts/research_package.py \
  --package research/p112-two-hub-tariff-minimum
```

The direct scientific commands need no Git object, no network and no pending
branch:

```sh
python3.12 -W error -B research/p112-two-hub-tariff-minimum/verify.py
python3.12 -W error -B research/p112-two-hub-tariff-minimum/independent.py
python3.12 -O -W error -B research/p112-two-hub-tariff-minimum/test_controls.py
```

Set `TMPDIR` to a private external run directory for the disposable control
copies. Controls copy the package into owned regular byte copies, never change
modes, and never touch source files, runtimes or frozen inputs. Production
checks stay enabled under `-O`.

### Environment actually used for this package

CPython 3.12 is **not installed in the machine that produced this package**, so
the registered replay command above was **not** run here. What was actually
run, on CPython 3.15.0:

```text
python3 -W error -B scripts/research_package.py \
  --package research/p112-two-hub-tariff-minimum --check-only
  -> PASS_PACKAGE_METADATA_AND_PINS (not a mathematical acceptance check)

python3 -W error -B research/p112-two-hub-tariff-minimum/verify.py
  -> PASS_TWO_HUB_TARIFF_MINIMUM
python3 -W error -B research/p112-two-hub-tariff-minimum/independent.py
  -> PASS_TWO_HUB_TARIFF_MINIMUM_INDEPENDENT
python3 -W error -B research/p112-two-hub-tariff-minimum/test_controls.py
  -> PASS_TWO_HUB_TARIFF_MINIMUM_CONTROLS
```

Measured wall times for the three scientific commands on that interpreter:
0.06 s, 0.02 s and 1.14 s. The structural metadata and pin validation passes;
the full `scripts/research_package.py` replay under CPython 3.12, Ruff
lint/format, `scripts/check_research_commit.py --check-source-history`, the
selected cold replay, Lean and Docker are **all unrun** and are listed as open
obligations. No `CHECKS.json` receipt is claimed, because the receipt generator
is the 3.12 replay that did not run.

## Limitations

- Author-written. Independent human review and formal proof-kernel review are
  unclaimed.
- The optimum is over one fixed row model: PR3583's twenty-one premises,
  rational evaluators, and reader supports equal to an admissible reader
  premise. A different literal tariff, a different Gram label, or a
  characteristic-two target is a different model and is not covered.
- The bound is about this certificate only. It is not the 42-port literal
  factorization floor for other graphs, and it is not a universal pair floor.
- Acquisition, coefficient execution, dirty restoration, frames, hosting,
  precision, stock, compiler and all-size admission, complete consumers, both
  supplier invoices and the multiplication theorem are all unrun here.
- The selected cold replay, Lean and Docker are unrun.

## Open next questions

- Is the forced excess of twelve specific to the `K3,2` placement, or does a
  third independent hub force the same two-unit pattern on more reader rows?
  A rooted-minor transfer of the current argument would settle it.
- Does the same two-bearing-query mechanism show up in a literal
  actual-reader factorization of a *single*-hub certificate, where PR3573
  still has a working exceptional transfer? That is the cheapest place to look
  for a construction that genuinely beats 54 rather than matching it.
- Can a tariff model that is not row-local charge these six rows differently,
  and does the answer move any actual coverage identity? Any such model needs
  its own fully charged derivation; it cannot be read off this one.