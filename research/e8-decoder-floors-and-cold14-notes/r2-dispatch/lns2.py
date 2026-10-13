"""LNS: dispatch all-jp8 (call 5 ck->jp8); minimise #partial owners with CP-SAT neighbourhoods."""
import sys,random,json,gzip,pickle,os
from load import *
from ortools.sat.python import cp_model
seed=int(sys.argv[1]);ITERS=int(sys.argv[2]);NB=int(sys.argv[3]);TL=float(sys.argv[4]);ST=sys.argv[5]
random.seed(seed)
W=P['windows']
CAP={};TIM={}
allown=[]
for k,(c,ts) in W.items():
    o,ch=map(int,k.split(','))
    for p in range(112): allown.append((o,ch,p));CAP[o,ch,p]=c;TIM[o,ch,p]=set(ts)
FAM={o:fam(*o) for o in allown}
jw=reg['jp8']['widths']
if os.path.exists(ST):
    asg=pickle.load(open(ST,'rb'))
else:
    asg={}  # (t,h) -> owner
    byw=defaultdict(list)
    for h in range(492):byw[jw[h]].append(h)
    for r in sorted(rows,key=lambda r:(r['time'],r['helper'])):
        o=(r['owner_replica'],r['child'],r['port'])
        if r['time']!=5: asg[r['time'],r['helper']]=o
        elif byw[r['width']]: asg[5,byw[r['width']].pop()]=o
    for w,v in byw.items():
        for h in v: asg[5,h]=None
def width(role):return reg['jp8']['widths'][role[1]] if role[0]==5 else reg[P['provider_calls'][role[0]]['provider']]['widths'][role[1]]
def state():
    occ=defaultdict(list)
    for r,o in asg.items():
        if o is not None:occ[o].append(r)
    return occ
def score(occ):
    fill={o:sum(width(r) for r in v) for o,v in occ.items()}
    part=[o for o,f in fill.items() if f<CAP[o]]
    un=sum(1 for o in asg.values() if o is None)
    return un,part,fill
occ=state();un,part,fill=score(occ)
print('start unassigned',un,'partial',len(part),flush=True)
for it in range(ITERS):
    occ=state();un,part,fill=score(occ)
    # neighbourhood: partial owners + owners of unassigned-time + random others sharing times
    O=set(part)
    unr=[r for r,o in asg.items() if o is None]
    seedt={r[0] for r in unr}|{t for o in part for t in TIM[o]}
    cand=[o for o in allown if TIM[o]&seedt and o not in O]
    full=[o for o in cand if o in occ];emp=[o for o in cand if o not in occ]
    O|=set(random.sample(full,min(NB,len(full))))
    O|=set(random.sample(emp,min(NB//6,len(emp))))
    O=sorted(O);Oi={o:j for j,o in enumerate(O)}
    freer=[r for r,o in asg.items() if o is None or o in Oi]
    used=set((r[0],FAM[o]) for r,o in asg.items() if o is not None and o not in Oi)
    m=cp_model.CpModel();x={}
    byown=defaultdict(list);byfam=defaultdict(list)
    for i,r in enumerate(freer):
        c=[]
        for j,o in enumerate(O):
            if r[0] in TIM[o] and (r[0],FAM[o]) not in used and width(r)<=CAP[o]:
                v=m.NewBoolVar('');x[i,j]=v;c.append(v);byown[j].append((i,v));byfam[r[0],FAM[o]].append(v)
                if asg[r]==o:m.AddHint(v,1)
        m.AddExactlyOne(c)
    pen=[]
    for j,o in enumerate(O):
        s=sum(width(freer[i])*v for i,v in byown[j])
        f=m.NewBoolVar('');e=m.NewBoolVar('')
        m.Add(s<=CAP[o]);m.Add(s==CAP[o]).OnlyEnforceIf(f);m.Add(s==0).OnlyEnforceIf(e)
        p=m.NewBoolVar('');m.AddBoolOr([f,e,p]);pen.append(p)
    for k,v in byfam.items():
        if len(v)>1:m.AddAtMostOne(v)
    m.Minimize(sum(pen))
    s=cp_model.CpSolver();s.parameters.max_time_in_seconds=TL;s.parameters.num_workers=10
    st=s.Solve(m)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        new=dict(asg)
        for (i,j),v in x.items():
            if s.Value(v):new[freer[i]]=O[j]
        old=(un,len(part))
        asg_bak=asg;asg=new
        un2,part2,_=score(state())
        if (un2,len(part2))<=old: pickle.dump(asg,open(ST,'wb'))
        else: asg=asg_bak
        print(it,'owners',len(O),'roles',len(freer),s.StatusName(st),'obj',s.ObjectiveValue(),'->',un2,len(part2),flush=True)
    else: print(it,s.StatusName(st),flush=True)
occ=state();un,part,fill=score(occ)
print('final',un,len(part),sorted(Counter(CAP[o]-fill[o] for o in part).items()))
