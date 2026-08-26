"""A7 TASK 1: every 8-edge spanning 2-connected graph on 8 labelled vertices
is a Hamilton cycle.  Brute force over all C(28,8) = 3108105 edge subsets.

Mutation controls:
  MC1-A  weaken the predicate to "spanning + connected" (drop 2-connectivity)
         -> the count must move away from 2520.
  MC1-B  corrupt each surviving witness by swapping one edge for a non-edge
         -> the corrupted graph must fail the predicate or fail 2-regularity.
  MC1-C  corrupt the vertex-deletion loop to skip vertex 0
         -> the count must move away from 2520.
"""

import itertools
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_A7_TASK1.json")


def spanning_connected(edge_idx):
    adj = C.adj_from_edgeidx(edge_idx)
    if any(adj[x] == 0 for x in range(8)):
        return False
    return C._connected_on(adj, 255)


def spanning_2conn_skip0(edge_idx):
    """MC1-C: deliberately broken -- never deletes vertex 0."""
    adj = C.adj_from_edgeidx(edge_idx)
    if any(adj[x] == 0 for x in range(8)):
        return False
    if not C._connected_on(adj, 255):
        return False
    for v in range(1, 8):
        if not C._connected_on(adj, 255 & ~(1 << v)):
            return False
    return True


def is_hamilton_cycle(edge_idx):
    """2-regular and connected  <=>  single spanning cycle."""
    d = C.degrees(edge_idx)
    if any(x != 2 for x in d):
        return False
    return spanning_connected(edge_idx)


def cycle_order(edge_idx):
    adj = {x: [] for x in range(8)}
    for ei in edge_idx:
        u, v = C.EDGES[ei]
        adj[u].append(v)
        adj[v].append(u)
    order = [0, adj[0][0]]
    while len(order) < 8:
        prev, cur = order[-2], order[-1]
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        order.append(nxt)
    return order


def main():
    t0 = time.time()
    n_2conn = 0
    n_2conn_not2reg = 0
    counterexamples = []
    n_connected = 0            # MC1-A tally
    n_skip0 = 0                # MC1-C tally
    witnesses = []
    total = 0
    for comb in itertools.combinations(range(28), 8):
        total += 1
        d = [0] * 8
        bad = False
        for ei in comb:
            u, v = C.EDGES[ei]
            d[u] += 1
            d[v] += 1
        if min(d) == 0:
            continue                       # cannot span
        sc = spanning_connected(comb)
        if sc:
            n_connected += 1
        if not sc:
            continue
        if spanning_2conn_skip0(comb):
            n_skip0 += 1
        if not C.spanning_2conn(comb):
            continue
        n_2conn += 1
        if not is_hamilton_cycle(comb):
            n_2conn_not2reg += 1
            if len(counterexamples) < 5:
                counterexamples.append([list(C.EDGES[e]) for e in comb])
        if len(witnesses) < 3:
            witnesses.append(list(comb))
    dt = time.time() - t0

    # ---- MC1-B: corrupt witnesses --------------------------------------
    mc1b = []
    for w in witnesses:
        cyc = cycle_order(w)
        rest = [e for e in range(28) if e not in w]
        mutated = sorted(w[1:] + [rest[0]])
        mc1b.append({
            "original_cycle": cyc,
            "original_is_2conn_and_2regular": bool(C.spanning_2conn(w) and is_hamilton_cycle(w)),
            "mutated_edges": [list(C.EDGES[e]) for e in mutated],
            "mutated_is_2conn": bool(C.spanning_2conn(mutated)),
            "mutated_is_hamilton_cycle": bool(is_hamilton_cycle(mutated)),
        })

    res = {
        "task": "1: |Gamma|=8 => C_8",
        "subsets_examined": total,
        "n_spanning_connected_8edge": n_connected,
        "n_spanning_2connected_8edge": n_2conn,
        "n_2connected_but_not_2regular": n_2conn_not2reg,
        "counterexamples": counterexamples,
        "expected_2520": 2520,
        "seven_factorial_over_2": 2520,
        "verdict_count_matches": n_2conn == 2520,
        "verdict_all_2regular": n_2conn_not2reg == 0,
        "seconds": round(dt, 1),
        "mutation_controls": {
            "MC1-A_drop_2connectivity": {
                "count": n_connected,
                "differs_from_2520": n_connected != 2520,
                "FIRED": n_connected != 2520,
            },
            "MC1-C_skip_vertex0_deletion": {
                "count": n_skip0,
                "differs_from_2520": n_skip0 != 2520,
                "FIRED": n_skip0 != 2520,
            },
            "MC1-B_corrupt_witness": mc1b,
            "MC1-B_FIRED": all((not m["mutated_is_hamilton_cycle"]) for m in mc1b),
        },
    }
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
