#!/usr/bin/env python3
"""Smaller source-bound native template via the mean logarithmic exit rank.

The complete native/actual-compiler chain is replayed through its frozen
packed-tail receipt. New acceptance uses exact rational inequalities.
The quantified concavity and induction proof is in PROOF.md. Apache-2.0.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
PINS = {
    "kappa-4359-packed-tail/verify.py":
        "30140a9f186653784a498e31870dda91d0f2cd81a44c8c0097277084d77592a4",
    "kappa-4359-packed-tail/PROOF.md":
        "bd1745a1c0a7f13c86c381f6f352c390c0d8b9de219af267c4c5926bab69efe4",
    "kappa-4359-packed-tail/CERTIFICATE.json":
        "0d7286920f5b997fb948f91e26bb48e75fb0a05107bd41bfd0bc46ed9e88c15b",
}
TARGETS = {5: 140, 6: 52, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17559, 2: 5027, 3: 1738, 4: 714, 5: 254}
TESTED = Q("0.00231285")
UNIFORM = Q("0.002312848")
KAPPA = Q("0.00231284")
CAP = Q("0.00232")
THETA = Q(7, 16)
GAMMA = Q(1, 70)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_tail():
    for relative, expected in PINS.items():
        require(sha256((HERE.parent / relative).read_bytes()).hexdigest() == expected,
                "Changed frozen source/exit dependency: " + relative)
    path = HERE.parent / "kappa-4359-packed-tail/verify.py"
    spec = importlib.util.spec_from_file_location("log_mean_frozen_tail", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def choose_rank(c, u):
    require(0 < u < c < CAP, "The rank search needs a strict positive saving gap")
    for j in itertools.count(1):
        h = max(6, 2 ** (j - 1), (6 * c + GAMMA * j) // (c - u) + 1)
        if h < 2 ** j:
            return h, j


def build(source_root):
    tail = load_tail()
    previous = tail.build(source_root)
    expected = (HERE.parent / "kappa-4359-packed-tail/CERTIFICATE.json").read_text()
    require(json.dumps(previous, indent=2, sort_keys=True) + "\n" == expected,
            "Complete native, actual compiler, weak interface and tail replay")
    require(previous["source_commit"] == COMMIT
            and previous["status"] == "PASS_PACKED_NATIVE_STRICT_ENDPOINT_AND_EXPLICIT_TEMPLATE",
            "The same complete source-bound native construction is required")
    require({int(r): n for r, n in previous["new_profile"]["targets"].items()} == TARGETS
            and {int(r): n for r, n in previous["new_profile"]["paid"].items()} == PAID,
            "Exactly the same productive roles and complete paid invoice")
    require(previous["native_compiler_replay"]["paid_rounds"] == 25292
            and previous["native_compiler_replay"]["width"] == 2242
            and previous["native_compiler_replay"]["leaves"] == 127570,
            "Actual ownership and complete source-complement accounting")

    E = tail.load("kappa-4359-log-potential/verify.py", "log_mean_intervals")
    outer = tail.load("kappa-4359-outer-endpoint/verify.py", "log_mean_outer")
    require(Q(previous["tested_mixed_saving"]) == TESTED
            and Q(previous["uniform_saving"]) == UNIFORM
            and TESTED < Q(previous["root_bracket"][0])
            < Q(previous["root_bracket"][1]) < CAP,
            "The certified positive mixed test and full strict root family")
    require(2 <= min(TARGETS) == max(PAID) == 5 < max(TARGETS) == 57,
            "Finite weak matching and strictly decreasing recursive ranks")
    require(0 < GAMMA <= 1 and GAMMA.numerator == 1,
            "The concavity step requires gamma at most one")
    p1 = sum(r * count for r, count in PAID.items())
    p2 = sum(r * r * count for r, count in PAID.items())
    terms = {r: count * (r - 2) * r for r, count in PAID.items()}
    require(p1 == 36953 and p2 == 71083 and sum(terms.values()) == -2823,
            "Uniform paid-moment ratio remains strictly below two")
    require(terms[1] == -PAID[1] and terms[2] == 0
            and all(value > 0 for r, value in terms.items() if r > 2),
            "The termwise ratio proof is uniform for 0<t<=1")
    require(2 ** 16 < 5 ** 7 and THETA == Q(7, 16),
            "Exact bound log(2)/log(5)<theta")
    log2, log57 = E.log_integer(2), E.log_integer(57)
    require(log2[1] < Q(3, 4) and 3 < log57[0] < log57[1] < Q(81, 20),
            "Directed rational logarithms prove the affine comparison and eta bound")
    require(1 + Q(3, 4) == THETA * (1 + 3),
            "1+log(2)<theta*(1+log(57))")

    eta0 = (1 - CAP) * (1 - Q(81, 20) * CAP)
    theta_power_gap = eta0 ** GAMMA.denominator - THETA
    require(eta0 == Q(3088455621, 3125000000) > 0 and theta_power_gap > 0,
            "The new uniform logarithmic exit coefficient is below the complement margin")
    h, j = choose_rank(TESTED, UNIFORM)
    final_gap = h * (TESTED - UNIFORM) - 6 * TESTED - GAMMA * j
    require(h == 206938551 and j == 28 and h >= 6 and h < 2 ** j,
            "Exact new finite template and logarithmic power bound")
    require(final_gap == Q(1, 500000000),
            "Strict final uniform saving at the new rank")
    require((h - 1) * (TESTED - UNIFORM) <= 6 * TESTED + GAMMA * j,
            "One smaller H fails this sufficient strict inequality")
    require(eta0 ** 100 <= THETA,
            "The tempting smaller exponent gamma=1/100 fails this uniform comparison")
    tiny_h, tiny_j = choose_rank(TESTED, TESTED - Q(1, 10 ** 50))
    require(tiny_j > 128 and tiny_h < 2 ** tiny_j
            and tiny_h * Q(1, 10 ** 50) > 6 * TESTED + GAMMA * tiny_j,
            "The rank constructor has no fixed search cap for the strict family")

    point = outer.parameter_point(KAPPA, TESTED)
    require(point["parameters"]["complex_uniform_saving"] == UNIFORM
            and point["minimum_outer_slack"] == Q(498843579, 250000000000000000),
            "The new fixed uniform supplier provides the exact chosen outer saving")
    inherited = outer.inherited_crosscheck(source_root, point)
    require(inherited["inherited_checks"] == 63
            and inherited["matched_checks"] == 49
            and inherited["matched_outer_rows"] == 9,
            "Every inherited outer predicate and cost row is independently cross-checked")
    return {
        "schema": "packed-native-logarithmic-mean-template/1",
        "status": "PASS_NATIVE_LOG_MEAN_SMALLER_TEMPLATE_AND_FULL_OUTER",
        "source_commit": COMMIT,
        "source_sha256": previous["source_sha256"],
        "companion_sha256": PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": TARGETS, "paid": PAID},
        "native_paid_word_sha256": previous["native_paid_word_sha256"],
        "actual_role_contract_sha256": previous["actual_role_contract_sha256"],
        "tested_mixed_saving": str(TESTED), "uniform_saving": str(UNIFORM),
        "root_bracket": previous["root_bracket"],
        "uniform_saving_cap": str(CAP),
        "P_1": p1, "P_2": p2, "uniform_paid_ratio_integer_gap": p2 - 2 * p1,
        "theta": str(THETA), "gamma": str(GAMMA), "uniform_eta_lower": str(eta0),
        "exact_theta_power_gap": str(theta_power_gap),
        "log_2": E.outward(log2), "log_57": E.outward(log57),
        "exit_identity": "E_a=P_a^(G+1); E_t-weighted mean(log(e))=(G+1)*P'_t/P_t",
        "global_leaf_bound": "L(n)<=57^C*n^(1-C)*(1+log(n))^(1/70) for every strict 0<C<C_packed",
        "N": {"encoding": "2^H", "H": h}, "H_binary_upper_exponent": j,
        "previous_N_at_same_uniform_saving": previous["N"],
        "strict_final_power_gap": str(final_gap),
        "outer": outer.encode(point), "inherited_crosscheck": outer.encode(inherited),
        "native_compiler_replay": previous["native_compiler_replay"],
        "controls": {
            "gamma_one_over_100_fails_stated_uniform_comparison": True,
            "one_smaller_H_fails_stated_strict_rank_bound": True,
            "strict_gap_beyond_old_search_cap": {"J": tiny_j, "H": tiny_h},
        },
        "scope": [
            "Two concavity steps and the complete source/exit induction are proved in PROOF.md; finite arithmetic checks do not replace that proof.",
            "The entire actual native and compiler chain is authenticated and replayed before the new smaller rank is accepted.",
            "All source complements, paid owned-field calls, physical adapters and whole spectators remain charged.",
            "The new finite template has its own complete scalar, movement, storage, precision and reserve constants.",
            "The inherited native/all-column, fixed-tape, analytic and exact-recovery hypotheses remain conditional.",
            "The local mixed root is unchanged; no materialized winning template, practical runtime, or endpoint attainment is claimed.",
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
        require((HERE / "CERTIFICATE.json").read_text() == serialized,
                "Deterministic smaller-template certificate replay")
    print(json.dumps({key: result[key] for key in (
        "status", "tested_mixed_saving", "uniform_saving", "N",
        "previous_N_at_same_uniform_saving", "strict_final_power_gap",
        "inherited_crosscheck")}, sort_keys=True))


if __name__ == "__main__":
    main()
