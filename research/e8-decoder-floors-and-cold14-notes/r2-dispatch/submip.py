"""Window-subset exact repack: free every role hosted in windows S (plus unplaced roles), re-solve S with the
aggregate pattern MIP (Hall masks; cap<48 exact full; cap48 full/empty or remainder<=TIGHT), expand literally."""
import sys,json,pickle,random,time
import numpy as np
from collections import Counter,defaultdict
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix
from load import P,reg
sys.path.insert(0,'.')
V={int(k):v for k,v in json.load(open('V639.json')).items()};V[0]=0.0
WID=[4,5,7,8,9]
def build_state(T,neww):
    import gzip
    rows=json.loads(gzip.decompress(open('/Users/joelpulikkan/imb-r2/research/pr638-improvement-20261013/witness638/data/OWNERS.json.gz','rb').read()))
    own={};pool=defaultdict(list)
    for h in range(492):pool[neww[h]].append(h)
    for r in sorted(rows,key=lambda r:(r['time'],r['helper'])):
        o=(r['owner_replica'],r['child'],r['port'])
        if r['time']!=T:own[r['time'],r['helper']]=o
        elif pool[r['width']]:own[T,pool[r['width']].pop()]=o
    for w,v in pool.items():
        for h in v:own[T,h]=None
    return own
def solve(own,widthof,S,TIGHT,SECS,seed=0):
    W=P['windows']
    free=[r for r,o in own.items() if o is None or f'{o[0]},{o[1]}' in S]
    dem=Counter((r[0],widthof(r)) for r in free)
    ub=[];cost=[];R=[];lo=[];hi=[]
    def var(c,u=np.inf):ub.append(u);cost.append(-c);return len(ub)-1
    def con(row,l,h):R.append(row);lo.append(l);hi.append(h)
    groups={};invrow=defaultdict(dict)
    for key in S:
        cap,times=W[key]
        def pats(cap,L):
            out=[]
            def rec(pre,i,tot):
                r=cap-tot
                if r==0 or (cap==48 and (r<=TIGHT or r==48)): out.append(tuple(pre))
                for j in range(i,len(WID)):
                    w=WID[j]
                    if tot+w<=cap and len(pre)<L: rec(pre+[w],j,tot+w)
            rec([],0,0);return out
        ps=pats(cap,len(times));cnts=[Counter(q) for q in ps]
        pv=[var(V[cap-sum(q)] if cap-sum(q)!=48 else V[48],112) for q in ps]
        con({i:1 for i in pv},112,112)
        fl={}
        for t in times:
            for w in WID:
                if not dem[t,w] or not any(c[w] for c in cnts):continue
                i=var(0,112);fl[t,w]=i;invrow[t,w][i]=1
            seen=set()
            for mask in range(1,32):
                cols={w for b,w in enumerate(WID) if mask>>b&1}
                req=tuple(i for (tt,w),i in fl.items() if tt==t and w in cols)
                pres=tuple(j for j,c in zip(pv,cnts) if any(c[w] for w in cols))
                if req and (req,pres) not in seen:
                    seen.add((req,pres));row={i:1 for i in req}
                    for j in pres:row[j]=row.get(j,0)-1
                    con(row,-np.inf,0)
        for w in WID:
            row={i:1 for (t,ww),i in fl.items() if ww==w}
            for j,c in zip(pv,cnts):
                if c[w]:row[j]=row.get(j,0)-c[w]
            if row:con(row,0,0)
        groups[key]=dict(cap=cap,times=times,ps=ps,pv=pv,fl=fl)
    for (t,w),n in dem.items():
        if not invrow[t,w]:print('no window for',t,w);return None
        con(dict(invrow[t,w]),n,n)
    rr,cc,vv=[],[],[]
    for i,row in enumerate(R):
        for j,x in row.items():rr.append(i);cc.append(j);vv.append(x)
    A=coo_matrix((vv,(rr,cc)),shape=(len(R),len(ub))).tocsr()
    t0=time.time()
    res=milp(np.array(cost),integrality=np.ones(len(ub)),bounds=Bounds(np.zeros(len(ub)),np.array(ub)),constraints=LinearConstraint(A,lo,hi),options={'time_limit':SECS,'mip_rel_gap':1e-9})
    print('submip',len(S),'windows vars',len(ub),'status',res.status,res.message[:60],'obj',None if res.x is None else -res.fun,'secs',round(time.time()-t0,1),flush=True)
    if res.x is None:return None
    x=np.round(res.x).astype(int)
    rem=Counter()
    for key,g in groups.items():
        for q,i in zip(g['ps'],g['pv']):
            if x[i] and g['cap']-sum(q) and not (g['cap']==48 and not q):rem[g['cap']-sum(q)]+=x[i];print('  win',key,q,x[i])
    print(' remainders',dict(rem))
    # expand
    exec(open('expand_fn.py').read(),globals())
    pools=defaultdict(list)
    for r in free:pools[r[0],widthof(r)].append(r)
    new=dict(own)
    for gi,(key,g) in enumerate(sorted(groups.items())):
        plist=[q for q,i in zip(g['ps'],g['pv']) for _ in range(x[i])]
        flows={k:x[i] for k,i in g['fl'].items() if x[i]}
        slots=expand(plist,flows,gi)
        a,b=map(int,key.split(','))
        for port,s in enumerate(slots):
            for t,wd in s:new[pools[t,wd].pop()]=(a,b,port)
    assert not any(pools.values())
    return new,rem
if __name__=='__main__':
    T=int(sys.argv[1]);neww=json.load(open(sys.argv[2])) if sys.argv[2]!='-' else reg['jp8']['widths']
    S=sys.argv[3].split(';');TIGHT=int(sys.argv[4]);SECS=float(sys.argv[5]);OUT=sys.argv[6]
    own=build_state(T,neww)
    calls=[c['provider'] for c in P['provider_calls']]
    widthof=lambda r:neww[r[1]] if r[0]==T else reg[calls[r[0]]]['widths'][r[1]]
    out=solve(own,widthof,S,TIGHT,SECS)
    if out:pickle.dump(out[0],open(OUT,'wb'));print('saved',OUT)
