import sys
sys.argv=['aug.py','5','-','/dev/null']
src=open('aug.py').read().split("npath=0")[0]
exec(src)
s=(2,2,43);print(at[s],[wid(*r) for r in at[s].values()],bal[s])
for r in at[s].values():print(r,wid(*r),len(idx.get((r[0],wid(*r)-1),())))
Y,prev=bfs(s);print(Y,len(prev))
print([ (o,bal[o],[ (r,wid(*r)) for r in at[o].values()]) for o in snk])
