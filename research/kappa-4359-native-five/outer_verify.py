#!/usr/bin/env python3
"""Close the native width-five and weak-compiler chain at kappa=.00231165.

All companion receipts and source programs are authenticated and replayed.
The unchanged outer parameter algebra comes from the first reviewed strict
endpoint package. Native and analytic premises retain their stated scope.
Apache-2.0.
"""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
SOURCE_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
MATH_HASH = "4a51eea1d796224e4a8bb6e2031146ba743e63ed88b2e7e241093a7025a063de"
COMPANION_PINS = {
    "kappa-4359-native-five": "9a4036e30d38be476cd529b4aebba40270f719744c13a86efd9306892d903ed8",
    "kappa-4359-weak-compiler": "2bd9043b77e5219e92d101c3c5f469bf302618ac932484f169f1ad3614ac1187",
    "kappa-4359-weak-separation": "98c20fc702867a3d292ca5e9b9557773f7a132d859425deb9b519f1ad1379717",
}
KAPPA = Q("0.00231165")
TESTED = Q("0.00231166")
UNIFORM = Q("0.002311658")
TARGETS = {5: 102, 6: 90, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17521, 2: 5065, 3: 1738, 4: 714, 5: 254}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def math_engine():
    path = HERE.parent/"kappa-4359-outer-endpoint/verify.py"
    require(sha256(path.read_bytes()).hexdigest() == MATH_HASH, "reviewed outer equations and rational interval engine")
    spec = importlib.util.spec_from_file_location("reviewed_outer_family", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_companions(source_root):
    results = {}
    for package, expected in COMPANION_PINS.items():
        require(isinstance(expected, str) and len(expected) == 64, "every companion must have a final reviewed pin")
        directory = HERE.parent/package
        path = directory/"CERTIFICATE.json"
        require(sha256(path.read_bytes()).hexdigest() == expected, "changed companion receipt: "+package)
        result = json.loads(path.read_text())
        checker = directory/"verify.py"
        require(sha256(checker.read_bytes()).hexdigest() == result["generator_sha256"], "changed companion checker: "+package)
        if "proof_sha256" in result:
            proof = directory/("README.md" if package == "kappa-4359-native-five" else "PROOF.md")
            require(sha256(proof.read_bytes()).hexdigest() == result["proof_sha256"], "changed companion proof: "+package)
        command = [sys.executable, "-B", str(checker), "--source-root", str(source_root)]
        if package != "kappa-4359-weak-compiler":
            command.append("--check")
        replay = subprocess.run(command, capture_output=True, text=True)
        require(replay.returncode == 0, "companion replay failed for "+package+": "+replay.stderr)
        require(result["source_commit"] == SOURCE_COMMIT, "one immutable predecessor throughout the chain")
        results[package] = result
    return results


def validate_chain(native, compiler, rank, point):
    targets = {int(k): int(v) for k, v in native["new_profile"]["targets"].items()}
    paid = {int(k): int(v) for k, v in native["new_profile"]["paid"].items()}
    require(targets == TARGETS and paid == PAID, "outer bound uses the complete actual derivative tariff")
    require({int(k): int(v) for k, v in rank["new_profile"]["targets"].items()} == targets
            and {int(k): int(v) for k, v in rank["new_profile"]["paid"].items()} == paid,
            "native and weighted-tail profiles agree")
    require(native["depth_zero_full_rank_check"]["unchanged_complete_rank_one_leaf_count"] == 127570,
            "source complements are still fully paid")
    require(compiler["new_interface"] == "r_max <= k_min < m and k_min >= 2, with unchanged complete named-role and owned-field obligations",
            "the equal-rank interface is explicit")
    require(all(compiler["controls"].values()) and compiler["controls"]["minimum_one_nonterminating_lattice_rejected"],
            "the changed constructor retains its termination and ownership guards")
    require(rank["schema"] == "weighted-tail-weak-separation-template/1", "weighted exit-tail proof is required")
    require(Q(rank["tested_mixed_saving"]) == TESTED and Q(rank["uniform_saving"]) == UNIFORM,
            "rank certificate pays the actual stronger uniform saving")
    require(point["parameters"]["tested_mixed_saving"] == TESTED
            and point["parameters"]["complex_uniform_saving"] == UNIFORM, "outer and compiler exponents agree")
    require(rank["N"] == {"encoding": "2^H", "H": 756934981}, "the selected finite uniform template is specified")
    require(Q(rank["strict_final_power_gap"]) > 0 and Q(rank["complement_strict_gap"]) > 0,
            "finite-rank and full weighted-exit inequalities are strict")
    require(max(paid) == min(targets) == 5 < max(targets), "this is genuinely the weak-separation case")


def build(source_root):
    engine = math_engine()
    sources = engine.bind_sources(source_root)
    companions = replay_companions(source_root)
    native = companions["kappa-4359-native-five"]
    compiler = companions["kappa-4359-weak-compiler"]
    rank = companions["kappa-4359-weak-separation"]
    point = engine.parameter_point(KAPPA, TESTED)
    validate_chain(native, compiler, rank, point)
    margin = engine.mixed_margin(TARGETS, PAID, TESTED)
    require(margin[0] > 0, "independent positive derivative moment")
    crosscheck = engine.inherited_crosscheck(source_root, point)
    require(point["minimum_outer_slack"] == Q(249422087, 125000000000000000), "exact limiting outer slack")
    old_rank = deepcopy(rank)
    old_rank["uniform_saving"] = "0.002305088"
    old_rejected = False
    try:
        validate_chain(native, compiler, old_rank, point)
    except AssertionError:
        old_rejected = True
    require(old_rejected, "the first weaker uniform template cannot be reused for the new point")
    old_moment = engine.mixed_margin(engine.COMPLEX_TARGETS, engine.COMPLEX_PAID, TESTED)
    require(old_moment[1] < 0, "the stronger claim needs the actual native word change")
    return {
        "schema": "native-width-five-complete-conditional-outer-chain/1",
        "status": "PASS_NATIVE_WEAK_COMPILER_AND_CONDITIONAL_KAPPA_00231165",
        "source_commit": SOURCE_COMMIT, "source_sha256": sources,
        "companion_sha256": COMPANION_PINS, "outer_family_generator_sha256": MATH_HASH,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"OUTER.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": TARGETS, "paid": PAID},
        "tested_mixed_margin": margin, "outer": point, "inherited_crosscheck": crosscheck,
        "finite_template": {"tested_mixed_saving": TESTED, "uniform_saving": UNIFORM,
                            "N": rank["N"], "strict_final_power_gap": Q(rank["strict_final_power_gap"])},
        "controls": {"previous_weaker_uniform_template_rejected": old_rejected,
                     "unchanged_tariff_margin_at_new_test": old_moment},
        "increased_complements_retained": native["depth_zero_full_rank_check"],
        "conditional_dependencies": [
            "The source-bound autonomous native endpoints, all-column interpretation, physical adapters, and complete scalar/routing/owned-space bills from PR4359.",
            "The separately proved weak-rank integer compiler and weighted-exit-tail recurrence, charging every source complement and every owned-field paid call.",
            "The selected fixed template uses its own finite counts in the retained generic semantic precision, movement, and row-stock formulas.",
            "The unchanged ordinary BIT supplier at saving .0027 and the inherited analytic decomposition, fine-prime padding, fixed-tape routing, and exact recovery hypotheses.",
        ],
        "not_claimed": ["An unconditional integer-multiplication theorem.", "A formal proof of all native and analytic premises.",
                        "Materialized or practical finite template counts.", "Attainment of the improved local mixed root itself."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", "--check-only", action="store_true")
    args = parser.parse_args()
    engine = math_engine()
    result = build(args.source_root.resolve())
    text = json.dumps(engine.encode(result), indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE/"OUTER.json").read_text() == text, "committed stronger outer certificate differs from replay")
    print(json.dumps(engine.encode({"status": result["status"], "kappa": KAPPA,
                                   "uniform_saving": UNIFORM, "N": result["finite_template"]["N"],
                                   "minimum_outer_slack": result["outer"]["minimum_outer_slack"],
                                   "own_strict_checks": len(result["outer"]["strict_checks"]),
                                   "inherited_crosscheck": result["inherited_crosscheck"]}), sort_keys=True))


if __name__ == "__main__":
    main()
