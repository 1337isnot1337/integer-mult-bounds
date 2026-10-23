#!/usr/bin/env python3
"""Discovery-only changed owned-COPY contract, without editing predecessors.

Apache-2.0. Substantial OpenAI Codex assistance. The rank engine and signed-cut
solver are the credited general-gaussian-contact-search predecessor.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = ROOT / 'research/general-gaussian-contact-search'
for row in json.loads((HERE / 'SOURCES.json').read_text())['files']:
    if hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('Changed predecessor source: ' + row['path'])
spec = importlib.util.spec_from_file_location('owned_center_prior_discovery', PRIOR / 'discover.py')
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)
M = D.M
original_build = M.build


def owned_contacts(payload, model):
    """Trace node IDs using the predecessor's explicit chronological rules.

    No original file is rewritten. Each node is checked against its actual
    frame, and complete node counts/baseline invoices are checked separately.
    """
    c = payload['canonical']
    node = 2 + len(c['start'])
    copied = None
    found = []
    for event in payload['programs']['forward']:
        if event[0] == 'scalar':
            gate, frame = event[1:]
            M.need(model['nodes'][node] == frame, 'Actual scalar contact node alignment')
            if gate[0] == 'copy':
                M.need(gate[1] == ['C', 0] and gate[2][0] == 'L', 'Actual owned COPY source')
                copied = node, frame, gate[2][1]
            node += 1
        elif event[0] == 'warp':
            M.need(model['nodes'][node:node + 2] == event[3:5], 'Actual native warp contact alignment')
            node += 2
        elif event[0] == 'center':
            M.need(copied is not None, 'Every center has an actual preceding COPY')
            n, frame, source = copied
            M.need(event[1] == 0 and event[2] == frame and event[3] == 0 and event[4] == 8,
                   'Actual descending rank-eight owned center')
            found.append({'node': n, 'frame': frame, 'source': source, 'old_rank': 8})
            copied = None
    M.need(node + len(c['final']) == len(model['nodes']), 'Full chronological node inventory')
    M.need(len(found) == 8 and len({x['node'] for x in found}) == 8, 'All eight separate COPY/center lifetimes')
    return found


def build(payload, forms):
    model = original_build(payload, forms)
    original_paid, original_helpers = M.invoice(model, [])
    copied = owned_contacts(payload, model)
    frozen = set(model['fixed'])
    model['centers'] = {}
    model['owned_centers'] = copied
    for row in copied:
        node, frame = row['node'], row['frame']
        M.need(node in frozen, 'Original COPY contact is frozen')
        frozen.remove(node)
        # CLEAR can initialize zero at the chosen COPY chart. The actual
        # persistent source uses that same chart. Afterwards C returns to
        # the unchanged zero chart for every scatter ADD and final CLEAR.
        # Its real paid rank is the whole relative Fourier rank, not zero.
        sink = len(model['nodes'])
        model['nodes'].append(0)
        frozen.add(sink)
        old, new = model['old_spaces'][frame], model['new_spaces'][frame]
        old_rank, new_rank = M.dimension(old), M.dimension(new)
        M.need(old_rank == 8 and new_rank in (7, 8), 'Exact changed center width')
        model['edges'].append(('center', node, sink, [old_rank, new_rank, old_rank, new_rank]))
    model['fixed'] = sorted(frozen)
    paid, helpers = M.invoice(model, [])
    M.need(paid == original_paid and helpers == original_helpers, 'Full source bill retained after center release')
    return model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--end', type=int, default=511)
    ap.add_argument('--seconds', type=float, default=5.)
    args = ap.parse_args()
    source = ROOT / 'research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz'
    M.need(hashlib.sha256(source.read_bytes()).hexdigest() ==
           '7679daa4ec6a40f56fc7f0202379a6f454310e94945aba4f48beaaaafb838d05', 'Frozen actual round-three word')
    M.need(1 <= args.start <= args.end <= 511, 'Bounded nonzero functional interval')
    M.build = build
    started = time.monotonic()
    outpath = HERE / f'SEARCH-{args.start}-{args.end}.json'
    results = []
    for functional in range(args.start, args.end + 1):
        result = D.solve(source, [functional], args.seconds, 'none', 'kernel')
        result['owned_center_copy_inputs_released'] = True
        results.append(result)
        record = {'scope': 'BOUNDED_FLOATING_DISCOVERY_ONLY',
                  'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                  'changed_contract': 'Eight actual owned COPY contacts released and every changed center rank paid',
                  'requested_functionals': [args.start, args.end], 'completed': len(results),
                  'seconds': time.monotonic() - started, 'results': results}
        outpath.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
        print(json.dumps({k: result[k] for k in ('functionals', 'status', 'actual_local_energy', 'solver_objective', 'seconds')
                          if k in result}), flush=True)
        if result.get('actual_local_energy', 0.) < -1e-8:
            (HERE / 'CANDIDATE.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
            print('POSITIVE_UNVERIFIED_CANDIDATE_STOP', functional, flush=True)
            break


if __name__ == '__main__':
    main()
