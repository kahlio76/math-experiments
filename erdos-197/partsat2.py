import sys, itertools, time
from pysat.solvers import Cadical153
N=int(sys.argv[1]); lam=float(sys.argv[2]); start=int(sys.argv[3]) if len(sys.argv)>3 else 1
V=list(range(start,N+1)); cnt=[0]
def new(): cnt[0]+=1; return cnt[0]
col={u:new() for u in V}
TRUE=new()
o={}
def O(u,v):
    if u>v: return -O(v,u)
    if v>lam*u: return TRUE
    if (u,v) not in o: o[(u,v)]=new()
    return o[(u,v)]
S=Cadical153(); ncl=0
S.add_clause([TRUE])
def add(c):
    global ncl
    if TRUE in c: return
    c=[l for l in c if l!=-TRUE]
    S.add_clause(c); ncl+=1
def same(u,v,w): return [[-col[u],-col[v],-col[w]],[col[u],col[v],col[w]]]
for u,v,w in itertools.combinations(V,3):
    if w>lam*u and v>lam*u and w>lam*v: continue
    a,b,c=O(u,v),O(v,w),O(w,u)
    for pre in same(u,v,w):
        add(pre+[-a,-b,-c]); add(pre+[a,b,c])
nap=0
for x in V:
    for y in V:
        if y<=x: continue
        z=2*y-x
        if z>N: break
        a,b=O(x,y),O(z,y)
        for pre in same(x,y,z):
            add(pre+[-a,b]); add(pre+[a,-b]); nap+=1
S.add_clause([col[V[0]]])
t=time.time(); r=S.solve()
print(f"N={N} lam={lam} vars={cnt[0]} clauses={ncl} -> {'SAT' if r else 'UNSAT'} ({time.time()-t:.1f}s)",flush=True)
if r:
    m=set(l for l in S.get_model() if l>0)
    print('col:',''.join('A' if col[u] in m else 'B' for u in V),flush=True)
