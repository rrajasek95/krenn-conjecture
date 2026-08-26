#!/usr/bin/env python3
r"""W31 -- COMPLETION AND RE-VERIFICATION of the R2-gate witness.
UNAUDITED PROBE.  Exact integer arithmetic only.

WHY THIS EXISTS (a self-caught defect, recorded rather than quietly fixed).
`w31_r2gate.py` built the two-word witness by writing ONLY the rows x_i and
x'_i of the cross blocks, leaving every other entry at 0.  Its control G3
checked "all used cells nonzero" -- but the target W31-6a demands that EVERY
occupied cross cell be nonzero.  With unwritten rows left at zero the witness
did not meet the target's hypothesis, and worse, `w31_r3_qspan.py`'s control
Q5 then reported that all 30 L-free words were satisfied -- VACUOUSLY, because
words using an unwritten row see B = 0.  That is exactly the ledger-17 failure
mode (a condition satisfied because the object degenerated, not because the
mechanism worked), caught by a control that was put in to catch it.

THE REPAIR IS SOUND AND CHEAP.  per B(x,y) reads only row x_i of each cross
block A_{i,j}, so filling the OTHER rows with arbitrary nonzero values cannot
disturb the two words' conditions.  This script fills every remaining occupied
cell of the whole template with a nonzero value and re-verifies everything.

CONTROLS
  W1  every occupied cell of the template (all 148) is nonzero, and every
      unoccupied cell is zero.
  W2  the two words (0,2,1,0) and (0,2,1,1) still satisfy all 81 permanent
      equations each -- 162 equations, exact.
  W3  the OTHER 28 L-free words must now show violations; if they did not,
      the object would be far stronger than claimed and the claim would need
      restating.  (This is the control that catches the vacuity of W3's
      pre-repair version.)
  W4  the mirror R-free conditions are measured too -- reported, not assumed.
  W5  the full exact-source status: how many of the 6,558 mixed equations the
      object satisfies.  It is NOT a counterexample unless that is 6,558 with
      the three constants nonzero; reported honestly either way.
  W6  MUTATION: perturbing one used cell must break at least one of the 162.
"""
from __future__ import annotations

import json
import os
import random
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
L, R = (0, 1, 2, 3), (4, 5, 6, 7)
S4 = tuple(permutations(range(4)))
PMS = None

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def per4(M):
    return sum(M[0][s[0]] * M[1][s[1]] * M[2][s[2]] * M[3][s[3]] for s in S4)


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


