#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent second method for the retained-array catch-up package.

Shares no code with verify.py and does not import ceiling.py.

 A. Frames as explicit coordinate sets.  The base (non-replica) template schedule in the PR2346-
    pinned #1042 archive is replayed with each pair's applied coordinates stored as a Python set:
    a local call applies its stage's eight coordinates; an idle sweep applies rank/8 stage blocks
    taken from the idle child RANKS (its from/to level fields are only cross-checked, not used).
    A record snapshots its family's set; catch-up = |consumer set - record set| x rows
    (the PR1664 nested-frame distance).  Recomputes PR2540, INIT64, d_A and the zero witness.
 B. Moment arithmetic with decimal.Decimal at 80 digits (ln/exp from the decimal module):
    the no-saving threshold, the #1166 break-evens 573 / 71 against PR2474, and the route verdicts.
 C. Exact frame model by a different algorithm: Dijkstra over per-level reduced echelon bases
    (membership by Gaussian elimination, not span enumeration), with the meeting-level formula
    computed from ranks by elimination, on the complete GF(2)^2 / 4-level record-partner domain.

Run from the repository root:  python3 -I -B research/retained-array-catch-up/independent_check.py
Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5).
"""
import gzip
import hashlib
import heapq
import io
import itertools
import json
import sys
import tarfile
from decimal import Decimal as D, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ("research/community-frontier1042-audit/selected-replay.tar.gz",
           "22c3f4dce4b897a1d423d1388801933e288b6a6b1906cb15e1b16a5eb68db754")
MEMBER = ("t16/global/base/split-centres/GLOBAL-TEMPLATE.json.gz",
          "a179dad87651aba340a5a8ddbcd86a8e757cad87b8a1f8bad48106fbecd38518")
HOSTED = ("research/community-frontier1094-audit/selected-replay.tar.gz",
          "f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6",
          "candidate/strict/global/hosted/GLOBAL-TEMPLATE.json.gz",
          "2acf02b418078e37090495c601fe550448751d4f35912757b13a1f778efc7760")
PR2540_PROOF = ("research/qq16-complete-native-decoder/PROOF.md",
                "09d587f1d6bc250e90e29fa8751a40f45be79f1a8a56af0b645c144cefaefa46")


class Fail(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Fail(message)


# ------------------------------------------------------------------ A. coordinate sets
def template():
    raw = (ROOT / ARCHIVE[0]).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == ARCHIVE[1], "archive pin")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        member = tar.getmember(MEMBER[0])
        data = tar.extractfile(member).read()
    need(hashlib.sha256(data).hexdigest() == MEMBER[1], "template member pin")
    return json.loads(gzip.decompress(data))


def pr2540_frames():
    text = (ROOT / PR2540_PROOF[0]).read_text(encoding="utf-8")
    need(hashlib.sha256(text.encode("utf-8")).hexdigest() == PR2540_PROOF[1], "PR2540 proof pin")
    need("F_L=product_(j=0,...,8)" in text and "U1=<e0,...,e16>" in text, "PR2540 frame statements")
    f_l = set(range(0, 8 + 1))          # axes e0..e8
    f_u1 = set(range(0, 16 + 1))        # axes e0..e16
    need(f_l < f_u1, "nested frames")
    return len(f_u1 - f_l)


def coordinate_replay(t):
    stage_pair = {}
    for e in t["recipe"]:
        if e["kind"] == "local":
            stage_pair[e["stage"]] = e["pair"]
    rank = {c["child"]: c["rank"] for c in t["idle_children"] if c["port"] == 0}
    applied = {p: set() for p in range(4)}           # applied (stage block, axis) coordinates
    next_block = {p: 0 for p in range(4)}            # stage blocks are applied in order 0..8
    snapshots = [("entry", {p: frozenset(s) for p, s in applied.items()})]
    for e in t["execution_schedule"][:30]:
        kind = e["kind"]
        if kind == "local_cover_sweep":
            p = stage_pair[e["stage"]]
            need(next_block[p] == e["stage"], "local call applies the next stage block")
            applied[p] |= {(e["stage"], a) for a in range(8)}
            next_block[p] += 1
        elif kind == "idle_cover_sweep":
            p = e["pair"]
            ranks = [rank.get(c, 0) for c in e["child_indices"]]
            need(ranks[0] == ranks[1] and ranks[0] % 8 == 0, "idle child pair of equal multiple-of-8 rank")
            blocks = ranks[0] // 8
            need(e["from_level"] + 1 == next_block[p] and e["to_level"] == next_block[p] - 1 + blocks,
                 "declared idle levels agree with rank/8 blocks")
            for b in range(next_block[p], next_block[p] + blocks):
                applied[p] |= {(b, a) for a in range(8)}
            next_block[p] += blocks
        snapshots.append((kind, {p: frozenset(s) for p, s in applied.items()}))
    need(all(len(s) == 72 for s in applied.values()), "every pair ends with 72 applied coordinates")
    return snapshots, stage_pair


def law(snapshots, stage_pair, t):
    sched = t["execution_schedule"][:30]
    end = snapshots[-1][1]
    before = lambda i: snapshots[i][1]           # state before schedule entry i
    after = lambda i: snapshots[i + 1][1]
    gap = lambda rec, cons, p: len(cons[p] - rec[p])
    local_idx = {k: [i for i, e in enumerate(sched) if e["kind"] == "local_cover_sweep"
                     and stage_pair[e["stage"]] == k] for k in range(4)}
    out = {"PR2540": 16 * gap(after(0), after(1), 0)}
    out["INIT"] = [16 * gap(before(local_idx[k][0]), end, k) for k in range(4)]
    out["dA"] = [8 * gap(after([i for i in local_idx[k] if sched[i]["stage"] % 2][0]), end, k) for k in range(3)]
    touch = min(i for i, e in enumerate(sched) if
                (e["kind"] == "local_cover_sweep" and stage_pair[e["stage"]] == 3) or
                (e["kind"] == "idle_cover_sweep" and e["pair"] == 3 and e["to_level"] > e["from_level"]) or
                (e["kind"] == "bridge" and 3 in (e["src"], e["dst"])))
    out["zero_witness"] = (gap(snapshots[0][1], before(touch), 3),
                           sum(1 for e in sched[:touch] if e["kind"] == "local_cover_sweep"))
    return out


# ------------------------------------------------------------------ B. Decimal moments
getcontext().prec = 80
M, W = D(73), D(896) / D(9)
R_IDLE = 51


def child(r, a):
    return (D(r) / M) ** (1 - a) if r else D(0)


def relax(local, extra_rank8, extra_units, a):
    """Per-call moment: QQ16 5F+4B words, extra mass, idle remainder as rank-51 mass."""
    total = 72 * W + extra_units
    mass = sum(D(r) * n for r, n in local.items()) + 8 * extra_rank8
    idle = total - mass
    need(idle >= 0, "coverage law")
    s = sum(n * child(r, a) for r, n in local.items()) + extra_rank8 * child(8, a) + idle / R_IDLE * child(R_IDLE, a)
    return s / W


def qq16_words():
    core = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82}
    return {r: (5 * (n + (8 if r == 1 else 0)) + 4 * (n + (24 if r == 1 else 0))) / D(9) for r, n in core.items()}


def gains(units, pricing, kappa):
    a = kappa / (1 - kappa)
    local = qq16_words()
    per_call = D(units) / D(9)
    value = relax(local, per_call / 8 if pricing == "rank8" else D(0), per_call, a)
    return value < 1, abs(value - 1)


def decimal_checks():
    pr2474 = D("0.001703676387993676")
    out = {}
    for pricing, step, expect in (("idle", 1, 573), ("rank8", 8, 71)):
        ok_lo, m_lo = gains(expect * step, pricing, pr2474)
        ok_hi, m_hi = gains((expect + 1) * step, pricing, pr2474)
        need(ok_lo and not ok_hi, "break-even %s = %d" % (pricing, expect))
        need(min(m_lo, m_hi) > D(10) ** -40, "decision margin far above precision")
        out["breakeven_" + pricing] = expect
    # No positive saving, exactly (rationals): at a = 0 every child costs r/m, so the moment is
    # total/(m w) = (72 w + u/9)/(73 w), which is >= 1 iff u >= 9 w = 896 units per replica; and
    # every child cost (r/m)^(1-a) >= r/m for a >= 0, so the moment only grows with a.
    from fractions import Fraction as F
    w = F(896, 9)
    need(all(((72 * w + F(u, 9)) / (73 * w) >= 1) == (u >= 896) for u in range(0, 2000)), "896 threshold")
    local = qq16_words()
    for units in (3648, 3712, 1952, 960):
        need(relax(local, 0, D(units) / 9, D(0)) > 1, "no saving at %d" % units)
    ok, _ = gains(464, "idle", D("0.00221"))
    need(ok, "S-priced 464 array-calls keeps the #1166 ceiling above 0.00221")
    out["threshold"] = 896
    return out


# ------------------------------------------------------------------ C. echelon Dijkstra
P = 2


def pivot(row):
    return next(i for i, x in enumerate(row) if x)


def reduce(basis, v):
    """Reduce v by a fully reduced GF(2) echelon basis (distinct pivots, zero pivot columns elsewhere)."""
    v = list(v)
    for row in basis:
        if v[pivot(row)]:
            v = [(x + y) % P for x, y in zip(v, row)]
    return tuple(v)


def insert(basis, v):
    r = reduce(basis, v)
    if not any(r):
        return basis
    k = pivot(r)
    rows = [tuple((x + y) % P for x, y in zip(row, r)) if row[k] else row for row in basis]
    return tuple(sorted(rows + [r], key=pivot))


def rank(vectors):
    b = ()
    for v in vectors:
        b = insert(b, v)
    return len(b)


def members(basis):
    out = set()
    for coeffs in itertools.product(range(P), repeat=len(basis)):
        v = tuple(0 for _ in range(2))
        for c, row in zip(coeffs, basis):
            v = tuple((x + c * y) % P for x, y in zip(v, row))
        out.add(v)
    return out


def dijkstra(entry, demand, H):
    start = [()] * (H + 1)
    for v, h in entry:
        start[h] = insert(start[h], v)
    start = tuple(start)
    best = {start: 0}
    heap = [(0, start)]
    while heap:
        d, s = heapq.heappop(heap)
        if d > best[s]:
            continue
        if all(not any(reduce(s[h], v)) for v, h in demand):
            return d
        for h in range(H + 1):
            for v in members(s[h]):
                if not any(v):
                    continue
                for g in (h - 1, h + 1):
                    if 0 <= g <= H and any(reduce(s[g], v)):
                        n = list(s)
                        n[g] = insert(s[g], v)
                        n = tuple(n)
                        if d + 1 < best.get(n, 10 ** 9):
                            best[n] = d + 1
                            heapq.heappush(heap, (d + 1, n))
    need(False, "unreachable")


def frame_checks():
    vecs = [v for v in itertools.product(range(P), repeat=2) if any(v)]
    spaces = [()] + [(v,) for v in vecs] + [tuple(vecs[:2])]
    count = 0
    H = 3
    for R in spaces:
        for Pp in spaces:
            if rank(list(R) + list(Pp)) != len(R) + len(Pp):
                continue
            b = ()
            for v in list(R) + list(Pp):
                b = insert(b, v)
            whole = members(b)
            for O in spaces:
                if not O or not all(v in whole for v in O):
                    continue
                rho_r = rank(list(Pp) + list(O)) - rank(list(Pp))
                rho_p = rank(list(R) + list(O)) - rank(list(R))
                rho_o = rank(list(O))
                for hr, hp, hc in itertools.product(range(H + 1), repeat=3):
                    entry = [(v, hr) for v in R] + [(v, hp) for v in Pp]
                    demand = [(v, hc) for v in O]
                    opt = dijkstra(entry, demand, H)
                    formula = min(rho_r * abs(x - hr) + rho_p * abs(x - hp) + rho_o * abs(x - hc)
                                  for x in range(H + 1))
                    need(opt == formula, "meeting formula = Dijkstra optimum at %s" % ((R, Pp, O, hr, hp, hc),))
                    count += 1
    return count


def hosted_witness():
    """Selected hosted template: the first time anything acts on each replica-0 pair-3 Y stream."""
    raw = (ROOT / HOSTED[0]).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == HOSTED[1], "hosted archive pin")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        data = tar.extractfile(tar.getmember(HOSTED[2])).read()
    need(hashlib.sha256(data).hexdigest() == HOSTED[3], "hosted template pin")
    h = json.loads(gzip.decompress(data))
    first = {}
    for slot in h["hosting"]["pooled_slots"]:
        if slot["owner_replica"] == 0:
            f = slot["family"]
            first[f] = min(first.get(f, 10 ** 9), slot["time"])
    sweeps = [e for e in h["execution_schedule"] if e.get("replica") == 0]
    t14 = next(e["time"] for e in sweeps if e["kind"] == "idle_cover_sweep" and e["pair"] == 3)
    y_first = min(first.get(f, 10 ** 9) for f in range(784, 896))
    x_early = sum(1 for slot in h["hosting"]["pooled_slots"]
                  if slot["owner_replica"] == 0 and 672 <= slot["family"] < 784 and slot["time"] < t14)
    need(y_first >= t14, "pair-3 Y streams receive no hosted residual before pair 3's first sweep")
    return t14, x_early


def controls(t):
    """Negative/positive controls for the independent method (each must behave as stated)."""
    rejected = 0
    need(dijkstra([((1, 0), 0)], [((1, 0), 3)], 3) == 3, "positive control: one row climbs three levels")
    need(dijkstra([((1, 0), 0), ((0, 1), 3)], [((1, 1), 3)], 3) == 3, "positive control: record climb to partner")
    need(dijkstra([((1, 0), 0), ((0, 1), 3)], [((1, 1), 0)], 3) == 3, "positive control: partner descent")
    bad = json.loads(json.dumps(t))
    for e in bad["idle_children"]:
        if e["port"] == 0 and e["child"] == 4:
            e["rank"] -= 8                     # drop one stage block from pair 2's first idle sweep
    try:
        coordinate_replay(bad)
    except Fail:
        rejected += 1
    # A formula without the output-transport term must disagree with the optimum somewhere.
    wrong = sum(1 for hr, hp, hc in itertools.product(range(4), repeat=3)
                if dijkstra([((1, 0), hr), ((0, 1), hp)], [((1, 1), hc)], 3)
                != min(abs(x - hr) + abs(x - hp) for x in range(4)))
    need(wrong > 0, "negative control: dropping the output term must fail")
    rejected += 1
    return rejected


def main():
    t = template()
    snapshots, stage_pair = coordinate_replay(t)
    v = law(snapshots, stage_pair, t)
    need(pr2540_frames() == 8 and v["PR2540"] == 128, "PR2540: 16 x |F_U1 - F_L| = 16 x 8 = 128")
    need(v["INIT"] == [1152, 768, 512, 256] and v["dA"] == [448, 320, 192], "INIT / d_A climbs")
    total = sum(v["INIT"]) + sum(v["dA"])
    need(total == 3648, "INIT64 + d_A = 3648")
    need(sum(v["dA"]) == 960, "d_A alone 960")
    per_array = sorted([x // 16 for x in v["INIT"] for _ in range(16)] + [x // 8 for x in v["dA"] for _ in range(8)])
    need(sum(per_array[:62]) == 1952, "cheapest 62 of the 88 stated captures = 1952")
    need(v["zero_witness"] == (0, 6), "zero witness: no coordinate applied to pair 3 across six calls")
    dec = decimal_checks()
    n = frame_checks()
    rejected = controls(t)
    t14, x_early = hosted_witness()
    need((t14, x_early) == (40, 160), "witness window ends at time 40; pair-3 X streams host 160 residuals in it")
    print("PASS_RETAINED_ARRAY_CATCH_UP_INDEPENDENT pr2540=128 init64_dA=%d dA_only=960 cheapest62=1952 zero_witness_calls=6 "
          "breakeven_S=%d breakeven_C=%d no_saving=%d echelon_dijkstra_instances=%d controls_rejected=%d"
          % (total, dec["breakeven_idle"], dec["breakeven_rank8"], dec["threshold"], n, rejected))


if __name__ == "__main__":
    try:
        main()
    except Fail as exc:
        print("FAIL:", exc)
        sys.exit(1)
