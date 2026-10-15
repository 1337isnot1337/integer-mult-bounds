"""Exact check: the 21 dumbbell totals (l^perp, m^perp), l ⊥ m (beta = 2 each, cost 42) found by tight_ilp.py 21 hit every
12-clique >= 12 times, i.e. the clique-covering relaxation is integrally feasible at c = 21, cost 42."""
import pickle, numpy as np
from lines import views
S=views()['Gauss']; NO=S.NO
C=pickle.load(open('hits_table.pkl','rb'))['C']
D=[(0,13),(4,22),(5,50),(6,19),(6,28),(7,38),(8,19),(11,56),(12,17),(18,37),(18,58),(20,30),(21,33),(25,26),(35,55),(36,45),(37,47),(41,44),(42,51),(44,51),(48,53)]
perp=lambda l: {T for T in range(60) if T!=l and not NO[l,T]}
assert all(not NO[a,b] and a!=b for a,b in D)
N=[sum(1 for a,b in D if perp(a)&set(c) and perp(b)&set(c)) for c in C]
print('c = 21 dumbbell cover: cost', 2*len(D), 'min clique hits', min(N), 'max', max(N), 'PASS' if min(N)>=12 else 'FAIL')
