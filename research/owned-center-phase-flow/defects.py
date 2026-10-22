"""Exact single-paid-edge phase-defect screen; no numerical admission."""
import search as S
from collections import defaultdict
from pathlib import Path
import json,time
beg=time.monotonic();elim={};rows=[];selected=defaultdict(list);nv=0
def add(q,group):
 global nv
 original=q;rep=0
 while q:
  k=q.bit_length()-1
  if k in elim:r,w=elim[k];q^=r;rep^=w
  else:
   bit=1<<nv;selected[group].append(nv);nv+=1
   elim[k]=(q,rep^bit);rep=bit;break
 rows.append((group,rep))
def represent(q):
 rep=0
 while q:
  r,w=elim[q.bit_length()-1];q^=r;rep^=w
 return rep
for group,(kind,a,b,op) in enumerate(S.links):
 if kind=='paid':
  B=S.spacebasis(S.coords[S.frame[a]].keys()&S.coords[S.frame[b]].keys())
  for i,u in enumerate(B):
   for v in B[i:]:add(S.form(a,u,v)^S.form(b,u,v),group)
 else:
  if op<0:a,b=b,a
  B=S.frames[S.frame[a]]
  for i,u in enumerate(B):
   for v in B[i:]:add(S.form(a,u,v)^S.form(b,S.image(u,op),S.image(v,op)),group)
assert nv==S.nv
queries=[]
for r in range(224,632):
 a,b=S.starts[r],S.ends[r];B=S.spacebasis(S.coords[S.frame[a]].keys()&S.coords[S.frame[b]].keys())
 for i,u in enumerate(B):
  for v in B[i:]:queries.append((r,represent(S.form(a,u,v)^S.form(b,u,v))))
results=[];hits=[]
for group,indices in selected.items():
 if S.links[group][0]!='paid':continue
 mask=sum(1<<i for i in indices);E={}
 for g,rep in rows:
  if g==group:continue
  z=rep&mask
  while z:
   k=z.bit_length()-1
   if k in E:z^=E[k]
   else:E[k]=z;break
  if len(E)==len(indices):break
 null=len(indices)-len(E)
 if null:
  helpful=set();witnesses=[]
  for free in set(indices)-set(E):
   y=1<<free
   for k,row in sorted(E.items()):
    if (row&y).bit_count()%2:y^=1<<k
   affected=sorted({r for r,q in queries if (q&y).bit_count()%2})
   helpful.update(affected)
   if affected:witnesses.append(dict(free=free,helpers=affected))
  results.append(dict(edge=group,nullity=null,helpers=sorted(helpful)))
  if helpful:hits.append(dict(edge=group,witnesses=witnesses))
 if group%250==0:print('DEFECT',group,'nonzero',len(results),'productive',len(hits),'seconds',time.monotonic()-beg,flush=True)
out=dict(status='EXACT_SINGLE_PAID_EDGE_DEFECT_SCREEN',variables=nv,total_edges=len(S.links),groups_with_basis_rows=len(selected),nonzero_defects=results,productive_defects=hits,seconds=time.monotonic()-beg,no_kappa_claim=True)
S.HERE.joinpath('DEFECTS.json').write_text(json.dumps(out,indent=2)+'\n');print('DEFECT_RESULT',len(results),len(hits),flush=True)
