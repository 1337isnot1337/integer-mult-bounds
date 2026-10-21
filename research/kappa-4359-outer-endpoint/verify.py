#!/usr/bin/env python3
"""Exact strict outer points below the unchanged PR4359 complex mixed root.

The algebraic parameter family is a consequence of the supplier and outer
interfaces in PR4359. This file checks those implications arithmetically;
it does not prove the native-program or analytic premises.

The outer cost formulas are inherited from CrocSwap/integer-mult-bounds,
especially PR1673, PR1758, PR1786, and the retained check_ledger.py.
New parameter family and independent rational checks: Apache-2.0.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial
from pathlib import Path
import argparse
import ast
import gzip
import json
import subprocess
import sys
import tempfile

PINNED_COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
GRID = 1 << 320
COMPLEX_TARGETS = {6: 192, 7: 56, 8: 93, 9: 1229, 25: 448, 57: 224}
COMPLEX_PAID = {1: 17623, 2: 5065, 3: 1738, 4: 714, 5: 254}
BIT_SAVING = Q("0.0027")
TESTED_SAVING = Q("0.00230509")
TARGET = Q("0.00230508")
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
EXPECTED_SOURCE_SHA256 = {
    "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz": "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f",
    "research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md": "4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8",
    "research/kappa-rebuild/bit/DELAYED-COVER-BRIDGE.md": "9731b93026717f5fa15851e3633cbb4bdc76eba2bffb9d6b4a3b69f7dd502443",
    "research/kappa-rebuild/transfer-audit/FINITE-TEMPLATE-CLOSURE.md": "3f8508c63862dd83968bd30df91b08ba5afcee1e10db15ca546cdff0caef95d9",
    "research/kappa-rebuild/transfer-audit/OUTER-TRANSFER-AUDIT.md": "67569961d068633c6ff3ac9dfde47a0c17f0da6d20432799dcc920cff92b5779",
    "research/kappa-rebuild/controller/OUTER-PARAMETERS.json": "15818c10c41ac2ea650e503de830795f6c88830a7f9be9553dd938bb1d76717a",
    "research/kappa-observation-integration/release-work/current/package/outer/check_ledger.py": "1dd56009986eb14dd6603c9193c7ad71dd45c7d005bf71c9cd3f916e66f54d98",
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def lower(x):
    return Q((x * GRID).__floor__(), GRID)


def upper(x):
    return Q((x * GRID).__ceil__(), GRID)


def ln_unit(x):
    require(Q(1) <= x <= Q(2), "log argument is in [1,2]")
    v = (x - 1) / (x + 1)
    terms = 110
    partial = 2 * sum((v ** (2*j+1) / (2*j+1) for j in range(terms)), Q(0))
    tail = 2 * v ** (2*terms+1) / ((2*terms+1) * (1-v*v))
    return lower(partial), upper(partial+tail)


def ln_integer(k):
    require(isinstance(k, int) and k >= 1, "positive integer rank")
    j = k.bit_length() - 1
    lo, hi = ln_unit(Q(k, 1 << j))
    l2, h2 = ln_unit(Q(2))
    return lower(lo+j*l2), upper(hi+j*h2)


def exp_small(x):
    require(0 <= x < Q(1, 10), "exponential argument is in [0,1/10)")
    terms = 40
    partial = sum((x**j/factorial(j) for j in range(terms+1)), Q(0))
    first = x**(terms+1)/factorial(terms+1)
    tail = first/(1-x/Q(terms+2))
    return lower(partial), upper(partial+tail)


def rank_power(k, saving):
    lo, hi = ln_integer(k)
    a = exp_small(saving*lo)[0]
    b = exp_small(saving*hi)[1]
    return lower(Q(k)/b), upper(Q(k)/a)


def mixed_margin(targets, paid, saving):
    require(0 < saving < Q(1, 32), "saving lies in the verified interval range")
    counts = Counter(targets)
    counts.subtract(paid)
    lo = hi = Q(0)
    for rank, count in sorted(counts.items()):
        a, b = rank_power(rank, saving)
        lo += count*(a if count >= 0 else b)
        hi += count*(b if count >= 0 else a)
    return lower(lo), upper(hi)


def parameter_point(kappa=TARGET, tested=TESTED_SAVING, bit=BIT_SAVING):
    """All parameters are rational. Every displayed outer inequality is strict."""
    require(0 < kappa < tested < min(bit, Q(1, 32)), "0 < kappa < c < min(BIT,1/32)")
    d = (tested-kappa)/5
    uniform, b, a, q = tested-d, tested-2*d, tested-3*d, tested-4*d
    eps, beta = 1-d, 1-3*d
    r0 = layout = d/4
    stop = d
    sigma, tau = 1-b, 1-a
    internal = tau + (1-stop)*max(sigma-tau, Q(0))
    leaf = sigma + stop*(1-sigma)
    lam, lam_prime = 1-(q+a)/2, 1-q
    matrix_exponent = Q(45, 16)
    c_matrix = (3-matrix_exponent)/2
    xi = eps*(1+q)-c_matrix+layout
    key = beta+1-eps
    margins = {
        "main_transform": eps*q,
        "global_coordinate_router": a,
        "fused_gaussian": 1-eps+q*beta,
        "group_bit_router": 1-eps+a*beta,
        "group_scans": 1-eps+beta,
        "boundary_algebraic_matrix": c_matrix+xi-eps,
        "sparse_union_movement": xi+Q(1, 2)-eps,
        "polynomial_products": eps,
        "microbox_face_corrections": 1-(eps+beta+48-128+2),
    }
    checks = {
        "tested_mixed_above_uniform": tested-uniform,
        "uniform_above_selected_complex": uniform-b,
        "actual_BIT_above_effective": bit-a,
        "complex_above_effective": b-a,
        "q_positive": q,
        "complex_endpoint": b-q,
        "q_below_effective": a-q,
        "stop_positive": stop,
        "stop_below_one": 1-stop,
        "leaf_saving_above_effective": (1-stop)*b-a,
        "q_below_internal": 1-internal-q,
        "q_below_leaf": 1-leaf-q,
        "lambda_above_tau": lam-tau,
        "lambda_above_sigma": lam-sigma,
        "lambda_above_internal": lam-internal,
        "lambda_prime_above_lambda": lam_prime-lam,
        "lambda_prime_above_leaf": lam_prime-leaf,
        "epsilon_positive": eps,
        "epsilon_below_one": 1-eps,
        "cap_above_band": xi-Q(1, 2),
        "cap_below_cell": eps-xi,
        "group_positive": beta,
        "group_below_dimension": eps-beta,
        "support_router_span": 1-beta,
        "group_gauge_power_slack": 1-(2*xi-2)-r0-beta,
        "actual_logarithmic_group_guard": 1-(2*xi-2)-beta,
        "global_gamma_power_slack": 1-eps-r0,
        "actual_logarithmic_gamma_guard": 1-eps,
        "alpha_logarithm_absorption": r0,
        "group_key_fits_record": 1-key,
        "membership_arithmetic_fits_record": 1-beta-2*(1-eps),
        "microbox_halo_volume": 128-48-beta,
        "positive_layout_slack": layout,
        "short_record_fallback": eps-a,
        "complex_below_one_over_32": Q(1, 32)-b,
        "strassen_integer_power_gap": Q(2**45-7**16),
        "theta_positive_polynomial_power": Q(2),
        "cap_below_phase_cell_power": 2-xi,
        "halo_covers_generic_inverse_radius": Q(5),
        "union_tag_work_per_visit_fits_record": 1-beta,
        "union_header_fits_record": 1-beta,
        "source_axis_superpolynomial": 1-eps,
        "gaussian_above_main": margins["fused_gaussian"]-margins["main_transform"],
        "new_semantic_guard_with_C1_one": 1-eps,
        "fine_prime_halo_umbrella": Q(7, 2),
        "new_BIT_row_stock_sublinear_in_active_group": beta*(1-Q(3, 1000)),
        "fixed_halo_explicit_metadata_branch": 128-48-eps-beta-1,
        "new_semantic_group_guard": 1-beta,
    }
    checks.update({name+"_above_kappa": value-kappa for name, value in margins.items()})
    require(all(v > 0 for v in checks.values()), "every supplier, functional, and outer gap is positive")
    require(margins["main_transform"]-kappa == d*(1-q), "exact limiting gap identity")
    require(checks["leaf_saving_above_effective"] == d*(1-b), "exact stopped leaf gap")
    require(checks["gaussian_above_main"] == d*(1-2*q), "main-binding family invariant")
    require(min(margins.values()) == margins["main_transform"], "main transform is the unique limiting row")
    return {
        "parameters": {
            "kappa": kappa, "tested_mixed_saving": tested, "delta": d,
            "complex_uniform_saving": uniform, "b": b, "effective_saving": a,
            "q": q, "epsilon": eps, "group_beta": beta, "stop": stop,
            "r0": r0, "layout_slack": layout, "lambda": lam,
            "lambda_prime": lam_prime, "cap_xi": xi, "BIT_saving": bit,
            "Strassen_exponent": matrix_exponent, "theta_power": Q(2),
            "halo_power": 48, "core_power": 128,
        },
        "nine_outer_savings": margins, "strict_checks": checks,
        "minimum_outer_slack": min(margins.values())-kappa,
    }


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def bind_sources(root):
    actual = {}
    for path, expected in EXPECTED_SOURCE_SHA256.items():
        actual[path] = sha256((root/path).read_bytes()).hexdigest()
        require(actual[path] == expected, "immutable PR4359 source changed: "+path)
    # Authentication precedes parsing the invoice or executing any inherited
    # source function. These are immutable-source hashes, not regeneration hashes.
    profile_path = root/"research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz"
    profile = read_json(profile_path)["cover"]
    targets = {int(k): int(v) for k, v in profile["targets"].items()}
    paid = {int(k): int(v) for k, v in profile["paid"].items()}
    require(targets == COMPLEX_TARGETS and paid == COMPLEX_PAID, "complete unchanged pinned complex invoice")
    return actual


def inherited_crosscheck(root, point):
    """Cross-check against the unchanged, source-pinned inherited ledger function."""
    path = root/"research/kappa-observation-integration/release-work/current/package/outer/check_ledger.py"
    source = ast.parse(path.read_text())
    function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "ledger")
    constants = [n for n in source.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id.startswith("KAPPA_") for t in n.targets)]
    p = point["parameters"]
    saving = point["nine_outer_savings"]["main_transform"]
    # This exact grid makes the retained floor/backoff convention return the
    # prescribed strict target, with a strictly positive backoff.
    grid = saving.denominator * p["kappa"].denominator
    env = {
        "Q": Q, "R0": p["r0"], "ZETA": p["stop"], "SLACK": p["layout_slack"],
        "GAP": p["delta"], "STOP": p["stop"], "FLOOR": grid,
        "BACKOFF": saving-p["kappa"], "EPS": p["epsilon"], "BETA": p["group_beta"],
        "THETA_POWER": Q(2), "HALO_POWER": 48, "CORE_POWER": 128,
        "STRASSEN_TAU": Q(45, 16), "b": p["b"], "a": p["effective_saving"],
        "q": p["q"], "bit": p["BIT_saving"], "online": Q("0.00173098"),
        "old": Q("0.00173098"),
    }
    module = ast.fix_missing_locations(ast.Module(body=constants+[function], type_ignores=[]))
    exec(compile(module, str(path), "exec"), env)
    result = env["ledger"]("unchanged_p3_strict_root_approach")
    require(result["kappa"] == p["kappa"], "inherited target agrees")
    require(result["margins"] == point["nine_outer_savings"], "all inherited outer rows agree")
    require(all(v > 0 for v in result["strict_checks"].values()), "all inherited strict checks pass")
    common = set(result["strict_checks"]) & set(point["strict_checks"])
    require(all(result["strict_checks"][k] == point["strict_checks"][k] for k in common), "all common inherited predicates agree")
    return {"inherited_checks": len(result["strict_checks"]), "matched_checks": len(common),
            "matched_outer_rows": len(result["margins"]), "positive_backoff": saving-p["kappa"]}


def check_rank_certificate(root, point):
    package = HERE.parent/"kappa-4359-log-potential"
    checker = package/"verify.py"
    certificate = package/"CERTIFICATE.json"
    require(checker.is_file() and certificate.is_file(), "sibling logarithmic-potential certificate is required")
    replay = subprocess.run([sys.executable, "-B", str(checker), "--source-root", str(root), "--check"],
                            capture_output=True, text=True)
    require(replay.returncode == 0, "logarithmic-potential replay failed: "+replay.stderr)
    result = read_json(certificate)
    require(result["schema"] == "logarithmic-finite-template-certificate/1", "rank certificate schema")
    require(result["source_commit"] == PINNED_COMMIT, "rank certificate uses the same pending source commit")
    require(result["generator_sha256"] == sha256(checker.read_bytes()).hexdigest(), "rank checker source hash")
    require(result["proof_sha256"] == sha256((package/"PROOF.md").read_bytes()).hexdigest(), "rank proof source hash")
    for path in set(result["source_sha256"]) & set(EXPECTED_SOURCE_SHA256):
        require(result["source_sha256"][path] == EXPECTED_SOURCE_SHA256[path], "shared immutable rank source agrees")
    selected = next(case for case in result["cases"] if case["name"] == "complex_improved_outer_saving")
    p = point["parameters"]
    require(Q(selected["tested_mixed_saving"]) == p["tested_mixed_saving"], "rank test uses selected c")
    require(Q(selected["uniform_saving"]) == p["complex_uniform_saving"], "rank certificate pays selected U")
    require(selected["N"]["encoding"] == "2^H" and selected["N"]["H"] == 1729137493,
            "explicit selected uniform rank")
    require(Q(selected["strict_final_power_gap"]) > 0, "strict finite rank saving")
    return {"certificate_sha256": sha256(certificate.read_bytes()).hexdigest(),
            "generator_sha256": result["generator_sha256"], "proof_sha256": result["proof_sha256"],
            "case": selected["name"], "tested_mixed_saving": Q(selected["tested_mixed_saving"]),
            "uniform_saving": Q(selected["uniform_saving"]), "N": selected["N"],
            "strict_final_power_gap": Q(selected["strict_final_power_gap"]),
            "validation": "Full independent rank-certificate replay and exact c/U/N cross-check"}


def changed_source_control(root):
    """A changed inherited source is rejected before the AST execution gate."""
    relative = "research/kappa-observation-integration/release-work/current/package/outer/check_ledger.py"
    with tempfile.TemporaryDirectory(prefix="outer-endpoint-source-control-") as directory:
        fixture = Path(directory)
        for path in EXPECTED_SOURCE_SHA256:
            target = fixture/path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(root/path)
        changed = fixture/relative
        changed.unlink()
        changed.write_bytes((root/relative).read_bytes()+b"\nraise RuntimeError('untrusted mutation must never execute')\n")
        try:
            bind_sources(fixture)
        except AssertionError as error:
            require(str(error) == "immutable PR4359 source changed: "+relative, "changed source hits authentication gate")
            return True
    raise AssertionError("changed inherited source was accepted")


def encode(value):
    if isinstance(value, Q):
        with localcontext() as context:
            context.prec = 60
            return {"rational": str(value), "decimal": str(Decimal(value.numerator)/Decimal(value.denominator))}
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def build(root):
    sources = bind_sources(root)
    margin = mixed_margin(COMPLEX_TARGETS, COMPLEX_PAID, TESTED_SAVING)
    require(margin[0] > 0, "strict source-bound complex moment at c=.00230509")
    failed = mixed_margin(COMPLEX_TARGETS, COMPLEX_PAID, Q("0.002306"))
    require(failed[1] < 0, "nearby above-root request is rejected")
    point = parameter_point()
    crosscheck = inherited_crosscheck(root, point)
    rank = check_rank_certificate(root, point)
    rejected_equal = False
    try:
        parameter_point(TESTED_SAVING, TESTED_SAVING)
    except AssertionError:
        rejected_equal = True
    require(rejected_equal, "zero gap is rejected")
    return {
        "schema": "strict-mixed-root-outer-approach/1",
        "status": "PASS_EXACT_CONDITIONAL_PARAMETER_IMPLICATION",
        "source_commit": PINNED_COMMIT, "source_sha256": sources,
        "complex_targets": COMPLEX_TARGETS, "complex_paid": COMPLEX_PAID,
        "strict_mixed_margin_at_tested_saving": margin,
        "outer": point, "inherited_crosscheck": crosscheck, "explicit_uniform_template": rank,
        "package_sha256": {"verify.py": sha256(Path(__file__).read_bytes()).hexdigest(),
                           "README.md": sha256((HERE/"README.md").read_bytes()).hexdigest()},
        "controls": {"above_root_002306_margin": failed, "zero_gap_rejected": rejected_equal,
                     "changed_inherited_source_rejected_before_execution": changed_source_control(root)},
        "theorem_scope": "For every rational 0<kappa<c<min(C_complex_root,BIT_saving,1/32), the parameter family passes the stated strict outer interface, conditional on the unchanged native compiler, delayed cover, semantic/stock closure, and inherited analytic/tape hypotheses.",
        "template_closure": "Use the finite compiler at the authenticated new rank N, with the generic replacement scalar, semantic, stock and routing constants of the pinned FINITE-TEMPLATE-CLOSURE.md. The old .002304 template is not reused.",
        "not_claimed": ["A changed local productive tariff.", "Attainment of the mixed root itself.", "A formally verified compiler or an unconditional integer multiplication theorem."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=PROJECT_ROOT,
                        help="Checkout of pinned PR4359 sources; defaults to this project root")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path, help="Write a deterministic certificate to this path")
    action.add_argument("--check-only", "--check", action="store_true", help="Compare with committed certificate (default)")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    serialized = json.dumps(encode(result), indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(serialized)
    else:
        require((HERE/"CERTIFICATE.json").read_text() == serialized, "committed outer certificate differs from exact replay")
    point = result["outer"]
    print(json.dumps(encode({"status": result["status"], "kappa": TARGET,
                            "uniform_saving": point["parameters"]["complex_uniform_saving"],
                            "N": result["explicit_uniform_template"]["N"],
                            "minimum_outer_slack": point["minimum_outer_slack"],
                            "strict_checks": len(point["strict_checks"]),
                            "inherited_crosscheck": result["inherited_crosscheck"]}), sort_keys=True))


if __name__ == "__main__":
    main()
