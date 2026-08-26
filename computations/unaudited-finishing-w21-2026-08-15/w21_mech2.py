#!/usr/bin/env python3
"""W21 (RE-AIMED) -- WHY the residual linear system kills, and its controls.
UNAUDITED.  Exact only."""
import json, os, sys, random
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction
import w21_core as K
from w21_resid import setup, poly_of, load_blocks, residual_linear_test

out={"_header":"UNAUDITED W21 mechanism + controls for the residual linear kill."}
# ---- mechanism at an m=28 clean point ----
d=json.load(open(os.path.join(HERE,"results_more.json")))
bl=load_blocks(d["m28"][0]["point"]); T=K.W8_IMMUNE[28]
gam,cells,idx=setup(T)
shapes={}
mono=[]      # equations c*z_i = 0 with c != 0  -> z_i = 0 outright
for w in K.MIXED:
    p=poly_of(bl,gam,idx,w)
    if not p: continue
    dmax=max(len(k) for k in p)
    if dmax>1: continue
    nv=len([k for k in p if k!=()]); hasc=((),) [0] in p
    key=(nv, () in p)
    shapes[key]=shapes.get(key,0)+1
    if nv==1 and () not in p: mono.append((w,[k for k in p if k][0][0]))
print("degree-<=1 equation shapes (n_variables, has_constant_term) -> count:",
      sorted(shapes.items()))
print("PURE MONOMIAL equations (c*z_i = 0, so z_i = 0 immediately): %d, "
      "hitting cells %s" % (len(mono), sorted({cells[i] and str(cells[i]) for _,i in mono})))
out["shape_hist"]={str(k):v for k,v in sorted(shapes.items())}
out["n_pure_monomial_equations"]=len(mono)
out["cells_forced_zero_by_a_single_equation"]=sorted({str(cells[i]) for _,i in mono})
r=residual_linear_test(T,bl)
print("residual test at this point:", {k:r[k] for k in ("n_linear","rank","inconsistent","solution_dim","n_forced_zero")})
out["example_point_result"]={k:str(r.get(k)) for k in ("n_linear","rank","inconsistent","solution_dim","n_forced_zero")}
out["example_forced_cells"]=r.get("forced_zero_cells")

# ---- CONTROL A (explicit point, LEDGER 13b/18) for the FORCED-ZERO verdict:
# a linear system whose solution set has NO identically-zero coordinate must
# be reported with zero forced cells.
rng=random.Random(5150)
n=12
tgt=[Fraction(rng.randint(1,9)) for _ in range(n)]
rows=[]
for _ in range(300):
    rr=[Fraction(rng.randint(-5,5)) for _ in range(n)]
    rows.append(rr+[sum(rr[i]*tgt[i] for i in range(n))])
R,piv=K.rref(rows,n+1)
sol=[Fraction(0)]*n
for i,pc in enumerate(piv):
    if pc<n: sol[pc]=R[i][n]
ker=K.kernel_basis([r_[:n] for r_ in rows],n)
forced=[i for i in range(n) if sol[i]==0 and all(b[i]==0 for b in ker)]
print("CONTROL A (all-nonzero-solution system): forced-zero cells reported = %d (want 0); "
      "solution matches target: %s" % (len(forced), sol==tgt))
out["control_A_false_forced_zero"]=len(forced)
out["control_A_solution_correct"]=(sol==tgt)

# ---- CONTROL B (mutation): plant a coordinate that IS identically zero.
rows2=[]
for _ in range(300):
    rr=[Fraction(rng.randint(-5,5)) for _ in range(n)]
    rr[3]=Fraction(0)
    rows2.append(rr+[sum(rr[i]*tgt[i] for i in range(n))])
rows2.append([Fraction(1 if i==3 else 0) for i in range(n)]+[Fraction(0)])
R2,piv2=K.rref(rows2,n+1)
sol2=[Fraction(0)]*n
for i,pc in enumerate(piv2):
    if pc<n: sol2[pc]=R2[i][n]
ker2=K.kernel_basis([r_[:n] for r_ in rows2],n)
forced2=[i for i in range(n) if sol2[i]==0 and all(b[i]==0 for b in ker2)]
print("CONTROL B (planted identically-zero coordinate 3): forced-zero cells reported = %s "
      "(want [3])" % forced2)
out["control_B_forced"]=forced2
json.dump(out,open(os.path.join(HERE,"results_mech2.json"),"w"),indent=1,default=str)
