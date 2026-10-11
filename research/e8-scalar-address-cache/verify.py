"""Verify the source-bound stage-local address cache without repeating timing."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import unittest
import contract
import test_contract

ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Assertions must remain enabled')


def read(name):return json.loads((ROOT/name).read_bytes())
def sha(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
def snapshot():
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json'}


def verify(run_benchmark=False):
    manifest=read('MANIFEST.json')['files'];assert snapshot()==manifest
    sources=read('SOURCES.json');cfg=read('evidence/adapter/INPUTS.json')
    assert sources['commit']==cfg['source_commit']=='43e5aa3a2fb6701b1facf542f7f3dee0fbb33c3e'
    assert sources['emitter_git_blob']==cfg['git_blob']=='e033a8ceecc58a048477c4053331b8fc39680add'
    for directory in ['candidate','adapter']:
        for name,pin in read(f'evidence/{directory}/MANIFEST.json').items():
            assert sha(f'evidence/{directory}/{name}')==pin
    assert sha('ADDRESS-MAP.patch')==sha('evidence/candidate/ADDRESS-MAP.patch')
    upstream=read('evidence/UPSTREAM-SOURCES.json');assert upstream['commit']==sources['commit']
    for entry in upstream['files']:
        target='evidence/candidate/original_emit.py' if entry['path']=='evidence/adapter/original_emit.py' else entry['path']
        data=(ROOT/target).read_bytes()
        assert hashlib.sha256(data).hexdigest()==entry['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['git_blob']
    assert read('evidence/UPSTREAM-MANIFEST.json')['code/emit.py']==sha('evidence/candidate/original_emit.py')
    bindings=sources['external_input_bindings'];pins={}
    for entry in cfg['files']:
        assert sha(bindings[entry['path']])==entry['sha256'];pins[entry['path']]=entry['sha256']
    pins['adapter_manifest']=sha('evidence/adapter/MANIFEST.json')
    for f in cfg['fixtures']:
        completed=read(bindings[f['completion']])
        assert completed['status']==f['status']
        assert completed['source_before']==completed['source_after']
        assert completed['inputs_before']==completed['inputs_after']
        assert all(s['returncode']==0 for s in completed['steps'])
        assert completed['output_hashes'][f['output_key']]==sha(bindings[f['path']])
    result=read('evidence/RESULT.json');terminal=read('evidence/TERMINAL.json');launch=read('evidence/LAUNCH.json')
    assert result['status']=='PASS_EXACT_SCALAR_REPLAY_ADDRESS_MAP_CONTRACT'
    assert result['inputs_before']==result['inputs_after']==pins
    assert terminal['returncode']==0 and terminal['command']==launch['command']
    assert terminal['launch_sha256']==sha('evidence/LAUNCH.json')
    assert terminal['log_sha256']==sha('evidence/CONTRACT.log')==sha('evidence/RESULT.json')
    assert terminal['outputs']=={'RESULT.json':sha('evidence/RESULT.json')}
    assert launch['adapter_manifest_sha256']==pins['adapter_manifest'] and launch['assertions_enabled']
    assert result['machine']=='arm64' and result['ru_maxrss_unit']=='bytes'
    assert result['ru_maxrss']==terminal['child_ru_maxrss_bytes']
    contract.validate_source_scope()
    fixtures=contract.load_fixtures();actual=contract.check_records(fixtures);speedups=[]
    for current,recorded,fixture in zip(actual,result['fixtures'],cfg['fixtures'],strict=True):
        assert current=={k:v for k,v in recorded.items() if k not in ['fixture','timings']}
        assert recorded['fixture']==fixture['path']
        samples=recorded['timings']
        assert [s['order'] for s in samples]==[['original','candidate'],['candidate','original'],['original','candidate']]
        old=[s['seconds']['original'] for s in samples];new=[s['seconds']['candidate'] for s in samples]
        assert all(t>0 for t in old+new) and max(new)<min(old)
        speedups.append(statistics.median(old)/statistics.median(new))
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_contract)
    tests=unittest.TextTestRunner(verbosity=1).run(suite)
    assert tests.wasSuccessful() and tests.testsRun==2
    report=dict(status='PASS_EXACT_SCALAR_ADDRESS_CACHE',fixtures=len(actual),
        columns_each=[f['columns'] for f in actual],stages_each=11,bridge_controls_each=24,
        operand_comparisons=sum(f['contract']['operands'] for f in actual),
        complete_replay_digests=[f['complete_replay_sha256'] for f in actual],focused_tests=2,
        recorded_setup_inclusive_scalar_replay_speedups=speedups,
        scope='Exact pinned scalar-replay section on retained local words; no fresh PR447 admission, numerical bound or full-emitter speedup claim.')
    if run_benchmark:report['new_scalar_replay_benchmark']=contract.benchmark(fixtures)
    assert snapshot()==manifest
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark',action='store_true',help='Also time the source-extracted scalar replay with table setup included')
    parser.add_argument('--output',type=Path,help='Write to a new report file outside this package')
    args=parser.parse_args()
    if args.output and (args.output.exists() or args.output.resolve().is_relative_to(ROOT)):
        parser.error('Output must be a new file outside the package')
    report=json.dumps(verify(args.benchmark),indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:stream.write(report)
    print(report,end='')
