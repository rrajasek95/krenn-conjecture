#!/usr/bin/env python3
"""W21-M2-SING: staged / instrumented Singular runs so the BLOCKER is located
precisely (which stage, which ordering, which resource limit)."""
from __future__ import annotations

import sys
import time

sys.dont_write_bytecode = True
import m2core as M
import m2sys as S


def staged_script(eqs, free_cells, char=0, engine="std", sat_vars=None,
                  do_std=True, order="dp", rabino=None):
    names = {cell: "zzv%d" % k for k, cell in enumerate(free_cells)}
    varlist = [names[c] for c in free_cells]
    gens = ["zzg%d" % k for k in range(1, len(eqs) + 1)]
    M.check_no_shadowing(varlist, gens)
    vl = list(varlist)
    if rabino:
        vl = vl + ["zzu"]
    lines = ['LIB "elim.lib";', "option(noredefine);",
             "ring zzr = %d,(%s),%s;" % (char, ",".join(vl), order)]
    for k, p in enumerate(eqs, 1):
        lines.append("poly zzg%d = %s;" % (k, M.sing_poly(p, names)))
    gl = list(gens)
    if rabino:
        prod = "*".join(names[c] for c in rabino)
        lines.append("poly zzrab = zzu*(%s)-1;" % prod)
        gl.append("zzrab")
    lines.append("ideal zzI = %s;" % ",".join(gl))
    lines.append('"MARK_T0"; system("--ticks-per-sec",1000); rtimer;')
    if do_std:
        lines.append("ideal zzS = %s(zzI);" % engine)
        lines.append('"MARK_STD"; rtimer;')
        lines.append('"MARK_SIZE"; size(zzS);')
        lines.append('"MARK_UNIT0"; reduce(1,zzS);')
        lines.append('"MARK_DIM"; dim(zzS);')
        lines.append('"MARK_DEG"; size(zzS);')
    else:
        lines.append("ideal zzS = zzI;")
    if sat_vars:
        lines.append("list zzL;")
        lines.append("int zzstop = 0;")
        for k, cell in enumerate(sat_vars, 1):
            lines.append("if (zzstop == 0) {")
            lines.append("  zzL = sat(zzS, %s);" % names[cell])
            lines.append("  zzS = std(zzL[1]);")
            lines.append('  "MARK_SAT %d %s"; rtimer; reduce(1,zzS);' %
                         (k, names[cell]))
            lines.append("  if (reduce(1,zzS)==0) { zzstop = 1; }")
            lines.append("}")
        lines.append('"MARK_FINAL"; reduce(1,zzS);')
    lines.append("quit;")
    script = "\n".join(lines) + "\n"
    M.scan_script(script, vl, gens + (["zzrab"] if rabino else []))
    return script, names


def run(name, eqs, cells, char=0, timeout=600, engine="std", order="dp",
        sat_vars=None, do_std=True, rabino=None, gauge=True, verbose=True):
    if gauge:
        tree, free, nn, nc = S.gauge_fix(cells)
        eqs2 = [p for p in S.substitute(eqs, set(tree)) if p]
    else:
        tree, free = [], list(cells)
        eqs2 = list(eqs)
    sv = [c for c in (sat_vars or []) if c in free]
    rb = [c for c in (rabino or []) if c in free]
    script, names = staged_script(eqs2, free, char=char, engine=engine,
                                  order=order, sat_vars=sv, do_std=do_std,
                                  rabino=rb)
    open("script_%s.sing" % name, "w").write(script)
    t0 = time.time()
    try:
        out, st = M.run_singular(script, timeout=timeout)
    except M.SingularError as e:
        print("[%s] SINGULAR ERROR: %s" % (name, str(e)[:300]))
        return {"name": name, "status": "SINGULAR_ERROR", "err": str(e)[:1500]}
    el = time.time() - t0
    r = {"name": name, "char": char, "engine": engine, "order": order,
         "nvars": len(free) + (1 if rb else 0), "neqs": len(eqs2),
         "ngauge": len(tree), "seconds": round(el, 1)}
    if st == "TIMEOUT":
        r["status"] = "TIMEOUT"
        if verbose:
            print("[%s] TIMEOUT after %.0fs  (char=%d %s %s, vars=%d eqs=%d)"
                  % (name, el, char, engine, order, r["nvars"], len(eqs2)))
        return r
    open("log_%s.txt" % name, "w").write(out)
    r["status"] = "OK"
    toks = [t.strip() for t in out.splitlines() if t.strip()]
    i = 0
    while i < len(toks):
        t = toks[i]
        if t == "MARK_STD":
            r["std_ms"] = int(toks[i + 1]); i += 2; continue
        if t == "MARK_SIZE":
            r["gb_size"] = int(toks[i + 1]); i += 2; continue
        if t == "MARK_UNIT0":
            r["unit_before_sat"] = (toks[i + 1] == "0"); i += 2; continue
        if t == "MARK_DIM":
            r["dim"] = int(toks[i + 1]); i += 2; continue
        if t.startswith("MARK_SAT"):
            _, k, nm = t.split()
            r.setdefault("sat", []).append(
                (int(k), nm, int(toks[i + 1]), toks[i + 2] == "0"))
            i += 3; continue
        if t == "MARK_FINAL":
            r["unit_final"] = (toks[i + 1] == "0"); i += 2; continue
        i += 1
    if verbose:
        print("[%s] %.0fs char=%d %s/%s vars=%d eqs=%d | GB size=%s dim=%s "
              "unit_pre=%s sat_steps=%s unit_final=%s"
              % (name, el, char, engine, order, r["nvars"], len(eqs2),
                 r.get("gb_size"), r.get("dim"), r.get("unit_before_sat"),
                 len(r.get("sat", [])), r.get("unit_final")))
    return r
