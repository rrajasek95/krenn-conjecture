#!/usr/bin/env python3
"""W21-M2-SING: system builders + gauge-fixing + guarded Singular driver."""
from __future__ import annotations

import sys
import time
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
import m2core as M

ALLW = tuple(product(range(3), repeat=4))


# ------------------------------------------------------------------ builders
def sys_words(lwords=(), rwords=()):
    """equations of the L-free words `lwords` (all 81 y each) and of the
    R-free words `rwords` (all 81 x each).  Returns (eqs, cells, labels)."""
    eqs, labels = [], []
    seen = set()
    for x in lwords:
        assert tuple(x) in M.LFREE, ("not L-free", x)
        for y in ALLW:
            k = (tuple(x), tuple(y))
            if k in seen:
                continue
            seen.add(k)
            p = M.per_poly(tuple(x), tuple(y))
            if p:
                eqs.append(p)
                labels.append("L%s|%s" % (''.join(map(str, x)),
                                          ''.join(map(str, y))))
    for y in rwords:
        assert tuple(y) in M.RFREE, ("not R-free", y)
        for x in ALLW:
            k = (tuple(x), tuple(y))
            if k in seen:
                continue
            seen.add(k)
            p = M.per_poly(tuple(x), tuple(y))
            if p:
                eqs.append(p)
                labels.append("R%s|%s" % (''.join(map(str, x)),
                                          ''.join(map(str, y))))
    cells = set()
    for p in eqs:
        cells |= M.poly_vars(p)
    return eqs, sorted(cells), labels


def sys_fixed_y(y, lwords=None):
    """the FIXED-y slice: per B(x,y)=0 for every L-free x, one fixed y.
    Uses only the cells A_{i,j}[c][y_j] -- at most 48 of them."""
    lwords = M.LFREE if lwords is None else lwords
    eqs, labels = [], []
    for x in lwords:
        p = M.per_poly(tuple(x), tuple(y))
        if p:
            eqs.append(p)
            labels.append("Y%s|%s" % (''.join(map(str, x)),
                                      ''.join(map(str, y))))
    cells = set()
    for p in eqs:
        cells |= M.poly_vars(p)
    return eqs, sorted(cells), labels


def sys_fixed_x(x, rwords=None):
    """mirror: per B(x,y)=0 for every R-free y, one fixed L-word x."""
    rwords = M.RFREE if rwords is None else rwords
    eqs, labels = [], []
    for y in rwords:
        p = M.per_poly(tuple(x), tuple(y))
        if p:
            eqs.append(p)
            labels.append("X%s|%s" % (''.join(map(str, x)),
                                      ''.join(map(str, y))))
    cells = set()
    for p in eqs:
        cells |= M.poly_vars(p)
    return eqs, sorted(cells), labels


def merge(*systems):
    eqs, labels = [], []
    seen = set()
    for (e, c, lb) in systems:
        for p, l in zip(e, lb):
            key = tuple(sorted(p.items()))
            if key in seen:
                continue
            seen.add(key)
            eqs.append(p)
            labels.append(l)
    cells = set()
    for p in eqs:
        cells |= M.poly_vars(p)
    return eqs, sorted(cells), labels


# ------------------------------------------------------------------ gauge fix
def gauge_fix(cells):
    """spanning forest of the gauge graph on `cells`; those cells are set to 1.
    Returns (tree_cells, free_cells, nnodes, ncomp)."""
    tree, nnodes, ncomp = M.spanning_forest(cells)
    tree = [c for c in tree if c in set(cells)]
    free = [c for c in cells if c not in set(tree)]
    return tree, free, nnodes, ncomp


def substitute(eqs, fixed_to_one):
    """drop the fixed cells from every monomial (they equal 1)."""
    out = []
    for p in eqs:
        q = {}
        for mon, c in p.items():
            m2 = tuple(v for v in mon if v not in fixed_to_one)
            q[m2] = q.get(m2, 0) + c
        out.append({m: c for m, c in q.items() if c})
    return out


