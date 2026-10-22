"""Exact numerical support for the scoped threshold proof; stdlib only."""
from fractions import Fraction as Q
from math import factorial

def need(ok,msg):
    if not ok: raise ValueError(msg)

# A positive partial sum is a rigorous lower bound for exp(11/5).
s=sum((Q(11,5)**j)/factorial(j) for j in range(21))
need(s>9,'log(9) < 11/5')
need(9*Q(1,330)*Q(11,5)==Q(3,50),'per-bridge deficit bound')
need(2-33*Q(3,50)==Q(1,50),'strict positive moment gap')
spaces={frozenset([0])}
for x in range(1,8):
    spaces|={frozenset(set(U)|{u^x for u in U}) for U in tuple(spaces)}
def dim(U):return len(U).bit_length()-1
need(len(spaces)==16,'all binary three-dimensional ambient subspaces')
count=0
for U in spaces:
    for V in spaces:
        a,b,i=dim(U),dim(V),dim(U&V)
        r=a+b-2*i
        need(0<=r<=3,'subspace distance range')
        need(r==(b-a)+2*(a-i),'rank mass decomposition')
        need((a-i==0)==(U<=V),'zero excess exactly ascending')
        count+=1
print('PASS_SCOPED_NONNESTED_THRESHOLD',count,'ordered pairs; gap > 1/50')
