#!/usr/bin/env python3
"""Consolidate every W21-M2-SING result file into one ledger."""
import json, glob, os, sys
sys.dont_write_bytecode = True
out = {"_header": "UNAUDITED W21-M2-SING consolidated ledger"}
for f in sorted(glob.glob("results_*.json")):
    try: out[os.path.basename(f)[8:-5]] = json.load(open(f))
    except Exception as e: out[f] = "unreadable: %s" % e
json.dump(out, open("LEDGER.json","w"), indent=1, default=str)
def g(k, *path, default=None):
    v = out.get(k, {})
    for p in path:
        if isinstance(v, dict): v = v.get(p, {})
        else: return default
    return v if v != {} else default
print("=== CONTROLS ===")
print("C1 equation generator vs independent H engine : %s mismatches / %s"
      %(g("verify","C1_mismatch"), g("verify","C1_checks")))
print("chain(2,3) H == per(cols of M_j)              : %s mismatches / %s"
      %(g("kill","chain23_mismatch"), g("kill","chain23_checks")))
print("gauge forest cells/nodes/comps               : %s / %s / %s"
      %(g("verify","C5_tree_cells"), g("verify","C5_nodes"), g("verify","C5_components")))
print("gauge covariance violations                  : %s / %s"
      %(g("verify","C4_covariance_violations"), g("verify","C4_covariance_checks")))
sm = out.get("smoke", {})
nsm = sum(1 for k,v in sm.items() if isinstance(v,dict) and "ok" in v)
oksm = sum(1 for k,v in sm.items() if isinstance(v,dict) and v.get("ok"))
print("Singular harness smoke tests                 : %d/%d pass"%(oksm,nsm))
print("explicit point, system (a) violated eqs      : %s / %s"
      %(g("points","P1_system_a","violated"), g("points","P1_system_a","neqs")))
print("explicit point, zero cells among the 60      : %s"%g("points","P1_system_a","zero_cells"))
print("=== THEOREM W21-M2 ===")
sw = out.get("thm_sweep3_c0", [])
print("chart orbits with a dim-3 site (over Q)      : %d, unit=%d, non-unit=%d"
      %(len(sw), sum(1 for r in sw if r.get("unit")), sum(1 for r in sw if r.get("unit") is False)))
bd = out.get("stepBD_c0", [])
print("(2,2,2,2) branch I chart pairs (over Q)      : %d, unit=%d"%(len(bd), sum(1 for r in bd if r.get("unit"))))
ii = out.get("stepII_c0", [])
print("(2,2,2,2) branch II charts (over Q)          : %d, unit=%d"%(len(ii), sum(1 for r in ii if r.get("unit"))))
st = out.get("steps_c0", {})
print("FACT A sites / failures                      : %s / %s"%(st.get("factA_sites"), st.get("factA_failures")))
print("STEP B / STEP D / STEP E                     : %s / %s of 36 / %s of 6"
      %(st.get("stepB"), st.get("stepD_unit"), st.get("stepE_unit")))
for p in (5,7):
    ff = out.get("ff%d"%p)
    if ff: print("exhaustive F_%d counterexamples             : %s (pairs %s)"%(p, ff.get("counterexamples"), ff.get("pairs")))
print("=== FALSE-KILL CONTROLS (must all be 0) ===")
fk = out.get("thm_falsekill", [])
nf = sum(1 for r in fk if r.get("unit") is True)
nn = sum(1 for r in fk if r.get("unit") is False)
print("known-feasible dim types run through pipeline: %d tested, %d reported non-unit, %d FALSE KILLS"%(len(fk), nn, nf))
print("FACT A mutation (no dead cell) unit          : %s (want False)"%st.get("factA_mutation_unit"))
print("STEP B mutation unit                         : %s (want False)"%st.get("stepB_mutation"))
mu = out.get("mutations", {})
print("branch II no-saturation mutation unit        : %s (want False)"%mu.get("mut_branchII_nosat_unit"))
print("=== KILL ===")
kl = out.get("kill", {})
print("all-dirty L-free words : %s"%kl.get("kill_words_L"))
print("all-dirty R-free words : %s"%kl.get("kill_words_R"))
print("FACT A L-side %s/%s  R-side %s/%s"%(kl.get("factA_L_ok"),kl.get("factA_L_n"),kl.get("factA_R_ok"),kl.get("factA_R_n")))
