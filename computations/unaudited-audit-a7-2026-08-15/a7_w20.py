#!/usr/bin/env python3
"""A7 -- TARGET 4(a)-(d): independent audit of W20's tools.

(a) THEOREM W20-L (site linearity).  Re-derived: every perfect matching uses
    exactly ONE edge at t, so the hafnian row-expansion gives
        Phi_w = sum_{s in N_Gamma(t)} A_ts[w_t][w_s] * haf_{Gamma-t-s}(w),
    whose coefficients involve no block at t and no colour at t.  Hence each
    clean equation is LINEAR in the 3 x 3deg site-t data, and the equations
    with w_t = c constrain only the row vector v_c = (A_ts[c][d])_{s,d}.
    Solving v_c in ker(M_c) for c = 0,1,2 therefore lands EXACTLY on the
    clean variety.  If the kernel of the COMMON system (rows from words whose
    whole t-fibre is clean) is 1-dimensional, v_0, v_1, v_2 are proportional,
    i.e. every Gamma block at t is rank one with a common t-vector: site t
    FACTORS.  All of this is verified below on explicit instances.

(b) THEOREM W20-R (pattern-rank).  For a neighbour pattern p, V_c(p) =
    (A_ts[c][p_s])_s is a NONZERO vector orthogonal to Cf(p), so
    rank Cf(p) <= deg(t) - 1; equality makes V_0, V_1, V_2 proportional.
    Chaining over regular patterns that differ in ONE coordinate transports
    the proportionality constant (the >= 1 shared coordinates have nonzero
    entries), so connected + covering => site t factors.
    HIDDEN HYPOTHESES probed below: deg(t) >= 2 is REQUIRED for the chaining
    step; all cells nonzero is required twice.

(c) explicit non-factoring clean points at 26/27/28 (constructed here from a
    J-point by my own descent) and (d) the automorphism claim.
"""
from __future__ import annotations
import os, sys, json, random, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, EDGES, EIDX, MIXED, WORDS, F_gamma, k_of,
                     gamma_edges, PM_E, PMS, cell_index)
from a7_w19k_c8 import C8_WITNESS

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------ linear alg --
def rref(rows, n):
    R = [list(map(Fr, r)) for r in rows]
    piv, r = [], 0
    for c in range(n):
        sel = None
        for i in range(r, len(R)):
            if R[i][c]:
                sel = i
                break
        if sel is None:
            continue
        R[r], R[sel] = R[sel], R[r]
        pv = R[r][c]
        R[r] = [v / pv for v in R[r]]
        for i in range(len(R)):
            if i != r and R[i][c]:
                f = R[i][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    return [row for row in R[:r]], piv


def kernel(rows, n):
    if not rows:
        return [[Fr(int(i == k)) for i in range(n)] for k in range(n)]
    R, piv = rref(rows, n)
    free = [c for c in range(n) if c not in piv]
    out = []
    for f in free:
        v = [Fr(0)] * n
        v[f] = Fr(1)
        for i, p in enumerate(piv):
            v[p] = -R[i][f]
        out.append(v)
    return out


def proportional(a, b):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] * b[j] - a[j] * b[i] != 0:
                return False
    return True


# --------------------------------------------------- hafnian (subset DP) --
def haf_sub(blocks, edges, verts, w):
    """MY route: subset DP over the vertex list (W20 uses a recursion)."""
    verts = tuple(sorted(verts))
    idx = {v: i for i, v in enumerate(verts)}
    n = len(verts)
    ES = {tuple(sorted(e)) for e in edges}
    full = (1 << n) - 1
    memo = {}

    def rec(used):
        if used == full:
            return Fr(1)
        if used in memo:
            return memo[used]
        a = 0
        while (used >> a) & 1:
            a += 1
        tot = Fr(0)
        for b in range(a + 1, n):
            if (used >> b) & 1:
                continue
            e = (min(verts[a], verts[b]), max(verts[a], verts[b]))
            if e in ES:
                tot += blocks[e][w[e[0]]][w[e[1]]] * rec(used | (1 << a) | (1 << b))
        memo[used] = tot
        return tot
    return rec(0)


def phi_value(blocks, gam, w):
    return haf_sub(blocks, gam, list(range(8)), w)


# ---------------------------------------------------------- site systems --
def neighbours(gam, t):
    return sorted(s for e in gam for s in e if t in e and s != t)


def site_system(blocks, gam, t, words):
    nbr = neighbours(gam, t)
    ncols = 3 * len(nbr)
    others = [e for e in gam if t not in e]
    rows = {0: [], 1: [], 2: []}
    for w in words:
        row = [Fr(0)] * ncols
        for k, s in enumerate(nbr):
            vs = [v for v in range(8) if v not in (t, s)]
            row[3 * k + w[s]] += haf_sub(blocks, others, vs, w)
        if any(row):
            rows[w[t]].append(row)
    return nbr, ncols, rows


