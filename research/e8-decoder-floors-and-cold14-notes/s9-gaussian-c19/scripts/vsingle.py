import pickle,sys,numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
cap=int(sys.argv[1])
C=pickle.load(open('hits_table.pkl','rb'))['C']
M=np.zeros((640,60))
for k,cl in enumerate(C): M[k,cl]=1
T=pickle.load(open('types_e256.pkl','rb')); L=pickle.load(open('lift.pkl','rb')); dom=pickle.load(open('dom.pkl','rb'))
for k,r in enumerate(dom['reps']):
    a,b,R,e,m=T[r]; x,d=L[r]
    if d<=0: continue
    y=m-M[:,x].sum(1)
    res=milp(-np.ones(60),constraints=[LinearConstraint(M,-np.inf,cap-y)],integrality=np.ones(60),bounds=Bounds(0,cap),options={'time_limit':300})
    print('orbit',k,'R',R,'e',e,'alpha',len(x),'delta',d,'V',-res.fun,'V+alpha+delta',-res.fun+len(x)+d,flush=True)
