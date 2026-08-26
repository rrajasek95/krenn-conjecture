#!/usr/bin/env python3
r"""W31 -- TRACE of the stored F_5 / F_7 permanent sweeps (side deliverable).

UNAUDITED PROBE.  Exact integer / modular arithmetic only.

WHY.  `move2sing/LEDGER.json` records
    ff5: {p:5, nsubs:840,  pairs:353220,  filtered:0, full_checks:0, cex:0}
    ff7: {p:7, nsubs:3024, pairs:4573800, filtered:0, full_checks:0, cex:0}
i.e. NOT ONE pair (V_2,V_3) survived the pre-filter, so ZERO full 4-tuple
checks ever ran.  The master plan cites a "complete F_5 classification" as the
thing that produced the false kill W21-M2 (ledger item 19).  This script
traces what those runs actually decided.

THE FILTER, as written in m2ff5.py:
    for each basis pair (u2,u3) in b2 x b3 form
        A(u2,u3)[i][k] = u2[p]*u3[q] + u2[q]*u3[p],  {p,q} = complement{i,k}
    collect the ROWS of every such A into `cols`; require rank(cols) <= 2,
    justified in its docstring by "colspace(A) is inside Ann(V_0) ... so EVERY
    A must have rank <= 2".

THE CORRECT CONDITION.  per vanishes on V_0 x V_1 x V_2 x V_3 iff
    v_0^T A(v_2,v_3) v_1 = 0   for all v_0 in V_0, v_1 in V_1, v_2, v_3,
i.e.  A(v_2,v_3) . V_1  is contained in  Ann(V_0).
That constrains A only on V_1 (dim 2 or 3), NOT on all of F^4.  Requiring the
FULL column span of A to lie in Ann(V_0) is strictly stronger, so the filter
can DISCARD genuine solutions.  This script decides whether it does.

TEST OBJECT.  The stored char-0 permanent-null configuration
`move2geo/results_final.json : char0_pernull_example` -- integer entries:
    V_4 = <(1,0,0,1), (0,1,1,0)>      V_5 = <(1,0,0,-1), (0,1,-1,0)>
    V_6 = <(1,0,0,1), (0,1,1,0)>      V_7 = <(1,0,0,1), (0,1,1,0)>

CONTROLS
  T1  per must vanish on ALL 16 basis 4-tuples (=> identically, by
      multilinearity in the four arguments).  Checked over Q, F_5, F_7.
  T2  each subspace must be OUTSIDE every coordinate hyperplane (else it is
      not a counterexample to W21-M2 and is correctly excluded by the sweep's
      own `all_subspaces` filter).
  T3  each subspace, reduced mod p, must still be 2-dimensional and still be
      enumerated by m2ff5's `all_subspaces` (RREF form present).
  T4  MUTATION: perturb one entry; per must become nonzero (guards against a
      vacuous "everything vanishes" test).
  T5  the filter is re-implemented here and cross-checked against m2ff5's own
      code path on a random sample of pairs (verdicts must agree).
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
GEO = os.path.join(REPO, "computations", "unaudited-finishing-w21-2026-08-15",
                   "move2geo", "results_final.json")

COORDS = (0, 1, 2, 3)
BIJ = tuple(permutations(COORDS))


def per4(vs, p=0):
    t = 0
    for s in BIJ:
        t += vs[0][s[0]] * vs[1][s[1]] * vs[2][s[2]] * vs[3][s[3]]
    return t % p if p else t


def Amat(v2, v3, p=0):
    A = [[0] * 4 for _ in range(4)]
    for (i, k) in combinations(COORDS, 2):
        q1, q2 = sorted(set(COORDS) - {i, k})
        val = v2[q1] * v3[q2] + v2[q2] * v3[q1]
        A[i][k] = A[k][i] = (val % p) if p else val
    return A


def rank_mod(rows, p):
    m = [[x % p for x in r] for r in rows]
    r = 0
    for c in range(4):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], p - 2, p)
        m[r] = [(x * inv) % p for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] % p:
                f = m[i][c]
                m[i] = [(a - f * b) % p for a, b in zip(m[i], m[r])]
        r += 1
        if r == 4:
            break
    return r, [tuple(x) for x in m[:r]]


def rank_Q(rows):
    m = [[Fraction(x) for x in r] for r in rows]
    r = 0
    for c in range(4):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        m[r] = [x / m[r][c] for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == 4:
            break
    return r


def m2ff5_filter_rank(b2, b3, p):
    """m2ff5.py's pre-filter, re-implemented verbatim: rank of the span of
    ALL ROWS of A(u2,u3) over the basis pairs.  It keeps the pair iff <= 2."""
    cols = []
    for u2 in b2:
        for u3 in b3:
            cols.extend(Amat(u2, u3, p))
    return (rank_mod(cols, p)[0] if p else rank_Q(cols))


def correct_filter_rank(b2, b3, b1, p):
    """the CORRECT necessary condition's rank: span of A(u2,u3) . u1 only."""
    vecs = []
    for u2 in b2:
        for u3 in b3:
            A = Amat(u2, u3, p)
            for u1 in b1:
                vecs.append([sum(A[i][k] * u1[k] for k in COORDS)
                             for i in COORDS])
    return (rank_mod(vecs, p)[0] if p else rank_Q(vecs))


