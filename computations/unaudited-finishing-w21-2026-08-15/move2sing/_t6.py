import sys, time
sys.dont_write_bytecode = True
import m2core as M, m2thm as T
cfg = ((2,(0,1)),)*4
eqs, varids, rowideals = T.build(cfg)
names = {v:"zzv%d"%k for k,v in enumerate(varids)}
vl=[names[v] for v in varids]
print("nvars",len(varids),"neqs",len(eqs),"free rows",len(rowideals), flush=True)
# branch: choose generator #ch[k] from each free row, add Rabinowitsch u_k*v-1
import itertools
def branch(ch, char=32003, tmo=45):
    uvars=["zzu%d"%k for k in range(len(rowideals))]
    s='LIB "elim.lib";\nring zzr = %d,(%s),dp;\n'%(char,",".join(vl+uvars))
    gens=[]
    for k,p in enumerate(eqs,1):
        s+="poly zzg%d = %s;\n"%(k, M.sing_poly(p,names)); gens.append("zzg%d"%k)
    for k,ri in enumerate(rowideals):
        s+="poly zzh%d = zzu%d*%s-1;\n"%(k,k,names[ri[ch[k]]]); gens.append("zzh%d"%k)
    s+="ideal zzI = %s;\nideal zzS = std(zzI);\n"%",".join(gens)
    s+='"MARK_UNIT"; reduce(1,zzS);\nquit;\n'
    M.scan_script(s, vl+uvars, gens)
    t0=time.time()
    out,st=M.run_singular(s,timeout=tmo)
    if st=="TIMEOUT": return None, time.time()-t0
    return out.split("MARK_UNIT")[1].strip()=="0", time.time()-t0
for ch in [(0,)*8, (0,1,0,1,0,1,0,1), (1,)*8]:
    print(ch, branch(ch), flush=True)
