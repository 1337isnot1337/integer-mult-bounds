#!/usr/bin/env python3
"""Check actual center Fourier ranks and all incident copy bridges.

This is a small physical calibration, not a full supplier replay.
Apache-2.0. Substantial OpenAI Codex assistance; exact Clifford code is
retained from the credited source, unchanged.
"""
from collections import Counter
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import discover as D


def basis(bits):
    out = []
    space = {0}
    for x in range(512):
        if bits >> x & 1 and x not in space:
            out.append(x)
            space |= {y ^ x for y in tuple(space)}
    D.M.need(sum(1 << x for x in space) == bits, 'Exact independent space basis')
    return out


def run():
    path = D.ROOT / 'research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py'
    spec = importlib.util.spec_from_file_location('owned_center_clifford', path)
    ce = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = ce
    spec.loader.exec_module(ce)
    payload = D.M.load(D.ROOT / 'research/kappa-round3-warp-20261022/ACTUAL-WORD.json.gz')
    model = D.build(payload, [1])
    before, helpers = D.M.invoice(model, [])
    records = []
    for row in model['owned_centers']:
        chosen = {row['node']}
        records_one = []
        for kind, a, b, ranks in model['edges']:
            if a not in chosen and b not in chosen:
                continue
            D.M.need(kind in ('paid', 'center'), 'Calibration contains only actual scalar-adjacent center edges')
            def chart(n):
                frame = model['nodes'][n]
                bb = (basis(model['new_spaces'][frame]) if n in chosen
                      else payload['canonical']['frames'][frame])
                return ce.canonical_frame(9, bb)
            actual = chart(a).adjoint().then(chart(b))
            rec, compiled = ce.lower_child(actual)
            expected = ranks[(a in chosen) + 2 * (b in chosen)]
            D.M.need(rec['rank'] == expected, 'Actual nine-axis B-block rank matches changed edge')
            D.M.need(compiled.tab == actual.tab and compiled.zero_state() == actual.zero_state(),
                     'Both monomial adapters, Gaussian child and absolute phase')
            records_one.append({'kind': kind, 'rank': expected, 'left': rec['left'], 'right': rec['right']})
        after, h2 = D.M.invoice(model, chosen)
        D.M.need(h2 == helpers, 'Single COPY-chart change does not change helper endpoints')
        records.append({'copy_source': row['source'], 'node': row['node'], 'recipes': records_one,
                        'paid_delta': {r: after[r] - before[r] for r in sorted(set(after) | set(before))
                                       if after[r] != before[r]}})
    return {'status': 'PASS_OWNED_CENTER_KERNEL_PHYSICAL_CALIBRATION',
            'scope': 'Eight separate single-COPY chart changes at functional1; not a profitable supplier',
            'cases': records, 'new_kappa': False}


if __name__ == '__main__':
    result = run()
    (HERE / 'CALIBRATION.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'], 'centers', len(result['cases']))
