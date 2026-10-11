"""Offline audit of the pinned hosted-bit contract regression and proposed guard."""
from pathlib import Path
import difflib
import gzip
import hashlib
import json
import types
import unittest
import test_schedule_guard

if not __debug__:
    raise RuntimeError('Assertions must remain enabled')
ROOT = Path(__file__).resolve().parent


def raw(name):
    return (ROOT/name).read_bytes()


def sha(name):
    return hashlib.sha256(raw(name)).hexdigest()


def payload(name):
    data=raw(name)
    return gzip.decompress(data) if name.endswith('.gz') else data


def read(name):
    return json.loads(payload(name))


def snapshot():
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.json'}


def verify():
    manifest=read('MANIFEST.json')['files']
    assert snapshot() == manifest
    source=read('SOURCES.json')
    assert source['commit'] == '4e16d001d505d4f21dd2bcfc44591f9be4c279bd'
    for entry in source['files']:
        data=raw(entry['path'])
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == entry['git_blob']
    completed=read('evidence/COMPLETION.json')
    assert completed['status'] == 'PASS_MINIMAL_ACTUAL442_BIT_FIXTURE'
    assert completed['source_before'] == completed['source_after']
    assert completed['inputs_before'] == completed['inputs_after']
    adapter=read('evidence/adapter/MANIFEST.json')['files']
    assert completed['source_before'] == dict(adapter, **{'MANIFEST.json':sha('evidence/adapter/MANIFEST.json')})
    for name in ['driver.py','audit_stage.py','SOURCE-PINS.json']:
        assert sha('evidence/adapter/'+name) == adapter[name]
    pins=read('evidence/adapter/SOURCE-PINS.json')
    assert pins['head'] == source['commit'] and len(pins['files']) == 17
    for path,entry in pins['files'].items():
        assert entry['sha256'] == adapter['source/'+path]
    assert pins['files']['research/idle-axis-hosting/audit.py']['sha256'] == sha('vendor/audit.py')
    assert pins['files']['research/idle-axis-hosting/EXPECTED.json']['sha256'] == sha('upstream/EXPECTED.json')
    reused=read('evidence/REUSED-COMPLETION.json')
    assert sha('evidence/REUSED-COMPLETION.json') == completed['inputs_before']['completion']
    assert reused['status'] == 'PASS_CHANGED_PR438_BIT_FINITE_CHECK'
    assert reused['source_before'] == reused['source_after'] and reused['inputs_before'] == reused['inputs_after']
    for name,digest in completed['inputs_before'].items():
        if name != 'completion':
            assert digest == reused['output_hashes'][name]
    for name,path in read('evidence/RECEIPT-MAP.json').items():
        data=payload('inputs/'+name) if name in ['frames.json.gz','states.json.gz'] else raw('inputs/'+name)
        assert hashlib.sha256(data).hexdigest() == completed['output_hashes'][path]
    assert [s['name'] for s in completed['steps']] == ['kernel','export','source-spans','parent-global','parent-audit','hosted-bit','audit-contract']
    for stage in completed['steps']:
        assert stage['returncode'] == 0
        assert sha('evidence/logs/'+stage['name']+'.log') == stage['log_sha256'] == completed['output_hashes'][stage['name']+'.log']
    expected=read('EXPECTED.json')
    for name,key in [('parent','parent_template_sha256'),('hosted','hosted_template_sha256')]:
        assert hashlib.sha256(payload('inputs/'+name+'.json.gz')).hexdigest() == expected[key]
    assert expected['parent_template_sha256'] == read('upstream/PARENT-GLOBAL.json')['template_sha256']
    assert expected['hosted_template_sha256'] == read('upstream/EXPECTED.json')['bit_template_sha256']
    assert read('inputs/PARENT-GLOBAL.json')['template_sha256'] == read('inputs/PARENT-AUDIT.json')['template_sha256'] == expected['parent_template_sha256']
    assert len(read('inputs/PARENT-AUDIT.json')['mutations_rejected']) == 8
    assert len(read('inputs/KERNEL.json')['controls']) == 3
    frames=read('inputs/frames.json.gz')['frames'];states=read('inputs/states.json.gz')
    widths=[8-frames[str(states['initial'][str(i)])]['dim'] for i in range(240,987)]
    assert widths == read('inputs/widths.json')
    contract=read('inputs/AUDIT-CONTRACT.json')
    assert contract['parent_template_sha256'] == expected['parent_template_sha256']
    assert contract['hosted_template_sha256'] == expected['hosted_template_sha256']
    assert contract['profile'] == expected['profile'] and contract['hosted_residuals'] == expected['hosted_residuals'] == 39568
    assert [m['wrong_columns'] for m in contract['mutations']] == expected['original_accepted_wrong_columns'] == [8,3]
    assert all(m['original_audit_accepted'] for m in contract['mutations'])
    # Verify and execute the exact proposed two-line integration, leaving vendor bytes untouched.
    original=raw('vendor/audit.py').decode()
    derived=original.replace('import copy, gzip, hashlib, json, sys\n',
        'import copy, gzip, hashlib, json, sys\nfrom schedule_guard import require_hosted_bit_contract\n')
    derived=derived.replace('def audit_bit(t, parent_t, widths):\n',
        'def audit_bit(t, parent_t, widths):\n    require_hosted_bit_contract(t, parent_t)\n')
    patch=''.join(difflib.unified_diff(original.splitlines(True),derived.splitlines(True),
        fromfile='a/research/idle-axis-hosting/audit.py',tofile='b/research/idle-axis-hosting/audit.py'))
    assert patch == raw('hosting-audit.patch').decode()
    patched=types.ModuleType('patched_hosting_audit')
    exec(compile(derived,'<source-bound-hosting-audit-patch>','exec'),patched.__dict__)
    parent,hosted=read('inputs/parent.json.gz'),read('inputs/hosted.json.gz')
    paid,count=patched.audit_bit(hosted,parent,widths)
    assert {str(k):v for k,v in paid.items()} == expected['profile'] and count == expected['hosted_residuals']
    for name in ['exchange','bridge_zero']:
        try:patched.audit_bit(test_schedule_guard.mutate(hosted,name),parent,widths)
        except ValueError:pass
        else:raise AssertionError('Patched audit accepted '+name)
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_schedule_guard)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    assert result.wasSuccessful() and result.testsRun == 4
    assert snapshot() == manifest
    return dict(status='PASS_HOSTED_BIT_PARENT_CONTRACT_REGRESSIONS',
        upstream_commit=source['commit'],hosted_template_sha256=expected['hosted_template_sha256'],
        original_accepted_wrong_columns=[8,3],focused_tests=4,patched_audit='positive accepted; both invalid schedules rejected',
        scope='Authentic PR442 bit fixture; verifier strengthening only, no new numerical or invalid-bound claim.')


if __name__ == '__main__':
    print(json.dumps(verify(),indent=2))
