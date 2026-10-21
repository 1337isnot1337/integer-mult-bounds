#!/usr/bin/env python3
"""Replay source-bound terminal trimming, native p7 phases and the endpoint.

1337isnot1337 with substantial OpenAI Codex assistance. Apache-2.0.
Credits and conditional boundaries are detailed in README.md.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIOUS = ROOT/'research/pr4359-p7-padding'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def module(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


def encode(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x


def authenticate():
    manifest = json.loads((HERE/'SOURCES.json').read_text())
    checked = {}
    for row in manifest['files']:
        if row['usage'] != 'input':
            continue
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'],
             'Canonical source path')
        path = ROOT
        for part in rel.parts:
            path /= part
            need(not path.is_symlink(),'No source aliases')
        need(row['path'] not in checked,'Unique source pin')
        digest = sha256(path.read_bytes()).hexdigest()
        need(digest == row['sha256'],'Authenticated source: '+row['path'])
        checked[row['path']] = digest
    need(checked,'Nonempty authenticated source closure')
    return checked


def native_inventory():
    old = module('credited_pr4416_native',PREVIOUS/'native_inventory.py').run(PREVIOUS/'source')
    trim = module('new_terminal_trim',HERE/'native_trim.py').run()
    need(trim['status'] == 'PASS_TERMINAL_HELPER_TRIM_ALL_632_INPUTS_BOTH_ORIENTATIONS',
         'Both orientations and new exact helper normalizers pass')
    receipt = json.loads((PREVIOUS/'source/research/kappa-rebuild/complex/full-identity-certificates/RESULT.json').read_text())['providers']['THREE-base']
    old_H = Counter({int(k):v for k,v in receipt['helper_boundary']['widths'].items()})
    old_P = Counter({int(k):v for k,v in receipt['unsplit_replays']['forward']['paid_profile'].items()})
    new_H = Counter({int(k):v for k,v in trim['local_unsplit_targets'].items()})
    new_P = Counter({int(k):v for k,v in trim['local_unsplit_paid'].items()})
    stages = 2*old['p']+1
    need(stages == 15 and sum(old_H.values()) == sum(new_H.values()) == 408,
         'Every stage preserves all independent helper roles')
    need(old_H-new_H == Counter({5:22}) and new_H-old_H == Counter({4:22}),
         'Exactly22 helpers change productive rank5 to4')
    need(old_P-new_P == Counter({1:22}) and not new_P-old_P,
         'Exactly22 paid rank-one calls disappear per stage')
    T = Counter({int(k):v for k,v in old['targets'].items()})
    P = Counter({int(k):v for k,v in old['paid'].items()})
    for hist,before,after in ((T,old_H,new_H),(P,old_P,new_P)):
        for rank in set(before)|set(after):
            hist[rank] += stages*(after[rank]-before[rank])
        need(all(n >= 0 for n in hist.values()),'No negative rank multiplicities')
    T,P = +T,+P
    need(sum(T.values()) == old['productive_fields'] == 7688,
         'No new independent input credit')
    rank_margin = sum(k*n for k,n in T.items())-sum(k*n for k,n in P.items())
    need(rank_margin == old['rank_margin'] == 608,'Rank-one surplus is unchanged')
    return {'status':'PASS_TRIMMED_NATIVE_P7_WITH_SOURCE_GEOMETRY',
            'p':old['p'],'keep':old['keep'],'dimension':old['dimension'],
            'targets':dict(sorted(T.items())),'paid':dict(sorted(P.items())),
            'productive_fields':sum(T.values()),'paid_calls':sum(P.values()),
            'rank_margin':rank_margin,'removed_paid_rank_one_calls':22*stages,
            'native_scalar_allowance':old['native_scalar_allowance'],
            'new_adapter_cost_scope':'New finite monomial/route records are included when expanding full operation, height, error and stock constants; this field counts the source scalar primitives only.',
            'unchanged_main_geometry':old, 'local_trim':trim}


def verify():
    sources = authenticate()
    native = native_inventory()
    strict = module('new_strictification',HERE/'strictification.py').run(native)
    endpoint = module('new_endpoint',HERE/'endpoint.py').run(strict)
    family = module('new_family_limit',HERE/'family_limit.py')
    need(family.INVOICES['trimmed']['helpers'] ==
         {int(k):v for k,v in native['local_trim']['local_unsplit_targets'].items()}
         and family.INVOICES['trimmed']['paid'] ==
         {int(k):v for k,v in native['local_trim']['local_unsplit_paid'].items()},
         'The scoped family limit uses the actual new local invoice')
    family_result = family.run()
    # Independently written atanh/Taylor engine from PR4405, in contrast with
    # PR4433's outward fixed-point scaling/squaring engine used above.
    I = module('independent_pr4405_intervals',PREVIOUS/'dependencies/compiler-refill/template_bound.py')
    C = Q(strict['tested_saving'])
    T,P = native['targets'],native['paid']
    tlo,thi = I.moment_margin(T,{},C)
    plo,phi = I.moment_margin(P,{},C)
    need(tlo-phi > 0 and phi/tlo < 1-Q(1,10**9),
         'Independent new native moment and alpha cross-check')
    need(I.moment_margin(T,P,Q('.002696357'))[1] < 0,
         'Independent rejection above raw root bracket')
    bit = json.loads((PREVIOUS/'source/research/kappa-rebuild/bit/BIT-ALLSIZE-PARAMETERS.json').read_text())
    need(Q(bit['ordinary_saving_admitted']) == Q(endpoint['outer']['parameters']['bit_saving']),
         'Unchanged source ordinary BIT admission')
    return encode({'status':'PASS_SOURCE_BOUND_CONDITIONAL_TERMINAL_TRIM_IMPROVEMENT',
                   'kappa':endpoint['kappa'],'source_files':len(sources),
                   'native':native,'strictification':strict,'endpoint':endpoint,
                   'family_limit':family_result,
                   'independent_raw_moment_crosscheck':True,
                   'scope':'Exact local all-input replay, native p7 geometry, new phase normalizers, finite moment and outer arithmetic. The inherited all-column/analytic/precision/storage/fixed-tape/recovery hypotheses are explicit premises, not a formally verified full multiplication theorem.'})


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write-result',action='store_true')
    args = ap.parse_args()
    result = verify()
    receipt = HERE/'RESULT.json'
    if args.write_result:
        receipt.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        need(result == json.loads(receipt.read_text()),'Exact saved mathematical receipt reproduction')
    print(json.dumps({'status':result['status'],'kappa':result['kappa'],
                      'tensor_power':result['strictification']['tensor_power'],
                      'uniform_rank':result['endpoint']['compiler']['N'],
                      'source_files':result['source_files']}))
