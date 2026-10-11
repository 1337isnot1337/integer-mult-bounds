"""Receipt-only completion after wrapper JSON-limit error; no child replay."""
import sys,json,hashlib,gzip
from pathlib import Path
if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions required')
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
A=Path('/tmp/task2-pr384-verification-adapter');O=Path('/tmp/task2-pr384-component-verification-fresh');W=O/'candidate'
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=read(A/'SOURCE-MAPPING.json');R=Path(M['source377_root']);F=Path(M['certificate_snapshot'])
assert sha(A/'MANIFEST.json')=='c5c9072b2ef2439fae694c0dde807828e2e1aaf56a43389962974624a57c9fb7'
adapter=read(A/'MANIFEST.json')
for name,want in adapter.items():assert sha(A/name)==want,name
failure_sha=sha(O/'FAILURE.json');failure=read(O/'FAILURE.json')
assert failure['error'].startswith('Exceeds the limit (4300 digits) for integer string conversion: value has 9634 digits;')
assert failure['original_inputs_unchanged'] is True
stages=failure['stages']
assert [x['stage'] for x in stages]==['original377-full-eight-stage-regression','candidate-regression-pin-preparation','candidate-full-local-admission','candidate-data-banks-profile','candidate-exact-clifford','candidate-data-cover-phases','candidate-global-invoice','candidate-independent-template-moments','candidate-fixed-old-bit-regression']
for x in stages:
 assert x['returncode']==0 and sha(O/'logs'/(x['stage']+'.log'))==x['log_sha256']
old=read(O/'original377/VERIFICATION.json');assert len(old['fresh_stages'])==8 and old['complex_coarse']=='999240641319551/1000000000000000000'
for x in old['fresh_stages']:assert x['returncode']==0 and sha(O/'original377/logs'/(x['stage']+'.log'))==x['log_sha256']
def original_integrity():
 assert sha(R/'MANIFEST.json')==M['source377_manifest_sha256']
 actual={p.relative_to(R).as_posix():sha(p) for p in R.rglob('*') if p.is_file() and p!=R/'MANIFEST.json'}
 assert actual==read(R/'MANIFEST.json')['files'] and not any(p.is_symlink() for p in R.rglob('*'))
 assert sha(F)==M['certificate_compressed_sha256'] and hashlib.sha256(gzip.decompress(F.read_bytes())).hexdigest()==M['certificate_expanded_sha256']
 return actual
initial=original_integrity();frozen=read(O/'CANDIDATE-INPUTS.json')
C=W/'work/native358/vendor/complex-reserve/upstream/pr352/code/complex'
assert read(C/'pins-e8.json')==read(O/'measured-pins.json') and set(read(C/'pins-e8.json'))==set(read(O/'original-pins-e8.json'))
assert "else: raise ValueError('Missing frozen regression pin: '+key)" in (C/'code/p10pins.py').read_text()
assert not (O/'RECEIPT-COMPLETION.json').exists()
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
result=dict(status='PASS_COMPONENT_RECEIPTS_AFTER_JSON_LIMIT_COMPLETION',source_mapping_sha256=sha(A/'SOURCE-MAPPING.json'),adapter_manifest_sha256=sha(A/'MANIFEST.json'),candidate_inputs_sha256=sha(O/'CANDIDATE-INPUTS.json'),fresh_stages=stages,complex_coarse=price['coarse_complex'],clifford=cl,finite_invoice=inv['finite_invoice'],receipt_sha256=receipts,inputs_unchanged=True,scientific_stage_seconds=sum(x['seconds'] for x in stages),new_numerical_priority_claim=False,combined_kappa_admitted=False,scope='Independent component verification of PR384 existing proposed complex saving. Historical admission upstream_head/manifests are original provenance, not candidate provenance; exact consumed mapping and candidate hashes govern this run. Inherited E8/compiler/common-grid/precision/analytic interfaces remain conditional. No bit382 admission or Lean build.')
result.update(original_wrapper_status='FAIL_JSON_REPORT_PARSING_AFTER_ALL_SCIENTIFIC_STAGES',original_failure_sha256=failure_sha,receipt_completion_script_sha256=sha(Path(__file__)),no_child_replay=True)
assert sha(O/'FAILURE.json')==failure_sha
(O/'RECEIPT-COMPLETION.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
