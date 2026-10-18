"""Bounded new interior conjugation on the actual staged providers."""
import copy,gzip,json,sys
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).parent/'sources'))
import frames as F
P=Path(__file__).parent

def simplify(gs):
 out=[]
 for g in gs:
  if g[0]=='add':
   d,s=g[1:3]
   for j in range(len(out)-1,-1,-1):
    h=out[j]
    if h[0]!='add':
     if h[0]=='native' or h[1] in (d,s):break
     continue
    if h[1:3]==[d,s]:
     q=Q(g[3],g[4])+Q(h[3],h[4]);out.pop(j)
     if q: g=['add',d,s,q.numerator,q.denominator,[]]
     else:g=None
     break
    if s==h[1] or d==h[2]:break
  if g is not None:out.append(g)
 return out

def trial(w,h,d,q,start,stop):
 x=copy.deepcopy(w);g=x['B'][start]
 assert g[:5]==['add',d,h,q,1]
 # old state = E_dh(q) new state throughout the changed interval.
 # No reads of d or writes of d from h, nor native operators on h/d allowed.
 at={}
 for rec in w['warps']:at.setdefault(rec[0],[]).append(rec)
 middle=[]
 for i in range(start+1,stop):
  assert all(r[1] not in (d,h) for r in at.get(i,[]))
  middle += [['native',copy.deepcopy(r)] for r in at.get(i,[])]
  g=w['B'][i]
  assert not (g[0]=='add' and g[2]==d)
  assert not (g[0]=='scale' and g[1] in (d,h))
  middle.append(copy.deepcopy(g))
  if g[0]=='add' and g[1]==h:
   c=-q*Q(g[3],g[4]);middle.append(['add',d,g[2],c.numerator,c.denominator,[]])
 middle=simplify(middle)
 events=[]
 for i in range(start):
  events += [['native',copy.deepcopy(r)] for r in at.get(i,[])]
  events.append(copy.deepcopy(w['B'][i]))
 events += [['native',copy.deepcopy(r)] for r in at.get(start,[])]
 events += middle+[['add',d,h,q,1,[]]]
 for i in range(stop,len(w['B'])+1):
  events += [['native',copy.deepcopy(r)] for r in at.get(i,[])]
  if i<len(w['B']):events.append(copy.deepcopy(w['B'][i]))
 x['B']=[];x['warps']=[]
 for g in events:
  if g[0]=='native':
   rec=g[1];rec[0]=len(x['B']);x['warps'].append(rec)
  else:x['B'].append(g)
 graph=F.build(x);lo,up,bad=F.bounds(graph)
 result=dict(h=h,donor=d,start=start,stop=stop,scalar_delta=len(x['B'])-len(w['B']),frame_conflicts=len(bad))
 if bad:result['witness']=F.witness(graph,lo,up,bad)
 else:
  for (sec,i),b in zip(graph['labels'],lo):x[sec][i][-1]=list(b)
  result['frame_feasible']=True
 return result

def main():
 rows=[]
 for provider in ('base','extra'):
  w=json.load(gzip.open(P/'sources'/f'STAGED644-660-{provider}.json.gz'))
  for h,d,q in [(644,640,2),(660,656,-1)]:
   start=next(i for i,g in enumerate(w['B']) if g[:5]==['add',d,h,q,1])
   first=next(i for i in range(start+1,len(w['B'])) if w['B'][i][0]=='add' and w['B'][i][2]==d)
   stops=[i for i in range(start+1,first+1) if i==first or (w['B'][i][0]=='add' and h in w['B'][i][1:3])]
   for stop in stops:
    r=trial(w,h,d,q,start,stop)
    rows.append(dict(provider=provider,**r) if r else dict(provider=provider,h=h,stop=stop,unsupported_disjoint_warp_move=True))
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
