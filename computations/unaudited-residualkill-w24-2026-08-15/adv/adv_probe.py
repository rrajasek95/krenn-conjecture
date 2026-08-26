#!/usr/bin/env python3
"""ADVERSARIAL W24 -- controls, coincidence-triple certificates, Regime-B
ratio diagnostics, and FIELD-GENERIC (Q, Q(omega), Q(i)) descent + verdict.

UNAUDITED probe.  Exact only, no floats.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
W24 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-residualkill-w24-2026-08-15"
sys.path.insert(0, W24)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402
import adv_field as F                                             # noqa: E402

L = (0, 1, 2, 3)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
ISIG = {v: k for k, v in SIG.items()}


def ed(u, v):
    return (u, v) if u < v else (v, u)


# ================================================== field-generic machinery
def verdict_gen(m, bl, one, zero):
    """residual-system verdict over ANY exact field."""
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    rows_sk, cleanw, cells, live = RS.row_skeleton(m)
    idx = {e: i for i, e in enumerate(cells)}
    n = len(cells)
    allv = tuple(range(8))
    out = []
    for w, ones in rows_sk:
        v = [zero] * n
        for e in ones:
            rest = tuple(x for x in allv if x not in e)
            v[idx[e]] = F.haf_gen(bl, gam_set, rest, w, one, zero)
        c = F.haf_gen(bl, gam_set, allv, w, one, zero)
        if any(bool(x) for x in v) or c:
            out.append((w, v, c))
    aug = [list(v) + [-c] for _, v, c in out]
    R, piv = F.rref_gen(aug, n + 1, zero, one)
    res = dict(n_unknowns=n, n_rows=len(out), rank=len(piv))
    if n in piv:
        res.update(inconsistent=True, forced_zero=[], killed=True)
    else:
        sol = [zero] * n
        for i, pc in enumerate(piv):
            if pc < n:
                sol[pc] = R[i][n]
        ker = F.kernel_gen([list(v) for _, v, _ in out], n, zero, one)
        forced = [str(cells[i]) for i in range(n)
                  if not sol[i] and all(not b[i] for b in ker)]
        res.update(inconsistent=False, solution_dim=len(ker),
                   forced_zero=forced, killed=bool(forced))
    return res


def clean_viol_gen(m, bl, one, zero):
    gam_set = set(C.gamma_edges(C.TEMPLATES[m]))
    allv = tuple(range(8))
    return sum(1 for w in P.w21_clean(m)
               if F.haf_gen(bl, gam_set, allv, w, one, zero))


def seed_field(gam, gam_set, rng, cls, vals, tries=500):
    """field-generic 'J-point' seed: every cell of block e equals t_e, and
    one t_{e0} is solved so that the SCALAR Gamma-hafnian vanishes -- then
    Phi == 0 on ALL words, so the clean layer holds exactly."""
    one, zero = cls(1, 0), cls(0, 0)
    for _ in range(tries):
        t = {e: rng.choice(vals) for e in gam}
        e0 = gam[rng.randrange(len(gam))]
        a = b = zero
        for M in C.PMS:
            if not all(e in gam_set for e in M):
                continue
            p, has = one, False
            for e in M:
                if e == e0:
                    has = True
                else:
                    p = p * t[e]
            if has:
                a = a + p
            else:
                b = b + p
        if not a:
            continue
        t[e0] = -b / a
        if all(bool(v) for v in t.values()):
            return {e: [[t[e]] * 3 for _ in range(3)] for e in gam}
    return None


def descent_gen(m, rng, cls, order=None, passes=3, bl=None, vals=None):
    """exact descent onto the clean layer over an arbitrary quadratic field."""
    one, zero = cls(1, 0), cls(0, 0)
    T = C.TEMPLATES[m]
    gam = C.gamma_edges(T)
    gam_set = set(gam)
    clean = P.w21_clean(m)
    if vals is None:
        vals = [cls(1, 0), cls(0, 1), cls(-1, -1), cls(2, 0), cls(1, 1),
                cls(-1, 0), cls(0, -1), cls(1, -1), cls(-1, 1), cls(3, 0)]
    if bl is None:
        bl = seed_field(gam, gam_set, rng, cls, vals)
    if bl is None:
        return None, clean
    order = list(range(8)) if order is None else list(order)
    for _ in range(passes):
        for t in order:
            nb = sorted({s for e in gam for s in e if t in e and s != t})
            ncols = 3 * len(nb)
            rows = {0: [], 1: [], 2: []}
            for w in clean:
                r = [zero] * ncols
                nzr = False
                for k, s in enumerate(nb):
                    vs = tuple(v for v in range(8) if v != t and v != s)
                    h = F.haf_gen(bl, gam_set, vs, w, one, zero)
                    if h:
                        r[3 * k + w[s]] = r[3 * k + w[s]] + h
                        nzr = True
                if nzr and any(bool(x) for x in r):
                    rows[w[t]].append(r)
            newv, ok = {}, True
            for c in range(3):
                Kb = F.kernel_gen(rows[c], ncols, zero, one)
                if not Kb:
                    ok = False
                    break
                for _try in range(150):
                    coef = [rng.choice(vals + [zero]) for _ in Kb]
                    v = [sum((coef[i] * Kb[i][j] for i in range(len(Kb))),
                             zero) for j in range(ncols)]
                    if all(bool(z) for z in v):
                        break
                else:
                    ok = False
                    break
                newv[c] = v
            if not ok:
                continue
            save = {e: [r[:] for r in bl[e]] for e in gam}
            for k, s in enumerate(nb):
                e = (min(t, s), max(t, s))
                for c in range(3):
                    for d in range(3):
                        if e[0] == t:
                            bl[e][c][d] = newv[c][3 * k + d]
                        else:
                            bl[e][d][c] = newv[c][3 * k + d]
            allv = tuple(range(8))
            if any(F.haf_gen(bl, gam_set, allv, w, one, zero) for w in clean):
                for e in gam:
                    bl[e] = save[e]
    return bl, clean


# ================================================== coincidence triples
def triple_certificates(m):
    """For each i in L: find virtual points v* and words W0,W1,W2 that are
    isolated rows for the three singles at i, with c_{e_a}(W_a)=c_{e_a}(v*).
    Returns per-i counts and one explicit example."""
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    rows_sk, cleanw, cells, live = RS.row_skeleton(m)
    solo = {}
    for w, ones in rows_sk:
        if len(ones) == 1:
            solo.setdefault(ones[0], set()).add(w)
    out = {}
    for i in L:
        es = [e for e in sing if e[0] == i]
        assert len(es) == 3, es
        # structural nondegeneracy: X_a = a^L_{k_b,k_c} * d_{k_a}
        k = sorted(set(L) - {i})
        Xok = all(ed(k[a], SIG[k[a]]) in gam_set for a in range(3))
        q = SIG[i]
        rpresent = [a for a in range(3) if ed(SIG[k[a]], q) in gam_set]
        found = None
        cnt = 0
        # a virtual point is a full word; W_a = v* with the two coords
        # (i, j_a) overwritten by the cell of e_a.
        for vstar in C.WORDS:
            Ws = []
            good = True
            for e in es:
                al, be = sing[e]
                w2 = list(vstar)
                w2[e[0]] = al
                w2[e[1]] = be
                w2 = tuple(w2)
                if w2 not in solo.get(e, ()):
                    good = False
                    break
                Ws.append(w2)
            if not good:
                continue
            cnt += 1
            if found is None:
                found = (list(vstar), [list(x) for x in Ws],
                         [str(e) for e in es])
        out[i] = dict(n_virtual_points=cnt, X_all_present=Xok,
                      n_R_edges_present=len(rpresent), example=found)
    return out


# ================================================== main
def main():
    out = {"_header": "ADVERSARIAL W24 probe: controls + certificates. "
                      "UNAUDITED, exact only."}
    rng = random.Random(770077)

    # ------------------------------------------------- POSITIVE CONTROL 1
    # a hand-built row set that IS consistent with all 12 cells nonzero:
    # rows  z_e - 1 = 0  for every e  (constant -1, coefficient 1).
    n = 12
    rows = []
    for e in range(n):
        v = [Fraction(0)] * n
        v[e] = Fraction(1)
        rows.append((None, v, Fraction(-1)))
    aug = [list(v) + [-c] for _, v, c in rows]
    R, piv = C.rref(aug, n + 1)
    sol = [Fraction(0)] * n
    for i, pc in enumerate(piv):
        if pc < n:
            sol[pc] = R[i][n]
    ker = C.kernel_basis([list(v) for _, v, _ in rows], n)
    forced = [i for i in range(n) if sol[i] == 0 and all(b[i] == 0
                                                         for b in ker)]
    pc1 = dict(inconsistent=(n in piv), solution=[str(x) for x in sol],
               forced=forced,
               DETECTOR_SEES_SURVIVOR=(n not in piv and not forced
                                       and all(x != 0 for x in sol)))
    out["control_positive_fake_rows"] = pc1
    print("CONTROL+ (fake consistent rows): survivor detected =",
          pc1["DETECTOR_SEES_SURVIVOR"], flush=True)

    # ------------------------------------------------- POSITIVE CONTROL 2
    # empty row set (the Regime-A-with-all-c_e-zero dream): must be a
    # survivor verdict.
    ker = C.kernel_basis([], n)
    pc2 = dict(kernel_dim=len(ker), forced=[])
    out["control_positive_empty"] = pc2
    print("CONTROL+ (empty row set): kernel dim =", len(ker), flush=True)

    # ------------------------------------------------- MUTATION CONTROL
    pts = P.stored_points()
    mut = []
    for (m, tag, bl) in pts[:3]:
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        clean = P.w21_clean(m)
        base = sum(1 for w in clean if C.phi(bl, gs, w) != 0)
        bl2 = {e: [r[:] for r in bl[e]] for e in gam}
        bl2[gam[0]][0][0] = bl2[gam[0]][0][0] + Fraction(1, 7)
        pert = sum(1 for w in clean if C.phi(bl2, gs, w) != 0)
        d2 = RS.verdict(m, bl2)
        mut.append(dict(m=m, tag=tag, clean_viol_before=base,
                        clean_viol_after=pert,
                        verdict_after_incons=d2["inconsistent"],
                        forced_after=len(d2["forced_zero"])))
        print("CONTROL~ mutation m=%d %s: clean violations %d -> %d"
              % (m, tag, base, pert), flush=True)
    out["control_mutation"] = mut

    # ------------------------------------------------- TRIPLE CERTIFICATES
    tc = {}
    for m in (25, 26, 27, 28):
        tc[m] = triple_certificates(m)
        print("TRIPLES m=%d: %s" % (m, {i: (tc[m][i]["n_virtual_points"],
                                            tc[m][i]["X_all_present"],
                                            tc[m][i]["n_R_edges_present"])
                                        for i in L}), flush=True)
    out["triple_certificates"] = tc

    # ------------------------------------------- REGIME-B RATIO DIAGNOSTIC
    diag = []
    for (m, tag, bl) in pts:
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        nphi = sum(1 for w in C.WORDS if C.phi(bl, gs, w) != 0)
        if nphi == 0:
            continue
        cellsl, rowsl, cleanw = RS.build_system(m, bl)
        idx = {e: i for i, e in enumerate(cellsl)}
        per = {}
        for w, v, c in rowsl:
            nz = [i for i in range(len(cellsl)) if v[i] != 0]
            if len(nz) != 1:
                continue
            e = cellsl[nz[0]]
            per.setdefault(e, []).append((-c / v[nz[0]], c == 0))
        rec = dict(m=m, tag=tag, nphi=nphi)
        for e, lst in sorted(per.items()):
            vals = {r for r, _ in lst}
            rec[str(e)] = dict(n_solo=len(lst), n_distinct_ratios=len(vals),
                               has_zero_ratio=any(r == 0 for r in vals))
        diag.append(rec)
        if len(diag) >= 4:
            break
    out["regimeB_ratio_diag"] = diag
    for r in diag:
        ks = [k for k in r if k.startswith("(")]
        print("REGIME-B %s m=%d nphi=%d : distinct ratios per single = %s"
              % (r["tag"], r["m"], r["nphi"],
                 [r[k]["n_distinct_ratios"] for k in ks]), flush=True)

    json.dump(out, open(os.path.join(HERE, "results_probe.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
