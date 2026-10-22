"""Read the actual H word without its zero-frame helper compensation.
All helpers stay arbitrary. This is an interface probe, not a supplier claim.
"""
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions required")
from fractions import Fraction as Q
from collections import Counter
import sys,json,gzip
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
from hashlib import sha256
for name,digest in json.loads((HERE/"INPUTS.json").read_text())["source_sha256"].items():
 assert sha256((HERE/"sources"/name).read_bytes()).hexdigest()==digest
sys.path.insert(0,str(ROOT/'research/joint-helper-lattice'));import native_joint as J
F=J.F;V=F.load(ROOT/'research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py','dirty_H_rows');X=F.load(ROOT/'research/kappa-rebuild/complex/native_extensions.py','dirty_H_literal')
c=F.read(HERE/'sources/CANONICAL.json.gz');words=F.read(HERE/'sources/NATIVE.json.gz');out={}
for direction,word in words.items():
 i=word.index(['phase','zero_frame_center_compensation']);j=next(z for z in range(i+1,len(word)) if word[z][0]=='phase')
 removed=word[i:j];raw=word[:i]+word[j:]
 good,old=X.literal_replay(V,c,word,direction=='backward');rows,rec=X.literal_replay(V,c,raw,direction=='backward')
 assert rec['paid_profile']==old['paid_profile']
 changes=[];allwords=Counter();affected=set();inputs=set()
 for r in range(632):
  delta=dict(rows['L',r])
  for key,q in good['L',r].items():delta[key]=delta.get(key,Q(0))-q
  delta={k:v for k,v in delta.items() if v}
  if delta:
   affected.add(r)
   for key,q in delta.items():
    allwords[str(key[1:])]+=1;inputs.add(str(key));changes.append(dict(output=r,input=repr(key),coefficient=str(q)))
 out[direction]=dict(removed_events=len(removed),paid=rec['paid_profile'],scalar_allowance=rec['real_scalar_allowance'],affected_outputs=sorted(affected),distinct_input_terms=len(inputs),word_census=dict(allwords),changes=changes)
 print(direction,'outputs',len(affected),'terms',len(changes),'word types',list(allwords)[:5],flush=True)
data=gzip.compress((json.dumps(out,indent=2)+'\n').encode(),mtime=0)
if '--check' in sys.argv:assert (HERE/'RAW-DEFECT.json.gz').read_bytes()==data
else:(HERE/'RAW-DEFECT.json.gz').write_bytes(data)
