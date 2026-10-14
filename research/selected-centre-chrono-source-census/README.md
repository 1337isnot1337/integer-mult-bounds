# Centre-source rank census for dependent selected-call pairs (PR2048 open question 2)

**Status:** research note and scoped negative result. This is a finite certificate in a declared scalar
projection. It is not a native obstruction, not a formal proof and not a new kappa. The selected frontier
is unchanged.

## Question

PR1918 found that one forward pair with disjoint data (selected calls time 0 and time 1) has stacked
centre-source rank 16. It also gave a scoped linear-transcript lemma: sharing needs d >= rank. PR2048 lifted
that pair to native frames. Its open question 2 asks about pairs whose sources depend on each other in time.

This package replays all 144 selected `local_cover_sweep` calls in the same projection. It asks two things:

- Do pairs that share source owners, or that pass data from one call to a later one, have rank below 16?
- What is the rank of all 1,152 centre-source rows?

## Projection (inherited from PR1918, extended to every call)

- **Scalar operations.** `clear`, `copy`, `scale` and `add` are exact over Q. `climb`, `adapter` and
  `residual_adapter` act as the identity. The `center` event is the read cut.
- **Calls only.** The calls run in `execution_schedule` order from a formal initial vector with one
  independent variable per physical owner (14,336 owners). The 144 `bridge` events, 160
  `idle_cover_sweep` events, terminal events, bank padding and translate are **not executed**. For every
  dependent pair, the receipt counts the bridge and idle events between the two calls on their replicas.
- **Centre-source rows.** Row k is the value of private register `C_k` at its rank-8 `center` event.
  - Forward: the centre copies `L[word.centers[k]]`. The verifier checks that these 8 copies are
    `C_k <- L[92,57,81,224,11,240,9,256][k]` and that each row equals PR1918's phase-start cut.
  - Backward: the centre gathers 56 target-role terms, each with coefficient 1/4.
- **Composition per orientation.** Each orientation gets one exact local replay over 704 roles. The
  verifier checks clean private exit and these exact endpoints:
  - forward: `L_i += L_{i-112}` for 112 <= i < 224;
  - backward: `L_i -= L_{i+112}` for 0 <= i < 112.

  Every call is bound to its program through `local_program_sha256`.

## Results

1. **Global rank 1152/1152.** This holds exactly over Q and also mod 2^61-1. The forward rows (80 calls)
   have rank 640 and the backward rows (64 calls) have rank 512.

   So in this projection, no centre-source row of any call is a linear combination of other calls' rows.
   By PR1918's lemma, any grouping of k calls needs at least 8k source-dependent linear-transcript
   scalars, for every k.

2. **Every dependent pair has rank 16 (1,539 pairs).**

   | Dependency class | Pairs |
   |---|---:|
   | Share roles 0..111 owners (all 112 of them) | 96 |
   | Earlier write is read later, roles 0..223 (same 96 pairs) | 96 |
   | Share a formal support variable | 1,525 |

   By orientation: 1,141 forward-forward, 259 backward-forward and 139 forward-backward. Every pair also
   has rank 16 when restricted to the formal variables of its own roles 0..223 owners. **The null
   expectation holds, and no deficient pair exists in the declared projection.**

   The 96 shared-data pairs are exactly six classes of 16 same-replica pairs: f0->b1, b1->f2, b3->f4,
   b5->f6, b7->f8 and f0->f2.