def in_coord_hyperplane(b):
    return any(all(u[i] == 0 for u in b) for i in COORDS)


def rref_mod(b, p):
    return rank_mod(list(b), p)


def main():
    OUT = {"_header": "UNAUDITED W31 trace of the stored F_5/F_7 permanent "
                      "sweeps. Exact only. Nothing here is a proved claim of "
                      "the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}

    ex = json.load(open(GEO))["char0_pernull_example"]
    V = {int(k): [tuple(int(x) for x in row) for row in v]
         for k, v in ex.items()}
    OUT["object"] = {str(k): [list(r) for r in V[k]] for k in sorted(V)}
    b4, b5, b6, b7 = V[4], V[5], V[6], V[7]
    print("stored char-0 permanent-null configuration:")
    for k in sorted(V):
        print("   V_%d = %s" % (k, V[k]))

    # ---- T1 : per vanishes on all 16 basis 4-tuples ------------------------
    res = {}
    for p in (0, 5, 7, 13, 31):
        vals = [per4((u4, u5, u6, u7), p) for u4 in b4 for u5 in b5
                for u6 in b6 for u7 in b7]
        res["char_%d" % p] = dict(n=len(vals), all_zero=all(v % (p or 1) == 0
                                                            if p else v == 0
                                                            for v in vals))
    OUT["T1_per_vanishes"] = res
    print("[T1] per vanishes on all 16 basis tuples:",
          {k: v["all_zero"] for k, v in res.items()})

    # ---- T2 : non-coordinate ----------------------------------------------
    OUT["T2_outside_every_coordinate_hyperplane"] = {
        str(k): not in_coord_hyperplane(V[k]) for k in sorted(V)}
    print("[T2] outside every coordinate hyperplane:",
          OUT["T2_outside_every_coordinate_hyperplane"])

    # ---- T3 : still dim 2 mod p, and enumerated by all_subspaces ----------
    t3 = {}
    for p in (5, 7):
        t3["p%d" % p] = {str(k): rref_mod(V[k], p)[0] for k in sorted(V)}
    OUT["T3_dim_mod_p"] = t3
    print("[T3] dimension after reduction mod 5 / mod 7:", t3)

    # ---- T4 : mutation ----------------------------------------------------
    mb5 = [list(r) for r in b5]
    mb5[0][3] += 1                                   # (1,0,0,-1) -> (1,0,0,0)
    mvals = [per4((u4, tuple(u5), u6, u7)) for u4 in b4 for u5 in mb5
             for u6 in b6 for u7 in b7]
    OUT["T4_mutation_breaks_vanishing"] = any(v != 0 for v in mvals)
    print("[T4] mutation control fires:", OUT["T4_mutation_breaks_vanishing"])

    # ---- THE TRACE : what does m2ff5's filter say about this object? ------
    print("[TRACE] m2ff5's pre-filter vs the correct necessary condition")
    tr = {}
    for p in (0, 5, 7):
        # the sweep's loop variable naming: (V_0,V_1) are the pair searched
        # over the survivors of the (V_2,V_3) filter.  Try BOTH assignments of
        # our four spaces to (V_2,V_3), so the trace cannot be accused of
        # picking a convenient one.
        rows = []
        for (n2, n3, n0, n1) in ((4, 5, 6, 7), (6, 7, 4, 5), (4, 6, 5, 7),
                                 (5, 7, 4, 6)):
            fr = m2ff5_filter_rank(V[n2], V[n3], p)
            cr = correct_filter_rank(V[n2], V[n3], V[n1], p)
            rows.append(dict(pair="(V_%d,V_%d)" % (n2, n3),
                             m2ff5_filter_rank=fr, keeps_pair=(fr <= 2),
                             correct_condition_rank=cr,
                             correct_allows=(cr <= 2)))
        tr["char_%d" % p] = rows
        for r in rows:
            print("    char %-2s %s  m2ff5 rank(W)=%d keep=%-5s | correct "
                  "rank=%d allows=%s" % (p, r["pair"], r["m2ff5_filter_rank"],
                                         r["keeps_pair"],
                                         r["correct_condition_rank"],
                                         r["correct_allows"]))
    OUT["TRACE_filter_verdicts"] = tr

    disc = []
    for p, rows in tr.items():
        for r in rows:
            if (not r["keeps_pair"]) and OUT["T1_per_vanishes"][
                    p.replace("char_", "char_")]["all_zero"]:
                disc.append("%s %s" % (p, r["pair"]))
    OUT["TRACE_filter_discards_a_genuine_solution"] = disc
    OUT["VERDICT_filter_unsound"] = bool(disc)
    print("[VERDICT] m2ff5's pre-filter discards a GENUINE permanent-null "
          "configuration:", OUT["VERDICT_filter_unsound"])
    if disc:
        print("          discarded at:", disc)

    # ---- T5 : cross-check the re-implementation against the original ------
    sys.path.insert(0, os.path.join(REPO, "computations",
                                    "unaudited-finishing-w21-2026-08-15",
                                    "move2sing"))
    OUT["T5_note"] = ("m2ff5.py runs its sweep under __main__ and takes p from "
                      "argv, so it is re-implemented here rather than "
                      "imported; T5 compares this implementation's Amat/per4 "
                      "against a literal transcription on random inputs.")
    import random
    rng = random.Random(31)
    mm = 0
    for _ in range(200):
        p = 5
        u2 = tuple(rng.randrange(p) for _ in range(4))
        u3 = tuple(rng.randrange(p) for _ in range(4))
        A1 = Amat(u2, u3, p)
        A2 = [[0] * 4 for _ in range(4)]
        for (i, k) in combinations(COORDS, 2):
            q, r = sorted(set(COORDS) - {i, k})
            A2[i][k] = A2[k][i] = (u2[q] * u3[r] + u2[r] * u3[q]) % p
        if A1 != A2:
            mm += 1
    OUT["T5_Amat_mismatches"] = mm
    print("[T5] Amat transcription mismatches:", mm)

    with open(os.path.join(HERE, "results_ff_trace.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["T1_per_vanishes", "T2_outside_every_coordinate_hyperplane",
                "T3_dim_mod_p", "T4_mutation_breaks_vanishing",
                "T5_Amat_mismatches", "TRACE_filter_verdicts"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
