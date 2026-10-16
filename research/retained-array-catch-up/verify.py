#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Primary verifier: retained-array coordinate catch-up in the scalar common-frame transport model.

Checks (exact arithmetic; standard library only):
 1. Source pins and verbatim premise lines.
 2. Level timeline of the pinned selected #1094 hosted GLOBAL-TEMPLATE (replica 0). Every local
    call advances its pair one level; idle sweeps advance their declared levels; one level is
    eight coordinates (base-template idle child rank = 8 x levels; hosted children never exceed it).
 3. The catch-up law (PROOF.md Corollary 4) on controls: PR2540 128, PR2197 144, PR2678
    1792/3696, centre path 576 per replica.
 4. The #1166 routes: INIT64 + d_A = 3648 under the stated premises, d_A alone 960, cheapest
    62 stated captures 1952, (S)/(C) array-calls 464 published / 456 uniform, zero witness.
 5. Pricing with the pinned ceiling.py: exact 896 no-saving threshold, break-evens 573 / 71
    against PR2474 (reproducing the #1166 price gate), break-evens against other targets.
 6. Exact frame model: breadth-first minimum paid mass equals the per-cut rank bound (Lemma 1)
    and the meeting-level formula (Proposition 3) on complete finite domains; Lemma 1 is sound
    on general instances.
 7. Two-call rational tensor toy: omitting catch-up gives a wrong output; paid catch-up (or
    partner descent) repairs it.
 8. Negative controls: mutated levels, rows, windows, incidences, lifetimes, formulas, toy
    repairs and prices must fail.

Run from the repository root:  python3 -I -B research/retained-array-catch-up/verify.py
--write regenerates RESULT.json (refuses to replace a differing file unless --force is given).
Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5).
"""
import gzip
import hashlib
import io
import itertools
import json
import math
import random
import sys
import tarfile
from collections import deque
from fractions import Fraction as Q
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]

PINS = {
    "research/complex-local-word-ceiling/ceiling.py":
        "86a1432870b3b21d8454106ec9162fddc0471472d9214c590a1420f2426cedfc",
    "research/complex-local-word-ceiling/README.md":
        "b60be039cb0e03e064a27407d0bce9e58908d793da5ee405c876de5aebfa5f81",
    "research/dirty-host-cutrank-audit/PROOF.md":
        "2921c2c741ab5086a87c53340f18180ecc55675ca7dadc49579da32aba71d2f5",
    "research/idle-axis-hosting/PROOF.md":
        "cfe34bf0b64259661312dae22c3a23adc5bf6f6326951eee5c1488ccfc347542",
    "research/qq16-complete-native-decoder/PROOF.md":
        "09d587f1d6bc250e90e29fa8751a40f45be79f1a8a56af0b645c144cefaefa46",
    "research/qq16-entry-frame-tariff/README.md":
        "cb0e658cfbdd3fb74a43b195665d3b13d5eb8e74294831daa05165128ad9ef5d",
    "research/qq16-private-da-frame-floor-seed81b017/README.md":
        "8e4c3f1d2e76b110ef47aecdce8098c84403b969f8d6e386b0ecabb8173f091b",
    "research/qq16-final-record-obstruction/PROOF.md":
        "109490f1d9c4288445e11e65e77616d84555ce9f212df97c81e6efde0c2ebf43",
    "research/selected-centre-quarter-native/README.md":
        "bfae0aff6aefc90b2afb8da76bc6d07b698deeabdbd758d01910d9fdb937ec72",
    "research/centre-owner-observation-floor/README.md":
        "5f9079af7f45bff8d0b0acc8366f9c0def90fad9c8a38bab772b0ef13e3d5be0",
    "research/selected-centre-chrono-source-census/README.md":
        "0db44f2ce702ee1e5b11c9f8cd05517593bd259f45ae897437c58a1bd81b2943",
    "research/joint-query/README.md":
        "419f076e46f5a6ce43efe30a608baed0a535034c388e1ac76a29a2026685ba77",
    "research/community-frontier1094-audit/selected-replay.tar.gz":
        "f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6",
    "certificates/selected-result.json":
        "bb2eaa58647b353f88d0aec2eafb9d30df1be53589231b23e12ceef3e4bad129",
}
HOSTED_MEMBER = ("candidate/strict/global/hosted/GLOBAL-TEMPLATE.json.gz",
                 "2acf02b418078e37090495c601fe550448751d4f35912757b13a1f778efc7760")
BASE_MEMBER = ("candidate/strict/global/base/split-centres/GLOBAL-TEMPLATE.json.gz",
               "a179dad87651aba340a5a8ddbcd86a8e757cad87b8a1f8bad48106fbecd38518")

ANCHORS = {
    "research/dirty-host-cutrank-audit/PROOF.md": [
        "Its paid mass c is at least |nu(A)-nu(B)|.",
        "D_j\\ \\ge\\ \\dim(W_j^0+\\operatorname{span}Q_j)-\\dim W_j^0. \\tag{C-down}",
        "M\\ge\\sum_j(D_j+U_j). \\tag{A}",
        "The retained history is a mathematical device, not free physical storage.",
        "Any pre-existing side information belongs to the entry state.",
    ],
    "research/qq16-complete-native-decoder/PROOF.md": [
        "`F_L=product_(j=0,...,8) C_(d e_j)`",
        "`U1=<e0,...,e16>`",
        "This costs sixteen rank-eight children and puts x1_V in frame F_U1.",
    ],
    "research/qq16-entry-frame-tariff/README.md": [
        "| Common `F_L`, `F_L` | 224 H8 | 1,792 |",
        "| F0 gauges `F_L`, `F_L C_q^-1` | 112 H8 + 112 H9 | 1,904 |",
        "| Original entry gauges `C_q`, `I` | 112 H16 + 112 H17 | 3,696 |",
    ],
    "research/qq16-private-da-frame-floor-seed81b017/README.md": [
        "each differs from I in exactly 18 one-term Z4 entries.",
        "frames therefore needs at least 8 × 18 = 144 line calls.",
    ],
    "research/qq16-final-record-obstruction/PROOF.md": [
        "    0, 0, 0, 1, 1, 2, 2, 3, 3.",
        "Even stages are forward F_s; odd stages are backward B_(s,s+1).",
        "pair 0: B0 X_(0,U), B2 X_(0,U);",
    ],
    "research/idle-axis-hosting/PROOF.md": [
        "1. ι is an invocation on another pair, and nothing touches F between ι and τ.",
    ],
    "research/complex-local-word-ceiling/README.md": [
        "`{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}`, local mass 5,586.",
    ],
    "research/joint-query/README.md": [
        "| B_s_t | 214986 | 24 | 5546 | 528 | 48 |",
        "| F_s, s > 0 | 211210 | 8 | 5530 | 288 | 16 |",
    ],
    "research/selected-centre-chrono-source-census/README.md": [
        "2. **Every dependent pair has rank 16 (1,539 pairs).**",
        "b5->f6, b7->f8 and f0->f2.",
    ],
    "research/selected-centre-quarter-native/README.md": [
        "nevertheless `1/4` at the identity owner.",
    ],
    "research/centre-owner-observation-floor/README.md": [
        "**104 additional scalar coordinates at every old cover owner**, if each extra",
    ],
}

COORDS_PER_LEVEL = 8
M, FAMILIES, STAGES = 73, 896, 9
SELECTED_KAPPA = Q("0.001672660197076918")       # #1094, selected-result.json
PR2474_KAPPA = Q("0.001703676387993676")         # pending (PR2474)
PR2843_KAPPA = Q("0.00171865827784172")          # pending (PR2843 title value)
PR2848_KAPPA = Q("0.00171865850830493")          # pending (PR2848 title value)
BIT_ENDPOINT = Q("0.001733427039589844234749")   # PR589 bit supplier saving
GRID = Q(1, 10 ** 12)
FRAME_SAMPLE = 24
SELECTED = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}


class CheckFailure(Exception):
    pass


def need(ok, message):
    if not ok:
        raise CheckFailure(message)


# ------------------------------------------------------------------ 1. sources
def check_sources():
    for rel, pin in PINS.items():
        need(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == pin, "source hash mismatch: " + rel)
    for rel, lines in ANCHORS.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for line in lines:
            need(line in text, "premise anchor missing in %s: %r" % (rel, line))
    return {"pinned_files": len(PINS), "anchored_premise_lines": sum(len(v) for v in ANCHORS.values())}


def load_templates():
    raw = (ROOT / "research/community-frontier1094-audit/selected-replay.tar.gz").read_bytes()
    out = []
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        for name, pin in (HOSTED_MEMBER, BASE_MEMBER):
            found = [m for m in archive.getmembers() if m.name == name]
            need(len(found) == 1 and found[0].isfile(), "one regular member: " + name)
            data = archive.extractfile(found[0]).read()
            need(hashlib.sha256(data).hexdigest() == pin, "member hash: " + name)
            out.append(json.loads(gzip.decompress(data)))
    return out


# ------------------------------------------------------------------ 2. level timeline
def replica_events(hosted, base, replica=0):
    events = [e for e in hosted["execution_schedule"] if e.get("replica") == replica]
    need(len(events) == 30 and [e["source_event"] for e in events] == list(range(30)), "replica-0 events")
    need(hosted["live"] == 14336 and hosted["m"] == 73, "selected live families / width")
    need(all(b == 0 for b in hosted["hosting"]["banks"]), "selected template has no helper banks")
    strip = ("replica", "replicas", "source_event", "time", "provider_id", "entry_exit_phase_adapters")
    base_events = [{k: v for k, v in e.items() if k not in strip} for e in base["execution_schedule"][:30]]
    host_events = [{k: v for k, v in e.items() if k not in strip} for e in events]
    need(base_events == host_events, "hosted replica-0 schedule equals the base template schedule")
    return events


def level_timeline(hosted, base, events, mutate=None):
    """timeline[k] = (kind, source_event, levels of pairs 0..3 after it); timeline[0] = entry."""
    recipe = hosted["recipe"]
    local_pairs = [e["pair"] for e in recipe if e["kind"] == "local"]
    need(local_pairs == [0, 0, 0, 1, 1, 2, 2, 3, 3], "literal local pair binding (PR2346 recipe)")
    need(all(e["reverse"] == (e["stage"] % 2 == 1) for e in recipe if e["kind"] == "local"),
         "odd stages backward")
    stage_pair = dict(enumerate(local_pairs))
    base_rank = {c["child"]: c["rank"] for c in base["idle_children"] if c["port"] == 0}
    hosted_total = {}
    for c in hosted["idle_children"]:
        hosted_total.setdefault(c["child"], set()).add(c["hosted"] + c["rank"])
    level = [-1, -1, -1, -1]
    timeline = [("entry", None, tuple(level))]
    for e in events:
        if e["kind"] == "local_cover_sweep":
            p = stage_pair[e["stage"]]
            need(level[p] == e["stage"] - 1, "local stage %d starts one level below" % e["stage"])
            level[p] = e["stage"]
        elif e["kind"] == "idle_cover_sweep":
            p, frm, to = e["pair"], e["from_level"], e["to_level"]
            if mutate == "idle_to_level" and e["source_event"] == 5:
                to += 1
            need(level[p] == frm and to >= frm, "idle sweep continues the pair's level")
            if to > frm:
                want = COORDS_PER_LEVEL * (to - frm)
                need([base_rank[c] for c in e["child_indices"]] == [want, want],
                     "base idle children: eight coordinates per level (event %d)" % e["source_event"])
                for c in e["child_indices"]:
                    need(all(t <= want for t in hosted_total.get(c, {want})),
                         "hosted + remaining rank never exceeds the base child rank")
            level[p] = to
        timeline.append((e["kind"], e["source_event"], tuple(level)))
    need(level == [8, 8, 8, 8], "every pair ends at level 8 (nine levels = 72 paid coordinates)")
    return timeline, stage_pair


def lv_before(timeline, event):
    return timeline[event][2]


def lv_after(timeline, event):
    return timeline[event + 1][2]


def catch_up(cap, cons, pair, rows):
    gap = cons[pair] - cap[pair]
    need(gap >= 0, "consumer frame at or above the capture frame")
    return COORDS_PER_LEVEL * gap * rows


def routes(timeline, events, stage_pair, mutate=None):
    end = timeline[-1][2]
    locals_of = {k: [e["source_event"] for e in events if e["kind"] == "local_cover_sweep"
                     and stage_pair[e["stage"]] == k] for k in range(4)}
    out = {}
    rows = 15 if mutate == "pr2540_rows" else 16
    after_b1 = lv_after(timeline, 4 if mutate == "pr2540_incidence" else 1)
    out["PR2540_early_records"] = {"rows": 16, "capture": "after F0 (event 0)", "consumer": "F_U1 after B1 (event 1)",
                                   "capture_level": lv_after(timeline, 0)[0], "consumer_level": after_b1[0],
                                   "mass": catch_up(lv_after(timeline, 0), after_b1, 0, rows)}
    init = []
    for k in range(4):
        ev = locals_of[k][0]
        lv = list(lv_before(timeline, ev))
        if mutate == "init_capture_level" and k == 1:
            lv[1] = -1
        init.append({"bank": k, "capture_before_event": ev, "capture_level": lv[k], "rows": 16,
                     "consumer_level": end[k], "mass": catch_up(lv, end, k, 16)})
    da = []
    for k in range(3):
        ev = [x for x in locals_of[k] if events[x]["stage"] % 2 == 1][0]
        lv = lv_after(timeline, ev)
        da.append({"bank": k, "capture_after_event": ev, "capture_level": lv[k], "rows": 8,
                   "consumer_level": end[k], "mass": catch_up(lv, end, k, 8)})
    out["INIT64"], out["d_A"] = init, da
    out["INIT64_plus_dA_mass"] = sum(r["mass"] for r in init + da)
    out["d_A_only_mass"] = sum(r["mass"] for r in da)
    per_array = sorted([r["mass"] // r["rows"] for r in init + da for _ in range(r["rows"])])
    need(len(per_array) == 88, "88 stated arrays per owner per replica")
    out["cheapest_62_of_stated_captures_mass"] = sum(per_array[:62])
    touch = min(e["source_event"] for e in events
                if (e["kind"] == "local_cover_sweep" and stage_pair[e["stage"]] == 3)
                or (e["kind"] == "idle_cover_sweep" and e["pair"] == 3 and e["to_level"] > e["from_level"])
                or (e["kind"] == "bridge" and 3 in (e["src"], e["dst"])))
    if mutate == "witness_window":
        touch += 1
    calls = [e["stage"] for e in events if e["kind"] == "local_cover_sweep" and e["source_event"] < touch]
    out["zero_witness"] = {"pair": 3, "side": "Y (replica-0 families 784..895)", "capture": "entry",
                           "consumer_before_event": touch, "consumer_before_time": events[touch]["time"],
                           "calls_in_window": calls,
                           "law_mass_per_array": catch_up(timeline[0][2], lv_before(timeline, touch), 3, 1),
                           "S_per_array": len(calls), "C_mass_per_array": 8 * len(calls)}
    out["deferred_family_example"] = {
        "pair": 0, "side": "X (replica-0 families 0..111)", "capture": "after B5 (event 13)", "consumer": "end",
        "capture_time": events[13]["time"],
        "law_mass_per_array": catch_up(lv_after(timeline, 13), end, 0, 1), "C_mass_per_array": 8 * 3}
    return out


def hosting_checks(hosted, r, mutate=None):
    """Hosted helper residuals also change idle frames (idle-axis hosting moves factors to their
    invocation time). The witness and the deferred example use families that host nothing
    before the relevant time, and whose idle child is not partly hosted."""
    slots = hosted["hosting"]["pooled_slots"]
    idle = {(c["family"], c["child"]): c for c in hosted["idle_children"] if c["replica"] == 0}
    zw, df = r["zero_witness"], r["deferred_family_example"]
    limit = zw["consumer_before_time"] + (17 if mutate == "hosting_window" else 0)
    y3 = range(784, 896)
    early_y3 = [x for x in slots if x["owner_replica"] == 0 and x["family"] in y3 and x["time"] < limit]
    need(not early_y3, "no hosted residual on pair-3 Y families before the witness consumer")
    need(all(idle[(f, 10)]["hosted"] == 0 and idle[(f, 10)]["rank"] == 48 for f in y3),
         "pair-3 Y sweep -1 -> 5 is an unhosted rank-48 idle child")
    early_x3 = [x for x in slots if x["owner_replica"] == 0 and 672 <= x["family"] <= 783 and x["time"] < limit]
    x0 = range(0, 112)
    early_x0 = [x for x in slots if x["owner_replica"] == 0 and x["family"] in x0 and x["time"] <= df["capture_time"]]
    need(not early_x0, "no hosted residual on pair-0 X families before the deferred capture")
    need(all(idle[(f, 12)]["hosted"] == 0 and idle[(f, 12)]["rank"] == 48 for f in x0),
         "pair-0 X sweep 2 -> 8 is an unhosted rank-48 idle child")
    # Route captures sit at exact levels: every residual hosted on the source pair before the
    # capture belongs to an idle sweep that has already reached the capture level.
    sweep_to = {}
    for e in hosted["execution_schedule"]:
        if e.get("replica") == 0 and e["kind"] == "idle_cover_sweep":
            for c in e["child_indices"]:
                sweep_to[c] = (e["pair"], e["to_level"])
    times = {e["source_event"]: e["time"] for e in hosted["execution_schedule"] if e.get("replica") == 0}
    checked = 0
    captures = [(x["bank"], times[x["capture_before_event"]], x["capture_level"]) for x in r["INIT64"]]
    captures += [(x["bank"], times[x["capture_after_event"]], x["capture_level"]) for x in r["d_A"]]
    for pair, t_cap, level in captures:
        for x in slots:
            if x["owner_replica"] == 0 and 224 * pair <= x["family"] < 224 * (pair + 1) and x["time"] <= t_cap:
                need(sweep_to[x["child"]] [0] == pair and sweep_to[x["child"]][1] <= level,
                     "hosted residual before a route capture belongs to an already-reached level")
                checked += 1
    return {"pair3_Y_hosted_slots_in_window": 0, "pair3_X_hosted_slots_in_window": len(early_x3),
            "pair0_X_hosted_slots_before_deferred_capture": 0, "route_capture_prior_slots_checked": checked}


def array_calls(dA_lifetimes=(8, 5, 3)):
    return 16 * (9 + 6 + 4 + 2) + 8 * sum(dA_lifetimes)


# ------------------------------------------------------------------ 5. pricing
def load_ceiling():
    sys.path.insert(0, str(ROOT / "research/complex-local-word-ceiling"))
    try:
        import ceiling
    finally:
        sys.path.pop(0)
    need(hashlib.sha256(Path(ceiling.__file__).read_bytes()).hexdigest() ==
         PINS["research/complex-local-word-ceiling/ceiling.py"], "imported ceiling.py is the pinned file")
    return ceiling


def qq16_profile():
    core = {r: n for r, n in SELECTED.items() if r != 8}
    need(sum(r * n for r, n in core.items()) == 5522, "retained QQ16 core mass 5522")
    back = dict(core)
    back[1] += 24
    fwd = dict(core)
    fwd[1] += 8
    need(sum(r * n for r, n in back.items()) == 5546 and sum(r * n for r, n in fwd.items()) == 5530,
         "QQ16 native masses 5546 (B) / 5530 (F)")
    return {r: Q(5 * fwd[r] + 4 * back[r], 9) for r in core}


def priced(units, pricing):
    local = dict(qq16_profile())
    n = Q(units, STAGES)
    if pricing == "rank8":
        local[8] = local.get(8, 0) + n / 8
    elif pricing != "idle":
        raise ValueError(pricing)
    return local, n


def kappa_cap(C, units, pricing):
    local, centre = priced(units, pricing)
    try:
        a = C.ceiling(local, M, FAMILIES, STAGES, centre, grid=GRID)[1]
    except ValueError:
        return None
    return a / (1 + a)


def beats(C, units, pricing, kappa):
    """Certified: does the stated relaxation exceed `kappa` (relax(a_t) < 1 at a_t = kappa/(1-kappa))?"""
    local, centre = priced(units, pricing)
    try:
        lo, hi = C.relax(local, M, FAMILIES, STAGES, centre, kappa / (1 - kappa))
    except ValueError:
        return False                   # local word pays more than the coverage law allows
    need(hi < 1 or lo > 1, "enclosure separates the comparison point")
    return hi < 1


def breakeven(C, pricing, kappa, step):
    lo, hi = 0, 1 << 13
    need(beats(C, 0, pricing, kappa) and not beats(C, hi * step, pricing, kappa), "bracket")
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if beats(C, mid * step, pricing, kappa):
            lo = mid
        else:
            hi = mid
    return lo


def pricing_checks(C, route_mass):
    out = {}
    free = kappa_cap(C, 0, "idle")
    need(abs(free - Q("0.0047020509675915")) < Q(1, 10 ** 13), "free-controller cap 0.0047020509675915")
    out["free_controller_C0_kappa_cap"] = "%.16f" % free
    need(kappa_cap(C, 895, "idle") is not None and kappa_cap(C, 896, "idle") is None, "896 threshold (idle)")
    need(kappa_cap(C, 888, "rank8") is not None and kappa_cap(C, 896, "rank8") is None, "896 threshold (rank-8)")
    out["no_saving_threshold_units_per_replica"] = 896
    centre = kappa_cap(C, 576, "rank8")
    local, _ = priced(576, "rank8")
    need(local[8] == 8 and centre == (lambda a: a / (1 + a))(
        C.ceiling({**qq16_profile(), 8: Q(8)}, M, FAMILIES, STAGES, 64, grid=GRID)[1]),
        "576 rank-8 units per replica = eight rank-8 centre copies per call with C = 64")
    out["centre_path_576_kappa_cap"] = "%.16f" % centre
    be_s = breakeven(C, "idle", PR2474_KAPPA, 1)
    be_c = breakeven(C, "rank8", PR2474_KAPPA, 8)
    need((be_s, be_c) == (573, 71), "#1166 price-gate break-evens 573 (S) / 71 (C) reproduced")
    need(kappa_cap(C, 573, "idle") > PR2474_KAPPA >= kappa_cap(C, 574, "idle"), "ceiling agrees at 573/574")
    need(kappa_cap(C, 568, "rank8") > PR2474_KAPPA >= kappa_cap(C, 576, "rank8"), "ceiling agrees at 71/72")
    out["breakeven_vs_PR2474"] = {"S_array_calls": be_s, "C_array_calls": be_c}
    table = {}
    for name, kappa in (("selected_1094", SELECTED_KAPPA), ("PR2474", PR2474_KAPPA), ("PR2843", PR2843_KAPPA),
                        ("PR2848", PR2848_KAPPA), ("bit_endpoint_PR589", BIT_ENDPOINT)):
        table[name] = {"kappa": str(kappa), "idle_units": breakeven(C, "idle", kappa, 1),
                       "rank8_units": 8 * breakeven(C, "rank8", kappa, 8)}
    out["mass_breakeven_units_per_replica"] = table
    out["routes"] = {}
    for name, mass in route_mass.items():
        k_idle, k_r8 = kappa_cap(C, mass, "idle"), kappa_cap(C, mass, "rank8")
        out["routes"][name] = {"units_per_replica": mass,
                               "idle_priced_kappa_cap": None if k_idle is None else "%.16f" % k_idle,
                               "rank8_priced_kappa_cap": None if k_r8 is None else "%.16f" % k_r8}
    return out


# ------------------------------------------------------------------ 6. exact frame model
class Lattice:
    """Subspaces of GF(p)^n, indexed; join with one vector; membership."""

    def __init__(self, p, n):
        self.p, self.n = p, n
        self.vecs = list(itertools.product(range(p), repeat=n))
        self.zero = tuple([0] * n)
        self.subs, self.index = [], {}
        self._add(frozenset([self.zero]))
        frontier = [0]
        while frontier:
            nxt = []
            for s in frontier:
                for v in self.vecs:
                    t = self.close(self.subs[s] | {v})
                    if t not in self.index:
                        nxt.append(self._add(t))
            frontier = nxt
        self.join = [[self.index[self.close(s | {v})] for v in self.vecs] for s in self.subs]
        self.vid = {v: i for i, v in enumerate(self.vecs)}
        self.dim = [round(math.log(len(s), p)) for s in self.subs]

    def _add(self, s):
        self.index[s] = len(self.subs)
        self.subs.append(s)
        return self.index[s]

    def close(self, vectors):
        space = {self.zero}
        changed = True
        vectors = set(vectors)
        while changed:
            changed = False
            for a in list(space):
                for b in vectors:
                    for c in range(1, self.p):
                        w = tuple((x + c * y) % self.p for x, y in zip(a, b))
                        if w not in space:
                            space.add(w)
                            changed = True
        return frozenset(space)

    def span(self, vectors):
        return self.index[self.close(set(vectors))]


def bfs_all(L, start, H):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        d = dist[state]
        for h in range(H + 1):
            for v in L.subs[state[h]]:
                if v == L.zero:
                    continue
                vi = L.vid[v]
                for g in (h - 1, h + 1):
                    if 0 <= g <= H and v not in L.subs[state[g]]:
                        nxt = list(state)
                        nxt[g] = L.join[state[g]][vi]
                        nxt = tuple(nxt)
                        if nxt not in dist:
                            dist[nxt] = d + 1
                            queue.append(nxt)
    return dist


def min_mass(L, dist, demand):
    best = None
    for state, d in dist.items():
        if all(v in L.subs[state[h]] for v, h in demand) and (best is None or d < best):
            best = d
    need(best is not None, "demand unreachable")
    return best


def cut_bound(L, entry, demand, H, directions=("up", "down")):
    total = 0
    for j in range(1, H + 1):
        for side, keep in (("up", lambda h: h >= j), ("down", lambda h: h < j)):
            if side not in directions:
                continue
            e = [v for v, h in entry if keep(h)]
            d = [v for v, h in demand if keep(h)]
            total += L.dim[L.span(e + d)] - L.dim[L.span(e)]
    return total


def meeting_formula(L, R, P, O, hr, hp, hc):
    rho_r = L.dim[L.span(P + O)] - L.dim[L.span(P)]
    rho_p = L.dim[L.span(R + O)] - L.dim[L.span(R)]
    rho_o = L.dim[L.span(O)]
    return min(rho_r * abs(x - hr) + rho_p * abs(x - hp) + rho_o * abs(x - hc)
               for x in range(min(hr, hp, hc), max(hr, hp, hc) + 1))


def basis(L, s):
    out = []
    for v in sorted(L.subs[s]):
        if v != L.zero and v not in L.subs[L.span(out)]:
            out.append(v)
    return out


def frame_model_checks():
    stats = {"domains": [], "record_partner_instances": 0, "general_instances": 0,
             "general_tight": 0, "upward_only_failures": 0}
    for p, n, H in ((2, 2, 3), (3, 2, 2), (2, 3, 2)):
        L = Lattice(p, n)
        pairs = [(a, b) for a, b in itertools.product(range(len(L.subs)), repeat=2)
                 if len(L.subs[a] & L.subs[b]) == 1]
        complete = (p, n) != (2, 3)
        if not complete:      # GF(2)^3: deterministic sample of independent (R, P) pairs (seed 59)
            pairs = sorted(random.Random(59).sample(pairs, FRAME_SAMPLE))
        stats["domains"].append({"field": "GF(%d)" % p, "dim": n, "levels": H + 1, "subspaces": len(L.subs),
                                 "independent_RP_pairs": len(pairs),
                                 "coverage": "complete" if complete else "seeded sample (random.Random(59))"})
        for R_s, P_s in pairs:
            R, P = basis(L, R_s), basis(L, P_s)
            RP = L.subs[L.span(R + P)]
            outs = [o for o in range(len(L.subs)) if L.subs[o] <= RP and L.dim[o] > 0]
            for hr, hp in itertools.product(range(H + 1), repeat=2):
                st = [L.span([])] * (H + 1)
                st[hr] = L.span(R + (P if hp == hr else []))
                if hp != hr:
                    st[hp] = L.span(P)
                dist = bfs_all(L, tuple(st), H)
                entry = [(v, hr) for v in R] + [(v, hp) for v in P]
                for o in outs:
                    O = basis(L, o)
                    for hc in range(H + 1):
                        demand = [(v, hc) for v in O] + [(v, hp) for v in P]
                        opt = min_mass(L, dist, demand)
                        lb = cut_bound(L, entry, demand, H)
                        mf = meeting_formula(L, R, P, O, hr, hp, hc)
                        need(lb <= opt, "Lemma 1 soundness")
                        need(opt == lb == mf, "Proposition 3 exactness %s" % ((p, n, H, hr, hp, hc),))
                        if cut_bound(L, entry, demand, H, ("up",)) != opt:
                            stats["upward_only_failures"] += 1
                        stats["record_partner_instances"] += 1
        if (p, n, H) == (2, 2, 3):
            placed = [(v, h) for v in L.vecs if v != L.zero for h in range(H + 1)]
            sets = list(itertools.chain(itertools.combinations(placed, 1), itertools.combinations(placed, 2)))
            for e_rows in sets:
                st = [L.span([])] * (H + 1)
                for v, h in e_rows:
                    st[h] = L.join[st[h]][L.vid[v]]
                dist = bfs_all(L, tuple(st), H)
                avail = L.subs[L.span([v for v, _ in e_rows])]
                for d_rows in sets:
                    if all(v in avail for v, _ in d_rows):
                        opt = min_mass(L, dist, list(d_rows))
                        lb = cut_bound(L, list(e_rows), list(d_rows), H)
                        need(lb <= opt, "Lemma 1 soundness (general)")
                        stats["general_instances"] += 1
                        stats["general_tight"] += int(lb == opt)
    need(stats["upward_only_failures"] > 0, "negative control: an upward-only bound must fail somewhere")
    return stats


# ------------------------------------------------------------------ 7. tensor toy
HAD = ((1, 1), (1, -1))


def apply_axis(x, axis, inverse=False):
    y = [Q(0)] * 4
    for i in range(4):
        bits = [i & 1, (i >> 1) & 1]
        for b in (0, 1):
            jb = list(bits)
            jb[axis] = b
            y[i] += Q(HAD[bits[axis]][b]) * (Q(1, 2) if inverse else 1) * x[jb[0] + 2 * jb[1]]
    return y


def in_frame(x, axes):
    for a in axes:
        x = apply_axis(x, a)
    return x


def add(*xs):
    return [sum(t) for t in zip(*xs)]


def tensor_toy():
    rng = random.Random(20261016)
    naive_wrong = wrong_axis = 0
    trials = 25
    for _ in range(trials):
        x = [Q(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(4)]
        dx = [Q(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(4)]
        record = in_frame(x, [0])                       # captured after call 1 (axis 0 advanced)
        current = in_frame(add(x, dx), [0, 1])          # after call 2 (axis 1 advanced)
        want = in_frame(add(x, x, dx), [0, 1])          # consumer: x + (x + dx) in the current frame
        naive_wrong += add(record, current) != want
        need(add(apply_axis(record, 1), current) == want, "paid axis-1 catch-up repairs the output")
        wrong_axis += add(apply_axis(record, 0), current) != want
        down = apply_axis(current, 1, inverse=True)     # partner descends to the record's frame
        need(apply_axis(add(record, down), 1) == want, "partner descent + output climb also repairs it")
        need(add(record, in_frame(x, [0])) == in_frame(add(x, x), [0]), "same-frame consumer needs no catch-up")
    need(naive_wrong == trials, "negative control: omitting catch-up must give a wrong output")
    need(wrong_axis == trials, "negative control: catch-up on the wrong axis must fail")
    return {"trials": trials, "naive_wrong": naive_wrong, "wrong_axis_wrong": wrong_axis, "repaired_correct": trials}


# ------------------------------------------------------------------ 8. negative controls
def expect_failure(label, fn):
    try:
        fn()
    except CheckFailure:
        return label
    raise CheckFailure("negative control unexpectedly passed: " + label)


def negative_controls(hosted, base, events, C):
    tl, sp = level_timeline(hosted, base, events)

    def mutated(kind):
        return routes(tl, events, sp, mutate=kind)

    out = [
        expect_failure("idle sweep to_level +1", lambda: level_timeline(hosted, base, events, "idle_to_level")),
        expect_failure("PR2540 rows 16 -> 15", lambda: need(mutated("pr2540_rows")["PR2540_early_records"]["mass"] == 128, "")),
        expect_failure("PR2540 two incidences", lambda: need(mutated("pr2540_incidence")["PR2540_early_records"]["mass"] == 128, "")),
        expect_failure("INIT bank-1 capture level -1", lambda: need(mutated("init_capture_level")["INIT64_plus_dA_mass"] == 3648, "")),
        expect_failure("zero witness extended past first pair-3 touch",
                       lambda: need(mutated("witness_window")["zero_witness"]["law_mass_per_array"] == 0, "")),
        expect_failure("uniform lifetimes give 464 array-calls", lambda: need(array_calls((7, 5, 3)) == 464, "")),
        expect_failure("witness window stretched into pair-3 Y hosting (time + 17)",
                       lambda: hosting_checks(hosted, routes(tl, events, sp), mutate="hosting_window")),
        expect_failure("895 units/replica has no saving", lambda: need(kappa_cap(C, 895, "idle") is None, "")),
        expect_failure("break-even 574 (S) against PR2474", lambda: need(beats(C, 574, "idle", PR2474_KAPPA), "")),
    ]
    return out


# ------------------------------------------------------------------ main
def main(argv):
    result = {"schema": "retained-array-catch-up/1", "sources": check_sources()}
    hosted, base = load_templates()
    events = replica_events(hosted, base)
    timeline, stage_pair = level_timeline(hosted, base, events)
    result["levels"] = [{"after": "entry" if s is None else "event %d %s" % (s, k), "pairs_0_3": list(lv)}
                        for k, s, lv in timeline]
    r = routes(timeline, events, stage_pair)
    need(r["PR2540_early_records"]["mass"] == 128, "PR2540: 16 records x one level = 128 (its 16 H8)")
    need([x["capture_level"] for x in r["INIT64"]] == [-1, 2, 4, 6], "INIT capture levels -1/2/4/6")
    need([x["mass"] for x in r["INIT64"]] == [1152, 768, 512, 256], "INIT climbs 72/48/32/16 per array")
    need([x["capture_level"] for x in r["d_A"]] == [1, 3, 5], "d_A capture levels 1/3/5")
    need([x["mass"] for x in r["d_A"]] == [448, 320, 192], "d_A climbs 56/40/24 per array")
    need(r["INIT64_plus_dA_mass"] == 3648 and r["d_A_only_mass"] == 960, "INIT64 + d_A 3648; d_A alone 960")
    need(r["cheapest_62_of_stated_captures_mass"] == 1952, "cheapest 62 stated captures 1952")
    zw = r["zero_witness"]
    need(zw["law_mass_per_array"] == 0 and zw["calls_in_window"] == [0, 1, 2, 3, 4, 5]
         and zw["consumer_before_event"] == 14, "zero witness: pair 3 untouched through stages 0..5")
    dfe = r["deferred_family_example"]
    need(dfe["law_mass_per_array"] == 48 and dfe["C_mass_per_array"] == 24, "deferred-family example: law 48 > C 24")
    r["hosting"] = hosting_checks(hosted, r)
    need(r["hosting"]["pair3_X_hosted_slots_in_window"] == 160, "pair-3 X streams host 160 residuals in the window")
    centre_path = 8 * 8 * STAGES
    pr2197 = 8 * 18
    h_U1, h_L, h_q, h_I = 17, 9, 1, 0
    need(centre_path == 576 and pr2197 == 144, "centre path 576 / PR2197 144")
    need(224 * (h_U1 - h_L) == 1792 and 112 * (h_U1 - h_q) + 112 * (h_U1 - h_I) == 3696, "PR2678 1792 / 3696")
    need(h_L == 9 and h_U1 - h_L == COORDS_PER_LEVEL, "PR2540 frames: F_L nine axes, F_U1 seventeen (one level)")
    published, uniform = array_calls(), array_calls((7, 5, 3))
    need(published == 464 and uniform == 456 and 8 * uniform == r["INIT64_plus_dA_mass"],
         "array-calls 464 published / 456 uniform; law = 8 x uniform array-calls")
    r["array_calls"] = {"published": published, "uniform_lifetime": uniform, "S_units_published": published,
                        "C_mass_published": 8 * published, "C_mass_uniform": 8 * uniform}
    r["controls"] = {"PR2540": 128, "PR2197": pr2197, "PR2678_common_FL": 1792, "PR2678_entry": 3696,
                     "centre_path_per_replica": centre_path}
    # #2707 versus PR2540 child moments: 336 H1 versus 224 H1 + 16 H8 differ by 112 H1 - 16 H8.
    # 16 * 8^(1-a) > 112 for 0 <= a <= 1/16 because 8^(15/16) > 7, i.e. 8^15 > 7^16 (exact integers).
    need(8 ** 15 > 7 ** 16 and 336 - 224 == 112 and 16 * 8 == 128, "PR2707 numerator sign: 8^15 > 7^16")
    r["qq16_gate"] = {"retained_caller_retention_mass": 128, "retained_caller_H8": 16,
                      "zero_retention_H1_minus_retained_H1": 112, "sign_certificate": "8^15 > 7^16"}
    result["routes"] = r
    C = load_ceiling()
    result["pricing"] = pricing_checks(C, {
        "INIT64_plus_dA_law": r["INIT64_plus_dA_mass"], "d_A_only_law": r["d_A_only_mass"],
        "cheapest_62_stated_law": r["cheapest_62_of_stated_captures_mass"],
        "INIT64_plus_dA_S_published": published, "INIT64_plus_dA_C_published": 8 * published})
    for name in ("INIT64_plus_dA_law", "d_A_only_law", "cheapest_62_stated_law", "INIT64_plus_dA_C_published"):
        need(result["pricing"]["routes"][name]["idle_priced_kappa_cap"] is None, name + ": no positive saving")
    need(result["pricing"]["routes"]["INIT64_plus_dA_S_published"]["idle_priced_kappa_cap"] is not None,
         "S-priced 464 keeps a positive ceiling (the #1166 table)")
    result["frame_model"] = frame_model_checks()
    result["tensor_toy"] = tensor_toy()
    result["negative_controls_rejected"] = negative_controls(hosted, base, events, C)
    n_neg = len(result["negative_controls_rejected"]) + 3   # + upward-only bound + two toy controls
    fm = result["frame_model"]
    status = ("PASS_RETAINED_ARRAY_CATCH_UP pr2540=128 init64_dA=3648 dA_only=960 cheapest62=1952 "
              "array_calls=464/456 no_saving=896 breakeven_S=573 breakeven_C=71 zero_witness_calls=6 "
              "frame_instances=%d/%d negative_controls=%d no_new_kappa"
              % (fm["record_partner_instances"], fm["general_instances"], n_neg))
    result["status"] = status
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    target = PACKAGE / "RESULT.json"
    if "--write" in argv:
        if target.exists() and target.read_text() != text and "--force" not in argv:
            raise CheckFailure("RESULT.json differs; use --write --force to replace it")
        target.write_text(text)
    elif target.exists():
        need(json.loads(target.read_text()) == json.loads(text), "RESULT.json matches the recomputation")
    print(status)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except CheckFailure as exc:
        print("FAIL:", exc)
        sys.exit(1)
