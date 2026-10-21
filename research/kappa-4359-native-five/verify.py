#!/usr/bin/env python3
"""Authenticate and delete the 102 unnecessary width-five helper topups.

The derivative word retains the pinned native controller and every adapter.
Only the listed rank-one residual calls and their rank-six output promises
are removed. Compilation of its weakly separated tariff is a separate proof.
Apache-2.0; predecessor construction is PR4359 by zxv and its credited sources.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
SOURCE_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
COVER = "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz"
HELPERS = "research/kappa-rebuild/complex/fresh-certificates/THREE-base-HELPER-BOUNDARIES.json.gz"
PINS = {
    COVER: "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f",
    "research/kappa-rebuild/controller/p3_native_cover.py": "fae71fcbbd20b9ee73b049cf6f43ea1d048217fb15feb6055a007e47da3363fe",
    "research/kappa-rebuild/transfer-audit/P3-COVER-AUDIT.json": "4a458dcbd47cc521fd826acd961d62af51e75a5da2ce56c6f1575de0b1f3ff17",
    "research/kappa-rebuild/transfer-audit/p3_cover_audit.py": "a0fe9a26f77556e83b31b0c91fea909d6f3d8209d0f9f7ad4e5bc1375d33615e",
}
MATH_CHECKER_SHA256 = "4a51eea1d796224e4a8bb6e2031146ba743e63ed88b2e7e241093a7025a063de"
NEW_TARGETS = {5: 102, 6: 90, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
NEW_PAID = {1: 17521, 2: 5065, 3: 1738, 4: 714, 5: 254}
ROOT_LOW = Q("0.002311660492818048695136925339")
ROOT_HIGH = Q("0.002311660492818048695136925340")
STAGE_DIRECTIONS = ("forward", "backward", "forward", "backward", "forward", "backward", "forward")
RELOCATIONS = {
    "research/kappa-next-regime/direct-decoder/native_common.py":
        "research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder/native_common.py",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def digest_json(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def authenticate(source_root):
    pins = dict(PINS)
    for relative, expected in pins.items():
        require(sha256((source_root/relative).read_bytes()).hexdigest() == expected, "changed pinned input: "+relative)
    original = read_json(source_root/COVER)
    require(original["generator_sha256"] == PINS["research/kappa-rebuild/controller/p3_native_cover.py"], "exact original native generator")
    for relative, expected in original["sources"].items():
        # IMPORT.json preserves this source under dependencies and restores its
        # historical path only in a replay tree. Either layout uses exact bytes.
        retained = relative if (source_root/relative).is_file() else RELOCATIONS.get(relative, relative)
        require(sha256((source_root/retained).read_bytes()).hexdigest() == expected, "changed transitive native input: "+relative)
        pins[retained] = expected
    for name, expected in original["immutable_phase_sources"].items():
        relative = "research/kappa-next-regime/direct-decoder/sources/"+name
        retained = relative if (source_root/relative).is_file() else "research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder/sources/"+name
        require(sha256((source_root/retained).read_bytes()).hexdigest() == expected, "changed immutable phase source: "+name)
        pins[retained] = expected
    return original, read_json(source_root/HELPERS), pins


def rewrite_cover(original, helpers):
    """Return an exact source-relative native patch and the changed cover."""
    source = original["cover"]
    changed = deepcopy(source)
    recipes = {row["role"]: row for row in helpers["recipes"]}
    bindings = defaultdict(list)
    for row in source["helper_bindings"]:
        bindings[row["owner"]].append(row)
    fresh = {row["owner"]: row for row in source["fresh_outputs"]}
    require(len(fresh) == 1570, "fresh arbitrary output owners are distinct")
    all_residuals = defaultdict(list)
    for row in source["paid_residuals"]:
        all_residuals[row["owner"]].append(row)
    selected = {owner: row for owner, row in fresh.items() if row["native_width"] == 5}
    require(len(selected) == 102, "actual native census contains 102 width-five fresh outputs")
    removed = []
    witnesses = []
    for owner, output in sorted(selected.items()):
        require(output["target_rank"] == 6, "original output promise is width six")
        require(len(bindings[owner]) == 1, "fresh field is used by exactly one global local call")
        binding = bindings[owner][0]
        stage, role = binding["stage"], binding["role"]
        require(owner == f"G{stage}:{role}" and binding["kind"] == "fresh", "fresh field is not a main or copied-center field")
        require(output["stage"] == stage and binding["width"] == 5, "same single-stage native-width-five output")
        require(binding["axes"] == [1, 2, 4, 8, 16], "actual canonical five-axis embedding")
        require(len(all_residuals[owner]) == 1, "there is no other residual use of this fresh field")
        residual = all_residuals[owner][0]
        require(residual == {"owner": owner, "after_stage": stage, "axes": [32], "rank": 1, "kind": "fresh_topup"},
                "the removed operation is precisely its independent sixth-axis rank-one topup")
        require(not (set(binding["axes"]) & set(residual["axes"])), "topup axis is disjoint from native output axes")
        coordinate = source["owner_coordinate_maps"][binding["coordinate_map"]]
        require(coordinate["columns"] == coordinate["inverse_rows"] == [1 << j for j in range(57)],
                "fresh five-axis embedding leaves the sixth coordinate and all spectators unchanged")
        contract = binding["whole_helper_boundary"]
        require(contract["direction"] == STAGE_DIRECTIONS[stage] and contract["role"] == role
                and contract["provider"] == "THREE-base", "the exact oriented normalizer is retained")
        recipe = recipes[role]
        require(recipe["width"] == 5, "source native recipe has width five")
        normal = recipe["certificate"]["directions"][contract["direction"]]["existing_native_boundary_normal_form"]
        require(normal["rank"] == normal["factorization"]["rank"] == 5 and normal["exact_tableau_and_global_phase"],
                "pinned complete helper endpoint has its rank-five native normal form")
        require(not any(row["owner"] == owner for row in source["windows"]), "fresh field owns no main idle window")
        removed.append(deepcopy(residual))
        witnesses.append({"owner": owner, "stage": stage, "native_role": role, "direction": contract["direction"],
                          "native_axes": binding["axes"], "deleted_axis": 32,
                          "native_normal_form_sha256": digest_json(normal)})
    removed_owners = set(selected)
    changed["paid_residuals"] = [row for row in changed["paid_residuals"] if row["owner"] not in removed_owners]
    for row in changed["fresh_outputs"]:
        if row["owner"] in removed_owners:
            row["target_rank"] = 5
    targets = Counter({25: 448, 57: 224})
    targets.update(row["target_rank"] for row in changed["fresh_outputs"])
    paid = Counter({int(k): int(v) for k, v in source["paid"].items()})
    paid.subtract(row["rank"] for row in removed)
    changed["targets"] = dict(sorted(targets.items()))
    changed["paid"] = dict(sorted(paid.items()))
    validate_patch(source, changed, removed)
    return changed, removed, witnesses


def validate_patch(source, changed, removed):
    owners = {row["owner"] for row in removed}
    require(len(owners) == len(removed) == 102, "each of 102 calls is removed exactly once")
    require(Counter(row["after_stage"] for row in removed) == {0: 9, 1: 28, 3: 28, 5: 9, 6: 28}, "exact chronological removal census")
    require(all(row in source["paid_residuals"] and row["rank"] == 1 and row["kind"] == "fresh_topup" for row in removed),
            "all removed calls occur in the literal original residual word")
    remaining = [row for row in source["paid_residuals"] if row not in removed]
    require(changed["paid_residuals"] == remaining, "every other residual stays in order")
    require(len(source["fresh_outputs"]) == len(changed["fresh_outputs"]), "all arbitrary productive fields are retained")
    for old, new in zip(source["fresh_outputs"], changed["fresh_outputs"]):
        expected = dict(old)
        if old["owner"] in owners:
            expected["target_rank"] = 5
        require(new == expected, "removed sixth-axis call cannot retain an unearned rank-six endpoint")
    untouched = set(source)-{"paid_residuals", "fresh_outputs", "targets", "paid"}
    require(all(source[key] == changed[key] for key in untouched), "all native bindings, maps, windows, and owned storage are unchanged")
    require(changed["targets"] == NEW_TARGETS and changed["paid"] == NEW_PAID, "complete adjusted invoice")
    require(sum(k*v for k, v in NEW_TARGETS.items())-sum(k*v for k, v in NEW_PAID.items()) == 224, "rank surplus is preserved")
    require(sum(NEW_TARGETS.values()) == source["productive_fields"] == 2242, "no new productive output credit")
    require(max(NEW_PAID) == min(NEW_TARGETS) == 5 < max(NEW_TARGETS), "weak separation is explicit")


def interval_engine():
    path = HERE.parent/"kappa-4359-outer-endpoint/verify.py"
    require(sha256(path.read_bytes()).hexdigest() == MATH_CHECKER_SHA256, "reviewed exact interval checker source")
    spec = importlib.util.spec_from_file_location("frozen_outer_intervals", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(source_root):
    original, helpers, pins = authenticate(source_root)
    changed, removed, witnesses = rewrite_cover(original, helpers)
    engine = interval_engine()
    lo = engine.mixed_margin(NEW_TARGETS, NEW_PAID, ROOT_LOW)
    hi = engine.mixed_margin(NEW_TARGETS, NEW_PAID, ROOT_HIGH)
    require(lo[0] > 0 and hi[1] < 0, "exact enclosure of the improved local mixed root")
    tested = engine.mixed_margin(NEW_TARGETS, NEW_PAID, Q("0.00231166"))
    require(tested[0] > 0, "strict moment for the proposed weakly separated compiler")
    controls = {}
    mutations = {}
    unearned = deepcopy(changed)
    next(row for row in unearned["fresh_outputs"] if row["owner"] == removed[0]["owner"])["target_rank"] = 6
    mutations["unearned_sixth_axis_rejected"] = (unearned, removed)
    unpaid = deepcopy(changed)
    unpaid["paid"][5] -= 1
    mutations["unpaid_rank_five_work_rejected"] = (unpaid, removed)
    mutations["duplicate_removal_rejected"] = (changed, removed+[removed[0]])
    for name, (candidate, deletions) in mutations.items():
        try:
            validate_patch(original["cover"], candidate, deletions)
        except AssertionError:
            controls[name] = True
        else:
            raise AssertionError("negative control accepted: "+name)
    conservative_scalar = original["scalar_invoice"]["conservative_real_scalar_primitive_allowance"]
    require(conservative_scalar == 1147304, "retained full scalar allowance")
    old_targets = {int(k): int(v) for k, v in original["cover"]["targets"].items()}
    old_paid = {int(k): int(v) for k, v in original["cover"]["paid"].items()}
    target_mass_before = sum(k*v for k, v in old_targets.items())
    paid_mass_before = sum(k*v for k, v in old_paid.items())
    target_mass_after = sum(k*v for k, v in NEW_TARGETS.items())
    paid_mass_after = sum(k*v for k, v in NEW_PAID.items())
    all_rank = 57*2242
    old_complements, new_complements = all_rank-target_mass_before, all_rank-target_mass_after
    require(new_complements-old_complements == paid_mass_before-paid_mass_after == 102,
            "deleted topups reappear in source complement rank at depth zero")
    require(old_complements+paid_mass_before == new_complements+paid_mass_after == 127570,
            "one-unit rank57 full completion receives no fictitious free gain")
    return {
        "schema": "native-width-five-topup-deletion/1",
        "status": "PASS_LITERAL_NATIVE_DELETION_AND_EXACT_IMPROVED_MIXED_ROOT",
        "source_commit": SOURCE_COMMIT, "source_sha256": pins,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"README.md").read_bytes()).hexdigest(),
        "interval_checker_sha256": MATH_CHECKER_SHA256,
        "removed_topups": removed, "native_endpoint_witnesses": witnesses,
        "removed_by_stage": dict(sorted(Counter(row["after_stage"] for row in removed).items())),
        "new_profile": {"targets": NEW_TARGETS, "paid": NEW_PAID,
                        "rank_surplus": 224, "productive_fields": 2242,
                        "owned_center_fields": changed["owned_center_fields"],
                        "conservative_real_scalar_allowance": conservative_scalar},
        "depth_zero_full_rank_check": {
            "ambient_rank": 57, "productive_fields": 2242,
            "old_target_rank_mass": target_mass_before, "new_target_rank_mass": target_mass_after,
            "old_paid_rank_mass": paid_mass_before, "new_paid_rank_mass": paid_mass_after,
            "old_source_complement_rank_mass": old_complements,
            "new_source_complement_rank_mass": new_complements,
            "unchanged_complete_rank_one_leaf_count": 127570,
            "interpretation": "All complements and paid jobs are below rank57 and use the sequential base programs. Lower-rank productive outputs do not receive free completion credit."},
        "derived_cover_sha256": digest_json(changed),
        "unchanged_component_sha256": {key: digest_json(original[key]) for key in
            ("main_contacts", "main_endpoint_normalizers", "native_local_contract", "physical_order", "scalar_invoice")},
        "root_bracket": [str(ROOT_LOW), str(ROOT_HIGH)],
        "root_endpoint_margins": [[str(v) for v in lo], [str(v) for v in hi]],
        "tested_mixed_saving": "0.00231166", "tested_mixed_margin": [str(v) for v in tested],
        "controls": controls,
        "operator_argument": "For each listed fresh arbitrary field, retain the normalized native rank-five endpoint and delete its standalone rank-one call on the disjoint sixth axis. Every other operation is retained. This gives a finite derivative of the same all-column native word.",
        "remaining_obligations": [
            "The prior compiler's strict r_max<k_min condition fails; use the separately proved weak-separation extension.",
            "An outer kappa needs that compiler, a sufficient finite rank, fresh template constants, and all inherited native and analytic hypotheses.",
            "The source-bound native operator contracts retain the scope of PR4359; finite receipts are not a formal proof of them.",
        ],
        "new_kappa_claimed_by_this_file": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", "--check-only", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE/"CERTIFICATE.json").read_text() == text, "committed native-five certificate differs from replay")
    print(json.dumps({"status": result["status"], "removed_calls": len(result["removed_topups"]),
                      "new_profile": result["new_profile"], "root_bracket": result["root_bracket"]}, sort_keys=True))


if __name__ == "__main__":
    main()
