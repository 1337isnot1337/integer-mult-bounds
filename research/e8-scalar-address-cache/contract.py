"""Portable exact-source scalar-replay contracts, without supplier imports."""
import ast
import copy
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import re
import statistics
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'evidence/candidate'


def apply_patch_text(original, patch):
    # Locate each complete old hunk by unique exact context. The other patch
    # may have shifted line numbers, but no context may be altered or guessed.
    lines=original.splitlines(True); patchlines=patch.splitlines(True)
    assert patchlines[0].startswith('--- ') and patchlines[1].startswith('+++ ')
    out=[]; position=0; i=2
    while i<len(patchlines):
        match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',patchlines[i])
        assert match,patchlines[i]
        i+=1;oldlines=[];newlines=[]
        while i<len(patchlines) and not patchlines[i].startswith('@@ '):
            row=patchlines[i];assert row[0] in ' +-'
            if row[0] in ' -':oldlines.append(row[1:])
            if row[0] in ' +':newlines.append(row[1:])
            i+=1
        assert len(oldlines)==int(match[2] or 1) and len(newlines)==int(match[4] or 1)
        positions=[j for j in range(position,len(lines)-len(oldlines)+1) if lines[j:j+len(oldlines)]==oldlines]
        assert len(positions)==1
        start=positions[0];out.extend(lines[position:start]);out.extend(newlines)
        position=start+len(oldlines)
    out.extend(lines[position:]);return ''.join(out)


def validate_source_scope():
    original=(SOURCE/'original_emit.py').read_text()
    candidate=(SOURCE/'candidate_emit.py').read_text()
    patch=(ROOT/'ADDRESS-MAP.patch').read_text()
    assert ''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),
        fromfile='original/code/emit.py',tofile='candidate/code/emit.py'))==patch
    assert apply_patch_text(original,patch)==candidate
    old,new=ast.parse(original),ast.parse(candidate)
    expected=ast.parse('global_indices = [mapper(i) for i in range(LOCAL + 1)]').body[0]
    replacement=ast.parse('x,y=mapper(z[1]),mapper(z[2])').body[0]
    class Normalize(ast.NodeTransformer):
        def __init__(self):self.edits=[0,0]
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='global_indices':
                assert ast.dump(node)==ast.dump(expected)
                self.edits[0]+=1;return None
            if ast.unparse(node.targets[0])=='(x, y)' and ast.unparse(node.value)=='(global_indices[z[1]], global_indices[z[2]])':
                self.edits[1]+=1;return copy.deepcopy(replacement)
            return self.generic_visit(node)
    normalizer=Normalize();normalized=normalizer.visit(new)
    assert normalizer.edits==[1,1] and ast.dump(old)==ast.dump(normalized)
    digestpatch=(ROOT/'evidence/DIGEST.patch').read_text()
    digestcandidate=(ROOT/'evidence/digest_candidate_emit.py').read_text()
    combined=(ROOT/'evidence/combined_emit.py').read_text()
    assert apply_patch_text(original,digestpatch)==digestcandidate
    assert apply_patch_text(candidate,digestpatch)==apply_patch_text(digestcandidate,patch)==combined
    receipt=json.loads((ROOT/'evidence/COMPOSITION.json').read_text())
    assert receipt['status']=='PASS_PATCH_COMPOSITION_BOTH_ORDERS'
    assert hashlib.sha256(combined.encode()).hexdigest()==receipt['combined_sha256']


def load_functions():
    # Only the exact measured extraction and operand validator are executed.
    # The retained driver's imports, closure(), main and timed loop are not run.
    tree=ast.parse((ROOT/'evidence/adapter/driver.py').read_text())
    names={'extract','operand_contract','payload'}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(nodes)==len(names)
    ns=dict(ast=ast,copy=copy,hashlib=hashlib,json=json)
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),
                 '<retained-scalar-contract-functions>','exec'),ns)
    return ns['extract'],ns['operand_contract'],ns['payload']


def load_fixtures():
    return [json.loads(gzip.decompress((ROOT/f'inputs/fixture-{i}.json.gz').read_bytes())) for i in range(2)]


def check_records(fixtures):
    extract,operand_contract,payload=load_functions()
    old,recipe,section=extract(SOURCE/'original_emit.py')
    new,newrecipe,_=extract(SOURCE/'candidate_emit.py')
    assert recipe()==newrecipe()
    profiles=[]
    for template in fixtures:
        streams=template['local_programs'];V=120;R=len(template['calls'][0]['owners'])-2*V
        assert all(len(c['owners'])==2*V+R for c in template['calls'])
        before=payload(streams)
        bounds=operand_contract(section,streams,V,R,recipe())
        original,candidate=old(streams,V,R),new(streams,V,R)
        assert original==candidate
        assert candidate['nb']==24 and candidate['bridge_controls']==list(range(24)) and candidate['levels']==[10]*5
        assert before==payload(streams)
        profiles.append(dict(R=R,contract=bounds,complete_replay_sha256=payload(candidate),
            columns=len(candidate['vals'])-1,stages=candidate['stages'],controls=candidate['bridge_controls']))
    return profiles


def benchmark(fixtures):
    extract,_,_=load_functions()
    old,_,_=extract(SOURCE/'original_emit.py');new,_,_=extract(SOURCE/'candidate_emit.py')
    results=[]
    for template in fixtures:
        streams=template['local_programs'];V=120;R=len(template['calls'][0]['owners'])-2*V
        baseline=old(streams,V,R);timings=[]
        for repetition in range(3):
            order=['original','candidate'] if repetition%2==0 else ['candidate','original'];seconds={}
            for key in order:
                start=time.perf_counter();actual=(old if key=='original' else new)(streams,V,R)
                seconds[key]=time.perf_counter()-start
                assert actual==baseline
            timings.append(dict(order=order,seconds=seconds))
        ratio=statistics.median(t['seconds']['original'] for t in timings)/statistics.median(t['seconds']['candidate'] for t in timings)
        results.append(dict(timings=timings,median_speedup=ratio))
    return results