def site_vectors(blocks, gam, t):
    nbr = neighbours(gam, t)
    out = []
    for c in range(3):
        v = []
        for s in nbr:
            e = (min(t, s), max(t, s))
            for d in range(3):
                v.append(blocks[e][c][d] if e[0] == t else blocks[e][d][c])
        out.append(v)
    return nbr, out


def write_site(blocks, gam, t, nbr, vs):
    for k, s in enumerate(nbr):
        e = (min(t, s), max(t, s))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    blocks[e][c][d] = vs[c][3 * k + d]
                else:
                    blocks[e][d][c] = vs[c][3 * k + d]


def factors_at(blocks, gam, t):
    _, vs = site_vectors(blocks, gam, t)
    return all(proportional(vs[a], vs[b]) for a in range(3)
               for b in range(a + 1, 3))


def common_words(clean, t):
    S = set(clean)
    return [w for w in clean
            if all(w[:t] + (c,) + w[t + 1:] in S for c in range(3))]


# ------------------------------------------------------------- J-point ----
def jpoint(gam, rng, tries=400):
    Fg = [m for m in PMS if all(tuple(sorted(e)) in set(gam) for e in m)]
    for _ in range(tries):
        t = {e: Fr(rng.randint(-9, 9) or 3, rng.randint(1, 4)) for e in gam}
        e0 = gam[0]
        a = b = Fr(0)
        for m in Fg:
            p = Fr(1)
            has = False
            for e in m:
                if e == e0:
                    has = True
                else:
                    p *= t[e]
            if has:
                a += p
            else:
                b += p
        if a == 0:
            continue
        t[e0] = -b / a
        if all(v != 0 for v in t.values()):
            return {e: [[t[e]] * 3 for _ in range(3)] for e in gam}
    return None


# -------------------------------------------------------------- descent ---
def descent(T, seed, steps=160, tries=90):
    gam = gamma_edges(T)
    Fg = F_gamma(T)
    clean = [w for w in MIXED if k_of(T, w, Fg) == 0]
    rng = random.Random(seed)
    blocks = jpoint(gam, rng)
    if blocks is None:
        return None
    best = None
    for step in range(steps):
        t = rng.randrange(8)
        nbr, ncols, rows = site_system(blocks, gam, t, clean)
        Ks = [kernel(rows[c], ncols) for c in range(3)]
        if any(not K for K in Ks):
            continue
        pick = None
        for _ in range(tries):
            vs, ok = [], True
            for c in range(3):
                for _ in range(40):
                    co = [Fr(rng.randint(-7, 7)) for _ in Ks[c]]
                    v = [sum(co[i] * Ks[c][i][j] for i in range(len(Ks[c])))
                         for j in range(ncols)]
                    if all(x != 0 for x in v):
                        break
                else:
                    ok = False
                    break
                vs.append(v)
            if not ok:
                break
            rk = len(rref(vs, ncols)[0])
            if pick is None or rk > pick[0]:
                pick = (rk, vs)
            if rk == 3:
                break
        if pick is None:
            continue
        write_site(blocks, gam, t, nbr, pick[1])
        fac = [s for s in range(8) if factors_at(blocks, gam, s)]
        if best is None or len(fac) < best[0]:
            best = (len(fac), [dict(e) if False else None])
    fac = [s for s in range(8) if factors_at(blocks, gam, s)]
    clean_ok = all(phi_value(blocks, gam, w) == 0 for w in clean)
    nz = all(blocks[e][i][j] != 0 for e in gam
             for i in range(3) for j in range(3))
    return dict(m=sum(1 for x in T if x), seed=seed, factoring_sites=fac,
                n_factoring=len(fac), clean_equations_hold=clean_ok,
                all_gamma_cells_nonzero=nz, n_clean=len(clean),
                blocks={str(e): [[str(v) for v in r] for r in blocks[e]]
                        for e in gam}), blocks, gam, clean


