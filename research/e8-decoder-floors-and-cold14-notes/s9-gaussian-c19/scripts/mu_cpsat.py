"""Independent cross-check of the mu-packing optimum with CP-SAT: is there mu in Z>=0^60 with M mu <= cap and |mu| >= target?"""
import pickle, sys, numpy as np, time
from ortools.sat.python import cp_model
C=pickle.load(open('hits_table.pkl','rb'))['C']
cap=int(sys.argv[1]); target=int(sys.argv[2]); wk=int(sys.argv[3]) if len(sys.argv)>3 else 2
m=cp_model.CpModel(); mu=[m.NewIntVar(0,cap,'m%d'%i) for i in range(60)]
for cl in C: m.Add(sum(mu[t] for t in cl)<=cap)
m.Add(sum(mu)>=target)
s=cp_model.CpSolver(); s.parameters.num_workers=wk; s.parameters.max_time_in_seconds=3000
t=time.time(); r=s.Solve(m); print('cap',cap,'|mu|>=',target,s.StatusName(r),'%.0fs'%(time.time()-t),flush=True)
