"""Exact calibration of the scoped modulo-three state lower bound."""
from pathlib import Path
from fractions import Fraction as Q
import sys,json
if not __debug__:raise RuntimeError('Assertions required')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'research/joint-helper-lattice'));import native_joint as N
F=N.F;G=F.load(ROOT/'research/kappa-rebuild/complex/rebuild_native.py','minimum_geometry');g=G.geometry(F.read(ROOT/'research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder/sources/certificate.json.gz'))
R=[[2*g['L'][k].get(p,Q(0)) if p not in g['selected'] else Q(2*(p==s)) for p in range(112)] for k,s in enumerate(g['selected'])]
def mul(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def rank3(A):
 a=[[int(Q(x).numerator%3)*pow(Q(x).denominator%3,-1,3)%3 for x in row] for row in A];r=0
 for j in range(len(a[0])):
  p=next((i for i in range(r,len(a)) if a[i][j]),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];z=pow(a[r][j],-1,3);a[r]=[v*z%3 for v in a[r]]
  for i in range(len(a)):
   if i!=r:
    z=a[i][j];a[i]=[(x-z*y)%3 for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
I=[[int(i==j) for j in range(8)] for i in range(8)]
U=[row+[2*x for x in row] for row in I];V=I+[[-2*x for x in row] for row in I]
assert mul(R,list(zip(*R)))==[[56*x for x in row] for row in I]
assert mul(U,V)==[[-3*x for x in row] for row in I]
assert rank3(R)==rank3(U)==rank3(V)==8
assert rank3(mul(U,V))==0
assert rank3([[-3*x for x in row] for row in I])==0
S=[[Q(i==j)+Q(2*(i!=j)) for j in range(2)] for i in range(2)]
SI=[[Q(-1,3),Q(2,3)],[Q(2,3),Q(-1,3)]]
assert mul(S,SI)==[[1,0],[0,1]] and mul(SI,S)==[[1,0],[0,1]]
assert mul([[1,2]],SI)==[[1,0]] and mul(S,[[1],[-2]])==[[-3],[0]]
out=dict(status='SCOPED_SHARP_SIXTEEN_STATE_MINIMUM',ring='Z[1/2]',reduction_prime=3,rank_R=8,rank_U=8,rank_V=8,rank_UV=0,kernel_dimension_at_h16=8,necessary_state_dimension=16,construction_state_dimension=16,hypothesis='State couplings preserve primitive mod-three rank eight under invertible dyadic basis changes',rational_eight_state_relaxation_requires_inverse_one_third=True,rational_split_S=[[1,2],[2,1]],rational_split_inverse=[['-1/3','2/3'],['2/3','-1/3']],rational_split_physically_admitted=False,no_kappa_claim=True)
p=HERE/'STATE-MINIMUM.json'
if '--check' in sys.argv:assert json.loads(p.read_text())==out
else:p.write_text(json.dumps(out,indent=2)+'\n')
print('STATE_MINIMUM exact modulo-three ranks and attaining construction PASS')
