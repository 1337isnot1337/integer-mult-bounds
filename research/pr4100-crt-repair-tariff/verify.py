#!/usr/bin/env python3
"""Fixed-tape tariff of #4100 CRT.md section 4's sparse exception repair.

Standard library only. The actual macro S and the ideal switch T come from
#4100's own pinned check_batched_crt.py (compact, good). The repair runs on
explicit tapes, and every head move is counted, split into dense and sparse
parts:

- one split scan driven by the guard scan's hole mask;
- keys T(S^-1(x)) only at holes;
- two-bucket stable LSD radix passes over the keyed holes;
- one reinsertion scan comparing keys only at holes, then erasure.

Key evaluations are counted separately; their E(p,ell) cost is CRT.md's
premise. Finite corroboration of the written accounting in README.md, not an
all-size proof. Ryanson Jonathan with Claude Code (Claude Opus 5.5)
assistance. Apache-2.0.
"""
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/unconditional-batched-crt"


def need(condition, message):
    if not condition:
        raise AssertionError(message)


PHRASES = [
    "from both ends of each K-bit guard. Its bad density is at most",
    "    r [2/B + 8B/2^K] <= C p 2^-G.",
    "T(S^-1(x)), sort those holes by this full key on fixed tapes, and merge them",
    "cost explicitly increased to E(p,ell). It does not sort the full input.",
    "    2^-G E(p,ell) <= C 2^(-60 ell) (p+2)^(-48),",
    "bad-key evaluation, O(p)-bit keys, radix passes, counters and clearing all",
    "the E(p,ell) computation. Reinsertion reads the one-bit hole stream and",
    "    G=64(ell+ceil(log2(p+2))),  B=2^G,  K=64G,",
]
PR2250_PHRASE = "    O(V + M A^3 + delta M A(R+A))."


