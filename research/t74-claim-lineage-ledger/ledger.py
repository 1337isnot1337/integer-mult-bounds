#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Pinned κ ledger of the T74 handoff line, with every stated pairwise comparison re-checked (standard library only).

For each PR in PINS.json the script reads the claimed κ from the PR's own pinned claim file: outer/OUTER-CLAIM.json
or CLAIM.json, at the exact head, checked by git blob id and sha256. It then:
  1. lists the line in κ order, with the exact difference to every earlier entry;
  2. re-checks every stated comparison "exceeds PR#### by X", transcribed verbatim in COMPARISONS.json, against
     the pinned values. A statement is CONSISTENT when X matches the true difference to its printed precision
     (relative 1e-5), and a MISMATCH otherwise;
  3. checks the one README sentence of PR2435 that quotes PR2374's κ.
The expected set of mismatches is asserted, so the script doubles as a regression check of this ledger.

Scope: this is consolidation of stated numbers. No κ is re-derived, and no construction is checked here (see the
independent checks listed in README.md).
Prepared with substantial AI assistance (Claude Code, Anthropic); Apache-2.0.
Usage: python3 -I -B ledger.py [--repo PATH] [--fetch] [--remote URL] [--out]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from decimal import Decimal, getcontext

if not __debug__:
    sys.stdout.write('FAIL_T74_CLAIM_LEDGER refusing to run under python -O\n')
    sys.exit(2)
getcontext().prec = 120
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_DEFAULT = os.path.dirname(os.path.dirname(HERE))
REMOTE_DEFAULT = 'https://github.com/CrocSwap/integer-mult-bounds'
EXPECTED_MISMATCHES = {(2302, 2269), (2374, 2312), (2435, 2312)}
README_2435 = ('research/gmx-t74-borrow43-handoff/README.md',
               'exceeds PR2374 (our previous package, kappa 0.0016985113436976293')


class Fail(Exception):
    pass


def need(cond, what):
    if not cond:
        raise Fail(what)


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=REPO_DEFAULT)
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--remote', default=REMOTE_DEFAULT)
    ap.add_argument('--out', action='store_true')
    args = ap.parse_args()
    pins = json.load(open(os.path.join(HERE, 'PINS.json')))
    comps = json.load(open(os.path.join(HERE, 'COMPARISONS.json')))
    kappa = {}
    for n, p in pins.items():
        if git(args.repo, 'cat-file', '-e', p['head'] + '^{commit}').returncode and args.fetch:
            subprocess.run(['git', '-C', args.repo, 'fetch', '-q', args.remote, 'refs/pull/%s/head' % n], check=True)
        r = git(args.repo, 'show', p['head'] + ':' + p['path'])
        need(r.returncode == 0, 'PR%s head %s absent (rerun with --fetch)' % (n, p['head'][:8]))
        data = r.stdout
        need(hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() == p['git_blob'] and
             hashlib.sha256(data).hexdigest() == p['sha256'], 'pin PR%s %s' % (n, p['path']))
        k = json.loads(data)[p['key']]
        need(isinstance(k, str) and k.startswith('0.00'), 'PR%s kappa field' % n)
        kappa[int(n)] = Decimal(k)
    order = sorted(kappa, key=lambda n: kappa[n])
    print('T74 handoff line, pinned claim files, in kappa order:')
    prev = None
    for n in order:
        print('  PR%d  kappa %s  %s' % (n, str(kappa[n])[:24],
                                         '' if prev is None else '(+%.6e over PR%d)' % (kappa[n] - kappa[prev], prev)))
        prev = n
    rows, mismatches = [], set()
    for c in comps:
        s, t = c['source'], c['target']
        need(s in kappa and t in kappa, 'comparison PR%d -> PR%d not pinned' % (s, t))
        actual = kappa[s] - kappa[t]
        stated = Decimal(c['stated'])
        ok = abs(stated - actual) <= abs(actual) * Decimal('1e-5')
        if not ok:
            mismatches.add((s, t))
        # which pinned PR does the stated number actually match?
        explains = [m for m in kappa if m != s and abs(kappa[s] - kappa[m] - stated) <= abs(stated) * Decimal('1e-5')]
        rows.append(dict(source=s, target=t, stated=c['stated'], actual='%.6E' % actual,
                         status='CONSISTENT' if ok else 'MISMATCH', stated_value_matches=['PR%d' % m for m in explains],
                         quote=c['quote']))
        print('  PR%d vs PR%d: stated %s, pinned %.6E -> %s%s' % (
            s, t, c['stated'], actual, 'CONSISTENT' if ok else 'MISMATCH',
            '' if ok else ' (the stated number is the difference to %s)' % (', '.join('PR%d' % m for m in explains) or 'no pinned PR')))
    need(mismatches == EXPECTED_MISMATCHES, 'mismatch set changed: %s' % sorted(mismatches))
    # README sentence of PR2435 quoting PR2374's kappa
    rel, phrase = README_2435
    readme = git(args.repo, 'show', pins['2435']['head'] + ':' + rel).stdout.decode()
    need(phrase in readme, 'PR2435 README sentence not found')
    quoted = Decimal('0.0016985113436976293')
    readme_note = dict(path=rel, phrase=phrase, quoted_as_pr2374=str(quoted),
                       pr2374_pinned=str(kappa[2374])[:24], pr2435_pinned=str(kappa[2435])[:24],
                       quoted_value_is_pr2435=str(kappa[2435]).startswith(str(quoted)))
    need(readme_note['quoted_value_is_pr2435'], 'README quote check')
    print('  PR2435 README quotes "PR2374 (our previous package, kappa 0.0016985113436976293..." but that value is '
          "PR2435's own kappa; PR2374's pinned kappa is %s..." % str(kappa[2374])[:22])
    out = dict(object='T74 handoff-line kappa ledger and stated-comparison check',
               kappas={'PR%d' % n: str(kappa[n]) for n in order},
               comparisons=rows, mismatches=sorted('PR%d->PR%d' % m for m in mismatches),
               readme_2435=readme_note, python=sys.version.split()[0])
    if args.out:
        with open(os.path.join(HERE, 'ledger.receipt.json'), 'w') as f:
            f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    print('PASS_T74_CLAIM_LEDGER prs=%d comparisons=%d consistent=%d mismatches=%s readme_2435_mislabel=1'
          % (len(kappa), len(rows), len(rows) - len(mismatches), ','.join('%d->%d' % m for m in sorted(mismatches))))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Fail as e:
        sys.stdout.write('FAIL_T74_CLAIM_LEDGER %s\n' % e)
        sys.exit(1)
