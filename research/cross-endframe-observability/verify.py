#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact census of pooled rank-seven/rank-eight terminal observations.

This checker is independent of the PR2979 producer and its verifier. It reads
only the two pinned word JSONs, expands their non-target linear maps backwards
as formal warp-word polynomials over Q, and tests exact nuisance cancellation.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'rank7-joint-endframes' / 'data'
HASHES = {
    'base': 'abaf67bfcb257528658c906b612f57025617592bd7889828f92b97a5f4f4300d',
    'extra': 'e0eaf64c4d5d324693d43889bce1b9e53e8da00402105c8c978fd102f208bed7',
}
TARGET = set(range(112, 224))
EXPECTED_FORM = {
    (224, ()): F(-1, 2), (227, ()): F(1, 2),
    (229, ()): F(-1, 2), (231, ()): F(-1, 2),
    (232, ()): F(-1, 2), (233, ()): F(1, 2),
    (234, ()): F(-1, 2), (235, ()): F(1, 2),
    (236, ()): F(1, 2), (237, ()): F(-1, 2),
    (238, ()): F(1, 2), (239, ()): F(-1, 2),
    (276, ()): F(-1, 2), (292, ()): F(-1, 2),
}
EXPECTED_READOUT = {7: F(-1), 232: F(-1), 236: F(1), 238: F(1)}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def span(basis):
    values = {0}
    for v in basis:
        require(isinstance(v, int) and 0 <= v < 512, 'frame outside GF(2)^9')
        values |= {x ^ v for x in tuple(values)}
    return frozenset(values)


def dimension_union(spaces):
    pivots = {}
    for space in spaces:
        for value in space:
            x = value
            while x:
                pivot = x.bit_length() - 1
                if pivot in pivots:
                    x ^= pivots[pivot]
                else:
                    pivots[pivot] = x
                    break
    return len(pivots)


def load_provider(name):
    raw = (DATA / f'WORD-{name}.json.gz').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == HASHES[name], f'{name} source bytes changed')
    p = json.loads(gzip.decompress(raw))
    require(len(p['ports']) == 112 and len(p['warps']) == 72, f'{name} provider shape')

    live = set(range(704)) - set(p['removed'])
    frames = [span([p['ports'][r]]) if r < 112 else span([]) for r in range(704)]
    for r, basis in p['start_extra'].items():
        frames[int(r)] = span(basis)

    warps_at = defaultdict(list)
    for i, warp in enumerate(p['warps']):
        require(0 <= warp[0] <= len(p['B']), f'{name} warp position')
        warps_at[warp[0]].append(['warp', warp[1], i + 1, warp[3], warp[4]])
    events = list(p['A'])
    for i in range(len(p['B']) + 1):
        events.extend(warps_at.get(i, []))
        if i < len(p['B']):
            events.append(p['B'][i])
    events.extend(p['restore'])

    for g in events:
        kind, dest = g[:2]
        nxt = span(g[4]) if kind == 'warp' else span(g[-1])
        regs = [dest] if kind in ('warp', 'scale') else [dest, g[2]]
        for r in regs:
            require(r in live, f'{name} event touches removed register')
            frames[r] = nxt

    ops = []
    for g in events[p['prelude_events']:]:
        if g[1] in TARGET:
            continue
        require(g[0] != 'add' or g[2] not in TARGET, f'{name} non-target reads target')
        ops.append(g)
    eligible = (set(range(224, 704)) & live) - (
        set(map(int, p['helper_final'])) | set(map(int, p['start_extra']))
        | {c['source'] for c in p['initial_corrections']}
    )
    require(len(ops) == 5207, f'{name} non-target operator count')
    require(len(eligible) == 207, f'{name} eligible-input count')
    active = live - TARGET
    require(len(active) == 520, f'{name} tracked terminal count')

    groups = {7: defaultdict(list), 8: defaultdict(list)}
    for r in sorted(active):
        size = len(frames[r])
        if size == 128:
            groups[7][frames[r]].append(r)
        elif size == 256:
            groups[8][frames[r]].append(r)
    require((len(groups[7]), sum(map(len, groups[7].values()))) == (49, 104),
            f'{name} rank-seven endpoint census')
    require((len(groups[8]), sum(map(len, groups[8].values()))) == (126, 336),
            f'{name} rank-eight endpoint census')
    return raw, ops, eligible, groups


