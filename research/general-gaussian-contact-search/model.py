#!/usr/bin/env python3
"""Exact contact graph and Gaussian rank invoices; Apache-2.0.

Substantial OpenAI Codex assistance. Credit PR4672 contact cuts, PR4654
Clifford chart grammar, PR4610 native words and the retained PR4470 lineage.
"""
from collections import Counter
from pathlib import Path
import gzip,json
def need(x,s):
    if not x:raise ValueError(s)

def span(b):
    s={0}
    for x in b:s|={y^x for y in tuple(s)}
    return s

def mv(cols,x):
    y=0
    for i,a in enumerate(cols):
        if x>>i&1:y^=a
    return y

def inv(cols):
    values={mv(cols,x):x for x in range(512)}
    need(len(values)==512,'invertible G')
    return [values[1<<i] for i in range(9)]

def graph(payload,mode):
    c=payload['canonical'];frames=c['frames'];sp=list(map(span,frames))
    nodes=[0,0];edges=[];fixed={};rewards=[]
    def new(f,freeze=False):
        n=len(nodes);nodes.append(f)
        if freeze:fixed[n]=0
        return n
    cur=[new(f,r<224 or mode=='exits') for r,f in enumerate(c['start'])]
    entry=cur[:]
    def move(r,f,dst=None):
        a=cur[r];old=nodes[a]
        need(sp[old]<=sp[f],f'nested {r}:{old}->{f}')
        b=new(f) if dst is None else dst
        edges.append(('paid',a,b,len(frames[f])-len(frames[old]),tuple(frames[old])))
        cur[r]=b
    maps={x['op']:x['G_columns'] for x in c['warps']}
    maps.update({-op:inv(cols) for op,cols in list(maps.items())})
    for e in payload['programs']['forward']:
        if e[0]=='climb':
            _,_,r,a,b,width=e
            need(sp[a]<sp[b] and width==len(frames[b])-len(frames[a]),'original paid rank and nesting')
            continue
        if e[0]=='scalar':
            g,f=e[1:];refs=g[1:3] if g[0] in ('add','copy') else g[1:2]
            owned=any(r[0]!='L' for r in refs);contact=new(f,owned)
            for typ,r in refs:
                if typ=='L':move(r,f,contact)
        elif e[0]=='warp':
            _,role,op,a,b=e;need(role[0]=='L','persistent warp')
            r=role[1];move(r,a);src=cur[r];dst=new(b)
            edges.append(('warp',src,dst,tuple(frames[a]),tuple(mv(maps[op],v) for v in frames[a])))
            cur[r]=dst
        elif e[0]=='adapter':
            fixed[cur[e[2]]]=0
        elif e[0]=='center':
            _,_,a,b,width=e
            need(sp[a]<sp[b] or sp[b]<sp[a],'original owned-center nesting')
            need(width==abs(len(frames[b])-len(frames[a])),'original owned-center rank')
        else:need(e[0]=='phase','known chronological event')
    for r,f in enumerate(c['final']):
        dst=new(f,r<224 or mode=='entrances');move(r,f,dst)
        if r>=224:
            a,b=c['start'][r],f;need(sp[a]<=sp[b],'nested helper boundary')
            rewards.append((entry[r] if mode=='entrances' else dst,
                            len(frames[b])-len(frames[a]),tuple(frames[a])))
    return nodes,edges,fixed,rewards

def mask(space):
    return sum(1 << x for x in space)

def dimension(bits):
    n = bits.bit_count()
    need(n > 0 and n & (n-1) == 0, 'binary subspace size')
    return n.bit_length()-1

def fourier_rank(a, b):
    return dimension(a)+dimension(b)-2*dimension(a & b)

def load(path):
    raw = Path(path).read_bytes()
    return json.loads(gzip.decompress(raw) if str(path).endswith('.gz') else raw)

def build(payload, functionals):
    """All paid edges, including old zero edges, and both helper endpoints."""
    nodes, edges, fixed, _ = graph(payload, 'free')
    frames = payload['canonical']['frames']
    old = [mask(span(b)) for b in frames]
    kernel = mask(x for x in range(512)
                  if all((l & x).bit_count() % 2 == 0 for l in functionals))
    new = [s & kernel for s in old]
    tables = []
    for kind, a, b, x, y in edges:
        left = (old[nodes[a]], new[nodes[a]])
        right = (old[nodes[b]], new[nodes[b]])
        if kind == 'warp':
            image = {0: 0}
            for u, v in zip(x, y):
                image.update({z ^ u: w ^ v for z, w in list(image.items())})
            left = tuple(mask(image[z] for z in image if s >> z & 1) for s in left)
        ranks = [fourier_rank(left[i], right[j]) for i,j in ((0,0),(1,0),(0,1),(1,1))]
        if kind == 'warp': need(ranks[0] == 0, 'original native warp is monomial')
        tables.append((kind, a, b, ranks))
    helpers = []
    for r in range(224, 632):
        a, b = 2+r, len(nodes)-632+r
        left = (old[nodes[a]], new[nodes[a]])
        right = (old[nodes[b]], new[nodes[b]])
        ranks = [fourier_rank(left[i], right[j]) for i,j in ((0,0),(1,0),(0,1),(1,1))]
        helpers.append((r, a, b, ranks))
    centers = Counter(e[4] for e in payload['programs']['forward'] if e[0] == 'center')
    source_paid = Counter(e[5] for e in payload['programs']['forward'] if e[0] == 'climb') + centers
    result = dict(nodes=nodes, fixed=sorted(fixed), edges=tables, helpers=helpers,
                  centers=dict(centers), old_spaces=old, new_spaces=new)
    p,h = invoice(result, [])
    need(p == source_paid, 'reconstructed baseline invoice')
    return result

def invoice(model, selected):
    chosen = set(selected)
    need(not chosen.intersection(model['fixed']), 'main, adapter and owned boundaries frozen')
    need(all(2 <= n < len(model['nodes']) for n in chosen), 'valid selected contact')
    paid = Counter(model['centers'])
    helper = Counter()
    def rank_at(a, b, ranks):
        return ranks[(a in chosen)+2*(b in chosen)]
    for _,a,b,ranks in model['edges']:
        r=rank_at(a,b,ranks)
        if r: paid[r] += 1
    for _,a,b,ranks in model['helpers']:
        r=rank_at(a,b,ranks)
        need(r > 0, 'strict productive helper')
        helper[r] += 1
    return paid, helper

