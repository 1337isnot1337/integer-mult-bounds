#!/usr/bin/env python3
"""Source-bound uniform tail and finite-rank certificate for native repacking.

The native packing and actual compiler integration are authenticated and
replayed. Independent rational arithmetic checks the new mixed root,
uniform sufficient tail conditions, and the specified stronger template.
The quantified strict-endpoint argument is in PROOF.md. Apache-2.0.
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
ROOT = HERE.parents[1]
COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
PINS = {
    "kappa-4359-native-packing/verify.py":
        "9edf27738981b58c2bf8ca03bb70631c200aad0ca9948372f1c58fc445894da0",
    "kappa-4359-native-packing/README.md":
        "613b77c71ba3567ac07d83645025f59ec6bf92b6d92f94b45175311efa90bd00",
    "kappa-4359-native-packing/CERTIFICATE.json":
        "5c8cc831151aa7147e6c3dd2a6832d19026aecc660955131149bdc54f0b26878",
    "kappa-4359-native-packing/compiler_check.py":
        "52db679010d8da9aedd9eff7c111e5e39992188579f0596c6393837b90269c24",
    "kappa-4359-native-packing/COMPILER.md":
        "9a4402e6358a0cb862dc4cb79ff44965514a9f1522144f7581835f7839d4ba27",
    "kappa-4359-native-packing/COMPILER.json":
        "1cd2f4d3b115d2220f24f857748399f9637bc31269a90ca590bdd2301df710e6",
    "kappa-4359-weak-compiler/verify.py":
        "33d43a20a55e3eb6200abb478f3ef9bcd3d866233cacd7930d15c87fa0759605",
    "kappa-4359-weak-compiler/CERTIFICATE.json":
        "2bd9043b77e5219e92d101c3c5f469bf302618ac932484f169f1ad3614ac1187",
    "kappa-4359-weak-separation/PROOF.md":
        "27b6c38776b46cac2a81910773b6d59ebbb3b1f3f7a321a87b80aa728cc884d9",
    "kappa-4359-weak-separation/ENDPOINT.md":
        "e117bdeda7cfeb6537b9154f1b7491ab6d88b51b6cef191c27115421efb36b57",
    "kappa-4359-weak-separation/endpoint_verify.py":
        "097f7ed387d7f57ac3248d32f977f3904fd921a1b66316ad969ef10b323567ee",
    "kappa-4359-log-potential/verify.py":
        "ad92ee3790c441f7e3065e70527ada8a038f21ca70005832c67476d7f146e2ad",
    "kappa-4359-outer-endpoint/verify.py":
        "4a51eea1d796224e4a8bb6e2031146ba743e63ed88b2e7e241093a7025a063de",
    "kappa-4359-outer-endpoint/README.md":
        "de633bf01e893f2e2fcb87ec50c86688d6b0b676d1941c04a276b305db3646de",
}
TARGETS = {5: 140, 6: 52, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17559, 2: 5027, 3: 1738, 4: 714, 5: 254}
TESTED = Q("0.00231285")
UNIFORM = Q("0.002312848")
KAPPA = Q("0.00231284")
CAP = Q("0.00232")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load(relative, name):
    path = HERE.parent / relative
    require(relative in PINS and sha256(path.read_bytes()).hexdigest() == PINS[relative],
            "Authenticated executable companion: " + relative)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def replay_matches(relative, result):
    require((HERE.parent / relative).read_text() == json.dumps(result, indent=2, sort_keys=True) + "\n",
            "Complete deterministic companion replay: " + relative)


def profile(receipt):
    return ({int(k): v for k, v in receipt["new_profile"]["targets"].items()},
            {int(k): v for k, v in receipt["new_profile"]["paid"].items()})


def merge_sources(*groups):
    result = {}
    for group in groups:
        for path, digest in group.items():
            require(path not in result or result[path] == digest,
                    "All source-bound dependencies agree on the same predecessor bytes")
            result[path] = digest
    return result


def build(source_root):
    for relative, expected in PINS.items():
        require(sha256((HERE.parent / relative).read_bytes()).hexdigest() == expected,
                "Changed pinned companion: " + relative)
    native_module = load("kappa-4359-native-packing/verify.py", "tail_packed_native")
    native, cover = native_module.build(source_root)
    replay_matches("kappa-4359-native-packing/CERTIFICATE.json", native)
    compiler_module = load("kappa-4359-native-packing/compiler_check.py", "tail_packed_compiler")
    compiler = compiler_module.build(source_root)
    replay_matches("kappa-4359-native-packing/COMPILER.json", compiler)
    weak_module = load("kappa-4359-weak-compiler/verify.py", "tail_weak_interface")
    weak = weak_module.build(source_root)
    replay_matches("kappa-4359-weak-compiler/CERTIFICATE.json", weak)
    require(native["schema"] == "native-weak-idle-packing/1"
            and native["status"] == "PASS_LITERAL_REPACKING_FULL_NATIVE_INVOICE_AND_EXACT_MIXED_ROOT",
            "Complete literal native repacking is a required hypothesis")
    require(compiler["schema"] == "actual-native-packing-weak-compiler-integration/1"
            and compiler["status"] == "PASS_ACTUAL_PACKED_NATIVE_OWNERS_CAUSALITY_AND_RANK57_COMPILATION",
            "The actual new physical word passes the changed compiler interface")
    require(native["source_commit"] == compiler["source_commit"] == weak["source_commit"] == COMMIT,
            "One immutable predecessor for all three native and compiler contracts")
    require(profile(native) == profile(compiler) == (TARGETS, PAID), "Exactly the same new complete tariff")
    require(compiler["native_certificate_sha256"] == PINS["kappa-4359-native-packing/CERTIFICATE.json"]
            and compiler["native_producer_sha256"] == PINS["kappa-4359-native-packing/verify.py"],
            "Actual compiler receipt binds this native construction")
    require(compiler["actual_ordered_paid_word_sha256"] == native["paid_word"]["sha256"],
            "Actual paid owners and chronology agree, beyond their histograms")
    require(all(native["controls"].values()) and all(compiler["controls"].values())
            and all(weak["controls"].values()), "Native, lifetime, ownership and rank guards discriminate invalid inputs")
    require(weak["controls"]["minimum_one_nonterminating_lattice_rejected"],
            "The generic weak interface still excludes a nonterminating rank-one lattice")
    compiled = compiler["compiled"]
    require((compiled["width"], compiled["leaves"], compiled["units"]) == (2242, 127570, 1)
            and compiled["owned_fields_uncredited"] == 1, "Every actual rank57 source complement remains paid")
    require(compiler["paid_rounds"] == native["paid_word"]["rounds"] == 25292,
            "All actual paid calls, including owned-center calls, are retained")
    derived_targets = Counter({25: 448, 57: 224})
    derived_targets.update(row["target_rank"] for row in cover["fresh_outputs"])
    require(dict(derived_targets) == TARGETS and len(cover["fresh_outputs"]) == 1570,
            "Independent fresh-endpoint recount from the entire derived native cover")

    E = load("kappa-4359-log-potential/verify.py", "tail_independent_intervals")
    family = load("kappa-4359-weak-separation/endpoint_verify.py", "tail_unbounded_rank_family")
    outer = load("kappa-4359-outer-endpoint/verify.py", "tail_strict_outer_family")
    outer_sources = outer.bind_sources(source_root)
    sources = merge_sources(native["source_sha256"], compiler["source_sha256"],
                            weak["source_sha256"], outer_sources)
    m, q, rmax = max(TARGETS), min(TARGETS), max(PAID)
    require(2 <= q == rmax == 5 < m == 57, "The weak flow has finite depth and strictly smaller recursive exits")
    t = 1 - TESTED
    require(0 < KAPPA < UNIFORM < TESTED < CAP < Q("0.0027") < Q(1, 32),
            "Fresh strict supplier and outer gaps lie below the valid uniform cap")
    mixed = E.mixed_margin(TARGETS, PAID, TESTED)
    require(mixed[0] > 0, "Independently positive tested mixed surplus")
    lower, upper = map(Q, native["root_bracket"])
    require(lower == Q("0.002312854665364207351198238279")
            and upper == Q("0.002312854665364207351198238280")
            and TESTED < lower < upper < CAP, "Exact root interval and fresh uniform cap")
    lower_margin = E.mixed_margin(TARGETS, PAID, lower)
    upper_margin = E.mixed_margin(TARGETS, PAID, upper)
    cap_margin = E.mixed_margin(TARGETS, PAID, CAP)
    require(lower_margin[0] > 0 and upper_margin[1] < 0 and cap_margin[1] < 0,
            "Both root signs and the larger cap are independently separated")
    require(all(k >= q for k in TARGETS) and all(r <= q for r in PAID)
            and any(k > q for k in TARGETS), "The scaled mixed surplus is strictly increasing in t")
    f0 = sum(TARGETS.values()) - sum(PAID.values())
    p1 = sum(r * count for r, count in PAID.items())
    p2 = sum(r * r * count for r, count in PAID.items())
    target_mass = sum(k * count for k, count in TARGETS.items())
    f1 = Q(target_mass - p1, q)
    require(f0 == -23050 and f1 == Q(224, 5), "There is one mixed root and every smaller saving has positive surplus")
    terms = {r: count * (r - 2) * r for r, count in PAID.items()}
    require(p1 == 36953 and p2 == 71083 and sum(terms.values()) == p2 - 2 * p1 == -2823,
            "Uniform integer paid-tail inequality throughout 0<t<=1")
    require(terms[1] == -PAID[1] and terms[2] == 0
            and all(value > 0 for r, value in terms.items() if r >= 3),
            "The termwise bound uses only positive increasing r^t terms and the fixed rank-one term")
    theta, gamma, ell = Q(3, 4), Q(1, 20), Q(81, 20)
    v, tail = Q(505, 512), Q(1, 8)
    coefficient = v + (1 - v) * tail
    require(4 < q and m ** 3 > 16 ** 4 and theta < v ** 20,
            "Exact large-exit and logarithmic low-exit constants")
    require(theta * E.log_integer(m)[0] > 1 and E.log_integer(m)[1] < ell,
            "Rank-one logarithmic bound and exact complement logarithm")
    eta_lower = (1 - TESTED) * (1 - ell * TESTED)
    uniform_eta_lower = (1 - CAP) * (1 - ell * CAP)
    require(1 - ell * CAP > 0 and coefficient == Q(4047, 4096), "Uniform decreasing positive complement factors")
    require(uniform_eta_lower - coefficient == Q(53737869, 200000000000) > 0
            and eta_lower > uniform_eta_lower, "The larger native root still has strict uniform complement slack")
    h, j = family.choose_family_rank(TESTED, UNIFORM)
    final_gap = h * (TESTED - UNIFORM) - 6 * TESTED - gamma * j
    require(h == 756938551 and j == 30 and final_gap == Q(1, 500000000), "Exact sufficient stronger finite template")
    require(h >= 6 and h < 2 ** j and m < 2 ** 6, "All sufficient final logarithmic bounds")
    require((h - 1) * (TESTED - UNIFORM) <= 6 * TESTED + gamma * j,
            "One smaller H does not satisfy this strict sufficient inequality")
    previous_targets, previous_paid = dict(TARGETS), dict(PAID)
    previous_targets[5] -= 38
    previous_targets[6] += 38
    previous_paid[1] -= 38
    previous_paid[2] += 38
    previous_margin = E.mixed_margin(previous_targets, previous_paid, TESTED)
    require(previous_margin[1] < 0, "The previous native tariff cannot claim the new tested saving")
    point = outer.parameter_point(KAPPA, TESTED)
    require(point["parameters"]["complex_uniform_saving"] == UNIFORM
            and point["minimum_outer_slack"] == Q(498843579, 250000000000000000),
            "The exact selected uniform supplier pays the chosen strict outer point")
    return {
        "schema": "packed-native-weighted-tail-template/1",
        "status": "PASS_PACKED_NATIVE_STRICT_ENDPOINT_AND_EXPLICIT_TEMPLATE",
        "source_commit": COMMIT, "source_sha256": sources, "companion_sha256": PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": TARGETS, "paid": PAID},
        "native_paid_word_sha256": native["paid_word"]["sha256"],
        "actual_role_contract_sha256": compiler["actual_role_contract_sha256"],
        "tested_mixed_saving": str(TESTED), "uniform_saving": str(UNIFORM),
        "strict_mixed_margin": E.outward(mixed),
        "previous_tariff_margin_at_new_saving": E.outward(previous_margin),
        "root_bracket": native["root_bracket"],
        "root_margins": {"lower": E.outward(lower_margin), "upper": E.outward(upper_margin), "cap": E.outward(cap_margin)},
        "scaled_root_endpoint_values": {"F_0": f0, "F_1": str(f1)},
        "uniform_saving_cap": str(CAP), "t": str(t), "q": q, "m": m, "r_max": rmax,
        "P_1": p1, "P_2": p2, "uniform_paid_ratio_integer_gap": p2 - 2 * p1,
        "theta": str(theta), "gamma": str(gamma),
        "high_exit_fraction_strict_upper": str(tail),
        "complete_exit_coefficient_strict_upper": str(coefficient),
        "eta_lower": str(eta_lower), "complement_strict_gap": str(eta_lower - coefficient),
        "uniform_eta_lower": str(uniform_eta_lower),
        "uniform_complement_gap": str(uniform_eta_lower - coefficient),
        "exact_exit_moment": "E_a=P_a^(G+1), G=floor(log_5(n/57))",
        "global_leaf_bound": "For every 0<C<C_packed, L(n)<=57^C*n^(1-C)*max(1,log(n))^(1/20).",
        "N": {"encoding": "2^H", "H": h}, "H_binary_upper_exponent": j,
        "strict_final_power_gap": str(final_gap),
        "strict_uniform_moment": "P_N/B_N < N^(1-uniform_saving)",
        "outer": outer.encode(point),
        "full_endpoint_family": "Every fixed rational 0<kappa<C_packed, with its own fixed rational tested c, uniform U, finite template and complete constants.",
        "rank_algorithm": "Unbounded J search from the pinned endpoint verifier; H=max(6,2^(J-1),floor((6C+J/20)/(C-U))+1), accepting H<2^J.",
        "native_compiler_replay": {"width": compiled["width"], "leaves": compiled["leaves"],
                                   "units": compiled["units"], "paid_rounds": compiler["paid_rounds"],
                                   "native_controls": native["controls"], "compiler_controls": compiler["controls"]},
        "controls": {"previous_native_tariff_rejected_at_new_test": True,
                     "one_smaller_H_fails_stated_strict_rank_bound": True,
                     "previous_endpoint_cap_is_too_small": Q("0.002312") < TESTED,
                     "new_uniform_cap_is_above_root_and_not_a_valid_mixed_test": True},
        "scope": [
            "The complete new native cover, actual physical paid owners, and changed weak compiler guard are authenticated and replayed.",
            "All source complements, owned-center payments, whole-job adapters and complete spectators remain in the contract.",
            "The general strict family uses written monotonicity, source/exit cancellation, weighted-tail induction and unbounded rank search; finite point checks are not a proof of the quantified statement.",
            "The original native, all-column, fixed-tape, analytic, fine-prime and exact-recovery premises remain required.",
            "Each newly compiled word has its own complete scalar, movement, owned-space, precision and row-stock constants, fixed before input length varies.",
            "No root attainment, materialized large template, or practical-size claim is made.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(serialized)
    else:
        require((HERE / "CERTIFICATE.json").read_text() == serialized, "Exact complete packed-tail certificate replay")
    print(json.dumps({key: result[key] for key in
                      ("status", "tested_mixed_saving", "uniform_saving", "N", "root_bracket",
                       "uniform_complement_gap", "strict_final_power_gap")}, sort_keys=True))


if __name__ == "__main__":
    main()
