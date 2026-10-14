# Fixed-tape proof toolkit

Reusable, kernel-checked Lean infrastructure for finite multitape programs,
dirty workspace, subroutine scheduling, and asymptotic cost transfer. This
contribution leaves the selected supplier profiles and kappa unchanged.

The main assembly theorem, `VerifiedPipeline.compile_completed_frame`, turns
**every actual halted execution of a fixed finite heterogeneous TM2 program**
into a literal absolute-coordinate multitape execution. If the program's
maximum statement depth is at most `D` and the source takes `n` steps, the
physical execution takes at most `2*D*n` transitions and retains the encoded
final stacks. Each tape has a finite observation footprint of at most `t+1`
cells that suffices to replay the completed computation with the **same actual
time**, despite arbitrary changes to cells outside that footprint.

The implementation includes the transition tables and simulation proofs; the
conclusion is not an assumed compiler, routing gadget, or arithmetic oracle.
Input parsing, reversal, padding, and canonical-output conversion are separate
programs whose costs must be supplied when applying the theorem to another I/O
convention. The toolkit does not establish the fast multiplication theorem.

## What contributors can use

| Module | Checked interface |
|---|---|
| `Model` | Fixed finite state/alphabet/tape types; literal write/unit-move steps; exact runs and stack-tape primitives |
| `Locality` | Finite transition table; scanned-symbol-only decisions; exact all-cell locality; deterministic executions |
| `Composition` | Concrete finite sum-control composition with one charged, stationary handoff |
| `Absolute` | Exact-cost realization in the absolute integer-head/cell semantics used by multiplication work |
| `Trace` | Unit-speed head reach; sharp write cone; protected regions; whole idle tapes |
| `FrameRule` | Actual finite read/write footprints; lockstep dirty-data simulation; completed runs include terminal observations |
| `TM2Compiler` | Finite syntax-address control; every source macro is charged at most twice its statement depth |
| `TM2HeterogeneousCompiler` | Dependent stack alphabets embedded in a finite tagged sum; typed-tag preservation and exact output decoding |
| `Complexity` | Runtime witnesses tied to actual execution, halt and output; concrete quadratic bounds imply standard Big-O |
| `AsymptoticTransport` | Completed source contracts compile at explicit cost; fixed or uniformly bounded depth; independently charged adapters |
| `SubroutineContracts` | Fixed finite-stage scheduler, literal handoffs, exact sum of stage costs plus handoffs, volume invoice and spectator prefixes |
| `VerifiedPipeline` | Compiler, physical runtime, encoded output and completed dirty-frame theorem assembled without an extra assumption |
| `Examples` | A concrete three-tape/four-symbol copy program, universally correct on arbitrary dirty tapes in one actual step |

The complete interfaces and worked application patterns are in [API.md](API.md).
[PROOF.md](PROOF.md) states the mathematical scope and assembly argument.
[FRONTIER.md](FRONTIER.md) pins the nearby PRs and explains the contribution's
relation to the current transfer frontier.

## Reproduce

The inexpensive registered replay uses standard-library Python only:

```sh
python3 -I -B research/multitape-proof-toolkit/verify.py --out ../toolkit-finite-result
```

It checks the exact source inventory, finite dirty-copy/dispatch/write-move/tag
fixtures, and report-consumer corruption controls. Its result explicitly says
`kernel_check: not_run`. It does not replace the formal replay below.

The full formal replay requires the pinned **Lean 4.34.1** and the cached exact
Mathlib/dependency revisions in `lean/lake-manifest.json`. With that environment
already installed:

```sh
python3 -I -B research/multitape-proof-toolkit/replay.py \
  --lean /path/to/lean-4.34.1/bin/lean \
  --cache-project /path/to/project-with-the-pinned-lake-packages \
  --out ../toolkit-kernel-result
```

For a fresh environment, `cd research/multitape-proof-toolkit/lean`, then use
the pinned `lean-toolchain`, `lake update`, and `lake exe cache get` to install
dependencies before replay. These setup commands can use the network; the
replay itself does not download anything. `--cache-project` can then name this
`lean` directory. Derived `.lake` and `__pycache__` directories are not package
sources. The source manifest otherwise checks an exact file inventory.

Every package proof module is rebuilt serially into a **new external output
directory**. The audit enumerates declarations by their **defining module**,
including private and globally named helpers, compares the exact pinned
`expected/AXIOMS.json` inventory, and collects transitive axioms
for every one. It rejects locally declared axioms and dependencies beyond
`propext`, `Classical.choice`, and `Quot.sound`. Actual Lean fixtures verify
private/global ownership coverage and rejection of public axioms, unused
private axioms, and a private unproved theorem. No missing compiler, empty
report, skipped module, or parser-only path can count as formal success.

`VALIDATION.json` records the completed local validation. Hosted CI and external
human review are separate from that evidence. Generic registered-package replay
checks the source/finite layer; Lean needs the dedicated formal environment.
The ready CI recipe is [ci/formal.yml](ci/formal.yml); copy it to the displayed
workflow path to activate it. No hosted run is claimed by this package.

## Applying this to the multiplication frontier

1. Implement a concrete finite program or source TM2 routine. Keep unbounded
   words on tapes/stacks, not in the control register.
2. Prove its actual execution, halt, and output contract. Instantiate the
   compiler with a fixed syntax-depth bound.
3. Compose concrete tape-compatible stages with the scheduler. Its `k` is fixed
   before input quantifiers; count every one of its `k` handoffs.
4. Protect dirty ancestors using an actual footprint or checked idle-table
   certificate. Idle writes alone do not imply that dirty symbols are unread.
5. Charge each I/O adapter separately and use the asymptotic transfer theorems
   only after both source and adapter bounds have been established.

This provides formal reusable implications for other contributors' program,
footprint, and cost certificates. It is independent of any numerical supplier
search or claimed exponent improvement.

## Open next questions

- Instantiate the completed-frame rule on the concrete park/call/restore
  controller from PR1379. First supply its literal table and actual visited
  cells; its physical stream moves and recursive caller are not this toolkit's
  generic theorem. This would replace endpoint-only restoration with a usable
  completed-runtime guarantee.
- Supply charged serialized-input and canonical-output adapters for the
  upstream `x#y` or Mathlib tagged-pair conventions. Start with one fixed parser
  and a padding/reversal loop; the physical program and uniform cost proofs are
  required before claiming I/O interoperability.
- Extend the fixed-stage scheduler to a concrete recursive dispatcher with
  explicit on-tape call-stack control. Start with a single size-decreasing
  two-child caller; proving its row routing and parameter-independent overhead
  is a separate construction.

These next steps are recorded structurally in `TASK.json` so other contributors
can locate the precise interfaces and continue with their own computation.

## Credit

New proof implementations and replay tooling were prepared with substantial
OpenAI Codex assistance and three parallel Codex agents. The machine vocabulary
builds on Mathlib's tapes and TM2. The inspected absolute-coordinate convention
and the motivating frontier are credited in [NOTICE.md](NOTICE.md) and
[FRONTIER.md](FRONTIER.md). Original upstream sources are not changed or
silently replaced. New work is Apache-2.0.
