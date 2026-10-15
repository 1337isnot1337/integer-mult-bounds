"""c = 21, all totals tight (then all 21 are dumbbells, oriented): clique packing + diagonal + exact 2x2 support lemma on
every non-orthogonal pair.  argv: c timelimit"""
import pickle, sys, numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix
from f2check import NO
c=int(sys.argv[1]); tl=float(sys.argv[2]); cap=c-12
C=pickle.load(open('hits_table.pkl','rb'))['C']; PK=pickle.load(open('pairkinds.pkl','rb')); kinds=PK['kinds']; minimal=PK['minimal']
orth=lambda a,b: a!=b and not NO[a,b]
perp=lambda l: set(T for T in range(60) if orth(T,l))
ALL=set(range(60))
cols=[]
for a in range(60):
    for b in range(60):
        if orth(a,b): cols.append((2,(a,b),perp(a),perp(b)))
for l in range(60): cols+= [(3,(l,),perp(l),perp(l)),(3,(l,),perp(l),ALL),(3,(l,),ALL,perp(l))]
cols.append((4,(),ALL,ALL))
n=len(cols); pairs=[(a,b) for a in range(60) for b in range(a+1,60) if NO[a,b]]
nz=len(pairs)*len(minimal); N=n+nz
rows=[]; lb=[]; ub=[]
A=lil_matrix((640+60+len(pairs)*(1+3*len(minimal))+2,N)); r=0
for q,cl in enumerate(C):
    for k,(bt,x,X,Y) in enumerate(cols):
        v=len(set(x)&set(cl))
        if v: A[r,k]=v
    lb.append(-np.inf); ub.append(cap); r+=1
for T in range(60):
    for k,(bt,x,X,Y) in enumerate(cols):
        if T in X and T in Y: A[r,k]=1
    lb.append(1); ub.append(np.inf); r+=1
kid={kd:i for i,kd in enumerate(kinds)}
for p,(a,b) in enumerate(pairs):
    kcols={}
    for k,(bt,x,X,Y) in enumerate(cols):
        xs=tuple(i for i,t in enumerate((a,b)) if t in X); ys=tuple(i for i,t in enumerate((a,b)) if t in Y)
        if xs and ys: kcols.setdefault(kid[(xs,ys)],[]).append(k)
    for i,m in enumerate(minimal):
        z=n+p*len(minimal)+i; A[r,z]=1
    lb.append(1); ub.append(np.inf); r+=1
    for i,m in enumerate(minimal):
        z=n+p*len(minimal)+i
        for kd in set(m):
            for k in kcols.get(kd,[]): A[r,k]=1
            A[r,z]=-m.count(kd); lb.append(0); ub.append(np.inf); r+=1
for k in range(n): A[r,k]=1
lb.append(c); ub.append(c); r+=1
for k,(bt,x,X,Y) in enumerate(cols): A[r,k]=bt
lb.append(-np.inf); ub.append(42); r+=1
A=csr_matrix(A[:r])
print('cols',n,'binaries',nz,'rows',r,flush=True)
t=time.time()
res=milp(np.zeros(N),constraints=[LinearConstraint(A,lb,ub)],integrality=np.ones(N),bounds=Bounds(0,np.concatenate([np.full(n,c),np.ones(nz)])),options={'time_limit':tl})
print('c',c,'all-tight + 2x2 lemma:',res.status,res.message,'%.0fs'%(time.time()-t),flush=True)
if res.x is not None:
    x=np.round(res.x[:n]).astype(int); print([(cols[k][1],cols[k][0],x[k]) for k in np.nonzero(x)[0]])
