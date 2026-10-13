from price import price
from load import *
import json
base=Counter({int(k):v for k,v in P['profile'].items()})
b0=price(base)
V={}
for r in range(1,49):
    p=Counter(base);p[r]+=1;p[1]-=r
    V[r]=float((price(p)-b0)*10**9)
print({r:round(v,4) for r,v in V.items()})
json.dump(V,open('V639.json','w'))
