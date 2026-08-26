#!/usr/bin/env python3
"""W21 -- what survives of the move-2 kill after Theorem W21-M2 is refuted.
UNAUDITED.  Exact / combinatorial only.

The refuted step was 'all dim >= 2 and none in a coordinate hyperplane =>
per not identically 0'.  The surviving, sharper obstruction is a DEAD-CELL
COLUMN count: a dead cell of the cross block (i,j) at (a,b) forces
M_j^x[i][b] = 0 whenever x_i = a.  If TWO dead cells land in the SAME column
b of the same M_j^x, that column of M_j^x is a vector of V_j vanishing in two
coordinates -- and if dim V_j = 2 the only such vector is 0, contradicting
'every occupied cell is nonzero'.  So for such (x,j) either dim V_j = 3, or
V_j meets a codimension-2 coordinate subspace nontrivially.
This module tabulates, for all 30 L-free and 30 R-free words, the dead-cell
column multiplicities -- the exact input the next lane needs.
"""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w21_c8core as G

out={"_header":"UNAUDITED W21 dead-cell column multiplicities on the C_8 member."}
def tab(words, side):
    rows=[]
    for z in words:
        prof={}
        for j in (G.R if side=='L' else G.L):
            cnt={}
            for i in (G.L if side=='L' else G.R):
                key=(i,j) if side=='L' else (j,i)
                dc=G.DEAD.get(key)
                if dc is None: continue
                a,b=dc
                if side=='L':
                    if z[G.LPOS[i]]==a: cnt[b]=cnt.get(b,0)+1
                else:
                    if z[G.RPOS[i]]==b: cnt[a]=cnt.get(a,0)+1
            prof[j]=dict(n_dead=sum(cnt.values()), max_col_mult=max(cnt.values(), default=0),
                         cols={str(k):v for k,v in sorted(cnt.items())})
        ndirty=sum(1 for j in prof if prof[j]["n_dead"]>0)
        ndouble=sum(1 for j in prof if prof[j]["max_col_mult"]>=2)
        rows.append(dict(word=list(z), n_dirty_sites=ndirty, n_double_sites=ndouble,
                         profile={str(k):v for k,v in prof.items()}))
    return rows
for side,words in (('L',G.LFREE),('R',G.RFREE)):
    rows=tab(words,side)
    out[side]=rows
    dd=[r for r in rows if r["n_double_sites"]>0]
    d4=[r for r in rows if r["n_dirty_sites"]==4]
    print("%s-free words: %d; with all four opposite sites dirty: %d %s"
          % (side,len(rows),len(d4),[r["word"] for r in d4]))
    print("   with a DOUBLE dead-cell column (two dead cells in one column of one M): %d"%len(dd))
    for r in dd: print("      %s -> double at sites %s"
                       % (r["word"],[k for k,v in r["profile"].items() if v["max_col_mult"]>=2]))
json.dump(out,open("results_deadcol.json","w"),indent=1,default=str)
