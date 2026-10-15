import pickle, sys, numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
C=pickle.load(open('hits_table.pkl','rb'))['C']
M=np.zeros((640,60)); 
for k,c in enumerate(C): M[k,c]=1
cap=int(sys.argv[1])
t=time.time()
r=milp(-np.ones(60),constraints=[LinearConstraint(M,-np.inf,cap)],integrality=np.ones(60),bounds=Bounds(0,cap),options={'disp':False,'time_limit':float(sys.argv[2])})
print(cap, r.status, r.message, -r.fun if r.x is not None else None, 'bound', getattr(r,'mip_dual_bound',None), '%.0fs'%(time.time()-t))
if r.x is not None: print(np.round(r.x).astype(int).tolist())
