# Attribution and source boundaries

Prepared for Joel Pulikkan (GamingPuzzled) with Claude Opus 5.5 (Anthropic)
assistance via Claude Code, Apache-2.0.

- New in this package: the observation that PR890's fixed-family bound becomes
  replica-unbounded once the charged prefix payload is raised (its row cost is
  explicit), the T37 = T21 + T16 composition and proportional merge, the
  eight-role (44,3,2) -> (48,1) trade, the 8+8+8+8+5 bank lift and its audit,
  the 1024-bit charged-prefix adaptation, and the strict T37 composition.
- Chafik Boukhalfa (chafreaky), PR890: the T21 owner map (T5 witness, T16+T5
  interleaving, nine-role trade), 8+8+5 bank lift, independent checks, owner
  bound (whose signed-price relaxation identifies T37's target profile) and the
  verification driver this package adapts. Used unchanged from
  `research/complex-t21-owners` by path and hash pin.
- Hao Yan (@FanPUYen), PR858: T16 duplication and eleven-role correction,
  physical source-event windows, independent owner/chart audit and the
  replication-parameterization approach. Its constructor is used unchanged
  (twice: inside T21 and as the second T16 component).
- PR869/PR870: the unchanged U8 local word, builder and controller chain
  (NewBArch triangle-hybrid B; ColdWitness/icekylinx driver), vendored in PR890.
- Jeremy Kothe's PR799, Chafik Boukhalfa's PR741, the gauge44/PR645, PR635,
  PR514/PR484/PR507 controller lineage and the PR589 bit supplier remain
  dependencies, covered by the ancestral replay. PR795's signed dual (Chafik
  Boukhalfa) is the relaxation used to locate the T37 optimum.

`DEPENDENCY-PINS.json` pins every PR890 and repository file read by path.
`data/ADAPTER-EDITS.json` lists every literal source edit applied to PR890's
vendored PR870 code with its required multiplicity. `MANIFEST.json` binds this
package.
