"""Solver-free reconstruction of the frozen joint helper/warp candidate."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from hashlib import sha256
import json,gzip,sys
if sys.flags.optimize:raise RuntimeError('Run without -O')
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from warp_merge import synthesize

def construct():
 patch=json.load(open(HERE/'PATCH.json'));data=(HERE/'BASE-WORD.json.gz').read_bytes();assert sha256(data).hexdigest()==patch['base_sha256']
 base=json.loads(gzip.decompress(data));c=deepcopy(base['canonical']);c['frames'].extend(patch['added_frames'])
 for role,frame in patch['starts'].items():assert 224<=int(role)<632;c['start'][int(role)]=frame
 c['warps']=deepcopy(patch['warps']);words={}
 for direction,word in base['programs'].items():
  raw=[deepcopy(e) for e in word if e[0]!='climb']
  for change in patch['word_changes'][direction]:
   i=change['index'];assert raw[i]==change['old'];old,new=raw[i],change['new']
   assert old[0]==new[0] and old[0] in ('scalar','warp')
   assert old[1]==new[1] if old[0]=='scalar' else old[1:3]==new[1:3]
   raw[i]=deepcopy(new)
  words[direction]=synthesize(c,raw)
 c['R']=408;c['local_profile']={int(k):v for k,v in patch['paid'].items()}
 c['warp_edges']=[list(t) for t in sorted({(1 if e[2]>0 else -1,abs(e[2]),e[3],e[4]) for e in words['forward'] if e[0]=='warp'})]
 assert c['start'][:224]==base['canonical']['start'][:224] and c['final']==base['canonical']['final']
 for direction,word in words.items():
  assert Counter(e[-1] for e in word if e[0] in ('climb','center'))==c['local_profile']
  assert [e[1] for e in word if e[0]=='scalar']==[e[1] for e in base['programs'][direction] if e[0]=='scalar']
 for new,old in zip(c['warps'],base['canonical']['warps']):assert all(new[k]==old[k] for k in ['op','lender','B_pos'])
 raw=json.dumps(dict(canonical=c,programs=words),sort_keys=True,separators=(',',':')).encode();frozen=json.load(open(HERE/'FROZEN.json'))
 assert sha256(raw).hexdigest()==frozen['payload_sha256'] and gzip.decompress((HERE/'ACTUAL-WORD.json.gz').read_bytes())==raw
 assert sha256((HERE/'ACTUAL-WORD.json.gz').read_bytes()).hexdigest()==frozen['compressed_sha256']
 return c,words
if __name__=='__main__':construct();print('PASS_SOLVER_FREE_JOINT_RECONSTRUCTION')
