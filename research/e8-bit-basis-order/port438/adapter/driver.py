from pathlib import Path
import os,sys,json,hashlib,subprocess,gzip,time,resource
S=Path('/tmp/task2-pr438-basis-port/source');A=Path(__file__).resolve().parent;B=Path('/tmp/task2-pr433-default-envelope/run');O=Path('/tmp/task2-pr438-basis-finite-fresh')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def snap(root):
 assert not any(p.is_symlink() for p in root.rglob('*'))
 return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
if not __debug__ or sys.flags.optimize:raise RuntimeError('assertions disabled')
if O.exists():raise RuntimeError('fresh output required')
m=json.loads((S/'MANIFEST.json').read_text());before=snap(S);assert {k:v for k,v in before.items() if k!='MANIFEST.json'}==m['files']
am=json.loads((A/'MANIFEST.json').read_text());ab=snap(A);assert {k:v for k,v in ab.items() if k!='MANIFEST.json'}==am['files']
cp=B.parent/'COMPLETION.json';cr=json.loads(cp.read_text());PIN='3129eb4321f706542470f8443f66a6b4351a12a9ceec85e7f76aa19db1e1e32f';assert cr['status']=='PASS_RETAINED_DEFAULT_PR433_REPLAY' and cr['returncode']==0 and cr['source_manifest_before']==cr['source_manifest_after']==PIN
oldS=Path('/tmp/task2-pr433-immutable-static');assert sha(oldS/'MANIFEST.json')==PIN;assert {k:v for k,v in snap(oldS).items() if k!='MANIFEST.json'}==json.loads((oldS/'MANIFEST.json').read_text())['files']
bind=json.loads(Path('/tmp/task2-pr438-basis-port/COMPLEX-REUSE-BINDING.json').read_text());assert sha(cp)==bind['completion_sha256'];assert set(bind['changed_files'])=={'code/complex_phases.py','inputs/complex-phase-receipt.json'}
for n,z in bind['scientific_source_comparison'].items():
 assert sha(S/n)==z['sha256']
 if z['identical_433']:assert (S/n).read_bytes()==(oldS/n).read_bytes()
phase=json.loads((S/'inputs/complex-phase-receipt.json').read_text());canonical=B/'split-centres/CANONICAL-WORD.json.gz';assert sha(canonical)==phase['canonical_word_sha256'];assert hashlib.sha256(gzip.decompress(canonical.read_bytes())).hexdigest()=='be2d8d412b948bce50a0fc852ab4c01f57bff4c3c8272da80c09be5bcdf253bf';assert hashlib.sha256(gzip.decompress((S/'inputs/complex-phase-recipes.json.gz').read_bytes())).hexdigest()==phase['recipe_sha256']
reused={k:sha(B.parent/k) for k in bind['verified_outputs']};assert reused==bind['verified_outputs'];inputs=dict(completion=sha(cp),reuse_binding=sha(Path('/tmp/task2-pr438-basis-port/COMPLEX-REUSE-BINDING.json')),**reused)
def now():return dict(completion=sha(cp),reuse_binding=sha(Path('/tmp/task2-pr438-basis-port/COMPLEX-REUSE-BINDING.json')),**{k:sha(B.parent/k) for k in reused})
O.mkdir();(O/'scratch').mkdir();start=time.monotonic();steps=[]
def copy(src,dst,decompress=False):
 p=O/dst;p.parent.mkdir(parents=True,exist_ok=True);raw=src.read_bytes();p.write_bytes(gzip.decompress(raw) if decompress else raw)
