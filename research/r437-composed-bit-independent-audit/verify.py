"""Independent exact word-level audit of PR #3647's composed R437 bit word.

Usage (repository root):  python3 -I -B research/r437-composed-bit-independent-audit/verify.py [--write]

Inputs: the selected #589 word and #1043's FRAME-PATHS.json from main, plus PR #3647's
R438 (helper464 GL) word, R437 word and R437 record stream vendored under inputs/ (all
sha256-pinned in SOURCES.json).
Semantics: wordsem.py (written for this audit from the format of the selected #589 package).
Without --write the computed result must equal the committed RESULT.json.
Standard library only.  Sagar Thakrar (thakrarsagar), with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5).  Apache-2.0.
"""
import collections
import copy
import gzip
import hashlib
import json
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from wordsem import (Geometry, Reject, bits, canonical, check_final_frames, check_identity,  # noqa: E402
                     check_pullback, forward, load, need, paths, profile, pullback, rebuild_DC,
                     reverse_orientation)
import compose  # noqa: E402
import records  # noqa: E402
from compose import apply  # noqa: E402

W589 = 'research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz'
PATHS1043 = 'research/bit-boundary-persistence/FRAME-PATHS.json'
R438 = 'research/r437-composed-bit-independent-audit/inputs/FINAL-R438-WORD.json.gz'
R437 = 'research/r437-composed-bit-independent-audit/inputs/R437-COMPOSED-WORD.json.gz'
RECORDS = 'research/r437-composed-bit-independent-audit/inputs/R437-RECORDS.bin.gz'


