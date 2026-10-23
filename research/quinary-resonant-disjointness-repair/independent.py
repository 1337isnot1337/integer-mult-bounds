"""Separate literal Kronecker construction and column-space rank on the first resonant source."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent

def need(v,s):
    if not v:raise ValueError(s)
def column_rank(a):
    basis={}
    for col in zip(*a):
        v=[x%5 for x in col]
        for pivot,w in sorted(basis.items()):
            q=v[pivot];v=[(x-q*y)%5 for x,y in zip(v,w)]
        pivot=next((i for i,x in enumerate(v) if x),None)
        if pivot is not None:
            inv=pow(v[pivot],-1,5);basis[pivot]=[x*inv%5 for x in v]
    return len(basis)
T=[[1]];K=[[1,1],[1,0]]
for _ in range(4):T=[[a*b%5 for a in row for b in small] for row in T for small in K]
M=[[(int(i==j)-T[i][j])%5 for j in range(16)] for i in range(16)];B=[r[1:-1] for r in M[1:-1]]
need(column_rank(M)==10 and column_rank(B)==9,'independent tensor/deletion ranks')
# Complete kernel census of the 4x4 tensor J2⊗J2−I.
L=[[0,1,1,1],[0,0,0,1],[0,0,0,1],[0,0,0,0]]
count=0
for n in range(625):
    v=[n//5**j%5 for j in range(4)]
    count+=int(all(sum(x*y for x,y in zip(row,v))%5==0 for row in L))
need(count==25,'independent two-block kernel census')
s=json.loads((P/'SOURCES.json').read_text());rows=[r for r in s['files'] if r['usage']=='input'];need(len(rows)==2,'source list')
for r in rows:need(hashlib.sha256((P.parents[1]/r['path']).read_bytes()).hexdigest()==r['sha256'],'source bytes')
r=json.loads((P/'RESULT.json').read_text());need(type(r['no_physical_supplier'])is bool and r['no_physical_supplier'],'typed scope')
need(r['fixtures'][0]['rank']==9,'receipt fixture')
print('PASS_INDEPENDENT_QUINARY_TENSOR_AND_KERNEL')
