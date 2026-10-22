from pathlib import Path
import json,gzip,sys
if not __debug__: raise RuntimeError("Assertions must be enabled")
CHECK="--check" in sys.argv
from copy import deepcopy
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/helper-warp-joint'));from warp_merge import F,synthesize
x=json.loads(gzip.decompress((ROOT/'research/helper-warp-joint/ACTUAL-WORD.json.gz').read_bytes()));c=x['canonical'];changes=[r for r in json.load(open(HERE/'SCREEN.json'))['rows'] if r['best'] and not r['best']['delta']]
replacements={r['indices'][0]:r['best']['sequence'] for r in changes};omit={i for r in changes for i in r['indices']};assert len(omit)==3*len(changes)
V=F.load(ROOT/'research/kappa-causal-continuation/buffer-borrowing/verify_buffers.py','rewrite_rows');X=F.load(ROOT/'research/kappa-rebuild/complex/native_extensions.py','rewrite_literal');words={};reports={}
for d,p in x['programs'].items():
 raw=[deepcopy(e) for e in p if e[0]!='climb'];new=[]
 for i,e in enumerate(raw):
  if i in replacements:new.extend(['scalar',F.dual(g) if d=='backward' else g,f] for g,f in replacements[i])
  if i not in omit:new.append(e)
 pp=synthesize(c,new);assert Counter(e[-1] for e in pp if e[0] in ('climb','center'))==Counter(e[-1] for e in p if e[0] in ('climb','center'))
 assert Counter(tuple(e[2:]) for e in pp if e[0]=='climb')==Counter(tuple(e[2:]) for e in p if e[0]=='climb')
 assert [e for e in pp if e[0]=='warp']==[e for e in p if e[0]=='warp']
 rows,receipt=X.literal_replay(V,c,pp,d=='backward');assert all(rows['L',r]==V.expected(('L',r),[],d=='backward',False) for r in range(632));words[d]=pp;reports[d]=receipt
out=dict(canonical=c,programs=words)
data=gzip.compress(json.dumps(out,sort_keys=True,separators=(',',':')).encode(),mtime=0)
receipt=json.dumps(dict(status='PASS_LITERAL_NONCOMMUTING_REWRITES',rewrites=len(changes),reports=reports,no_new_kappa=True),indent=2)+'\n'
if CHECK:
 assert (HERE/'REWRITTEN-WORD.json.gz').read_bytes()==data
 assert (HERE/'REPLAY.json').read_text()==receipt
else:
 (HERE/'REWRITTEN-WORD.json.gz').write_bytes(data)
 (HERE/'REPLAY.json').write_text(receipt)
print('PASS_REWRITE',len(changes),'immutable check' if CHECK else 'regenerated')
