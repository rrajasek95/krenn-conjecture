#!/usr/bin/env python3
"""W29 D2 -- FULL core minimisation (the Laplace groups are minimised too) and
an independent DPLL re-decision of the small core.

d1 kept A0/A3 mandatory, which leaves ~12,000 clauses.  Here every group is
deletable, so the core that survives is the actual mathematical content of
the kill, and it is small enough for the hand-written DPLL to settle quickly.
"""
import json, sys, time
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
sys.path.insert(0, BASE)
import run_c2_unified as U
import run_d1_core as D
spec = sys.argv[1] if len(sys.argv) > 1 else ""
Rs = tuple(tuple(int(ch) for ch in p) if p else ()
           for p in (spec.split("|") + ["", "", ""])[:3])
OUT = f"{BASE}/results_d2_core2_{spec.replace('|','_') or 'singleton'}.json"
RES = {}
def ck(t=""):
    json.dump(RES, open(OUT, "w"), indent=1, default=str)
    if t: print(f"   [ck {t}]", flush=True)
t0 = time.time()
van = U.build_van(8, Rs)
RES["case"] = {"Rs": [list(r) for r in Rs], "nvars": van.nvars,
               "nclauses": len(van.cls)}
print(f"case {Rs}: {van.nvars} vars, {len(van.cls)} clauses", flush=True)
core, groups, base = D.extract_core(van, mandatory=())
kinds = {}
for k in core: kinds[k[0]] = kinds.get(k[0], 0) + 1
corecls = [cl for k in core for cl in groups[k]]
used = sorted({abs(l) for cl in corecls for l in cl})
RES["core"] = {"n_groups": len(core), "kinds": kinds,
               "n_clauses": len(corecls), "n_vars": len(used),
               "groups": [D.pretty(k) for k in core]}
print(f"[core] {len(core)} groups {kinds}; {len(corecls)} clauses over "
      f"{len(used)} variables ({round(time.time()-t0,1)}s)", flush=True)
ck("core")
t1 = time.time()
sat = D.dpll(corecls, van.nvars)
RES["own_dpll_core_sat"] = sat
RES["own_dpll_secs"] = round(time.time()-t1, 1)
print(f"[own DPLL] core satisfiable? {sat} (want False) "
      f"({RES['own_dpll_secs']}s)", flush=True)
RES["PASS"] = (sat is False)
RES["seconds"] = round(time.time()-t0, 1)
ck("final")
print(f"wrote {OUT}")
