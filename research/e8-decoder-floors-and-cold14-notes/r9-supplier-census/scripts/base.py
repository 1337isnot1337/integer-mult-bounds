import sys,json,time
sys.path.insert(0,'/Users/joelpulikkan/imb-harness/r7/tk')
import harness as H
SP='/private/tmp/claude-501/-Users-joelpulikkan-integer-mult-bounds/3231f0a2-7112-4dee-8ef4-f1fca97ae281/scratchpad/r9/'
for w in ['gauge44','extra']:
    t=time.time();P=H.Pricer(SP+f'words/{w}.json.gz');print(w,P.base_cost,P.base_profile,round(time.time()-t),flush=True)
t=time.time();P=H.Pricer(SP+'words/step0-gauge44.json.gz');print('step0',P.base_cost,P.base_profile)
ed=json.load(open(SP+'src/EDITS-1.json'))['edit'];print(ed)
r=P.price(ed);print('k554 on step0',r)
