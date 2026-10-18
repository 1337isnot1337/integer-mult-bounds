#!/usr/bin/env python3
"""Independent flag replay in abstract symplectic coordinates."""

from collections import deque
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source import authenticate


def require(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple((x + y) % 2 for x, y in zip(a, b))


def form(a, b):
    return sum(a[i]*b[i + 1] + a[i + 1]*b[i] for i in range(0, len(a), 2)) % 2


def number(a):
    return sum(x*2**i for i, x in enumerate(a))


def rank_mod(matrix, prime):
    rows = [[x % prime for x in row] for row in matrix]
    r = 0
    for c in range(len(rows[0])):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inverse = pow(rows[r][c], -1, prime)
        rows[r] = [x*inverse % prime for x in rows[r]]
        for i in range(r + 1, len(rows)):
            coefficient = rows[i][c]
            rows[i] = [(x - coefficient*y) % prime for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def all_sink_orders(width, expected):
    """Optimize over sink orders by subset DP using explicit annihilators."""
    require(width in (2, 4), "bounded sink-order dynamic program")
    vectors = list(itertools.product((0, 1), repeat=width))[1:]
    n = len(vectors)
    single = [sum(1 << i for i, x in enumerate(vectors) if form(x, y) == 0)
              for y in vectors]
    annihilators = [0]*(1 << n)
    annihilators[0] = (1 << n) - 1
    optimum, previous = [0]*(1 << n), [0]*(1 << n)
    transitions = 0
    for subset in range(1, 1 << n):
        first = subset & -subset
        annihilators[subset] = annihilators[subset ^ first] & single[first.bit_length() - 1]
        remaining, best = subset, -1
        while remaining:
            bit = remaining & -remaining
            score = optimum[subset ^ bit]
            if score > best:
                best, previous[subset] = score, bit
            remaining ^= bit
            transitions += 1
        optimum[subset] = best + annihilators[subset].bit_count()
    require(optimum[-1] == expected, "optimal regular selector over all sink orders")
    subset, order = (1 << n) - 1, []
    while subset:
        bit = previous[subset]
        order.append(vectors[bit.bit_length() - 1])
        subset ^= bit
    order.reverse()
    witness = [(x, y) for stop, y in enumerate(order) for x in vectors
               if all(form(x, z) == 0 for z in order[:stop + 1])]
    require(len(witness) == len(set(witness)) == expected, "sink-order optimum witness")
    require(all(form(y, x) == 0 for i, (_, y) in enumerate(witness) for x, _ in witness[i:]),
            "sink-order witness is triangular")
    return {"dimension": width + 1, "sink_subsets": 1 << n,
            "transitions": transitions, "regular_selector_maximum": expected}


def run_dimension(d):
    k, width = (d - 1)//2, d - 1
    vectors = sorted(itertools.product((0, 1), repeat=width), key=number)
    zero = (0,)*width
    basis = [tuple(int(i == j) for i in range(width)) for j in range(width)]
    # Closed-form symplectic basis in j-perp, independent of the primary
    # Gram-Schmidt construction. Coordinates are interleaved e_i,f_i.
    lift_basis = []
    for i in range(1, k + 1):
        lift_basis.extend((2**(2*i) - 1, 2**(2*i - 1) - 1 + 2**(2*i)))

    def lift(x):
        value = 2**d - 1
        for bit, image in zip(x, lift_basis):
            if bit:
                value ^= image
        return value

    def ambient_dot(x, y):
        return sum(((x >> i) & 1)*((y >> i) & 1) for i in range(d)) % 2

    require(len({lift(x) for x in vectors}) == 2**width, "injective odd lift")
    require(all(ambient_dot(lift(x), lift(y)) == (1 + form(x, y)) % 2
                for x in vectors for y in vectors), "independent mask/lift equation")
    universe = {(x, y) for x in vectors for y in vectors if form(x, y) == 0}
    maps = []
    for a in vectors[1:]:
        mapping = {x: add(x, a) if form(a, x) else x for x in vectors}
        require(all(mapping[mapping[x]] == x for x in vectors), "symplectic involution")
        require(all(form(mapping[x], mapping[y]) == form(x, y) for x in basis for y in basis),
                "symplectic generator")
        maps.append(mapping)
    unseen, orbits = set(universe), []
    while unseen:
        start = min(unseen)
        orbit, pending = {start}, deque([start])
        while pending:
            x, y = pending.popleft()
            for candidate in [(m[x], m[y]) for m in maps] + [(y, x)]:
                require(candidate in universe, "independent type orbit")
                if candidate not in orbit:
                    orbit.add(candidate)
                    pending.append(candidate)
        unseen -= orbit
        orbits.append(orbit)
    t, n, regular = 2**(d - 2), 2**(d - 1) - 1, (d - 3)*2**(d - 2) + 1
    expected_sizes = sorted(x for x in (1, 2*n, n, n*(t - 2)) if x)
    require(sorted(map(len, orbits)) == expected_sizes, "independent orbit sizes")
    flags, orbit_weights = [], []
    expected_digests = {
        (3, "low"): "7c13e839533ba611fd9160c7907ac4bed3e90556c16ede6862ab32543387ff63",
        (3, "high"): "7c13e839533ba611fd9160c7907ac4bed3e90556c16ede6862ab32543387ff63",
        (5, "low"): "0cf9d4433f4388d5d03aa7954b23f547d70fa5c64ea4586377c1a4287c7e5e54",
        (5, "high"): "9003b127e3ea12b62271165f4038c65c8b1eab99d084b1998fb85425d9a2bbc3",
        (7, "low"): "c72aa3bd2bf9e37c6489b253bcc95703abdc1a08540b0480d313008f8533f4cc",
        (7, "high"): "e9d4b6909890c800b601eabef1a3ffb807388b610d381e5a850b87f7333464e5",
    }
    for label, ordered in (("low", basis), ("high", basis[::2] + basis[1::2])):
        sinks = []
        for coordinates in vectors:
            value = zero
            for bit, direction in zip(coordinates, ordered):
                if bit:
                    value = add(value, direction)
            sinks.append(value)
        selected, encoded = [], []
        for stop, y in enumerate(sinks):
            xs = sorted((x for x in vectors if all(form(x, z) == 0 for z in sinks[:stop + 1])), key=lift)
            selected.extend((x, y) for x in xs)
            encoded.extend((lift(x), lift(y)) for x in xs)
        require(len(selected) == (d + 1)*t, "independent flag size")
        require(all(form(y, x) == 0 for i, (_, y) in enumerate(selected) for x, _ in selected[i:]),
                "independent triangular selector")
        digest = hashlib.sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()
        require(digest == expected_digests[(d, label)], "independent flag digest")
        incidences = sorted((len(o), len(o.intersection(selected))) for o in orbits)
        diagonal = k if label == "low" else 2**k - 1
        expected = [(1, 1), (2*n, 2*n), (n, diagonal)]
        if t > 2:
            expected.append((n*(t - 2), regular - diagonal))
        require(incidences == sorted(expected), "independent flag orbit counts")
        orbit_weights.append([F(len(o.intersection(selected)), len(o)) for o in orbits])
        flags.append({"flag": label, "selector_sha256": digest, "incidences": incidences})
    rho = F(regular, n*(t - 1))
    alpha = F(0) if k == 1 else (F(regular, t - 1) - k)/(2**k - 1 - k)
    for i, o in enumerate(orbits):
        x, y = next(iter(o))
        target = F(1) if x == zero or y == zero else rho
        require((1 - alpha)*orbit_weights[0][i] + alpha*orbit_weights[1][i] == target,
                "independent rational mixture")
    # The core has rank one. Arbitrary permitted cross blocks and repeated
    # special types must add exactly six, not merely preserve full rank.
    e, f = basis[:2]
    ports = [(zero, zero)]*2 + [(e, zero)]*2 + [(zero, f)]*2 + [(e, e), (f, f)]
    matrix = [[int(i == j) if form(y, x) == 0 else 1 + (i + j) % 3
               for j, (x, _) in enumerate(ports)] for i, (_, y) in enumerate(ports)]
    for i in (6, 7):
        for j in (6, 7):
            matrix[i][j] = 1
    require(all(i == j or form(y, x) or matrix[i][j] == 0
                for i, (_, y) in enumerate(ports) for j, (x, _) in enumerate(ports)),
            "independent peeling fixture fits")
    for prime in (2, 3, 5, 7):
        require(rank_mod(matrix, prime) == 7, "exact special-port rank addition")
    if d == 3:
        # All seven special/one-special ports are isolated. The three regular
        # diagonal types admit an all-ones rank-one core, attaining rank eight.
        full = sorted(universe)
        endpoint = [[int(i == j) for j in range(len(full))] for i in range(len(full))]
        regular_indices = [i for i, (x, y) in enumerate(full) if x != zero and y != zero]
        require(len(regular_indices) == 3, "dimension-three regular core")
        for i in regular_indices:
            for j in regular_indices:
                endpoint[i][j] = 1
        require(all(i == j or form(y, x) or endpoint[i][j] == 0
                    for i, (_, y) in enumerate(full) for j, (x, _) in enumerate(full)),
                "dimension-three attainment fits")
        require(all(rank_mod(endpoint, p) == 8 for p in (2, 3, 5, 7)),
                "dimension-three weighted-bound attainment")
    return {"dimension": d, "universe": len(universe), "rho": str(rho),
            "high_weight": str(alpha), "flags": flags, "peeling_fields": [2, 3, 5, 7]}


if __name__ == "__main__":
    require(len(sys.argv) == 1, "unknown independent flag arguments")
    authenticate()
    print(json.dumps({"status": "PASS_INDEPENDENT_ODD_FLAGS",
                      "certificates": [run_dimension(d) for d in (3, 5, 7)],
                      "all_sink_orders": [all_sink_orders(2, 1), all_sink_orders(4, 17)]}, sort_keys=True))
