"""Jointly optimize all helper entrances, scalar contacts and shared warp maps from PR4626.
Derived from intqwq/Cao Yifan; new flag constraints by Cinna Davis with OpenAI assistance.
Discovery only. Apache-2.0.
"""
from collections import Counter,defaultdict
from copy import deepcopy
from itertools import product
from pathlib import Path
import argparse,gzip,json,sys,time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE/'.deps'))
import numpy as np
import scipy
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_array
sys.path.insert(0,str(HERE))
from warp_merge import J,F,roles,synthesize
from flags import matching_map
from intervals import complete_interval,basis


def load_base():
    payload=json.loads(gzip.decompress((HERE/'BASE-WORD.json.gz').read_bytes()))
    return deepcopy(payload['canonical']),deepcopy(payload['programs'])


from flags import matching_flag


def main(op,time_limit):
    started=time.monotonic();c,programs=load_base();p=[deepcopy(e) for e in programs['forward'] if e[0]!='climb']
    spans=[F.span(b) for b in c['frames']];dims=[len(b) for b in c['frames']];labels={s:i for i,s in enumerate(spans)}
    def label(s):
        s=frozenset(s)
        if s not in labels:
            b=[];v={0}
            for x in sorted(s):
                if x not in v:b.append(x);v|={y^x for y in tuple(v)}
            labels[s]=len(spans);spans.append(s);dims.append(len(b));c['frames'].append(b)
        return labels[s]
    jc={};mc={}
    def join(a,b):
        key=min(a,b),max(a,b)
        if key not in jc:
            if spans[a]<=spans[b]:jc[key]=b
            elif spans[b]<=spans[a]:jc[key]=a
            else:
                v=set(spans[a])
                for x in c['frames'][b]:
                    if x not in v:v|={y^x for y in tuple(v)}
                jc[key]=label(v)
        return jc[key]
    def meet(a,b):
        key=min(a,b),max(a,b)
        if key not in mc:mc[key]=label(spans[a]&spans[b])
        return mc[key]
    const=lambda f:-f-1
    fixed=lambda n:-n-1
    ops=list(range(1,73)) if op=='all' else [op]
    # Optimistic relaxation: each nontrivial occurrence has an independent G.
    # No claim that these choices share the original physical operator.
    selected_ops={i:1000+i for i,e in enumerate(p) if e[0]=='warp'}
    fixed_lines={}
    oldstart=c['start'][:]
    current=[const(f) for f in c['start']];edges=[];original={};variables=[];free_records={}
    starts={len(p)+r:r for r in range(224,632)}
    for node,r in starts.items():
        variables.append(node);original[node]=c['start'][r];current[r]=node
    def edge(a,b):
        if isinstance(a,tuple):
            edges.append((a[0],b,('free',a[1])));free_records[a[1]]=(a[0],b)
        else:edges.append((a,b,'normal'))
    for i,e in enumerate(p):
        rs=roles(e)
        if e[0]=='scalar' and rs:
            g=e[1];allL=all(r[0]=='L' for r in (g[1:3] if g[0] in ('add','copy') else g[1:2]))
            node=i if allL else const(e[2])
            if allL:variables.append(i);original[i]=e[2]
            for r in rs:edge(current[r],node);current[r]=node
        elif e[0]=='warp':
            r=e[1][1]
            if i in selected_ops:current[r]=(current[r][0] if isinstance(current[r],tuple) else current[r],selected_ops[i])
            else:edge(current[r],const(e[3]));current[r]=const(e[4])
    for r,f in enumerate(c['final']):edge(current[r],const(f))
    incoming=defaultdict(list);outgoing=defaultdict(list)
    for a,b,k in edges:
        if k=='normal':incoming[b].append(a);outgoing[a].append(b)
    lower={};upper={}
    for n in variables:
        z=0
        for a in incoming[n]:z=join(z,lower[a] if a>=0 else fixed(a))
        lower[n]=z
    for n in reversed(variables):
        z=1
        for b in outgoing[n]:z=meet(z,upper[b] if b>=0 else fixed(b))
        if n in starts:z=meet(z,c['final'][starts[n]])
        upper[n]=z
    domain={};cache={};counts=Counter()
    for n in [v for v in variables if v not in starts]+list(starts):
        lo,hi=lower[n],upper[n];key=lo,hi
        F.need(spans[lo]<=spans[original[n]]<=spans[hi],'Original scalar in relaxed interval')
        if key not in cache:
            qs={};choices=complete_interval(spans,dims,c['frames'],(lo,),(hi,),qs,max_gap=5)
            counts.update(qs)
            # Wide intervals use a bounded, explicitly incomplete catalogue.
            if qs.get('skipped_large_interval') and len(choices)>128:
                choices=sorted(choices,key=lambda f:(dims[f],f));step=max(1,len(choices)//120);choices=choices[::step][:120]+[lo,hi]
                counts['catalogue_truncated']+=1
            cache[key]=choices
        domain[n]=list(dict.fromkeys(cache[key]+[original[n]]))
        if n in starts:
            final=c['final'][starts[n]]
            domain[n]=[f for f in domain[n] if spans[f]<spans[final]]
            F.need(original[n] in domain[n],'Original strict productive helper remains feasible')
    aliases={n:const(v[0]) for n,v in domain.items() if len(v)==1}
    E=Counter((aliases.get(a,a),aliases.get(b,b),k) for a,b,k in edges)
    active={n:v for n,v in domain.items() if len(v)>1}
    print('MODEL_DOMAINS',op,len(active),sum(map(len,active.values())),dict(counts),flush=True)
    costs=[];integrality=[];nodevars={};rows=[];cols=[];data=[];lb=[];ub=[]
    def newvar(cost,integer=False):
        i=len(costs);costs.append(cost);integrality.append(int(integer));return i
    def constraint(coefs,target):
        r=len(lb);lb.append(target);ub.append(target)
        for v,a in coefs.items():
            if a:rows.append(r);cols.append(v);data.append(a)
    for n,choices in active.items():
        nodevars[n]={f:newvar(0.,True) for f in choices};constraint({v:1 for v in nodevars[n].values()},1)
    t=1-.00302157135;weight=[0.]+[r**t-r for r in range(1,10)];constant=0.;old_objective=0.
    oldhelpers=Counter(dims[c['final'][r]]-dims[oldstart[r]] for r in range(224,632))
    for node,r in starts.items():
        enddim=dims[c['final'][r]];old_objective-=weight[enddim-dims[oldstart[r]]]
        if node in active:
            for f,v in nodevars[node].items():costs[v]-=weight[enddim-dims[f]]
        else:constant-=weight[enddim-dims[domain[node][0]]]
    def oldframe(n):return original[n] if n>=0 else fixed(n)
    for (a,b,kind),multiplicity in E.items():
        A=active[a] if a>=0 else [fixed(a)];B=active[b] if b>=0 else [fixed(b)]
        # The retained native grammar has no zero-rank frame-retag event.
        # Keep identical frame IDs on zero-rank ordinary edges; a same-span
        # different-gauge monomial is outside this bounded discovery model.
        def valid(f,g):
            if kind=='normal':return f==g or spans[f]<spans[g]
            if dims[f]>dims[g]:return False
            restriction=fixed_lines.get(kind[1])
            if restriction is None:return True
            la,lb=restriction;inside=la in spans[f]
            if inside:return lb in spans[g]
            return lb not in spans[g] or dims[f]<dims[g]
        of,og=oldframe(a),oldframe(b);F.need(valid(of,og),'Original edge feasible')
        old_objective+=multiplicity*weight[dims[og]-dims[of]]
        if a<0 and b<0:constant+=multiplicity*weight[dims[B[0]]-dims[A[0]]];continue
        if a<0 or b<0:
            n=b if a<0 else a
            for f in active[n]:
                x,y=(A[0],f) if a<0 else (f,B[0]);v=nodevars[n][f]
                if not valid(x,y):constraint({v:1},0)
                else:costs[v]+=multiplicity*weight[dims[y]-dims[x]]
            continue
        margA=defaultdict(dict);margB=defaultdict(dict)
        for f,g in product(A,B):
            if not valid(f,g):continue
            v=newvar(multiplicity*weight[dims[g]-dims[f]])
            margA[f][v]=1;margB[g][v]=1
        for f,x in nodevars[a].items():constraint({**margA[f],x:-1},0)
        for g,x in nodevars[b].items():constraint({**margB[g],x:-1},0)
    print('MODEL_READY',op,len(costs),len(lb),'old',old_objective,'seconds',time.monotonic()-started,flush=True)
    matrix=csc_array((np.asarray(data,float),(np.asarray(rows,np.int32),np.asarray(cols,np.int32))),shape=(len(lb),len(costs)))
    result=milp(np.asarray(costs),integrality=np.asarray(integrality),bounds=Bounds(0,1),constraints=LinearConstraint(matrix,np.asarray(lb),np.asarray(ub)),options={'time_limit':time_limit,'mip_rel_gap':1e-10})
    row={'status':'DISCOVERY_ONLY','operator':op,'scipy':scipy.__version__,'numpy':np.__version__,'solver_status':int(result.status),'message':result.message,'variables':len(costs),'constraints':len(lb),'old_objective':old_objective,'constant':constant,'objective':None if result.fun is None else float(result.fun)+constant,'counts':dict(counts),'seconds':time.monotonic()-started}
    row['scope']='Optimistic independent-map discovery only; no common-G or physical word claim'
    row['relaxed_gain']=None if result.fun is None else old_objective-float(result.fun)-constant
    (HERE/'RESULT.json').write_text(json.dumps(row,indent=2)+'\n')
    print(json.dumps(row,indent=2))

if __name__=='__main__':main('all',90)
