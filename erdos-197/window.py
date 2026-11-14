import sys, itertools, time
from pysat.solvers import Cadical153
def window_sat(Fa, Fb, M, M2):
    W=list(range(M,M2+1)); cnt=[0]
    def new(): cnt[0]+=1; return cnt[0]
    col={w:new() for w in W}   # true = A
    o={}
    def O(u,v):
        if u>v: return -O(v,u)
        if (u,v) not in o: o[(u,v)]=new()
        return o[(u,v)]
    S=Cadical153()
    for u,v,w in itertools.combinations(W,3):
        a,b,c=O(u,v),O(v,w),O(w,u)
        for sg in (1,-1):
            pre=[-sg*col[u],-sg*col[v],-sg*col[w]]
            S.add_clause(pre+[-a,-b,-c]); S.add_clause(pre+[a,b,c])
    Wset=set(W)
    for x in W:
        for y in W:
            if y<=x: continue
            z=2*y-x
            if z not in Wset: break
            a,b=O(x,y),O(z,y)
            for sg in (1,-1):
                pre=[-sg*col[x],-sg*col[y],-sg*col[z]]
                S.add_clause(pre+[-a,b]); S.add_clause(pre+[a,-b])
    # attacks: u in F (placed before all of W), v in W, z=2v-u in W same class => z before v
    for F,sg in ((Fa,1),(Fb,-1)):
        for u in F:
            for v in W:
                z=2*v-u
                if z in Wset and z!=v:
                    S.add_clause([-sg*col[v],-sg*col[z],O(z,v)])
    r=S.solve(); return r
K=int(sys.argv[1]); M=int(sys.argv[2]); M2=int(sys.argv[3])
surv=[]
t0=time.time()
for mask in range(1<<(K-1)):   # color of 1 fixed = A (symmetry)
    Fa=[1]+[k for k in range(2,K+1) if mask>>(k-2)&1]; Fb=[k for k in range(2,K+1) if not mask>>(k-2)&1]
    if window_sat(Fa,Fb,M,M2): surv.append(mask)
print(f"K={K} window=[{M},{M2}] survivors {len(surv)}/{1<<(K-1)} ({time.time()-t0:.0f}s)")
for mask in surv[:40]:
    print(''.join('A' if k==1 or mask>>(k-2)&1 else 'B' for k in range(1,K+1)))
