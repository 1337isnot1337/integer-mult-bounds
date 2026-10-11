from pathlib import Path
import json,os,sys,copy,hashlib,importlib.util
from basis_postprocess import reorder_basis
S=Path('/tmp/task2-pr438-basis-port/source');D=Path(os.environ['E8_OUTPUT'])/'bit426-source-centres';p=D/'bit-source-centres.json';raw=p.read_bytes();w=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='cc6242d90ccdd8477521ea16f35ee2667dbe6c48cc60c6e4e9bcf6460497b233'
w0=copy.deepcopy(w);n=reorder_basis(w);assert w==w0 and reorder_basis(n)==n
for k in set(w)-{'A','B','ret','source_basis_gates'}:assert n[k]==w[k]
old=w['source_basis_gates'];new=n['source_basis_gates'];assert n['A'][:-new]==w['A'][:-old] and n['B'][new:]==w['B'][old:]
sys.path.insert(0,str(S/'vendor/kernel417'));import e8core
r0=e8core.replay(w,span_mode='z');r=e8core.replay(n,span_mode='z');assert not r0['viol'] and not r['viol'] and r['H']==r0['H'] and r['sig']==r0['sig']
def reflected(x):
 v=x['v'];N=2*v+x['R'];rows=[1<<i for i in range(N)];ops=[]
 for ph in ['D','A']:ops.extend((d,s) for f,d,ss in x[ph] for s in ss)
 ops.extend((v+t,q) for k,q in enumerate(x['ret']) for t,a in enumerate(x['scatter']) if k in a)
 for ph in ['B','C']:ops.extend((d,s) for f,d,ss in x[ph] for s in ss)
 for d,s in reversed(ops):rows[d]^=rows[s]
 expected=[1<<i for i in range(N)]
 for t in range(v):expected[v+t]^=1<<t
 assert rows==expected
reflected(w);reflected(n)
sp=importlib.util.spec_from_file_location('original_constructor',S/'code/bit_construct.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);assert mod.replay(n) and not mod.replay(n,skip_inverse=True) and not mod.replay(n,skip_dirt=True)
data=json.dumps(n,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(data).hexdigest()=='2be5d42a53e367648f4dd33fd4a368c61e1565f0cf7c48bfe887ca953a735063'
(D/'bit-source-centres-postkernel-original.json').write_bytes(raw);p.write_bytes(data)
(D/'BASIS-STAGE.json').write_text(json.dumps(dict(status='PASS_POST_KERNEL_BASIS_STAGE',input_sha256=hashlib.sha256(raw).hexdigest(),output_sha256=hashlib.sha256(data).hexdigest(),counts=[old,new],columns=r['n'],profile=r['H'],controls=['inverse omission','dirt omission'],reflected_columns=True,upstream_kernel_receipt_preserved=True),indent=2)+'\n')
print('PASS basis stage',old,new,r['n'])
