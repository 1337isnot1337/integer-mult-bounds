# Thirty-seven replicas on the U8 word

The retained conditional framework admits

```
kappa = 1661960547713947 / 10^18 = 0.001661960547713947
```

This is **2.773066918e-9 above PR890** (0.001661957774647029). The U8 local
word, its 504 helper widths, the PR589 bit supplier, both moment engines and the
outer recipe are unchanged. The owner map has **37 replicas, 333 complete calls
and 167,832 whole-helper roles**; its idle profile is `{48:11086, 1:6}`.

## Idea

PR890 proves that no replica count `T <= 22` or whole-owner placement improves
T21 for this word. The cap `T <= 22` comes only from the charged 512-bit global
prefix payload (`113+18T < 512`). That payload is a finite constant paid in the
invoice's row reserve (`2*payload`), the prefix reserve and the bootstrap
cutoffs; the moments and the 47 outer inequalities do not see it. This package
charges **1024 bits** (row coefficient `17495 < 20161`, prefix `779 < 1024`).

Rerunning PR890's own signed-price relaxation without the cap shows that
`{48:11086, 1:6}` at T37 attains the dual with equality and is the best
normalized profile for every replica count. It is constructed as PR890's T21
plus a second PR858 T16 (replicas 21..36), merged proportionally, plus an
eight-role credit-neutral trade `(44,3,2) -> (48,1)`. See [PROOF.md](PROOF.md).

## Reproduce

From the repository root, with Python 3.11+ and the existing frontier replay's
NumPy/SymPy/SciPy, C++17 and Boost dependencies (set `CPATH` to the Boost
include directory if needed):

```sh
python -B research/complex-t37-owners/verify.py --work /tmp/t37-cold
```

It rebuilds PR589, PR741 and PR799, rebuilds U8 and its controls, constructs
T37 (rerunning PR890's T21 and PR858's T16 constructors and audits), lifts the
8+8+8+8+5 bank envelope and audits it with eight mutations, runs PR890's
unchanged independent checker on the T21 component and the T37-parameterized
checker on all roles, rejects all eight omitted edits and the sequential
schedule, then runs bind, emit, asynchronous audit (15 mutations), invoice,
assembly, 69 admission and 12 bit-supplier controls and two exact moment
engines with all 47 outer inequalities. No optimizer runs. Reuse of a verified
PR799 replay works as in PR890 (`--baseline799 DIR --ancestor741 DIR/ancestor`).

`freeze.py` is the discovery path used once to write `data/SPEC.json`; it is not
a verification premise.

## Scope

Finite conditional witness. All-size compilation, common-label and
mutable-source realization, whole-call hosting, precision/tape, analytic
transfer and bit H1-H5 remain inherited hypotheses. The explicit new premise is
the 1024-bit charged prefix payload, priced through the reserves above. Not an
unconditional multiplication theorem or an optimality claim beyond the
relaxation stated in PROOF.md.
