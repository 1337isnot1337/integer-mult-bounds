#!/usr/bin/env python3
"""Three short rows and unit coefficients (#4600 open question 2, petalas), exact for m <= 13.

Model: #4280's row model as restated in #4600 (profiles lambda, rho, beta with m nonincreasing entries in [0, m];
correct iff sum L = sum rho = sum beta = sum rho L = sum B(L) = 0 and sum rho B(L) = -c (mod m)). #4600 proves that
unit c needs at least three short rows and asks whether three suffice for every unit when m >= 6.

This verifier enumerates the model exactly (every nonincreasing rho and beta, every lambda with exactly three short
rows L1 >= L2 >= L3, L1 + L2 + L3 = 0 mod m, preceded by f full rows) and finds, for each m <= 13:
  * m <= 5: no nonzero coefficient at all is realized with three short rows (so no unit);
  * 6 <= m <= 13: every unit is realized with exactly three short rows.
So the answer to #4600's open question 2 is yes for 6 <= m <= 13, and the threshold m >= 6 is sharp.
Ryanson Jonathan with Claude Code (Claude Opus 5.5) assistance. Apache-2.0.
"""
from math import gcd
import json
import sys


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def profiles(m):
    out = []

    def rec(prefix, top):
        if len(prefix) == m:
            out.append(tuple(prefix))
            return
        for v in range(top, -1, -1):
            prefix.append(v)
            rec(prefix, v)
            prefix.pop()
    rec([], m)
    return out


def three_row_coefficients(m):
    balanced = [p for p in profiles(m) if sum(p) % m == 0]
    rho = {f: {(p[f] % m, p[f + 1] % m, p[f + 2] % m) for p in balanced} for f in range(m - 2)}
    prefixes = []
    for p in balanced:
        pre = [0]
        for v in p:
            pre.append(pre[-1] + v)
        prefixes.append([x % m for x in pre])
    found = set()
    for l1 in range(1, m):
        for l2 in range(1, l1 + 1):
            for l3 in range(1, l2 + 1):
                if (l1 + l2 + l3) % m:
                    continue
                bs = {(pr[l1], pr[l2], pr[l3]) for pr in prefixes if (pr[l1] + pr[l2] + pr[l3]) % m == 0}
                for f in range(m - 2):
                    for a, b, c in rho[f]:
                        if (a * l1 + b * l2 + c * l3) % m == 0:
                            for x, y, z in bs:
                                v = -(a * x + b * y + c * z) % m
                                if v:
                                    found.add(v)
    return found


def main():
    table = {}
    for m in range(2, 14):
        found = three_row_coefficients(m)
        units = {c for c in range(1, m) if gcd(c, m) == 1}
        if m <= 5:
            need(not found, "m <= 5: nothing realized with three short rows")
        else:
            need(units <= found, "m = %d: every unit realized with three short rows" % m)
        table[m] = sorted(found)
    print(json.dumps({"status": "PASS_THREE_SHORT_ROW_UNITS", "realized_by_m": table, "new_kappa_claimed": False},
                     indent=1))


if __name__ == "__main__":
    sys.exit(main())
