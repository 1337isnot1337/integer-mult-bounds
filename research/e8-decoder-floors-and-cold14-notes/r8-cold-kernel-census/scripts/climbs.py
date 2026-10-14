import sys,gzip,json,collections
sys.path.insert(0,'/Users/joelpulikkan/imb-harness/r7/tk')
import word as Wd
def climbs(w):
    ev=collections.Counter()
    orig=Wd.dimension
    cur=None
    # re-implement recount with per-register tally
    v,helpers=w['report']['v'],w['report']['R'];n=2*v+helpers
    full=frozenset(range(512));span=Wd.span;dim=Wd.dimension
    cur=[frozenset((0,p)) for p in w['ports']]+[frozenset((0,))]*(n-v)
    for r,vs in w['start_extra'].items(): cur[int(r)]=span(tuple(vs))
    def climb(r,t,tag):
        k=dim(t)-dim(cur[r])
        if k: ev[(r,k)]+=1
        cur[r]=t
    for sec in ('A','B'):
        for e in w[sec]:
            t=span(tuple(e[-1]));rs=e[1:3] if e[0]=='add' else e[1:2]
            for r in rs: climb(r,t,sec)
    for i,vs in w['early_cleanup']:
        e=w['cleanup'][i];rs=e[1:3] if e[0]=='add' else e[1:2]
        for r in rs: climb(r,span(tuple(vs)),'E')
    return ev
a=climbs(json.load(gzip.open(sys.argv[1])));b=climbs(json.load(gzip.open(sys.argv[2])))
diff={k:b[k]-a[k] for k in set(a)|set(b) if a[k]!=b[k]}
print(sorted(diff.items()))
