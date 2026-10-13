# SPDX-License-Identifier: Apache-2.0
"""Build T37: the unchanged PR890 T21 map, a second PR858 T16 map, eight edits.

PR890's T21 constructor (PR858 T16 + literal T5 + nine edits) and Hao Yan's
PR858 T16 constructor are imported unchanged from the repository and their own
audits run first. The second T16 copy is relabelled into replicas 21..36. The
two call sequences are merged proportionally, preserving each one's own order.
Eight frozen whole-role edits then concentrate the four non-48 remainders
(44,3,2 plus the existing ones) into six rank-one children. No optimizer runs.
All roles and windows are independently checked by independent_check.py.
"""
import argparse
import copy
from fractions import Fraction
from pathlib import Path
from common import HERE, ROOT, read, require, sha, identity, dump, write_gzip, load

T21_PACKAGE = ROOT/'research/complex-t21-owners'
SECOND = 21


def relabel(roles, shift):
    out = []
    for old in roles:
        role = dict(old)
        for key in ('replica', 'owner_replica'):
            role[key] += shift
        role['copy'] += shift*112
        role['family'] += shift*896
        out.append(role)
    return out


def merged_order(first, second):
    """Stable proportional merge: call i of `first` has key (i+1)/len(first),
    call j of `second` has key (j+1)/len(second); ties keep `first` earlier."""
    keyed = [(Fraction(i+1, len(first)), 0, tuple(c)) for i, c in enumerate(first)]
    keyed += [(Fraction(j+1, len(second)), 1, tuple(c)) for j, c in enumerate(second)]
    return [list(c) for _, _, c in sorted(keyed)]


def location(role):
    return {k: role[k] for k in ('owner_replica', 'child', 'port', 'offset')}


def move(role, destination, plan):
    role.update(destination)
    r, child, port = (role[k] for k in ('owner_replica', 'child', 'port'))
    role['copy'] = r*112+port
    role['family'] = r*896+(2*plan['pairs'][str(child)]+plan['sides'][str(child)])*112+port


def unedited(source_plan, source_owners):
    """T21 + relabelled T16 and the merged 333-call order, before the eight edits."""
    t21_builder = load(T21_PACKAGE/'build_owners.py', 'unchanged_pr890_t21_owners')
    # Its shared `common` import resolves to this package; bind its own data root.
    t21_builder.HERE = T21_PACKAGE
    t21, t21_order, t21_details = t21_builder.construct(source_plan, source_owners)
    require(len(t21) == 189*504 and len(t21_order) == 189, 'Inherited T21 inventory')
    t16_builder = load(T21_PACKAGE/'vendor/pr870/t16/build_owners.py', 'unchanged_pr858_t16_owners')
    plan, source = read(source_plan), read(source_owners)
    t16 = t16_builder.construct(source, plan)
    require(t16_builder.audit(t16, plan) == {1: 2, 2: 1, 44: 1, 48: 4793}, 'Inherited T16 audit')
    t16_order = [[s, r+8*g] for s, r in plan['order'] for g in range(2)]
    second = relabel(t16, SECOND)
    order = merged_order(t21_order, [[s, r+SECOND] for s, r in t16_order])
    at = {tuple(key): time for time, key in enumerate(order)}
    require(len(at) == 333 and set(at) == {(s, r) for s in range(9) for r in range(37)}, 'T37 invocation inventory')
    roles = copy.deepcopy(t21)+second
    for role in roles:
        role['time'] = at[role['stage'], role['replica']]
    roles.sort(key=lambda r: (r['time'], r['helper']))
    return roles, order, plan, t21, dict(t21_construction=dict(changed_roles=t21_details['changed_roles'],
                                                           t16_content_sha256=t21_details['t16_content_sha256'],
                                                           t5_content_sha256=t21_details['t5_content_sha256']),
                                    t21_content_sha256=identity(t21), second_t16_content_sha256=identity(t16))


def construct(source_plan, source_owners, edits=None):
    roles, order, plan, t21, details = unedited(source_plan, source_owners)
    before = copy.deepcopy(roles)
    bykey = {(r['time'], r['helper']): r for r in roles}
    require(len(bykey) == 333*504, 'Joined role identities')
    edits = read(HERE/'data/EDITS.json') if edits is None else edits
    for edit in edits:
        role = bykey[tuple(edit['role'])]
        require(location(role) == edit['before'], 'Frozen edit source location')
        move(role, edit['after'], plan)
    changed = sum(a != b for a, b in zip(before, roles))
    return roles, order, dict(details, changed_roles=changed), t21


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'Owner output must be new')
    source = ROOT/'research/gauge44-frames-x/data'
    roles, order, details, t21 = construct(source/'PLAN.json', source/'OWNERS.json.gz')
    require(details['changed_roles'] == 8 == len(read(HERE/'data/EDITS.json')), 'Exactly eight changed roles')
    args.out.mkdir(parents=True)
    write_gzip(args.out/'OWNERS.json.gz', roles)
    # The unchanged PR890 T21 component, for its own inherited independent audit.
    write_gzip(args.out/'T21-OWNERS.json.gz', t21)
    dump(args.out/'ORDER.json', order)
    dump(args.out/'OWNER-CONSTRUCTION.json', dict(
        status='PASS_LITERAL_T21_PLUS_T16_EIGHT_ROLE_CONSTRUCTION', roles=len(roles),
        owners_sha256=sha(args.out/'OWNERS.json.gz'), owners_content_sha256=identity(roles), **details))


if __name__ == '__main__':
    main()
