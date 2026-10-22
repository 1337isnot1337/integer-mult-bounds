#!/usr/bin/env python3
from discover import *
from copy import deepcopy
sys.path.insert(0,str(ROOT/'research/helper-warp-joint'));from warp_merge import F,synthesize
spans=[F.span(b) for b in c['frames']];dims=list(map(len,c['frames']));before=[];current=c['start'][:]
for e in raw:
 before.append(current[:])
 if e[0]=='scalar':
  for r in rs(e):
   if r[0]=='L':current[r[1]]=e[2]
 elif e[0]=='warp':current[e[1][1]]=e[4]
def bill(seq,start,end,roles):
 cur={r:start[r] for r in roles};count=Counter()
 for g,f in seq:
  for role in g[1:3]:
   r=role[1];old=cur[r]
   if not spans[old]<=spans[f]:return None
   if dims[f]>dims[old]:count[dims[f]-dims[old]]+=1
   cur[r]=f
 for r in roles:
  if not spans[cur[r]]<=spans[end[r]]:return None
  if dims[end[r]]>dims[cur[r]]:count[dims[end[r]]-dims[cur[r]]]+=1
 return count
rows=[];best=None;t=1-.00302177585
for v in candidates:
 i,j,k=v['indices'];roles={r[1] for r in touch[i]|touch[j]};start=before[i];end={}
 for r in roles:
  nxt=next((z for z in range(k+1,len(raw)) if ('L',r) in touch[z]),None)
  end[r]=c['final'][r] if nxt is None else raw[nxt][3] if raw[nxt][0]=='warp' else raw[nxt][2]
 old=bill([(raw[z][1],raw[z][2]) for z in (i,j,k)],start,end,roles);assert old is not None
 def dom(g):return [f for f,s in enumerate(spans) if all(spans[start[r[1]]]<=s<=spans[end[r[1]]] for r in g[1:3])]
 moves=[v['middle'],v['correction']];domains=list(map(dom,moves));local=None;tested=0
 for order in [(0,1),(1,0)]:
  for a in domains[order[0]]:
   for b in domains[order[1]]:
    seq=[(moves[order[0]],a),(moves[order[1]],b)];new=bill(seq,start,end,roles)
    if new is None:continue
    tested+=1;delta={r:new[r]-old[r] for r in new.keys()|old.keys() if new[r]!=old[r]};assert sum(r*n for r,n in delta.items())==0
    gain=-sum(n*r**t for r,n in delta.items())
    if local is None or gain>local['gain']+1e-12:local=dict(gain=gain,delta=delta,sequence=seq)
 row=dict(indices=v['indices'],domains=list(map(len,domains)),tested=tested,best=local);rows.append(row)
 if local and (best is None or local['gain']>best['best']['gain']):best=row
 print(row,flush=True)
(HERE/'SCREEN.json').write_text(json.dumps(dict(status='DISCOVERY_ONLY',rows=rows,best=best),indent=2)+'\n')
if best and best['best']['gain']>1e-12:
 i,j,k=best['indices'];seq=best['best']['sequence'];words={}
 for d,p in x['programs'].items():
  pp=[deepcopy(e) for e in p if e[0]!='climb'];new=[]
  for z,e in enumerate(pp):
   if z==i:new.extend(['scalar',F.dual(g) if d=='backward' else g,f] for g,f in seq)
   if z not in (i,j,k):new.append(e)
  words[d]=synthesize(c,new)
 out=dict(canonical=c,programs=words)
 (HERE/'CANDIDATE-WORD.json.gz').write_bytes(gzip.compress(json.dumps(out,sort_keys=True,separators=(',',':')).encode(),mtime=0))
