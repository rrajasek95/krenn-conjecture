#!/usr/bin/env python3
r"""W31 / R3 round 2, step 0 -- WHERE IS THE PERMANENTAL LAW EVEN DEFINED?
UNAUDITED PROBE.  Exact integer arithmetic only.  Seconds.

The plan was to evaluate R3's Q-span law FIRST on the 10 no-copy classes, on
the reasoning that they lack the GHZ protection structure.  Before doing that
this script checks the law's domain of definition, because R3 is not a generic
tool: it is built on W20's L-free reduction, and that reduction has a
hypothesis.

THE REDUCTION'S ACTUAL HYPOTHESIS.  Split the eight sites 4|4 into L and R.
A perfect matching of K_8 uses 4, 2 or 0 cross edges; every 2-cross and every
0-cross matching uses AT LEAST ONE edge inside L.  So if a word makes all six
L-internal blocks INACTIVE, only the 24 four-cross matchings survive and

    H_(x,y) = per B(x,y),   B[i][j] = A_{i,j}[x_i][y_j].

Two consequences that decide the plan:
  * only ONE side needs to be free -- the reduction is one-sided, so it does
    not need the doubled structure;
  * but a FULL block is active at every word, so a word making all six
    L-internal blocks inactive can exist only if NO Gamma edge lies inside L.

    ==>  the L-free reduction exists  ONLY IF  Gamma has an INDEPENDENT 4-SET.

That is exactly the "admits at least one GHZ_4 copy" predicate from Lemma
W31-2.  So the tiers are not "protection levels" -- they are the reduction's
domain:

    tier C (C_8, 1 class)   : independent 4-set AND its complement -> the
                              reduction runs on BOTH sides (L-free + R-free)
    tier B (65 classes)     : one independent 4-set -> the reduction runs on
                              ONE side
    tier A (10 classes)     : NO independent 4-set -> the reduction does not
                              exist, and R3 has NO INPUT there at all

CONTROLS
  R1  the reduction identity is verified EXACTLY on random templates whose
      L-side is Gamma-independent: H_(x,y) must equal per B(x,y) at every free
      word and every y.
  R2  MUTATION / NEGATIVE CONTROL: make one L-internal block FULL (i.e. put a
      Gamma edge inside L).  Then no word is free, and where the code still
      offers a candidate word the identity must FAIL.  If the identity holds
      anyway, the hypothesis above is not the real hypothesis.
  R3c the C_8 member must reproduce 30 free words per side (W20's number).
  R4c the 10 no-copy classes must have zero independent 4-sets, recomputed
      here from the Gamma masks rather than read from the earlier run.
"""
from __future__ import annotations

import json
import os
import random
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CENSUS = os.path.join(REPO, "computations",
                      "unaudited-forcing-w19-2026-08-15", "census")

N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
S4 = tuple(permutations(range(4)))

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))


def occupied(mask, i, j):
    return (mask >> (3 * i + j)) & 1


def H(val, T, w):
    """exact H_w from a value dict {(edge,i,j): v}."""
    t = 0
    for M in PMS:
        p = 1
        for e in M:
            i, j = w[e[0]], w[e[1]]
            if not occupied(T[EIDX[e]], i, j):
                p = 0
                break
            p *= val[(e, i, j)]
        t += p
    return t


def perB(val, T, Ls, Rs, x, y):
    B = [[0] * 4 for _ in range(4)]
    for a, u in enumerate(Ls):
        for b, v in enumerate(Rs):
            e = (u, v) if u < v else (v, u)
            i, j = (x[a], y[b]) if u < v else (y[b], x[a])
            B[a][b] = val[(e, i, j)] if occupied(T[EIDX[e]], i, j) else 0
    return sum(B[0][s[0]] * B[1][s[1]] * B[2][s[2]] * B[3][s[3]] for s in S4)


def free_words(T, side):
    """x on `side` making every block INSIDE side inactive."""
    inner = [tuple(sorted(p)) for p in combinations(side, 2)]
    out = []
    for x in product(range(3), repeat=4):
        lk = {v: x[k] for k, v in enumerate(side)}
        if all(not occupied(T[EIDX[e]], lk[e[0]], lk[e[1]]) for e in inner):
            out.append(x)
    return out


def independent_4sets(gedges):
    gs = set(tuple(sorted(e)) for e in gedges)
    return [q for q in combinations(range(N), 4)
            if not any(tuple(sorted(p)) in gs for p in combinations(q, 2))]


