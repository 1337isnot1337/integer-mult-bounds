#!/usr/bin/env python3
"""Certify uniform sufficient conditions below the native width-five root.

The quantified endpoint theorem is in ENDPOINT.md. This receipt checks
its source-bound integer inequalities, strict root bracket, unbounded
rank search at a concrete point, and literal equality-tree exit products.
It leaves the frozen concrete proof and certificate unchanged.
Apache-2.0.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import prod
from pathlib import Path
import argparse
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
COMPANION_PINS = {
    "kappa-4359-weak-separation/verify.py":
        "07a950c217320b2770b783e8b2b0bf9bf039e9b336bb9156f1bb162bd2fd7a1c",
    "kappa-4359-weak-separation/PROOF.md":
        "27b6c38776b46cac2a81910773b6d59ebbb3b1f3f7a321a87b80aa728cc884d9",
    "kappa-4359-weak-separation/CERTIFICATE.json":
        "98c20fc702867a3d292ca5e9b9557773f7a132d859425deb9b519f1ad1379717",
    "kappa-4359-native-five/CERTIFICATE.json":
        "9a4036e30d38be476cd529b4aebba40270f719744c13a86efd9306892d903ed8",
    "kappa-4359-weak-compiler/verify.py":
        "33d43a20a55e3eb6200abb478f3ef9bcd3d866233cacd7930d15c87fa0759605",
    "kappa-4359-outer-endpoint/verify.py":
        "4a51eea1d796224e4a8bb6e2031146ba743e63ed88b2e7e241093a7025a063de",
    "kappa-4359-outer-endpoint/README.md":
        "de633bf01e893f2e2fcb87ec50c86688d6b0b676d1941c04a276b305db3646de",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_module(relative, name):
    path = HERE.parent / relative
    require(relative in COMPANION_PINS, "An imported companion must be explicitly pinned")
    require(sha256(path.read_bytes()).hexdigest() == COMPANION_PINS[relative],
            "Changed imported companion: " + relative)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def choose_family_rank(tested, uniform):
    """No finite search cap: each strict rational gap has a finite answer."""
    gap = tested - uniform
    require(0 < uniform < tested < 1, "A positive strict uniform gap is required")
    j = 1
    while True:
        threshold = (6 * tested + Q(j, 20)) / gap
        h = max(6, 2 ** (j - 1), threshold.numerator // threshold.denominator + 1)
        if h < 2 ** j:
            require(h * gap > 6 * tested + Q(j, 20), "Strict sufficient final rank")
            return h, j
        j += 1


def equality_exit_products(source_root):
    weak = load_module("kappa-4359-weak-compiler/verify.py", "endpoint_equality_interface")
    original = weak.load_original(source_root)
    roles = (("a", 2), ("b", 2), ("c", 3))
    rounds = ((1, "a"), (2, "owned-C0"), (1, "b"), (2, "c"))
    rule = weak.WeakRule(roles, rounds)
    paid_ranks = tuple(rank for rank, owner in rounds)
    rows = []
    for rank in (3, 6, 12, 24, 48):
        tree = original.IntegerTree(rule, rank)
        actual = Counter(job["rank"] for batch in tree.exits for job in batch)
        expected = Counter(prod(path) for path in product(paid_ranks, repeat=tree.depth + 1))
        require(actual == expected, "All literal exits equal the ordered paid-round products")
        moments = {}
        for power in range(4):
            moment = sum(count * size ** power for size, count in actual.items())
            require(moment == sum(size ** power for size in paid_ranks) ** (tree.depth + 1),
                    "The complete literal exit histogram has the claimed moment")
            moments[power] = moment
        rows.append({"rank": rank, "generations": tree.depth,
                     "exit_histogram": dict(sorted(actual.items())), "integer_moments": moments})
    return {"paid_round_ranks": paid_ranks, "cases": rows,
            "scope": "Complete equality-case exit histograms, including repeated paid ranks, compared with independently enumerated ordered rank products."}


def build(source_root):
    for relative, expected in COMPANION_PINS.items():
        require(sha256((HERE.parent / relative).read_bytes()).hexdigest() == expected,
                "Changed pinned companion: " + relative)
    core = load_module("kappa-4359-weak-separation/verify.py", "endpoint_concrete_weak_proof")
    concrete = core.build(source_root)
    require((HERE / "CERTIFICATE.json").read_text()
            == json.dumps(concrete, indent=2, sort_keys=True) + "\n",
            "Complete deterministic concrete weak-certificate replay")
    native = json.loads((HERE.parent / "kappa-4359-native-five/CERTIFICATE.json").read_text())
    require(native["source_commit"] == concrete["source_commit"] == COMMIT,
            "The native and compiler theorems have the same immutable predecessor")
    targets, paid = core.TARGETS, core.PAID
    require({int(k): v for k, v in native["new_profile"]["targets"].items()} == targets
            and {int(k): v for k, v in native["new_profile"]["paid"].items()} == paid,
            "The full endpoint family uses the identical native tariff")
    E = core.arithmetic()
    q, m = min(targets), max(targets)
    require(q == 5 and m == 57 and max(paid) == q,
            "The monotonicity and weighted-tail proof use the actual weak separation")
    require(all(k >= q for k in targets) and all(r <= q for r in paid)
            and any(k > q for k in targets), "Strictly increasing scaled mixed surplus")
    f0 = sum(targets.values()) - sum(paid.values())
    f1 = Q(sum(k * count for k, count in targets.items())
           - sum(r * count for r, count in paid.items()), q)
    require(f0 == -23050 and f1 == Q(224, 5), "Unique root strictly between zero and one")
    lower, upper = map(Q, native["root_bracket"])
    require(lower == Q("0.002311660492818048695136925339")
            and upper == Q("0.002311660492818048695136925340"), "Exact native root bracket")
    lower_margin = E.mixed_margin(targets, paid, lower)
    upper_margin = E.mixed_margin(targets, paid, upper)
    require(lower_margin[0] > 0 and upper_margin[1] < 0,
            "Independent strictly positive and negative root-bracket signs")
    cap = Q("0.002312")
    cap_margin = E.mixed_margin(targets, paid, cap)
    require(upper < cap < Q("0.0027") < Q(1, 32) and cap_margin[1] < 0,
            "One uniform rational cap above the unique root and below the BIT supplier")
    p1 = sum(count * rank for rank, count in paid.items())
    p2 = sum(count * rank ** 2 for rank, count in paid.items())
    terms = {rank: count * (rank - 2) * rank for rank, count in paid.items()}
    require(p1 == 36991 and p2 == 71197 and sum(terms.values()) == p2 - 2 * p1 == -2785,
            "Uniform paid-moment ratio follows from the exact integer termwise bound")
    require(terms[1] == -paid[1] and terms[2] == 0
            and all(value > 0 for rank, value in terms.items() if rank >= 3),
            "All nonconstant terms have the sign required to use r^t<=r")
    theta, gamma, ell = Q(3, 4), Q(1, 20), Q(81, 20)
    v, tail = Q(505, 512), Q(1, 8)
    coefficient = v + (1 - v) * tail
    require(4 < q and m ** 3 > 16 ** 4 and theta < v ** 20,
            "Fixed exit-tail and low-exit logarithmic inequalities")
    require(theta * E.log_integer(m)[0] > 1 and E.log_integer(m)[1] < ell,
            "Uniform logarithmic base and complement comparisons")
    eta_lower = (1 - cap) * (1 - ell * cap)
    require(1 - ell * cap > 0 and coefficient == Q(4047, 4096),
            "Both decreasing complement factors remain positive")
    require(eta_lower - coefficient == Q(1544696341, 5000000000000) > 0,
            "The same strict complement margin holds throughout the endpoint interval")
    engine = load_module("kappa-4359-outer-endpoint/verify.py", "endpoint_outer_parameter_family")
    sources = engine.bind_sources(source_root)
    sources.update(core.SOURCE_PINS)
    point = engine.parameter_point(Q("0.00231165"), Q("0.00231166"))
    p = point["parameters"]
    h, j = choose_family_rank(p["tested_mixed_saving"], p["complex_uniform_saving"])
    require(h == concrete["N"]["H"] == 756934981 and j == 30,
            "The unbounded family search reproduces the concrete sufficient rank")
    narrow_h, narrow_j = choose_family_rank(Q(1, 1000), Q(1, 1000) - Q(1, 10 ** 50))
    require(narrow_j > 128 and narrow_h < 2 ** narrow_j,
            "The family search handles strict rational gaps beyond the former convenience cap")
    zero_gap_rejected = False
    try:
        choose_family_rank(Q(1, 1000), Q(1, 1000))
    except AssertionError:
        zero_gap_rejected = True
    require(zero_gap_rejected, "Endpoint equality cannot be passed to the strict-rank search")
    return {
        "schema": "native-width-five-strict-endpoint-family/1",
        "status": "PASS_UNIFORM_SUFFICIENT_CONDITIONS_FOR_ALL_STRICT_NATIVE_FIVE_SAVINGS",
        "source_commit": COMMIT, "source_sha256": sources, "companion_sha256": COMPANION_PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "ENDPOINT.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": targets, "paid": paid},
        "scaled_mixed_root": {"divisor": q, "F_at_0": f0, "F_at_1": str(f1),
                              "strict_monotonicity": "Every target k>=q and every paid r<=q; at least one target has k>q."},
        "root_bracket": native["root_bracket"],
        "mixed_margins": {"lower_root_bracket": E.outward(lower_margin),
                          "upper_root_bracket": E.outward(upper_margin),
                          "uniform_cap": E.outward(cap_margin)},
        "uniform_saving_cap": str(cap), "P_1": p1, "P_2": p2,
        "termwise_P_next_minus_2P_upper": terms, "strict_integer_ratio_gap": p2 - 2 * p1,
        "theta": str(theta), "gamma": str(gamma),
        "high_exit_fraction_strict_upper": str(tail),
        "complete_exit_coefficient_strict_upper": str(coefficient),
        "uniform_eta_lower": str(eta_lower), "uniform_complement_gap": str(eta_lower - coefficient),
        "global_leaf_bound": "For every 0<C<C_star, L(n)<=57^C*n^(1-C)*max(1,log(n))^(1/20).",
        "outer_family": "For every rational 0<kappa<C_star choose rational kappa<c<C_star and d=(c-kappa)/5; U=c-d, b=c-2d, a=c-3d, q=c-4d, epsilon=1-d, beta=1-3d.",
        "rank_family": "Unbounded J search; H=max(6,2^(J-1),floor((6c+J/20)/(c-U))+1), accepting H<2^J.",
        "concrete_outer_point": engine.encode(point),
        "concrete_rank": {"H": h, "J": j},
        "equality_exit_products": equality_exit_products(source_root),
        "controls": {"zero_uniform_gap_rejected": zero_gap_rejected,
                     "narrow_gap_beyond_128_checked": {"gap": str(Q(1, 10 ** 50)), "H": narrow_h, "J": narrow_j},
                     "uniform_cap_above_root_rejected_as_mixed_test": True},
        "scope": [
            "The quantified result follows from the written monotonicity, uniform tail induction, unbounded rank search, and previously proved outer parameter family.",
            "The source-bound native, whole-job-adapter, complete-spectator, all-column, fixed-tape, analytic and exact-recovery hypotheses remain required.",
            "Every fixed strict saving has its own finite compiled word and its own complete constants.",
            "The root itself is not attained, and no practical-size or materialized-template claim is made.",
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
        require((HERE / "ENDPOINT.json").read_text() == serialized, "Exact endpoint receipt replay")
    print(json.dumps({key: result[key] for key in
                      ("status", "root_bracket", "uniform_saving_cap", "strict_integer_ratio_gap",
                       "uniform_complement_gap", "concrete_rank")}, sort_keys=True))


if __name__ == "__main__":
    main()
