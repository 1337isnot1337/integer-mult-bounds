# Remove terminal helper transforms from the native supplier

The native supplier behind [the p7 construction](../pr4359-p7-padding/NATIVE.md)
has 408 independent arbitrary helper inputs. Each helper returns autonomously.
Twenty-two helpers have a final paid transform after their last contact with
another field. Removing those transforms improves the complete moment invoice.
The helper outputs then have rank four instead of rank five.

This is a changed finite native construction. Its use in a multiplication bound
retains the predecessor's native compiler, physical interface, routing and
analytic premises. The tensor and outer endpoint certificates are separate
parts of this package.

## The operator change

The source is the pinned `THREE-base-FULL-IDENTITY` canonical object and its two
literal native words. They are generated and documented by
[the full-identity reconstruction](../kappa-rebuild/complex/FULL-IDENTITY.md).
There are 224 arbitrary data fields, 408 arbitrary helper fields, and one
reused owned center. The owned center is initialized and erased for each use.

For each helper, the constructor locates every cross-field `ADD` or `COPY`
contact in the complete word. It finds exactly 22 paid climbs after the
helper's last contact. Each climb changes a four-dimensional frame to a
five-dimensional frame. Only scalar scaling and the inherited residual adapter
can follow on that helper. The affected helper roles are:

```text
277 282 293 298 307 309 323 325 341 346 353
355 357 362 369 371 373 378 385 387 389 394
```

For each affected role, the construction performs these changes:

1. Delete its final rank-one climb.
2. Retag any subsequent scalar scaling at the four-dimensional frame.
3. Set its terminal canonical frame to that four-dimensional frame.
4. Replace its two inherited residual adapters with exact whole-invocation
   monomial normalizers for the new rank-four helper operator.

