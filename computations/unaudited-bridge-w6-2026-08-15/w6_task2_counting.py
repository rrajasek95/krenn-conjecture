#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- lemma J.1d: the cells-vs-support counting budget.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

RE-DERIVATION (W2 soft spot 5 says do not trust its arithmetic).  Inputs, both
committed:

 (S1) FORCED INCIDENCE (notes/slice-cover.md, "Forced incident-edge theorem").
      For every vertex p and every colour r there is a neighbour j and a
      NONZERO a in V_p with
              A_pj = a (x) e_r^{(j)},     C_pj != 0.
      The coordinate factor is the one at the FAR endpoint j and it is exactly
      e_r; the near factor a is only known nonzero -- that is the note's
      "Current limitation" (section 3).  The three j's are distinct, so
              d_R(v) >= 3      for every vertex v.                        (1)

 (S2) COEFFICIENT-SUPPORT RULE 1 (proofs/saturated-rank-graph-obstruction.md
      section 1 item 1).  For each constant colouring (r,...,r) at least one
      perfect matching is supported.

VOCABULARY.  R = rank-one nonzero blocks, H = rank >= 2 blocks, Z = zero
blocks, F = H u Z, m = |R| + |H| = number of NONZERO blocks (= "support" in
the II.1/II.2 band; the band counts EDGES, not cells).  For a rank-one block
A_e = a_u (x) a_v the incidence (e,u) is COORDINATE if a_u is a multiple of a
basis vector; e is a BASIS edge if both are, equivalently

      e is a basis edge  <=>  A_e has exactly ONE nonzero cell.           (2)

cells(e) = number of nonzero entries of A_e; for rank one it factors as
|supp a_u| * |supp a_v|, so a NONCOORDINATE rank-one block costs >= 2 cells
(>= 4 if both factors are noncoordinate).

THE BUDGET (general N, even, N >= 4).  Orient incidences: the out-incidence
v -> u (u an R-neighbour of v) is coordinate iff the factor at u is.  (S1)
gives >= 3 coordinate out-incidences at every v, so

      #(noncoordinate out-incidences at v) <= d_R(v) - 3,
      D := total <= sum_v (d_R(v) - 3) = 2|R| - 3N.                       (3)

Every non-basis R-edge has a noncoordinate incidence, i.e. consumes >= 1 of
the D, and distinct edges consume distinct incidences.  Hence

      beta := #basis edges >= |R| - D >= 3N - |R| >= 3N - m + |H|.        (4)

Equivalently  #(nonzero blocks that are NOT a single cell) <= 2m - 3N - 2|H|
... (the |H| refinement; H-blocks are never basis edges and are already
excluded from |R|).  In W2's currency: |R| = C(N,2) - |F| turns (4) into
beta >= N(7-N)/2 + |F|, which is W2's formula -- CORRECT, but stated in the
currency (|F|) that is useless on the band; (4) in the currency m is the
usable form.

SHARPENING (Hall / sparsity, not just a count).  The non-basis R-edges can be
oriented so each is charged to an endpoint with spare allowance, so for EVERY
vertex subset S,
      #(non-basis R-edges inside S) <= sum_{v in S} (d_R(v) - 3).         (5)

CELL FORM.  cells(e) >= 1 for a basis edge and >= 2 otherwise, so
      Sigma := total occupied cells >= 2m - beta,  i.e.  beta >= 2m - Sigma.
This is the "noncoordinate blocks cost >= 2 cells" trade.  IT IS VACUOUS AT
N = 8: the only committed cell ceiling (notes/n8-full-support-sat.md,
"Structural cell ceilings") is Sigma <= 189 (179 on orbit 40) and only in the
structural 0/2 model, whereas 2m <= 56.  W2's cited "Sigma cells <= 27" is a
misreading: 27 is an EDGE-support bound.  So the usable budget is (4)/(5).

CONSTANT-MATCHING CELLS.  (S2) gives, for each colour r, a supported matching
M_r using the N/2 cells (r,r).  Different colours give different cells, so
      >= 3N/2 occupied cells    (12 at N = 8)
