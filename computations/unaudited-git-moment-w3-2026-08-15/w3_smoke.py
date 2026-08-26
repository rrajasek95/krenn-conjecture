"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.  Smoke tests."""
from __future__ import annotations

import random
from fractions import Fraction

from w3_balance import classify, verify_balance, verify_degeneration
from w3_core import cell_index, cells, edge_index, edges, node
from w3_verify_a1 import prism_source


def prism_support(n=6):
    a, P = prism_source(n)
    return frozenset(k for k, x in enumerate(a) if x != 0)


def full_support(n):
    return frozenset(range(len(cells(n))))


def edge_full_support(n, graph):
    """All 9 cells on each edge of `graph`."""
    EI = edge_index(n)
    CI = cell_index(n)
    S = set()
    for (u, v) in graph:
        u, v = min(u, v), max(u, v)
        for i in range(3):
            for j in range(3):
                S.add(CI[(EI[(u, v)], i, j)])
    return frozenset(S)


def report(label, n, S):
    tag, cert = classify(n, S)
    extra = ""
    if tag.startswith("D") and cert:
        extra = f"  kills {len(cert['killed'])}/{len(S)} cells"
    elif tag == "P":
        extra = f"  mu={[str(m) for m in cert['mu']]}"
    print(f"{label:52s} |S|={len(S):4d}  -> {tag}{extra}")
    return tag, cert


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7   -- balance smoke tests")
    print()
    report("n=6 prism border support (9 cells)", 6, prism_support(6))
    report("n=6 full cell support (135)", 6, full_support(6))
    report("n=8 full cell support (252)", 8, full_support(8))

    # a deliberately unbalanced support: prism minus one cell
    S = set(prism_support(6))
    s0 = sorted(S)[0]
    report("n=6 prism minus one cell", 6, frozenset(S - {s0}))

    # edge-full supports at n=8 for some graphs
    K8 = [(u, v) for u in range(8) for v in range(u + 1, 8)]
    report("n=8 edge-full K8 (28 edges)", 8, edge_full_support(8, K8))
    cube = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)]
    report("n=8 edge-full cube (12 edges, cubic)", 8, edge_full_support(8, cube))
    k44 = [(u, v) for u in range(4) for v in range(4, 8)]
    report("n=8 edge-full K4,4 (16 edges, bipartite)", 8, edge_full_support(8, k44))
    # a non-regular graph
    g = cube + [(0, 2)]
    report("n=8 edge-full cube+chord (13 edges, non-regular)", 8, edge_full_support(8, g))

    # random cell supports at n=6
    rng = random.Random(7)
    tallyD = tallyP = tallyQ = 0
    for _ in range(60):
        S = frozenset(s for s in range(len(cells(6))) if rng.random() < 0.35)
        if len(S) < 6:
            continue
        tag, _ = classify(6, S)
        if tag == "P":
            tallyP += 1
        elif tag.startswith("D"):
            tallyD += 1
        else:
            tallyQ += 1
    print()
    print(f"random n=6 cell supports (p=0.35): balanced {tallyP}, degenerable {tallyD}, undecided {tallyQ}")
