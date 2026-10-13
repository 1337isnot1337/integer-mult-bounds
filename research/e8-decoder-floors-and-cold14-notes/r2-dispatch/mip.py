"""free-dispatch exact-window pattern MIP over {jp8(u4), st2, ck}; >=MINALT non-jp8 calls; Hall masks; V639 values."""
import json,sys,time,pickle
import numpy as np
from collections import Counter,defaultdict
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix
from load import P,reg
V={int(k):v for k,v in json.load(open('V639.json')).items()};V[0]=0.0
st2=json.load(open('st2-PLAN.json'))['provider_registry']['jp8']
REG={'jp8':reg['jp8'],'ck':reg['ck'],'st2':st2}
provs=sys.argv[1].split(',');TIGHT=int(sys.argv[2]);SECS=float(sys.argv[3]);OUT=sys.argv[4];MINALT=int(sys.argv[5]);LPONLY=len(sys.argv)>6 and sys.argv[6]=='lp'
# check sibling families have disjoint times
fams=defaultdict(list)
for k,(c,ts) in P['windows'].items():
    o,ch=map(int,k.split(','));fams[o,P['pairs'][str(ch)],P['sides'][str(ch)]].append(set(ts))
for f,L in fams.items():
    for i in range(len(L)):
        for j in range(i):assert not L[i]&L[j],f
inv={p:Counter(REG[p]['widths']) for p in provs}
val={p:sum(V[int(r)]*c for r,c in REG[p]['actual_paid_profile'].items()) for p in provs}
print('vals',{p:val[p]-val['jp8'] for p in provs})
WID=[4,5,7,8,9]
def pats(cap,L):
    out=[]
    def rec(pre,i,tot):
        r=cap-tot
        if cap<48 or r<=TIGHT or r==48: out.append(tuple(pre))
        for j in range(i,len(WID)):
            w=WID[j]
            if tot+w<=cap and len(pre)<L: rec(pre+[w],j,tot+w)
    rec([],0,0);return out
ub=[];cost=[];R=[];lo=[];hi=[]
def var(c,u=np.inf):ub.append(u);cost.append(-c);return len(ub)-1
def con(row,l,h):R.append(row);lo.append(l);hi.append(h)
sel={(t,p):var(val[p],1) for t in range(72) for p in provs}
for t in range(72):con({sel[t,p]:1 for p in provs},1,1)
con({sel[t,p]:1 for t in range(72) for p in provs if p!='jp8'},MINALT,np.inf)
groups={};invrow=defaultdict(dict)
for key,(cap,times) in P['windows'].items():
    ps=pats(cap,len(times));cnts=[Counter(q) for q in ps]
    pv=[var(V[cap-sum(q)],112) for q in ps]
    con({i:1 for i in pv},112,112)
    fl={}
    for t in times:
        for w in WID:
            if not any(c[w] for c in cnts):continue
            i=var(0,112);fl[t,w]=i;invrow[t,w][i]=1
        seen=set()
        for mask in range(1,32):
            cols={w for b,w in enumerate(WID) if mask>>b&1}
            req=tuple(i for (tt,w),i in fl.items() if tt==t and w in cols)
            pres=tuple(j for j,c in zip(pv,cnts) if any(c[w] for w in cols))
            if req and (req,pres) not in seen:
                seen.add((req,pres));row={i:1 for i in req}
                for j in pres:row[j]=row.get(j,0)-1
                con(row,-np.inf,0)
    for w in WID:
        row={i:1 for (t,ww),i in fl.items() if ww==w}
        for j,c in zip(pv,cnts):
            if c[w]:row[j]=row.get(j,0)-c[w]
        if row:con(row,0,0)
    groups[key]=dict(cap=cap,times=times,ps=ps,pv=pv,fl=fl)
for t in range(72):
    for w in WID:
        row=dict(invrow[t,w])
        for p in provs:
            if inv[p][w]:row[sel[t,p]]=-inv[p][w]
        con(row,0,0)
rr,cc,vv=[],[],[]
for i,row in enumerate(R):
    for j,x in row.items():rr.append(i);cc.append(j);vv.append(x)
A=coo_matrix((vv,(rr,cc)),shape=(len(R),len(ub))).tocsr()
print('vars',len(ub),'cons',len(R),flush=True)
base=71*val['jp8']+val['ck']+V[36]+2229*V[48] if 'ck' in provs else None
t0=time.time()
res=milp(np.array(cost),integrality=np.zeros(len(ub)) if LPONLY else np.ones(len(ub)),bounds=Bounds(np.zeros(len(ub)),np.array(ub)),constraints=LinearConstraint(A,lo,hi),options={'time_limit':SECS,'mip_rel_gap':1e-12,'disp':False})
print(res.status,res.message,'obj',-res.fun if res.x is not None else None,'base639',base,'gain(1e-9b)',(-res.fun-base) if res.x is not None and base else None,'secs',time.time()-t0,flush=True)
if res.x is None:sys.exit()
if LPONLY:
    d=Counter()
    for (t,p),i in sel.items():d[p]+=res.x[i]
    print('lp dispatch',dict(d));sys.exit()
x=np.round(res.x).astype(int)
disp={t:p for (t,p),i in sel.items() if x[i]}
rem=Counter()
for key,g in groups.items():
    for q,i in zip(g['ps'],g['pv']):
        if x[i] and g['cap']-sum(q):rem[g['cap']-sum(q)]+=x[i]
print('dispatch',Counter(disp.values()),{t:p for t,p in disp.items() if p!='jp8'},'remainders',dict(rem))
pickle.dump(dict(groups=groups,x=x,disp=disp,REG=REG),open(OUT+'.pkl','wb'))
