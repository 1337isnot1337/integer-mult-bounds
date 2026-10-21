#!/usr/bin/env python3
"""All-p ceiling for the declared two-chain complete invoice formulas.

The unbounded proof is in PROOF.md. Exact directed neighbor bounds and
authenticated complete source replays supply its finite premises.
Apache-2.0.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
COMPANION_PINS = {
    "verify.py": "5f5e00fce1d3940189f957a2bde03bd9cd07daaefbd1e86958e0c461e415fa0c",
    "PROOF.md": "3600e8445612f732ffe0bbd4cb4c0f5b32761109da6f85c70067a3f66be6991a",
    "CERTIFICATE.json": "af8dfb46adcdbf1acee2580b3a539204df9f4c5d2ea48b875d693f37eb8cffe4",
}
SOURCE_PACKAGE = "research/pr4359-p7-padding"
SOURCE_PINS = {
    "scan.py": "30caf3b8d64862ba32c3b708b52c88db10ff1eeb4f68f1624f2ff488869b6cdc",
    "source/research/kappa-rebuild/complex/full-identity-certificates/RESULT.json":
        "943d5fad2fc529f470df05a35446e07ecaef7344abfce450d2c2eb2c9b3798f6",
}
EXPECTED_H = {5:28, 6:18, 7:56, 8:93, 9:213}
EXPECTED_N = {1:2487, 2:713, 3:224, 4:102, 5:20, 8:8}


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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "Python source loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def dependencies(source_root):
    companion = HERE.parent/"kappa-4416-root-family"
    for relative, pin in COMPANION_PINS.items():
        require(sha256((companion/relative).read_bytes()).hexdigest() == pin,
                "Changed root-family companion: "+relative)
    for relative, pin in SOURCE_PINS.items():
        require(sha256((source_root/SOURCE_PACKAGE/relative).read_bytes()).hexdigest() == pin,
                "Changed declared-invoice source: "+relative)
    family = load("chain_limit_root_family", companion/"verify.py")
    replay = family.build(source_root)
    require(replay == json.loads((companion/"CERTIFICATE.json").read_text()),
            "Complete exact root-family, outer and native dependency replay")
    require(replay["status"] == "PASS_ALL_FIXED_STRICT_ROOT_BELOW_KAPPAS_AND_SCOPED_MOMENT_CEILING",
            "Required strict root-family result")
    # Its full replay authenticated this implementation before this import.
    logs = load("chain_limit_logs", HERE.parent/"kappa-4416-log-template/verify.py")
    scan = load("chain_limit_source_scan", source_root/SOURCE_PACKAGE/"scan.py")
    local_path = next(path for path in SOURCE_PINS if path.endswith("RESULT.json"))
    local = json.loads((source_root/SOURCE_PACKAGE/local_path).read_text())["providers"]["THREE-base"]
    helpers = {int(r): n for r, n in local["helper_boundary"]["widths"].items()}
    paid = {int(r): n for r, n in local["unsplit_replays"]["forward"]["paid_profile"].items()}
    backward = {int(r): n for r, n in local["unsplit_replays"]["backward"]["paid_profile"].items()}
    require(helpers == EXPECTED_H and paid == backward == EXPECTED_N,
            "Actual local helper counts and both complete paid orientations")
    return family, family.Intervals(logs), scan, replay, helpers, paid


def profile(p, a, helpers, paid):
    require(type(p) is int and p >= 1 and type(a) is int and 0 <= a < p,
            "Declared integer p and valid chain split")
    targets = Counter({r: (2*p+1)*n for r, n in helpers.items()})
    calls = Counter({r: (2*p+1)*n for r, n in paid.items()})
    targets[16*p+9] += 224
    for length in (a, p-1-a):
        for j in range(length):
            targets[16*j+25] += 224
            calls[16*j+16] += 224
    calls[8] += 224*(p-1)
    return targets, calls


def signed(targets, paid):
    result = Counter(targets)
    result.subtract(paid)
    return {r: n for r, n in result.items() if n}


def subtract(first, second):
    result = Counter(first)
    result.subtract(second)
    return {r: n for r, n in result.items() if n}


def balanced(p, helpers, paid):
    return signed(*profile(p, (p-1)//2, helpers, paid))


def band(E, coefficients, low, high):
    """Enclose the whole saving interval, including all signed terms."""
    require(Q(0) < low < high < Q(1), "Strict saving interval")
    lower = upper = Q(0)
    for rank, count in coefficients.items():
        rank_lower = E.power(rank, high, 256)[0]
        rank_upper = E.power(rank, low, 256)[1]
        lower += count*(rank_lower if count >= 0 else rank_upper)
        upper += count*(rank_upper if count >= 0 else rank_lower)
    return lower, upper


def neighbor_maximum(p, E, helpers, paid, low, high):
    require(type(p) is int and p >= 2, "An interior center for both neighbors")
    middle = balanced(p, helpers, paid)
    values = [band(E, subtract(middle, balanced(q, helpers, paid)), low, high)
              for q in (p-1, p+1)]
    require(all(pair[0] > 0 for pair in values), "Both strict neighbor differences")
    return values


def increment_formula(p, helpers, paid):
    result = Counter({r: 2*n for r, n in signed(helpers, paid).items()})
    j = (p-1)//2
    for rank, count in ((16*p+25, 224), (16*p+9, -224),
                        (16*j+25, 224), (16*j+16, -224), (8, -224)):
        result[rank] += count
    return {r: n for r, n in result.items() if n}


def structural_identities(helpers, paid):
    local = signed(helpers, paid)
    # Each pair is (constant coefficient, coefficient of p).
    affine = {r: [n, 2*n] for r, n in local.items()}
    affine[8][0] += 224
    affine[8][1] -= 224
    expected = {1:[-2487, -4974], 2:[-713, -1426], 3:[-224, -448],
                4:[-102, -204], 5:[8, 16], 6:[18, 36], 7:[56, 112],
                8:[309, -54], 9:[213, 426]}
    require(affine == expected, "Exact net affine coefficients for every p")
    require(all(affine[8][0]+p*affine[8][1] >= 0 for p in range(1, 6))
            and 54*6-309 > 0 and 54 > 0,
            "The two sign regimes cover all positive integer p")
    remaining_nine = [affine[9][0]+affine[8][0], affine[9][1]+affine[8][1]]
    require(remaining_nine == [522, 372] and min(remaining_nine) > 0,
            "Rank-nine mass pays the entire negative rank-eight pairing")
    d0, d1 = sum(local.values()), sum(r*n for r, n in local.items())
    require((d0, d1) == (-3146, -1856), "Exact local moments at t=0,1")
    m0 = [d0+448, 2*d0-224]
    m1 = [d1+224*8, 2*d1+224*17]
    require(m0 == [-2698, -6516] and m1 == [-64, 96]
            and m0[0] < 0 and m0[1] < 0 and sum(m1) > 0 and m1[1] > 0,
            "Uniform strict endpoint signs for every p>=1")
    return {"local_moments": [d0, d1], "net_affine_coefficients": affine,
            "paired_rank_eight_count": [-309, 54], "remaining_rank_nine": remaining_nine,
            "t_zero_affine_moment": m0, "t_one_affine_moment": m1}


def rejects(action, label):
    try:
        action()
    except AssertionError:
        return True
    raise AssertionError("Required control did not reject: "+label)


def build(source_root):
    family, E, scan, replay, helpers, paid = dependencies(source_root)
    low, high = map(Q, replay["raw_root_and_uniform_tail"]["root_enclosure"])
    require((low, high) == (family.LOW, family.HIGH), "Authenticated strict root enclosure")
    source_checks = []
    for p, a in ((1, 0), (6, 2), (7, 3), (8, 3)):
        targets, calls = profile(p, a, helpers, paid)
        original_t, original_p, mask = scan.profile(p, a, helpers, paid)
        require(targets == original_t and calls == original_p,
                "Complete declared counts equal immutable source profile")
        require(sum(targets.values())-sum(calls.values()) == -6516*p-2698
                and sum(r*n for r, n in targets.items())-sum(r*n for r, n in calls.items()) == 96*p-64,
                "Complete endpoint identities at the boundary and relevant neighbors")
        source_checks.append({"p": p, "a": a, "b": p-1-a, "mask": mask,
                              "targets": targets, "paid": calls})
        if p == 7:
            require(mask == 232127 and dict(targets) == {int(r): n for r, n in replay["targets"].items()}
                    and dict(calls) == {int(r): n for r, n in replay["paid"].items()},
                    "The maximizing formula is the actual admitted complete p7 invoice")
    structure = structural_identities(helpers, paid)
    for p in (1, 6, 7):
        require(subtract(balanced(p+1, helpers, paid), balanced(p, helpers, paid)) ==
                increment_formula(p, helpers, paid),
                "Exact balanced increment identity at both floor parities and p=1")
    neighbors = neighbor_maximum(7, E, helpers, paid, low, high)
    decimal_bounds = [(Q("1.253606978240"), Q("1.253606978241")),
                      (Q("1.427475680484"), Q("1.427475680485"))]
    require(all(a < lo <= hi < b for (lo, hi), (a, b) in zip(neighbors, decimal_bounds)),
            "The displayed strict rational bounds hold throughout the root bracket")
    unbalanced = band(E, subtract(balanced(7, helpers, paid),
                                 signed(*profile(7, 2, helpers, paid))), low, high)
    require(unbalanced[0] > 0, "A genuinely unbalanced split loses at the root")
    controls = {
        "p_zero_rejected": rejects(lambda: profile(0, 0, helpers, paid), "nonpositive p"),
        "invalid_chain_split_rejected": rejects(lambda: profile(7, 7, helpers, paid), "a=p"),
        "p6_cannot_replace_maximizer": rejects(
            lambda: neighbor_maximum(6, E, helpers, paid, low, high), "wrong center p6"),
        "p8_cannot_replace_maximizer": rejects(
            lambda: neighbor_maximum(8, E, helpers, paid, low, high), "wrong center p8"),
        "unbalanced_p7_strictly_worse": unbalanced[0] > 0,
    }
    require(all(controls.values()), "Every discriminating chain-limit control")
    return encode({
        "schema": "all-p-declared-two-chain-mixed-moment-ceiling/1",
        "status": "PASS_ALL_P_DECLARED_CHAIN_CEILING_AT_P7_ROOT",
        "source_commit": replay["source_commit"], "companion_sha256": COMPANION_PINS,
        "source_sha256": SOURCE_PINS, "complete_companion_replay_status": replay["status"],
        "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE/"PROOF.md").read_bytes()).hexdigest(),
        "local_targets": helpers, "local_paid": paid, "root_enclosure": [low, high],
        "declared_source_profile_checks": source_checks, "global_structure": structure,
        "p7_minus_p6_whole_bracket": neighbors[0], "p7_minus_p8_whole_bracket": neighbors[1],
        "displayed_strict_neighbor_bounds": decimal_bounds, "unbalanced_p7_margin": unbalanced,
        "negative_controls": controls,
        "scope": [
            "All integers p>=1 and all a in {0,...,p-1} in the exact declared complete-invoice formula.",
            "No new native admission or classification of arbitrary controllers or idle masks.",
            "The ceiling concerns positive complete mixed moments and their charged tensor/completion/splitting closure.",
            "The conditional p7 family attains every strict root-below kappa under its inherited premises.",
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
        require((HERE/"CERTIFICATE.json").read_text() == text, "Deterministic exact chain-limit replay")
    print(json.dumps({"status": result["status"], "root_enclosure": result["root_enclosure"],
                      "displayed_strict_neighbor_bounds": result["displayed_strict_neighbor_bounds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
