#!/usr/bin/env python3
"""Independent arithmetic check of #4470 (conditional kappa 0.00302015, joint helper boundaries).

With its own certified interval logarithms (the helpers of research/p17-b480-check, copied here), this checks the
numbers printed in #4470 (head b9a13c16): the p16 invoice totals (64,620 paid jobs, 10,928 productive fields, rank
masses 239,886 / 239,134, surplus 752); the local profile change against #4447 (paid {1:2254,2:514,3:444,4:103,5:40,8:8}
-> {1:2237,2:388,3:494,4:147,5:36,8:8}: 53 fewer jobs; helpers {4:26,5:2,7:29,8:42,9:309} -> {4:28,7:7,8:47,9:326};
both masses +37) and its surplus-gain polynomial (vanishes at t = 1, positive on a grid of (0, 1)); the raw root
bracket (0.0030201659770, 0.0030201659771); and the higher-moment tails alpha, gamma_u, delta at #4470's tested
saving 604031/200000000, u = 1/5, cutoff 20, floor 21, against its limits 1 - 1e-9, 97/100, 97/100.
Invoices are as printed in #4470; nothing is imported from it. Not checked: the logarithmic compiler (H = 6.42e13)
and the outer rows. Ryanson Jonathan with Claude Code (Claude Opus 5.5) assistance. Apache-2.0.
"""
from fractions import Fraction as Q
import json
import sys

GRID = Q(1, 10**50)


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def down(x):
    return (x / GRID).__floor__() * GRID


def up(x):
    return (x / GRID).__ceil__() * GRID


def ln_bounds(n):
    """certified ln n for integer n >= 1 (reduction to [1, 2) and the atanh series)"""
    if n == 1:
        return Q(0), Q(0)
    k = n.bit_length() - 1
    y = Q(n, 2 ** k)
    out = [Q(0), Q(0)]
    for part, scale in ((y, 1), (Q(2), k)):
        if part == 1 or scale == 0:
            continue
        u = (part - 1) / (part + 1)
        s, term, j = Q(0), u, 0
        while True:
            s += term / (2 * j + 1)
            j += 1
            term *= u * u
            tail = term / (2 * j + 1) / (1 - u * u)
            if tail < GRID:
                break
        out[0] += scale * down(2 * s)
        out[1] += scale * up(2 * (s + tail))
    return out[0], out[1]


def exp_bounds(x_lo, x_hi):
    """certified exp on a small interval (|x| < 1)"""
    def series(x):
        s, term = Q(0), Q(1)
        for i in range(70):
            s += term
            term = term * x / (i + 1)
        return s, abs(term) * 2
    a, ea = series(x_lo)
    b, eb = series(x_hi)
    return down(a - ea), up(b + eb)


LN = {}


def ln(n):
    if n not in LN:
        LN[n] = ln_bounds(n)
    return LN[n]


def moment(hist, C):
    """bounds of sum count * k^(1-C)"""
    lo = hi = Q(0)
    for k, w in hist.items():
        e = exp_bounds(-C * ln(k)[1], -C * ln(k)[0])
        lo, hi = lo + w * k * e[0], hi + w * k * e[1]
    return lo, hi


def pow_upper(x, v):
    """certified upper bound of x^v for 0 < x < 1 rational: exp(v ln x) with ln x <= -(1-x) - (1-x)^2/2"""
    y = 1 - x
    lnx_hi = -(y + y * y / 2)
    return lnx_hi * v



# #4440's query-thinned units (strictification only; its compiler uses the older power majorant)
T4440C = {153: 224, 17: 448, 25: 448, 33: 448, 41: 448, 49: 448, 5: 532, 57: 448, 6: 342, 65: 448, 7: 1064, 73: 448, 8: 1767, 9: 4047}
P4440C = {1: 49045, 16: 448, 2: 13547, 24: 448, 3: 4256, 32: 448, 4: 1938, 40: 448, 48: 448, 5: 380, 56: 448, 64: 448, 72: 448, 8: 152}
T4440B = {127: 222, 15: 444, 22: 444, 29: 444, 36: 444, 43: 444, 50: 444, 57: 444, 64: 222, 8: 7902}
P4440B = {1: 25479, 14: 444, 2: 24156, 21: 444, 28: 444, 3: 1422, 35: 444, 4: 792, 42: 444, 49: 444, 5: 1836, 56: 444, 6: 198, 63: 222, 7: 342}
EXPECT4440 = {"complex": ("0.999999952117240859760145478346", "0.967466409565147920980822933860", "0.941649713484853845388929204841"),
              "BIT": ("0.999995735238059506641600561768", "0.957429821066420278606254392111", "0.949707924144871179442776557219")}
