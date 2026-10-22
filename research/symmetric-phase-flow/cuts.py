"""Bounded rank-one paid phase-flow discovery; credits PR4654 PHASE-CUT."""
import search as S
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from collections import defaultdict,deque
import json,time
R=S.roots;idx={r:i for i,r in enumerate(R)};N=len(R);source=N;sink=N+1;t=1-.003021775870775;scale=1000000
power=lambda r:r**t if r else 0.
rows=[];best=None;beg=time.monotonic()
def active(l,B):return any((l&v).bit_count()%2 for v in B)
for mode in ['entrance_fixed','exit_fixed']:
 fixed=set(S.zero)|{S.find(n) for n in (S.starts[224:] if mode=='entrance_fixed' else S.ends[224:])}
 for l in range(1,512):
  unary=defaultdict(float);pair=defaultdict(float);terms=[];rewards=[]
  for kind,a,b,op in S.links:
   ra,rb=S.find(a),S.find(b);U=S.frames[S.frame[a]];V=S.frames[S.frame[b]]
   if kind=='paid':
    I=S.spacebasis(S.coords[S.frame[a]].keys()&S.coords[S.frame[b]].keys());r=len(U)+len(V)-2*len(I)
    w=power(r+1)-power(r) if active(l,I) else 0.;c10=c01=w;c11=0.
   else:
    if op<0:a,b=b,a;ra,rb=rb,ra;U,V=V,U
    aa=tuple((l&u).bit_count()%2 for u in U);bb=tuple((l&S.image(u,op)).bit_count()%2 for u in U)
    ar=int(any(aa));br=int(any(bb));cr=0 if aa==bb else ar+br
    c10=power(ar);c01=power(br);c11=power(cr)
   terms.append((ra,rb,c10,c01,c11))
   if ra==rb:unary[ra]+=c11;continue
   C=max(0.,(c10+c01-c11)/2);unary[ra]+=c10-C;unary[rb]+=c01-C;pair[min(ra,rb),max(ra,rb)]+=C
  for r in range(224,632):
   a,b=S.starts[r],S.ends[r];I=S.spacebasis(S.coords[S.frame[a]].keys()&S.coords[S.frame[b]].keys());g=len(S.frames[S.frame[b]])-len(S.frames[S.frame[a]])
   n=S.find(b if mode=='entrance_fixed' else a);reward=power(g+1)-power(g) if active(l,I) else 0.;unary[n]-=reward;rewards.append((n,reward))
  cap=defaultdict(int)
  for (a,b),w in pair.items():
   k=round(w*scale)
   if k:cap[idx[a],idx[b]]+=k;cap[idx[b],idx[a]]+=k
  for n,u in unary.items():
   k=round(abs(u)*scale)
   if k:cap[(idx[n],sink) if u>=0 else (source,idx[n])]+=k
  for n in fixed:cap[idx[n],sink]+=1000000000
  ar=np.array(list(cap));data=np.array(list(cap.values()),dtype=np.int64);C=csr_matrix((data,(ar[:,0],ar[:,1])),shape=(N+2,N+2));flow=maximum_flow(C,source,sink);res=C-flow.flow
  seen={source};q=deque([source])
  while q:
   a=q.popleft()
   for j in range(res.indptr[a],res.indptr[a+1]):
    b=int(res.indices[j])
    if res.data[j]>0 and b not in seen:seen.add(b);q.append(b)
  chosen={r for r in R if idx[r] in seen};assert not chosen&fixed
  cost=sum(c11 if a in chosen and b in chosen else c10 if a in chosen else c01 if b in chosen else 0. for a,b,c10,c01,c11 in terms)-sum(w for n,w in rewards if n in chosen)
  row=dict(mode=mode,functional=l,energy=cost,selected=len(chosen));rows.append(row)
  if best is None or cost<best['energy']:best=dict(row,chosen=sorted(chosen))
  if l%64==0:print('CUTS',mode,l,'best',best['energy'],'seconds',time.monotonic()-beg,flush=True)
S.HERE.joinpath('CUTS.json').write_text(json.dumps(dict(status='BOUNDED_APPROXIMATE_MINCUT_DISCOVERY',scale=scale,exponent=t,rows=rows,best=best,seconds=time.monotonic()-beg,no_kappa_claim=True),indent=2)+'\n')
print('BEST',best,flush=True)
