#!/usr/bin/env python3
"""Stronger odd-dimensional rank certificates from two symplectic flags."""

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import reduce
import hashlib
import json
from operator import xor
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source import authenticate


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return (a & b).bit_count() % 2


def parameters(d):
    need(type(d) is int and d >= 3 and d % 2 == 1, "odd dimension at least three")
    k, t = (d - 1)//2, 2**(d - 2)
    n, regular = 2*t - 1, (d - 3)*t + 1
    low, high = k, 2**k - 1
    alpha = F(0) if k == 1 else (F(regular, t - 1) - low)/(high - low)
    rho = F(regular, n*(t - 1))
    need(k == 1 or 0 < alpha < 1, "valid flag mixture")
    return {"k": k, "t": t, "n": n, "regular": regular,
            "low": low, "high": high, "alpha": alpha, "rho": rho}


def symplectic_pairs(d):
    need(d in (3, 5, 7), "bounded odd flag geometry")
    work = [1 ^ (1 << i) for i in range(1, d)]
    pairs = []
    while work:
        e = work[0]
        f = next((v for v in work[1:] if dot(e, v)), None)
        need(f is not None, "nondegenerate alternating complement")
        work = [v ^ (e if dot(v, f) else 0) ^ (f if dot(v, e) else 0)
                for v in work if v not in (e, f)]
        pairs.append((e, f))
    need(len(pairs) == (d - 1)//2, "symplectic pair count")
    for i, (e, f) in enumerate(pairs):
        need(not e.bit_count() % 2 and not f.bit_count() % 2 and dot(e, f),
             "symplectic pair")
        for j, (u, v) in enumerate(pairs):
            need(dot(e, u) == dot(f, v) == 0 and dot(e, v) == (i == j),
                 "symplectic basis Gram matrix")
    return tuple(pairs)


def universe(d):
    need(d in (3, 5, 7), "bounded odd flag geometry")
    odd = [v for v in range(2**d) if v.bit_count() % 2]
    return tuple((q, w) for q in odd for w in odd if dot(q, w))


def orbit(d, port):
    q, w = port
    j = 2**d - 1
    if q == w == j:
        return "special"
    if q == j or w == j:
        return "one-special"
    return "diagonal" if q == w else "cross"


def selector(d, flag):
    need(flag in ("low", "high"), "known flag")
    pairs = symplectic_pairs(d)
    basis = ([x for pair in pairs for x in pair] if flag == "low" else
             [e for e, _ in pairs] + [f for _, f in pairs])
    sinks = [reduce(xor, (b for i, b in enumerate(basis) if mask >> i & 1), 0)
             for mask in range(2**len(basis))]
    h = [x for x in range(2**d) if not x.bit_count() % 2]
    need(set(sinks) == set(h), "flag enumerates the complete alternating space")
    j, chosen, sizes = 2**d - 1, [], []
    for stop, y in enumerate(sinks):
        block = sorted((j ^ x, j ^ y) for x in h if all(not dot(x, z) for z in sinks[:stop + 1]))
        chosen.extend(block)
        sizes.append(len(block))
    return tuple(chosen), tuple(basis), tuple(sizes)


def check_selector(d, flag, chosen):
    need(flag in ("low", "high"), "known flag")
    need(len(chosen) == len(set(chosen)), "flag repeats a type")
    need(set(chosen) <= set(universe(d)), "flag contains an inadmissible type")
    need(all(dot(w, q) for i, (_, w) in enumerate(chosen) for q, _ in chosen[i:]),
         "flag is not triangular")
    p = parameters(d)
    counts = Counter(orbit(d, x) for x in chosen)
    expected = {"special": 1, "one-special": 2*p["n"], "diagonal": p[flag],
                "cross": p["regular"] - p[flag]}
    need(all(counts[name] == count for name, count in expected.items()), "wrong flag orbit counts")
    need(len(chosen) == (d + 1)*p["t"], "flag size")
    return expected


def weights(d, flag):
    p = parameters(d)
    return {"special": F(1), "one-special": F(1), "diagonal": F(p[flag], p["n"]),
            "cross": F(0) if d == 3 else F(p["regular"] - p[flag], p["n"]*(p["t"] - 2))}


def check_mixture(d, alpha):
    p = parameters(d)
    need(0 <= alpha <= 1, "convex flag mixture")
    low, high = weights(d, "low"), weights(d, "high")
    regular_orbits = ("diagonal",) if d == 3 else ("diagonal", "cross")
    need(all((1 - alpha)*low[name] + alpha*high[name] == p["rho"] for name in regular_orbits),
         "mixture does not balance regular orbits")


def weighted_bounds(d, multiplicities):
    need(set(multiplicities) <= set(universe(d)), "weighted ports are inadmissible")
    need(all(type(x) is int and x >= 0 for x in multiplicities.values()), "nonnegative integer multiplicities")
    counts = Counter()
    for port, count in multiplicities.items():
        counts[orbit(d, port)] += count
    p = parameters(d)
    low = sum(weights(d, "low")[name]*count for name, count in counts.items())
    high = sum(weights(d, "high")[name]*count for name, count in counts.items())
    peeled = counts["special"] + counts["one-special"]
    balanced = peeled + p["rho"]*(counts["diagonal"] + counts["cross"])
    need(max(low, high) >= balanced, "weighted maximum dominates the balanced row")
    return {"low": low, "high": high, "maximum": max(low, high),
            "balanced": balanced, "peeled": peeled}


def run(archive=None):
    authenticate(archive)
    reports = []
    for d in (3, 5, 7):
        p = parameters(d)
        allowed = universe(d)
        orbit_sizes = Counter(orbit(d, x) for x in allowed)
        expected_sizes = {"special": 1, "one-special": 2*p["n"], "diagonal": p["n"],
                          "cross": p["n"]*(p["t"] - 2)}
        need(all(orbit_sizes[name] == size for name, size in expected_sizes.items()), "odd type orbits")
        flags = []
        for flag in ("low", "high"):
            chosen, basis, sizes = selector(d, flag)
            counts = check_selector(d, flag, chosen)
            check_selector(d, flag, tuple((w, q) for q, w in reversed(chosen)))
            flags.append({"flag": flag, "types": len(chosen), "counts": counts,
                          "basis": basis, "blocks": sizes,
                          "selector_sha256": hashlib.sha256(json.dumps(chosen, separators=(",", ":")).encode()).hexdigest()})
        check_mixture(d, p["alpha"])
        uniform = weighted_bounds(d, {x: 1 for x in allowed})
        need(uniform["low"] == uniform["high"] == (d + 1)*p["t"], "uniform orbit calibration")
        irregular = weighted_bounds(d, {x: (7*i + 2) % 5 for i, x in enumerate(allowed)})
        if d > 3:
            diagonal_only = weighted_bounds(d, {x: 7 for x in allowed if orbit(d, x) == "diagonal"})
            cross_only = weighted_bounds(d, {x: 7 for x in allowed if orbit(d, x) == "cross"})
            need(diagonal_only["high"] > diagonal_only["balanced"] > diagonal_only["low"],
                 "high flag improves a diagonal-heavy population")
            need(cross_only["low"] > cross_only["balanced"] > cross_only["high"],
                 "low flag improves a cross-heavy population")
        reports.append({"dimension": d, "universe": len(allowed), "flags": flags,
                        "rho": str(p["rho"]), "high_weight": str(p["alpha"]),
                        "weighted_fixture": {key: str(value) for key, value in irregular.items()}})
    for d in range(5, 50, 2):
        p = parameters(d)
        check_mixture(d, p["alpha"])
        need(p["low"] < F(p["regular"], p["t"] - 1) < p["high"], "strict mixing interval")
    need(parameters(5)["rho"] == F(17, 105) and parameters(7)["rho"] == F(43, 651), "new source instances")
    need(int(5/parameters(5)["rho"]) == 30, "five-dimensional bit-window limit")
    need(5*parameters(5)["rho"] == F(17, 21) > F(291, 400), "declared charge-five screen")
    for rank_one, expected in ((74, False), (75, True), (76, True)):
        terms = 44 + rank_one
        ports = 15*44 + rank_one
        need((parameters(5)["rho"]*ports <= terms) == expected,
             "mixed-rank count boundary")
    return {"status": "PASS_ODD_FLAG_RANK", "certificates": reports,
            "scope": "Two finite flags corroborate the arbitrary-field/multiplicity proof; no supplier or kappa claim."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source_archive), sort_keys=True))
