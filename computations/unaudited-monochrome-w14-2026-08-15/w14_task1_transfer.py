#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 1(b): the monochrome-transfer LEMMA itself.

The proved skeleton (see REPORT):

  EVALUATION PRINCIPLE.  Every f in span{E_w} has f(E_cc) = 0 as soon as the
  colour-c slice is clean (E_w(E_cc) = 0 for every word w).  Since
  (s^a kappa_c^{h-a})(E_cc) = s_c^a with s_c = A_pq(c,c), a clean colour-c
  slice excludes EVERY monochrome-c monomial when s_c != 0, and excludes
  kappa_c^h unconditionally.  Same argument works degreewise for the IDEAL.

  So the only residual case of the lemma is  a >= 1  AND  A_pq(c,c) = 0.
  There the graded projection gives the exact criterion
        s^a kappa_c^{h-a} in span{E_w}  =>  G_a^{(c)} is not identically 0,
  where G_j^{(c)}(w) = sum_{|J| = j} x_J Haf^{(c)}(U \\ V(J), w) and cleanness
  with s_c = 0 only says G_0^{(c)} = 0.

This script decides that residual case EXACTLY at h = 3 by building sources
with

  (F1) W13's construction: the colour-c row of every p-block is 0
       => every G_j^{(c)} = 0 (strictly stronger than a clean slice);
  (F2) support-clean with a live level 1: colour-c rows of the p-blocks
       killed at 4 of the 6 sites => G_0 = 0 but G_1 != 0, with A_pq(c,c) = 0;
  (F3) one site with no colour-c attachment to EITHER p or q (W5's support
       shape) => G_0 = 0, G_1 != 0, with A_pq(c,c) = 0;
  (F4) same as F2/F3 but with A_pq(c,c) != 0 (control: the proved regime).

and testing membership of every monochrome monomial in the degree-3 error
span, exactly over Q.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import product as iproduct

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)

from w14_core import (COLORS, NCAP, delta, det3, error_poly, G_level, in_span,
                      mono_name, mono_poly, no_zero_row_or_col, poly_eval,
                      poly_row, random_source, rank3, require, rref_exact,
                      sites, solve_combination, s_vector)

WORDS3 = list(iproduct(range(3), repeat=6))


def fix_pair_block(src, rng, c, zero_diag):
    """Make A_pq full rank, no zero row/column, with A_cc = 0 or != 0."""
    while True:
        A = [[rng.randint(-4, 4) for _ in COLORS] for _ in COLORS]
        if zero_diag:
            A[c][c] = 0
        elif A[c][c] == 0:
            continue
        if rank3(A) == 3 and no_zero_row_or_col(A):
            src[(0, 1)] = A
            return A


def build(kind, h, rng, c, zero_diag=True):
    src = random_source(h, rng, lo=-4, hi=4)
    P, Q, U = sites(h)
    if kind == "F1":                       # W13: kill colour-c p-row everywhere
        for a in U:
            for cv in COLORS:
                src[(P, a)][c][cv] = 0
    elif kind == "F2":                     # kill it at 4 of the 6 sites
        for a in U[:4]:
            for cv in COLORS:
                src[(P, a)][c][cv] = 0
    elif kind == "F3":                     # one site, both sides
        a = U[0]
        for cv in COLORS:
            src[(P, a)][c][cv] = 0
            src[(Q, a)][c][cv] = 0
    else:
        raise ValueError(kind)
    fix_pair_block(src, rng, c, zero_diag)
    return src


def slice_profile(src, h, c, words):
    """G_j^{(c)}(w) for j = 0..h-2, plus the slice error, over all words."""
    dc = delta(c)
    G = {j: [G_level(src, h, w, dc, dc, j) for w in words]
         for j in range(h - 1)}
    sc = src[(0, 1)][c][c]
    err = [sum(sc ** j * G[j][n] for j in range(h - 1))
           for n in range(len(words))]
    return G, err


