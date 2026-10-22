from pathlib import Path
from copy import deepcopy
import gzip,json,subprocess,sys,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
x=json.loads(gzip.decompress((ROOT/'research/helper-warp-joint/ACTUAL-WORD.json.gz').read_bytes()));patterns=json.load(open(ROOT/'research/noncommuting-contact-rewrite/OPTIMISTIC-WINDOWS.json'));good={(r['first'],r['last']) for r in json.load(open(HERE/'ALL-INTERVAL-SCREEN.json'))['rows'] if not r['relaxed_empty_intervals']};groups={}
for v in patterns:
 if (v['first'],v['last']) in good:groups.setdefault((tuple(sorted(v['delta'].items())),len(v['corrections'])),v)
for v in groups.values():
 dest=HERE/'cases'/f"{v['first']}-{v['last']}";dest.mkdir(parents=True,exist_ok=True)
 if (v['first'],v['last'])==(11454,13548):
  shutil.copyfile(HERE/'MILP-OPall.json',dest/'MILP.json');shutil.copyfile(HERE/'REWRITE.json',dest/'REWRITE.json');continue
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
 (HERE/'BASE-WORD.json.gz').write_bytes(gzip.compress(json.dumps(dict(canonical=x['canonical'],programs=programs),sort_keys=True,separators=(',',':')).encode(),mtime=0));(HERE/'REWRITE.json').write_text(json.dumps(v,indent=2)+'\n');shutil.copyfile(HERE/'REWRITE.json',dest/'REWRITE.json')
 print('START',v['first'],v['last'],flush=True)
 with (dest/'run.log').open('w') as f:r=subprocess.run([sys.executable,'-B',str(HERE/'search.py'),'--operator','all','--seconds','120'],stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:print('BLOCKED',r.returncode,flush=True);continue
 shutil.copyfile(HERE/'MILP-OPall.json',dest/'MILP.json');receipt=json.load(open(dest/'MILP.json'));print('RESULT',v['first'],v['last'],receipt.get('actual_moment_reduction'),flush=True)
 if receipt.get('actual_moment_reduction',0)>1e-10:print('POSITIVE_STOP_FOR_VALIDATION',flush=True);break
