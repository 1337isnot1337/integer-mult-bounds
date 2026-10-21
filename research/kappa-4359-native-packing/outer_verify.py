#!/usr/bin/env python3
"""Authenticate and replay the complete conditional kappa=.00231284 chain.

The literal repacked native cover, actual equality-case compiler, independent
weighted-tail rank theorem, and full outer ledger must all agree exactly.
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
COMPANIONS = {
    "native": {"directory": ".", "receipt": "CERTIFICATE.json", "checker": "verify.py", "proof": "README.md",
               "sha256": "5c8cc831151aa7147e6c3dd2a6832d19026aecc660955131149bdc54f0b26878", "check_flag": True},
    "compiler": {"directory": ".", "receipt": "COMPILER.json", "checker": "compiler_check.py", "proof": "COMPILER.md",
                 "sha256": "1cd2f4d3b115d2220f24f857748399f9637bc31269a90ca590bdd2301df710e6", "check_flag": True},
    "tail": {"directory": "../kappa-4359-packed-tail", "receipt": "CERTIFICATE.json", "checker": "verify.py", "proof": "PROOF.md",
             "sha256": "0d7286920f5b997fb948f91e26bb48e75fb0a05107bd41bfd0bc46ed9e88c15b", "check_flag": True},
}
KAPPA = Q("0.00231284")
TESTED = Q("0.00231285")
UNIFORM = Q("0.002312848")
TARGETS = {5: 140, 6: 52, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17559, 2: 5027, 3: 1738, 4: 714, 5: 254}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def math_engine():
    path = HERE.parent/"kappa-4359-outer-endpoint/verify.py"
    require(sha256(path.read_bytes()).hexdigest() == MATH_HASH, "unchanged reviewed outer equations and rational intervals")
    spec = importlib.util.spec_from_file_location("frozen_outer_for_packed_native", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_companions(source_root):
    results = {}
    for name, config in COMPANIONS.items():
        expected = config["sha256"]
        require(isinstance(expected, str) and len(expected) == 64, "each dependency has a final immutable receipt pin")
        directory = (HERE/config["directory"]).resolve()
        path = directory/config["receipt"]
        require(sha256(path.read_bytes()).hexdigest() == expected, "changed companion receipt: "+name)
        receipt = json.loads(path.read_text())
        checker = directory/config["checker"]
        require(sha256(checker.read_bytes()).hexdigest() == receipt["generator_sha256"], "changed companion source: "+name)
        if "proof_sha256" in receipt:
            require(sha256((directory/config["proof"]).read_bytes()).hexdigest() == receipt["proof_sha256"],
                    "changed companion proof: "+name)
        require(receipt["source_commit"] == SOURCE_COMMIT, "one pinned original native construction")
        command = [sys.executable, "-B", str(checker), "--source-root", str(source_root)]
        if config["check_flag"]:
            command.append("--check")
        replay = subprocess.run(command, capture_output=True, text=True)
        require(replay.returncode == 0, "companion replay failed for "+name+": "+replay.stderr)
        results[name] = receipt
    return results


def profile(value):
    return {int(rank): int(count) for rank, count in value.items()}


def validate_chain(native, compiler, tail, point):
    require(native["schema"] == "native-weak-idle-packing/1", "the literal repacked cover is required")
    require(profile(native["new_profile"]["targets"]) == TARGETS
            and profile(native["new_profile"]["paid"]) == PAID,
            "outer theorem uses the complete actual native packing profile")
    require(compiler["schema"] == "actual-native-packing-weak-compiler-integration/1",
            "actual named-role and chronological owner integration is required")
    require(profile(compiler["new_profile"]["targets"]) == TARGETS and profile(compiler["new_profile"]["paid"]) == PAID,
            "actual compiled role contract uses the same native packing profile")
    require(profile(tail["new_profile"]["targets"]) == TARGETS and profile(tail["new_profile"]["paid"]) == PAID,
            "independent analytic induction uses the same complete native packing profile")
    require(native["depth_zero_full_rank_check"]["unchanged_complete_rank_one_leaf_count"] == 127570
            and Q(compiler["compiled"]["leaves"]) == 127570
            and Q(compiler["compiled"]["width"]) == 2242,
            "actual depth-zero compiler pays every source complement")
    require(all(compiler["controls"].values()), "actual paid-owner integration controls all reject")
    require(compiler["native_certificate_sha256"] == COMPANIONS["native"]["sha256"]
            and compiler["actual_ordered_paid_word_sha256"] == native["paid_word"]["sha256"],
            "compiler uses precisely the authenticated literal native paid-owner word")
    require(tail["schema"] == "packed-native-weighted-tail-template/1", "the new weighted-tail theorem is required")
    require(Q(tail["tested_mixed_saving"]) == TESTED and Q(tail["uniform_saving"]) == UNIFORM,
            "the chosen finite rank pays this exact tested and uniform saving")
    require(point["parameters"]["tested_mixed_saving"] == TESTED
            and point["parameters"]["complex_uniform_saving"] == UNIFORM,
            "outer and finite-template exponents agree")
    require(tail["N"] == {"encoding": "2^H", "H": 756938551}, "exact fixed uniform template rank")
    require(Q(tail["strict_final_power_gap"]) == Q(1, 500000000)
            and Q(tail["complement_strict_gap"]) > 0
            and Q(tail["uniform_complement_gap"]) == Q(53737869, 200000000000),
            "point and uniform endpoint induction gaps are strictly positive")
    require(native["paid_integer_moments"] == {"P1": 36953, "P2": 71083, "P2_minus_2P1": -2823},
            "the weighted tail has an exact integer moment-ratio witness")
    require(max(PAID) == min(TARGETS) == 5 < max(TARGETS), "equal paid and target ranks retain the weak interface")


def build(source_root):
    engine = math_engine()
    sources = engine.bind_sources(source_root)
    receipts = replay_companions(source_root)
    native, compiler, tail = receipts["native"], receipts["compiler"], receipts["tail"]
    point = engine.parameter_point(KAPPA, TESTED)
    validate_chain(native, compiler, tail, point)
    mixed = engine.mixed_margin(TARGETS, PAID, TESTED)
    require(mixed[0] > 0, "independent exact mixed margin at the stronger tested point")
    crosscheck = engine.inherited_crosscheck(source_root, point)
    require(point["minimum_outer_slack"] == Q(498843579, 250000000000000000), "exact limiting outer slack")
    old_tail = deepcopy(tail)
    old_tail["uniform_saving"] = "0.002311658"
    old_rejected = False
    try:
        validate_chain(native, compiler, old_tail, point)
    except AssertionError:
        old_rejected = True
    require(old_rejected, "the previous weaker compiled saving does not establish this new point")
    previous_targets = {5: 102, 6: 90, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
    previous_paid = {1: 17521, 2: 5065, 3: 1738, 4: 714, 5: 254}
    previous_margin = engine.mixed_margin(previous_targets, previous_paid, TESTED)
    require(previous_margin[1] < 0, "the new tested saving needs the actual native repacking")
    return {
        "schema": "repacked-native-complete-conditional-outer-chain/1",
        "status": "PASS_NATIVE_PACKING_COMPILER_TAIL_AND_CONDITIONAL_KAPPA_00231284",
        "source_commit": SOURCE_COMMIT, "source_sha256": sources,
        "companion_sha256": {name: config["sha256"] for name, config in COMPANIONS.items()},
        "outer_family_generator_sha256": MATH_HASH,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"OUTER.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": TARGETS, "paid": PAID},
        "tested_mixed_margin": mixed, "outer": point, "inherited_crosscheck": crosscheck,
        "finite_template": {"tested_mixed_saving": TESTED, "uniform_saving": UNIFORM,
                            "N": tail["N"], "strict_final_power_gap": Q(tail["strict_final_power_gap"])},
        "strict_endpoint_corollary": {"root_bracket": native["root_bracket"],
                                      "uniform_complement_gap": Q(tail["uniform_complement_gap"]),
                                      "scope": "Every rational 0<kappa<C_* under the retained native and analytic hypotheses; C_* is not attained."},
        "controls": {"previous_weaker_uniform_template_rejected": old_rejected,
                     "previous_native_five_margin_at_new_test": previous_margin},
        "full_source_complement_check": native["depth_zero_full_rank_check"],
        "conditional_dependencies": [
            "The original source-bound autonomous native endpoint, all-column and physical adapter contracts, with the new exact idle-owner assignment.",
            "The weak-rank compiler, actual role/paid-owner instantiation, and separately proved weighted-tail recurrence charge every source complement and every owned-field call.",
            "This new fixed uniform template uses its own finite scalar, movement, owned-space, precision and row-stock counts in the retained generic formulas.",
            "The unchanged BIT supplier at admitted saving .0027 and inherited analytic decomposition, fine-prime padding, fixed-tape execution and exact recovery hypotheses.",
        ],
        "not_claimed": ["An unconditional integer-multiplication theorem.", "A formal verification of all native and analytic premises.",
                        "Practical or fully materialized finite-template counts.", "Global packing optimality or attainment of the local mixed root."],
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
        require((HERE/"OUTER.json").read_text() == text, "committed complete packed outer certificate differs from replay")
    print(json.dumps(engine.encode({"status": result["status"], "kappa": KAPPA, "uniform_saving": UNIFORM,
                                   "N": result["finite_template"]["N"],
                                   "minimum_outer_slack": result["outer"]["minimum_outer_slack"],
                                   "own_strict_checks": len(result["outer"]["strict_checks"]),
                                   "inherited_crosscheck": result["inherited_crosscheck"]}), sort_keys=True))


if __name__ == "__main__":
    main()
