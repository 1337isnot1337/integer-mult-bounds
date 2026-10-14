"""Generalized helper-donor cold-kernel census (family G, strictly contains PR1297's family).
For pivot q and deletion set D of q's early uses (all non-empty subsets), shocks are:
  cut(h,i):  h += a*q inserted right after the B gate i-1 that reads h (any reader, any h != q), or at B start;
             restored by h -= a*q at the end of early cleanup.  Response u = col_i[h] - e_h.
  hook(g):   s += c*q / s -= c*q around any early add gate g = (t += k*s), s != q.  Response v = k*c*col_g[t].
Solve d = a*u (+ b*v) exactly over Q by hashing images in V/<d> (projectively normalized); dyadic a, c only.
All candidates are then screened exactly (mod p map, cones, exact frames) by price_all.py."""
import gzip,json,sys,itertools,time,os
from fractions import Fraction as Q
from multiprocessing import Pool
from relations import coef,add,col,dy
W=None
def init(path):
    global W; W=json.load(gzip.open(path))
def canon(x,d,k0):
    if not x: return None
    r=Q(x.get(k0,0))/d[k0]
    y={k:v-r*d.get(k,0) for k,v in x.items()}
    for k,v in d.items():
        if k not in x and r: y[k]=-r*v
    y={k:v for k,v in y.items() if v}
    if not y: return ('D',)       # x proportional to d
    ks=sorted(y); n=y[ks[0]]
    return tuple((k,y[k]/n) for k in ks)
def work(args):
    q,dele=args; w=W; B=w['B']; dele=set(dele)
    first=next((i for i,g in enumerate(B) if g[1]==q),len(B))
    tail=[w['cleanup'][i] for i,U in w['early_cleanup']]; seq=B+tail
    new=[g for i,g in enumerate(B) if i not in dele]+tail
    d=add(col(seq,q),col(new,q),-1)
    if not d: return [dict(pivot=q,dele=sorted(dele),kind='free',ed=dict(delete=sorted(dele),insert=[],tail=[],prepend=[]))]
    k0=min(d)
    cols={}; get=lambda j: cols.get(j) or {j:Q(1)}
    U=[];Vv=[]
    for i in range(len(seq)-1,-1,-1):
        g=seq[i]
        if i<first and i not in dele and g[0]=='add':
            t,s=g[1:3]
            if s!=q:
                Vv.append((i,g,{k:coef(g)*v for k,v in get(t).items()}))   # response per unit c
                U.append((i+1,s,add(get(s),{s:Q(1)},-1)))                  # cut right after read of s (state after gate i)
        if i in dele: continue
        if g[0]=='add':
            t,s=g[1:3];cols[s]=add(get(s),get(t),coef(g))
        else: cols[g[1]]={k:v*coef(g) for k,v in get(g[1]).items()}
    for h in set(get(x) and x for x in []) : pass
    # cuts at B start for every register read before first
    seen=set(s for _,s,_ in U)
    for s in seen: U.append((0,s,add(get(s),{s:Q(1)},-1)))
    NE=len(w['early_cleanup']);out=[]
    def hookins(i,g,c): return [[i,['add',g[2],q,c.numerator,c.denominator,[]]],[i+1,['add',g[2],q,-c.numerator,c.denominator,[]]]]
    def cutins(cut,h,a): return [[cut,['add',h,q,a.numerator,a.denominator,[]]]],[[NE,['add',h,q,-a.numerator,a.denominator,[]]]]
    base=dict(pivot=q,dele=sorted(dele))
    hu={};hv={}
    for cut,h,u in U:
        if not u or h==q: continue
        cu=canon(u,d,k0)
        if cu==('D',):
            a=Q(d[k0])/u[k0]
            if dy(a):
                ins,tl=cutins(cut,h,a);out.append(dict(base,kind='helper',helper=h,cut=cut,amount=str(a),ed=dict(delete=sorted(dele),insert=ins,tail=tl,prepend=[])))
        else: hu.setdefault(cu,[]).append((cut,h,u))
    for i,g,v in Vv:
        if not v: continue
        cv=canon(v,d,k0)
        if cv==('D',):
            c=Q(d[k0])/v[k0]
            if dy(c): out.append(dict(base,kind='hook',donor=g[2],hook=i,output=g[1],ed=dict(delete=sorted(dele),insert=hookins(i,g,c),tail=[],prepend=[])))
        else: hv.setdefault(cv,[]).append((i,g,v))
    for key in set(hu)&set(hv):
        for cut,h,u in hu[key]:
            for i,g,v in hv[key]:
                if h==g[2] and cut in (i,i+1): continue
                # solve d = a u + b v (u,v independent, both nonzero mod d)
                ks=sorted(set(u)|set(v)|set(d)); sol=None
                for x,y in itertools.combinations(ks,2):
                    det=u.get(x,0)*v.get(y,0)-u.get(y,0)*v.get(x,0)
                    if det:
                        a=Q(d.get(x,0)*v.get(y,0)-d.get(y,0)*v.get(x,0))/det;b=Q(u.get(x,0)*d.get(y,0)-u.get(y,0)*d.get(x,0))/det
                        if all(a*u.get(k,0)+b*v.get(k,0)==d.get(k,0) for k in ks): sol=(a,b)
                        break
                if not sol: continue
                a,c=sol
                if not a or not c or not dy(a) or not dy(c): continue
                ins,tl=cutins(cut,h,a)
                out.append(dict(base,kind='two',helper=h,cut=cut,amount=str(a),donor=g[2],hook=i,output=g[1],ed=dict(delete=sorted(dele),insert=hookins(i,g,c)+ins,tail=tl,prepend=[])))
    return out
if __name__=='__main__':
    path,outp,mode=sys.argv[1],sys.argv[2],sys.argv[3]
    init(path);B=W['B'];first={}
    for i,g in enumerate(B): first.setdefault(g[1],i)
    early={}
    for i,g in enumerate(B):
        if g[0]=='add' and i<first.get(g[2],10**9): early.setdefault(g[2],[]).append(i)
    PV=set(map(int,os.environ["PIVOTS"].split(","))) if os.environ.get("PIVOTS") else None
    jobs=[]
    for q,E in sorted(early.items()):
        if PV and q not in PV: continue
        if mode=='full': jobs.append((q,tuple(E)))
        else:
            for r in range(1,len(E)+1):
                for S in itertools.combinations(E,r): jobs.append((q,S))
    t=time.time();res=[]
    with Pool(int(os.environ.get('NW','10')),initializer=init,initargs=(path,)) as P:
        for n,o in enumerate(P.imap_unordered(work,jobs,chunksize=2)):
            res+=o
            if n%100==0: print('progress',n,len(jobs),len(res),round(time.time()-t),flush=True)
    import collections
    print('jobs',len(jobs),'cands',len(res),'pivots',len({r['pivot'] for r in res}),'kinds',collections.Counter(r['kind'] for r in res),'sec',round(time.time()-t,1))
    json.dump(res,open(outp,'w'))
