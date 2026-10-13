"""Rank candidate unit families by a helper-adjusted estimate of the achievable saving (MODEL; see est_model.py).

Per candidate (side, h, v, cst, z):
  X*      certified #595 ceiling (skel.X, best odd s in 3..15) at x = cst / v      [exact interval upper end]
  rho*    break-even helpers per port: the rho at which the calibrated model estimate (best s) equals the calibrated
          model estimate of the E8 word of the same side at its shipped intensity and best s (bit #555 at
          rho = 439/111, complex #568 at rho = 496/112): same model, same s freedom on both sides
  a_est   calibrated model estimate at three helper-intensity hypotheses (E8's shipped intensity transferred):
            rho_same = rho_E8                                (helpers per port unchanged)
            rho_dim  = rho_E8 * (z/(h-1)) / (z_E8/(h_E8-1))  (readers per window dimension)  <- central
            rho_read = rho_E8 * z / z_E8                     (readers per port)
          in both piece-scaling modes ('abs' pessimistic, 'rel' optimistic).
Candidates: E8 references; triple family T_h (bit cst = h(h-1), complex cst = h^2: centre decoders, checked by
triple.py); Lorentzian I_{11,1}, I_{13,1} (label decoders, cst 110 / 156, checked by lorentz.py).
Usage: python rank.py REPO_ROOT [--json out]
"""
import json
import sys
from fractions import Fraction as Fr
from math import comb

REPO = sys.argv[1]
sys.path.insert(0, REPO + '/research/format-limits/scripts')
sys.dont_write_bytecode = True
from skel import X                      # noqa: E402

import est_model as E                   # noqa: E402

REF = {'bit': dict(h=8, rho=Fr(439, 111), z=63, a=1.7331e-3),
       'complex': dict(h=9, rho=Fr(496, 112), z=52, a=1.5987e-3)}


def xstar(h, x):
    best = None
    for s in range(3, 17, 2):
        r = X(s, h, 1, Fr(x))
        if r and (best is None or r['hi'] > best[1]):
            best = (s, r['hi'])
    return best


def candidates():
    C = [dict(name='E8 bit 111/63 (#555)', side='bit', h=8, v=111, cst=63, z=63),
         dict(name='E8 bit 120/72', side='bit', h=8, v=120, cst=72, z=63),
         dict(name='E8 complex 112/64 (#568)', side='complex', h=9, v=112, cst=64, z=52),
         dict(name='I_{11,1} bit', side='bit', h=11, v=220, cst=110, z=Fr(165 * 115 + 55 * 129, 220)),
         dict(name='I_{13,1} bit', side='bit', h=13, v=364, cst=156, z=Fr(286 * 183 + 78 * 231, 364))]
    for h in (10, 11, 12, 13, 14, 16, 18, 20, 22, 24, 26, 28, 30):
        C.append(dict(name='T_%d bit' % h, side='bit', h=h, v=comb(h, 3), cst=h * (h - 1), z=3 * comb(h - 3, 2)))
    for h in (12, 14, 16, 18, 20, 22, 24, 26, 28, 30):
        C.append(dict(name='T_%d complex' % h, side='complex', h=h, v=comb(h, 3), cst=h * h,
                      z=comb(h - 3, 3) + 3 * (h - 3)))
    return C


def cal_est(side, h, x, rho, mode, cal):
    b = E.estimate(side, h, x, rho, mode)
    return (None, None, None) if b is None else (b[0], b[1] * cal, b[2])


def breakeven(side, h, x, mode, cal, target):
    lo, hi = Fr(0), Fr(400)
    f = lambda r: (cal_est(side, h, x, r, mode, cal)[1] or 0.0)
    if f(lo) < target:
        return 0.0
    if f(hi) >= target:
        return float(hi)
    for _ in range(40):
        mid = (lo + hi) / 2
        if f(mid) >= target:
            lo = mid
        else:
            hi = mid
    return float(lo)


def main():
    rows = []
    cals = {(sd, md): E.calibration(sd, md) for sd in ('bit', 'complex') for md in ('abs', 'rel')}
    print('calibration factors', {k: round(v, 4) for k, v in cals.items()})
    target = {sd: cal_est(sd, REF[sd]['h'], Fr(63, 111) if sd == 'bit' else Fr(64, 112), REF[sd]['rho'], 'abs',
                          cals[(sd, 'abs')])[1] for sd in ('bit', 'complex')}
    print('E8 targets (calibrated model, best s):', {k: '%.4e' % v for k, v in target.items()})
    for c in candidates():
        sd, h = c['side'], c['h']
        x = Fr(c['cst'], c['v'])
        ref = REF[sd]
        xs = xstar(h, x)
        rh = {'same': ref['rho'],
              'dim': ref['rho'] * Fr(c['z']) / (h - 1) / Fr(ref['z'], ref['h'] - 1),
              'read': ref['rho'] * Fr(c['z']) / ref['z']}
        row = dict(name=c['name'], side=sd, h=h, v=c['v'], cst=c['cst'], x=float(x), z=float(c['z']),
                   Xstar=float(xs[1]) if xs else None, Xs=xs[0] if xs else None,
                   rho={k: float(v) for k, v in rh.items()})
        for md in ('abs', 'rel'):
            row['rho_star_' + md] = breakeven(sd, h, x, md, cals[(sd, md)], target[sd])
            for k, r in rh.items():
                s_, a_, ch = cal_est(sd, h, x, r, md, cals[(sd, md)])
                row['a_%s_%s' % (k, md)] = a_
                row['s_%s_%s' % (k, md)] = s_
                if k == 'dim' and md == 'abs' and ch:
                    row['chain_dim_abs'] = {kk: round(vv, 5) for kk, vv in ch.items()}
        rows.append(row)
        f = lambda v: '%.3e' % v if v else '   -    '
        print('%-26s h=%2d v=%5d x=%.4f z=%7.1f X*=%s | rho*: abs %6.2f rel %6.2f | rho same/dim/read %5.2f/%6.2f/%7.2f | '
              'a_dim abs %s rel %s | a_same abs %s | a_read abs %s'
              % (row['name'], h, c['v'], row['x'], row['z'], f(row['Xstar']), row['rho_star_abs'], row['rho_star_rel'],
                 row['rho']['same'], row['rho']['dim'], row['rho']['read'], f(row['a_dim_abs']), f(row['a_dim_rel']),
                 f(row['a_same_abs']), f(row['a_read_abs'])), flush=True)
    if '--json' in sys.argv:
        json.dump(rows, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
