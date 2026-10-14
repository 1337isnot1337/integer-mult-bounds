"""Two-value holder kernel search (extends PR1957 gencomp2): delete B read(s) of a value v, compensate with inserted
reads x += lam*y where y holds v, OR holds v + u for a residual direction u shared by >=2 holder windows (so the u parts
can cancel).  Exactness is matrix-valued: sum_j lam_j val_j (x) col_j == Delta on every (input, output) entry, over B+tails,
plus the B-only target-row (dirt) rows.  Frame-cost oracle = PR1957 CostOracle; every solution is priced exactly."""
import os, sys, json, time, math
from fractions import Fraction as Q
from collections import defaultdict
sys.path.insert(0, '/private/tmp/claude-501/-Users-joelpulikkan-integer-mult-bounds/3231f0a2-7112-4dee-8ef4-f1fca97ae281/scratchpad/r9/src/pr1957/research/t74-k554-local-exhaustion/tools')
import _paths
from ortools.sat.python import cp_model
from fc3 import solve
from costorc import CostOracle
V = 112
coef = lambda g: Q(g[3], g[4]) if g[0] == 'add' else Q(g[2], g[3])

def windows(seq, nreg, skip=frozenset()):
    rows = {}; get = lambda x: rows.get(x, {x: Q(1)})
    start = [0] * nreg; cur = [None] * nreg; out = []
    for i, g in enumerate(seq):
        if i in skip: continue
        t = g[1]
        if g[0] == 'add':
            a = dict(get(t)); c = coef(g)
            for k, v in get(g[2]).items():
                a[k] = a.get(k, 0) + c * v
                if not a[k]: del a[k]
        else: a = {k: v * coef(g) for k, v in get(t).items()}
        old = get(t); rows[t] = a
        if a != old:
            out.append((t, start[t], i + 1, old)); start[t] = i + 1
    for x in range(nreg): out.append((x, start[x], len(seq) + 1, get(x)))
    return out

def resid(val, v, k0):
    r = Q(val.get(k0, 0)) / v[k0]
    y = {k: x - r * v.get(k, 0) for k, x in val.items()}
    for k, x in v.items():
        if k not in val and r: y[k] = -r * x
    y = {k: x for k, x in y.items() if x}
    if not y: return (), r
    ks = sorted(y); n = y[ks[0]]
    return tuple((k, y[k] / n) for k in ks), r

