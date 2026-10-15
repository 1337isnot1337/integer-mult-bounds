import sys, time
from f2check import *
perp = lambda l: [T for T in range(60) if T != l and not NO[l, T]]
D=eval(sys.argv[1])
t=time.time(); ok,sol=solve_opts([[(perp(a),perp(b)),(perp(b),perp(a))] for a,b in D]); print('free orientation:',ok,'%.1fs'%(time.time()-t))
if ok: print('decoder check',check_decoder(*sol))
