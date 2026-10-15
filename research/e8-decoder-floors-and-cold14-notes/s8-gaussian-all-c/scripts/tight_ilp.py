"""Clique covering using only tight types (dumbbells (l^perp,m^perp) l⊥m beta 2; (l^perp,l^perp)/(l^perp,K4) beta 3; (K4,K4) beta 4),
for a fixed number c of totals: misses per clique = sum over chosen totals of |C ∩ x_t| <= c - 12, cost <= 42.
argv: c"""
import pickle, sys, numpy as np
from ortools.sat.python import cp_model
from lines import views
S=views()['Gauss']; NO=S.NO
C=pickle.load(open('hits_table.pkl','rb'))['C']
c=int(sys.argv[1])
pairs=[(a,b) for a in range(60) for b in range(a+1,60) if not NO[a,b]]
m=cp_model.CpModel()
nD={p:m.NewIntVar(0,21,'d%d_%d'%p) for p in pairs}; nS={l:m.NewIntVar(0,14,'s%d'%l) for l in range(60)}; nF=m.NewIntVar(0,3,'f')
m.Add(sum(nD.values())+sum(nS.values())+nF==c)
m.Add(2*sum(nD.values())+3*sum(nS.values())+4*nF<=42)
mu={l:[] for l in range(60)}
for (a,b),v in nD.items(): mu[a].append(v); mu[b].append(v)
for l,v in nS.items(): mu[l].append(v)
for cl in C: m.Add(sum(v for l in cl for v in mu[l])<=c-12)
s=cp_model.CpSolver(); s.parameters.num_workers=8; s.parameters.max_time_in_seconds=300
r=s.Solve(m); print('c',c,'status',s.StatusName(r))
if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    print('D',[(p,s.Value(v)) for p,v in nD.items() if s.Value(v)],'S',[(l,s.Value(v)) for l,v in nS.items() if s.Value(v)],'F',s.Value(nF))
