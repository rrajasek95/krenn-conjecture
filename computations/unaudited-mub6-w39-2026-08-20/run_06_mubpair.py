"""W39-T1 extra calibration (must-UNSAT at the QUADRUPLE layer):

Brierley-Weigert (https://arxiv.org/abs/0901.4051) report that the 48 vectors
MU to {I, F_6} form exactly 16 second Hadamard bases and that NO TWO of those
16 are mutually unbiased to each other -- which is what caps the F_6 chain at
three MUBs.  This script re-derives that statement with certified interval
arithmetic on the exact Krawczyk boxes.

Two bases B_p, B_q (index sets of certified fibre points) are mutually
unbiased iff, for every cross pair (p,q),
      |<v_p, v_q>|^2 = 1/6   <=>   A(p,q)^2 + 3 B(p,q)^2 = 54,
with A, B as in run_05 (sanity: the self value is A=18, B=0, giving
A^2+3B^2 = 324 and |<v,v>|^2 = 1).  If for SOME cross pair the enclosure of
A^2 + 3B^2 - 54 EXCLUDES zero, the two bases are CERTIFIED not mutually
unbiased.  One-sided and sound in the direction we need.

Running this on F_6 is a genuine must-UNSAT control: a pipeline that reports
a mutually unbiased pair among the 16 is broken.
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "realroot"))

from isolate import Iv                                        # noqa: E402
from mub_systems import fibre_system, F6_EXP, S6_EXP          # noqa: E402
from run_05_t1_clique import (parse_gens, propose, certify_all,  # noqa: E402
                              AB_enclosures, disjoint, find_cliques)


def pair_is_certified_not_MU(boxes, C1, C2):
    """Return (certified_not_MU, n_cross_pairs_excluding_54)."""
    n_excl = 0
    for p in C1:
        for q in C2:
            A, B = AB_enclosures(boxes[p], boxes[q])
            val = A * A + Iv(3) * B * B - Iv(54)
            if not val.contains_zero():
                n_excl += 1
    return n_excl > 0, n_excl


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "F6"
    exp, order, n_real = {"F6": (F6_EXP, 6, 48), "S6": (S6_EXP, 3, None)}[tag]
    if n_real is None:
        n_real = json.load(open(os.path.join(HERE,
                            "results_t1b_S6_viewA.json")))["n_real"]
    gens, _ = fibre_system(exp, order)
    sysm = parse_gens(gens)
    approx, _ = propose(sysm, n_real, seed=0)
    boxes, failed = certify_all(sysm, approx)
    ok_disj, _ = disjoint(boxes)
    complete = (len(boxes) == n_real and ok_disj)
    print(f"[{tag}] certified {len(boxes)}/{n_real} boxes, complete={complete}",
          flush=True)
    if not complete:
        print("UNCHECKED: enumeration not provably complete")
        sys.exit(1)
    n = len(boxes)
    adj = {i: set() for i in range(n)}
    for i, j in itertools.combinations(range(n), 2):
        A, B = AB_enclosures(boxes[i], boxes[j])
        if A.contains_zero() and B.contains_zero():
            adj[i].add(j)
            adj[j].add(i)
    cliques = find_cliques(adj, n, 6, cap=500)
    print(f"[{tag}] candidate 6-cliques (second bases): {len(cliques)}",
          flush=True)
    rec = {"tag": tag, "n_boxes": n, "n_cliques": len(cliques),
           "cliques": [list(c) for c in cliques], "pairs": []}
    all_not_mu = True
    for a, b in itertools.combinations(range(len(cliques)), 2):
        cert, n_excl = pair_is_certified_not_MU(boxes, cliques[a], cliques[b])
        rec["pairs"].append({"i": a, "j": b, "certified_not_MU": cert,
                             "n_cross_pairs_excluding": n_excl})
        if not cert:
            all_not_mu = False
    rec["all_pairs_certified_not_MU"] = all_not_mu
    rec["n_basis_pairs"] = len(rec["pairs"])
    print(f"[{tag}] basis pairs tested: {rec['n_basis_pairs']}; "
          f"ALL certified NOT mutually unbiased: {all_not_mu}", flush=True)
    with open(os.path.join(HERE, f"results_t3_mubpair_{tag}.json"), "w") as fh:
        json.dump(rec, fh, indent=2, default=str)
    print("CONTROL MANIFEST OK: executed [certify, cliques, basis_pair_MU_test]")
    if tag == "F6" and not all_not_mu:
        print("CALIBRATION FAILURE: F6 must have NO mutually unbiased pair "
              "among its 16 second bases")
        sys.exit(1)


if __name__ == "__main__":
    main()
