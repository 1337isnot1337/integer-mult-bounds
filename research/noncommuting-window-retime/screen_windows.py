from pathlib import Path
from copy import deepcopy
import json,gzip,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
# Reuse only graph construction, not the numerical optimizer.
s=(HERE/'search.py').read_text();prefix=s[:s.index('    domain={};cache={};counts=Counter()')]
prefix=prefix.replace('def main(op,time_limit):','def screen(c,programs,op="all"):').replace('started=time.monotonic();c,programs=load_base();p=', 'started=time.monotonic();c=deepcopy(c);p=')
prefix+='    return [dict(node=n,lower=c["frames"][lower[n]],upper=c["frames"][upper[n]]) for n in variables if not spans[lower[n]]<=spans[upper[n]]]\n'
namespace={'__file__':str(HERE/'search.py'),'__name__':'screen_graph'};exec(compile(prefix,str(HERE/'search.py'),'exec'),namespace)
x=json.loads(gzip.decompress((ROOT/'research/helper-warp-joint/ACTUAL-WORD.json.gz').read_bytes()));patterns=json.load(open(ROOT/'research/noncommuting-contact-rewrite/OPTIMISTIC-WINDOWS.json'));out=[]
def changed(v):
 programs={}
 for d,word in x['programs'].items():
  new=[];index=-1
  for e in word:
   if e[0]!='climb':index+=1
   if e[0]=='climb' or index not in (v['first'],v['last']):new.append(e)
   if e[0]!='climb' and str(index) in v['corrections']:
    ee=deepcopy(v['corrections'][str(index)])
    if d=='backward':ee[1][1],ee[1][2]=ee[1][2],ee[1][1];ee[1][3]*=-1
    new.append(ee)
  programs[d]=new
 return programs
for idx,v in enumerate(patterns):
 programs=changed(v);bad=namespace['screen'](x['canonical'],programs)
 out.append(dict(first=v['first'],last=v['last'],relaxed_empty_intervals=len(bad),first_witness=bad[:1]))
 if idx%20==0:print('SCREENED',idx+1,'empty',len(bad),flush=True)
 if not bad:
  (HERE/'BASE-WORD.json.gz').write_bytes(gzip.compress(json.dumps(dict(canonical=x['canonical'],programs=programs),sort_keys=True,separators=(',',':')).encode(),mtime=0));(HERE/'REWRITE.json').write_text(json.dumps(v,indent=2)+'\n');print('FOUND_FEASIBLE_RELAXATION',idx,v['first'],v['last'],flush=True);break
(HERE/'INTERVAL-SCREEN.json').write_text(json.dumps(dict(status='NECESSARY_NORMAL_EDGE_SCREEN',rows=out,total_candidates=len(patterns),exhausted=len(out)==len(patterns)),indent=2)+'\n')
