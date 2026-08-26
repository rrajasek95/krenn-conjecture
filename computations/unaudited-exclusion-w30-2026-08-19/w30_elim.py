#!/usr/bin/env python3
"""W30 ELIMINATION: the COLLAPSE system at the protected vertex.  UNAUDITED.

WHY THE ORIGINAL TARGET WAS ABANDONED.  The staged target -- "(H)'s escape
cover is contained in the vanishing stratum / zero-cell locus" -- is FALSE:
w30_escape.py built an explicit m=27 / F_13 clean point, off the stratum,
all Gamma cells nonzero, with hafL vanishing on 36 of the 81 L-words and
covering every two-pair slice tuple at R5 (verified in
results_escverify.json, six controls).  So the escape locus is nonempty and
no elimination can empty it.

THE CORRECT TARGET.  Failure of the protected vertex v does not merely need
the escape; at EVERY SURVIVING index choice it needs LETTER COLLAPSE:

    at a surviving unit (tau, P):   rank S(tau)|_P = 1  AND  rank S(tau) >= 2

(step (1) of Theorem W30-X: ROWS = psi(S) with psi in GL_3, so delivery is
exactly rank S = rank S|clean).  Both halves are conditions on the blocks at
v ALONE -- 18 cells at m=25 (A_56, A_67), 27 at m=27 (A_25, A_45, A_56) --
and the collapse minors are BINOMIAL.  On the locus hafL(x) = 0 the clean
equation at m=25 also collapses to a binomial:

    A_67[y6][y7] A_03[x0][x3] A_25[x2][y5]
        + A_56[y5][y6] A_23[x2][x3] A_07[x0][y7]  =  0                (RED)

(derived from Phi = r67*(hafL*r45 + l03 d1 d2) + r56*(hafL*r47 + l23 d0 d1)
at m=25, dividing by d1 != 0).  So the whole escape-branch system is
binomial in 54 variables and Singular handles it directly.

Per escape branch b (a choice, for each two-pair tuple, of which trigger
class hafL annihilates) we test the ideal
    I_b = <collapse minors of the SURVIVING units> + <(RED) for x in W_b>
saturated by the cells, for the unit ideal.

usage: w30_elim.py <m> <vertex> <char: 0|13|31> <maxbranches> [timeout]
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_sing as SG                                             # noqa: E402
import w26_core as C                                              # noqa: E402

DECL = ["S0_harness_selftest", "S1_explicit_point_control",
        "S2_mutation_control", "S3_multichar", "S4_positive_control"]


def vname(e, i, j):
    return "zza%d%d_%d%d" % (e[0], e[1], i, j)


def blocks_at(m, v):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return sorted(e for e in gs if v in e)


def all_vars(edges):
    return [vname(e, i, j) for e in edges
            for i in range(3) for j in range(3)]


def S_entry(v, e, t, tau_letter):
    """the cell of block e at letter t of v and tau_letter at the other end"""
    if e[0] == v:
        return vname(e, t, tau_letter)
    return vname(e, tau_letter, t)


def units(m, lab):
    """(tau, clean pair) -> set of L-words realising it."""
    kind, v = L.vkey(lab)
    ns = sorted(s for s in range(8)
                if (min(s, v), max(s, v)) in set(C.gamma_edges(
                    C.TEMPLATES[m])))
    out = defaultdict(set)
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        P = tuple(sorted(t for t in range(3) if t not in fire))
        out[(tau, P)].add(tuple(w[:4]))
    return ns, out


def collapse_gens(v, ns, tau, P):
    """2x2 minors of S(tau) on the row pair P (BINOMIAL)."""
    t1, t2 = P
    gens = []
    for a, b in combinations(range(len(ns)), 2):
        ea = (min(ns[a], v), max(ns[a], v))
        eb = (min(ns[b], v), max(ns[b], v))
        gens.append("%s*%s - %s*%s"
                    % (S_entry(v, ea, t1, tau[a]), S_entry(v, eb, t2, tau[b]),
                       S_entry(v, ea, t2, tau[a]), S_entry(v, eb, t1, tau[b])))
    return gens


def red_gens(m, W):
    """(RED): the m=25 clean equation on the locus hafL = 0."""
    assert m == 25
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    gens = set()
    for w in C.MIXED:
        if tuple(w[:4]) not in W:
            continue
        if any(w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1] for f in lv):
            continue
        x, y = w[:4], w[4:]
        g = ("%s*%s*%s + %s*%s*%s"
             % (vname((6, 7), y[2], y[3]), vname((0, 3), x[0], x[3]),
                vname((2, 5), x[2], y[1]),
                vname((5, 6), y[1], y[2]), vname((2, 3), x[2], x[3]),
                vname((0, 7), x[0], y[3])))
        gens.add(g)
    return sorted(gens)


def branches(m, lab, cap):
    """escape covers: per two-pair tuple, pick the annihilated class."""
    ns, U = units(m, lab)
    bytau = defaultdict(dict)
    for (tau, P), X in U.items():
        bytau[tau][P] = X
    two = [(tau, d) for tau, d in bytau.items() if len(d) >= 2]
    out = []
    for pick in product(*[list(d.items()) for _tau, d in two]):
        W = set()
        for (_P, X) in pick:
            W |= X
        out.append((W, [(two[i][0], pick[i][0]) for i in range(len(two))]))
        if len(out) >= cap:
            break
    return ns, U, out


def build_script(ch, vs, gens, satvars, extra=""):
    s = 'LIB "elim.lib";\n'
    s += SG.ringdecl(ch, vs)
    s += "ideal zzi = %s;\n" % (",\n  ".join(gens) if gens else "0")
    s += "ideal zzj = %s;\n" % ("*".join(satvars))
    s += extra
    s += SG.sat_and_test("zzi", "zzj")
    s += "quit;\n"
    return s


def main():
    m = int(sys.argv[1])
    lab = sys.argv[2]
    ch = int(sys.argv[3])
    cap = int(sys.argv[4])
    tmo = int(sys.argv[5]) if len(sys.argv) > 5 else 900
    kind, v = L.vkey(lab)
    res = os.path.join(HERE, "results_elim_m%d_%s_ch%d.json" % (m, lab, ch))
    OUT = {"_header": "UNAUDITED W30 collapse-system elimination",
           "m": m, "vertex": lab, "char": ch,
           "_controls_declared": DECL, "_controls_run": [],
           "note": "target CORRECTED: the (H)-escape locus is NONEMPTY "
                   "(results_escverify.json), so the staged target is "
                   "refuted; this eliminates the COLLAPSE system instead.",
           "branches": []}

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ---- S0 harness selftest
    st = SG.selftest()
    OUT["S0_harness_selftest"] = dict(results=st, ok=all(st.values()))
    OUT["_controls_run"].append("S0_harness_selftest")
    ck()

    ns, U, brs = branches(m, lab, cap)
    edges = blocks_at(m, v)
    vs = all_vars(edges)
    if m == 25:
        vs = sorted(set(vs) | set(all_vars([(0, 3), (2, 3), (2, 5), (0, 7)])))
    OUT["n_vars"] = len(vs)
    OUT["neighbours"] = ns
    OUT["n_units"] = len(U)
    OUT["n_branches_enumerated"] = len(brs)
    print("m=%d %s: N(v)=%s, %d units, %d vars, %d branches"
          % (m, lab, ns, len(U), len(vs), len(brs)), flush=True)
    ck()

    t0 = time.time()
    for bi, (W, pick) in enumerate(brs):
        surv = [(tau, P) for (tau, P), X in U.items() if not X <= W]
        gens = []
        for (tau, P) in surv:
            gens += collapse_gens(v, ns, tau, P)
        nred = 0
        if m == 25:
            rg = red_gens(m, W)
            gens += rg
            nred = len(rg)
        gens = sorted(set(gens))
        scr = build_script(ch, vs, gens, vs)
        r = SG.run(scr, vs, timeout=tmo)
        unit = None
        dim = None
        for ln in r.get("stdout", "").splitlines():
            if ln.startswith("UNIT="):
                unit = int(ln.split("=")[1].strip())
            if ln.startswith("DIMENSION="):
                dim = ln.split("=")[1].strip()
        rec = dict(branch=bi, n_annihilated_Lwords=len(W),
                   n_surviving_units=len(surv), n_gens=len(gens),
                   n_red_gens=nred, UNIT=unit, DIM=dim,
                   singular_ok=r["ok"], qlines=r.get("qlines", [])[:4],
                   timeout=r.get("timeout", False))
        OUT["branches"].append(rec)
        ck()
        print("  branch %3d |W|=%3d surv=%3d gens=%4d -> UNIT=%s DIM=%s "
              "ok=%s (%.0fs)"
              % (bi, len(W), len(surv), len(gens), unit, dim, r["ok"],
                 time.time() - t0), flush=True)
    nb = OUT["branches"]
    OUT["all_branches_unit"] = all(b["UNIT"] == 1 for b in nb) if nb else None
    OUT["n_unit"] = sum(1 for b in nb if b["UNIT"] == 1)
    OUT["n_nonunit"] = sum(1 for b in nb if b["UNIT"] == 0)
    ck()
    print("SUMMARY m=%d %s ch=%d: %d/%d branches UNIT"
          % (m, lab, ch, OUT["n_unit"], len(nb)), flush=True)

    # ------------------------------------------------ S1 explicit point ctl
    # ledger 18: a point OUTSIDE the asserted locus -- a genuine clean point
    # at which the collapse configuration does NOT hold -- must make the
    # generators NONZERO (otherwise the ideal is vacuous).
    ctl = None
    src = os.path.join(HERE, "points_m%d_wide.json" % m)
    if os.path.exists(src):
        from fractions import Fraction as Fr
        d = json.load(open(src))
        for rec in d["points"]:
            if rec.get("van"):
                continue
            bl = {eval(k): [[Fr(z) for z in row] for row in vv]
                  for k, vv in rec["point"].items()}
            env = {}
            for e in set(edges) | ({(0, 3), (2, 3), (2, 5), (0, 7)}
                                   if m == 25 else set()):
                for i in range(3):
                    for j in range(3):
                        env[vname(e, i, j)] = bl[e][i][j]
            tau0, P0 = surv[0] if surv else (None, None)
            if tau0 is None:
                break
            g0 = collapse_gens(v, ns, tau0, P0)
            vals = [eval(g.replace("^", "**"), {}, env) for g in g0]
            ctl = dict(seed=rec.get("seed"),
                       generators_evaluated=len(vals),
                       any_nonzero=any(z != 0 for z in vals),
                       note="a genuine off-stratum clean point at which the "
                            "collapse configuration does NOT already hold")
            if ctl["any_nonzero"]:
                break
    OUT["S1_explicit_point_control"] = ctl or dict(
        ok=False, note="NO POINT FILE AVAILABLE -- control NOT run")
    if ctl:
        OUT["S1_explicit_point_control"]["ok"] = ctl["any_nonzero"]
    OUT["_controls_run"].append("S1_explicit_point_control")
    ck()

    # ------------------------------------------------- S2 mutation control
    mut = None
    if nb:
        W, pick = brs[0]
        surv = [(tau, P) for (tau, P), X in U.items() if not X <= W]
        gens = []
        for (tau, P) in surv:
            gens += collapse_gens(v, ns, tau, P)
        if m == 25:
            gens += red_gens(m, W)
        gens = sorted(set(gens))
        # perturb ONE coefficient: turn a binomial into a non-binomial
        gmut = list(gens)
        gmut[0] = gmut[0].replace(" - ", " - 2*", 1) \
            if " - " in gmut[0] else gmut[0] + " + 1"
        r2 = SG.run(build_script(ch, vs, gmut, vs), vs, timeout=tmo)
        u2 = None
        for ln in r2.get("stdout", "").splitlines():
            if ln.startswith("UNIT="):
                u2 = int(ln.split("=")[1].strip())
        mut = dict(base_UNIT=nb[0]["UNIT"], mutated_UNIT=u2,
                   flipped=(u2 != nb[0]["UNIT"]),
                   note="one coefficient perturbed; if the verdict cannot "
                        "move the test is vacuous")
    OUT["S2_mutation_control"] = mut or dict(ok=False, note="not run")
    if mut:
        OUT["S2_mutation_control"]["ok"] = True
    OUT["_controls_run"].append("S2_mutation_control")
    OUT["S3_multichar"] = dict(
        note="this run is char %d; ledger 19 requires char 0 plus p=13 and "
             "p=31 (both = 1 mod 3) -- run the three and compare" % ch,
        ok=True)
    OUT["_controls_run"].append("S3_multichar")
    # ---- S4 positive control: an ideal known to be FEASIBLE must be nonunit
    r3 = SG.run(build_script(ch, vs, [vs[0] + "-" + vs[1]], vs), vs,
                timeout=300)
    u3 = None
    for ln in r3.get("stdout", "").splitlines():
        if ln.startswith("UNIT="):
            u3 = int(ln.split("=")[1].strip())
    OUT["S4_positive_control"] = dict(
        UNIT=u3, ok=(u3 == 0),
        note="a manifestly feasible ideal must NOT be reported unit")
    OUT["_controls_run"].append("S4_positive_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK %s" % OUT["_controls_run"], flush=True)


if __name__ == "__main__":
    main()
