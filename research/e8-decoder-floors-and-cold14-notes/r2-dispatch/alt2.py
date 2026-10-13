from price import price
from load import *
J=Counter({int(r):c for r,c in reg['jp8']['actual_paid_profile'].items()})
def b(var_delta,wdelta,n=1):
    p=Counter()
    for r,c in J.items():p[r]+=72*c
    for r,c in var_delta.items():p[r]+=n*c
    idle=106992-n*wdelta
    p[48]+=idle//48
    if idle%48:p[idle%48]+=1
    return float(price(p))
print('target',0.0016391439889600812)
print('identical',b({},0))
print('minus one u4 end',b({1:-2,2:1,4:-1,5:1},1))
print('minus 4 u4 (st2)',b({1:-8,2:4,4:-4,5:4},4))
print('plus one dim8 end (u4-like)',b({1:2,2:-1,4:1,5:-1},-1))
