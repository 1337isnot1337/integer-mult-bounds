# SPDX-License-Identifier: Apache-2.0
"""Reject every omitted T37 edit and a non-interleaved (sequential) schedule."""
import argparse
import copy
from pathlib import Path
from common import HERE, ROOT, read, require, dump, load
from build_owners import move


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--local', type=Path, required=True)
    parser.add_argument('--owners', type=Path, required=True)
    parser.add_argument('--order', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    audit = load(HERE/'independent_check.py', 'independent_t37_controls')
    audit.T, audit.EXPECTED_IDLE = 37, {48: 11086, 1: 6}
    parent = read(args.base/'split-centres/GLOBAL-TEMPLATE.json.gz')
    phases = read(args.base/'work/complex-nine-native/DATA-PHASES.json')
    ports = read(args.base/'split-centres/CANONICAL-WORD.json.gz')['ports']
    word = read(args.local/'CANONICAL-WORD.json.gz')
    replay = read(args.local/'INDEPENDENT-LOCAL-REPLAY.json')
    roles = read(args.owners)
    context = audit.make_context(parent, phases, ports, word, replay, roles)
    audit.check_roles(context, roles)
    plan = read(ROOT/'research/gauge44-frames-x/data/PLAN.json')
    rejected = []
    for edit in read(HERE/'data/EDITS.json'):
        bad = copy.deepcopy(roles)
        role = next(r for r in bad if [r['time'], r['helper']] == edit['role'])
        move(role, edit['before'], plan)
        try:
            audit.check_roles(context, bad)
        except ValueError as error:
            rejected.append(dict(role=edit['role'], reason=str(error)))
        else:
            raise ValueError('Accepted omitted T37 edit: '+str(edit['role']))
    require(len(rejected) == 8, 'Eight omitted-edit rejections')
    # The same roles under the complete sequential schedule (all T21 calls,
    # then all second-T16 calls). Each component keeps its own order, so only
    # the cross-component trade can fail; rebuild the actual event windows.
    order = read(args.order)
    sequential = [key for key in order if key[1] < 21]+[key for key in order if key[1] >= 21]
    at = {tuple(key): time for time, key in enumerate(sequential)}
    bad = copy.deepcopy(roles)
    for role in bad:
        role['time'] = at[role['stage'], role['replica']]
    other = audit.make_context(parent, phases, ports, word, replay, bad)
    try:
        audit.check_roles(other, bad)
    except ValueError as error:
        sequential_reason = str(error)
    else:
        raise ValueError('Accepted sequential schedule')
    dump(args.out, dict(status='PASS_EIGHT_T37_OMITTED_EDITS_AND_SEQUENTIAL_CONTROL',
                       omitted_edit_controls=rejected, sequential_schedule_rejection=sequential_reason))
    print('PASS eight omitted edits and sequential-schedule control')


if __name__ == '__main__':
    main()
