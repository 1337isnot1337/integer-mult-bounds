# PR #774 finite and formal coverage

The [review continuation](https://github.com/CrocSwap/integer-mult-bounds/pull/774#issuecomment-6160960125)
requests both finite and formal coverage of the constrained forest construction.
The reviewed construction is commit `50f8c366f27a9083e0655593a1be3d6810d1f053`,
whose complete diff from `66849e1475c930fd7732b1a0067ffee7e1e95f60` adds the
22 files below. This follow-up adds CI and documentation; the construction,
proof, source pins and frozen certificates are unchanged.

## Coverage of the submitted package

| Files | Obligation and evidence |
| --- | --- |
| `construct.py`, `data/word.json.gz`, `data/recipe.json`, `data/optimum.json.gz`, `data/optimum-recipe.json` | `reproduce.py` rebuilds both words and recipes and compares canonical JSON. `verify.py` independently derives K from A/scatter/B, checks all 660 arbitrary-input columns and exact frame/COPY/ERASE paths, and checks all 7,140 non-tree cycle inequalities including seed-6 tie order. |
| `budget.py`, `data/budget.json` | Reconstruction compares the entire 724-state certificate. The independent `verify.cut_budget` recurrence returns 15,025 D XORs; literal replay attains this lower bound with cuts 5, 34, 39, 57, 78 and strict `64 F^3 B^2 < 2^104`. |
| `verify.py`, `test_verify.py`, `reproduce.py` | All 23 adversarial/positive tests pass, including wrong endpoints, pricing, provenance, source types, the 106-bit uncut failure and the cheaper out-of-class 15,023-XOR rewire. The CLI requires the selected circuit to attain the cut-class optimum. |
| `Forest.lean`, `lean-toolchain`, `data/lean-axioms.txt` | Lean 4.21.0 compiles the complete file. Its seven audited theorems cover linearity, reversal, ordered forest action and compensated injection for arbitrary helper/target inputs. Each reports only `propext` and `Quot.sound`; the fresh output matches the recorded axiom report. |
| `native.py`, `data/native-selected.json`, `data/native-unconstrained.json` | Fresh unchanged C++ checkers accept the original and selected circuits at 5/9/11 stages: 900/1,380/1,620 formal columns and 6/18/24 omitted-bridge controls. Missing restoration is frame-legal but fails every endpoint checker. The uncut calibration fails all three native 104-bit checks. Fresh receipts match the historical results after normalizing elapsed times and output-directory paths. |
| `PROOF.md` | The forest/dummy-root-tree bijection preserves cost including both target XORs. The cycle exchange argument proves the unconstrained minimum. The cut recurrence considers retain/cut for each child, conditioned on its retained ancestor; the fixed work-row forward lower bound plus an attaining literal replay certifies the restricted optimum. These are written arguments with exact finite checks, not Lean optimality theorems. |
| `SOURCES.json`, `CLAIM.json`, `VALIDATION.json`, `NOTICE.md`, `README.md` | All 14 pinned repository inputs match. The original validation is historical macOS evidence. Attribution, seed/search scope, concurrent #759 credit and the distinction between the unconstrained floor and the feasible cut optimum remain explicit. |

## Reproduction and execution status

Run from the repository root, using a fresh output directory outside it:

```sh
python3 -B research/r420-forest-cut-budget/reproduce.py --lean /path/to/lean-4.21.0/bin/lean
python3 -B research/r420-forest-cut-budget/native.py --out /fresh/selected --boost /path/containing/boost
python3 -B research/r420-forest-cut-budget/native.py --out /fresh/uncut --boost /path/containing/boost --candidate research/r420-forest-cut-budget/data/optimum.json.gz --recipe research/r420-forest-cut-budget/data/optimum-recipe.json --expect-prefix-rejection
```

The 2026-10-14 follow-up reran these checks locally on macOS arm64 with
Python 3.14.7, Apple clang 21.0.0, Boost 1.85.0 and Lean 4.21.0. The selected
record integrity check also passed. The
[CI workflow](../../.github/workflows/r420-forest-cut-budget.yml) requires
the same finite, formal and native coverage on Ubuntu 24.04 / Python 3.13,
with bounded runtimes, read-only permissions and retained revision/input
identities and receipts. A local pass does not establish a hosted Linux pass;
the Actions run for the checked revision supplies that evidence separately.

Hosted Linux coverage passed at `e1a23bbecf308368865d827febf185fc03a74546`:
[run 38681040914](https://github.com/anthonylei/integer-mult-bounds/actions/runs/38681040914).
All finite, Lean, native acceptance/rejection and unchanged-artifact steps
passed; the run retains its revision, file inventory, logs and receipts.

## Claim boundary

Lean proves the generic Boolean compensation identity and forest ordering.
It does not bind the concrete JSON word or prove MST/DP optimality, physical
frames, global invoices or multiplication. The executable checks supply the
concrete finite evidence. In particular, 15,025 is optimal only over cuts of
the fixed oriented seed-6 tree; the 15,023 rewire demonstrates the boundary.

Full changed-word hosted-parent/whole-owner reconstruction, semantic-interface
integration, global invoices and outer assembly remain open, as disclosed in
the original submission. Repository-wide verification and native replay of
the separate 15,023 scope-control word were not run. No new κ or completed
supplier admission follows from this coverage. This follow-up is Codex-assisted
verification and written review, not independent human peer review.
