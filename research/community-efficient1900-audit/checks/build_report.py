from pathlib import Path
import json,shutil,hashlib,collections
P=Path('/tmp/pr-efficient1900');R=Path('/tmp/integer-mult-efficient1100-20261015');A=R/'research/community-efficient1900-audit';A.mkdir(parents=True,exist_ok=True)
sel=json.loads((P/'selection.json').read_text());ledger=json.loads((R/'docs/research/pr-ledger.json').read_text());old={x['number']:x for x in ledger['pull_requests']};states=json.loads((P/'integration-state.json').read_text()) if (P/'integration-state.json').exists() else {};ready=json.loads((P/'ready-scopes.json').read_text()) if (P/'ready-scopes.json').exists() else {}
# Sparse merges can remove unchanged historical ledger inputs. Restore only missing bytes.
import subprocess
for rel in list(ledger['source_sha256'])+['research/pr-reconciliation-20261012/starting-snapshot.json']:
 f=R/rel
 if not f.exists():
  f.parent.mkdir(parents=True,exist_ok=True)
  f.write_bytes(subprocess.check_output(['git','show','HEAD:'+rel],cwd=R))
shutil.copytree(P/'packets',A/'packets',dirs_exist_ok=True);shutil.copy2(P/'selection.json',A/'SELECTION.json');shutil.copy2(P/'live-snapshot.json',A/'LIVE-SNAPSHOT.json');(A/'checks').mkdir(exist_ok=True)
for pat in ['check-*.json','check-*.log','provenance-*.json','finding-*.json','run_2921.py','run_2906.py','run_2906_supplement.py','prepare_2906.py','baseline_2906.py','hydrate_2906.py','extract_native_group.py','prepare_native_inputs.py','run_native_group.py','run_native_traffic_stock.py','authenticate_native_exports.py','register_native_group.py']:
 for f in P.glob(pat):shutil.copy2(f,A/'checks'/f.name)
if (P/'combined-2906/tests/test_exit_cleanup_macos.py').exists():shutil.copy2(P/'combined-2906/tests/test_exit_cleanup_macos.py',A/'checks/test_exit_cleanup_macos.py')
rows=[]
for item in sel['prs']:
 n=item['number'];meta=json.loads((P/f'{n}.json').read_text());pk=json.loads((P/'packets'/f'{n}.json').read_text());prior=old.get(n,{});same=prior.get('reviewed_head')==pk['head'];accepted=str(n) in ready;state=states.get(str(n));published=state is not None and state['state']=='MERGED'
 question=prior.get('unresolved_question') if same else None
 if not question:question=('Revised head: compare against the prior reviewed source and complete affected review/replay obligations.' if prior else 'Review the complete changed-file inventory and claim scope; authenticate dependencies and finish declared checks before incorporation.')
 scope=ready[str(n)] if accepted else ('Carry forward prior unresolved obligations; this pass authenticates current metadata and the complete Git diff, not the mathematical claim.' if same else 'Exact-head metadata and complete Git-diff inventory only; substantive review and verification remain pending.')
 rows.append(dict(number=n,metadata={k:meta[k] for k in ('number','title','author','headRefOid','isDraft')},reviewed_head=pk['head'],current_head=pk['head'],prior_reviewed_head=prior.get('reviewed_head'),disposition='incorporated' if published else 'partially_reviewed',github_state='MERGED' if published else 'OPEN',integration_location=list(pk['path_groups']) if published else [],unresolved_question=None if published else 'Reviewed; publication pending.' if accepted else question,closure=dict(kind='merged',merge_commit=state['mergeCommit']['oid'],url=meta['url']) if published else None,scope=scope,ready_to_integrate=accepted,review_completion=dict(changed_file_coverage=accepted,scoped_mechanism_review=accepted,required_execution_complete=accepted,published=published),verification_evidence=list(dict.fromkeys(prior.get('verification_evidence',[])+[f'research/community-efficient1900-audit/packets/{n}.json']+[f'research/community-efficient1900-audit/checks/{f.name}' for f in sorted(P.glob(f'check-{n}*.json'))]))))
(A/'DISPOSITIONS.json').write_text(json.dumps(dict(scope=sel['scope'],pull_requests=rows),indent=2)+'\n')
merged=sum(x['review_completion']['published'] for x in rows);metrics=dict(selected=100,ready=len(ready),merged=merged,remaining=100-merged,baseline=sel['baseline'],new=44,revised=4,carry_forward=52,limits='Inventory collection is not a completed review. Heavy checks serial, sampled 1GiB process-group guard; no Lean, Docker or new agents.')
(A/'METRICS.json').write_text(json.dumps(metrics,indent=2)+'\n')
lines=['# Efficient nineteenth 100-PR reconciliation','',f'**{merged} merged; {100-merged} pending.** Frozen selection: 44 new submissions, four revised heads and 52 carried-forward reviews. Baseline `{sel["baseline"]}`. Complete Git inventories are retained for all 100; this does not grant mathematical approval.','', 'The selected conditional κ is unchanged. Attribution and predecessor notices remain with each contribution. Prior unresolved review obligations carry forward; neither age nor a smaller headline justifies closure.','', '## Reviewed contributions','','| PR | Contributor | Scope |','| --- | --- | --- |']
for x in rows:
 if x['ready_to_integrate']:lines.append(f'| [#{x["number"]}](https://github.com/CrocSwap/integer-mult-bounds/pull/{x["number"]}) | {x["metadata"]["author"]["login"]} | {x["scope"]} |')
lines+=['','## Remaining review','','| PR | Contributor | Next step |','| --- | --- | --- |']
for x in rows:
 if not x['ready_to_integrate']:lines.append(f'| [#{x["number"]}](https://github.com/CrocSwap/integer-mult-bounds/pull/{x["number"]}) | {x["metadata"]["author"]["login"]} | {x["unresolved_question"].replace("|","/")} |')
lines+=['','## Evidence and limits','','Packets bind each author head, complete Git changed-file inventory and baseline. Checks retain commands, logs, exact inputs and failed setup attempts. Ready groups may integrate independently of longer reviews. Source-authenticated prior verification may be reused only for unchanged inputs and stated coverage. No full supplier replay, formal theorem audit or selected-bound change is implied.','','## Open next questions','','Complete the remaining mechanism, proof, compatibility and execution obligations, grouping shared dependencies and keeping expensive replays serial. Refresh the live queue before any closure decision.','']
text='\n'.join(lines);(A/'README.md').write_text(text);(R/'docs/research/community-efficient1900-review.md').write_text(text)
if (P/'resolution-plan.json').exists():shutil.copy2(P/'resolution-plan.json',A/'INTEGRATION-RESOLUTIONS.json')
print(metrics)
