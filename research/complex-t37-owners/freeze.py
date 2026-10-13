# SPDX-License-Identifier: Apache-2.0
"""Freeze path (not a verification premise): rerun the PR870 controller chain in
WITNESS_DISCOVER mode on the T37 owners, record every pinned value, and write
data/SPEC.json. verify.py must then pass strictly against the frozen values.

Inputs are an existing verified PR799 replay and a fresh U8 native build
(--native, the `native` directory of a cold verify.py or PR890 replay).
"""
import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from common import HERE, ROOT, read, require, sha, identity, dump

SOURCE = ROOT/'research/complex-k492-owner-repair/vendor/multicold'
T21 = ROOT/'research/complex-t21-owners'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline799', type=Path, required=True)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    require(not work.exists(), 'New work directory required')
    work.mkdir(parents=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONINTMAXSTRDIGITS='0',
               PYTHON=sys.executable, MULTICOLD_SOURCE=str(SOURCE), GAIN_PR564_SOURCE=str(SOURCE))

    def run(script, *arguments):
        subprocess.run([sys.executable, '-B', str(SOURCE/'code/run_portable.py'), str(script), *map(str, arguments)],
                       cwd=ROOT, env=env, check=True)

    base = args.baseline799.resolve()/'global/global/base'
    local = args.native.resolve()/'local'
    run(HERE/'build_owners.py', '--out', work/'owners')
    run(HERE/'build_parent.py', '--base', base, '--owners', work/'owners/OWNERS.json.gz',
        '--order', work/'owners/ORDER.json', '--out', work/'lift')
    run(HERE/'source_adapters.py', work/'runtime')
    plan, roles = read(work/'lift/PLAN.json'), read(work/'owners/OWNERS.json.gz')
    content = identity(roles)
    value = copy.deepcopy(plan)
    value['assignment_sha256'] = value['replica_lift']['owners_file_sha256'] = content
    spec = read(HERE/'data/SPEC.json')
    spec['data'] = dict(plan_sha256=sha(work/'lift/PLAN.json'), owners_sha256=sha(work/'owners/OWNERS.json.gz'),
                        owners_content_sha256=content, plan_semantic_sha256=identity(value))
    spec['pivot_swap']['recipe'] = str((T21/'vendor/pr870/construction/layers_np/PIVOT-SWAP-NP.json').resolve())
    (work/'runtime/data').mkdir()
    dump(work/'runtime/data/SPEC.json', spec)
    env.update(WITNESS_SPEC=str(work/'runtime/data/SPEC.json'), WITNESS_DISCOVER='1',
               WITNESS_RECORD=str(work/'WITNESS-RECORD.jsonl'))
    shutil.copytree(args.baseline799.resolve()/'global/parent558', work/'parent')
    shutil.copyfile(work/'lift/GLOBAL-TEMPLATE.json.gz', work/'parent/complex-global/base/split-centres/GLOBAL-TEMPLATE.json.gz')
    code, g = work/'runtime/code', work/'global'
    run(code/'bind_providers_portable.py', '--baseline', work/'parent', '--provider', 'gauge44='+str(local), '--plan', work/'lift/PLAN.json', '--out', g)
    run(code/'emit_allcold.py', '--base', g/'base', '--owners', work/'owners/OWNERS.json.gz', '--plan', g/'PLAN.json', '--out', g/'hosted')
    run(code/'audit_allcold.py', g/'base', g/'hosted', g/'audit/ASYNC-AUDIT.json', '--mutation-controls')
    run(code/'invoice_allcold.py', '--base', g/'base', '--hosted', g/'hosted', '--audit', g/'audit', '--out', g/'audit',
        '--retained-invoice', SOURCE/'vendor/pr558/vendor/pr552/complex-global/vendor531/evidence/audit/PREFIX-AND-INVOICE.json')
    run(code/'assemble.py', SOURCE, g, work/'ASSEMBLY.json')
    disc = work/'discovery'
    disc.mkdir()
    shutil.copyfile(work/'WITNESS-RECORD.jsonl', disc/'WITNESS-RECORD.jsonl')
    shutil.copyfile(work/'ASSEMBLY.json', disc/'ASSEMBLY.json')
    frozen = work/'SPEC-FROZEN.json'
    seed = copy.deepcopy(spec)
    seed['pivot_swap'] = read(HERE/'data/SPEC.json')['pivot_swap']
    dump(frozen, seed)
    subprocess.run([sys.executable, '-B', str(code/'freeze_spec.py'), '--spec', frozen, '--discovery', disc], check=True)
    result = read(frozen)
    result['data'] = spec['data']
    claim = read(HERE/'data/CLAIM.json')
    assembly = read(work/'ASSEMBLY.json')
    require(assembly['kappa_decimal'] == claim['kappa_decimal'], 'Discovery reproduces the claimed exponent')
    dump(HERE/'data/SPEC.json', result)
    print('FROZEN', assembly['kappa_decimal'])


if __name__ == '__main__':
    main()
