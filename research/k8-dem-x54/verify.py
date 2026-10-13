"""Rebuild and admit the eight-slot three-demotion witness (X54 on #1148's word) with #1148's unchanged T16 owners."""
import argparse,gzip,hashlib,importlib.util,json,os,shutil,subprocess,sys,time
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];PRE=ROOT/'research/k8-eight-ends-t16';DEM=ROOT/'research/k8-three-demotions';WORDPRE=ROOT/'research/k8-eight-ends'
def rd(p):
 p=Path(p);return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def payload(p):return hashlib.sha256(gzip.decompress(Path(p).read_bytes())).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
 assert __debug__
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--base',type=Path);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--parent-from',type=Path);ap.add_argument('--native-from',type=Path);a=ap.parse_args()
 work=a.work.resolve();assert not work.exists() and not work.is_relative_to(ROOT)
 for rel,h in rd(P/'MANIFEST.json').items():assert sha(P/rel)==h,rel
 for rel,h in rd(P/'SOURCE-PINS.json').items():assert sha(ROOT/rel)==h,rel
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONINTMAXSTRDIGITS='0')
 for k in ('PYTHONOPTIMIZE','WITNESS_DISCOVER','WITNESS_RECORD','WITNESS_SPEC'):env.pop(k,None)
 work.mkdir(parents=True);steps=[]
 def run(name,script,*args):
  t=time.monotonic();log=work/(name+'.log')
  with log.open('w') as f:r=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
  steps.append(dict(step=name,exit_code=r.returncode,seconds=time.monotonic()-t,log_sha256=sha(log)));dump(work/'STEPS.json',steps);assert r.returncode==0,(name,log.read_text()[-6000:]);print('PASS',name,flush=True)
 if a.parent_from:parent=a.parent_from.resolve()
 else:
  assert a.base,'--base (the seven-slot k8 word) is required to rebuild the preceding geometry'
  parent=work/'parent';run('parent',PRE/'verify.py','--base',a.base.resolve(),'--work',parent)
 assert rd(parent/'RESULT.json')['status']=='PASS_K8_EIGHT_ENDS_T16_COMPLETE_ADMISSION'
 for rel,h in rd(DEM/'PARENT-PINS.json').items():assert sha(parent/rel)==h,rel
 raw=work/'FULL-WORD.json.gz';run('build',P/'build_word.py','--out',raw)
 assert payload(raw)==rd(P/'RECIPE-X54-dem.json')['expect_sha256']
 run('independent-local',ROOT/'research/gauge44-slots/independent/audit_local.py','--word',raw,'--main',ROOT,'--output',work/'AUDIT-LOCAL.json')
 run('x54-controls',P/'controls.py','--out',work/'x54-controls')
 if a.native_from:native=a.native_from.resolve()
 else:
  native=work/'native';run('native',WORDPRE/'replay_native.py',raw,native)
 ns=rd(native/'STEPS.json');assert [x['step'] for x in ns]==['native','ledgers','local-replay','wrappers','phases'] and all(x['exit_code']==0 for x in ns)
 local=native/'local';assert payload(local/'FULL-WORD.json.gz')==payload(raw)
 spec=importlib.util.spec_from_file_location('identities',PRE/'vendor/pr1074/code/generated_identity.py');ident=importlib.util.module_from_spec(spec);spec.loader.exec_module(ident)
 assert ident.artifact_identities(local)==rd(P/'data/PLAN.json.gz')['provider_registry']['gauge44']['artifact_semantic_sha256']
 data=work/'data';data.mkdir();(data/'PLAN.json').write_bytes(gzip.decompress((P/'data/PLAN.json.gz').read_bytes()))
 shutil.copy2(DEM/'OWNERS.json.gz',data/'OWNERS.json.gz');shutil.copy2(P/'data/SPEC.json',data/'SPEC.json')
 run('strict-global',DEM/'run_global.py','--local',local,'--parent-work',parent,'--data',data,'--work',work/'global')
 result=rd(work/'global/REPLAY.json');claim=rd(P/'CLAIM.json');assert result['kappa_decimal']==claim['kappa_decimal']
 assert Q(result['kappa'])>Q(rd(DEM/'CLAIM.json')['kappa']),'strict gain over #1148'
 receipt=dict(status='PASS_X54_ON_THREE_DEMOTIONS_COMPLETE_ADMISSION',kappa=result['kappa'],kappa_decimal=result['kappa_decimal'],complex_lower=result['complex_lower'],bit_lower=result['bit_lower'],controls=result['controls'],x54_controls=10,outer_strict_inequalities=47,native_steps=ns,native_semantic_artifacts=ident.artifact_identities(local),native_reuse=bool(a.native_from),parent_reuse=bool(a.parent_from),previous_kappa=rd(DEM/'CLAIM.json')['kappa_decimal'],scope=claim['scope'],steps=steps)
 dump(work/'RESULT.json',receipt);print(receipt['status'],receipt['kappa_decimal'])
if __name__=='__main__':main()
