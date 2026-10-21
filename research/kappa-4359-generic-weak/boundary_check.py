#!/usr/bin/env python3
"""Check the all-maximal-paid boundary of the literal weak compiler.

The exact lattice derivation is in BOUNDARY.md. This is a synthetic complete
role contract, not a claimed native circuit or a multiplication lower bound.
Apache-2.0. The frozen compiler is from PR4359; its mixed flow is from PR4268.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
SOURCE_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
ORIGINAL_PATH = "research/kappa-rebuild/transfer-audit/finite_dag_audit.py"
ORIGINAL_HASH = "f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e"
WEAK_CHECKER_HASH = "33d43a20a55e3eb6200abb478f3ef9bcd3d866233cacd7930d15c87fa0759605"
WEAK_RECEIPT_HASH = "2bd9043b77e5219e92d101c3c5f469bf302618ac932484f169f1ad3614ac1187"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def authenticate(source_root):
    original_path = source_root / ORIGINAL_PATH
    require(sha256(original_path.read_bytes()).hexdigest() == ORIGINAL_HASH,
            "the original literal compiler source is unchanged")
    weak_directory = HERE.parent / "kappa-4359-weak-compiler"
    weak_path = weak_directory / "verify.py"
    receipt_path = weak_directory / "CERTIFICATE.json"
    require(sha256(weak_path.read_bytes()).hexdigest() == WEAK_CHECKER_HASH,
            "the reviewed WeakRule implementation is unchanged")
    require(sha256(receipt_path.read_bytes()).hexdigest() == WEAK_RECEIPT_HASH,
            "the reviewed generic interface receipt is unchanged")
    receipt = json.loads(receipt_path.read_text())
    require(receipt["schema"] == "weak-separation-finite-compiler-interface/1"
            and receipt["source_commit"] == SOURCE_COMMIT
            and receipt["generator_sha256"] == WEAK_CHECKER_HASH
            and receipt["source_sha256"][ORIGINAL_PATH] == ORIGINAL_HASH,
            "the interface receipt binds the same original compiler")
    spec = importlib.util.spec_from_file_location("generic_weak_boundary_rule", weak_path)
    weak = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = weak
    spec.loader.exec_module(weak)
    original = weak.load_original(source_root)
    return weak, original


def build(source_root):
    weak, original = authenticate(source_root)
    roles = (("a", 2), ("b", 3))
    rounds = ((2, "a"), (2, "owned-C0"))
    rule = weak.WeakRule(roles, rounds)
    require(rule.targets == Counter({2: 1, 3: 1}) and rule.dimension == 3,
            "the stated two-target boundary contract is instantiated")
    require(Counter(rank for rank, owner in rounds) == Counter({2: 2}),
            "both paid calls have the maximal permitted rank")
    require(3 > 2, "sqrt(3)-sqrt(2) is a strictly positive mixed surplus at t=1/2")
    p1 = sum(rank for rank, owner in rounds)
    p2 = sum(rank * rank for rank, owner in rounds)
    require(p1 == 4 and p2 == 8 and Q(p2, p1) == 2,
            "the rational tilted-mean upper bound equals q, so its strict guard fails")
    require(not any(rank < 2 for rank, owner in rounds),
            "the positive generic theorem's nonmaximal-paid condition is absent")
    old_rejects = False
    try:
        original.Rule(roles, rounds)
    except AssertionError:
        old_rejects = True
    require(old_rejects, "the original strictly separated interface excludes this example")

    compiler = original.Compiler(rule)
    values = {0: Q(1), 1: Q(2)}
    require(compiler.compile(1)["per_array"] == values[0]
            and compiler.compile(2)["per_array"] == values[1],
            "rank-one base leaves give f_0=1 and f_1=2")
    rows = []
    for exponent in range(2, 9):
        rank = 2 ** exponent
        compiled = compiler.compile(rank)
        tree = compiler.trees[rank]
        generation = exponent - 2
        width_before_replication = 2 ** (exponent - 1)
        require(tree.depth == generation, "G=k-2 at ambient rank 2^k")
        require(Q(rank, 3 * 2 ** generation) == Q(4, 3) < Q(3, 2),
                "a single rank-three target factor cannot fit at the required degree")
        require(len(tree.units) == width_before_replication - 1
                and all(unit["point"] == (generation - len(unit["path"]), 0)
                        and unit["column"] == rank // 4 for unit in tree.units),
                "every ordered class has its unique all-two lattice point")
        expected_sources = Counter({rank // 2: 1,
                                    3 * rank // 4: width_before_replication - 1})
        require(tree.source_counter == expected_sources,
                "one half-rank source and all three-quarter-rank sources are retained")
        exits = Counter(job["rank"] for batch in tree.exits for job in batch)
        require(exits == Counter({rank // 2: width_before_replication}),
                "all terminal paid calls have half the ambient rank")
        require(len(tree.sources) == width_before_replication,
                "normalization uses every independent source")
        epsilon = Q(1, width_before_replication)
        expected_value = ((1 + epsilon) * values[exponent - 1]
                          + (1 - epsilon) * values[exponent - 2])
        require(compiled["per_array"] == expected_value,
                "the actual full-completion bill equals the derived recurrence")
        require(expected_value >= values[exponent - 1] + values[exponent - 2]
                and expected_value > values[exponent - 1],
                "these exact samples satisfy the proved Fibonacci comparison")
        require(compiled["owned_fields_uncredited"] == compiled["units"],
                "all recursively allocated owned centers remain uncredited")
        integral = all(compiled["replication"] * count % child_width == 0
                       for kind, size, count, child_width in compiled["ordered_requirements"])
        require(integral, "every chronological child batch is actually integral")
        owned_enters_child = any(field[0] == "owned" for unit in tree.units
                                 for field in unit["fields"].values())
        if exponent >= 3:
            require(owned_enters_child, "the paid call on owned storage enters a real child")
        values[exponent] = expected_value
        rows.append({
            "exponent_k": exponent,
            "ambient_rank": rank,
            "tree": tree.summary(),
            "full_rank_arrays": compiled["width"],
            "rank_one_leaves": compiled["leaves"],
            "leaves_per_array": str(expected_value),
            "replication": compiled["replication"],
            "recursive_unit_count": compiled["units"],
            "ordered_batches_integral": integral,
            "owned_center_enters_child": owned_enters_child,
        })
    require(values[2] == Q(7, 2) and values[3] == Q(47, 8)
            and values[4] == Q(619, 64), "independent initial recurrence values")
    return {
        "schema": "literal-weak-compiler-all-maximal-paid-boundary/1",
        "status": "PASS_LITERAL_COMPILER_FIBONACCI_BOUNDARY",
        "source_commit": SOURCE_COMMIT,
        "source_sha256": {ORIGINAL_PATH: ORIGINAL_HASH},
        "weak_interface_generator_sha256": WEAK_CHECKER_HASH,
        "weak_interface_receipt_sha256": WEAK_RECEIPT_HASH,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "BOUNDARY.md").read_bytes()).hexdigest(),
        "roles": roles,
        "paid_rounds": rounds,
        "owned_roles": rule.owned,
        "mixed_test": {"t": "1/2", "surplus": "sqrt(3)-sqrt(2)>0",
                       "exact_square_comparison": "3>2"},
        "rank_one_surplus": 1,
        "paid_mean": {"P1": p1, "P2": p2, "P2_over_P1": "2", "q": 2,
                      "strict_nonmaximal_paid_guard_satisfied": False},
        "old_strict_interface_rejects": old_rejects,
        "recurrence": {
            "f_k": "L(2^k)", "f_0": "1", "f_1": "2",
            "valid_for": "Every integer k>=2; proved from exact lattice and source/exit counts.",
            "formula": "f_k=(1+2^(1-k))*f_(k-1)+(1-2^(1-k))*f_(k-2)",
            "lower_bound": "f_k>=phi^k, where phi=(1+sqrt(5))/2>sqrt(2)",
        },
        "materialized_cases": rows,
        "scope": [
            "A synthetic complete-role contract for the literal finite compiler, including a paid owned-center call.",
            "The all-k recurrence and growth obstruction are proved in BOUNDARY.md; seven finite graphs corroborate them.",
            "No finite A and fixed gamma bound this compiler's L(n) by A*n^(1/2)*max(1,ln(n))^gamma for all n.",
        ],
        "not_claimed": [
            "A native circuit realizing the synthetic role contract.",
            "A lower bound for integer multiplication or arbitrary algorithms.",
            "Impossibility of every other uniformization construction or of a useful specially chosen finite rank.",
            "A failure of the actual repacked native tariff, which has many paid ranks strictly below q.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", "--check-only", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(serialized)
    else:
        require((HERE / "BOUNDARY.json").read_text() == serialized,
                "the deterministic boundary receipt matches the committed bytes")
    print(json.dumps({"status": result["status"],
                      "materialized_ranks": [row["ambient_rank"] for row in result["materialized_cases"]],
                      "growth_obstruction": result["recurrence"]["lower_bound"]}, sort_keys=True))


if __name__ == "__main__":
    main()
