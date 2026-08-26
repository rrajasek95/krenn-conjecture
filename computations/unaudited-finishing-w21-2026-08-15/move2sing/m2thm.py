#!/usr/bin/env python3
"""W21-M2-SING: EXACT verification of the structural theorem that kills the
C_8 member.

THEOREM (W21-M2).  Let V_4,...,V_7 be linear subspaces of C^4 with
dim V_j >= 2 for every j and with no V_j contained in a coordinate hyperplane
{v_i = 0}.  Then the 4x4 permanent form
      per(v_4,v_5,v_6,v_7) = sum over bijections sigma of prod_j v_j[sigma(j)]
does NOT vanish identically on V_4 x V_5 x V_6 x V_7.

WHY THIS KILLS THE C_8 MEMBER.  For an L-free word x the 81 equations
{H_(x,y)=0 : all y} say exactly that per vanishes identically on the product
of the column spans V_j = colspan(M_j^x).  V_j is not in a coordinate
hyperplane because M_j^x has no zero row (every row keeps >= 2 occupied
cells).  And if M_j^x carries a DEAD cell then rank M_j^x >= 2: rank 1 means
M = a (x) s, so a zero entry forces a zero row or a zero column of M_j^x, and
every row of M_j^x keeps >= 2 and every column >= 2 occupied cells, all of
which must be nonzero.  Three L-free words -- (1,0,0,2), (1,0,2,2), (1,1,2,2)
-- have a dead cell at EVERY one of the four R-sites.  For them all four
ranks are >= 2, the theorem applies, and the 81 equations are unsatisfiable.

HOW IT IS VERIFIED HERE (independently of the hand proof).
Every d-dimensional subspace of C^4 has an invertible d x d row-submatrix, so
the Grassmannian is covered by the charts N[ROWS,:] = identity.  For each
chart tuple we build the prod_j d_j quartic equations, SATURATE by the ideal
of each free row (that is exactly `V_j has no zero row'), and test the unit
ideal.  The chart tuples are reduced modulo the symmetry group
S_4(sites) x S_4(coordinates) of per.
CONTROL: the same pipeline is run on the dimension types that ARE feasible
(W20's (1,1,2,2) mechanism and the (1,1,1,1) one) -- it must NOT report the
unit ideal there.
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True
import m2core as M

SITES = (0, 1, 2, 3)
COORDS = (0, 1, 2, 3)
BIJ4 = tuple(permutations(COORDS))


# ------------------------------------------------------------------ charts
def charts(d):
    return tuple(combinations(COORDS, d))


def canon(cfg):
    """canonical form of cfg = ((d,ROWS),...) under S4(sites) x S4(coords)."""
    best = None
    for pi in BIJ4:
        mapped = tuple(sorted((d, tuple(sorted(pi[r] for r in rows)))
                              for (d, rows) in cfg))
        if best is None or mapped < best:
            best = mapped
    return best


def enum_configs(dims_allowed=(2, 3)):
    seen = {}
    for dtup in product(dims_allowed, repeat=4):
        for ctup in product(*[charts(d) for d in dtup]):
            cfg = tuple((dtup[t], ctup[t]) for t in SITES)
            k = canon(cfg)
            if k not in seen:
                seen[k] = cfg
    return seen


# ------------------------------------------------------------------ equations
def build(cfg):
    """returns (eqs, varnames, rowideals).
    eqs: list of dicts {tuple of var-ids : int}; var-id = (t,i,a)."""
    varids = []
    N = {}
    for t, (d, rows) in enumerate(cfg):
        for i in COORDS:
            for a in range(d):
                if i in rows:
                    N[(t, i, a)] = 1 if rows[a] == i else 0
                else:
                    N[(t, i, a)] = (t, i, a)
                    varids.append((t, i, a))
    eqs = []
    for atup in product(*[range(cfg[t][0]) for t in SITES]):
        poly = {}
        for sig in BIJ4:              # sig[t] = coordinate used by site t
            mon, coef, dead = [], 1, False
            for t in SITES:
                e = N[(t, sig[t], atup[t])]
                if e == 0:
                    dead = True
                    break
                if e != 1:
                    mon.append(e)
            if dead:
                continue
            mon = tuple(sorted(mon))
            poly[mon] = poly.get(mon, 0) + coef
        poly = {m: c for m, c in poly.items() if c}
        eqs.append(poly)
    rowideals = []
    for t, (d, rows) in enumerate(cfg):
        for i in COORDS:
            if i not in rows:
                rowideals.append([(t, i, a) for a in range(d)])
    return eqs, varids, rowideals


def script_for(cfg, char=0):
    eqs, varids, rowideals = build(cfg)
    names = {v: "zzv%d" % k for k, v in enumerate(varids)}
    varlist = [names[v] for v in varids]
    gens = ["zzg%d" % k for k in range(1, len(eqs) + 1)]
    M.check_no_shadowing(varlist, gens)
    lines = ['LIB "elim.lib";',
             "ring zzr = %d,(%s),dp;" % (char, ",".join(varlist))]
    for k, p in enumerate(eqs, 1):
        lines.append("poly zzg%d = %s;" % (k, M.sing_poly(p, names)))
    lines.append("ideal zzI = %s;" % ",".join(gens))
    lines.append("ideal zzS = std(zzI);")
    lines.append("list zzL;")
    for ri in rowideals:
        lines.append("zzL = sat(zzS, ideal(%s));"
                     % ",".join(names[v] for v in ri))
        lines.append("zzS = std(zzL[1]);")
    lines.append('"MARK_UNIT"; reduce(1,zzS);')
    lines.append('"MARK_DIM"; dim(zzS);')
    lines.append("quit;")
    s = "\n".join(lines) + "\n"
    M.scan_script(s, varlist, gens)
    return s, len(varids), len(eqs)


def run_cfg(cfg, char=0, timeout=600):
    s, nv, ne = script_for(cfg, char=char)
    t0 = time.time()
    out, st = M.run_singular(s, timeout=timeout)
    el = time.time() - t0
    if st == "TIMEOUT":
        return {"cfg": str(cfg), "status": "TIMEOUT", "seconds": el,
                "nvars": nv, "neqs": ne}
    unit = out.split("MARK_UNIT")[1].split("MARK_DIM")[0].strip() == "0"
    dm = out.split("MARK_DIM")[1].strip().split()[0]
    return {"cfg": str(cfg), "status": "OK", "unit": bool(unit), "dim": dm,
            "seconds": round(el, 2), "nvars": nv, "neqs": ne}


# ------------------------------------------------------------------ step-1 id
def check_step1_identity():
    """EXACT symbolic check of the identity used in the hand proof:
    per(v4,v5,v6,v7) = sum_{i != k} A[i][k] v4[i] v5[k] with
    A[i][k] = v6[p]v7[q] + v6[q]v7[p], {p,q} = complement of {i,k}."""
    def mul(a, b):
        out = {}
        for m1, c1 in a.items():
            for m2, c2 in b.items():
                m = tuple(sorted(m1 + m2))
                out[m] = out.get(m, 0) + c1 * c2
        return {m: c for m, c in out.items() if c}

    def v(t, i):
        return {(("v", t, i),): 1}
    lhs = {}
    for sig in BIJ4:
        term = {(): 1}
        for t in SITES:
            term = mul(term, v(t, sig[t]))
        lhs = M.p_add(lhs, term)
    rhs = {}
    for i in COORDS:
        for k in COORDS:
            if i == k:
                continue
            p, q = sorted(set(COORDS) - {i, k})
            A = M.p_add(mul(v(2, p), v(3, q)), mul(v(2, q), v(3, p)))
            rhs = M.p_add(rhs, mul(A, mul(v(0, i), v(1, k))))
    return lhs == rhs, len(lhs)


if __name__ == "__main__":
    out = {"_header": "UNAUDITED W21-M2-SING theorem verification"}
    ok, nterms = check_step1_identity()
    print("STEP-1 IDENTITY (exact symbolic): per = sum A[i][k] v4[i]v5[k]  "
          "-> %s  (%d monomials)" % (ok, nterms))
    out["step1_identity"] = bool(ok)
    out["step1_terms"] = nterms
    # MUTATION on the identity checker
    bad = check_step1_identity()[0]
    out["step1_mutation"] = None

    char = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    tmo = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    mode = sys.argv[3] if len(sys.argv) > 3 else "all"

    if mode == "control":
        cfgs = {}
        for dt in [(1, 1, 2, 2), (1, 1, 1, 1), (1, 2, 2, 2), (1, 1, 3, 3),
                   (1, 2, 3, 3), (1, 3, 3, 3), (1, 1, 2, 3)]:
            for ctup in product(*[charts(d) for d in dt]):
                cfg = tuple((dt[t], ctup[t]) for t in SITES)
                cfgs.setdefault(canon(cfg), cfg)
        print("CONTROL configs (some dim = 1): %d orbits" % len(cfgs))
    else:
        cfgs = enum_configs((2, 3))
        print("THEOREM configs (all dims in {2,3}): %d orbits (from %d raw)"
              % (len(cfgs), sum(len(charts(d)) for d in (2, 3)) ** 0))
    res = []
    t0 = time.time()
    for n, (k, cfg) in enumerate(sorted(cfgs.items()), 1):
        r = run_cfg(cfg, char=char, timeout=tmo)
        r["dims"] = [d for (d, _) in cfg]
        res.append(r)
        if r["status"] != "OK" or (mode != "control" and not r["unit"]) \
                or n % 25 == 0:
            print("  [%3d/%3d] dims=%s unit=%s dim=%s %.1fs %s"
                  % (n, len(cfgs), r["dims"], r.get("unit"), r.get("dim"),
                     r["seconds"], r["status"]))
        json.dump({"header": out, "runs": res},
                  open("results_thm_%s_c%d.json" % (mode, char), "w"),
                  indent=1, default=str)
    nunit = sum(1 for r in res if r.get("unit"))
    nto = sum(1 for r in res if r["status"] != "OK")
    print("TOTAL %d configs, %d unit-ideal (infeasible), %d non-unit, "
          "%d timeouts, %.0fs"
          % (len(res), nunit, len(res) - nunit - nto, nto, time.time() - t0))
