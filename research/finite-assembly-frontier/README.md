# Finite assembly up to the supplied-cap ceiling

This package proves a constructive parameter theorem for the retained balanced
outer assembly. Let c be an admitted rational bit cap, b an admitted rational
complex cap, a0 = 384599/10^10, and u = min(b,c). Assume:

- a0 < u and b < 1/32;
- an admitted finite coefficient charge C <= 2^B for a positive integer B;
- the inherited weighted bootstrap, retained bridge bounds, and supplier
  compiler, common-grid, restored-work, precision and analytic interfaces.

Under these premises, it constructs a finite witness for every rational target

    0 < kappa < min(b,c)/(1+min(b,c)).

It selects strictly positive backoffs, a finite number of bootstrap levels,
and explicit integer cutoffs, then checks all 47 inequalities with the unchanged
balanced outer engine. It also finds the greatest admissible point on any
specified rational grid. The ceiling is relative to these caps and this
assembly family, and is never claimed as an attained endpoint. The bootstrap
starts at the fixed a0 above; selecting other caps does not change that premise.
See [PROOF.md](PROOF.md) for the finite construction and strict-ceiling argument.

## Focused review boundary

This directory is self-contained for its default offline verification. It can
be reviewed independently of the earlier E8 packages in PR275.

| Review question | Source and evidence |
| --- | --- |
| Why does every permitted target have a finite witness? | [PROOF.md](PROOF.md), including termination, positive backoffs and all 47 strict inequalities. |
| Does the constructor implement that theorem? | [assembly.py](assembly.py) and the unchanged [vendor/outer.py](vendor/outer.py). `BRIDGE` retains the literal and row bounds; `--coefficient-bits` supplies a charge, not an admission. |
| Where do the worked example's caps and finite charge come from? | [evidence.py](evidence.py), [SOURCES.json](SOURCES.json), and the source-bound receipts and complete invoice under `inputs/`. |
| What can be reproduced offline? | [verify.py](verify.py), the five behavioral contracts in [test_assembly.py](test_assembly.py), and [MANIFEST.json](MANIFEST.json). |

Retain all 50 manifested files plus `MANIFEST.json`, including source notices,
licenses, original receipts and logs. The mathematical core is small; the full
evidence closure is needed to substantiate the historical supplier example.

## Historical worked example

The worked example uses [PR433](https://github.com/CrocSwap/integer-mult-bounds/pull/433)
at `6d9244518175caf9e0089f92486959bc2c317273`. Its published value is
0.001120864952258278. On a 10^-27 grid this method gives

    kappa = 280216238064569651155257 / 250000000000000000000000000
          = 0.001120864952258278604621028.

This historical value is not a claim to the current numerical frontier. The
gain over its pinned baseline is only about 6.04621e-19. The reusable parameter
theorem and verifier are the contribution; no practical speedup or new supplier
construction is claimed. Nine finite bootstrap levels suffice. No infinite iteration or zero
parameter is used, and all inherited conditional interfaces remain premises.

## Verification

Run the offline standard-library verification, with assertions enabled:

```sh
python3 -B research/finite-assembly-frontier/verify.py
```

Add `--output /absolute/path/to/new-result.json` to retain all exact parameters,
cutoffs, moment intervals and strict margins. To select parameters for other
already admitted caps, use `assembly.py --bit C --complex B --grid 1/10...`
with rational numbers such as `1/1000`; alternatively supply `--target K`.
The CLI does not admit supplier claims by itself. In particular, the default
512-bit coefficient charge is established for the retained example; it must
be justified or replaced with an admitted charge for another supplier.

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

## Applying the theorem to different caps

A different supplier needs its own source-bound cap admission, complete finite
invoice, and an explicit match to the bootstrap and `BRIDGE` premises above.
Changing the CLI inputs or reusing the PR433 receipts does not establish those
facts. The relative ceiling theorem continues to require all its premises.

Recurrence pricing is part of that admission. The historical
`evidence.py::moment_pair` includes the inherited bad-residue surcharge for both
suppliers. [PR559](https://github.com/CrocSwap/integer-mult-bounds/pull/559) uses
a native complex moment without that surcharge while retaining it for the bit
supplier. Its caps therefore need an appropriate admission adapter before they
can replace this package's historical inputs. This distinction concerns cap
admission; it does not change the abstract supplied-cap theorem proved here.

The suppliers' compiler, compressed-window, arbitrary dirty-bank, restored-work,
fixed-tape/common-grid, precision and analytic interfaces remain assumptions.
This package does not establish an unconditional multiplication theorem or a
Lean proof. Attribution is in NOTICE.md and the preserved source notices.
