#!/usr/bin/env python3
"""Rebind the actual idle owners after admitting native rank-five outputs.

Every input is pinned before use. This constructs and checks the full
changed helper assignment, all residual calls, and the actual ordered
native paid word. The improved outer theorem is a separate certificate.
Apache-2.0; predecessor native construction: PR4359 and its source credits.
"""
from collections import Counter, defaultdict, deque
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
SOURCE_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
PREDECESSOR_GENERATOR = "20fb4742fbc8341ee799e0c6d0ebed981b86c17f763a900e539550a8f2b1cf1c"
PREDECESSOR_RECEIPT = "9a4036e30d38be476cd529b4aebba40270f719744c13a86efd9306892d903ed8"
NATIVE = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz"
FORMAL = "research/kappa-rebuild/bit/COMPLEX-CONTROLLER-FACTOR.json"
STAGES = ((0, "forward"), (0, "backward"), (0, "forward"),
          (1, "backward"), (1, "forward"), (2, "backward"), (2, "forward"))
STOCK = {5: 28, 6: 18, 7: 56, 8: 93, 9: 213}
PAIRS = ((93, 8, 8), (56, 7, 9), (56, 9, 7), (18, 6, 9), (1, 9, 6))
NEW_TARGETS = {5: 140, 6: 52, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
NEW_PAID = {1: 17559, 2: 5027, 3: 1738, 4: 714, 5: 254}
ROOT_LOW = Q("0.002312854665364207351198238279")
ROOT_HIGH = Q("0.002312854665364207351198238280")
TESTED = Q("0.00231285")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest_json(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_predecessor(source_root):
    path = HERE.parent/"kappa-4359-native-five/verify.py"
    require(sha256(path.read_bytes()).hexdigest() == PREDECESSOR_GENERATOR,
            "authenticated native-five source and transitive authentication routine")
    receipt_path = path.with_name("CERTIFICATE.json")
    require(sha256(receipt_path.read_bytes()).hexdigest() == PREDECESSOR_RECEIPT,
            "authenticated first native improvement receipt")
    spec = importlib.util.spec_from_file_location("frozen_native_five_for_packing", path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    original, helpers, pins = engine.authenticate(source_root)
    previous, removed, witnesses = engine.rewrite_cover(original, helpers)
    receipt = engine.read_json(receipt_path)
    require(digest_json(previous) == receipt["derived_cover_sha256"],
            "the new packing starts from the exact earlier native word")
    require(NATIVE in pins and FORMAL in pins, "actual local and chronological words are authenticated")
    return engine, original, previous, helpers, pins


def rank(vectors):
    basis = {}
    for vector in vectors:
        value = vector
        while value:
            pivot = value.bit_length()-1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def coordinate_map(axes, dimension=57):
    return cached_coordinate_map(tuple(axes), dimension)


@lru_cache(maxsize=None)
def cached_coordinate_map(axes, dimension):
    """Independent exact completion and inverse over GF(2)."""
    columns = list(axes)
    require(rank(columns) == len(columns), "new helper target axes are independent")
    for j in range(dimension):
        if rank(columns+[1 << j]) > len(columns):
            columns.append(1 << j)
    require(len(columns) == dimension, "new address map is a full ambient automorphism")
    rows = [sum(((column >> i) & 1) << j for j, column in enumerate(columns))
            for i in range(dimension)]
    augmented = [row | (1 << (dimension+i)) for i, row in enumerate(rows)]
    for j in range(dimension):
        pivot = next(i for i in range(j, dimension) if (augmented[i] >> j) & 1)
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        for i in range(dimension):
            if i != j and ((augmented[i] >> j) & 1):
                augmented[i] ^= augmented[j]
    require(all((row & ((1 << dimension)-1)) == 1 << i for i, row in enumerate(augmented)),
            "new address inverse is exact")
    return {"columns": columns, "inverse_rows": [row >> dimension for row in augmented]}


def split_axes(axes):
    return [axes[i:i+5] for i in range(0, len(axes), 5)]


def rebind_cover(previous, helpers):
    """Construct the literal new bindings, leaving the scalar controller fixed."""
    changed = deepcopy(previous)
    patterns = [[a, b] for count, a, b in PAIRS for _ in range(count)]
    require(len(patterns) == 224, "224 actual owners per wide window")
    families = defaultdict(list)
    for window in changed["windows"]:
        families[window["family"]].append(window)
    require(set(families) == {0, 1, 2, 3}, "four retained original idle families")
    for family in (0, 3):
        require(len(families[family]) == 224, "complete wide-family owner list")
        for window, pattern in zip(families[family], patterns):
            window["widths"] = list(pattern)

    pools = []
    for stage in range(7):
        pool = defaultdict(deque)
        for recipe in helpers["recipes"]:
            pool[recipe["width"]].append(recipe["role"])
        pools.append(pool)
    bindings, residuals, fresh = [], [], []
    for window in changed["windows"]:
        cursor = 0
        for stage, width in zip(window["stages"], window["widths"]):
            if not width:
                continue
            require(pools[stage][width], "the requested oriented helper exists at this stage")
            role = pools[stage][width].popleft()
            axes = window["axes"][cursor:cursor+width]
            require(len(axes) == width, "new helper slice fits wholly inside its idle window")
            cursor += width
            bindings.append({"stage": stage, "role": role, "width": width,
                             "owner": window["owner"], "axes": axes,
                             "kind": "original_idle", "window_index": window["index"]})
        for axes in split_axes(window["axes"][cursor:]):
            residuals.append({"owner": window["owner"], "after_stage": max(window["stages"]),
                              "axes": axes, "rank": len(axes), "kind": "idle_remnant"})
    for stage, pool in enumerate(pools):
        for width, roles in sorted(pool.items()):
            for role in roles:
                owner = f"G{stage}:{role}"
                bindings.append({"stage": stage, "role": role, "width": width, "owner": owner,
                                 "axes": [1 << j for j in range(width)], "kind": "fresh"})
                fresh.append({"owner": owner, "stage": stage, "native_width": width, "target_rank": width})
    coordinates = {}
    for row in bindings:
        key = ",".join(map(str, row["axes"]))
        if key not in coordinates:
            coordinates[key] = coordinate_map(row["axes"])
        row["coordinate_map"] = key
        row["whole_helper_boundary"] = {
            "provider": "THREE-base", "direction": STAGES[row["stage"]][1], "role": row["role"],
            "selector": "certificate.directions.direction.existing_native_boundary_normal_form"}
    changed.update(helper_bindings=bindings, paid_residuals=residuals, fresh_outputs=fresh,
                   owner_coordinate_maps=coordinates, targets=NEW_TARGETS, paid=NEW_PAID)
    return changed


def validate_cover(previous, changed, helpers):
    """Check full endpoints and inventories, independently of the pool algorithm."""
    require(len(changed["windows"]) == len(previous["windows"]) == 896,
            "every retained physical idle owner remains present")
    require(set(changed) == set(previous), "same complete native-cover interface")
    untouched = set(previous)-{"windows", "helper_bindings", "paid_residuals", "fresh_outputs",
                               "owner_coordinate_maps", "targets", "paid"}
    require(all(changed[key] == previous[key] for key in untouched),
            "main productive ranks, owned center, and external cleanup obligations are retained")
    changed_windows = []
    for index, (old, new) in enumerate(zip(previous["windows"], changed["windows"])):
        require({key: value for key, value in old.items() if key != "widths"}
                == {key: value for key, value in new.items() if key != "widths"},
                "whole-window operator, owner, chronological slot, axes and phase are unchanged")
        family, offset = divmod(index, 224)
        require(new["family"] == family, "window family order is unchanged")
        if old["widths"] != new["widths"]:
            require(family in (0, 3) and offset >= 205 and old["widths"] == [5, 9],
                    "only the final 19 old (5,9) wide owners change")
            require(new["widths"] == ([6, 9] if offset < 223 else [9, 6]),
                    "18 literal (6,9) owners and one literal (9,6) owner")
            changed_windows.append({"family": family, "offset": offset, "owner": new["owner"],
                                    "stages": new["stages"], "old_widths": old["widths"],
                                    "new_widths": new["widths"], "axes": new["axes"],
                                    "translation_after": new["translation_after"]})
    require(len(changed_windows) == 38, "exactly 38 rank-16 owner windows are repacked")

    recipes = {row["role"]: row for row in helpers["recipes"]}
    require(len(recipes) == 408 and Counter(row["width"] for row in recipes.values()) == STOCK,
            "exact complete actual local helper stock")
    bindings = changed["helper_bindings"]
    require(len(bindings) == 2856, "all 408 helpers in each of seven native calls are bound")
    by_stage_owner, by_stage_role, by_owner = {}, {}, defaultdict(list)
    normalizers = []
    for row in bindings:
        stage, owner, role, width = row["stage"], row["owner"], row["role"], row["width"]
        require((stage, owner) not in by_stage_owner and (stage, role) not in by_stage_role,
                "no same-stage physical owner alias and no reused local helper role")
        by_stage_owner[stage, owner] = row
        by_stage_role[stage, role] = row
        by_owner[owner].append(row)
        require(role in recipes and recipes[role]["width"] == width == len(row["axes"]),
                "literal native role has precisely the advertised hosted rank")
        require(all(0 < axis < 1 << 57 for axis in row["axes"]), "every view stays within ambient rank57")
        contract = row["whole_helper_boundary"]
        require(contract == {"provider": "THREE-base", "direction": STAGES[stage][1], "role": role,
                             "selector": "certificate.directions.direction.existing_native_boundary_normal_form"},
                "same source-bound oriented whole-helper normalizer")
        normal = recipes[role]["certificate"]["directions"][STAGES[stage][1]]["existing_native_boundary_normal_form"]
        require(normal["rank"] == normal["factorization"]["rank"] == width
                and normal["exact_tableau_and_global_phase"],
                "all original native helper endpoints retain full rank and phase certificates")
        normalizers.append((stage, role, digest_json(normal)))
        key = row["coordinate_map"]
        require(key == ",".join(map(str, row["axes"]))
                and changed["owner_coordinate_maps"][key] == coordinate_map(row["axes"]),
                "every new physical view is an explicit full invertible conjugation")
    for stage, (pair, direction) in enumerate(STAGES):
        require({role for s, role in by_stage_role if s == stage} == set(range(224, 632)),
                "every exact local helper role appears once at each stage")
        active = {f"{side}{pair}:{port}" for side in ("X", "Y") for port in range(112)}
        require(active.isdisjoint(owner for s, owner in by_stage_owner if s == stage),
                "a live main input is never used as a helper")
    # Every hosted endpoint and every paid idle complement must partition the
    # unchanged ordered whole-window axes. This distinguishes a paid rebind
    # from a histogram-only rank exchange.
    expected_residuals = []
    idle_keys = set()
    for window in changed["windows"]:
        consumed = []
        for stage, width in zip(window["stages"], window["widths"]):
            if not width:
                require((stage, window["owner"]) not in by_stage_owner,
                        "an empty window slot has no hidden helper use")
                continue
            key = (stage, window["owner"])
            require(key in by_stage_owner and key not in idle_keys,
                    "each hosted call has a unique literal idle-window slot")
            idle_keys.add(key)
            row = by_stage_owner[key]
            require(row["kind"] == "original_idle" and row["window_index"] == window["index"]
                    and row["width"] == width,
                    "the bound field, stage, window and native width agree")
            require(row["axes"] == window["axes"][len(consumed):len(consumed)+width],
                    "hosted helper takes exactly its ordered disjoint axis slice")
            consumed += row["axes"]
        remaining = window["axes"][len(consumed):]
        require(len(consumed) <= len(window["axes"]) and rank(window["axes"]) == len(window["axes"]),
                "the complete idle axes remain independent and fully accounted")
        for axes in split_axes(remaining):
            expected_residuals.append({"owner": window["owner"], "after_stage": max(window["stages"]),
                                       "axes": axes, "rank": len(axes), "kind": "idle_remnant"})
    require(changed["paid_residuals"] == expected_residuals,
            "all remaining window axes receive their exact ordered paid calls")
    fresh = {row["owner"]: row for row in changed["fresh_outputs"]}
    require(len(fresh) == len(changed["fresh_outputs"]) == 1570,
            "the new device has exactly 1570 distinct fresh arbitrary productive fields")
    window_owners = {row["owner"] for row in changed["windows"]}
    for owner, output in fresh.items():
        require(owner not in window_owners and len(by_owner[owner]) == 1,
                "each fresh arbitrary field is used by exactly one helper and by no idle window")
        row = by_owner[owner][0]
        require(owner == f"G{row['stage']}:{row['role']}" and row["kind"] == "fresh",
                "fresh native role identity is explicit")
        require(output == {"owner": owner, "stage": row["stage"],
                           "native_width": row["width"], "target_rank": row["width"]},
                "fresh outputs receive exactly their autonomous native endpoint ranks")
        require(row["axes"] == [1 << j for j in range(row["width"])],
                "fresh arbitrary endpoint uses the canonical positive native axes")
    require({(row["stage"], row["owner"]) for row in bindings if row["kind"] == "original_idle"} == idle_keys,
            "no hidden idle call lies outside the complete window list")
    require(set(by_owner)-window_owners == set(fresh), "there are no extra unaccounted helper fields")
    targets = Counter({25: 448, 57: 224})
    targets.update(row["target_rank"] for row in fresh.values())
    require(dict(sorted(targets.items())) == changed["targets"] == NEW_TARGETS,
            "the actual native owner reconstruction earns the complete changed target histogram")
    require(sum(targets.values()) == changed["productive_fields"] == 2242,
            "all arbitrary main and fresh source arrays are counted")
    return changed_windows, digest_json(sorted(normalizers))


def reconstruct_word(original, changed, native_word, formal):
    events = [event for event in formal["physical_events"] if event[0] == "LOCAL"]
    require([(row[2], "backward" if row[3] else "forward") for row in events] == list(STAGES)
            and [row[1] for row in events] == list(range(7)),
            "the retained formal controller has the same seven literal native stages")
    rounds, stage_rows = [], []
    for stage, (pair, direction) in enumerate(STAGES):
        helper = {row["role"]: row["owner"] for row in changed["helper_bindings"] if row["stage"] == stage}
        begin = len(rounds)
        for event in native_word[direction]:
            if event[0] == "climb":
                role = event[2]
                owner = (f"X{pair}:{role}" if role < 112 else f"Y{pair}:{role-112}" if role < 224 else helper[role])
                rounds.append((event[-1], owner))
            elif event[0] == "center":
                rounds.append((event[-1], "owned-C0"))
        rounds.extend((row["rank"], row["owner"]) for row in changed["paid_residuals"] if row["after_stage"] == stage)
        stage_rows.append({"stage": stage, "pair": pair, "direction": direction,
                           "paid": dict(sorted(Counter(rank for rank, owner in rounds[begin:]).items())),
                           "owned_center_calls": sum(owner == "owned-C0" for rank, owner in rounds[begin:])})
    paid = Counter(rank for rank, owner in rounds)
    require(dict(sorted(paid.items())) == changed["paid"] == NEW_PAID,
            "every actual native paid event and every remaining residual is charged")
    require(len(rounds) == 25292 and all(row["owned_center_calls"] > 0 for row in stage_rows),
            "the full chronological word retains all paid work on its owned center")
    return rounds, stage_rows


def build(source_root):
    engine, original, previous, helpers, pins = load_predecessor(source_root)
    changed = rebind_cover(previous, helpers)
    windows, normalizers_hash = validate_cover(previous, changed, helpers)
    native = engine.read_json(source_root/NATIVE)
    formal = engine.read_json(source_root/FORMAL)["selected_p3_keep43"]
    rounds, stages = reconstruct_word(original, changed, native, formal)
    intervals = engine.interval_engine()
    low = intervals.mixed_margin(NEW_TARGETS, NEW_PAID, ROOT_LOW)
    high = intervals.mixed_margin(NEW_TARGETS, NEW_PAID, ROOT_HIGH)
    tested = intervals.mixed_margin(NEW_TARGETS, NEW_PAID, TESTED)
    require(low[0] > 0 and high[1] < 0 and tested[0] > 0,
            "exact new mixed root enclosure and positive tested saving")
    old_targets = {int(k): int(v) for k, v in previous["targets"].items()}
    old_paid = {int(k): int(v) for k, v in previous["paid"].items()}
    require({k: NEW_TARGETS.get(k, 0)-old_targets.get(k, 0) for k in set(NEW_TARGETS)|set(old_targets)}
            == {5: 38, 6: -38, 7: 0, 8: 0, 9: 0, 25: 0, 57: 0}, "exact changed productive ranks")
    require({k: NEW_PAID.get(k, 0)-old_paid.get(k, 0) for k in set(NEW_PAID)|set(old_paid)}
            == {1: 38, 2: -38, 3: 0, 4: 0, 5: 0}, "exact changed paid ranks")
    target_mass = sum(k*v for k, v in NEW_TARGETS.items())
    paid_mass = sum(k*v for k, v in NEW_PAID.items())
    complements = 57*2242-target_mass
    require(target_mass-paid_mass == 224 and complements+paid_mass == 127570,
            "the complete rank57 leaf count still includes every source complement")
    require(complements-(57*2242-sum(k*v for k, v in old_targets.items())) == 38,
            "the 38 lowered endpoint ranks are charged as 38 additional source complements")
    require(max(NEW_PAID) == min(NEW_TARGETS) == 5 < max(NEW_TARGETS), "weak separation remains explicit")
    normalizers_old = []
    recipe_by_role = {row["role"]: row for row in helpers["recipes"]}
    for row in previous["helper_bindings"]:
        stage, role = row["stage"], row["role"]
        normal = recipe_by_role[role]["certificate"]["directions"][STAGES[stage][1]]["existing_native_boundary_normal_form"]
        normalizers_old.append((stage, role, digest_json(normal)))
    require(digest_json(sorted(normalizers_old)) == normalizers_hash,
            "the full oriented native normalizer multiset and its scalar allowance are unchanged")
    controls = {}
    overdraw = deepcopy(changed)
    first = overdraw["helper_bindings"][0]
    other = next(row for row in overdraw["helper_bindings"][1:]
                 if row["stage"] == first["stage"] and row["role"] != first["role"])
    first["role"] = other["role"]
    unpaid = deepcopy(changed)
    unpaid["paid_residuals"].pop()
    unearned = deepcopy(changed)
    next(row for row in unearned["fresh_outputs"] if row["native_width"] == 5)["target_rank"] = 6
    overlap = deepcopy(changed)
    selected = next(row for row in overlap["helper_bindings"] if row["owner"] == windows[0]["owner"] and row["stage"] == windows[0]["stages"][1])
    selected["axes"][0] = windows[0]["axes"][0]
    for name, candidate in (("duplicate_native_role_rejected", overdraw), ("unpaid_idle_axis_rejected", unpaid),
                            ("unearned_fresh_sixth_axis_rejected", unearned), ("overlapping_hosted_axes_rejected", overlap)):
        try:
            validate_cover(previous, candidate, helpers)
        except (AssertionError, KeyError):
            controls[name] = True
        else:
            raise AssertionError("negative control accepted: "+name)
    return {
        "schema": "native-weak-idle-packing/1",
        "status": "PASS_LITERAL_REPACKING_FULL_NATIVE_INVOICE_AND_EXACT_MIXED_ROOT",
        "source_commit": SOURCE_COMMIT, "source_sha256": pins,
        "predecessor_receipt_sha256": PREDECESSOR_RECEIPT,
        "predecessor_generator_sha256": PREDECESSOR_GENERATOR,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"README.md").read_bytes()).hexdigest(),
        "wide_patterns": [list(row) for row in PAIRS], "changed_windows": windows,
        "new_profile": {"targets": NEW_TARGETS, "paid": NEW_PAID, "productive_fields": 2242,
                        "owned_center_fields": 1, "rank_surplus": 224,
                        "conservative_real_scalar_allowance": original["scalar_invoice"]["conservative_real_scalar_primitive_allowance"]},
        "paid_word": {"rounds": len(rounds), "sha256": digest_json(rounds), "stages": stages},
        "normalizer_multiset_sha256": normalizers_hash,
        "derived_cover_sha256": digest_json(changed),
        "depth_zero_full_rank_check": {"ambient_rank": 57, "productive_fields": 2242,
            "target_rank_mass": target_mass, "paid_rank_mass": paid_mass,
            "source_complement_rank_mass": complements, "additional_source_complements": 38,
            "unchanged_complete_rank_one_leaf_count": complements+paid_mass},
        "root_bracket": [str(ROOT_LOW), str(ROOT_HIGH)],
        "root_endpoint_margins": [[str(v) for v in low], [str(v) for v in high]],
        "tested_mixed_saving": str(TESTED), "tested_mixed_margin": [str(v) for v in tested],
        "paid_integer_moments": {"P1": paid_mass, "P2": sum(k*k*v for k, v in NEW_PAID.items()),
                                  "P2_minus_2P1": sum(k*(k-2)*v for k, v in NEW_PAID.items())},
        "controls": controls,
        "conditional_scope": [
            "The prior autonomous native helper endpoints, complete all-column local word and physical adapter contracts retain their source-bound scope.",
            "All original main contact maps, idle-window phases, endpoint normalizers, scalar controller operations, and the owned center remain fixed.",
            "The new whole-helper coordinate maps are exact fixed GF(2) address automorphisms and have their own finite movement bill.",
            "No global optimality of the packing is claimed. Numerical search is not an input to this exact checker.",
            "The weak compiler, finite uniform rank, generic fixed-template constants, and outer analytic transfer are separate obligations.",
        ],
        "new_kappa_claimed_by_this_file": False,
    }, changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--cover-out", type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", "--check-only", action="store_true")
    args = parser.parse_args()
    result, cover = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE/"CERTIFICATE.json").read_text() == text, "committed native packing receipt differs from replay")
    if args.cover_out:
        args.cover_out.write_text(json.dumps(cover, indent=2, sort_keys=True)+"\n")
    print(json.dumps({key: result[key] for key in ("status", "new_profile", "root_bracket",
                                                "paid_integer_moments", "depth_zero_full_rank_check")}, sort_keys=True))


if __name__ == "__main__":
    main()
