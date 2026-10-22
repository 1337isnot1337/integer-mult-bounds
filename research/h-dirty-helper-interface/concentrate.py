"""Concentrate the retained H helper defect into eight arbitrary state ports.
No clean-helper credit is claimed for those ports.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json,gzip,sys,ast
if not __debug__:raise RuntimeError('Assertions required')
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
from hashlib import sha256
for name,digest in json.loads((HERE/"INPUTS.json").read_text())["source_sha256"].items():
 assert sha256((HERE/"sources"/name).read_bytes()).hexdigest()==digest
sys.path.insert(0,str(ROOT/'research/joint-helper-lattice'));import native_joint as J
F=J.F;V=F.load(ROOT/'research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py','state_H_rows');X=F.load(ROOT/'research/kappa-rebuild/complex/native_extensions.py','state_H_literal')
c=F.read(HERE/'sources/CANONICAL.json.gz');words=F.read(HERE/'sources/NATIVE.json.gz');probe=F.read(HERE/'RAW-DEFECT.json.gz')
roles=[r for r in range(224,632) if c['start'][r]==0 and c['final'][r]==1];assert len(roles)==326;assert all(c['start'][r]==0 and c['final'][r]==1 for r in roles)
B=[[Q(0) for _ in roles] for _ in range(112)]
for e in probe['forward']['changes']:
 (kind,r),word=ast.literal_eval(e['input']);assert kind=='L' and not word and r in roles
 B[e['output']-112][roles.index(r)]=Q(e['coefficient'])
ops=[];k=0;pivots=[]
while True:
 found=next(((i,j) for i in range(112) for j in range(k,len(roles)) if B[i][j]),None)
 if found is None:break
 i,j=found
 if j!=k:
  for row in B:row[k],row[j]=row[j],row[k]
  ops.append(('swap',k,j,Q(1)))
 for j in range(k+1,len(roles)):
  while B[i][j]:
   q=Q(-(B[i][j]//B[i][k]))
   if q:
    for row in B:row[j]+=q*row[k]
    ops.append(('add',k,j,q))
   if B[i][j]:
    for row in B:row[k],row[j]=row[j],row[k]
    ops.append(('swap',k,j,Q(1)))
 pivots.append(str(B[i][k]))
 k+=1
assert k==8 and all(not z for row in B for z in row[8:])
def inverse(op):
 kind,a,b,q=op;return kind,a,b,-q if kind=='add' else q
def transpose(op):
 kind,a,b,q=op;return kind,b,a,q

def emit(seq,frame):
 out=[]
 for kind,a,b,q in seq:
  a,b=['L',roles[a]],['L',roles[b]]
  if kind=='add':out.append(['scalar',['add',a,b,q.numerator,q.denominator],frame])
  else:
   out.extend([['scalar',['add',a,b,1,1],frame],['scalar',['scale',b,-1,1],frame],['scalar',['add',b,a,1,1],frame],['scalar',['add',a,b,-1,1],frame]])
 return out
newwords={};receipts={};differences={}
for direction,word in words.items():
 i=word.index(['phase','zero_frame_center_compensation']);j=next(z for z in range(i+1,len(word)) if word[z][0]=='phase');raw=word[:i]+word[j:]
 if direction=='forward':pre=list(reversed(ops));post=list(map(inverse,ops))
 else:pre=[transpose(inverse(op)) for op in reversed(ops)];post=list(map(transpose,ops))
 new=emit(pre,0)+raw+emit(post,1)
 good,old=X.literal_replay(V,c,word,direction=='backward');rows,rec=X.literal_replay(V,c,new,direction=='backward')
 assert rec['paid_profile']==old['paid_profile']
 assert [e for e in new if e[0] in ('climb','warp','center')]==[e for e in word if e[0] in ('climb','warp','center')]
 delta=[]
 for r in range(632):
  keys=set(rows['L',r])|set(good['L',r])
  for key in sorted(keys):
   q=rows['L',r].get(key,0)-good['L',r].get(key,0)
   if not q:continue
   if direction=='forward':assert 112<=r<224 and key[0][0]=='L' and key[0][1] in roles[:8] and not key[1]
   else:assert r in roles[:8] and key[0][0]=='L' and 112<=key[0][1]<224 and not key[1]
   delta.append(dict(output=r,input=repr(key),coefficient=str(q)))
 differences[direction]=delta;receipts[direction]=rec;newwords[direction]=new
 print('CONCENTRATED',direction,'defect terms',len(delta),'paid unchanged',flush=True)
f={(e['output'],ast.literal_eval(e['input'])[0][1]):Q(e['coefficient']) for e in differences['forward']};b={(ast.literal_eval(e['input'])[0][1],e['output']):Q(e['coefficient']) for e in differences['backward']}
assert all(f.get(k,0)==-b.get(k,0) for k in f.keys()|b.keys())
out=dict(status='EXACT_EIGHT_STATE_PORT_INTERFACE',state_roles=roles[:8],original_affected_helpers=106,remaining_clean_helpers=400,original_clean_rank9_helpers=326,remaining_clean_rank9_helpers=318,rank=8,pivots=pivots,elementary_operations=len(ops),differences=differences,receipts=receipts,scope='Typed arbitrary state ports, not eight clean Gaussian outputs; no global closure or kappa claimed')
artifacts={
 'EIGHT-STATE.json':(json.dumps(out,indent=2)+'\n').encode(),
 'EIGHT-STATE-WORD.json.gz':gzip.compress(json.dumps(dict(canonical=c,programs=newwords),sort_keys=True,separators=(',',':')).encode(),mtime=0),
 'BASIS-OPS.json':(json.dumps([[kind,a,b,str(q)] for kind,a,b,q in ops],indent=2)+'\n').encode()}
for name,data in artifacts.items():
 if '--check' in sys.argv:assert (HERE/name).read_bytes()==data,name
 else:(HERE/name).write_bytes(data)
