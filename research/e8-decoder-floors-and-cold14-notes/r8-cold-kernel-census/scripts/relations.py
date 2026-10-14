"""Exhaustive helper-donor cold-kernel relation census (generalizes PR1297 search_relations.py).
For every register q with early uses (reads before q's first B write) and every non-empty subset D of those early uses,
solve d = a*u + b*v exactly over Q, where d is the change of q's final column caused by deleting D, u is a helper cut
shock (h += a*q right after an early output read of helper h; restored at end of early cleanup), v is a donor hook
(donor += c*q / donor -= c*q around an output read of donor).  Also one-shock relations (a only / b only).
Dyadic coefficients only.  Output: list of candidate edit dicts in harness format (indices into the given word)."""
import gzip,json,sys,itertools,time
from fractions import Fraction as Q
from multiprocessing import Pool
def coef(g): return Q(g[3],g[4]) if g[0]=='add' else Q(g[2],g[3])
def add(a,b,c):
    d=dict(a)
    for k,v in b.items():
        x=d.get(k,Q(0))+c*v
        if x: d[k]=x
        else: d.pop(k,None)
    return d
def col(seq,q):
    r={q:Q(1)}
    for g in seq:
        t=g[1]
        if g[0]=='add':
            x=r.get(t,Q(0))+coef(g)*r.get(g[2],Q(0))
        else: x=r.get(t,Q(0))*coef(g)
        if x: r[t]=x
        else: r.pop(t,None)
    return r
dy=lambda c: not (c.denominator&(c.denominator-1))
def solve2(u,v,d):
    keys=set(u)|set(v)|set(d)
    # least squares-free exact: pick two independent rows
    ks=sorted(keys)
    for i,j in itertools.combinations(ks,2):
        det=u.get(i,0)*v.get(j,0)-u.get(j,0)*v.get(i,0)
        if det:
            a=Q(d.get(i,0)*v.get(j,0)-d.get(j,0)*v.get(i,0))/det;b=Q(u.get(i,0)*d.get(j,0)-u.get(j,0)*d.get(i,0))/det
            if all(a*u.get(k,0)+b*v.get(k,0)==d.get(k,0) for k in keys): return a,b
            return None
    return None   # u,v dependent: covered by one-shock
def solve1(u,d):
    k=next(iter(d));
    if not u.get(k): return None
    a=Q(d[k])/u[k]
    if set(u)==set(d) and all(a*u[x]==d[x] for x in d): return a
    return None
W=None
def init(path):
    global W; W=json.load(gzip.open(path))
def work(args):
    q,dele=args; w=W; B=w['B']; dele=set(dele)
    first=next((i for i,g in enumerate(B) if g[1]==q),len(B))
    tail=[w['cleanup'][i] for i,U in w['early_cleanup']]; seq=B+tail
    new=[g for i,g in enumerate(B) if i not in dele]+tail
    d=add(col(seq,q),col(new,q),-1)
    if not d: return [dict(pivot=q,dele=sorted(dele),kind='free',ed=dict(delete=sorted(dele),insert=[],tail=[],prepend=[]))]
    cols={};hs=[];ts=[]
    get=lambda j: cols.get(j) or {j:Q(1)}
    for i in range(len(seq)-1,-1,-1):
        g=seq[i]
        if i<first and g[0]=='add' and 112<=g[1]<224 and g[2]>=224 and g[2]!=q and i not in dele:
            h=g[2];eff=add(get(h),{h:Q(1)},-1)
            if eff: hs.append((i+1,h,eff))
            ts.append((i,g,dict(get(g[1]))))
        if i in dele: continue
        if g[0]=='add':
            t,s=g[1:3];cols[s]=add(get(s),get(t),coef(g))
        else: cols[g[1]]={k:v*coef(g) for k,v in get(g[1]).items()}
    out=[];NE=len(w['early_cleanup'])
    def hookins(i,g,c): return [[i,['add',g[2],q,c.numerator,c.denominator,[]]],[i+1,['add',g[2],q,-c.numerator,c.denominator,[]]]]
    def cutins(cut,h,a): return [[cut,['add',h,q,a.numerator,a.denominator,[]]]],[[NE,['add',h,q,-a.numerator,a.denominator,[]]]]
    for cut,h,u in hs:
        a=solve1(u,d)
        if a is not None and dy(a):
            ins,tl=cutins(cut,h,a);out.append(dict(pivot=q,dele=sorted(dele),kind='helper',helper=h,cut=cut,amount=str(a),ed=dict(delete=sorted(dele),insert=ins,tail=tl,prepend=[])))
    for i,g,v in ts:
        b=solve1(v,d)
        if b is not None:
            c=b/coef(g)
            if dy(c): out.append(dict(pivot=q,dele=sorted(dele),kind='hook',donor=g[2],hook=i,output=g[1],correction=str(b),ed=dict(delete=sorted(dele),insert=hookins(i,g,c),tail=[],prepend=[])))
    for cut,h,u in hs:
        for i,g,v in ts:
            if h==g[2]: continue
            s=solve2(u,v,d)
            if s:
                a,b=s;c=b/coef(g)
                if not a or not b or not dy(a) or not dy(c): continue
                ins,tl=cutins(cut,h,a)
                out.append(dict(pivot=q,dele=sorted(dele),kind='two',helper=h,cut=cut,amount=str(a),donor=g[2],hook=i,output=g[1],correction=str(b),ed=dict(delete=sorted(dele),insert=hookins(i,g,c)+ins,tail=tl,prepend=[])))
    return out
if __name__=='__main__':
    path,outp=sys.argv[1],sys.argv[2]; mode=sys.argv[3] if len(sys.argv)>3 else 'full'
    init(path);B=W['B'];first={}
    for i,g in enumerate(B): first.setdefault(g[1],i)
    early={}
    for i,g in enumerate(B):
        if g[0]=='add' and i<first.get(g[2],10**9): early.setdefault(g[2],[]).append(i)
    jobs=[]
    import os; PV=set(map(int,os.environ["PIVOTS"].split(","))) if os.environ.get("PIVOTS") else None
    for q,E in sorted(early.items()):
        if PV and q not in PV: continue
        if mode=='full': jobs.append((q,tuple(E)))
        else:
            for r in range(1,len(E)+1):
                for S in itertools.combinations(E,r): jobs.append((q,S))
    t=time.time();res=[]
    with Pool(10,initializer=init,initargs=(path,)) as P:
        for o in P.imap_unordered(work,jobs,chunksize=4): res+=o
    print('jobs',len(jobs),'cands',len(res),'pivots',len({r['pivot'] for r in res}),'sec',round(time.time()-t,1))
    json.dump(res,open(outp,'w'))