def analyse(kind, c, zero_diag, rng, h=3, words=None, verbose=True):
    words = words or WORDS3
    src = build(kind, h, rng, c, zero_diag)
    A = src[(0, 1)]
    G, err = slice_profile(src, h, c, words)
    clean = all(x == 0 for x in err)
    rows = [poly_row(error_poly(src, h, w), h) for w in words]
    basis, piv = rref_exact(rows)
    sv = s_vector(src)
    membership = {}
    for cc in COLORS:
        for a in range(0, h - 1):
            b = tuple((h - a) if t == cc else 0 for t in COLORS)
            target = poly_row(mono_poly(a, b, sv), h)
            membership[mono_name(a, b)] = in_span(basis, piv, target)
    rec = {"kind": kind, "colour": c, "A_cc": A[c][c], "det_A": det3(A),
           "rank_A": rank3(A), "no_zero_row_col": no_zero_row_or_col(A),
           "slice_clean": clean, "span_dim": len(piv),
           "G_levels_nonzero": {j: any(x != 0 for x in G[j])
                                for j in range(h - 1)},
           "in_span": membership}
    if verbose:
        inn = sorted(k for k, v in membership.items() if v)
        print(f"  [{kind}] colour {c}, A_cc = {A[c][c]}, det {det3(A)}: "
              f"slice clean = {clean}; "
              f"G_j nonzero: {rec['G_levels_nonzero']}; span dim {len(piv)}")
        print(f"        monomials IN the span: {inn}")
    return rec, src, rows, basis, piv


def certificate(src, rows, words, h, c, a, tag):
    """If s^a kappa_c^{h-a} is in the span, produce and verify lambda exactly."""
    sv = s_vector(src)
    b = tuple((h - a) if t == c else 0 for t in COLORS)
    target = poly_row(mono_poly(a, b, sv), h)
    lam = solve_combination(rows, target)
    if lam is None:
        return None
    chk = [sum(lam[i] * rows[i][n] for i in range(len(rows)))
           for n in range(len(target))]
    require(chk == [Fraction(x) for x in target], ("bad certificate", tag))
    dc = delta(c)
    proj = [sum(lam[i] * G_level(src, h, words[i], dc, dc, j)
                for i in range(len(words))) for j in range(h - 1)]
    return {"tag": tag, "monomial": mono_name(a, b),
            "level_projections": [str(x) for x in proj],
            "expected": [str(Fraction(1 if j == a else 0))
                         for j in range(h - 1)],
            "support": sum(1 for x in lam if x != 0)}


def main():
    t0 = time.time()
    rng = random.Random(271828)
    out = {"trials": [], "certificates": []}
    print("== W14 Task 1(b): the residual case of the transfer lemma (h = 3) ==")
    print("\n-- F1: W13's clean-by-construction family (all G_j = 0) --")
    for c in COLORS:
        for zd in (True, False):
            rec, *_ = analyse("F1", c, zd, rng)
            out["trials"].append(rec)

    print("\n-- F2/F3: CLEAN colour-c slice with A_pq(c,c) = 0 and G_1 != 0 --")
    for kind in ("F2", "F3"):
        for c in COLORS:
            for trial in range(2):
                rec, src, rows, basis, piv = analyse(kind, c, True, rng)
                out["trials"].append(rec)
                if rec["slice_clean"] and rec["in_span"].get(
                        mono_name(1, tuple(2 if t == c else 0 for t in COLORS))):
                    cert = certificate(src, rows, WORDS3, 3, c, 1,
                                       f"{kind}-c{c}-t{trial}")
                    if cert:
                        out["certificates"].append(cert)
                        print(f"        CERTIFICATE {cert['monomial']}: "
                              f"level projections {cert['level_projections']} "
                              f"(expected {cert['expected']})")

    print("\n-- F4 (control): same shapes but A_pq(c,c) != 0 "
          "(proved regime: everything monochrome-c must be OUT) --")
    for kind in ("F2", "F3"):
        for c in COLORS:
            rec, *_ = analyse(kind, c, False, rng)
            rec["kind"] = kind + "/A_cc!=0"
            out["trials"].append(rec)

    with open(HERE + "/results_task1_transfer.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nwrote results_task1_transfer.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
