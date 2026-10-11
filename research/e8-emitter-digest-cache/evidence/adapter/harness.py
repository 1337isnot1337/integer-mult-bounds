"""Execute only AST-extracted original/patched hashing loops on retained fixtures.
No supplier main(), imports, compiler, geometry, phase, price or assembly execution.
Output must be fresh. All inputs remain unchanged; no cleanup.
"""
import ast,copy,gzip,hashlib,json,os,resource,sys,time,statistics
from pathlib import Path
from collections import Counter
from digest_encoder import compile_stream,encoded_records
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def closure():
 m=json.loads((ROOT/'MANIFEST.json').read_text());assert set(m)=={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
 for n,h in m.items():assert sha(ROOT/n)==h,n
 return sha(ROOT/'MANIFEST.json')
def extract(path,patched):
 tree=ast.parse(path.read_text());main=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main')
 def hashes_expanded(loop):
  return any(isinstance(y,ast.Call) and isinstance(y.func,ast.Attribute) and y.func.attr=='update' and isinstance(y.func.value,ast.Name) and y.func.value.id=='expanded' for y in ast.walk(loop))
 loops=[x for x in ast.walk(main) if isinstance(x,ast.For) and (ast.unparse(x.target)=='(z, encoded)' if patched else ast.unparse(x.target)=='z') and hashes_expanded(x)]
 assert len(loops)==1
 # Exact original loop body, with only initial counter and return added.
 args=['streams','ori','owners','LOCAL','LIVE','paid','expanded','compiled']
 fn=ast.FunctionDef(name='run',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=a) for a in args],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[ast.Assign(targets=[ast.Name(id='full_event_count',ctx=ast.Store())],value=ast.Constant(0)),copy.deepcopy(loops[0]),ast.Return(value=ast.Name(id='full_event_count',ctx=ast.Load()))],decorator_list=[])
 mod=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]));env={'json':json,'encoded_records':encoded_records};exec(compile(mod,str(path)+':extracted-loop','exec'),env);return env['run']
class Recorder:
 def __init__(self,expected=None,aggregate=None):self.expected=None if expected is None else iter(expected);self.rows=[];self.digest=hashlib.sha256();self.aggregate=aggregate
 def update(self,b):
  if self.expected is not None:assert b==next(self.expected)
  else:self.rows.append(b)
  self.digest.update(b)
  if self.aggregate is not None:self.aggregate.update(b)
 def finish(self):
  if self.expected is not None:
   try:next(self.expected)
   except StopIteration:pass
   else:raise AssertionError('extra original record')
def main(out):
 if not __debug__ or sys.flags.optimize:raise RuntimeError('assertions disabled')
 assert not out.exists();out.mkdir();start=time.perf_counter();manifest=closure();pins=json.loads((ROOT/'INPUTS.json').read_text());assert hashlib.sha1(b'blob '+str((ROOT/'original_emit.py').stat().st_size).encode()+b'\0'+(ROOT/'original_emit.py').read_bytes()).hexdigest()==pins['emitter_git_blob']
 fixtures=[]
 try:
  for pin in pins['fixtures']:
   p=Path(pin['path']);assert sha(p)==pin['sha256'];fixtures.append(json.loads(gzip.decompress(p.read_bytes())))
  orig=extract(ROOT/'original_emit.py',False);fast=extract(ROOT/'candidate_emit.py',True);records=0;profiles=[];opcodes=set();signed=False;private=False
  for d in fixtures:
   streams=d['local_programs'];compiled={k:compile_stream(v) for k,v in streams.items()};before=json.dumps([streams,d['calls']],sort_keys=True);po=Counter();pf=Counter();ho=hashlib.sha256();hf=hashlib.sha256()
   for c in d['calls']:
    ori=c['orientation'];owners=c['owners'];n=len(owners);a=Recorder(aggregate=ho);b=Recorder(a.rows,aggregate=hf) # independent actual-byte aggregates
    co=orig(streams,ori,owners,n,d['live'],po,a,compiled);cf=fast(streams,ori,owners,n,d['live'],pf,b,compiled);b.finish();assert co==cf and a.digest.digest()==b.digest.digest();records+=co
   assert po==pf and ho.digest()==hf.digest();assert before==json.dumps([streams,d['calls']],sort_keys=True);profiles.append({'calls':len(d['calls']),'count':sum(len(streams[c['orientation']]) for c in d['calls']),'digest':ho.hexdigest(),'paid_profile':dict(sorted(po.items()))})
   for events in streams.values():
    opcodes.update(z[0] for z in events);signed|=any(any(x<0 for x in z) for z in events);private|=any(z[0]!=0 and z[2]>=n for z in events)
  assert opcodes=={0,1,2,3} and signed and private
  rejected=[]
  for z in [[0,0],[1,0,0],[2,0,1,2,3,4],[3,0,1,2,3,4,False]]:
   try:compile_stream([z])
   except AssertionError:rejected.append(z)
   else:raise AssertionError('invalid schema accepted')
  # Setup-inclusive repeated-call timings, both fixtures/all calls. Hashes/accounting still exact.
  times={'original':[],'cached':[]};orders=[]
  for rep in range(3):
   digests=[]
   order=[('original',orig),('cached',fast)] if rep%2==0 else [('cached',fast),('original',orig)]
   orders.append([name for name,fn in order])
   for name,fn in order:
    t=time.perf_counter();hd=hashlib.sha256();paid=Counter();cnt=0
    for d in fixtures:
     streams=d['local_programs'];compiled={k:compile_stream(v) for k,v in streams.items()} if name=='cached' else {}
     for c in d['calls']:cnt+=fn(streams,c['orientation'],c['owners'],len(c['owners']),d['live'],paid,hd,compiled)
    times[name].append(time.perf_counter()-t);digests.append((hd.hexdigest(),cnt,paid))
   assert digests[0]==digests[1]
  assert closure()==manifest
  for pin in pins['fixtures']:assert sha(Path(pin['path']))==pin['sha256']
  result={'status':'PASS_EXACT_EXTRACTED_HASHING_LOOP','manifest_sha256':manifest,'records_byte_compared':records,'fixtures':profiles,'opcodes':sorted(opcodes),'signed_and_private_operands':True,'schema_controls':len(rejected),'timings_including_compile_and_owner_cache':times,'benchmark_order':orders,'median_speedup':statistics.median(times['original'])/statistics.median(times['cached']),'seconds':time.perf_counter()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'hashing-loop microbenchmark only; no full wrapper/runtime/numerical improvement claim','python':sys.version,'source_and_fixtures_unchanged':True}
  (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
 except BaseException as e:
  closure();(out/'FAILURE.json').write_text(json.dumps({'error':repr(e),'source_manifest':manifest,'seconds':time.perf_counter()-start},indent=2)+'\n');raise
if __name__=='__main__':main(Path(sys.argv[1]).resolve())
