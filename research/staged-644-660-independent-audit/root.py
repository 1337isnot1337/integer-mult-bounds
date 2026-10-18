#!/usr/bin/env python3
"""Exact moment-root brackets for the published PR3605 and PR3148 complete paid histograms.

M(b) = sum_r r*H[r]*(73/r)^b / (73*663040); the complex root solves M(b)=1
(PR3605 DERIVATION.md).  Primary engine: outward-rounded exact rational interval
arithmetic (atanh/Taylor series with explicit remainders).  Second engine:
decimal floating point at 70 digits with Newton iteration and an explicit error
budget.  Standard library only.  This re-evaluates published histograms; it does
not certify the owner journals that produce them.

Sagar Thakrar (thakrarsagar), with substantial AI assistance from Claude
(Anthropic, Claude Opus 5.5). Apache-2.0.
"""
from collections import Counter
import decimal
import gzip
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
M_DIM, STOCK, CALLS = 73, 896 * 740, 6660
BITS = 320                                   # outward rounding grid 2^-320


class RootFailure(Exception):
    pass


def need(ok, *why):
    if not ok:
        raise RootFailure(' '.join(map(str, why)))


def down(x):
    return Q(math.floor(x * (1 << BITS)), 1 << BITS)


def up(x):
    return Q(-math.floor(-x * (1 << BITS)), 1 << BITS)


def atanh(y):
    """Interval for atanh(y), 0<y<1/2: partial sum plus geometric remainder bound."""
    total, term, k, y2 = Q(0), y, 0, y * y
    while term > Q(1, 1 << (BITS + 8)):
        total += term / (2 * k + 1)
        term *= y2
        k += 1
    return down(total), up(total + term / (2 * k + 1) / (1 - y2))


def scale(c, iv):
    return (down(c * iv[0]), up(c * iv[1])) if c >= 0 else (down(c * iv[1]), up(c * iv[0]))


def plus(a, b):
    return down(a[0] + b[0]), up(a[1] + b[1])


LN2 = scale(2, atanh(Q(1, 3)))
LN3 = plus(LN2, scale(2, atanh(Q(1, 5))))           # ln 3 = ln 2 + ln(3/2)
LN5 = plus(scale(2, LN2), scale(2, atanh(Q(1, 9))))  # ln 5 = 2 ln 2 + ln(5/4)
LN73 = plus(scale(6, LN2), scale(2, atanh(Q(9, 137))))  # ln 73 = 6 ln 2 + ln(73/64)


def ln_ratio(r):
    """Interval for ln(73/r), r a positive integer below 73 built from 2, 3, 5."""
    exps, rest = [], r
    for p in (2, 3, 5):
        e = 0
        while rest % p == 0:
            rest //= p
            e += 1
        exps.append(e)
    need(rest == 1 and 0 < r < M_DIM, 'rank outside the stdlib log table', r)
    lo = LN73[0] - sum(e * iv[1] for e, iv in zip(exps, (LN2, LN3, LN5)))
    hi = LN73[1] - sum(e * iv[0] for e, iv in zip(exps, (LN2, LN3, LN5)))
    return down(lo), up(hi)


def exp_interval(t_lo, t_hi):
    """exp on [t_lo,t_hi] with 0<=t_lo<=t_hi<1: positive Taylor terms, explicit tail."""
    need(0 <= t_lo <= t_hi < 1, 'exp argument range')

    def partial(t):
        total, term, k = Q(0), Q(1), 0
        while term > Q(1, 1 << (BITS + 8)):
            total += term
            k += 1
            term = term * t / k
        return total, term, k
    lo, _, _ = partial(t_lo)
    hi, term, k = partial(t_hi)
    return down(lo), up(hi + term / (1 - t_hi / (k + 1)))


LOGS = {}


