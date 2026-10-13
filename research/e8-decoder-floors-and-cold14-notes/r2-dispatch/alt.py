from price import price
from load import *
base=Counter()
for r,c in reg['jp8']['actual_paid_profile'].items(): base[int(r)]+=72*c
print('target 0.0016391439889600812')
for split in ([48],[47,1],[44,4],[40,8],[36,12],[24,24],[46,2],[45,3],[47,47,2],[16,16,16]):
    p=Counter(base);p[48]+=2229-1 if sum(split)==48 else 2229-2
    for g in split:p[g]+=1
    print(split,float(price(p)))
