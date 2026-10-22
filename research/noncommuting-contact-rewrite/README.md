# Noncommuting scalar-contact rewrites

Prepared for Cinna Davis with OpenAI assistance. Retains the repository's credited native sources and Apache-2.0 terms.

## Result

Twenty-two exact conjugate-ADD rewrites preserve every persistent endpoint, both orientations, every paid bridge and warp, and all helper interfaces. Scalar primitive allowances decrease by 216 in each orientation, to 157904 forward and 157952 backward. The paid profile and kappa do not change.

The source is `research/helper-warp-joint/ACTUAL-WORD.json.gz`, published at 7197831b13c8f5715055a608a148fbfde7b38b7d. Its profile coincides with Cao Yifan's concurrent PR4610; no profile priority is claimed.

Run `python -B research/noncommuting-contact-rewrite/apply.py --check`. This immutable replay checks all 632 literal columns, owned cleanup, and the full multiset of role-bound paid transitions. Existing absolute-phase certificates apply to the identical physical bridges and warps. The replay does not rerun those certificates or certify a new complete multiplication theorem.

## Discovery coverage

`discover.py` finds 23 inverse-ADD conjugation patterns. `search.py` tests 55 feasible frame assignments. Twenty-two are cost-neutral; the remaining pattern worsens the paid moment. `joint_search.py` reruns the joint helper/map model after the neutral rewrites and finds no improvement. The floating-point MILP result is not an exact optimality certificate.

`conjugate_windows.py` examines 861 larger patterns, with 223 fixed-frame feasible proposals. None is cheaper. `optimistic_windows.py` identifies 353 heuristic nominees by deleting outer gates without charging corrections. This heuristic is not a lower bound after unrestricted retiming.

Discovery scripts regenerate their JSON outputs. Only `apply.py --check` is an immutable replay. The source tree is required; this directory alone is not a standalone export.

## Open next questions

Joint retiming of larger rewrites may escape fixed-contact screening. See the adjacent window-retime package for four tested representatives. A cheaper profile still requires complete native and absolute-phase replay.
