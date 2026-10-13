"""Neighbourhood CP-SAT: switch call 5 from ck to jp8 and repack to a perfect (full-or-empty) owner map."""
import sys,random,json,gzip,copy
from load import *
from ortools.sat.python import cp_model
seed=int(sys.argv[1]);NFULL=int(sys.argv[2]);NEMPTY=int(sys.argv[3]);TL=float(sys.argv[4])
random.seed(seed)
W=P['windows']
def cap(o):return W[f'{o[0]},{o[1]}'][0]
def times(o):return set(W[f'{o[0]},{o[1]}'][1])
allown=[(int(k.split(',')[0]),int(k.split(',')[1]),p) for k in W for p in range(112)]
occ=defaultdict(list)
for r in rows: occ[(r['owner_replica'],r['child'],r['port'])].append(r)
ckw=reg['ck']['widths'];jw=reg['jp8']['widths']
# t=5 slots: match jp8 helpers to ck slots by width
t5=[r for r in rows if r['time']==5]
byw=defaultdict(list)
for h in range(492):byw[jw[h]].append(h)
keep=[];free7=[]
pool={w:list(v) for w,v in byw.items()}
for r in sorted(t5,key=lambda r:r['helper']):
    w=r['width']
    if pool[w] and not (w==7 and len(free7)<30 and False): keep.append((r,pool[w].pop()))
    else: free7.append(r)
newroles=[(5,h,jw[h]) for w,v in pool.items() for h in v]   # unplaced jp8 helpers
print('free slots',len(free7),Counter(r['width'] for r in free7),'new roles',Counter(w for _,_,w in newroles))
# pick free7 among the kept 7-slots? they are the ck 7s with no jp8 7 left (pool order). Neighbourhood:
O=set((r['owner_replica'],r['child'],r['port']) for r in free7)
O.add((1,8,111))
full=[o for o in allown if o in occ and o not in O]
emp=[o for o in allown if o not in occ and 5 in times(o)]
O|=set(random.sample(full,min(NFULL,len(full))))
O|=set(random.sample(emp,min(NEMPTY,len(emp))))
O=sorted(O)
freer=[]  # (time,helper,width,orig)
fixedrows=[]
f7=set(id(r) for r in free7)
t5map={id(r):h for r,h in keep}
for o,v in occ.items():
    for r in v:
        if id(r) in f7: continue
        h=t5map.get(id(r),r['helper'])
        if o in O: freer.append((r['time'],h,r['width']))
        else: fixedrows.append((r['time'],h,r['width'],o))
freer+=newroles
used=set((t,fam(*o)) for t,h,w,o in fixedrows)
print('owners',len(O),'free roles',len(freer),'freewidth',sum(w for _,_,w in freer),'cap',sum(cap(o) for o in O))
m=cp_model.CpModel()
x={}
for i,(t,h,w) in enumerate(freer):
    c=[]
    for j,o in enumerate(O):
        if t in times(o) and (t,fam(*o)) not in used and w<=cap(o):
            x[i,j]=m.NewBoolVar('');c.append(x[i,j])
    if not c: print('role has no owner',t,h,w);sys.exit(1)
    m.AddExactlyOne(c)
u=[m.NewBoolVar('') for o in O]
for j,o in enumerate(O):
    m.Add(sum(freer[i][2]*x[i,jj] for (i,jj) in x if jj==j)==cap(o)*u[j])
byfam=defaultdict(list)
for (i,j),v in x.items(): byfam[freer[i][0],fam(*O[j])].append(v)
for k,v in byfam.items():
    if len(v)>1:m.AddAtMostOne(v)
s=cp_model.CpSolver();s.parameters.max_time_in_seconds=TL;s.parameters.num_workers=10
st=s.Solve(m);print('status',s.StatusName(st))
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    assign=[(freer[i],O[j]) for (i,j),v in x.items() if s.Value(v)]
    out=[dict(time=t,helper=h,width=w,owner=list(o)) for (t,h,w),o in assign]+[dict(time=t,helper=h,width=w,owner=list(o)) for t,h,w,o in fixedrows]
    json.dump(out,open(f'sol-{seed}.json','w'))
    print('saved',len(out))
