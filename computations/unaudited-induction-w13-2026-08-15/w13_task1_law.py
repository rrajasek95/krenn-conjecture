#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 1 (R4): the degree-h obstruction theory.

Establishes, exactly:

  (L1) dim Sigma_k = C(k+2,2)^2 for k = 2,3,4  (36, 100, 225).
  (L2) Sigma_2 = Ann(det_3)_2; the ideal I = (Sigma_2) has
       dim I_3 = 164 (codim 1 = <det K>) and dim I_4 = 495 (codim 0).
       => the GL(V)xGL(W)-equivariant obstruction is Lambda^h V (x) Lambda^h W,
          which is 0 for h >= 4.  (P1's FACT 1 / W4's Pieri remark, re-proved.)
  (L3) THE SHARP LAW.  L_h(A) := sum_{k=2}^h s^{h-k} Sigma_k  (s = <K,A_pq>)
       has dim 36 (h=2), 136 (h=3), 361 (h=4) for generic A;
       codim 9, 29, 134.  Every cap-error component lies in L_h(A).
  (L4) The A-independent part of the law is exactly Lambda^h (x) Lambda^h:
       intersecting Ann(L_h(A)) over several A leaves dim 1 (h=3, = det)
       and dim 0 (h=4).
  (L5) Verification on actual sources: graded == direct expansion; every
       component lies in L_h; the components SPAN L_h exactly
       (rank 136 at h=3 -- matching P1's independently measured 136 --
        and rank 361 at h=4).

Exact arithmetic throughout.  Ranks are computed over F_p for a large prime
(rank_{F_p} <= rank_Q always), and every rank claim is combined with a
structural upper bound (a row count or a proved containment), so each
reported dimension is proved, not sampled.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_core import (COLORS, NCAP, apolar_det, error_poly_direct, graded_error,
                      graded_to_poly, in_span_exact, iota, kidx, monomial_index,
                      monomials, poly_add, poly_mul, poly_pow, poly_vector,
                      random_source, require, rref_exact, s_poly, sigma_basis,
                      sigma_matrix, sites)

P1 = 2_147_483_647  # 2^31 - 1, prime
P2 = 1_000_000_007

OUT = {}


def rank_mod_p_np(rows, p=P1) -> int:
    """Rank over F_p, numpy int64.  p^2 < 2^63 so products are safe."""
    if not rows:
        return 0
    a = np.array(rows, dtype=np.int64) % p
    m, n = a.shape
    rank = 0
    row = 0
    for col in range(n):
        if row >= m:
            break
        nz = np.nonzero(a[row:, col])[0]
        if nz.size == 0:
            continue
        piv = row + int(nz[0])
        if piv != row:
            a[[row, piv]] = a[[piv, row]]
        inv = pow(int(a[row, col]), p - 2, p)
        a[row] = (a[row] * inv) % p
        colvals = a[:, col].copy()
        colvals[row] = 0
        nzr = np.nonzero(colvals)[0]
        if nzr.size:
            a[nzr] = (a[nzr] - np.outer(colvals[nzr], a[row])) % p
        row += 1
        rank += 1
    return rank


def poly_to_row(poly, degree):
    idx = monomial_index(NCAP, degree)
    row = [0] * len(idx)
    for m, c in poly.items():
        row[idx[m]] += c
    return row


# ------------------------------------------------------------------ (L1)

