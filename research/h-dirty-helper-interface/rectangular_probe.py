"""Test a dyadic rectangular inverse for the uncompleted J interface."""
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions required")
from fractions import Fraction as Q
import json,ast,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/joint-helper-lattice'));import native_joint as J
F=J.F;N=F.load(ROOT/'research/kappa-rebuild/complex/rebuild_native.py','rect_geometry');packet=F.read(ROOT/'research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder/sources/certificate.json.gz');geo=N.geometry(packet)
a=json.loads((HERE/'EIGHT-STATE.json').read_text());roles=a['state_roles'];B=[[Q(0) for _ in range(8)] for _ in range(112)]
for e in a['differences']['forward']:B[e['output']-112][roles.index(ast.literal_eval(e['input'])[0][1])]=Q(e['coefficient'])
R=[[2*geo['L'][k].get(p,Q(0)) if p not in geo['selected'] else Q(2*(p==s)) for k,s in enumerate(geo['selected'])] for p in range(112)]
def inv(A):
 n=len(A);M=[list(row)+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
 for j in range(n):
  k=next(i for i in range(j,n) if M[i][j]);M[j],M[k]=M[k],M[j];q=M[j][j];M[j]=[x/q for x in M[j]]
  for i in range(n):
   if i!=j:
    q=M[i][j];M[i]=[x-q*y for x,y in zip(M[i],M[j])]
 return [r[n:] for r in M]
def mul(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
ind=[];piv={}
for i,row in enumerate(B):
 v=row[:]
 for k,b in piv.items():
  q=v[k];v=[x-q*y for x,y in zip(v,b)]
 k=next((k for k,x in enumerate(v) if x),None)
 if k is not None:
  q=v[k];piv[k]=[x/q for x in v];ind.append(i)
assert len(ind)==8
E=mul(inv([B[i] for i in ind]),[R[i] for i in ind]);EI=inv(E);assert mul(B,E)==R
def dyadic(A):return all(not(x.denominator&(x.denominator-1)) for row in A for x in row)
# R^T R = 4(I-J); R R^T=56 I. Thus J^2-3 R^T R=I.
Rt=list(map(list,zip(*R)));G=mul(R,Rt);JJ=[[geo['J'][i].get(j,Q(0)) for j in range(112)] for i in range(112)]
assert G==[[4*(Q(i==j)-JJ[i][j]) for j in range(112)] for i in range(112)]
assert mul(Rt,R)==[[Q(56*(i==j)) for j in range(8)] for i in range(8)]
# Rectangular A=[J,R^T,2R^T], B=[J;R;-2R] has AB=I.
J2=mul(JJ,JJ);assert [[J2[i][j]-3*G[i][j] for j in range(112)] for i in range(112)]==[[Q(i==j) for j in range(112)] for i in range(112)]
out=dict(status='EXACT_RECTANGULAR_RIGHT_INVERSE_ALGEBRA',basis_change_dyadic=dyadic(E),basis_inverse_dyadic=dyadic(EI),basis_change=[[str(x) for x in row] for row in E],basis_inverse=[[str(x) for x in row] for row in EI],state_ports_required=16,left_dimension=128,right_dimension=112,identity='[J,Rt,2Rt] [J;R;-2R] = I112',missing=['Physical dual wrapper proof','Gaussian width-nine state versus width-eight main compatibility','Complete controller and state restoration'],no_kappa_claim=True)
if '--check' in sys.argv:assert json.loads((HERE/'RECTANGULAR.json').read_text())==out
else:(HERE/'RECTANGULAR.json').write_text(json.dumps(out,indent=2)+'\n')
print('RECTANGULAR',dyadic(E),dyadic(EI),flush=True)
