#!/usr/bin/env python3
"""Find exact conjugate-ADD rewrites, not commuting gate relocations."""
import json,gzip,sys
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
x=json.loads(gzip.decompress((ROOT/'research/helper-warp-joint/ACTUAL-WORD.json.gz').read_bytes()));c=x['canonical'];raw=[e for e in x['programs']['forward'] if e[0]!='climb']
def rs(e):
 if e[0]=='scalar':
  g=e[1];return {tuple(r) for r in (g[1:3] if g[0] in ('add','copy') else g[1:2])}
 if e[0]=='warp':return {tuple(e[1])}
 if e[0]=='center':return {('C',e[1])}
 return set()
def add(e):return e[0]=='scalar' and e[1][0]=='add' and all(r[0]=='L' for r in e[1][1:3])
touch=[rs(e) for e in raw];last={};candidates=[];counts=Counter()
for k,e in enumerate(raw):
 if not add(e):continue
 g=e[1];key=tuple(g[1]),tuple(g[2]);u=Q(g[3],g[4]);prior=last.get(key);last[key]=(k,u)
 if prior is None or prior[1]!=-u:continue
 i=prior[0];a=raw[i][1];t,s=key;outside=touch[i]
 # Find a unique middle event touching either outer role.
 mids=[j for j in range(i+1,k) if touch[j]&outside]
 if len(mids)!=1:continue
 j=mids[0];b=raw[j]
 if not add(b):continue
 bg=b[1];d,src=tuple(bg[1]),tuple(bg[2]);v=Q(bg[3],bg[4]);first=-u
 if src==t and d!=s:dst,source,co=d,s,first*v
 elif d==s and src!=t:dst,source,co=t,src,-first*v
 else:continue
 allroles=touch[i]|touch[j]
 if any(touch[z]&allroles for z in range(i+1,k) if z!=j):continue
 candidates.append(dict(indices=[i,j,k],outer=a,middle=bg,correction=['add',list(dst),list(source),co.numerator,co.denominator],frames=[raw[z][2] for z in (i,j,k)]));counts['exact_conjugation_patterns']+=1
print(dict(counts),'events',len(raw));(HERE/'PATTERNS.json').write_text(json.dumps(candidates,indent=2)+'\n')
