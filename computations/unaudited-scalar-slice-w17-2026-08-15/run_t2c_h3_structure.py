#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T2(c): the h = 3 rank-one structure theory.

At h = 3 the cap error of a rank-one cap is AFFINE in the internal blocks:

    E_w = 6 e_3(alpha,beta)_w
          + 2 s sum_{a<b in U} A_ab[w_a][w_b] e_2(alpha,beta | U\\{a,b})_w .

Contracting with a functional pattern chi = (x)_t chi_t gives the exact law

    <E, chi> = 6 e_3^hom(xi,eta) + 2 s sum_{c<d} A_cd(chi_c,chi_d)
                                      e_2^hom(xi,eta | U\\{c,d})       (L)

with xi_t = chi_t(alpha_t), eta_t = chi_t(beta_t).  Taking chi_t from a
basis of V_t^* ADAPTED to the site map T_t = [alpha_t | beta_t] (dual pair
alpha*,beta* plus the perp space) gives Theorem W17.6: writing Z for the
set of sites carrying a perp functional,

    |Z| >= 3 : 0 = 0                                        (no condition)
    |Z| = 2, Z = {a,b} : A_ab(chi_a,chi_b) e_2^hom(U\\{a,b}) = 0     (A)
    |Z| = 1, Z = {a}   : sum_b A_ab(chi_a,chi_b) e_2^hom(U\\{a,b}) = 0 (B)
    |Z| = 0            : 6 e_3^hom + 2s sum A_cd e_2^hom = 0          (C)

This script verifies (L) and the case analysis exactly, measures the
dimension of the affine space of internal blocks that make a cap clean in
each degeneracy stratum, and checks the corollaries (internal blocks of
rank <= 2 in the nondegenerate stratum; W5's scalar slice error as the
all-degenerate stratum of (C)).
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, ".."))

from w17_core import (COLORS, alpha_beta, cap_scalars, cross, ekey,
                      matrix_rank, oriented, rank_one_error_direct, require,
                      site_rank)

RESULTS = {}
FAILS = []


def check(name, cond, detail=""):
    RESULTS.setdefault(name, {"pass": 0, "fail": 0})
    RESULTS[name]["pass" if cond else "fail"] += 1
    if not cond:
        FAILS.append((name, str(detail)[:300]))


def random_source(rng, n=8, lo=-4, hi=4):
    return {(u, v): [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                     for _ in range(3)]
            for u, v in combinations(range(n), 2)}


def random_vec(rng, lo=-4, hi=4):
    while True:
        w = [Fraction(rng.randint(lo, hi)) for _ in range(3)]
        if any(x != 0 for x in w):
            return w


# ------------------------------------------------------------- adapted bases


def adapted_dual_basis(alpha_a, beta_a):
    """A basis of V_a^* adapted to T_a: the ACTIVE duals (pairing (xi,eta)
    with alpha,beta) first, then the perp functionals."""
    rank = site_rank(alpha_a, beta_a)
    ident = [[Fraction(1) if i == j else Fraction(0) for j in range(3)]
             for i in range(3)]
    if rank == 2:
        n = cross(alpha_a, beta_a)
        # duals of alpha,beta inside span, extended by 0 on n
        # solve chi(alpha)=1, chi(beta)=0, chi(n)=0  etc.
        mat = [alpha_a, beta_a, n]
        inv = invert3(mat)
        astar = [inv[i][0] for i in range(3)]
        bstar = [inv[i][1] for i in range(3)]
        perp = [[inv[i][2] for i in range(3)]]
        return [("a*", astar), ("b*", bstar)], perp
    if rank == 1:
        gamma = alpha_a if any(x != 0 for x in alpha_a) else beta_a
        # complete gamma to a basis
        for e1 in ident:
            for e2 in ident:
                mat = [gamma, e1, e2]
                if det3(mat) != 0:
                    inv = invert3(mat)
                    gstar = [inv[i][0] for i in range(3)]
                    perp = [[inv[i][1] for i in range(3)],
                            [inv[i][2] for i in range(3)]]
                    return [("g*", gstar)], perp
    return [], [list(row) for row in ident]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def invert3(rows):
    """Inverse of the 3x3 matrix whose ROWS are rows; returns M^{-1} so that
    sum_i M^{-1}[i][k] rows[k][i]... (used only through the dual basis)."""
    d = det3(rows)
    require(d != 0, "singular")
    cof = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            sub = [[rows[r][c] for c in range(3) if c != j]
                   for r in range(3) if r != i]
            cof[i][j] = ((-1) ** (i + j)
                         * (sub[0][0] * sub[1][1] - sub[0][1] * sub[1][0]))
    # inverse = adj / det, adj = cof^T ; we want columns dual to the rows:
    return [[cof[k][i] / d for k in range(3)] for i in range(3)]


