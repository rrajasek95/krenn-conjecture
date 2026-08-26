import sys, time
sys.dont_write_bytecode = True
import m2core as M, m2thm as T
cfg = ((2,(0,1)),)*4
eqs, varids, rowideals = T.build(cfg)
names = {v:"zzv%d"%k for k,v in enumerate(varids)}
vl=[names[v] for v in varids]
print("nvars",len(varids),"neqs",len(eqs),"rowideals",len(rowideals), flush=True)
def go(tag, body, char=32003, tmo=60):
    s = 'LIB "elim.lib";\nring zzr = %d,(%s),dp;\n'%(char,",".join(vl))
    for k,p in enumerate(eqs,1): s += "poly zzg%d = %s;\n"%(k, M.sing_poly(p,names))
    s += "ideal zzI = %s;\n"%",".join("zzg%d"%k for k in range(1,len(eqs)+1))
    s += body + "quit;\n"
    M.scan_script(s, vl, ["zzg%d"%k for k in range(1,len(eqs)+1)])
    t0=time.time()
    try:
        out,st = M.run_singular(s, timeout=tmo)
    except M.SingularError as e:
        print(tag,"ERR",str(e)[:200], flush=True); return
    print(tag, st, "%.1fs"%(time.time()-t0), (out or "")[:300].replace("\n"," | "), flush=True)
go("stdonly", 'ideal zzS = std(zzI);\n"SZ";size(zzS);"DIM";dim(zzS);\n')
go("sat1", 'ideal zzS = std(zzI);\nlist zzL = sat(zzS, ideal(%s));\nzzS=std(zzL[1]);\n"U";reduce(1,zzS);"DIM";dim(zzS);\n'%",".join(names[v] for v in rowideals[0]))
