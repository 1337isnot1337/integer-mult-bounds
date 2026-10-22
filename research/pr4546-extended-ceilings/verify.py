#!/usr/bin/env python3
"""Independent recomputation of PR #4546's twelve-window shear ceilings, extended to five- and six-shear words.

Nothing is imported from #4546. The windows are extracted with this file's own code from the canonical #4470
constructor in main (research/joint-helper-lattice/native_joint.py, run in an isolated subprocess on its pinned
inputs) and cross-checked against #4546's vendored RESULT.json (index, roles, coefficients, start/exit dimensions,
old paid profile, matching-word count and relaxed-profile count at length <= 4).

Model (#4546's README, re-implemented). Three persistent fields (a, b, x) carry binary frames (subspaces of F_2^9).
The window's endpoint is a += ca x; b += cb x with ca, cb in {-1, 1}. A candidate is any word of unit shears
y_i += s y_j (i != j, s = +-1) with the same exact integer 3x3 endpoint. Each shear acts in one common frame; frames
only grow along a field's path; exits are fixed. Forward mandatory spans (sum of the operands' current lower bounds)
and backward permissible intersections (from the fixed exits) bound every contact frame; integer contact dimensions
between those bounds, nondecreasing along each field and capped by its exit, are enumerated, every positive gap
(including the exit gap) is charged, and the charged rank mass equals the total exit-minus-entrance mass. This
relaxation contains every actual monotone path, so the old cost minus the least relaxed cost bounds any gain from
above. Ranks are priced r^(1-C) with C = 0.00302015 (certified rational enclosures).

Checks: (1) length <= 4 reproduces #4546 exactly (22,621 words, 84 matches per sign case, the relaxed-profile counts,
zero ceilings); (2) lengths 5 and 6 (248,832 and 2,985,984 more words; matches found by meet in the middle) are
evaluated the same way and their best optimistic gain is reported per window.
Ryanson Jonathan with Claude Code (Claude Opus 5.5) assistance. Apache-2.0.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "PR4546-RESULT.json"  # #4546 head 55b8d34c, research/four-shear-window-ceilings/RESULT.json, blob f2f41100
RESULT_SHA256 = "9e2306e8023f03b483701cd06bfafb0b4980de457b39e0e41c1009cecd2da96a"
C = Fr(60403, 20000000)
GATES = tuple((i, j, s) for i in range(3) for j in range(3) if i != j for s in (-1, 1))
IDENTITY = (1, 0, 0, 0, 1, 0, 0, 0, 1)


def need(condition, message):
    if not condition:
        raise AssertionError(message)


# ---------------------------------------------------------------- integer endpoint census
def act(m, g):
    i, j, s = g
    out = list(m)
    for k in range(3):
        out[3 * i + k] += s * m[3 * j + k]
    return tuple(out)


def target(ca, cb):
    return act(act(IDENTITY, (0, 2, ca)), (1, 2, cb))


def words_of_length(n):
    layer = [(IDENTITY, ())]
    for _ in range(n):
        layer = [(act(m, g), w + (g,)) for m, w in layer for g in GATES]
    return layer


@lru_cache(None)
def matches(ca, cb, max_len):
    T = target(ca, cb)
    found, visited = [], 0
    for n in range(min(max_len, 4) + 1):
        layer = words_of_length(n)
        visited += len(layer)
        found += [w for m, w in layer if m == T]
    if max_len >= 5:
        # Meet in the middle: word = p + q with M(q) M(p) = T, i.e. M(p) = M(q)^-1 T.
        pre = {n: defaultdict(list) for n in (2, 3)}
        for n in (2, 3):
            for m, w in words_of_length(n):
                pre[n][m].append(w)
        for n in range(5, max_len + 1):
            lp, lq = (2, 3) if n == 5 else (3, 3)
            for _, q in words_of_length(lq):
                # M(q) = E_qk ... E_q1, so M(q)^-1 T = E_q1^-1 ... E_qk^-1 T: apply inverses from the last gate.
                inv = T
                for (i, j, s) in reversed(q):
                    inv = act(inv, (i, j, -s))
                for p in pre[lp].get(inv, ()):
                    found.append(p + q)
            visited += 12 ** n
    return tuple(found), visited


# ---------------------------------------------------------------- binary frames
@lru_cache(None)
def span(basis):
    vals = {0}
    for v in basis:
        vals |= {x ^ v for x in vals}
    return frozenset(vals)


def dim(sp):
    return len(sp).bit_length() - 1


@lru_cache(None)
def ssum(a, b):
    basis = []
    for v in list(a) + list(b):
        for bv in basis:
            v = min(v, v ^ bv)
        if v:
            basis.append(v)
    return span(tuple(sorted(basis)))


def relaxed(starts, ends, word):
    if not all(a <= b for a, b in zip(starts, ends)):
        return set()
    cur, lower = list(starts), []
    for i, j, _ in word:
        f = ssum(cur[i], cur[j])
        lower.append(f)
        cur[i] = cur[j] = f
    cur, upper = list(ends), [None] * len(word)
    for k in range(len(word) - 1, -1, -1):
        i, j, _ = word[k]
        f = cur[i] & cur[j]
        upper[k] = f
        cur[i] = cur[j] = f
    if not all(a <= b for a, b in zip(lower, upper)):
        return set()
    bounds = [(dim(a), dim(b)) for a, b in zip(lower, upper)]
    s0, e0 = tuple(dim(x) for x in starts), tuple(dim(x) for x in ends)
    out = set()

    def visit(k, state, hist):
        if k == len(word):
            h = list(hist)
            for a, b in zip(state, e0):
                if b > a:
                    h[b - a] += 1
            need(sum(r * n for r, n in enumerate(h)) == sum(e0) - sum(s0), "rank mass")
            out.add(tuple(h))
            return
        i, j, _ = word[k]
        lo, hi = bounds[k]
        for dd in range(max(lo, state[i], state[j]), min(hi, e0[i], e0[j]) + 1):
            h, st = list(hist), list(state)
            for r in (i, j):
                if dd > st[r]:
                    h[dd - st[r]] += 1
                st[r] = dd
            visit(k + 1, tuple(st), tuple(h))

    visit(0, s0, (0,) * 10)
    return out


# ---------------------------------------------------------------- certified rank prices r^(1-C)
def ln_bounds(y, terms=80):
    y = Fr(y)
    e = 0
    while y >= 2:
        y /= 2
        e += 1

    def core(v):
        z = (v - 1) / (v + 1)
        s, p = Fr(0), z
        for k in range(terms):
            s += 2 * p / (2 * k + 1)
            p *= z * z
        return s, s + 2 * p / ((2 * terms + 1) * (1 - z * z))

    a, b = core(y)
    c, d = core(Fr(2))
    return a + e * c, b + e * d


def prices():
    out = {1: (Fr(1), Fr(1))}
    for r in range(2, 10):
        lo, hi = ln_bounds(r)
        xs = (C * lo, C * hi)

        def expm(x, terms=30):  # exp(-x) for 0 < x < 1/100: alternating series bounds
            t, s = Fr(1), Fr(1)
            for n in range(1, terms):
                t *= -x / n
                s += t
            return s - abs(t * x / terms), s + abs(t * x / terms)

        out[r] = (r * expm(xs[1])[0], r * expm(xs[0])[1])
    return out


PRICE = prices()


def gain_upper(old, new):
    """Upper bound on cost(old) - cost(new) with certified prices; exact 0 for identical profiles."""
    if old == new:
        return Fr(0)
    tot = Fr(0)
    for r in range(1, 10):
        n = old[r] - new[r]
        if n:
            tot += n * (PRICE[r][1] if n > 0 else PRICE[r][0])
    return tot


# ---------------------------------------------------------------- windows from the canonical constructor
def construct():
    with tempfile.TemporaryDirectory(prefix="ext-ceiling-cache-") as cache:
        code = ("import json,sys;sys.path.insert(0,sys.argv[1]);import native_joint;"
                "c,p,b,o,n=native_joint.construct();print(json.dumps({'c':c,'p':p['forward']}))")
        run = subprocess.run([sys.executable, "-I", "-B", "-X", "pycache_prefix=" + cache, "-c", code,
                              str(ROOT / "research/joint-helper-lattice")], capture_output=True, check=True, timeout=120)
    data = json.loads(run.stdout)
    return data["c"], data["p"]


def extract_windows(c, program):
    word = [e for e in program if e[0] != "climb"]
    frames = c["frames"]
    state = list(c["start"])
    phase, out = None, []

    def roles(e):
        g = e[1]
        return g[1:3] if g[0] in ("add", "copy") else g[1:2]

    for pos, e in enumerate(word):
        if e[0] == "phase":
            phase = e[1]
        if phase in ("B", "cleanup_tail") and pos + 1 < len(word):
            f = word[pos + 1]
            if e[0] == f[0] == "scalar" and e[1][0] == f[1][0] == "add" and all(r[0] == "L" for r in roles(e) + roles(f)):
                a, x, b, y = e[1][1][1], e[1][2][1], f[1][1][1], f[1][2][1]
                ca, cb = Fr(*e[1][3:]), Fr(*f[1][3:])
                if x == y and len({a, b, x}) == 3 and ca in (-1, 1) and cb in (-1, 1):
                    owners = (a, b, x)
                    starts = [span(tuple(frames[state[r]])) for r in owners]
                    ends = []
                    for r in owners:
                        t = c["final"][r]
                        for later in word[pos + 2:]:
                            if later[0] == "scalar" and ["L", r] in roles(later):
                                t = later[2]
                                break
                            if later[0] == "warp" and later[1] == ["L", r]:
                                t = later[3]
                                break
                        ends.append(span(tuple(frames[t])))
                    actual = [span(tuple(frames[e[2]])), span(tuple(frames[f[2]]))]
                    out.append({"index": pos, "phase": phase, "roles": list(owners), "coefficients": [int(ca), int(cb)],
                                "starts": starts, "ends": ends, "frames": actual})
        if e[0] == "scalar":
            for r in roles(e):
                if r[0] == "L":
                    state[r[1]] = e[2]
        elif e[0] == "warp":
            state[e[1][1]] = e[4]
    return out


def actual_profile(starts, ends, frames):
    word = ((0, 2, 0), (1, 2, 0))
    st, h = list(starts), [0] * 10
    for (i, j, _), f in zip(word, frames):
        for r in (i, j):
            need(st[r] <= f, "actual frame monotone")
            if dim(f) > dim(st[r]):
                h[dim(f) - dim(st[r])] += 1
            st[r] = f
    for a, b in zip(st, ends):
        need(a <= b, "actual exit monotone")
        if dim(b) > dim(a):
            h[dim(b) - dim(a)] += 1
    return tuple(h)


def extract_nonadjacent(c, program):
    """Pairs a += ca x ... b += cb x (unit ca, cb) in phases B/cleanup_tail separated by >= 1 operation, none of which
    touches a, b or x (so the pair can be rewritten in place). Starts are taken at the first shear, exits after the second."""
    word = [e for e in program if e[0] != "climb"]
    frames = c["frames"]

    def roles(e):
        g = e[1]
        return g[1:3] if g[0] in ("add", "copy") else g[1:2]

    def touches(e, fields):
        if e[0] == "scalar":
            return any(r[0] == "L" and r[1] in fields for r in roles(e))
        return e[0] == "warp" and e[1][0] == "L" and e[1][1] in fields

    state, phase, states = list(c["start"]), None, []
    for e in word:
        if e[0] == "phase":
            phase = e[1]
        states.append((phase, list(state)))
        if e[0] == "scalar":
            for r in roles(e):
                if r[0] == "L":
                    state[r[1]] = e[2]
        elif e[0] == "warp":
            state[e[1][1]] = e[4]
    out = []
    for pos, e in enumerate(word):
        ph, st = states[pos]
        if ph not in ("B", "cleanup_tail") or e[0] != "scalar" or e[1][0] != "add" or not all(r[0] == "L" for r in roles(e)):
            continue
        a, x, ca = e[1][1][1], e[1][2][1], Fr(*e[1][3:])
        if ca not in (-1, 1):
            continue
        for q in range(pos + 1, len(word)):
            f = word[q]
            if f[0] == "phase":
                break
            if (f[0] == "scalar" and f[1][0] == "add" and all(r[0] == "L" for r in roles(f)) and f[1][2][1] == x
                    and f[1][1][1] not in (a, x) and Fr(*f[1][3:]) in (-1, 1) and q > pos + 1):
                b = f[1][1][1]
                if not any(touches(word[k], {a, b, x}) for k in range(pos + 1, q)):
                    owners = (a, b, x)
                    ends = []
                    for r in owners:
                        t = c["final"][r]
                        for later in word[q + 1:]:
                            if later[0] == "scalar" and ["L", r] in roles(later):
                                t = later[2]
                                break
                            if later[0] == "warp" and later[1] == ["L", r]:
                                t = later[3]
                                break
                        ends.append(span(tuple(frames[t])))
                    out.append({"index": pos, "partner": q, "coefficients": [int(ca), int(Fr(*f[1][3:]))],
                                "starts": [span(tuple(frames[st[r]])) for r in owners], "ends": ends,
                                "frames": [span(tuple(frames[e[2]])), span(tuple(frames[f[2]]))]})
            if touches(f, {a, x}):
                break
    return out


def subspaces_between(L, U, k):
    """Every subspace F with L <= F <= U and dim F = k."""
    if not L <= U or not dim(L) <= k <= dim(U):
        return []
    found, seen, stack = set(), {L}, [L]
    while stack:
        cur = stack.pop()
        if dim(cur) == k:
            found.add(cur)
            continue
        for vec in U:
            if vec not in cur:
                nxt = ssum(cur, span((vec,)))
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return list(found)


def geometric_best_gain(starts, ends, old, word):
    """Exact search over actual nested subspaces (joint incidence enforced) for one word; None if infeasible."""
    cur, upper = list(ends), [None] * len(word)
    for k in range(len(word) - 1, -1, -1):
        i, j, _ = word[k]
        f = cur[i] & cur[j]
        upper[k] = f
        cur[i] = cur[j] = f
    best = [None]

    def rec(k, state, hist):
        if k == len(word):
            h = list(hist)
            for r in range(3):
                if not state[r] <= ends[r]:
                    return
                g = dim(ends[r]) - dim(state[r])
                if g:
                    h[g] += 1
            gain = gain_upper(old, tuple(h))
            if best[0] is None or gain > best[0]:
                best[0] = gain
            return
        i, j, _ = word[k]
        L, U = ssum(state[i], state[j]), upper[k]
        for dd in range(dim(L), dim(U) + 1):
            for F in subspaces_between(L, U, dd):
                h, st = list(hist), list(state)
                for r in (i, j):
                    g = dim(F) - dim(st[r])
                    if g:
                        h[g] += 1
                    st[r] = F
                rec(k + 1, tuple(st), tuple(h))

    rec(0, tuple(starts), (0,) * 10)
    return best[0]


def single_contact_retiming(c, program):
    """For every two-operand scalar contact in the whole word (all phases), compare the incumbent contact dimension with
    every admissible dimension between the operands' current-frame sum and their next-contact (exit) intersection.
    Any dimension in that range is realisable by a nested subspace, so this is exact for single-contact retiming."""
    word = [e for e in program if e[0] != "climb"]
    frames = c["frames"]

    def roles(e):
        g = e[1]
        return g[1:3] if g[0] in ("add", "copy") else g[1:2]

    exit_after, cur = [None] * len(word), {}
    for k in range(len(word) - 1, -1, -1):
        e = word[k]
        exit_after[k] = dict(cur)
        if e[0] == "scalar":
            for r in roles(e):
                if r[0] == "L":
                    cur[r[1]] = e[2]
        elif e[0] == "warp" and e[1][0] == "L":
            cur[e[1][1]] = e[3]

    def cost(h):
        return sum(n * PRICE[r][1] for r, n in enumerate(h) if n and r)

    state, phase, tally = list(c["start"]), None, Counter()
    for k, e in enumerate(word):
        if e[0] == "phase":
            phase = e[1]
        if e[0] == "scalar" and len(roles(e)) == 2 and all(r[0] == "L" for r in roles(e)):
            i, j = roles(e)[0][1], roles(e)[1][1]
            Si, Sj = span(tuple(frames[state[i]])), span(tuple(frames[state[j]]))
            Ei = span(tuple(frames[exit_after[k].get(i, c["final"][i])]))
            Ej = span(tuple(frames[exit_after[k].get(j, c["final"][j])]))
            F0 = span(tuple(frames[e[2]]))
            L, U = ssum(Si, Sj), Ei & Ej
            need(L <= F0 <= U, "incumbent contact inside its bounds")

            def prof(dd):
                h = [0] * 10
                for lo_, hi_ in ((dim(Si), dd), (dd, dim(Ei)), (dim(Sj), dd), (dd, dim(Ej))):
                    if hi_ > lo_:
                        h[hi_ - lo_] += 1
                return tuple(h)

            incumbent = cost(prof(dim(F0)))
            need(all(cost(prof(dd)) >= incumbent for dd in range(dim(L), dim(U) + 1)), f"single-contact optimum at {k}")
            tally[phase] += 1
        if e[0] == "scalar":
            for r in roles(e):
                if r[0] == "L":
                    state[r[1]] = e[2]
        elif e[0] == "warp":
            state[e[1][1]] = e[4]
    return dict(tally)


def matches_alphabet(ca, cb, coefs, max_len):
    """All words of length <= max_len over shears y_i += c y_j (c in coefs) with the window endpoint (meet in middle)."""
    gates = tuple((i, j, c) for i in range(3) for j in range(3) if i != j for c in coefs)

    def layer(n):
        out = [(IDENTITY, ())]
        for _ in range(n):
            out = [(act(m, g), w + (g,)) for m, w in out for g in gates]
        return out

    half = max_len // 2
    pre = defaultdict(list)
    for n in range(half + 1):
        for m, w in layer(n):
            pre[n, m].append(w)
    T, found = target(ca, cb), []
    for total in range(max_len + 1):
        lp = min(half, total)
        lq = total - lp
        for _, q in layer(lq):
            inv = T
            for (i, j, c) in reversed(q):
                inv = act(inv, (i, j, -c))
            found += [p + q for p in pre.get((lp, inv), ())]
    return found


def main():
    raw = RESULT.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == RESULT_SHA256, "vendored #4546 RESULT.json")
    ref = {w["index"]: w for w in json.loads(raw)["windows"]}
    c, program = construct()
    wins = extract_windows(c, program)
    need(len(wins) == 128, "#4546's 128 eligible windows")
    every = wins
    wins = wins[:12]
    rows = []
    for w in wins:
        r = ref[w["index"]]
        need(w["roles"] == r["roles"] and w["coefficients"] == r["coefficients"] and w["phase"] == r["phase"], "window identity")
        need([dim(x) for x in w["starts"]] == r["start_dimensions"] and [dim(x) for x in w["ends"]] == r["exit_dimensions"],
             "window dimensions")
        old = actual_profile(w["starts"], w["ends"], w["frames"])
        need({str(k): v for k, v in enumerate(old) if v} == r["old_paid"], "old paid profile")
        row = {"index": w["index"], "old_paid": {str(k): v for k, v in enumerate(old) if v}}
        for L in (4, 5, 6):
            ms, visited = matches(*w["coefficients"], L)
            profiles = set()
            compatible = 0
            for word in ms:
                ps = relaxed(w["starts"], w["ends"], word)
                if ps:
                    compatible += 1
                profiles |= ps
            best = max(gain_upper(old, p) for p in profiles)
            if L == 4:
                need(visited == 22621 and len(ms) == 84 == r["compatible_words"] == compatible, "length-4 census")
                need(len(profiles) == r["relaxed_profiles"], "length-4 relaxed profile count")
                need(best == 0, "length-4 zero ceiling")
            row[f"len<={L}"] = {"matching_words": len(ms), "compatible": compatible, "relaxed_profiles": len(profiles),
                                "best_gain_upper": str(best), "positive": best > 0}
        rows.append(row)
    summary = {L: sum(1 for r in rows if r[f"len<={L}"]["positive"]) for L in (4, 5, 6)}
    # All 128 eligible windows (#4546 tested only the first twelve): lengths <= 4 and <= 6.
    phases = Counter(w["phase"] for w in every)
    profile_counts = Counter()
    for w in every:
        old = actual_profile(w["starts"], w["ends"], w["frames"])
        for L in (4, 6):
            ms, _ = matches(*w["coefficients"], L)
            profiles = set()
            for word in ms:
                profiles |= relaxed(w["starts"], w["ends"], word)
            need(profiles and max(gain_upper(old, p) for p in profiles) == 0, f"zero ceiling, window {w['index']}, len<={L}")
            if L == 6:
                profile_counts[len(profiles)] += 1
    # Nonunit coefficients: optimistic in the rewrite's favour (their scalar-height cost is not charged).
    nonunit = {}
    for coefs, L in (((-2, -1, 1, 2), 6), ((-3, -2, -1, 1, 2, 3), 5)):
        cache = {}
        for w in every:
            key = tuple(w["coefficients"])
            if key not in cache:
                cache[key] = matches_alphabet(key[0], key[1], coefs, L)
            old = actual_profile(w["starts"], w["ends"], w["frames"])
            profiles = set()
            for word in cache[key]:
                profiles |= relaxed(w["starts"], w["ends"], word)
            need(profiles and max(gain_upper(old, p) for p in profiles) == 0, f"zero ceiling with coefficients {coefs}")
        nonunit[f"coefficients {sorted(set(abs(c) for c in coefs))}, len<={L}"] = {
            "matching_words_per_sign_case": len(next(iter(cache.values()))), "windows_zero": len(every)}
    # Nonadjacent pairs (a model change #4546 suggests): relaxation first; exact joint geometry where it is positive.
    nonadj = extract_nonadjacent(c, program)
    na = Counter()
    for w in nonadj:
        old = actual_profile(w["starts"], w["ends"], w["frames"])
        ms, _ = matches(*w["coefficients"], 6)
        positive_words = []
        for word in ms:
            ps = relaxed(w["starts"], w["ends"], word)
            if ps and max(gain_upper(old, p) for p in ps) > 0:
                positive_words.append(word)
        if not positive_words:
            na["zero_by_relaxation"] += 1
            continue
        for word in positive_words:
            g = geometric_best_gain(w["starts"], w["ends"], old, word)
            need(g is None or g <= 0, f"exact geometry: no gain, window {w['index']}")
        na["zero_by_exact_geometry"] += 1
        na["exact_geometry_words_checked"] += len(positive_words)
    need(len(nonadj) == 88 and na["zero_by_relaxation"] + na["zero_by_exact_geometry"] == 88, "88 nonadjacent pairs")
    # #4543's receiver-sharing word a += s b; b += cb x; a -= s b with s = -ca cb, on all 128 windows. The relaxation
    # contains every actual monotone path, so "infeasible" here means the rewrite cannot meet the frame contract at all.
    rs = Counter()
    for w in every:
        ca, cb = w["coefficients"]
        sgn = -ca * cb
        word = ((0, 1, sgn), (1, 2, cb), (0, 1, -sgn))
        m = IDENTITY
        for g in word:
            m = act(m, g)
        need(m == target(ca, cb), "receiver-sharing endpoint identity with s = -ca*cb")
        old = actual_profile(w["starts"], w["ends"], w["frames"])
        profiles = relaxed(w["starts"], w["ends"], word)
        if not profiles:
            # The certain obstruction: the first gate a += s b needs a common frame containing b's entrance frame
            # inside a's exit frame.
            need(not (w["starts"][1] <= w["ends"][0]), "infeasibility explained by S_b not inside E_a")
            rs["infeasible", w["phase"]] += 1
            continue
        need(max(gain_upper(old, p) for p in profiles) == 0, "receiver sharing never improves")
        rs["incumbent_admitted" if old in profiles else "incumbent_excluded", w["phase"]] += 1
    print(json.dumps({"status": "PASS_PR4546_EXTENDED_CEILINGS", "windows": rows,
                      "nonunit_coefficients_all_windows": nonunit,
                      "single_contact_retiming_all_phases": single_contact_retiming(c, program),
                      "nonadjacent_pairs_len<=6": {"count": len(nonadj), **dict(na)},
                      "receiver_sharing_4543_all_windows": {f"{k[0]}:{k[1]}": v for k, v in sorted(rs.items())},
                      "windows_with_positive_optimistic_gain": summary,
                      "all_eligible_windows": {"count": len(every), "phases": dict(phases),
                                               "zero_ceiling_len<=4": len(every), "zero_ceiling_len<=6": len(every),
                                               "relaxed_profile_count_histogram_len<=6": dict(sorted(profile_counts.items()))},
                      "new_kappa_claimed": False}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
