from pathlib import Path
import os,sys,json,gzip,hashlib,copy,importlib.util
O=Path(os.environ['FIXTURE_OUTPUT']);S=Path(__file__).resolve().parent/'source/research/idle-axis-hosting';B=O/'parent/bit426-source-centres';H=O/'hosted'
read=lambda p:json.loads(p.read_bytes());parent=json.loads(gzip.decompress((B/'global/GLOBAL-TEMPLATE.json.gz').read_bytes()));t=json.loads(gzip.decompress((H/'GLOBAL-TEMPLATE.json.gz').read_bytes()))
sp=importlib.util.spec_from_file_location('original442audit',S/'audit.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
st=read(B/'records/249-states.json');fs=read(B/'records/frames.json')['frames'];width=[8-fs[str(st['initial'][str(i)])]['dim'] for i in range(240,987)]
profile,n=a.audit_bit(t,parent,width);g=read(H/'GLOBAL.json');assert profile=={int(r):z for r,z in g['profile'].items()} and n==g['hosted_residuals']==39568
assert (g['live'],g['physical'],g['maxchild'])==(9457,9466,8)
def scalar(events):
 x=[1<<i for i in range(8)]
 for e in events:
  if e['kind']=='local_cover_sweep':p=e['pair'];src,dst=(2*p+1,2*p) if e['reverse'] else (2*p,2*p+1);x[dst]^=x[src]
  elif e['kind']=='bridge':
   if e['coefficient']&1:d,s=e['dst'],e['src'];x[2*d]^=x[2*s];x[2*s+1]^=x[2*d+1]
  elif e['kind']=='exchange':
   for p in range(4):x[2*p],x[2*p+1]=x[2*p+1],x[2*p]
 return x
identity=[1<<i for i in range(8)];assert scalar(t['schedule'])==identity;out=[]
for name in ['omit_terminal_exchange','zero_bridge_coefficient']:
 q=copy.deepcopy(t)
 if name=='omit_terminal_exchange':assert q['schedule'][-1]['kind']=='exchange';q['schedule'].pop()
 else:next(e for e in q['schedule'] if e['kind']=='bridge')['coefficient']=0
 p,m=a.audit_bit(q,parent,width);assert p==profile and m==n;v=scalar(q['schedule']);assert v!=identity
 out.append(dict(name=name,original_audit_accepted=True,wrong_columns=sum(a!=b for a,b in zip(v,identity)),columns=v))
(O/'AUDIT-CONTRACT.json').write_text(json.dumps(dict(status='PASS_ACTUAL442_BIT_FIXTURE_AND_AUDIT_REGRESSIONS',parent_template_sha256=hashlib.sha256(gzip.decompress((B/'global/GLOBAL-TEMPLATE.json.gz').read_bytes())).hexdigest(),hosted_template_sha256=hashlib.sha256(gzip.decompress((H/'GLOBAL-TEMPLATE.json.gz').read_bytes())).hexdigest(),profile=dict(profile),hosted_residuals=n,mutations=out,scope='Actual442bit template positive fixture and audit contract regressions; no new phase,price,combinedbound orcomplex run'),indent=2)+'\n');print('PASS actual442bit positive +2 accepted invalid schedule mutations')
