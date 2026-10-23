#!/usr/bin/env python3
"""Exact ghost-rank witness for the original continuous relaxation only.
JoyboyBrian, with OpenAI Codex assistance. Apache-2.0.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import load, build, need, HERE

EDGE = (9288, 11432, (1,2,4,8,16,32,64,128,256))


def feasible(ns, values):
    need(len(values) == len(ns['initial']), 'Column count')
    for value, low, high in zip(values, ns['lp'].col_lower_, ns['lp'].col_upper_):
        need(F(low) <= value <= F(high), 'Variable bound')
    for i,(row,low,high) in enumerate(zip(ns['rows'], ns['lb'], ns['ub'])):
        total = sum((F(c)*values[k] for k,c in row.items()), F(0))
        need((low == float('-inf') or F(low) <= total) and
             (high == float('inf') or total <= F(high)), 'Model row ' + str(i))


def witness(ns, frame):
    need(EDGE in ns['yd'] and ns['E'][EDGE] == 1, 'Actual unique witness edge')
    a,b,m = EDGE
    values = [F(v) for v in ns['initial']]
    ns['g'].check(ns['s'].original_values)
    need(frame.dimension(ns['s'].original_values[b])-frame.dimension(ns['s'].original_values[a]) == 1, 'Actual source rank one')
    ys = ns['yd'][EDGE]
    need({0,1,2} <= set(ys), 'Witness selector ranks')
    for r,k in ys.items():
        values[k] = F(1,2) if r in (0,2) else F(0)
    feasible(ns, values)
    need(all(values[k] == F(ns['initial'][k]) for ks in ns['x'].values() for k in ks), 'All source frames fixed')
    need([k for k in range(len(values)) if values[k] != F(ns['initial'][k])] == sorted(ys[r] for r in (0,1,2)), 'Only three selector entries change')
    return values


def run():
    frame,replay,retained=load()
    result={'status':'PASS_ORIGINAL_CONTINUOUS_RELAXATION_GAP', 'scope':'Original marginal/rank-selector continuous relaxation; not the binary MIP or a pair-consistent LP', 'directions':{}}
    for direction in ('forward','backward'):
        ns=build(direction,frame,replay,retained)
        feasible(ns,[F(v) for v in ns['initial']])
        values=witness(ns,frame)
        model={'rows':[{str(k):v for k,v in sorted(r.items())} for r in ns['rows']],
               'lower':['-inf' if l == float('-inf') else l for l in ns['lb']], 'upper':ns['ub'],
               'columns':len(values), 'unit_column_bounds':True}
        result['directions'][direction]={'nodes':len(ns['lo']),'flexible':len(ns['D']),
            'domain_choices':sum(map(len,ns['D'].values())), 'columns':len(values),'rows':len(ns['rows']),
            'nonzeros':sum(map(len,ns['rows'])), 'builder_lines':ns['builder_lines'],
            'model_sha256':hashlib.sha256(json.dumps(model,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'program_sha256':hashlib.sha256(json.dumps(retained['programs'][direction],separators=(',',':')).encode()).hexdigest(),
            'edge':[EDGE[0],EDGE[1],list(EDGE[2])], 'selector_columns':ns['yd'][EDGE],
            'source_bases':[frame.basis(ns['s'].original_values[i]) for i in EDGE[:2]],
            'all_rows_and_bounds_exact':True}
    return result

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
