#!/usr/bin/env python3
"""A5 / claim 4: the (T2) COUNTEREXAMPLE, established three independent ways.

Witness: A_pq = P = the permutation matrix of the transposition (1 2),
    A = [[1,0,0],[0,0,1],[0,1,0]],
which has NO zero row, NO zero column and det A = -1 (FULL RANK).
Then  kappa_0 kappa_1^2  (two distinct kappa colours) lies in L_3(A).

(1) CLOSED-FORM CERTIFICATE (hand-checkable, no linear algebra):
        kappa_0 kappa_1^2 = s * kappa_1^2
                            - (1/6) iota_3(e_1 e_1 e_1 (x) f_1 f_1 f_2)
                            - (1/6) iota_3(e_1 e_1 e_2 (x) f_1 f_1 f_1)
    with s = <K, A> = K_00 + K_12 + K_21 and kappa_1^2 = (e_1 (x) f_1)^2.
    Verified here as an exact polynomial identity in the nine K variables.
(2) exact membership via my Sigma-power basis (independent route);
(3) the same at h = 4 with kappa_0 kappa_1^3, and the reach test: a source
    whose p-q block is A, asking whether the monomial is in span{E_w} --
    i.e. whether it is a genuine degree-h certificate, not merely allowed.
"""
from __future__ import annotations
import json, random, sys
from itertools import permutations
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
import a5_fast as F
from a5_t4_taxonomy import monomial_vec, det3, has_zero_line

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
res = {}
W = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
svec = [W[i][j] for i in range(3) for j in range(3)]
print("witness A =", W, " det =", det3(W), " zero line:", has_zero_line(W))


def iota_poly(mu, nu):
    k = len(mu)
    acc = {}
    for sg in permutations(range(k)):
        e = [0] * 9
        for t in range(k):
            e[3 * mu[t] + nu[sg[t]]] += 1
        key = tuple(e)
        acc[key] = acc.get(key, 0) + 1
    return acc


# ---- (1) closed-form certificate, h = 3
s = A.var_poly(svec)
kap1sq = A.ppow(A.var_poly([1 if (i, j) == (1, 1) else 0
                            for i in range(3) for j in range(3)]), 2)
lhs = A.pmul(A.var_poly([1 if (i, j) == (0, 0) else 0
                         for i in range(3) for j in range(3)]), kap1sq)
t1 = iota_poly((1, 1, 1), (1, 1, 2))
t2 = iota_poly((1, 1, 2), (1, 1, 1))
rhs = A.pmul(s, kap1sq)
from fractions import Fraction
rhs = {m: Fraction(c) for m, c in rhs.items()}
for t in (t1, t2):
    rhs = A.padd(rhs, {m: -Fraction(c, 6) for m, c in t.items()})
ok1 = ({m: Fraction(c) for m, c in lhs.items()} == {m: c for m, c in rhs.items() if c})
print("(1) closed-form identity kappa_0 kappa_1^2 = s*kappa_1^2 - (1/6)(P1+P2):", ok1)
# and the two permanents really are in Sigma_3 (they are iota_3 of basis
# elements, by construction), double-checked against the power basis:
rng = random.Random(5)
sig3 = A.int_echelon(A.sigma_rows_powers(3, rng))
ok1b = all(A.in_span_exact(sig3[0], sig3[1], A.poly_vec(t, 3)) for t in (t1, t2))
print("    both permanents lie in the (u(x)v)^3 power span of Sigma_3:", ok1b)
res["closed_form_identity"] = ok1
res["permanents_in_sigma3"] = ok1b

# ---- (2) independent exact membership, h = 3 and h = 4
res["membership"] = {}
for h, key in ((3, (0, 1, 2, 0)), (4, (0, 1, 3, 0)), (4, (1, 1, 2, 0)),
               (4, (0, 1, 2, 1)), (3, (0, 1, 1, 1)), (3, (1, 1, 1, 0))):
    rows = A.L_rows(h, svec, rng)
    ech, piv = A.int_echelon(rows)
    v = monomial_vec(h, svec, key[0], key[1:])
    inside = A.in_span_exact(ech, piv, v)
    name = "s^%d " % key[0] + " ".join(f"k{c}^{key[1+c]}" for c in range(3) if key[1 + c])
    print(f"(2) h={h} monomial {name:22s} in L_h(A): {inside}   (dim L_h = {len(piv)})")
    res["membership"][f"h{h}_{key}"] = {"in_L": inside, "dimL": len(piv), "name": name}

# ---- (3) REACH TEST: is it in the actual error span of a source with A_pq = W?
res["reach"] = []
for h in (3, 4):
    for trial in range(3 if h == 3 else 1):
        rng2 = random.Random(700 + trial + 10 * h)
        src = A.random_source(h, rng2)
        src[(0, 1)] = [row[:] for row in W]          # force A_pq = the witness
        assert A.s_vector(src) == svec
        bm = F.block_matrices(h, svec)
        # certify the fast route against raw eq. (4) on a few words
        for _ in range(3):
            w = tuple(rng2.choice(A.C3) for _ in range(2 * h))
            assert A.poly_vec(A.cap_error_raw(src, h, w), h) == F.error_vec_fast(src, h, w, bm)
        words, M = F.all_error_vectors(src, h, bm)
        # use a subset of words at h=4 (a subset span is a lower bound: a
        # POSITIVE membership verdict on the subset proves membership in the
        # full error span)
        idx = list(range(M.shape[0])) if h == 3 else sorted(
            rng2.sample(range(M.shape[0]), 600))
        rows = [[int(x) for x in M[i]] for i in idx]
        ech, piv = A.int_echelon(rows)
        dim_span = len(piv)
        keys = [(0, 1, 2, 0)] if h == 3 else [(0, 1, 3, 0), (1, 1, 2, 0)]
        rec = {"h": h, "trial": trial, "dim_span_E": dim_span}
        for key in keys:
            v = monomial_vec(h, svec, key[0], key[1:])
            rec[str(key)] = A.in_span_exact(ech, piv, v)
        # and the monochrome control kappa_0^h (must be IN if tight)
        mono = (0,) + tuple(h if c == 0 else 0 for c in range(3))
        rec["monochrome_k0^h"] = A.in_span_exact(ech, piv, monomial_vec(h, svec, 0, mono[1:]))
        print(f"(3) h={h} trial {trial}: dim span(E_w) = {dim_span}; " +
              "; ".join(f"{k}={v}" for k, v in rec.items() if k.startswith("(")) +
              f"; kappa_0^{h} in span = {rec['monochrome_k0^h']}", flush=True)
        res["reach"].append(rec)

json.dump(res, open(OUT + "results_t4_refutation.json", "w"), indent=1)
