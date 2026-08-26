#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 1(b) at h = 4: is the transfer counterexample
an h = 3 accident?

Uses the PROVED graded equivalence (directness of L_h(A) at full rank):

    s^a kappa_c^{h-a} in span{E_w}
      <=>  the graded vector (0,...,0, e_c^{h-a}(x)f_c^{h-a}/(h-a)!, 0,...)
           lies in the span of the graded vectors (z_{w,k})_{k=2..h}.

The graded vectors are far cheaper than the degree-h polynomials, so h = 4
(N = 10) is reachable exactly over Q.  h = 3 is run first as a cross-check
against the direct polynomial test.
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

from w14_core import (COLORS, NCAP, delta, det3, error_poly, G_level,
                      graded_error, in_span, mono_name, mono_poly, monomials,
                      no_zero_row_or_col, poly_eval, poly_row, random_source,
                      rank3, require, rref_exact, sigma_basis, sites,
                      s_vector)
from w14_task1_transfer import build


def graded_row(z, h):
    """Flatten {k: {(mu,nu): c}} into one exact vector."""
    row = []
    for k in range(2, h + 1):
        idx = {key: n for n, key in enumerate(sigma_basis(k))}
        vec = [0] * len(idx)
        for key, c in z[k].items():
            vec[idx[key]] += c
        row.extend(vec)
    return row


def target_row(h, a, c):
    """Graded vector of s^a kappa_c^{h-a} (times (h-a)! to stay integral)."""
    row = []
    for k in range(2, h + 1):
        idx = {key: n for n, key in enumerate(sigma_basis(k))}
        vec = [0] * len(idx)
        if k == h - a:
            key = ((c,) * k, (c,) * k)
            vec[idx[key]] = 1
        row.extend(vec)
    return row


def run(h, kind, c, zero_diag, rng, nwords, check_direct=False):
    src = build(kind, h, rng, c, zero_diag)
    A = src[(0, 1)]
    P, Q, U = sites(h)
    if h == 3 and nwords is None:
        words = list(iproduct(range(3), repeat=2 * h))
    else:
        words = [tuple(rng.randrange(3) for _ in range(2 * h))
                 for _ in range(nwords)]
        words += [(cc,) * (2 * h) for cc in COLORS]
    Ecc = [1 if n == 3 * c + c else 0 for n in range(NCAP)]
    zs = [graded_error(src, h, w) for w in words]
    rows = [graded_row(z, h) for z in zs]
    basis, piv = rref_exact(rows)
    # cleanness of the colour-c slice, from the level functions
    dc = delta(c)
    sc = A[c][c]
    Gs = {j: [G_level(src, h, w, dc, dc, j) for w in words]
          for j in range(h - 1)}
    clean_sample = all(sum(sc ** j * Gs[j][n] for j in range(h - 1)) == 0
                       for n in range(len(words)))
    rec = {"h": h, "kind": kind, "colour": c, "A_cc": sc, "det_A": det3(A),
           "rank_A": rank3(A), "no_zero_row_col": no_zero_row_or_col(A),
           "words": len(words), "graded_span_dim": len(piv),
           "slice_clean_on_sample": clean_sample,
           "G_nonzero": {j: any(x != 0 for x in Gs[j]) for j in range(h - 1)}}
    for a in range(0, h - 1):
        rec[mono_name(a, tuple((h - a) if t == c else 0 for t in COLORS))] = \
            in_span(basis, piv, target_row(h, a, c))
    if check_direct:
        prows = [poly_row(error_poly(src, h, w), h) for w in words]
        pb, pp = rref_exact(prows)
        sv = s_vector(src)
        agree = True
        for a in range(0, h - 1):
            b = tuple((h - a) if t == c else 0 for t in COLORS)
            direct = in_span(pb, pp, poly_row(mono_poly(a, b, sv), h))
            if direct != rec[mono_name(a, b)]:
                agree = False
        rec["graded_test_agrees_with_direct"] = agree
        rec["direct_span_dim"] = len(pp)
    return rec


def main():
    t0 = time.time()
    rng = random.Random(56789)
    out = []
    print("== W14 Task 1(b) at h = 4: the transfer boundary, exact over Q ==")
    print("\n-- h = 3 cross-check (graded test vs direct polynomial test) --")
    for kind in ("F1", "F2"):
        rec = run(3, kind, 0, True, rng, None, check_direct=True)
        out.append(rec)
        print(f"  [{kind}] colour 0, A_cc = {rec['A_cc']}: clean "
              f"{rec['slice_clean_on_sample']}, graded span {rec['graded_span_dim']}"
              f", direct span {rec['direct_span_dim']}, agree "
              f"{rec['graded_test_agrees_with_direct']}; "
              f"k0^3 {rec['k0^3']}, sk0^2 {rec['sk0^2']}")

    print("\n-- h = 4 (N = 10) --")
    for kind in ("F1", "F2", "F3"):
        for zd in ((True,) if kind != "F1" else (True,)):
            for c in (0, 1):
                rec = run(4, kind, c, zd, rng, 520)
                out.append(rec)
                mono = {k: v for k, v in rec.items()
                        if k.startswith(("k", "s")) and isinstance(v, bool)}
                print(f"  [{kind}] colour {c}, A_cc = {rec['A_cc']}, "
                      f"clean(sample) {rec['slice_clean_on_sample']}, "
                      f"G nonzero {rec['G_nonzero']}, graded span "
                      f"{rec['graded_span_dim']}/{361}")
                print(f"        monochrome-{c} membership: {mono}")
    print("\n-- h = 4 control: A_cc != 0 (the PROVED regime) --")
    for kind in ("F2", "F3"):
        rec = run(4, kind, 0, False, rng, 520)
        out.append(rec)
        mono = {k: v for k, v in rec.items()
                if k.startswith(("k", "s")) and isinstance(v, bool)}
        print(f"  [{kind}] colour 0, A_cc = {rec['A_cc']}, clean(sample) "
              f"{rec['slice_clean_on_sample']}: {mono}")
    with open(HERE + "/results_task1_h4.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nwrote results_task1_h4.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
