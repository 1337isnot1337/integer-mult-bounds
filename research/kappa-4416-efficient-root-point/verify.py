#!/usr/bin/env python3
"""Exact finite p7 template at the already admitted conditional kappa .002686489.

All source files are authenticated before imports. Two directed moment
engines, the exact logarithmic template and all 54+3 outer guards are
recomputed. The proof and inherited conditional scope are in PROOF.md.
Apache-2.0.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE_PACKAGE = "research/pr4359-p7-padding"
SOURCE_COMMIT = "e9058860b5c850760fdf970e796a96aefcdb1d98"
PINS = {
    "kappa-4416-log-template/verify.py":
        "8c4b9ece37d2a12dd26a3c182709888251cad81d977637614ec6b6fcb1fa7713",
    "kappa-4416-log-template/PROOF.md":
        "bd96275f80fb5d94d5add5a60645f42466c217fa29bd5c60883fcc980e42bd7e",
    "kappa-4416-log-template/CERTIFICATE.json":
        "7162d01fab3c87b16998fecdd879a590e01f1d0b31a76f9af23b1ee86f64112b",
    "kappa-4416-padding-endpoint/verify.py":
        "2cfd49cba8b5fd467d185593e7d714d07635e660ff7b9e4a5500099ecdf7ecc9",
    "kappa-4416-padding-endpoint/PROOF.md":
        "e366fa51daedacbd104949c77d7d7233556fef543428e1ce9d7ad09403fb07eb",
    "kappa-4416-padding-endpoint/CERTIFICATE.json":
        "80dc286ed59618f88b6773a347bfdcdd7ee10e18da06f17372914b83587e4db6",
    "kappa-4416-root-family/verify.py":
        "5f5e00fce1d3940189f957a2bde03bd9cd07daaefbd1e86958e0c461e415fa0c",
    "kappa-4416-root-family/PROOF.md":
        "3600e8445612f732ffe0bbd4cb4c0f5b32761109da6f85c70067a3f66be6991a",
    "kappa-4416-root-family/CERTIFICATE.json":
        "af8dfb46adcdbf1acee2580b3a539204df9f4c5d2ea48b875d693f37eb8cffe4",
}
C = Q("0.00268648904")
KAPPA = Q("0.002686489")
UNIFORM = Q(470135581, 175000000000)
V = 9750
ALPHA_GAP = Q(3, 2*10**11)
TAIL_BOUND = Q(4991, 5000)
THETA = Q(61, 75)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "Python source loader")
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def build(source_root):
    for relative, expected in PINS.items():
        require(sha256((HERE.parent/relative).read_bytes()).hexdigest() == expected,
                "Changed frozen dependency: "+relative)
    padding = module("efficient_point_padding", HERE.parent/"kappa-4416-padding-endpoint/verify.py")
    previous = padding.build(source_root)
    require(previous == json.loads((HERE.parent/"kappa-4416-padding-endpoint/CERTIFICATE.json").read_text()),
            "Complete authenticated native, logarithmic, padding and outer source replay")
    require(previous["status"] == "PASS_COMPLETE_P7_PADDING_AND_HIGHER_CONDITIONAL_KAPPA",
            "Expected complete source-chain status")
    targets = {int(k): v for k, v in previous["targets"].items()}
    paid = {int(k): v for k, v in previous["paid"].items()}
    require(targets == {5:420, 6:270, 7:840, 8:1395, 9:3195, 25:448, 41:448, 57:448, 121:224}
            and paid == {1:37305, 2:10695, 3:3360, 4:1530, 5:300, 8:1464, 16:448, 32:448, 48:448},
            "Exactly the unchanged full raw p7 invoice")
    B, T1, P1 = sum(targets.values()), sum(r*n for r, n in targets.items()), sum(r*n for r, n in paid.items())
    require((B, T1, P1, sum(paid.values())) == (7688, 131723, 131115, 55998)
            and B*17 < P1 < T1 and 10 < 17 < 121,
            "Full productive ownership, paid counts and charged completion comparison")
    pkg = source_root/SOURCE_PACKAGE
    E = module("efficient_point_source_intervals", pkg/"source/research/kappa-rebuild/architecture/mixed_target_probe.py")
    I = module("efficient_point_independent_intervals", pkg/"dependencies/compiler-refill/template_bound.py")
    L = module("efficient_point_source_ledger", pkg/"dependencies/compiler-refill/endpoint.py")
    logs = module("efficient_point_logarithmic_template", HERE.parent/"kappa-4416-log-template/verify.py")
    engines = {}
    for name, engine in (("source", E), ("independent", I)):
        if name == "source":
            tlo, thi = engine.moment(targets, C)
            plo, phi = engine.moment(paid, C)
        else:
            tlo, thi = engine.moment_margin(targets, {}, C)
            plo, phi = engine.moment_margin(paid, {}, C)
        llo, lhi = engine.log_interval(10)
        clo, chi = engine.exp_interval(C*llo)[0], engine.exp_interval(C*lhi)[1]
        alpha = plo/thi, phi/tlo
        tail = P1/(chi*thi), P1/(clo*tlo)
        completion = B*17/(chi*thi), B*17/(clo*tlo)
        require(0 < alpha[1] < 1-ALPHA_GAP < 1,
                name+": complete raw moment supports the finite alpha envelope")
        require(completion[1] < tail[1] < TAIL_BOUND < 1,
                name+": both complete paid tails satisfy the same exact bound")
        engines[name] = {
            "target_moment": E.show((tlo, thi)), "paid_moment": E.show((plo, phi)),
            "target_minus_paid": E.show((tlo-phi, thi-plo)),
            "alpha": E.show(alpha), "original_paid_tail": E.show(tail),
            "completion_paid_tail": E.show(completion),
        }
    require(V == 25*390 and 2*4991**390 < 5000**390, "Exact finite rational decay blocks")
    bound = 1/(1+V*ALPHA_GAP)+Q(4, 2**25)
    require(bound == Q(6710887200000117, 6710887381467136) < 1,
            "Complete tensor, splitting and completion moment is strictly positive")
    require(1-bound == Q(181467019, 6710887381467136), "Exact charged mixed-moment gap")
    previous_block = 1/(1+(V-390)*ALPHA_GAP)+Q(4, 2**24)
    require(previous_block >= 1, "One fewer decay block fails this sufficient envelope")
    require(UNIFORM == KAPPA+6*(C-KAPPA)/7, "Exact seven-gap uniform saving")
    template = logs.derive_template(121, 17, 10, V, C, UNIFORM, THETA)
    gamma, b, h, j = (template[key] for key in ("gamma", "binary_ambient_bound", "H", "J"))
    require((gamma, b, h, j) == (608, 67459, 5670914876226139, 53),
            "Exact actual-eta logarithmic template values")
    require(template["final_strict_power_gap"] == Q(1, 175000000000),
            "Exact strict final power gap")
    require(template["potential_log_gap_interval"][0] > Q("0.00134580448"),
            "Reported actual logarithmic contraction margin")
    log_theta, log_m, log_t = logs.log_interval(1/THETA), logs.log_interval(Q(121)), logs.log_interval(1-C)
    prior_gamma_upper = (gamma-1)*log_theta[1]-(C*V*log_m[0]-log_t[1])
    require(prior_gamma_upper < 0, "One lower gamma fails the actual potential comparison")
    require((h-1)*(C-UNIFORM) <= b*C+gamma*j,
            "One lower H fails the same strict sufficient inequality")
    require(logs.rank_candidate(C, UNIFORM, b, gamma, j-1) >= 2**(j-1),
            "The preceding logarithmic bin is insufficient")
    outer = padding.outer_point(C, KAPPA, L)
    require(outer["ledger"]["parameters"]["complex_uniform_saving"] == template["uniform_saving"],
            "The complete outer consumer is funded by this exact uniform template")
    # This frozen receipt is used only for a historical rank comparison.
    family = json.loads((HERE.parent/"kappa-4416-root-family/CERTIFICATE.json").read_text())
    old = family["explicit_constructive_member"]
    old_h = old["template"]["N"]["H"]
    require(Q(old["requested_kappa"]) == KAPPA and old_h == 47400257013113900919251
            and old_h > 8350000*h and old["tensor_power"] == 34359739029,
            "Same final kappa and a logarithmic-rank reduction greater than 8.35 million")
    return encode({
        "schema": "efficient-finite-p7-strict-root-point/1",
        "status": "PASS_COMPLETE_CONDITIONAL_KAPPA_002686489_WITH_SMALLER_FINITE_TEMPLATE",
        "source_commit": SOURCE_COMMIT, "dependency_sha256": PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"PROOF.md").read_bytes()).hexdigest(),
        "source_result_sha256": previous["source_result_sha256"],
        "source_replay_status": previous["status"],
        "tested_saving": C, "kappa": KAPPA, "uniform_saving": UNIFORM,
        "targets": targets, "paid": paid, "tensor_power": V,
        "target_floor_base": 17, "paid_cutoff_base": 10,
        "alpha_gap": ALPHA_GAP, "paid_tail_upper": TAIL_BOUND,
        "moment_engines": engines, "normalized_paid_moment_upper": bound,
        "strict_complete_moment_gap": 1-bound,
        "rank_one_surplus": {"positive_base": T1, "negative_base": P1, "power": V},
        "template": template, "outer": outer,
        "historical_generic_comparison": {
            "receipt_sha256": PINS["kappa-4416-root-family/CERTIFICATE.json"],
            "same_kappa": KAPPA, "old_H": old_h, "new_H": h,
            "log2_rank_reduction_factor": Q(old_h, h),
            "historical_receipt_used_as_mathematical_premise": False,
        },
        "negative_controls": {
            "one_fewer_decay_block_upper": previous_block,
            "one_lower_gamma_log_gap_upper": logs.outward((prior_gamma_upper, prior_gamma_upper))[1],
            "one_lower_H_rejected": True, "preceding_logarithmic_bin_rejected": True,
            "full_outer_mutations": outer["controls"],
        },
        "scope": [
            "The unchanged source native chronology and complete invoice are authenticated and replayed.",
            "All paid target completions, paid splits, whole-job adapters, owned-bank calls and source complements remain charged.",
            "The full seven-gap outer point uses the exact uniform saving certified by this new finite word.",
            "All new finite-word scalar, movement, storage, precision and reserve constants must use the new actual word counts.",
            "The all-column, physical, precision, analytic, fixed-tape and exact-recovery premises remain conditional.",
            "No globally optimal kappa, minimal word, practical runtime or unconditional multiplication theorem is claimed.",
        ],
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--out", type=Path)
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE/"CERTIFICATE.json").read_text() == text, "Exact deterministic efficient-point receipt")
    print(json.dumps({"status": result["status"], "kappa": result["kappa"],
                      "N": result["template"]["N_encoding"],
                      "strict_complete_moment_gap": result["strict_complete_moment_gap"],
                      "minimum_outer_slack": result["outer"]["minimum_saving_minus_kappa"]}, sort_keys=True))


if __name__ == "__main__":
    main()