The new normalizers appear explicitly in the directional receipt. They act
around the whole native invocation, under the same boundary convention as
[the predecessor's helper certificates](../kappa-rebuild/complex/README.md#all408-productive-helper-boundaries).
Their finite routing cost belongs in the caller's routing allowance.

### Why the other outputs do not change

Fix one affected helper. Its final paid transform acts on that field alone.
No later operation reads the helper into another field, or adds another field
into it. Subsequent scalar scaling commutes with the transform. Deleting the
transform therefore changes only that helper's own output operator.

The source endpoint is autonomous on every arbitrary helper input. Its helper
block is diagonal, and its data outputs have no helper-input defect. Replacing
the input monomial for this helper consequently changes no other output.
The new output monomial also acts only on that helper. This argument uses
arbitrary inputs throughout; it does not initialize, overwrite or identify
any persistent field.

All affected helpers start at the zero frame. If `F_U` denotes the exact
canonical operator for the new terminal frame, their bare physical residual
is `F_U` in forward orientation and its complex conjugate in backward
orientation. For each orientation, the exact compiler supplies monomials
`M_pre` and `M_post` such that

\[
M_{\rm post}\,F_U\,M_{\rm pre}=C_4.
\]

The check decodes the supplied recipes independently and compares both their
Clifford tableaux and exact zero-state amplitudes. The latter fixes the
absolute phase. In backward orientation the same check uses the conjugate
bare residual and again produces the positive standard `C_4` endpoint.
All 44 changed helper operators receive these checks.

## Complete local invoice

The helper profile and paid profile per native invocation become

```text
H = {4:22, 5:6, 6:18, 7:56, 8:93, 9:213}
P = {1:2465, 2:713, 3:224, 4:102, 5:20, 8:8}.
```

The constructor derives `H` from every changed canonical entrance and exit.
It derives `P` from every paid event in the changed literal word. It then
compares both derived dictionaries with the displayed profiles.

As in the p7 source invoice, the eight adjacent owned-center `5+3` chains are
replaced by their direct rank-eight operators. Each direct operator has the
same entrance and exit as its original chain. The exact compiler checks its
rank, tableau and absolute phase in both orientations. This contributes 16
additional phase checks. The owned center receives no productive credit.

The source profiles have 28 rank-five helpers and 2,487 rank-one payments.
The construction moves 22 helper jobs from rank five to rank four and removes
22 rank-one payments. The helper rank mass falls from 3,301 to 3,279. The paid
rank mass falls from 5,157 to 5,135. Their difference is unchanged.

The native scalar allowance is also unchanged: 158,120 in forward orientation
and 158,168 in backward orientation. New whole-invocation boundary monomials
still require the caller's finite routing allowance.

### The p7 moment improvement

There are 15 native invocations in the source p7 controller. Replacing every
native invocation by this construction gives the complete profiles

```text
T = {4:330, 5:90, 6:270, 7:840, 8:1395, 9:3195,
     25:448, 41:448, 57:448, 121:224}
P = {1:36975, 2:10695, 3:3360, 4:1530, 5:300,
     8:1464, 16:448, 32:448, 48:448}.
```

Both total rank masses decrease by 330. The surplus remains 608. For
`0 < t < 1`, the improvement in the moment surplus is exactly

\[
330\bigl(1+4^t-5^t\bigr)>0.
\]

The inequality follows from strict concavity of `x^t`. A numerical screen
places the changed profile's moment root at approximately
`c = 0.002696356026296`, compared with approximately `0.002686489` for the
source profile. Those numerical values are search guidance. A certified
saving requires the separate exact tensor and outer endpoint checks.

## Reproduction and source closure

From the repository root, run:

```sh
python3 -B research/pr4416-terminal-helper-trim/native_trim.py
```

The expected status is
`PASS_TERMINAL_HELPER_TRIM_ALL_632_INPUTS_BOTH_ORIENTATIONS`.
The constructor writes no files by default. To retain its deterministic
receipt, use:

```sh
python3 -B research/pr4416-terminal-helper-trim/native_trim.py \
  --write-result /tmp/native-trim-result.json
```

The Python entry point `run()` returns the same receipt. Calling
`run(include_objects=True)`, or adding `--include-objects` to the command,
also includes the changed canonical object and both changed literal words.
The receipt otherwise records canonical JSON payload hashes for those objects.
Regenerated gzip container bytes are not used as a mathematical equality test.

Every input is authenticated before import or replay. The complete direct
input list is:

| Input, relative to the repository root | Purpose |
|---|---|
| `research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-CANONICAL.json.gz` | Canonical frames and native metadata |
| `research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz` | Both literal source words |
| `research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py` | Independent exact native interpreter |
| `research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py` | Exact Clifford compiler |
| `research/kappa-function-composition/complex/prune_native.py` | Exact recipe decoding and conjugation |
| `research/kappa-rebuild/complex/rebuild_native.py` | Whole-invocation normal forms and phase checks |

The corresponding six SHA256 pins are explicit in `native_trim.py` and in
the returned receipt. Only the Python standard library is required. Imported
utility entry points that read other source files are not called.

The independent native interpreter checks both original source words, then
both changed words. It checks all 632 independent persistent input columns,
every scalar frame, every free noncommuting warp word, the complete paid
profile, and the initialized and erased center workspace. Its two changed
endpoint receipts establish the same main identity shear and autonomous
logical helper outputs with the new terminal frames.

Two controls must fail. The first deletes a climb needed before a later
cross-field contact. The second tries to assign rank-five productive credit
to a changed rank-four operator. The receipt records both rejections.

## Open next questions

1. Can a larger native port interface reuse the existing paid helper progress?
   Start by deriving the complete arbitrary-input endpoint of proposed extra
   ports. Any off-diagonal helper defect must be removed or explicitly priced.
2. Can a nonterminal helper segment be exposed as an independent productive
   job? A useful first test is simultaneous row and column isolation at an
   intermediate native cut. Row isolation alone does not establish autonomy.
3. Can a changed center construction produce additional arbitrary outputs?
   The main obstacle is its physical coupling into the data outputs. A
   logical scalar cancellation is insufficient when the physical frames differ.

The source native construction, controller, independent interpreter and
Clifford compiler retain their predecessor attribution and licenses. This
addition is under the repository's Apache-2.0 license and uses substantial
OpenAI assistance.
