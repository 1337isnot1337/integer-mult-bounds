#!/usr/bin/env python3
"""Merge equal sums across the common-point circuits, with exact certificates.

Supports are represented by their provenance in the small pair circuit, not
by half a million dense global bit vectors. A sum that occurs in two distinct
common-point groups must be a pair-star; its fixed pair and union of vertices
identify its support exactly.
"""
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json

from exclusion_circuit import ExclusionCircuit


class SharedPointCircuit:
    def __init__(self,h,circuit=None):
        """Merge equal pair-star sums across common-point groups.

        Tooling note (shared-point / bit-compression replay): the merge/lookup
        loop keeps the historical node-allocation order and output keys, but
        pre-sorts the local active set and output items once, unpacks child
        mappings without a per-node generator, and binds hot attributes locally.
        ``merged_additions``, topology and ``circuit_sha256`` are unchanged.
        See ``research/shared-point-init/``.
        """
        assert h>=6 and h!=9, 'The ambient form I-J/9 must be nondegenerate'
        self.h=h
        self.local=circuit or ExclusionCircuit(h-1)
        assert self.local.n==h-1, 'Pair circuit has the wrong ground size'
        self.inputs=list(combinations(range(h),3))
        self.variables={t:i+1 for i,t in enumerate(self.inputs)}
        nin=len(self.inputs)
        self.args=[None]*(nin+1)
        self.core=[0]+[sum(1<<i for i in t) for t in self.inputs]
        self.union=list(self.core)
        self.provenance=[None]*(nin+1)
        self.points=[[j for j in range(h) if j!=i] for i in range(h)]
        local_inputs=self.local.inputs
        self.pair_ids=[{tuple(points[k] for k in pair):i+1
                       for i,pair in enumerate(local_inputs)} for points in self.points]
        lookup={};self.outputs={};self.merged=0
        local_args=self.local.args
        active_sorted=sorted(self.local.active)
        outputs_items=sorted(self.local.outputs.items())
        variables=self.variables
        core=self.core;union=self.union;args=self.args;provenance=self.provenance
        append_args=args.append;append_core=core.append
        append_union=union.append;append_prov=provenance.append
        for common in range(h):
            mapping={}
            pts=self.points[common]
            bit=1<<common
            for node in active_sorted:
                ab=local_args[node]
                if ab is None:
                    a,b=local_inputs[node-1]
                    mapping[node]=variables[tuple(sorted((common,pts[a],pts[b])))]
                    continue
                a=mapping[ab[0]];b=mapping[ab[1]]
                cval=core[a]&core[b];uval=union[a]|union[b]
                assert cval&bit
                if cval.bit_count()>=2:
                    key=(cval,uval)
                    hit=lookup.get(key)
                    if hit is not None:
                        mapping[node]=hit;self.merged+=1
                        continue
                    new=len(args);mapping[node]=new
                    append_args((a,b));append_core(cval);append_union(uval)
                    append_prov((common,node));lookup[key]=new
                else:
                    new=len(args);mapping[node]=new
                    append_args((a,b));append_core(cval);append_union(uval)
                    append_prov((common,node))
            outs=self.outputs
            for pair,node in outputs_items:
                outs[common,tuple(sorted((common,*(pts[x] for x in pair))))]=mapping[node]
        self.active=set();stack=list(self.outputs.values());active=self.active
        while stack:
            n=stack.pop()
            if n in active:continue
            active.add(n)
            edge=args[n]
            if edge:stack.extend(edge)
        self.additions=sum(args[n] is not None for n in active)

    @lru_cache(maxsize=16384)
    def support_in(self,node,common):
        """Exact pair-input support in coordinates with this common point."""
        assert self.core[node]&(1<<common)
        if self.args[node] is None:
            pair=tuple(x for x in self.inputs[node-1] if x!=common)
            return 1<<(self.pair_ids[common][pair]-1)
        old,local=self.provenance[node]
        if old==common:return self.local.support[local]
        # This node occurs in two groups, so every triple contains both points.
        assert self.core[node].bit_count()==2
        fixed=self.core[node]&~(1<<common)
        other=fixed.bit_length()-1
        remaining=self.union[node]&~self.core[node]
        answer=0
        while remaining:
            bit=remaining&-remaining;remaining-=bit
            pair=tuple(sorted((other,bit.bit_length()-1)))
            answer|=1<<(self.pair_ids[common][pair]-1)
        return answer

    def contained(self,a,b):
        common=(self.core[b]&-self.core[b]).bit_length()-1
        return bool(self.core[a]&(1<<common)) and not (
            self.support_in(a,common)&~self.support_in(b,common))

    def verify(self):
        self.local.verify()
        digest=sha256()
        for node in sorted(self.active):
            if self.args[node]:
                a,b=self.args[node];common,local=self.provenance[node]
                assert a<node and b<node
                A=self.support_in(a,common);B=self.support_in(b,common)
                assert not A&B
                assert A|B==self.local.support[local]
                assert self.core[node]==self.core[a]&self.core[b]
                assert self.union[node]==self.union[a]|self.union[b]
            assert self.core[node]
            digest.update(json.dumps((node,self.args[node],self.provenance[node]),
                                     separators=(',',':')).encode()+b'\n')
        for (common,target),node in sorted(self.outputs.items()):
            excluded=tuple(self.points[common].index(x) for x in target if x!=common)
            assert self.support_in(node,common)==self.local.support[self.local.outputs[excluded]]
            digest.update(json.dumps((common,target,node),separators=(',',':')).encode()+b'\n')
        return dict(h=self.h,inputs=len(self.inputs),partial_outputs=len(self.outputs),
                    additions=self.additions,roles=self.additions+len(self.outputs),
                    merged_additions=self.merged,
                    all_additions_disjoint=True,all_partial_outputs_exact=True,
                    every_node_has_common_point=True,circuit_sha256=digest.hexdigest())

    compile=ExclusionCircuit.compile

    def verify_frames(self,code=None):
        """Check all role inclusions; reverse frames are orthogonal complements."""
        code=code or self.compile();frames=[0]*code['roles']
        for triple,slot in code['sources'].items():frames[slot]=self.variables[triple]
        for node,ins,outs in code['gates']:
            for slot in set(ins+outs):
                assert not frames[slot] or self.contained(frames[slot],node)
                frames[slot]=node
        for target,slot in code['outputs'].items():assert frames[slot]==self.outputs[target]
        # Output target lines enter the complement of these output spans.
        # The exact output relation proved above supplies that orthogonality.
        reverse=[0]*code['roles']
        for target,slot in code['outputs'].items():reverse[slot]=self.outputs[target]
        for node,ins,outs in reversed(code['gates']):
            for slot in set(ins+outs):
                assert not reverse[slot] or self.contained(node,reverse[slot])
                reverse[slot]=node
        for triple,slot in code['sources'].items():assert reverse[slot]==self.variables[triple]
        return dict(roles=code['roles'],forward_frames_nested=True,
                    reverse_complement_frames_nested=True,
                    nondegeneracy='Every source span has a common point; its orthogonal complement is nondegenerate.')

    def program(self):
        code=self.compile();index={t:i for i,t in enumerate(self.inputs)}
        return dict(triples=self.inputs,roles=code['roles'],
                    gates=[(ins,outs) for _,ins,outs in code['gates']],
                    sources=[(index[t],slot) for t,slot in code['sources'].items()],
                    outputs=[(index[t],slot) for (_,t),slot in code['outputs'].items()])


if __name__=='__main__':
    c=SharedPointCircuit(46)
    print(c.verify())
    print(c.verify_frames())
