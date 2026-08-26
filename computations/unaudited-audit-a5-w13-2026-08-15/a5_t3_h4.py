#!/usr/bin/env python3
"""A5 / claims 2+3 at h=4, exhaustive over all 6561 words via the exact
annihilator (perp) of L_4(A).  Membership E_w in L_4 is then an exact integer
orthogonality check, and the span rank uses numpy F_p elimination at two
primes with the structural upper bound dim L_4."""
from __future__ import annotations
import json, random, sys, time
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
import a5_fast as F
import numpy as np

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
h = 4
res = []
rng = random.Random(999)

# sanity: numpy rank agrees with the pure-python rank on a small random matrix
for _ in range(3):
    R = [[rng.randint(-5, 5) for _ in range(20)] for _ in range(15)]
    assert A.rank_mod_p_np(R, 1000003) == A.rank_mod_p(R, 1000003)
print("rank_mod_p_np cross-check OK", flush=True)

for tag, kw in [("dense", {}), ("wide", {"lo": -9, "hi": 9}), ("sparse", {"zero_prob": 0.3})]:
    src = A.random_source(h, rng, **kw)
    svec = A.s_vector(src)
    bmats = F.block_matrices(h, svec)
    t0 = time.time()
    bad = 0
    for _ in range(6):
        w = tuple(rng.choice(A.C3) for _ in range(2 * h))
        if A.poly_vec(A.cap_error_raw(src, h, w), h) != F.error_vec_fast(src, h, w, bmats):
            bad += 1
    print(f"[{tag}] fast-vs-raw(eq.4) mismatches {bad}/6 [{time.time()-t0:.0f}s]", flush=True)
    assert bad == 0

    t0 = time.time()
    Lr = A.L_rows(h, svec, rng)
    ech, piv = A.int_echelon(Lr)
    dimL = len(piv)
    Phi = A.perp_basis(Lr, len(A.deg_monoms(h)))
    print(f"[{tag}] dim L_4 = {dimL}, dim perp = {len(Phi)} [{time.time()-t0:.0f}s]", flush=True)

    t0 = time.time()
    words, M = F.all_error_vectors(src, h, bmats)
    print(f"[{tag}] built {M.shape} [{time.time()-t0:.0f}s]", flush=True)

    PH = np.array(Phi, dtype=object)
    ok, info = A.product_is_exactly_zero(np.array(M, dtype=object), PH)
    nonorth = 0 if ok else 1
    print(f"[{tag}] CRT certificate: bound={info['bound']} primes={info['primes']}", flush=True)
    nz_words = int(np.count_nonzero(M.any(axis=1)))
    print(f"[{tag}] EXACT: {nz_words} nonzero E_w; violations of E_w _|_ perp = {nonorth}",
          flush=True)

    r1 = A.rank_mod_p_np([[int(x) for x in r] for r in M], 2147483629)
    r2 = A.rank_mod_p_np([[int(x) for x in r] for r in M], 1000003)
    print(f"[{tag}] rank span(E_w): {r1} / {r2} (two primes); dim L_4 = {dimL}", flush=True)

    # control: a random vector must NOT be orthogonal to the perp
    v = np.array([[rng.randint(-9, 9) for _ in range(M.shape[1])]], dtype=object)
    ctl = not A.product_is_exactly_zero(v, PH)[0]
    # control: E_w plus a unit vector where a perp functional is nonzero
    i0 = int(np.nonzero(M.any(axis=1))[0][0])
    j0 = int(np.nonzero(np.array(Phi[0]))[0][0])
    v2 = np.array([[int(M[i0][j]) + (1 if j == j0 else 0) for j in range(M.shape[1])]], dtype=object)
    ctl2 = not A.product_is_exactly_zero(v2, PH)[0]
    print(f"[{tag}] CONTROLS random vector not _|_ perp: {ctl}; E_w + e_j breaks: {ctl2}",
          flush=True)
    res.append({"src": tag, "dimL": dimL, "dim_perp": len(Phi), "nz_words": nz_words,
                "membership_violations": nonorth, "rank_p1": r1, "rank_p2": r2,
                "fills_L": r1 == dimL and r2 == dimL,
                "control_random_not_perp": ctl, "control_shifted_breaks": ctl2})
    json.dump(res, open(OUT + "results_t3_h4.json", "w"), indent=1)
print("DONE")
