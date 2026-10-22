#!/usr/bin/env python3
"""Exact necessary screen for a fixed scalar response-space decoder.
Apache-2.0. Substantial OpenAI assistance. No new kappa claimed.
"""
from fractions import Fraction as F
if not __debug__:raise RuntimeError("Assertions must be enabled")
from pathlib import Path
import hashlib, importlib.util, json, sys
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder'
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
n=load(BASE/'native_common.py','hull_native')
r=load(ROOT/'research/kappa-rebuild/complex/rebuild_native.py','hull_geometry')
packet,phases=n.load_sources(); geo=r.geometry(packet)
qs=[x['q'] for x in phases['recipes']]
# H-I=UC with C=[L,I] and U=[-L^t;11I], in original port order.
U=[[11*int(i==a) if i in geo['selected'] else -geo['L'][k].get(i,F(0))
    for k,a in enumerate(geo['selected'])] for i in range(112)]
assert all(any(row) for row in U)
assert len(set(qs))==112
C=[[geo['L'][k].get(j,F(0)) if j not in geo['selected'] else F(j==a) for j in range(112)] for k,a in enumerate(geo['selected'])]
assert all(sum(U[i][k]*C[k][j] for k in range(8)) == geo['H'][i].get(j,F(0))-int(i==j) for i in range(112) for j in range(112))

def rank(rows):
    basis={}
    for row in rows:
        v=list(map(F,row))
        for j,b in sorted(basis.items()):
            if v[j]:
                c=v[j];v=[x-c*y for x,y in zip(v,b)]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:
            c=v[j];basis[j]=[x/c for x in v]
    return len(basis)

from collections import Counter
import random
from itertools import product
import time
beg=time.monotonic();rows=[]
for y in range(512):
 groups=[[U[p] for p,q in enumerate(qs) if ((q&y).bit_count()%2)==b] for b in [0,1]]
 dims=[rank(g) for g in groups];rows.append(dict(frequency=y,eigenclass_ranks=dims,required_channels=sum(dims)))
print('POINTWISE',dict(Counter(v['required_channels'] for v in rows)),flush=True)
# Each individual eigenvalue projector preserves a proposed invariant module.
# At a fixed frequency, its dimension must contain each restricted U column span.
rng=random.Random(20261022);witness=None
for trial in range(128):
 ys=[rng.randrange(1,512) for _ in range(3)]
 groups=[[U[p] for p,q in enumerate(qs) if sum((q&y).bit_count()%2 for y in ys)%4==b] for b in range(4)]
 dims=[rank(g) for g in groups]
 if sum(dims)==32:witness=dict(frequencies=ys,eigenclass_ranks=dims,required_channels=32);break
assert witness is not None
out=dict(status='EXACT_POINTWISE_RESPONSE_CHANNEL_RANK',rows=rows,distribution=dict(Counter(v['required_channels'] for v in rows)),three_column_witness=witness,seconds=time.monotonic()-beg,no_kappa_claim=True)
path=Path(__file__).with_name('RESULT.json')
if '--check' in sys.argv:
 old=json.loads(path.read_text());assert {k:v for k,v in old.items() if k!='seconds'}=={k:v for k,v in out.items() if k!='seconds'}
else:path.write_text(json.dumps(out,indent=2)+'\n')
print('THREE_COLUMNS',witness)