for src,dst in [('inputs/e8-r865.json.gz','work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz'),('inputs/bit-geometry.json.gz','inherited/bit-geometry.json.gz')]:copy(S/src,dst)
for n in ['moment','base_two_moment','outer']:copy(S/('vendor/engines/'+n+'.py'),'work/pr361/code/engines/'+n+'.py')
for k in reused:copy(B.parent/k,k.removeprefix('run/'))
p=O/'bit426-source-centres';p.mkdir();copy(S/'inputs/bit-r767.json.gz','bit426-source-centres/bit-input.json',True)
env=dict(os.environ,E8_OUTPUT=str(O),PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(O/'scratch'));env.pop('PYTHONOPTIMIZE',None)
try:
 tasks=[(n,S/('code/'+n+'.py'),[]) for n in ['bit_construct','bit_reset','bit_kernel']]+[('post_basis',A/'post_stage.py',[]),('export',S/'vendor/export_records.py',[p/'bit-source-centres.json',p/'records']),('global',S/'code/bit_global.py',['--source',p,'--local-check',p,'--out',p/'global']),('audit',S/'code/bit_audit.py',['--local-check',p,'--out',p/'global']),('price',S/'code/bit_price.py',[]),('combined',S/'code/combined.py',[])]
 for name,file,args in tasks:
  with (O/(name+'.log')).open('w') as log:r=subprocess.run([sys.executable,'-B',str(file),*map(str,args)],cwd=O,env=env,stdout=log,stderr=subprocess.STDOUT)
  steps.append(dict(name=name,returncode=r.returncode,log_sha256=sha(O/(name+'.log'))));assert r.returncode==0,(name,r.returncode)
 result=json.loads((O/'RESULT.json').read_text());expected=json.loads((S/'EXPECTED.json').read_text())
 for k,v in expected.items():
  if k not in {'bit_invoice','bit_template_sha256'}:assert result[k]==v,(k,result[k],v)
 g=json.loads((p/'global/GLOBAL.json').read_text());audit=json.loads((p/'global/AUDIT.json').read_text());assert len(audit['mutations_rejected'])==8
 assert (g['R'],g['live'],g['physical'])==(747,14223,14232);assert result['bit_invoice']['coefficient_bits']==193 and result['bit_invoice']['two_level_coefficient_bits']==423
 P={int(r):n for r,n in audit['profile'].items()};E=sum(P.values());mass=sum(r*n for r,n in P.items());geo=json.loads((p/'global/GEOMETRY.json').read_text())
 assert g['banks_per_stage']==727 and mass==64*g['live']-2496 and P=={1:180792,2:74232,3:22248,4:24984,5:7344,7:6768,8:648,14:3840,28:3840,42:3840}
 unit=72*g['local_additions']+g['bridge_additions'];J=8*8*9*(240+g['R'])+8*(2*4*120*8)+2*g['bank_assignments']+2*g['copy_erase_episodes']
 selectors=2*9*8*((g['live']-1)+g['R']*64*(geo['max_route_factors']+63+64));prefix=int(g['global_prefix_bound'])
 coefficient=unit+J*16*(4096+1)**2+J*g['physical']+E*(8*4096+8+128*128**3)+16*64**3+g['copy_erase_episodes']+selectors+prefix+1
 two=(coefficient+1)**2*(E+1)**2;assert coefficient==11618636861972555523343873296287586172648663760810665400081 and two.bit_length()==423 and g['local_additions']==14757
 (O/'FINITE-COMPARISON.json').write_text(json.dumps(dict(status='PASS_ACTUAL_FRESH_FINITE_INVOICE',candidate_coefficient=str(coefficient),candidate_bits=coefficient.bit_length(),candidate_two_level_bits=two.bit_length(),source_projected_coefficient='82188330587888376961373106195271196377707398804483318967211886464529',source_projected_bits=226,source_projected_two_level_bits=488,baseline_scope='Local replay plus exact algebra nomination; baseline full global not rerun',b=result['complex_lower'],c=result['bit_lower'],k=result['kappa']),indent=2)+'\n')
 assert snap(S)==before and snap(A)==ab and now()==inputs
 (O/'COMPLETION.json').write_text(json.dumps(dict(status='PASS_CHANGED_PR438_BIT_FINITE_CHECK',scope='Post-kernel port of published basis method; independently completed PR433 complex evidence reused; no new exponent or runtime claim',source_before=before,source_after=snap(S),adapter_manifest_sha256=sha(A/'MANIFEST.json'),inputs_before=inputs,inputs_after=now(),steps=steps,wall_seconds=time.monotonic()-start,child_usage=list(resource.getrusage(resource.RUSAGE_CHILDREN)),output_hashes=snap(O)),indent=2)+'\n')
except BaseException as e:
 (O/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps,source_unchanged=snap(S)==before,adapter_unchanged=snap(A)==ab,input_unchanged=now()==inputs,wall_seconds=time.monotonic()-start),indent=2)+'\n');raise
