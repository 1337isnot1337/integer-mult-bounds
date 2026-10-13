"""Compare a fresh run (OUT/*.json) with the shipped expected values (expected.json); one PASS/FAIL line per claim.

Exact fields (integers, fractions, certified interval ends) must be equal.  Model estimates (rank.json) are compared
with relative tolerance 1e-9.  A minrank that the shipped run left as a range 'lo..hi' (SAT timeout) is accepted when
the fresh value lies in that range.
Usage: python check.py OUT expected.json            (python check.py --freeze OUT expected.json writes it)
"""
import json
import pathlib
import sys

FIELDS = {
    'ade': (['unit'], ['v', 'h', 'c0', 'omega', 'cst_lab', 'x_lab', 'Xstar_lab', 'DoverCost_lab']),
    'triple': (['side', 'h'], ['v', 'window', 'span', 'c_centre', 'c0', 'clique_lb', 'z', 'cst_att', 'cst_thmC',
                               'X_att', 'X_thmC', 'lab_min']),
    'lorentz': (['n'], ['v', 'window', 'c0', 'omega', 'z', 'cst_lab', 'per_total', 'x', 'Xstar']),
    'cover': (['unit', 'source'], ['readers', 'rank_readers', 'h', 'cover_lb', 'cover_ub', 'best_section_found']),
    'lorentz_minrank': (['n'], ['omega', 'c0', 'lo', 'hi', 'log']),
    'rank': (['name'], ['h', 'v', 'cst', 'x', 'z', 'Xstar', 'Xs', 'rho_star_abs', 'rho_star_rel', 'a_same_abs',
                        'a_same_rel', 'a_dim_abs', 'a_dim_rel', 'a_read_abs', 'a_read_rel']),
}
TOL = {'rank'}


def strip(row, fields):
    out = {}
    for f in fields:
        v = row.get(f)
        if isinstance(v, dict) and 'hi' in v:
            v = {k: v[k] for k in ('s', 'hi') if k in v}
        out[f] = v
    return out


def load(out):
    d = {}
    for name in FIELDS:
        p = pathlib.Path(out) / (name + '.json')
        if p.exists():
            d[name] = json.loads(p.read_text())
    return d


def key(row, kf):
    return '|'.join(str(row.get(k)) for k in kf)


def freeze(out, exp):
    d = load(out)
    E = {}
    for name, rows in d.items():
        kf, ff = FIELDS[name]
        E[name] = {key(r, kf): dict(strip(r, ff), **({'minrank': r['minrank']} if 'minrank' in r else {})) for r in rows}
    pathlib.Path(exp).write_text(json.dumps(E, indent=1, sort_keys=True, default=str))


def close(a, b, tol):
    if isinstance(a, float) and isinstance(b, (int, float)) and tol:
        return abs(a - b) <= 1e-9 * max(1.0, abs(b)) if abs(b) < 1 else abs(a / b - 1) <= 1e-9
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    return a == b


def minrank_ok(fresh, exp):
    if isinstance(exp, str) and '..' in exp:
        lo, hi = map(int, exp.split('..'))
        if isinstance(fresh, str):
            flo, fhi = map(int, fresh.split('..'))
            return lo <= flo and fhi <= hi
        return lo <= int(fresh) <= hi
    return fresh == exp


def check(out, exp):
    E = json.loads(pathlib.Path(exp).read_text())
    d = load(out)
    bad = 0
    for name, rows in E.items():
        if name not in d:
            print('FAIL %s missing' % name); bad += 1; continue
        kf, ff = FIELDS[name]
        fresh = {key(r, kf): r for r in d[name]}
        for k, ev in rows.items():
            r = fresh.get(k)
            ok = r is not None
            if ok:
                sr = strip(r, ff)
                ok = all(close(sr[f], ev[f], name in TOL) for f in ff)
                if 'minrank' in ev:
                    ok = ok and minrank_ok(r.get('minrank'), ev['minrank'])
            print(('PASS ' if ok else 'FAIL ') + '%s %s' % (name, k), flush=True)
            bad += not ok
    print('%d FAIL' % bad)
    return bad


if __name__ == '__main__':
    if sys.argv[1] == '--freeze':
        freeze(sys.argv[2], sys.argv[3])
    else:
        sys.exit(1 if check(sys.argv[1], sys.argv[2]) else 0)
