#!/usr/bin/env python3
"""Independent endpoint-width and append-only repair audit of PR4633."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import gzip,json,sys
if sys.flags.optimize:raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'research/kappa-rebuild/bit/sources/pr589-regenerated'
artifact_bytes=(HERE/'QUOTIENT-BIT-WORD.json.gz').read_bytes();a=json.loads(gzip.decompress(artifact_bytes));word_bytes=(SOURCE/'WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(word_bytes));frames=json.loads((SOURCE/'records/frames.json').read_text())['frames'];assert sha256(word_bytes).hexdigest()==a['source_word_sha256']
# Independent exhaustive nullspace enumeration in ambient F2^8.
spaces={}
for key,f in frames.items():
 masks=[sum((x%2)<<i for i,x in enumerate(row)) for row in f['A']]
 space={x for x in range(256) if all((x&m).bit_count()%2==0 for m in masks)}
 assert len(space)==1<<f['dim'];spaces[int(key)]=space

def dimensions(kernel):
 pivot=(kernel&-kernel).bit_length()-1
 def phi(x):
  if x>>pivot&1:x^=kernel
  return (x&((1<<pivot)-1))|((x>>(pivot+1))<<pivot)
 out={}
 for f,space in spaces.items():
  image={phi(x) for x in space};d=len(image).bit_length()-1;assert len(image)==1<<d
  out[f]=8 if d==7 else d # PR4633's re-padding of every full-image frame.
 return out
old_dims={int(k):f['dim'] for k,f in frames.items()}
def widths(d):return [d[f]-d[s] for s,f in zip(w['start'],w['final'])]
assert widths(old_dims)[:222]==[7]*222
all_rows=[]
for kernel in range(1,256):
 ds=dimensions(kernel);r=widths(ds);pairs=Counter(zip(r[:111],r[111:222]));assert all(v in (6,8) for v in r[111:222])
 all_rows.append(dict(kernel=kernel,main_widths=dict(sorted(Counter(r[:222]).items())),pairs={f'{a},{b}':n for (a,b),n in sorted(pairs.items())},pairs_with_equal_width=sum(n for (a,b),n in pairs.items() if a==b),append_width7_rank_lower_bound=sum(abs(v-7) for v in r[:222])))
row=all_rows[a['kernel_vector']-1];assert a['kernel_vector']==150
r=widths(dimensions(150));ad={int(k):v for k,v in a['frame_dims'].items()};ar=[ad[f]-ad[s] for s,f in zip(a['start'],a['final'])];assert r==ar
assert row['pairs']=={'7,6':101,'7,8':4,'8,6':6} and row['pairs_with_equal_width']==0
assert row['append_width7_rank_lower_bound']==117 and Counter(r[222:])=={8:439}
# Recompute the declared paid invoice from records, not RESULT.json.
paid=Counter()
for op,x,y,cc,f,z in a['records']:
 if op==0 and f:paid[f]+=1
 elif op==2:paid[abs(ad[cc]-ad[f])]+=1
assert paid=={1:1198,2:1255,3:207,4:86,5:41,6:23,7:1}
old=Counter({1:1323,2:1342,3:79,4:44,5:102,6:11,7:19});repair=paid.copy();repair[1]+=117
caps=[sum((repair[r]-old[r])*min(r,k) for r in set(repair)|set(old)) for k in range(1,8)]
assert caps==[8,24,127,102,35,29,11] and min(caps)>0
# Controls: changing an endpoint width or omitting one paid repair fails.
bad=list(ar);bad[0]-=1;assert bad!=r
under=paid.copy();under[1]+=116;assert sum(k*n for k,n in under.items())!=sum(k*n for k,n in repair.items())
consumer=(ROOT/'research/kappa-rebuild/bit/mixed_productive_bit.py').read_text();assert 'matrix[x] = shift(matrix[x], 1 << (stage+1))' in consumer and 'matrix[y] = shift(matrix[y], 1 << (stage+1))' in consumer
# Audit the final dimension-three revision separately, without overwriting the
# independently checked original kernel150 receipt.
latest_bytes=(HERE/'LATEST-QUOTIENT-BIT-WORD.json.gz').read_bytes();latest=json.loads(gzip.decompress(latest_bytes))
K={0}
for v in latest['kernel_basis']:K|={x^v for x in tuple(K)}
k=len(K).bit_length()-1;assert k==3 and len(K)==8
ld={}
for f,space in spaces.items():
 inter=len(space&K);d=old_dims[f]-(inter.bit_length()-1);assert inter==1<<(inter.bit_length()-1)
 ld[f]=8 if d==8-k else d
lr=widths(ld);lad={int(f):d for f,d in latest['frame_dims'].items()};lar=[lad[f]-lad[s] for s,f in zip(latest['start'],latest['final'])]
assert lr==lar and Counter(lr[:222])=={4:103,7:70,8:49} and Counter(lr[222:])=={8:439}
lpaid=Counter()
for op,x,y,cc,f,z in latest['records']:
 if op==0 and f:lpaid[f]+=1
 elif op==2:lpaid[abs(lad[cc]-lad[f])]+=1
assert lpaid=={1:1020,2:495,3:75,4:442,5:143,6:4,7:12,8:2}
repair_add=Counter(abs(v-7) for v in lr[:222] if v!=7);assert repair_add=={3:103,1:49}
lrepair=lpaid+repair_add;target=Counter({8:18*439,127:222});globalpaid=Counter({r:18*n for r,n in lrepair.items()});globalpaid[1]+=111*15
for length in (7,8):
 for j in range(1,length+1):target[1+7*(j+1)]+=222;globalpaid[7*(j+1)]+=222
globalcaps=[sum(n*min(r,q) for r,n in globalpaid.items())-sum(n*min(r,q) for r,n in target.items()) for q in range(1,128)]
assert min(globalcaps)==globalcaps[-1]==525 and all(v>0 for v in globalcaps)
latest_receipt=dict(source_head='b390d64abfcdba1a3816b86fc763cbc95d43c12c',artifact_sha256=sha256(latest_bytes).hexdigest(),kernel_basis=latest['kernel_basis'],kernel_dimension=k,main_widths=dict(sorted(Counter(lr[:222]).items())),optimistic_append_repairs=dict(sorted(repair_add.items())),paid=dict(sorted(lpaid.items())),repaired_paid=dict(sorted(lrepair.items())),repaired_global_capped_paid_minus_target=globalcaps,all_concave_first_moments_fail=True)

from exact_moment import check as moment_check
exact_margins=moment_check()
out=dict(latest_dimension_three=latest_receipt,exact_first_moment_failures=exact_margins,status='PASS_PR4633_ENDPOINT_AND_APPEND_REPAIR_AUDIT',source_pr=4633,source_head='b2998bacd50d57c301fe67c5392054440c42398c',artifact_sha256=sha256(artifact_bytes).hexdigest(),source_word_sha256=sha256(word_bytes).hexdigest(),kernel150=row,all255_kernels=all_rows,paid=dict(sorted(paid.items())),optimistic_append_repaired_paid=dict(sorted(repair.items())),capped_repaired_minus_source=caps,source_paid_mass=sum(k*n for k,n in old.items()),repaired_paid_mass=sum(k*n for k,n in repair.items()),scope='Existing width-seven common-stage consumer; append-only independent main corrections with unchanged quotient word, helpers and all other invoice rows. Not a lower bound on re-synthesis or a changed controller.',no_new_kappa=True)
if '--check' in sys.argv:assert json.loads((HERE/'RESULT.json').read_text())==json.loads(json.dumps(out))
else:(HERE/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['status'],'kernel150 pairs',row['pairs'],'append cost >=117; capped gaps',caps)
