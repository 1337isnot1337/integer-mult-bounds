#!/usr/bin/env python3
"""Behavioral checks of source binding, fixed evidence and phase sensitivity.

Ross Richardson with OpenAI Codex assistance. Apache-2.0.
"""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def main():
    sources = json.loads((HERE / 'SOURCES.json').read_text())
    with tempfile.TemporaryDirectory(prefix='p104-native-tests-') as temporary:
        root = Path(temporary)
        package = root / HERE.relative_to(ROOT)
        shutil.copytree(HERE, package, ignore=shutil.ignore_patterns('__pycache__'))
        for source in sources['files']:
            if source['usage'] == 'input':
                path = root / source['path']
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / source['path'], path)
        command = [sys.executable, '-I', '-O', '-B', str(package / 'verify.py')]

        def run(extra=()):
            return subprocess.run(command + list(extra), cwd=root, text=True,
                                  capture_output=True, timeout=600)

        for name in ('NATIVE.json.gz', 'RESULT.json', 'inputs/CIRCUIT.json'):
            path = package / name
            original = path.read_bytes()
            path.unlink()
            result = run()
            need(result.returncode != 0 and not path.exists(), 'missing evidence regenerated: '+name)
            path.write_bytes(original)
        print('PASS missing fixed evidence fails without regeneration')

        source_path = root / next(s['path'] for s in sources['files'] if s['usage'] == 'input')
        original = source_path.read_bytes()
        source_path.write_bytes(original + b'\n')
        result = run()
        need(result.returncode != 0 and 'input pin mismatch' in result.stderr, 'source drift accepted')
        source_path.write_bytes(original)
        print('PASS immutable source drift rejects')

        path = package / 'RESULT.json'
        original = path.read_bytes()
        path.write_text('{invalid json')
        need(run().returncode != 0, 'malformed receipt accepted')
        path.write_bytes(original)
        destination = root / 'occupied.json'
        destination.write_text('keep this exact text')
        result = run(['--out', str(destination)])
        need(result.returncode != 0 and destination.read_text() == 'keep this exact text',
             'exclusive output damaged existing data')
        destination.unlink()
        print('PASS malformed receipt and occupied output reject')

        # The exact mathematical payload survives a changed gzip timestamp.
        path = package / 'NATIVE.json.gz'
        raw = gzip.decompress(path.read_bytes())
        path.write_bytes(gzip.compress(raw, mtime=123456789))
        before = snapshot(root)
        for p in root.rglob('*'):
            if p.is_file():
                p.chmod(0o444)
        result = run()
        need(result.returncode == 0, 'Git-free read-only recompressed replay failed: '+result.stderr[-2000:])
        need(snapshot(root) == before, 'read-only replay changed files')
        for p in root.rglob('*'):
            if p.is_file():
                p.chmod(0o644)
        print('PASS Git-free read-only replay and equivalent gzip payload')

    # Deliberately remove only the phase predicate, leaving every signed Pauli
    # comparison intact. A phase fault must become an unexpected acceptance,
    # so the control suite itself must fail. This changes no source file.
    spec = importlib.util.spec_from_file_location('phase_sensitivity_audit', HERE / 'check.py')
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    certificate = json.loads(gzip.decompress((HERE / 'NATIVE.json.gz').read_bytes()))
    circuit = json.loads((HERE / 'inputs/CIRCUIT.json').read_text())
    old_equal = check.N.equal

    def tableau_only(actual, expected, label):
        check.N.require(check.N.tableau(actual) == check.N.tableau(expected),
                        label + ': signed Pauli action')

    check.N.equal = tableau_only
    try:
        try:
            check.run_controls(certificate, circuit)
        except ValueError as error:
            need('phase' in str(error).lower() and
                 ('accept' in str(error).lower() or 'reject' in str(error).lower()),
                 'phase-deletion control failed for unrelated reason: '+str(error))
        else:
            raise ValueError('phase controls stayed green after deleting exact phase predicate')
    finally:
        check.N.equal = old_equal
    print('PASS phase-predicate deletion makes controls fail')
    print('PASS_P104_TWO_TARGET_NATIVE_BEHAVIOR groups=6')


if __name__ == '__main__':
    main()
