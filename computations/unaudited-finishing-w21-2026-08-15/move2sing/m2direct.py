#!/usr/bin/env python3
"""Direct attempts (blocker documentation / bonus confirmation):
 A) the FULL 81-equation system of the all-dirty L-free word (1,0,0,2)
 B) one (2,2,2,2) chart config of the W21-M2 theorem"""
import sys, json, time
sys.dont_write_bytecode = True
import m2sys as S, m2stage as ST, m2thm as T
res={}
x=(1,0,0,2)
e,cl,lb = S.sys_words(lwords=[x])
print("A) single all-dirty word x=%s : %d equations, %d cells"%(x,len(e),len(cl)), flush=True)
for char in (32003,0):
    r = ST.run("x1002_c%d"%char, e, cl, char=char, timeout=1500,
               sat_vars=None, do_std=True)
    res["A_c%d"%char]=r; json.dump(res, open("results_direct.json","w"), indent=1, default=str)
cfg=((2,(0,1)),)*4
print("B) (2,2,2,2) all-same-chart config, char 0, 1500s", flush=True)
r=T.run_cfg(cfg, char=0, timeout=1500); res["B"]=r; print(r, flush=True)
json.dump(res, open("results_direct.json","w"), indent=1, default=str)
