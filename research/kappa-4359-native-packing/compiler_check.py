#!/usr/bin/env python3
"""Compile the actual repacked native rule with every paid owner retained.

The authenticated packing producer is used only to reconstruct its exact
cover. This checker independently extracts main/fresh roles, paid owners,
and controller chronology, then runs the frozen finite compiler at rank57.
Apache-2.0. Native word and original compiler: PR4359.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
PRODUCER_HASH = "9edf27738981b58c2bf8ca03bb70631c200aad0ca9948372f1c58fc445894da0"
NATIVE_RECEIPT_HASH = "5c8cc831151aa7147e6c3dd2a6832d19026aecc660955131149bdc54f0b26878"
WEAK_HASH = "33d43a20a55e3eb6200abb478f3ef9bcd3d866233cacd7930d15c87fa0759605"
NATIVE = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz"
FORMAL = "research/kappa-rebuild/bit/COMPLEX-CONTROLLER-FACTOR.json"
TARGETS = {5: 140, 6: 52, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17559, 2: 5027, 3: 1738, 4: 714, 5: 254}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest_json(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(path, expected, name):
    require(sha256(path.read_bytes()).hexdigest() == expected, "authenticated program: "+str(path.name))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check_chronology(events, cover):
    """An incomplete borrowed field cannot be read before its exact IDLE."""
    local = {event[1]: i for i, event in enumerate(events) if event[0] == "LOCAL"}
    require(set(local) == set(range(7)), "all seven local stages occur")
    families = {}
    for window in cover["windows"]:
        pair, stages = window["pair"], window["stages"]
        matches = [i for i, event in enumerate(events) if event == ["IDLE", pair, stages]]
        require(len(matches) == 1, "the original whole-window completion occurs exactly once")
        ending = matches[0]
        first = local[min(stages)]
        require(first <= local[max(stages)] < ending, "all hosted calls precede their complete idle endpoint")
        require(window["owner"] == f"{window['side']}{pair}:{window['port']}",
                "the checked controller pair is the actual borrowed physical owner")
        for event in events[first:ending]:
            if event[0] == "LOCAL":
                require(event[2] != pair, "an incomplete idle owner is never an active local input")
            elif event[0] == "ADD":
                require(event[1]//2 != pair and event[2]//2 != pair,
                        "no scalar bridge reads or writes an incomplete idle owner")
            elif event[0] == "SIGNED_SWAP":
                require(event[1]//2 != pair and event[2]//2 != pair,
                        "no signed swap touches an incomplete idle owner")
            elif event[0] == "IDLE":
                require(event[1] != pair, "no second completion intervenes on the same idle owner")
            else:
                raise AssertionError("unknown controller operation in an idle lifetime")
        families[window["family"]] = {"pair": pair, "stages": stages,
                                       "first_event": first, "complete_event": ending}
    require(len(families) == 4, "all four original idle families are checked")
    return families


def build(source_root):
    producer = load(HERE/"verify.py", PRODUCER_HASH, "authenticated_packing_producer")
    receipt_path = HERE/"CERTIFICATE.json"
    require(sha256(receipt_path.read_bytes()).hexdigest() == NATIVE_RECEIPT_HASH,
            "authenticated complete native packing certificate")
    receipt = json.loads(receipt_path.read_text())
    require(receipt["source_commit"] == COMMIT and receipt["generator_sha256"] == PRODUCER_HASH,
            "the native certificate binds the selected producer and immutable predecessor")
    weak = load(HERE.parent/"kappa-4359-weak-compiler/verify.py", WEAK_HASH,
                "packing_weak_compiler_interface")
    frozen = weak.load_original(source_root)
    native_engine, original, previous, helpers, pins = producer.load_predecessor(source_root)
    cover = producer.rebind_cover(previous, helpers)
    require(digest_json(cover) == receipt["derived_cover_sha256"],
            "the complete reconstructed cover is exactly the independently reviewed native artifact")
    require({int(k): v for k, v in receipt["new_profile"]["targets"].items()} == TARGETS
            and {int(k): v for k, v in receipt["new_profile"]["paid"].items()} == PAID,
            "this integration uses the exact new profile")
    require(NATIVE in pins and FORMAL in pins, "both actual instruction words were authenticated")
    native = native_engine.read_json(source_root/NATIVE)
    formal = native_engine.read_json(source_root/FORMAL)["selected_p3_keep43"]
    chronology = check_chronology(formal["physical_events"], cover)
    main_roles = {}
    for row in original["main_endpoint_normalizers"]:
        role, port = row["original_input_role"], row["port"]
        name = f'{"Y" if role % 2 else "X"}{role // 2}:{port}'
        require(name not in main_roles, "all actual main endpoints have distinct physical names")
        main_roles[name] = row["target_rank"]
    fresh_roles = {row["owner"]: row["target_rank"] for row in cover["fresh_outputs"]}
    require(len(main_roles) == 672 and len(fresh_roles) == len(cover["fresh_outputs"]) == 1570,
            "all 2242 actual independent productive fields are reconstructed")
    require(set(main_roles).isdisjoint(fresh_roles), "fresh fields cannot alias main fields")
    roles = tuple(sorted(main_roles.items()))+tuple(sorted(fresh_roles.items()))
    stages = [event for event in formal["physical_events"] if event[0] == "LOCAL"]
    require([event[1] for event in stages] == list(range(7)), "actual local invocation order")
    rounds, stage_rows = [], []
    for _, stage, pair, reverse in stages:
        direction = "backward" if reverse else "forward"
        selected = [row for row in cover["helper_bindings"] if row["stage"] == stage]
        helper = {row["role"]: row["owner"] for row in selected}
        require(len(selected) == len(helper) == len(set(helper.values())) == 408
                and set(helper) == set(range(224, 632)), "one distinct actual owner per exact local helper role")
        active = {f"{side}{pair}:{port}" for side in ("X", "Y") for port in range(112)}
        require(active.isdisjoint(helper.values()), "no helper borrows an active main field")
        first = len(rounds)
        for event in native[direction]:
            if event[0] == "climb":
                role = event[2]
                owner = (f"X{pair}:{role}" if role < 112 else
                         f"Y{pair}:{role-112}" if role < 224 else helper[role])
                rounds.append((event[-1], owner))
            elif event[0] == "center":
                rounds.append((event[-1], "owned-C0"))
        rounds.extend((row["rank"], row["owner"]) for row in cover["paid_residuals"]
                      if row["after_stage"] == stage)
        stage_rounds = rounds[first:]
        stage_rows.append({"stage": stage, "pair": pair, "direction": direction,
                           "paid": dict(sorted(Counter(rank for rank, owner in stage_rounds).items())),
                           "owned_center_calls": sum(owner == "owned-C0" for rank, owner in stage_rounds)})
    rounds = tuple(rounds)
    require(len(rounds) == 25292 and digest_json(rounds) == receipt["paid_word"]["sha256"],
            "independent actual paid-owner extraction matches the complete native receipt")
    expected_stages = [dict(row, paid={int(k): v for k, v in row["paid"].items()})
                       for row in receipt["paid_word"]["stages"]]
    require(stage_rows == expected_stages, "all chronological stage invoices agree")

    def contract(candidate_roles, candidate_rounds):
        rule = weak.WeakRule(candidate_roles, candidate_rounds)
        require(rule.targets == Counter(TARGETS), "all actual productive endpoint ranks are paid for")
        require(Counter(rank for rank, owner in candidate_rounds) == Counter(PAID),
                "every actual paid child, including every center call, remains charged")
        return rule

    rule = contract(roles, rounds)
    compiler = frozen.Compiler(rule)
    compiled = compiler.compile(57)
    tree = compiler.trees[57]
    require((compiled["width"], compiled["leaves"], compiled["units"]) == (2242, 127570, 1),
            "complete actual repacked rank57 supplier including every source complement")
    require(tree.depth == 0 and len(tree.exits) == len(rounds), "one unit and all ordered native exit batches")
    unit = tree.units[0]
    for index, ((rank, owner), batch) in enumerate(zip(rounds, tree.exits)):
        require(len(batch) == 1, "one actual field per chronological native exit")
        job = batch[0]
        require(job["round"] == index and job["rank"] == rank
                and job["field"] == unit["fields"].get(owner, unit["owned"].get(owner)),
                "round order, child rank, and actual physical owner survive compilation")
    require(tree.source_counter == Counter(TARGETS), "actual changed source ranks, not the prior source profile")
    require(tree.topological_size() == len(tree.nodes), "complete actual repacked graph is acyclic")
    tree.validate_fields()
    require(compiled["owned_fields_uncredited"] == 1, "the native center remains uncredited")
    require(all(compiled["replication"]*count % width == 0
                for kind, size, count, width in compiled["ordered_requirements"]),
            "every chronological batch independently clears denominators")
    old_fresh = {row["owner"]: row["target_rank"] for row in previous["fresh_outputs"]}
    stale_roles = tuple(sorted(main_roles.items()))+tuple(sorted(old_fresh.items()))
    first_center = next(i for i, (rank, owner) in enumerate(rounds) if owner == "owned-C0")
    unpaid = rounds[:first_center]+rounds[first_center+1:]
    premature = list(formal["physical_events"])
    premature.insert(1, ["ADD", 2, 0, 1])
    controls = {
        "strict_original_constructor_rejects_actual_equality": weak.rejection(lambda: frozen.Rule(roles, rounds)),
        "stale_prior_fresh_owner_contract_rejected": weak.rejection(lambda: contract(stale_roles, rounds)),
        "dropped_actual_owned_center_call_rejected": weak.rejection(lambda: contract(roles, unpaid)),
        "premature_bridge_on_incomplete_idle_rejected": weak.rejection(lambda: check_chronology(premature, cover)),
    }
    require(all(controls.values()), "all actual contract and lifetime controls are rejected")
    return {
        "schema": "actual-native-packing-weak-compiler-integration/1",
        "status": "PASS_ACTUAL_PACKED_NATIVE_OWNERS_CAUSALITY_AND_RANK57_COMPILATION",
        "source_commit": COMMIT, "source_sha256": pins,
        "native_producer_sha256": PRODUCER_HASH, "native_certificate_sha256": NATIVE_RECEIPT_HASH,
        "weak_interface_sha256": WEAK_HASH, "original_compiler_sha256": weak.SOURCE_HASH,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"COMPILER.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": TARGETS, "paid": PAID},
        "productive_fields": len(roles), "paid_rounds": len(rounds),
        "actual_role_contract_sha256": digest_json(roles), "actual_ordered_paid_word_sha256": digest_json(rounds),
        "fresh_owner_changes": {"removed": sorted(set(old_fresh)-set(fresh_roles)),
                                "added": sorted(set(fresh_roles)-set(old_fresh))},
        "idle_lifetime_guards": chronology, "stages": stage_rows,
        "compiled": {key: str(value) if isinstance(value, Fraction) else value
                     for key, value in compiled.items() if key != "ordered_requirements"},
        "event_graph": tree.summary(), "controls": controls,
        "scope": [
            "The actual newly repacked main/fresh roles and every chronological paid owner are reconstructed.",
            "The complete native endpoint and new coordinate-map proofs remain in the separately authenticated packing certificate.",
            "Literal rank57 compilation has one native unit and generation depth zero, with every source complement paid.",
            "The generic positive-generation equality compiler tests remain separately authenticated; this is not a materialized large template.",
            "The stronger mixed saving requires a new tail/rank certificate and outer transfer using this same full profile.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    serialized = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(serialized)
    else:
        require((HERE/"COMPILER.json").read_text() == serialized, "exact actual native packing integration replay")
    print(json.dumps({key: result[key] for key in
                      ("status", "productive_fields", "paid_rounds", "event_graph", "controls")}, sort_keys=True))


if __name__ == "__main__":
    main()
