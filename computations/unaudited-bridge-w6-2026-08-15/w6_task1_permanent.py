#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- J.1c: the h=3 dictionary in R_cell (permanents).

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

W4 gave the h = 2 dictionary in R_cell (2+2 splits; criterion (C)).  Its h = 3
analogue, derived and verified here:

  In R_cell write the cell of A_px as (i_x, j_x) with weight alpha_x (row =
  colour at p) and of A_qx as (k_x, l_x) with weight beta_x.  Then

      R_ab(c_a,c_b) = [c_a=j_a][c_b=l_b] alpha_a beta_b K_{i_a k_b}
                    + [c_a=l_a][c_b=j_b] alpha_b beta_a K_{i_b k_a},

  so an oriented perfect matching of U is exactly a 3+3 split U = X u Y
  (X the p-sides) together with a bijection sigma : X -> Y.  Every oriented
  matching with p-side X forces the SAME word

      w(X)_x = j_x  (x in X),      w(X)_y = l_y  (y in Y),

  and the r^3 part of E_{w} is

      [r^3]_w = sum over { X : w(X) = w }
                per_3( [ alpha_x beta_y K_{i_x k_y} ]_{x in X, y in Y} ).  (P3)

  A 3x3 PERMANENT, not a determinant -- which is why the determinantal
  (Lambda^3 x Lambda^3) obstruction of P1/W4 annihilates it.

CONSEQUENCE (the h=3 support criterion).  (P3) is proportional to K_{ab}^3 iff
every entry of the permanent's matrix is K_{ab}, i.e. iff i_x = a for all
x in X and k_y = b for all y in Y.  With (a,b) = (c,c) this is (C3-kappa) for
kappa_c^3, and with (a,b) the cell of A_pq it is (C3-s) for s^3.  These are
SUPPORT conditions on the cell pattern -- the h=3 shape of W4's (C).

They are SUFFICIENT for proportionality of one component but NOT necessary
for membership in the span (measured in w6_task1_bridge.py: membership occurs
with the criterion false, because several 3+3 splits can share a word and
because the s r^2 x layer contributes too).  That is the honest h=3 residue.

Run: python3 w6_task1_permanent.py
"""

from __future__ import annotations

import json
import random
import sys
from itertools import combinations, permutations

P1 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p1-2026-08-15")
if P1 not in sys.path:
    sys.path.insert(0, P1)

import wsplit_core as core                                        # noqa: E402
from wsplit_core import P, Q, U, SITE_SLOT, kidx, error_row       # noqa: E402


def rcell_star_source(rng, absent=0.0):
    """R_cell source with A_xy = 0 for x,y in U, so 6E = r^3 exactly."""
    src = core.zero_source()
    cells = {}
    for x in U:
        for anchor in (P, Q):
            if rng.random() < absent:
                cells[(anchor, x)] = None
                continue
            i, j = rng.randrange(3), rng.randrange(3)
            weight = rng.choice([1, 2, -1, 3])
            src[core.edge_key(anchor, x)][i][j] = weight
            cells[(anchor, x)] = (i, j, weight)
    i, j = rng.randrange(3), rng.randrange(3)
    src[(P, Q)][i][j] = rng.choice([1, 2, -1])
    cells[(P, Q)] = (i, j, src[(P, Q)][i][j])
    return src, cells


def word_of_split(cells, X):
    """w(X): w_x = j_x for x in X, w_y = l_y for y in Y (None if absent)."""
    word = [None] * len(U)
    for x in U:
        anchor = P if x in X else Q
        entry = cells[(anchor, x)]
        if entry is None:
            return None
        word[SITE_SLOT[x]] = entry[1]
    return tuple(word)


def permanent_cubic(cells, X):
    """(P3) as {cubic monomial -> coefficient}."""
    Y = tuple(y for y in U if y not in X)
    out = {}
    for sigma in permutations(Y):
        coefficient = 1
        keys = []
        ok = True
        for x, y in zip(X, sigma):
            pcell, qcell = cells[(P, x)], cells[(Q, y)]
            if pcell is None or qcell is None:
                ok = False
                break
            coefficient *= pcell[2] * qcell[2]
            keys.append(kidx(pcell[0], qcell[0]))
        if not ok:
            continue
        key = tuple(sorted(keys))
        out[key] = out.get(key, 0) + coefficient
    return {k: v for k, v in out.items() if v}


def predicted_row(cells, word):
    total = {}
    for X in combinations(U, 3):
        if word_of_split(cells, X) != word:
            continue
        for key, value in permanent_cubic(cells, X).items():
            total[key] = total.get(key, 0) + value
    return {k: v for k, v in total.items() if v}


def main():
    print("UNAUDITED PROBE (W6) -- R_cell h=3 permanent dictionary, "
          "HEAD 31cefe2", flush=True)
    rng = random.Random(20260815)
    checked = mismatches = nonzero_rows = 0
    proportional = {"kappa": 0, "s": 0}
    for trial in range(14):
        src, cells = rcell_star_source(rng, absent=0.15 if trial % 2 else 0.0)
        for word in core.WORDS:
            actual = error_row(src, word)
            predicted = predicted_row(cells, word)
            checked += 1
            if actual != predicted:
                mismatches += 1
                if mismatches <= 3:
                    print("  MISMATCH", word, actual, predicted)
            if actual:
                nonzero_rows += 1
                keys = set(actual)
                if len(keys) == 1:
                    only = next(iter(keys))
                    a, b = divmod(only[0], 3)
                    if only == (only[0],) * 3:
                        if a == b:
                            proportional["kappa"] += 1
                        pair = cells[(P, Q)]
                        if pair and (a, b) == (pair[0], pair[1]):
                            proportional["s"] += 1
    print(f"  words checked {checked}, mismatches {mismatches}, "
          f"nonzero components {nonzero_rows}")
    print(f"  components proportional to a pure cube: {proportional}")
    payload = {"words_checked": checked, "mismatches": mismatches,
               "nonzero_components": nonzero_rows,
               "pure_cube_components": proportional,
               "claim": "[r^3]_w = sum over 3+3 splits X with w(X)=w of "
                        "per_3([alpha_x beta_y K_{i_x k_y}])"}
    with open("results_permanent.json", "w") as handle:
        json.dump(payload, handle, indent=1)
    print("wrote results_permanent.json")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
