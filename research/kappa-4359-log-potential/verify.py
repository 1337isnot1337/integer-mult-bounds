#!/usr/bin/env python3
"""Check smaller finite template ranks using a logarithmic superpotential.

The checker uses only integer and Fraction arithmetic. It authenticates the
pending PR #4359 inputs, independently encloses their mixed moments, and
checks the sufficient inequalities in PROOF.md. It does not emit the finite
native words or formally verify their operator contracts.
"""
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
SOURCE_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
PINS = {
    "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz":
        "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f",
    "research/kappa-rebuild/bit/MIXED-PRODUCTIVE-BIT.json":
        "2f69a19f417c0e0d141c180f9b2fae3d358391b9a230f5848ee07c45450e70bf",
    "research/kappa-rebuild/controller/EXPLICIT-TEMPLATE-BOUNDS.json":
        "3f1abfafa6f1bb192aafdf342a33ef60fd469fb0764be3eb1516984fc3c22c3f",
    "research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md":
        "4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8",
    "research/kappa-rebuild/transfer-audit/finite_dag_audit.py":
        "f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def log_near_one(value, terms=64):
    """Enclose log(value) for 1 <= value <= 2 by the atanh series."""
    value = Q(value)
    require(1 <= value <= 2, "Logarithm argument reduction")
    z = (value - 1) / (value + 1)
    square = z * z
    power = z
    partial = Q(0)
    for j in range(terms):
        partial += 2 * power / (2 * j + 1)
        power *= square
    # The uncomputed denominators are at least 2*terms+1.
    remainder = 2 * power / ((2 * terms + 1) * (1 - square))
    return partial, partial + remainder


@lru_cache(None)
def log_integer(value):
    require(isinstance(value, int) and value >= 1, "Positive integral rank")
    shift = value.bit_length() - 1
    residual = log_near_one(Q(value, 2**shift))
    ln2 = log_near_one(Q(2))
    return residual[0] + shift * ln2[0], residual[1] + shift * ln2[1]


def exp_negative(value, terms=64):
    """Alternating-series enclosure of exp(-value), for 0 <= value < 1."""
    require(0 <= value < 1 and terms % 2 == 0, "Exponential series conditions")
    term = Q(1)
    total = term
    for j in range(1, terms + 1):
        term *= -value / j
        total += term
    lower = total - term * value / (terms + 1)
    return lower, total


@lru_cache(None)
def rank_power(rank, saving):
    """Enclose rank**(1-saving), with no floating-point evaluation."""
    logarithm = log_integer(rank)
    low = rank * exp_negative(saving * logarithm[1])[0]
    high = rank * exp_negative(saving * logarithm[0])[1]
    return low, high


def mixed_margin(targets, paid, saving):
    lower = upper = Q(0)
    for rank in set(targets) | set(paid):
        coefficient = targets.get(rank, 0) - paid.get(rank, 0)
        bounds = rank_power(rank, saving)
        lower += coefficient * bounds[0 if coefficient >= 0 else 1]
        upper += coefficient * bounds[1 if coefficient >= 0 else 0]
    return lower, upper


def decimal_integer(value, digits):
    sign = "-" if value < 0 else ""
    value = abs(value)
    whole, fractional = divmod(value, 10**digits)
    return f"{sign}{whole}.{fractional:0{digits}d}"


def outward(bounds, digits=40):
    scale = 10**digits
    lower, upper = (value * scale for value in bounds)
    low_integer = lower.numerator // lower.denominator
    high_integer = -((-upper.numerator) // upper.denominator)
    return [decimal_integer(low_integer, digits), decimal_integer(high_integer, digits)]


def choose_rank(saving, uniform_saving, gamma, m):
    gap = saving - uniform_saving
    require(gap > 0, "Uniform saving must be strictly below the tested mixed saving")
    b = m.bit_length()  # m < 2**b, including powers of two.
    for j in range(1, 129):
        threshold = (b * saving + gamma * j) / gap
        h = max(b, 2**(j - 1), threshold.numerator // threshold.denominator + 1)
        if h < 2**j:
            return h, j, b
    raise AssertionError("No sufficient compressed rank in the search range")


def case(name, targets, paid, saving, uniform_saving, theta, gamma,
         log_m_upper, previous_h=None):
    m, kmin, rmax = max(targets), min(targets), max(paid)
    t = 1 - saving
    require(0 < uniform_saving < saving < 1, "Strict saving interval")
    require(1 <= rmax < kmin <= m, "Strict native rank separation")
    require(0 < theta < 1 and gamma > 0, "Logarithmic potential parameters")
    require(rmax**theta.denominator < kmin**theta.numerator,
            "Every exit obeys e < n**theta")
    require(m >= 16 and theta > Q(1, 2), "theta*log(n)>1 throughout induction")
    require(log_integer(2)[0] > Q(1, 2) and log_integer(2)[1] < 1,
            "Elementary bounds on log(2)")
    require(log_integer(m)[1] < log_m_upper, "Certified rational upper bound on log(m)")
    eta_lower = t * (1 - saving * log_m_upper)
    require(0 < eta_lower < 1, "Positive complement slack")
    require(theta**gamma.numerator < eta_lower**gamma.denominator,
            "theta**gamma < eta_lower <= t*m**(t-1)")
    margin = mixed_margin(targets, paid, saving)
    require(margin[0] > 0, "Strict mixed superpotential from the authenticated tariff")
    h, j, b = choose_rank(saving, uniform_saving, gamma, m)
    gap = saving - uniform_saving
    final_gap = gap * h - b * saving - gamma * j
    require(h < 2**j and m < 2**b and final_gap > 0,
            "m**saving * log(2**h)**gamma < (2**h)**gap")
    require((h - 1) * gap <= b * saving + gamma * j,
            "One smaller H fails this stated sufficient inequality")
    bad_margin = mixed_margin(targets, paid, Q("0.004"))
    require(bad_margin[1] < 0, "The authenticated tariff rejects saving 0.004")
    output = {
        "name": name,
        "targets": {str(k): v for k, v in sorted(targets.items())},
        "paid": {str(k): v for k, v in sorted(paid.items())},
        "m": m, "k_min": kmin, "r_max": rmax,
        "tested_mixed_saving": str(saving),
        "uniform_saving": str(uniform_saving),
        "t": str(t), "theta_upper": str(theta), "gamma": str(gamma),
        "log_m_upper": str(log_m_upper), "eta_lower": str(eta_lower),
        "strict_mixed_margin": outward(margin),
        "source_exit_potential": "sum_e x_e*e^t <= sum_s w_s*s^t",
        "global_leaf_bound": "L(n) <= m^(1-t)*n^t*max(1,log(n))^gamma",
        "N": {"encoding": "2^H", "H": h},
        "H_binary_upper_exponent": j,
        "m_binary_upper_exponent": b,
        "uniform_saving_gap": str(gap),
        "strict_final_power_gap": str(final_gap),
        "strict_uniform_moment": "P_N/B_N < N^(1-uniform_saving)",
        "negative_controls": {
            "zero_gamma_fails_complement_contraction": Q(1) >= eta_lower,
            "one_smaller_H_fails_stated_final_inequality": True,
            "saving_0.004_rejected_by_actual_tariff": True,
        },
        "materialized_native_word": False,
    }
    if previous_h is not None:
        require(h < previous_h, "Strictly smaller explicit ambient rank")
        output["previous_N"] = {"encoding": "2^H", "H": previous_h}
        output["previous_H_divided_by_new_H"] = str(Q(previous_h, h))
    return output


def build(source_root):
    for relative, expected in PINS.items():
        path = source_root / relative
        require(path.is_file(), f"Missing pinned input {path}; use --source-root for PR #4359")
        require(sha256(path.read_bytes()).hexdigest() == expected, f"Changed pinned input: {relative}")
    complex_source = read_json(source_root / "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz")["cover"]
    bit_source = next(row for row in read_json(
        source_root / "research/kappa-rebuild/bit/MIXED-PRODUCTIVE-BIT.json")["candidates"]
        if row["pairs"] == 3 and row["keep_idle_mask"] == 43)
    old_cases = read_json(source_root / "research/kappa-rebuild/controller/EXPLICIT-TEMPLATE-BOUNDS.json")["cases"]
    previous = {row["family"]: row["N"]["H1"] for row in old_cases}
    ctargets = {int(k): int(v) for k, v in complex_source["targets"].items()}
    cpaid = {int(k): int(v) for k, v in complex_source["paid"].items()}
    btargets = {int(k): int(v) for k, v in bit_source["targets"].items()}
    bpaid = {int(k): int(v) for k, v in bit_source["paid"].items()}
    cases = [
        case("complex_incumbent_saving", ctargets, cpaid,
             Q("0.002305"), Q("0.002304"), Q(9, 10), Q(1, 9), Q(81, 20), previous["complex"]),
        case("bit_incumbent_saving", btargets, bpaid,
             Q("0.002769"), Q("0.00276"), Q(15, 16), Q(7, 32), Q(4), previous["BIT"]),
        case("complex_improved_outer_saving", ctargets, cpaid,
             Q("0.00230509"), Q("0.002305088"), Q(9, 10), Q(1, 9), Q(81, 20)),
    ]
    return {
        "schema": "logarithmic-finite-template-certificate/1",
        "status": "PASS_RATIONAL_LOG_POTENTIAL_AND_EXPLICIT_TEMPLATE_RANKS",
        "source_pr": "https://github.com/CrocSwap/integer-mult-bounds/pull/4359",
        "source_commit": SOURCE_COMMIT,
        "source_sha256": PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "arithmetic": "Exact integer/Fraction arithmetic; atanh log enclosure and alternating exp enclosure",
        "cases": cases,
        "scope": [
            "Conditional on the pinned finite compiler and complete native arbitrary-input contracts.",
            "The new proof bounds paid rank-one leaves, including all complements and exits.",
            "Every scalar, routing, owned-storage and precision constant must be computed from the selected finite word.",
            "No winning instruction list, GL cover, B_N, P_N or U_N is materialized.",
            "An integer-multiplication kappa requires the separate outer-transfer argument and its inherited hypotheses.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path, help="Write the deterministic certificate to this path")
    action.add_argument("--check", action="store_true", help="Compare against the committed certificate (default)")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE / "CERTIFICATE.json").read_text() == text, "Committed certificate differs from exact replay")
    print(json.dumps({"status": result["status"], "cases": [
        {key: row[key] for key in ("name", "uniform_saving", "N", "strict_final_power_gap")}
        for row in result["cases"]
    ]}, sort_keys=True))


if __name__ == "__main__":
    main()
