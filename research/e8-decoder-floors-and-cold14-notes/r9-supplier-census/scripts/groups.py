"""Group B reads by normalized source value at read time; report groups of gain-carrying reads (PR1957 relaxation)."""
import gzip,json,sys,collections
from fractions import Fraction as Q
w=json.load(gzip.open(sys.argv[1])); rel=json.load(open(sys.argv[2]))
coef=lambda g: Q(g[3],g[4]) if g[0]=='add' else Q(g[2],g[3])
B=w['B']; tails=[w['cleanup'][i] for i,U in w['early_cleanup']]; seq=B+tails
rows={}; get=lambda x: rows.get(x,{x:Q(1)})
def norm(r):
    k0=min(r);a=r[k0];return tuple(sorted((k,v/a) for k,v in r.items()))
G=collections.defaultdict(list)
for i,g in enumerate(seq):
    if g[0]=='add':
        if i<len(B): G[norm(get(g[2]))].append(i)
        a=dict(get(g[1]));c=coef(g)
        for k,v in get(g[2]).items():
            a[k]=a.get(k,0)+c*v
            if not a[k]: del a[k]
    else: a={k:v*coef(g) for k,v in get(g[1]).items()}
    rows[g[1]]=a
out=[]
for key,L in G.items():
    gl=[i for i in L if rel.get(str(i),{}).get('delta',0)<0]
    if len(gl)>=2: out.append(dict(key=str(key)[:60],reads=L,gain=gl,deltas=[rel[str(i)]['delta'] for i in gl],src=sorted({B[i][2] for i in gl})))
out.sort(key=lambda r:-len(r['gain']))
print(len(out),'groups with >=2 gain reads; sizes',collections.Counter(len(r['gain']) for r in out))
for r in out[:60]: print(r['src'],r['gain'],r['deltas'])
json.dump(out,open(sys.argv[3],'w'))
