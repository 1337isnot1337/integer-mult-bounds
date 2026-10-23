# Owned-wire floor with native and helper boundaries free

Each of the eight owned wires in the actual round-three word pays Fourier
rank mass at least eight and moment at least 8^t for 0<t<=1, under the fixed
scalar word, fixed main entrance/exit spaces and monotone persistent L paths.
Both helper boundaries and every native input/output relation can be removed.
The owned C itinerary may move on both sides, use nonnested canonical charts,
and take arbitrary paid intermediate Clifford charts under the retained
projected-subspace rank convention. The source attains the bound.

The proof extends Matarener's [PR5060](https://github.com/CrocSwap/integer-mult-bounds/pull/5060)
owned-wire floor from fixed native/helper boundaries to a newer word and the
larger domain above, using Dugongue's relative-rank grammar. Those results and
their elementary propagation/path lemmas are prior work. This is a scoped
extension, not a whole-profile optimum or a higher kappa. The selected
conditional bound at the base remains kappa 0.00302015.

[PROOF.md](PROOF.md) gives the theorem, path and rank arguments, hypotheses
and limits. [WITNESSES.json](WITNESSES.json) contains 128 independent entrance
paths with 2,204 links and 144 outgoing cap paths with 2,516 links. These cover
both actual orientations and every owned lifetime separately. Only fixed main
boundaries supply the witnesses; no clean logical helper input is assumed.

Reproduce with standard Python 3.12 or later:

```sh
python3 -B scripts/research_package.py --package research/monotone-owned-centre-floor
python3 -I -B research/monotone-owned-centre-floor/verify.py
python3 -I -O -B research/monotone-owned-centre-floor/verify.py
```

The registered normal/optimized commands reconstruct the complete source
paid/helper baseline, check 300 corruption/hyperplane/cap/warp-cut controls,
and calibrate the projection-rank inequality on every ordered pair of binary
Lagrangians in dimensions 1..3 (18,459 pairs). The written dimension argument,
not those finite samples, proves the general inequality. `verify.py --write`
regenerates the deterministic witness artifact. Normal verification does not
write it. No solver, network or predecessor executable import is needed.

Source: Cao Yifan / intqwq's round-three word, retained in
`research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz`, with compressed and
decompressed SHA256 bindings. `SOURCES.json` pins the exact live input and
provenance. All frozen predecessor bytes remain unchanged. Credit Matarener's
#5060 proof, Dugongue's #4534 owned-retiming and #4654 chart grammar,
Cinna Davis's native/controller/retiming and general Gaussian contact work,
zxv, Jacob Alan Sussman and the retained E8/scalar/Clifford/compiler lineage.

The investigation continues the
[common-kernel prototype](https://github.com/1337isnot1337/integer-mult-bounds/tree/8052b4818738986960c5b243097b3fffb6d21139/research/owned-centre-kernel-retiming)
and [independent-contact claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/4611#discussioncomment-19139586).
The prototype permits nonmonotone persistent edges and is not excluded.
The nearest-Clifford/split-contact work in
[discussion #5125](https://github.com/CrocSwap/integer-mult-bounds/discussions/5125)
also has a distinct interface. Canonical investigation:
[the scoped update](https://github.com/CrocSwap/integer-mult-bounds/discussions/4611#discussioncomment-19143793).

Prepared by Cinna Davis / 1337isnot1337 with substantial OpenAI Codex
assistance; no subagents; Apache-2.0. Written scoped proof plus author-checked
finite evidence, not independent human or proof-kernel acceptance. A package
merge would not select a frontier or prove a full multiplication theorem.

## Open next questions

- Can nonmonotone persistent L transports jointly with changed native maps and
  owned contacts improve the fully paid moment? This changes the containment
  paths used here; the old common-kernel/fixed-map scan does not decide it.
  First derive a bounded joint model with every former zero bridge, every
  center job and every helper residual priced at actual relative Fourier rank.
  Exact native phases, endpoint/ownership replay and compiler/outer funding
  remain the acceptance obligations.
- Can a changed scalar word or paid split-contact interface remove a required
  common-frame path cheaply enough? Name the exact edit, emit both full words
  and reconstruct all paid/helper children before search. Existing #5125
  claims must be checked before taking an overlapping instance.

The structured questions, scope and stopping decision are in
[TASK.json](TASK.json). No additional floating search is claimed.
