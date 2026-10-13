import sys,json,pickle
from load import *
from price import price
st=pickle.load(open(sys.argv[1],'rb'));T5=int(sys.argv[3]) if len(sys.argv)>3 else 5
jw=json.load(open(sys.argv[2])) if len(sys.argv)>2 and sys.argv[2]!='-' else reg['jp8']['widths']
prof5=json.load(open(sys.argv[4])) if len(sys.argv)>4 else reg['jp8']['actual_paid_profile']
W=P['windows'];fill=Counter()
for (t,h),o in st.items():
    fill[o]+= jw[h] if t==T5 else reg[P['provider_calls'][t]['provider']]['widths'][h]
idle=Counter()
for k,(c,ts) in W.items():
    a,b=map(int,k.split(','))
    for p in range(112):
        f=fill.get((a,b,p),0);assert f<=c
        if f<c:idle[c-f]+=1
prof=Counter(idle)
for t in range(72):
    pr=prof5 if t==T5 else reg[P['provider_calls'][t]['provider']]['actual_paid_profile']
    for r,c in pr.items():prof[int(r)]+=c
print('idle',sorted(idle.items()),'b',float(price(prof)))
