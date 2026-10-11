# Exact width-73 bank optimizer

This package replaces a floating packing search with a deterministic integer construction for residual ranks `{4,5,7,8,9}`. It returns bank patterns in the existing emitter's format, proves when the packing attains the exact cost lower bound, and computes the minimum replica count. The proof includes the paid rank-one fallback term for every exponent `0 < b < 1`.

For the published PR404, PR409 and PR410 inventories, it constructs optimal banks directly. It does not claim a new multiplication bound. Its contribution is an exact optimizer and a necessary-and-sufficient feasibility theorem for this bank subproblem. This closes the packing search for these fixed inventories while leaving entrance and local-program optimization open.

## Use

Python 3.11+ and its standard library are sufficient. No installation, compiler, solver, network access or floating arithmetic is needed.

```sh
python3 -B research/e8-exact-bank-optimizer/verify.py
python3 -B research/e8-exact-bank-optimizer/bank_optimizer.py \
  research/e8-exact-bank-optimizer/inputs/example-inventory.json \
  --replica-multiple 8 --output /path/to/new-patterns.json
```

The example uses PR410's inventory and produces 1,471 banks with 743 rank-one pads at 16 replicas. The output file must be new. `--replicas N` selects a specific admissible replication; otherwise the optimizer selects the minimum. `--replica-multiple 8` preserves the replication requirement of the existing E8 expander. Omitting it computes the unrestricted packing minimum, which alone does not validate an architecture.

The library API is `construct(inventory, replicas=None, replica_multiple=1)`, returning `(patterns, certificate)`. `check(patterns, expanded_inventory)` independently counts the witness's items, ranks, padding and equality conditions. Unsupported ranks or invalid counts are rejected. `NoSaturatingPacking` means no replication can reach this particular lower bound; it does not say that all other packing is impossible.

## Result

Writing `K = sum n_r` and `W = sum (r-1)n_r`, an equality packing exists precisely when

```
W % 64 == 0
9*W/64 - K >= 0
n_8 >= n_4
n_8 + 2*n_7 >= 3*n_4
```

It uses `W/64` banks and `9*W/64-K` rank-one pads. When the three scale-invariant inequalities hold, the minimum replication is `64/gcd(W,64)`. The proof and constructive grouping argument are in [PROOF.md](PROOF.md).

| Inventory | Packing minimum | Minimum with architecture multiple 8 | Banks at architecture minimum | Rank-one pads |
|---|---:|---:|---:|---:|
| PR404 | 4 | 8 | 738 | 394 |
| PR409 | 32 | 32 | 2,947 | 1,531 |
| PR410 | 16 | 16 | 1,471 | 743 |

The algorithm operates on a bounded number of compressed pattern counts. It does not loop over every item or replicate. Its integer bit complexity depends on input bit lengths.

## Verification and scope

The tests compare the feasibility decision and every successful witness with an independent exhaustive pattern-reachability oracle over 16,875 small inventories. They also check the pinned published witnesses, two enlarged research inventories, architecture constraints, certificate mutations, unsupported inputs and multiplicities above `10^40`.

The bank theorem optimizes the full moment numerator for a fixed local ledger and residual inventory, including fallback. It therefore optimizes the admissible coarse root within that bank model. It does not establish the all-size multiplication interfaces, local phase correctness, owner routing, a finite compiler invoice, or a new outer κ. Changing a witness in a supplier still requires that supplier's complete admission.

Source inventories, immutable revisions and attribution are recorded in [SOURCES.json](SOURCES.json) and [NOTICE.md](NOTICE.md). Prepared for George Lydakis with substantial OpenAI Codex and Ody assistance.
