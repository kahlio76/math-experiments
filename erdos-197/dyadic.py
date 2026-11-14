# Partition: A = {0} ∪ ⋃_j [4^j, 2*4^j), B = rest. Blocks ordered sequentially.
# Within block I=[L,2L): LSB-binary preference order; check constraint (ii) consistency.
import sys
def blocks_A(J): return [(4**j, 2*4**j) for j in range(J)]
def blocks_B(J): return [(2*4**j, 4**(j+1)) for j in range(J)]
def check(blocks, extra_low, name):
    for j,(L,R) in enumerate(blocks):
        low=set(extra_low)
        for (l,r) in blocks[:j]: low|=set(range(l,r))
        I=range(L,R)
        pref={}  # (k,w)->bit
        conflict=0; npairs=0
        for b in I:
            for c in range(b+1,R):
                a=2*b-c
                if a in low:
                    npairs+=1
                    d=c-b; k=(d&-d).bit_length()-1; w=b&((1<<k)-1); bit=(c>>k)&1
                    if pref.setdefault((k,w),bit)!=bit: conflict+=1
        print(name,j,L,R,'pairs',npairs,'conflicts',conflict)
check(blocks_A(6),[0],'A'); check(blocks_B(6),[],'B')
