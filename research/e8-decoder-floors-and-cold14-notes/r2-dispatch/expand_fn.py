import random
import numpy as np
from scipy.sparse import csr_matrix,coo_matrix
from scipy.sparse.csgraph import maximum_flow
from scipy.optimize import milp,LinearConstraint,Bounds
from collections import Counter,defaultdict
WID=[4,5,7,8,9]
def expand(plist,flows,seed):
    times=sorted({t for t,w in flows});counts=[Counter(p) for p in plist];rng=random.Random(seed)
    for attempt in range(60):
        used=[set() for _ in plist];result=[[] for _ in plist]
        colors=sorted(WID,key=lambda w:(sum(w in p for p in plist),w))
        if attempt:rng.shuffle(colors)
        ok=True
        for width in colors:
            active=[p for p in range(len(counts)) if counts[p][width]]
            if not active:continue
            rng.shuffle(active);start=1+len(times);sink=start+len(active);rr,cc,vv=[],[],[]
            for ti,t in enumerate(times):
                d=flows.get((t,width),0)
                if d:
                    rr.append(0);cc.append(1+ti);vv.append(d)
                    for pi,port in enumerate(active):
                        if t not in used[port]:rr.append(1+ti);cc.append(start+pi);vv.append(1)
            for pi,port in enumerate(active):rr.append(start+pi);cc.append(sink);vv.append(counts[port][width])
            f=maximum_flow(csr_matrix((vv,(rr,cc)),shape=(sink+1,sink+1),dtype=np.int64),0,sink)
            if f.flow_value!=sum(flows.get((t,width),0) for t in times):ok=False;break
            F=f.flow.tocoo() if hasattr(f.flow,'tocoo') else coo_matrix(f.flow)
            for a,b,v in zip(F.row,F.col,F.data):
                if v>0 and 1<=a<start and start<=b<sink:
                    port=active[b-start];t=times[a-1];used[port].add(t);result[port].append((t,width))
        if ok:return result
    # exact fallback
    keys=[];tv=defaultdict(dict);pvr=defaultdict(dict);tp=defaultdict(dict)
    for port,c in enumerate(counts):
        for width,n in c.items():
            for t in times:
                if flows.get((t,width),0):
                    i=len(keys);keys.append((port,t,width));tv[t,width][i]=1;pvr[port,width][i]=1;tp[t,port][i]=1
    R=[];lo=[];hi=[]
    for k,row in tv.items():R.append(row);lo.append(flows[k]);hi.append(flows[k])
    for (port,width),row in pvr.items():R.append(row);lo.append(counts[port][width]);hi.append(counts[port][width])
    for row in tp.values():R.append(row);lo.append(0);hi.append(1)
    rr,cc,vv=[],[],[]
    for i,row in enumerate(R):
        for j,v in row.items():rr.append(i);cc.append(j);vv.append(v)
    res=milp(np.zeros(len(keys)),integrality=np.ones(len(keys)),bounds=Bounds(0,1),constraints=LinearConstraint(coo_matrix((vv,(rr,cc)),shape=(len(R),len(keys))).tocsr(),lo,hi),options={'time_limit':120})
    assert res.x is not None,'expansion infeasible'
    result=[[] for _ in counts]
    for i,(port,t,width) in enumerate(keys):
        if round(res.x[i]):result[port].append((t,width))
    return result
