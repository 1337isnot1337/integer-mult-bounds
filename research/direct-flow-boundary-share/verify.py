#!/usr/bin/env python3
"""Boundary-exit potential share in #4436's direct p7 flow (evidence for a conditional reduction).

Using an independent implementation of #4436's partially matched flow (the same as research/pr4436-direct-flow-check),
for every rank 121 <= N <= 3000 and a 1%-geometric grid up to 5*10^5 this computes
    beta(N) = sum over boundary exits x_e e^t / sum over sources w_s s^t,     t = 1 - 0.0026865,
and checks: every exit is at most r_max N / m (r_max = 48, m = 121), every leaf exit is at most r_max^(G+1), the
exact rank-one potential identity holds, and max beta < 0.16 (observed 0.1545). Floating-point shares are
numerical evidence for the README's conditional lemma, not a proof of a uniform bound.
Ryanson Jonathan with Claude Code (Claude Opus 5.5) assistance. Apache-2.0.
"""
import json
import sys

from fractions import Fraction as Q
from math import factorial
def multis(n_types, size):
    if n_types == 0:
        if size == 0: yield ()
        return
    for x in range(size + 1):
        for rest in multis(n_types - 1, size - x): yield (x,) + rest
def flow(N, W, P):
    ks = sorted(W); m = ks[-1]; kmin = ks[0]
    def c(a):
        v = 1
        for k, x in zip(ks, a): v *= k ** x
        return v
    def u(a):
        v = factorial(sum(a))
        for k, x in zip(ks, a): v = v // factorial(x) * W[k] ** x
        return v
    G = 0
    while kmin ** (G + 1) <= N // m: G += 1
    F = [{1: 1}]
    for d in range(1, G + 1):
        nxt = {}
        for rho, cnt in F[d - 1].items():
            for r, pr in P.items():
                if m * rho * r <= N: nxt[rho * r] = nxt.get(rho * r, 0) + cnt * pr
        F.append(nxt)
    S, X, BX = {}, {}, {}
    col = units = matched = 0
    add = lambda D, k, v: D.__setitem__(k, D.get(k, 0) + v)
    present = lambda rho, a: m * rho * c(a) <= N
    for d in range(G + 1):
        for rho, cnt in F[d].items():
            for b in multis(len(ks), G - d):
                if not present(rho, b): continue
                units += cnt * u(b); col += cnt * u(b) * rho * c(b)
                for r, pr in P.items():
                    issued = cnt * pr * u(b); rank = r * rho * c(b)
                    if d == G:
                        add(X, rank, issued); continue
                    D = sum(W[k] * u(tuple(x - (i == j) for j, x in enumerate(b)))
                            for i, k in enumerate(ks) if b[i] > 0 and present(rho * r, tuple(x - (i == j) for j, x in enumerate(b))))
                    matched += cnt * pr * D
                    if issued - cnt * pr * D:
                        add(X, rank, issued - cnt * pr * D); add(BX, rank, issued - cnt * pr * D)
    for a in multis(len(ks), G):
        if present(1, a):
            for k in ks: add(S, k * c(a), W[k] * u(a))
    for d in range(1, G + 1):
        for rho, cnt in F[d - 1].items():
            for r, pr in P.items():
                for a in multis(len(ks), G - d):
                    if not present(rho * r, a): continue
                    for i, k in enumerate(ks):
                        b = list(a); b[i] += 1
                        if not present(rho, tuple(b)):
                            add(S, rho * r * c(tuple(b)), cnt * pr * u(a) * W[k])
    return dict(G=G, S=S, X=X, BX=BX, col=col, units=units, matched=matched)


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    W = {5: 420, 6: 270, 7: 840, 8: 1395, 9: 3195, 25: 448, 41: 448, 57: 448, 121: 224}
    P = {1: 37305, 2: 10695, 3: 3360, 4: 1530, 5: 300, 8: 1464, 16: 448, 32: 448, 48: 448}
    m, rmax, surplus = 121, 48, 608
    t = 1 - 0.0026865
    Ns = sorted(set(list(range(121, 3001)) + [int(121 * 1.01 ** k) for k in range(0, 850)]))
    Ns = [n for n in Ns if n <= 500000]
    best, at = 0.0, None
    for N in Ns:
        r = flow(N, W, P)
        need(all(e * m <= rmax * N for e in r["X"]), f"N={N}: exits <= r_max N/m")
        need(all(e <= rmax ** (r["G"] + 1) or e in r["BX"] for e in r["X"]), f"N={N}: leaf exits <= r_max^(G+1)")
        need(sum(s * v for s, v in r["S"].items()) - sum(e * v for e, v in r["X"].items()) == surplus * r["col"],
             f"N={N}: potential identity")
        st = sum(v * s ** t for s, v in r["S"].items())
        bt = sum(v * e ** t for e, v in r["BX"].items())
        if bt / st > best:
            best, at = bt / st, N
    need(best < 0.16, "max boundary share below 0.16")
    print(json.dumps({"status": "PASS_DIRECT_FLOW_BOUNDARY_SHARE", "ranks_scanned": len(Ns), "max_N": Ns[-1],
                      "max_boundary_share": round(best, 6), "at_N": at, "eta_reference": 0.984,
                      "new_kappa_claimed": False}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
