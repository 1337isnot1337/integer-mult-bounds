# C04 portable loader review

Status: PASS for the inspected loader and final adaptation map, after correction of the manually executed oracle path. Heavy scientific stages remain the root's execution obligation. No package or frozen source was edited by this reviewer.

Inspected SHA256 values:

- verify.py: a07bbbc84d4310bbd7bc4d8b40b27a309fbdfabd4ea76516376601818318f732
- ADAPTATIONS.json: 147a2cad963185f51eb8e0881470931b18f181cfe8df815480d9b59dc8ae8ab0
- FROZEN-SHA256.json: a6393759e393cbf55500e04188601c0a799e2390b2cd3f844542ec3851744c22

- controls.py: ee5f9da59b570521e3c765e331bc2037a7c41f54303c017f0f0ab07a939c2def
- VERIFY.json: c26edd3102ce1eb9fc1a2f72a88fabb889aa5c8ecd335f399913f24cf6b72d36

## Source binding and assertion preservation

The installed SourceFileLoader.get_code replacement routes every source module under the package root through Portable.code. That function reads the source bytes, authenticates those same bytes, applies the enumerated unique substitutions, and compiles with dont_inherit=True and optimize=0. It never asks the original loader to select a package bytecode cache. SourceFileLoader.exec_module injects the same PORTABLE instance into nested modules before execution. Normal imports such as e8_cubed and explicit nested spec loaders therefore receive the same protection. Unregistered package source fails authentication. Every registered frozen file is checked both before and after the stage.

A concrete gap in the initial map was found and fixed by the root: legacy-budget/optimistic_budget.py directly execs the interval oracle, bypassing SourceFileLoader. The final map uses PORTABLE.authenticate for its raw oracle/receipt reads and PORTABLE.code(REPO/ORACLE) for the executed oracle. This now authenticates and registers the manually executed source, while retaining all historical assertions. The scientific oracle bytes and source-hash fields are unchanged.

## Adaptation scope and receipt comparison

The map changes only source location, immutable-source loading, output handling, and retained assertion compilation. It does not change factors, matrices, arithmetic, ranks, coefficients, chronology, controls, or precision equations. Replacing historical writes by comparisons avoids overwriting fixed evidence. The composition write option is explicitly rejected. Local absolute paths are mapped to the preserved source tree and inherited run inputs. Dictionary keys representing source paths receive the same normalization during receipt comparison.

Every mathematical JSON field is compared recursively. The only excluded fields are RESULT elapsed_seconds/environment and frozen replay elapsed_seconds/optimization_flag. These are runtime observations, not numerical claims. Canonical recipe outputs are compared byte-for-byte for both new and baseline recipes, including their serialization and phase witnesses. Required receipt sets must match exactly at the end of each stage. Path normalization does not alter scalar values or omit scientific fields.

The six declared stages cover:

- factor: full frozen asymmetric result, including original assertions and controls;
- native: actual recipe generation, all new recipe bytes and complete native result;
- replay: all frozen new/baseline operator checks and replay controls;
- adapters: baseline recipe regeneration and complete semantic/Boolean adapter invoice;
- precision: native coefficients, full label census and finite exact-grid/range ledger;
- composition: frozen all-column chronological compensation composition result.

This restores fresh execution of the generation controls and chain checks when all six stages pass; replay alone would not establish that coverage. Execution receipts identify loaded source files, now including the direct interval oracle. Package-level checks should also bind verify.py and ADAPTATIONS.json; FROZEN-SHA256 intentionally lists the preserved inputs rather than authenticating its own verifier.

## Meaningful lightweight controls performed

All controls ran with an optimized Python caller and temporary fixtures, without editing package files:

1. A syntactically valid matching-timestamp .pyc was deliberately made to execute a cached replacement. Ordinary import accepted it before loader installation. A nested import through Portable then executed the authenticated source instead.
2. That source contained an always-failing historical assert. It still raised the named AssertionError with the -O caller, proving optimize=0 reaches nested source execution.
3. Modifying an authenticated child source after the initial scan was rejected at load time with the source-hash error.
4. Changing rank_mass_change, the common fractional grid, total operator coverage, or baseline recipe coverage in otherwise valid receipts was rejected by the complete JSON comparison.
5. Adding one whitespace byte to new recipe serialization was rejected by the byte comparison.
6. Importing the actual revised legacy-budget module, without running its expensive main, registered precisely the legacy module and its interval oracle. The executed oracle's SHA256 matched the frozen entry.

No remaining loader defect was found in the inspected revision. These tests establish source-binding and comparison behavior; they do not replace the root's normal/optimized registered mathematical validation, portable export replay, or exact-head hosted checks.

## Final registered controls and metadata

The root added controls.py and registered it in normal and optimized modes. Source review confirms its rejection helper raises unexpected acceptance outside the caught ValueError path; it tests modified source, mathematical receipt and recipe bytes, missing coverage, and acceptance of the explicitly ignored duration observation. Its temporary fixture poisons matching caches for the real physical compiler and its nested Clifford vendor, then exercises the retained Op.then dimension assertion and exact nested execution set. These are meaningful controls of the actual wrapper boundary. The root reports optimized controls and metadata validation passing; this reviewer did not repeat those runs.

VERIFY.json registers all six scientific stages under -I -O -B with the frozen code forced to optimize=0, plus controls under -I -B and -I -O -B. The README accurately distinguishes generator/replay controls, arbitrary complex operator scope, logical FULL restoration, standalone exact precision, and excluded finite-tape/approximate-child/joint-supplier claims. Source acquisition and export instructions match the inspected closure. The registered full stage executions and hosted checks remain independently reported root evidence.
