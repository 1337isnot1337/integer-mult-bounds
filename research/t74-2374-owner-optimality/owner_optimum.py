#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Certificate that PR2374's owner fill is optimal for the PR2322 T74 words over all whole-helper fills.

PR2374 (jeremykothe2) claims "an exact window-free-optimal owner fill" on PR2322's words. Its published leftover
idle ranks are I = {1:21978, 3:8592, 5:2552, 32:1, 48:24560} and its claimed kappa is 0.0016971949509017704...
This script audits the optimality claim by a different method and over a larger class: the bin-pattern integer
program of PR2387/PR2360 (after PR1129).

Every legal whole-helper owner fill puts each helper role whole into one idle bin (ranks 8/16/32/48, counts
49728/33152/33152/33152). So its idle remainders come from an integer pattern-count vector x >= 0 with the bin
and width-inventory row sums. The moment is linear in x for fixed a.

Steps:
  1. Re-derive PR2374's root from the local profile plus I. The PR2322 profile is recounted in PR2402; both
     providers have {1:2335, 2:512, 3:426, 4:120, 5:38, 8:8}, with dispatch 249/417. Certify it lies within 1e-15
     of the claimed kappa.
  2. At a0 = kappa_2374 + 1e-15, take an exact rational dual (y, z) that is feasible against 800-bit LOWER
     enclosures of h(r) = (r/73)^(1-a0) for all 1163 patterns. Every integer x then satisfies
         66304 mu_x(a0) >= L_loc + D + sum_p rc_p x_p,   rc_p >= 0 exact.
     If sum rc_p x_p >= T := 66304 - L_loc - D, then mu_x(a0) >= 1, so b_x <= a0.
  3. Enumerate exactly every integer x with sum rc_p x_p < T. Only patterns with rc_p < T can appear; the LP
     basis system is solved in exact rationals. Degenerate patterns (rc ~ 0) are shown to swap only
     zero-remainder patterns, so they never change the idle multiset; they enter only through integrality,
     residues mod det(B). Each surviving x is shown to have idle multiset I exactly. Its moment at a0 is then
     certified >= 66304 directly with lower enclosures.
  Conclusion: every legal whole-helper owner fill of the PR2322 words on the unchanged T74 template has
  b <= kappa_2374 + 1e-15, and I is the only idle multiset within the dual gap. The negative control repeats the
  exclusion at kappa_2374 - 1e-12, where PR2374's own fill must survive.

Prepared with substantial AI assistance (Claude Code, Anthropic); Apache-2.0.  Credits in README.md.
Usage: python3 -I -B owner_optimum.py [--out]
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
import sys
import time
from collections import Counter
from fractions import Fraction

if not __debug__:
    sys.stdout.write('FAIL_T74_2374_OWNER_OPTIMUM refusing to run under python -O\n')
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = {  # byte copies of PR2387 (this author), as vendored and pinned in PR2402
    'vendor/pr2387/ceiling_lp.py': ('48362358660f74e0e235865df3e172494c191212',
                                    '63e2d35b07342508680e20f4b60c4da888acf4c771cd9b10400c21490f1491be'),
    'vendor/pr2387/vendor/iter3/price_check.py': ('708753e7703077a8ce4311293f02e42afb801934',
                                                  '19fcfb9f4d766959c599223090142edb03998229459cff1266960ca6b7ed1e0f'),
}
KAPPA_2374 = Fraction('0.001697194950901770426594081877309541199782925447437522970580')  # PR2374 body, 58 digits
IDLE_2374 = {1: 21978, 3: 8592, 5: 2552, 32: 1, 48: 24560}                                  # PR2374 body
EPS = Fraction(1, 10 ** 15)


class Fail(Exception):
    pass


def need(cond, what):
    if not cond:
        raise Fail(what)


