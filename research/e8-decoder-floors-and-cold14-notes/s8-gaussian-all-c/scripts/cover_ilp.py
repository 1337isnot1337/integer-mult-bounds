"""Clique-covering ILP relaxation (c-free): integer multiplicities n_t of rank-maximal flat-pair types with deficit <= 384,
every 12-clique covered >= 12 times, sum rank*n <= 42.  Feasible => relaxation cannot close all c; infeasible => all c closed."""
import pickle, numpy as np, time, sys
from ortools.sat.python import cp_model
d=pickle.load(open('hits_table.pkl','rb')); fl=d['fl']; C=d['C']
T=pickle.load(open('types.pkl','rb')); ts=T['types']; R=T['R']; D=T['D']
L=np.zeros((len(fl),60),np.int64)
for i,(f,dd) in enumerate(fl): L[i,sorted(f)]=1
inc=np.zeros((60,640),np.int64)
for k,c in enumerate(C): inc[c,k]=1
meet=(L@inc>0)
m=cp_model.CpModel(); n=[]
for k,(a,b) in enumerate(ts):
    ub=42//int(R[k]) if D[k]==0 else min(42//int(R[k]),384//int(D[k]))
    n.append(m.NewIntVar(0,ub,'n%d'%k))
cols=[np.nonzero(meet[a]&meet[b])[0] for a,b in ts]
rows=[[] for _ in range(640)]
for k,cl in enumerate(cols):
    for q in cl: rows[q].append(k)
for q in range(640): m.Add(sum(n[k] for k in rows[q])>=12)
m.Add(sum(int(R[k])*n[k] for k in range(len(n)))<=int(sys.argv[1]) if len(sys.argv)>1 else 42)
m.Add(sum(int(D[k])*n[k] for k in range(len(n)))<=384)
s=cp_model.CpSolver(); s.parameters.num_workers=8; s.parameters.max_time_in_seconds=float(sys.argv[2]) if len(sys.argv)>2 else 900
t=time.time(); r=s.Solve(m); print('status',s.StatusName(r),'%.0fs'%(time.time()-t))
if r in (cp_model.FEASIBLE,cp_model.OPTIMAL):
    sol=[(k,s.Value(n[k])) for k in range(len(n)) if s.Value(n[k])]
    print('solution: totals',sum(v for k,v in sol),'cost',sum(int(R[k])*v for k,v in sol))
    from collections import Counter
    print(Counter((len(fl[ts[k][0]][0]),len(fl[ts[k][1]][0]),int(R[k]),int(D[k])) for k,v in sol for _ in range(v)))
    pickle.dump(sol,open('cover_sol.pkl','wb'))
