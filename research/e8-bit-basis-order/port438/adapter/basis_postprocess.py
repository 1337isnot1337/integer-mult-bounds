"""Reorder a compatible full-frame source basis after upstream transformations.

George Lydakis with OpenAI Codex assistance. Apache-2.0.
This preserves the copied forms; downstream supplier validation is still required.
"""
import copy
import json
from pathlib import Path


def reorder_basis(word):
    if not __debug__:
        raise RuntimeError('Assertions must remain enabled')
    v, count = word['v'], word['source_basis_gates']
    full = word['final'][0]
    if not isinstance(count, int) or count <= 0 or count > min(len(word['A']), len(word['B'])):
        raise ValueError('A nonempty, explicitly delimited source basis is required')
    basis = word['A'][-count:]
    if word['B'][:count] != list(reversed(basis)):
        raise ValueError('The original basis block must have its literal inverse')
    rows = [1 << i for i in range(v)]
    for frame, destination, sources in basis:
        if frame != full or not 0 <= destination < v or len(sources) != 1 or not 0 <= sources[0] < v or sources[0] == destination:
            raise ValueError('The basis block must consist of full-frame source XORs')
        rows[destination] ^= rows[sources[0]]
    if not word['ret'] or len(set(word['ret'])) != len(word['ret']) or any(not 0 <= r < v for r in word['ret']):
        raise ValueError('Retained forms must occupy distinct original source rows')
    forms = [rows[r] for r in word['ret']]
    echelon = {}
    for row in forms:
        for pivot, other in sorted(echelon.items(), reverse=True):
            if row >> pivot & 1:
                row ^= other
        assert row, 'Copied forms must be independent'
        echelon[row.bit_length()-1] = row
    pivots = sorted(echelon, reverse=True)
    matrix = [1 << i for i in range(v)]
    for pivot, row in zip(pivots, forms):
        matrix[pivot] = row
    target = matrix[:]
    elimination = []
    def add(destination, source):
        matrix[destination] ^= matrix[source]
        elimination.append([full, destination, [source]])
    for pivot in range(v):
        found = next(i for i in range(pivot, v) if matrix[i] >> pivot & 1)
        if found != pivot:
            add(pivot, found); add(found, pivot); add(pivot, found)
        for row in range(v):
            if row != pivot and matrix[row] >> pivot & 1:
                add(row, pivot)
    assert matrix == [1 << i for i in range(v)]
    forward = list(reversed(elimination))
    check = [1 << i for i in range(v)]
    for _, destination, sources in forward:
        check[destination] ^= check[sources[0]]
    assert check == target and [check[r] for r in pivots] == forms
    old_touched = {r for _, d, sources in basis for r in [d]+sources}
    new_touched = {r for _, d, sources in forward for r in [d]+sources}
    if old_touched != new_touched:
        raise ValueError('Reordering must preserve the source rows entering the full frame')
    current = word['start'][:]
    for frame, destination, sources in word['D']+word['A'][:-count]:
        for row in [destination]+sources:
            current[row] = frame
    for row in new_touched:
        current[row] = full
    if any(current[row] != full for row in pivots):
        raise ValueError('Every copied form must be at the full frame')
    result = copy.deepcopy(word)
    result['A'] = result['A'][:-count]+forward
    result['B'] = elimination+result['B'][count:]
    result['ret'] = pivots
    result['source_basis_gates'] = len(forward)
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path, help='A new candidate file; the input is preserved')
    args = parser.parse_args()
    result = reorder_basis(json.loads(args.input.read_bytes()))
    with args.output.open('x') as stream:
        stream.write(json.dumps(result, sort_keys=True, separators=(',', ':')))
