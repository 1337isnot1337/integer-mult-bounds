"""Check the complete package closure and run the finite regression suite."""
from pathlib import Path
import hashlib, json, subprocess, sys

if not __debug__:
    raise RuntimeError('Assertions are required')
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def snapshot():
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.json'}


manifest = json.loads((ROOT/'MANIFEST.json').read_text())['files']
assert snapshot() == manifest, 'Package closure changed'
sources = json.loads((ROOT/'SOURCES.json').read_text())
for name, entry in sources['vendor'].items():
    raw = (ROOT/'vendor'/name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == entry['sha256']
    if 'git_blob' in entry:
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == entry['git_blob']
for name, entry in sources['fixtures'].items():
    assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest() == entry['fixture_sha256']
result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_chart_audit.py'], cwd=ROOT)
assert snapshot() == manifest, 'Package changed during verification'
if result.returncode:
    raise SystemExit(result.returncode)
print('PASS_DIRTY_CHART_AUDIT_PACKAGE', len(manifest), 'source files')
