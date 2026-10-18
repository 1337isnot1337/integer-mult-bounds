#!/usr/bin/env python3
"""Review controls for the P104 fixed-cover support cut (PR3259) and its contract.

Standard library only.  Shares no code with PR3182, PR3252, PR3259 or PR3427.
Frames are GF(2) subspaces of F_2^n held as canonical reduced-echelon keys.

  P104   rebuilds frames, covers, the 2,309-edge pool and the 4,992 required
         entries; replays PR3259's layered relaxation with a literal frame-hosting
         index (control) and evaluates the path-nested one-helper criterion
         (sharp untimed support) by two loop orders and by an independent
         full-memory recurrence in the manner of PR3252.
  ORACLE exhaustive/bounded small programs with exact Fraction coefficients.
  ROWS   three single-relaxation witnesses (unpriced; operations counted).
"""

import hashlib
import json
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUTS = {
    "research/p104-joint-unit-flags/CERTIFICATE.json":
        "a98126428a8da6eae91c50afcc42e014a284c82b554ef77e5b3a34fc6d228128",
    "research/p104-native-channel/inputs/LOWRANK-WITNESS.json":
        "0f541bef7f19fdeffd67157684e9f03d785f42c89973632f508fc1a0452b580e",
    "research/p104-native-channel/inputs/P104-FIXTURE.json":
        "516c06f6ec3cb84be588c546108de897650288576dd5fbf5fe44b9c5546ad8a4",
}


def need(ok, msg):
    if not ok:
        raise SystemExit("FAIL: " + msg)


# ---------------------------------------------------------------- GF(2) keys
def key(vectors):
    """Canonical reduced row-echelon basis (descending pivots) of a span."""
    rows = []
    for v in vectors:
        for r in rows:
            v = min(v, v ^ r)
        if v:
            rows = [min(r, r ^ v) for r in rows] + [v]
    return tuple(sorted(rows, reverse=True))


def le(small, big):
    """small <= big as subspaces (both canonical keys)."""
    return len(key(big + small)) == len(big)


def span_add(k, v):
    return key(k + (v,))


def subspaces(dim_space, k):
    """All k-dim subspaces of F_2^dim_space as tuples of basis vectors (RREF)."""
    out = []
    for piv in combinations(range(dim_space), k):
        free = [(i, j) for i, p in enumerate(piv) for j in range(p)
                if j not in piv]
        for code in range(1 << len(free)):
            rows = [1 << p for p in piv]
            for bit, (i, j) in enumerate(free):
                if code >> bit & 1:
                    rows[i] |= 1 << j
            out.append(tuple(rows))
    return out


# ---------------------------------------------------------------- P104 inputs
def load():
    data = {}
    for rel, digest in INPUTS.items():
        raw = (ROOT / rel).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == digest, "input hash " + rel)
        data[rel] = json.loads(raw)
    return [data[r] for r in INPUTS]


def frame_paths(word):
    paths = {n: [key(b)] for n, b in word["initial_frames"].items()
             if n[0] in "XY"}
    for ev in word["program"]:
        if ev[0] == "transport" and ev[1][0] in "XY":
            old, new = key(ev[2]), key(ev[3])
            need(paths[ev[1]][-1] == old and le(old, new) and
                 len(new) == len(old) + ev[4], "monotone transport " + ev[1])
            paths[ev[1]].append(new)
    for n, b in word["final_frames"].items():
        need(n not in paths or paths[n][-1] == key(b), "final frame " + n)
    need(len(paths) == 208, "104 X and 104 Y paths")
    return paths


def channel_roles(word):
    """X is never written and Y never read by the original channel."""
    writes, reads = set(), set()
    for ev in word["program"]:
        if ev[0] in ("add", "copy"):
            writes.add(ev[1][0])
            reads.add(ev[2][0])
        elif ev[0] in ("zero", "erase"):
            writes.add(ev[1][0])
    need("X" not in writes and "Y" not in reads, "immutable X / unread Y")
    return sorted(writes), sorted(reads)


def hyperplane_of(cap, functional):
    vals = [(v & functional).bit_count() & 1 for v in cap]
    j = vals.index(1)
    return key([v ^ (cap[j] if vals[i] else 0)
                for i, v in enumerate(cap) if i != j])


