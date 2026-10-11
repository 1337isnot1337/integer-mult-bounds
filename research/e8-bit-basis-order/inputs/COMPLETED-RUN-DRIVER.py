from pathlib import Path
import os,sys,json,hashlib,subprocess,gzip,time,resource
S=Path('/tmp/task2-pr433-immutable-static');B=Path('/tmp/task2-pr433-default-envelope/run');V=Path('/tmp/task2-r758-basis-screen/high_reverse/bit426-source-centres/bit-source-centres.json');O=Path('/tmp/task2-r758-high-reverse-finite-fresh')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def closure():return {p.relative_to(S).as_posix():sha(p) for p in S.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
if not __debug__ or sys.flags.optimize:raise RuntimeError('assertions disabled')
if O.exists():raise RuntimeError('fresh output required')
start=time.monotonic()
PIN='3129eb4321f706542470f8443f66a6b4351a12a9ceec85e7f76aa19db1e1e32f'
assert sha(S/'MANIFEST.json')==PIN
completed=B.parent/'COMPLETION.json'; cr=json.loads(completed.read_text());assert cr['status']=='PASS_RETAINED_DEFAULT_PR433_REPLAY' and cr['returncode']==0 and cr['source_manifest_before']==cr['source_manifest_after']==PIN
manifest=json.loads((S/'MANIFEST.json').read_text());before=closure();assert before==manifest['files'];assert sha(V)=='ee95a35d2bbdba598ea4e40917467090a956b06fad15b3f00d260f0db7ebd453'
O.mkdir();(O/'scratch').mkdir();reused={}
for src,dst in [('work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz','work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz'),('inherited/bit-geometry.json.gz','inherited/bit-geometry.json.gz'),*[(f'work/pr361/code/engines/{n}.py',f'work/pr361/code/engines/{n}.py') for n in ['moment','base_two_moment','outer']],*[(f'split-centres/{n}.json',f'split-centres/{n}.json') for n in ['INTEGRATION','INDEPENDENT-REPLAY']]]:
 assert sha(B/src)==cr['output_hashes']['run/'+src]
 p=O/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((B/src).read_bytes());reused[src]=sha(B/src)
p=O/'bit426-source-centres';p.mkdir();(p/'bit-source-centres.json').write_bytes(V.read_bytes())
input_before=dict(candidate=sha(V),baseline_completion=sha(completed),**reused)
def inputs_now():return dict(candidate=sha(V),baseline_completion=sha(completed),**{k:sha(B/k) for k in reused})
env=dict(os.environ,E8_OUTPUT=str(O),PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(O/'scratch'));env.pop('PYTHONOPTIMIZE',None)
steps=[]
try:
 for name,script,args in [('export','vendor/export_records.py',[p/'bit-source-centres.json',p/'records']),('global','code/bit_global.py',['--source',p,'--local-check',p,'--out',p/'global']),('audit','code/bit_audit.py',['--local-check',p,'--out',p/'global']),('price','code/bit_price.py',[]),('combined','code/combined.py',[])]:
  with (O/(name+'.log')).open('w') as log:r=subprocess.run([sys.executable,'-B',str(S/script),*map(str,args)],cwd=O,env=env,stdout=log,stderr=subprocess.STDOUT)
  steps.append(dict(name=name,returncode=r.returncode,log_sha256=sha(O/(name+'.log'))));assert r.returncode==0,(name,r.returncode)
 assert closure()==before and inputs_now()==input_before
 (O/'COMPLETION.json').write_text(json.dumps(dict(status='PASS_CHANGED_BIT_FINITE_CHECK',scope='changed bit only; unchanged complex receipts reused; no phase replay',source_manifest_sha256=sha(S/'MANIFEST.json'),candidate_sha256=sha(V),reused=reused,input_before=input_before,input_after=inputs_now(),steps=steps,wall_seconds=time.monotonic()-start,child_usage=list(resource.getrusage(resource.RUSAGE_CHILDREN)),output_hashes={p.relative_to(O).as_posix():sha(p) for p in O.rglob('*') if p.is_file()}),indent=2)+'\n')
except BaseException as e:
 (O/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps,source_unchanged=closure()==before,input_unchanged=inputs_now()==input_before,wall_seconds=time.monotonic()-start),indent=2)+'\n');raise
