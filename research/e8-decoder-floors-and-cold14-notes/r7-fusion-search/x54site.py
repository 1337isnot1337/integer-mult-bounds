import sys; sys.path.insert(0,'.')
import harness as C, repair as R, fusion as G
from exchange import copy_pairs, movable_reads
F=sys.argv[1]
R.init(F); w=R.P.base
h=589; r,ic=copy_pairs(w)[h]; print('pair',h,r,ic, 'movable', movable_reads(w,h,r,ic))
cs=[c for c in G.candidates(w) if 54 in (c['A'],c['H']) or 589 in (c['A'],c['H'])]
print('fusions touching 54/589:',len(cs))
best=[]
for c in cs:
    x=R.repair(c)
    if x['best']: best.append((x['best']['delta'],c['t'],c['A'],c['H'],c['p'],c['rest'],x['best']['steps']))
for b in sorted(best)[:15]: print(b)
