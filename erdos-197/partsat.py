import sys, itertools, time
from pysat.solvers import Cadical153
N=int(sys.argv[1]); lam=float(sys.argv[2]); start=int(sys.argv[3]) if len(sys.argv)>3 else 1
V=list(range(start,N+1))
cnt=[0]
def new(): cnt[0]+=1; return cnt[0]
col={u:new() for u in V}   # true = class A
o={}
def O(u,v):  # u before v (only meaningful if same color)
    if u<v:
        if (u,v) not in o: o[(u,v)]=new()
        return o[(u,v)]
    return -O(v,u)
S=Cadical153(); ncl=0
def add(c):
    global ncl; S.add_clause(c); ncl+=1
def same(u,v,w):
    # returns list of (clause-prefix) for "all same color" cases
    return [[-col[u],-col[v],-col[w]],[col[u],col[v],col[w]]]
# fixed orders
fixed=0
for u in V:
    for v in V:
        if u<v and v>lam*u: add([O(u,v)]); fixed+=1
# transitivity among same color: for each triple, if same color then no cyclic orientation
for u,v,w in itertools.combinations(V,3):
    for pre in same(u,v,w):
        # forbid cycles u<v<w<u and u>v>w>u in order sense
        add(pre+[-O(u,v),-O(v,w),-O(w,u)])
        add(pre+[O(u,v),O(v,w),O(w,u)])
# AP constraints: x<y<z, z=2y-x : middle extremal => O(x,y) <-> O(z,y)
nap=0
for x in V:
    for y in V:
        if y<=x: continue
        z=2*y-x
        if z>N: break
        for pre in same(x,y,z):
            add(pre+[-O(x,y),O(z,y)]); add(pre+[O(x,y),-O(z,y)]); nap+=1
add([col[V[0]]])  # symmetry break
t=time.time(); r=S.solve()
print(f"N={N} lam={lam} vars={cnt[0]} clauses={ncl} fixed={fixed} aps={nap} -> {'SAT' if r else 'UNSAT'} ({time.time()-t:.1f}s)",flush=True)
if r:
    m=set(l for l in S.get_model() if l>0)
    A=[u for u in V if col[u] in m]; B=[u for u in V if col[u] not in m]
    def order(C):
        def before(u,v): 
            l=O(u,v); return (l in m) if l>0 else (-l not in m)
        return sorted(C,key=lambda u: sum(1 for w in C if w!=u and before(w,u)))
    print('A:',''.join('A' if col[u] in m else 'B' for u in V))
    print('orderA:',order(A)[:60]); print('orderB:',order(B)[:60])
