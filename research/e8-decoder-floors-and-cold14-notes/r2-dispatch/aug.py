"""Exchange-chain repair: switch call T to a new jp8-family word; place it in the ck slots by width; then fill the
partial owner Z by moving roles in, and route all unit excesses to deficits by same-time width-(w,w-1) swaps (BFS)."""
import sys,json,pickle,random
from collections import deque
from load import *
T=int(sys.argv[1]);NEWW=json.load(open(sys.argv[2])) if sys.argv[2]!='-' else reg['jp8']['widths'];OUT=sys.argv[3]
EXTRA4=int(sys.argv[4]) if len(sys.argv)>4 else 0   # owners that must end with exactly 4 used (one 4-role)
random.seed(int(sys.argv[5]) if len(sys.argv)>5 else 0)
W=P['windows'];CAP={};TIM={}
for k,(c,ts) in W.items():
    a,b=map(int,k.split(','))
    for p in range(112):CAP[a,b,p]=c;TIM[a,b,p]=set(ts)
calls=[c['provider'] for c in P['provider_calls']]
def wid(t,h):return NEWW[h] if t==T else reg[calls[t]]['widths'][h]
own={}   # (t,h)->owner
oldw=reg[calls[T]]['widths']
pool=defaultdict(list)
for h in range(492):pool[NEWW[h]].append(h)
pend=[]
for r in sorted(rows,key=lambda r:(r['time'],r['helper'])):
    o=(r['owner_replica'],r['child'],r['port'])
    if r['time']!=T:own[r['time'],r['helper']]=o
    elif pool[r['width']]:own[T,pool[r['width']].pop()]=o
    else:pend.append((o,r['width']))
newroles=[(T,h) for w,v in pool.items() for h in v]
# pair the leftover old slots with new roles (widths bigger): greedy by sorting
pend.sort(key=lambda x:x[1]);newroles.sort(key=lambda r:NEWW[r[1]])
assert len(pend)==len(newroles)
for (o,w),r in zip(pend,newroles):own[r]=o
at=defaultdict(dict)
for r,o in own.items():at[o][r[0]]=r
fill={o:sum(wid(*r) for r in d.values()) for o,d in at.items()}
exc={o:fill[o]-CAP[o] for o in fill if fill[o]>CAP[o]}
print('excess',sum(exc.values()),len(exc))
# partial owners
part=[o for o in CAP if 0<fill.get(o,0)<CAP[o]]
print('partial',[(o,fill[o]) for o in part])
Z=part[0]
need=CAP[Z]-fill[Z]
# choose donors: roles at times allowed in Z (free times), greedy: 9s from distinct times, from owners not in exc
free=[t for t in TIM[Z] if t not in at[Z]]
random.shuffle(free)
byt=defaultdict(list)
for r,o in own.items():byt[r[0]].append(r)
def move(r,dst):
    src=own[r];del at[src][r[0]];fill[src]-=wid(*r);own[r]=dst;at[dst][r[0]]=r;fill[dst]=fill.get(dst,0)+wid(*r)
deficit={}
rem=need-sum(exc.values())+EXTRA4*0   # not used
# fill Z exactly with need units using donors' roles
tot=0;ts=iter(free)
plan=[]
while tot<need:
    t=next(ts);left=need-tot
    cands=[r for r in byt[t] if own[r]!=Z and wid(*r)<=left and CAP[own[r]]==48 and own[r] not in exc]
    if not cands:continue
    # prefer 9s unless remainder small
    cands.sort(key=lambda r:-wid(*r))
    r=cands[0] if left>=9 or any(wid(*c)==left for c in cands)==False else next(c for c in cands if wid(*c)==left)
    plan.append(r);tot+=wid(*r)
for r in plan:
    d=own[r];move(r,Z)
print('Z filled',fill[Z],CAP[Z])
# extra 4-owners: move a 4-role into an empty 48 owner
empties=[o for o in CAP if CAP[o]==48 and fill.get(o,0)==0]
for k in range(EXTRA4):
    for _ in range(10000):
        r=random.choice([r for r,o in own.items() if wid(*r)==4])
        e=[o for o in empties if r[0] in TIM[o]]
        if e:move(r,e[0]);empties.remove(e[0]);break
bal={o:fill.get(o,0)-CAP[o] for o in at if at[o]}
# owners that must be exactly 4 used are not CAP-balanced: treat target fill
target={o:(4 if fill.get(o,0)==4 and CAP[o]==48 and len(at[o])==1 else CAP[o]) for o in at if at[o]}
bal={o:fill[o]-target[o] for o in target}
src=[o for o,b in bal.items() if b>0];snk={o for o,b in bal.items() if b<0}
print('sources',sum(bal[o] for o in src),'sinks',-sum(bal[o] for o in snk))
idx=defaultdict(list)   # (t,width)->roles
for r in own:idx[r[0],wid(*r)].append(r)
def bfs(s):
    prev={s:None};q=deque([s])
    while q:
        x=q.popleft()
        rs=list(at[x].values());random.shuffle(rs)
        for r in rs:
            w=wid(*r)
            for y in idx.get((r[0],w-1),()):
                Y=own[y]
                if Y in prev:continue
                prev[Y]=(x,r,y)
                if Y in snk and bal[Y]<0:return Y,prev
                q.append(Y)
    return None,prev
def swap(r,y):
    X,Y=own[r],own[y];t=r[0]
    own[r],own[y]=Y,X;at[X][t]=y;at[Y][t]=r
    fill[X]+=wid(*y)-wid(*r);fill[Y]+=wid(*r)-wid(*y)
npath=0
while any(bal[o]>0 for o in src):
    s=next(o for o in src if bal[o]>0)
    Y,prev=bfs(s)
    if Y is None:print('stuck at',s);break
    path=[];cur=Y
    while prev[cur] is not None:x,r,y=prev[cur];path.append((r,y));cur=x
    for r,y in reversed(path):swap(r,y)
    bal[s]-=1;bal[Y]+=1;npath+=1
print('paths',npath,'remaining',sum(b for b in bal.values() if b>0))
assert all(fill[o]<=CAP[o] for o in fill)
pickle.dump({r:o for r,o in own.items()},open(OUT,'wb'))