_W = None
def run(P, dels, maxterms, K, tl, out=None, slack=0, lamr=8, maxcand=6000, verbose=True):
    global _W
    w = P.base; B = w['B']; NB = len(B); tails = [w['cleanup'][i] for i, U in w['early_cleanup']]; seq = B + tails; L = len(seq)
    nreg = 2 * V + w['report']['R']
    W = windows(seq, nreg, frozenset(dels))      # holder values of the DELETED program
    # values at deletion
    rows = {}; get = lambda x: rows.get(x, {x: Q(1)}); srcval = {}
    for i, g in enumerate(seq):
        if i > max(dels): break
        if i in dels: srcval[i] = dict(get(g[2]))
        t = g[1]
        if g[0] == 'add':
            a = dict(get(t)); c = coef(g)
            for k, v in get(g[2]).items():
                a[k] = a.get(k, 0) + c * v
                if not a[k]: del a[k]
        else: a = {k: v * coef(g) for k, v in get(t).items()}
        rows[t] = a
    v = srcval[dels[0]]; k0 = min(v)
    for i in dels: assert resid(srcval[i], v, k0)[0] == (), 'deleted reads must share a value'
    w2, r = solve(P, dict(delete=dels)); ddel = r['cost'] - P.base_cost
    bud = -ddel - 1 + slack
    orc = CostOracle(w2, P.costs.c); ds = sorted(dels)
    def to2(p): return p - sum(1 for t in ds if t < p)
    vin = set(v)
    cls = defaultdict(list)
    ov = set()
    for wid, (y, a, b, val) in enumerate(W):
        key, _ = resid(val, v, k0)
        cls[key].append(wid)
        if set(val) & vin: ov.add(wid)
    keep = [wid for key, L_ in cls.items() if key == () or (len(L_) >= 2 and any(x in ov for x in L_)) for wid in L_]
    holders = defaultdict(list)
    for wid in keep:
        y, a, b, val = W[wid]
        for p in range(a, min(b, L + 1)): holders[p].append(wid)
    colsF, colsB = {}, {}
    SF = lambda x: colsF.get(x, {x: Q(1)}); SB = lambda x: colsB.get(x, {x: Q(1)})
    D, DB = defaultdict(Q), defaultdict(Q); dset = set(dels); seen = {}; cand = []
    def step(cols, Sf, g):
        if g[0] == 'add':
            t, s = g[1], g[2]; c = coef(g); a = dict(Sf(s))
            for k, x in Sf(t).items():
                a[k] = a.get(k, 0) + c * x
                if not a[k]: del a[k]
            cols[s] = a
        else: x = g[1]; cols[x] = {k: y * coef(g) for k, y in Sf(x).items()}
    for i in range(L, -1, -1):
        g = seq[i] if i < L else None
        if g is None: pass
        elif i in dset:
            t = g[1]; c = coef(g)
            for kin, vv in srcval[i].items():
                for k, x in SF(t).items(): D[(kin, k)] += c * vv * x
                if i < NB:
                    for k, x in SB(t).items():
                        if V <= k < 2 * V: DB[(kin, k)] += c * vv * x
        else:
            step(colsF, SF, g)
            if i < NB: step(colsB, SB, g)
        if i in holders and i not in dset:
            p2 = to2(i) if i < NB else i - len(ds)
            for wid in holders[i]:
                y, a, b, val = W[wid]
                for x in range(nreg):
                    if x == y: continue
                    cst = orc.cost(x, y, p2)
                    if cst > bud: continue
                    vf = SF(x); vb = {k: z for k, z in SB(x).items() if V <= k < 2 * V} if i < NB else {}
                    kk = (x, wid, tuple(sorted(vf.items())), tuple(sorted(vb.items())), i < NB)
                    if kk in seen and seen[kk] <= cst: continue
                    seen[kk] = cst
                    rf = {(ki, k): vi * z for ki, vi in val.items() for k, z in vf.items()}
                    rb = {(ki, k): vi * z for ki, vi in val.items() for k, z in vb.items()}
                    cand.append((x, y, i, rf, rb, cst, wid))
    D = {k: x for k, x in D.items() if x}; DB = {k: x for k, x in DB.items() if x}
    nwin0 = len(cls.get((), [])); ncls = sum(1 for k, L_ in cls.items() if k and len(L_) >= 2 and any(x in ov for x in L_))
    info = dict(dels=dels, ddel=ddel, bud=bud, pure_windows=nwin0, two_value_classes=ncls, cand=len(cand), D=len(D), DB=len(DB))
    if verbose: print(info, flush=True)
    if len(cand) > maxcand or ddel >= 0: return dict(info, skipped='too many candidates' if ddel < 0 else 'no deletion gain', res=[])
    den = 1
    for c_ in cand:
        for z in list(c_[3].values()) + list(c_[4].values()): den = den * z.denominator // math.gcd(den, z.denominator)
    for z in list(D.values()) + list(DB.values()): den = den * z.denominator // math.gcd(den, z.denominator)
    SC = 2 * den
    m = cp_model.CpModel(); lam = []; zz = []
    for j in range(len(cand)):
        l = m.NewIntVar(-lamr, lamr, ''); b = m.NewBoolVar(''); m.Add(l == 0).OnlyEnforceIf(b.Not()); m.Add(l != 0).OnlyEnforceIf(b); lam.append(l); zz.append(b)
    byF = defaultdict(list); byB = defaultdict(list)
    for j, c_ in enumerate(cand):
        for e, z in c_[3].items(): byF[e].append((j, z))
        for e, z in c_[4].items(): byB[e].append((j, z))
    ok = True
    for E, T, by in ((D, set(D) | set(byF), byF), (DB, set(DB) | set(byB), byB)):
        for e in T:
            rhs = E.get(e, Q(0)) * 2 * SC; terms = [lam[j] * int(z * SC) for j, z in by.get(e, [])]
            if not terms:
                if rhs: ok = False
                continue
            m.Add(sum(terms) == int(rhs))
    byY = defaultdict(list)
    for j, c_ in enumerate(cand): byY[c_[1]].append(j)
    npair = 0
    for j, c_ in enumerate(cand):      # an insert into x must not feed a later (or same-slot) insert reading x
        for k in byY.get(c_[0], []):
            if cand[k][2] >= c_[2]: m.Add(zz[j] + zz[k] <= 1); npair += 1
    info['chain_pairs'] = npair
    m.Add(sum(zz) <= maxterms)
    m.Add(sum(zz[j] * cand[j][5] for j in range(len(cand))) <= bud)
    m.Minimize(sum(zz[j] * (cand[j][5] + 50) for j in range(len(cand))))
    info['shape'] = ok; res = []
    if ok:
        for it in range(K):
            s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 2
            st = s.Solve(m)
            if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): info['stop'] = s.StatusName(st); break
            supp = [j for j in range(len(cand)) if s.Value(zz[j])]
            terms = [(cand[j][0], cand[j][1], cand[j][2], Q(s.Value(lam[j]), 2)) for j in supp]
            m.Add(sum(zz[j] for j in supp) <= len(supp) - 1)
            ed = dict(delete=list(dels), insert=[], tail=[], prepend=[])
            for x, y, p, l in terms:
                gte = ['add', x, y, l.numerator, l.denominator, []]
                if p < NB: ed['insert'].append((p, gte))
                else: ed['tail'].append((p - NB, gte))
            ed['insert'].sort(key=lambda t: t[0]); ed['tail'].sort(key=lambda t: t[0])
            rr = P.price(ed, timeout=240)
            two = any(resid(W[cand[j][6]][3], v, k0)[0] != () for j in supp)
            res.append(dict(terms=[(x, y, p, str(l)) for x, y, p, l in terms], two_value=two, est=sum(cand[j][5] for j in supp), status=rr.get('status'), delta=rr.get('delta'), profile=rr.get('profile'), ed=ed))
            if verbose: print(it, res[-1]['terms'], two, rr.get('status'), rr.get('delta'), flush=True)
    info['res'] = res
    if out: json.dump(info, open(out, 'w'), indent=1, default=str)
    return info

if __name__ == '__main__':
    import harness as H
    P = H.Pricer(sys.argv[1]); jobs = json.loads(sys.argv[2])
    for dels in jobs: run(P, dels, int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), slack=int(sys.argv[6]) if len(sys.argv) > 6 else 0)