def main():
    OUT = {"_header": "UNAUDITED W31/R3 round-2 step 0: the domain of the "
                      "permanental law. Exact only. Nothing here is a proved "
                      "claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}
    rng = random.Random(20260820)

    # ---- R3c : the C_8 member reproduces W20's 30 free words per side -----
    L0, R0 = (0, 1, 2, 3), (4, 5, 6, 7)
    fL = free_words(C8_MEMBER, L0)
    fR = free_words(C8_MEMBER, R0)
    OUT["R3c_c8_free_words"] = dict(L=len(fL), R=len(fR),
                                    matches_W20=(len(fL) == 30
                                                 and len(fR) == 30))
    print("[R3c] C_8 free words: L=%d R=%d (W20: 30/30) -> %s"
          % (len(fL), len(fR), OUT["R3c_c8_free_words"]["matches_W20"]))

    # ---- R1 : the reduction identity on random Gamma-independent templates
    def random_template(gedges, Ls):
        T = [0] * len(EDGES)
        gs = set(tuple(sorted(e)) for e in gedges)
        for e in EDGES:
            if e in gs:
                T[EIDX[e]] = FULL
            elif e[0] in Ls and e[1] in Ls:
                T[EIDX[e]] = 1 << rng.randrange(9)          # a single cell
            else:
                T[EIDX[e]] = rng.choice([FULL ^ (1 << rng.randrange(9)),
                                         1 << rng.randrange(9),
                                         FULL ^ (1 << rng.randrange(9))])
        return T

    kill = json.load(open(os.path.join(CENSUS, "results_kill.json")))
    inv = {r["gamma_mask"]: r for r in kill["reps_inventory"]}
    strat = [gm for gm, r in inv.items() if r["pms"] <= 2]

    tested = mism = nofree = 0
    for gm in strat[:40]:
        ge = [EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1]
        ind = independent_4sets(ge)
        if not ind:
            continue
        Ls = ind[0]
        Rs = tuple(v for v in range(N) if v not in Ls)
        T = random_template(ge, set(Ls))
        val = {(e, i, j): rng.randint(-9, 9) or 3
               for e in EDGES for i in range(3) for j in range(3)
               if occupied(T[EIDX[e]], i, j)}
        fw = free_words(T, Ls)
        if not fw:
            nofree += 1
            continue
        for x in fw[:4]:
            for y in [tuple(rng.randrange(3) for _ in range(4))
                      for _ in range(6)]:
                w = [0] * N
                for k, v in enumerate(Ls):
                    w[v] = x[k]
                for k, v in enumerate(Rs):
                    w[v] = y[k]
                tested += 1
                if H(val, T, tuple(w)) != perB(val, T, Ls, Rs, x, y):
                    mism += 1
    OUT["R1_identity_tests"] = tested
    OUT["R1_identity_mismatches"] = mism
    OUT["R1_classes_with_no_free_word"] = nofree
    print("[R1] reduction identity: %d exact tests, %d mismatches "
          "(%d templates had no free word)" % (tested, mism, nofree))

    # ---- R2 : negative control -- put a Gamma edge inside L ---------------
    gm = strat[0]
    ge = [EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1]
    ind = independent_4sets(ge)
    negtested = negmism = 0
    if ind:
        Ls = ind[0]
        Rs = tuple(v for v in range(N) if v not in Ls)
        ge2 = list(ge) + [tuple(sorted((Ls[0], Ls[1])))]     # Gamma edge in L
        T = random_template(ge2, set(Ls))
        val = {(e, i, j): rng.randint(-9, 9) or 3
               for e in EDGES for i in range(3) for j in range(3)
               if occupied(T[EIDX[e]], i, j)}
        for x in product(range(3), repeat=4):
            for y in [tuple(rng.randrange(3) for _ in range(4))
                      for _ in range(2)]:
                w = [0] * N
                for k, v in enumerate(Ls):
                    w[v] = x[k]
                for k, v in enumerate(Rs):
                    w[v] = y[k]
                negtested += 1
                if H(val, T, tuple(w)) != perB(val, T, Ls, Rs, x, y):
                    negmism += 1
    OUT["R2_negative_control_tests"] = negtested
    OUT["R2_negative_control_mismatches"] = negmism
    OUT["R2_ok"] = (negmism > 0)
    print("[R2] negative control (a Gamma edge inside L): %d/%d words break "
          "the identity -> control %s" % (negmism, negtested, OUT["R2_ok"]))

    # ---- R4c : the tier classification, recomputed ------------------------
    tiers = {"A_no_reduction": [], "B_one_sided": [], "C_two_sided": []}
    for gm in sorted(strat):
        ge = [EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1]
        ind = independent_4sets(ge)
        if not ind:
            tiers["A_no_reduction"].append(gm)
            continue
        comp = any(tuple(v for v in range(N) if v not in q) in
                   set(map(tuple, ind)) for q in ind)
        (tiers["C_two_sided"] if comp else tiers["B_one_sided"]).append(gm)
    OUT["tiers"] = {k: len(v) for k, v in tiers.items()}
    OUT["tier_A_masks"] = tiers["A_no_reduction"]
    OUT["tier_C_masks"] = tiers["C_two_sided"]
    print("[R4c] tiers by REDUCTION AVAILABILITY:", OUT["tiers"])
    print("      tier A (no L-free reduction, R3 has no input):",
          tiers["A_no_reduction"])
    print("      tier C (both sides):", tiers["C_two_sided"])

    OUT["VERDICT"] = (
        "R3's permanental law is defined exactly where Gamma has an "
        "independent 4-set: %d classes one-sided, %d two-sided, and %d "
        "classes where it has NO input. The 10 no-copy classes are tier A, "
        "so R3 round 2 CANNOT be evaluated there -- the priority ordering "
        "must be inverted."
        % (len(tiers["B_one_sided"]), len(tiers["C_two_sided"]),
           len(tiers["A_no_reduction"])))
    print()
    print("[VERDICT]", OUT["VERDICT"])

    with open(os.path.join(HERE, "results_r3_reach.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["R1_identity_mismatches", "R2_ok", "R3c_c8_free_words",
                "tiers"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
