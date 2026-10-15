"""Run minrank(O) <= c tests on complements of unions of pair-orbit reps.  argv: c solver nproc."""
import sys, time, pickle
sys.path.insert(0, sys.path[0])
from multiprocessing import Pool
from pairs import load, job

if __name__ == '__main__':
    c = int(sys.argv[1]); solver = sys.argv[2]; npr = int(sys.argv[3])
    G, hyp = load()
    reps = pickle.load(open('pair_orbits.pkl', 'rb'))['reps']
    jobs = [(tuple(sorted(set(hyp[a]) | set(hyp[b]))), c, solver) for a, b, _ in reps]
    res = {}
    with Pool(npr) as p:
        for k, ((U, c_, s, r, t, nO), (a, b, n)) in enumerate(zip(p.imap(job, jobs), reps)):
            res[(a, b)] = r
            print('pair (%4d,%4d) |H1|=%2d |H2|=%2d |O|=%2d orbit %5d c=%d %s %s %.1fs [%d/%d]' % (
                a, b, len(hyp[a]), len(hyp[b]), nO, n, c, s, 'SAT' if r else 'UNSAT', t, k + 1, len(jobs)), flush=True)
    pickle.dump(res, open('pair_res_c%d_%s.pkl' % (c, solver), 'wb'))
    print('SAT pairs:', sum(res.values()), 'of', len(res), flush=True)
