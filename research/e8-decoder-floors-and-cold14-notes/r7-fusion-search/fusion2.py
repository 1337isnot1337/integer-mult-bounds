"""fusion2: generalized read fusion sweep (superset of fusion.py + repair.py's base fusions).
A target t reads A (coef a, at iA) and H (coef h, at iH), H any non-target register (entrance pre-read reads included).
Donate q*A into H (q = a/h dyadic) at EVERY gap class p in the valid window, delete t's read of A, restore H -= q*A at
every B gap class up to H's next read/scale or A's next write, every early-tail class, or as FULL prepend.
Each fusion is priced alone and with the full read-set exchange of the copy pair containing A or H (as in #1195).
usage: python -B fusion2.py WORD.json.gz OUT.json [--workers N] [--count]"""
import argparse, collections, json, multiprocessing as mp, time
from fractions import Fraction as Q
import harness as C
from fusion import index, dyadic, any_in
from exchange import copy_pairs, movable_reads, is_target
from joint import swap_edit, merge
from joint2 import gap_classes
def candidates(w):
    I = index(w); B = I['B']; nB = len(B); out = []
    by_t = collections.defaultdict(list)
    for i, e in enumerate(B):
        if e[0] == 'add' and is_target(e[1]): by_t[e[1]].append((i, e[2], Q(e[3], e[4])))
    for t, rs in by_t.items():
        for (iA, A, a) in rs:
            for (iH, H, ch) in rs:
                if H == A or iH == iA or t in (A, H): continue
                if any_in(I['RD'][t] + I['SC'][t], min(iA, iH), max(iA, iH) + 1): continue
                q = a / ch
                if not dyadic(q): continue
                othersH = [x for x in I['RD'][H] + I['SC'][H] if x != iH]
                lo = max([x + 1 for x in othersH if x < iH], default=0)
                ev = set(I['W'][H]) | set(I['W'][A]) | set(I['RD'][A]) | set(othersH)
                for p in gap_classes(ev, lo, iH):
                    if any_in(I['W'][A], min(p, iA + 1), max(p, iA + 1)): continue      # A holds the value t read
                    g = ['add', H, A, q.numerator, q.denominator, []]; gr = ['add', H, A, -q.numerator, q.denominator, []]
                    nxt = min([x for x in othersH if x > iH] + [x for x in I['W'][A] if x >= p] + [nB])
                    rests = []
                    for rp in gap_classes(ev, iH + 1, nxt): rests.append(("B%d" % rp, dict(insert=[(p, g), (rp, gr)])))
                    if not any_in(I['W'][A], p, nB) and not any_in(othersH, iH + 1, nB):
                        jmax = min(I['TW'][A] + I['TR'][H] + [len(I['T'])])
                        tev = {k for k, e in enumerate(I['T']) if H in C.regs(e) or A in C.regs(e)}
                        for tp in sorted({0, jmax} | {k + 1 for k in tev if k + 1 <= jmax}): rests.append(("T%d" % tp, dict(insert=[(p, g)], tail=[(tp, gr)])))
                        if A not in I['low'] and H not in I['low'] and not I['TW'][A] and not I['TR'][H]: rests.append(("P", dict(insert=[(p, g)], prepend=[gr])))
                    for tag, e in rests:
                        ed = dict(delete=[iA], insert=e.get('insert', []), tail=e.get('tail', []), prepend=e.get('prepend', []))
                        out.append(dict(t=t, A=A, H=H, iA=iA, iH=iH, p=p, rest=tag, ed=ed))
    return out
P = None; PAIRS = None
def init(path):
    global P, PAIRS
    P = C.Pricer(path); PAIRS = copy_pairs(P.base)
def run(c):
    best = None; tried = []
    eds = [((), c['ed'])]
    for h, (r, ic) in PAIRS.items():
        if c['A'] in (h, r) or c['H'] in (h, r):
            rest = [m for m in movable_reads(P.base, h, r, ic) if m[0] not in c['ed']['delete']]
            ss = [swap_edit(P.base, h, r, ic, m) for m in rest]
            if rest and all(ss):
                m2 = merge([c['ed']] + ss)
                if m2: eds.append(((("exchange", h),), m2))
    for key, ed in eds:
        x = P.price(ed, timeout=120); tried.append((key, x.get('status')))
        if x.get('delta') is not None and (best is None or x['delta'] < best['delta']): best = dict(delta=x['delta'], steps=key, profile=x['profile'])
    return dict({k: v for k, v in c.items() if k != 'ed'}, tried=tried, best=best)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("word"); ap.add_argument("out"); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--count", action="store_true")
    a = ap.parse_args(); cs = candidates(C.load(a.word)); print("fusion2 candidates:", len(cs), "distinct (t,A,H):", len({(c['t'], c['A'], c['H']) for c in cs}), flush=True)
    if a.count: raise SystemExit
    t0 = time.time(); res = []
    with mp.get_context("fork").Pool(a.workers, initializer=init, initargs=(a.word,), maxtasksperchild=40) as pool:
        for n, r in enumerate(pool.imap_unordered(run, cs, chunksize=1), 1):
            res.append(r)
            if n % 500 == 0: print(f"  {n}/{len(cs)} {time.time()-t0:.0f}s feasible {sum(1 for x in res if x['best'])} gains {sum(1 for x in res if x['best'] and x['best']['delta'] < 0)}", flush=True)
    gains = sorted([x for x in res if x['best'] and x['best']['delta'] < 0], key=lambda x: x['best']['delta'])
    print(f"done {len(res)} in {time.time()-t0:.0f}s feasible {sum(1 for x in res if x['best'])} gains {len(gains)}")
    for x in gains[:30]: print("  gain", -x['best']['delta'], x['t'], x['A'], x['H'], x['p'], x['rest'], x['best']['steps'], x['best']['profile'])
    json.dump(res, open(a.out, "w"))
