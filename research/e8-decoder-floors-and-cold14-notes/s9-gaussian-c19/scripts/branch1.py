"""Exact case split for c totals, cost <= cm (relaxation 'lifted packing').  Non-tight totals with delta>0 ('deficient');
case 0: none -> pure mu ILP.  Otherwise WLOG (line group) the deficient total of largest e is the orbit representative t1;
the other deficient totals have e <= min(e1, slack - e1).  Each case: max |mu| + sum delta over
M mu + y_t1 + sum n_t y_t <= cap, sum n_t e_t <= slack - e1, mu in Z^60, n in Z.  Exclusion iff every case < 4c - cm.
argv: c cm case(orbit index or -1) timelimit"""
import pickle, sys, numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix, hstack, vstack
c=int(sys.argv[1]); cm=int(sys.argv[2]); case=int(sys.argv[3]); tl=float(sys.argv[4])
cap=c-12; slack=128*(cm+c)-7680; need=4*c-cm
C=pickle.load(open('hits_table.pkl','rb'))['C']
M=np.zeros((640,60))
for k,cl in enumerate(C): M[k,cl]=1
T=pickle.load(open('types_e256.pkl','rb')); L=pickle.load(open('lift.pkl','rb')); dom=pickle.load(open('dom.pkl','rb')); orb=dom['orb']
fixed=np.zeros(640); base=0; e1=None
if case>=0:
    r=dom['reps'][case]; a,b,R,e1,m=T[r]; x,d=L[r]; assert d>0 and e1<=slack
    fixed=m-M[:,x].sum(1); base=d+len(x)   # t1's own x lines are not in mu: count alpha directly
    cols=[i for i in range(len(T)) if L[i][1]>0 and T[i][3]<=min(e1,slack-e1)]
else: cols=[]
n=len(cols)
Y=csr_matrix(np.array([T[i][4]-M[:,L[i][0]].sum(1) for i in cols]).T) if n else csr_matrix((640,0))
dl=np.array([L[i][1]+len(L[i][0]) for i in cols],float)   # gain g_t = alpha + delta (x lines counted here, not in mu)
el=np.array([T[i][3] for i in cols],float)
# note: for deficient types we count their x lines inside their own column (load M x + y = m_t): exact miss vector
Ycol=csr_matrix(np.array([T[i][4] for i in cols],float).T) if n else csr_matrix((640,0))
obj=-np.concatenate([np.ones(60),dl])
FEAS=len(sys.argv)>5 and sys.argv[5]=='feas'     # feasibility form: add row  |mu| + sum g >= need - base
A=vstack([hstack([csr_matrix(M),Ycol]),csr_matrix(np.concatenate([np.zeros(60),el])[None,:]),csr_matrix(obj[None,:])])
ub=np.concatenate([cap-T[dom['reps'][case]][4] if case>=0 else np.full(640,cap),[slack-(e1 or 0)],[-(need-base) if FEAS else np.inf]])
t0=time.time()
res=milp(obj,constraints=[LinearConstraint(A,-np.inf,ub)],integrality=np.ones(60+n),bounds=Bounds(0,cap),options={'time_limit':tl})
val=None if res.x is None else -res.fun+base
bound=-res.mip_dual_bound+base if getattr(res,'mip_dual_bound',None) is not None else None
if FEAS:
    print('c=%d cost<=%d case %d e1 %s cols %d -> %s'%(c,cm,case,e1,n,'EXCLUDED (infeasible)' if res.status==2 else ('FEASIBLE' if res.x is not None else 'OPEN: '+res.message)),'%.0fs'%(time.time()-t0),flush=True)
    if res.x is not None: xx=np.round(res.x).astype(int); print('  mu',xx[:60].tolist(),'deficient',[(cols[k],int(orb[cols[k]]),xx[60+k]) for k in range(n) if xx[60+k]])
    sys.exit()
ok=(res.status==0 and val<need-0.5) or (bound is not None and bound<need-0.5)
print('c=%d cost<=%d case %d e1 %s cols %d -> %s (opt: best %s, dual bound %s, need %d)'%(c,cm,case,e1,n,'EXCLUDED' if ok else 'OPEN',None if val is None else round(val),None if bound is None else round(bound,3),need),'%.0fs'%(time.time()-t0),flush=True)
if res.x is not None and val>=need:
    xx=np.round(res.x).astype(int); print('  mu',xx[:60].tolist(),'deficient',[(cols[k],int(orb[cols[k]]),xx[60+k]) for k in range(n) if xx[60+k]])
