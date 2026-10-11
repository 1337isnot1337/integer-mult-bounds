from pathlib import Path
import json,hashlib,os,sys,subprocess,time,resource
A=Path(__file__).resolve().parent;S=A/'source/research';B=Path('/tmp/task2-pr438-basis-finite-fresh');O=Path('/tmp/task2-pr442-bit-fixture-fresh');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def snap(p):
 assert not any(f.is_symlink() for f in p.rglob('*'))
 return {f.relative_to(p).as_posix():sha(f) for f in p.rglob('*') if f.is_file()}
if not __debug__ or sys.flags.optimize:raise RuntimeError('assertions disabled')
if O.exists():raise RuntimeError('fresh output required')
before=snap(A);m=json.loads((A/'MANIFEST.json').read_text());assert {n:h for n,h in before.items() if n!='MANIFEST.json'}==m['files']
pins=json.loads((A/'SOURCE-PINS.json').read_text());assert pins['head']=='4e16d001d505d4f21dd2bcfc44591f9be4c279bd'
for n,z in pins['files'].items():
 raw=(A/'source'/n).read_bytes();assert sha(A/'source'/n)==z['sha256'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==z['git_blob']
cp=B/'COMPLETION.json';cr=json.loads(cp.read_text());assert sha(cp)=='a7a2efeef20ba6b8fa381b19bd6bd83745bdca4b2ba255de5caa863ff74eec30';assert cr['status']=='PASS_CHANGED_PR438_BIT_FINITE_CHECK' and all(z['returncode']==0 for z in cr['steps']);assert cr['source_before']==cr['source_after'] and cr['inputs_before']==cr['inputs_after']
reset='bit426-source-centres/bit-source-centres-prekernel.json';reuse={n:cr['output_hashes'][n] for n in [reset,'inherited/bit-geometry.json.gz','work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz']}
for n,h in reuse.items():assert sha(B/n)==h
assert reuse[reset]=='98ffef9246c8bf6c537ab5e134321abea05cf0b7830c9e3fd92cbe4e88d8c308'
inputs=dict(completion=sha(cp),**reuse)
def now():return dict(completion=sha(cp),**{n:sha(B/n) for n in reuse})
parentpin=json.loads((S/'idle-axis-hosting/MANIFEST.json').read_text())['parent_manifest_sha256'];assert sha(S/'e8-early-reset-kernel/MANIFEST.json')==parentpin=='95a9570287b64d22de30e6ae3acf931d5f6daef1a163f0c99532e1a24639fbc2'
O.mkdir();(O/'scratch').mkdir();start=time.monotonic();steps=[];parent=O/'parent';p=parent/'bit426-source-centres';p.mkdir(parents=True)
for n in reuse:
 target=O/'reset-input.json' if n==reset else parent/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((B/n).read_bytes())
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(O/'scratch'),FIXTURE_OUTPUT=str(O));env.pop('PYTHONOPTIMIZE',None)
try:
 tasks=[('kernel',S/'e8-early-reset-kernel/apply.py',[O/'reset-input.json',p/'bit-source-centres.json'],O),('export',S/'split-centres-global/vendor/export_records.py',[p/'bit-source-centres.json',p/'records'],O),('source-spans',S/'e8-early-reset-kernel/source_span.py',[p/'bit-source-centres.json',p/'records/frames.json'],O),('parent-global',S/'e8-early-reset-kernel/bit_global.py',['--source',p,'--local-check',p,'--out',p/'global'],parent),('parent-audit',S/'e8-early-reset-kernel/bit_audit.py',['--local-check',p,'--out',p/'global'],parent),('hosted-bit',S/'idle-axis-hosting/bit_hosted.py',[p/'global',p,O/'hosted'],O),('audit-contract',A/'audit_stage.py',[],O)]
 for name,file,args,cwd in tasks:
  with (O/(name+'.log')).open('w') as log:r=subprocess.run([sys.executable,'-B',str(file),*map(str,args)],cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
  steps.append(dict(name=name,returncode=r.returncode,log_sha256=sha(O/(name+'.log'))));assert r.returncode==0,(name,r.returncode)
  if name=='kernel':assert sha(p/'bit-source-centres.json')=='da4aa797d6dad909fd1faaa90abea749b026299ac8cad3ad0a4a248e16bdb5f5';assert len(json.loads((p/'bit-kernel-receipt.json').read_text())['controls'])==3
  if name=='parent-global':assert json.loads((p/'global/GLOBAL.json').read_text())['template_sha256']=='f9ce9ac945d9e8ea737dc5e456e366a7e2a21d8b989d24b742d7f124d26fb32f'
  if name=='parent-audit':assert len(json.loads((p/'global/AUDIT.json').read_text())['mutations_rejected'])==8
  if name=='hosted-bit':assert json.loads((O/'hosted/GLOBAL.json').read_text())['template_sha256']==json.loads((S/'idle-axis-hosting/EXPECTED.json').read_text())['bit_template_sha256']=='dd7833dcaff8c84b258847f4c4d65b6402c702700ae37d2c464083ee37b24126'
 assert snap(A)==before and now()==inputs
 (O/'COMPLETION.json').write_text(json.dumps(dict(status='PASS_MINIMAL_ACTUAL442_BIT_FIXTURE',source_before=before,source_after=snap(A),inputs_before=inputs,inputs_after=now(),steps=steps,wall_seconds=time.monotonic()-start,child_usage=list(resource.getrusage(resource.RUSAGE_CHILDREN)),output_hashes=snap(O),scope='Bit-only deterministic fixture and2auditcontract regressions. Reused completed438 exact resetinput; no full parent/complex/phase/price/assembly replay, no numericalbound admission'),indent=2)+'\n')
except BaseException as e:
 (O/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps,source_unchanged=snap(A)==before,input_unchanged=now()==inputs,wall_seconds=time.monotonic()-start),indent=2)+'\n');raise
