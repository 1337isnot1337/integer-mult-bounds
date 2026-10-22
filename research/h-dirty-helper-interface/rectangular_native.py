"""Emit a dyadic sixteen-state J interface, not a completed recursive caller."""
from pathlib import Path
from fractions import Fraction as Q
import json,gzip,sys
if not __debug__: raise RuntimeError('Assertions required')
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/joint-helper-lattice'));import native_joint as NJ
F=NJ.F; V=F.load(ROOT/'research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py','rect_native_rows'); X=F.load(ROOT/'research/kappa-rebuild/complex/native_extensions.py','rect_native_eval')
a=F.read(HERE/'EIGHT-STATE-WORD.json.gz'); c=a['canonical']; original=F.read(HERE/'sources/NATIVE.json.gz')
roles=[r for r in range(224,632) if c['start'][r]==0 and c['final'][r]==1][:16]
E=[[Q(x) for x in row] for row in json.loads((HERE/'RECTANGULAR.json').read_text())['basis_change']]
def inverse(seq):
 return [(k,d,s,-q if k=='add' else 1/q if k=='scale' else q) for k,d,s,q in reversed(seq)]
def transpose(seq):
 return [(k,s if k=='add' else d,d if k=='add' else s,q) for k,d,s,q in reversed(seq)]
def factor(A):
 M=[r[:] for r in A]; n=len(M);ops=[]
 def apply(k,d,s,q):
  if k=='add': M[d]=[x+q*y for x,y in zip(M[d],M[s])]
  elif k=='scale': M[d]=[q*x for x in M[d]]
  else: M[d],M[s]=M[s],M[d]
  ops.append((k,d,s,q))
 for j in range(n):
  for i in range(j,n):
   den=max(x.denominator for x in M[i]);assert den&(den-1)==0
   if den!=1:apply('scale',i,i,Q(den))
  p=next(i for i in range(j,n) if M[i][j])
  if p!=j:apply('swap',j,p,Q(1))
  for i in range(j+1,n):
   while M[i][j]:
    q=-(M[i][j]//M[j][j])
    if q:apply('add',i,j,Q(q))
    if M[i][j]:apply('swap',i,j,Q(1))
  pivot=M[j][j];assert abs(pivot.numerator)&(abs(pivot.numerator)-1)==0
  if pivot!=1:apply('scale',j,j,1/pivot)
  for i in range(n):
   if i!=j and M[i][j]:apply('add',i,j,-M[i][j])
 assert M==[[Q(i==j) for j in range(n)] for i in range(n)]
 return inverse(ops)
def emit(seq,frame):
 out=[]
 def add(d,s,q):out.append(['scalar',['add',['L',roles[d]],['L',roles[s]],q.numerator,q.denominator],frame])
 def scale(d,q):out.append(['scalar',['scale',['L',roles[d]],q.numerator,q.denominator],frame])
 for k,d,s,q in seq:
  assert q.denominator&(q.denominator-1)==0
  if k=='add':add(d,s,q)
  elif k=='scale':scale(d,q)
  else:
   add(d,s,Q(1));scale(s,Q(-1));add(s,d,Q(1));add(d,s,Q(-1))
 return out
N=F.load(ROOT/'research/kappa-rebuild/complex/rebuild_native.py','rect_native_geometry');geo=N.geometry(F.read(ROOT/'research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder/sources/certificate.json.gz'))
R=[[2*geo['L'][k].get(p,Q(0)) if p not in geo['selected'] else Q(2*(p==s)) for p in range(112)] for k,s in enumerate(geo['selected'])]
e=factor(E); U=[('add',i,8+i,Q(2)) for i in range(8)]; W=[('add',8+i,i,Q(-2)) for i in range(8)]
newwords={};receipts={}
for direction,word in a['programs'].items():
 source=original[direction]; start=source.index(['phase','fresh_H112_completion']);end=next((i for i in range(start+1,len(source)) if source[i][0]=='phase'),len(source)); completion=source[start:end]
 i=word.index(['phase','fresh_H112_completion']);assert word[i:i+len(completion)]==completion
 core=word[:i]+word[i+len(completion):]
 if direction=='forward':pre=U+e;post=inverse(pre)
 else:post=transpose(e)+W;pre=inverse(post)
 new=emit(pre,0)+core+emit(post,1)+[['scalar',['clear',['C',0]],0]]
 rows,receipt=X.literal_replay(V,c,new,direction=='backward')
 expected={('L',r):V.identity(('L',r)) for r in range(632)}
 for p in range(112):
  dst=p if direction=='backward' else 112+p;offset=112 if direction=='backward' else 0;sign=-1 if direction=='backward' else 1
  for q,value in geo['J'][p].items():V.add(expected['L',dst],V.identity(('L',offset+q)),sign*value)
  for k in range(8):
   if direction=='forward':
    V.add(expected['L',dst],V.identity(('L',roles[k])),R[k][p]);V.add(expected['L',dst],V.identity(('L',roles[k+8])),2*R[k][p])
   else:
    V.add(expected['L',roles[k]],V.identity(('L',112+p)),-R[k][p]);V.add(expected['L',roles[k+8]],V.identity(('L',112+p)),2*R[k][p])
 bad=[r for r in range(632) if rows['L',r]!=expected['L',r]];assert not bad,bad[:10]
 assert receipt['paid_profile']=={1:2237,2:388,3:494,4:147,5:36}
 expected_paid=[x for x in core if x[0] in ('climb','warp','center')]; assert [x for x in new if x[0] in ('climb','warp','center')]==expected_paid
 newwords[direction]=new;receipts[direction]=receipt
 print('RECTANGULAR_NATIVE',direction,'all 632 columns exact',flush=True)
out=dict(status='EXACT_TYPED_SIXTEEN_STATE_J_INTERFACE',state_roles=roles,remaining_clean_helpers=392,remaining_clean_rank9_helpers=310,basis_E_elementary_operations=len(e),receipts=receipts,forward='Y += J X + Rt u + 2 Rt v',backward='X -= J Y; u -= R Y; v += 2 R Y',not_raw_inverse_transposes=True,missing=['Gaussian width-nine states versus width-eight main jobs','Global controller','State restoration and independent target credit','Full rounding/compiler/outer integration'],no_kappa_claim=True)
artifacts={'RECTANGULAR-NATIVE.json':(json.dumps(out,indent=2)+'\n').encode(),'RECTANGULAR-NATIVE-WORD.json.gz':gzip.compress(json.dumps(dict(canonical=c,programs=newwords),sort_keys=True,separators=(',',':')).encode(),mtime=0)}
for name,data in artifacts.items():
 if '--check' in sys.argv:assert (HERE/name).read_bytes()==data,name
 else:(HERE/name).write_bytes(data)