3. **PR1918's data-only robustness check does not carry over to the dependent class.** Take the 16
   same-replica forward-stage-0 -> backward-stage-1 pairs. Each pair uses the same 224 owners, and no
   bridge or idle event touches the replica between the two calls.

   Restrict each pair to its source-data owners (roles 0..111, PR1918's own statistic). The rank is
   then **8, not 16, for all 16 pairs**. The verifier checks an exact identity for every k and every
   replica:

   `backward1 centre k |_D = (1/4) * forward0 centre k |_D`

   The forward-0 centre does not read the target block T (roles 112..223). The backward-1 centre
   restricted to T has rank 8. So the formal rank 16 of these pairs comes entirely from the pre-call
   contents of the target block.

   This is not a deficiency in the template's semantics, where every owner is a live data family. It
   does mean that independence in this class rests on an assumption about T, not on the data block.
   RESULT.json stores exact left-kernel witnesses, checked by direct evaluation.

4. **Sensitivity diagnostics.** These are *not* the template's semantics, and are reported only to
   show which assumptions the full rank rests on.
   - Zero every owner first touched in a helper role (>= 224). The global rank drops to 570. 55 calls
     have all-zero rows, including every backward call in stages 3, 5 and 7.
   - Zero every owner not first touched in roles 0..111. The global rank drops to 418.

   In the native schedule, the omitted bridge and idle events carry data into these owners, so these
   collapses are expected projection effects. They show that the full-rank result depends on owner
   contents that the calls-only projection does not model.

## Reproduce

From the repository root, Python 3.12 or later, standard library only. It takes about 30 s and under
200 MB of peak RSS:

```sh
python3 -I -B research/selected-centre-chrono-source-census/verify.py
```

Expected output, as one line:

```text
PASS_SELECTED_CENTRE_CHRONO_SOURCE_CENSUS calls=144 rows=1152 global_rank_q=1152 global_rank_mod_p=1152 dependent_pairs=1539 formal_pair_rank_hist={'16': 1539} pair_local_rank_hist={'16': 1539} deficient_formal_or_pair_local=0 f0_b1_same_block_data_only_ranks=[(8, 16)] controls=8
```

To run it through the package hook:

```sh
python3 scripts/research_package.py --package research/selected-centre-chrono-source-census
```

## Controls (each must fail or change the receipt)

**Internal controls, run on every verification:**

- Reproduce PR1918: its 16 source maps match exactly, with rank 16 and data-only rank 16.
- Duplicated rows give rank 8.
- Reversed-order rows give rank 8.
- The forward centre copies equal `word.centers`.
- Perturbing one phase-A `add` coefficient in the backward program changes the program binding and
  changes or rejects the local map.
- Omitting one backward centre gather `add` changes the centre input.
- Omitting the final private `clear` is rejected as a dirty exit.
- Flipping one bit in the archive or in a member changes its SHA256 pin.
- rank mod p never exceeds rank over Q.

**External controls, run in a scratch copy on 2026-10-14:**

| Change | Result |
|---|---|
| None (clean copy) | PASS |
| `global_rank_q` edited in RESULT.json | `result receipt differs` |
| One byte of the archive copy flipped | `pin mismatch: ...selected-replay.tar.gz` |
| PR1918 `source_rank` edited | `pin mismatch: ...selected-centre-composed-source-rank/RESULT.json` |
| One kernel-witness coefficient changed from `-1/4` to `-1/2` | `result receipt differs` |

## Sources and pins

- **Base commit:** `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`.
- **Archive:** `research/community-frontier1094-audit/selected-replay.tar.gz`, sha256
  `f1da8061...d529d6`. The members are pinned in verify.py: GLOBAL-TEMPLATE `2acf02b4...7760`,
  LOCAL-PROGRAMS `241fde27...ef3a` and CANONICAL-WORD `16bc0ebb...d219`.
- **Selected record:** `certificates/selected-result.json`, sha256 `10b9e340...fa32`.
- **PR1918 receipt:** `research/selected-centre-composed-source-rank/RESULT.json`, sha256 `31555505...a668`.

Full digests and Git blobs are in [SOURCES.json](SOURCES.json). Program digests are bound per call:
forward `071ecdac...`, backward `f36c5831...`.

## Scope, inherited assumptions, unresolved obligations

- **Inherited assumptions.**
  - PR1918's scalar projection: frames, adapters, residual adapters and climbs act as the identity.
  - The centre event is the read cut.
  - Physical owners carry independent formal values before the first call.
- **Not executed.** Bridges, idle cover sweeps, terminal events, padding and translate. Rank under the
  native schedule is **not** certified. Rank is lower semicontinuous, so the true composed map could
  have lower rank.
- **Unresolved.**
  - A native lift (PR2048-style) of any of these statements.
  - The semantics of the target block at forward-stage-0 entry (see result 3).
  - Persistent-storage, transport, restoration, hosting and precision invoices for any reuse.
- No kappa follows from any outcome here.

## Open next questions

These are also listed in [TASK.json](TASK.json).

1. **Execute bridges and idle sweeps.** Do the conclusions hold when bridges and idle sweeps run at owner
   level?
   - *Why it matters:* the full rank depends on owner contents that these events change (result 4).
   - *First step:* derive the owner-level scalar semantics of one bridge from `route_semantics` and
     DATA-PHASES, then replay replica 0, stages 0-2.
   - *Blocker:* these events are pair- and family-level, and the frame data is outside this projection.
2. **Target-block semantics.** At forward-stage-0 entry, is the target block independent live data, or is
   it zero, preconditioned or a function of D?
   - *Why it matters:* if it is not independent, the 16 forward0->backward1 pairs drop to rank 8. That
     would be a linear-transcript sharing lead in this projection.
   - *First step:* trace the template's initial data assignment and its "frame-zero output
     preconditioner".
   - *Blocker:* input-data semantics.
3. **Native lift of the 1/4 identity.** Does the `(1/4)` D-part identity lift to native 512-address
   frames?
   - *Why it matters:* even if it does, the target-block part still needs its own rank-8 evaluation.
     Storage, transport, restoration, hosting and precision must also be fully priced.
   - *First step:* apply PR2048's native lift to calls 0 and 4.
   - *Blocker:* native centre semantics.

## Credit and overlap

- **Projection, replay logic and lemma:** PR1918 (Adam Gall,
  `research/selected-centre-composed-source-rank`). This package reimplements its replay with credit and
  pins its receipt.
- **Open question 2:** open PR2048 (commdata2338).
- **Related work:**
  - Early-fanout and zero-storage test: PR2076 and Discussion #2058 (1337isnot1337). The census claimed
    there was abandoned and never run.
  - Owner-aliasing census: PR1829 (Cinna Davis).
  - Nonadjacent owner aliasing: Discussion #1963.
  - Sharing budgets: PR1708, PR1748 (ToikY), PR1791 (rtyu193-rgb) and PR1664.
- **Selected construction:** the #1094 lineage (Rohan Arun et al.; see `certificates/selected-result.json`).
- **Concurrent idea:** a sibling local session drafted a similar census card and aborted it. Nothing was
  reused.

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5). Apache-2.0.
