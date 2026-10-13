"""Maximum pairwise non-orthogonal cliques of I_{n,1} (the #595 pattern graph, G_st != 0) and their S_n orbits.
Orbits are found by isomorphism of the coloured incidence graph (clique lines x points of [n]); each class is checked
with networkx's exact VF2 isomorphism against its representative."""
import sys, itertools, json
from collections import Counter, defaultdict
import networkx as nx
import numpy as np
sys.dont_write_bytecode = True
import units as U


def lines(n):
    return list(itertools.combinations(range(n), 3)) + list(itertools.combinations(range(n), 2))


def inc_graph(n, cl, LN):
    g = nx.Graph()
    for p in range(n):
        g.add_node(('p', p), col='p')
    for t in cl:
        g.add_node(('l', t), col='T' if len(LN[t]) == 3 else 'P')
        for p in LN[t]:
            g.add_edge(('l', t), ('p', p))
    return g


def orbits(n):
    L, G, lab = U.lorentz_family(n)
    LN = lines(n)
    v = len(L)
    H = nx.Graph(); H.add_nodes_from(range(v))
    H.add_edges_from((i, j) for i in range(v) for j in range(i + 1, v) if G[i, j] != 0)
    cls = [sorted(c) for c in nx.find_cliques(H)]
    om = max(map(len, cls))
    cls = [c for c in cls if len(c) == om]
    by = defaultdict(list)
    for c in cls:
        g = inc_graph(n, c, LN)
        by[nx.weisfeiler_lehman_graph_hash(g, node_attr='col', iterations=4)].append(c)
    reps = []
    nm = lambda a, b: a['col'] == b['col']
    for hsh, cs in by.items():
        local = []
        for c in cs:
            g = inc_graph(n, c, LN)
            for r in local:
                if nx.is_isomorphic(g, r[1], node_match=nm):
                    r[2].append(c); break
            else:
                local.append([c, g, [c]])
        reps += [(r[0], r[2]) for r in local]
    return om, cls, reps, LN


if __name__ == '__main__':
    n = int(sys.argv[1])
    om, cls, reps, LN = orbits(n)
    print('n=%d omega=%d maximum cliques=%d orbits=%d' % (n, om, len(cls), len(reps)))
    out = []
    for rep, mem in reps:
        typ = Counter(len(LN[t]) for t in rep)
        print('  orbit size %d: %d triples + %d pairs, rep %s' % (len(mem), typ[3], typ[2], [LN[t] for t in rep]))
        out.append(dict(size=len(mem), rep=rep, triples=typ[3], pairs=typ[2]))
    if len(sys.argv) > 2:
        json.dump(dict(n=n, omega=om, count=len(cls), orbits=out), open(sys.argv[2], 'w'), indent=1)


def survival_bound(n):
    """Union bound: k punctures kill at most k * max_t #{maximum cliques through t} cliques, so some maximum clique
    survives every puncture of k < count / max_per_line lines (then the clique gauge of punct_sat.py is WLOG up to S_n,
    run once per orbit)."""
    om, cls, reps, LN = orbits(n)
    per = Counter(t for c in cls for t in c)
    mx = max(per.values())
    kmax = (len(cls) - 1) // mx
    return dict(count=len(cls), max_per_line=mx, survive_upto=kmax, orbits=len(reps))
