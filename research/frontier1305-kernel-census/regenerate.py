#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Rebuild every evidence file into a new directory and compare it byte-for-byte with evidence/.

Stages: census.py (standard library) for both #1297/#1305 final words with both restoration rules and for the #1297
input word (positive control); price.py, deletion.py and retime.py with the #1186 exact frame harness; optionally
idle_optimum.py on a completed #1305 verify run.  Cost weights use IMB_B = 0.001679979627113687, the certified complex
lower endpoint of #1305's profile (kappa itself is never taken from these weights).

usage: python3 -B regenerate.py --toolkit <PR #1186 checkout>/research/exact-frame-toolkit --out NEW_DIR [--workers 12]
       [--idle-run <#1305 verify work dir> --idle-owners <#1305 package>/OWNERS.json.gz]
"""
import argparse, filecmp, os, subprocess, sys, time
from pathlib import Path
PKG = Path(__file__).resolve().parent
IMB_B = '0.001679979627113687'
WORDS = dict(base=PKG / 'inputs/BASE-WORD.json.gz', extra=PKG / 'inputs/EXTRA-WORD.json.gz', control=PKG / 'inputs/CONTROL-WORD.json.gz')
ap = argparse.ArgumentParser(); ap.add_argument('--toolkit', type=Path, required=True); ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--workers', type=int, default=12); ap.add_argument('--idle-run', type=Path); ap.add_argument('--idle-owners', type=Path)
a = ap.parse_args(); out = a.out.resolve(); assert not out.exists(), 'output directory must be new'; out.mkdir(parents=True)
env = dict(os.environ, IMB_B=IMB_B, IMB_ROOT=str(PKG.parents[1]), PYTHONDONTWRITEBYTECODE='1')   # the toolkit reads vendored PR551 gk modules from this checkout
env.pop('PYTHONOPTIMIZE', None)
def run(*args):
    t0 = time.time(); log = out / 'regenerate.log'
    with log.open('a') as f:
        f.write('$ ' + ' '.join(map(str, args)) + '\n'); f.flush()
        rc = subprocess.run([sys.executable, '-B', *map(str, args)], env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    assert rc == 0, (args, log.read_text()[-3000:]); print('PASS', Path(args[0]).name, Path(str(args[-1])).name if not str(args[-1]).startswith('-') else '', f'{time.time()-t0:.0f}s', flush=True)
W = str(a.workers); T = a.toolkit.resolve()
for w in ('base', 'extra'):
    for rule in ('tail', 'first'):
        run(PKG / 'census.py', WORDS[w], out / f'CENSUS-{w}-{rule}.json', '--workers', W, '--restore', rule)
        run(PKG / 'price.py', T, WORDS[w], out / f'CENSUS-{w}-{rule}.json', out / f'PRICES-{w}-{rule}.json', '--workers', W)
    run(PKG / 'deletion.py', T, WORDS[w], out / f'DELETION-{w}.json', '--workers', W)
    run(PKG / 'retime.py', T, WORDS[w], out / f'DELETION-{w}.json', out / f'RETIME-{w}.json', '--workers', W)
run(PKG / 'census.py', WORDS['control'], out / 'CENSUS-control-tail.json', '--workers', W, '--pivots', '555', '567')
run(PKG / 'price.py', T, WORDS['control'], out / 'CENSUS-control-tail.json', out / 'PRICES-control-tail.json', '--workers', W)
run(PKG / 'deletion.py', T, WORDS['control'], out / 'DELETION-control.json', '--workers', W, '--pivots', '555', '567')
if a.idle_run:
    run(PKG / 'idle_optimum.py', a.idle_run.resolve() / 'strict/global', a.idle_owners.resolve(), out / 'IDLE-OPTIMUM-1305.json')
names = sorted(p.name for p in out.glob('*.json'))
same = [n for n in names if (PKG / 'evidence' / n).exists() and filecmp.cmp(out / n, PKG / 'evidence' / n, shallow=False)]
print('identical to evidence/:', len(same), 'of', len(names)); [print('  DIFFERS or new:', n) for n in names if n not in same]
