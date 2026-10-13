#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact relief thresholds for the coverage law behind the selected complex local word.

Model (all inputs explicit; semantics follow PR1012's coverage identity and the
moment model of https://github.com/CrocSwap/integer-mult-bounds/pull/1240, whose
arithmetic is NOT imported here):

  * width m = 73; a call has w = families / stages live data families (selected
    line: 896 families over 9 stages);
  * coverage identity: paid rank mass + idle mass = (m - unpaid) * w + centre,
    i.e. each live family keeps `unpaid` unpaid coordinates (1 on the selected
    line) and each call pays a centre path of `centre` (64 on the selected line);
  * the local word fixes its paid child profile per call (the selected #1094 word
    is {1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}, mass 5586, recorded at
    research/gauge44-slots-t16/README.md and re-priced by PR #1240);
  * all remaining mass is idle/remainder children of rank at most R, where the
    outer halving guard m^2 > 2 R^2 gives R = 51 at m = 73.

For a >= 0 a child of rank r costs (r/m)^(1-a); with idle mass M at fixed ranks
<= R the cheapest idle histogram puts all of M into (possibly fractional) rank-R
children, so the optimistic relaxation moment per call is

    relax(a) = [ sum_local n_r (r/m)^(1-a) + (M/R) (R/m)^(1-a) ] / w .

relax is increasing in a; the packing ceiling a* solves relax(a*) = 1.  A failing
relaxation (relax(a_t) > 1 at target a_t) falsifies every construction with those
interface parameters; a passing one is optimistic only (no realizability claim).

This package computes certified brackets for a* and for the exact interface
thresholds that put a* above two targets: a = 1/99 (headline planning target)
and a = kappa_bit/(1 - kappa_bit) (the retained-transfer unbinding target where
the complex side would stop binding over the pinned bit supplier).

Exact rational intervals: ln via atanh chains, exp by Taylor series with a
geometric tail bound, outward rounding to 2^-PREC.  Standard library only.
Contributor: Navinor, with help from opencode.  Apache-2.0.
"""
import argparse
import json
from fractions import Fraction as Q
from functools import lru_cache
from math import isqrt

PREC = 256

M = 73
STAGES = 9
FAMILIES0 = 896
CENTRE0 = 64
UNPAID0 = 1
WORD = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}  # selected #1094 local word per call
WORD_MASS = sum(r * n for r, n in WORD.items())  # 5586
# PR #1240 reports the incumbent ceiling as a < 0.001690054109089 (positive control).
REF_CEILING = Q(1690054109089, 10 ** 15)
# scripts/research_baseline.py at the base commit: bit_saving = 1733427039589844234749/10^24.
KAPPA_BIT = Q(1733427039589844234749, 10 ** 24)
A_T1 = Q(1, 99)  # headline target
A_T2 = KAPPA_BIT / (1 - KAPPA_BIT)  # unbinding target, retained kappa = a/(1+a)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def down(x):
    return Q((x.numerator << PREC) // x.denominator, 1 << PREC)


def up(x):
    return -down(-x)


@lru_cache(None)
def atanh(t):
    """[lo, hi] enclosure of atanh(t) for rational 0 < t <= 1/3."""
    require(0 < t <= Q(1, 3), 'atanh range')
    s, p, k = Q(0), t, 0
    while True:
        term = p / (2 * k + 1)
        s += term
        p *= t * t
        k += 1
        tail = p / ((2 * k + 1) * (1 - t * t))
        if tail < Q(1, 1 << (PREC + 8)):
            return down(s), up(s + tail)


@lru_cache(None)
def ln_int(k):
    """[lo, hi] enclosure of ln k for integer k >= 1: ln k = ln(k-1) + 2 atanh(1/(2k-1))."""
    require(isinstance(k, int) and k >= 1, 'ln domain')
    if k == 1:
        return Q(0), Q(0)
    lo, hi = ln_int(k - 1)
    a, b = atanh(Q(1, 2 * k - 1))
    return down(lo + 2 * a), up(hi + 2 * b)


def exp_pair(lo, hi):
    """[lo', hi'] enclosure of exp([lo, hi]) for 0 <= lo <= hi <= 1/2."""
    require(0 <= lo <= hi <= Q(1, 2), 'exp range')

    def series(y, upper):
        s, t, k = Q(1), Q(1), 0
        while True:
            k += 1
            t = t * y / k
            s += t
            if t * y < Q(1, 1 << (PREC + 8)):
                return up(s + 2 * t * y / (k + 1)) if upper else down(s)

    return series(lo, False), series(hi, True)


def child_cost(r, a):
    """[lo, hi] enclosure of (r/m)^(1-a) = (r/m) * exp(a * ln(m/r)), 0 <= a <= 1/20."""
    require(0 <= a <= Q(1, 20) and 0 < r < M, 'child cost domain')
    lm, um = ln_int(M)
    lr, ur = ln_int(r)
    e = exp_pair(a * max(Q(0), lm - ur), a * (um - lr))
    return down(Q(r, M) * e[0]), up(Q(r, M) * e[1])


def max_idle_rank(m):
    """Largest R with m^2 > 2 R^2 (outer halving guard)."""
    r = isqrt((m * m - 1) // 2)
    while 2 * (r + 1) ** 2 < m * m:
        r += 1
    while 2 * r * r >= m * m:
        r -= 1
    return r


R = max_idle_rank(M)


def model(local, unpaid=UNPAID0, centre=CENTRE0, families=FAMILIES0, stages=STAGES, rank_cap=R):
    """Per-call coverage quantities; Fraction counts allowed."""
    require(2 * rank_cap * rank_cap < M * M, 'idle rank cap violates the halving guard')
    require(1 <= unpaid < M, 'unpaid coordinates per family')
    require(0 <= centre, 'centre charge')
    require(stages >= 1 and families >= 1, 'template counts')
    require(all(0 < r < M for r in local) and all(n >= 0 for n in local.values()), 'local profile')
    w = Q(families) / stages
    require(unpaid * w > centre, 'coverage deficit is not positive')
    total = (M - unpaid) * w + centre
    local_mass = sum(r * Q(n) for r, n in local.items())
    idle = total - local_mass
    require(idle >= 0, 'local word pays more mass than the coverage law allows')
    return dict(w=w, total=total, local_mass=local_mass, idle=idle, deficit=unpaid * w - centre)


def relax(local, a, unpaid=UNPAID0, centre=CENTRE0, families=FAMILIES0, stages=STAGES, rank_cap=R):
    """[lo, hi] enclosure of the per-call relaxation moment at saving a."""
    q = model(local, unpaid, centre, families, stages, rank_cap)
    lo = hi = Q(0)
    for r, n in local.items():
        c = child_cost(r, a)
        lo, hi = lo + Q(n) * c[0], hi + Q(n) * c[1]
    c = child_cost(rank_cap, a)
    k = q['idle'] / rank_cap
    lo, hi = lo + k * c[0], hi + k * c[1]
    return down(lo / q['w']), up(hi / q['w'])


def moment_sign(local, a, **kw):
    """-1: moment below one at a; +1: above one.  Raises if the enclosure straddles."""
    lo, hi = relax(local, a, **kw)
    if hi < 1:
        return -1
    if lo > 1:
        return 1
    raise ValueError('moment enclosure straddles one')


def ceiling(local, grid=Q(1, 10 ** 18), **kw):
    """Bracket [a_lo, a_hi] of the packing ceiling a*: relax(a_lo) < 1 < relax(a_hi)."""
    lo, hi = Q(0), Q(1, 20)
    require(moment_sign(local, hi, **kw) > 0, 'search window too small')
    require(moment_sign(local, lo, **kw) < 0, 'relaxation has no positive saving')
    while hi - lo > grid:
        mid = (lo + hi) / 2
        if moment_sign(local, down(mid), **kw) < 0:
            lo = down(mid)
        else:
            hi = up(mid)
    return lo, hi


def target_met(local, a_t, **kw):
    """True iff the relaxation admits saving >= a_t (moment below one at a_t)."""
    return moment_sign(local, a_t, **kw) < 0


def bisect_param(met, lo, hi, grid):
    """Certified bracket [p_lo, p_hi] with met increasing in p: not met(p_lo), met(p_hi)."""
    lo, hi = Q(lo), Q(hi)
    require(met(hi) and not met(lo), 'parameter bracket does not straddle the threshold')
    while hi - lo > grid:
        mid = (lo + hi) / 2
        if met(mid):
            hi = mid
        else:
            lo = mid
    return lo, hi


def de_diagnostic(local, unpaid=UNPAID0, centre=CENTRE0, families=FAMILIES0, stages=STAGES):
    """D = m*w - total mass (exact) and E = sum n_r r ln(m/r) over local + rank-R idle.

    First-order diagnostic: a* <= D/E (strict for a* > 0), from (r/m)^(1-a) >=
    (r/m)(1 + a ln(m/r)) and relax(a*) = 1.
    """
    q = model(local, unpaid, centre, families, stages)
    d = M * q['w'] - q['total']
    lo = hi = Q(0)
    counts = dict(local)
    counts[R] = counts.get(R, Q(0)) + q['idle'] / R
    for r, n in counts.items():
        lm, um = ln_int(M)
        lr, ur = ln_int(r)
        lo += Q(n) * r * down(lm - ur)
        hi += Q(n) * r * up(um - lr)
    return d, lo, hi


class Report:
    def __init__(self):
        self.lines = []
        self.cert = {}

    def check(self, ok, name, detail):
        if not ok:
            raise AssertionError('FAIL_' + name + ': ' + detail)
        self.lines.append('PASS ' + name + ' ' + detail)


def frac_str(x):
    return f'{x.numerator}/{x.denominator}'


def dec(x, digits=15):
    return f'{float(x):.{digits}f}'


def run(out_path):
    rep = Report()

    # --- model identity: coverage law reproduces the recorded 7232 total and 1646 idle.
    q = model(WORD)
    rep.check(q['total'] == Q(7232) and q['idle'] == Q(1646), 'COVERAGE_IDENTITY',
              f"total={q['total']} idle={q['idle']} w={frac_str(q['w'])} deficit={frac_str(q['deficit'])}")

    # --- positive control: reproduce PR #1240's incumbent ceiling.
    # #1240 reports the first 1e-15 grid point above a*, so its number is an upper
    # bound; require our true bracket to sit within one grid step below it.
    lo, hi = ceiling(WORD)
    rep.check(hi - lo <= Q(2, 10 ** 18) and hi <= REF_CEILING and lo >= REF_CEILING - Q(1, 10 ** 15),
              'INCUMBENT_CEILING',
              f'a* in [{dec(lo, 18)}, {dec(hi, 18)}] vs #1240 grid ceiling {dec(REF_CEILING, 15)}')
    rep.cert['incumbent_ceiling'] = {'a_lo': frac_str(lo), 'a_hi': frac_str(hi),
                                    'decimal': dec(hi, 18), 'pr1240_reported': dec(REF_CEILING, 15)}

    # --- targets: T2 (unbinding) is the nearer goal, above the incumbent packing ceiling.
    rep.check(0 < A_T2 < A_T1 and A_T2 > REF_CEILING, 'TARGETS',
              f'a_T1=1/99={dec(A_T1)} a_T2={frac_str(A_T2)}={dec(A_T2, 18)}')
    rep.cert['targets'] = {'a_T1': '1/99', 'a_T2': frac_str(A_T2), 'kappa_bit': frac_str(KAPPA_BIT)}

    # --- unpaid-coordinate threshold u* (continuous bracket + least integer).
    u_res = {}
    for tag, a_t in (('T1', A_T1), ('T2', A_T2)):
        met = lambda u, a_t=a_t: target_met(WORD, a_t, unpaid=u)
        ulo, uhi = bisect_param(met, Q(1), Q(12), Q(1, 10 ** 9))
        ints = [u for u in range(1, 13) if met(Q(u))]
        least = ints[0]
        rep.check(met(Q(least)) and (least == 1 or not met(Q(least - 1))),
                  f'UNPAID_THRESHOLD_{tag}',
                  f'u* in ({dec(ulo, 9)}, {dec(uhi, 9)}); least integer u = {least}')
        u_res[tag] = {'u_lo': frac_str(ulo), 'u_hi': frac_str(uhi), 'least_integer': ints[0]}
    rep.cert['unpaid_thresholds'] = u_res

    # --- centre-charge threshold c* (met for c <= c*).
    c_res = {}
    for tag, a_t in (('T1', A_T1), ('T2', A_T2)):
        met = lambda c, a_t=a_t: target_met(WORD, a_t, centre=c)
        try:
            clo, chi = bisect_param(lambda c: not met(c), Q(0), Q(64), Q(1, 10 ** 9))
            c_res[tag] = {'c_lo': frac_str(clo), 'c_hi': frac_str(chi), 'met_at_zero': met(Q(0))}
            rep.check(met(clo) and not met(chi), f'CENTRE_THRESHOLD_{tag}',
                      f'c* in ({dec(clo, 9)}, {dec(chi, 9)}); target met iff c <= c*')
        except ValueError:
            # Not met even at c = 0: certified obstruction for centre relief alone.
            lo0, hi0 = ceiling(WORD, centre=Q(0))
            rep.check(hi0 < a_t, f'CENTRE_OBSTRUCTION_{tag}',
                      f'no c in [0,64] meets the target; sup a* at c=0 in ({dec(lo0, 15)}, {dec(hi0, 15)})')
            c_res[tag] = {'obstruction': True, 'a_star_c0_lo': frac_str(lo0), 'a_star_c0_hi': frac_str(hi0)}
    rep.cert['centre_thresholds'] = c_res

    # --- families-per-call threshold F* at stages = 9 (met for F >= F*).
    # The floor 693 is the least families with total mass >= the word's 5586.
    f_res = {}
    for tag, a_t in (('T1', A_T1), ('T2', A_T2)):
        met = lambda f, a_t=a_t: target_met(WORD, a_t, families=f)
        flo, fhi = bisect_param(met, 693, 18000, Q(1))
        # integer tightening: scan down to the least integer families with the target met.
        fmin = -(-fhi.numerator // fhi.denominator)
        while fmin > 693 and met(fmin - 1):
            fmin -= 1
        rep.check(met(fmin) and not met(fmin - 1), f'FAMILIES_THRESHOLD_{tag}',
                  f'F* in [{fmin - 1}+ , {fmin}] families per replica (w = F/9 per call)')
        f_res[tag] = {'families_least': fmin, 'families_prev_not_met': fmin - 1,
                      'w_at_threshold': frac_str(Q(fmin, STAGES))}
    rep.cert['families_thresholds'] = f_res

    # --- paid-word scaling threshold s* (local counts * s, met for s <= s*).
    s_res = {}
    for tag, a_t in (('T1', A_T1), ('T2', A_T2)):
        met = lambda s, a_t=a_t: target_met({r: n * s for r, n in WORD.items()}, a_t)
        slo, shi = bisect_param(lambda s: not met(s), Q(0), Q(1), Q(1, 10 ** 9))
        rep.check(met(slo) and not met(shi), f'WORD_SCALING_{tag}',
                  f's* in ({dec(slo, 9)}, {dec(shi, 9)}); target met iff paid counts <= s* x current')
        s_res[tag] = {'s_lo': frac_str(slo), 's_hi': frac_str(shi)}
    rep.cert['word_scaling_thresholds'] = s_res

    # --- pair obstructions and sufficiency margins.
    lo2, hi2 = ceiling(WORD, unpaid=2, centre=0)
    rep.check(hi2 < A_T1, 'PAIR_UNPAID2_CENTRE0_OBSTRUCTION_T1',
              f'sup a* at (u=2, c=0) in ({dec(lo2, 15)}, {dec(hi2, 15)}) < 1/99: unpaid relief up to 2 with any centre charge cannot reach T1')
    lo3, hi3 = ceiling(WORD, unpaid=3, centre=CENTRE0)
    rep.check(lo3 > A_T1, 'PAIR_UNPAID3_SUFFICIENCY_T1',
              f'a* at (u=3, c=64) in ({dec(lo3, 15)}, {dec(hi3, 15)}) > 1/99 (optimistic sufficiency)')
    rep.cert['pairs'] = {'u2_c0_T1': {'a_lo': frac_str(lo2), 'a_hi': frac_str(hi2)},
                        'u3_c64_T1': {'a_lo': frac_str(lo3), 'a_hi': frac_str(hi3)}}

    # --- D/E diagnostic and the convexity margin a* < D/E at named points.
    de_res = {}
    points = [('incumbent', {}), ('u2_c0', dict(unpaid=2, centre=0)), ('u3_c64', dict(unpaid=3)),
              ('c0', dict(centre=0))]
    for name, kw in points:
        d, elo, ehi = de_diagnostic(WORD, **kw)
        alo, ahi = ceiling(WORD, **kw)
        # convexity: a* < D/E strictly, certified as a*_hi < (D/E)_lo = D/E_hi.
        rep.check(d > 0 and ahi < d / ehi, f'DE_DIAGNOSTIC_{name}',
                  f'D={frac_str(d)} E in ({dec(elo, 9)}, {dec(ehi, 9)}) D/E ~ {dec(d / ehi, 15)} a* ~ {dec(ahi, 15)}')
        de_res[name] = {'D': frac_str(d), 'E_lo': frac_str(elo), 'E_hi': frac_str(ehi),
                        'a_star_lo': frac_str(alo), 'a_star_hi': frac_str(ahi)}
    rep.cert['de_diagnostics'] = de_res

    # --- failure controls: each mutant must be rejected or strictly worse.
    for bad, why in ((dict(unpaid=0), 'unpaid'), (dict(rank_cap=52), 'halving guard'),
                     (dict(centre=-1), 'negative centre')):
        try:
            model(WORD, **bad)
        except ValueError:
            rep.lines.append(f'PASS CONTROL_REJECT_{why.replace(" ", "_")}')
        else:
            raise AssertionError(f'FAIL_CONTROL_REJECT_{why}: accepted')
    try:
        model({1: WORD[1] + 2000, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8})
    except ValueError:
        rep.lines.append('PASS CONTROL_REJECT_over_paid_word')
    else:
        raise AssertionError('FAIL_CONTROL_REJECT_over_paid_word: accepted')
    mutant = dict(WORD)
    mutant[1] += 1
    mlo, mhi = ceiling(mutant)
    rep.check(mhi < lo, 'CONTROL_MUTANT_ONE_EXTRA_RANK1_LOWERS_CEILING',
              f'mutant a* ~ {dec(mhi, 15)} < incumbent ~ {dec(lo, 15)}')
    m2lo, m2hi = ceiling(WORD, families=FAMILIES0 + 9)
    rep.check(m2lo > hi, 'CONTROL_MONOTONE_FAMILIES',
              f'F+9 raises a* to ~{dec(m2lo, 15)} > incumbent ~{dec(hi, 15)}')

    rep.cert['model'] = {'m': M, 'stages': STAGES, 'families': FAMILIES0, 'centre': CENTRE0,
                        'unpaid': UNPAID0, 'idle_rank_cap': R, 'local_word': WORD,
                        'local_mass': WORD_MASS}
    rep.lines.append('PASS_COMPLEX_COVERAGE_LAW_RELIEF')

    print('\n'.join(rep.lines))
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as fh:
            json.dump({'status': 'PASS_COMPLEX_COVERAGE_LAW_RELIEF', 'model': rep.cert['model'],
                       'targets': rep.cert['targets'], 'incumbent_ceiling': rep.cert['incumbent_ceiling'],
                       'unpaid_thresholds': rep.cert['unpaid_thresholds'],
                       'centre_thresholds': rep.cert['centre_thresholds'],
                       'families_thresholds': rep.cert['families_thresholds'],
                       'word_scaling_thresholds': rep.cert['word_scaling_thresholds'],
                       'pairs': rep.cert['pairs'], 'de_diagnostics': rep.cert['de_diagnostics'],
                       'log': rep.lines}, fh, indent=2)
            fh.write('\n')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', help='write the complete certificate JSON here')
    args = ap.parse_args()
    return run(args.out)


if __name__ == '__main__':
    raise SystemExit(main())
