"""Measured regression-pin preparation, NOT final candidate admission."""
import sys,os,json,importlib.util
from pathlib import Path
if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions required')
sys.dont_write_bytecode=True
C=Path(sys.argv[1]).resolve()
os.environ['CX_PINS']=str(C/'pins-e8.json')
for key in ['CX_SOURCE_PINS','CX_RECORD']:os.environ.pop(key,None)
s=importlib.util.spec_from_file_location('measured_guard',C/'portable_complex.py');G=importlib.util.module_from_spec(s);s.loader.exec_module(G)
r=G.run(C,progress=lambda s:print(s,flush=True))
import p10pins
old=json.loads((C/'pins-e8.json').read_text());old.update(p10pins.RECORD)
assert set(old)==set(json.loads(Path(sys.argv[2]).read_text())), 'Regression pin key closure changed'
assert r['label_checks']['invocation_calls']==3973 and r['label_checks']['invocation_rank_mass']==9039
Path(sys.argv[3]).write_text(json.dumps(old,sort_keys=True,indent=2)+'\n')
Path(sys.argv[4]).write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print('PIN_PREPARATION_ONLY; final strict pinned replay required')
