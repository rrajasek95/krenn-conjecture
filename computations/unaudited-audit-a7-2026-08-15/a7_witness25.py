#!/usr/bin/env python3
"""A7 -- the m=25 REFUTATION WITNESS.

Constructs an EXPLICIT exact rational point of the m=25 template with
  * every occupied cell nonzero,
  * every one of the 2,624 effectively-clean mixed equations H_w = 0 exact,
  * NO site factoring (all eight sites checked),
  * A14[0][.] constant and A14[1][.] NON-constant, i.e. squarely inside
    W19's "case 3" -- the case whose only resolution used the sign-flipped
    equations.
and verifies it with the independent A7 engine (both the direct fibre sum and
the subset DP).

Construction (derived by hand in REPORT.md):  in the Branch-B gauge take
  A03 = A25 = A07 = A45 = A47 = A23 = J (all-ones),  mu = nu = 1,
  A14 = [[1,1,1],[1,f,f],[1,1,1]],
  A56 columns 0 and 2 constant = -1, column 1 = (s0,s1,s2),
  A67 rows 0 and 2 = (1,1,1),      row 1 = (1,t1,t2),
and the L-blocks A01, A02, A12, A13 tuned so that P_L(x) = -1 on the 36
L-words whose clean box meets site-6 colour 1 (A13 rows 0 and 2 constant,
A02 columns 0,1 equal, A12 rows 0,2 columns 0,1 equal, A01 solved).
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, EDGES, EIDX, WORDS, MIXED, CONSTS, F_gamma,
                     k_of, fibre, H_value, H_value_dp, gamma_edges, PM_E,
                     cell_index)

HERE = os.path.dirname(os.path.abspath(__file__))
T25 = W8_IMMUNE[25]
FG25 = F_gamma(T25)

J = [[Fr(1)] * 3 for _ in range(3)]


def build(f=2, s=(1, 2, 3), t=(1, 2, 3)):
    B = {}
    for e in ((0, 3), (2, 5), (0, 7), (4, 5), (4, 7), (2, 3)):
        B[e] = [[Fr(1)] * 3 for _ in range(3)]
    B[(1, 4)] = [[Fr(1), Fr(1), Fr(1)],
                 [Fr(1), Fr(f), Fr(f)],
                 [Fr(1), Fr(1), Fr(1)]]
    B[(5, 6)] = [[Fr(-1), Fr(s[b]), Fr(-1)] for b in range(3)]
    B[(6, 7)] = [[Fr(1), Fr(1), Fr(1)],
                 [Fr(1), Fr(t[1]), Fr(t[2])],
                 [Fr(1), Fr(1), Fr(1)]]
    # ---- L-blocks: P_L(x) = -1 on the 36 words with x1 in {0,2}, x2 in {0,1}
    B[(1, 3)] = [[Fr(1), Fr(1), Fr(1)],
                 [Fr(1), Fr(1), Fr(2)],      # row 1 free
                 [Fr(1), Fr(1), Fr(1)]]
    B[(0, 2)] = [[Fr(1), Fr(1), Fr(5)],
                 [Fr(2), Fr(2), Fr(6)],
                 [Fr(3), Fr(3), Fr(7)]]
    B[(1, 2)] = [[Fr(1), Fr(1), Fr(4)],
                 [Fr(5), Fr(6), Fr(7)],      # row 1 free
                 [Fr(2), Fr(2), Fr(8)]]
    A01 = [[None] * 3 for _ in range(3)]
    for x0 in range(3):
        for x1 in (0, 2):
            A01[x0][x1] = Fr(-1) - B[(0, 2)][x0][0] * B[(1, 3)][x1][0] \
                          - B[(1, 2)][x1][0]
        A01[x0][1] = Fr(1)                    # free column
    B[(0, 1)] = A01
    A = {}
    for ei, e in enumerate(EDGES):
        if T25[ei] == 0:
            continue
        if T25[ei] == 511:
            for i in range(3):
                for j in range(3):
                    A[(ei, 3 * i + j)] = B[e][i][j]
        else:
            for c in range(9):
                if (T25[ei] >> c) & 1:
                    A[(ei, c)] = Fr(7)        # single cells: any nonzero value
    return A, B


def site_vectors(B, t):
    """(block, 3-vector at site t) for every Gamma block incident to t."""
    out = []
    for e in gamma_edges(T25):
        if t not in e:
            continue
        M = B[e]
        if e[0] == t:                      # site-t index is the ROW
            rows = [[M[i][j] for i in range(3)] for j in range(3)]
        else:                              # site-t index is the COLUMN
            rows = [[M[i][j] for j in range(3)] for i in range(3)]
        for v in rows:
            out.append((e, tuple(v)))
    return out


def factors(B, t):
    """site t factors iff every site-t vector of every Gamma block at t is
    parallel to a single common vector."""
    vs = [v for _, v in site_vectors(B, t)]
    vs = [v for v in vs if any(v)]
    base = vs[0]
    for v in vs[1:]:
        for i in range(3):
            for j in range(i + 1, 3):
                if base[i] * v[j] - base[j] * v[i] != 0:
                    return False
    return True


def check(A, B, label, single_val=None):
    res = dict(label=label)
    res["all_cells_nonzero"] = all(v != 0 for v in A.values())
    bad_clean, bad_dp = [], 0
    n_clean = 0
    for w in MIXED:
        if k_of(T25, w, FG25) != 0:
            continue
        n_clean += 1
        h = H_value(T25, w, A)
        if h != 0:
            bad_clean.append("".join(map(str, w)))
        if H_value_dp(T25, w, A) != h:
            bad_dp += 1
    res["n_clean_equations"] = n_clean
    res["n_clean_violated"] = len(bad_clean)
    res["clean_violations_sample"] = bad_clean[:5]
    res["engine_dp_mismatches"] = bad_dp
    res["constants_H"] = [str(H_value(T25, w, A)) for w in CONSTS]
    res["factoring_sites"] = [t for t in range(8) if factors(B, t)]
    res["n_mixed_violated"] = sum(1 for w in MIXED if H_value(T25, w, A) != 0)
    res["A14"] = [[str(v) for v in r] for r in B[(1, 4)]]
    res["A56"] = [[str(v) for v in r] for r in B[(5, 6)]]
    res["A67"] = [[str(v) for v in r] for r in B[(6, 7)]]
    res["A14_0_constant"] = len(set(B[(1, 4)][0])) == 1
    res["A14_1_constant"] = len(set(B[(1, 4)][1])) == 1
    return res


def main():
    out = {}
    A, B = build()
    r = check(A, B, "A7 m=25 case-3 witness")
    out["witness"] = r
    for k, v in r.items():
        print("%-26s %s" % (k, v))
    # MUTATION CONTROLS -----------------------------------------------------
    ctrl = {}
    # C1: break one derived relation -> clean equations must FAIL
    A2, B2 = build()
    B2[(5, 6)][1][0] = Fr(-3)            # A56[1][0] no longer constant column
    A2t = dict(A2)
    A2t[(EIDX[(5, 6)], 3 * 1 + 0)] = Fr(-3)
    ctrl["C1_perturb_A56"] = check(A2t, B2, "perturbed A56")["n_clean_violated"]
    # C2: a factoring choice must be DETECTED as factoring
    A3, B3 = build(f=1, s=(-1, -1, -1), t=(1, 1, 1))
    r3 = check(A3, B3, "degenerate all-factoring point")
    ctrl["C2_degenerate_factoring_sites"] = r3["factoring_sites"]
    ctrl["C2_clean_violated"] = r3["n_clean_violated"]
    # C3: vary the free parameters -- a whole family must work
    fam = []
    for f in (2, 3, -2):
        for s in ((1, 2, 3), (2, -1, 5)):
            for t in ((1, 2, 3), (1, -2, 4)):
                Ax, Bx = build(f=f, s=s, t=t)
                rx = check(Ax, Bx, "f=%s s=%s t=%s" % (f, s, t))
                fam.append(dict(f=f, s=list(s), t=list(t),
                                clean_violated=rx["n_clean_violated"],
                                factoring=rx["factoring_sites"],
                                nonzero=rx["all_cells_nonzero"],
                                consts=rx["constants_H"],
                                mixed_violated=rx["n_mixed_violated"]))
    ctrl["C3_family"] = fam
    out["controls"] = ctrl
    print("\nCONTROLS")
    print("C1 perturbed A56 -> clean violations:", ctrl["C1_perturb_A56"])
    print("C2 degenerate point factoring sites:",
          ctrl["C2_degenerate_factoring_sites"],
          "clean violations:", ctrl["C2_clean_violated"])
    for d in fam:
        print("C3", d)
    json.dump(out, open(os.path.join(HERE, "results_witness25.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