def add(dst, src, q):
    for key, c in list(src.items()):
        value = dst.get(key, F(0)) + q * c
        if value:
            dst[key] = value
        else:
            dst.pop(key, None)


def terminal_rows(ops, terminals):
    """Return exact formal-polynomial rows: terminal registers -> initial state."""
    state = [{} for _ in range(704)]
    for r in terminals:
        state[r][(r, ())] = F(1)
    for g in reversed(ops):
        kind, dest = g[:2]
        if kind == 'add':
            add(state[g[2]], state[dest], F(g[3], g[4]))
        elif kind == 'scale':
            q = F(g[2], g[3])
            state[dest] = {key: q * c for key, c in state[dest].items()}
        else:
            t = g[2]
            state[dest] = {
                (r, word[:-1] if word and word[-1] == -t else word + (t,)): c
                for (r, word), c in state[dest].items()
            }
    rows = {r: {} for r in terminals}
    for initial, poly in enumerate(state):
        for (terminal, word), c in poly.items():
            rows[terminal][(initial, word)] = c
    return rows


def nuisance_kernel(channels, rows, eligible):
    """Basis for readouts whose every protected coefficient polynomial vanishes."""
    basis = {}
    keys = set().union(*(rows[r].keys() for r in channels))
    for key in sorted(keys):
        if key[0] in eligible:
            continue
        v = [rows[r].get(key, F(0)) for r in channels]
        for pivot, row in sorted(basis.items()):
            q = v[pivot]
            if q:
                v = [x - q * y for x, y in zip(v, row)]
        pivot = next((j for j, value in enumerate(v) if value), None)
        if pivot is not None:
            q = v[pivot]
            basis[pivot] = [value / q for value in v]

    free = [j for j in range(len(channels)) if j not in basis]
    kernel = []
    for f in free:
        v = [F(0)] * len(channels)
        v[f] = F(1)
        for pivot in sorted(basis, reverse=True):
            v[pivot] = -sum(basis[pivot][j] * v[j]
                            for j in range(pivot + 1, len(channels)))
        kernel.append(v)
    return kernel


def eligible_forms(channels, kernel, rows, eligible):
    forms = []
    for readout in kernel:
        form = {}
        for r, q in zip(channels, readout):
            if not q:
                continue
            for key, c in rows[r].items():
                if key[0] in eligible:
                    value = form.get(key, F(0)) + q * c
                    if value:
                        form[key] = value
                    else:
                        form.pop(key, None)
        forms.append(form)
    return forms


def sparse_rank(vectors):
    basis = {}
    rank = 0
    for vector in vectors:
        v = dict(vector)
        while v:
            pivot = min(v)
            if pivot not in basis:
                q = v[pivot]
                basis[pivot] = {j: c / q for j, c in v.items()}
                rank += 1
                break
            q = v[pivot]
            for j, c in basis[pivot].items():
                value = v.get(j, F(0)) - q * c
                if value:
                    v[j] = value
                else:
                    v.pop(j, None)
    return rank


def scan_join_rank(groups, rows, eligible, arity):
    spaces = sorted(groups, key=lambda s: tuple(sorted(s)))
    join_count = 0
    positive = []
    for selected in combinations(spaces, arity):
        if dimension_union(selected) != 8:
            continue
        join_count += 1
        channels = [r for space in selected for r in groups[space]]
        kernel = nuisance_kernel(channels, rows, eligible)
        forms = eligible_forms(channels, kernel, rows, eligible)
        rank = sparse_rank(forms)
        if rank:
            positive.append((channels, kernel, forms, rank))
    return join_count, positive


def normalized_witness(channels, kernel, forms):
    witnesses = [(lam, form) for lam, form in zip(kernel, forms) if form]
    require(len(witnesses) == 1, 'candidate must have one nonzero eligible witness')
    lam, form = witnesses[0]
    coefficients = {r: q for r, q in zip(channels, lam) if q}
    require(7 in coefficients, 'candidate witness missing register 7')
    scale = F(-1) / coefficients[7]
    coefficients = {r: q * scale for r, q in coefficients.items()}
    form = {key: q * scale for key, q in form.items()}
    return coefficients, form


