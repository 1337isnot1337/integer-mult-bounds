#!/usr/bin/env python3
"""Freeze a solver-independent patch, compacting only appended unused frames."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,gzip,hashlib,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from warp_merge import synthesize
base=json.load(gzip.open(HERE/'BASE-WORD.json.gz'));x=json.load(gzip.open(HERE/'CANDIDATE-WORD.json.gz'));c=x['canonical'];b=base['canonical'];recipes=json.load(open(HERE/'CANDIDATE.json'))['warp_recipes']
for w in c['warps']:
 rec=recipes[str(w['op'])];w['from_frame']=rec['input'];w['to_frame']=rec['output']
# Retain a predecessor logical operator whenever it already transports every
# newly selected actual frame pair; arbitrary basis completions are unnecessary.
spaces=[]
for basis in c['frames']:
 space={0}
 for v in basis:space|={x^v for x in list(space)}
 spaces.append(space)
def image(cols,x):
 y=0
 for i,v in enumerate(cols):
  if x>>i&1:y^=v
 return y
oldG={w['op']:w['G_columns'] for w in b['warps']}
restored=0
for w in c['warps']:
 cols=oldG[w['op']];table=[image(cols,x) for x in range(512)];inv={y:x for x,y in enumerate(table)}
 classes={(e[2],e[3],e[4]) for word in x['programs'].values() for e in word if e[0]=='warp' and abs(e[2])==w['op']}
 if all({(table[z] if op>0 else inv[z]) for z in spaces[a]}==spaces[d] for op,a,d in classes):
  restored+=int(w['G_columns']!=cols);w['G_columns']=cols[:]
print('Retained predecessor G where valid:',restored)
used=set(c['start']+c['final'])
for w in c['warps']:used.update((w['from_frame'],w['to_frame']))
for p in x['programs'].values():
 for e in p:
  if e[0]=='scalar':used.add(e[2])
  elif e[0] in ('warp','climb'):used.update(e[3:5])
  elif e[0]=='center':used.update(e[2:4])
keep=list(range(len(b['frames'])))+sorted(i for i in used if i>=len(b['frames']));labels={old:new for new,old in enumerate(keep)}
c['frames']=[c['frames'][i] for i in keep];c['start']=[labels[i] for i in c['start']];c['final']=[labels[i] for i in c['final']]
for w in c['warps']:
 for k in ('from_frame','to_frame'):w[k]=labels[w[k]]
for p in x['programs'].values():
 for e in p:
  if e[0]=='scalar':e[2]=labels[e[2]]
  elif e[0] in ('warp','climb'):e[3:5]=[labels[i] for i in e[3:5]]
  elif e[0]=='center':e[2:4]=[labels[i] for i in e[2:4]]
P=Counter(e[-1] for e in x['programs']['forward'] if e[0] in ('climb','center'));c['local_profile']=dict(P);c['R']=408
c['warp_edges']=[list(t) for t in sorted({(1 if e[2]>0 else -1,abs(e[2]),e[3],e[4]) for e in x['programs']['forward'] if e[0]=='warp'})]
patch=dict(base_sha256=hashlib.sha256((HERE/'BASE-WORD.json.gz').read_bytes()).hexdigest(),added_frames=c['frames'][len(b['frames']):],starts={r:f for r,f in enumerate(c['start']) if f!=b['start'][r]},warps=c['warps'],word_changes={},paid=dict(P))
for d,word in x['programs'].items():
 old=[e for e in base['programs'][d] if e[0]!='climb'];new=[e for e in word if e[0]!='climb'];assert len(old)==len(new)
 changes=[]
 for i,(a,z) in enumerate(zip(old,new)):
  if a!=z:
   assert a[0]==z[0] and a[0] in ('scalar','warp')
   assert (a[1]==z[1]) if a[0]=='scalar' else(a[1:3]==z[1:3])
   changes.append(dict(index=i,old=a,new=z))
 patch['word_changes'][d]=changes
 assert synthesize(c,new)==word
raw=json.dumps(x,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0)
(HERE/'PATCH.json').write_text(json.dumps(patch,indent=2)+'\n');(HERE/'ACTUAL-WORD.json.gz').write_bytes(compressed)
(HERE/'FROZEN.json').write_text(json.dumps(dict(compressed_sha256=hashlib.sha256(compressed).hexdigest(),payload_sha256=hashlib.sha256(raw).hexdigest(),frames=len(c['frames']),added_used_frames=len(patch['added_frames'])),indent=2)+'\n')
print('Frozen',len(patch['starts']),'helper entrances',len(c['frames']),'frames',dict(P))
