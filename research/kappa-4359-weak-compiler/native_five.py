#!/usr/bin/env python3
"""Instantiate the actual native width-five word in the weak compiler.

This reconstructs named roles and every ordered paid owner from immutable
native sources, removes exactly the authenticated 102 topups, and compiles
the resulting rank-57 word. The large saving template is not materialized.
Apache-2.0. Native construction and original compiler: PR4359.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
COVER = "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz"
FORMAL = "research/kappa-rebuild/bit/COMPLEX-CONTROLLER-FACTOR.json"
NATIVE = "research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz"
SOURCE_PINS = {
    COVER: "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f",
    FORMAL: "a6d3d835c1ccf4bee5a9771beb0bec8e0dcb3c4b9e49d158835f195507ade280",
    NATIVE: "c54b0a3e129d28e6dbf74fa731fc3bb70fe3c6705f07256750fbecddcc842d39",
}
WEAK_HASH = "33d43a20a55e3eb6200abb478f3ef9bcd3d866233cacd7930d15c87fa0759605"
DELETION_HASH = "9a4036e30d38be476cd529b4aebba40270f719744c13a86efd9306892d903ed8"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def digest_json(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build(root):
    for relative, expected in SOURCE_PINS.items():
        require(sha256((root/relative).read_bytes()).hexdigest() == expected,
                "unchanged actual native source: "+relative)
    weak_path = HERE/"verify.py"
    require(sha256(weak_path.read_bytes()).hexdigest() == WEAK_HASH,
            "authenticated new weak rule interface")
    spec = importlib.util.spec_from_file_location("weak_native_integration", weak_path)
    weak = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = weak
    spec.loader.exec_module(weak)
    original_compiler = weak.load_original(root)
    deletion_path = HERE.parent/"kappa-4359-native-five/CERTIFICATE.json"
    require(sha256(deletion_path.read_bytes()).hexdigest() == DELETION_HASH,
            "authenticated native deletion receipt")
    deletion = read(deletion_path)
    cover_receipt = read(root/COVER)
    cover = cover_receipt["cover"]
    formal = read(root/FORMAL)["selected_p3_keep43"]
    native = read(root/NATIVE)
    require(cover_receipt["sources"][FORMAL] == SOURCE_PINS[FORMAL]
            and cover_receipt["sources"][NATIVE] == SOURCE_PINS[NATIVE],
            "the cover binds these same actual formal and local native words")
    targets = {int(k): v for k, v in deletion["new_profile"]["targets"].items()}
    paid = {int(k): v for k, v in deletion["new_profile"]["paid"].items()}
    removed = deletion["removed_topups"]
    removed_owners = {row["owner"] for row in removed}
    require(len(removed_owners) == len(removed) == 102, "102 distinct actual deletions")
    require(sorted(removed, key=lambda row: row["owner"]) == sorted(
        (row for row in cover["paid_residuals"] if row["owner"] in removed_owners),
        key=lambda row: row["owner"]), "the literal residual word contains exactly the listed removals")
    main_roles = {}
    for row in cover_receipt["main_endpoint_normalizers"]:
        role, port = row["original_input_role"], row["port"]
        name = f'{"Y" if role % 2 else "X"}{role // 2}:{port}'
        require(name not in main_roles, "distinct actual main endpoint owner")
        main_roles[name] = row["target_rank"]
    require(len(main_roles) == 672, "all six main fields at each of 112 ports")
    fresh_roles = {}
    for row in cover["fresh_outputs"]:
        name = row["owner"]
        require(name not in fresh_roles, "distinct actual fresh owner")
        changed = name in removed_owners
        require(changed == (row["native_width"] == 5), "all and only native-five fresh roles change")
        if changed:
            require(row["target_rank"] == 6, "deleted call supplied the sixth axis")
        fresh_roles[name] = 5 if changed else row["target_rank"]
    require(len(fresh_roles) == 1570 and set(main_roles).isdisjoint(fresh_roles),
            "all fresh and main productive fields are distinct")
    roles = tuple(sorted(main_roles.items()))+tuple(sorted(fresh_roles.items()))
    stages = [event for event in formal["physical_events"] if event[0] == "LOCAL"]
    require([event[1] for event in stages] == list(range(7)),
            "seven local invocations occur in the authenticated controller order")
    rounds, stage_rows = [], []
    for _, stage, pair, reversed_direction in stages:
        direction = "backward" if reversed_direction else "forward"
        selected = [row for row in cover["helper_bindings"] if row["stage"] == stage]
        helper = {row["role"]: row["owner"] for row in selected}
        require(len(selected) == len(helper) == 408 and set(helper) == set(range(224, 632)),
                "every literal native helper has exactly one binding")
        active = {f"{side}{pair}:{port}" for side in ("X", "Y") for port in range(112)}
        require(len(set(helper.values())) == 408 and active.isdisjoint(helper.values()),
                "all helper inputs are distinct and separate from the active main pair")
        begin = len(rounds)
        for event in native[direction]:
            if event[0] == "climb":
                role = event[2]
                owner = (f"X{pair}:{role}" if role < 112 else
                         f"Y{pair}:{role-112}" if role < 224 else helper[role])
                rounds.append((event[-1], owner))
            elif event[0] == "center":
                rounds.append((event[-1], "owned-C0"))
        rounds.extend((row["rank"], row["owner"]) for row in cover["paid_residuals"]
                      if row["after_stage"] == stage and row["owner"] not in removed_owners)
        local_rounds = rounds[begin:]
        stage_rows.append({"stage": stage, "pair": pair, "direction": direction,
                           "paid_rounds": len(local_rounds),
                           "paid": dict(sorted(Counter(rank for rank, owner in local_rounds).items())),
                           "owned_center_calls": sum(owner == "owned-C0" for rank, owner in local_rounds)})
    rounds = tuple(rounds)

    def contract(candidate_roles, candidate_rounds):
        rule = weak.WeakRule(candidate_roles, candidate_rounds)
        require(rule.targets == Counter(targets), "all complete productive endpoint ranks are earned")
        require(Counter(rank for rank, owner in candidate_rounds) == Counter(paid),
                "complete literal native paid invoice, including owned-center calls")
        return rule

    rule = contract(roles, rounds)
    require(weak.rejection(lambda: original_compiler.Rule(roles, rounds)),
            "the actual native tariff genuinely needs the changed equality guard")
    compiler = original_compiler.Compiler(rule)
    compiled = compiler.compile(57)
    tree = compiler.trees[57]
    require((compiled["width"], compiled["leaves"], compiled["units"]) == (2242, 127570, 1),
            "actual full rank-57 completion includes every changed source complement")
    require(tree.depth == 0 and len(tree.exits) == len(rounds),
            "one native unit with every paid round represented separately")
    unit = tree.units[0]
    for index, ((rank, owner), batch) in enumerate(zip(rounds, tree.exits)):
        require(len(batch) == 1, "one actual field in each ordered native exit batch")
        job = batch[0]
        field = unit["fields"].get(owner, unit["owned"].get(owner))
        require(job["round"] == index and job["rank"] == rank and job["field"] == field,
                "chronology, paid rank, and physical owner survive the interface")
    require(tree.topological_size() == len(tree.nodes), "literal native paid-owner graph is acyclic")
    tree.validate_fields()
    require(all(compiled["replication"]*count % width == 0
                for kind, size, count, width in compiled["ordered_requirements"]),
            "every chronological batch clears independently")
    require(compiled["owned_fields_uncredited"] == 1, "the native center remains uncredited")
    first_owned = next(i for i, (rank, owner) in enumerate(rounds) if owner == "owned-C0")
    unpaid = rounds[:first_owned]+rounds[first_owned+1:]
    unearned = tuple((name, 6 if name == min(removed_owners) else rank) for name, rank in roles)
    controls = {
        "strict_original_rule_rejects_actual_native_equality":
            weak.rejection(lambda: original_compiler.Rule(roles, rounds)),
        "dropped_actual_owned_center_call_rejected": weak.rejection(lambda: contract(roles, unpaid)),
        "unearned_deleted_sixth_axis_credit_rejected": weak.rejection(lambda: contract(unearned, rounds)),
    }
    require(all(controls.values()), "actual native integration controls discriminate unpaid work")
    return {
        "schema": "actual-native-five-weak-compiler-integration/1",
        "status": "PASS_ACTUAL_NATIVE_FIVE_OWNERS_ORDER_AND_RANK57_COMPILATION",
        "source_commit": COMMIT, "source_sha256": SOURCE_PINS,
        "weak_interface_sha256": WEAK_HASH, "original_compiler_sha256": weak.SOURCE_HASH,
        "native_deletion_sha256": DELETION_HASH,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "role_contract_sha256": digest_json(roles), "ordered_paid_word_sha256": digest_json(rounds),
        "productive_fields": len(roles), "paid_rounds": len(rounds),
        "targets": targets, "paid": paid, "stages": stage_rows,
        "compiled": {key: str(value) if isinstance(value, Fraction) else value
                     for key, value in compiled.items() if key != "ordered_requirements"},
        "event_graph": tree.summary(), "controls": controls,
        "scope": [
            "Actual native p3 role names and chronological paid owners are reconstructed from pinned sources.",
            "Exactly the separately authenticated 102 rank-one residuals are removed.",
            "The literal rank57 compiler graph has one native unit and generation depth zero.",
            "Positive-generation equality scheduling is exercised by the independent toy certificate.",
            "This rank57 completion does not attain the improved mixed exponent.",
            "The native endpoint proof, large uniform-template theorem, and outer transfer remain separate obligations.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    serialized = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(serialized)
    else:
        require((HERE/"NATIVE-FIVE.json").read_text() == serialized, "exact native integration replay")
    print(json.dumps({key: result[key] for key in
                      ("status", "productive_fields", "paid_rounds", "event_graph", "controls")}, sort_keys=True))


if __name__ == "__main__":
    main()
