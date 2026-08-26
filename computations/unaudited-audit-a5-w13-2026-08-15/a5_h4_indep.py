import random, sys, json
sys.path.insert(0,"/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
rng=random.Random(77)
inter=None
for t in range(4):
    M=[[rng.randint(-6,6) for _ in range(3)] for _ in range(3)]
    sv=[M[i][j] for i in range(3) for j in range(3)]
    P=A.perp_basis(A.L_rows(4,sv,rng), len(A.deg_monoms(4)))
    print("A",M,"dim perp",len(P),flush=True)
    if inter is None: inter=P
    else:
        u=A.perp_basis(inter,len(A.deg_monoms(4)))
        w=A.perp_basis(P,len(A.deg_monoms(4)))
        inter=A.perp_basis(u+w,len(A.deg_monoms(4)))
    print("  running intersection dim",len(inter),flush=True)
json.dump({"h4_A_independent_dim":len(inter)},open("results_h4_indep.json","w"))
