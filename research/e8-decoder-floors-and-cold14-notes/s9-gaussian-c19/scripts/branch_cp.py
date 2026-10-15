"""CP-SAT version of branch1.py feasibility form (same case split, same columns).  argv: c cm case timelimit workers"""
import pickle, sys, numpy as np, time
from ortools.sat.python import cp_model
c=int(sys.argv[1]); cm=int(sys.argv[2]); case=int(sys.argv[3]); tl=float(sys.argv[4]); wk=int(sys.argv[5])
cap=c-12; slack=128*(cm+c)-7680; need=4*c-cm
C=pickle.load(open('hits_table.pkl','rb'))['C']
T=pickle.load(open('types_e256.pkl','rb')); L=pickle.load(open('lift.pkl','rb')); dom=pickle.load(open('dom.pkl','rb'))
base=0; e1=0; load0=np.zeros(640,int)
if case>=0:
    r=dom['reps'][case]; a,b,R,e1,m=T[r]; x,d=L[r]; assert d>0 and e1<=slack
    base=4-R; load0=m.astype(int)
    cols=[i for i in range(len(T)) if L[i][1]>0 and T[i][3]<=min(e1,slack-e1)]
else: cols=[]
md=cp_model.CpModel()
mu=[md.NewIntVar(0,cap,'m%d'%t) for t in range(60)]
nv=[md.NewIntVar(0,min(cap,(slack-e1)//T[i][3]),'n%d'%i) for i in cols]
for q,cl in enumerate(C):
    terms=[mu[t] for t in cl]+[nv[k] for k,i in enumerate(cols) if T[i][4][q]]
    md.Add(sum(terms)<=cap-int(load0[q]))
md.Add(sum(T[i][3]*nv[k] for k,i in enumerate(cols))<=slack-e1)
md.Add(sum(mu)+sum((4-T[i][2])*nv[k] for k,i in enumerate(cols))>=need-base)
s=cp_model.CpSolver(); s.parameters.num_workers=wk; s.parameters.max_time_in_seconds=tl
t=time.time(); res=s.Solve(md)
print('CP-SAT c=%d cost<=%d case %d e1 %s cols %d -> %s'%(c,cm,case,e1,len(cols),{'INFEASIBLE':'EXCLUDED (infeasible)'}.get(s.StatusName(res),s.StatusName(res))),'%.0fs'%(time.time()-t),flush=True)
