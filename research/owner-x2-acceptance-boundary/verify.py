#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""X2 acceptance-boundary audit for the selected CrocSwap/integer-mult-bounds#1094 supplier owner map.

Navinor, with help from opencode. Apache-2.0.

One named obligation of the selected complex supplier (certificates/selected-result.json,
CrocSwap/integer-mult-bounds#1094 frozen OWNERS/PLAN/SPEC at audited head 0fc329d0bec93ca7cd288eaea1295172e8789810):

  X2  pending axes of distinct idle children of one physical family are disjoint,
      so a family's hosts on different children never share a cell.

X2 is checked by geometry() in Josie Elliston's independent owner audit
(research/t16-owner-audit-seed67/verify.py, CrocSwap/integer-mult-bounds#1091), composed onto CrocSwap/integer-mult-bounds#1094 by
research/community-batch1099-audit/check_frontier1094.py. This package traces
where that check actually executes, and builds the smallest semantic
counterexample it rejects: a one-integer mutation of the pinned DATA-PHASES
pending axes that preserves every role-level and window-level aggregate.

Checks in this file:
  1. Positive control: the pinned inputs pass the complete R1-R7/X1/X2 audit.
  2. M1 (minimal adversarial instance): one pending axis of one idle child is
     replaced by an axis already pending for a distinct idle child of the same
     physical family at the same port. Superficial aggregates (ranks, windows,
     role counts, widths, profile) are unchanged. geometry() must reject at X2.
  2b. Witness: under M1, exhibit the exact physical cell written twice (family,
      axis) by two roles that every role-level rule accepts.
  3. M2 failure control: one axis duplicated inside a single child's pending
     list. geometry() must reject at X2 as well.
  4. Blindness: with only the X2 need() suppressed, geometry() returns an
     identical geometry object and the complete R1-R7/X1 rule set accepts the
     M1 fixture. The X2 rule is the only rule that reads pending axes.
  5. Coverage inventory: the existing 11 owner-audit controls and the frozen
     verifier's 6 independent-t16 controls contain no X2-directed mutant.
  6. Enforcement trace (static, recorded with exact excerpts): the selected
     reproduce command and the CI workflow do not execute the CrocSwap/integer-mult-bounds#1094 owner
     composition, and the frozen CrocSwap/integer-mult-bounds#1087 verifier chain keys hosted cells per
     (owner, child, port), so cross-child cell sharing is outside its rule set.

Unrun obligations are listed in RESULT.json and the README.
"""
import copy
import gzip
import hashlib
import importlib.util
import json
import re
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    path = Path(path)
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())


def text(path):
    return Path(path).read_text(encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError('X2 boundary audit: ' + message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- inputs

a = load_module('owner_audit', ROOT / 'research/t16-owner-audit-seed67/verify.py')
pins = read(ROOT / 'research/t16-owner-audit-seed67/SOURCES.json')['inputs']
require(sha(ROOT / a.TEMPLATE) == pins['template_sha256'], 'template pin')
require(sha(ROOT / a.PHASES) == pins['data_phases_sha256'], 'DATA-PHASES pin')
require(hashlib.sha256(gzip.decompress(a.WORD.read_bytes())).hexdigest() == pins['word_content_sha256'],
        'seven-slot word pin')

word = read(a.WORD)
template = read(ROOT / a.TEMPLATE)
phases = read(ROOT / a.PHASES)
widths = a.word_widths(word)
local = a.as_profile(word['report']['local_profile'])

pkg = ROOT / 'research/complex-t16-rare-pattern-exchanges'
spec = read(pkg / 'data/SPEC.json')
plan = read(pkg / 'data/PLAN.json')
roles = read(pkg / 'data/OWNERS.json.gz')
expected_idle = a.as_profile(spec['expected']['idle_remainder_profile'])
T = 16

# ---------------------------------------------------------------- 1. positive control

geo0 = a.geometry(template, phases)
owned0 = a.audit(geo0, widths, local, roles, plan, expected_idle, T)
require(owned0['roles'] == len(roles), 'positive control role count')

# ---------------------------------------------------------------- M1 fixture

place, rank = geo0['place'], geo0['rank']
children = sorted(rank)


def axes_lists(ph):
    """Yield mutable (recipe_index, child_key, list) pending-axis lists."""
    for ri, recipe in enumerate(ph['recipes']):
        kids = recipe['idle_children']
        items = enumerate(kids) if isinstance(kids, list) else ((int(k), v) for k, v in kids.items())
        for child, item in items:
            yield ri, child, item['orthogonal_axes']


axes_map = {}
for ri, child, raw in axes_lists(phases):
    axes_map[child, phases['recipes'][ri]['port']] = [int(x) for x in raw]

groups = {}
for child in children:
    groups.setdefault(place[child], []).append(child)

candidate = None
for where, siblings in sorted(groups.items()):
    for i, c1 in enumerate(siblings):
        for c2 in siblings[i + 1:]:
            for port in range(112):
                l1 = axes_map.get((c1, port))
                l2 = axes_map.get((c2, port))
                if not l1 or not l2:
                    continue
                shared = [x for x in l1 if x not in l2]
                if not shared:
                    continue
                for k in range(len(l2)):
                    if l2[k] not in l1:
                        candidate = dict(where=where, c1=c1, c2=c2, port=port,
                                         value=shared[0], c1_index=l1.index(shared[0]), c2_index=k)
                        break
                if candidate:
                    break
            if candidate:
                break
        if candidate:
            break
    if candidate:
        break
require(candidate is not None, 'no cross-child axis locus found')

phases_m1 = copy.deepcopy(phases)
port_index = next(ri for ri, r in enumerate(phases_m1['recipes']) if r['port'] == candidate['port'])
kids = phases_m1['recipes'][port_index]['idle_children']
entry = kids[candidate['c2']] if isinstance(kids, list) else kids[str(candidate['c2'])]
before = int(entry['orthogonal_axes'][candidate['c2_index']])
entry['orthogonal_axes'][candidate['c2_index']] = candidate['value']

# Single-locus and superficial-aggregate guards.
raw_delta = sum(1 for (_, _, old), (_, _, new) in zip(axes_lists(phases), axes_lists(phases_m1))
                for u, v in zip(old, new) if int(u) != int(v))
require(raw_delta == 1, 'M1 must be a one-integer mutation')
geo_m1_x2suppressed = None

rejects = {}
for name, ph in (('M1_cross_child_axis', phases_m1),):
    try:
        a.geometry(template, ph)
    except a.Reject as exc:
        rejects[name] = str(exc)
require(rejects.get('M1_cross_child_axis', '').startswith('X2:'),
        'M1 must be rejected at X2, got: ' + rejects.get('M1_cross_child_axis'))

# ---------------------------------------------------------------- 2b. cell-collision witness

c1, c2, port = candidate['c1'], candidate['c2'], candidate['port']
pair, side = place[c1]
require(place[c2] == (pair, side), 'witness children must share the physical family')
value = candidate['value']
axis_index_in_bases = None


def covers(role, child, port_, index):
    return (role['child'] == child and role['port'] == port_
            and role['offset'] <= index < role['offset'] + role['width'])


witness = None
for owner in range(T):
    left = [z for z in roles if z['owner_replica'] == owner and covers(z, c1, port, candidate['c1_index'])]
    right = [z for z in roles if z['owner_replica'] == owner and covers(z, c2, port, candidate['c2_index'])]
    if left and right:
        z1, z2 = left[0], right[0]
        family = owner * a.FAMILIES_PER_REPLICA + (2 * pair + side) * a.V + port
        require(z1['family'] == family and z2['family'] == family, 'witness family identity')
        witness = dict(owner_replica=owner, family=family, shared_axis=value,
                       role_a={k: z1[k] for k in ('time', 'stage', 'replica', 'helper', 'child', 'port', 'offset', 'width')},
                       role_b={k: z2[k] for k in ('time', 'stage', 'replica', 'helper', 'child', 'port', 'offset', 'width')},
                       note='Both roles resolve pending-axis %d of family %d at port %d; the R1-R7/X1 rule set '
                            'keys cells per (owner, child, port) and accepts both.' % (value, family, port))
        break
require(witness is not None, 'no colliding role pair found for M1')

# ---------------------------------------------------------------- 3. M2 failure control

phases_m2 = copy.deepcopy(phases)
m2 = None
for ri, child, raw in axes_lists(phases_m2):
    vals = [int(x) for x in raw]
    if len(vals) >= 2:
        duplicate = vals[0]
        if duplicate not in vals[1:]:
            kids = phases_m2['recipes'][ri]['idle_children']
            entry = kids[child] if isinstance(kids, list) else kids[str(child)]
            entry['orthogonal_axes'][-1] = duplicate
            m2 = dict(recipe_index=ri, child=child, index=len(vals) - 1,
                      port=phases_m2['recipes'][ri]['port'], value=duplicate)
            break
require(m2 is not None, 'no within-child duplicate locus found')
require((m2['recipe_index'], m2['child'], m2['index'])
        != (port_index, candidate['c2'], candidate['c2_index']), 'M1 and M2 must use different loci')
try:
    a.geometry(template, phases_m2)
except a.Reject as exc:
    rejects['M2_within_child_duplicate'] = str(exc)
require(rejects.get('M2_within_child_duplicate', '').startswith('X2:'),
        'M2 must be rejected at X2, got: ' + rejects.get('M2_within_child_duplicate'))

# ---------------------------------------------------------------- 4. blindness of R1-R7/X1

original_need = a.need


def need_x2_suppressed(ok, rule, msg):
    if rule == 'X2':
        return
    original_need(ok, rule, msg)


a.need = need_x2_suppressed
try:
    geo_m1_x2suppressed = a.geometry(template, phases_m1)
    owned_m1 = a.audit(geo_m1_x2suppressed, widths, local, roles, plan, expected_idle, T)
finally:
    a.need = original_need
require(geo_m1_x2suppressed == geo0, 'geometry object must not depend on pending axes')
require(owned_m1 == owned0, 'R1-R7/X1 must be blind to the X2 violation')

# ---------------------------------------------------------------- 5. control inventory

controls = a.controls(geo0, widths, local, roles, plan, expected_idle, T)
control_names = [c['name'] for c in controls]
require(len(control_names) == 11 and all(c['rejected_by'] != 'X2' or c['name'] == 'plan_window_truncated'
                                        for c in controls), 'unexpected owner-audit control battery')

tar_path = pkg / 'upstream1087.tar.gz'
frozen = {}
with tarfile.open(tar_path) as tar:
    for name in ('verify_t16.py', 't16/indep16.py', 'code/audit_allcold.py', 'code/emit_allcold.py'):
        frozen[name] = tar.extractfile(name).read().decode('utf-8')
indep_controls = re.findall(r"candidates\.append\(\('([a-z0-9_]+)'", frozen['t16/indep16.py'])
require(len(indep_controls) == 6, 'frozen independent-t16 control battery size')
require('X2' not in ''.join(frozen.values()), 'frozen verifier unexpectedly mentions X2')

# ---------------------------------------------------------------- 6. enforcement trace

makefile = text(ROOT / 'Makefile')
m = re.search(r'frontier1094-verify:.*?(?=\n\S)', makefile, re.S)
require(m is not None, 'frontier1094-verify target missing')
target = m.group(0)
verify_frontier = text(ROOT / 'scripts/verify_frontier1094.py')
selected_record_check = text(ROOT / 'scripts/verify_selected_result.py')
ci = text(ROOT / '.github/workflows/community-batch1099.yml')
claim_prs = [c['pr'] for c in read(ROOT / 'research/t16-owner-audit-seed67/SOURCES.json')['claims']]
require('check_frontier1094' not in target and 'check_frontier1094' not in verify_frontier
        and 'check_frontier1094' not in selected_record_check, 'reproduce path unexpectedly runs the composition')
require('check_frontier1094' not in ci, 'CI unexpectedly runs the composition')
require('research/t16-owner-audit-seed67/verify.py --fetch' in ci, 'CI owner-audit step missing')
require(1094 not in claim_prs, 'CrocSwap/integer-mult-bounds#1094 unexpectedly inside the owner-audit claim list')
require('bin_key = (owner, child, port)' in frozen['t16/indep16.py'], 'indep16 bin keying changed')
require('orthogonal_axes' in frozen['code/audit_allcold.py']
        and 'len(pend)==prank[i]' in frozen['code/audit_allcold.py'], 'audit_allcold pending-axis read changed')

# ---------------------------------------------------------------- result

result = dict(
    status='PASS_PR1094_X2_ACCEPTANCE_BOUNDARY_AUDIT',
    scope=dict(
        obligation='X2: pending axes of distinct idle children of one physical family are disjoint',
        object='selected CrocSwap/integer-mult-bounds#1094 frozen OWNERS/PLAN/SPEC data (research/complex-t16-rare-pattern-exchanges/data)',
        audited_head='0fc329d0bec93ca7cd288eaea1295172e8789810',
        selected_kappa='836330098538459/500000000000000000',
    ),
    pins=dict(template_sha256=pins['template_sha256'], data_phases_sha256=pins['data_phases_sha256'],
              word_content_sha256=pins['word_content_sha256'],
              owners_sha256=sha(pkg / 'data/OWNERS.json.gz'), plan_sha256=sha(pkg / 'data/PLAN.json'),
              spec_sha256=sha(pkg / 'data/SPEC.json'),
              owner_audit_sha256=sha(ROOT / 'research/t16-owner-audit-seed67/verify.py'),
              composition_sha256=sha(ROOT / 'research/community-batch1099-audit/check_frontier1094.py'),
              upstream1087_sha256=sha(tar_path)),
    positive_control=dict(idle=owned0['idle'], profile=owned0['profile'], rank_mass=owned0['rank_mass'],
                          deficit=owned0['deficit'], calls=owned0['calls'], roles=owned0['roles'],
                          windows=owned0['windows'], x2_child_ports=geo0['x2_child_ports']),
    minimal_adversarial_instance=dict(
        mutation='one integer in DATA-PHASES pending axes',
        locus=dict(where=list(candidate['where']), children=[c1, c2], port=port,
                   replaced_index_in_c2=candidate['c2_index'], old_value=before, new_value=value,
                   taken_from_child=c1, index_in_c1=candidate['c1_index']),
        mutated_differing_integers=raw_delta,
        rejected_by=rejects,
        cell_collision_witness=witness),
    blindness=dict(
        method='X2 need() suppressed only to measure what the remaining rule set sees',
        geometry_identical=geo_m1_x2suppressed == geo0,
        rule_set_accepts=owned_m1 == owned0,
        rule_set='R1-R7 plus X1 (owner-audit rule bodies)'),
    control_inventory=dict(owner_audit_controls=control_names,
                           frozen_independent_t16_controls=indep_controls,
                           x2_directed_mutants_before_this_package=0),
    enforcement_trace=dict(
        reproduce_target=target.strip().splitlines(),
        reproduce_stages=['historical-source', 'baseline1042-cold (or baseline reuse)', 'rare-pattern-exchanges'],
        selected_record_check='scripts/verify_selected_result.py validates the selected record and its '
                              'proof_supplement hashes; it imports no subprocess module and executes no composition',
        ci_workflow='.github/workflows/community-batch1099.yml runs research/t16-owner-audit-seed67/verify.py --fetch '
                    '(its pinned claim list excludes the selected supplier) and check_pr1048_counterexample.py; '
                    'it does not run check_frontier1094.py',
        x2_checked_by='research/t16-owner-audit-seed67/verify.py geometry(), composed on CrocSwap/integer-mult-bounds#1094 by '
                      'research/community-batch1099-audit/check_frontier1094.py at batch1099 review time',
        frozen_chain='upstream1087.tar.gz verify_t16.py stages lift16/audit_allcold/indep16; indep16 keys cells per '
                     '(owner, child, port); audit_allcold asserts only len(pending) == rank per child',
    ),
    unrun_obligations=[
        'Full make frontier1094-verify cold replay with the M1-mutated DATA-PHASES (needs the frontier1042 cold baseline; '
        'out of session budget). Acceptance of M1 by the frozen chain is established by code trace, not by execution.',
        'No T8/T16 claim other than CrocSwap/integer-mult-bounds#1094 was re-audited; the historical owner-boundary-audit package was not rerun.',
        'No kappa, supplier adoption, or multiplication-theorem claim is made or tested here.',
    ],
)
(HERE / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(result['status'], 'M1 rejected at', rejects['M1_cross_child_axis'][:60])
