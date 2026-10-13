"""Q3 (MODEL, not a bound): S3's calibrated helper model (est_model.py, unchanged) on the best punctured I_{11,1} unit.
Q1 shows no puncture lowers x below 1/2 for centre decoders (certificate) and none was found for label decoders,
so the best unit is the unpunctured 220/110 (h = 11); the first sub-10 total (210/109) is shown for comparison.
Helper intensities rho (helpers per port):
  skel_cells  : E8 cell architecture transferred (2 carriers/source + 1 aux per cell, 3 cells/line/2 = 1.5/port,
                + 11 totals + one extra 4-frame for the odd pair count: (440 + 330 + 11 + 6)/220)
  skel_pairs2 : same, pair sources with 2 branches (pair 2-cover; frames not cells): (385 + 330 + 11 + 6)/220
  E8 shipped  : 439/111
  rho_dim     : S3's readers-per-window-dimension transfer
Usage: python model3.py REPO_ROOT [--json out]"""
import sys, json
from fractions import Fraction as Fr
sys.dont_write_bytecode = True
import rank as RK       # noqa  (imports skel via REPO in argv[1])
E = RK.E

units = [dict(name='I_{11,1} 220/110 (best; no improving puncture)', h=11, v=220, cst=110),
         dict(name='I_{11,1} punctured 210/109 (pair-label total at 9)', h=11, v=210, cst=109)]
rhos = {'skel_cells': Fr(440 + 330 + 11 + 6, 220), 'skel_pairs2': Fr(385 + 330 + 11 + 6, 220),
        'E8_shipped': Fr(439, 111), 'rho_dim': Fr(439, 111) * Fr(165 * 115 + 55 * 129, 220) / 10 / Fr(63, 7),
        'three': Fr(3)}
cals = {md: E.calibration('bit', md) for md in ('abs', 'rel')}
target = RK.cal_est('bit', 8, Fr(63, 111), Fr(439, 111), 'abs', E.calibration('bit', 'abs'))[1]
out = []
print('E8 #555 calibrated model target a = %.4e' % target)
for u in units:
    x = Fr(u['cst'], u['v'])
    xs = RK.xstar(u['h'], x)
    row = dict(name=u['name'], x=str(x), Xstar=float(xs[1]), Xs=xs[0])
    for md in ('abs', 'rel'):
        row['rho_star_' + md] = RK.breakeven('bit', u['h'], x, md, cals[md], target)
        for k, r in rhos.items():
            s_, a_, _ = RK.cal_est('bit', u['h'], x, r, md, cals[md])
            row['a_%s_%s' % (k, md)] = a_
    out.append(row)
    print('%s: x=%s X*=%.4e | rho* abs %.2f rel %.2f' % (u['name'], x, row['Xstar'], row['rho_star_abs'], row['rho_star_rel']))
    for k, r in rhos.items():
        print('   rho %-11s = %.3f: a_est abs %.4e  rel %.4e  (E8 %.4e)' % (k, float(r), row['a_%s_abs' % k], row['a_%s_rel' % k], target))
if '--json' in sys.argv:
    json.dump(dict(target=target, rhos={k: float(v) for k, v in rhos.items()}, rows=out),
              open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