def covers(cert, paths):
    L = [paths["X%d" % i][0] for i in range(104)]
    H = [paths["Y%d" % i][-1] for i in range(104)]
    need(all(len(x) == 1 for x in L) and all(len(h) == 8 for h in H), "ends")
    A = [span_add(L[a // 2], v) for a, v in enumerate(
        v for row in cert["forms"]["departure"] for v in row)]
    B = [hyperplane_of(H[b // 2], f) for b, f in enumerate(
        f for row in cert["forms"]["arrival"] for f in row)]
    need(len(A) == len(B) == 208, "208 slots")
    need(all(len(x) == 2 for x in A) and all(len(x) == 7 for x in B), "dims")
    edges = [(a, b) for a in range(208) for b in range(208) if le(A[a], B[b])]
    need(len(edges) == 2309, "2,309 compatible pairs")
    return L, A, B, H, edges


def e8_ports(fixture):
    """Positive E8 roots in doubled coordinates (first nonzero > 0)."""
    roots = []
    for v in product((-2, 0, 2), repeat=8):
        if sum(x * x for x in v) == 8:
            roots.append(v)
    for v in product((-1, 1), repeat=8):
        if v.count(-1) % 2 == 0:
            roots.append(v)
    roots = [r for r in roots if next(x for x in r if x) > 0]
    need(len(roots) == 120, "120 positive roots")
    drop = {tuple(r) for k in ("F0", "C")
            for r in fixture["section4_explicit_P104"][k]}
    ports = sorted(set(roots) - drop)
    need(len(ports) == 104, "104 ports")
    return ports


def required(ports):
    """C = I - G/8 (doubled roots): support and exact values."""
    n = len(ports)
    C = [[Fraction(int(t == s)) - Fraction(sum(
        x * y for x, y in zip(ports[t], ports[s])), 8) for s in range(n)]
        for t in range(n)]
    need(C[71][102] == Fraction(-1, 2), "C[71,102] = -1/2")
    need(sum(c != 0 for row in C for c in row) == 4992, "4,992 required")
    return C


# ------------------------------------------------- per-dimension intervals
def interval(L, A, B, H, edge, d):
    a, b = edge
    return {1: (L[a // 2], L[a // 2]), 2: (A[a], A[a]),
            7: (B[b], B[b]), 8: (H[b // 2], H[b // 2])}.get(d, (A[a], B[b]))


def admits(lo, hi, frame):
    return len(frame) >= len(lo) and len(frame) <= len(hi) and \
        le(lo, frame) and le(frame, hi)


def flats_between(lo, hi, d):
    """All d-dim keys F with lo <= F <= hi (literal enumeration)."""
    if lo == hi:
        return [lo]
    comp, cur = [], lo
    for v in hi:
        nxt = span_add(cur, v)
        if len(nxt) > len(cur):
            comp.append(v)
            cur = nxt
    need(cur == hi, "complement")
    out = []
    for sub in subspaces(len(comp), d - len(lo)):
        vecs = []
        for row in sub:
            w = 0
            for i in range(len(comp)):
                if row >> i & 1:
                    w ^= comp[i]
            vecs.append(w)
        out.append(key(lo + tuple(vecs)))
    return out


# --------------------------------------- PR3259 layered relaxation (control)
def layered(geo, paths):
    L, A, B, H, edges = geo
    n = len(edges)
    direct = [sum(1 << s for s in range(104)
                  if set(paths["X%d" % s]) & set(paths["Y%d" % t]))
              for t in range(104)]
    out, state, hist, rel, wr = direct[:], [0] * n, [], [], []
    for d in range(1, 9):
        ivs = [interval(L, A, B, H, e, d) for e in edges]
        hosts, mine = {}, []
        for i, (lo, hi) in enumerate(ivs):
            fl = flats_between(lo, hi, d)
            mine.append(fl)
            for f in fl:
                hosts[f] = hosts.get(f, 0) | 1 << i
        adj = []
        for fl in mine:
            m = 0
            for f in fl:
                m |= hosts[f]
            adj.append(m)
        reads = [0] * n
        writes = [0] * n
        for kind, acc in (("X", reads), ("Y", writes)):
            for s in range(104):
                for f in paths[kind + str(s)]:
                    if len(f) == d and f in hosts:
                        m = hosts[f]
                        while m:
                            low = m & -m
                            acc[low.bit_length() - 1] |= 1 << s
                            m ^= low
        seeded = [st | r for st, r in zip(state, reads)]
        state = seeded[:]
        for i in range(n):
            if seeded[i]:
                m = adj[i]
                while m:
                    low = m & -m
                    state[low.bit_length() - 1] |= seeded[i]
                    m ^= low
        for i in range(n):
            w = writes[i]
            while w:
                low = w & -w
                out[low.bit_length() - 1] |= state[i]
                w ^= low
        hist.append(sum(1 << i for i in range(n) if state[i] >> 102 & 1))
        rel.append(adj)
        wr.append(writes)
    back = sum(1 << i for i in range(n) if wr[7][i] >> 71 & 1)
    for d in (7, 6, 5):
        grown = back
        for i in range(n):
            if back >> i & 1:
                grown |= rel[d][i]
        back = grown
    return out, [bin(h).count("1") for h in hist], back, hist[4]


# ------------------------------------ path-nested one-helper criterion (sharp)
def endpoint_masks(geo):
    L, A, B, H, edges = geo
    dep, arr = [0] * 208, [0] * 208
    for i, (a, b) in enumerate(edges):
        dep[a] |= 1 << i
        arr[b] |= 1 << i
    return dep, arr


def admit_mask(geo, masks, f):
    """Helper types whose fixed-cover flag can pass through frame f."""
    L, A, B, H, edges = geo
    dep, arr = masks
    d = len(f)
    if d in (1, 2):
        low = L if d == 1 else A
        return sum_or(dep[a] for a in range(208)
                      if (low[a // 2] if d == 1 else low[a]) == f)
    if d in (7, 8):
        return sum_or(arr[b] for b in range(208)
                      if (B[b] if d == 7 else H[b // 2]) == f)
    if 3 <= d <= 6:
        return sum_or(dep[a] for a in range(208) if le(A[a], f)) & \
            sum_or(arr[b] for b in range(208) if le(f, B[b]))
    return 0


def sum_or(masks):
    m = 0
    for x in masks:
        m |= x
    return m


def sharp_by_frames(geo, paths):
    """Method 1 (RREF keys): pair snapshots V <= W sharing a helper type."""
    masks = endpoint_masks(geo)
    frames = {f for k in "XY" for i in range(104) for f in paths[k + str(i)]}
    adm = {f: admit_mask(geo, masks, f) for f in frames}
    out = []
    for t in range(104):
        m = 0
        ys = paths["Y%d" % t]
        for s in range(104):
            xs = paths["X%d" % s]
            if set(xs) & set(ys) or any(
                    adm[v] & adm[w] and le(v, w) for v in xs for w in ys):
                m |= 1 << s
        out.append(m)
    return out


def points(k):
    """Point-set bitmap of a span (512-bit integer)."""
    pts = [0]
    for v in k:
        pts += [p ^ v for p in pts]
    return sum(1 << p for p in pts)


def sharp_by_edges(geo, paths):
    """Method 2 (point bitmaps): per helper type, admitted read/write pairs."""
    L, A, B, H, edges = geo
    bm = {n: [points(f) for f in fs] for n, fs in paths.items()}
    Lp, Ap = [points(x) for x in L], [points(x) for x in A]
    Bp, Hp = [points(x) for x in B], [points(x) for x in H]
    snaps = [(p, n) for n in bm if n[0] in "XY" for p in bm[n]
             if 2 <= p.bit_count() <= 256]
    out = [0] * 104
    for t in range(104):
        for s in range(104):
            if set(bm["X%d" % s]) & set(bm["Y%d" % t]):
                out[t] |= 1 << s
    for a, b in edges:
        flag = {2: Lp[a // 2], 4: Ap[a], 128: Bp[b], 256: Hp[b // 2]}
        ok = []
        for p, n in snaps:
            c = p.bit_count()
            if (flag.get(c) == p) if c in flag else (
                    Ap[a] & p == Ap[a] and p & Bp[b] == p):
                ok.append((p, n))
        for v, sn in ok:
            if sn[0] != "X":
                continue
            for w, tn in ok:
                if tn[0] == "Y" and v & w == v:
                    out[int(tn[1:])] |= 1 << int(sn[1:])
    return out


def full_memory(geo, paths):
    """Method 3: PR3252's full-memory recurrence, reimplemented over the whole
    pool.  Carry old memories; insert each admitted source snapshot; relay only
    old memories S over contacts as S + L(h,d) + L(w,d) when it fits both
    upper bounds; output a source at a target snapshot containing a memory.
    Memories are grouped by subspace key with a source bitmask."""
    L, A, B, H, edges = geo
    n = len(edges)
    out = [sum(1 << s for s in range(104)
               if set(paths["X%d" % s]) & set(paths["Y%d" % t]))
           for t in range(104)]
    snaps = {"X": {}, "Y": {}}
    for k in "XY":
        for i in range(104):
            for f in paths[k + str(i)]:
                snaps[k][f] = snaps[k].get(f, 0) | 1 << i
    mem = [{} for _ in range(n)]
    for d in range(1, 9):
        ivs = [interval(L, A, B, H, e, d) for e in edges]
        hosts, mine = {}, []
        for i, (lo, hi) in enumerate(ivs):
            fl = flats_between(lo, hi, d)
            mine.append(fl)
            for f in fl:
                hosts[f] = hosts.get(f, 0) | 1 << i
        nxt = [dict(m) for m in mem]
        for h in range(n):
            nb = 0
            for f in mine[h] if mem[h] else ():
                nb |= hosts[f]
            nb &= ~(1 << h)
            while nb:
                w = (nb & -nb).bit_length() - 1
                nb &= nb - 1
                for S, sm in mem[h].items():
                    T = key(S + ivs[h][0] + ivs[w][0])
                    if len(T) <= d and le(T, ivs[h][1]) and le(T, ivs[w][1]):
                        nxt[w][T] = nxt[w].get(T, 0) | sm
        for f, sm in snaps["X"].items():
            m = hosts.get(f, 0) if len(f) == d else 0
            while m:
                i = (m & -m).bit_length() - 1
                m &= m - 1
                nxt[i][f] = nxt[i].get(f, 0) | sm
        mem = [prune(m) for m in nxt]
        for f, tm in snaps["Y"].items():
            m = hosts.get(f, 0) if len(f) == d else 0
            while m:
                i = (m & -m).bit_length() - 1
                m &= m - 1
                src = sum_or(sm for S, sm in mem[i].items() if le(S, f))
                for t in range(104):
                    if tm >> t & 1:
                        out[t] |= src
    return out


def prune(m):
    """Keep, per source, only subset-minimal memories (outputs unchanged)."""
    keep = {}
    for S in sorted(m, key=len):
        sm = m[S]
        for S2, sm2 in keep.items():
            if len(S2) < len(S) and le(S2, S):
                sm &= ~sm2
        if sm:
            keep[S] = sm
    return keep


def missing(C, support):
    return [(t, s) for t in range(104) for s in range(104)
            if C[t][s] != 0 and not support[t] >> s & 1]


def p104():
    cert, word, fixture = load()
    paths = frame_paths(word)
    roles = channel_roles(word)
    geo = covers(cert, paths)
    C = required(e8_ports(fixture))
    lay, fwd, back, f5 = layered(geo, paths)
    miss_l = missing(C, lay)
    need(miss_l == [(71, 102)], "layered relaxation misses only (71,102)")
    need(fwd == [16, 25, 52, 365, 1725, 2283, 2285, 2297], "forward cone")
    need(bin(back).count("1") == 37 and back & f5 == 0, "backward 37, disjoint")
    sharp = sharp_by_frames(geo, paths)
    need(sharp == sharp_by_edges(geo, paths), "sharp criterion: two loop orders")
    need(sharp == full_memory(geo, paths), "PR3252 full-memory test = sharp")
    need(all(sharp[t] & ~lay[t] == 0 for t in range(104)), "sharp <= layered")
    return {"roles": roles, "geo": geo, "paths": paths, "C": C,
            "layered": lay, "sharp": sharp, "missing_layered": miss_l,
            "missing_sharp": missing(C, sharp), "forward": fwd}


# ------------------------------------------------ sensitivity rows (support)
def channel_states(word):
    """Structural X-dependence of every original-channel register per frame."""
    frame, dep, hist = {}, {}, {}
    for n, b in word["initial_frames"].items():
        frame[n] = key(b)
        dep[n] = 1 << int(n[1:]) if n[0] == "X" else 0
        hist[n] = {frame[n]: dep[n]}
    for ev in word["program"]:
        n = ev[1]
        if ev[0] == "transport":
            frame[n] = key(ev[3])
        elif ev[0] == "add":
            dep[n] |= dep[ev[2]]
        elif ev[0] == "copy":
            frame[n], dep[n] = key(ev[3]), dep[ev[2]]
        elif ev[0] == "zero":
            frame[n], dep[n] = key(ev[2]), 0
        # erase: keep dependence (over-approximation; no cancellation used)
        hist.setdefault(n, {})
        hist[n][frame[n]] = hist[n].get(frame[n], 0) | dep[n]
    return hist


def rows(r, word):
    geo, paths, ms = r["geo"], r["paths"], set(r["missing_sharp"])
    masks, adm = endpoint_masks(geo), {}

    def hop(v, w):
        for f in (v, w):
            if f not in adm:
                adm[f] = admit_mask(geo, masks, f)
        return v == w or (adm[v] & adm[w] and le(v, w))

    def count(sup):
        return sum(1 for t, s in ms if sup[t] >> s & 1), bool(sup[71] >> 102 & 1)

    hist = channel_states(word)
    ys = [(t, j, w) for t in range(104) for j, w in enumerate(paths["Y%d" % t])]
    xin = {(t, j): sum(1 << s for s in range(104) if any(
        hop(v, w) for v in paths["X%d" % s])) for t, j, w in ys}

    def relay(seed):
        inn = dict(seed)
        changed = True
        while changed:
            changed = False
            for u, k, wu in ys:
                avail = 0
                for kk in range(k + 1):
                    avail |= inn[(u, kk)]
                for t, j, wt in ys:
                    if t != u and avail & ~inn[(t, j)] and hop(wu, wt):
                        inn[(t, j)] |= avail
                        changed = True
        sup = [0] * 104
        for (t, j), m in inn.items():
            sup[t] |= m
        return sup

    r1 = relay(xin)
    r1c = relay({(t, j): xin[(t, j)] | hist["Y%d" % t].get(w, 0)
                 for t, j, w in ys})
    free = [sum(1 << s for s in range(104) if any(
        1 <= len(v) <= len(w) <= 8 and le(v, w)
        for v in paths["X%d" % s] for w in paths["Y%d" % t]))
        for t in range(104)]
    old = [(n, f, m) for n, h in hist.items() if n[0] not in "XY"
           for f, m in h.items() if m]
    r3 = [0] * 104
    for n, f, m in old:
        for t in range(104):
            if any(hop(f, w) for w in paths["Y%d" % t]):
                r3[t] |= m
    w2 = [(len(v), len(w)) for v in paths["X102"] for w in paths["Y71"]
          if 1 <= len(v) <= len(w) <= 8 and le(v, w)]
    w3 = sorted({(n, len(f)) for n, f, m in old if m >> 102 & 1 and
                 any(hop(f, w) for w in paths["Y71"])})
    # target feedback: first Y71 snapshot whose channel increments hold X102
    w1c = [len(f) for f in paths["Y71"]
           if hist["Y71"].get(f, 0) >> 102 & 1][:1]
    return {"R1_correction_only_Y_relay": count(r1),
            "R1c_Y_relay_with_channel_content": count(r1c),
            "R2_free_nested_flags": count(free),
            "R3_old_channel_helper_reads": count(r3),
            "R2_witness_dims": w2, "R3_witness_states": w3,
            "R1c_witness_reads": w1c}


# ------------------------------------------- consequence for PR3427's rank
def frac_rank(rows):
    a, rk = [list(r) for r in rows], 0
    for c in range(len(a[0]) if a else 0):
        p = next((i for i in range(rk, len(a)) if a[i][c] != 0), None)
        if p is None:
            continue
        a[rk], a[p] = a[p], a[rk]
        for i in range(len(a)):
            if i != rk and a[i][c] != 0:
                f = a[i][c] / a[rk][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[rk])]
        rk += 1
    return rk


def bareiss_det(m):
    """Exact integer determinant by fraction-free elimination."""
    a, n, sign, prev = [r[:] for r in m], len(m), 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            p = next((i for i in range(k + 1, n) if a[i][k]), None)
            if p is None:
                return 0
            a[k], a[p], sign = a[p], a[k], -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1]


def greedy_rectangle(sharp, C):
    """Deterministic greedy: for each seed column grow S while the common
    unsupported row set R keeps min(|R|,|S|) increasing; keep max rank."""
    n = len(C)
    uns = [[not sharp[t] >> s & 1 for s in range(n)] for t in range(n)]
    best = (0, (), ())
    for s0 in range(n):
        S, R = [s0], [t for t in range(n) if uns[t][s0]]
        while True:
            cand = sorted(((min(len(r2), len(S) + 1), len(r2), -s, r2)
                           for s in range(n) if s not in S
                           for r2 in [[t for t in R if uns[t][s]]]),
                          reverse=True)
            if not cand or cand[0][0] <= min(len(R), len(S)):
                break
            S.append(-cand[0][2])
            R = cand[0][3]
        rk = frac_rank([[C[t][s] for s in S] for t in R])
        if rk > best[0]:
            best = (rk, tuple(sorted(R)), tuple(sorted(S)))
    return best


RANK_ROWS = (2, 4, 5, 13, 15, 25, 32, 36, 39, 48, 52, 73, 76, 82, 87, 89,
             94, 98, 102)
RANK_COLS = (2, 5, 11, 13, 15, 16, 20, 25, 28, 32, 40, 48, 61, 65, 76, 84,
             94, 102)
MINOR_ROWS = (2, 4, 5, 13, 15, 25, 32, 36, 39, 48, 52, 73, 76, 82, 87, 94,
              102)
MINOR_COLS = (2, 5, 11, 13, 15, 16, 20, 25, 28, 32, 40, 48, 61, 65, 76, 94,
              102)


def rank_consequence(r):
    """Any D = U^-1 - G/2 vanishes on unsupported pairs, so on an unsupported
    rectangle (U^-1 - I)[R,S] = -C[R,S] and rank(U - I) >= rank C[R,S]."""
    sharp, C = r["sharp"], r["C"]
    need(all(not sharp[t] >> s & 1 for t in RANK_ROWS for s in RANK_COLS),
         "rectangle unsupported")
    need(greedy_rectangle(sharp, C) == (17, RANK_ROWS, RANK_COLS),
         "greedy rectangle")
    rk = frac_rank([[C[t][s] for s in RANK_COLS] for t in RANK_ROWS])
    det = bareiss_det([[int(8 * C[t][s]) for s in MINOR_COLS]
                       for t in MINOR_ROWS])
    need(rk == 17 and det != 0, "rank 17 by elimination and a nonzero minor")
    return rk, det


# ------------------------------------------------- small-domain oracle
class Rng:
    """Deterministic LCG so the oracle needs no stdlib random state."""

    def __init__(self, seed):
        self.x = seed

    def below(self, n):
        self.x = (self.x * 6364136223846793005 + 1442695040888963407) % 2**64
        return (self.x >> 33) % n

    def coef(self):
        return Fraction(self.below(19) + 1, self.below(7) + 1) * (
            -1 if self.below(2) else 1)


def grow(rng, n, low, high, d):
    """Random d-dim key between low and high (low <= high)."""
    cur = low
    while len(cur) < d:
        v = rng.below(1 << n)
        if le((v,), high):
            cur = span_add(cur, v)
    return cur


def instance(rng, n, nx=3, ny=3, nt=3, rigid=False):
    full = key([1 << i for i in range(n)])
    zero = ()

    def chain(start_dim, end_dim):
        out = [grow(rng, n, zero, full, start_dim)]
        while len(out[-1]) < end_dim:
            step = 1 + rng.below(end_dim - len(out[-1]))
            out.append(grow(rng, n, out[-1], full, len(out[-1]) + step))
        return out
    xs = [chain(1, n) for _ in range(nx)]
    ys = [chain(0, n - 1) for _ in range(ny)]
    types = []
    pairs = [(a, b) for c in xs for a in c for e in ys for b in e
             if 1 <= len(a) < len(b) and le(a, b)]
    for _ in range(nt):
        flag = [zero]
        if pairs and rng.below(2):  # thread the flag through a read/write pair
            a, b = pairs[rng.below(len(pairs))]
            while len(flag[-1]) < len(a):
                flag.append(grow(rng, n, flag[-1], a, len(flag[-1]) + 1))
            while len(flag[-1]) < len(b):
                flag.append(grow(rng, n, flag[-1], b, len(flag[-1]) + 1))
        for d in range(len(flag), n + 1):
            flag.append(grow(rng, n, flag[-1], full, d))
        fixed = {0: zero, n: full}
        for d in range(1, n):
            if rigid or rng.below(2):
                fixed[d] = flag[d]
        types.append(fixed)
    return n, xs, ys, types


def type_interval(fixed, d):
    lo = max((k for k in fixed if k <= d))
    hi = min((k for k in fixed if k >= d))
    return fixed[lo], fixed[hi]


def small_admit(fixed, f):
    lo, hi = type_interval(fixed, len(f))
    return le(lo, f) and le(f, hi)


def small_sharp(inst):
    n, xs, ys, types = inst
    sup = set()
    for s, xc in enumerate(xs):
        for t, yc in enumerate(ys):
            if set(xc) & set(yc) or any(
                    le(v, w) and any(small_admit(ty, v) and small_admit(ty, w)
                                     for ty in types)
                    for v in xc for w in yc if 1 <= len(v) <= len(w) <= n - 1):
                sup.add((t, s))
    return sup


def small_layered(inst):
    n, xs, ys, types = inst
    sup = {(t, s) for s, xc in enumerate(xs) for t, yc in enumerate(ys)
           if set(xc) & set(yc)}
    state = [set() for _ in types]
    for d in range(1, n):
        fl = [set(flats_between(*type_interval(ty, d), d)) for ty in types]
        reads = [{s for s, xc in enumerate(xs) if fl[i] & set(xc)}
                 for i in range(len(types))]
        seeded = [state[i] | reads[i] for i in range(len(types))]
        state = [set().union(*(seeded[j] for j in range(len(types))
                               if fl[i] & fl[j])) for i in range(len(types))]
        for i in range(len(types)):
            for t, yc in enumerate(ys):
                if fl[i] & set(yc):
                    sup |= {(t, s) for s in state[i]}
    return sup


def helper_flag(rng, inst, ty):
    """Random full flag through the type's fixed members, biased toward
    X/Y snapshot frames so that contacts actually occur."""
    n, xs, ys, _ = inst
    snaps = {f for c in xs + ys for f in c}
    flag = [()]
    for d in range(1, n + 1):
        lo, hi = type_interval(ty, d)
        base = key(flag[-1] + lo)
        hits = sorted(f for f in snaps if len(f) == d and le(base, f)
                      and le(f, hi))
        if hits and rng.below(8):
            flag.append(hits[rng.below(len(hits))])
        else:
            flag.append(grow(rng, n, base, hi, d))
    return flag


def run_program(rng, inst, steps, violate=None, direct=True):
    """Random straight-line program choosing uniformly among the operations
    legal at each moment; returns its nonzero source->target pairs."""
    n, xs, ys, types = inst
    full = key([1 << i for i in range(n)])
    nh = 4
    tys = [{0: (), n: full} if violate == "offcover"
           else types[rng.below(len(types))] for _ in range(nh)]
    flags = [helper_flag(rng, inst, ty) for ty in tys]
    pos, xp, yp = [0] * nh, [0] * len(xs), [0] * len(ys)
    hv = [{("D", h): Fraction(1)} for h in range(nh)]
    yv = [{} for _ in ys]
    extra = None
    if violate == "oldstate":
        f = [c for c in xs + ys for c in c if 1 <= len(c) < n]
        extra = (f[rng.below(len(f))], {("X", rng.below(len(xs))): Fraction(1)})

    def axpy(dst, c, src):
        for k, v in src.items():
            dst[k] = dst.get(k, 0) + c * v
            if dst[k] == 0:
                del dst[k]
    for _ in range(steps):
        fr = [flags[h][pos[h]] for h in range(nh)]
        xf = [xs[i][xp[i]] for i in range(len(xs))]
        yf = [ys[j][yp[j]] for j in range(len(ys))]
        acts = [("xadv", i) for i in range(len(xs)) if xp[i] + 1 < len(xs[i])]
        acts += [("yadv", j) for j in range(len(ys)) if yp[j] + 1 < len(ys[j])]
        for h in range(nh):
            ups = range(pos[h] + 1, n + 1)
            if violate == "descent":
                ups = [p for p in range(n + 1) if p != pos[h]]
            if ups:  # one transport action per helper; target drawn later
                acts.append(("tr", h, list(ups)))
            acts += [("read", h, i) for i in range(len(xs)) if fr[h] == xf[i]]
            acts += [("write", h, j) for j in range(len(ys)) if fr[h] == yf[j]]
            acts += [("mix", h, g) for g in range(nh) if g != h and (
                fr[h] == fr[g] or violate == "crossframe")]
            if violate == "yread":
                acts += [("yread", h, j) for j in range(len(ys))
                         if fr[h] == yf[j]]
            if extra and fr[h] == extra[0]:
                acts.append(("old", h))
        acts += [("direct", i, j) for i in range(len(xs))
                 for j in range(len(ys)) if direct and xf[i] == yf[j]]
        act = acts[rng.below(len(acts))]
        c = rng.coef()
        if act[0] == "xadv":
            xp[act[1]] += 1
        elif act[0] == "yadv":
            yp[act[1]] += 1
        elif act[0] == "tr":
            pos[act[1]] = act[2][rng.below(len(act[2]))]
            hv[act[1]] = {k: c * v for k, v in hv[act[1]].items()}
        elif act[0] == "read":
            axpy(hv[act[1]], c, {("X", act[2]): Fraction(1)})
        elif act[0] == "write":
            axpy(yv[act[2]], c, hv[act[1]])
        elif act[0] == "mix":
            axpy(hv[act[2]], c, hv[act[1]])
        elif act[0] == "yread":
            axpy(hv[act[1]], c, yv[act[2]])
        elif act[0] == "old":
            axpy(hv[act[1]], c, extra[1])
        else:
            axpy(yv[act[2]], c, {("X", act[1]): Fraction(1)})
    return {(t, k[1]) for t in range(len(ys)) for k in yv[t] if k[0] == "X"}


def y_relay_counterexample():
    """Minimal F_2^3 program: reading a target relays X0 outside both tests.

    e1,e2,e3 = 1,2,4.  X0: <e1> -> FULL.  Y0: 0 -> <e1> -> <e1,e2>.
    Y1: 0 -> <e1,e2>.  Type T1 fixes <e1> < <e1,e3>; type T2 fixes
    <e2> < <e1,e2>.  h1 (T1) reads X0 at <e1> and writes Y0 there; Y0 is
    transported by the frozen channel; h2 (T2, dim-2 frame <e1,e2>) reads
    Y0 and writes Y1.  Four scalar operations; coefficient c1*c2*c3*c4.
    """
    full = key([1, 2, 4])
    t1 = {0: (), 1: key([1]), 2: key([1, 4]), 3: full}
    t2 = {0: (), 1: key([2]), 2: key([1, 2]), 3: full}
    inst = (3, [[key([1]), full]], [[(), key([1]), key([1, 2])],
                                     [(), key([1, 2])]], [t1, t2])
    c = [Fraction(2), Fraction(-3), Fraction(5, 7), Fraction(-1, 2)]
    need(inst[1][0][0] == t1[1], "h1 reads X0 at its line")
    h1 = c[0]                                   # h1 += c0 * X0  at <e1>
    y0 = c[1] * h1                              # Y0 += c1 * h1  at <e1>
    need(inst[2][0][2] == t2[2], "Y0 later frame equals h2 frame")
    h2 = c[2] * y0                              # h2 += c2 * Y0  at <e1,e2>
    y1 = c[3] * h2                              # Y1 += c3 * h2  at <e1,e2>
    need(y1 != 0, "nonzero relayed coefficient")
    sharp, lay = small_sharp(inst), small_layered(inst)
    need((1, 0) not in sharp and (1, 0) not in lay, "Y relay escapes")
    return (1, True)


def oracle(seed=20261018, trials=((3, 3000), (4, 1500)), steps=120):
    rng = Rng(seed)
    checked = {"programs": 0, "nonzero_coefficients": 0, "strict_gap": 0,
               "helper_mediated": 0}
    for n, count in trials:
        for _ in range(count):
            inst = instance(rng, n)
            sharp, lay = small_sharp(inst), small_layered(inst)
            need(sharp <= lay, "oracle: sharp support inside layered")
            checked["strict_gap"] += sharp < lay
            # Direct X->Y adds are seeded identically by both tests; omit
            # them so every coefficient is carried by helper paths.
            got = run_program(rng, inst, steps, direct=False)
            need(got <= sharp, "oracle: legal coefficient outside sharp test")
            checked["programs"] += 1
            checked["nonzero_coefficients"] += len(got)
            checked["helper_mediated"] += sum(
                not set(inst[1][s]) & set(inst[2][t]) for t, s in got)
    escapes = {"yread": y_relay_counterexample()}
    for bad in ("descent", "crossframe", "offcover", "oldstate"):
        found = None
        for attempt in range(1, 4001):
            inst = instance(rng, 3 + attempt % 2, rigid=True)
            got = run_program(rng, inst, steps, bad)
            if not got <= small_sharp(inst):
                found = (attempt, not got <= small_layered(inst))
                break
        need(found is not None, "negative control has no teeth: " + bad)
        escapes[bad] = found
    return checked, escapes


PR3427_SOURCE_MASKS = (  # published per-source target masks, sources 0..3
    0x15088a1021120142242d061684, 0x1504102110011204022d109084,
    0x1b0000480c4084800021001083, 0x2a889524212d01425a52a06020)


def main():
    r = p104()
    sharp = r["sharp"]
    for s, mask in enumerate(PR3427_SOURCE_MASKS):
        need(sum(1 << t for t in range(104) if sharp[t] >> s & 1) == mask,
             "PR3427 four-column support masks")
    ms = r["missing_sharp"]
    need(len(ms) == 2682 and (71, 102) in ms, "2,682 sharp-missing entries")
    need(len({t for t, _ in ms}) == 104 and len({s for _, s in ms}) == 104,
         "every row and column has a sharp-missing entry")
    need(sum(bin(m).count("1") for m in sharp) == 2310 and
         sum(bin(m).count("1") for m in r["layered"]) == 10815, "support sizes")
    _, word, _ = load()
    rw = rows(r, word)
    need(rw["R1_correction_only_Y_relay"] == (0, False), "R1")
    need(rw["R1c_Y_relay_with_channel_content"] == (2682, True), "R1c")
    need(rw["R2_free_nested_flags"] == (2682, True), "R2")
    need(rw["R3_old_channel_helper_reads"] == (2682, True), "R3")
    need(rw["R2_witness_dims"] == [(1, 8)], "R2 witness")
    need(rw["R3_witness_states"] == [("D11", 5)], "R3 witness")
    need(rw["R1c_witness_reads"] == [5], "R1c feedback witness")
    rk, det = rank_consequence(r)
    checked, escapes = oracle()
    need(checked == ORACLE_EXPECTED, "oracle receipt %r" % (checked,))
    need(escapes == ESCAPES_EXPECTED, "negative controls %r" % (escapes,))
    print(json.dumps({"channel_roles": r["roles"], "layered_missing":
                      r["missing_layered"], "forward_cone": r["forward"],
                      "rank_bound": rk, "minor_det_8C": det,
                      "sharp_missing": len(ms), "rows": rw, "oracle": checked,
                      "negative_controls": escapes}, sort_keys=True))
    print("PASS_P104_FIXED_COVER_CUT_REVIEW layered_missing=1 "
          "sharp_missing=2682 of 4992 pr3427_masks=4 rank_U_minus_I>=17 "
          "rows=4 oracle_programs=%d no_kappa" % checked["programs"])


ORACLE_EXPECTED = {"programs": 4500, "nonzero_coefficients": 269,
                   "strict_gap": 3556, "helper_mediated": 107}
ESCAPES_EXPECTED = {"yread": (1, True), "descent": (1, True),
                    "crossframe": (7, True), "offcover": (184, True),
                    "oldstate": (144, True)}

if __name__ == "__main__":
    main()
