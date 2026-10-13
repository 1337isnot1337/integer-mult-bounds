"""joint2: generalized triangle-hybrid / source-holder family per copy pair (superset of joint.py).

Differences from joint.py: (1) the holder donation position p ranges over EVERY gap class (positions between consecutive
B events touching H or src) in the window where src keeps the value t read and H is neither read by another register nor
scaled before t's read of H; (2) restores range over every B gap class after t's read of H up to the next read/scale of H or
write of src, every early-tail position class, and the FULL prepend; (3) each movable read independently chooses
keep / swap / fuse(option) (cartesian product).  Exactness is re-checked by harness.Pricer (mod p) and frames solved exactly.
usage: python -B joint2.py WORD.json.gz OUT.json [--workers N] [--count]"""
import argparse, itertools, json, multiprocessing as mp, time, collections
from fractions import Fraction as Q
import harness as C
from fusion import index, dyadic, any_in
from exchange import copy_pairs, movable_reads, is_target
from joint import swap_edit, merge
def reads_of(B, t):
    return [(i, e[2], Q(e[3], e[4])) for i, e in enumerate(B) if e[0] == 'add' and e[1] == t]
def gap_classes(events, lo, hi):
    """representative insertion positions in [lo, hi]: one per gap between consecutive events (position = event index + 1)."""
    pts = sorted({lo} | {x + 1 for x in events if lo <= x + 1 <= hi})
    return pts
def holder_options(w, I, m, h, r, ic):
    j, t, src, (a0, b0) = m; a = Q(a0, b0); B = I['B']; nB = len(B); out = []
    for (iH, H, cH) in reads_of(B, t):
        if iH == j or H in (h, r, t): continue
        q = a / cH
        if not dyadic(q): continue
        lo_t, hi_t = min(j, iH), max(j, iH)
        if any_in(I['RD'][t] + I['SC'][t], lo_t, hi_t + 1): continue
        othersH = [x for x in I['RD'][H] + I['SC'][H] if x != iH]
        # donation window: p <= iH, no other read/scale of H in [p, iH), src unchanged between p and j
        lo = max([x + 1 for x in othersH if x < iH] + [ic + 1 if src == h else 0])
        lo = max(lo, max([x + 1 for x in I['W'][src] if x < min(j, iH)], default=0)) if j < iH else lo
        if j < iH: lo = max(lo, max([x + 1 for x in I['W'][src] if x < j], default=0))
        else: lo = max(lo, j + 1) if any_in(I['W'][src], j + 1, iH) else lo
        if lo > iH: continue
        ev = set(I['W'][H]) | set(I['W'][src]) | set(I['RD'][src]) | set(othersH)
        for p in gap_classes(ev, lo, iH):
            if j < iH and p <= j and any_in(I['W'][src], p, j): continue
            if (j < iH and p > j and any_in(I['W'][src], j + 1, p)) or (j > iH and any_in(I['W'][src], p, j)): continue
            g = ['add', H, src, q.numerator, q.denominator, []]; gr = ['add', H, src, -q.numerator, q.denominator, []]
            nxt = min([x for x in othersH if x > iH] + [x for x in I['W'][src] if x > iH] + [nB])
            rs = []
            for rp in gap_classes(ev, iH + 1, nxt):
                if any_in(I['W'][src], p, rp): continue
                rs.append(("B%d" % rp, dict(insert=[(p, g), (rp, gr)])))
            if not any_in(I['W'][src], p, nB) and not any_in(othersH, iH + 1, nB):
                jmax = min(I['TW'][src] + I['TR'][H] + [len(I['T'])])
                tev = {k for k, e in enumerate(I['T']) if H in C.regs(e) or src in C.regs(e)}
                for tp in sorted({0, jmax} | {k + 1 for k in tev if k + 1 <= jmax}): rs.append(("T%d" % tp, dict(insert=[(p, g)], tail=[(tp, gr)])))
                if src not in I['low'] and H not in I['low'] and not I['TW'][src] and not I['TR'][H]: rs.append(("P", dict(insert=[(p, g)], prepend=[gr])))
            for tag, e in rs:
                ed = dict(delete=[j], insert=e.get('insert', []), tail=e.get('tail', []), prepend=e.get('prepend', []))
                out.append((dict(H=H, iH=iH, p=p, rest=tag), ed))
    return out
def candidates(w):
    I = index(w); out = []
    for h, (r, ic) in copy_pairs(w).items():
        M = movable_reads(w, h, r, ic)
        if not M: continue
        choices = []
        for m in M:
            ch = [("keep", None, dict(delete=[], insert=[], tail=[], prepend=[]))]
            s = swap_edit(w, h, r, ic, m)
            if s: ch.append(("swap", None, s))
            ch += [("fuse", o, e) for o, e in holder_options(w, I, m, h, r, ic)]
            choices.append(ch)
        for combo in itertools.product(*choices):
            if all(c[0] == "keep" for c in combo): continue
            if not any(c[0] == "fuse" for c in combo): continue          # pure exchanges: xsweep.py
            ed = merge([c[2] for c in combo])
            if ed is None: continue
            out.append(dict(h=h, r=r, choice=[(m[0], m[1], m[2], c[0], c[1]) for m, c in zip(M, combo)], ed=ed))
    return out
P = None
def init(path):
    global P
    P = C.Pricer(path)
def run(c):
    x = P.price(c['ed'], timeout=120)
    return dict(c, status=x.get('status'), delta=x.get('delta'), profile=x.get('profile'))
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("word"); ap.add_argument("out"); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--count", action="store_true"); ap.add_argument("--pairs", default=""); ap.add_argument("--skip", default="")
    a = ap.parse_args(); w = C.load(a.word); cs = candidates(w)
    if a.pairs: cs = [c for c in cs if str(c['h']) in a.pairs.split(",")]
    if a.skip:
        done = {json.dumps(r["ed"], sort_keys=True) for r in json.load(open(a.skip))}; n0 = len(cs)
        cs = [c for c in cs if json.dumps(json.loads(json.dumps(c["ed"])), sort_keys=True) not in done]; print("skipped", n0 - len(cs))
    per = collections.Counter(c['h'] for c in cs); print("joint2 candidates:", len(cs), dict(per), flush=True)
    if a.count: raise SystemExit
    t0 = time.time(); res = []
    with mp.get_context("fork").Pool(a.workers, initializer=init, initargs=(a.word,), maxtasksperchild=40) as pool:
        for n, r in enumerate(pool.imap_unordered(run, cs, chunksize=1), 1):
            res.append(r)
            if n % 200 == 0: print(f"  {n}/{len(cs)} {time.time()-t0:.0f}s gains {sum(1 for x in res if x['delta'] is not None and x['delta'] < 0)}", flush=True)
    st = collections.Counter(r['status'] for r in res)
    gains = sorted([r for r in res if r['delta'] is not None and r['delta'] < 0], key=lambda r: r['delta'])
    print(f"done {len(res)} in {time.time()-t0:.0f}s status {dict(st)} gains {len(gains)}")
    for g in gains[:40]: print("  gain", -g['delta'], "pair", g['h'], g['r'], g['choice'], g['profile'])
    json.dump(res, open(a.out, "w"))
