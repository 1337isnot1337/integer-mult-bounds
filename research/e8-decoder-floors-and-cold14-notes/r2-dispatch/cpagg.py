"""Aggregate exact-window pattern model (Hall masks) in CP-SAT with free dispatch over provs, >=MINALT non-jp8,
hinted with PR639's literal map. Objective: maximize sum of mass-neutral V (1e-9 b, scaled x1000)."""
import json,sys,time,pickle,gzip
from collections import Counter,defaultdict
from ortools.sat.python import cp_model
from load import P,reg,rows
V={int(k):v for k,v in json.load(open('V639.json')).items()};V[0]=0.0
st2=json.load(open('st2-PLAN.json'))['provider_registry']['jp8']
REG={'jp8':reg['jp8'],'ck':reg['ck'],'st2':st2}
provs=sys.argv[1].split(',');TIGHT=int(sys.argv[2]);SECS=float(sys.argv[3]);OUT=sys.argv[4];MINALT=int(sys.argv[5])
FIX=json.loads(sys.argv[6]) if len(sys.argv)>6 else {}   # {time:provider}
SC=1000
inv={p:Counter(REG[p]['widths']) for p in provs}
val={p:sum(V[int(r)]*c for r,c in REG[p]['actual_paid_profile'].items()) for p in provs}
WID=[4,5,7,8,9]
# hint from PR639
own=defaultdict(list)
for r in rows:own[r['owner_replica'],r['child'],r['port']].append((r['time'],r['width']))
hpat=defaultdict(Counter);hflow=defaultdict(Counter)
for k in P['windows']:
    a,b=map(int,k.split(','))
    for p in range(112):
        L=own.get((a,b,p),[]);hpat[k][tuple(sorted(w for _,w in L))]+=1
        for t,w in L:hflow[k][t,w]+=1
def pats(cap,L,extra):
    out=set()
    def rec(pre,i,tot):
        r=cap-tot
        if r==0 or r<=TIGHT or r==cap: out.add(tuple(pre))
        for j in range(i,len(WID)):
            w=WID[j]
            if tot+w<=cap and len(pre)<L: rec(pre+[w],j,tot+w)
    rec([],0,0);return sorted(out|set(extra))
m=cp_model.CpModel();obj=[]
sel={}
for t in range(72):
    for p in provs:
        v=m.NewBoolVar('');sel[t,p]=v;obj.append(int(round(val[p]*SC))*v)
        m.AddHint(v,1 if P['provider_calls'][t]['provider']==p else 0)
        if str(t) in FIX: m.Add(v==(1 if FIX[str(t)]==p else 0))
    m.AddExactlyOne([sel[t,p] for p in provs])
m.Add(sum(sel[t,p] for t in range(72) for p in provs if p!='jp8')>=MINALT)
invrow=defaultdict(list);groups={}
for key,(cap,times) in P['windows'].items():
    ps=pats(cap,len(times),list(hpat[key]));cnts=[Counter(q) for q in ps]
    pv=[]
    for q in ps:
        v=m.NewIntVar(0,112,'');pv.append(v);obj.append(int(round(V[cap-sum(q)]*SC))*v);m.AddHint(v,hpat[key][q])
    m.Add(sum(pv)==112)
    fl={}
    for t in times:
        for w in WID:
            if not any(c[w] for c in cnts):continue
            v=m.NewIntVar(0,112,'');fl[t,w]=v;invrow[t,w].append(v);m.AddHint(v,hflow[key][t,w])
        seen=set()
        for mask in range(1,32):
            cols={w for b,w in enumerate(WID) if mask>>b&1}
            req=tuple((t,w) for (tt,w) in fl if tt==t and w in cols)
            pres=tuple(j for j,c in enumerate(cnts) if any(c[w] for w in cols))
            if req and (req,pres) not in seen:
                seen.add((req,pres));m.Add(sum(fl[k] for k in req)<=sum(pv[j] for j in pres))
    for w in WID:
        fs=[v for (t,ww),v in fl.items() if ww==w]
        m.Add(sum(fs)==sum(c[w]*pv[j] for j,c in enumerate(cnts) if c[w]))
    groups[key]=dict(cap=cap,times=times,ps=ps,pv=pv,fl=fl)
for t in range(72):
    for w in WID:
        m.Add(sum(invrow[t,w])==sum(inv[p][w]*sel[t,p] for p in provs))
m.Maximize(sum(obj))
s=cp_model.CpSolver();s.parameters.max_time_in_seconds=SECS;s.parameters.num_workers=10;s.parameters.log_search_progress=False
base=71*val['jp8']+(val['ck'] if 'ck' in val else 0)+V[36]+2229*V[48]
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s):super().__init__();s.t0=time.time()
    def on_solution_callback(s):print('sol %.1fs obj %.3f gain_vs_639 %.3f bound %.3f'%(time.time()-s.t0,s.ObjectiveValue()/SC,s.ObjectiveValue()/SC-base,s.BestObjectiveBound()/SC),flush=True)
st=s.Solve(m,CB())
print(s.StatusName(st),'obj',s.ObjectiveValue()/SC,'bound',s.BestObjectiveBound()/SC,'base639',base,flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    disp={t:p for (t,p),v in sel.items() if s.Value(v)}
    rem=Counter()
    x={}
    for key,g in groups.items():
        g2=dict(cap=g['cap'],times=g['times'],ps=g['ps'],pv=[s.Value(v) for v in g['pv']],fl={k:s.Value(v) for k,v in g['fl'].items()})
        x[key]=g2
        for q,n in zip(g['ps'],g2['pv']):
            if n and g['cap']-sum(q) and not(g['cap']==48 and not q):rem[g['cap']-sum(q)]+=n
    print('dispatch',Counter(disp.values()),{t:p for t,p in disp.items() if p!='jp8'},'remainders',dict(rem))
    pickle.dump(dict(groups=x,disp=disp),open(OUT+'.pkl','wb'))