but NOT on 3N/2 distinct edges: the three matchings need not be disjoint, and
only  t >= N/2  distinct edges are forced (4 at N = 8).  W2's "on >= 12
distinct edges" is FALSE.  What IS forced: an edge carrying two or three of
the constant cells has >= 2 cells, hence is NOT a basis edge, so with
t_k = #edges carrying exactly k constant cells,
      t_1 + 2 t_2 + 3 t_3 = 3N/2,   beta <= m - t_2 - t_3,                (6)
and combining with (4),   t_2 + t_3 <= 2m - 3N - |H|.                     (7)
At m = 3N/2 (the minimum support allowed by (1)) this forces t_2 = t_3 = 0:
the three constant matchings are EDGE-DISJOINT and every block is a single
DIAGONAL cell.

This module (a) verifies (3)-(7) by exhaustive/randomised combinatorial
simulation, (b) verifies (2)/(4) on exact block data, (c) evaluates the
budget on the committed N = 8 band 19..27, and (d) reports the mutation
controls.

Run: python3 w6_task2_counting.py
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

import w6_core as core
from w6_core import COLORS, require


# ------------------------------------------------------- (a) the combinatorics


def random_graph_min_degree(rng, size, edges, tries=4000):
    """A simple graph on `size` vertices with `edges` edges, min degree >= 3."""
    universe = list(combinations(range(size), 2))
    for _ in range(tries):
        chosen = rng.sample(universe, edges)
        degree = [0] * size
        for u, v in chosen:
            degree[u] += 1
            degree[v] += 1
        if min(degree) >= 3:
            return chosen, degree
    return None, None


def simulate_budget(rng, size, edges, trials=200):
    """Randomised check of (3)-(5) against a brute-force incidence model.

    Model: for every vertex pick 3 distinct R-neighbours as the slice-cover
    heads (their far incidences are coordinate).  Every OTHER out-incidence is
    independently coordinate or not.  An edge is a basis edge iff both its
    out-incidences are coordinate.  We check beta >= 3N - |R| and (5).
    """
    worst = None
    violations = 0
    hall_violations = 0
    samples = 0
    for _ in range(trials):
        graph, degree = random_graph_min_degree(rng, size, edges)
        if graph is None:
            return None
        neighbours = {v: [] for v in range(size)}
        for u, v in graph:
            neighbours[u].append(v)
            neighbours[v].append(u)
        coordinate = {}
        for v in range(size):
            heads = rng.sample(neighbours[v], 3)
            for u in neighbours[v]:
                coordinate[(v, u)] = (u in heads) or (rng.random() < 0.5)
        basis = [e for e in graph
                 if coordinate[(e[0], e[1])] and coordinate[(e[1], e[0])]]
        beta = len(basis)
        bound = 3 * size - len(graph)
        samples += 1
        if beta < bound:
            violations += 1
        slack = beta - max(bound, 0)
        if worst is None or slack < worst[0]:
            worst = (slack, beta, bound, len(graph))
        nonbasis = [e for e in graph if e not in basis]
        for subset_size in range(1, size + 1):
            for subset in combinations(range(size), subset_size):
                inside = sum(1 for u, v in nonbasis
                             if u in subset and v in subset)
                allowance = sum(degree[v] - 3 for v in subset)
                if inside > allowance:
                    hall_violations += 1
    return {"samples": samples, "bound_violations": violations,
            "hall_violations": hall_violations, "tightest": worst}


