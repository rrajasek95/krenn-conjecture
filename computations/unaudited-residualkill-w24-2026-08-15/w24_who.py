#!/usr/bin/env python3
"""W24 -- WHICH words carry the pure monomial rows, and why is their
constant Phi_w = 0?  UNAUDITED.  Exact only."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402

FULLBOX_L = [(1, 2, 0, 0), (1, 2, 0, 1), (2, 2, 0, 0), (2, 2, 0, 1)]
FULLBOX_R = [(1, 2, 0, 0), (1, 2, 0, 1), (2, 2, 0, 0), (2, 2, 0, 1)]

out = {}
pts = P.stored_points()
for m, tag, bl in pts:
    if m != 28:
        continue
    d = RS.verdict(m, bl, want_detail=True)
    if d["inconsistent"] or len(d["forced_zero"]) != 12:
        continue
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    cells, rows, cleanw = RS.build_system(m, bl)
    n = len(cells)
    pure = []
    for w, v, c in rows:
        nv = [i for i in range(n) if v[i] != 0]
        if len(nv) == 1 and c == 0:
            pure.append((w, cells[nv[0]]))
    print("point %s: %d pure rows" % (tag, len(pure)))
    # classify by x-part / y-part membership in the full boxes
    cnt = Counter()
    for w, e in pure:
        x, y = w[:4], w[4:]
        cnt[(x in FULLBOX_L, y in FULLBOX_R)] += 1
    print("  (x full-box, y full-Xbox) ->", dict(cnt))
    # how many x-parts / y-parts occur
    xs = Counter(w[:4] for w, _ in pure)
    ys = Counter(w[4:] for w, _ in pure)
    print("  distinct x among pure rows: %d ; distinct y: %d"
          % (len(xs), len(ys)))
    # For the pure rows: is Phi_w=0 because hafL(x)=0? because the whole
    # x-fibre {(x,y'): all y'} has Phi = 0?  Test both.
    hl = {}
    for w, _ in pure:
        x = w[:4]
        if x in hl:
            continue
        hl[x] = sum(bl[(i, j)][x[i]][x[j]] * bl[(k, l)][x[k]][x[l]]
                    for (i, j), (k, l) in (((0, 1), (2, 3)), ((0, 2), (1, 3)),
                                           ((0, 3), (1, 2))))
    print("  x-parts with hafL(x) = 0: %d of %d"
          % (sum(1 for x in hl if hl[x] == 0), len(hl)))
    # whole-fibre test: for each x occurring, is Phi_(x,y')=0 for ALL 81 y'?
    from itertools import product as iproduct
    allzero_x = 0
    for x in xs:
        if all(C.phi(bl, gam_set, tuple(x) + yy) == 0
               for yy in iproduct(range(3), repeat=4)):
            allzero_x += 1
    print("  x-parts whose ENTIRE 81-word fibre has Phi = 0: %d of %d"
          % (allzero_x, len(xs)))
    ally = 0
    for y in ys:
        if all(C.phi(bl, gam_set, tuple(xx) + tuple(y)) == 0
               for xx in iproduct(range(3), repeat=4)):
            ally += 1
    print("  y-parts whose ENTIRE 81-word fibre has Phi = 0: %d of %d"
          % (ally, len(ys)))
    # global: how many of the 6561 words have Phi = 0?
    nz = sum(1 for w in C.WORDS if C.phi(bl, gam_set, w) != 0)
    print("  words (of 6561) with Phi != 0: %d" % nz)
    out[tag] = dict(n_pure=len(pure), box_split={str(k): v for k, v in
                                                 cnt.items()},
                    n_x=len(xs), n_y=len(ys),
                    x_hafL_zero=sum(1 for x in hl if hl[x] == 0),
                    x_fibre_all_zero=allzero_x, y_fibre_all_zero=ally,
                    n_words_phi_nonzero=nz)
    break
json.dump(out, open(os.path.join(HERE, "results_who.json"), "w"),
          indent=1, default=str)
