"""Conditional cached-response budget only; no native construction."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json,sys,hashlib
if not __debug__:raise RuntimeError('Assertions required')
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/kappa-rebuild/architecture'));import mixed_target_probe as E
source=HERE/'sources/SOURCE-BUDGET.json';a=json.loads(source.read_text());S=Counter({int(k):v for k,v in a['targets'].items()});S.subtract({int(k):v for k,v in a['paid'].items()})
C=Q('.0030217758');budget=E.moment(S,C);assert budget[0]>344 and budget[1]<345
paid=336;remaining=tuple(x-paid for x in budget)
assert remaining[0]>8 and remaining[1]<9
lo,hi=Q('.003'),Q('.004')
for _ in range(28):
 mid=(lo+hi)/2;l,u=E.moment(S,mid)
 if l>paid:lo=mid
 elif u<paid:hi=mid
 else:raise ValueError('Insufficient interval precision')
variants=[]
for count in [8,16]:
 for totalrank,label in [(63,'disjoint nine-axis jobs'),(57,'shared head seven calls')]:
  changed=Counter(S);changed[9]-=7*count;changed[totalrank]+=count
  # A J candidate also removes the eight rank-one H completions in each call.
  if count==16:changed[1]+=56
  margin=E.moment(changed,C)
  variants.append(dict(state_ports=count,merged_rank=totalrank,axis_hypothesis=label,remove_H_completions=(count==16),remaining_after_hypothetical_336_boundary=E.show(tuple(x-336 for x in margin)),all_state_restoration_assumed_not_proved=True))
out=dict(status='CONDITIONAL_CACHE_BOUNDARY_BUDGET_ONLY',benchmark=str(C),budget=E.show(budget),hypothetical_one_head_per_interval_cost=paid,remaining_for_all_cache_work=E.show(remaining),hypothetical_boundary_only_crossing=[str(lo),str(hi)],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),persistent_state_scenarios=variants,no_native_candidate=True,no_kappa_claim=True)
p=HERE/'CACHE-BUDGET.json'
if '--check' in sys.argv:assert json.loads(p.read_text())==out
else:p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
