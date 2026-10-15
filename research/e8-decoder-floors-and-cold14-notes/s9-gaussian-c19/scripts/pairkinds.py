"""2x2 support lemma data: kinds (Xs, Ys) with Xs, Ys nonempty subsets of {a,b} (a,b non-orthogonal lines).
A total of kind (Xs,Ys) contributes w u^T with supp w <= Xs, supp u <= Ys.  B[{a,b},{a,b}] = I_2 is required.
Brute force: minimal multisets of kinds (size <= 4) for which I_2 is reachable.  Feasibility is monotone under adding totals."""
import itertools, pickle
import numpy as np
subs=[(0,),(1,),(0,1)]
kinds=[(x,y) for x in subs for y in subs]
def vecs(s): return [v for v in itertools.product((0,1),repeat=2) if all(v[i]==0 for i in range(2) if i not in s)]
I=np.eye(2,dtype=int)
def feasible(ms):
    opts=[[(np.array(w),np.array(u)) for w in vecs(kinds[k][0]) for u in vecs(kinds[k][1])] for k in ms]
    for ch in itertools.product(*opts):
        S=sum((np.outer(w,u) for w,u in ch),np.zeros((2,2),int))%2
        if (S==I).all(): return True
    return False
minimal=[]
for size in range(1,5):
    for ms in itertools.combinations_with_replacement(range(9),size):
        if any(all(ms.count(k)>=m.count(k) for k in set(m)) for m in minimal): continue
        if feasible(ms): minimal.append(ms)
print(len(minimal),'minimal feasible kind-multisets:')
for m in minimal: print('  ',[kinds[k] for k in m])
pickle.dump({'kinds':kinds,'minimal':minimal},open('pairkinds.pkl','wb'))
