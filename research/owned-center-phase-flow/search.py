"""Exact phase-form screen with owned-center gauges, extending PR4654.
Discovery only; positive solutions require separate physical admission.
"""
from pathlib import Path
if not __debug__:raise RuntimeError("Run with assertions enabled")
import gzip,json,time,sys
from hashlib import sha256
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
blob=(ROOT/'research/helper-warp-joint/ACTUAL-WORD.json.gz').read_bytes()
assert sha256(blob).hexdigest()=='a576b7d9f3559306b2f3bc99d23ecb2c23fd78b28bdf0cfab19bed852103ffd6'
x=json.loads(gzip.decompress(blob));c=x['canonical'];p=x['programs']['forward'];frames=c['frames'];t0=time.monotonic()
parent=[];frame=[];zero=set();links=[]
def node(f):
 n=len(parent);parent.append(n);frame.append(f);return n
def find(n):
 while parent[n]!=n:parent[n]=parent[parent[n]];n=parent[n]
 return n
def union(a,b):
 a,b=find(a),find(b)
 if a==b:return
 assert frame[a]==frame[b]
 parent[b]=a
cur=[node(f) for f in c['start']];starts=cur[:];zero.update(cur[:224])
owned=None
for e in p:
 kind=e[0]
 if kind=='climb':
  r,a,b=e[2:5];assert frame[cur[r]]==a;n=node(b);links.append(('paid',cur[r],n,None));cur[r]=n
 elif kind=='warp':
  _,r,op,a,b=e;r=r[1];assert frame[cur[r]]==a;n=node(b);links.append(('warp',cur[r],n,op));cur[r]=n
 elif kind=='scalar':
  g=e[1];roles=g[1:3] if g[0] in ('add','copy') else g[1:2]
  if g[0]=='clear':
   assert g[1]==['C',0];owned=node(e[2]);continue
  ns=[cur[r[1]] if r[0]=='L' else owned for r in roles]
  assert all(n is not None and frame[n]==e[2] for n in ns)
  for n in ns[1:]:union(ns[0],n)
 elif kind=='center':
  _,r,a,b,rank=e;assert r==0 and frame[owned]==a
  n=node(b);links.append(('paid',owned,n,None));owned=n
 elif kind=='adapter':zero.add(cur[e[2]])
ends=cur[:];zero.update(cur[:224]);zero={find(n) for n in zero};roots=sorted({find(n) for n in range(len(parent))});offset={};nv=0
for n in roots:
 if n in zero:continue
 d=len(frames[frame[n]]);offset[n]=nv;nv+=d*(d+1)//2
coords={}
for f in set(frame):
 B=frames[f];D={0:0}
 for j,b in enumerate(B):D.update({a^b:v^(1<<j) for a,v in tuple(D.items())})
 coords[f]=D
G={w['op']:w['G_columns'] for w in c['warps']}
def image(v,op):
 cols=G[abs(op)];y=0
 for i,col in enumerate(cols):
  if v>>i&1:y^=col
 return y
def form(n,a,b):
 n=find(n)
 if n in zero:return 0
 f=frame[n];u,v=coords[f][a],coords[f][b];d=len(frames[f]);q=0;idx=offset[n]
 for i in range(d):
  for j in range(i,d):
   bit=((u>>i)&1)*((v>>j)&1)
   if i!=j:bit^=((u>>j)&1)*((v>>i)&1)
   if bit:q^=1<<idx
   idx+=1
 return q
basis={};lowbasis={};eqs=0
def reduce(q):
 while q:
  k=q.bit_length()-1
  if k not in basis:return q
  q^=basis[k]
 return 0
def add(q):
 global eqs
 eqs+=1;z=q
 while z:
  k=(z&-z).bit_length()-1
  if k in lowbasis:z^=lowbasis[k]
  else:lowbasis[k]=z;break
 q=reduce(q)
 if q:basis[q.bit_length()-1]=q
def spacebasis(S):
 B=[];span={0}
 for a in sorted(S):
  if a not in span:B.append(a);span|={v^a for v in tuple(span)}
 return B
print('GRAPH',len(parent),len(roots),'VARIABLES',nv,flush=True)
for z,(kind,a,b,op) in enumerate(links):
 if kind=='paid':
  B=spacebasis(coords[frame[a]].keys()&coords[frame[b]].keys())
  for i,u in enumerate(B):
   for v in B[i:]:add(form(a,u,v)^form(b,u,v))
 else:
  if op<0:a,b=b,a
  B=frames[frame[a]]
  assert {image(u,op) for u in coords[frame[a]]}==set(coords[frame[b]])
  for i,u in enumerate(B):
   for v in B[i:]:add(form(a,u,v)^form(b,image(u,op),image(v,op)))
 if z%500==0:print('ELIM',z,len(basis),'seconds',time.monotonic()-t0,flush=True)
assert len(basis)==len(lowbasis)
queries=[]
for r in range(224,632):
 a,b=starts[r],ends[r];B=spacebasis(coords[frame[a]].keys()&coords[frame[b]].keys())
 for i,u in enumerate(B):
  for v in B[i:]:
   q=form(a,u,v)^form(b,u,v);rem=reduce(q)
   if rem:queries.append(dict(helper=r,pair=[u,v],free_bit=rem.bit_length()-1))
out=dict(status='EXACT_HOMOGENEOUS_PHASE_SCREEN',nodes=len(parent),merged_nodes=len(roots),variables=nv,equations=eqs,rank=len(basis),nullity=nv-len(basis),productive_queries=queries,seconds=time.monotonic()-t0,no_kappa_claim=True)
if '--check' in sys.argv:
 old=json.loads((HERE/'RESULT.json').read_text());assert {k:v for k,v in old.items() if k!='seconds'}=={k:v for k,v in out.items() if k!='seconds'}
else:(HERE/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print('RESULT',len(queries),'productive residuals',flush=True)
