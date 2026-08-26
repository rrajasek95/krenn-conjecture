#!/usr/bin/env python3
"""A7 -- TARGET 1(a): independent audit of THEOREM W16-A (m = 25 dichotomy).

Independent re-derivation + verification, in four parts.

(A) THE TWO-TERM IDENTITY.  With x = (w0,w1,w2,w3), y = (w4,w5,w6,w7),
        Phi_w  =  D_x[y4][y5] * A67[y6][y7]  +  E_x[y4][y7] * A56[y5][y6]
    where
        P_L(x) = A01[x0][x1]A23[x2][x3] + A02[x0][x2]A13[x1][x3]
                                        + A03[x0][x3]A12[x1][x2]
        D_x    = P_L(x) A45 + A03[x0][x3] * A14[x1][.] (x) A25[x2][.]
        E_x    = P_L(x) A47 + A23[x2][x3] * A14[x1][.] (x) A07[x0][.]
    Verified as an identity of EXACT multilinear polynomials on all 6561 words
    (my own sparse polynomial arithmetic, no probe code).

(B) X_free.  Both the word-clean and the effectively-clean versions of
    "every one of the 81 y-words is clean" are computed exhaustively.

(C) STEP A, re-derived BY HAND (see PROOF below) and confirmed exactly:
    for FIXED A56, A67 with all 18 cells nonzero, the linear system
        D[a][b] A67[c][d] + E[a][d] A56[b][c] = 0    for all a,b,c,d in {0,1,2}
    has ONLY the zero solution unless rank(M6) = 1, where M6 is the 3x6 matrix
    with row c = (A56[0][c],A56[1][c],A56[2][c], A67[c][0],A67[c][1],A67[c][2]);
    and rank(M6) = 1 is EXACTLY "site 6 factors" (both Gamma blocks at site 6
    rank one with a common site-6 vector).  Nullity is then exactly 3.

    HAND PROOF.  The system decouples over a: for each a it reads
        D[b] A67[c][d] + E[d] A56[b][c] = 0            (*)
    in the 6 unknowns D[0..2], E[0..2].
    - If D = 0 then E[d]A56[b][c] = 0 for all b,c,d and, all cells of A56
      being nonzero, E = 0.  Symmetrically E = 0 forces D = 0.  So a nonzero
      solution has D != 0 and E != 0.
    - Fix (b0,c0).  (*) gives E[d] = -D[b0] A67[c0][d] / A56[b0][c0] for all d,
      i.e. E is parallel to the row A67[c0][.]; this holds for EVERY c0, so
      A67[c][d] = delta[c] E[d] for some delta (E != 0).
    - Fix (c0,d0).  (*) gives D[b] = -E[d0] A56[b][c0] / A67[c0][d0] for all b,
      i.e. D is parallel to the column A56[.][c0]; for EVERY c0, so
      A56[b][c] = D[b] gamma[c] for some gamma (D != 0).
    - Substituting: D[b]E[d](delta[c] + gamma[c]) = 0 for all b,c,d, hence
      delta = -gamma.  Then row c of M6 equals gamma[c]*(D[0],D[1],D[2],
      -E[0],-E[1],-E[2]): rank(M6) = 1, A56 = D (x) gamma, A67 = -gamma (x) E,
      so both Gamma blocks at site 6 are rank one with the SAME site-6 vector
      gamma: site 6 factors.
    - Conversely if row c of M6 is gamma[c]*v then D[b] := v_b, E[d] := -v_{3+d}
      solves (*); as the three a-blocks are independent copies, nullity = 3
      exactly (the per-a solution space is 1-dimensional: D determines
      A56 = D (x) gamma up to scale, and gamma[c] != 0 pins E).
    Consequence: rank(M6) >= 2  =>  D_x = E_x = 0 for every x whose full 81-word
    y-box is clean.  That is exactly the W16-A dichotomy.

(D) CONTROLS.  (i) exhaustive structured sweep (ledger 12) over ALL rank
    profiles reachable with entries in a small set, not random draws;
    (ii) the sharp near-miss: A56, A67 both rank 1 with NON-parallel site-6
    vectors (rank(M6) = 2) must have nullity 0;
    (iii) mutation controls that must FIRE.
"""
from __future__ import annotations
import os, sys, json, itertools, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, EDGES, EIDX, MIXED, WORDS, F_gamma, PM_E,
                     cell_index, k_of, word_clean, single_cells, fibre)

HERE = os.path.dirname(os.path.abspath(__file__))
T25 = W8_IMMUNE[25]