def moment(hist, b):
    """Interval enclosure of M(b) for a rational b>0."""
    lo = hi = Q(0)
    for r, count in hist.items():
        if r not in LOGS:
            LOGS[r] = ln_ratio(r)
        e = exp_interval(down(b * LOGS[r][0]), up(b * LOGS[r][1]))
        lo += r * count * e[0]
        hi += r * count * e[1]
    return down(lo / (M_DIM * STOCK)), up(hi / (M_DIM * STOCK))


def bracket(hist, digits):
    """Adjacent decimal endpoints C<D=C+10^-digits with upper M(C)<1<lower M(D), by interval bisection."""
    unit = Q(1, 10 ** digits)
    a, b = Q(1, 1000), Q(3, 1000)
    need(moment(hist, a)[1] < 1 < moment(hist, b)[0], 'initial bracket')
    a, b = a / unit, b / unit                     # integers
    while b - a > 1:
        mid = (a + b) // 2
        lo, hi = moment(hist, mid * unit)
        if hi < 1:
            a = mid
        elif lo > 1:
            b = mid
        else:
            raise RootFailure('interval too wide to decide at %s' % (mid * unit))
    return a * unit, b * unit


def decimal_root(hist):
    """Second engine: Newton in 70-digit decimal arithmetic; returns the root and a safe error radius."""
    D = decimal.Decimal
    with decimal.localcontext(decimal.Context(prec=70, rounding=decimal.ROUND_HALF_EVEN)):
        logs = {r: (D(M_DIM) / D(r)).ln() for r in hist}
        weights = {r: D(r * c) for r, c in hist.items()}
        denom = D(M_DIM * STOCK)
        b = D('0.00173')
        for _ in range(60):
            f = sum(weights[r] * (b * logs[r]).exp() for r in hist) / denom - 1
            df = sum(weights[r] * logs[r] * (b * logs[r]).exp() for r in hist) / denom
            step = f / df
            b -= step
            if abs(step) < D('1e-62'):
                break
        need(abs(step) < D('1e-62') and df > 1, 'decimal Newton did not settle')
    # Each of the ~40 operations per evaluation is correctly rounded at 70 digits;
    # |f| error < 1e-66 and df > 1, so 1e-55 is a deliberately loose radius.
    return b, D('1e-55')


def load_hist(obj):
    return {int(k): int(v) for k, v in obj.items()}


def aggregate_idle(cert, inventory, local):
    """Recount PR3605's idle histogram from its published aggregate integer witness.

    Groups are [capacity, lo, hi, bins]; x rows are (group, width pattern, count);
    z rows are (group, macro-call, width, roles).  Checks record types and ranges,
    duplicate records, bin counts, capacities, the open/closed windows as published,
    width supply = role flow, the per-call demand S*inventory for all 333 macro-calls,
    the per-copy group capacity, and the witness's own inventory and profile fields
    (the same legality checks as PR3605 owners/verify_aggregate.py, reimplemented).
    The windows themselves are taken as published, not derived from the source template.
    """
    widths, S, groups = cert['widths'], cert['S'], cert['groups']
    need(widths == [4, 5, 6, 7, 8, 9] and S == 20 and len(cert['order']) == 333, 'aggregate shape')
    need({int(w): n for w, n in cert['inventory'].items()} == inventory, 'witness inventory field')
    idle, bins, supply, flow, demand, per_copy = (Counter() for _ in range(6))
    seen_x, seen_z = set(), set()
    for g, pattern, n in cert['x']:
        need(type(g) is int and 0 <= g < len(groups) and len(pattern) == 6 and type(n) is int and n > 0
             and all(type(k) is int and k >= 0 for k in pattern), 'pattern record', g)
        need((g, tuple(pattern)) not in seen_x, 'duplicate pattern record', g)
        seen_x.add((g, tuple(pattern)))
        used = sum(w * k for w, k in zip(widths, pattern))
        need(used <= groups[g][0] and sum(pattern) <= S, 'pattern', g)
        bins[g] += n
        if used < groups[g][0]:
            idle[groups[g][0] - used] += n
        for w, k in zip(widths, pattern):
            supply[g, w] += n * k
    need(all(bins[g] == S * groups[g][3] for g in range(len(groups))), 'bin inventory')
    for g, t, w, n in cert['z']:
        need(all(type(k) is int for k in (g, t, w, n)) and 0 <= g < len(groups) and 0 <= t < 333
             and w in widths and n > 0, 'role-flow record', g, t)
        need((g, t, w) not in seen_z, 'duplicate role-flow record', g, t, w)
        seen_z.add((g, t, w))
        need(groups[g][1] < t <= groups[g][2], 'source window', g, t)
        flow[g, w] += n
        demand[t, w] += n
        per_copy[g, t] += n
    need(flow == +supply, 'pattern supply differs from role flow')
    need(all(demand[t, w] == S * inventory[w] for t in range(333) for w in widths), 'per-call width demand')
    need(all(n <= S * groups[g][3] for (g, t), n in per_copy.items()), 'per-copy group capacity')
    profile = Counter({r: 333 * S * n for r, n in local.items()}) + idle
    need({int(r): n for r, n in cert['profile'].items()} == profile, 'witness profile field')
    return idle, sum(S * g[3] for g in groups), sum(S * g[3] * g[0] for g in groups)


