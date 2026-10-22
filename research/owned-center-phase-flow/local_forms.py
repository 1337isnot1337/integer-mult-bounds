"""Exhaust all localized helper-entrance forms of dimension at most five."""
import search as S
from collections import Counter
import json,time
beg=time.monotonic();t=1-.003021775870775;power=lambda r:r**t if r else 0.
cache={}
def rank(code,d):
 key=code,d
 if key in cache:return cache[key]
 piv={}
 for i in range(d):
  x=(code>>(d*i))&((1<<d)-1)
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 cache[key]=len(piv);return len(piv)
results=[];best=None;tested=0
nodes=sorted({S.find(n) for n in S.starts[224:]}-S.zero)
for node in nodes:
 d=len(S.frames[S.frame[node]])
 if not 0<d<=5:continue
 nv=d*(d+1)//2;shift=S.offset[node];mask=(1<<nv)-1;effects=Counter()
 def effect(base,sign,B,fn):
  k=len(B);maps=[0]*nv
  for i,u in enumerate(B):
   for j,v in enumerate(B):
    q=(fn(u,v)>>shift)&mask
    while q:
     bit=q&-q;maps[bit.bit_length()-1]^=1<<(k*i+j);q^=bit
  if any(maps):effects[base,k,tuple(maps)]+=sign
 for kind,a,b,op in S.links:
  if node not in (S.find(a),S.find(b)):continue
  if kind=='paid':
   B=S.spacebasis(S.coords[S.frame[a]].keys()&S.coords[S.frame[b]].keys());r=len(S.frames[S.frame[a]])+len(S.frames[S.frame[b]])-2*len(B)
   effect(r,1,B,lambda u,v:S.form(a,u,v)^S.form(b,u,v))
  else:
   if op<0:a,b=b,a
   B=S.frames[S.frame[a]]
   effect(0,1,B,lambda u,v:S.form(a,u,v)^S.form(b,S.image(u,op),S.image(v,op)))
 for r in range(224,632):
  a,b=S.starts[r],S.ends[r]
  if node not in (S.find(a),S.find(b)):continue
  B=S.spacebasis(S.coords[S.frame[a]].keys()&S.coords[S.frame[b]].keys());g=len(S.frames[S.frame[b]])-len(S.frames[S.frame[a]])
  effect(g,-1,B,lambda u,v:S.form(a,u,v)^S.form(b,u,v))
 effects=[(base,k,maps,sign) for (base,k,maps),sign in effects.items() if sign];state=[0]*len(effects);local=(0.,0);prev=0
 for z in range(1,1<<nv):
  gray=z^(z>>1);change=(gray^prev).bit_length()-1;prev=gray;energy=0.
  for j,(base,k,maps,sign) in enumerate(effects):
   state[j]^=maps[change];energy+=sign*(power(base+rank(state[j],k))-power(base))
  if energy<local[0]:local=energy,gray
  tested+=1
 row=dict(node=node,dimension=d,forms=(1<<nv)-1,energy=local[0],form_bits=local[1]);results.append(row)
 if best is None or row['energy']<best['energy']:best=row
 print('LOCAL',row,'seconds',time.monotonic()-beg,flush=True)
S.HERE.joinpath('LOCAL-FORMS.json').write_text(json.dumps(dict(status='EXHAUSTIVE_LOCALIZED_FORM_DISCOVERY_FLOAT_MOMENTS',rows=results,best=best,tested=tested,seconds=time.monotonic()-beg,no_kappa_claim=True),indent=2)+'\n')