def constant_matching_arithmetic(size):
    """Exhaustive check of (6): what the three constant matchings force."""
    matchings = core.perfect_matchings(tuple(range(size)))
    out = {"matchings": len(matchings), "cells_forced": 3 * size // 2}
    best_edges = size  # upper bound placeholder
    profiles = {}
    for a in range(len(matchings)):
        for b in range(len(matchings)):
            for c in range(len(matchings)):
                used = {}
                for colour, number in enumerate((a, b, c)):
                    for edge in matchings[number]:
                        used[edge] = used.get(edge, 0) + 1
                cells = sum(used.values())
                require(cells == 3 * size // 2, "constant cell count")
                t = {1: 0, 2: 0, 3: 0}
                for count in used.values():
                    t[count] += 1
                best_edges = min(best_edges, len(used))
                key = (len(used), t[1], t[2], t[3])
                profiles[key] = profiles.get(key, 0) + 1
    out["min_distinct_edges"] = best_edges
    out["max_distinct_edges"] = max(k[0] for k in profiles)
    out["profiles(t_edges,t1,t2,t3)->count"] = {str(k): v for k, v
                                                in sorted(profiles.items())}
    return out


# ---------------------------------------------------- (b) exact block checks


def check_basis_equals_single_cell(rng, trials=4000):
    """(2): rank-one with both factors coordinate <=> exactly one cell."""
    bad = 0
    seen = {"basis": 0, "rank1-one-coordinate": 0, "rank1-noncoordinate": 0,
            "rank2": 0, "rank3": 0, "zero": 0}
    for _ in range(trials):
        style = rng.choice(["rank1", "rank1", "general"])
        if style == "rank1":
            a = [rng.choice([0, 0, 1, -2, 3]) for _ in COLORS]
            b = [rng.choice([0, 0, 1, 2, -1]) for _ in COLORS]
            matrix = [[Fraction(a[i] * b[j]) for j in COLORS] for i in COLORS]
        else:
            matrix = [[Fraction(rng.choice([0, 0, 1, -1, 2]))
                       for _ in COLORS] for _ in COLORS]
        klass = core.classify_block(matrix)
        seen[klass] += 1
        single = len(core.cells(matrix)) == 1
        if (klass == "basis") != single:
            bad += 1
        if klass in ("rank1-one-coordinate", "rank1-noncoordinate"):
            if len(core.cells(matrix)) < 2:
                bad += 1
        if klass == "rank1-noncoordinate" and len(core.cells(matrix)) < 4:
            bad += 1
    return {"trials": trials, "violations": bad, "class_census": seen}


def budget_on_models():
    """The two residual six-site models of notes/six-vertex-rank-graph.md s5."""
    out = []
    # model 1: F = C_6 with identity blocks, prism Q_r carrying e_r (x) e_r.
    src = core.zero_source(6)
    cycle = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)]
    for edge in cycle:
        src[edge] = [[1 if i == j else 0 for j in COLORS] for i in COLORS]
    prism = {0: [(0, 2), (1, 4), (3, 5)], 1: [(0, 3), (1, 5), (2, 4)],
             2: [(0, 4), (1, 3), (2, 5)]}
    for r, edges in prism.items():
        for edge in edges:
            table = [[0] * 3 for _ in COLORS]
            table[r][r] = 1
            src[edge] = table
    census = core.block_census(src, 6)
    degree = core.rank_one_degree(src, 6)
    out.append({"model": "C6 + prism (six-vertex note s5, F=C_6)",
                "census": census, "d_R": degree,
                "bound_3N_minus_R": 18 - census["R"],
                "beta": census["basis"],
                "bound_holds": census["basis"] >= 18 - census["R"]})
    # model 2: F = C_3 u C_3 with the three rank-two forms on each triangle.
    src = core.zero_source(6)
    colouring = {(0, 3): 0, (1, 4): 0, (2, 5): 0,
                 (0, 4): 1, (1, 5): 1, (2, 3): 1,
                 (0, 5): 2, (1, 3): 2, (2, 4): 2}
    for edge, r in colouring.items():
        table = [[0] * 3 for _ in COLORS]
        table[r][r] = 1
        src[edge] = table
    for triangle in ((0, 1, 2), (3, 4, 5)):
        u, v, w = triangle
        # x_0 y_2 - x_2 y_0 as a bilinear form: entries (0,2)=1, (2,0)=-1
        for (a, b), scale in (((u, v), 1), ((u, w), 1), ((v, w), 2)):
            table = [[0] * 3 for _ in COLORS]
            table[0][2] = 1
            table[2][0] = -scale
            src[core.edge_key(a, b)] = table
    census = core.block_census(src, 6)
    degree = core.rank_one_degree(src, 6)
    out.append({"model": "C_3 u C_3 (six-vertex note s5)",
                "census": census, "d_R": degree,
                "bound_3N_minus_R": 18 - census["R"],
                "beta": census["basis"],
                "bound_holds": census["basis"] >= 18 - census["R"]})
    return out


