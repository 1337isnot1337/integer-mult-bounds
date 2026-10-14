"""Multi-shock cold-kernel census (family G2/G3): any 2 or 3 shocks from S = cuts U (after any read of any h, or at B
start) and hooks V (around any early add gate), any type mix (cut+cut, hook+hook, cut+hook, ...).
d in span(s1,s2[,s3]) found exactly by Gaussian quotient hashing; dyadic, nonzero coefficients only.
usage: relations3.py WORD OUT.json K MODE(full|subsets) [MINUSES]"""
import gzip,json,sys,itertools,time,os,collections
from fractions import Fraction as Q
from multiprocessing import Pool
from relations import coef,add,col,dy
W=None;K=2
def init(path,k):
    global W,K; W=json.load(gzip.open(path));K=k
def reduce(x,basis):
    """basis: list of (pivot key, vector) in echelon form; returns reduced copy."""
    y=dict(x)
    for k,b in basis:
        r=y.get(k)
        if r:
            r=Q(r)/b[k]
            for kk,vv in b.items():
                z=y.get(kk,0)-r*vv
                if z: y[kk]=z
                else: y.pop(kk,None)
    return y
def norm(y):
    ks=sorted(y); n=y[ks[0]]; return tuple((k,y[k]/n) for k in ks)
def solve(vecs,d):
    """exact least solve d = sum c_i vecs_i (vecs independent) via Fraction Gaussian elimination."""
    keys=sorted(set().union(*vecs)|set(d)); n=len(vecs)
    M=[[v.get(k,Q(0)) for v in vecs]+[Q(d.get(k,0))] for k in keys]
    r=0;piv=[]
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]),None)
        if p is None: return None
        M[r],M[p]=M[p],M[r]
        inv=1/M[r][c]; M[r]=[x*inv for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]:
                f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
    if any(row[n] for row in M[r:]): return None
    return [M[i][n] for i in range(n)]
def work(args):
    q,dele=args; w=W; B=w['B']; dele=set(dele)
    first=next((i for i,g in enumerate(B) if g[1]==q),len(B))
    tail=[w['cleanup'][i] for i,U in w['early_cleanup']]; seq=B+tail
    new=[g for i,g in enumerate(B) if i not in dele]+tail
    d=add(col(seq,q),col(new,q),-1)
    if not d: return []
    cols={}; get=lambda j: cols.get(j) or {j:Q(1)}
    S=[]
    for i in range(len(seq)-1,-1,-1):
        g=seq[i]
        if i<first and i not in dele and g[0]=='add':
            t,s=g[1:3]
            if s!=q:
                S.append(('hook',i,g,{k:coef(g)*v for k,v in get(t).items()}))
                S.append(('cut',i+1,s,add(get(s),{s:Q(1)},-1)))
        if i in dele: continue
        if g[0]=='add':
            t,s=g[1:3];cols[s]=add(get(s),get(t),coef(g))
        else: cols[g[1]]={k:v*coef(g) for k,v in get(g[1]).items()}
    for s in {x[2] for x in S if x[0]=='cut'}: S.append(('cut',0,s,add(get(s),{s:Q(1)},-1)))
    S=[x for x in S if x[3]]
    # dedupe identical (kind,pos,reg) entries
    seen=set();S2=[]
    for x in S:
        key=(x[0],x[1],x[2] if x[0]=='cut' else x[2][2])
        if key not in seen: seen.add(key);S2.append(x)
    S=S2
    k0=min(d); bd=[(k0,d)]
    NE=len(w['early_cleanup'])
    def edit(shocks,coefs):
        ins=[];tl=[]
        for (kind,pos,obj,v),c in zip(shocks,coefs):
            if kind=='hook':
                cc=c  # response v already per unit c
                ins+= [[pos,['add',obj[2],q,cc.numerator,cc.denominator,[]]],[pos+1,['add',obj[2],q,-cc.numerator,cc.denominator,[]]]]
            else:
                ins+= [[pos,['add',obj,q,c.numerator,c.denominator,[]]]]; tl+=[[NE,['add',obj,q,-c.numerator,c.denominator,[]]]]
        return dict(delete=sorted(dele),insert=ins,tail=tl,prepend=[])
    out=[]
    def emit(shocks):
        c=solve([x[3] for x in shocks],d)
        if c is None or any(not x or not dy(x) for x in c): return
        out.append(dict(pivot=q,dele=sorted(dele),kind='+'.join(x[0] for x in shocks),shocks=[[x[0],x[1],x[2] if x[0]=='cut' else x[2][2]] for x in shocks],ed=edit(shocks,c)))
    # reduced images mod d
    R1=[]
    for x in S:
        y=reduce(x[3],bd)
        if y: R1.append((x,y))
    if K==2:
        h=collections.defaultdict(list)
        for x,y in R1: h[norm(y)].append(x)
        for grp in h.values():
            for a,b in itertools.combinations(grp,2): emit([a,b])
    else:
        for ia,(a,ya) in enumerate(R1):
            ka=min(ya); basis=bd+[(ka,ya)]
            h=collections.defaultdict(list)
            for x,y in R1[ia+1:]:
                z=reduce(y,[(ka,ya)])
                if z: h[norm(z)].append(x)
            for grp in h.values():
                for b,c in itertools.combinations(grp,2): emit([a,b,c])
                if len(out)>20000: return out
    return out
if __name__=='__main__':
    path,outp,k,mode=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]; minu=int(sys.argv[5]) if len(sys.argv)>5 else 1
    init(path,k);B=W['B'];first={}
    for i,g in enumerate(B): first.setdefault(g[1],i)
    early={}
    for i,g in enumerate(B):
        if g[0]=='add' and i<first.get(g[2],10**9): early.setdefault(g[2],[]).append(i)
    PV=set(map(int,os.environ["PIVOTS"].split(","))) if os.environ.get("PIVOTS") else None
    jobs=[]
    for q,E in sorted(early.items()):
        if (PV and q not in PV) or len(E)<minu: continue
        if mode=='full': jobs.append((q,tuple(E)))
        else:
            for r in range(1,len(E)+1):
                for S in itertools.combinations(E,r): jobs.append((q,S))
    t=time.time();res=[]
    with Pool(int(os.environ.get('NW','10')),initializer=init,initargs=(path,k)) as P:
        for n,o in enumerate(P.imap_unordered(work,jobs,chunksize=1)):
            res+=o
            if n%50==0: print('progress',n,len(jobs),len(res),round(time.time()-t),flush=True)
    print('jobs',len(jobs),'cands',len(res),'pivots',len({r['pivot'] for r in res}),'kinds',collections.Counter(r['kind'] for r in res),'sec',round(time.time()-t,1))
    json.dump(res,open(outp,'w'))
