#!/usr/bin/env python3
"""Entry point: independent audit of the PR #2802 increment over PR #2751 (T74 retired7), verdict extended to PR #2818.

Runs every named rule of increment_audit.py on the pinned inputs, then the 15 negative controls of
increment_controls.py (each must be rejected by its named rule).  Inputs are git blobs at the pinned PR heads,
checked against sha256 pins; --fetch downloads refs/pull/<n>/head only for absent commits (FETCH_HEAD only).

Usage (repository root):  python3 -I -B research/t74-retired7-increment-audit/verify.py --fetch [--out RECEIPT.json]
Final line: PASS_T74_RETIRED7_INCREMENT_AUDIT rules=26/26 controls=15/15 ... or FAIL_T74_RETIRED7_INCREMENT_AUDIT ...

Prepared by thakrarsagar with substantial AI assistance from Claude (Anthropic, Claude Opus 5.5). Apache-2.0.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import increment_audit as A  # noqa: E402
import increment_controls as K  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument('--blob-dir', help='exported blobs laid out as DIR/<commit[:12]>/<repo path>')
    ap.add_argument('--fetch', action='store_true', help='fetch the pinned PR heads if absent (writes FETCH_HEAD only)')
    ap.add_argument('--out', help='write the deterministic receipt here')
    a = ap.parse_args()
    t0 = time.monotonic()
    if a.fetch and not a.blob_dir:
        A.fetch_missing(a.repo)
    js = A.load_all(a.repo, a.blob_dir)
    res = A.run_all(js)
    ok_c, ctl = K.run(js)
    n_rules = len(res['rules'])
    n_pass = sum(1 for v in res['rules'].values() if v['ok'])
    n_ctl = sum(1 for v in ctl.values() if v['rejected_by_expected_rule'])
    receipt = dict(
        status='PASS' if (res['ok'] and ok_c) else 'FAIL',
        commits=A.COMMIT, pins={k: dict(commit=A.COMMIT[v[0]], path=v[1], sha256=v[2]) for k, v in sorted(A.PINS.items())},
        claims_under_test=A.CLAIMED, rules=res['rules'], controls=ctl,
        scope=('Finite exact checks of the PR #2802 increment (stages refit5/alias5/refit5c/refit7/hostmove2/alias7/refit7c) '
               'over the pinned PR #2751 words: event diff, per-register occupancy, warps/frames/profile, free-algebra and '
               'matrix replays, the 271728-role fill with word-derived R, complete profile/mass/root, and PR #2818 identity. '
               'Inherited T74/#1319 admission, native lowering, outer proof and PR #2751 recovery are not checked.'))
    if a.out:
        with open(a.out, 'w') as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True, default=str)
            fh.write('\n')
    line = '%s rules=%d/%d controls=%d/%d commit2802=%s commit2818=%s' % (
        'PASS_T74_RETIRED7_INCREMENT_AUDIT' if receipt['status'] == 'PASS' else 'FAIL_T74_RETIRED7_INCREMENT_AUDIT',
        n_pass, n_rules, n_ctl, len(ctl), A.COMMIT['c2802'][:12], A.COMMIT['c2818'][:12])
    print('elapsed %.0fs' % (time.monotonic() - t0))
    print(line)
    return 0 if receipt['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
