"""Authenticate and open the actual PR3935 physical tensor/router cohort."""
from contextlib import contextmanager
from hashlib import sha1, sha256
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import urllib.request
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_active = None


def authenticate():
    for row in json.loads((HERE/'SOURCES.json').read_text())['files']:
        if row['usage'] == 'input' and sha256((ROOT/row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('source changed: '+row['path'])


def activate():
    authenticate()
    if _active is None:
        raise ValueError('authenticated CRT tensor cohort required')
    return _active


def source_manifest():
    manifest = json.loads((HERE/'NETWORK-SOURCES.json').read_text())
    if manifest['repository'] != 'CrocSwap/integer-mult-bounds' or manifest['head'] != '240597ed313fc2854c0462b23c89dc3bae72aaf5':
        raise ValueError('fixed CRT tensor source identity')
    expected = {'tensor_sources.py', 'tensor_router.py', 'tensor_fixture.py', 'tensor_plan.py',
                'inputs/chirp-export.tar.gz', 'inputs/expansion-export.tar.gz', 'inputs/headroom-source.tar', 'PROOF.md'}
    paths = {row['path'] for row in manifest['files']}
    if paths != {'research/physical-gaussian-tensor/'+name for name in expected} or len(paths) != len(manifest['files']):
        raise ValueError('exact CRT tensor dependency inventory')
    return manifest


def check_tree(root, manifest):
    root = Path(root)
    for row in manifest['files']:
        path = root/row['path']
        if not path.is_file() or path.is_symlink() or path.stat().st_size != row['size']:
            raise ValueError('complete frozen tensor source: '+row['path'])
        body = path.read_bytes()
        blob = sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        if sha256(body).hexdigest() != row['sha256'] or blob != row['git_blob']:
            raise ValueError('frozen tensor source changed: '+row['path'])


def fetch_tree(root, manifest):
    for row in manifest['files']:
        path = Path(root)/row['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        url = 'https://raw.githubusercontent.com/'+manifest['repository']+'/'+manifest['head']+'/'+row['path']
        request = urllib.request.Request(url, headers={'User-Agent': 'integer-mult-crt-source-replay'})
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read(row['size']+1)
        if len(body) != row['size'] or sha256(body).hexdigest() != row['sha256']:
            raise ValueError('downloaded tensor source differs: '+row['path'])
        path.write_bytes(body)
    check_tree(root, manifest)


@contextmanager
def opened(source_root=None, fetch=False):
    global _active
    authenticate()
    if _active is not None or 'tensor_sources' in sys.modules or 'cardinal_counts' in sys.modules:
        raise ValueError('cold CRT tensor namespace')
    if source_root is not None and fetch:
        raise ValueError('choose an offline source root or a fresh fetched tree')
    manifest = source_manifest()
    temporary = None
    if source_root is None:
        if not fetch:
            raise ValueError('supply --source-root or explicitly permit --fetch')
        temporary = tempfile.TemporaryDirectory(prefix='crt-tensor-dependency-')
        source_root = Path(temporary.name)
    source_root = Path(source_root)
    old_path = sys.path[:]
    module = None
    try:
        if fetch:
            fetch_tree(source_root, manifest)
        check_tree(source_root, manifest)
        package = source_root/'research/physical-gaussian-tensor'
        spec = importlib.util.spec_from_file_location('tensor_sources', package/'tensor_sources.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules['tensor_sources'] = module
        spec.loader.exec_module(module)
        with module.opened() as state:
            _active = state
            sys.path.insert(0, str(package))
            try:
                yield state
            finally:
                _active = None
    finally:
        sys.path[:] = old_path
        if sys.modules.get('tensor_sources') is module:
            del sys.modules['tensor_sources']
        if temporary is not None:
            temporary.cleanup()
