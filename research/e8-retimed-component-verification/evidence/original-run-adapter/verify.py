"""Bounded independent verification of an existing proposed complex component.
No deletion, install, producer/Lean proof or new combined kappa claim.
"""
import os,sys,json,gzip,hashlib,shutil,subprocess,time,argparse
from pathlib import Path
if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions required')
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();O=args.output.resolve()
if O.exists():raise RuntimeError('Fresh output required')
M=read(A/'SOURCE-MAPPING.json');R=Path(M['source377_root']);F=Path(M['certificate_snapshot'])
def original_integrity():
 assert sha(R/'MANIFEST.json')==M['source377_manifest_sha256']
 actual={p.relative_to(R).as_posix():sha(p) for p in R.rglob('*') if p.is_file() and p!=R/'MANIFEST.json'}
 assert actual==read(R/'MANIFEST.json')['files'] and not any(p.is_symlink() for p in R.rglob('*'))
 assert sha(F)==M['certificate_compressed_sha256']
 assert hashlib.sha256(gzip.decompress(F.read_bytes())).hexdigest()==M['certificate_expanded_sha256']
 return actual
initial=original_integrity();adapter=read(A/'MANIFEST.json')
old_cert=json.loads(gzip.decompress((R/'work/pr361/complex/gcert1-e8-r783.json.gz').read_bytes()));new_cert=json.loads(gzip.decompress(F.read_bytes()))
assert {k for k in set(old_cert)|set(new_cert) if old_cert.get(k)!=new_cert.get(k)}=={'A','B','blocks','derived_from','frames'}
assert new_cert['frames'][:len(old_cert['frames'])]==old_cert['frames']
for name,want in adapter.items():assert sha(A/name)==want,name
O.mkdir();(O/'logs').mkdir();(O/'tmp').mkdir()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',TMPDIR=str(O/'tmp'))
for k in ['PYTHONOPTIMIZE','CX_PINS','CX_SOURCE_PINS','CX_RECORD']:env.pop(k,None)
stages=[];begun=time.monotonic()
def run(name,argv,cwd):
 start=time.monotonic();log=O/'logs'/(name+'.log');print(name,flush=True)
 with log.open('w') as f:r=subprocess.run([sys.executable,'-B']+list(map(str,argv)),cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 stages.append(dict(stage=name,returncode=r.returncode,seconds=time.monotonic()-start,log_sha256=sha(log)))
 if r.returncode:raise RuntimeError(name+' failed; all artifacts retained')
try:
 # Unchanged complete original377 regression; no cached PASS substitute.
 run('original377-full-eight-stage-regression',[R/'verify.py','--work',O/'original377'],O)
 old=read(O/'original377/VERIFICATION.json');assert old['complex_coarse']=='999240641319551/1000000000000000000' and len(old['fresh_stages'])==8
 W=O/'candidate';W.mkdir();shutil.copytree(R/'work',W/'work')
 for rel,spec in M['overlays'].items():
  assert sha(R/rel)==spec['original_sha256'] and sha(A/rel)==spec['adapter_sha256']
  (W/rel).write_bytes((A/rel).read_bytes())
 C=W/'work/native358/vendor/complex-reserve/upstream/pr352/code/complex'
 pins=read(C/'inputs/complex/source-pins.json');cp=pins['certificate']
 original_pins=O/'original-pins-e8.json';original_pins.write_bytes((C/'pins-e8.json').read_bytes())
 (W/'work/pr361/complex/gcert1-e8-r783.json.gz').write_bytes(F.read_bytes());(C/cp['path']).write_bytes(F.read_bytes())
 cp.update(compressed_sha256=sha(F),uncompressed_sha256=M['certificate_expanded_sha256'],source_pin=M['source378_head'],url='https://github.com/CrocSwap/integer-mult-bounds/blob/'+M['source378_head']+'/research/e8-complex-far-retiming/data/gcert1-e8-r783-far.json.gz')
 (C/'inputs/complex/source-pins.json').write_text(json.dumps(pins,sort_keys=True,indent=2)+'\n')
 # Preserve structural pins; measure candidate-specific regression values separately.
 p=read(original_pins);structural={k:p[k] for k in ['V','R','H','cst','N','scatter','centre_ranks']}
 (C/'pins-e8.json').write_text(json.dumps(structural,indent=2)+'\n')
 run('candidate-regression-pin-preparation',[A/'measure_pins.py',C,original_pins,O/'measured-pins.json',O/'pin-preparation-guard.json'],W)
 (C/'pins-e8.json').write_bytes((O/'measured-pins.json').read_bytes())
 # Strengthen final pin helper: missing keys are errors, never record-mode acceptance.
 helper=C/'code/p10pins.py';s=helper.read_text();assert s.count('else: RECORD[key]=value')==1
 helper.write_text(s.replace('else: RECORD[key]=value',"else: raise ValueError('Missing frozen regression pin: '+key)"))
 (O/'STRICT-PIN-HELPER.diff').write_text("- else: RECORD[key]=value\n+ else: raise ValueError('Missing frozen regression pin: '+key)\n")
 # Bind actual adapted inputs before final replay. Historical manifests remain original provenance.
 frozen={p.relative_to(W).as_posix():sha(p) for p in W.rglob('*') if p.is_file()}
 (O/'CANDIDATE-INPUTS.json').write_text(json.dumps(frozen,sort_keys=True,indent=2)+'\n')
 run('candidate-full-local-admission',[W/'work/native358/vendor/complex-reserve/admit.py','--source',C.parent.parent,'--output',W/'work/complex-nine-native/local-admission'],W)
 for name,script in [('candidate-data-banks-profile','complex_candidate.py'),('candidate-exact-clifford','verify_clifford_frames.py'),('candidate-data-cover-phases','data_phases.py'),('candidate-global-invoice','global_nine.py'),('candidate-independent-template-moments','audit_nine_template.py'),('candidate-fixed-old-bit-regression','outer_fixed.py')]:
  run(name,[W/'work/odd-stages'/script],W)
 out=W/'work/complex-nine-native';raw=read(out/'local-admission/UPSTREAM-GUARD.json');a=read(out/'local-admission/INDEPENDENT-AUDIT.json');cl=read(out/'CLIFFORD-REVIEW.json');inv=read(out/'GLOBAL-REVIEW.json');price=read(out/'INDEPENDENT-TEMPLATE-AUDIT.json')
 assert a['finite_guard']['all_retained_guards_pass'] and all(a['finite_guard']['controls'].values())
 assert raw['splice']['certificate_sha256']==sha(F) and raw['label_checks']['frame_count']==948 and raw['label_checks']['invocation_calls']==3973
 assert len(raw['splice']['controls'])==20 and all(x['rejected'] for x in raw['splice']['controls']) and len(raw['program_check']['controls'])==2
 for ori in ['forward','backward']:
  assert a['scalar_words'][ori]['all_live_rows_correct'] and a['scalar_words'][ori]['all_private_work_restored_zero'] and a['scalar_words'][ori]['independent_live_columns']==1023
 assert cl['frames']==948 and cl['all_child_equalities_include_global_phase'] and len(price['structural_controls_rejected'])==5 and price['bridge_omission_controls']==9
 assert price['coarse_complex']=='999632926176283/1000000000000000000' and price['next_grid_rejected']
 assert inv['invocations']==72 and inv['rank_mass']==1072575 and inv['deficit']==2496 and inv['finite_invoice']['physical_row_coefficient']<20161
 # Script outputs may overwrite shipped data receipts; code/certificate/pin inputs must not change.
 changed={rel for rel,want in frozen.items() if sha(W/rel)!=want}
 allowed={'work/odd-stages/COMPLEX-NINE-CANDIDATE.json'}
 assert changed<=allowed,changed
 assert original_integrity()==initial
 for name,want in adapter.items():assert sha(A/name)==want,name
 receipts={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file()}
 result=dict(status='PASS_NEW_LOCAL_WORD_NINE_STAGE_COMPONENT_VERIFICATION',source_mapping_sha256=sha(A/'SOURCE-MAPPING.json'),adapter_manifest_sha256=sha(A/'MANIFEST.json'),candidate_inputs_sha256=sha(O/'CANDIDATE-INPUTS.json'),fresh_stages=stages,complex_coarse=price['coarse_complex'],clifford=cl,finite_invoice=inv['finite_invoice'],receipt_sha256=receipts,inputs_unchanged=True,seconds=time.monotonic()-begun,new_numerical_priority_claim=False,combined_kappa_admitted=False,scope='Independent component verification of PR384 existing proposed complex saving. Historical admission upstream_head/manifests are original provenance, not candidate provenance; exact consumed mapping and candidate hashes govern this run. Inherited E8/compiler/common-grid/precision/analytic interfaces remain conditional. No bit382 admission or Lean build.')
 (O/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
except BaseException as e:
 (O/'FAILURE.json').write_text(json.dumps(dict(error=str(e),stages=stages,original_inputs_unchanged=original_integrity()==initial),indent=2)+'\n');raise
