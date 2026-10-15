"""Rank-maximal flat-pair types with deficit <= 384 (any total of a cost<=42 decoder can be replaced, for the clique-covering
relaxation, by its span pair, then by a rank-maximal enlargement: hits only grow, rank (cost) unchanged)."""
import pickle, numpy as np
d=pickle.load(open('hits_table.pkl','rb')); fl=d['fl']; R=d['R']; H=d['hits']; C=d['C']
n=len(fl); L=[set(f) for f,dd in fl]
sup=[[j for j in range(n) if L[i] < L[j]] for i in range(n)]
D=192*R-H
ok=(R>0)&(D<=384)
enlX=np.zeros((n,n),bool); enlY=np.zeros((n,n),bool)
for i in range(n):
    if sup[i]:
        enlX[i]=(R[sup[i],:]==R[i][None,:]).any(0)
        enlY[:,i]=(R[:,sup[i]]==R[:,i][:,None]).any(1)
mx=ok&~enlX&~enlY
ts=np.argwhere(mx); print('types',len(ts))
from collections import Counter
print(Counter((len(fl[a][0]),len(fl[b][0]),int(R[a,b]),int(D[a,b])) for a,b in ts).most_common())
pickle.dump({'types':ts,'R':R[mx],'D':D[mx]},open('types.pkl','wb'))
