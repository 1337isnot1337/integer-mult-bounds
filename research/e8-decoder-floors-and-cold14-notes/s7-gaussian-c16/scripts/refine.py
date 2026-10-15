"""S7 step 2d: exact joint refinement of the configurations surviving dumbbell.py.

For a level-k rep T (one 3-flat per cheap total) assign each member a type:
  'a' (a side of dim <= 2): choose a 2-flat Z inside T[i] containing that side; EVERY 3-flat H containing Z is a legal choice
      for this total, so every transversal using any such H must be a level-k set.  At most 2 'a' members, and if 2, the
      pair (Z1, Z2) must be a level-2 set of the 2-flat search (lev_c16_d2.pkl).
  'p' (dumbbell): partner Y with beta(T[i], Y) = 2; both T[i] and Y are legal.
  'q': only T[i].
Requirement from cost <= 42: 3*#a + #p >= 22 - k.  ALL transversals of the joint choice must be level-k sets.
(A side of dim 1, a line l, is inside some 2-flat Z inside T[i], and every 3-flat through Z contains l, so 'a' with Z is
a relaxation of the line case.)  Prints the configurations that survive (should be none for exclusion)."""
import sys, time, pickle, itertools
sys.path.insert(0, sys.path[0])
import numpy as np
from levels2 import load_flats, canon

G, fl3, P3 = load_flats('3')
_, fl2, P2 = load_flats('2')
NF = len(fl3)
good = pickle.load(open('lev_c16_d3_hi.pkl', 'rb'))['good']
good2 = pickle.load(open('lev_c16_d2.pkl', 'rb'))['good']
dd = pickle.load(open('dumbbell_out.pkl', 'rb'))
beta = dd['beta']; feasible = dd['feasible']
set3 = [set(f) for d, f in fl3]; set2 = [set(f) for d, f in fl2]
through = [[h for h in range(NF) if set2[z] <= set3[h]] for z in range(len(fl2))]
inside = [[z for z in range(len(fl2)) if set2[z] <= set3[h]] for h in range(NF)]
cache = {}


def ok(X):
    X = tuple(X)
    if len(set(X)) < len(X): return False
    if X not in cache: cache[X] = canon(P3, X) in good[len(X)]
    return cache[X]


def joint_ok(T, opts):
    """opts[i] = list of legal 3-flats for member i; every transversal must be a level-k set."""
    for X in itertools.product(*opts):
        if not ok(sorted(X)): return False
    return True


def analyse(k, T):
    T = list(T)
    need = 22 - k
    subst = lambda i, h: sorted(T[:i] + [h] + T[i + 1:])
    part = {i: [y for y in range(NF) if y not in T and beta[T[i], y] == 2 and ok(subst(i, y))] for i in range(k)}
    aopt = {i: [z for z in inside[T[i]] if all(h == T[i] or (h not in T and ok(subst(i, h))) for h in through[z])] for i in range(k)}
    sols = []
    # choose A (<= 2 members with a 2-flat), then dumbbells among the rest with backtracking
    for na in range(0, 3):
        if 3 * na + (k - na) < need: continue
        for A in itertools.combinations(range(k), na):
            if any(not aopt[i] for i in A): continue
            for Zs in itertools.product(*[aopt[i] for i in A]):
                if na == 2:
                    if Zs[0] == Zs[1] or canon(P2, list(Zs)) not in good2[2]: continue
                base = [[T[i]] for i in range(k)]
                for i, z in zip(A, Zs): base[i] = through[z]
                if not joint_ok(T, base): continue
                rest = [i for i in range(k) if i not in A and part[i]]
                pneed = need - 3 * na
                if pneed <= 0:
                    sols.append((A, Zs, {})); continue
                # backtracking over dumbbells
                found = []
                def rec(pos, choice):
                    if found: return
                    if len(choice) >= pneed:
                        found.append(dict(choice)); return
                    if len(choice) + len(rest) - pos < pneed: return
                    for q in range(pos, len(rest)):
                        i = rest[q]
                        for y in part[i]:
                            if y in [v for v in choice.values()]: continue
                            opts = [list(o) for o in base]
                            for j, yy in list(choice.items()) + [(i, y)]: opts[j] = [T[j], yy]
                            if joint_ok(T, opts):
                                choice[i] = y; rec(q + 1, choice); del choice[i]
                                if found: return
                rec(0, {})
                if found: sols.append((A, Zs, found[0]))
                if sols: return sols, part, aopt
    return sols, part, aopt


if __name__ == '__main__':
    t0 = time.time(); surv = []
    for k, T, p in feasible:
        sols, part, aopt = analyse(k, T)
        na = sum(1 for i in aopt if aopt[i])
        print('k=%2d T=%s  doublable %d  a-capable %d  -> %s (%.0fs)' % (
            k, T, sum(1 for i in part if part[i]), na, 'SURVIVES %s' % (sols[0],) if sols else 'excluded', time.time() - t0), flush=True)
        if sols: surv.append((k, T, sols[0]))
    pickle.dump(surv, open('refine_out.pkl', 'wb'))
    print('SURVIVING CONFIGURATIONS:', len(surv), flush=True)
