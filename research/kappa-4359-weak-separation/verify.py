#!/usr/bin/env python3
"""Exact weighted-tail certificate for the weakly separated mixed compiler.

The native width-five deletion and equal-rank scheduling interface are
separate authenticated dependencies. This checker independently recounts
the deletion, proves the required moment inequalities by exact rational
enclosures, and checks the sufficient template rank in PROOF.md.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = HERE.parents[1]
SOURCE_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
MATH_PATH = HERE.parent / "kappa-4359-log-potential/verify.py"
MATH_HASH = "ad92ee3790c441f7e3065e70527ada8a038f21ca70005832c67476d7f146e2ad"
SOURCE_PINS = {
    "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz":
        "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f",
    "research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md":
        "4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8",
    "research/kappa-rebuild/transfer-audit/finite_dag_audit.py":
        "f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e",
}
COMPANION_PINS = {
    "kappa-4359-native-five/CERTIFICATE.json":
        "9a4036e30d38be476cd529b4aebba40270f719744c13a86efd9306892d903ed8",
    "kappa-4359-weak-compiler/CERTIFICATE.json":
        "2bd9043b77e5219e92d101c3c5f469bf302618ac932484f169f1ad3614ac1187",
}
TARGETS = {5: 102, 6: 90, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
PAID = {1: 17521, 2: 5065, 3: 1738, 4: 714, 5: 254}
TESTED_SAVING = Q("0.00231166")
UNIFORM_SAVING = Q("0.002311658")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def arithmetic():
    require(sha256(MATH_PATH.read_bytes()).hexdigest() == MATH_HASH,
            "Authenticated exact rational arithmetic implementation")
    spec = importlib.util.spec_from_file_location("logarithmic_template_arithmetic", MATH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def literal_profile(source_root):
    source = read_json(source_root / "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz")["cover"]
    owners = {}
    for row in source["fresh_outputs"]:
        if row["native_width"] == 5:
            require(row["target_rank"] == 6, "The removed completion adds exactly one axis")
            require(row["owner"] not in owners, "Each changed target has a distinct physical owner")
            owners[row["owner"]] = row["stage"]
    require(len(owners) == 102, "All 102 native width-five fresh outputs")
    removed = sorted((row for row in source["paid_residuals"]
                      if row["kind"] == "fresh_topup" and row["owner"] in owners),
                     key=lambda row: row["owner"])
    require(len(removed) == 102, "Exactly one deleted paid call for each changed output")
    require(Counter(row["owner"] for row in removed) == Counter({owner: 1 for owner in owners}),
            "No duplicate deletion or unpaired target change")
    require(all(row["rank"] == 1 and row["after_stage"] == owners[row["owner"]]
                for row in removed), "Every deletion is the correct chronological rank-one completion")
    targets = Counter({int(k): int(v) for k, v in source["targets"].items()})
    paid = Counter({int(k): int(v) for k, v in source["paid"].items()})
    targets[5] += len(owners)
    targets[6] -= len(owners)
    paid[1] -= len(removed)
    require(dict(targets) == TARGETS and dict(paid) == PAID, "Literal derivative matches the tested tariff")
    require(sum(k*v for k, v in targets.items()) - sum(k*v for k, v in paid.items()) == 224,
            "Rank-unit surplus retained after complete accounting")
    return sorted(owners), removed


def positive_moment(arithmetic_module, paid, saving, extra_power=0):
    lower = upper = Q(0)
    for rank, count in paid.items():
        lo, hi = arithmetic_module.rank_power(rank, saving)
        weight = count * rank**extra_power
        lower += weight * lo
        upper += weight * hi
    return lower, upper


def build(source_root):
    for relative, expected in SOURCE_PINS.items():
        path = source_root / relative
        require(path.is_file(), f"Missing pinned PR #4359 input: {path}")
        require(sha256(path.read_bytes()).hexdigest() == expected, f"Changed pinned source: {relative}")
    require(len(COMPANION_PINS) == 2, "Both native and compiler companion receipts must be pinned")
    companions = {}
    for relative, expected in COMPANION_PINS.items():
        path = HERE.parent / relative
        require(sha256(path.read_bytes()).hexdigest() == expected,
                f"Changed companion receipt: {relative}")
        companions[relative] = read_json(path)
    native = companions["kappa-4359-native-five/CERTIFICATE.json"]
    compiler = companions["kappa-4359-weak-compiler/CERTIFICATE.json"]
    require(native["schema"] == "native-width-five-topup-deletion/1"
            and native["status"] == "PASS_LITERAL_NATIVE_DELETION_AND_EXACT_IMPROVED_MIXED_ROOT",
            "Pinned complete native deletion certificate")
    require(compiler["schema"] == "weak-separation-finite-compiler-interface/1"
            and compiler["status"] == "PASS_EQUALITY_RULE_AND_MULTIGENERATION_OWNED_DAG",
            "Pinned explicit weak-rank compiler interface")
    require(native["source_commit"] == compiler["source_commit"] == SOURCE_COMMIT,
            "One common immutable predecessor")
    owners, removed = literal_profile(source_root)
    native_targets = {int(k): int(v) for k, v in native["new_profile"]["targets"].items()}
    native_paid = {int(k): int(v) for k, v in native["new_profile"]["paid"].items()}
    require(native_targets == TARGETS and native_paid == PAID,
            "Moment and native endpoint certificates use exactly the same tariff")
    require(native["removed_topups"] == removed, "Every literal deleted call is bound to the native witness")
    require(all(compiler["controls"].values()), "Compiler controls reject inadmissible rank/owner cases")
    require(compiler["controls"]["minimum_one_nonterminating_lattice_rejected"],
            "The relaxed compiler still rejects a rank-one target lattice")
    E = arithmetic()
    C, Cu = TESTED_SAVING, UNIFORM_SAVING
    t = 1 - C
    m, q, rmax = max(TARGETS), min(TARGETS), max(PAID)
    require(0 < Cu < C < 1 and 2 <= q < m and rmax <= q,
            "Weak separation with a nontrivial target lattice and decreasing ambient ranks")
    mixed = E.mixed_margin(TARGETS, PAID, C)
    require(mixed[0] > 0, "Strict native mixed superpotential")
    p_t = positive_moment(E, PAID, C)
    p_next = positive_moment(E, PAID, C, extra_power=1)
    require(p_next[1] < 2 * p_t[0], "P_(t+1)/P_t < 2 with directed rational enclosures")
    require(2**2 < q, "Paid moment growth is less than sqrt(q)")
    theta, gamma = Q(3, 4), Q(1, 20)
    require(m**3 > 16**4, "Weighted high-exit fraction 2*m^(-3/4) < 1/8")
    require(theta * E.log_integer(m)[0] > 1,
            "Rank-one exits satisfy the logarithmic low-exit bound")
    v_upper, tail_upper = Q(505, 512), Q(1, 8)
    require(theta < v_upper**20, "theta**gamma < 505/512")
    exit_coefficient = v_upper + (1 - v_upper) * tail_upper
    require(exit_coefficient == Q(4047, 4096), "Full low/high convex-combination charge")
    ell = Q(81, 20)
    require(E.log_integer(m)[1] < ell, "Rational upper bound on log(m)")
    eta_lower = t * (1 - C * ell)
    require(eta_lower > exit_coefficient, "Complement slack strictly dominates all exits")
    h, j, b = E.choose_rank(C, Cu, gamma, m)
    final_gap = h * (C - Cu) - b * C - gamma * j
    require(h == 756934981 and j == 30 and b == 6 and final_gap == Q(1, 500000000),
            "Specified successful finite uniform rank")
    require(h >= b and h < 2**j and m < 2**b,
            "Final logarithmic and ambient-rank bounds")
    require((h - 1) * (C - Cu) <= b * C + gamma * j,
            "One less H fails the stated strict sufficient inequality")
    old_targets = dict(TARGETS)
    old_targets[6] += old_targets.pop(5)
    old_paid = dict(PAID)
    old_paid[1] += 102
    old_margin = E.mixed_margin(old_targets, old_paid, C)
    require(old_margin[1] < 0, "The unchanged native tariff does not support the new tested saving")
    require(rmax == q, "The example genuinely requires weak separation")
    return {
        "schema": "weighted-tail-weak-separation-template/1",
        "status": "PASS_NATIVE_WEAK_SEPARATION_TAIL_AND_EXPLICIT_TEMPLATE",
        "source_commit": SOURCE_COMMIT,
        "source_sha256": SOURCE_PINS,
        "companion_sha256": COMPANION_PINS,
        "arithmetic_generator_sha256": MATH_HASH,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "new_profile": {"targets": TARGETS, "paid": PAID},
        "changed_fresh_owner_count": len(owners),
        "tested_mixed_saving": str(C), "uniform_saving": str(Cu),
        "strict_mixed_margin": E.outward(mixed),
        "old_tariff_margin_at_new_saving": E.outward(old_margin),
        "t": str(t), "q": q, "m": m, "r_max": rmax,
        "theta": str(theta), "gamma": str(gamma),
        "exact_exit_moment": "E_a=P_a^(G+1), G=floor(log_q(n/m))",
        "paid_moment_ratio": E.outward((p_next[0]/p_t[1], p_next[1]/p_t[0])),
        "paid_moment_ratio_strict_upper": "2",
        "high_exit_potential_bound": "high_exit_t/source_t <= 2*m^(-1/2)*n^(-1/4) <= 2*m^(-3/4) < 1/8",
        "low_exit_log_factor_upper": str(v_upper),
        "high_exit_fraction_upper": str(tail_upper),
        "complete_exit_coefficient_upper": str(exit_coefficient),
        "eta_lower": str(eta_lower),
        "complement_strict_gap": str(eta_lower - exit_coefficient),
        "global_leaf_bound": "L(n) <= m^(1-t)*n^t*max(1,log(n))^(1/20)",
        "N": {"encoding": "2^H", "H": h},
        "H_binary_upper_exponent": j, "m_binary_upper_exponent": b,
        "strict_final_power_gap": str(final_gap),
        "strict_uniform_moment": "P_N/B_N < N^(1-uniform_saving)",
        "negative_controls": {
            "old_strict_separation_fails_for_actual_new_tariff": rmax >= q,
            "old_tariff_cannot_claim_new_mixed_saving": True,
            "one_smaller_H_fails_stated_final_bound": True,
            "entire_exit_potential_cannot_be_treated_as_low": Q(1) > eta_lower,
        },
        "scope": [
            "The weak-separation construction requires 2<=k_min<m and r_max<=k_min.",
            "The complete native derivative and changed compiler guard are separately authenticated.",
            "The source/exit recurrence charges every complement and every paid call on owned storage.",
            "No near-threshold native word, B_N, P_N, U_N or full precision constant is materialized.",
            "Every finite-template constant must be replaced using this selected word.",
            "A complete integer-multiplication bound requires the separate outer transfer and inherited hypotheses.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE / "CERTIFICATE.json").read_text() == text,
                "Committed weak-separation certificate differs from exact replay")
    print(json.dumps({key: result[key] for key in (
        "status", "tested_mixed_saving", "uniform_saving", "N",
        "strict_mixed_margin", "complement_strict_gap", "strict_final_power_gap")}, sort_keys=True))


if __name__ == "__main__":
    main()
