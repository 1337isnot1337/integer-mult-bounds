#!/usr/bin/env python3
"""Exact ADD conjugation across blocks, with full fixed-map frame pricing."""
from discover import *
from copy import deepcopy
sys.path.insert(0,str(ROOT/'research/helper-warp-joint'));from warp_merge import F,synthesize
spans=[F.span(b) for b in c['frames']];dims=list(map(len,c['frames']));old=Counter(e[-1] for e in x['programs']['forward'] if e[0] in ('climb','center'));t=1-.00302177585
last={};patterns=[]
for k,e in enumerate(raw):
 if not add(e):continue
 g=e[1];key=tuple(g[1]),tuple(g[2]);u=Q(g[3],g[4]);prior=last.get(key);last[key]=(k,u)
 if prior is None or prior[1]!=-u:continue
 i=prior[0];target,source=key;corrections={};valid=True
 for j in range(i+1,k):
  if not touch[j]&set(key):continue
  b=raw[j]
  if not add(b):valid=False;break
  bg=b[1];dst,src=map(tuple,bg[1:3]);v=Q(bg[3],bg[4])
  if src==target and dst==source:valid=False;break
  if src==target and dst!=source:d,s,co=dst,source,-u*v
  elif dst==source and src!=target:d,s,co=target,src,u*v
  else:continue
  corrections[j]=['scalar',['add',list(d),list(s),co.numerator,co.denominator],b[2]]
  if len(corrections)>8:valid=False;break
 if valid and corrections:patterns.append((i,k,corrections))
print('WINDOW_PATTERNS',len(patterns),flush=True)
def price(i,k,corr,emit=False):
 current=c['start'][:];prof=Counter();word=[]
 def climb(r,f):
  a=current[r]
  if not spans[a]<=spans[f]:return False
  if dims[f]>dims[a]:prof[dims[f]-dims[a]]+=1
  current[r]=f;return True
 for z,e in enumerate(raw):
  if z in (i,k):continue
  seq=[e]+([corr[z]] if z in corr else [])
  for ee in seq:
   if ee[0]=='scalar':
    for role in rs(ee):
     if role[0]=='L' and not climb(role[1],ee[2]):return None
   elif ee[0]=='warp':
    if not climb(ee[1][1],ee[3]):return None
    current[ee[1][1]]=ee[4]
   elif ee[0]=='center':prof[ee[-1]]+=1
   if emit:word.append(ee)
 for r,f in enumerate(c['final']):
  if not climb(r,f):return None
 return (prof,word)
results=[];best=None
for i,k,corr in patterns:
 out=price(i,k,corr)
 if out is None:results.append(dict(first=i,last=k,corrections=len(corr),status='INFEASIBLE_FIXED_FRAME_CONTACT'));continue
 prof,_=out;delta={r:prof[r]-old[r] for r in prof.keys()|old.keys() if prof[r]!=old[r]};assert sum(r*n for r,n in delta.items())==0
 gain=-sum(n*r**t for r,n in delta.items());row=dict(first=i,last=k,corrections=len(corr),gain=gain,delta=delta,status='PROFILE_SCREEN');results.append(row)
 if best is None or gain>best[0]:best=(gain,i,k,corr)
print('VALID',sum(r['status']=='PROFILE_SCREEN' for r in results),'BEST',best[:3] if best else None,flush=True)
(HERE/'WINDOWS.json').write_text(json.dumps(dict(status='DISCOVERY_ONLY',results=results),indent=2)+'\n')
if best and best[0]>1e-10:
 gain,i,k,corr=best;prof,word=price(i,k,corr,True);words={'forward':synthesize(c,word)}
 # Rebuild opposite orientation from its unchanged baseline and exact dual insertions.
 pp=[deepcopy(e) for e in x['programs']['backward'] if e[0]!='climb'];out=[]
 for z,e in enumerate(pp):
  if z in (i,k):continue
  out.append(e)
  if z in corr:out.append(['scalar',F.dual(corr[z][1]),corr[z][2]])
 words['backward']=synthesize(c,out)
 (HERE/'WINDOW-CANDIDATE.json.gz').write_bytes(gzip.compress(json.dumps(dict(canonical=c,programs=words),sort_keys=True,separators=(',',':')).encode(),mtime=0));print('POSITIVE_UNVERIFIED',gain,prof)