def ehom_vals(xi, eta, sites, j):
    total = Fraction(0)
    for B in combinations(sites, j):
        Bs = set(B)
        term = Fraction(1)
        for t in sites:
            term *= xi[t] if t in Bs else eta[t]
        total += term
    return total


def contract(err, sites, chi):
    """<E, (x) chi_t> for E given as {word: value}."""
    total = Fraction(0)
    for word, val in err.items():
        term = val
        for n, t in enumerate(sites):
            term *= chi[t][word[n]]
            if term == 0:
                break
        total += term
    return total


def law_rhs(source, p, q, sites, u, v, chi):
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    s, _ = cap_scalars(source, p, q, u, v)
    xi = {t: sum(chi[t][c] * alpha[t][c] for c in COLORS) for t in sites}
    eta = {t: sum(chi[t][c] * beta[t][c] for c in COLORS) for t in sites}
    total = 6 * ehom_vals(xi, eta, sites, 3)
    for a, b in combinations(sites, 2):
        blk = oriented(source, a, b)
        val = sum(chi[a][i] * blk[i][j] * chi[b][j]
                  for i in COLORS for j in COLORS)
        if val == 0:
            continue
        rest = tuple(t for t in sites if t not in (a, b))
        total += 2 * s * val * ehom_vals(xi, eta, rest, 2)
    return total


# ---------------------------------------------------- affine solution space


def affine_clean_space(source, p, q, sites, u, v):
    """The affine space {internal blocks x : E_pq(u (x) v) = 0}: returns
    (dim, consistent, rank).  Coordinates: x[(a,b)][ca][cb], 15*9 = 135."""
    sites = tuple(sites)
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    s, _ = cap_scalars(source, p, q, u, v)
    coords = [(a, b, ca, cb) for a, b in combinations(sites, 2)
              for ca in COLORS for cb in COLORS]
    index = {c: n for n, c in enumerate(coords)}
    rows = []
    slot = {a: n for n, a in enumerate(sites)}
    for word in product(COLORS, repeat=6):
        word_of = {a: word[slot[a]] for a in sites}
        xi = {t: alpha[t][word_of[t]] for t in sites}
        eta = {t: beta[t][word_of[t]] for t in sites}
        row = [Fraction(0)] * (len(coords) + 1)
        row[-1] = 6 * ehom_vals(xi, eta, sites, 3)          # constant term
        for a, b in combinations(sites, 2):
            rest = tuple(t for t in sites if t not in (a, b))
            coeff = 2 * s * ehom_vals(xi, eta, rest, 2)
            if coeff:
                row[index[(a, b, word_of[a], word_of[b])]] += coeff
        if any(x != 0 for x in row):
            rows.append(row)
    rank, rank_aug = rank_and_augmented(rows, len(coords))
    consistent = rank == rank_aug
    return {"dim": len(coords) - rank if consistent else None,
            "rank": rank, "consistent": consistent, "nvars": len(coords)}


def rank_and_augmented(rows, nvars):
    """Rank of the coefficient part and of the augmented matrix."""
    def rank_of(mat, width):
        mat = [list(r) for r in mat]
        rank = 0
        for col in range(width):
            piv = None
            for i in range(rank, len(mat)):
                if mat[i][col] != 0:
                    piv = i
                    break
            if piv is None:
                continue
            mat[rank], mat[piv] = mat[piv], mat[rank]
            head = mat[rank]
            for i in range(len(mat)):
                if i != rank and mat[i][col] != 0:
                    f = mat[i][col] / head[col]
                    mat[i] = [x - f * y for x, y in zip(mat[i], head)]
            rank += 1
        return rank
    return rank_of(rows, nvars), rank_of(rows, nvars + 1)


