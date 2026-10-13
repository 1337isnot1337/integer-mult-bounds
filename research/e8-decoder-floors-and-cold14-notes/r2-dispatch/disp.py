import json,sys
from collections import Counter
from fractions import Fraction as Q
from price import price
P=json.load(open('/Users/joelpulikkan/imb-r2/research/pr638-improvement-20261013/witness638/data/PLAN.json'))
reg=P['provider_registry']
W={p:sum(reg[p]['widths']) for p in reg}
print(W)
base=Counter({int(k):v for k,v in P['profile'].items()})
print('base b',float(price(base)))
for nck in range(0,6):
    prof=Counter()
    for p,n in (('jp8',72-nck),('ck',nck)):
        for r,c in reg[p]['actual_paid_profile'].items(): prof[int(r)]+=n*c
    idle=107028+(W['jp8']-W['ck'])*(nck-1)
    prof[48]+=idle//48
    if idle%48: prof[idle%48]+=1
    b=price(prof);print(nck,idle,float(b))
