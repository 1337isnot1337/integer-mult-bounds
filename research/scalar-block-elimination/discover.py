#!/usr/bin/env python3
"""Exact acyclic scalar-block elimination, preserving native contact frames."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
from copy import deepcopy
import json,gzip,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/helper-warp-joint'));from warp_merge import F,synthesize
x=json.loads(gzip.decompress((ROOT/'research/helper-warp-joint/ACTUAL-WORD.json.gz').read_bytes()));c=x['canonical'];p=[e for e in x['programs']['forward'] if e[0]!='climb'];dims=list(map(len,c['frames']));oldpaid=Counter(e[-1] for e in x['programs']['forward'] if e[0] in ('climb','center'));t=1-.00302177585

def eligible(e):return e[0]=='scalar' and e[1][0] in ('add','scale') and all(r[0]=='L' for r in (e[1][1:3] if e[1][0]=='add' else e[1][1:2]))
def roles(e):return [r[1] for r in (e[1][1:3] if e[1][0]=='add' else e[1][1:2])]
def unit(q):return q!=0 and abs(q.numerator)&(abs(q.numerator)-1)==0 and q.denominator&(q.denominator-1)==0
blocks=[];i=0
while i<len(p):
 if not eligible(p[i]):i+=1;continue
 j=i+1
 while j<len(p) and eligible(p[j]) and p[j][2]==p[i][2]:j+=1
 if j-i>=2 and 0<dims[p[i][2]]<9:blocks.append((i,j))
 i=j
records=[];best=None
for i,j in blocks:
 frame=p[i][2];rs=sorted({r for e in p[i:j] for r in roles(e)});M={r:{r:Q(1)} for r in rs}
 for e in p[i:j]:
  g=e[1];r=g[1][1]
  if g[0]=='scale':q=Q(g[2],g[3]);M[r]={s:a*q for s,a in M[r].items() if a*q}
  else:
   source=g[2][1];q=Q(g[3],g[4])
   for s,a in M[source].items():
    M[r][s]=M[r].get(s,Q(0))+q*a
    if not M[r][s]:del M[r][s]
 if not all(unit(M[r].get(r,Q(0))) for r in rs):continue
 edges={r:{s for s in M[r] if s!=r} for r in rs};incoming=Counter(s for r in rs for s in edges[r]);queue=[r for r in rs if not incoming[r]];order=[]
 while queue:
  r=queue.pop();order.append(r)
  for s in sorted(edges[r]):
   incoming[s]-=1
   if not incoming[s]:queue.append(s)
 if len(order)!=len(rs):continue
 new=[]
 for r in order:
  a=M[r][r]
  if a!=1:new.append(['scalar',['scale',['L',r],a.numerator,a.denominator],frame])
  for s,a in sorted(M[r].items()):
   if s!=r:new.append(['scalar',['add',['L',r],['L',s],a.numerator,a.denominator],frame])
 used={r for e in new for r in roles(e)};removed=set(rs)-used
 if not removed or len(new)>2*(j-i):continue
 altered=p[:i]+new+p[j:];pp=synthesize(c,altered);paid=Counter(e[-1] for e in pp if e[0] in ('climb','center'));delta={r:paid[r]-oldpaid[r] for r in paid.keys()|oldpaid.keys() if paid[r]!=oldpaid[r]};gain=-sum(n*r**t for r,n in delta.items());assert sum(r*n for r,n in delta.items())==0
 rec=dict(first=i,last_exclusive=j,frame=frame,dimension=dims[frame],old_gates=j-i,new_gates=len(new),removed_roles=sorted(removed),delta=delta,gain=gain,replacement=new);records.append(rec)
 if best is None or gain>best['gain']:best=rec
 print('REWRITE',i,j,'removed',len(removed),'gain',gain,flush=True)
(HERE/'RESULT.json').write_text(json.dumps(dict(status='DISCOVERY_ONLY',blocks_screened=len(blocks),candidates=records,best=best),indent=2)+'\n');print('DONE',len(blocks),len(records),'best gain',None if best is None else best['gain'])
if best and best['gain']>1e-10:
 i,j=best['first'],best['last_exclusive'];words={}
 for d,word in x['programs'].items():
  raw=[deepcopy(e) for e in word if e[0]!='climb'];replacement=deepcopy(best['replacement'])
  if d=='backward':
   for e in replacement:e[1]=F.dual(e[1])
  words[d]=synthesize(c,raw[:i]+replacement+raw[j:])
 (HERE/'CANDIDATE-WORD.json.gz').write_bytes(gzip.compress(json.dumps(dict(canonical=c,programs=words),sort_keys=True,separators=(',',':')).encode(),mtime=0));print('POSITIVE_UNVERIFIED_NATIVE')