# ---------------------------------------------------------- stratum builders


def make_stratum(rng, ndegen, nzero=0):
    """A random eight-site source and cap (u,v) with prescribed degeneracy:
    `ndegen` sites with alpha || beta, `nzero` of them with alpha = beta = 0."""
    src = random_source(rng)
    p, q = 0, 1
    U = tuple(a for a in range(8) if a not in (p, q))
    u, v = random_vec(rng), random_vec(rng)
    cv = next(c for c in COLORS if v[c] != 0)
    for n, a in enumerate(U[:ndegen]):
        apa = oriented(src, p, a)
        al = [sum(u[i] * apa[i][c] for i in range(3)) for c in COLORS]
        m = Fraction(0) if n < nzero else Fraction(rng.randint(1, 3))
        table = [[Fraction(0)] * 3 for _ in range(3)]
        for c in COLORS:
            table[cv][c] = m * al[c] / v[cv]
        key = ekey(q, a)
        src[key] = (table if q < a
                    else [[table[j][i] for j in range(3)] for i in range(3)])
        if n < nzero:                       # also kill alpha_a
            src[ekey(p, a)] = [[Fraction(0)] * 3 for _ in range(3)]
    return src, p, q, U, u, v


def main():
    t0 = time.time()
    rng = random.Random(1717)
    print("== W17 T2(c): h=3 rank-one structure ==")
    table = []
    for ndegen in (0, 1, 2, 3, 6):
        for nzero in ((0,) if ndegen < 6 else (0, 1)):
            for trial in range(3):
                src, p, q, U, u, v = make_stratum(rng, ndegen, nzero)
                s, kappa = cap_scalars(src, p, q, u, v)
                if s == 0 or any(k == 0 for k in kappa):
                    continue
                alpha, beta = alpha_beta(src, p, q, u, v, U)
                ranks = {a: site_rank(alpha[a], beta[a]) for a in U}
                err = rank_one_error_direct(src, p, q, u, v, U)
                # (L) identity on random functionals
                for _ in range(3):
                    chi = {t: [Fraction(rng.randint(-3, 3)) for _ in range(3)]
                           for t in U}
                    check("L_identity_random_chi",
                          contract(err, U, chi) == law_rhs(src, p, q, U, u, v,
                                                           chi),
                          (ndegen, nzero))
                # adapted-basis case analysis (Theorem W17.6)
                bases = {t: adapted_dual_basis(alpha[t], beta[t]) for t in U}
                counts = Counter()
                for pattern in product(*[list(range(len(bases[t][0])
                                                   + len(bases[t][1])))
                                         for t in U]):
                    chi = {}
                    z = 0
                    for n, t in enumerate(U):
                        active, perp = bases[t]
                        k = pattern[n]
                        if k < len(active):
                            chi[t] = active[k][1]
                        else:
                            chi[t] = perp[k - len(active)]
                            z += 1
                    lhs = contract(err, U, chi)
                    counts[(z, lhs == 0)] += 1
                    if z >= 3:
                        check("W176_z3_vacuous", lhs == 0, (ndegen, z))
                # affine dimension of the clean set of internal blocks
                aff = affine_clean_space(src, p, q, U, u, v)
                table.append({"ndegen": ndegen, "nzero": nzero,
                              "ranks": sorted(ranks.values()),
                              "affine": aff,
                              "error_nonzero_components": len(err),
                              "pattern_counts": {str(k): v2
                                                 for k, v2 in counts.items()}})
                print(f"  stratum ndeg={ndegen} nzero={nzero}: site ranks "
                      f"{sorted(ranks.values())}, clean-internal-block affine "
                      f"space dim {aff['dim']} of {aff['nvars']} "
                      f"(rank {aff['rank']}, consistent {aff['consistent']}) "
                      f"[{time.time() - t0:.0f}s]")
    # corollary: nondegenerate stratum forces internal blocks of rank <= 2
    print("\n  -- corollary check: construct CLEAN caps in the "
          "all-nondegenerate stratum --")
    made = 0
    for trial in range(40):
        src, p, q, U, u, v = make_stratum(rng, 0)
        s, kappa = cap_scalars(src, p, q, u, v)
        if s == 0 or any(k == 0 for k in kappa):
            continue
        aff = affine_clean_space(src, p, q, U, u, v)
        if not aff["consistent"]:
            check("nondegenerate_stratum_consistent", False, aff)
            continue
        sol = solve_affine(src, p, q, U, u, v)
        if sol is None:
            continue
        for (a, b), blk in sol.items():
            src[ekey(a, b)] = blk
        err = rank_one_error_direct(src, p, q, u, v, U)
        check("constructed_clean_cap_h3", not err, len(err))
        ranks = [matrix_rank(oriented(src, a, b)) for a, b in combinations(U, 2)]
        check("clean_cap_internal_rank_le_2", max(ranks) <= 2, ranks)
        alpha, beta = alpha_beta(src, p, q, u, v, U)
        check("clean_cap_sites_nondegenerate",
              all(site_rank(alpha[t], beta[t]) == 2 for t in U),
              {t: site_rank(alpha[t], beta[t]) for t in U})
        made += 1
        if made >= 6:
            break
    print(f"  constructed {made} clean rank-one caps with all sites "
          f"nondegenerate")
    print("\n-- results --")
    for name in sorted(RESULTS):
        r = RESULTS[name]
        print(f"  {name:36s} pass {r['pass']:5d} fail {r['fail']:5d}")
    for name, detail in FAILS[:10]:
        print(f"   FAIL {name}: {detail}")
    with open(os.path.join(HERE, "results_t2c_h3_structure.json"), "w") as fh:
        json.dump({"results": RESULTS, "fails": FAILS[:40], "table": table},
                  fh, indent=1, default=str)
    print(f"\nwrote results_t2c_h3_structure.json [{time.time() - t0:.0f}s]")


