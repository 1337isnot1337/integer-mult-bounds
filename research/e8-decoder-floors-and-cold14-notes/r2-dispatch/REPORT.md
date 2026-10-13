# R2 progress (record track)
Worktree ~/imb-r2 (branch research/cold14-r2, base pr639 cf2f6d77). Tools ~/imb-harness/r2 (load.py, price.py, disp.py, alt*.py, lns*.py, aug.py, mip.py, V639.json).
## Findings so far
- #639 global profile = sum provider profiles + idle; idle = 387072 - total widths. jp8(u4) widths 3890, ck 3854, st2-jp8 (#635 word) 3894.
- Concentrated-idle bound: 72 jp8 -> b 0.0016392558 (+1.118e-7 b over #639 0.0016391440). BUT global assembly controls need 2 dispatched providers (README: ck pinned at t=5 for that reason).
- 2nd-provider options (concentrated bound): st2 jp8 word (#635) x1: b 0.0016392519 (+1.08e-7); jp8 minus one u4 end: 0.0016392548.
- Literal packing: LNS (CP-SAT) for 72 jp8 stalls at ~24 partial owners (b 0.0016389 < base). Perfect packing not found yet.
- Running: mip.py (aggregate free-dispatch exact-window MIP, Hall masks) LP bound over {jp8,ck,st2}.
## Update (handback)
- V639.json: mass-neutral b values (1e-9 b) vs #639 profile. Provider net vs jp8(u4): ck -247.4 profile (+36 width -> net ~-101 => the 1.1e-7 gap); st2 +16.37 profile, +4 width (~-16.3 idle) => ~neutral.
- Lever 1 accounting: u4-type end {1:+2,2:-1,4:+1,5:-1}, width -1 => net -0.025 per end per call (neutral/negative). Dim-7 factored end pair ({1:+2,2:+2,5:-2}, width -4) => +2.25 per pair per call: further dim-7 ends would be the real lever 1.
- Sub-MIP (submip.py, windows touching t<=7, jp8 at t=5, rest fixed): optimum forces 64 owners (9,9,9,9,9) idle 3 in window 5,8 => perfect packing not available locally.
- Launched (may still be running, ~/imb-harness/r2): c1.log = cpagg.py jp8,ck,st2 free dispatch CP-SAT hinted by #639 (only hint solution found so far); f72.log = cpfeas.py pure feasibility of perfect 72-jp8 packing; mip2.log = HiGHS free-dispatch MIP.
- Package skeleton: ~/imb-r2/research/complex-571-cold14-r2 (copy of witness638 + data/recipes/k492-st2-cold_end.json.gz = #635 jp8 recipe, sha 90952fde..). Not wired up; no commit.
Resume: cd ~/imb-harness/r2; cat c1.log f72.log mip2.log. If a dispatch {jp8 x(72-k), st2 x k} with idle profile beating b 0.0016391439889600812 is found: expand (expand_fn.py), wire st2 provider into SPEC/WITNESS (build entry = #635 SPEC build.providers.jp8, providers entry = #635 SPEC providers.jp8, registry = st2-PLAN.json jp8 with directory providers/st2), drop ck/ck_504, fix extras/check_native_owners.py + check_u4_portable provider lists, drop PR638 owner-replay steps from verify.sh, run verify.