def lnq(x):
    a, b = ln(x.numerator), ln(x.denominator)
    return a[0] - b[1], a[1] - b[0]


def powq(base, e):
    """certified base^e for integer base >= 1 and rational exponent e (|e ln base| < 1.2)"""
    l = ln(base)
    lo, hi = (e * l[0], e * l[1]) if e >= 0 else (e * l[1], e * l[0])
    return exp_bounds(lo, hi)


def mom(hist, expo):
    lo = hi = Q(0)
    for k, w in hist.items():
        e = powq(k, expo - 1)
        lo, hi = lo + w * k * e[0], hi + w * k * e[1]
    return lo, hi




P = {"1": 41946, "16": 448, "2": 6984, "24": 448, "3": 8892, "32": 448, "4": 2646, "40": 448, "48": 448, "5": 648, "56": 448, "64": 448, "72": 224, "8": 144}
T = {"145": 224, "17": 448, "25": 448, "33": 448, "4": 504, "41": 448, "49": 448, "57": 448, "65": 448, "7": 126, "73": 224, "8": 846, "9": 5868}


def main():
    Pi = {int(k): w for k, w in P.items()}
    Ti = {int(k): w for k, w in T.items()}
    need(sum(Pi.values()) == 64620 and sum(Ti.values()) == 10928, "invoice counts")
    need(sum(k * w for k, w in Ti.items()) == 239886 and sum(k * w for k, w in Pi.items()) == 239134, "rank masses, surplus 752")
    old_p, new_p = {1: 2254, 2: 514, 3: 444, 4: 103, 5: 40, 8: 8}, {1: 2237, 2: 388, 3: 494, 4: 147, 5: 36, 8: 8}
    old_h, new_h = {4: 26, 5: 2, 7: 29, 8: 42, 9: 309}, {4: 28, 7: 7, 8: 47, 9: 326}
    need(sum(old_p.values()) - sum(new_p.values()) == 53, "53 fewer paid jobs per local call")
    mass = lambda h: sum(k * w for k, w in h.items())
    need(mass(new_p) - mass(old_p) == 37 == mass(new_h) - mass(old_h), "both masses rise by 37")
    keys = set(old_p) | set(new_p) | set(old_h) | set(new_h)
    coef = {k: (new_h.get(k, 0) - old_h.get(k, 0)) - (new_p.get(k, 0) - old_p.get(k, 0)) for k in keys}
    coef = {k: c for k, c in coef.items() if c}
    need(coef == {1: 17, 2: 126, 3: -50, 4: -42, 5: 2, 7: -22, 8: 5, 9: 17}, "surplus-gain polynomial")
    need(sum(c * k for k, c in coef.items()) == 0, "gain vanishes at t = 1")
    need(min(sum(c * k ** (i / 1000) for k, c in coef.items()) for i in range(1, 1000)) > 0, "gain positive on a grid of (0,1)")
    lo, hi = Q(30201659770, 10**13), Q(30201659771, 10**13)
    tl, th = moment(Ti, lo); pl, ph = moment(Pi, lo)
    need(tl > ph, "T_t > P_t at the lower root end")
    tl, th = moment(Ti, hi); pl, ph = moment(Pi, hi)
    need(th < pl, "T_t < P_t at the upper root end")
    tested = Q(604031, 200000000)
    t = 1 - tested
    tl, th = moment(Ti, tested); pl, ph = moment(Pi, tested)
    alpha = ph / tl
    gamma = mom(Pi, t + Q(1, 5))[1] / (powq(20, Q(1, 5))[0] * tl)
    delta = Q(sum(Ti.values()) * 21) / (powq(20, tested)[0] * tl)
    need(alpha < 1 - Q(1, 10**9) and gamma < Q(97, 100) and delta < Q(97, 100), "tails within #4470's limits")
    need(abs(float(alpha) - 0.999999988558808354) < 1e-15 and abs(float(gamma) - 0.956176646497545) < 1e-12
         and abs(float(delta) - 0.958284435309221) < 1e-12, "tails match #4470's printed values")
    print(json.dumps({"status": "PASS_PR4470_ARITHMETIC_CHECK", "paid_jobs": 64620, "fields": 10928, "surplus": 752,
                      "root_bracket": ["0.0030201659770", "0.0030201659771"], "alpha_upper": f"{float(alpha):.15f}",
                      "gamma_upper": f"{float(gamma):.12f}", "delta_upper": f"{float(delta):.12f}",
                      "new_kappa_claimed": False}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
