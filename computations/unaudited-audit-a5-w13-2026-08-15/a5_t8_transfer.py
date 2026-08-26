#!/usr/bin/env python3
"""A5 / claim 8: the 6/6 transfer evidence protocol.

Three things W13 never did and one it did:
 (A) actually MEASURE slice cleanliness (W13 only asserts it in a docstring):
     tensor-clean means E_w(E_cc) = 0 for EVERY word w, where E_cc is the
     elementary cap covector.  I measure it from my own error polynomials.
 (B) re-run 2 of the 6 trials with independent code (h=3, full 3^6 words):
     span dimension and the IN/OUT pattern of every monochrome monomial.
 (C) redo an h=4 trial with ALL 6561 words (W13 sampled 503 of 6561, so its
     h=4 "out of span" verdicts were statements about a sampled subspace).
 (D) test the CORRECTED statement (the evaluation principle) and its residual
     case: build sources that are clean with A_pq(c,c) = 0 and a live level 1
     (W14's F2 shape) and see whether s*kappa_c^{h-1} re-enters the span.

Span protocol (exact): pick a maximal independent subset of the E_w rows using
F_p, echelon it exactly over Q, compute its exact annihilator, and verify by
CRT that EVERY E_w is annihilated -- which proves the selected rows span the
whole error space exactly.  Membership verdicts are then exact both ways.
"""
from __future__ import annotations
import json, random, sys, time
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
import a5_fast as F
from a5_t4_taxonomy import monomial_vec, det3
import numpy as np

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
res = {"cleanliness": [], "trials": [], "residual": []}


def eval_at_Ecc(vec, h, c):
    """E_w(E_cc) = the coefficient of K_cc^h (all other monomials vanish)."""
    e = [0] * 9
    e[3 * c + c] = h
    return vec[A.monom_index(h)[tuple(e)]]


def exact_span(M):
    """Exact echelon of a spanning subset of the rows of M, certified to span
    the whole row space.  Returns (ech, piv, dim, certified)."""
    rows = [[int(x) for x in M[i]] for i in range(M.shape[0])]
    p = 2147483629
    # one mod-p forward pass, recording which ORIGINAL rows become pivots
    N = np.array([[x % p for x in r] for r in rows], dtype=np.int64)
    order = list(range(len(rows)))
    sel, r = [], 0
    for col in range(N.shape[1]):
        nz = np.nonzero(N[r:, col])[0]
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        if i != r:
            N[[r, i]] = N[[i, r]]
            order[r], order[i] = order[i], order[r]
        inv = pow(int(N[r, col]), p - 2, p)
        N[r] = (N[r] * inv) % p
        cv = N[r + 1:, col].copy()
        nzr = np.nonzero(cv)[0]
        if nzr.size:
            N[r + 1:][nzr] = (N[r + 1:][nzr] - cv[nzr, None] * N[r][None, :]) % p
        sel.append(order[r])
        r += 1
        if r == N.shape[0]:
            break
    cur = [rows[i] for i in sel]
    ech, piv = A.int_echelon(cur)
    assert len(piv) == len(sel), "selected rows not independent over Q"
    Phi = A.perp_basis(cur, M.shape[1])
    ok, info = A.product_is_exactly_zero(np.array(rows, dtype=object),
                                         np.array(Phi, dtype=object))
    return ech, piv, len(piv), ok


def build_clean_source(h, rng, c, shape="F1", zero_diag=True):
    """shape F1 = W13's (kill the colour-c row of EVERY p-block);
       shape F2 = kill it at all but two U-sites (clean, but level 1 lives)."""
    src = A.random_source(h, rng, lo=-4, hi=4)
    p, q, U = A.sites(h)
    kill = U if shape == "F1" else U[:len(U) - 2]
    for a in kill:
        for cv in A.C3:
            src[(p, a)][c][cv] = 0
    if zero_diag:
        src[(p, q)][c][c] = 0
    return src


def analyse(src, h, c, tag, all_words=True, nwords=None, rng=None):
    svec = A.s_vector(src)
    bm = F.block_matrices(h, svec)
    # certify the fast route against raw eq. (4)
    for _ in range(3):
        w = tuple(rng.choice(A.C3) for _ in range(2 * h))
        assert A.poly_vec(A.cap_error_raw(src, h, w), h) == F.error_vec_fast(src, h, w, bm)
    words, M = F.all_error_vectors(src, h, bm)
    if not all_words:
        idx = sorted(rng.sample(range(len(words)), nwords - 3))
        idx += [words.index(tuple([cc] * (2 * h))) for cc in A.C3]
        M = M[sorted(set(idx))]
        words = [words[i] for i in sorted(set(idx))]
    # (A) cleanliness, measured
    vals = [eval_at_Ecc([int(x) for x in M[i]], h, c) for i in range(M.shape[0])]
    clean = all(v == 0 for v in vals)
    ech, piv, dim, certified = exact_span(M)
    rec = {"tag": tag, "h": h, "colour": c, "words_used": len(words),
           "A_pq": [row[:] for row in src[(0, 1)]], "A_cc": src[(0, 1)][c][c],
           "det_A": det3(src[(0, 1)]), "slice_clean_measured": clean,
           "n_nonzero_slice_values": sum(1 for v in vals if v != 0),
           "span_dim": dim, "span_certified_complete": certified}
    for a in range(0, h - 1):
        for cc in A.C3:
            bs = tuple((h - a) if t == cc else 0 for t in A.C3)
            v = monomial_vec(h, svec, a, bs)
            rec[f"s^{a} k{cc}^{h-a}"] = A.in_span_exact(ech, piv, v)
    return rec


def main():
    rng = random.Random(90210)
    # ---------------- (B) two of the six trials, h = 3, F1 shape
    for c in (0, 1):
        src = build_clean_source(3, rng, c, "F1", zero_diag=False)
        rec = analyse(src, 3, c, f"B: W13 F1 shape h=3 colour {c}", rng=rng)
        print(json.dumps(rec), flush=True)
        res["trials"].append(rec)
    # ---------------- (C) h = 4 with ALL words vs W13's 503-word sample
    c = 0
    src = build_clean_source(4, rng, c, "F1", zero_diag=False)
    t0 = time.time()
    rec_full = analyse(src, 4, c, "C: F1 shape h=4, ALL 6561 words", rng=rng)
    print(json.dumps(rec_full), flush=True)
    res["trials"].append(rec_full)
    rec_samp = analyse(src, 4, c, "C: same source, 503-word sample (W13's protocol)",
                       all_words=False, nwords=503, rng=rng)
    print(json.dumps(rec_samp), flush=True)
    res["trials"].append(rec_samp)
    print(f"  [h=4 both protocols {time.time()-t0:.0f}s]", flush=True)
    # ---------------- (D) residual case: clean, A_cc = 0, level 1 alive
    for c in (0, 2):
        for t in range(2):
            src = build_clean_source(3, rng, c, "F2", zero_diag=True)
            rec = analyse(src, 3, c, f"D: F2 shape h=3 colour {c} trial {t}", rng=rng)
            print(json.dumps(rec), flush=True)
            res["residual"].append(rec)
    json.dump(res, open(OUT + "results_t8_transfer.json", "w"), indent=1)


if __name__ == "__main__":
    main()