def load_lp():
    for rel, (blob, sha) in VENDOR.items():
        data = open(os.path.join(HERE, rel), 'rb').read()
        need(hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() == blob and
             hashlib.sha256(data).hexdigest() == sha, 'vendored pin ' + rel)
    spec = importlib.util.spec_from_file_location('pr2387_ceiling_lp', os.path.join(HERE, 'vendor/pr2387/ceiling_lp.py'))
    lp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lp)
    return lp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', action='store_true')
    args = ap.parse_args()
    t0 = time.time()
    C = load_lp()
    P = C.P
    case = 'pr2322_control'
    W = C.W_LIVE
    loc = C.local_counts(case)
    need(sum(r * n for r, n in IDLE_2374.items()) + sum(r * n for r, n in loc.items()) == 73 * W - 23680,
         'PR2374 idle multiset + local profile = rank mass 73 W - deficit')

    def h_up(r, a):
        if r == 0:
            return Fraction(0)
        ll, lu = P.log_enclosure(C.M, r)
        el, eu = P.exp_enclosure((a.numerator * ll) // a.denominator, P.cdiv(a.numerator * lu, a.denominator))
        return Fraction(r * eu, C.M * P.ONE)

    def wmu_idle(idle, a, upper):
        f = h_up if upper else C.h_lower
        return sum(n * f(r, a) for r, n in loc.items()) + sum(n * f(r, a) for r, n in idle.items())

    # ---- 1. PR2374's root is within 1e-15 of its claimed kappa -------------------------------------------------
    hi_a, lo_a = KAPPA_2374 + EPS, KAPPA_2374 - EPS
    need(wmu_idle(IDLE_2374, hi_a, False) > W and wmu_idle(IDLE_2374, lo_a, True) < W,
         'PR2374 idle multiset root is not within 1e-15 of its claimed kappa')
    out = dict(object='PR2374 owner fill on the PR2322 T74 words: optimality over all whole-helper fills',
               pr2374_root_bracket=[str(lo_a), str(hi_a)])
    print('1. local profile + PR2374 idle multiset: root certified in kappa_2374 +- 1e-15')

    def exclusion(a0, label):
        """Return (T, survivors) for the exact dual at a0."""
        _mu, sol, du = C.lp_mu_float(case, float(a0))
        y = {R: Fraction(du[i]) for i, R in enumerate(C.NB)}
        z = {w: Fraction(du[len(C.NB) + i]) for i, w in enumerate(C.WID)}
        L = {r: C.h_lower(r, a0) for r in range(0, 49)}
        worst = {R: Fraction(0) for R in C.NB}
        for R, p in C.COLS:
            s = L[R - sum(p)] - y[R] - sum(z[w] for w in p)
            worst[R] = min(worst[R], s)
        y = {R: y[R] + worst[R] for R in C.NB}
        rc = [L[R - sum(p)] - y[R] - sum(z[w] for w in p) for R, p in C.COLS]
        need(min(rc) >= 0, 'exact dual feasibility')
        rhs = C.rhs_of(case)
        D = sum(C.NB[R] * y[R] for R in C.NB) + sum(rhs[len(C.NB) + i] * z[w] for i, w in enumerate(C.WID))
        Lloc = sum(n * C.h_lower(r, a0) for r, n in loc.items())
        T = W - Lloc - D
        basis = sorted(j for j, x in sol.items() if x > 1e-9)
        need(len(basis) == len(C.NB) + len(C.WID), 'LP basis size')
        cand = [j for j in range(len(C.COLS)) if rc[j] < T and j not in basis]
        need(all(rc[j] < T for j in basis), 'basic columns inside the budget')
        rows = len(C.NB) + len(C.WID)

        def col(j):
            R, p = C.COLS[j]
            return [Fraction(1 if R == RR else 0) for RR in C.NB] + [Fraction(p.count(w)) for w in C.WID]

        Bm = [[col(j)[i] for j in basis] for i in range(rows)]

        def solve(b):
            A = [Bm[i][:] + [Fraction(b[i])] for i in range(rows)]
            for c in range(rows):
                piv = next(r for r in range(c, rows) if A[r][c] != 0)
                A[c], A[piv] = A[piv], A[c]
                pv = A[c][c]
                A[c] = [v / pv for v in A[c]]
                for r in range(rows):
                    if r != c and A[r][c] != 0:
                        f = A[r][c]
                        A[r] = [u - f * v for u, v in zip(A[r], A[c])]
            return [A[i][rows] for i in range(rows)]

        # degenerate columns: rc tiny; check they only exchange zero-remainder patterns (idle multiset invariant)
        degen = [j for j in cand if rc[j] < T / 10 ** 6]
        heavy = [j for j in cand if j not in degen]
        for j in degen:
            lam = solve(col(j))
            need(C.COLS[j][0] - sum(C.COLS[j][1]) == 0 and
                 all(l == 0 or C.COLS[b][0] - sum(C.COLS[b][1]) == 0 for l, b in zip(lam, basis)),
                 'degenerate column %s changes the idle multiset' % (C.COLS[j],))
        # Completeness of the degenerate sweep: if every degenerate column has an integral basis representation,
        # integrality of x_B does not depend on its count, and a feasible x with positive degenerate counts maps
        # to the count-0 representative, which has the same idle multiset and sum rc, provided that representative
        # is nonnegative.  Nonnegativity at count 0 is asserted below for every heavy combination.
        lam_integral = all(l.denominator == 1 for j in degen for l in solve(col(j)))
        det_den = 1
        for j in degen:
            for l in solve(col(j)):
                det_den = det_den * l.denominator // __import__('math').gcd(det_den, l.denominator)
        xb0 = solve(rhs)
        for v in xb0:
            det_den = det_den * v.denominator // __import__('math').gcd(det_den, v.denominator)
        maxc = {j: int(T // rc[j]) for j in heavy}
        survivors = []
        for counts in itertools.product(*[range(maxc[j] + 1) for j in heavy]):
            s = sum(c * rc[j] for c, j in zip(counts, heavy))
            if s >= T:
                continue
            if lam_integral:
                b0 = list(rhs)
                for c, j in zip(counts, heavy):
                    b0 = [bi - c * v for bi, v in zip(b0, col(j))]
                need(all(v >= 0 for v in solve(b0)), 'count-0 representative negative for heavy combination %s' % (counts,))
            for kz in itertools.product(range(det_den), repeat=len(degen)):
                b = list(rhs)
                for c, j in list(zip(counts, heavy)) + list(zip(kz, degen)):
                    cj = col(j)
                    b = [bi - c * v for bi, v in zip(b, cj)]
                xb = solve(b)
                if all(v.denominator == 1 and v >= 0 for v in xb):
                    idle = Counter()
                    for v, j in list(zip(xb, basis)) + list(zip(counts, heavy)) + list(zip(kz, degen)):
                        R, p = C.COLS[j]
                        if v and R - sum(p):
                            idle[R - sum(p)] += int(v)
                    survivors.append(dict(heavy={str(C.COLS[j]): c for c, j in zip(counts, heavy) if c},
                                          degenerate_residues=list(kz), sum_rc=float(s), idle=dict(sorted(idle.items()))))
        info = dict(a0=str(a0), T=float(T), dual_repair={str(R): float(worst[R]) for R in C.NB},
                    basis=[str(C.COLS[j]) for j in basis], degenerate=[str(C.COLS[j]) for j in degen],
                    heavy={str(C.COLS[j]): dict(rc=float(rc[j]), max_count=maxc[j]) for j in heavy},
                    det_lcm=det_den, degenerate_representation_integral=lam_integral, survivors=len(survivors),
                    distinct_heavy_parts=len({json.dumps(s['heavy'], sort_keys=True) for s in survivors}),
                    survivor_idle_multisets=sorted({json.dumps(s['idle'], sort_keys=True) for s in survivors}))
        print('%s: a0 = %s; budget T = %.4e; basis %d, degenerate %d, heavy %d candidate patterns; integer survivors %d'
              % (label, ('kappa_2374 + 1e-15' if a0 > KAPPA_2374 else 'kappa_2374 - 1e-12'), float(T), len(basis),
                 len(degen), len(heavy), len(survivors)))
        return T, survivors, info

    # ---- 2/3. exclusion at a0 = kappa_2374 + 1e-15 ------------------------------------------------------------------
    a0 = KAPPA_2374 + EPS
    T, surv, info = exclusion(a0, '2. exclusion')
    want = {str(k): v for k, v in sorted(IDLE_2374.items())}
    for s in surv:
        need({str(k): v for k, v in s['idle'].items()} == want, 'a survivor with a different idle multiset: %s' % s)
    need(wmu_idle(IDLE_2374, a0, False) >= W, 'the only surviving idle multiset has mu(a0) >= 1')
    out['exclusion'] = info
    print('3. every integer pattern solution inside the budget has PR2374\'s idle multiset, whose moment at a0 is '
          'certified >= 66304; hence every legal whole-helper fill has b <= kappa_2374 + 1e-15')

    # ---- negative control -----------------------------------------------------------------------------------------
    a1 = KAPPA_2374 - Fraction(1, 10 ** 12)
    T1, surv1, info1 = exclusion(a1, 'control')
    need(any({str(k): v for k, v in s['idle'].items()} == want for s in surv1) and wmu_idle(IDLE_2374, a1, True) < W,
         'negative control: below its root PR2374\'s own fill must survive the exclusion')
    norm = lambda d: json.dumps({str(k): v for k, v in d.items()}, sort_keys=True)
    others = sorted({norm(s['idle']) for s in surv1} - {norm(want)})
    need(not others, 'a different idle multiset survives at kappa_2374 - 1e-12: %s' % others)
    out['negative_control'] = dict(a=str(a1), survivors=len(surv1), pr2374_fill_survives=True,
                                   survivor_idle_multisets=info1['survivor_idle_multisets'])
    print('   control: %d survivors at kappa_2374 - 1e-12 (degenerate copies of %d heavy part(s)), all with PR2374\'s '
          'idle multiset (uniqueness within 1e-12)' % (len(surv1), info1['distinct_heavy_parts']))
    out['conclusion'] = ('Every legal whole-helper owner fill of the PR2322 words on the unchanged T74 template has '
                         'b <= kappa_2374 + 1e-15; within the exact dual budget the only feasible idle multiset is '
                         'PR2374\'s {1:21978,3:8592,5:2552,32:1,48:24560}.')
    out['scope'] = ('Pattern relaxation of all whole-helper fills (windows, families and ports dropped), so the bound '
                    'covers every legal fill; realization of PR2374\'s fill is PR2374\'s own check, not re-run here.')
    out['python'] = sys.version.split()[0]
    if args.out:
        with open(os.path.join(HERE, 'owner_optimum.receipt.json'), 'w') as f:
            f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    print('runtime %.1fs' % (time.time() - t0))
    print('PASS_T74_2374_OWNER_OPTIMUM survivors_above=%d bound=kappa_2374+1e-15 idle_multisets_within_1e-12=1 no_new_kappa'
          % len(surv))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Fail as e:
        sys.stdout.write('FAIL_T74_2374_OWNER_OPTIMUM %s\n' % e)
        sys.exit(1)
