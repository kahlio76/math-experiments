import sys, itertools
from pysat.solvers import Cadical153
def solve_block(I, low, extra_fixed=()):
    I=list(I); idx={v:i for i,v in enumerate(I)}; n=len(I)
    var={}
    def o(u,v):  # literal: u before v
        if u<v: return var.setdefault((u,v),len(var)+1)
        return -var.setdefault((v,u),len(var)+1)
    for u in I:
        for v in I:
            if u<v: o(u,v)
    S=Cadical153()
    # transitivity
    for a,b,c in itertools.permutations(I,3):
        if a<b and a<c: pass
        S.add_clause([-o(a,b),-o(b,c),o(a,c)]) if True else None
    Iset=set(I); lowset=set(low)
    ncross=0
    for x in I:
        for y in I:
            if y<=x: continue
            z=2*y-x
            if z in Iset:
                # o(x,y) <-> o(z,y)
                S.add_clause([-o(x,y),o(z,y)]); S.add_clause([o(x,y),-o(z,y)])
    for b in I:
        for c in I:
            if c>b and (2*b-c) in lowset: S.add_clause([o(c,b)]); ncross+=1
            if c<b and (2*b-c) in lowset: S.add_clause([o(c,b)]); ncross+=1  # decreasing AP a>b>c with a earlier
    r=S.solve()
    order=None
    if r:
        m=set(l for l in S.get_model() if l>0)
        before={u:sum(1 for v in I if v!=u and (o(v,u) in m if o(v,u)>0 else -o(v,u) not in m)) for u in I}
        order=sorted(I,key=lambda u:before[u])
    return r,ncross,order
if __name__=="__main__":
    J=int(sys.argv[1])
    for name,blocks,low0 in [('A',[(4**j,2*4**j) for j in range(J)],[0]),('B',[(2*4**j,4**(j+1)) for j in range(J)],[])]:
        low=list(low0)
        for (L,R) in blocks:
            r,nc,order=solve_block(range(L,R),low)
            print(name,L,R,'SAT' if r else 'UNSAT','cross',nc, order[:40] if order and R-L<=64 else '',flush=True)
            low+=list(range(L,R))