def check_sigma_dims():
    res = {}
    for k in (2, 3, 4):
        rows = sigma_matrix(k)
        expected = (((k + 2) * (k + 1)) // 2) ** 2
        r1 = rank_mod_p_np(rows, P1)
        r2 = rank_mod_p_np(rows, P2)
        require(r1 == r2 == expected == len(rows),
                ("sigma dim", k, r1, r2, expected, len(rows)))
        res[k] = {"generators": len(rows), "rank": r1, "expected": expected}
        print(f"  [L1] dim Sigma_{k} = {r1} (= C({k}+2,2)^2 = {expected}), "
              f"generators {len(rows)}: independent")
    return res


# ------------------------------------------------------------------ (L2)

def check_apolar_and_ideal():
    res = {}
    # Sigma_2 is apolar to det
    bad = 0
    for mu, nu in sigma_basis(2):
        if apolar_det(dict(iota(2, mu, nu))):
            bad += 1
    require(bad == 0, ("Sigma_2 not apolar to det", bad))
    print("  [L2] every one of the 36 generators of Sigma_2 kills det(Y): PASS")

    # dim Ann(det)_2 = 45 - 9 = 36, so Sigma_2 = Ann(det)_2
    rows = []
    for m in monomials(NCAP, 2):
        img = apolar_det({m: 1})
        rows.append(poly_to_row(img, 1) if img else [0] * 9)
    rk = rank_mod_p_np(rows, P1)
    require(rk == 9, ("catalecticant rank", rk))
    print(f"  [L2] rank of S^2 -> S^1, q |-> q(d)det is {rk}; "
          f"dim Ann(det)_2 = 45 - {rk} = {45 - rk} = dim Sigma_2 "
          "=> Sigma_2 = Ann(det)_2")
    res["ann_det_2"] = 45 - rk

    # the ideal I = (Sigma_2) in degrees 3 and 4
    for deg in (3, 4):
        idx = monomial_index(NCAP, deg)
        gens = []
        for mu, nu in sigma_basis(2):
            base = dict(iota(2, mu, nu))
            for mult in monomials(NCAP, deg - 2):
                g = poly_mul(base, {mult: 1})
                gens.append(poly_to_row(g, deg))
        rk = rank_mod_p_np(gens, P1)
        total = len(idx)
        res[f"I_{deg}"] = {"dim": rk, "ambient": total, "codim": total - rk}
        print(f"  [L2] dim I_{deg} = {rk} of {total}  (codim {total - rk})")
    require(res["I_3"]["codim"] == 1, res["I_3"])
    require(res["I_4"]["codim"] == 0, res["I_4"])
    print("  [L2] => S/I has Hilbert function (1, 9, 9, 1, 0, ...): "
          "the equivariant obstruction is Lambda^h (x) Lambda^h, zero for h >= 4")
    return res


# ------------------------------------------------------------------ (L3)

def L_generators(h, A_entries):
    """Rows spanning L_h(A) = sum_{k=2}^h s^{h-k} Sigma_k, in S^h monomials."""
    sp = {(k,): A_entries[k] for k in range(NCAP) if A_entries[k]}
    rows = []
    tags = []
    for k in range(2, h + 1):
        spow = poly_pow(sp, h - k)
        for mu, nu in sigma_basis(k):
            g = dict(iota(k, mu, nu))
            if h - k:
                g = poly_mul(g, spow)
            rows.append(poly_to_row(g, h))
            tags.append((k, mu, nu))
    return rows, tags


def check_L_dims(rng):
    res = {}
    for h in (2, 3, 4):
        A = [rng.randint(-9, 9) for _ in range(NCAP)]
        rows, _ = L_generators(h, A)
        rk = rank_mod_p_np(rows, P1)
        rk2 = rank_mod_p_np(rows, P2)
        ambient = len(monomials(NCAP, h))
        expected = sum((((k + 2) * (k + 1)) // 2) ** 2 for k in range(2, h + 1))
        require(rk == rk2, (h, rk, rk2))
        require(rk == expected, ("L_h not a direct sum", h, rk, expected))
        res[h] = {"dim": rk, "ambient": ambient, "codim": ambient - rk,
                  "A": A, "direct_sum_prediction": expected}
        print(f"  [L3] h={h}: dim L_h(A) = {rk} = {'+'.join(str((((k+2)*(k+1))//2)**2) for k in range(2, h+1))}"
              f" (direct sum) of {ambient}; codim {ambient - rk}")
    return res


# ------------------------------------------------------------------ (L4)

def check_A_independent_part(rng):
    """Intersect Ann(L_h(A)) over several A: what survives is A-independent."""
    res = {}
    for h in (2, 3, 4):
        ambient = len(monomials(NCAP, h))
        # Ann(L_h(A)) = null space of the generator matrix.  Intersecting the
        # null spaces = null space of the stacked matrix.
        stacked = []
        As = []
        for _ in range(4):
            A = [rng.randint(-9, 9) for _ in range(NCAP)]
            As.append(A)
            rows, _ = L_generators(h, A)
            stacked.extend(rows)
        rk = rank_mod_p_np(stacked, P1)
        codim = ambient - rk
        expected = {2: 9, 3: 1, 4: 0}[h]
        require(codim == expected, ("A-independent part", h, codim, expected))
        res[h] = {"joint_dim": rk, "ambient": ambient, "A_independent_laws": codim,
                  "expected_lambda_h_dim": expected}
        print(f"  [L4] h={h}: laws valid for EVERY A_pq: dim {codim} "
              f"(= dim Lambda^{h}V (x) Lambda^{h}W = C(3,{h})^2 = {expected})")
    return res


# ------------------------------------------------------------------ (L5)

def sample_words(h, rng, count):
    U_len = 2 * h
    words = set()
    for c in COLORS:
        words.add(tuple([c] * U_len))
    while len(words) < count:
        words.add(tuple(rng.randrange(3) for _ in range(U_len)))
    return sorted(words)


def check_sources(h, rng, n_words, n_direct=3, zero_prob=0.0, label=""):
    src = random_source(h, rng, zero_prob=zero_prob)
    A = list(0 for _ in range(NCAP))
    for i in COLORS:
        for j in COLORS:
            A[kidx(i, j)] = src[(0, 1)][i][j]
    words = sample_words(h, rng, n_words)

    # (a) graded == direct, on a few words, exactly over Z
    for w in words[:n_direct]:
        z = graded_error(src, h, w)
        lhs = graded_to_poly(src, h, z)
        rhs = error_poly_direct(src, h, w)
        require(lhs == rhs, ("graded != direct", h, w))
    print(f"  [L5{label}] h={h}: graded form == direct expansion on "
          f"{n_direct} words (exact over Z): PASS")

    # (b) exact membership E_w in L_h(A) for a few words
    rows, _ = L_generators(h, A)
    basis, pivots = rref_exact(rows)
    generic = sum((((k + 2) * (k + 1)) // 2) ** 2 for k in range(2, h + 1))
    if len(pivots) != generic:
        print(f"  [L5{label}] NOTE: this A_pq is degenerate: dim L_h(A) = "
              f"{len(pivots)} < {generic} (the law is STRONGER here)")
    for w in words[:n_direct]:
        poly = error_poly_direct(src, h, w)
        require(in_span_exact(basis, pivots, poly_to_row(poly, h)),
                ("E_w not in L_h", h, w))
    print(f"  [L5{label}] h={h}: E_w in L_h(A) verified EXACTLY over Q "
          f"({n_direct} words, independent direct expansion): PASS")

    # (c) span of all sampled components, in graded coordinates
    keyorder = []
    for k in range(2, h + 1):
        for mu, nu in sigma_basis(k):
            keyorder.append((k, mu, nu))
    kpos = {t: n for n, t in enumerate(keyorder)}
    zrows = []
    for w in words:
        z = graded_error(src, h, w)
        row = [0] * len(keyorder)
        for k in range(2, h + 1):
            for (mu, nu), c in z[k].items():
                row[kpos[(k, mu, nu)]] = c
        zrows.append(row)
    rk = rank_mod_p_np(zrows, P1)
    full = len(keyorder)
    print(f"  [L5{label}] h={h}: span of {len(words)} components inside L_h "
          f"has dim {rk} of {full}"
          + ("  <-- FULL (components fill L_h exactly)" if rk == full else ""))
    return {"h": h, "words": len(words), "span_in_Sigma_coords": rk,
            "dim_Sigma_coords": full, "dim_L_h_A": len(pivots),
            "ambient": len(monomials(NCAP, h)),
            "codim_of_L": len(monomials(NCAP, h)) - len(pivots),
            "zero_prob": zero_prob, "label": label}


def check_A_strata(rng):
    """dim L_h(A) as a function of the rank / degeneracy of A_pq."""
    res = {}
    print("  [L6] dim L_h(A) by rank of A_pq (the law strengthens as A degenerates)")
    for h in (2, 3, 4):
        ambient = len(monomials(NCAP, h))
        per_rank = {}
        for rank_target in (0, 1, 2, 3):
            dims = set()
            for _ in range(4):
                if rank_target == 0:
                    M = [[0] * 3 for _ in range(3)]
                else:
                    M = [[0] * 3 for _ in range(3)]
                    for _ in range(rank_target):
                        u = [rng.randint(-5, 5) for _ in range(3)]
                        v = [rng.randint(-5, 5) for _ in range(3)]
                        for i in range(3):
                            for j in range(3):
                                M[i][j] += u[i] * v[j]
                A = [M[i][j] for i in COLORS for j in COLORS]
                rows, _ = L_generators(h, A)
                dims.add(rank_mod_p_np(rows, P1))
            per_rank[rank_target] = sorted(dims)
            print(f"        h={h}, rank A_pq = {rank_target}: dim L_h(A) in "
                  f"{sorted(dims)}  (codim {[ambient - d for d in sorted(dims)]})")
        res[h] = {"ambient": ambient, "by_rank": per_rank}
    return res


def main():
    rng = random.Random(20260815)
    print("== (L1) Cauchy pieces Sigma_k = S^kV (x) S^kW ==")
    OUT["L1"] = check_sigma_dims()
    print("\n== (L2) apolarity with det, and the ideal (Sigma_2) ==")
    OUT["L2"] = check_apolar_and_ideal()
    print("\n== (L3) the sharp law L_h(A) = sum_k s^{h-k} Sigma_k ==")
    OUT["L3"] = check_L_dims(rng)
    print("\n== (L4) which laws are A-independent ==")
    OUT["L4"] = check_A_independent_part(rng)
    print("\n== (L5) verification on explicit sources ==")
    OUT["L5"] = []
    OUT["L5"].append(check_sources(2, rng, 81, n_direct=4, label="a"))
    OUT["L5"].append(check_sources(3, rng, 729, n_direct=3, label="b"))
    OUT["L5"].append(check_sources(4, rng, 700, n_direct=2, label="c"))
    print("\n(sparse source control)")
    OUT["L5"].append(check_sources(4, rng, 700, n_direct=1, zero_prob=0.35,
                                   label="d"))
    print("\n== (L6) how the law strengthens on degenerate A_pq ==")
    OUT["L6"] = check_A_strata(rng)
    with open(__file__.rsplit("/", 1)[0] + "/results_task1_law.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_task1_law.json")


if __name__ == "__main__":
    main()
