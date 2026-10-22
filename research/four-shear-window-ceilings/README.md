# Finite four-shear ceilings on receiver windows

Assignment B independently screens the same first twelve source-indexed receiver windows as fork PR15, but covers every word of at most four unit shears on the three persistent fields rather than only the three-shear receiver identity. The construction checker is not imported. No new kappa, global ceiling, or physical attainability claim is made. The actual source-bound outcome must be read from the hosted replay.

## Alphabet and complete census

There are twelve generators y_i += sign*y_j, i != j, sign in {-1,1}. The checker enumerates every word of lengths zero through four, including cancellations, so it visits 1+12+144+1728+20736=22621 words. It compares exact integer 3 by 3 endpoint matrices with a += ca*x; b += cb*x. For each of the four sign choices exactly 84 words match: two of length two, two of length three and eighty of length four. No heuristic pruning or floating-point equality is used.

## Optimistic geometry theorem

For each endpoint-matching word, propagate mandatory lower subspaces forward. At a contact of fields i,j, every legal common frame must contain the sum of their current lower subspaces; update both lower bounds to that sum. Propagate upper subspaces backwards from the three fixed exits, replacing the bounds of both operands by their intersection. Induction shows every genuinely legal monotone frame path satisfies L_j contained in F_j contained in U_j at every contact. If L_j is not contained in U_j, that word is impossible under this contract.

For surviving words, enumerate every integer contact dimension between dim(L_j) and dim(U_j), subject to nondecreasing dimensions along each operand's path and the fixed terminal dimensions. Charge both operands' positive entrance/intermediate gaps, and every remaining exit gap. The sum of charged ranks must equal the total terminal-minus-entrance rank mass. This deliberately forgets some simultaneous subspace-incidence constraints. It can admit extra profiles, never remove an actual legal path. Therefore the minimum relaxed paid moment is a lower bound on every legal implementation's cost, and old cost minus that lower bound is a rigorous optimistic ceiling on local savings.

The checker keeps all distinct relaxed profiles and bounds every signed old-minus-new difference with directed rational intervals. Identical profiles are exactly equal, not a floating-point near-zero gain. The powers are obtained independently of PR15 by binary-reduced logarithms and an alternating expansion of r*exp(-C log r), at C=0.00302015. The output marks no-strict-gain only when every upper gain bound is nonpositive. A positive optimistic profile is not an attainable circuit.

## Exact source and validation

The original pinned constructor emits the forward word only; no predecessor proof engine or PR15 acceptance routine is called. The window extraction independently follows the actual field demands and fixes each next required frame. Both old scalar operations are adjacent in the nontransport chronological word. No productive helper endpoint, warp or external operation is changed. Individual window ceilings must not be added when windows overlap or share resources.

Seven live sources are pinned by Git blob and SHA256 on canonical f9f85c1e4fa1e955ff39f10fca447e3e2a4e4adc, corresponding to PR4470 b9a13c1673e0e9697de410de16e8bbf3207a7363. Python 3.12, standard library only:

```sh
python -B scripts/research_package.py --package research/four-shear-window-ceilings
python -I -O -B research/four-shear-window-ceilings/verify.py --self-test
```

Local normal and optimised controls check the four complete scalar censuses, all 68 legal small geometric paths in the declared toy domain, required terminal charges, incompatible exits and exact equal-invoice handling. The written relaxation argument justifies the bound beyond those toy cases. The historical baseline helper and a full native/outer replay were not run.

## Task and overlap

This is the user's ceiling assignment, refined from independent-moment and complementary to PR15's construction. PR4121 searches older T360 sources; this uses PR4470's productive-helper boundaries. The old #4091 fixed-inventory ceiling is not applied to this changed mechanism. New #4529/#4532/#4533 concern the compiler. Searches were targeted, not exhaustive overlap pagination or a novelty certificate. No frozen inputs or selected record change.

## Open next questions

If a window has no headroom, change the alphabet, length cap, adjacency or boundary contract explicitly before expanding. If the relaxation leaves headroom, first realise one optimistic profile by actual nested common frames and charge the complete word in both orientations. Do not treat the relaxed profile as a construction or sum overlapping gains. TASK.json records the first step and blockers.

## Credit

Credit zxv's receiver-sharing and productive-helper work, Cinna Davis's PR4470, Jacob Alan Sussman, GamingPuzzled's earlier finite census and the retained native/geometry/Clifford/outer contributors. The source constructor is inherited generation; the scalar enumeration, relaxation and interval checker are separately implemented here for Chris R / Clear1nsight with substantial OpenAI assistance, Apache-2.0. Separate workstreams do not imply independently launched agents or human/formal acceptance.
