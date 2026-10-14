"""Run the H6 export gate without rewriting the checked-out CI evidence."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pins = json.loads((HERE/'gate/PINS.json').read_text())['files']
    names = set(pins)
    names.update(str(path.relative_to(ROOT)) for path in HERE.rglob('*') if path.is_file()
                 and '__pycache__' not in path.parts)
    before = {name: digest(ROOT/name) for name in names}
    need(all(before[name] == pin['sha256'] for name, pin in pins.items()),
         'CI inherited input binding')
    gitdir = subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'],
                                     cwd=ROOT, text=True).strip()
    with tempfile.TemporaryDirectory(prefix='h6-ci-') as directory:
        export = Path(directory)/'source-tree'
        unrelated = Path(directory)/'unrelated-cwd'
        unrelated.mkdir()
        for name in sorted(names):
            destination = export/name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, destination)
        environment = dict(os.environ, GIT_DIR=gitdir, GIT_WORK_TREE=str(export))
        gate = export/'research/h6-compensation-network/gate/replay.py'
        subprocess.run([sys.executable, '-I', '-O', '-B', str(gate)], cwd=unrelated,
                       env=environment, check=True)
        receipt = json.loads(gate.with_name('RESULT.json').read_text())
        need(receipt['status'] == 'PASS_SUCCESSOR_FRESH_EXPORT_AND_MUTATION_GATES',
             'CI must execute the complete fresh-export gate')
        need(all(digest(ROOT/name) == value for name, value in before.items()),
             'CI replay rewrote checked-out source/evidence')
        print(json.dumps(dict(status='PASS_H6_CI_REPLAY_CHECKOUT_UNCHANGED',
            inherited_files=receipt['inherited_pinned_files'],
            scripts=len(receipt['audit_script_sha256']),
            specifications=len(receipt['specification_sha256']),
            gate_checks=receipt['checks'],
            semantic_corruption_controls=len(receipt['semantic_negative_controls']),
            scope='Scoped successor replay with retained exhaustive predecessor evidence; no all-size or hosted-admission claim.'),
            sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
