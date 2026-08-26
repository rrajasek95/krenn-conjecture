#!/usr/bin/env python3
"""A5 / claim 5, with the APOLARITY pairing (my first pass wrongly used the
plain coefficient dot product; the two differ by the multinomial factors e!).

    <phi, F> := phi(d/dK) F = sum_e e! phi_e F_e ,
so phi is apolar to L_h iff the vector (e! phi_e) annihilates L_h.
"""
from __future__ import annotations
import json, random, sys
from fractions import Fraction
from itertools import combinations, permutations
from math import factorial
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
res = {}
rng = random.Random(13)


def efact(e):
    f = 1
    for x in e:
        f *= factorial(x)
    return f


def to_apolar(psi, h):
    """dot-perp vector -> apolar form coefficients (rational)."""
    return [Fraction(psi[i], efact(A.deg_monoms(h)[i])) for i in range(len(psi))]


def order_along(phi, h, R, Amat):
    """coefficients of t^0..t^h of phi(R + tA), phi given by its coefficients."""
    out = [Fraction(0)] * (h + 1)
    for idx, c in enumerate(phi):
        if not c:
            continue
        e = A.deg_monoms(h)[idx]
        poly = [Fraction(1)]
        for v in range(9):
            for _ in range(e[v]):
                r, a = R[v // 3][v % 3], Amat[v // 3][v % 3]
                new = [Fraction(0)] * (len(poly) + 1)
                for d, cc in enumerate(poly):
                    new[d] += cc * r
                    new[d + 1] += cc * a
                poly = new
        for j, cc in enumerate(poly):
            out[j] += c * cc
    return out


# sanity: phi(d/dK) (u^T K v)^k = k! phi(uv^T)
for k in (2, 3):
    for _ in range(4):
        u = [rng.randint(-4, 4) for _ in range(3)]
        v = [rng.randint(-4, 4) for _ in range(3)]
        F = A.poly_vec(A.ppow(A.var_poly([u[i] * v[j] for i in range(3)
                                          for j in range(3)]), k), k)
        phi = [Fraction(rng.randint(-5, 5)) for _ in A.deg_monoms(k)]
        lhs = sum(Fraction(efact(A.deg_monoms(k)[i])) * phi[i] * F[i]
                  for i in range(len(F)))
        R = [[u[i] * v[j] for j in range(3)] for i in range(3)]


        # evaluate phi at R directly
        val = Fraction(0)
        for i, c in enumerate(phi):
            if not c:
                continue
            e = A.deg_monoms(k)[i]
            t = Fraction(1)
            for w in range(9):
                if e[w]:
                    t *= Fraction(R[w // 3][w % 3]) ** e[w]
            val += c * t
        assert lhs == factorial(k) * val, ("pairing identity failed", k)
print("claim5: pairing identity phi(d/dK)(u^T K v)^k = k! phi(uv^T) verified", flush=True)
res["pairing_identity"] = True

for h in (2, 3, 4):
    Amat = [[rng.randint(-5, 5) for _ in range(3)] for _ in range(3)]
    svec = [Amat[i][j] for i in range(3) for j in range(3)]
    Lr = A.L_rows(h, svec, rng)
    Psi = A.perp_basis(Lr, len(A.deg_monoms(h)))
    bad_fwd = 0
    for psi in Psi[:15]:
        phi = to_apolar(psi, h)
        for _ in range(8):
            u = [rng.randint(-4, 4) for _ in range(3)]
            v = [rng.randint(-4, 4) for _ in range(3)]
            R = [[u[i] * v[j] for j in range(3)] for i in range(3)]
            co = order_along(phi, h, R, Amat)
            if any(co[j] != 0 for j in range(h - 1)):
                bad_fwd += 1
    # converse: solution space of the order condition, with enough rank-ones
    ncols = len(A.deg_monoms(h))
    eqs, prev, stable = [], None, 0
    basisvecs = []
    for idx in range(ncols):
        e = [Fraction(0)] * ncols
        e[idx] = Fraction(1)
        basisvecs.append(e)
    for trial in range(700):
        u = [rng.randint(-7, 7) for _ in range(3)]
        v = [rng.randint(-7, 7) for _ in range(3)]
        R = [[u[i] * v[j] for j in range(3)] for i in range(3)]
        cols = [order_along(bv, h, R, Amat) for bv in basisvecs]
        for j in range(h - 1):
            eqs.append([int(cols[idx][j]) for idx in range(ncols)])
        if trial % 50 == 49:
            r = len(A.int_echelon(eqs)[1])
            if r == prev:
                stable += 1
                if stable >= 2:
                    break
            else:
                stable = 0
            prev = r
    sol = A.perp_basis(eqs, ncols)          # apolar coefficient vectors
    # compare with the rescaled perp
    tgt = []
    for s in sol:
        w = [Fraction(s[i]) * efact(A.deg_monoms(h)[i]) for i in range(ncols)]
        den = 1
        for x in w:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
        tgt.append([int(x * den) for x in w])
    ech, piv = A.int_echelon(Psi)
    same = (len(sol) == len(Psi)) and all(A.in_span_exact(ech, piv, t) for t in tgt)
    print(f"claim5 h={h}: dim perp(L_h) = {len(Psi)}; forward violations = {bad_fwd}; "
          f"order-condition space dim = {len(sol)}; spaces equal = {same}", flush=True)
    res[f"h{h}"] = {"dim_perp": len(Psi), "forward_violations": bad_fwd,
                    "order_dim": len(sol), "equal": bool(same)}
    # CONTROL: a random form must NOT satisfy the order condition
    junk = [Fraction(rng.randint(-5, 5)) for _ in range(ncols)]
    u = [1, 2, 3]
    v = [2, -1, 1]
    R = [[u[i] * v[j] for j in range(3)] for i in range(3)]
    co = order_along(junk, h, R, Amat)
    res[f"h{h}"]["control_random_form_fails_order"] = any(co[j] != 0 for j in range(h - 1))

# Sigma_k^perp (apolar) = degree-k part of the Segre ideal
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
for k in (2, 3, 4):
    ideal_rows = []
    for m in minors:
        for extra in A.deg_monoms(k - 2):
            ideal_rows.append(A.poly_vec(A.pmul(m, {extra: 1}), k))
    Psi = A.perp_basis(A.sigma_rows_powers(k, rng), len(A.deg_monoms(k)))
    apol = []
    for s in Psi:
        w = [Fraction(s[i], efact(A.deg_monoms(k)[i])) for i in range(len(s))]
        den = 1
        for x in w:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
        apol.append([int(x * den) for x in w])
    ech, piv = A.int_echelon(ideal_rows)
    same = (len(A.int_echelon(ideal_rows)[1]) == len(apol)) and all(
        A.in_span_exact(ech, piv, a) for a in apol)
    print(f"claim5 Sigma_{k}: dim apolar perp = {len(apol)}; dim degree-{k} Segre "
          f"ideal = {len(piv)}; equal = {same}", flush=True)
    res[f"segre_k{k}"] = {"dim_perp": len(apol), "dim_ideal": len(piv), "equal": bool(same)}

json.dump(res, open(OUT + "results_t5_apolarity.json", "w"), indent=1)
print("DONE")
