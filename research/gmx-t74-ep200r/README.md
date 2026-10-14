# 220-digit endpoint and outer-witness refinement on PR1424 / PR1536 / PR1549 (construction unchanged)

**Current claim (matches `CLAIM.json` and `SPEC.json`): conditional kappa = 0.0016768552290713218862064567722745926195124487395104752628033651910511566552120096495157846916413845429929275438103942180631016965288202851222935391871757186450912861283049468793633058255444681490343981523271533501139143**, which is **8.152327e-201** above PR1549's 0.001676855229071321886...03439, and **9.815233e-200** above PR1536's 0.001676855229071321886...0343.

**Soundness repair retained:** Retains PR1519/PR1536's fine Mercator engine repair (even term count) and independent exact 2*atanh oracle stage (`code/oracle_check.py`, run by `verify.py` as stage `fine-engine-oracle`). The construction, scalar words, provider inventory, owners and paid profile are PR1424's (PR1319's 74-replica exact fill of PR1297's four cold kernels), unchanged.

## What changed relative to PR1536 and PR1549
1. **220-digit certified complex endpoints:** Both native and conservative complex endpoints are refined to a 1e-220 certified bracket (`endpoint_digits` = 220). Both rational engines (`fine_mercator` with DYAD 2^830 and `fine_moment` with GRID 10^240) certify accept at the endpoint and reject at endpoint + 1e-220.
2. **Deepened outer witness settings:** In `SPEC.json:outer_refinement`: `grid_digits` = 220 (deepened from 200 to 220 digits), `margin_digits` = 260 (eta = beta = 10^-260, target backoff 10^-263), `bootstrap_steps` = 100 (deepened from 90 to 100 steps).
3. **Strict assembly replay:** Passes all 47 outer inequalities, conservative checks, and 4 rejection controls (`next_grid`, `zero_eta`, `zero_beta`, `unit_beta`).
4. **Full package-owned verification:** Passed all 6 stages (`PASS_T74_EXACT_FILL_COMPLETE_FINITE_ADMISSION`).

Reproduce from this package: `python3 -B verify.py --work /absolute/new/work --base-native-from /bound/base/native --extra-native-from /bound/extra/native`. Omit the native reuse flags to regenerate the native providers. Assertions must be enabled. Full verification used explicit source-bound native reuse; no fresh native replay or hosted CI success is claimed.

Conditional finite construction only. All-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape, exact recovery, analytic transfer, PR559 recurrence correction and PR589 bit H1-H5 assumptions remain. No unconditional theorem, full Lean certification, global packing optimum or independent human review is claimed.

Credits: Jeremy Kothe / PR1536, PR1479, PR1458, PR1444, PR1377, PR1274; PhilippeVV / PR1519 for finding the Mercator lower-bound bug; Rohan Arun / PR1485, PR1464, PR1424, PR1319, PR1297; Jeremy Diviney / PR1193; Thomas DiFiore / PR1148; Hao Yan; eumemic and icekylinx/Zhihao Chen; PR547/548/559 and PR589 suppliers. Prepared by Midhat / Antigravity with AI assistance. Apache-2.0; all predecessor notices retained.
