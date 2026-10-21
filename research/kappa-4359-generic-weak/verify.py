#!/usr/bin/env python3
"""Exact constructive constants for the generic weak-separation theorem.

The complete quantified argument is in PROOF.md. A nontrivial exact example
has paid mean six and minimum target nine. The original integer flow and
the reviewed WeakRule are authenticated before one literal graph is built.
No native realization of this synthetic role contract is claimed.
Apache-2.0. Original mixed flow: PR4268; finite compiler: PR4359.
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
SOURCES = {
    "research/kappa-rebuild/transfer-audit/finite_dag_audit.py":
        "f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e",
    "research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md":
        "4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8",
}
COMPANIONS = {
    "kappa-4359-weak-compiler/verify.py":
        "33d43a20a55e3eb6200abb478f3ef9bcd3d866233cacd7930d15c87fa0759605",
    "kappa-4359-weak-compiler/CERTIFICATE.json":
        "2bd9043b77e5219e92d101c3c5f469bf302618ac932484f169f1ad3614ac1187",
    "kappa-4359-weak-separation/PROOF.md":
        "27b6c38776b46cac2a81910773b6d59ebbb3b1f3f7a321a87b80aa728cc884d9",
    "kappa-4359-generic-weak/boundary_check.py":
        "489283996fda6feb3faf62824e8509dd91ba519c4201aecf27b7197877f55428",
    "kappa-4359-generic-weak/BOUNDARY.md":
        "34b0832f0d6d07bf3be024348ecdd452cd52ffc3534e532f2a7ff1c47cf91070",
    "kappa-4359-generic-weak/BOUNDARY.json":
        "be06faf5ad6c9277f0c98067ced97431705513460c29c6062b954d5c6635a1a4",
}
TARGETS = {9: 1, 16: 1}
PAID = {1: 1, 4: 1, 9: 1}
TESTED = Q(1, 2)
UNIFORM = Q(3, 4)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(item) for item in value]
    return value


def integer_root(value, degree):
    """Floor of the positive integer degree-th root, by integer bisection."""
    require(type(value) is int and value >= 0 and type(degree) is int and degree >= 1,
            "integer-root arguments")
    if value <= 1 or degree == 1:
        return value
    low, high = 0, 1 << ((value.bit_length() + degree - 1) // degree)
    while high - low > 1:
        middle = (low + high) // 2
        if middle ** degree <= value:
            low = middle
        else:
            high = middle
    return low


def power_bounds(rank, exponent, bits):
    """Directed dyadic bounds for an integer rank to a rational power."""
    require(type(rank) is int and rank >= 1 and isinstance(exponent, Q)
            and exponent > 0 and type(bits) is int and bits >= 1,
            "positive rational-power arguments")
    a, degree = exponent.numerator, exponent.denominator
    value = rank ** a
    root = integer_root(value, degree)
    if root ** degree == value:
        return Q(root), Q(root)
    scale = 1 << bits
    lower_integer = integer_root(value << (bits * degree), degree)
    return Q(lower_integer, scale), Q(lower_integer + 1, scale)


def positive_mixed_certificate(targets, paid, t):
    """Refine until a strict positive margin is certified.

    The theorem assumes strict positivity. Refinement terminates on those
    inputs. A separated nonpositive interval is rejected; arbitrary exact
    equality is not promised a terminating classification.
    """
    coefficients = {rank: targets.get(rank, 0) - paid.get(rank, 0)
                    for rank in sorted(set(targets) | set(paid))}
    bits, tried = 1, []
    while True:
        powers = {rank: power_bounds(rank, t, bits) for rank in coefficients}
        lower = sum((count * powers[rank][0 if count >= 0 else 1]
                     for rank, count in coefficients.items()), Q(0))
        upper = sum((count * powers[rank][1 if count >= 0 else 0]
                     for rank, count in coefficients.items()), Q(0))
        tried.append(bits)
        if lower > 0:
            return {"precision_bits": bits, "precisions_tried": tried,
                    "coefficients": coefficients, "powers": powers,
                    "margin": (lower, upper)}
        require(upper > 0, "the strict mixed moment is not positive")
        bits *= 2


def validate_profile(targets, paid, t, z):
    require(targets and paid, "nonempty productive targets and paid word")
    require(all(type(rank) is int and rank >= 1 and type(count) is int and count >= 1
                for profile in (targets, paid) for rank, count in profile.items()),
            "positive integral ranks and multiplicities")
    require(isinstance(t, Q) and isinstance(z, Q) and 0 < t < z < 1,
            "fixed rational exponents with a strict positive saving gap")
    q, m = min(targets), max(targets)
    require(2 <= q < m and max(paid) <= q,
            "finite weak flow with strictly smaller recursive ranks")
    require(any(rank < q for rank in paid),
            "at least one positive-multiplicity paid rank is below q")


def choose_uniform_rank(t, z, b, gamma):
    """Unbounded dyadic exponent search; no fixed cap on J."""
    require(isinstance(t, Q) and isinstance(z, Q) and 0 < t < z < 1
            and type(b) is int and b >= 5 and type(gamma) is int and gamma >= 1,
            "positive fixed rational exponent gap and finite base constants")
    delta, j = z - t, 1
    while True:
        threshold = (b * (1 - t) + gamma * j) / delta
        h = max(b, 2 ** (j - 1), threshold.numerator // threshold.denominator + 1)
        if h < 2 ** j:
            return h, j
        j += 1


def constructive_parameters(targets, paid, t, z):
    validate_profile(targets, paid, t, z)
    mixed = positive_mixed_certificate(targets, paid, t)
    q, m = min(targets), max(targets)
    p1 = sum(rank * count for rank, count in paid.items())
    p2 = sum(rank * rank * count for rank, count in paid.items())
    u, eta0 = Q(p2, p1), t / m
    require(1 <= u < q and eta0 > 0, "strict rational paid-mean and complement bounds")
    h = 2
    while u ** h >= q ** (h - 1):
        h += 1
    alpha, theta = 1 - Q(1, h), 1 - Q(1, 2 * h)
    gamma = 1
    while theta ** gamma >= eta0 / 2:
        gamma += 1
    threshold = 2 * u / eta0
    d = threshold.numerator // threshold.denominator + 1
    n0 = max(m, 16, d ** (2 * h))
    b = n0.bit_length()
    H, J = choose_uniform_rank(t, z, b, gamma)
    require(u / d < eta0 / 2 and theta ** gamma < eta0 / 2,
            "both exit contributions fit their strict half margins")
    require(n0 >= 16 and theta >= Q(3, 4) and theta * 2 > 1,
            "theta*ln(n0)>1 follows from ln(2)>1/2")
    require(H >= b and n0 < 2 ** b and H < 2 ** J,
            "finite base and logarithmic rank comparisons")
    rank_gap = H * (z - t) - b * (1 - t) - gamma * J
    require(rank_gap > 0, "strict sufficient uniform-rank power gap")
    return {
        "targets": targets, "paid": paid, "t": t, "z": z,
        "mixed": mixed, "q": q, "m": m, "P_1": p1, "P_2": p2,
        "u": u, "eta_0": eta0, "h": h, "alpha": alpha,
        "theta": theta, "gamma": gamma, "D": d, "n_0": n0,
        "b": b, "tail_fraction_strict_upper": u / d,
        "complete_exit_coefficient_strict_upper": theta ** gamma + u / d,
        "eta_0_minus_exit_bound": eta0 - theta ** gamma - u / d,
        "A": {"encoding": "n_0^(1-t)", "n_0": n0, "exponent": 1 - t},
        "N": {"encoding": "2^H", "H": H}, "J": J,
        "strict_final_power_gap": rank_gap,
    }


def authenticate(source_root):
    for path, expected in SOURCES.items():
        require(sha256((source_root / path).read_bytes()).hexdigest() == expected,
                "unchanged predecessor source: " + path)
    for path, expected in COMPANIONS.items():
        require(sha256((HERE.parent / path).read_bytes()).hexdigest() == expected,
                "unchanged reviewed companion: " + path)
    path = HERE.parent / "kappa-4359-weak-compiler/verify.py"
    spec = importlib.util.spec_from_file_location("generic_weak_frozen_interface", path)
    weak = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = weak
    spec.loader.exec_module(weak)
    return weak, weak.load_original(source_root)


def exact_power(rank, exponent):
    value = rank ** exponent.numerator
    result = integer_root(value, exponent.denominator)
    require(result ** exponent.denominator == value,
            "this verification instance has an exact integral potential")
    return result


def rejection(call):
    try:
        call()
    except AssertionError:
        return True
    return False


def build(source_root):
    weak, original = authenticate(source_root)
    parameters = constructive_parameters(TARGETS, PAID, TESTED, UNIFORM)
    require((parameters["h"], parameters["gamma"], parameters["D"], parameters["b"],
             parameters["N"]["H"], parameters["J"]) == (9, 73, 449, 159, 3823, 12),
            "independent nontrivial exact parameter choices")
    require(parameters["mixed"]["margin"] == (1, 1)
            and parameters["strict_final_power_gap"] == Q(1, 4),
            "exact mixed and final strict margins")
    p_t = sum(count * exact_power(rank, TESTED) for rank, count in PAID.items())
    p_next = sum(count * exact_power(rank, TESTED + 1) for rank, count in PAID.items())
    require(p_t == 6 and p_next == 36 and Q(p_next, p_t) == 6 > 2
            and parameters["u"] == 7 < parameters["q"] == 9,
            "the new example is outside the earlier paid-ratio-below-two regime")
    eta = TESTED * Q(exact_power(16, TESTED), 16)
    require(eta == Q(1, 8) > parameters["eta_0"] == Q(1, 32),
            "the generic rational complement bound is conservative")

    roles = (("a", 9), ("b", 16))
    rounds = ((1, "a"), (4, "owned-C0"), (9, "b"))
    rule = weak.WeakRule(roles, rounds)
    require(dict(rule.targets) == TARGETS
            and Counter(rank for rank, owner in rounds) == PAID,
            "complete distinct named fields and every physical paid owner")
    tree = original.IntegerTree(rule, 1296)
    require(tree.depth == 2, "one meaningful two-generation flow")
    actual_exits = Counter(job["rank"] for batch in tree.exits for job in batch)
    expected_exits = Counter(prod(sequence) for sequence in
                             product((rank for rank, owner in rounds), repeat=tree.depth + 1))
    require(actual_exits == expected_exits,
            "complete exit histogram equals all ordered paid products")
    require(all(tree.rank < rule.dimension * rank <= rule.dimension * tree.rank
                for rank in tree.source_counter) and max(actual_exits) < tree.rank,
            "the full source band and strict exit-rank descent")
    require(any(field[0] == "owned" for unit in tree.units for field in unit["fields"].values()),
            "a paid owned center is an actual nested productive field")
    moments = []
    for exponent in (TESTED, Q(1), Q(2)):
        T = sum(count * exact_power(rank, exponent) for rank, count in TARGETS.items())
        P = sum(count * exact_power(rank, exponent) for rank, count in PAID.items())
        S = sum(count * exact_power(rank, exponent) for rank, count in tree.source_counter.items())
        E = sum(count * exact_power(rank, exponent) for rank, count in actual_exits.items())
        columns = sum(exact_power(unit["column"], exponent) for unit in tree.units)
        require(E == P ** (tree.depth + 1) and S - E == (T - P) * columns,
                "exact exit factorization and full internal-job cancellation")
        moments.append({"exponent": exponent, "T": T, "P": P, "S": S, "E": E,
                        "unit_column_moment": columns, "mixed_surplus": T - P})
    require(moments[1]["mixed_surplus"] == 11, "the automatic positive rank-one surplus")

    refinement = positive_mixed_certificate({2: 1, 3: 2}, {1: 2, 2: 2}, TESTED)
    require(refinement["precisions_tried"] == [1, 2, 4, 8]
            and refinement["margin"] == (Q(11, 256), Q(7, 128)),
            "a strict non-square mixed margin requires real directed refinement")
    cube_interval = power_bounds(2, Q(2, 3), 4)
    require(cube_interval[0] ** 3 < 4 < cube_interval[1] ** 3,
            "directed algebraic enclosure also handles a non-square denominator")
    close_gap = Q(1, 10 ** 50)
    close_H, close_J = choose_uniform_rank(TESTED, TESTED + close_gap,
                                          parameters["b"], parameters["gamma"])
    require(close_J > 128 and close_H < 2 ** close_J
            and close_H * close_gap > parameters["b"] * (1 - TESTED) + parameters["gamma"] * close_J,
            "the generic rank routine has no hidden fixed cap on J")

    h, gamma, d = parameters["h"], parameters["gamma"], parameters["D"]
    H, J, b = parameters["N"]["H"], parameters["J"], parameters["b"]
    controls = {
        "all_paid_ranks_equal_q_rejected": rejection(lambda:
            constructive_parameters({2: 1, 3: 1}, {2: 2}, TESTED, UNIFORM)),
        "empty_paid_word_rejected": rejection(lambda:
            constructive_parameters(TARGETS, {}, TESTED, UNIFORM)),
        "paid_rank_above_q_rejected": rejection(lambda:
            constructive_parameters(TARGETS, {1: 1, 10: 1}, TESTED, UNIFORM)),
        "rank_one_lattice_rejected": rejection(lambda:
            constructive_parameters({1: 1, 2: 1}, {1: 1}, TESTED, UNIFORM)),
        "exact_zero_mixed_margin_rejected": rejection(lambda:
            constructive_parameters(TARGETS, {1: 2, 4: 1, 9: 1}, TESTED, UNIFORM)),
        "zero_uniform_gap_rejected": rejection(lambda:
            choose_uniform_rank(TESTED, TESTED, b, gamma)),
        "one_less_h_fails_strict_mean_bound": parameters["u"] ** (h - 1) >= parameters["q"] ** (h - 2),
        "one_less_gamma_fails_strict_low_exit_bound": parameters["theta"] ** (gamma - 1) >= parameters["eta_0"] / 2,
        "one_less_D_fails_strict_high_exit_bound": parameters["u"] / (d - 1) >= parameters["eta_0"] / 2,
        "one_less_H_fails_strict_uniform_bound": (H - 1) * (UNIFORM - TESTED) <= b * (1 - TESTED) + gamma * J,
    }
    require(all(controls.values()), "all structural and strict-parameter controls discriminate")
    return encode({
        "schema": "generic-weak-separation-effective-logarithmic-template/1",
        "status": "PASS_GENERIC_RATIONAL_PARAMETERS_AND_NONMAXIMAL_PAID_BOUNDARY",
        "source_commit": COMMIT, "source_sha256": SOURCES,
        "companion_sha256": COMPANIONS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "case": parameters, "actual_paid_mean_at_t": Q(p_next, p_t),
        "actual_eta": eta, "exact_A": exact_power(parameters["n_0"], 1 - TESTED),
        "named_roles": roles, "ordered_paid_rounds": rounds,
        "materialized_flow": {"tree": tree.summary(), "moment_identities": moments,
                              "exact_ordered_product_histogram": dict(sorted(expected_exits.items()))},
        "algebraic_refinement_case": refinement,
        "non_square_denominator_interval": {"rank": 2, "t": Q(2, 3), "interval": cube_interval},
        "unbounded_rank_search_case": {"gap": close_gap, "H": close_H, "J": close_J},
        "controls": controls,
        "global_bound": "L(n)<=n_0^(1-t)*n^t*max(1,ln(n))^gamma for every positive integer n.",
        "strict_uniform_bound": "For each fixed rational t<z<1, the unbounded search specifies N=2^H with L(N)<N^z.",
        "scope": [
            "The theorem assumes a complete native mixed-unit contract, positive integral ranks and counts, 2<=q<m, r<=q, a nonempty paid word with some r<q, and a fixed rational strict mixed test 0<t<1.",
            "The synthetic positive example has R_t=6 and q=9; no native operator implementation is claimed for that example.",
            "The exact graph includes every source, exit, complement rank and paid owned field. No winning large template is materialized.",
            "All three parameter searches are unbounded; their termination is proved under the stated strict hypotheses.",
            "Dyadic algebraic refinement terminates on positive mixed margins; it is not a promised total equality classifier.",
            "The separate authenticated boundary receipt documents a real obstruction to the literal compiler's global bound when every paid rank equals q.",
            "All physical, arbitrary-input, spectator, adapter, scalar, restoration, precision and outer analytic premises remain separate obligations.",
        ],
    })


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
                "exact deterministic generic-theorem receipt replay")
    print(json.dumps({"status": result["status"], "N": result["case"]["N"],
                      "J": result["case"]["J"], "actual_paid_mean": result["actual_paid_mean_at_t"],
                      "graph_rank": result["materialized_flow"]["tree"]["rank"],
                      "strict_final_power_gap": result["case"]["strict_final_power_gap"],
                      "controls": len(result["controls"])}, sort_keys=True))


if __name__ == "__main__":
    main()
