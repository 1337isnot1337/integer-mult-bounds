"""Commuting-window retiming census: move one B add gate g=(t += c*s) to the far end (earliest / latest) of its maximal
window of commuting neighbours (h commutes with g iff h neither reads t nor writes s; scales on t or s block).
Exact by construction (checked again mod p by the pricer).  usage: retime.py WORD OUT.json"""
import gzip,json,sys
w=json.load(gzip.open(sys.argv[1]));B=w['B'];out=[]
def comm(g,h):
    if g[0]!='add': return False
    t,s=g[1],g[2]
    if h[0]=='scale': return h[1] not in (t,s)
    return h[2]!=t and h[1]!=s
for i,g in enumerate(B):
    if g[0]!='add': continue
    j=i
    while j+1<len(B) and comm(g,B[j+1]): j+=1
    k=i
    while k-1>=0 and comm(g,B[k-1]): k-=1
    gate=list(g[:5])+[[]]
    if j>i: out.append(dict(pivot=g[2],kind='late',gate=i,to=j,ed=dict(delete=[i],insert=[[j+1,gate]],tail=[],prepend=[])))
    if k<i: out.append(dict(pivot=g[2],kind='early',gate=i,to=k,ed=dict(delete=[i],insert=[[k,gate]],tail=[],prepend=[])))
print(len(out));json.dump(out,open(sys.argv[2],'w'))
