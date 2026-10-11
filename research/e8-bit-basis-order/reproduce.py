"""Portable pinned-PR433 bit-only reproduction; complex evidence is reused explicitly."""
import argparse,gzip,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PIN='3129eb4321f706542470f8443f66a6b4351a12a9ceec85e7f76aa19db1e1e32f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def snapshot(root):
 paths=list(root.rglob('*'))
 if any(p.is_symlink() for p in paths):raise RuntimeError('Symlinks are outside the pinned closure')
 return {p.relative_to(root).as_posix():sha(p) for p in paths if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json'}
def main():
 if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions must be enabled')
 if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,required=True);group=ap.add_mutually_exclusive_group(required=True);group.add_argument('--output',type=Path);group.add_argument('--check-inputs',action='store_true');a=ap.parse_args();S=a.source.resolve();O=a.output.resolve() if a.output else None
 if O is not None and (O.exists() or O.is_relative_to(ROOT) or O.is_relative_to(S)):raise RuntimeError('Output must be fresh and outside both packages')
 package_before=snapshot(ROOT);source_before=snapshot(S)
 assert package_before==read(ROOT/'MANIFEST.json')['files']
 assert sha(S/'MANIFEST.json')==sha(ROOT/'inputs/SUPPLIER-MANIFEST.json')==PIN
 assert source_before==read(S/'MANIFEST.json')['files']
 provenance=read(ROOT/'SOURCES.json')
 for z in provenance['files']:
  raw=(ROOT/z['path']).read_bytes();raw=gzip.decompress(raw) if z['gzip'] else raw
  assert hashlib.sha256(raw).hexdigest()==z['original_sha256'],z['path']
 original=(ROOT/'vendor/bit_construct.py').read_text();assert original==(S/'code/bit_construct.py').read_text()
 changes=[('sorted(echelon.items())','sorted(echelon.items(), reverse=True)'),('p = (row & -row).bit_length() - 1','p = row.bit_length() - 1'),('pivots = sorted(echelon)','pivots = sorted(echelon, reverse=True)')]
 derived=original
 for before,after in changes:
  assert derived.count(before)==1;derived=derived.replace(before,after)
 assert hashlib.sha256(derived.encode()).hexdigest()=='61578d8959893e7fec667d5e7697cc6faef773d1e7c50a45e929e69a0038f279'
 expected=read(ROOT/'EXPECTED.json');candidate=gzip.decompress((ROOT/'inputs/candidate/word.json.gz').read_bytes());assert hashlib.sha256(candidate).hexdigest()==expected['candidate_sha256']
 baseline=read(ROOT/'inputs/baseline/COMPLETION.json');assert baseline['status']=='PASS_RETAINED_DEFAULT_PR433_REPLAY' and baseline['returncode']==0 and baseline['source_manifest_before']==baseline['source_manifest_after']==PIN
 copies=[('source','inputs/e8-r865.json.gz','work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz'),('source','inputs/bit-geometry.json.gz','inherited/bit-geometry.json.gz')]+[('source','vendor/engines/'+n+'.py','work/pr361/code/engines/'+n+'.py') for n in ['moment','base_two_moment','outer']]+[('package','inputs/complex/'+n+'.json','split-centres/'+n+'.json') for n in ['INTEGRATION','INDEPENDENT-REPLAY']]
 for kind,path,dst in copies:
  assert sha((S if kind=='source' else ROOT)/path)==baseline['output_hashes']['run/'+dst],path
 # Input mode validates bytes and the exact three-line derivation only; it executes no supplier stage.
 if a.check_inputs:
  assert snapshot(ROOT)==package_before and snapshot(S)==source_before
  print(json.dumps(dict(status='PASS_INPUTS_ONLY_NO_SCIENTIFIC_EXECUTION',derived_constructor_sha256=hashlib.sha256(derived.encode()).hexdigest(),candidate_sha256=expected['candidate_sha256'],source_manifest_sha256=PIN)));return
 start=time.monotonic();O.mkdir();(O/'scratch').mkdir();steps=[]
 def copy(data,dst):
  p=O/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 for kind,path,dst in copies:copy(((S if kind=='source' else ROOT)/path).read_bytes(),dst)
 p=O/'bit426-source-centres';p.mkdir();copy(gzip.decompress((S/'inputs/bit-r767.json.gz').read_bytes()),'bit426-source-centres/bit-input.json');copy(derived.encode(),'derived-bit-construct.py')
 env=dict(os.environ,E8_OUTPUT=str(O),PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(O/'scratch'));env.pop('PYTHONOPTIMIZE',None)
 def run(name,script,*args):
  with (O/(name+'.log')).open('w') as log:r=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],cwd=O,env=env,stdout=log,stderr=subprocess.STDOUT)
  steps.append(dict(name=name,returncode=r.returncode,log_sha256=sha(O/(name+'.log'))));assert r.returncode==0,(name,r.returncode)
 try:
  run('construct',O/'derived-bit-construct.py');assert sha(p/'bit-source-centres.json')==expected['candidate_sha256']
  run('export',S/'vendor/export_records.py',p/'bit-source-centres.json',p/'records')
  run('global',S/'code/bit_global.py','--source',p,'--local-check',p,'--out',p/'global')
  run('audit',S/'code/bit_audit.py','--local-check',p,'--out',p/'global')
  run('price',S/'code/bit_price.py');run('combined',S/'code/combined.py')
  result=read(O/'RESULT.json');assert result['kappa']==expected['kappa']
  g=read(p/'global/GLOBAL.json');geo=read(p/'global/GEOMETRY.json');E=g['paid_calls'];J=576*998+61440+2*g['bank_assignments']+2*g['copy_erase_episodes'];selectors=144*(14501+758*64*(geo['max_route_factors']+127))
  coefficient=72*g['local_additions']+g['bridge_additions']+J*(16*4097**2+14511)+E*(8*64**2+8+128*128**3)+16*64**3+g['copy_erase_episodes']+selectors+int(g['global_prefix_bound'])+1
  assert str(coefficient)==expected['coefficient'] and str((coefficient+1)**2*(E+1)**2)==expected['two_level_coefficient']
  assert snapshot(ROOT)==package_before and snapshot(S)==source_before
  completion=dict(status='PASS_PORTABLE_CHANGED_BIT_FINITE_REPRODUCTION',scope='Changed bit stages; original complex evidence reused; no complex/phase replay',steps=steps,source_manifest_sha256=PIN,package_manifest_sha256=sha(ROOT/'MANIFEST.json'),source_before=source_before,source_after=snapshot(S),package_before=package_before,package_after=snapshot(ROOT),coefficient=str(coefficient),wall_seconds=time.monotonic()-start,child_usage=list(resource.getrusage(resource.RUSAGE_CHILDREN)),output_hashes=snapshot(O))
  (O/'COMPLETION.json').write_text(json.dumps(completion,indent=2)+'\n');print(completion['status'])
 except BaseException as e:
  (O/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps,source_unchanged=snapshot(S)==source_before,package_unchanged=snapshot(ROOT)==package_before,wall_seconds=time.monotonic()-start),indent=2)+'\n');raise
if __name__=='__main__':main()
