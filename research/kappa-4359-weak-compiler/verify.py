#!/usr/bin/env python3
"""Exercise the finite compiler at equal paid/target minimum rank.

The constructor is new. The original IntegerTree and Compiler are imported
unchanged after SHA-256 authentication. The mathematical justification of
weak separation is in the companion weak-separation proof package.
Apache-2.0. Original compiler: PR4359; mixed flow: PR4268.
"""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = "research/kappa-rebuild/transfer-audit/finite_dag_audit.py"
SOURCE_HASH = "f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class WeakRule:
    """A complete role contract with r_max <= k_min < m and k_min >= 2.

    This is deliberately a separate type. It does not bypass the old strict
    constructor or imply that the old proof already admitted equality.
    """
    roles: tuple
    rounds: tuple
    owned: tuple = ("owned-C0",)

    def __post_init__(self):
        require(self.roles and self.rounds, "nonempty productive roles and paid rounds")
        names = [name for name, rank in self.roles]
        require(all(isinstance(name, str) and name for name in names+self.owned_list()),
                "every physical field has a nonempty name")
        require(len(set(names)) == len(names), "distinct productive roles")
        require(len(set(self.owned)) == len(self.owned), "distinct owned roles")
        require(set(names).isdisjoint(self.owned), "owned storage receives no productive credit")
        require(all(type(rank) is int and rank > 0 for name, rank in self.roles),
                "positive integral target ranks")
        known = set(names) | set(self.owned)
        require(all(type(rank) is int and rank > 0 and name in known for rank, name in self.rounds),
                "every paid call has a positive integral rank and an actual physical owner")
        kmin = min(rank for name, rank in self.roles)
        rmax = max(rank for rank, name in self.rounds)
        require(2 <= kmin and rmax <= kmin < self.dimension,
                "weak separation r_max <= k_min < m with k_min >= 2")

    def owned_list(self):
        return list(self.owned)

    @property
    def targets(self):
        return Counter(rank for name, rank in self.roles)

    @property
    def dimension(self):
        return max(rank for name, rank in self.roles)


def load_original(root):
    path = root/SOURCE
    require(sha256(path.read_bytes()).hexdigest() == SOURCE_HASH, "unchanged original finite compiler")
    spec = importlib.util.spec_from_file_location("pr4359_frozen_compiler", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rejection(call):
    try:
        call()
    except (AssertionError, ValueError):
        return True
    return False


def build(root):
    original = load_original(root)
    roles = (("a", 2), ("b", 2), ("c", 3))
    rounds = ((1, "a"), (2, "owned-C0"), (1, "b"), (2, "c"))
    rule = WeakRule(roles, rounds)
    require(max(r for r, owner in rounds) == min(r for owner, r in roles),
            "the tested contract genuinely has an equality edge")
    require(rejection(lambda: original.Rule(roles, rounds)), "the old strict constructor rejects equality")
    compiler = original.Compiler(rule)
    rows = []
    for rank in (3, 6, 12, 24, 48):
        compiled = compiler.compile(rank)
        tree = compiler.trees[rank]
        require(tree.topological_size() == len(tree.nodes), "equal-rank flow remains acyclic")
        tree.validate_fields()
        require(all(job["rank"] < rank for batch in tree.exits for job in batch),
                "every exit has smaller ambient rank")
        require(compiled["leaves"] <= rank*compiled["width"], "no lost complementary jobs in rank budget")
        require(compiled["owned_fields_uncredited"] == compiled["units"],
                "one conservatively allocated owned field per unit, never credited")
        owned_nested = any(field[0] == "owned" for unit in tree.units for field in unit["fields"].values())
        if rank >= 6:
            require(owned_nested, "a parent's owned center is an actual child input field")
        rows.append({
            "rank": rank,
            "width": compiled["width"], "leaves": compiled["leaves"],
            "units": compiled["units"], "leaves_per_array": str(compiled["per_array"]),
            "replication": compiled["replication"],
            "owned_center_enters_child": owned_nested,
            "tree": tree.summary(),
            "ordered_batches_integral": all(compiled["replication"]*n % width == 0
                                             for kind, size, n, width in compiled["ordered_requirements"]),
        })
        require(rows[-1]["ordered_batches_integral"], "every chronological child batch clears independently")
    controls = {
        "old_strict_constructor_rejects_equality": rejection(lambda: original.Rule(roles, rounds)),
        "paid_rank_above_minimum_rejected": rejection(lambda: WeakRule(roles, ((3, "owned-C0"),))),
        "minimum_equal_to_ambient_rejected": rejection(lambda: WeakRule((("a", 2), ("b", 2)), ((2, "a"),))),
        "minimum_one_nonterminating_lattice_rejected": rejection(lambda: WeakRule((("a", 1), ("b", 2)), ((1, "a"),))),
        "duplicate_productive_name_rejected": rejection(lambda: WeakRule((("a", 2), ("a", 3)), rounds)),
        "owned_role_credited_as_productive_rejected": rejection(lambda: WeakRule((("owned-C0", 2), ("c", 3)), rounds)),
        "nonexistent_paid_owner_rejected": rejection(lambda: WeakRule(roles, ((2, "missing"),))),
    }
    require(all(controls.values()), "all invalid interface controls are rejected")
    # Reuse the original graph validator to challenge a concrete alias in a
    # new, equality-case tree. Restore it before returning the receipt.
    tree = compiler.trees[12]
    fields = tree.units[0]["fields"]
    first, second = tuple(fields)[:2]
    saved = fields[second]
    try:
        fields[second] = fields[first]
        alias_rejected = rejection(tree.validate_fields)
    finally:
        fields[second] = saved
    require(alias_rejected, "equal-rank child roles cannot alias independent source fields")
    controls["actual_equality_tree_alias_rejected"] = alias_rejected
    return {
        "schema": "weak-separation-finite-compiler-interface/1",
        "status": "PASS_EQUALITY_RULE_AND_MULTIGENERATION_OWNED_DAG",
        "source_commit": "da637c87c89482bc4c86be36bd0071b3d400dbed",
        "source_sha256": {SOURCE: SOURCE_HASH},
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "new_interface": "r_max <= k_min < m and k_min >= 2, with unchanged complete named-role and owned-field obligations",
        "toy_roles": roles, "toy_paid_rounds": rounds,
        "cases": rows, "controls": controls,
        "scope": [
            "The new WeakRule deliberately broadens the accepted rank interface.",
            "The original IntegerTree and Compiler implementations are unchanged.",
            "Five literal equality-case graphs, including owned-center recursion and independent ordered batching, are checked.",
            "The toy is a generic complete-role contract, not a claimed native transform.",
            "The weak-separation theorem and adjusted actual native profile require their separate proofs and certificates.",
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
        require((HERE/"CERTIFICATE.json").read_text() == serialized, "exact deterministic certificate replay")
    print(json.dumps({"status": result["status"], "ranks": [row["rank"] for row in result["cases"]],
                      "maximum_generations": max(row["tree"]["generations"] for row in result["cases"]),
                      "rejection_controls": len(result["controls"])}))


if __name__ == "__main__":
    main()
