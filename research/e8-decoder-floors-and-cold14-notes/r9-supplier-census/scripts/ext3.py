"""Extended value-holder kernel census driver (wraps PR1957 gencomp2.run unchanged).
usage: ext.py WORD JOBS.json OUTDIR maxterms K tl slack nworkers
JOBS = [[dels...], ...]; budget = -ddel - 1 + slack (slack>0 relaxes the non-additive frame-cost oracle; every
solution is priced exactly by the PR1186 frame solver)."""
import os, sys, json, time
sys.path.insert(0, '/private/tmp/claude-501/-Users-joelpulikkan-integer-mult-bounds/3231f0a2-7112-4dee-8ef4-f1fca97ae281/scratchpad/r9/tools')
import contextlib, io, gencomp3
from multiprocessing import Pool
P = None; ARGS = None
def init(word, args):
    global P, ARGS
    import harness as H; P = H.Pricer(word); ARGS = args
def job(dels):
    import gencomp3 as G
    from fc3 import solve
    mt, K, tl, slack, od = ARGS
    t = time.time()
    try:
        _, r = solve(P, dict(delete=dels)); ddel = r['cost'] - P.base_cost
        if ddel >= 0: return dels, dict(ddel=ddel, skip=True)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            info = G.run(P, dels, mt, K, tl, os.path.join(od, 'x-%s.json' % '-'.join(map(str, dels))), slack=slack, verbose=False); res = info['res']; info.pop('res')
        best = min([x['delta'] for x in res if x.get('delta') is not None], default=None)
        return dels, dict(info, nsol=len(res), best=best, st=[(x['status'], x['delta'], x['two_value']) for x in res], sec=round(time.time() - t, 1))
    except Exception as e:
        return dels, dict(err=repr(e)[:200])
if __name__ == '__main__':
    word, jp, od = sys.argv[1:4]; mt, K, tl, slack, nw = int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
    os.makedirs(od, exist_ok=True); jobs = json.load(open(jp)); summ = os.path.join(od, 'SUMMARY.json')
    done = json.load(open(summ)) if os.path.exists(summ) else {}
    jobs = [j for j in jobs if '-'.join(map(str, j)) not in done]
    t = time.time()
    with Pool(nw, initializer=init, initargs=(word, (mt, K, tl, slack, od)), maxtasksperchild=40) as pool:
        for n, (dels, r) in enumerate(pool.imap_unordered(job, jobs)):
            done['-'.join(map(str, dels))] = r
            if r.get('best') is not None and r['best'] < 0: print('GAIN', dels, r, flush=True)
            print(n, len(jobs), dels, r.get('ddel'), r.get('nsol'), r.get('best'), r.get('err', ''), r.get('sec'), round(time.time() - t), flush=True)
            json.dump(done, open(summ, 'w'))
