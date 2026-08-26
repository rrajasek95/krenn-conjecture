#!/usr/bin/env python3
"""T3 -- do the program's own hypotheses reach the Kruskal boundary? (UNAUDITED)

Reuses the COMMITTED checkers rather than re-deriving their objects:

  computations/verify_simultaneous_diagonal_flattening_palette_fusion_gate.py
  computations/verify_three_cut_cp_uniqueness_tight_boundary.py

T3.1  cut/shore factors of Delta_{4,3}: k-rank of every F_S over all 14
      oriented cuts, computed from the committed checker's own dense gauges.
T3.2  the decisive control: those same factors have MAXIMAL k-ranks and a
      Kruskal budget of 9 >= 8, and the fusion conclusion is nevertheless
      FALSE for them -- because the missing datum is the second CP
      decomposition (the fusion square), not the k-rank.
T3.3  per-site local CP factor matrices at the repo's six-site instance:
      k-ranks (1,1,3,3,3,3).  There the k-rank hypothesis genuinely fails.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))

import importlib.util
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from exactlin import (aligned_monomial, diagonal_embedding, factors_through,
                      khatri_rao, krank, mat, matmul, monomial_map, rank,
                      require, transpose)

COMPUTATIONS = Path(__file__).resolve().parents[1]
RESULTS = {}


def load(name):
    path = COMPUTATIONS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def banner(text):
    print("=" * 72)
    print(text)
    print("=" * 72)


GATE = "verify_simultaneous_diagonal_flattening_palette_fusion_gate.py"


def rebuild_committed_cut_factors(r=3):
    """Rebuild the committed checker's factorization of Delta_{4,3}: for each
    of the 7 unoriented cuts a dense Vandermonde-type gauge and its
    inverse-transpose on the complementary shore."""
    gate = load(GATE)
    sites = tuple(range(4))
    subsets = tuple(tuple(c) for size in range(1, len(sites))
                    for c in combinations(sites, size))
    gauges = {}
    order = []
    for shore in subsets:
        if shore in gauges:
            continue
        other = gate.complement(shore, sites)
        owner, mate = sorted((shore, other), key=gate.cut_mask)
        gauge = gate.varying_dense_gauge(len(order) + 1)
        gauges[owner] = gauge
        gauges[mate] = gate.inverse(gate.transpose(gauge))
        order.append((owner, mate))
    factors = {shore: [list(row) for row in
                       gate.multiply(gate.diagonal_embedding(len(shore)),
                                     gauges[shore])]
               for shore in subsets}
    return gate, subsets, gauges, factors


def t3_1_shore_factor_kranks():
    banner("T3.1  k-rank of every committed cut/shore factor of Delta_{4,3}")
    gate, subsets, gauges, factors = rebuild_committed_cut_factors()
    ledger = []
    for shore in subsets:
        F = factors[shore]
        G = [list(row) for row in gauges[shore]]
        kF, kG = krank(F), krank(G)
        require(rank(F) == 3, ("shore factor lost rank", shore))
        require(kF == 3, ("shore factor k-rank below 3", shore, kF))
        require(kG == 3, ("gauge k-rank below 3", shore, kG))
        ledger.append({"shore": shore, "rows": len(F), "rank": rank(F),
                       "krank": kF, "gauge_krank": kG,
                       "monomial": monomial_map(F, gate.diagonal_embedding(
                           len(shore))) is not None})
    print(f"  {len(ledger)} oriented shores (14 oriented cut factors of the 7 cuts):")
    print(f"  rank(F_S) = 3 and k-rank(F_S) = 3 for ALL of them.")
    print(f"  monomial shore factors among them: "
          f"{sum(1 for e in ledger if e['monomial'])} / {len(ledger)}")
    print("  Reason (note eq. (4)): F_S = D_S G_S with G_S in GL_3, and a")
    print("  3-column matrix has k-rank 3 exactly when it has full column rank.")
    print("  => the k-rank hypothesis is FREE for shore factors of any exact")
    print("     rank-3 cut factorization.  No minimum-support, occurrence-")
    print("     faithfulness or activity hypothesis is needed to obtain it,")
    print("     and none of them can strengthen it.")
    RESULTS["T3.1"] = {"shores": len(ledger),
                       "all_rank_3": all(e["rank"] == 3 for e in ledger),
                       "all_krank_3": all(e["krank"] == 3 for e in ledger),
                       "monomial_count": sum(1 for e in ledger if e["monomial"])}


def t3_2_kranks_are_not_the_obstruction():
    banner("T3.2  DECISIVE CONTROL: maximal k-ranks, Kruskal budget 9 >= 8, "
           "and the fusion conclusion still FALSE")
    gate, subsets, gauges, factors = rebuild_committed_cut_factors()
    tested = 0
    fused = 0
    monomial = 0
    for left in subsets:
        for right in subsets:
            if gate.cut_mask(left) >= gate.cut_mask(right):
                continue
            if set(left) & set(right):
                continue
            if len(set(left) | set(right)) == 4:
                continue
            A = factors[left]
            B = factors[right]
            U = diagonal_embedding(len(left))
            V = diagonal_embedding(len(right))
            kA, kB = krank(A), krank(B)
            budget = kA + kB + 3            # third factor is I_3
            require(kA == 3 and kB == 3, ("k-rank", left, right, kA, kB))
            require(budget >= 8, ("budget", budget))
            C = factors_through(A, B, U, V)
            omega = gate.rank_fraction(
                [[gauges[left][a][c] * gauges[right][b][c] for c in range(3)]
                 for a in range(3) for b in range(3) if a != b])
            tested += 1
            if C is not None:
                fused += 1
                if aligned_monomial(A, B, U, V) is not None:
                    monomial += 1
            require((C is not None) == (omega == 0),
                    ("square vs Omega disagree", left, right))
            require(omega > 0, ("committed counterguard lost its defect",
                                left, right))
    print(f"  {tested} disjoint proper shore pairs from the committed checker.")
    print(f"  every one: k_A = k_B = 3, Kruskal budget k_A+k_B+k_I = 9 >= 8.")
    print(f"  fusion squares that actually exist: {fused}")
    print(f"  monomially aligned pairs: {monomial}")
    print("  So the Kruskal k-rank condition is satisfied with slack while the")
    print("  fusion conclusion is FALSE for these factors.  There is no")
    print("  contradiction: Kruskal needs a SECOND decomposition of the same")
    print("  tensor, and that second decomposition IS the fusion square.")
    print("  Kruskal therefore CONSUMES the fusion square; it cannot supply it.")
    RESULTS["T3.2"] = {"pairs": tested, "kruskal_budget": 9,
                       "fusion_squares_existing": fused,
                       "monomial_pairs": monomial}


def t3_3_local_cp_factor_kranks():
    banner("T3.3  per-site local CP factor k-ranks at the repo's six-site "
           "instance")
    module = load("verify_three_cut_cp_uniqueness_tight_boundary.py")
    tensor = module.matching_tensor()
    words = tuple(tensor)
    kranks = []
    for vertex in module.VERTICES:
        columns = [[Fraction(int(k == word[vertex])) for k in range(3)]
                   for word in words]
        matrix = transpose([list(c) for c in columns])
        kranks.append(krank(matrix))
    print(f"  six-site output support: {sorted(words)}")
    print(f"  per-site local CP factor k-ranks: {kranks}   sum = {sum(kranks)}")
    require(kranks == [1, 1, 3, 3, 3, 3],
            ("local k-ranks changed", kranks))
    print("  Two sites have k-rank 1.  So at the LOCAL (per-site) CP factor")
    print("  level the program does NOT get k-rank 3 for free, and the repo's")
    print("  own note three-cut-cp-uniqueness-tight-boundary.md records this")
    print("  as the escape.  (Scope: that source's output is not Delta_{6,3};")
    print("  it is a counterguard, not a Krenn source.)")
    print("  The shore factors of T3.1 and these local factors are DIFFERENT")
    print("  matrices: the fusion square is about the former.")
    RESULTS["T3.3"] = {"local_kranks": kranks, "sum": sum(kranks)}


def main():
    t3_1_shore_factor_kranks()
    t3_2_kranks_are_not_the_obstruction()
    t3_3_local_cp_factor_kranks()
    banner("T3 VERDICT")
    print("  For the objects the fusion square is about (cut/shore factors),")
    print("  the k-rank hypothesis is automatic and therefore vacuous: it is")
    print("  supplied by eq. (4), not by minimum support or occurrence")
    print("  faithfulness.  Reaching the Kruskal boundary buys nothing, because")
    print("  the boundary was never the obstruction; the missing datum is the")
    print("  fusion square itself (provenance).")
    return RESULTS


if __name__ == "__main__":
    main()
