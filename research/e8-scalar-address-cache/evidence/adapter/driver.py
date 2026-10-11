import argparse, ast, copy, gzip, hashlib, json, platform, resource, sys, time
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def payload(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def closure():
    cfg=json.loads((HERE/'INPUTS.json').read_text()); hashes={}
    for entry in cfg['files']:
        p=Path(entry['path']); assert not p.is_symlink() and sha(p)==entry['sha256']; hashes[str(p)]=sha(p)
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for name,h in manifest.items(): assert sha(HERE/name)==h
    hashes['adapter_manifest']=sha(HERE/'MANIFEST.json')
    original=Path(cfg['original']); b=original.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==cfg['git_blob']
    for f in cfg['fixtures']:
        c=json.loads(Path(f['completion']).read_text()); assert c['status']==f['status'] and c['source_before']==c['source_after']
        assert c['output_hashes'][f['output_key']]==sha(Path(f['path']))
        assert all(s.get('returncode',s.get('rc',0))==0 for s in c['steps'])
    return cfg,hashes

def extract(path):
    tree=ast.parse(path.read_text()); recipe=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='recipe')
    main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    starts=[i for i,n in enumerate(main.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='events' for t in n.targets)]
    assert len(starts)==1
    end=next(i for i in range(starts[0],len(main.body)) if isinstance(main.body[i],ast.Assign) and any(isinstance(t,ast.Name) and t.id=='indexed' for t in main.body[i].targets))
    section=copy.deepcopy(main.body[starts[0]:end])
    # No supplier imports/main/hosting calls are executed.
    fn=ast.FunctionDef(name='run',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=n) for n in ['streams','V','R']],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.parse('LOCAL=2*V+R').body+section+[ast.Return(value=ast.Dict(keys=[ast.Constant(n) for n in ['vals','levels','schedule','stages','bridge_controls','z','nb']],values=[ast.Name(id=n,ctx=ast.Load()) for n in ['vals','levels','schedule','stages','bridge_controls','z','nb']]))],decorator_list=[])
    ns={'K':5,'L':11}; exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(recipe),fn],type_ignores=[])),str(path),'exec'),ns)
    return ns['run'],ns['recipe'],section

def operand_contract(section,streams,V,R,events):
    loops=[n for n in ast.walk(ast.Module(body=section,type_ignores=[])) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='e' and any(isinstance(k,ast.FunctionDef) and k.name=='mapper' for k in ast.walk(n))]
    assert len(loops)==1
    local=next(n for n in ast.walk(loops[0]) if isinstance(n,ast.FunctionDef) and n.name=='mapper')
    count=0; private=0; reflected=set(); stages=set(); LOCAL=2*V+R; n=10*V+11*R
    for e in events:
        if e['kind']!='local': continue
        s,p,rev=e['stage'],e['pair'],e['reverse']; ns=dict(LOCAL=LOCAL,temp=n,V=V,R=R,K=5,s=s,p=p,rev=rev)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(local)],type_ignores=[])),'exact-original-mapper','exec'),ns)
        mapping=ns['mapper']; table=[mapping(i) for i in range(LOCAL+1)]; assert table[LOCAL]==n
        for z in streams['reverse' if rev else 'forward']:
            if z[0]==0: continue
            assert z[0] in (1,2,3)
            for i in z[1:3]:
                assert type(i) is int and 0<=i<=LOCAL and mapping(i)==table[i]; count+=1;private+=i==LOCAL
        reflected.add(rev);stages.add(s)
    assert stages==set(range(11)) and reflected=={False,True} and private>0
    return dict(operands=count,private_operands=private,stages=sorted(stages),reflections=sorted(reflected))

HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    if not __debug__ or sys.flags.optimize: raise RuntimeError('assertions required')
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();assert not out.exists() and not out.is_relative_to(HERE);out.mkdir()
    start=time.monotonic();before=None
    try:
        cfg,before=closure();old,recipe,section=extract(Path(cfg['original']));new,newrecipe,_=extract(Path(cfg['candidate']));assert recipe()==newrecipe();events=recipe();assert len([e for e in events if e['kind']=='local'])==11
        results=[]
        for fixture in cfg['fixtures']:
            t=json.loads(gzip.decompress(Path(fixture['path']).read_bytes()));streams=t['local_programs'];V=120;R=len(t['calls'][0]['owners'])-2*V
            assert all(len(c['owners'])==2*V+R for c in t['calls'])
            bounds=operand_contract(section,streams,V,R,events)
            original=old(streams,V,R);candidate=new(streams,V,R);assert original==candidate
            assert candidate['nb']==24 and candidate['bridge_controls']==list(range(24)) and candidate['levels']==[10]*5
            timings=[]
            for rep in range(3):
                order=['original','candidate'] if rep%2==0 else ['candidate','original'];dur={}
                for key in order:
                    tick=time.perf_counter();actual=(old if key=='original' else new)(streams,V,R);dur[key]=time.perf_counter()-tick;assert actual==original
                timings.append(dict(order=order,seconds=dur))
            results.append(dict(fixture=fixture['path'],R=R,contract=bounds,complete_replay_sha256=payload(candidate),columns=len(candidate['vals'])-1,stages=candidate['stages'],controls=candidate['bridge_controls'],timings=timings))
        _,after=closure();assert before==after
        result=dict(status='PASS_EXACT_SCALAR_REPLAY_ADDRESS_MAP_CONTRACT',scope='setup-inclusive scalar-replay microbenchmark on retained local words; not fresh supplier admission',inputs_before=before,inputs_after=after,fixtures=results,wall_seconds=time.monotonic()-start,platform=platform.platform(),machine=platform.machine(),python=sys.version,ru_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,ru_maxrss_unit='bytes' if sys.platform=='darwin' else 'KiB')
        (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    except BaseException as e:
        try: _,after=closure()
        except BaseException as check: after={'closure_failure':repr(check)}
        (out/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),inputs_before=before,inputs_after=after,wall_seconds=time.monotonic()-start),indent=2)+'\n');raise
