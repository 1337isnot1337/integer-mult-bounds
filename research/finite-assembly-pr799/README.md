# PR799 supplied-cap application of finite assembly

This sibling applies George Lydakis's retained finite-assembly theorem to the
maintainer-admitted PR799 native-complex cap and unchanged PR589 bit cap. It
reuses the existing `finite-assembly-frontier` package unchanged, including its
historical433 fixture, both exact rational engines, proof and five tests.

The selected target is
`0.001661634653669567075843432`, compared with PR799's
`0.001661634653669567`. The difference is `7.5843432e-20`. This is a tiny parameter
selection improvement and a reusable theorem application, not a substantive
frontier breakthrough, new physical construction, runtime speedup or
unconditional multiplication theorem. Nine finite bootstrap levels suffice.
The strict supremum is not attained.

## Immutable offline inputs

Use the public repository `CrocSwap/integer-mult-bounds` at exactly
`f567884aeb8851b6e794af1184119a3bfbe1e631`. `UPSTREAM.json` pins source bytes,
Git blobs, the complete X4 source package, checker closure, PR741 ancestry,
and the two archives the verifier reads. Do not use a newer checkout, cap-only
README input or the historical PR645/PR543 package ASSEMBLY.

A normal checkout at that commit is sufficient. For a smaller snapshot:

```sh
git clone --filter=blob:none --no-checkout https://github.com/CrocSwap/integer-mult-bounds.git ../integer-mult-pr799-upstream
git -C ../integer-mult-pr799-upstream sparse-checkout init --no-cone
git -C ../integer-mult-pr799-upstream sparse-checkout set --no-cone --stdin < research/finite-assembly-pr799/SNAPSHOT-PATHS.txt
git -C ../integer-mult-pr799-upstream checkout f567884aeb8851b6e794af1184119a3bfbe1e631
```

From the repository root, with this package at
`research/finite-assembly-pr799` next to the unchanged core, run:

```sh
python3 -E -S -B research/finite-assembly-pr799/verify.py \
  --upstream ../integer-mult-pr799-upstream \
  --output ../integer-mult-pr799-result
```

`--core PATH` permits another location for the same pinned core package.
The output directory must not exist and must be outside both input packages.
Input files are checked before import and after verification. This is an offline
source and receipt application, not a replacement for the original physical replay.

## Exact reuse boundary

The current standalone ASSEMBLY is byte-bound to the separate
`integrated799-replay.tar.gz`, whose owner and invoice hashes match. The
submitted `pr799-replay.tar.gz` is a different coherent run; it is not silently
substituted or mixed with these leaves.

The original PR741/PR799 binding functions are imported unchanged. They check
source-bound ancestry, bit record, recorded stage completions and artifacts,
profiles, frames/phases/wrappers, owner/invoice and controls. The original
`assemble.assemble` recomputes the complex finite invoice and conservative,
native-complex and bit moment/outer witnesses. Its complete JSON result must
match the current receipt. Native complex omits the bad-residue surcharge;
bit retains it. The conservative admission is checked first.

The bit coefficient bound `393 < 512` and row bound18355 are reused through
byte-bound PR589 EXPECTED/RESULT and the authenticated earlier physical replay;
this verifier does not regenerate the underlying bit coefficient integer.
Original compiler, common-label/mutable-source realization, whole-call hosting,
precision/tape, weighted-bootstrap and analytic/H1-H5 assumptions remain.
The finite-assembly premises retain `a0=384599/10^10`, `a0<min(b,c)`,
`b<1/32`, coefficient charge512 and the same semantic/literal/row bridge.

Exactly one policy chooses `greatest_grid_target(bit, complex, 1/10^27)` using
unchanged `construct()`. Both engines check the selected seed under the correct
models. The finite cutoffs,47 strict margins and five invalid endpoint/backoff
controls are verified. `EXPECTED.json` pins the entire admitted assembly and
seed intervals as well as target/baseline/difference/levels. No grid sweep is
performed. Partial receipts and primary failures are retained.

## Attribution and scope

George Lydakis's finite-assembly theorem is the new reusable interface. PR799
X4 is Jeremy Kothe's work; PR741 frames are Chafik Boukhalfa's; PR589 is
DreamingOfClouds' bit supplier on eumemic's PR555 construction. Rohan Arun's
PR559 native-complex correction, icekylinx's source gauge, earlier entrance,
cold-end and owner work, the original engine/proof authors and cumulative
notices retain their attribution. See `NOTICE.md` and upstream source notices.
