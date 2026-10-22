"""Elementary rational enclosures; no floating point in acceptance."""
from fractions import Fraction as Q
from collections import Counter

def log_bounds(r):
 k=r.bit_length()-1;y=Q(r,1<<k)
 def atanh(z):
  n=45;s=sum((2*z**(2*j+1)/Q(2*j+1) for j in range(n)),Q(0));tail=2*z**(2*n+1)/Q(2*n+1)/(1-z*z);return s,s+tail
 a,b=atanh(Q(1,3));c,d=atanh((y-1)/(y+1));return k*a+c,k*b+d

def exp_minus(x):
 assert 0<=x<1
 term=Q(1);s=term
 for j in range(1,23):term*=-x/Q(j);s+=term
 # degree22 is upper; degree23 is lower by the alternating-series theorem.
 return s+term*(-x/Q(23)),s

def power(r,kappa):
 a,b=log_bounds(r);lo,_=exp_minus(kappa*b);_,hi=exp_minus(kappa*a);return r*lo,r*hi

def check():
 target=Counter({8:18*439,127:222});paid=Counter({1:18*(1198+117)+111*15,2:18*1255,3:18*207,4:18*86,5:18*41,6:18*23,7:18})
 for length in (7,8):
  for j in range(1,length+1):target[1+7*(j+1)]+=222;paid[7*(j+1)]+=222
 out=[]
 for kappa in (Q(3464248972,10**12),Q(12401086416,10**12)):
  bounds={r:power(r,kappa) for r in paid.keys()|target.keys()}
  lo=sum(n*bounds[r][0] for r,n in paid.items())-sum(n*bounds[r][1] for r,n in target.items());hi=sum(n*bounds[r][1] for r,n in paid.items())-sum(n*bounds[r][0] for r,n in target.items());assert lo>0
  unit=10**6;a=lo.numerator*unit//lo.denominator;b=-((-hi.numerator*unit)//hi.denominator)
  assert Q(a,unit)<=lo<=hi<=Q(b,unit)
  out.append(dict(kappa=str(kappa),paid_minus_target_lower_micro=a,paid_minus_target_upper_micro=b,strict_first_moment_fails=True))
 return out
if __name__=='__main__':print(check())