# --------------------------------------------------- sparse exact polys ----
def pmul(a, b):
    o = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            k = tuple(sorted(ma + mb))
            v = o.get(k, 0) + ca * cb
            if v:
                o[k] = v
            else:
                o.pop(k, None)
    return o


def padd(*ps):
    o = {}
    for p in ps:
        for k, c in p.items():
            v = o.get(k, 0) + c
            if v:
                o[k] = v
            else:
                o.pop(k, None)
    return o


def var(ei, c):
    return {((ei, c),): 1}


def Aterm(u, v, cu, cv):
    """the polynomial variable A_uv[cu][cv] (u<v)."""
    return var(EIDX[(u, v)], 3 * cu + cv)


# ------------------------------------------------------------- part (A) ----
def phi_direct(T, w, Fg):
    o = {}
    for mi in Fg:
        mon = tuple(sorted((e, cell_index(e, w)) for e in PM_E[mi]))
        o[mon] = o.get(mon, 0) + 1
    return o


def P_L(x):
    x0, x1, x2, x3 = x
    return padd(pmul(Aterm(0, 1, x0, x1), Aterm(2, 3, x2, x3)),
                pmul(Aterm(0, 2, x0, x2), Aterm(1, 3, x1, x3)),
                pmul(Aterm(0, 3, x0, x3), Aterm(1, 2, x1, x2)))


def D_mat(x):
    x0, x1, x2, x3 = x
    pl = P_L(x)
    return [[padd(pmul(pl, Aterm(4, 5, a, b)),
                  pmul(Aterm(0, 3, x0, x3),
                       pmul(Aterm(1, 4, x1, a), Aterm(2, 5, x2, b))))
             for b in range(3)] for a in range(3)]


def E_mat(x):
    x0, x1, x2, x3 = x
    pl = P_L(x)
    return [[padd(pmul(pl, Aterm(4, 7, a, d)),
                  pmul(Aterm(2, 3, x2, x3),
                       pmul(Aterm(1, 4, x1, a), Aterm(0, 7, x0, d))))
             for d in range(3)] for a in range(3)]


def check_identity():
    Fg = F_gamma(T25)
    bad = []
    for x in itertools.product(range(3), repeat=4):
        D, E = D_mat(x), E_mat(x)
        for y in itertools.product(range(3), repeat=4):
            a, b, c, d = y
            lhs = phi_direct(T25, tuple(x) + tuple(y), Fg)
            rhs = padd(pmul(D[a][b], Aterm(6, 7, c, d)),
                       pmul(E[a][d], Aterm(5, 6, b, c)))
            if lhs != rhs:
                bad.append((x, y))
    return len(bad), bad[:5], len(Fg)


# ------------------------------------------------------------- part (B) ----
def x_free_sets():
    Fg = F_gamma(T25)
    sc = single_cells(T25)
    wc, ec = [], []
    for x in itertools.product(range(3), repeat=4):
        allw = [tuple(x) + tuple(y) for y in itertools.product(range(3), repeat=4)]
        if all(word_clean(T25, w, sc) for w in allw):
            wc.append(x)
        if all(k_of(T25, w, Fg) == 0 for w in allw):
            ec.append(x)
    return wc, ec


# ------------------------------------------------------------- part (C) ----
def nullity(rows, ncols):
    rows = [list(map(Fraction, r)) for r in rows]
    rank, nr = 0, len(rows)
    for c in range(ncols):
        sel = None
        for i in range(rank, nr):
            if rows[i][c]:
                sel = i
                break
        if sel is None:
            continue
        rows[rank], rows[sel] = rows[sel], rows[rank]
        pv = rows[rank][c]
        rows[rank] = [v / pv for v in rows[rank]]
        for i in range(nr):
            if i != rank and rows[i][c]:
                f = rows[i][c]
                rows[i] = [p - f * q for p, q in zip(rows[i], rows[rank])]
        rank += 1
    return ncols - rank


def rank_of(rows, ncols):
    return ncols - nullity(rows, ncols)


def per_a_system(A56, A67):
    """(*) for one a: unknowns [D0,D1,D2,E0,E1,E2]."""
    rows = []
    for b, c, d in itertools.product(range(3), repeat=3):
        r = [0] * 6
        r[b] += A67[c][d]
        r[3 + d] += A56[b][c]
        rows.append(r)
    return rows


