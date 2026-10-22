#!/usr/bin/env python3
"""Independent exact rank control, not execution of PR4813's paid schedule."""
from fractions import Fraction as F
import json
from pathlib import Path
Z=(F(0),F(0)); O=(F(1),F(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def neg(a):return (-a[0],-a[1])
def inv(a):
 d=a[0]**2+a[1]**2
 if not d:raise ValueError('zero pivot')
 return (a[0]/d,-a[1]/d)
def need(p,m):
 if not p:raise ValueError(m)
def rank(a):
 a=[list(r) for r in a]; k=0
 for j in range(len(a[0])):
  p=next((r for r in range(k,len(a)) if a[r][j]!=Z),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k]; v=inv(a[k][j]);a[k]=[mul(v,x) for x in a[k]]
  for r in range(len(a)):
   if r!=k and a[r][j]!=Z:
    c=a[r][j];a[r]=[add(x,neg(mul(c,y))) for x,y in zip(a[r],a[k])]
  k+=1
 return k
# A = C0 = ((1+i)I + (1-i)X0)/2, independently reconstructed.
a=[[(F(1,2),F(1,2)) if r==c else ((F(1,2),F(-1,2)) if r==(c^1) else Z) for c in range(8)] for r in range(8)]
for r in range(8):
 for c in range(8):
  v=Z
  for k in range(8):v=add(v,mul((a[k][r][0],-a[k][r][1]),a[k][c]))
  need(v==(O if r==c else Z),'C0 is not unitary')
bottom=[[a[r%8][c%8] if r//8==c//8 else Z for c in range(40)] for r in range(40)]
zero_top=[[Z]*40 for _ in range(40)]
need(rank(bottom)==40,'retained diagonal observations lost rank')
need(rank(zero_top+bottom)==40,'zeroing all claimed v/w rows changed full rank')
mut=[r[:] for r in bottom]
for r in range(32,40):mut[r]=[Z]*40
need(rank(zero_top+mut)==32,'negative control failed to detect a missing input bank')
result={'status':'PASS_PR4813_RANK_CONTROL','source_pr':4813,'source_head':'9e33ecf009d36118f49ac86e9a0ee36e38dca44f','A_dimension':8,'A_unitary':True,'retained_observation_rank':40,'rank_with_all_v_and_w_rows_zero':40,'rank_with_one_retained_bank_removed':32,'paid_schedule_executed':False,'new_kappa':False}
expected=Path(__file__).with_name('CHECKS.json')
if expected.exists():need(json.loads(expected.read_text())==result,'frozen receipt mismatch')
print(json.dumps(result,sort_keys=True))
