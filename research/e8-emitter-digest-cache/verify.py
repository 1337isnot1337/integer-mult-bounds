"""Source bindings, complete byte contract and focused encoder regressions."""
from pathlib import Path
import argparse
import hashlib
import json
import statistics
import unittest
import contract
import test_digest_encoder

ROOT=Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('Assertions must remain enabled')


def read(name):return json.loads((ROOT/name).read_bytes())
def sha(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
def snapshot():
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json'}


def verify(run_benchmark=False):
    manifest=read('MANIFEST.json')['files']
    assert snapshot()==manifest
    source=read('SOURCES.json')
    assert source['commit']=='43e5aa3a2fb6701b1facf542f7f3dee0fbb33c3e'
    for entry in source['files']:
        data=(ROOT/entry['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==entry['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['git_blob']
    assert read('evidence/UPSTREAM-MANIFEST.json')['code/emit.py']==sha('evidence/adapter/original_emit.py')
    adapter=read('evidence/adapter/MANIFEST.json')
    for name,pin in adapter.items():assert sha('evidence/adapter/'+name)==pin
    assert sha('digest_encoder.py')==adapter['digest_encoder.py']
    assert sha('EMITTER.patch')==adapter['EMITTER.patch']
    terminal=read('evidence/TERMINAL.json')
    result=read('evidence/RESULT.json')
    launch=read('evidence/LAUNCH.json')
    assert terminal['status']=='PASS_TERMINAL_EVIDENCE'
    assert terminal['result_sha256']==sha('evidence/RESULT.json')
    assert terminal['launch_sha256']==sha('evidence/LAUNCH.json')
    assert terminal['log_sha256']==launch['log_sha256']==sha('evidence/CONTRACT.log')
    assert launch['returncode']==0 and launch['system']=='Darwin' and launch['machine']=='arm64'
    assert terminal['manifest_sha256']==result['manifest_sha256']==sha('evidence/adapter/MANIFEST.json')
    assert terminal['sources_and_fixtures_unchanged'] and result['source_and_fixtures_unchanged']
    pins=read('evidence/adapter/INPUTS.json')
    assert pins['latest_head']==source['commit']
    for fixture,original in zip(source['fixtures'],pins['fixtures'],strict=True):
        assert sha(fixture['path'])==fixture['sha256']==original['sha256']
        completed=read(fixture['completion'])
        assert completed['source_before']==completed['source_after']
        assert completed['inputs_before']==completed['inputs_after']
        assert all(s['returncode']==0 for s in completed['steps'])
        assert completed['output_hashes'][fixture['original_output_path']]==fixture['sha256']
    contract.validate_source_scope()
    fixtures=contract.load_fixtures()
    actual=contract.check_records(fixtures)
    assert actual==result['fixtures']
    assert sum(x['count'] for x in actual)==result['records_byte_compared']==2742552
    assert sum(x['calls'] for x in actual)==144
    assert result['opcodes']==[0,1,2,3] and result['schema_controls']==4
    timing=result['timings_including_compile_and_owner_cache']
    assert len(timing['original'])==len(timing['cached'])==3
    assert all(x>0 for values in timing.values() for x in values)
    assert statistics.median(timing['original'])/statistics.median(timing['cached'])==result['median_speedup']
    assert result['benchmark_order']==[['original','cached'],['cached','original'],['original','cached']]
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_digest_encoder)
    tests=unittest.TextTestRunner(verbosity=1).run(suite)
    assert tests.wasSuccessful() and tests.testsRun==2
    report=dict(status='PASS_BYTE_IDENTICAL_EMITTER_DIGEST_CACHE',records=2742552,calls=144,
                fixture_digests=[x['digest'] for x in actual],focused_tests=2,
                source_checks='All original emitter AST outside import/cache setup/hash-loop unchanged',
                recorded_setup_inclusive_hash_loop_speedup=result['median_speedup'],
                scope='Pinned PR447 loop contract on completed PR438/PR442 workloads; no full supplier replay or end-to-end speedup claim.')
    if run_benchmark:report['new_hash_loop_benchmark']=contract.benchmark(fixtures)
    assert snapshot()==manifest
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark',action='store_true',help='Also time the extracted loops with cache setup included')
    parser.add_argument('--output',type=Path,help='Write the report to a new file outside the package')
    args=parser.parse_args()
    if args.output and (args.output.exists() or args.output.resolve().is_relative_to(ROOT)):
        parser.error('Output must be a new file outside the package')
    report=json.dumps(verify(args.benchmark),indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:stream.write(report)
    print(report,end='')
