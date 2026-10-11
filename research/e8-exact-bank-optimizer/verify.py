"""Check package closure and run the independent finite oracle."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def snapshot():
    if any(p.is_symlink() for p in ROOT.rglob('*')):
        raise ValueError('Symlinks are not part of this package')
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json'}


def main():
    before=snapshot()
    if before!=json.loads((ROOT/'MANIFEST.json').read_text())['files']:
        raise ValueError('Package source closure changed')
    result=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_bank_optimizer.py'],cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)
    if snapshot()!=before:
        raise ValueError('Package files changed during verification')
    print('PASS_EXACT_BANK_OPTIMIZER_SOURCE_CLOSURE_AND_INDEPENDENT_ORACLE')


if __name__=='__main__':main()
