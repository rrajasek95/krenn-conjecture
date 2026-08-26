import sys, json
sys.dont_write_bytecode = True
import m2sys as S, m2stage as ST
y=(0,1,0,1)
e,cl,lb = S.sys_fixed_y(y)
res=[]
# stage A: std only, mod p, subsets of equations of growing size
for n in (8,12,16,20,30):
    r = ST.run("y0101_std%d_p"%n, e[:n], cl, char=32003, timeout=100, do_std=True)
    res.append(r)
    if r["status"]=="TIMEOUT": break
json.dump(res, open("results_stageA.json","w"), indent=1, default=str)