# ------------------------------------------------------------------ Singular
def build_script(eqs, free_cells, char=0, sat_vars=None, timeout_note="",
                 extra_head=(), do_dim=True, max_sat=None):
    names = {cell: "zzv%d" % k for k, cell in enumerate(free_cells)}
    varlist = [names[c] for c in free_cells]
    gens = ["zzg%d" % k for k in range(1, len(eqs) + 1)]
    M.check_no_shadowing(varlist, gens)                      # LEDGER 13
    lines = ['LIB "elim.lib";']                              # LEDGER 11
    lines.append("ring zzr = %d,(%s),dp;" % (char, ",".join(varlist)))
    lines.extend(extra_head)
    for k, p in enumerate(eqs, 1):
        lines.append("poly zzg%d = %s;" % (k, M.sing_poly(p, names)))
    lines.append("ideal zzI = %s;" % ",".join(gens))
    lines.append("ideal zzS = std(zzI);")
    lines.append('"MARK_STD";')
    lines.append("size(zzS);")
    lines.append('"MARK_UNIT0";')
    lines.append("reduce(1,zzS);")
    if do_dim:
        lines.append('"MARK_DIM";')
        lines.append("dim(zzS);")
    sv = list(free_cells) if sat_vars is None else list(sat_vars)
    if max_sat is not None:
        sv = sv[:max_sat]
    lines.append("list zzL;")
    lines.append("int zzstop = 0;")
    for k, cell in enumerate(sv, 1):
        lines.append("if (zzstop == 0) {")
        lines.append("  zzL = sat(zzS, %s);" % names[cell])
        lines.append("  zzS = std(zzL[1]);")
        lines.append('  "MARK_SAT %d %s";' % (k, names[cell]))
        lines.append("  reduce(1,zzS);")
        lines.append("  if (reduce(1,zzS)==0) { zzstop = 1; }")
        lines.append("}")
    lines.append('"MARK_FINAL";')
    lines.append("reduce(1,zzS);")
    lines.append('"MARK_FINALDIM";')
    lines.append("dim(std(zzS));")
    lines.append("quit;")
    script = "\n".join(lines) + "\n"
    M.scan_script(script, varlist, gens)                     # LEDGER 13 guard
    return script, names


def parse_out(out):
    """returns dict with unit0 (bool), dim0, sat steps, final unit."""
    toks = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    res = {"sat": []}
    i = 0
    while i < len(toks):
        t = toks[i]
        if t == "MARK_STD":
            res["ngens"] = int(toks[i + 1]); i += 2; continue
        if t == "MARK_UNIT0":
            res["unit0"] = (toks[i + 1] == "0"); i += 2; continue
        if t == "MARK_DIM":
            res["dim0"] = int(toks[i + 1]); i += 2; continue
        if t.startswith("MARK_SAT"):
            _, k, nm = t.split()
            res["sat"].append((int(k), nm, toks[i + 1] == "0")); i += 2
            continue
        if t == "MARK_FINAL":
            res["unit_final"] = (toks[i + 1] == "0"); i += 2; continue
        if t == "MARK_FINALDIM":
            res["dim_final"] = int(toks[i + 1]); i += 2; continue
        i += 1
    return res


def run_system(name, eqs, cells, char=0, timeout=1800, sat_vars=None,
               max_sat=None, verbose=True):
    tree, free, nnodes, ncomp = gauge_fix(cells)
    eqs2 = substitute(eqs, set(tree))
    eqs2 = [p for p in eqs2 if p]
    # a constant equation (nonzero constant, no monomials removed) would be an
    # instant kill -- record it
    consts = [p for p in eqs2 if list(p.keys()) == [()]]
    script, names = build_script(eqs2, free, char=char, sat_vars=sat_vars,
                                 max_sat=max_sat)
    open("script_%s.sing" % name, "w").write(script)
    t0 = time.time()
    try:
        out, st = M.run_singular(script, timeout=timeout)
    except M.SingularError as e:
        return {"name": name, "status": "SINGULAR_ERROR", "err": str(e)[:2000],
                "nvars": len(free), "neqs": len(eqs2)}
    el = time.time() - t0
    if st == "TIMEOUT":
        return {"name": name, "status": "TIMEOUT", "seconds": el,
                "nvars": len(free), "neqs": len(eqs2),
                "ncells": len(cells), "ngauge": len(tree)}
    r = parse_out(out)
    r.update({"name": name, "status": "OK", "seconds": el, "char": char,
              "nvars": len(free), "neqs": len(eqs2), "ncells": len(cells),
              "ngauge": len(tree), "nconst_eqs": len(consts)})
    open("log_%s.txt" % name, "w").write(out)
    if verbose:
        print("[%s] char=%d cells=%d gauge=%d vars=%d eqs=%d  %.1fs  "
              "unit0=%s dim0=%s sat_steps=%d unit_final=%s dim_final=%s"
              % (name, char, len(cells), len(tree), len(free), len(eqs2), el,
                 r.get("unit0"), r.get("dim0"), len(r["sat"]),
                 r.get("unit_final"), r.get("dim_final")))
    return r