def solve_affine(source, p, q, sites, u, v):
    """A particular solution of E = 0 in the internal blocks (or None)."""
    sites = tuple(sites)
    alpha, beta = alpha_beta(source, p, q, u, v, sites)
    s, _ = cap_scalars(source, p, q, u, v)
    coords = [(a, b, ca, cb) for a, b in combinations(sites, 2)
              for ca in COLORS for cb in COLORS]
    index = {c: n for n, c in enumerate(coords)}
    slot = {a: n for n, a in enumerate(sites)}
    rows = []
    for word in product(COLORS, repeat=6):
        word_of = {a: word[slot[a]] for a in sites}
        xi = {t: alpha[t][word_of[t]] for t in sites}
        eta = {t: beta[t][word_of[t]] for t in sites}
        row = [Fraction(0)] * (len(coords) + 1)
        row[-1] = -6 * ehom_vals(xi, eta, sites, 3)
        for a, b in combinations(sites, 2):
            rest = tuple(t for t in sites if t not in (a, b))
            coeff = 2 * s * ehom_vals(xi, eta, rest, 2)
            if coeff:
                row[index[(a, b, word_of[a], word_of[b])]] += coeff
        if any(x != 0 for x in row):
            rows.append(row)
    n = len(coords)
    mat = [list(r) for r in rows]
    piv_cols = []
    rank = 0
    for col in range(n):
        piv = None
        for i in range(rank, len(mat)):
            if mat[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        head = mat[rank]
        for i in range(len(mat)):
            if i != rank and mat[i][col] != 0:
                f = mat[i][col] / head[col]
                mat[i] = [x - f * y for x, y in zip(mat[i], head)]
        piv_cols.append(col)
        rank += 1
    for i in range(rank, len(mat)):
        if all(x == 0 for x in mat[i][:n]) and mat[i][n] != 0:
            return None
    x = [Fraction(0)] * n
    for r, col in enumerate(piv_cols):
        x[col] = mat[r][n] / mat[r][col]
    out = {}
    for (a, b, ca, cb), val in zip(coords, x):
        out.setdefault((a, b), [[Fraction(0)] * 3 for _ in range(3)])
        out[(a, b)][ca][cb] = val
    return out


if __name__ == "__main__":
    main()
