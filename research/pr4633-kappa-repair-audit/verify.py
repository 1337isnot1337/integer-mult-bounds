#!/usr/bin/env python3
"""Exact endpoint/repair audit of PR4633 b390d64. Apache-2.0.

Prepared by Cinna Davis with substantial OpenAI Codex assistance.
Credits: DaysSky/PR4633, pinterbanget/PR4604, petalas/PR4627,
rohanarun's endpoint audit, and the credited PR589/PR4470 suppliers.
This checks a failed proposal; it does not certify a replacement supplier.
"""
import gzip
import contextlib
import importlib.util
import io
import json
import struct
import sys
import tempfile
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    if str(path).endswith('.gz'):
        with gzip.open(path, 'rt') as handle:
            return json.load(handle)
    return json.loads(path.read_text())


def rank_q(rows):
    rows = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for col in range(len(rows[0]) if rows else 0):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        v = rows[rank][col]
        rows[rank] = [x/v for x in rows[rank]]
        for i in range(rank+1, len(rows)):
            v = rows[i][col]
            rows[i] = [x-v*y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def span(basis):
    out = {0}
    for v in basis:
        out |= {x ^ v for x in out}
    return frozenset(out)


def binary_frame(annihilator):
    rows = [sum((x & 1) << i for i, x in enumerate(row)) for row in annihilator]
    return frozenset(x for x in range(256)
                     if all((r & x).bit_count() % 2 == 0 for r in rows))


def port_contract(start, final, spaces, pairs, ambient, block):
    """Necessary q=1 conditions, independent of logical-value replay."""
    counts, accepted = Counter(), 0
    for p in range(pairs):
        a, b = spaces[start[p]], spaces[final[p]]
        c, d = spaces[start[p+pairs]], spaces[final[p+pairs]]
        dims = tuple(len(s).bit_length()-1 for s in (a, b, c, d))
        counts[dims] += 1
        accepted += (dims == (1, ambient, 0, block)
                     and a & d == {0} and len(span(a | d)) == 2**ambient)
    return {'accepted_ports': accepted, 'rejected_ports': pairs-accepted,
            'endpoint_dimensions': {str(k): n for k, n in sorted(counts.items())}}


def rank_mismatches(records, dims):
    return sum(f != dims[c]-dims[y] for op, x, y, c, f, z in records if op == 0)


def mass(profile):
    return sum(r*n for r, n in profile.items())


def profile(value):
    return Counter({int(k): n for k, n in value.items()})


def invoice(helpers, paid, ports, block):
    """Proposal's 16-stage, 18-call, split-7 scalar invoice."""
    targets = Counter({r: 18*n for r, n in helpers.items()})
    costs = Counter({r: 18*n for r, n in paid.items()})
    costs[1] += 15*ports
    targets[1+18*block] += 2*ports
    for length in (7, 8):
        for j in range(1, length+1):
            targets[1+block*(j+1)] += 2*ports
            costs[block*(j+1)] += 2*ports
    return targets, costs, mass(targets)-mass(costs)


def main():
    bit = ROOT/'research/bit-ambient-quotient'
    source = ROOT/'research/kappa-rebuild/bit/sources/pr589-regenerated'
    w = read(source/'WORD.json.gz')
    frames = {int(k): f for k, f in read(source/'records/frames.json')['frames'].items()}
    a, result = read(bit/'QUOTIENT-BIT-WORD.json.gz'), read(bit/'RESULT.json')
    spec = importlib.util.spec_from_file_location('author_bit', bit/'verify.py')
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    need(w['form'] == '<x,y>/2' and len(frames) == 636, 'Rational E8 source')
    dims = {f: item['dim'] for f, item in frames.items()}
    for f, item in frames.items():
        need(rank_q(item['A'])+dims[f] == 8 and rank_q(item['B']) == dims[f],
             'Exact source rational dimensions')
        need(all(sum(x*y for x, y in zip(a, b)) == 0 for a in item['A'] for b in item['B']),
             'Exact source annihilator/basis agreement')
    normals = []
    for p in range(111):
        entrance, terminal = frames[w['start'][p]], frames[w['final'][p+111]]
        need(tuple(dims[f] for f in (w['start'][p], w['final'][p],
                                     w['start'][p+111], w['final'][p+111])) == (1, 8, 0, 7),
             'Source endpoint dimensions')
        u, n = entrance['B'][0], terminal['A'][0]
        need(sum(x*y for x, y in zip(u, n)) != 0, 'Source rational complement')
        normals.append(n)
    need(rank_q(normals) == 8, 'Source terminal intersection is zero')
    binary = {f: binary_frame(item['A']) for f, item in frames.items()}
    need(all(len(binary[f]) == 2**dims[f] for f in frames), 'Binary dimensions alone pass')
    need(len(set(binary.values())) == 157, '636 rational frames collapse to 157 binary spaces')
    binary_source = port_contract(w['start'], w['final'], binary, 111, 8, 7)
    spaces = {i: span(b) for i, b in enumerate(a['frame_bases'])}
    qdims = {int(k): d for k, d in a['frame_dims'].items()}
    need(all(len(spaces[f]) == 2**d for f, d in qdims.items()), 'Artifact basis dimensions')
    bit_contract = port_contract(a['start'], a['final'], spaces, 111, 8, 7)
    need(bit_contract['accepted_ports'] == 0, 'Every submitted BIT port fails')
    lost = [p for p in range(111) if qdims[a['start'][p]] == 0]
    erased_rank = rank_q([frames[w['start'][p]]['B'][0] for p in lost])
    need(len(lost) == 41 and erased_rank > len(a['kernel_basis']),
         'No rational linear quotient with the declared kernel dimension lifts this map')
    independent_ports, independent_vectors = [], []
    for p in lost:
        vec = frames[w['start'][p]]['B'][0]
        if rank_q(independent_vectors+[vec]) > len(independent_vectors):
            independent_ports.append(p)
            independent_vectors.append(vec)
    need(binary[w['start'][8]] == binary[w['start'][9]], 'Sign-distinct lines identified')
    need(rank_q([frames[w['start'][p]]['B'][0] for p in (8, 9)]) == 2,
         'The identified source lines are rationally independent')
    records = list(struct.iter_unpack('<6i', (source/'records/249-records.bin').read_bytes()))
    need(rank_mismatches(records, dims) == rank_mismatches(a['records'], qdims) == 0,
         'Original MOVE charges match dimensions')
    for reverse in (False, True):
        old, _, _ = v.replay(records, w['start'], w['final'], dims, reverse)
        new, _, _ = v.replay(a['records'], a['start'], a['final'], qdims, reverse)
        need(old == profile(result['emitted_paid']) and new == profile(result['quotient_paid']),
             'Author logical replay positive controls in both directions')
    mutant = deepcopy(a['records'])
    for event in mutant:
        if event[0] == 0:
            event[4] = 0
    mismatches = rank_mismatches(mutant, qdims)
    mutant_paid, _, _ = v.replay(mutant, a['start'], a['final'], qdims, False)
    need(mismatches > 0 and mass(mutant_paid) < mass(new), 'Undercharged MOVE mutation passes author')
    with tempfile.TemporaryDirectory(prefix='pr4633-mutation-') as directory:
        mutated_artifact = deepcopy(a)
        mutated_artifact['records'] = mutant
        path = Path(directory)
        with gzip.open(path/'QUOTIENT-BIT-WORD.json.gz', 'wt') as handle:
            json.dump(mutated_artifact, handle)
        original_here = v.HERE
        try:
            v.HERE = path
            with contextlib.redirect_stdout(io.StringIO()):
                v.main()
        finally:
            v.HERE = original_here
        mutation_result = read(path/'RESULT.json')
    need(mutation_result['status'] == 'PASS_BIT_AMBIENT_QUOTIENT',
         'Full author verifier accepts undercharged MOVE mutation')
    helpers = Counter({8: 439})
    main = sum(qdims[a['final'][r]]-qdims[a['start'][r]] for r in range(222))
    central_old, central_new = mass(old)-mass(helpers)-1554, mass(new)-mass(helpers)-main
    need((1554-main, central_old, central_new) == (260, 63, 36), 'Removed main/COPY work')
    t0, p0, s0 = invoice(helpers, old, 111, 7)
    t1, p1, s1 = invoice(helpers, new, 111, 7)
    need((s0, s1) == (753, 5919) and s1-s0 == 18*(260+27), 'Entire BIT surplus gain accounted for')
    t_small, p_small, small_surplus = invoice(helpers, new, 111, 4)
    small_kappa = v.admissible_kappa(t_small, p_small)
    need(small_kappa is None, 'Block-4 repricing has no passing point in author screen search')

    complex_dir = ROOT/'research/complex-ambient-quotient'
    c = read(ROOT/'research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-CANONICAL.json.gz')
    parent = read(ROOT/'research/fresh-helper-boundary/CHANGES.json')
    need(all(r >= 224 for field in ('entrances', 'exits') for r, old_frame, new_frame in parent[field]),
         'Complex predecessor preserves main boundaries')
    patch = read(ROOT/'research/joint-helper-lattice/PATCH.json')
    need(all(m['ordinal'] >= 224 for m in patch['changes'] if m['phase'] in ('entrance', 'exit')),
         'Joint helper patch preserves main boundaries')
    cspaces = {i: span(b) for i, b in enumerate(c['frames'])}
    source_complex = port_contract(c['start'], c['final'], cspaces, 112, 9, 8)
    need(source_complex['accepted_ports'] == 112, 'All source complex ports pass')
    normals = []
    for p in range(112):
        h = cspaces[c['final'][p+112]]
        normals.append(next(n for n in range(1, 512) if all((n & x).bit_count() % 2 == 0 for x in h)))
    need(len(span(normals)) == 512, 'Complex terminal intersection is zero')
    q = read(complex_dir/'QUOTIENT-WORD.json.gz')
    qspaces = {i: span(b) for i, b in enumerate(q['frames'])}
    complex_contract = port_contract(q['start'], q['final'], qspaces, 112, 9, 8)
    reduced_contract = port_contract(q['start'], q['final'], qspaces, 112, 8, 7)
    need(complex_contract['accepted_ports'] == 0 and reduced_contract['accepted_ports'] == 56,
         'No block-8 port; only half the block-7 ports have q=1')
    cr = read(complex_dir/'RESULT.json')
    ch, cp = profile(cr['helper_widths']), profile(cr['paid_profile'])
    _, _, complex_surplus = invoice(ch, cp, 112, 8)
    t_reduced, p_reduced, reduced_surplus = invoice(ch, cp, 112, 7)
    need((complex_surplus, reduced_surplus) == (3776, -256), 'Complex block repricing')
    need(v.admissible_kappa(t_reduced, p_reduced) is None, 'Block-7 screen search fails')
    output = {
        'status': 'PASS_PR4633_REPAIR_AUDIT',
        'reviewed_head': 'b390d64abfcdba1a3816b86fc763cbc95d43c12c',
        'supported_new_kappa': None,
        'scope': 'Exact counterexamples and necessary endpoint conditions; no replacement supplier.',
        'bit': {'rational_source_ports_accepted': 111, 'binary_source_contract': binary_source,
                'quotient_contract': bit_contract, 'rational_frames': 636,
                'distinct_binary_reductions': 157, 'erased_rational_lines': len(lost),
                'erased_rational_span_rank': erased_rank, 'declared_kernel_dimension': 3,
                'independent_erased_port_witness': independent_ports,
                'terminal_normal_rank_over_Q': 8,
                'source_kappa_screen': v.admissible_kappa(t0, p0),
                'unjustified_quotient_screen': v.admissible_kappa(t1, p1),
                'source_surplus': s0, 'unjustified_quotient_surplus': s1,
                'removed_main_rank': 260, 'removed_COPY_related_rank': 27,
                'block4_surplus': small_surplus, 'block4_screen_search_result': small_kappa,
                'undercharged_MOVE_mutation_accepted_by_author': True,
                'independent_rank_mismatches': mismatches,
                'undercharged_mutation_reported_kappa': mutation_result['quotient_kappa']},
        'complex': {'source_contract': source_complex, 'quotient_block8_contract': complex_contract,
                    'quotient_block7_contract': reduced_contract, 'terminal_normal_rank_over_F2': 9,
                    'unjustified_block8_surplus': complex_surplus, 'block7_surplus': reduced_surplus}}
    (HERE/'RESULT.json').write_text(json.dumps(output, indent=2, sort_keys=True)+'\n')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
