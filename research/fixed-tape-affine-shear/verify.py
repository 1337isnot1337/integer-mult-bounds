#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only source-bound finite-machine replay and controls."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from loader import authenticate, load_macros, need
from kernel import build_program
import independent as i


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def export(program):
    return json.loads(json.dumps(dict(tapes=program.tapes, entry=program.entry,
                                     instructions=program.instructions)))


def pattern(n, seed):
    return [((j * j + 3 * j + seed) ^ (j >> (seed % 3))) & 1 for j in range(n)]


def cases():
    for q in range(1, 9):
        for c in range(q):
            for h in range(q):
                yield (1, q, 1, 1), c, h, pattern(q*q, c*7+h), False
    for c in range(3):
        for h in range(3):
            for k in range(9):
                yield (1, 3, 1, 1), c, h, [int(j == k) for j in range(9)], True
    for shape in ((2, 5, 2, 2), (2, 6, 3, 2), (3, 7, 2, 2), (2, 9, 2, 3), (1, 17, 1, 1)):
        p, q, g, s = shape
        for c, h in ((0, q-1), (q-1, q-1), ((q+1)//2, 0), (2, 3 % q)):
            yield shape, c, h, pattern(p*q*q*g*s, c+h), True


def source_binding(contents):
    program = json.loads(gzip.decompress(contents['research/bit-row-route-generator/PROGRAM.json.gz']))
    selected = [s for s in program['steps'] if s['op'] == 'ordered_shift'
                and s['addresses'] == [3, 0] and s['coefficient'] == [1, 2]]
    need(bool(selected), 'actual source half leaf at ordered addresses 0 -> 3')
    leaves = [s for s in program['steps'] if s['op'] == 'ordered_shift'
              and s['addresses'][0] > s['addresses'][1]]
    need(set(tuple(s['coefficient']) for s in leaves) == {(1, 1), (-1, 1), (1, 2), (-1, 2)},
         'exact admitted later-target coefficient inventory')
    half = [s for s in leaves if s['coefficient'][1] == 2]
    for q in (3, 5, 7, 11):
        for e in range(1, 9):
            Q = q**e
            need((2*((Q+1)//2)) % Q == 1 and (2*((Q-1)//2)) % Q == Q-1,
                 'source half descriptor identity')
    return dict(actual_half_0_to_3=len(selected), serialized_later_target_leaves=len(leaves),
                serialized_half_leaves=len(half), source_f=program['f'], source_q=program['q'],
                source_w=program['w'], descriptor_preparation='charged separate binary half/increment scan',
                whole_route_admitted=False)


def physical(modules, mode, saved):
    programs = {str(inv): build_program(modules, inv) for inv in (False, True)}
    counts = {k: len(p.instructions) for k, p in programs.items()}
    need(saved == {k: export(p) for k, p in programs.items()}, 'literal exported tables match assembler')
    total = 0
    volume = 0
    max_steps = max_span = 0
    digest = hashlib.sha256()
    for case_number, (shape, c, h, payload, translated) in enumerate(cases()):
        for inverse in (False, True):
            bank = i.fixtures(shape, c, h, payload, translated)
            key = str(inverse)
            if mode == 'primary':
                m = modules['machine']
                run = m.Machine(programs[key], [m.Tape(cells, head) for cells, head in bank]).run(1024*len(payload)+1)
                # Adapt only the observation interface, not the execution.
                class View:
                    def __init__(self, tape, visits):
                        self.head = tape.head
                        self.cells = tape.cells
                        self.low = min(visits or {tape.head})
                        self.high = max(visits or {tape.head})
                    def snapshot(self):
                        return dict(self.cells)
                tapes = [View(t, v) for t, v in zip(run.tapes, run.visits)]
                steps = run.steps
            else:
                tapes, steps = i.execute(saved[key], bank, 1024*len(payload)+1)
            span = i.check_result(tapes, steps, bank, shape, c, h, payload, inverse)
            total += 1
            volume += len(payload)
            max_steps = max(max_steps, steps)
            max_span = max(max_span, span)
            digest.update(canonical([shape, c, h, inverse, steps, span, i.oracle(shape, c, h, payload, inverse)]))
    return dict(cases=total, payload_bits=volume, instructions=counts, tapes=19, alphabet_symbols=7,
                transitions_bound_per_bit=1024, visited_cells_bound_per_bit=64,
                maximum_fixture_steps=max_steps, maximum_fixture_span=max_span,
                transcript_sha256=digest.hexdigest())


def expect_reject(fn, text):
    try:
        fn()
    except (ValueError, RuntimeError):
        return
    raise ValueError('control accepted: ' + text)


def controls(modules, saved, contents):
    base = saved['False']
    shape, c, h = (2, 5, 2, 2), 3, 2
    payload = [int(j == 0) for j in range(200)]
    checks = []
    for field, value in ((4, 0), (5, 0), (6, 0), (7, 0), (14, 6), (16, 6)):
        bank = i.fixtures(shape, c, h, payload)
        bank[field] = i.binary(value, 0)
        expect_reject(lambda: i.execute(base, bank, 100000), 'bad extent/coefficient')
        checks.append('input_' + str(field))
    bank = i.fixtures(shape, c, h, payload)
    bank[14] = i.marked([i.ONE, i.ZERO], 0)
    expect_reject(lambda: i.execute(base, bank, 100000), 'noncanonical coefficient')
    checks.append('noncanonical')
    bank = i.fixtures(shape, c, h, payload)
    bank[2] = ({0:i.ONE}, 0)
    expect_reject(lambda: i.execute(base, bank, 100000), 'occupied scratch')
    checks.append('occupied_scratch')
    bad = json.loads(json.dumps(base))
    pos = next(k for k, r in enumerate(bad['instructions']) if r == ['move', 0, 1])
    bad['instructions'][pos][2] = 2
    expect_reject(lambda: i.validate(bad), 'nonlocal move')
    checks.append('nonlocal_move')
    bank = i.fixtures(shape, c, h, payload)
    tapes, steps = i.execute(saved['True'], bank, 100000)
    expect_reject(lambda: i.check_result(tapes, steps, bank, shape, c, h, payload), 'wrong orientation')
    checks.append('wrong_orientation')
    for t, symbol in ((2, i.ONE), (17, i.LEFT)):
        tapes, steps = i.execute(base, bank, 100000)
        tapes[t].write(symbol)
        expect_reject(lambda: i.check_result(tapes, steps, bank, shape, c, h, payload), 'retained scratch')
        checks.append('retained_scratch_' + str(t))
    path = next(iter(contents))
    expect_reject(lambda: authenticate({path: contents[path] + b'\n'}), 'source mutation')
    checks.append('source_hash')
    # Endpoint-preserving unbilled work must change the physical observation.
    bad = json.loads(json.dumps(base))
    halt = next(k for k, r in enumerate(bad['instructions']) if r[0] == 'halt')
    bad['instructions'][halt] = ['goto', len(bad['instructions'])]
    bad['instructions'].extend([['move', 1, 1], ['move', 1, -1], ['halt']])
    good_tapes, good_steps = i.execute(base, bank, 100000)
    bad_tapes, bad_steps = i.execute(bad, bank, 100000)
    need(all(t.snapshot() == u.snapshot() and t.head == u.head for t,u in zip(good_tapes,bad_tapes)),
         'cost-only mutation preserves endpoint')
    need(bad_steps == good_steps + 3, 'cost-only mutation observation includes jump and moves')
    checks.append('unbilled_extra_steps')
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--mode', choices=('primary', 'independent', 'controls'), default='independent')
    args = parser.parse_args()
    contents = authenticate()
    modules = load_macros(contents)
    tables = {str(inv): export(build_program(modules, inv)) for inv in (False, True)}
    table_path = HERE / 'TABLE.json.gz'
    if args.write:
        table_path.write_bytes(gzip.compress(canonical(tables), mtime=0))
    saved = json.loads(gzip.decompress(table_path.read_bytes()))
    need(saved == tables, 'complete table export')
    result = dict(schema_version=1, binding=source_binding(contents),
                  physical=physical(modules, 'independent' if args.mode == 'controls' else args.mode, saved),
                  controls=controls(modules, saved, contents))
    receipt = HERE / 'RESULT.json'
    if args.write:
        receipt.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    need(canonical(result) == canonical(json.loads(receipt.read_text())), 'typed exact receipt comparison')
    print('PASS_FIXED_TAPE_AFFINE_SHEAR', args.mode, json.dumps(result['physical'], sort_keys=True))


if __name__ == '__main__':
    main()