def analyze(name):
    raw, ops, eligible, groups = load_provider(name)
    rank7 = groups[7]
    rank8 = groups[8]
    terminals = sorted({r for g in (rank7, rank8) for rs in g.values() for r in rs})
    rows = terminal_rows(ops, terminals)

    single7 = sum(sparse_rank(eligible_forms(rs, nuisance_kernel(rs, rows, eligible), rows, eligible))
                  for rs in rank7.values())
    single8 = sum(sparse_rank(eligible_forms(rs, nuisance_kernel(rs, rows, eligible), rows, eligible))
                  for rs in rank8.values())
    require(single7 == 0, f'{name} individual rank-seven endpoint exposed eligible input')
    require(single8 == 0, f'{name} individual rank-eight endpoint exposed eligible input')

    pair_count, pair_positive = scan_join_rank(rank7, rows, eligible, 2)
    triple_count, triple_positive = scan_join_rank(rank7, rows, eligible, 3)
    require(pair_count == 413, f'{name} rank-eight pair-join count')
    require(triple_count == 2571, f'{name} rank-eight triple-join count')
    require(len(pair_positive) == 1 and len(triple_positive) == 1,
            f'{name} unexpected pair/triple eligible observation')

    pair = pair_positive[0]
    coeffs, form = normalized_witness(pair[0], pair[1], pair[2])
    require(coeffs == EXPECTED_READOUT, f'{name} pair readout identity changed: {coeffs}')
    require(form == EXPECTED_FORM, f'{name} pair input form changed: {form}')
    triple_coeffs, triple_form = normalized_witness(
        triple_positive[0][0], triple_positive[0][1], triple_positive[0][2]
    )
    require(triple_coeffs == EXPECTED_READOUT and triple_form == EXPECTED_FORM,
            f'{name} triple did not reproduce the same four-register witness')

    # Each of the four readouts is necessary; deleting any one kills the signal.
    for removed in EXPECTED_READOUT:
        smaller = [r for r in pair[0] if r != removed]
        kernel = nuisance_kernel(smaller, rows, eligible)
        forms = eligible_forms(smaller, kernel, rows, eligible)
        require(sparse_rank(forms) == 0, f'{name} witness survived deleting register {removed}')

    return {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'individual_rank7_classes': len(rank7),
        'individual_rank8_classes': len(rank8),
        'rank7_pairs_with_rank8_join': pair_count,
        'positive_pair_classes': len(pair_positive),
        'rank7_triples_with_rank8_join': triple_count,
        'positive_triple_classes': len(triple_positive),
        'witness_readout': coeffs,
        'witness_form': form,
    }


def main():
    results = {name: analyze(name) for name in ('base', 'extra')}
    require({k: v for k, v in results['base'].items() if k != 'sha256'}
            == {k: v for k, v in results['extra'].items() if k != 'sha256'},
            'provider orientation results differ')
    r = results['base']
    print('PASS_CROSS_ENDFRAME_OBSERVABILITY')
    print('pinned PR2979 orientation hashes:', results['base']['sha256'], results['extra']['sha256'])
    print('rank-seven endpoint classes: 49; rank-eight endpoint classes: 126')
    print('individual rank-7/rank-8 classes with eligible signal: 0 / 0')
    print('rank-8 joins among rank-7 pairs: 413; positive classes: 1')
    print('rank-8 joins among rank-7 triples: 2571; positive classes: 1 (same witness)')
    print('readout: -out[7] - out[232] + out[236] + out[238]')
    print('input form: 1/2 * (-h224 + h227 - h229 - h231 - h232 + h233 - h234 + h235 + h236 - h237 + h238 - h239 - h276 - h292)')
    print('exact protected-column and formal-warp cancellation; deleting any one readout kills the signal')
    print('scope: information identity only; no consumer, complete invoice or kappa improvement')


if __name__ == '__main__':
    main()
