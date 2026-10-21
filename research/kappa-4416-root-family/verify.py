#!/usr/bin/env python3
"""Constructive conditional p7 root family and its scoped mixed-moment ceiling.

Only integer and rational operations decide acceptance. Immutable companion
files are authenticated before import and their complete source chain is
replayed. The proof, physical premises and scope are in PROOF.md.
Apache-2.0.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import cache
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import itertools
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
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
}
SOURCE_PACKAGE = "research/pr4359-p7-padding"
SOURCE_COMMIT = "e9058860b5c850760fdf970e796a96aefcdb1d98"
LOW = Q("0.002686489048851021139378940762")
HIGH = Q("0.002686489048851021139378940763")
CAP = Q("0.00268649")
KAPPA0 = Q("0.002686488")
SAMPLE_KAPPA = Q("0.002686489")
THETA = Q(61, 75)
TAIL = Q(999, 1000)
BLOCK = 693
EXPECTED_T = {5:420, 6:270, 7:840, 8:1395, 9:3195,
              25:448, 41:448, 57:448, 121:224}
EXPECTED_P = {1:37305, 2:10695, 3:3360, 4:1530, 5:300,
              8:1464, 16:448, 32:448, 48:448}


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


def ceil(value):
    value = Q(value)
    return -((-value.numerator)//value.denominator)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "Python source loader")
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def dependencies(source_root):
    for relative, expected in PINS.items():
        require(sha256((HERE.parent/relative).read_bytes()).hexdigest() == expected,
                "Changed authenticated companion: "+relative)
    padding = module("root_family_padding", HERE.parent/"kappa-4416-padding-endpoint/verify.py")
    replay = padding.build(source_root)
    require(replay == json.loads((HERE.parent/"kappa-4416-padding-endpoint/CERTIFICATE.json").read_text()),
            "Complete native, companion, padding and outer receipt replay")
    require(replay["status"] == "PASS_COMPLETE_P7_PADDING_AND_HIGHER_CONDITIONAL_KAPPA",
            "Required paid-padding source chain")
    previous = next(c for c in replay["cases"] if c["name"] == "higher_conditional_endpoint")
    require(Q(previous["kappa"]) == KAPPA0 and
            Q(previous["outer"]["minimum_saving_minus_kappa"]) > 0,
            "Actual fixed point used when the requested kappa is smaller")
    logs = module("root_family_logs", HERE.parent/"kappa-4416-log-template/verify.py")
    # The preceding replay authenticated every source byte before these imports.
    ledger = module("root_family_ledger", source_root/SOURCE_PACKAGE/"dependencies/compiler-refill/endpoint.py")
    return padding, logs, ledger, replay


class Intervals:
    """Increasing-precision directed moments; there is no fixed-width ceiling."""
    def __init__(self, logs):
        self.logs = logs

    @cache
    def log(self, rank, bits):
        require(type(rank) is int and rank >= 1 and type(bits) is int and bits >= 32,
                "Positive integer logarithm and variable precision")
        return self.logs.outward(self.logs.log_interval(Q(rank), max(1, bits//2)), bits)

    @staticmethod
    def exp(x, terms):
        require(isinstance(x, Q) and 0 <= x < 1 and type(terms) is int and terms >= 1,
                "Positive Taylor enclosure range")
        term = total = Q(1)
        for j in range(1, terms+1):
            term *= x/j
            total += term
        following = term*x/(terms+1)
        return total, total+following/(1-x/(terms+2))

    @cache
    def power(self, rank, saving, bits):
        require(0 <= saving <= CAP, "Certified local elementary-function range")
        if rank == 1:
            return Q(1), Q(1)
        lo, hi = self.log(rank, bits)
        exp_lo = self.exp(saving*lo, max(1, bits//4))[0]
        exp_hi = self.exp(saving*hi, max(1, bits//4))[1]
        return self.logs.outward((Q(rank)/exp_hi, Q(rank)/exp_lo), bits)

    def moment(self, profile, saving, bits):
        require(all(type(r) is int and r >= 1 and type(n) is int and n >= 0
                    for r, n in profile.items()), "Unsigned complete rank profile")
        return tuple(sum(n*self.power(r, saving, bits)[i] for r, n in profile.items())
                     for i in (0, 1))

    def moments(self, targets, paid, saving, bits):
        return self.moment(targets, saving, bits), self.moment(paid, saving, bits)

    def margin(self, targets, paid, saving, bits):
        (tlo, thi), (plo, phi) = self.moments(targets, paid, saving, bits)
        return tlo-phi, thi-plo


def raw_root_and_uniform_tail(E, targets, paid):
    positive = {5:120, 6:270, 7:840, 9:3126, 121:224}
    negative = {1:37305, 2:10695, 3:3360, 4:1530}
    pairs = [(69, 8, 9), (448, 16, 25), (448, 32, 41), (448, 48, 57)]
    decomposition = Counter(positive)
    decomposition.subtract(negative)
    for n, low, high in pairs:
        decomposition[high] += n
        decomposition[low] -= n
    actual = Counter(targets)
    actual.subtract(paid)
    require(dict(sorted((r, n) for r, n in decomposition.items() if n)) ==
            dict(sorted((r, n) for r, n in actual.items() if n)),
            "Global signed-rank decomposition is the exact native mixed profile")
    require(all(r >= 5 for r in positive) and all(r < 5 for r in negative)
            and all(5 <= a < b and n > 0 for n, a, b in pairs),
            "Every term of the scaled decomposition has the proved derivative sign")
    require(sum(actual.values()) == -48310 and sum(r*n for r, n in actual.items()) == 608,
            "Strict integer endpoints give a unique root on the entire exponent interval")
    low, high = E.margin(targets, paid, LOW, 256), E.margin(targets, paid, HIGH, 256)
    require(low[0] > 0 and high[1] < 0 and KAPPA0 < LOW < HIGH < CAP,
            "Two-sided strict rational root enclosure")
    derivative_upper = (sum(n*r*E.log(r, 256)[1] for r, n in paid.items())
                        - sum(n*E.power(r, CAP, 256)[0]*E.log(r, 256)[0]
                              for r, n in targets.items()))
    require(derivative_upper < -223288, "Independent derivative upper bound on the whole cap interval")
    slope_lower = sum(n*r*(E.log(10, 256)[0]-E.log(r, 256)[1])
                      for r, n in targets.items())
    require(slope_lower > -138300, "The convex denominator has the stated tangent slope")
    denominator_lower = Q(131723)-138300*CAP
    uniform_tail_gap = TAIL*denominator_lower-131115
    require(uniform_tail_gap == Q("105.106974567") > 0,
            "A uniform rational paid-tail gap covers all root-below savings")
    require(7688*17 == 130696 < 131115 and 10 < 17 < 121,
            "Every paid completion fits and has a smaller tail than the original paid bill")
    require(2*999**BLOCK < 1000**BLOCK and 2*61**4 < 75**4
            and 10**75 < 17**61 and CAP < Q(1, 2),
            "Exact fixed decay and logarithmic contraction blocks")
    coarse = E.margin(targets, paid, LOW, 64)
    require(coarse[0] < 0 < coarse[1],
            "A fixed short interval is inconclusive and must be refined")
    bad = E.margin(targets, paid, CAP, 256)
    require(bad[1] < 0, "A nonpositive raw point is outside this positive-moment construction")
    return {
        "root_enclosure": [LOW, HIGH], "root_endpoint_margins": [low, high],
        "global_scaled_profile": {"positive": positive, "negative": negative, "pairs": pairs},
        "t_zero_moment": -48310, "t_one_moment": 608,
        "global_sign_scope": "For every 0<C<1, the raw moment is positive exactly when C<C_star.",
        "local_cap": CAP, "local_derivative_upper": derivative_upper,
        "tangent_slope_lower": slope_lower, "coarse_tangent_slope_lower": -138300,
        "uniform_denominator_lower": denominator_lower, "uniform_paid_tail_upper": TAIL,
        "uniform_tail_strict_gap": uniform_tail_gap,
        "padding_numerator": 130696, "paid_tail_numerator": 131115,
        "decay_block": BLOCK, "theta": THETA, "theta_half_power": 4,
        "precision_control": {"inconclusive_64_bit_margin": coarse,
                              "strict_256_bit_margin": low},
        "nonpositive_raw_control": {"saving": CAP, "margin": bad},
    }


class Poly:
    """Small exact Q[x,d] ring used to execute the unchanged source ledger."""
    def __init__(self, terms):
        self.terms = {key: Q(value) for key, value in terms.items() if value}

    @staticmethod
    def of(value):
        return value if isinstance(value, Poly) else Poly({(0, 0): Q(value)})

    def __add__(self, other):
        out = dict(self.terms)
        for key, value in self.of(other).terms.items():
            out[key] = out.get(key, Q(0))+value
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self+-self.of(other)

    def __rsub__(self, other):
        return self.of(other)+-self

    def __mul__(self, other):
        out = {}
        for (i, j), a in self.terms.items():
            for (k, ell), b in self.of(other).terms.items():
                key = i+k, j+ell
                out[key] = out.get(key, Q(0))+a*b
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.of(other)
        require(set(other.terms) == {(0, 0)}, "Only a nonzero scalar polynomial divisor")
        return self*(1/other.terms[(0, 0)])

    def __eq__(self, other):
        return self.terms == self.of(other).terms

    def __lt__(self, other):
        difference = self-self.of(other)
        # The retained ledger only compares sigma-tau=-d with zero.
        # Since d>0, a nonzero scalar multiple of d has this strict sign.
        # Reject any attempted ordering involving x or other monomials.
        if not difference.terms:
            return False
        require(set(difference.terms) == {(0, 1)},
                "Only the proved nonzero-d ordering is available to the ledger")
        return difference.terms[(0, 1)] < 0

    def serialized(self):
        return {str(i)+","+str(j): value for (i, j), value in sorted(self.terms.items())}


def outer_parameters(kappa, saving):
    d = (saving-kappa)/7
    return {
        "kappa": kappa, "tested_saving": saving,
        "complex_uniform_saving": kappa+6*d,
        "b": kappa+5*d, "a": kappa+4*d, "q": kappa+3*d,
        "bit_saving": Q("0.0027"), "epsilon": 1-d, "beta": 1-3*d,
        "r0": d/10, "stop": d, "layout": d, "d": d,
    }


def symbolic_outer(ledger):
    x, d = Poly({(1, 0): 1}), Poly({(0, 1): 1})
    kappa = KAPPA0+x
    p = outer_parameters(kappa, kappa+7*d)
    sigma_minus_tau = (1-p["b"])-(1-p["a"])
    require(sigma_minus_tau == -d and max(sigma_minus_tau, Q(0)) == 0,
            "The exact max branch is zero because sigma-tau=-d<0")
    result = ledger.ledger(p)
    require((len(result["strict_checks"]), len(result["functional_checks"]),
             len(result["margins"])) == (54, 3, 9),
            "Every retained strict, functional and cost row is present")
    xmax, dmax = CAP-KAPPA0, (CAP-KAPPA0)/7
    witnesses = {}
    for group in ("strict_checks", "functional_checks"):
        for name, value in result[group].items():
            value = Poly.of(value)
            require(value.terms, "A zero outer predicate cannot be strictly positive")
            d_power = min(j for i, j in value.terms)
            remainder = Poly({(i, j-d_power): a for (i, j), a in value.terms.items()})
            lower = remainder.terms.get((0, 0), Q(0))
            lower += sum(a*xmax**i*dmax**j for (i, j), a in remainder.terms.items()
                         if a < 0 and (i, j) != (0, 0))
            require(lower > 0, "Universal rational positivity witness: "+name)
            witnesses[group+"/"+name] = {
                "polynomial": value.serialized(), "positive_d_factor": d_power,
                "remaining_polynomial": remainder.serialized(),
                "remaining_strict_lower_bound": lower,
            }
    require(len(witnesses) == 57, "All universal predicate witnesses")
    cost_slacks = {}
    for name, margin in result["margins"].items():
        difference = Poly.of(margin)-kappa
        require(difference == result["strict_checks"][name+"_above_kappa"],
                "The actual cost row matches its universal strict predicate: "+name)
        cost_slacks[name] = difference.serialized()
    return {
        "variables": ["x=kappa-kappa0", "d=(C-kappa)/7"],
        "kappa0": KAPPA0, "x_closed_range": [Q(0), xmax],
        "d_range": {"strict_lower": Q(0), "upper": dmax},
        "internal_max_branch": "sigma-tau=-d<0, hence max=0",
        "predicate_count": len(witnesses), "predicate_witnesses": witnesses,
        "cost_slack_polynomials": cost_slacks,
        "smaller_kappa_method": "Use the authenticated fixed kappa0 program and weaken its exponent.",
    }


def generic_template(saving, uniform, v, logs):
    require(type(v) is int and v >= 1 and 0 < uniform < saving < CAP,
            "Strict finite generic compiler inputs")
    b = 7*v
    K = ceil(1+b*saving)
    gamma = 4*K
    require(121 < 2**7 and K >= 1+b*saving and gamma == 4*K,
            "Symbolic ambient and eta exponents; no huge power is constructed")
    require(2*61**4 < 75**4 and 10**75 < 17**61
            and THETA > Q(1, 2) and 121 > 16,
            "Generic strict contraction and rank-one exit safeguards")
    h, j = logs.choose_rank(saving, uniform, b, gamma)
    gap = h*(saving-uniform)-b*saving-gamma*j
    require(h >= max(b, 2) and h < 2**j and gap > 0,
            "Complete finite logarithmic template inequality")
    return {
        "m": {"base": 121, "exponent": v},
        "minimum_target": {"base": 17, "exponent": v},
        "maximum_paid": {"base": 10, "exponent": v},
        "binary_ambient_bound": b, "eta_dyadic_exponent": K,
        "theta": THETA, "gamma": gamma, "uniform_saving": uniform,
        "N": {"encoding": "2^H", "H": h}, "J": j,
        "strict_final_power_gap": gap,
        "huge_ambient_or_contraction_powers_materialized": False,
    }


def constructive_member(kappa, E, targets, paid, logs, ledger):
    """Partial constructor with the proved precondition kappa<C_star.

    Precision and the dyadic candidate index both increase. A candidate
    equality or inconclusive interval is skipped, not refined forever.
    A strictly root-above request is eventually rejected by its own sign.
    """
    require(isinstance(kappa, Q) and 0 < kappa < CAP, "Requested positive saving inside the cap")
    if kappa <= KAPPA0:
        return {"requested_kappa": kappa, "method": "weaken_authenticated_kappa0", "supplier_kappa": KAPPA0}
    for index in itertools.count(1):
        saving = kappa+Q(1, 2**index)
        if saving >= CAP:
            continue
        bits = 128+8*index
        own_margin = E.margin(targets, paid, kappa, bits)
        require(own_margin[1] > 0, "The requested raw saving has a strictly nonpositive certified moment")
        (tlo, thi), (plo, phi) = E.moments(targets, paid, saving, bits)
        if tlo > phi:
            break
    alpha_upper = phi/tlo
    gap = 1-alpha_upper
    epsilon_bits = 1
    while Q(1, 2**epsilon_bits) > gap:
        epsilon_bits += 1
    epsilon = Q(1, 2**epsilon_bits)
    require(0 < epsilon <= gap < 1, "A certified positive dyadic raw-moment gap")
    ell = max(4, ceil(1/(BLOCK*epsilon)))
    v = BLOCK*ell
    require(ell >= 4 and v*epsilon >= 1,
            "The generic rule has complete normalized paid moment below three quarters")
    # Never form 2**ell, theta**gamma or an ambient integer of tensor size.
    paid_bound = 1/(1+v*epsilon)+Q(1, 4)
    require(paid_bound <= Q(3, 4) < 1, "Complete charged-tail certificate")
    parameters = outer_parameters(kappa, saving)
    template = generic_template(saving, parameters["complex_uniform_saving"], v, logs)
    outer = ledger.ledger(parameters)
    require((len(outer["strict_checks"]), len(outer["functional_checks"]),
             len(outer["margins"])) == (54, 3, 9)
            and all(q > 0 for group in ("strict_checks", "functional_checks") for q in outer[group].values())
            and all(q > kappa for q in outer["margins"].values()),
            "The explicit constructed member funds every actual outer row and guard")
    require(template["uniform_saving"] == outer["parameters"]["complex_uniform_saving"],
            "The exact finite supplier funds the same uniform saving used by the consumer")
    return {
        "requested_kappa": kappa, "method": "constructive_strict_root_family",
        "candidate_index": index, "elementary_precision_bits": bits,
        "tested_saving": saving, "target_moment": [tlo, thi], "paid_moment": [plo, phi],
        "alpha_upper": alpha_upper, "certified_alpha_gap": epsilon,
        "decay_blocks": ell, "tensor_power": v,
        "normalized_complete_paid_moment_upper": paid_bound,
        "strict_complete_moment_gap": 1-paid_bound,
        "template": template, "outer": outer,
        "minimum_outer_saving_minus_kappa": min(outer["margins"].values())-kappa,
        "rank_one_surplus": {"positive_base": 131723, "negative_base": 131115, "power": v},
    }


def must_reject(action, label):
    try:
        action()
    except AssertionError:
        return True
    raise AssertionError("Required negative control did not reject: "+label)


def build(source_root):
    padding, logs, ledger, previous = dependencies(source_root)
    targets = {int(k): v for k, v in previous["targets"].items()}
    paid = {int(k): v for k, v in previous["paid"].items()}
    require(targets == EXPECTED_T and paid == EXPECTED_P,
            "Exactly the authenticated complete raw p7 invoice")
    E = Intervals(logs)
    root = raw_root_and_uniform_tail(E, targets, paid)
    outer = symbolic_outer(ledger)
    member = constructive_member(SAMPLE_KAPPA, E, targets, paid, logs, ledger)
    smaller = constructive_member(Q(1, 1000000), E, targets, paid, logs, ledger)
    controls = {
        "smaller_kappa_uses_certified_fixed_point": smaller["method"] == "weaken_authenticated_kappa0",
        "closed_uniform_gap_rejected": must_reject(
            lambda: generic_template(Q("0.002686489"), Q("0.002686489"), 1, logs),
            "closed uniform saving gap"),
        "outside_cap_rejected": must_reject(
            lambda: constructive_member(CAP, E, targets, paid, logs, ledger), "outside certified cap"),
        "base18_completion_numerator_exceeds_paid_numerator": 7688*18 > 131115,
        "fixed_short_interval_inconclusive": root["precision_control"]["inconclusive_64_bit_margin"][0] < 0,
    }
    require(all(controls.values()), "All named family controls")
    return encode({
        "schema": "constructive-p7-strict-root-family-and-moment-ceiling/1",
        "status": "PASS_ALL_FIXED_STRICT_ROOT_BELOW_KAPPAS_AND_SCOPED_MOMENT_CEILING",
        "source_commit": SOURCE_COMMIT, "companion_sha256": PINS,
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"PROOF.md").read_bytes()).hexdigest(),
        "source_result_sha256": previous["source_result_sha256"],
        "complete_source_replay_status": previous["status"],
        "targets": targets, "paid": paid, "raw_root_and_uniform_tail": root,
        "universal_outer_family": outer, "explicit_constructive_member": member,
        "smaller_kappa_example": smaller, "negative_controls": controls,
        "scope": [
            "Every fixed rational 0<kappa<C_star has a finite conditional program with full inherited outer parameters.",
            "All native, all-column, physical, whole-job, storage, precision, analytic, fixed-tape and recovery premises remain inherited.",
            "The ceiling concerns positive complete mixed moments under the specified raw tensor, paid completion and paid splitting operations.",
            "No universal algorithm lower bound, unconditional multiplication theorem, global controller optimum or practical expanded word is claimed.",
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
        require((HERE/"CERTIFICATE.json").read_text() == text, "Exact deterministic root-family receipt replay")
    member = result["explicit_constructive_member"]
    print(json.dumps({"status": result["status"], "root_enclosure": result["raw_root_and_uniform_tail"]["root_enclosure"],
                      "universal_predicate_count": result["universal_outer_family"]["predicate_count"],
                      "sample_kappa": member["requested_kappa"], "sample_N": member["template"]["N"]}, sort_keys=True))


if __name__ == "__main__":
    main()
