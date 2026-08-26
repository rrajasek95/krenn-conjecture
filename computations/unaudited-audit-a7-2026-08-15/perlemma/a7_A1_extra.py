#!/usr/bin/env python3
"""A7 SUB-AUDIT -- extra machine checks for the CORRECTED proof of W20-P and
for a strengthened A6 stratum.  Exact only.

(1) L(n) -- the statement my corrected induction actually proves:
        per_n == 0 on X_1 x ... x X_n with dim X_j >= n-1 for every j
        ==> all X_j are one and the same coordinate hyperplane.
    Exhaustive over X_j in {C^n} u {hyperplanes with {-1,0,1} normals}.
    In particular it tests the sub-claim "no X_j can be the full space",
    which is the ingredient the W20 sketch got wrong.

(2) S3 -- the sub-claim used in my proof of Lemma W20-P4c:
        per_3 == 0 on <a> x Y x Z with a all-nonzero and dim Y, dim Z >= 2
    is impossible in characteristic != 2.  Exhaustive stratum + the symbolic
    determinant identity det S = 2*a1*a2*a3 that proves it.

(3) P4c on a much larger u-stratum: all 128 sign-classes of {-2,-1,1,2}^4
    times ALL 11,480 multisets of {-1,0,1} normals.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations_with_replacement, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from a7_core import (per, kernel_basis, is_common_coordinate,       # noqa: E402
                     per_vanishes_on_product, sign_reps)


def spaces_for(n):
    """(label, basis, normal-or-None) for C^n and for every {-1,0,1}-normal
    hyperplane."""
    out = [("FULL", [[1 if i == k else 0 for i in range(n)]
                     for k in range(n)], None)]
    for nv in sign_reps(n):
        out.append((str(list(nv)), kernel_basis(nv), nv))
    return out


def check_L(n):
    sp = spaces_for(n)
    tested = 0
    vanishing = []
    violations = []
    full_involved = 0
    for combo in combinations_with_replacement(range(len(sp)), n):
        tested += 1
        if not per_vanishes_on_product([sp[k][1] for k in combo]):
            continue
        labs = [sp[k][0] for k in combo]
        vanishing.append(labs)
        if any(sp[k][2] is None for k in combo):
            full_involved += 1
            violations.append(labs)          # L(n) forbids a full factor
            continue
        if not is_common_coordinate([sp[k][2] for k in combo]):
            violations.append(labs)
    return dict(n=n, n_spaces=len(sp), n_multisets_tested=tested,
                n_vanishing=len(vanishing),
                n_vanishing_involving_the_full_space=full_involved,
                vanishing_sample=vanishing[:8],
                n_violations_of_L=len(violations), violations=violations[:6])


def check_S3():
    """per_3 == 0 on <a> x Y x Z, a all-nonzero, dim Y,Z >= 2."""
    sp = spaces_for(3)
    us = [u for u in product((1, -1), repeat=3) if u[0] == 1]
    us += [(1, 2, 3), (2, -3, 5), (1, 1, 7), (6, 3, 2)]
    tested = 0
    bad = []
    for u in us:
        for combo in combinations_with_replacement(range(len(sp)), 2):
            tested += 1
            bases = [[list(u)]] + [sp[k][1] for k in combo]
            if per_vanishes_on_product(bases):
                bad.append(dict(u=list(u),
                                spaces=[sp[k][0] for k in combo]))
    return dict(n_u=len(us), n_tested=tested, n_vanishing=len(bad),
                witnesses=bad[:6])


def symbolic_S3():
    import sympy as sp
    a1, a2, a3, y1, y2, y3, z1, z2, z3 = sp.symbols(
        "a1 a2 a3 y1 y2 y3 z1 z2 z3")
    a = [a1, a2, a3]
    y = [y1, y2, y3]
    z = [z1, z2, z3]
    P = sp.expand(per([a, y, z]))
    S = sp.Matrix([[sp.expand(sp.diff(P, y[i], z[j])) for j in range(3)]
                   for i in range(3)])
    return dict(bilinear_matrix=[[str(S[i, j]) for j in range(3)]
                                 for i in range(3)],
                determinant=str(sp.factor(S.det())),
                equals_2a1a2a3=(sp.simplify(S.det() - 2 * a1 * a2 * a3) == 0),
                note="S is invertible whenever 2*a1*a2*a3 != 0, so a plane Z "
                     "has dim S(Z) = 2 > 1 and per_3 cannot vanish on "
                     "<a> x Y x Z; in characteristic 2 det S = 0 and the "
                     "argument (and P4c) genuinely fail")


def p4c_big_u():
    cand = sign_reps(4)
    bases = [kernel_basis(nv) for nv in cand]
    us = [u for u in product((1, -1, 2, -2), repeat=4) if u[0] > 0]
    tested = 0
    bad = []
    for u in us:
        ul = list(u)
        for combo in combinations_with_replacement(range(len(cand)), 3):
            tested += 1
            B = [bases[k] for k in combo]
            van = True
            for idx in product(range(3), repeat=3):
                if per([ul] + [B[j][idx[j]] for j in range(3)]):
                    van = False
                    break
            if van:
                bad.append(dict(u=ul, normals=[list(cand[k]) for k in combo]))
    return dict(n_u=len(us), n_tested=tested, n_vanishing=len(bad),
                witnesses=bad[:6])


def main():
    res = {"_header": "A7 SUB-AUDIT -- extra checks for the corrected proof "
                      "and a larger P4c stratum.  Exact only."}
    for n in (3, 4):
        res["L_n%d" % n] = check_L(n)
        print("L(%d):" % n, res["L_n%d" % n], flush=True)
    res["S3_exhaustive"] = check_S3()
    print("S3:", res["S3_exhaustive"], flush=True)
    res["S3_symbolic"] = symbolic_S3()
    print("S3 symbolic:", res["S3_symbolic"], flush=True)
    res["P4c_big_u"] = p4c_big_u()
    print("P4c big-u stratum:", res["P4c_big_u"], flush=True)
    json.dump(res, open(os.path.join(HERE, "a7_results_A1_extra.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