def relabel(hist, k):
    """k rank-48 idle children relabelled as 48k rank-1 children (k<0: the reverse); rank mass unchanged."""
    out = dict(hist)
    out[48] -= k
    out[1] += 48 * k
    need(min(out.values()) >= 0, 'relabel exceeds the histogram')
    return out


def min_relabels(hist, lo_point, hi_point):
    """Least k>0 proved to put the root below [lo_point, hi_point]: lower M_k(lo_point) > 1 while
    upper M_(k-1)(hi_point) < 1.  M is linear in the histogram; the float guess is only a start.
    """
    base, one = moment(hist, lo_point)[0], moment(relabel(hist, 1), lo_point)[0]
    k = max(1, math.ceil((1 - base) / (one - base)))
    while moment(relabel(hist, k), lo_point)[0] <= 1:
        k += 1
    while k > 1 and moment(relabel(hist, k - 1), lo_point)[0] > 1:
        k -= 1
    need(k == 1 or moment(relabel(hist, k - 1), hi_point)[1] < 1, 'relabel threshold undecided', k)
    return k


def main():
    pr3605 = json.loads((HERE / 'inputs' / 'PR3605-CLAIM.json').read_text(encoding='utf-8'))
    pr3148_path = ROOT / 'research/coupled-carrier-cap740/CLAIM.json'
    pr3148 = json.loads(pr3148_path.read_text(encoding='utf-8'))
    sources = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    pins = {row.get('local', row.get('path')): row['sha256'] for row in sources['files'] + sources['snapshot']}
    need(hashlib.sha256((HERE / 'inputs' / 'PR3605-CLAIM.json').read_bytes()).hexdigest() == pins['inputs/PR3605-CLAIM.json'], 'PR3605 claim pin')
    need(hashlib.sha256(pr3148_path.read_bytes()).hexdigest() == pins['research/coupled-carrier-cap740/CLAIM.json'], 'PR3148 claim pin')

    new, old = load_hist(pr3605['profile']), load_hist(pr3148['profile'])
    local_new, local_old = Counter({1: 2439, 2: 726, 3: 224, 4: 102, 5: 20, 8: 8}), Counter(load_hist(pr3148['local_profile']))
    idle_new = Counter({1: 174156, 3: 48334, 4: 1, 5: 10792, 6: 3, 48: 283185})   # PR3605 DERIVATION.md
    idle_old = Counter({1: 173160, 3: 48951, 5: 13875, 48: 282569})               # PR3148 README
    times = lambda c: Counter({r: CALLS * x for r, x in c.items()})
    need(times(local_new) + idle_new == Counter(new), 'PR3605 H = 6660 L + I')
    need(times(local_old) + idle_old == Counter(old), 'PR3148 H = 6660 L + I')
    mass = lambda h: sum(r * c for r, c in h.items())
    need(mass(new) == mass(old) == 65088 * 740, 'rank mass invariant')
    cert_path = HERE / 'inputs' / 'AGGREGATE-INTEGER-FLOW.json.gz'
    need(hashlib.sha256(cert_path.read_bytes()).hexdigest() == pins['inputs/AGGREGATE-INTEGER-FLOW.json.gz'], 'aggregate pin')
    audited_widths = {4: 26, 5: 2, 6: 18, 7: 52, 8: 97, 9: 213}   # derived from frames by verify.py
    idle_count, bin_count, capacity = aggregate_idle(json.loads(gzip.decompress(cert_path.read_bytes())), audited_widths, local_new)
    need(idle_count == idle_new, 'aggregate witness idle histogram differs from DERIVATION.md', dict(idle_count))
    need(capacity == mass(idle_new) + CALLS * sum(w * c for w, c in audited_widths.items()), 'capacity balance')
    cert = json.loads(gzip.decompress(cert_path.read_bytes()))
    window_cut = [row[:] for row in cert['z']]
    j = next(j for j, row in enumerate(window_cut) if cert['groups'][row[0]][1] >= 0)
    window_cut[j][1] = cert['groups'][window_cut[j][0]][1]           # role on the excluded lower endpoint
    for label, bad_cert, widths in (('parent widths 7:50/8:99', cert, {**audited_widths, 7: 50, 8: 99}),
                                    ('one pattern record deleted', {**cert, 'x': cert['x'][1:]}, audited_widths),
                                    ('one pattern record duplicated', {**cert, 'x': cert['x'] + cert['x'][:1]}, audited_widths),
                                    ('one role-flow record deleted', {**cert, 'z': cert['z'][1:]}, audited_widths),
                                    ('role on an excluded lower window endpoint', {**cert, 'z': window_cut}, audited_widths)):
        try:
            aggregate_idle(bad_cert, widths, local_new)
        except RootFailure:
            continue
        raise RootFailure('aggregate control accepted: ' + label)

    out = {'status': 'PASS_EXACT_MOMENT_BRACKETS', 'model': 'M(b)=sum_r r*H[r]*(73/r)^b/(73*663040)',
           'rank_mass': mass(new), 'stock_times_dimension': M_DIM * STOCK, 'histograms': {},
           'aggregate_witness_recount': {'idle': {str(k): v for k, v in sorted(idle_count.items())},
                                         'bins': bin_count, 'capacity_rank_units': capacity,
                                         'scope': 'arithmetic of the published integer witness with the audited '
                                                  'widths; windows as published; no literal journal or chronology'}}
    published = {'PR3605': (new, [Q(x) for x in pr3605['root_interval']], 24),
                 'PR3148': (old, [Q(x) for x in pr3148['root']], 25)}
    roots = {}
    for name, (hist, (c, d), digits) in published.items():
        lo_c, hi_c = moment(hist, c)
        lo_d, hi_d = moment(hist, d)
        need(hi_c < 1 < lo_d, 'published bracket fails', name)
        own = bracket(hist, 30)
        dec, radius = decimal_root(hist)
        need(Q(dec) - Q(radius) > own[0] and Q(dec) + Q(radius) < own[1], 'decimal engine disagrees', name)
        need(c <= own[0] and own[1] <= d, 'own 30-digit bracket outside the published one', name)
        roots[name] = own
        out['histograms'][name] = {
            'histogram': {str(k): v for k, v in sorted(hist.items())},
            'published_bracket': [str(c), str(d)], 'published_digits': digits,
            'M_upper_at_C_minus_1': float(hi_c - 1), 'M_lower_at_D_minus_1': float(lo_d - 1),
            'bracket_30_digits': [str(own[0]), str(own[1])],
            'decimal_engine_root_70_digits': str(dec)}
    # Counterfactual arithmetic attribution: swap one component at a time.  The hybrid
    # histograms are not realized owner journals and do not conserve rank mass.
    hybrids = {'PR3148 idle + PR3605 local': times(local_new) + idle_old,
               'PR3148 local + PR3605 idle': times(local_old) + idle_new}
    attribution = {}
    for name, hist in hybrids.items():
        a, b = bracket(dict(hist), 30)
        attribution[name] = {'bracket_30_digits': [str(a), str(b)], 'rank_mass': mass(hist),
                             'shift_from_PR3148_lower': float(a - roots['PR3148'][0])}
    out['attribution'] = attribution
    out['root_delta_PR3605_minus_PR3148'] = [str(roots['PR3605'][0] - roots['PR3148'][1]),
                                             str(roots['PR3605'][1] - roots['PR3148'][0])]
    # Mass-changing sensitivity: one idle child added or removed (rank mass changes by r).
    # At fixed window classes, bin counts and widths the capacity balance fixes mass(I), so
    # these perturbations model group-geometry or width errors, not placement errors.
    sensitivity = {}
    for r in (1, 48):
        for sign in (1, -1):
            hist = dict(new)
            hist[r] += sign
            a, b = bracket(hist, 30)
            sensitivity['%+d rank-%d child (rank mass %+d)' % (sign, r, sign * r)] = {
                'bracket_30_digits': [str(a), str(b)],
                'shift_from_PR3605_lower': float(a - roots['PR3605'][0])}
    out['mass_changing_sensitivity_PR3605'] = sensitivity
    # Mass-conserving sensitivity.  Idle ranks are capacities minus pattern widths, so lie in
    # [1, 48] (capacities 8/16/32/48).  For a change moving m units of idle mass, linearity of M
    # and 1 <= (73/r)^b / (73/48)^b <= 73^b / (73/48)^b give |dM(b)| <= m*(73^b-(73/48)^b)/(73*663040)
    # at every b>0, with equality for relabel(.., m/48).  Since M increases in b, every such
    # change leaves the root between those of relabel(.., +k) and relabel(.., -k) when m <= 48k.
    capacities = sorted({g[0] for g in cert['groups']})
    need(capacities == [8, 16, 32, 48] and max(idle_new) == 48, 'idle ranks within [1,48]')
    conserving = {}
    for k in (1, -1):
        a, b = bracket(relabel(new, k), 30)
        conserving['%+d relabel (rank-48 idle child <-> 48 rank-1 children)' % k] = {
            'bracket_30_digits': [str(a), str(b)], 'shift_from_PR3605_lower': float(a - roots['PR3605'][0])}
    move8 = dict(new)                                         # one width-8 role: full bin -> empty 48-bin
    move8[8] += 1
    move8[48] -= 1
    move8[40] = 1
    need(mass(move8) == mass(new), 'width-8 move conserves mass')
    a, b = bracket(move8, 30)
    conserving['one width-8 role moved from a full bin to an empty capacity-48 bin'] = {
        'bracket_30_digits': [str(a), str(b)], 'shift_from_PR3605_lower': float(a - roots['PR3605'][0])}
    k_gain = min_relabels(new, *roots['PR3148'])
    k_threshold = min_relabels(new, Q(173, 100000), Q(173, 100000))
    conserving['least relabels putting the PR3605 root below the PR3148 root'] = k_gain
    conserving['least relabels putting the PR3605 root below 0.00173'] = k_threshold
    out['mass_conserving_sensitivity_PR3605'] = conserving
    out['local_delta_per_call'] = {str(r): local_new[r] - local_old[r] for r in sorted(set(local_new) | set(local_old)) if local_new[r] != local_old[r]}
    out['idle_delta'] = {str(r): idle_new[r] - idle_old[r] for r in sorted(set(idle_new) | set(idle_old)) if idle_new[r] != idle_old[r]}
    encoded = json.dumps(out, indent=1, sort_keys=True) + '\n'
    if '--write' in sys.argv:
        (HERE / 'ROOT-RESULT.json').write_text(encoded, encoding='utf-8', newline='\n')
    else:
        need((HERE / 'ROOT-RESULT.json').read_text(encoding='utf-8') == encoded, 'ROOT-RESULT.json receipt differs')
    print(out['status'])


if __name__ == '__main__':
    main()
