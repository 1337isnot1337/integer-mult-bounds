"""Strict full paid-minus-helper moment improvement, on every0<t<1."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json,gzip,importlib.util,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
if sys.flags.optimize:raise RuntimeError('Run without -O')
a=json.load(gzip.open(HERE/'BASE-WORD.json.gz'));b=json.load(gzip.open(HERE/'ACTUAL-WORD.json.gz'))
def invoice(x):
 c=x['canonical'];P=Counter(e[-1] for e in x['programs']['forward'] if e[0] in ('climb','center'))
 H=Counter(len(c['frames'][c['final'][r]])-len(c['frames'][c['start'][r]]) for r in range(224,632));return P,H
P,H=invoice(b);P0,H0=invoice(a);coeff={r:P[r]-H[r]-P0[r]+H0[r] for r in set(P)|set(H)|set(P0)|set(H0)};coeff={r:n for r,n in coeff.items() if n}
assert coeff=={1:-1,2:-2,3:5,4:-7,5:4,7:1,9:-1} and sum(r*n for r,n in coeff.items())==0
path=ROOT/'research/higher-moment-strictification/verify.py';spec=importlib.util.spec_from_file_location('joint_gain_intervals',path);E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
bounds=[]
for i in range(256):
 l,r=Q(i,256),Q(i+1,256);v=Q(0)
 for rank,n in coeff.items():
  z=E.mul(E.power(rank,l if n>0 else r),E.log_bounds(rank));v+=n*z[0 if n>0 else 1]
 assert v>0,(i,float(v));bounds.append(str(v))
out=dict(status='PASS_UNIFORM_FULL_MOMENT_GAIN_OVER_PR4626',new_minus_old_paid_minus_helpers=coeff,delta_at_one=0,delta_at_zero=sum(coeff.values()),cover_intervals=256,derivative_lower_bounds=bounds,minimum_derivative_lower_bound=str(min(map(Q,bounds))),global_multiplier=18,conclusion='The net cost difference is strictly increasing on[0,1] and zero at1, hence strictly negative for every0<t<1. All helper credit changes are included.')
p=HERE/'UNIFORM-GAIN.json'
if '--check' in sys.argv:assert json.load(open(p))==json.loads(json.dumps(out))
else:p.write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],float(min(map(Q,bounds))))