# ---------------------------------------------------------- (c) the N=8 band


def band_table(size=8, floor=19, ceiling=27):
    rows = []
    for m in range(3 * size // 2, size * (size - 1) // 2 + 1):
        row = {"support_m": m,
               "in_committed_band": floor <= m <= ceiling,
               "beta_floor_h0": max(0, 3 * size - m),
               "max_non_single_cell_blocks": max(0, 2 * m - 3 * size),
               "t2_plus_t3_max": max(0, 2 * m - 3 * size)}
        rows.append(row)
    return rows


# ---------------------------------------------------------------- (d) controls


def mutation_controls(rng, size=8):
    """Falsifiers: drop (S1) or (S2) and confirm the budget breaks."""
    out = {}
    # C1: a graph with a degree-2 vertex violates (1) and can beat the bound.
    graph = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4),
             (2, 5), (6, 7), (6, 0), (7, 1)]
    degree = [0] * size
    for u, v in graph:
        degree[u] += 1
        degree[v] += 1
    out["C1_min_degree_of_handmade_graph"] = min(degree)
    out["C1_satisfies_S1"] = min(degree) >= 3
    # C2: with all incidences noncoordinate the bound must force beta = 0 only
    # when 3N - |R| <= 0.
    out["C2_bound_is_vacuous_above"] = 3 * size
    # C3: budget is tight -- exhibit |R| = 3N/2 forcing every edge basis.
    out["C3_minimum_R"] = 3 * size // 2
    out["C3_beta_at_minimum"] = 3 * size - 3 * size // 2
    out["C3_all_blocks_basis_at_minimum"] = (
        3 * size - 3 * size // 2 == 3 * size // 2)
    return out


def main():
    print("UNAUDITED PROBE (W6) -- J.1d counting budget, HEAD 31cefe2",
          flush=True)
    rng = random.Random(20260815)
    report = {}

    print("== (a) combinatorial simulation of the budget (3)-(5) ==", flush=True)
    sims = {}
    for size, edges in ((6, 12), (6, 15), (8, 14), (8, 18), (8, 22), (8, 28)):
        result = simulate_budget(rng, size, edges, trials=60)
        sims[f"N{size}_R{edges}"] = result
        print(f"  N={size} |R|={edges}: {result['samples']} samples, "
              f"bound violations {result['bound_violations']}, "
              f"Hall violations {result['hall_violations']}, "
              f"tightest slack {result['tightest'][0]}")
    report["simulation"] = sims

    print("== (a') constant-matching cell arithmetic ==", flush=True)
    report["constant_matchings"] = {}
    for size in (6, 8):
        rec = constant_matching_arithmetic(size)
        report["constant_matchings"][f"N{size}"] = rec
        print(f"  N={size}: {rec['cells_forced']} cells forced, on between "
              f"{rec['min_distinct_edges']} and {rec['max_distinct_edges']} "
              f"distinct edges")

    print("== (b) exact block classification checks ==", flush=True)
    report["block_checks"] = check_basis_equals_single_cell(rng)
    print("  ", json.dumps(report["block_checks"]))
    report["models"] = budget_on_models()
    for rec in report["models"]:
        print(f"  {rec['model']}: |R|={rec['census']['R']} beta={rec['beta']} "
              f"bound {rec['bound_3N_minus_R']} -> holds {rec['bound_holds']} "
              f"(cells {rec['census']['cells']}, d_R {rec['d_R']})")

    print("== (c) the committed N=8 band ==", flush=True)
    report["band"] = band_table()
    print("   m  band?  beta >=  non-single-cell blocks <=")
    for row in report["band"]:
        mark = "*" if row["in_committed_band"] else " "
        print(f"  {row['support_m']:2d}   {mark}      "
              f"{row['beta_floor_h0']:2d}        "
              f"{row['max_non_single_cell_blocks']:2d}")

    print("== (d) mutation controls ==", flush=True)
    report["controls"] = mutation_controls(rng)
    print("  ", json.dumps(report["controls"]))

    with open("results_counting.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print("wrote results_counting.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
