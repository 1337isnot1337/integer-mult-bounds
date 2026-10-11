"""Verify the finite theorem package and its pinned PR433 worked example."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from fractions import Fraction as Q

if not __debug__:
    raise RuntimeError('Assertions must remain enabled')
sys.dont_write_bytecode = True
from assembly import BRIDGE, INITIAL, ceilq, construct, greatest_grid_target, jsonable, load_outer
from evidence import moment_pair, supplier_inputs

ROOT = Path(__file__).resolve().parent


def snapshot():
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.json'}


def check_baseline(data):
    # Independently reproduce the published finite parameters and all 47
    # rational margins from the fresh actual supplier prices and charged bill.
    bit, complex_ = data['bit'], data['complex']
    eta = beta = Q(1, 10**18)
    seed = min(bit, (1-beta)*complex_)-Q(1, 10**24)
    value = INITIAL
    cutoffs = []
    for _ in range(6):
        old = value
        value = (1-seed)*seed+seed*old
        gap = min(seed-value, 1-value-seed, 1-value-seed*(1-old), 1-seed)
        length = max(ceilq(36/gap**2), ceilq(2*(4+512)/gap))
        cutoffs.append({'gap': str(gap), 'cutoff_log2': str(length)})
    expected = data['published']
    outer = load_outer().assembly(value, complex_, BRIDGE, data['baseline'], eta=eta, beta=beta)
    assert cutoffs == expected['bootstrap']
    assert jsonable(outer['strict_constraints']) == expected['strict_outer_constraints']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional new result file outside the package')
    args = parser.parse_args()
    if args.output:
        output = args.output.resolve()
        assert not output.exists() and not output.is_relative_to(ROOT)
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())['files']
    assert snapshot() == manifest, 'Package closure mismatch'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_assembly.py'],
                   cwd=ROOT, env=env, check=True)
    data = supplier_inputs()
    check_baseline(data)
    grid = Q(1, 10**27)
    target = greatest_grid_target(data['bit'], data['complex'], grid)
    result = construct(data['bit'], data['complex'], target, coefficient_bits=512)
    assert target > data['baseline']
    assert target < result['supremum'] <= target+grid
    moments = data['moments']
    moments['selected_seed'] = moment_pair(data['profile'], 64, data['live'], result['seed'])
    controls = []
    outer = load_outer()
    for name, k, eta, beta in [
        ('next_grid', target+grid, result['eta'], result['beta']),
        ('zero_eta', target, Q(0), result['beta']),
        ('zero_beta', target, result['eta'], Q(0)),
        ('unit_beta', target, result['eta'], Q(1)),
    ]:
        try:
            outer.assembly(result['bootstrap_chain'][-1], data['complex'], BRIDGE, k, eta=eta, beta=beta)
        except AssertionError:
            controls.append(name)
        else:
            raise AssertionError('Invalid outer parameters admitted: '+name)
    result.update(baseline=data['baseline'], gain=target-data['baseline'], grid=grid,
                  bootstrap_levels=len(result['cutoffs']), moment_intervals=moments,
                  coefficient=str(data['coefficient']), two_level_coefficient=str(data['two_level_coefficient']),
                  supplier_invoice=data['invoice'], rejected_controls=controls,
                  supplier_manifest_sha256=data['source_manifest_sha256'])
    result = jsonable(result)
    for key, value in json.loads((ROOT/'EXPECTED.json').read_text()).items():
        assert result[key] == value, (key, result[key], value)
    assert snapshot() == manifest, 'Package changed during verification'
    result['package_manifest_sha256'] = hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest()
    if args.output:
        with output.open('x') as stream:
            stream.write(json.dumps(result, indent=2)+'\n')
    print('PASS_FINITE_ASSEMBLY_FRONTIER', result['target'], 'nine finite levels; 47 strict constraints')


if __name__ == '__main__':
    main()
