"""Tight-types-only covering ILP (S8 tight_ilp) + diagonal coverage: every line T lies in X_j and Y_j of some total.
argv: c timelimit"""
import pickle, sys, numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
from lines import views
S=views()['Gauss']; NO=S.NO
C=pickle.load(open('hits_table.pkl','rb'))['C']
c=int(sys.argv[1]); tl=float(sys.argv[2])
orth=lambda a,b: a!=b and not NO[a,b]
pairs=[(a,b) for a in range(60) for b in range(a+1,60) if orth(a,b)]
# columns: dumbbells (beta2, x={a,b}), singles l (beta3, x={l}), full (beta4)
cols=[]
for a,b in pairs: cols.append((2,[a,b],[T for T in range(60) if orth(T,a) and orth(T,b)]))
for l in range(60): cols.append((3,[l],[T for T in range(60) if orth(T,l)]))
cols.append((4,[],list(range(60))))
n=len(cols); A=[];lb=[];ub=[]
M=np.zeros((640,n))
for k,(beta,x,cov) in enumerate(cols):
    for q,cl in enumerate(C): M[q,k]=len(set(x)&set(cl))
A.append(M); lb+= [-np.inf]*640; ub+=[c-12]*640
D=np.zeros((60,n))
for k,(beta,x,cov) in enumerate(cols): D[cov,k]=1
A.append(D); lb+=[1]*60; ub+=[np.inf]*60
A.append(np.ones((1,n))); lb.append(c); ub.append(c)
A.append(np.array([[cl[0] for cl in cols]])); lb.append(-np.inf); ub.append(42)
t=time.time()
r=milp(np.array([cl[0] for cl in cols],float),constraints=[LinearConstraint(np.vstack(A),lb,ub)],integrality=np.ones(n),bounds=Bounds(0,c),options={'time_limit':tl})
print('c',c,'status',r.status,r.message,'cost',r.fun,'%.0fs'%(time.time()-t))
if r.x is not None:
    x=np.round(r.x).astype(int); print([(cols[k][0],cols[k][1],x[k]) for k in np.nonzero(x)[0]])
