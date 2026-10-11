"""Portable source-extracted hashing contract; no supplier module is imported."""
import ast
import copy
import difflib
import gzip
import hashlib
import json
import statistics
import time
from collections import Counter
from pathlib import Path
from digest_encoder import compile_stream, encoded_records

ROOT = Path(__file__).resolve().parent
ADAPTER = ROOT/'evidence/adapter'


def contains_hash_update(node):
    return any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute)
               and isinstance(x.func.value,ast.Name) and x.func.value.id=='expanded'
               and x.func.attr=='update' for x in ast.walk(node))


def hashing_loop(node):
    return (isinstance(node,ast.For) and ast.unparse(node.target) in ['z','(z, encoded)']
            and contains_hash_update(node))


def validate_source_scope():
    original=(ADAPTER/'original_emit.py').read_text()
    candidate=(ADAPTER/'candidate_emit.py').read_text()
    patch=''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),
        fromfile='original/code/emit.py',tofile='candidate/code/emit.py'))
    assert patch == (ROOT/'EMITTER.patch').read_text()
    old,new=ast.parse(original),ast.parse(candidate)
    loops=[x for x in ast.walk(old) if hashing_loop(x)]
    assert len(loops)==1
    class Normalize(ast.NodeTransformer):
        def __init__(self):self.edits=[0,0,0]
        def visit_ImportFrom(self,node):
            if node.module=='digest_encoder':
                self.edits[0]+=1
                return None
            return node
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='compiled':
                self.edits[1]+=1
                return None
            return self.generic_visit(node)
        def visit_For(self,node):
            if hashing_loop(node):
                self.edits[2]+=1
                return copy.deepcopy(loops[0])
            return self.generic_visit(node)
    normalizer=Normalize()
    normalized=normalizer.visit(new)
    assert normalizer.edits==[1,1,1]
    assert ast.dump(old,include_attributes=False)==ast.dump(normalized,include_attributes=False)


def load_loops():
    # Reuse the exact measured extraction and byte-recorder definitions only.
    # No resource/platform import or main() from the retained harness is executed.
    tree=ast.parse((ADAPTER/'harness.py').read_text())
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))
           and n.name in ['extract','Recorder']]
    assert len(nodes)==2
    module=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
    namespace=dict(ast=ast,copy=copy,json=json,hashlib=hashlib,encoded_records=encoded_records)
    exec(compile(module,'<retained-contract-helpers>','exec'),namespace)
    extract=namespace['extract']
    return extract(ADAPTER/'original_emit.py',False),extract(ADAPTER/'candidate_emit.py',True),namespace['Recorder']


def load_fixtures():
    sources=json.loads((ROOT/'SOURCES.json').read_text())
    return [json.loads(gzip.decompress((ROOT/f['path']).read_bytes())) for f in sources['fixtures']]


def check_records(fixtures):
    original,cached,Recorder=load_loops()
    profiles=[]
    for fixture in fixtures:
        streams=fixture['local_programs']
        compiled={name:compile_stream(events) for name,events in streams.items()}
        before=json.dumps([streams,fixture['calls']],sort_keys=True)
        paid_original,paid_cached=Counter(),Counter()
        hash_original,hash_cached=hashlib.sha256(),hashlib.sha256()
        count=0
        for call in fixture['calls']:
            orientation,owners=call['orientation'],call['owners']
            old=Recorder(aggregate=hash_original)
            new=Recorder(old.rows,aggregate=hash_cached)
            n=len(owners)
            old_count=original(streams,orientation,owners,n,fixture['live'],paid_original,old,compiled)
            new_count=cached(streams,orientation,owners,n,fixture['live'],paid_cached,new,compiled)
            new.finish()
            assert old_count==new_count and old.digest.digest()==new.digest.digest()
            count+=old_count
        assert paid_original==paid_cached and hash_original.digest()==hash_cached.digest()
        assert before==json.dumps([streams,fixture['calls']],sort_keys=True)
        profiles.append(dict(calls=len(fixture['calls']),count=count,digest=hash_original.hexdigest(),
            paid_profile={str(k):v for k,v in sorted(paid_original.items())}))
    return profiles


def benchmark(fixtures):
    original,cached,_=load_loops()
    samples={'original':[],'cached':[]}
    orders=[]
    for repetition in range(3):
        order=[('original',original),('cached',cached)]
        if repetition%2:order.reverse()
        orders.append([name for name,_ in order])
        results=[]
        for name,fn in order:
            start=time.perf_counter()
            digest,paid,count=hashlib.sha256(),Counter(),0
            for fixture in fixtures:
                streams=fixture['local_programs']
                compiled={key:compile_stream(events) for key,events in streams.items()} if name=='cached' else {}
                for call in fixture['calls']:
                    count+=fn(streams,call['orientation'],call['owners'],len(call['owners']),
                              fixture['live'],paid,digest,compiled)
            samples[name].append(time.perf_counter()-start)
            results.append((digest.hexdigest(),paid,count))
        assert results[0]==results[1]
    return dict(seconds_including_compile_and_owner_cache=samples,order=orders,
                median_speedup=statistics.median(samples['original'])/statistics.median(samples['cached']),
                scope='Extracted hashing loop on retained workloads; not end-to-end supplier runtime.')