def sha(path):
    with open(os.path.join(ROOT, path), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pins():
    src = json.load(open(os.path.join(HERE, 'SOURCES.json')))
    out = {}
    for f in src['files'] + src['snapshot']:
        path = f.get('path') or 'research/r437-composed-bit-independent-audit/' + f['local']
        if f.get('usage', 'input') == 'input' or 'local' in f:
            need(sha(path) == f['sha256'], 'pin mismatch for %s' % path)
            out[path] = f['sha256']
    return out


def adds(w):
    c = {s: sum(len(g[2]) for g in w[s]) for s in 'DABC'}
    c['scatter'] = sum(len(r) for r in w['scatter'])
    c['total'] = sum(c.values())
    return c


def interface(w, geo):
    """Hypotheses of the selected interleaved scalar-interface lemma (H1-H5) and its conclusion."""
    v, n = w['v'], 2 * w['v'] + w['R']
    y = lambda r: v <= r < 2 * v
    out = {}
    out['H1'] = not any(not y(g[1]) and any(y(s) for s in g[2]) for sec in 'DABC' for g in w[sec])
    out['H2'] = all(len(w['frames'][g[0]]) == 0 and y(g[1]) and all(s >= 2 * v for s in g[2]) for g in w['D'])
    out['H3'] = (all(not y(g[1]) for g in w['A']) and all(2 * v <= q < n for q in w['ret'])
                 and all(y(g[1]) or all(not y(s) for s in g[2]) for g in w['B']))
    D, C = rebuild_DC(w)
    out['H4_C_literal_reverse'] = C == w['C']
    out['D0_rebuilt'] = D == w['D']
    raw, _, _, _ = forward(w, geo, sections=('A', 'scatter', 'B'), frames_on=False)
    ym, xm = ((1 << v) - 1) << v, (1 << v) - 1
    out['H5_V_identity'] = all(raw[v + t] & ym == 1 << (v + t) for t in range(v))
    out['U_block'] = all(raw[r] & ym == 0 for r in range(n) if not y(r))
    out['J_identity'] = all(raw[v + t] & xm == 1 << t for t in range(v))
    return out


def word_checks(name, w, geo):
    """Primary forward method, reverse pull-back, entrywise agreement, reverse orientation."""
    v, n = w['v'], 2 * w['v'] + w['R']
    val, cur, climbs, copies = forward(w, geo)
    check_final_frames(w, geo)
    bad = check_identity(w, val)
    col = pullback(w)
    badp = check_pullback(w, col)
    agree = all(((val[r] >> j) & 1) == ((col[j] >> r) & 1) for r in range(n) for j in range(n))
    rev = check_identity(w, reverse_orientation(w, geo))
    sw = {s: sum(1 for g in w[s] if g[1] < v) for s in 'DABC'}
    return dict(columns=n, sources=v, helpers=w['R'], forward_bad_columns=len(bad), pullback_bad_columns=len(badp),
                methods_agree_entrywise=agree, reverse_orientation_bad_columns=len(rev),
                copy_ranks=[c[2] for c in copies], profile=profile(geo, climbs, copies),
                mass=sum(k * x for k, x in profile(geo, climbs, copies).items()),
                scalar_adds=adds(w), gates={s: len(w[s]) for s in 'DABC'}, source_writes=sw,
                interface=interface(w, geo)), (val, climbs, copies)


def trace(w, akeys):
    """Per gate (origin key): destination, frame, value after, operand values; C gates are keyed
    by the A/B gate they literally reverse."""
    geo = Geometry(w)
    v = w['v']
    zkeys = [k for sec, ks in (('A', akeys), ('B', [('B', i) for i in range(len(w['B']))]))
             for k, g in zip(ks, w[sec]) if not (v <= g[1] < 2 * v)]
    ckeys = [('C',) + k for k in reversed(zkeys)]
    need(len(ckeys) == len(w['C']), 'C length')
    out, climbs = {}, []
    keymap = {'A': akeys, 'B': [('B', i) for i in range(len(w['B']))], 'C': ckeys}

    def tr(ev, val, cur):
        sec = ev[0]
        if sec in keymap:
            k = keymap[sec][ev[1]]
            out[k] = (ev[3], ev[2], val[ev[3]], tuple(val[s] for s in ev[4]), ev[4])
    _, _, cl, _ = forward(w, geo, trace=tr)
    # A move inside an edited window is dated by the last unchanged gate before it, so that a
    # re-synthesized node is compared window by window and any move across an unchanged gate shows.
    anchor = {}
    for sec in ('A', 'B', 'C'):
        last = None
        for k in keymap[sec]:
            if unchanged(k):
                last = k
                anchor[k] = k
            else:
                anchor[k] = ('window after', last)
    for r, a, b, where in cl:
        if where[0] in keymap:
            climbs.append((r, a, b, anchor[keymap[where[0]][where[1]]]))
        else:
            climbs.append((r, a, b, where))
    return out, climbs


EDITED_589_A = {compose.E464_DEL, compose.E470_DEL, compose.E470_READ} | set(range(*compose.E464_NODE_AT))


def unchanged(k):
    if k[0] == 'C':
        return unchanged(k[1:])
    return k[0] == 'B' or (k[0] == 'A' and k[1] not in EDITED_589_A)


def project(x, dead, ren):
    y = 0
    for b in bits(x):
        if b not in dead:
            y |= 1 << ren(b)
    return y


def compare(T0, T1, dead, ren, v):
    """Aligned trace comparison of a control/edited word (T1) against a reference (T0)."""
    clean = (1 << (2 * v)) - 1
    full_diff, clean_diff, dirt_cols, sw = [], [], set(), 0
    common = [k for k in T1 if k in T0]
    for k in common:
        d0, f0, x0, s0, r0 = T0[k]
        d1, f1, x1, s1, r1 = T1[k]
        need(ren(d0) == d1 and f0 == f1 and [ren(r) for r in r0] == list(r1), 'aligned gate %s differs in shape' % (k,))
        a = [project(x0, dead, ren)] + [project(s, dead, ren) for s in s0]
        b = [x1] + list(s1)
        if a != b:
            full_diff.append(k)
            for p, q in zip(a, b):
                dirt_cols |= set(bits(p ^ q))
        if [p & clean for p in a] != [q & clean for q in b]:
            clean_diff.append(k)
        if d1 < v:
            sw += 1
    return dict(aligned_gates=len(common), full_value_differences=sorted(full_diff, key=str),
                clean_value_differences=len(clean_diff), differing_columns=sorted(dirt_cols),
                source_write_gates_compared=sw)


def source_history(T, climbs, v):
    acc = {s: [] for s in range(v)}
    for k, (d, f, _, _, regs) in T.items():
        if k[0] == 'C':
            continue
        if d < v:
            acc[d].append((str(k), f, 'write'))
        for s in regs:
            if s < v:
                acc[s].append((str(k), f, 'read'))
    cl = {s: [(str(k), a, b) for r, a, b, k in climbs if r == s] for s in range(v)}
    return acc, cl


def history_diff(h0, h1, v):
    out = {}
    for s in range(v):
        a, b = set(h0[s]), set(h1[s])
        if a != b:
            out[s] = dict(removed=sorted(a - b), added=sorted(b - a))
    return out


def run():
    t0 = time.process_time()
    res = {'status': None, 'pins': pins()}
    w589 = load(os.path.join(ROOT, W589))
    r438 = load(os.path.join(ROOT, R438))
    r437 = load(os.path.join(ROOT, R437))
    fp = json.load(open(os.path.join(ROOT, PATHS1043)))
    v = w589['v']
    geo = Geometry(w589)
    for w in (r438, r437):
        need(all(w[k] == w589[k] for k in ('lines', 'frames', 'scatter', 'v', 'h', 'form', 'format', 'coords',
                                           'ports_geom', 'punctured')), 'geometry or scatter changed')
    res['frame_closure_memberships'] = geo.closure_checks()
    res['frames'] = len(geo.frames)

    # Controls and composition, built literally from selected #589
    node = r438['A'][1985:1995]
    c464, d464, ren464, k464 = apply(w589, node, do464=True)
    c470, d470, ren470, k470 = apply(w589, node, do470=True)
    comp, dcomp, rencomp, kcomp = apply(w589, node, do464=True, do470=True)
    strip = lambda w: {k: x for k, x in w.items() if k != 'stats'}
    res['composition'] = dict(
        e464_node=node,
        c464_equals_pr_R438_except_stats=strip(c464) == strip(r438),
        composed_equals_pr_R437_except_stats=strip(comp) == strip(r437),
        stats_589=w589['stats'], stats_pr_R438=r438['stats'], stats_pr_R437=r437['stats'],
        canonical_sha256=dict(
            w589=hashlib.sha256(canonical(w589)).hexdigest(),
            pr_R438=hashlib.sha256(canonical(r438)).hexdigest(),
            pr_R437=hashlib.sha256(canonical(r437)).hexdigest(),
            c470_rebuilt=hashlib.sha256(canonical(c470)).hexdigest()),
        edit_windows_589_A=dict(e464=[compose.E464_DEL, list(compose.E464_NODE_AT)],
                                e470=[compose.E470_DEL, compose.E470_READ]))

    words = [('selected589', w589), ('C464_pr_R438', r438), ('C470_rebuilt_1043', c470), ('R437_pr', r437)]
    res['words'] = {}
    side = {}
    for name, w in words:
        res['words'][name], side[name] = word_checks(name, w, geo)
    _, cl589, _ = side['selected589']
    _, cl470, _ = side['C470_rebuilt_1043']
    res['frame_paths_1043'] = dict(
        selected589_equals_baseline=[p for _, p in sorted(paths(w589, cl589).items())] == fp['baseline'],
        c470_equals_candidate=[p for _, p in sorted(paths(c470, cl470).items())] == fp['candidate'])
    prof = {k: res['words'][k]['profile'] for k, _ in words}
    delta = lambda a, b: {r: prof[a].get(r, 0) - prof[b].get(r, 0) for r in sorted(set(prof[a]) | set(prof[b]))
                          if prof[a].get(r, 0) != prof[b].get(r, 0)}
    d1, d2, d3 = (delta('C464_pr_R438', 'selected589'), delta('C470_rebuilt_1043', 'selected589'),
                  delta('R437_pr', 'selected589'))
    res['profile_delta'] = dict(e464=d1, e470=d2, composed=d3,
                                additive={r: d1.get(r, 0) + d2.get(r, 0) for r in set(d1) | set(d2)
                                          if d1.get(r, 0) + d2.get(r, 0)} == d3,
                                composed_vs_C464=delta('R437_pr', 'C464_pr_R438'))

    # Aligned traces: what each edit changes, and whether the edits interact
    T589, C589 = trace(w589, [('A', i) for i in range(len(w589['A']))])
    T464, C464 = trace(c464, k464)
    T470, C470 = trace(c470, k470)
    T437, C437 = trace(r437, kcomp)
    res['traces'] = dict(
        e464_vs_589=compare(T589, T464, d464, ren464, v),
        e470_vs_589=compare(T589, T470, d470, ren470, v),
        composed_vs_589=compare(T589, T437, dcomp, rencomp, v),
        composed_vs_C464=compare(T464, T437, [469], lambda r: r - (r > 469), v),
        composed_vs_C470=compare(T470, T437, [464], lambda r: r - (r > 464), v))
    # SOURCE77 late read and source chronology
    h589, sc589 = source_history(T589, C589, v)
    h437, sc437 = source_history(T437, C437, v)
    k_new = ('A470', 0)
    d, f, after, (x77,), regs = T437[k_new]
    res['source77'] = dict(
        new_read=dict(frame=f, frame_lines=geo.frames[f], frame_dim=geo.dim[f], receiver=d,
                      source_value_is_clean_input=x77 == 1 << 77),
        source77_climbs_589=[(str(k), a, b) for r, a, b, k in C589 if r == 77],
        source77_climbs_R437=[(str(k), a, b) for r, a, b, k in C437 if r == 77],
        receiver444_climbs_589=[(str(k), a, b) for r, a, b, k in C589 if r == 444],
        receiver444_climbs_R437=[(str(k), a, b) for r, a, b, k in C437 if r == 444])
    res['source_chronology'] = dict(
        all_source_climbs_identical=sc589 == {s: sc437[s] for s in range(v)},
        access_history_differences=history_diff(h589, h437, v))
    # Records consumed by PR #3647's hosting/invoice stage: byte equality with an independent
    # lowering of the audited word, then record replay in both orientations.
    with open(os.path.join(ROOT, RECORDS), 'rb') as fh:
        raw = gzip.decompress(fh.read())
    mine = records.lower(r437, geo)
    theirs = list(struct.iter_unpack('<6i', raw))
    fwd = records.replay(r437, geo, theirs, False)
    rev = records.replay(r437, geo, theirs, True)
    res['records'] = dict(
        pr_stream_sha256=hashlib.sha256(raw).hexdigest(), pr_stream_bytes=len(raw), records=len(theirs),
        independent_lowering_byte_equal=records.pack(mine) == raw,
        kinds={k: x for k, x in sorted(collections.Counter(r[0] for r in theirs).items())},
        forward=dict(bad_columns=len(fwd[0]), profile=fwd[1], adds=fwd[2], copies=fwd[3]),
        reverse=dict(bad_columns=len(rev[0]), profile=rev[1], adds=rev[2], copies=rev[3]))
    res['mutants'] = mutants(w589, node, geo)
    # Bounded cross-check of the published whole profile (PR #3647 README/COMPOSED-PROOF): split it
    # into 288 local calls of the audited local profile plus a per-replica idle remainder.  The
    # remainder itself (matching, owners, hosting) is NOT rederived here.
    claimed = {1: 380160, 2: 400864, 3: 22176, 4: 26592, 5: 29376, 6: 17376, 7: 26496, 34: 64, 42: 352}
    loc = {int(k): x for k, x in res['words']['R437_pr']['profile'].items()}
    calls, replicas = 9 * 32, 32
    idle = {r: claimed.get(r, 0) - calls * loc.get(r, 0) for r in sorted(set(claimed) | set(loc))}
    need(all(x >= 0 and x % replicas == 0 for x in idle.values()), 'claimed profile does not split')
    res['whole_profile_split'] = dict(
        claimed=claimed, local_calls=calls, replicas=replicas,
        idle_children_per_replica={r: x // replicas for r, x in idle.items() if x},
        rank_mass=sum(r * x for r, x in claimed.items()), live_data=28416,
        deficit=64 * 28416 - sum(r * x for r, x in claimed.items()),
        helper_occurrences=calls * r437['R'])
    drop = lambda gates, q: [[f, d - (d > q), [x - (x > q) for x in srcs if x != q]] for f, d, srcs in gates]
    res['compensation_facts'] = dict(
        e470_D0_is_C464_D0_with_column_deleted=drop(c464['D'], 469) == r437['D'],
        e464_D0_is_589_D0_with_column_deleted=drop(w589['D'], 464) == c464['D'],
        e470_D0_is_589_D0_with_column_deleted=drop(w589['D'], 470) == c470['D'])
    res['cpu_seconds_note'] = 'not recorded (platform dependent)'
    ok = (all(x['forward_bad_columns'] == 0 and x['pullback_bad_columns'] == 0 and x['methods_agree_entrywise']
              and x['reverse_orientation_bad_columns'] == 0 and all(x['interface'].values())
              for x in res['words'].values())
          and res['composition']['c464_equals_pr_R438_except_stats']
          and res['composition']['composed_equals_pr_R437_except_stats']
          and all(res['frame_paths_1043'].values()) and res['profile_delta']['additive']
          and all(t['clean_value_differences'] == 0 for t in res['traces'].values())
          and res['traces']['composed_vs_C464']['full_value_differences'] == []
          and res['traces']['e470_vs_589']['full_value_differences'] == []
          and res['traces']['composed_vs_C470']['full_value_differences'] == res['traces']['e464_vs_589']['full_value_differences']
          and res['source_chronology']['all_source_climbs_identical']
          and res['source77']['new_read']['frame'] == 186 and res['source77']['new_read']['source_value_is_clean_input']
          and res['source77']['source77_climbs_589'] == res['source77']['source77_climbs_R437']
          and all(m['rejected'] == m['expect_rejected'] for m in res['mutants'])
          and res['whole_profile_split']['rank_mass'] == 1808352 and res['whole_profile_split']['deficit'] == 10272
          and res['whole_profile_split']['helper_occurrences'] == 125856
          and res['records']['independent_lowering_byte_equal']
          and res['records']['pr_stream_sha256'] == 'caeb2eb0e417992788c32c1f5812ada60b46d1dfdba9f4ac376299b2dede13cb'
          and all(res['records'][o]['bad_columns'] == 0 and res['records'][o]['profile'] == res['words']['R437_pr']['profile']
                  for o in ('forward', 'reverse')))
    res['status'] = 'PASS_INDEPENDENT_R437_WORD_AUDIT' if ok else 'FAIL'
    return res, time.process_time() - t0


def mutants(w589, node, geo):
    out = []
    v = w589['v']
    T589, C589 = trace(w589, [('A', i) for i in range(len(w589['A']))])
    sc589 = source_history(T589, C589, v)[1]

    def judge(label, w, keys, expect, note):
        reason, ident = None, None
        try:
            r, _ = word_checks(label, w, geo)
            ident = r['forward_bad_columns'] == 0
            if r['forward_bad_columns'] or r['pullback_bad_columns']:
                reason = 'identity fails on %d columns' % r['forward_bad_columns']
            elif not all(r['interface'].values()):
                reason = 'interface fails: ' + ','.join(k for k, x in r['interface'].items() if not x)
            else:
                T, C = trace(w, keys)
                sc = source_history(T, C, v)[1]
                if sc != {s: sc589[s] for s in range(v)}:
                    moved = [s for s in range(v) if sc[s] != sc589[s]]
                    reason = 'source chronology changed for sources %s' % moved
        except Reject as e:
            reason = 'legality: ' + str(e)
        out.append(dict(mutant=label, rejected=reason is not None, reason=reason, expect_rejected=expect, note=note,
                        legal_and_f2_identity=ident))

    comp, dead, ren, keys = apply(w589, node, do464=True, do470=True)
    m = copy.deepcopy(comp)
    m['D'] = []
    judge('drop_D0', m, keys, True, 'no frame-zero dirt compensation')
    m = copy.deepcopy(comp)
    m['C'] = []
    judge('drop_cleanup_C', m, keys, True, 'no literal reverse cleanup')
    # stale compensation/cleanup: selected #589's D0 and C with the two deleted helpers' operands
    # and gates removed and the survivors renamed (what reuse of the old D0/C would give)
    def project_gates(gates):
        g2 = []
        for f, d, srcs in gates:
            if d in dead:
                continue
            ss = [ren(x) for x in srcs if x not in dead]
            if ss:
                g2.append([f, ren(d), ss])
        return g2
    m = copy.deepcopy(comp)
    m['D'] = project_gates(w589['D'])
    judge('stale_D0_from_589', m, keys, True, 'selected D0 reused with the deleted helpers dropped')
    m = copy.deepcopy(comp)
    m['C'] = project_gates(w589['C'])
    judge('stale_C_from_589', m, keys, True, 'selected C reused with the deleted helpers dropped')
    m, _, _, k = apply(w589, node, do464=True, do470=True, read=[79, 444, [77]])
    judge('late_read_at_frame79', m, k, True, 'replacement read at the removed carrier frame 79 (descends SOURCE77)')
    m, _, _, k = apply(w589, node, do464=True, do470=True, read_at=compose.E470_DEL - 1)
    judge('early_read_at_birth', m, k, True, 'replacement read moved to the removed birth position (before A[426])')
    m, _, _, k = apply(w589, node, do464=True, do470=True, read=[186, 444, [77]], read_at=None)
    judge('positive_control_composed', m, k, False, 'the composed word itself')
    # revert one deletion: E470 read removed outright (receiver never gets SOURCE77)
    m, _, _, k = apply(w589, node, do464=True, do470=True, read='drop')
    judge('drop_replacement_read', m, k, True, 'helper470 deleted without the replacement read')
    # naive helper464 deletion: old node with the 464 operand dropped instead of the GL node
    naive = [[f, d, [s for s in srcs if s != 464]] for f, d, srcs in compose.E464_OLD_NODE]
    m, _, _, k = apply(w589, naive, do464=True, do470=True)
    judge('naive_464_deletion', m, k, True, 'old node kept, helper464 operand dropped (no GL re-synthesis)')
    for j in range(len(node)):
        m, _, _, k = apply(w589, node[:j] + node[j + 1:], do464=True, do470=True)
        judge('gl_node_drop_gate_%d' % j, m, k, True, 'one of the ten GL node gates removed')
    return out


def main():
    res, cpu = run()
    path = os.path.join(HERE, 'RESULT.json')
    text = json.dumps(res, indent=1, sort_keys=True, default=list) + '\n'
    if '--write' in sys.argv:
        open(path, 'w').write(text)
    else:
        need(os.path.exists(path) and open(path).read() == text, 'computed result differs from RESULT.json')
    print(res['status'], 'cpu %.1fs' % cpu)
    return 0 if res['status'].startswith('PASS') else 1


if __name__ == '__main__':
    sys.exit(main())