def full_system(A56, A67):
    """all a: unknowns D[a][b] (9) then E[a][d] (9)."""
    rows = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        r = [0] * 18
        r[3 * a + b] += A67[c][d]
        r[9 + 3 * a + d] += A56[b][c]
        rows.append(r)
    return rows


def M6(A56, A67):
    return [[A56[0][c], A56[1][c], A56[2][c],
             A67[c][0], A67[c][1], A67[c][2]] for c in range(3)]


def rank_M6(A56, A67):
    return rank_of(M6(A56, A67), 6)


def analyse(A56, A67):
    return dict(rank_M6=rank_M6(A56, A67),
                rank_A56=rank_of(A56, 3), rank_A67=rank_of(A67, 3),
                nullity_per_a=nullity(per_a_system(A56, A67), 6),
                nullity_full=nullity(full_system(A56, A67), 18))


# ---------------------------------------------------- exhaustive controls --
def _decouple_check(ntrials=40):
    """the full 18-unknown system must decouple into 3 identical copies of the
    per-a system, so nullity_full == 3 * nullity_per_a."""
    rnd = random.Random(11)
    bad = 0
    for _ in range(ntrials):
        A56 = [[rnd.randrange(-4, 5) or 3 for _ in range(3)] for _ in range(3)]
        A67 = [[rnd.randrange(-4, 5) or 2 for _ in range(3)] for _ in range(3)]
        if nullity(full_system(A56, A67), 18) != 3 * nullity(
                per_a_system(A56, A67), 6):
            bad += 1
    return bad


def _fast_has_kernel(A56, A67):
    """integer Gaussian elimination on the 27x6 per-a system; True iff the
    solution space is nonzero."""
    rows = []
    for b in range(3):
        for c in range(3):
            for d in range(3):
                r = [0] * 6
                r[b] += A67[c][d]
                r[3 + d] += A56[b][c]
                rows.append(r)
    rank = 0
    for col in range(6):
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pr = rows[rank]
        pv = pr[col]
        for i in range(rank + 1, len(rows)):
            if rows[i][col]:
                f = rows[i][col]
                rows[i] = [a * pv - f * b for a, b in zip(rows[i], pr)]
        rank += 1
        if rank == 6:
            return False
    return rank < 6


def _fast_rankM6(A56, A67):
    rows = [[A56[0][c], A56[1][c], A56[2][c],
             A67[c][0], A67[c][1], A67[c][2]] for c in range(3)]
    rank = 0
    for col in range(6):
        piv = None
        for i in range(rank, 3):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pr = rows[rank]
        pv = pr[col]
        for i in range(rank + 1, 3):
            if rows[i][col]:
                f = rows[i][col]
                rows[i] = [a * pv - f * b for a, b in zip(rows[i], pr)]
        rank += 1
        if rank == 3:
            break
    return rank


def exhaustive_sweep(vals):
    """LEDGER 12: EXHAUSTIVE over a structured all-cells-nonzero stratum.

    Sweeps every pair (A56, A67) with all 18 entries in `vals`.  The verdict
    must be: (solution space nonzero) <=> rank(M6) == 1, with no exceptions.
    """
    tally = {}
    viol = []
    n = 0
    mats = [[list(f[0:3]), list(f[3:6]), list(f[6:9])]
            for f in itertools.product(vals, repeat=9)]
    for A56 in mats:
        for A67 in mats:
            n += 1
            r6 = _fast_rankM6(A56, A67)
            hk = _fast_has_kernel(A56, A67)
            key = (r6, hk)
            tally[key] = tally.get(key, 0) + 1
            if hk != (r6 == 1) and len(viol) < 8:
                viol.append(dict(A56=A56, A67=A67, rank_M6=r6, has_kernel=hk))
    return n, {str(k): v for k, v in sorted(tally.items())}, viol


def near_miss_sweep():
    """SHARP NEAR MISS: A56 and A67 BOTH rank one but with NON-parallel
    site-6 vectors -- exhaustive over {1,2}-entried generating vectors.
    rank(M6) must be 2 and the solution space must be zero."""
    vs = list(itertools.product((1, 2), repeat=3))
    n, bad, tally = 0, [], {}
    for alpha in vs:
        for gamma in vs:
            A56 = [[alpha[b] * gamma[c] for c in range(3)] for b in range(3)]
            for gamma2 in vs:
                par = all(gamma2[i] * gamma[0] == gamma2[0] * gamma[i]
                          for i in range(3))
                for psi in vs:
                    A67 = [[gamma2[c] * psi[d] for d in range(3)]
                           for c in range(3)]
                    n += 1
                    r6 = _fast_rankM6(A56, A67)
                    hk = _fast_has_kernel(A56, A67)
                    tally[str((par, r6, hk))] = tally.get(str((par, r6, hk)), 0) + 1
                    if (not par) and (r6 != 2 or hk) and len(bad) < 8:
                        bad.append(dict(A56=A56, A67=A67, rank_M6=r6,
                                        has_kernel=hk))
                    if par and (r6 != 1 or not hk) and len(bad) < 8:
                        bad.append(dict(parallel=True, A56=A56, A67=A67,
                                        rank_M6=r6, has_kernel=hk))
    return n, tally, bad


