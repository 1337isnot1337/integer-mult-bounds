"""Reconstruct the two-stage-cycle owner map, run the unchanged strict T16 admission,
then the independent seed67 owner audit, exact pricing and PR1069 sweep."""
from pathlib import Path
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

if not __debug__:
    raise RuntimeError('Assertions must remain enabled')
P = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
CONTROLS = dict(admission=69, bit_supplier=12, independent_t16=6, controller_mutations=15)


def run(main, work):
    pins = json.loads((P/'INPUTS.json').read_text())
    for name, h in pins.items():
        assert sha(main/name) == h, 'Changed dependency: '+name
    package_pins = json.loads((P/'MANIFEST.json').read_text())
    actual = {f.relative_to(P).as_posix(): sha(f) for f in P.rglob('*')
              if f.is_file() and f != P/'MANIFEST.json' and '__pycache__' not in f.parts}
    assert actual == package_pins, 'Package inventory mismatch'

    # 1. Byte-exact PLAN/SPEC and content-exact OWNERS from selected PR1094 + DIFF.
    modspec = importlib.util.spec_from_file_location('two_stage_build', P/'build.py')
    mod = importlib.util.module_from_spec(modspec)
    modspec.loader.exec_module(mod)
    blobs = mod.derive(main)
    for name, b in zip(('OWNERS.json.gz', 'PLAN.json', 'SPEC.json'), blobs):
        assert b == (P/'data'/name).read_bytes(), 'Reconstruction mismatch: '+name

    # 2. The PR1407 dependency: every row this package changes relative to PR1407
    #    must land exactly on the committed map (PR1407's bytes are pinned, not shipped).
    rows = json.loads(gzip.decompress((P/'data/OWNERS.json.gz').read_bytes()))
    dep = json.loads((P/'DEPENDENCY-PR1407.json').read_text())
    d1407 = json.loads((P/'DIFF-vs-pr1407.json').read_text())
    assert len(d1407) == dep['changed_rows'] and all(rows[d['index']] == d['after'] for d in d1407)
    parent = [r.copy() for r in rows]
    for d in d1407:
        parent[d['index']] = d['before'].copy()
    # Undoing this package's rows yields exactly PR1407's pinned owner table.
    assert hashlib.sha256(mod.canonical(parent)).hexdigest() == dep['pr1407_owners_content_sha256']

    # 3. Unchanged PR1087 strict verifier on the overlaid data.
    source = work/'source'
    source.mkdir(parents=True)
    archive = main/'research/complex-t16-rare-pattern-exchanges/upstream1087.tar.gz'
    with tarfile.open(archive) as t:
        for m in t.getmembers():
            assert m.isfile() and (source/m.name).resolve().is_relative_to(source.resolve())
        t.extractall(source, filter='data')
    original = json.loads((source/'MANIFEST.json').read_text())
    assert {f.relative_to(source).as_posix(): sha(f) for f in source.rglob('*')
            if f.is_file() and f != source/'MANIFEST.json'} == original
    for name in ('OWNERS.json.gz', 'PLAN.json', 'SPEC.json'):
        shutil.copyfile(P/'data'/name, source/'data'/name)
    local = work/'local'
    local.mkdir()
    local_pins = json.loads((P/'LOCAL-PINS.json').read_text())
    with tarfile.open(main/'research/community-frontier1094-audit/selected-replay.tar.gz') as t:
        prefix = 'candidate/strict/global/base/providers/gauge44/'
        for name, h in local_pins.items():
            member = t.getmember(prefix+name)
            assert member.isfile()
            b = t.extractfile(member).read()
            assert hashlib.sha256(b).hexdigest() == h
            (local/name).write_bytes(b)
    # No discovery, source reconstruction, optimizer, credential environment,
    # or native cold rebuild. The full controller and invoice are regenerated.
    env = {k: os.environ[k] for k in ('PATH', 'SYSTEMROOT', 'WINDIR', 'TMPDIR', 'TEMP', 'TMP') if k in os.environ}
    env.update(PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONINTMAXSTRDIGITS='0')
    subprocess.run([sys.executable, '-E', '-S', '-B', str(source/'verify_t16.py'),
                    '--main', str(main), '--local', str(local), '--work', str(work/'strict')], env=env, check=True)
    result = json.loads((work/'strict/REPLAY.json').read_text())
    target = json.loads((P/'CANDIDATE.json').read_text())
    assert result['status'] == 'PASS_GAUGE44_T16_STRICT_GLOBAL_REPLAY'
    assert result['kappa'] == target['expected_updates']['kappa']
    assert result['conservative_kappa_decimal'] == target['expected_updates']['conservative_kappa_decimal']
    assert result['complex_profile'] == target['expected_updates']['global_profile']
    assert result['idle_remainder_profile'] == target['expected_updates']['idle_remainder_profile']
    assert result['actual_73_axis_charts'] == target['expected_updates']['actual_73column_sigmas'] == 10000
    assert result['controls'] == CONTROLS

    # 4. Independent seed67 owner audit, pinned-engine pricing and PR1069 sweep.
    subprocess.run([sys.executable, '-I', '-B', str(P/'check.py'), '--main', str(main),
                    '--replay', str(work/'strict'), '--out', str(work/'CHECK.json')], env=env, check=True)
    check = json.loads((work/'CHECK.json').read_text())
    assert check['price_new']['kappa_decimal'] == result['kappa_decimal'] == '0.001672684510394236'
    for name, h in pins.items():
        assert sha(main/name) == h
    print('PASS_TWO_STAGE_EJECTION_CYCLES', result['kappa_decimal'], result['idle_remainder_profile'])


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--main', type=Path, default=P.parents[1])
    ap.add_argument('--work', type=Path)
    args = ap.parse_args()
    if args.work:
        args.work.mkdir(parents=True, exist_ok=False)
        run(args.main.resolve(), args.work.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix='two-stage-cycles-') as d:
            run(args.main.resolve(), Path(d))
