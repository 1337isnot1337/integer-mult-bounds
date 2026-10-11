import hashlib,json,os,runpy,shutil
from pathlib import Path
src=Path('/tmp/pr275-pr433-static');r=Path('/tmp/task2-pr433-default-envelope/run');out=Path('/tmp/pr275-pr433-finite-capture');out.mkdir()
for name in ['bit426-source-centres/global/GLOBAL.json','bit426-source-centres/global/GEOMETRY.json','bit426-source-centres/global/AUDIT.json','split-centres/INTEGRATION.json','split-centres/INDEPENDENT-REPLAY.json','work/pr361/code/engines/outer.py','work/pr361/code/engines/moment.py','work/pr361/code/engines/base_two_moment.py']:
 dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/name,dest)
os.environ['E8_OUTPUT']=str(out)
x=runpy.run_path(str(src/'code/combined.py'),run_name='__main__')
actual=json.loads((out/'RESULT.json').read_text());original=json.loads((r/'RESULT.json').read_text())
assert actual=={k:v for k,v in original.items() if k not in ['verification_steps','phase_mode','manifest_sha256']}
report={'status':'PASS_UNCHANGED_PR433_ASSEMBLY_LOCALS','combined_source_sha256':hashlib.sha256((src/'code/combined.py').read_bytes()).hexdigest(),'coefficient':str(x['coefficient']),'two_level_coefficient':str(x['two']),'route_items':x['J'],'selectors':x['selectors'],'unit_additions':x['unit'],'source_result_sha256':hashlib.sha256((r/'RESULT.json').read_bytes()).hexdigest()}
(out/'LOCALS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
