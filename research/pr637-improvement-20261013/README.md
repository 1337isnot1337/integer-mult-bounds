# Owner improvement over PR637

Conditional **κ = 0.001636456810414854**, exceeding pinned
[PR637](https://github.com/CrocSwap/integer-mult-bounds/pull/637)
by **0.000000008347117783**.

Twenty literal owner rows change. Two neutral swaps and a whole-group transfer
combine idle ranks 4 and 32 into 1 and 35. The native supplier words, dispatch,
and admission code are inherited unchanged from PR637. The complete portable
witness is in [witness637/](witness637/README.md); the
[packing supplement](../kappa-packing-pr637-20261013/README.md) reconstructs the
assignment from pinned PR637 data.

Before publication, exact binding, physical owner admission and its 23 controls,
the finite invoice, both moment engines, a separate rational native/owner/moment
checker, and five independent corruption controls passed. A full fresh replay
of the pinned PR637 baseline passed all 64 stages, with no reuse.

**Publication status:** the new witness's full fresh replay is pending. The
[validation directory](validation/) contains the completed prepublication checks;
its final receipt will be added when the fresh replay finishes.

```sh
PYTHON=python3 sh research/pr637-improvement-20261013/witness637/verify.sh /tmp/pr637-improved-fresh
```

Use Python 3.10+, a C++ compiler, Boost headers, and a new output directory.
The inherited compiler, all-size, realization, analytic-transfer and bit H1–H5
assumptions remain. This is a conditional research bound. It does not attain the
relaxed fixed-dispatch packing ceiling, which would require idle ranks 36 and
2229 copies of 48.

Prepared by Chi Zhao with substantial OpenAI Codex assistance. Upstream
construction and contributor credits are preserved in the witness.
