#!/usr/bin/env python3
r"""W31 / R3 -- the PERMANENTAL Q-SPAN LAW on the C_8 stratum member.
UNAUDITED PROBE.  Exact rational arithmetic only.  Single process, seconds.

THE TRANSPORT.  W30's cofactor identity is hafnian multilinearity and needs
clean words as input; the stratum has none.  W20's L-free reduction supplies
the substitute: for an L-free word x and EVERY y,

    H_(x,y) = per B(x,y),      B(x,y)[i][j] = A_{i,j}[x_i][y_j]     (4x4)

so 3,960 of the 6,558 mixed equations are pure permanent conditions on the 16
cross blocks.  Expanding per along column j (permanental cofactor expansion):

    per B(x,y) = sum_i B[i][j] * P_{i,j}(x, y|^j),
    P_{i,j} = per of the 3x3 minor with row i and column j deleted.

With C_j(x)[i][d] := A_{i,j}[x_i][d]  (4x3, so V^x_j = colspan C_j(x)),
setting y_j = 0,1,2 at a FIXED y|^j gives the three equations

    C_j(x)^T . P_j(x, y|^j) = 0,      P_j = (P_{0,j},...,P_{3,j}) in Q^4.

Hence  V^x_j  is contained in  P_j^perp  for every one of the 27 choices of
y|^j, so with  Pcal_j(x) := span{ P_j(x, y|^j) } :

    ***  rank C_j(x)  <=  4 - dim Pcal_j(x)   ***        (the Q-span law)

dim Pcal_j >= 2  =>  rank C_j <= 2   (W20's derived condition, uniformly);
dim Pcal_j >= 3  =>  rank C_j <= 1   (COLLAPSE: the row-x_i slices of the four
blocks at site j factor as u_i * lambda_d -- a factoring-site conclusion the
campaign's downstream machinery already consumes).

STRUCTURAL GIFT ON THIS TEMPLATE.  deg_Gamma(v) = 2 at every site and
Gamma - {v,s} is a path on 6 vertices, which has exactly ONE perfect matching,
so the Gamma-side cofactors are single monomials: nonzero as soon as the Gamma
cells are.  The "Q != 0" side condition that cost W30 several rounds is free.

CONTROLS
  Q1  the cofactor identity per B = sum_i B[i][j] P_{i,j} verified as an
      identity on random exact matrices, at every column j, with a MUTATION
      control that must fire.
  Q2  the law itself must hold at every object tested (rank C_j + dim Pcal_j
      <= 4).  A violation means the derivation is wrong.
  Q3  POSITIVE OBJECT: the R2-gate witness (satisfies the full 81-equation
      permanent condition at BOTH L-free words (0,2,1,0) and (0,2,1,1), all
      occupied cross cells nonzero).  Its ranks and spans are the first real
      measurement of the mechanism.
  Q4  NEGATIVE CONTROL: a generic all-nonzero assignment (not a solution) must
      give dim Pcal_j = 4, hence rank C_j <= 0 -- i.e. the law is violated
      unless the permanent equations hold.  This shows the constraint has
      content and is not an identity satisfied by everything (ledger 17: never
      decide a forcing question at a random specialisation -- here the random
      point is used ONLY as a negative control, never as evidence for a kill).
  Q5  the witness must FAIL the equations at the other 28 L-free words --
      otherwise it would be a far stronger object than claimed.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
N, Q3 = 8, 3
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
L, R = (0, 1, 2, 3), (4, 5, 6, 7)
S4 = tuple(permutations(range(4)))
S3 = tuple(permutations(range(3)))

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def per_n(M, n):
    idx = S4 if n == 4 else S3
    return sum(_prod(M[i][s[i]] for i in range(n)) for s in idx)


def _prod(it):
    t = 1
    for v in it:
        t *= v
    return t


def rank_Q(rows, ncol):
    m = [[Fraction(v) for v in r] for r in rows]
    r = 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [v / pv for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == ncol:
            break
    return r


def Bmat(A, x, y):
    return [[A[(i, R[j])][x[i]][y[j]] for j in range(4)] for i in range(4)]


def minor(M, i0, j0):
    return [[M[i][j] for j in range(4) if j != j0]
            for i in range(4) if i != i0]


def Pvec(A, x, yrest, j):
    """P_j(x, y|^j) in Q^4: the four permanental cofactors at column j."""
    y = [0] * 4
    k = 0
    for jj in range(4):
        if jj != j:
            y[jj] = yrest[k]
            k += 1
    out = []
    for i in range(4):
        M = Bmat(A, x, y)
        out.append(per_n(minor(M, i, j), 3))
    return out


def Cmat(A, x, j):
    return [[A[(i, R[j])][x[i]][d] for d in range(3)] for i in range(4)]


def main():
    OUT = {"_header": "UNAUDITED W31/R3 permanental Q-span law. Exact "
                      "rational arithmetic only. Nothing here is a proved "
                      "claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}
    cross = {(i, j): C8_MEMBER[EIDX[(i, j)]] for i in L for j in R}
    occ = {(i, j): set(cells_of(cross[(i, j)])) for i in L for j in R}

    # ---- Q1 : the cofactor identity ---------------------------------------
    rng = random.Random(20260820)
    bad = 0
    for _ in range(60):
        M = [[rng.randint(-9, 9) for _ in range(4)] for _ in range(4)]
        p = per_n(M, 4)
        for j in range(4):
            if sum(M[i][j] * per_n(minor(M, i, j), 3)
                   for i in range(4)) != p:
                bad += 1
    OUT["Q1_cofactor_identity_failures"] = bad
    Mm = [[rng.randint(1, 9) for _ in range(4)] for _ in range(4)]
    mutfire = (sum(Mm[i][0] * per_n(minor(Mm, i, 1), 3) for i in range(4))
               != per_n(Mm, 4))
    OUT["Q1_mutation_fires"] = mutfire
    print("[Q1] cofactor-identity failures:", bad, " mutation fires:", mutfire)

    # ---- build the R2-gate witness ----------------------------------------
    AB = ((1, 1), (1, 2), (2, 1))
    SIGN = {4: (1, 1, 1, 1), 5: (1, 1, -1, -1), 6: (1, 1, 1, 1),
            7: (1, 1, 1, 1)}
    PAT = (0, 1, 1, 0)
    XW = ((0, 2, 1, 0), (0, 2, 1, 1))

    def zeroset(x, j, d):
        return frozenset(i for i in L if (x[i], d) not in occ[(i, j)])

    A = {(i, j): [[0] * 3 for _ in range(3)] for i in L for j in R}
    for x in XW:
        for j in R:
            for d in range(3):
                a, b = AB[d]
                z = zeroset(x, j, d)
                if z == frozenset({0, 3}):
                    a = 0
                elif z == frozenset({1, 2}):
                    b = 0
                for i in L:
                    A[(i, j)][x[i]][d] = SIGN[j][i] * (a if PAT[i] == 0 else b)

    # ---- Q3/Q5 : the witness solves the two words, fails the others -------
    lsing = {}
    for (u, v) in combinations(L, 2):
        mk = C8_MEMBER[EIDX[(u, v)]]
        if bin(mk).count("1") == 1:
            lsing[(u, v)] = cells_of(mk)[0]
    lfree = [x for x in product(range(3), repeat=4)
             if all(not (x[u] == i and x[v] == jj)
                    for (u, v), (i, jj) in lsing.items())]
    solved, unsolved = [], []
    for x in lfree:
        viol = sum(1 for y in product(range(3), repeat=4)
                   if per_n(Bmat(A, x, y), 4) != 0)
        (solved if viol == 0 else unsolved).append((list(x), viol))
    OUT["Q3_words_fully_solved"] = [w for w, _ in solved]
    OUT["Q5_words_with_violations"] = len(unsolved)
    print("[Q3] L-free words whose full 81-equation condition holds:",
          OUT["Q3_words_fully_solved"])
    print("[Q5] L-free words with violations:", len(unsolved), "of", len(lfree))

    # ---- Q2/Q3 : the law at the witness -----------------------------------
    meas = {}
    for x in XW:
        for j in range(4):
            rows = [Pvec(A, x, yr, j) for yr in product(range(3), repeat=3)]
            dP = rank_Q(rows, 4)
            rC = rank_Q(list(zip(*Cmat(A, x, j))), 4)   # rank of the 4x3
            meas["x=%s,j=%d" % (list(x), R[j])] = dict(
                dim_Pcal=dP, rank_C=rC, law_holds=(rC + dP <= 4))
    OUT["Q3_measurements_at_witness"] = meas
    OUT["Q2_law_violations_at_witness"] = sum(
        1 for v in meas.values() if not v["law_holds"])
    for k in sorted(meas):
        print("    %-18s dim Pcal = %d , rank C = %d , law holds: %s"
              % (k, meas[k]["dim_Pcal"], meas[k]["rank_C"],
                 meas[k]["law_holds"]))
    print("[Q2] law violations at the witness:",
          OUT["Q2_law_violations_at_witness"])

    # ---- Q4 : negative control -- a generic all-nonzero assignment --------
    G = {(i, j): [[0] * 3 for _ in range(3)] for i in L for j in R}
    for i in L:
        for j in R:
            for (r, c) in occ[(i, j)]:
                G[(i, j)][r][c] = rng.randint(1, 30)
    gm = {}
    for x in XW:
        for j in range(4):
            rows = [Pvec(G, x, yr, j) for yr in product(range(3), repeat=3)]
            gm["x=%s,j=%d" % (list(x), R[j])] = dict(
                dim_Pcal=rank_Q(rows, 4),
                rank_C=rank_Q(list(zip(*Cmat(G, x, j))), 4))
    OUT["Q4_generic_control"] = gm
    OUT["Q4_generic_always_full_span"] = all(v["dim_Pcal"] == 4
                                             for v in gm.values())
    print("[Q4] generic all-nonzero point: dim Pcal =",
          sorted({v["dim_Pcal"] for v in gm.values()}),
          " (4 everywhere means the constraint has full content):",
          OUT["Q4_generic_always_full_span"])

    with open(os.path.join(HERE, "results_r3.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["Q1_cofactor_identity_failures", "Q1_mutation_fires",
                "Q2_law_violations_at_witness", "Q3_measurements_at_witness",
                "Q4_generic_control", "Q5_words_with_violations"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
