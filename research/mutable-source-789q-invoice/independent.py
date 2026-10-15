#!/usr/bin/env python3
"""Independent column-image replay of the 7Q champion and tariff arithmetic.

Does not import model.py or verify.py. Wentao Li + AI, Apache-2.0.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAMPION = (0, 1, 2, 6, 12, 24, 16, 0)


def fail(message):
    raise SystemExit(f"FAIL_INDEPENDENT: {message}")


def invoice(q, r, x):
    # Same abstract complete-call fixture as PR1898: (b,a,x)=(38,2,2).
    leaves = 28 * q + r
    nodes = 9 * q
    dispatch = q + r + x
    return leaves + nodes + x + dispatch


def even_R(slots):
    n = len(slots)
    best = [99] * 32
    for bits in range(1 << n):
        if bits.bit_count() % 2:
            continue
        value = 0
        for i in range(n):
            if bits >> i & 1:
                value ^= slots[i]
        size = bits.bit_count()
        if size < best[value]:
            best[value] = size
    if any(best[mask] >= 99 for mask in range(1, 32)):
        return None
    return sum(best[1:])


def path_x(closed):
    total = 0
    for a, b in zip(closed, closed[1:]):
        delta = a ^ b
        if delta == 0:
            fail("zero edge")
        total += 2 * (delta.bit_count() - 1)
    return total


def replay(closed):
    if len(closed) < 2 or closed[0] != 0 or closed[-1] != 0:
        fail("path must be closed at 0")
    slots = closed[:-1]
    reads = {}
    n = len(slots)
    for mask in range(1, 32):
        found = None
        for size in range(2, n + 1, 2):
            for subset in combinations(range(n), size):
                value = 0
                for i in subset:
                    value ^= slots[i]
                if value == mask:
                    found = subset
                    break
            if found is not None:
                break
        if found is None:
            fail(f"mask {mask} uncovered")
        reads[mask] = found

    matrix = [[1 if i == j else 0 for j in range(5)] for i in range(5)]
    z = [0] * 5
    outputs = {m: [0] * 5 for m in range(1, 32)}

    def apply_X(s, t):
        for j in range(5):
            matrix[t][j] ^= matrix[s][j]

    for step in range(len(closed) - 1):
        for mask, subset in reads.items():
            if step in subset:
                for j in range(5):
                    outputs[mask][j] ^= z[j]
        delta = closed[step] ^ closed[step + 1]
        target = (delta & -delta).bit_length() - 1
        donors = [j for j in range(5) if j != target and delta >> j & 1]
        for j in donors:
            apply_X(j, target)
        for j in range(5):
            z[j] ^= matrix[target][j]
        if z != [(closed[step + 1] >> j) & 1 for j in range(5)]:
            fail(f"connector drift at step {step}: {z} vs {closed[step + 1]}")
        for j in reversed(donors):
            apply_X(j, target)

    if z != [0] * 5:
        fail("connector not restored")
    identity = [[1 if i == j else 0 for j in range(5)] for i in range(5)]
    if matrix != identity:
        fail("sources not restored")
    for mask in range(1, 32):
        want = [(mask >> j) & 1 for j in range(5)]
        if outputs[mask] != want:
            fail(f"bad output mask {mask}: {outputs[mask]} != {want}")
    r = even_R(slots)
    if r is None:
        fail("even_R failed")
    return r, path_x(closed)


def main():
    cert = json.loads((HERE / "CERTIFICATE.json").read_text())
    r, x = replay(CHAMPION)
    if not (r == 82 and x == 6):
        fail(f"champion R/X {r}/{x}")
    if invoice(7, r, x) != 442:
        fail("champion tariff")
    if invoice(6, 96, 8) != 436:
        fail("6Q tariff")
    if invoice(10, 62, 4) != 512:
        fail("10Q tariff")
    if invoice(8, 74, 0) != 452:
        fail("8Q floor")
    if invoice(9, 62, 0) != 466:
        fail("9Q floor")
    if cert["Q7"]["champion_invoice"]["tariff"] != 442:
        fail("cert Q7")
    if cert["Q8"]["tariff_lower_bound_X_ge_0"] != 452:
        fail("cert Q8")
    if cert["Q9"]["tariff_lower_bound"] != 466:
        fail("cert Q9")
    try:
        replay((0, 1, 2, 6, 12, 24, 16))
        fail("unclosed path should fail")
    except SystemExit as exc:
        if "FAIL_INDEPENDENT" not in str(exc):
            raise
    if invoice(7, 82, 4) == 442:
        fail("undercount must not match champion")
    print("PASS_INDEPENDENT_789Q_INVOICE", "champion=442 floors=452,466 controls=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
