"""Re-derive every UNSAT pruning of the 3-flat level search (levels 2..maxlev) and re-solve it with another solver.
Only UNSAT verdicts can remove configurations, so only they need cross-checking (a wrong SAT would only keep more).
argv: c dims pkl maxlev solver nproc   (first three as levels3.py, which reads them at import)"""
import sys, time, pickle
sys.path.insert(0, sys.path[0])
from multiprocessing import Pool
import levels3
from levels3 import gen, init, compl, sat_job
from sub_minrank import run
from levels2 import S


def job(args):
    X, O, cc, solver = args
    r, t, _ = run(S, O, cc, solver)
    return X, r, t


if __name__ == '__main__':
    good = levels3.good; maxlev = int(sys.argv[4]); solver = sys.argv[5]; npr = int(sys.argv[6])
    c = levels3.c
    bad = 0; tot = 0; t0 = time.time()
    for m in range(2, maxlev + 1):
        with Pool(npr, initializer=init, initargs=(good[m - 1],)) as pool:
            cand = set()
            if m == 2:  # all pair orbits (gen() prefilters by pair compatibility, so use the orbit list directly)
                cand = {levels3.canon(levels3.P, [a, b]) for a, b, _ in pickle.load(open('pair_orbits.pkl', 'rb'))['reps']}
                assert len(cand) == 178
            else:
                for out in pool.imap_unordered(gen, sorted(good[m - 1]), chunksize=4): cand.update(out)
            assert good[m] <= cand
            uns = sorted(cand - good[m])
            print('level %d: %d candidates, %d good, %d UNSAT prunings to recheck with %s' % (m, len(cand), len(good[m]), len(uns), solver), flush=True)
            for X, r, t in pool.imap_unordered(job, [(X, compl(X), c - m, solver) for X in uns]):
                tot += 1; bad += bool(r)
                print('  %s |O|=%d minrank<=%d: %s %.1fs' % (X, len(compl(X)), c - m, 'SAT (MISMATCH)' if r else 'UNSAT', t), flush=True)
    print('CROSSCHECK %s: %d UNSAT prunings rechecked, %d mismatches (%.0fs)' % (solver, tot, bad, time.time() - t0), flush=True)
