#!/usr/bin/env python3
"""Independent arithmetic check of #4447 (kappa 0.00300123) and #4453 (kappa 0.00300120).

Both report the same B/480 contact patch on #4441's p17 invoice. This verifier checks, with its own certified
interval logarithms: the invoice is #4441's plus exactly 19 per-call swaps [2,2,1,3] -> [1,1,2,4]; the raw root
bracket; for each PR the higher-moment strictification (main's research/higher-moment-strictification theorem:
alpha = P_t/T_t, gamma_u = P_(t+u)/(c^u T_t), delta = B b/(c^C T_t), bound alpha^v + 2 gamma_u^v + 2 delta^v < 1)
at the PR's own (C, v, c, b, u) and stated rational limits; the polylog compiler conditions (theta, the shifted
exit condition, theta_bar^p < eta, m^(1-t) < 2^p) at ambient 153^v; and the least H with (1+H)^p < 2^((z-t)H).
Invoices and parameters are as printed in the PRs; nothing is imported from them.
Ryanson Jonathan with Claude Code (Claude Opus 5.5) assistance. Apache-2.0.
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



T = {153: 224, 17: 448, 25: 448, 33: 448, 4: 494, 41: 448, 49: 448, 5: 38, 57: 448, 65: 448, 7: 551, 73: 448, 8: 798, 9: 5871}
P = {1: 44618, 16: 448, 2: 9766, 24: 448, 3: 8436, 32: 448, 4: 1957, 40: 448, 48: 448, 5: 760, 56: 448, 64: 448, 72: 448, 8: 152}
P4441 = {1: 44599, 16: 448, 2: 9785, 24: 448, 3: 8455, 32: 448, 4: 1938, 40: 448, 48: 448, 5: 760, 56: 448, 64: 448, 72: 448, 8: 152}
CASES = {
    "4447": {"kappa": Q("0.00300123"), "C": Q(600247, 200000000), "v": 1024, "c": 20, "b": 21, "u": Q(1, 5),
             "limits": (1 - Q(1, 10**9), Q(97, 100), Q(19, 20)), "theta_bar": Q(63, 64), "p": 1000, "H": 64215200000000},
    "4453": {"kappa": Q(7503, 2500000), "C": Q(150061, 50000000), "v": 675, "c": 18, "b": 22, "u": Q(3, 25),
             "limits": (Q(999999981, 10**9), Q(491, 500), Q(391, 400)), "theta_bar": Q(15, 16), "p": 160, "H": 2299850000000},
}


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


def log2_upper_of_H1(H):
    """certified upper bound of log2(1+H)"""
    n = H + 1
    l = ln(n) if n < 2**60 else None
    return l


def ln_int(n):
    k = n.bit_length() - 1
    y = Q(n, 2 ** k)
    u = (y - 1) / (y + 1)
    s, term, j = Q(0), u, 0
    while True:
        s += term / (2 * j + 1)
        j += 1
        term *= u * u
        tail = term / (2 * j + 1) / (1 - u * u) if u else Q(0)
        if tail < Q(1, 10**40):
            break
    l2 = ln(2)
    return 2 * s + k * l2[0], 2 * (s + tail) + k * l2[1]


def main():
    from collections import Counter
    d = Counter(P4441)
    d.update({1: 19, 4: 19})
    d.subtract({2: 19, 3: 19})
    need(+d == Counter(P), "invoice = #4441 + 19 swaps [2,2,1,3] -> [1,1,2,4]")
    need(sum(T.values()) == 11560 and sum(P.values()) == 69273, "fields and calls")
    need((sum(k * w for k, w in T.items()), sum(k * w for k, w in P.items())) == (260798, 259998), "rank surplus 800")
    need(all((1 + 4 ** x) < 2 ** x + 3 ** x for x in (0.1, 0.5, 0.9)), "concavity spot checks")
    # raw root bracket
    def alpha(C):
        tl, th = mom(T, 1 - C)
        pl, ph = mom(P, 1 - C)
        return pl / th, ph / tl
    lo, hi = Q("0.0030012390168"), Q("0.0030012390174")
    need(alpha(lo)[1] < 1 < alpha(hi)[0], "root bracket (0.0030012390168, 0.0030012390174)")
    out = {"status": "PASS_PR4447_PR4453_ARITHMETIC", "new_kappa_claimed": False,
           "invoice": {"fields": 11560, "paid_calls": 69273, "rank_surplus": 800}, "root_bracket": [str(lo), str(hi)]}
    B = sum(T.values())
    for name, cs in CASES.items():
        C, v, c, b, u = cs["C"], cs["v"], cs["c"], cs["b"], cs["u"]
        t = 1 - C
        need(u >= C and t + u >= 1 and 1 < c < b < 153, f"{name}: theorem hypotheses")
        tl, th = mom(T, t)
        pl, ph = mom(P, t)
        a_hi = ph / tl
        g_num = mom(P, t + u)[1]
        cu = powq(c, u)[0]
        g_hi = g_num / (cu * tl)
        cC = powq(c, C)[0]
        d_hi = B * b / (cC * tl)
        la, lg, ld = cs["limits"]
        need(a_hi < la and g_hi < lg and d_hi < ld, f"{name}: alpha, gamma_u, delta below the stated limits")
        total = 1 / (1 + v * (1 - la)) + 2 * lg ** v + 2 * ld ** v
        need(total < 1, f"{name}: alpha^v + 2 gamma^v + 2 delta^v < 1")
        # compiler (polylog majorant): m = 153^v, r_max = c^v, k_min = b^v
        tb, p = cs["theta_bar"], cs["p"]
        A_, Bd = tb.numerator, tb.denominator
        need(c ** Bd < b ** A_, f"{name}: theta = log c / log b < theta_bar")
        need((Bd - A_) + Bd * v * ln(c)[1] / ln(2)[0] <= A_ * v * ln(153)[0] / ln(2)[1], f"{name}: 2^(b-a) r^b <= m^a")
        # eta = t * 153^(v (t-1)); need theta_bar^p < eta and m^(1-t) < 2^p (logs)
        ln_eta_lo = lnq(t)[0] - v * C * ln(153)[1]
        need(p * lnq(tb)[1] < ln_eta_lo, f"{name}: theta_bar^p < eta")
        need(v * C * ln(153)[1] < p * ln(2)[0], f"{name}: m^(1-t) < 2^p")
        dgap = (C - cs["kappa"]) / 7
        z = 1 - (cs["kappa"] + 6 * dgap)
        zt = z - t
        need(zt == dgap, f"{name}: z - t = d")
        H = cs["H"]
        def ok(Hx):
            l = ln_int(Hx + 1)
            return p * l[1] < zt * Hx * ln(2)[0]
        need(ok(H), f"{name}: (1+H)^p < 2^((z-t)H) at stated H")
        lo_h, hi_h = 1, H
        while lo_h < hi_h:
            mid = (lo_h + hi_h) // 2
            if ok(mid):
                hi_h = mid
            else:
                lo_h = mid + 1
        out[name] = {"alpha_upper": f"{float(a_hi):.15f}", "gamma_u_upper": f"{float(g_hi):.12f}",
                     "delta_upper": f"{float(d_hi):.12f}", "stated_limits": [str(x) for x in cs["limits"]],
                     "tensor_bound": f"{float(total):.10f}", "stated_H": H, "least_certified_H": lo_h}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    sys.exit(main())
