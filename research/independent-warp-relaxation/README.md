# Independent-map relaxation of the current scalar word

Prepared for Cinna Davis with OpenAI assistance. Derived from the credited joint helper/map search of Cinna Davis and Cao Yifan. Apache-2.0.

The model gives every warp occurrence its own independently chosen invertible map. Consecutive warp occurrences are composed into one unconstrained map. This removes shared-map consistency and fixed prelude-line restrictions. Helper entrances and scalar contacts remain variables; all endpoints and helper exits retain the source contract.

This is deliberately optimistic. It does not produce a physical word and cannot certify a positive kappa. A feasible source solution remains in the model. Ordinary frame edges are still monotone, and intervals of gap greater than five use a bounded catalogue.

On the published helper-warp witness, HiGHS solved 1,661,639 variables and 320,373 constraints in about 28 seconds. The reported objective difference is -7.96e-13, consistent with no gain within floating-point tolerance. No exact dual certificate or global optimum is claimed. One gap-nine interval was truncated. This screen does not rule out choices outside that catalogue, new scalar words, nonmonotone frames or changed helper interfaces.

Run `OPENBLAS_NUM_THREADS=1 python -B research/independent-warp-relaxation/search.py` to regenerate RESULT.json. This requires SciPy and NumPy and writes discovery output. The source word is `research/helper-warp-joint/ACTUAL-WORD.json.gz` from public commit 7197831b13c8f5715055a608a148fbfde7b38b7d. No upstream sources are modified.

## Open next questions

The relaxation suggests that merely freeing the prelude native maps is not a promising isolated change in this bounded contact model. Investigate a changed scalar/helper graph or a fully priced typed supplier instead. A mathematical ceiling would require an exact optimization certificate and complete frame domains.
