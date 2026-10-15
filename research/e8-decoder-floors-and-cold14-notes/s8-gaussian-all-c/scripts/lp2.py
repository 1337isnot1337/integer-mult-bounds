import pickle, numpy as np, networkx as nx
from scipy.optimize import linprog
from lines import views
S=views()['Gauss']; NO=S.NO
d=pickle.load(open('hits_table.pkl','rb')); fl=d['fl']; R=d['R']; H=d['hits']
n=len(fl); v=60
L=np.zeros((n,v),np.int64)
for i,(f,dd) in enumerate(fl): L[i,sorted(f)]=1
dims=np.array([dd for f,dd in fl])
g=nx.Graph([(i,j) for i in range(v) for j in range(i+1,v) if NO[i,j]])
cl=list(nx.find_cliques(g))
fams={}
def famhits(sets):
    inc=np.zeros((v,len(sets)),np.int64)
    for k,s in enumerate(sets): inc[list(s),k]=1
    meet=(L@inc>0).astype(np.int64); return meet@meet.T
from collections import Counter
print(Counter(len(c) for c in cl))
for s in sorted(set(len(c) for c in cl)):
    sets=[c for c in cl if len(c)==s]; fams['clq%d'%s]=(famhits(sets),s,len(sets))
fams['line']=(famhits([[T] for T in range(v)]),1,60)
for dd in (1,2,3):
    idx=np.where(dims==dd)[0]
    inc=((L@L[idx].T)==L.sum(1)[:,None]).astype(np.int64)
    a=inc.sum(1); N=len(idx)-a[:,None]-a[None,:]+inc@inc.T
    fams['cmp%d'%dd]=(N,15,len(idx))
fams['all']=(((L.sum(1)[:,None]>0)&(L.sum(1)[None,:]>0)).astype(np.int64),15,1)
names=list(fams); print(names)
mask=R>0
rows=np.stack([fams[k][0][mask] for k in names],1); rr=R[mask]
u=np.unique(np.concatenate([rows,rr[:,None]],1),axis=0); print('rows',len(u))
dem=np.array([fams[k][1]*fams[k][2] for k in names],float)
# vars: y (per family, uniform), mu>=0 ; constraint rows: hits.y - mu <= r ; maximize dem.y - c*mu
for c in (17,18,19,20,22,25,30,42):
    obj=np.concatenate([-dem,[c]])
    A=np.concatenate([u[:,:-1],-np.ones((len(u),1))],1)
    res=linprog(obj,A_ub=A,b_ub=u[:,-1],bounds=[(0,None)]*(len(names)+1),method='highs')
    y=res.x; print(c, round(-res.fun,4), {names[i]:round(y[i],5) for i in range(len(names)) if y[i]>1e-9}, 'mu',round(y[-1],4))
