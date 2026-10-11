# Finite assembly up to the supplied-cap ceiling

For admitted rational caps c (bit) and b (complex), this package constructs a
finite witness for every rational target

    0 < kappa < min(b,c)/(1+min(b,c)).

It selects strictly positive backoffs, a finite number of bootstrap levels,
and explicit integer cutoffs, then checks all 47 inequalities with the unchanged
balanced outer engine. It also finds the greatest admissible point on any
specified rational grid. The ceiling is relative to these caps and this
assembly family, and is never claimed as an attained endpoint. See PROOF.md.

The worked example uses [PR433](https://github.com/CrocSwap/integer-mult-bounds/pull/433)
at `6d9244518175caf9e0089f92486959bc2c317273`. Its published value is
0.001120864952258278. On a 10^-27 grid this method gives

    kappa = 280216238064569651155257 / 250000000000000000000000000
          = 0.001120864952258278604621028.

The gain is only about 6.04621e-19. The reusable parameter theorem and verifier
are the contribution; no practical speedup or new supplier construction is
claimed. Nine finite bootstrap levels suffice. No infinite iteration or zero
parameter is used, and all inherited conditional interfaces remain premises.

Run the offline standard-library verification, with assertions enabled:

```sh
python3 -B research/finite-assembly-frontier/verify.py
```

Add `--output /absolute/path/to/new-result.json` to retain all exact parameters,
cutoffs, moment intervals and strict margins. To select parameters for other
already admitted caps, use `assembly.py --bit C --complex B --grid 1/10...`
with rational numbers such as `1/1000`; alternatively supply `--target K`.
The CLI does not admit supplier claims by itself.

The default verifier checks complete package closure, public source hashes,
24 retained receipts/logs from one successful 13-stage supplier replay, receipt
cross-references, and the finite invoice. It recomputes both supplier moments
and the selected seed with both rational engines, reproduces the published
assembly, and checks grid maximality and invalid-parameter rejection.

For a new supplier replay, obtain the pinned PR433 package from
[its immutable tree](https://github.com/icekylinx/integer-mult-bounds/tree/6d9244518175caf9e0089f92486959bc2c317273/research/split-centres-global)
and run its `python3 -B verify.py /absolute/path/to/new/output` command.
`inputs/supplier-MANIFEST.json` and `supplier-SOURCE-BINDING.json` identify the
exact inputs. Our default verification reuses retained supplier evidence;
it does not repeat the word, geometry or phase computations.

The suppliers' compiler, compressed-window, arbitrary dirty-bank, restored-work,
fixed-tape/common-grid, precision and analytic interfaces remain assumptions.
This package does not establish an unconditional multiplication theorem or a
Lean proof. Attribution is in NOTICE.md and the preserved source notices.