def mutation_controls():
    """Controls that MUST fire (detector sanity)."""
    out = {}
    # M1: drop the all-nonzero hypothesis -> the equivalence must BREAK.
    # search a small stratum for an explicit witness with a zero cell.
    wit = None
    for A56f in itertools.product((0, 1, 2), repeat=9):
        A56 = [list(A56f[0:3]), list(A56f[3:6]), list(A56f[6:9])]
        if all(v for r_ in A56 for v in r_):
            continue
        A67 = [[1, 2, 3], [1, 1, 4], [2, 1, 1]]
        r = analyse(A56, A67)
        if r["nullity_full"] > 0 and r["rank_M6"] >= 2:
            wit = dict(A56=A56, A67=A67, **r)
            break
    out["M1_zero_cell_breaks_equivalence"] = dict(fired=(wit is not None),
                                                  witness=wit)
    # M2: perturb one cell of a factoring pair -> nullity must drop to 0.
    g = (1, 2, 3)
    A56 = [[a * c for c in g] for a in (1, 2, 5)]
    A67 = [[g[c] * d for d in (1, 3, 7)] for c in range(3)]
    base = analyse(A56, A67)
    A67[1][1] += 1
    pert = analyse(A56, A67)
    out["M2_perturb_factoring"] = dict(base=base, perturbed=pert,
                                       fired=(base["nullity_full"] == 3 and
                                              pert["nullity_full"] == 0))
    # M3: planted solution check -- construct (D,E) from M6 rank 1 and verify
    A56 = [[a * c for c in g] for a in (1, 2, 5)]
    A67 = [[-g[c] * d for d in (1, 3, 7)] for c in range(3)]
    D = [1, 2, 5]
    E = [1, 3, 7]
    resid = max(abs(D[b] * A67[c][d] + E[d] * A56[b][c])
                for b, c, d in itertools.product(range(3), repeat=3))
    out["M3_planted_solution_residual"] = dict(residual=resid, fired=(resid == 0))
    return out


def main():
    res = {}
    nb, sample, nF = check_identity()
    res["A_two_term_identity"] = dict(mismatches=nb, sample=str(sample), nF=nF,
                                      n_words=6561)
    print("A) two-term identity: |F(Gamma)|=%d  mismatches over 6561 words = %d"
          % (nF, nb))
    wc, ec = x_free_sets()
    res["B_X_free"] = dict(word_clean=[list(x) for x in wc],
                           eff_clean=[list(x) for x in ec])
    print("B) X_free (word-clean) = %s ; (effectively-clean) = %s"
          % (wc, ec))
    dc = _decouple_check()
    res["C_decoupling_mismatches"] = dc
    print("C-0) nullity_full == 3*nullity_per_a failures:", dc, flush=True)
    for tag, vals in (("{1,2}", (1, 2)), ("{-1,1}", (-1, 1)),
                      ("{1,2,3} rank-1 A56", None)):
        if vals is None:
            continue
        n1, t1, v1 = exhaustive_sweep(vals)
        print("C-i) EXHAUSTIVE sweep entries in %s: %d instances, tally %s, "
              "violations %d" % (tag, n1, t1, len(v1)), flush=True)
        res["C_exhaustive_sweep_%s" % tag] = dict(n=n1, tally=t1,
                                                  violations=v1)
    n2, t2, v2 = near_miss_sweep()
    print("C-ii) SHARP NEAR-MISS sweep: %d instances, tally %s, violations %d"
          % (n2, t2, len(v2)), flush=True)
    res["C_near_miss"] = dict(n=n2, tally=t2, violations=v2)
    mc = mutation_controls()
    res["D_mutation_controls"] = mc
    for k, v in mc.items():
        print("D) %s fired=%s" % (k, v.get("fired")))
    json.dump(res, open(os.path.join(HERE, "results_w16a.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
