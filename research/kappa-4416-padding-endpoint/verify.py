#!/usr/bin/env python3
"""Source-bound larger target padding and a higher conditional p7 endpoint.

All acceptance arithmetic is rational or integer. The native source and
the companion logarithmic theorem are authenticated before use. The
complete conditional argument and replacement word constants are in
PROOF.md. Apache-2.0.
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
SOURCE_REL = Path("research/pr4359-p7-padding")
SOURCE_COMMIT = "e9058860b5c850760fdf970e796a96aefcdb1d98"
COMPANION = HERE.parent / "kappa-4416-log-template"
COMPANION_PINS = {
    "verify.py": "8c4b9ece37d2a12dd26a3c182709888251cad81d977637614ec6b6fcb1fa7713",
    "PROOF.md": "bd96275f80fb5d94d5add5a60645f42466c217fa29bd5c60883fcc980e42bd7e",
    "CERTIFICATE.json": "7162d01fab3c87b16998fecdd879a590e01f1d0b31a76f9af23b1ee86f64112b",
}
THETA = Q(61, 75)
TAIL_BOUND = Q(4991, 5000)
BLOCK = 390
CASES = [
    {
        "name": "larger_floor_same_endpoint",
        "C": Q("0.00268648"), "kappa": Q("0.00268647"),
        "v": 6240, "alpha_gap": Q(1, 10**8),
        "expected_bits": 43174, "expected_K": 117, "expected_gamma": 393,
        "expected_H": 12185590261265, "expected_J": 44,
    },
    {
        "name": "higher_conditional_endpoint",
        "C": Q("0.002686489"), "kappa": Q("0.002686488"),
        "v": 8970, "alpha_gap": Q(8, 10**11),
        "expected_bits": 62063, "expected_K": 168, "expected_gamma": 564,
        "expected_H": 190671120967650, "expected_J": 48,
    },
]


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
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def baseline(source_root):
    for relative, expected in COMPANION_PINS.items():
        require(sha256((COMPANION / relative).read_bytes()).hexdigest() == expected,
                "Changed frozen logarithmic companion: " + relative)
    B = module("padding_endpoint_log_companion", COMPANION / "verify.py")
    result = B.build(source_root)
    require(encode(result) == json.loads((COMPANION / "CERTIFICATE.json").read_text()),
            "Complete source-authenticated companion receipt replay")
    return result


def choose_rank(bits, saving, uniform, gamma):
    require(0 < uniform < saving < Q(1, 2), "Strict finite uniform saving gap")
    for j in itertools.count(1):
        h = max(bits, 2, 2**(j - 1),
                (bits*saving + gamma*j) // (saving-uniform) + 1)
        if h < 2**j:
            return h, j


def logarithmic_template(case):
    v, c, kappa = case["v"], case["C"], case["kappa"]
    uniform = kappa + 6*(c-kappa)/7
    bits = (121**v).bit_length()
    eta_debt = 1 + bits*c
    K = -((-eta_debt.numerator)//eta_debt.denominator)
    eta_lower = Q(1, 2**K)
    require(10**THETA.denominator < 17**THETA.numerator,
            "The actual paid/target bases satisfy strict exit contraction")
    require(Q(1, 2) < THETA < 1 and 121 > 16,
            "theta*log(m)>1, including the rank-one exit guard")
    require(Q(1, 2) < 1-c and eta_debt <= K,
            "eta=(1-C)*m^-C is strictly above the dyadic lower bound")
    gamma = 1
    while THETA**gamma >= eta_lower:
        gamma += 1
    require(THETA**gamma < eta_lower <= THETA**(gamma-1),
            "Exact logarithmic potential and preceding-exponent rejection")
    h, j = choose_rank(bits, c, uniform, gamma)
    gap = h*(c-uniform)-bits*c-gamma*j
    require((bits, K, gamma, h, j) ==
            (case["expected_bits"], case["expected_K"], case["expected_gamma"],
             case["expected_H"], case["expected_J"]),
            "Exact declared finite-template values")
    require(h >= bits and h < 2**j and gap == c-uniform > 0,
            "Strict uniform leaf bound at the declared finite rank")
    require((h-1)*(c-uniform) <= bits*c+gamma*j,
            "One lower H fails this stated strict sufficient bound")
    tiny_h, tiny_j = choose_rank(bits, c, c-Q(1, 10**50), gamma)
    require(tiny_j > 128 and tiny_h < 2**tiny_j
            and tiny_h*Q(1, 10**50) > bits*c+gamma*tiny_j,
            "The finite-rank search has no fixed iteration cap")
    return {
        "m": "121^"+str(v), "minimum_target": "17^"+str(v),
        "maximum_paid": "10^"+str(v), "ambient_binary_bound": bits,
        "theta": THETA, "eta_dyadic_exponent": K,
        "eta_strict_lower_bound": eta_lower, "gamma": gamma,
        "uniform_saving": uniform, "H": h, "J": j, "N": "2^"+str(h),
        "strict_final_power_gap": gap,
        "unbounded_search_control": {"H": tiny_h, "J": tiny_j},
    }


def outer_point(c, kappa, ledger):
    d = (c-kappa)/7
    p = {
        "kappa": kappa, "tested_saving": c,
        "complex_uniform_saving": kappa+6*d,
        "b": kappa+5*d, "a": kappa+4*d, "q": kappa+3*d,
        "bit_saving": Q("0.0027"), "epsilon": 1-d,
        "beta": 1-3*d, "r0": d/10, "stop": d, "layout": d, "d": d,
    }
    value = ledger.ledger(p)
    require(len(value["strict_checks"]) == 54
            and len(value["functional_checks"]) == 3
            and len(value["margins"]) == 9, "Every source outer cost and predicate")
    require(all(x > 0 for x in value["strict_checks"].values())
            and all(x > 0 for x in value["functional_checks"].values()),
            "All 57 strict and functional outer predicates")
    require(all(x > kappa for x in value["margins"].values()),
            "All nine cost savings strictly exceed the final kappa")
    controls = {}
    for label, change in (
        ("unfunded_tested_endpoint", {"kappa": c}),
        ("closed_uniform_gap", {"complex_uniform_saving": p["b"]}),
        ("closed_precision_slack", {"epsilon": Q(1)}),
        ("insufficient_BIT", {"bit_saving": Q("0.0023")}),
    ):
        mutated = ledger.ledger(dict(p, **change))
        failed = {k: v for k, v in mutated["strict_checks"].items() if v <= 0}
        require(failed, "The full consumer rejects " + label)
        controls[label] = failed
    return {
        "ledger": value, "minimum_saving_minus_kappa": min(value["margins"].values())-kappa,
        "controls": controls,
    }


def build(source_root):
    previous = baseline(source_root)
    source_result = previous["source_replay"]
    require(source_result["status"] ==
            "PASS_SOURCE_BOUND_CONDITIONAL_P7_PAID_PADDING_IMPROVEMENT",
            "The exact complete native p7 source is required")
    strict = source_result["strictification"]
    native = strict["native_inventory"]
    targets = {int(k): v for k, v in strict["targets"].items()}
    paid = {int(k): v for k, v in strict["paid"].items()}
    require((native["p"], native["keep"], native["dimension"]) == (7, 232127, 121),
            "The same full physical controller and ambient rank")
    B = sum(targets.values())
    T1, P1 = (sum(r*n for r, n in hist.items()) for hist in (targets, paid))
    require((B, T1, P1, sum(paid.values())) == (7688, 131723, 131115, 55998),
            "Complete productive ownership and paid-call inventory")
    require(B*17 == 130696 < P1 < T1 and 10 < 17 < 121,
            "Completion is fully paid, fits the ambient rank, and has a smaller tail")
    require(TAIL_BOUND**BLOCK < Q(1, 2), "Exact rational paid-tail decay block")

    pkg = source_root / SOURCE_REL
    E = module("padding_endpoint_primary_intervals",
               pkg/"source/research/kappa-rebuild/architecture/mixed_target_probe.py")
    I = module("padding_endpoint_independent_intervals",
               pkg/"dependencies/compiler-refill/template_bound.py")
    L = module("padding_endpoint_frozen_ledger", pkg/"dependencies/compiler-refill/endpoint.py")
    bit = json.loads((pkg/"source/research/kappa-rebuild/bit/BIT-ALLSIZE-PARAMETERS.json").read_text())
    require(Q(bit["ordinary_saving_admitted"]) == Q("0.0027"),
            "The same separately admitted ordinary BIT saving")

    cases = []
    for case in CASES:
        c, kappa, v = case["C"], case["kappa"], case["v"]
        alpha_upper = 1-case["alpha_gap"]
        engines = {}
        for name, engine in (("source", E), ("independent", I)):
            if name == "source":
                tlo, thi = engine.moment(targets, c)
                plo, phi = engine.moment(paid, c)
            else:
                tlo, thi = engine.moment_margin(targets, {}, c)
                plo, phi = engine.moment_margin(paid, {}, c)
            llo, lhi = engine.log_interval(10)
            clo = engine.exp_interval(c*llo)[0]
            chi = engine.exp_interval(c*lhi)[1]
            alpha = (plo/thi, phi/tlo)
            tail = (P1/(chi*thi), P1/(clo*tlo))
            padding = (B*17/(chi*thi), B*17/(clo*tlo))
            wrong_floor = (B*18/(chi*thi), B*18/(clo*tlo))
            require(0 < alpha[1] < alpha_upper < 1,
                    name+": full raw mixed margin supports the chosen envelope")
            require(tail[1] < TAIL_BOUND < 1 and padding[1] < TAIL_BOUND,
                    name+": both paid tails are charged below the same envelope")
            require(wrong_floor[0] > 1,
                    name+": enlarging the floor to base18 fails the padding-tail criterion")
            engines[name] = {
                "target_moment": E.show((tlo, thi)),
                "paid_moment": E.show((plo, phi)),
                "alpha": E.show(alpha), "original_paid_tail": E.show(tail),
                "completion_tail": E.show(padding),
                "base18_rejected_completion_tail": E.show(wrong_floor),
            }
        require(v % BLOCK == 0, "Whole rational tail-decay blocks")
        blocks = v//BLOCK
        upper = 1/(1+v*case["alpha_gap"])+Q(4, 2**blocks)
        require(upper < 1, "Complete tensor/padding/splitting moment is strictly positive")
        earlier_v = v-BLOCK
        earlier = 1/(1+earlier_v*case["alpha_gap"])+Q(4, 2**(blocks-1))
        require(earlier >= 1, "One fewer block fails this sufficient charged-tail envelope")
        template = logarithmic_template(case)
        outer = outer_point(c, kappa, L)
        require(template["uniform_saving"] ==
                outer["ledger"]["parameters"]["complex_uniform_saving"],
                "The finite supplier actually funds the complete outer consumer")
        cases.append({
            "name": case["name"], "tested_saving": c, "kappa": kappa,
            "tensor_power": v, "paid_cutoff_base": 10, "target_floor_base": 17,
            "alpha_upper": alpha_upper, "paid_tail_upper": TAIL_BOUND,
            "decay_block_length": BLOCK, "decay_block_count": blocks,
            "normalized_paid_moment_upper": upper,
            "strict_complete_moment_gap": 1-upper,
            "preceding_block_rejected_upper": earlier,
            "moment_engines": engines, "template": template, "outer": outer,
            "rank_one_surplus": str(T1)+"^"+str(v)+"-"+str(P1)+"^"+str(v),
        })
    bad_c = Q("0.00268649")
    lo, hi = E.moment(targets, bad_c)
    plo, phi = E.moment(paid, bad_c)
    require(hi-plo < 0, "The nearby higher tested raw point is strictly rejected")
    return encode({
        "schema": "p7-larger-paid-floor-and-higher-conditional-endpoint/1",
        "status": "PASS_COMPLETE_P7_PADDING_AND_HIGHER_CONDITIONAL_KAPPA",
        "source_commit": SOURCE_COMMIT, "companion_sha256": COMPANION_PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"PROOF.md").read_bytes()).hexdigest(),
        "targets": targets, "paid": paid,
        "productive_fields": B, "target_rank_one_moment": T1, "paid_rank_one_moment": P1,
        "new_padding_rank_bound": B*17, "padding_tail_below_original_tail": True,
        "source_replay_status": source_result["status"],
        "source_result_sha256": sha256((pkg/"RESULT.json").read_bytes()).hexdigest(),
        "cases": cases,
        "nearby_raw_moment_rejection": {
            "tested_saving": bad_c, "target_minus_paid": E.show((lo-phi, hi-plo)),
        },
        "scope": [
            "The complete source native controller, paid invoice and outer receipt are authenticated and replayed.",
            "Chronological native composition and fully paid target completion are applied to the same arbitrary original fields.",
            "The logarithmic proof retains every source complement, paid owned-bank call, whole-job normalizer and finite batch denominator.",
            "Each new compiled word has its own scalar, movement, storage, precision and reserve constants.",
            "The all-column, physical, analytic, fixed-tape and exact-recovery premises remain conditional.",
            "No materialized winning word, practical runtime, globally optimal kappa or selected-frontier change is claimed.",
        ],
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True,
                        help="Separate checkout root of pinned PR4416, containing research/pr4359-p7-padding.")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--out", type=Path)
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build(args.source_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        require((HERE/"CERTIFICATE.json").read_text() == text,
                "Exact deterministic larger-floor and endpoint receipt")
    print(json.dumps({
        "status": result["status"],
        "cases": [{"name": c["name"], "kappa": c["kappa"], "N": c["template"]["N"],
                   "minimum_outer_slack": c["outer"]["minimum_saving_minus_kappa"]}
                  for c in result["cases"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
