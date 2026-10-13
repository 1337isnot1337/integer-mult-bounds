#!/usr/bin/env python3
"""Exact spectral split-residual diagnostic; Python standard library only.

Douglas R. Colkitt with substantial OpenAI Codex assistance. Apache-2.0.
No supplier imports, floating arithmetic, or assertions disabled by -O.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def multiplicities(width, ambient):
    """Binomial eigenvalue counts of C_width on 2**ambient coefficients."""
    require(0 <= width <= ambient, "invalid width")
    return [sum(comb(width, k) for k in range(j, width + 1, 4))
            << (ambient - width) for j in range(4)]


def multiplicities_dp(width):
    counts = [1, 0, 0, 0]
    for _ in range(width):
        counts = [counts[j] + counts[(j - 1) % 4] for j in range(4)]
    return counts


def make_route(a, b):
    """Full permutation: source eigenvectors first, scratch in unused slots."""
    r = a + b
    n = 1 << r
    phases = [(i & ((1 << a) - 1)).bit_count() % 4 for i in range(n)]
    phases += [(i & ((1 << b) - 1)).bit_count() % 4 for i in range(n)]
    bins = [[i for i, p in enumerate(phases) if p == j] for j in range(4)]
    need = multiplicities(r, r)
    require(all(len(bins[j]) >= need[j] for j in range(4)),
            "insufficient eigenspace capacity")
    used = [0] * 4
    route = []
    for x in range(n):
        j = x.bit_count() % 4
        route.append(bins[j][used[j]])
        used[j] += 1
    occupied = set(route)
    route += [i for i in range(2 * n) if i not in occupied]
    check_route(route, phases, r)
    return route, phases


def check_route(route, phases, r):
    n = 1 << r
    require(len(route) == 2 * n and sorted(route) == list(range(2 * n)),
            "route is not a permutation")
    require(all(phases[route[x]] == x.bit_count() % 4 for x in range(n)),
            "route mismatches a source eigenvalue")


@dataclass
class Vector:
    """(real + i*imag) / 2**shift, with unbounded exact integer numerators."""

    real: list
    imag: list
    shift: int = 0


def zero(n):
    return Vector([0] * n, [0] * n)


def basis(n, column):
    v = zero(n)
    v.real[column] = 1
    return v


def equal(x, y):
    shift = max(x.shift, y.shift)
    return (len(x.real) == len(y.real)
            and all((a << (shift - x.shift)) == (b << (shift - y.shift))
                    for a, b in zip(x.real + x.imag, y.real + y.imag)))


def walsh(v, width, inverse=False):
    re, im = v.real.copy(), v.imag.copy()
    for axis in range(width):
        bit = 1 << axis
        for block in range(0, len(re), 2 * bit):
            for i in range(block, block + bit):
                j = i + bit
                re[i], re[j] = re[i] + re[j], re[i] - re[j]
                im[i], im[j] = im[i] + im[j], im[i] - im[j]
    return Vector(re, im, v.shift + (width if inverse else 0))


def kernel(v, width):
    """Butterfly evaluation with C = ((1+i,1-i),(1-i,1+i))/2."""
    re, im = v.real.copy(), v.imag.copy()
    for axis in range(width):
        bit = 1 << axis
        for block in range(0, len(re), 2 * bit):
            for i in range(block, block + bit):
                j = i + bit
                sr, si = re[i] + re[j], im[i] + im[j]
                dr, di = re[i] - re[j], im[i] - im[j]
                re[i], im[i], re[j], im[j] = sr - di, si + dr, sr + di, si - dr
    return Vector(re, im, v.shift + width)


def mul(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def power(z, exponent):
    out = (1, 0)
    for _ in range(exponent):
        out = mul(out, z)
    return out


def reference_column(width, column):
    """Independent Kronecker entry formula; no butterfly or encoder calls."""
    n = 1 << width
    entries = [mul(power((1, 1), width - d), power((1, -1), d))
               for d in range(width + 1)]
    vals = [entries[(x ^ column).bit_count()] for x in range(n)]
    return Vector([z[0] for z in vals], [z[1] for z in vals], width)


def join(x, y):
    shift = max(x.shift, y.shift)
    re = [a << (shift - x.shift) for a in x.real]
    im = [a << (shift - x.shift) for a in x.imag]
    re += [a << (shift - y.shift) for a in y.real]
    im += [a << (shift - y.shift) for a in y.imag]
    return Vector(re, im, shift)


def split(v):
    n = len(v.real) // 2
    return (Vector(v.real[:n], v.imag[:n], v.shift),
            Vector(v.real[n:], v.imag[n:], v.shift))


def permute(v, route, inverse=False):
    if inverse:
        return Vector([v.real[i] for i in route], [v.imag[i] for i in route], v.shift)
    re, im = [0] * len(route), [0] * len(route)
    for source, target in enumerate(route):
        re[target], im[target] = v.real[source], v.imag[source]
    return Vector(re, im, v.shift)


def phase(v, exponents):
    units = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    out = [mul((x, y), units[k % 4]) for x, y, k in zip(v.real, v.imag, exponents)]
    return Vector([z[0] for z in out], [z[1] for z in out], v.shift)


def walsh_by_child(v, width, inverse=False):
    """Check the paid reduction H_k=(1-i)^k S_k C_k S_k independently."""
    exponents = [(i & ((1 << width) - 1)).bit_count() for i in range(len(v.real))]
    out = phase(kernel(phase(v, exponents), width), exponents)
    factor = power((1, -1), width)
    values = [mul((x, y), factor) for x, y in zip(out.real, out.imag)]
    return Vector([z[0] for z in values], [z[1] for z in values],
                  out.shift + (width if inverse else 0))


def collapsed_program(h, z, route, phases, width):
    """Cancel both host sandwiches into phases; keep the source boundaries."""
    v = permute(join(walsh(h, width), z), route)
    v = phase(v, phases)
    u, v = split(permute(v, route, True))
    return walsh(u, width, True), phase(v, [-phases[i] for i in route[len(h.real):]])


def program(h, z, a, b, route, phases, repair=True, omit=None):
    """E^-1 (C_a direct-sum C_b) E, followed by the dirty phase repair."""
    r = a + b
    source = h if omit == "source_boundaries" else walsh(h, r)
    x, y = split(permute(join(source, z), route))
    if omit != "host_entry":
        x, y = walsh(x, a, True), walsh(y, b, True)
    if omit != "host_calls":
        x, y = kernel(x, a), kernel(y, b)
    x, y = walsh(x, a), walsh(y, b)
    u, v = split(permute(join(x, y), route, True))
    if omit != "source_boundaries":
        u = walsh(u, r, inverse=(omit != "normalization"))
    if repair:
        direction = 1 if omit == "repair_sign" else -1
        v = phase(v, [direction * phases[i] for i in route[len(h.real):]])
    return u, v


def verify_pins():
    pins = json.loads((HERE / "SOURCE-PINS.json").read_text())
    for path, expected in pins["local_sha256"].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected,
                "source pin mismatch: " + path)
    return pins["base_commit"]


def audit():
    base = verify_pins()
    a, b = 4, 5
    r, n = a + b, 1 << (a + b)
    route, phases = make_route(a, b)
    source_counts = multiplicities(r, r)
    host_counts = [multiplicities(a, r)[j] + multiplicities(b, r)[j]
                   for j in range(4)]
    complement = [host_counts[j] - source_counts[j] for j in range(4)]
    require([sum(phases[i] == j for i in route[n:]) for j in range(4)] == complement,
            "complement multiplicity mismatch")

    # Independent arithmetic checks and finite support for the all-f proof.
    for width in range(289):
        require(multiplicities(width, width) == multiplicities_dp(width),
                "binomial/DP eigenvalue disagreement")
    dilations = []
    for f in range(1, 33):
        source = multiplicities(9 * f, 9 * f)
        hosts = [multiplicities(4 * f, 9 * f)[j] + multiplicities(5 * f, 9 * f)[j]
                 for j in range(4)]
        require(all(hosts[j] >= source[j] for j in range(4)), "dilation capacity")
        require(min(Fraction(hosts[j] - source[j], 1 << (9 * f))
                    for j in range(4)) >= Fraction(3, 64), "uniform slack")
        dilations.append({"f": f, "source": source, "hosts": hosts})

    z = zero(n)
    # All complex-linear basis columns, with independent dense tensor entries.
    for column in range(n):
        h = basis(n, column)
        expected = reference_column(r, column)
        require(equal(kernel(h, r), expected), "kernel/reference mismatch")
        for inverse in (False, True):
            require(equal(walsh(h, r, inverse), walsh_by_child(h, r, inverse)),
                    "Walsh one-child invoice identity")
        u, v = program(h, z, a, b, route, phases, repair=False)
        require(equal(u, expected) and equal(v, z), "clean dilation identity")
        u, v = collapsed_program(h, z, route, phases, r)
        require(equal(u, expected) and equal(v, z), "collapsed clean identity")
    for column in range(n):
        scratch = basis(n, column)
        u, v = program(z, scratch, a, b, route, phases, repair=False)
        wanted = phase(scratch, [phases[i] for i in route[n:]])
        require(equal(u, z) and equal(v, wanted), "dirty complement identity")
        u, v = program(z, scratch, a, b, route, phases)
        require(equal(u, z) and equal(v, scratch), "dirty restoration identity")
        u, v = collapsed_program(z, scratch, route, phases, r)
        require(equal(u, z) and equal(v, scratch), "collapsed dirty identity")

    controls = {}
    try:
        make_route(1, 1)
    except ValueError as exc:
        require(str(exc) == "insufficient eigenspace capacity", "wrong capacity failure")
        controls["rank_two_into_two_rank_one_owners"] = "REJECTED: missing -1 eigenspace"
    require(len(controls) == 1, "infeasible embedding accepted")
    bad = route.copy()
    bad[0], bad[1] = bad[1], bad[0]
    try:
        check_route(bad, phases, r)
    except ValueError as exc:
        require(str(exc) == "route mismatches a source eigenvalue", "wrong route failure")
        controls["wrong_eigenvalue_route"] = "REJECTED"
    require(len(controls) == 2, "bad route accepted")
    h = basis(n, 0)
    expected = reference_column(r, 0)
    for omission in ["source_boundaries", "host_entry", "host_calls", "normalization"]:
        u, v = program(h, z, a, b, route, phases, omit=omission)
        require(not (equal(u, expected) and equal(v, z)), "mutation survived: " + omission)
        controls["omit_" + omission] = "REJECTED on source basis column 0"
    j = next(j for j, slot in enumerate(route[n:]) if phases[slot] % 2 == 1)
    dirty = basis(n, j)
    for name, repair, omission in [("unrestored_dirty_workspace", False, None),
                                   ("wrong_dirty_repair_sign", True, "repair_sign")]:
        u, v = program(z, dirty, a, b, route, phases, repair=repair, omit=omission)
        require(not equal(v, dirty), "dirty mutation survived")
        controls[name] = {"status": "REJECTED", "scratch_basis_column": j,
                          "unrepaired_phase_exponent": phases[route[n + j]]}

    # At sigma=1 rank mass is already larger. For 0<sigma<1 every ratio
    # in (0,1) only increases, so these are exact uniform lower bounds.
    charged = {r: 2, a: 3, b: 3}
    optimistic = {r: 2, a: 2, b: 2}
    charged_ratio = sum(Fraction(k * width, r) for width, k in charged.items())
    free_owner_ratio = sum(Fraction(k * width, r) for width, k in optimistic.items())
    require(charged_ratio == 5 and free_owner_ratio == 4, "complete cost profile")
    return {
        "status": "PASS_EXACT_DILATION_AND_UNFAVORABLE_BOUNDARY_BUDGET",
        "base_commit": base,
        "assignment_seed": 51,
        "object": {"r": r, "a": a, "b": b, "coefficients_per_stream": n},
        "source_multiplicities": source_counts,
        "host_multiplicities": host_counts,
        "dirty_complement_multiplicities": complement,
        "route_sha256": digest(route),
        "coverage": {"clean_basis_columns": n, "dirty_basis_columns": n,
                     "dirty_repaired_basis_columns": n,
                     "independent_tensor_columns": n,
                     "Walsh_child_reduction_columns_both_directions": 2 * n,
                     "collapsed_program_basis_columns": 2 * n,
                     "binomial_dp_widths": [0, 288], "dilation_f": [1, 32],
                     "dilation_counts_sha256": digest(dilations)},
        "uniform_capacity_slack_lower_bound": "3/64",
        "recursive_width_profile": dict(sorted(charged.items())),
        "free_host_width_profile": dict(sorted(optimistic.items())),
        "moment_ratio_lower_bound_for_0_lt_sigma_le_1": str(charged_ratio),
        "free_host_moment_ratio_lower_bound": str(free_owner_ratio),
        "collapsed_host_sandwich_profile": {r: 2},
        "collapsed_host_moment_ratio": "2",
        "negative_controls": controls,
        "scope": "Exact finite operator replay and written all-f algebraic argument; "
                 "this literal encoder loses even with free routing and owner calls. "
                 "No all-size tape compiler, global lower bound, or new kappa.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, help="write a fresh deterministic certificate")
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(text)
    else:
        require(json.loads(text) == json.loads((HERE / "CERTIFICATE.json").read_text()),
                "committed certificate differs from the replay")
    print(result["status"])
    print("512 clean + 512 dirty + 512 repaired columns; 8 negative controls; "
          "moment ratio >= 5 (>= 4 with free hosts; 2 after host collapse).")


if __name__ == "__main__":
    main()
