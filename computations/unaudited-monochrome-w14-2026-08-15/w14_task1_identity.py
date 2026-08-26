#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 1(a): the monochrome-transfer IDENTITY.

Everything here is exact (Python ints / Fractions).

Identities established/verified (h = 3 and h = 4):

 (I0) cross-check of W14's own E_w expansion against W13's two independent
      expansions (direct and graded).
 (I1) HAFNIAN CLOSED FORM.  For a subset W' of U with |W'| = 2k,
         Haf^{(u,v)}(W') := sum_{M' perfect matching of W'} prod_{f in M'} R_f(u(x)v)
                          = k! * sum_{|S| = k} prod_{a in S}<u,P_a> prod_{b in W'\\S}<v,Q_b>.
 (I2) LEVEL LAW.   z_{w,k}(u,v) = (1/k!) G_{h-k}^{(u,v)}(w), where
         G_j^{(u,v)}(w) = sum_{J partial matching, |J| = j} x_J * Haf^{(u,v)}(U \\ V(J)).
      (z_{w,k} is W13's graded datum, read as a bidegree-(k,k) form.)
 (I3) RANK-ONE EXPANSION.  E_w(u (x) v) = sum_{j=0}^{h-2} alpha^j G_j^{(u,v)}(w),
      alpha = u^T A_pq v.
 (I4) SLICE LAW.  the colour-c slice error = E_w(E_cc) = sum_j s_c^j G_j^{(c)}(w),
      s_c = A_pq(c,c),  G_j^{(c)} = G_j^{(delta_c, delta_c)}.
 (I5) DIRECTNESS of L_h(A) = (+)_k s^{h-k} iota_k(Sigma_k) at full-rank A
      (and its FAILURE at rank <= 2).
 (I6) TRANSFER PROJECTION.  if s^a kappa_c^{h-a} = sum_w lambda_w E_w then
         sum_w lambda_w G_j^{(c)}(w) = delta_{ja}     (j = 0..h-2),
      and more generally sum_w lambda_w G_j^{(u,v)}(w) = delta_{ja} (u_c v_c)^{h-a}.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product as iproduct

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)
sys.path.insert(0, HERE + "/../unaudited-induction-w13-2026-08-15")

import w14_core as C
from w14_core import (COLORS, NCAP, delta, det3, error_poly, graded_error,
                      G_level, hafnian_slice, hafnian_slice_closed, in_span,
                      L_rows, mono_name, mono_poly, poly_eval, poly_row,
                      random_source, rank3, require, rref_exact, sigma_basis,
                      sites, slice_error, solve_combination, s_vector, z_eval)

RESULTS = {}


def kron(u, v):
    """The 9-vector of the rank-one cap K = u (x) v."""
    return [u[i] * v[j] for i in COLORS for j in COLORS]


# ------------------------------------------------------------------ (I0)

def check_I0(h, rng, ntrials=2, nwords=6):
    """W14's E_w vs W13's error_poly_direct and graded_to_poly."""
    import w13_core as W13
    ok = 0
    total = 0
    for _ in range(ntrials):
        src = random_source(h, rng)
        words = [tuple(rng.randrange(3) for _ in range(2 * h))
                 for _ in range(nwords)]
        for w in words:
            mine = error_poly(src, h, w)
            theirs = W13.error_poly_direct(src, h, w)
            theirs_graded = W13.graded_to_poly(src, h, W13.graded_error(src, h, w))
            mine_graded = C.graded_to_poly(src, h, graded_error(src, h, w))
            total += 1
            require(mine == theirs, ("I0 direct mismatch", h, w))
            require(mine == theirs_graded, ("I0 graded mismatch", h, w))
            require(mine == mine_graded, ("I0 own-graded mismatch", h, w))
            ok += 1
    print(f"  (I0) h={h}: {ok}/{total} words agree across 4 independent "
          f"expansions (W14 direct/graded, W13 direct/graded)")
    return {"checked": total, "agree": ok}


# ------------------------------------------------------------------ (I1)-(I4)

def check_identities(h, rng, ntrials=3, nwords=8, nuv=3):
    P, Q, U = sites(h)
    counts = {"I1": 0, "I2": 0, "I3": 0, "I4": 0}
    for _ in range(ntrials):
        src = random_source(h, rng)
        A = src[(0, 1)]
        words = [tuple(rng.randrange(3) for _ in range(2 * h))
                 for _ in range(nwords)]
        for w in words:
            E = error_poly(src, h, w)
            z = graded_error(src, h, w)
            uvs = [([rng.randint(-3, 3) for _ in COLORS],
                    [rng.randint(-3, 3) for _ in COLORS]) for _ in range(nuv)]
            uvs += [(delta(c), delta(c)) for c in COLORS]
            for u, v in uvs:
                # (I1) hafnian closed form on every even subset of U
                for size in range(0, 2 * h + 1, 2):
                    for W_ in combinations(U, size):
                        a1 = hafnian_slice(src, h, w, u, v, W_)
                        a2 = hafnian_slice_closed(src, h, w, u, v, W_)
                        require(a1 == a2, ("I1", h, w, W_))
                        counts["I1"] += 1
                # (I2) level law
                fact = 1
                for k in range(2, h + 1):
                    fact = 1
                    for t in range(2, k + 1):
                        fact *= t
                    lhs = z_eval(z[k], u, v) * fact
                    rhs = G_level(src, h, w, u, v, h - k)
                    require(lhs == rhs, ("I2", h, w, k, u, v, lhs, rhs))
                    counts["I2"] += 1
                # (I3) rank-one expansion
                lhs = poly_eval(E, kron(u, v))
                alpha = sum(u[i] * v[j] * A[i][j] for i in COLORS for j in COLORS)
                rhs = sum(alpha ** j * G_level(src, h, w, u, v, j)
                          for j in range(h - 1))
                require(lhs == rhs, ("I3", h, w, u, v))
                require(lhs == slice_error(src, h, w, u, v), ("I3b", h, w))
                counts["I3"] += 1
            # (I4) colour slice law
            for c in COLORS:
                Ecc = [1 if n == 3 * c + c else 0 for n in range(NCAP)]
                lhs = poly_eval(E, Ecc)
                sc = A[c][c]
                rhs = sum(sc ** j * G_level(src, h, w, delta(c), delta(c), j)
                          for j in range(h - 1))
                require(lhs == rhs, ("I4", h, w, c))
                counts["I4"] += 1
    print(f"  (I1) h={h}: {counts['I1']} hafnian closed-form checks PASS")
    print(f"  (I2) h={h}: {counts['I2']} level-law checks PASS "
          f"(z_(w,k)(u,v) = G_(h-k)/k!)")
    print(f"  (I3) h={h}: {counts['I3']} rank-one expansion checks PASS")
    print(f"  (I4) h={h}: {counts['I4']} colour-slice-law checks PASS")
    return counts


# ------------------------------------------------------------------ (I5)

def dim_L_exact(h, A):
    rows = L_rows(h, [A[i][j] for i in COLORS for j in COLORS])
    _, piv = rref_exact(rows)
    return len(piv), len(rows)


def check_I5(h, rng):
    """Directness of the graded law: dim L_h(A) = sum_k dim Sigma_k iff rank 3."""
    def rank_r(r):
        while True:
            M = [[0] * 3 for _ in range(3)]
            for _ in range(r):
                u = [rng.randint(-5, 5) for _ in COLORS]
                v = [rng.randint(-5, 5) for _ in COLORS]
                for i in COLORS:
                    for j in COLORS:
                        M[i][j] += u[i] * v[j]
            if rank3(M) == r:
                return M
    expect = sum(len(sigma_basis(k)) for k in range(2, h + 1))
    out = []
    tests = [("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
             ("generic rank 3", rank_r(3)),
             ("permutation", [[0, 1, 0], [0, 0, 1], [1, 0, 0]]),
             ("diag(1,2,-3)", [[1, 0, 0], [0, 2, 0], [0, 0, -3]]),
             ("rank 3, A_00 = 0", None),
             ("rank 2", rank_r(2)),
             ("rank 1", rank_r(1))]
    while tests[4][1] is None:
        M = rank_r(3)
        M[0][0] = 0
        if rank3(M) == 3:
            tests[4] = ("rank 3, A_00 = 0", M)
    for label, A in tests:
        d, nrows = dim_L_exact(h, A)
        direct = (d == expect)
        print(f"  (I5) h={h} {label:22s} rank {rank3(A)}: dim L_h = {d} "
              f"(sum dim Sigma_k = {expect}) -> "
              f"{'DIRECT' if direct else 'NOT direct'}")
        out.append({"label": label, "A": A, "rank": rank3(A), "dim_L": d,
                    "expected_if_direct": expect, "direct": direct})
    return out


# ------------------------------------------------------------------ (I6)

def check_I6(h, rng, ntrials=2, nuv=3):
    """The transfer projection on sources where the monomial IS in the span."""
    P, Q, U = sites(h)
    out = []
    for _ in range(ntrials):
        src = random_source(h, rng)
        A = src[(0, 1)]
        if rank3(A) != 3:
            continue
        words = (list(iproduct(range(3), repeat=2 * h)) if h == 3 else
                 [tuple(rng.randrange(3) for _ in range(2 * h))
                  for _ in range(420)] + [(c,) * (2 * h) for c in COLORS])
        rows = [poly_row(error_poly(src, h, w), h) for w in words]
        basis, piv = rref_exact(rows)
        sv = s_vector(src)
        for c in COLORS:
            for a in range(0, h - 1):
                b = tuple((h - a) if t == c else 0 for t in COLORS)
                target = poly_row(mono_poly(a, b, sv), h)
                if not in_span(basis, piv, target):
                    out.append({"h": h, "monomial": mono_name(a, b),
                                "in_span": False})
                    continue
                lam = solve_combination(rows, target)
                require(lam is not None, ("I6 solve failed", h, a, c))
                # exact re-check of the combination
                chk = [sum(lam[i] * rows[i][n] for i in range(len(rows)))
                       for n in range(len(target))]
                require(chk == [Fraction(x) for x in target],
                        ("I6 combination wrong", h, a, c))
                rec = {"h": h, "monomial": mono_name(a, b), "in_span": True,
                       "levels_ok": True, "uv_ok": True}
                for j in range(h - 1):
                    val = sum(lam[i] * G_level(src, h, words[i], delta(c),
                                               delta(c), j)
                              for i in range(len(words)))
                    want = Fraction(1 if j == a else 0)
                    if val != want:
                        rec["levels_ok"] = False
                        rec[f"G_{j}"] = str(val)
                # general (u,v) version
                for _ in range(nuv):
                    u = [rng.randint(-3, 3) for _ in COLORS]
                    v = [rng.randint(-3, 3) for _ in COLORS]
                    for j in range(h - 1):
                        val = sum(lam[i] * G_level(src, h, words[i], u, v, j)
                                  for i in range(len(words)))
                        want = (Fraction(u[c] * v[c]) ** (h - a)
                                if j == a else Fraction(0))
                        if val != want:
                            rec["uv_ok"] = False
                out.append(rec)
                print(f"  (I6) h={h} {rec['monomial']:8s} in span: "
                      f"level projection {'OK' if rec['levels_ok'] else 'FAIL'}"
                      f", general (u,v) projection "
                      f"{'OK' if rec['uv_ok'] else 'FAIL'}")
    return out


def main():
    t0 = time.time()
    rng = random.Random(140714)
    print("== W14 Task 1(a): the transfer identity, exact over Q ==")
    for h in (3, 4):
        print(f"\n-- h = {h} (N = {2 * h + 2}) --")
        RESULTS[f"I0_h{h}"] = check_I0(h, rng, ntrials=2, nwords=(6 if h == 3 else 3))
        RESULTS[f"ident_h{h}"] = check_identities(
            h, rng, ntrials=(3 if h == 3 else 1),
            nwords=(6 if h == 3 else 2), nuv=(3 if h == 3 else 2))
    print()
    RESULTS["I5_h3"] = check_I5(3, rng)
    print()
    RESULTS["I6_h3"] = check_I6(3, rng, ntrials=1)
    with open(HERE + "/results_task1_identity.json", "w") as fh:
        json.dump(RESULTS, fh, indent=1, default=str)
    print(f"\nwrote results_task1_identity.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
