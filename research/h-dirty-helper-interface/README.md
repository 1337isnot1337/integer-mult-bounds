# Concentrate the H defect into eight arbitrary state ports

Prepared for Cinna Davis with OpenAI assistance. Apache-2.0. Retains Cinna Davis's PR4470 supplier and H completion, zxv's native/Clifford framework, Jacob Alan Sussman's mixed-target work, and the cumulative source credits in sources/README.md.

## Verified local construction

Removing the zero-frame compensation from the retained H word exposes a rank-eight defect. Forward execution sends helper-input contamination into 112 main Y outputs. Backward execution sends the negative transpose defect into 106 helper outputs. Every affected helper has the same physical input frame zero and output frame full nine.

An integer unimodular change of basis concentrates this defect into helper roles 224 through 231. The change uses 553 elementary column operations. A Euclidean elimination avoids division by odd pivots; its implementation uses integer shears and swaps only. Each swap is emitted as actual scalar operations.

Forward input uses T and output uses T^-1. Backward input uses T^-transpose and output uses T^transpose. All input operations occur at common frame zero, and output operations at common full frame nine. Consequently the remaining 400 helpers retain their original independent Gaussian interfaces. These include 318 clean rank-nine helpers. The eight selected fields are arbitrary state inputs, NOT eight clean productive outputs of the new coupled interface.

The emitted word is EIGHT-STATE-WORD.json.gz. Both orientations are replayed on all 632 persistent columns, including arbitrary owned input and final owned cleanup. All changes are checked against the retained clean H endpoint. Forward contamination is supported only from the eight state inputs to main Y outputs; backward contamination is its exact negative transpose from main Y inputs to the eight state outputs.

Every paid bridge, native warp and owned-center event remains literally identical and in the same order as the retained H word. Only scalar operations change. Thus the complete recursive profile remains:

    {1:2245, 2:388, 3:494, 4:147, 5:36}.

No new physical bridge or warp phase pair is introduced. Phase admission is inherited from the retained H source and its original unchanged dependencies; it is not rerun here. Scalar allowances are 171116 in each orientation. Measured prefix row-l1 bounds are 5274 forward and 2384 backward; denominator bounds are 32 and 64 respectively. These finite values are not a complete rounding or outer-transfer proof.

## A separate rectangular algebraic target

Write the uncompleted symmetric kernel as J=I-R^transpose R/4, where R R^transpose=56I_8. Exact rational checks give

    J^2 - 3 R^transpose R = I_112.

The concentrated defect basis changes to R^transpose by a matrix E for which both E and E^-1 are dyadic. This suggests a sixteen-state interface with

    A = [J, R^transpose, 2 R^transpose],
    B = [J; R; -2 R],
    A B = I_112.

The coefficients use 1 and 2 with a sign change, not an unproved square root or division by three. A is 112-by-128 and B is 128-by-112. RECTANGULAR.json verifies this exact algebra and the dyadic basis matrices.

This is NOT an emitted sixteen-state native controller. Its state fields have width nine while the old main jobs have width eight. That mismatch, shared-head reuse, actual state restoration and all target credits must be resolved. A right-inverse matrix alone does not supply a legal recursive caller.

## Replay

From the repository root, with assertions enabled:

    python -B research/h-dirty-helper-interface/probe.py --check
    python -B research/h-dirty-helper-interface/concentrate.py --check
    python -B research/h-dirty-helper-interface/rectangular_probe.py --check

The first two commands authenticate included source snapshots. They reproduce the raw defect, actual integer basis operations, complete emitted word and receipts without modifying them. The third checks the separate rectangular algebra using the credited geometry source. Without --check the scripts regenerate their own artifacts. The registered package command runs these checks and the conditional cache budget: `python -B scripts/research_package.py --package research/h-dirty-helper-interface`. This is a scoped local replay, not the selected scientific cold replay.

## Conditional budget

CACHE-BUDGET.md and CACHE-BUDGET.json reprice explicitly hypothetical persistent-state scenarios. They distinguish disjoint helper axes from repeated head axes and never count coupled state outputs as restored targets. The eight-state word itself supplies no one-head boundary decoder.

## Open next questions

Can the eight-state interface be carried through the H controller without paying to recreate every response? Can the sixteen-state rectangular candidate be given compatible Gaussian widths and independent restored outputs? Reprice all linked state targets, including lost credit when repeated transforms share an axis. No new kappa follows until those obligations close.