def main():
    global PMS
    PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))
    OUT = {"_header": "UNAUDITED W31 witness completion + re-verification. "
                      "Exact integer arithmetic only. Nothing here is a "
                      "proved claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}
    rng = random.Random(31415)
    occ = {e: set(cells_of(C8_MEMBER[EIDX[e]])) for e in EDGES}
    cross_occ = {(i, j): occ[(i, j)] for i in L for j in R}

    # ---- build the witness on the two words' rows -------------------------
    AB = ((1, 1), (1, 2), (2, 1))
    SIGN = {4: (1, 1, 1, 1), 5: (1, 1, -1, -1), 6: (1, 1, 1, 1),
            7: (1, 1, 1, 1)}
    PAT = (0, 1, 1, 0)
    XW = ((0, 2, 1, 0), (0, 2, 1, 1))
    A = {(i, j): [[0] * 3 for _ in range(3)] for i in L for j in R}
    written = set()
    for x in XW:
        for j in R:
            for d in range(3):
                a, b = AB[d]
                z = frozenset(i for i in L if (x[i], d) not in cross_occ[(i, j)])
                if z == frozenset({0, 3}):
                    a = 0
                elif z == frozenset({1, 2}):
                    b = 0
                for i in L:
                    A[(i, j)][x[i]][d] = SIGN[j][i] * (a if PAT[i] == 0 else b)
                    written.add((i, j, x[i], d))

    # ---- the repair: fill every remaining occupied cell with a nonzero ----
    filled = 0
    for i in L:
        for j in R:
            for (r, c) in sorted(cross_occ[(i, j)]):
                if (i, j, r, c) not in written:
                    A[(i, j)][r][c] = rng.randint(1, 20)
                    filled += 1
    OUT["cells_filled_by_repair"] = filled
    print("[repair] occupied cross cells filled with nonzero values:", filled)

    # full template values (the 12 L/R single cells too, for W1)
    val = {}
    for e in EDGES:
        for (r, c) in sorted(occ[e]):
            if e[0] in L and e[1] in R:
                val[(e, r, c)] = A[(e[0], e[1])][r][c]
            else:
                val[(e, r, c)] = rng.randint(1, 20)

    # ---- W1 ---------------------------------------------------------------
    w1a = all(v != 0 for v in val.values())
    w1b = all(A[(i, j)][r][c] == 0 for i in L for j in R
              for r in range(3) for c in range(3)
              if (r, c) not in cross_occ[(i, j)])
    OUT["W1_all_occupied_nonzero"] = w1a
    OUT["W1_all_unoccupied_zero"] = w1b
    OUT["W1_n_occupied_cells"] = len(val)
    print("[W1] occupied cells:", len(val), " all nonzero:", w1a,
          " unoccupied cross cells zero:", w1b)

    # ---- L-free words and the permanent conditions ------------------------
    lsing = {}
    for (u, v) in combinations(L, 2):
        mk = C8_MEMBER[EIDX[(u, v)]]
        if bin(mk).count("1") == 1:
            lsing[(u, v)] = cells_of(mk)[0]
    rsing = {}
    for (u, v) in combinations(R, 2):
        mk = C8_MEMBER[EIDX[(u, v)]]
        if bin(mk).count("1") == 1:
            rsing[(u, v)] = cells_of(mk)[0]
    lfree = [x for x in product(range(3), repeat=4)
             if all(not (x[u] == i and x[v] == j)
                    for (u, v), (i, j) in lsing.items())]
    rfree = [y for y in product(range(3), repeat=4)
             if all(not (y[u - 4] == i and y[v - 4] == j)
                    for (u, v), (i, j) in rsing.items())]

    def Bm(x, y):
        return [[A[(i, R[j])][x[i]][y[j]] for j in range(4)] for i in range(4)]

    tally = {}
    for x in lfree:
        tally[tuple(x)] = sum(1 for y in product(range(3), repeat=4)
                              if per4(Bm(x, y)) != 0)
    OUT["W2_violations_at_the_two_target_words"] = {
        str(list(x)): tally[x] for x in XW}
    OUT["W2_both_words_fully_satisfied"] = all(tally[x] == 0 for x in XW)
    others = {str(list(x)): tally[x] for x in lfree if x not in XW}
    OUT["W3_other_Lfree_words_violations"] = others
    OUT["W3_n_other_words_with_violations"] = sum(1 for v in others.values()
                                                  if v > 0)
    print("[W2] violations at the two target words:",
          OUT["W2_violations_at_the_two_target_words"],
          " both satisfied:", OUT["W2_both_words_fully_satisfied"])
    print("[W3] of the other 28 L-free words,",
          OUT["W3_n_other_words_with_violations"], "now show violations")

    # ---- W4 : the mirror -------------------------------------------------
    rt = {}
    for y in rfree:
        rt[str(list(y))] = sum(1 for x in product(range(3), repeat=4)
                               if per4(Bm(x, y)) != 0)
    OUT["W4_Rfree_violations"] = rt
    OUT["W4_n_Rfree_satisfied"] = sum(1 for v in rt.values() if v == 0)
    print("[W4] R-free (mirror) words fully satisfied:",
          OUT["W4_n_Rfree_satisfied"], "of", len(rfree))

    # ---- W5 : the full mixed system --------------------------------------
    def H(w):
        t = 0
        for M in PMS:
            p = 1
            for e in M:
                r, c = w[e[0]], w[e[1]]
                if (r, c) not in occ[e]:
                    p = 0
                    break
                p *= val[(e, r, c)]
            t += p
        return t
    mixed = [w for w in product(range(3), repeat=N) if len(set(w)) > 1]
    nz = sum(1 for w in mixed if H(w) != 0)
    consts = [H((c,) * N) for c in range(3)]
    OUT["W5_mixed_equations_violated"] = nz
    OUT["W5_mixed_equations_satisfied"] = len(mixed) - nz
    OUT["W5_constant_values_nonzero"] = [v != 0 for v in consts]
    OUT["W5_is_an_exact_source"] = (nz == 0 and all(v != 0 for v in consts))
    print("[W5] mixed equations satisfied: %d of %d ; constants nonzero: %s ;"
          " IS AN EXACT SOURCE: %s"
          % (len(mixed) - nz, len(mixed), OUT["W5_constant_values_nonzero"],
             OUT["W5_is_an_exact_source"]))

    # ---- W6 : mutation ----------------------------------------------------
    i0, j0, r0, d0 = sorted(written)[0]
    A[(i0, j0)][r0][d0] += 1
    mut = all(sum(1 for y in product(range(3), repeat=4)
                  if per4(Bm(x, y)) != 0) == 0 for x in XW)
    A[(i0, j0)][r0][d0] -= 1
    OUT["W6_mutation_breaks_a_target_word"] = (not mut)
    print("[W6] mutation control fires:",
          OUT["W6_mutation_breaks_a_target_word"])

    OUT["GATE_VERDICT_W31_6a_refuted"] = bool(
        OUT["W2_both_words_fully_satisfied"] and w1a and w1b)
    print()
    print("[GATE] W31-6a (two L-free words, all occupied cross cells "
          "nonzero) is REFUTED by an explicit exact witness:",
          OUT["GATE_VERDICT_W31_6a_refuted"])

    with open(os.path.join(HERE, "results_witness.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["W1_all_occupied_nonzero", "W1_all_unoccupied_zero",
                "W2_both_words_fully_satisfied",
                "W3_n_other_words_with_violations", "W4_n_Rfree_satisfied",
                "W5_is_an_exact_source", "W6_mutation_breaks_a_target_word"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
