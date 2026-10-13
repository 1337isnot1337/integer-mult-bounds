# Independent PR1042 replay-capsule closure

**Status:** independent verification; no new construction and no new kappa.

This package independently checks the frozen publication capsule behind selected PR1042, conditional kappa `1672188119205421 / 10^18`. It was selected by OS-random seed **75** at base `ba82555c64e1879e4b7decce28186f208fcb8262`.

## Result

`verify.py` treats `research/community-frontier1042-audit/selected-replay.tar.gz` as untrusted data, uses only the Python standard library, never extracts a member, and imports no construction code. It authenticates 458 safe regular members (45,647,427 expanded bytes), all 457 declared artifact digests, exact inventory closure, ten successful stage/log bindings, six promoted receipts, and the selected/integration publication pins.

## Reproduce

```sh
make frontier1042-capsule-closure-verify
```

Expected final markers: `PASS_FRONTIER1042_CAPSULE_CLOSURE`, six tests, `OK`. The target also runs under optimized Python so checks cannot depend on removable assertions.

## Controls

The suite rejects path traversal, duplicate members, undeclared members, mutated artifact bytes, a nonzero stage, and a promoted-receipt mismatch.

## Scope

This is finite integrity and binding evidence about the committed capsule. It does not establish that recorded commands ran, independently recompute T16 mathematics, verify named source packages, discharge inherited interfaces, prove analytic transfer, benchmark multiplication, or formalize the full theorem.

## Attribution

Martin Rv (@martinxxx9), with substantial Perplexity AI assistance in research, implementation, verification and writing. It preserves all PR1042 and batch1047 predecessor attribution. Apache-2.0.