def check_sources():
    pins = {row["path"]: row["sha256"]
            for row in json.loads((Path(__file__).parent / "SOURCES.json").read_text())["files"]}
    for rel in ("research/unconditional-batched-crt/CRT.md",
                "research/unconditional-batched-crt/check_batched_crt.py",
                "research/selected-complex-compact-adapters/PROOF.md"):
        need(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == pins[rel], f"pin {rel}")
    text = (SOURCE / "CRT.md").read_text()
    for phrase in PHRASES:
        need(phrase in text, f"CRT.md phrase missing: {phrase}")
    need(PR2250_PHRASE in (ROOT / "research/selected-complex-compact-adapters/PROOF.md").read_text(),
         "PR2250 repair tariff phrase")
    spec = importlib.util.spec_from_file_location("pr4100_crt", SOURCE / "check_batched_crt.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, len(PHRASES) + 1


class Tape:
    def __init__(self, width=1):
        self.cells, self.pos, self.moves, self.end, self.w = [], 0, 0, 0, width

    def goto(self, i):
        self.moves += abs(i - self.pos) * self.w
        self.pos = i

    def read(self):
        need(self.pos < self.end, "read past the end marker")
        v = self.cells[self.pos]
        self.pos += 1
        self.moves += self.w
        return v

    def write(self, v):
        if self.pos < len(self.cells):
            self.cells[self.pos] = v
        else:
            self.cells.append(v)
        self.pos += 1
        self.moves += self.w
        self.end = max(self.end, self.pos)

    def truncate(self):
        self.end = self.pos

    def erase(self):
        """Blank the written region (one sweep) and return to its origin."""
        self.goto(self.end)
        self.goto(0)
        self.moves += self.end * self.w
        self.end = 0


class Counter:
    """L-bit binary address counter; head rests on the low end."""

    def __init__(self, L):
        self.bits, self.moves, self.L = [0] * L, 0, L

    def increment(self):
        i = 0
        while i < self.L and self.bits[i]:
            self.bits[i] = 0
            i += 1
        if i < self.L:
            self.bits[i] = 1
        self.moves += 2 * (i + 1)

    def value(self):
        self.moves += 2 * self.L  # read every bit and return
        return sum(b << i for i, b in enumerate(self.bits))

    def reset(self):
        self.bits = [0] * self.L
        self.moves += 2 * self.L


def fixture(crt, bits, cb, yb, guard, fn):
    L = 2 * cb + yb
    M = 1 << L

    def split(q):
        return q >> (cb + yb), (q >> yb) & ((1 << cb) - 1), q & ((1 << yb) - 1)

    def join(u, t, y):
        return (u << (cb + yb)) | (t << yb) | y

    S, T, good = [0] * M, [0] * M, [False] * M
    for q in range(M):
        u, t, y = split(q)
        S[q] = join(*crt.compact(u, t, y, fn, bits=bits, positions=(0,), ybits=yb, control_bits=cb))
        T[q] = join(u, t, y ^ fn(y)[0])
        good[q] = crt.good(u, t, y, bits=bits, positions=(0,), guard=guard)
    need(sorted(S) == list(range(M)) and sorted(T) == list(range(M)), "S and T are bijections")
    for q in range(M):
        need(good[S[q]] == good[q] and good[T[q]] == good[q], "S and T preserve the good set")
        if good[q]:
            need(S[q] == T[q], "S agrees with T on good addresses")
    inv_S = [0] * M
    for q in range(M):
        inv_S[S[q]] = q
    return L, M, S, T, good, inv_S


def repair(L, M, R, S, T, good, inv_S, *, key_mode="TS^-1", full_sort=False):
    """After the macro, the record from q sits at S(q). Return the final layout and the meters."""
    DATA, GOOD, BAD, B = Tape(R), Tape(R), Tape(L + R), [Tape(L + R), Tape(L + R)]
    MASK = Tape(1)
    ctr = Counter(L)
    for x in range(M):
        DATA.write(inv_S[x])            # record id = original address
        MASK.write(0 if good[x] else 1)  # the guard scan's owned hole mask (#4201)
    DATA.truncate(); MASK.truncate(); DATA.goto(0); MASK.goto(0)
    DATA.moves = MASK.moves = 0
    evaluations = 0

    def key_of(x):
        if key_mode == "TS^-1":
            return T[inv_S[x]]
        if key_mode == "S^-1":           # control: forget the ideal map
            return inv_S[x]
        raise ValueError(key_mode)

    # Split scan: good records to GOOD; holes get their address, key and record on BAD.
    for x in range(M):
        hole = MASK.read()
        rec = DATA.read()
        sorted_here = full_sort or hole
        if sorted_here:
            addr = ctr.value()
            need(addr == x, "counter tracks the current address")
            evaluations += 1
            BAD.write((key_of(x), rec))
        else:
            GOOD.write(rec)
        ctr.increment()
    BAD.truncate(); GOOD.truncate()
    n_sorted = BAD.end
    # Two-bucket stable LSD radix passes on the L-bit keys.
    for j in range(L):
        BAD.goto(0)
        for _ in range(n_sorted):
            key, rec = BAD.read()
            B[(key >> j) & 1].write((key, rec))
        for b in B:
            b.truncate()
        BAD.goto(0)
        for b in B:
            b.goto(0)
            for _ in range(b.end):
                BAD.write(b.read())
            b.erase()
        BAD.truncate()
    BAD.goto(0)
    # Reinsertion: output overwrites DATA from cell 0; keys compared only at holes.
    MASK.goto(0); GOOD.goto(0); DATA.goto(0)
    ctr.reset()
    for x in range(M):
        hole = MASK.read()
        if full_sort:
            key, rec = BAD.read()
        elif hole:
            key, rec = BAD.read()
            addr = ctr.value()
            need(key == addr, "sorted key equals the current hole address")
        else:
            rec = GOOD.read()
        DATA.write(rec)
        ctr.increment()
    for tape in (GOOD, BAD, MASK):
        tape.erase()
    DATA.goto(0)
    layout = DATA.cells[:M]
    dense = DATA.moves + GOOD.moves + MASK.moves
    sparse = BAD.moves + B[0].moves + B[1].moves
    return layout, dict(dense=dense, sparse=sparse, counter=ctr.moves, evaluations=evaluations,
                        n_sorted=n_sorted)


def written_bounds(L, M, R, nbad):
    """README accounting, in cells.

    Dense: DATA read, rewind, write, rewind (4MR); GOOD write, rewind, read and
    two-sweep erase (5MR at most); MASK read, rewind, read and erase (5M).
    Sorted holes: one keyed write, then per radix pass nine sweeps (read,
    bucket write, two rewinds, bucket read, concatenation write, two-sweep
    erase, next rewind), plus reinsertion read and erase: (L+R)(9L+6) per hole.
    Counter: two amortized scans (8M), address reads at holes in both scans
    (4L each), and a reset."""
    dense = 9 * M * R + 5 * M
    sparse = nbad * (L + R) * (9 * L + 6)
    counter = 8 * M + 4 * L * nbad + 4 * L
    return dense, sparse, counter


FN = {
    "bit2": lambda y: ((y >> 2) & 1,),
    "parity": lambda y: ((y >> 1).bit_count() & 1,),
    "and14": lambda y: (((y >> 1) & 1) & ((y >> 4) & 1),),
}
FIXTURES = [  # bits, control bits, y bits, guard, source function
    (2, 2, 6, 6, "bit2"),
    (2, 4, 6, 6, "parity"),
    (3, 3, 8, 8, "and14"),
    (3, 4, 8, 8, "parity"),
    (4, 4, 8, 8, "bit2"),
]


def check_repairs(crt):
    rows = []
    for bits, cb, yb, guard, name in FIXTURES:
        L, M, S, T, good, inv_S = fixture(crt, bits, cb, yb, guard, FN[name])
        R = L  # records and keys both Theta(p)
        nbad = M - sum(good)
        B = 1 << bits
        need(Fraction(nbad, M) <= Fraction(2, B) + Fraction(8 * B, 1 << guard), "density <= 2/B + 8B/2^K")
        layout, meter = repair(L, M, R, S, T, good, inv_S)
        need(all(layout[T[q]] == q for q in range(M)), "repair realizes T on every record")
        need(meter["evaluations"] == nbad, "keys evaluated only at holes")
        dense_b, sparse_b, counter_b = written_bounds(L, M, R, nbad)
        need(meter["dense"] <= dense_b, f"dense within bound {bits},{cb},{yb}")
        need(meter["sparse"] <= sparse_b, f"sorted part within bound {bits},{cb},{yb}: {meter['sparse']} > {sparse_b}")
        need(meter["counter"] <= counter_b, "counter within bound")
        rows.append(dict(bits=bits, control_bits=cb, ybits=yb, guard=guard, source=name, L=L, M=M,
                         holes=nbad, density=round(nbad / M, 4),
                         density_bound=round(2 / B + 8 * B / 2 ** guard, 4),
                         dense_per_MR=round(meter["dense"] / (M * R), 3),
                         sparse_per_hole_LR=round(meter["sparse"] / max(1, nbad * L * (L + R)), 3),
                         sparse_per_MR=round(meter["sparse"] / (M * R), 3)))
    return rows


def check_controls(crt):
    bits, cb, yb, guard, name = FIXTURES[1]
    L, M, S, T, good, inv_S = fixture(crt, bits, cb, yb, guard, FN[name])
    R = L
    nbad = M - sum(good)
    out = {}
    # Keys S^-1(x) still permute the bad set (S preserves it), so the reinsertion
    # key check passes; the layout is wrong because the holes skip T.
    wrong_layout, _ = repair(L, M, R, S, T, good, inv_S, key_mode="S^-1")
    out["key_without_T_wrong_records"] = sum(wrong_layout[T[q]] != q for q in range(M))
    need(out["key_without_T_wrong_records"] > 0, "control: keys S^-1(x) misplace hole records")
    layout = [inv_S[x] for x in range(M)]  # no repair at all
    out["no_repair_wrong_records"] = sum(layout[T[q]] != q for q in range(M))
    need(out["no_repair_wrong_records"] > 0, "control: skipping repair leaves holes wrong")
    full_layout, full = repair(L, M, R, S, T, good, inv_S, full_sort=True)
    need(all(full_layout[T[q]] == q for q in range(M)), "full sort is also correct")
    _, sparse_meter = repair(L, M, R, S, T, good, inv_S)
    out["full_sort_evaluations"] = full["evaluations"]
    out["sparse_evaluations"] = sparse_meter["evaluations"]
    out["full_sort_per_MR"] = round(full["sparse"] / (M * R), 2)
    # The full-input sort moves Theta(L) records' worth per record: not O(V).
    need(full["sparse"] / (M * R) > 8 * L * 0.9, "control: sorting the full input costs Theta(L) V")
    return out


def check_absorption():
    """At #4100's parameters, with L <= p and R >= p/8 (Theta(p) records and addresses):
    sorted/V <= delta(1+L/R)(9L+6) and hole counter reads/V <= delta 4L/R, delta <= r(2/B+8B/2^K), r <= L/(100G)."""
    rows = []
    for k in (4, 8, 16, 32, 64):
        p = 1 << k
        lg = (p + 1).bit_length()  # exact ceil(log2(p+2)); floats round 2^64+2 down
        for ell in (lg, 2 * lg, 8 * lg):          # eventually ell >= ceil(log2(p+2))
            G = 64 * (ell + lg)
            B, K = 1 << G, 64 * G
            L, R = p, Fraction(p, 8)
            r = Fraction(L, 100 * G)
            delta = r * (Fraction(2, B) + Fraction(8 * B, 1 << K))
            sorted_over_V = delta * (1 + L / R) * (9 * L + 6)
            counter_over_V = delta * 4 * L / R
            need(sorted_over_V + counter_over_V < Fraction(1, 2 ** 64), "sparse repair is o(V) with huge margin")
            # CRT.md's E line: 2^-G * 2^(4 ell) (p+2)^16 <= 2^(-60 ell) (p+2)^(-48).
            lhs = Fraction(1 << (4 * ell), 1 << G) * (p + 2) ** 16
            rhs = Fraction(1, 1 << (60 * ell)) / (p + 2) ** 48
            need(lhs <= rhs, "2^-G E-envelope inequality")
            total = sorted_over_V + counter_over_V
            rows.append(dict(p=p, ell=ell, log2_sparse_over_V=round(math.log2(total.numerator) - math.log2(total.denominator), 1)))
    return rows


def main():
    crt, phrases = check_sources()
    rows = check_repairs(crt)
    controls = check_controls(crt)
    absorption = check_absorption()
    print(json.dumps({
        "status": "PASS_PR4100_CRT_REPAIR_TARIFF_FINITE",
        "source_phrases": phrases,
        "fixtures": rows,
        "controls": controls,
        "absorption": absorption,
        "max_dense_per_MR": max(r["dense_per_MR"] for r in rows),
        "max_sparse_per_hole_LR": max(r["sparse_per_hole_LR"] for r in rows),
        "all_size_theorem_claimed": False,
        "new_kappa_claimed": False,
    }, indent=1))


if __name__ == "__main__":
    sys.exit(main())
