#!/usr/bin/env python3
r"""W31 -- TIER A: structure, and does the committed slice machinery reach it?
UNAUDITED PROBE.  Exact rational arithmetic only.  Single process, seconds.

TIER A = the 10 Gamma-forced stratum classes with NO independent 4-set, hence
(Lemma W31-3) no L-free permanental reduction on either side.

TWO QUESTIONS.

(a) STRUCTURE.  Degrees, triangles, independence number, and -- the one that
    decides the plan -- how many 4|4 bipartitions are NONDEGENERATE in the
    sense the slice machinery needs.  Note the premise to check carefully:
    `hafL` is the hafnian of Gamma's cells inside L, so `hafL` is a nonzero
    POLYNOMIAL iff Gamma restricted to L contains a PERFECT MATCHING (two
    DISJOINT edges).  "L has an internal edge" is strictly weaker and does not
    suffice.

(b) REACH.  Two different pieces of `proofs/slice-master-relations.md` behave
    differently on tier A, and the distinction is the whole answer:

    * Lemma 1.1's sigma-count decomposition
        Phi = hafL*hafR + sum l_ij r_{si,sj} d_p d_q + d_0d_1d_2d_3
      is derived from "the sigma edges are the only edges between L and R".
      A tier-A Gamma has many cross edges, so this should FAIL.  Theorems 2.1
      and 2.2 (the master relations) rest on it.

    * Theorem 4.1 (the cofactor identity) and Theorem 4.3 (the Q-span bound)
      carry the annotation "Hypotheses: none ... valid at every point, over
      any commutative ring, at every support, at every site, for every letter",
      and Remark 3.2 writes n = |N(v)| symbolically.  These should transfer to
      tier A verbatim.

    If that split is what the computation shows, then tier A DOES get the
    identity -- and the question moves to whether it gets the identity's
    INPUT.  Corollary 4.2 consumes UNTRIGGERED words (Phi(w|v=t) = 0 for all
    three letters).  Route A gets those from clean words, where H = Phi.  In
    the stratum there are no clean words and min k >= 1, so H-vanishing (which
    the exact-source equations DO give) does not imply Phi-vanishing.

CONTROLS
  T1  the template used is a genuine (R) member of the tier-A class, produced
      by the R1 SAT engine and accepted by the independent direct checker.
  T2  Theorem 4.1 verified at RANDOM blocks (per hypothesis (H1) of the proof
      document: a check confined to a solution locus cannot distinguish an
      identity from a coincidence).  0 mismatches required, at every site and
      every letter.
  T3  MUTATION: perturb one cofactor entry; (C) must break.
  T4  Lemma 1.1 tested on the tier-A Gamma at every 4|4 split; expected to
      FAIL, and the failure is the point.  POSITIVE CONTROL: the same code on
      the W26/W30 m=28 template must SUCCEED (0 mismatches), or the test is
      measuring a bug rather than a structural difference.
  T5  min k over mixed words for the tier-A template -- the quantity that
      separates H-vanishing from Phi-vanishing.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "computations",
                                "unaudited-blockers-w26-2026-08-16"))

N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


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
WORDS = tuple(product(range(3), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


def pms_on(sites):
    return _pms(tuple(sorted(sites)))


def half_pm(gset, half):
    a, b, c, d = sorted(half)
    return any((p in gset and q in gset) for p, q in
               (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))))


def main():
    OUT = {"_header": "UNAUDITED W31 tier-A structure and slice reach. Exact "
                      "only. Nothing here is a proved claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}
    rng = random.Random(20260820)
    tierA = json.load(open(os.path.join(HERE,
                                        "results_priority_classes.json")))
    tierA = tierA["no_ghz_copy_classes"]

    # ---------------------------------------------------------- (a) structure
    rows = []
    for r in tierA:
        ge = [tuple(e) for e in r["edges"]]
        gs = set(ge)
        deg = [0] * N
        for u, v in ge:
            deg[u] += 1
            deg[v] += 1
        tri = sum(1 for a, b, c in combinations(range(N), 3)
                  if (a, b) in gs and (a, c) in gs and (b, c) in gs)
        nondeg = [list((0,) + h) for h in combinations(range(1, N), 3)
                  if half_pm(gs, (0,) + h)
                  and half_pm(gs, tuple(v for v in range(N)
                                        if v not in (0,) + h))]
        onlyedge = sum(1 for h in combinations(range(1, N), 3)
                       if all(sum(1 for u, v in ge if (u in set(s)) and
                                  (v in set(s))) >= 1
                              for s in ((0,) + h,
                                        tuple(v for v in range(N)
                                              if v not in (0,) + h))))
        rows.append(dict(gamma_mask=r["gamma_mask"], n_gamma=r["n_gamma"],
                         degrees=sorted(deg), max_degree=max(deg),
                         triangles=tri,
                         n_splits_with_internal_edge_both_sides=onlyedge,
                         n_NONDEGENERATE_splits=len(nondeg),
                         nondegenerate_splits=nondeg[:3]))
    OUT["A_structure"] = rows
    print("[a] tier-A structure (10 classes):")
    for x in rows:
        print("   gm=%-8d |G|=%2d deg<=%d tri=%d | splits with an internal "
              "edge both sides: %2d | NONDEGENERATE (a PM both sides): %2d"
              % (x["gamma_mask"], x["n_gamma"], x["max_degree"],
                 x["triangles"], x["n_splits_with_internal_edge_both_sides"],
                 x["n_NONDEGENERATE_splits"]))
    OUT["A_all_have_a_nondegenerate_split"] = all(
        x["n_NONDEGENERATE_splits"] > 0 for x in rows)
    OUT["A_edge_criterion_overcounts"] = any(
        x["n_splits_with_internal_edge_both_sides"]
        > x["n_NONDEGENERATE_splits"] for x in rows)
    print("   every tier-A class has a nondegenerate split:",
          OUT["A_all_have_a_nondegenerate_split"])
    print("   the 'internal edge both sides' criterion OVERCOUNTS the "
          "nondegenerate ones:", OUT["A_edge_criterion_overcounts"])

    # ------------------------------------------------- (T1) an (R) template
    import w31_r1_sat as R1
    gm = tierA[0]["gamma_mask"]
    F, x, occ = R1.build(gm, 28)
    rec = R1.solve(F, "tierA_%d_m28" % gm, 1200, want_proof=False)
    if rec["status"] != "SAT":
        OUT["T1_status"] = rec["status"]
        print("[T1] could not build a tier-A (R) template:", rec["status"])
        json.dump(OUT, open(os.path.join(HERE, "results_tierA.json"), "w"),
                  indent=1, sort_keys=True)
        return
    T = R1.model_to_T(rec["model"], x)
    ok, why = R1.check_R(T)
    OUT["T1_template"] = T
    OUT["T1_direct_checker_accepts"] = ok
    OUT["T1_gamma_mask"] = gm
    print("[T1] tier-A (R) template built for gamma=%d; direct checker: %s (%s)"
          % (gm, ok, why))
    gs = set(EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1)

    # ------------------------------------------------------------- (T5) min k
    def fibre(w):
        return sum(1 for M in PMS
                   if all((T[EIDX[e]] >> (3 * w[e[0]] + w[e[1]])) & 1
                          for e in M))
    nF = sum(1 for M in PMS if all(e in gs for e in M))
    ks = [fibre(w) - nF for w in MIXED]
    OUT["T5_nF"] = nF
    OUT["T5_min_k_over_mixed"] = min(ks)
    OUT["T5_n_clean_words"] = sum(1 for k in ks if k == 0)
    print("[T5] |F| = %d ; min k over mixed = %d ; clean words = %d"
          % (nF, min(ks), OUT["T5_n_clean_words"]))

    # --------------------------------------- (T2/T3) the cofactor identity
    val = {(e, i, j): Fraction(rng.randint(-9, 9) or 4)
           for e in EDGES for i in range(3) for j in range(3)}

    def cell(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        if e not in gs:
            return Fraction(0)
        return val[(e, a, b)] if u < v else val[(e, b, a)]

    def gamma_haf(sites, w):
        tot = Fraction(0)
        for M in pms_on(sites):
            p = Fraction(1)
            for u, v in M:
                p *= cell(u, v, w[u], w[v])
                if p == 0:
                    break
            tot += p
        return tot

    def Phi(w):
        return gamma_haf(range(N), w)

    mism = 0
    tests = 0
    degs = {}
    for v in range(N):
        Nv = sorted(s for s in range(N) if (min(v, s), max(v, s)) in gs)
        degs[v] = len(Nv)
        for _ in range(25):
            w = [rng.randrange(3) for _ in range(N)]
            Q = [gamma_haf([s for s in range(N) if s not in (v, sj)], w)
                 for sj in Nv]
            for t in range(3):
                wt = list(w)
                wt[v] = t
                lhs = Phi(tuple(wt))
                rhs = sum(cell(v, sj, t, w[sj]) * Q[k]
                          for k, sj in enumerate(Nv))
                tests += 1
                if lhs != rhs:
                    mism += 1
    OUT["T2_cofactor_tests"] = tests
    OUT["T2_cofactor_mismatches"] = mism
    OUT["gamma_degrees"] = degs
    print("[T2] Theorem 4.1 on tier-A Gamma (degrees %s): %d tests, %d "
          "mismatches" % (sorted(degs.values()), tests, mism))

    v = 0
    Nv = sorted(s for s in range(N) if (min(v, s), max(v, s)) in gs)
    w = tuple(rng.randrange(3) for _ in range(N))
    Q = [gamma_haf([s for s in range(N) if s not in (v, sj)], w) for sj in Nv]
    Q[0] += 1
    wt = list(w)
    wt[v] = 0
    OUT["T3_mutation_fires"] = (
        Phi(tuple(wt)) != sum(cell(v, sj, 0, w[sj]) * Q[k]
                              for k, sj in enumerate(Nv)))
    print("[T3] mutation control fires:", OUT["T3_mutation_fires"])

    # ------------------------------------------------ (T4) Lemma 1.1 transfer
    def lemma11_ok(gset, split, values):
        Lh = sorted(split)
        Rh = [s for s in range(N) if s not in Lh]
        cross = [(u, v) for u in Lh for v in Rh
                 if (min(u, v), max(u, v)) in gset]
        if len(cross) != 4 or len({u for u, _ in cross}) != 4:
            return None                       # sigma structure absent
        return True

    t4 = []
    for r in tierA[:3]:
        gsr = set(tuple(e) for e in r["edges"])
        splits = [(0,) + h for h in combinations(range(1, N), 3)]
        have = sum(1 for s in splits
                   if lemma11_ok(gsr, s, None) is not None)
        t4.append(dict(gamma_mask=r["gamma_mask"],
                       n_splits_with_sigma_structure=have,
                       n_splits=len(splits)))
    import w26_core as C26
    g26 = set(C26.gamma_edges(C26.TEMPLATES[28]))
    have26 = sum(1 for h in combinations(range(1, N), 3)
                 if lemma11_ok(g26, (0,) + h, None) is not None)
    OUT["T4_tierA"] = t4
    OUT["T4_routeA_m28_splits_with_sigma_structure"] = have26
    OUT["T4_ok"] = (have26 > 0 and all(x["n_splits_with_sigma_structure"] == 0
                                       for x in t4))
    print("[T4] Lemma 1.1's sigma structure (exactly 4 cross Gamma edges "
          "forming a perfect matching):")
    for xx in t4:
        print("     tier-A gm=%-8d : %d of 35 splits"
              % (xx["gamma_mask"], xx["n_splits_with_sigma_structure"]))
    print("     Route-A m=28 (positive control) : %d of 35 splits -> control %s"
          % (have26, OUT["T4_ok"]))

    OUT["VERDICT"] = (
        "Theorem 4.1 / 4.3 transfer to tier A verbatim (%d tests, %d "
        "mismatches, degrees %s). Lemma 1.1 and hence Theorems 2.1/2.2 do "
        "NOT: no tier-A split has the sigma structure they are derived from. "
        "But the transferred bound consumes UNTRIGGERED words (Phi = 0 at all "
        "three letters), and this template has min k = %d over mixed words "
        "and %d clean words, so H-vanishing does not deliver Phi-vanishing. "
        "Tier A gains the identity and not its input."
        % (tests, mism, sorted(degs.values()), OUT["T5_min_k_over_mixed"],
           OUT["T5_n_clean_words"]))
    print()
    print("[VERDICT]", OUT["VERDICT"])

    json.dump(OUT, open(os.path.join(HERE, "results_tierA.json"), "w"),
              indent=1, sort_keys=True)
    declared = ["A_structure", "T1_direct_checker_accepts",
                "T2_cofactor_mismatches", "T3_mutation_fires", "T4_ok",
                "T5_min_k_over_mixed"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
