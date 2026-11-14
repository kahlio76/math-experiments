import sys,time
from pysat.formula import CNF
from pysat.solvers import Cadical153
f=CNF(from_file=sys.argv[1]); S=Cadical153(bootstrap_with=f.clauses)
t=time.time(); r=S.solve(); print(sys.argv[1],'SAT' if r else 'UNSAT',f'{time.time()-t:.1f}s',flush=True)
if r:
    m=S.get_model(); N=int(sys.argv[3]); St=int(sys.argv[2])
    print('col:',''.join('A' if m[u-St]>0 else 'B' for u in range(St,N+1)))
    open(sys.argv[1]+'.model','w').write(' '.join(map(str,m)))
