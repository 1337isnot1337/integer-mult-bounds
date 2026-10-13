"""price.py: exact frame pricing (#1186 harness: program-map screen, cone caps, tail-mutable optimal frames, cut equality)
of census matches on one word.  Needs the #1186 toolkit directory (research/exact-frame-toolkit of PR #1186).
usage: price.py TOOLKIT_DIR WORD.json.gz CENSUS.json OUT.json [--workers N]"""
import argparse, json, os, resource, sys, time, multiprocessing as mp
ap = argparse.ArgumentParser(); ap.add_argument('toolkit'); ap.add_argument('word'); ap.add_argument('census'); ap.add_argument('out')
ap.add_argument('--workers', type=int, default=8); ap.add_argument('--check-literal', type=int, default=1); a = ap.parse_args()
sys.path.insert(0, a.toolkit)
import harness as H
P = None
def init():
    global P; P = H.Pricer(a.word, check_literal=bool(a.check_literal))
def run(m):
    r = P.price(m['ed'], timeout=300)
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3 > 8: r['rss_exit'] = True
    return dict({k: v for k, v in m.items() if k != 'ed'}, ed=m['ed'], price=r)
if __name__ == '__main__':
    cen = json.load(open(a.census)); ms = [m for r in cen for m in r['matches']]
    t0 = time.time(); init(); print('base cost', P.base_cost, 'profile', P.base_profile, f'{time.time()-t0:.1f}s', flush=True)
    out = []
    with mp.get_context('fork').Pool(a.workers, initializer=init, maxtasksperchild=6) as pool:
        for n, r in enumerate(pool.imap_unordered(run, ms), 1):
            out.append(r); p = r['price']
            print(f"  {n}/{len(ms)} {time.time()-t0:.0f}s pivot {r['pivot']} h {r['helper']} donor {r['donor']} -> {p.get('status')} delta {p.get('delta')} {p.get('profile')}", flush=True)
    out.sort(key=lambda r: (r['pivot'], r['helper'], r['donor'], r['cut'], r['hook']))
    json.dump(out, open(a.out, 'w'), sort_keys=True)
    g = sorted([r for r in out if r['price'].get('delta') is not None and r['price']['delta'] < 0], key=lambda r: r['price']['delta'])
    print('priced', len(out), 'gains', len(g), 'pivots with gains', sorted({r['pivot'] for r in g}))
    for r in g[:40]: print('   gain', r['pivot'], r['helper'], r['donor'], r['price']['delta'], r['price']['profile'])
