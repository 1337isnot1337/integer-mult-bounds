"""Audit normalized dirty endpoints without collapsing distinct entrance charts.

Ordinary scalar identity and a correct paid histogram do not imply independent
helper endpoints. See PROOF.md for the precise interface and limitations.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, gzip, hashlib, json, sys

if not __debug__:
    raise RuntimeError('Assertions are required')
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'vendor'))
import clifford_exact as X
import emit419 as EM


def read(path):
    raw = Path(path).read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def programs419(candidate):
    assert candidate['v'] == 120 and candidate['h'] == 9
    EM.setR(candidate['R'])
    whitening = EM.prewhite(candidate, {301,387})
    return {ori:list(EM.emit(candidate, ori, {}, {301,387}, whitening))
            for ori in ('forward','backward')}

def replay(c, events, orientation, charts):
    n = 2*c['v']+c['R']
    ext = dict(c['ext'])
    reg = {('L', i): {(i, -1): Q(1)} for i in range(n)}
    phases = []
    for e in events:
        if e[0] == 'phase': phases.append(e[1])
        if list(e) == ['phase', 'ad0'] and charts:
            for i, f in ext.items():
                assert all(tag == -1 for j, tag in reg['L', i])
                reg['L', i] = {(j, f): a for (j, tag), a in reg['L', i].items()}
        if e[0] != 'scalar': continue
        op = e[2]
        target = tuple(op[1])
        if op[0] == 'clear': reg[target] = {}; continue
        source = tuple(op[2])
        if op[0] == 'copy': reg[target] = dict(reg.get(source, {})); continue
        assert op[0] == 'add'
        q = Q(op[3], op[4]) if len(op) == 5 else Q(op[3])
        dest = reg.setdefault(target, {})
        for k, value in dict(reg.get(source, {})).items():
            a = dest.get(k, Q(0))+q*value
            if a: dest[k] = a
            else: dest.pop(k, None)
    assert phases == ['old_response','ad0','A','centers','B','final','adF','cleanup','done'], 'Unexpected phase order'
    expected = {('L', i): {(i, ext[i] if charts and i in ext else -1): Q(1)} for i in range(n)}
    for t in range(c['v']):
        if orientation == 'forward': expected['L', c['v']+t][t, -1] = Q(1)
        else: expected['L', t][c['v']+t, -1] = Q(-1)
    delta = {}
    for i in range(n):
        row = dict(reg['L', i])
        for k, value in expected['L', i].items(): row[k] = row.get(k, Q(0))-value
        row = {k:a for k,a in row.items() if a}
        if row: delta[i] = row
    assert all(not row for key, row in reg.items() if key[0] != 'L')
    return delta


def gaussian_witness(c, delta):
    # Do not infer an error merely from treating frame operators as independent.
    # Instantiate actual pinned Gaussian matrices on a concrete basis vector.
    for output, row in sorted(delta.items()):
        for source in sorted({j for j, frame in row}, key=lambda j: (j == output, j)):
            terms = {frame:a for (j,frame),a in row.items() if j == source}
            value = [[Q(0), Q(0)] for _ in range(1<<c['h'])]
            for frame, factor in terms.items():
                op = X.ident(c['h']) if frame == -1 else X.canonical_frame(c['h'], c['frames'][frame]).adjoint()
                vector, denominator = op.zero_state(0)
                for i,(a,b) in enumerate(vector):
                    value[i][0] += factor*Q(a, 1<<denominator)
                    value[i][1] += factor*Q(b, 1<<denominator)
            bad = [(i,a,b) for i,(a,b) in enumerate(value) if a or b]
            if bad:
                return dict(output_register=output, dirty_source=source, input_address=0,
                    coefficient_operator=[dict(frame=frame, basis=[] if frame == -1 else c['frames'][frame], coefficient=str(a)) for frame,a in sorted(terms.items())],
                    nonzero_output_coordinates=len(bad), first_nonzero=dict(address=bad[0][0], real=str(bad[0][1]), imaginary=str(bad[0][2])),
                    expected_difference='0', off_diagonal=source != output,
                    interpretation='Exact endpoint mismatch before the final invertible output chart. An off-diagonal response cannot be removed by independent invertible changes on each helper.')
    return None  # Basis-zero search is sufficient to certify a witness, not to exclude one.


def audit(candidate, programs):
    assert set(programs) == {'forward','backward'}
    orientations = {}
    for orientation, events in programs.items():
        ordinary = replay(candidate, events, orientation, charts=False)
        delta = replay(candidate, events, orientation, charts=True)
        witness = gaussian_witness(candidate, delta) if delta else None
        status = ('FAIL_ORDINARY_SCALARS' if ordinary else
                  'PASS_FORMAL_ENDPOINT' if not delta else
                  'FAIL_EXACT_GAUSSIAN_ENDPOINT' if witness else
                  'UNRESOLVED_FORMAL_MISMATCH')
        orientations[orientation] = dict(status=status,
            ordinary_scalar_bad_registers=len(ordinary),
            chart_sensitive_bad_registers=len(delta),
            chart_sensitive_bad_targets=sum(candidate['v'] <= i < 2*candidate['v'] for i in delta),
            exact_witness=witness)
    passed = all(x['status'] == 'PASS_FORMAL_ENDPOINT' for x in orientations.values())
    return dict(status='PASS_REQUIRED_ENDPOINT' if passed else 'ENDPOINT_NOT_ESTABLISHED',
                orientations=orientations,
                scope='Required independent-helper endpoint only. This does not certify the full supplier, '
                      'exclude a coupled-bank construction, or invalidate an unconditional theorem. '
                      'A formal mismatch without an actual Gaussian witness is unresolved, not a disproof.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--programs', type=Path, help='JSON or gzip containing local_programs')
    source.add_argument('--emitter419', action='store_true', help='Generate the unchanged PR419 bracket')
    parser.add_argument('--output', type=Path, required=True, help='New JSON result path')
    args = parser.parse_args()
    candidate = read(args.candidate)
    programs = read(args.programs)['local_programs'] if args.programs else programs419(candidate)
    result = audit(candidate, programs)
    result['candidate_sha256'] = hashlib.sha256(args.candidate.read_bytes()).hexdigest()
    if args.programs:
        result['programs_sha256'] = hashlib.sha256(args.programs.read_bytes()).hexdigest()
    with args.output.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(result['status'])
    return 0 if result['status'] == 'PASS_REQUIRED_ENDPOINT' else 1


if __name__ == '__main__':
    sys.exit(main())
