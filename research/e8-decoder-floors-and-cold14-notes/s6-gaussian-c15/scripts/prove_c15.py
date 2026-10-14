"""G2 settled: no 15-total Gaussian-E8 decoder has a column-space vector supported in a 3-flat.

Reduction (argued, elementary): if B = W U^T (W, U in F2^{60x15}) is valid and x != 0 has supp(W x) inside a 3-flat H,
then with O = lines outside H, W[O] x = 0, so rank W[O] <= 14 and B[O,O] = W[O] U[O]^T is a rank-<=14 matrix obeying
the decoder pattern induced on O.  Hence it suffices that minrank(pattern on O) >= 15 for every 3-flat H (same for U by
transposition).  By symmetry (group of order 11520 on the lines, orbits.py) one H per orbit suffices; argv 'all' runs all
1500 3-flats instead (group-free check).  Calibrations: c = 15 on O must be SAT; c = 14 / 15 on all 60 lines UNSAT / SAT."""
import sys, time, pickle
sys.path.insert(0, sys.path[0])
from multiprocessing import Pool
from lines import views
from sub_minrank import run

S = views()['Gauss']

def job(args):
    H, c, solver = args
    O = [T for T in range(60) if T not in set(H)]
    r, t, k = run(S, O, c, solver)
    return H, c, solver, r, t, k

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'orbits'
    solvers = sys.argv[2].split(',') if len(sys.argv) > 2 else ['cadical153']
    if mode == 'all':
        F = pickle.load(open('flats_Gauss.pkl', 'rb'))
        Hs = sorted(sorted(f) for f, d in F.items() if d == 3); assert len(Hs) == 1500
        jobs = [(H, 14, solvers[0]) for H in Hs]
    else:
        reps = pickle.load(open('orbits.pkl', 'rb'))['hyp_reps']
        Hs = [h for h, _ in reps]
        jobs = [(H, c, s) for H in Hs for c in (14, 15) for s in solvers]
        for c in (14, 15):
            r, t, k = run(S, range(60), c, solvers[0])
            print('all 60 lines  c=%d %s %.1fs' % (c, 'SAT' if r else 'UNSAT', t), flush=True)
    bad = 0; n = 0
    with Pool(3) as p:
        for H, c, s, r, t, k in p.imap_unordered(job, jobs):
            n += 1
            exp = (c == 15)
            bad += (r != exp)
            if mode != 'all' or r or n % 100 == 0:
                print('|H|=%2d |O|=%2d c=%d %-11s %s %.1fs clique-gauge %d  [%d/%d]' % (len(H), 60 - len(H), c, s, 'SAT' if r else 'UNSAT', t, k, n, len(jobs)), flush=True)
    print('ALL AS EXPECTED' if bad == 0 else 'MISMATCHES: %d' % bad, flush=True)
