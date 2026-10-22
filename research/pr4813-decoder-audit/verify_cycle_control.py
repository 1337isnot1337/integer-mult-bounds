#!/usr/bin/env python3
"""Exact Rayleigh-quotient controls for the published half-XOR cycles."""
from fractions import Fraction as F
import json
from pathlib import Path
def need(ok,msg):
 if not ok:raise ValueError(msg)
def norm2(x):return sum(v*v for b in x for v in b)
def apply(x,masks):
 w=len(x)
 return [[x[k][j]+F(1,2)*x[(k+1)%w][j^masks[k]] for j in range(len(x[0]))] for k in range(w)]
def check(masks,claimed,n=16):
 w=len(masks);plus=[[F(1)]*n for _ in range(w)];alt=[[F((-1)**k)]*n for k in range(w)]
 large=norm2(apply(plus,masks))/norm2(plus)
 small=norm2(apply(alt,masks))/norm2(alt)
 need(large==F(9,4),'constant-vector quotient')
 need(small==F(w+8,4*w),'alternating-vector quotient')
 bound=large/small
 need(bound>claimed*claimed,'published whole-cycle condition bound was not refuted')
 # Independently preserve the distinction: the loop-only Neumann bound can hold.
 need(claimed==(1+F(1,2)**w)/(1-F(1,2)**w),'wrong Schur-loop comparison')
 return {'arrays':w,'coordinates_per_array':n,'masks':masks,'large_rayleigh':str(large),'small_rayleigh':str(small),'condition_squared_lower_bound':str(bound),'claimed_whole_cycle_bound':str(claimed),'claimed_bound_refuted':True}
r={'status':'PASS_BLOCK4_CYCLE_CONDITION_CONTROLS','pr4818':check([1,2,4],F(9,7)),'pr4819':check(list(range(1,14)),F(8193,8191)),'pr4826':check([1,2,4],F(9,7),32),'paid_schedule_executed':False,'new_kappa':False}
p=Path(__file__).with_name('CYCLE-CHECKS.json')
if p.exists():need(json.loads(p.read_text())==r,'receipt mismatch')
print(json.dumps(r,sort_keys=True))
