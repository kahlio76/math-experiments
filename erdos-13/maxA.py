import sys, itertools
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
def solve(N,r):
    W=WCNF()
    # var i <-> i in A, i=1..N
    for a in range(1,N+1):
        larger=list(range(a+1,N+1))
        # multisets of size r from larger with sum divisible by a
        # DP-ish enumeration with pruning by combinations_with_replacement
        for combo in itertools.combinations_with_replacement(larger,r):
            if sum(combo)%a==0:
                W.append([-a]+[-b for b in set(combo)])
    for i in range(1,N+1): W.append([i],weight=1)
    with RC2(W) as rc:
        m=rc.compute(); A=[x for x in m if x>0]
    return A
r=int(sys.argv[1])
for N in range(int(sys.argv[2]),int(sys.argv[3])+1,int(sys.argv[4])):
    A=solve(N,r)
    print(f"r={r} N={N} max|A|={len(A)} N/(r+1)={N/(r+1):.2f} excess={len(A)-N/(r+1):.2f} A={A}",flush=True)
