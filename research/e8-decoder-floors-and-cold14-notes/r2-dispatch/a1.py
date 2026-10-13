from load import *
print(len(rows), rows[0])
occ=defaultdict(list)
for r in rows: occ[(r['owner_replica'],r['child'],r['port'])].append(r)
fill={k:sum(r['width'] for r in v) for k,v in occ.items()}
part=[(k,fill[k],P['windows'][f'{k[0]},{k[1]}'][0]) for k in fill if fill[k]<P['windows'][f'{k[0]},{k[1]}'][0]]
print('partial',part, [ (r['time'],r['helper'],r['width']) for r in occ[part[0][0]]])
t5=[r for r in rows if r['time']==5]
ckw=reg['ck']['widths'];jw=reg['jp8']['widths']
mism=Counter((ckw[h],jw[h]) for h in range(492) if ckw[h]!=jw[h])
print('mismatch by index',mism)
# roles per owner stats
print(Counter(len(v) for v in occ.values()))
empty=[k for k in ((o,c,p) for k2 in P['windows'] for o,c in [map(int,k2.split(','))] for p in range(112)) if k not in occ]
print('empty owners',len(empty), Counter(f'{k[0]},{k[1]}' for k in empty).most_common(40))
