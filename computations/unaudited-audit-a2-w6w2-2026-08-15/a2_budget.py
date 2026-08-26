#!/usr/bin/env python3
"""AUDIT A2 / claims A.1 and A.2 -- the budget and the m = 3N/2 corollary.

A.1  Combinatorial simulation of the slice-cover selection, testing
     (B)  beta >= 3N - m + |H|
     (H)  for every S: #(non-basis rank-one edges inside S)
                        <= sum_{v in S} (d_R(v) - 3)
     on adversarially-chosen extremal realisations, plus mutation controls
     (a selection with only TWO slots per vertex must break (B), and a
     deliberately wrong constant 3N+1 must be violated).

A.2  At m = 3N/2 the budget forces beta = m, |H| = 0, d_R(v) = 3; the three
     nonempty constant fibres then force the template to be three EDGE-DISJOINT
     diagonal perfect matchings, i.e. a properly 3-edge-coloured cubic graph.
     Here every such template at N = 8 is enumerated and counted for mixed
     singletons.
"""

from __future__ import annotations

import json
import random
from itertools import combinations

from a2_core import audit_template, geom, normalise_template
from a2_rcell_exhaust import MATCHINGS, perfect_matchings

N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


# ------------------------------------------------------------------- A.1


def simulate(rng, trials=4000, slots=3, constant=None):
    """Random support + slice-cover selection; check (B) and (H)."""
    constant = 3 * N if constant is None else constant
    violB = violH = 0
    tested = 0
    tight = 0
    for _ in range(trials):
        m = rng.randrange(12, 29)
        support = set(rng.sample(range(len(EDGES)), m))
        adj = {v: [] for v in range(N)}
        for i in support:
            u, v = EDGES[i]
            adj[u].append(i)
            adj[v].append(i)
        if any(len(adj[v]) < slots for v in range(N)):
            continue
        # a selection: every vertex picks `slots` distinct incident edges,
        # one per colour
        sel = {}                       # (vertex, colour) -> edge index
        ok = True
        for v in range(N):
            pick = rng.sample(adj[v], slots)
            for c, i in enumerate(pick):
                sel[(v, c)] = i
        if not ok:
            continue
        used = {}
        for (v, c), i in sel.items():
            used.setdefault(i, []).append((v, c))
        basis = {i for i, lst in used.items() if len(lst) == 2}
        rank_one = set(used)                       # every selected edge is R
        # extremal realisation: unselected edges are rank >= 2
        H = support - rank_one
        beta = len(basis)
        tested += 1
        if beta < constant - m + len(H):
            violB += 1
        if beta == constant - m + len(H):
            tight += 1
        # Hall
        dR = [0] * N
        for i in rank_one:
            u, v = EDGES[i]
            dR[u] += 1
            dR[v] += 1
        for size in range(1, N + 1):
            for S in combinations(range(N), size):
                Sset = set(S)
                inside = sum(1 for i in rank_one - basis
                             if EDGES[i][0] in Sset and EDGES[i][1] in Sset)
                allow = sum(dR[v] - 3 for v in S)
                if inside > allow:
                    violH += 1
                    break
    return {"tested": tested, "budget_violations": violB,
            "hall_violations": violH, "tight_cases": tight,
            "slots": slots, "constant": constant}


# ------------------------------------------------------------------- A.2


def disjoint_matching_triples():
    out = []
    for a in range(len(MATCHINGS)):
        sa = set(MATCHINGS[a])
        for b in range(len(MATCHINGS)):
            sb = set(MATCHINGS[b])
            if sa & sb:
                continue
            for c in range(len(MATCHINGS)):
                sc = set(MATCHINGS[c])
                if sa & sc or sb & sc:
                    continue
                out.append((a, b, c))
    return out


def main():
    rng = random.Random(20260815)
    report = {}
    report["A1_simulation"] = simulate(rng)
    print("A.1 simulation (3 slots per vertex, correct constant 3N):",
          report["A1_simulation"])
    report["A1_control_two_slots"] = simulate(rng, slots=2)
    print("A.1 mutation control (only TWO slots per vertex -- the budget "
          "should now FAIL sometimes):", report["A1_control_two_slots"])
    report["A1_control_wrong_constant"] = simulate(rng, constant=3 * N + 1)
    print("A.1 mutation control (constant 3N+1 -- must be violated):",
          report["A1_control_wrong_constant"])

    g = geom(N)
    triples = disjoint_matching_triples()
    print(f"A.2: ordered triples of pairwise disjoint perfect matchings of "
          f"K_8: {len(triples)}")
    worst = None
    cubic_ok = 0
    for a, b, c in triples:
        t = [frozenset() for _ in EDGES]
        for colour, mi in enumerate((a, b, c)):
            for e in MATCHINGS[mi]:
                t[EIDX[e]] = frozenset({(colour, colour)})
        rep = audit_template(g, normalise_template(g, t), exact=False)
        assert rep["m"] == 12 and rep["beta"] == 12
        deg = [0] * N
        for i, s in enumerate(t):
            if s:
                deg[EDGES[i][0]] += 1
                deg[EDGES[i][1]] += 1
        if min(deg) == max(deg) == 3:
            cubic_ok += 1
        if worst is None or rep["mixed_singletons"] < worst[0]:
            worst = (rep["mixed_singletons"], [a, b, c], rep["const_fibres"])
    print(f"A.2: all {len(triples)} are 3-regular: {cubic_ok == len(triples)}; "
          f"MINIMUM mixed singleton count over all of them: {worst[0]} "
          f"(witness triple {worst[1]}, constant fibres {worst[2]})")
    report["A2"] = {"triples": len(triples), "all_cubic": cubic_ok == len(triples),
                    "min_mixed_singletons": worst[0]}
    with open("results_budget.json", "w") as h:
        json.dump(report, h, indent=1, default=str)
    print("wrote results_budget.json")


if __name__ == "__main__":
    main()
