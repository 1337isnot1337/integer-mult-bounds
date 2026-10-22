#!/usr/bin/env python3
"""Which coefficients admit exactly two short rows? (#4600 open question 1, petalas)

Model (#4280 row model, as restated in #4600): a balanced depth-four word with modulus m is a triple of profiles
(lambda, rho, beta), each with m entries in [0, m] and nonincreasing (lambda is the partition of row lengths L_q).
It is correct exactly when
    sum L_q = sum rho_q = sum beta_p = 0,  sum rho_q L_q = sum B(L_q) = 0,  sum rho_q B(L_q) = -c   (mod m),
with B(L) = beta_1 + ... + beta_L. A short row has 0 < L_q < m. #4600 proves: two short rows imply m | cL for each
short length L (so units need three), and gives the family m = 8t, c = 4t.

New here:
  (1) Theorem (written proof). If exactly two short rows realize c != 0 then gcd(c, m) >= 3.
      Proof: by #4600, m/g | L_1, L_2 with g = gcd(c, m) and L_1 + L_2 = m. If g = 2, L_1 = L_2 = m/2. The
      congruences become (r_1 - r_2) m/2 = 0, 2 B(m/2) = 0 and c = -(r_1 + r_2) B(m/2) (mod m). The first makes
      r_1 - r_2, hence r_1 + r_2, even; the second gives B(m/2) in {0, m/2}; so c = 0 (mod m). Contradiction.
  (2) Exact exhaustive enumeration of the profile model for every m <= 12 (all nonincreasing rho and beta, all
      placements of the two short rows): the achievable nonzero c are exactly {c : gcd(c, m) >= 3}. So for m <= 12
      the strengthened condition is also sufficient, while the annihilator condition alone is not (m = 4, 6, 8, 10, 12
      have annihilator-allowed c with gcd 2 that no two-short-row word realizes).
  (3) #4600's family m = 8t, c = 4t: profiles valid and all congruences hold, with exactly two short rows, t = 1..64.
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


def two_row_coefficients(m):
    """All nonzero c realized with exactly two short rows, by exhaustive enumeration of rho and beta."""
    balanced = [p for p in profiles(m) if sum(p) % m == 0]
    rho_pairs = {f: {(p[f] % m, p[f + 1] % m) for p in balanced} for f in range(m - 1)}
    b_pairs = {}
    for p in balanced:
        pre = [0]
        for v in p:
            pre.append(pre[-1] + v)
        for la in range((m + 1) // 2, m):
            b_pairs.setdefault(la, set()).add((pre[la] % m, pre[m - la] % m))
    found = set()
    for f in range(m - 1):              # lambda = (m^f, L_a, L_b, 0, ...) with L_a + L_b = m
        for la in range((m + 1) // 2, m):
            lb = m - la
            for ra, rb in rho_pairs[f]:
                if (ra * la + rb * lb) % m:
                    continue
                for x, y in b_pairs[la]:
                    if (x + y) % m == 0:
                        c = -(ra * x + rb * y) % m
                        if c:
                            need(c * la % m == 0 and c * lb % m == 0, "#4600 annihilator condition")
                            found.add(c)
    return found


def family_check(t):
    m = 8 * t
    lam = [m, 6 * t, 2 * t] + [0] * (m - 3)
    rho = [m - 4, 4] + [0] * (m - 2)
    beta = [5] * t + [4] * t + [2] * (2 * t) + [1] * (3 * t) + [0] * t
    for p in (lam, rho, beta):
        need(len(p) == m and all(0 <= v <= m for v in p) and all(a >= b for a, b in zip(p, p[1:])), "profile")
    pre = [0]
    for v in beta:
        pre.append(pre[-1] + v)
    big_b = lambda length: pre[length]
    need(sum(lam) % m == sum(rho) % m == sum(beta) % m == 0, "sums")
    need(sum(r * l for r, l in zip(rho, lam)) % m == 0 and sum(big_b(l) for l in lam) % m == 0, "weighted sums")
    c = -sum(r * big_b(l) for r, l in zip(rho, lam)) % m
    need(c == 4 * t and sum(0 < l < m for l in lam) == 2, "c = 4t with exactly two short rows")


def main():
    table = {}
    for m in range(2, 13):
        found = two_row_coefficients(m)
        strengthened = {c for c in range(1, m) if gcd(c, m) >= 3}
        annihilator = {c for c in range(1, m) if any(c * l % m == 0 for l in range(1, m))}
        need(found == strengthened, "m = %d: achievable set is exactly gcd(c, m) >= 3" % m)
        need(found <= annihilator, "annihilator condition is necessary")
        table[m] = {"achievable": sorted(found), "annihilator_only": sorted(annihilator - found)}
    need(any(v["annihilator_only"] for v in table.values()), "annihilator condition alone is not sufficient")
    for t in range(1, 65):
        family_check(t)
    print(json.dumps({"status": "PASS_TWO_SHORT_ROW_COEFFICIENTS", "table": table, "family_t_checked": 64,
                      "new_kappa_claimed": False}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
