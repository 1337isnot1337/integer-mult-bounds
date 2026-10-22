#!/usr/bin/env python3
"""Replay unchanged PR3563 evidence on its authenticated historical snapshot.

Adapted from Clear1nsight PR14 solely to bind the original manifest to current
canonical ancestry. Apache-2.0; substantial OpenAI assistance.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PUBLICATION = 'f9f85c1e4fa1e955ff39f10fca447e3e2a4e4adc'
PACKAGE = 'research/historical-1042-link'
ORIGINAL = {'verify.py':'12170922e5cd84746089d022f103bfe931fb8a15',
            'test_verify.py':'140840530cbd9b4fdd80d8fa067334b61bfa4c17',
            'RESULT.json':'a9d58d28814fc4a7c9b50a165b48d1a4f52d1892',
            'SOURCES.json':'c6119ca5a8233edd0f8ed3a2e606de5b088d9fcf'}
INPUTS = {'docs/research/current-status.md','certificates/selected-result.json',
          'certificates/checkpoints/frontier1042.json'}

def require(ok, why):
    if not ok:
        raise ValueError(why)

def blob_id(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def checked_path(path):
    p=PurePosixPath(path)
    require(not p.is_absolute() and str(p)==path and '..' not in p.parts
            and '\\' not in path and '\0' not in path, 'Unsafe historical path')
    return path

def git_bytes(spec):
    env=dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
    return subprocess.check_output(['git','--no-replace-objects','cat-file','blob',spec],
                                   cwd=ROOT,env=env,timeout=30)

def main():
    raw=git_bytes(PUBLICATION+':'+PACKAGE+'/SOURCES.json')
    require(blob_id(raw)==ORIGINAL['SOURCES.json'],'Original manifest changed')
    manifest=json.loads(raw)
    rows=[r for r in manifest['files'] if r['usage']=='input']
    require(len(rows)==3 and {r['path'] for r in rows}==INPUTS,'Input inventory changed')
    payload={PACKAGE+'/SOURCES.json':raw}
    for name in ('verify.py','test_verify.py','RESULT.json'):
        path=HERE/name
        require(path.is_file() and not path.is_symlink(),'Missing/aliased frozen file')
        data=path.read_bytes()
        require(blob_id(data)==ORIGINAL[name],'Frozen bytes changed')
        payload[PACKAGE+'/'+name]=data
    for row in rows:
        path=checked_path(row['path'])
        data=git_bytes(manifest['base_commit']+':'+path)
        require(blob_id(data)==row['git_blob'],'Historical blob mismatch')
        require(hashlib.sha256(data).hexdigest()==row['sha256'],'Historical hash mismatch')
        payload[path]=data
        if path.endswith('frontier1042.json'):
            require((ROOT/path).read_bytes()==data,'Live historical checkpoint changed')
    with tempfile.TemporaryDirectory(prefix='historical-1042-replay-') as directory:
        root=Path(directory)
        for relative,data in payload.items():
            p=root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
        for name in ('verify.py','test_verify.py'):
            subprocess.run([sys.executable,*flags,str(root/PACKAGE/name)],cwd=root,check=True,timeout=30)
        require(all((root/p).read_bytes()==data for p,data in payload.items()),'Frozen replay mutated evidence')
    print('PASS_HISTORICAL_1042_SNAPSHOT current_frontier_not_asserted=true')

if __name__=='__main__':
    main()
