"""Logical ADD merging across exactly commuting instructions; exploratory."""
from pathlib import Path
import sys,importlib.util,json
from collections import Counter
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('joint_trace_source',ROOT/'research/joint-helper-lattice/native_joint.py');J=importlib.util.module_from_spec(spec);spec.loader.exec_module(J)
c,programs,*_=J.construct()

def roles(e):
 if e[0]=='warp':return {tuple(e[1])}
 if e[0]=='scalar':
  g=e[1];return {tuple(r) for r in g[1:] if isinstance(r,list) and r and r[0] in ('L','C','W')}
 return set()
def add(e):return e[0]=='scalar' and e[1][0]=='add' and all(r[0]=='L' for r in e[1][1:3])
def commutes(a,b):
 if a[0]=='phase' or b[0]=='phase':return False
 if b[0] in ('climb','center'):return b[0]=='climb'
 if b[0]=='scalar' and b[1][0]=='add':
  _,ad,asrc,*_=a[1];_,bd,bsrc,*_=b[1]
  return ad!=bsrc and asrc!=bd
 return not(roles(a)&roles(b))
for d,p in programs.items():
 out=[];moves=[]
 for i,e in enumerate(p):
  if e[0]=='climb':continue
  if add(e):
   for j in range(len(out)-1,-1,-1):
    old=out[j]
    if add(old) and old[1][1:3]==e[1][1:3]:
     q=Fraction(*old[1][3:5])+Fraction(*e[1][3:5]);moves.append([i,j,str(q)])
     if q:old[1][3:5]=[q.numerator,q.denominator]
     else:out.pop(j)
     break
    if not commutes(e,old):break
   else:out.append(e);continue
   if moves and moves[-1][0]==i:continue
  out.append(e)
 print(d,'before',len(p),'after',len(out),'merged',len(moves),'zero',sum(q=='0' for _,_,q in moves),flush=True)
 Path('/tmp/scalar-trace-'+d+'.json').write_text(json.dumps(out))
 def synthesize(program):
  cur=c['start'][:];out=[]
  def climb(r,f):
   a=cur[r]
   if a==f:return
   if not J.F.span(c['frames'][a])<J.F.span(c['frames'][f]):raise ValueError(('non-monotone',r,a,f))
   out.append(['climb','trace',r,a,f,len(c['frames'][f])-len(c['frames'][a])]);cur[r]=f
  for e in program:
   if e[0]=='scalar':
    for r in roles(e):
     if r[0]=='L':climb(r[1],e[2])
   elif e[0]=='warp':climb(e[1][1],e[3]);cur[e[1][1]]=e[4]
   out.append(e)
  for r,f in enumerate(c['final']):climb(r,f)
  return out
 new=synthesize(out)
 paid=Counter(e[5] if e[0]=='climb' else e[4] for e in new if e[0] in ('climb','center'))
 oldpaid=Counter(e[5] if e[0]=='climb' else e[4] for e in p if e[0] in ('climb','center'))
 print(d,'paid',dict(paid),'delta',{k:paid[k]-oldpaid[k] for k in set(paid)|set(oldpaid)},flush=True)
 Path('/tmp/scalar-trace-native-'+d+'.json').write_text(json.dumps(new))
