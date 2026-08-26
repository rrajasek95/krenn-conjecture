#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 3: evidence for the named next lemma
("monochrome transfer").

F1 (Prop. W13.7, h-uniform): the coefficient of kappa_c^h in E_w is E_w(E_cc)
= the colour-c monochrome slice error.  So a CLEAN colour-c slice forces
kappa_c^h out of the error span.

The next lemma asks the same for a >= 1: does a clean colour-c slice also force
s^a kappa_c^{h-a} out of the error span?  Here we build sources whose colour-c
slice is clean by construction (the colour-c row of every p-block vanishes, so
every R-form of the slice is zero) and test membership of each monochrome
monomial in the ACTUAL degree-h error span, exactly over Q.
"""
import random, sys, json
from fractions import Fraction
sys.path.insert(0, '.')
from w13_core import (COLORS, NCAP, graded_error, graded_to_poly, in_span_exact,
                      kidx, random_source, rref_exact, sigma_basis, sites)
from w13_task1_law import poly_to_row, rank_mod_p_np, P1
from w13_task1_taxonomy import mono_name, mono_poly, flat, det3
from itertools import product as iproduct

def slice_clean_source(h, rng, c):
    src = random_source(h, rng, lo=-4, hi=4)
    P, Q, U = sites(h)
    for a in U:                      # kill the colour-c row of every p-block
        for cv in COLORS:
            src[(P, a)][c][cv] = 0
    return src

def span_rows(src, h, words):
    rows = []
    for w in words:
        z = graded_error(src, h, w)
        rows.append(poly_to_row(graded_to_poly(src, h, z), h))
    return rows

out = {}
rng = random.Random(31415)
for h in (3, 4):
    words = list(iproduct(range(3), repeat=2*h)) if h == 3 else \
        [tuple(rng.randrange(3) for _ in range(2*h)) for _ in range(500)] + \
        [tuple([c]*(2*h)) for c in range(3)]
    res = []
    for trial in range(3):
        c = trial % 3
        src = slice_clean_source(h, rng, c)
        A = [[src[(0,1)][i][j] for j in COLORS] for i in COLORS]
        rows = span_rows(src, h, words)
        basis, piv = rref_exact(rows)
        rec = {"h": h, "clean_colour": c, "det_A": det3(A), "span_dim": len(piv)}
        for a in range(0, h-1):
            for cc in range(3):
                b = tuple((h-a) if t == cc else 0 for t in range(3))
                vec = [Fraction(x) for x in poly_to_row(mono_poly(a, b, flat(A)), h)]
                for r, col in enumerate(piv):
                    if vec[col]:
                        f = vec[col]
                        vec = [x - f*y for x, y in zip(vec, basis[r])]
                rec[mono_name(a, b)] = all(x == 0 for x in vec)
        res.append(rec)
        inn = [k for k, v in rec.items() if v is True]
        print(f"  h={h} trial {trial}: colour {c} slice CLEAN by construction; "
              f"error span dim {len(piv)}; monochrome monomials IN the span: "
              f"{sorted(inn)}")
    out[f"h{h}"] = res
json.dump(out, open('results_task3_transfer.json','w'), indent=1, default=str)
print("wrote results_task3_transfer.json")
