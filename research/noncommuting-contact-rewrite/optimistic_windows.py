from conjugate_windows import *
rows=[]
for i,k,corr in patterns:
 prof,_=price(i,k,{})
 assert prof is not None
 delta={r:prof[r]-old[r] for r in prof.keys()|old.keys() if prof[r]!=old[r]};gain=-sum(n*r**t for r,n in delta.items())
 if gain>1e-10:
  rows.append(dict(first=i,last=k,corrections={str(j):e for j,e in corr.items()},optimistic_gain=gain,delta=delta))
rows.sort(key=lambda r:-r['optimistic_gain']);(HERE/'OPTIMISTIC-WINDOWS.json').write_text(json.dumps(rows,indent=2)+'\n');print('OPTIMISTIC_CANDIDATES',len(rows),[(r['first'],r['last'],r['optimistic_gain']) for r in rows[:20]])