# ------------------------------------------------------ pattern criterion -
def pattern_analysis(blocks, gam, t, clean):
    nbr = neighbours(gam, t)
    deg = len(nbr)
    others = [e for e in gam if t not in e]
    crows = common_words(clean, t)
    pats = {}
    for w in crows:
        p = tuple(w[s] for s in nbr)
        row = []
        for s in nbr:
            vs = [v for v in range(8) if v not in (t, s)]
            row.append(haf_sub(blocks, others, vs, w))
        pats.setdefault(p, []).append(row)
    ranks = {p: len(rref(rows, deg)[0]) for p, rows in pats.items()}
    over = [p for p, r in ranks.items() if r > deg - 1]      # must be empty
    reg = [p for p, r in ranks.items() if r == deg - 1]
    # connectivity of regular patterns under single-coordinate moves
    idx = {p: i for i, p in enumerate(reg)}
    par = list(range(len(reg)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for p in reg:
        for k in range(deg):
            for d in range(3):
                q = p[:k] + (d,) + p[k + 1:]
                if q in idx and q != p:
                    ra, rb = find(idx[p]), find(idx[q])
                    if ra != rb:
                        par[ra] = rb
    ncomp = len({find(i) for i in range(len(reg))}) if reg else 0
    covered = {(k, d) for p in reg for k, d in enumerate(p)}
    covering = covered == {(k, d) for k in range(deg) for d in range(3)}
    return dict(site=t, deg=deg, n_patterns=len(pats), n_regular=len(reg),
                rank_violations=len(over), n_components=ncomp,
                connected=(ncomp == 1), covering=covering,
                criterion_fires=(ncomp == 1 and covering and bool(reg)),
                actually_factors=factors_at(blocks, gam, t))


# ------------------------------------------------------- automorphisms ----
def aut_group(T):
    Tm = list(T)
    out = []
    for perm in itertools.permutations(range(8)):
        for cp in itertools.permutations(range(3)):
            ok = True
            for ei, (u, v) in enumerate(EDGES):
                pu, pv = perm[u], perm[v]
                e2 = EIDX[(min(pu, pv), max(pu, pv))]
                new = 0
                for c in range(9):
                    if not (Tm[ei] >> c) & 1:
                        continue
                    i, j = c // 3, c % 3
                    ci, cj = cp[i], cp[j]
                    if pu < pv:
                        new |= 1 << (3 * ci + cj)
                    else:
                        new |= 1 << (3 * cj + ci)
                if new != Tm[e2]:
                    ok = False
                    break
            if ok:
                out.append((perm, cp))
    return out


def main():
    res = {}
    # ---- (a)+(c): descent to non-factoring clean points -------------------
    for m in (26, 27, 28):
        T = W8_IMMUNE[m]
        runs = []
        for seed in (2, 5, 11, 23):
            r, blocks, gam, clean = descent(T, seed)
            r.pop("blocks")
            runs.append(r)
            print("m=%d seed=%d -> factoring %s  clean_ok=%s nonzero=%s"
                  % (m, seed, r["factoring_sites"], r["clean_equations_hold"],
                     r["all_gamma_cells_nonzero"]), flush=True)
        res["descent_m%d" % m] = runs
    # ---- keep one m=28 point for the pattern criterion --------------------
    pat = {}
    for m in (26, 27, 28):
        T = W8_IMMUNE[m]
        r, blocks, gam, clean = descent(T, 5)
        pat["m%d_point" % m] = dict(factoring=r["factoring_sites"],
                                    clean_ok=r["clean_equations_hold"],
                                    nonzero=r["all_gamma_cells_nonzero"],
                                    blocks=r["blocks"])
        pa = [pattern_analysis(blocks, gam, t, clean) for t in range(8)]
        pat["m%d_patterns" % m] = pa
        print("m=%d pattern criterion:" % m, flush=True)
        for d in pa:
            print("   site %d deg %d: patterns %d regular %d rank_viol %d "
                  "conn %s cover %s fires %s | factors %s"
                  % (d["site"], d["deg"], d["n_patterns"], d["n_regular"],
                     d["rank_violations"], d["connected"], d["covering"],
                     d["criterion_fires"], d["actually_factors"]), flush=True)
    res["pattern"] = pat
    # ---- (d) automorphisms ------------------------------------------------
    auts = {}
    for m in range(24, 29):
        g = aut_group(W8_IMMUNE[m])
        auts["m%d" % m] = dict(order=len(g),
                               elements=[[list(p), list(c)] for p, c in g])
        print("Aut(m=%d) order %d: %s" % (m, len(g), auts["m%d" % m]["elements"]),
              flush=True)
    g = aut_group(C8_WITNESS)
    auts["C8"] = dict(order=len(g), elements=[[list(p), list(c)] for p, c in g])
    print("Aut(C_8 witness) order %d" % len(g), flush=True)
    # mutation control: a template with an obvious symmetry must show it
    sym = [511] * 28
    auts["all_full_control"] = dict(order=len(aut_group(sym)))
    print("CONTROL Aut(all-FULL template) order %d (expect 40320*6=241920)"
          % auts["all_full_control"]["order"], flush=True)
    res["automorphisms"] = auts
    json.dump(res, open(os.path.join(HERE, "results_w20.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
