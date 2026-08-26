#!/usr/bin/env python3
"""A5 / claims 5 and 7.

W13.5 (apolarity): phi _|_ L_h(A) iff t -> phi(R + tA) vanishes to order
>= h-1 at t = 0 for every rank-one R; Sigma_k^perp = degree-k part of the
Segre ideal; det Y is the unique A-independent element at h=3.

W13.7: the kappa_c^h coefficient of E_w equals E_w(E_cc), which equals the
level-h cap error (eq. (4)) of the scalar colour-c slice data; for the
monochrome word c^{2h} that is exactly W5's colour-c slice error.
"""
from __future__ import annotations
import json, random, sys
from fractions import Fraction
from itertools import combinations, permutations, product
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
res = {}
rng = random.Random(24601)


# --------------------------------------------------------------- claim 5
def phi_eval(phi_vec, h, M):
    """phi(M) for M a 3x3 matrix; phi given in my degree-h monomial basis."""
    tot = 0
    for idx, c in enumerate(phi_vec):
        if not c:
            continue
        e = A.deg_monoms(h)[idx]
        term = c
        for v in range(9):
            if e[v]:
                term *= M[v // 3][v % 3] ** e[v]
        tot += term
    return tot


def order_along(phi_vec, h, R, Amat):
    """coefficients of t^0..t^h in phi(R + tA)."""
    coeffs = []
    for j in range(h + 1):
        # coefficient of t^j: sum over monomials, expand (R+tA) entrywise
        tot = 0
        for idx, c in enumerate(phi_vec):
            if not c:
                continue
            e = A.deg_monoms(h)[idx]
            # product over variables of (R_v + t A_v)^{e_v}: collect t^j
            poly = [1]
            for v in range(9):
                for _ in range(e[v]):
                    r, a = R[v // 3][v % 3], Amat[v // 3][v % 3]
                    new = [0] * (len(poly) + 1)
                    for d, cc in enumerate(poly):
                        new[d] += cc * r
                        new[d + 1] += cc * a
                    poly = new
            if j < len(poly):
                tot += c * poly[j]
        coeffs.append(tot)
    return coeffs


res["apolarity"] = []
for h in (2, 3, 4):
    Amat = [[rng.randint(-5, 5) for _ in range(3)] for _ in range(3)]
    svec = [Amat[i][j] for i in range(3) for j in range(3)]
    Lr = A.L_rows(h, svec, rng)
    Phi = A.perp_basis(Lr, len(A.deg_monoms(h)))
    # forward direction: every perp element vanishes to order >= h-1 along A
    bad_fwd = 0
    for phi in Phi[:12]:
        for _ in range(6):
            u = [rng.randint(-4, 4) for _ in range(3)]
            v = [rng.randint(-4, 4) for _ in range(3)]
            R = [[u[i] * v[j] for j in range(3)] for i in range(3)]
            co = order_along(phi, h, R, Amat)
            if any(co[j] != 0 for j in range(h - 1)):
                bad_fwd += 1
    # converse: the linear system "order >= h-1 along A at every rank-one"
    # has solution space of exactly dim(perp).  Build the equations by
    # expanding phi(uv^T + tA) symbolically in u, v (random sampling of
    # (u,v) suffices to cut the space; verify the dimension stabilises).
    ncols = len(A.deg_monoms(h))
    eqs = []
    for _ in range(180):
        u = [rng.randint(-6, 6) for _ in range(3)]
        v = [rng.randint(-6, 6) for _ in range(3)]
        R = [[u[i] * v[j] for j in range(3)] for i in range(3)]
        for j in range(h - 1):
            row = []
            for idx in range(ncols):
                e = [0] * ncols
                e[idx] = 1
                row.append(order_along(e, h, R, Amat)[j])
            eqs.append(row)
    sol = A.perp_basis(eqs, ncols)
    same = (len(sol) == len(Phi))
    if same:
        ech, piv = A.int_echelon(Phi)
        same = all(A.in_span_exact(ech, piv, s) for s in sol)
    print(f"claim5 h={h}: dim perp(L_h) = {len(Phi)}; forward violations = {bad_fwd}; "
          f"order-condition solution space dim = {len(sol)}; spaces equal = {same}",
          flush=True)
    res["apolarity"].append({"h": h, "dim_perp": len(Phi), "forward_violations": bad_fwd,
                             "order_space_dim": len(sol), "equal": bool(same)})

# Sigma_k^perp = degree-k part of the Segre ideal (k = 2, 3)
minors = []
for i1, i2 in combinations(range(3), 2):
    for j1, j2 in combinations(range(3), 2):
        f = {}
        e = [0] * 9
        e[3 * i1 + j1] += 1
        e[3 * i2 + j2] += 1
        f[tuple(e)] = 1
        e = [0] * 9
        e[3 * i1 + j2] += 1
        e[3 * i2 + j1] += 1
        f[tuple(e)] = f.get(tuple(e), 0) - 1
        minors.append(f)
for k in (2, 3):
    ideal_rows = []
    for m in minors:
        for extra in (A.deg_monoms(k - 2) if k > 2 else [tuple([0] * 9)]):
            ideal_rows.append(A.poly_vec(A.pmul(m, {extra: 1}), k))
    dim_ideal = len(A.int_echelon(ideal_rows)[1])
    sig = A.int_echelon(A.sigma_rows_powers(k, rng))
    perp_sig = A.perp_basis(A.sigma_rows_powers(k, rng), len(A.deg_monoms(k)))
    ech, piv = A.int_echelon(ideal_rows)
    same = (dim_ideal == len(perp_sig)) and all(
        A.in_span_exact(ech, piv, p) for p in perp_sig)
    print(f"claim5 Sigma_{k}^perp: dim = {len(perp_sig)}; degree-{k} part of the "
          f"Segre ideal: dim = {dim_ideal}; equal = {same}", flush=True)
    res[f"segre_ideal_k{k}"] = {"dim_perp": len(perp_sig), "dim_ideal": dim_ideal,
                                "equal": bool(same)}

# det Y is the unique A-independent element of L_3(A)^perp
det_vec = [0] * len(A.deg_monoms(3))
for pi in permutations(range(3)):
    inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    e = [0] * 9
    for i in range(3):
        e[3 * i + pi[i]] += 1
    det_vec[A.monom_index(3)[tuple(e)]] += (-1) ** inv
inter = None
for t in range(6):
    Amat = [[rng.randint(-6, 6) for _ in range(3)] for _ in range(3)]
    svec = [Amat[i][j] for i in range(3) for j in range(3)]
    P = A.perp_basis(A.L_rows(3, svec, rng), len(A.deg_monoms(3)))
    if inter is None:
        inter = P
    else:
        # intersection of two row spaces via perp of (perp1 + perp2)
        u = A.perp_basis(inter, len(A.deg_monoms(3)))
        w = A.perp_basis(P, len(A.deg_monoms(3)))
        inter = A.perp_basis(u + w, len(A.deg_monoms(3)))
ech, piv = A.int_echelon(inter)
det_in = A.in_span_exact(ech, piv, det_vec)
print(f"claim5: dim of the A-independent part of L_3^perp over 6 random A = "
      f"{len(inter)}; contains det = {det_in}", flush=True)
res["det_unique"] = {"dim": len(inter), "contains_det": bool(det_in)}
# Hilbert function of the apolar algebra of det_3
hf = []
for d in range(5):
    rows = []
    for e in A.deg_monoms(d):
        # apply the differential operator to det
        val = [0] * len(A.deg_monoms(3 - d)) if d <= 3 else [0]
        if d <= 3:
            for idx, c in enumerate(det_vec):
                if not c:
                    continue
                m = A.deg_monoms(3)[idx]
                if all(m[v] >= e[v] for v in range(9)):
                    coef = c
                    for v in range(9):
                        for t in range(e[v]):
                            coef *= (m[v] - t)
                    rest = tuple(m[v] - e[v] for v in range(9))
                    val[A.monom_index(3 - d)[rest]] += coef
        rows.append(val)
    hf.append(len(A.int_echelon(rows)[1]) if any(any(r) for r in rows) else 0)
print("claim5: Hilbert function of the apolar algebra of det_3 =", hf, flush=True)
res["hilbert_det3"] = hf


# --------------------------------------------------------------- claim 7
def slice_error_scalar(s, rvals, xvals, U, h):
    """eq. (4) for scalar data: r_e, x_e on the pairs of U."""
    rw = {frozenset(e): {(0,) * 9: Fraction(rvals[e])} for e in rvals if rvals[e]}
    xw = {frozenset(e): {(0,) * 9: Fraction(xvals[e])} for e in xvals if xvals[e]}
    from math import factorial
    full = frozenset(U)
    tot = Fraction(0)
    rp = {0: {frozenset(): dict(A.ONE)}}
    xp = {0: {frozenset(): dict(A.ONE)}}
    for k in range(1, h + 1):
        rp[k] = A.sf_mul(rp[k - 1], rw) if rw else {}
        xp[k] = A.sf_mul(xp[k - 1], xw) if xw else {}
    for k in range(2, h + 1):
        term = A.sf_mul(rp[k], xp[h - k])
        f = term.get(full)
        if not f:
            continue
        val = f[(0,) * 9] / (factorial(k) * factorial(h - k))
        tot += Fraction(s) ** (h - k) * val
    return tot


res["w137"] = []
for h in (3, 4):
    for trial in range(3):
        src = A.random_source(h, rng)
        p, q, U = A.sites(h)
        slot = {u: n for n, u in enumerate(U)}
        for c in A.C3:
            ok_all, ok_mono = True, None
            for wi in range(30):
                w = (tuple([c] * (2 * h)) if wi == 0
                     else tuple(rng.choice(A.C3) for _ in range(2 * h)))
                E = A.cap_error_raw(src, h, w)
                e = [0] * 9
                e[3 * c + c] = h
                coeff = E.get(tuple(e), 0)
                # slice data at this word, read in colour-c row of the p/q blocks
                s = src[(p, q)][c][c]
                rvals, xvals = {}, {}
                for a, b in combinations(U, 2):
                    ca, cb = w[slot[a]], w[slot[b]]
                    rvals[(a, b)] = (A.blk(src, p, a, c, ca) * A.blk(src, q, b, c, cb)
                                     + A.blk(src, p, b, c, cb) * A.blk(src, q, a, c, ca))
                    xvals[(a, b)] = src[(a, b)][ca][cb]
                pred = slice_error_scalar(s, rvals, xvals, U, h)
                if pred != coeff:
                    ok_all = False
                if wi == 0:
                    ok_mono = (pred == coeff)
            print(f"claim7 h={h} trial={trial} colour={c}: kappa_c^h coefficient "
                  f"== scalar slice-error formula on 30 words: {ok_all} "
                  f"(monochrome word: {ok_mono})", flush=True)
            res["w137"].append({"h": h, "trial": trial, "c": c,
                                "all_words": ok_all, "monochrome": ok_mono})

json.dump(res, open(OUT + "results_t57.json", "w"), indent=1)
print("DONE")
