#!/usr/bin/env python3
"""Exact audit of the binomial-SCC holonomy/cokernel reduction.

A connected source-labelled binomial component has rows

    a_e X_u + b_e X_v.

Over the Laurent fraction field its right kernel is either zero, when one
cycle has nontrivial signed holonomy, or one-dimensional, when every cycle
is compatible.  In the latter case one spanning-tree propagation constructs
the unique cokernel functional explicitly.  For physical plus-binomial
rows with exponent-trivial holonomy this is the alternating bipartition
functional; an odd cycle is therefore a unit in characteristic zero.

The checker exhausts all connected simple graphs through six vertices,
checks the signless-incidence rank/bipartite dichotomy over Q, audits the
general rational propagation theorem on deterministic coefficient packets,
and freezes the three-matching K4 core charge used by the crossed-debt note.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json


EXPECTED_DIGEST = "6eaa20c695eea7d925fc866bf3d59b328c27f01e601dc079cb4af17af851d495"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(rows, width):
    work = [dict((j, Fraction(value)) for j, value in row.items() if value)
            for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((i for i in range(pivot_row, len(work))
                      if work[i].get(column)), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = {
            j: value / scale for j, value in work[pivot_row].items()
        }
        for i in range(len(work)):
            if i == pivot_row:
                continue
            factor = work[i].get(column, Fraction(0))
            if not factor:
                continue
            updated = dict(work[i])
            for j, value in work[pivot_row].items():
                updated[j] = updated.get(j, Fraction(0)) - factor * value
                if not updated[j]:
                    updated.pop(j)
            work[i] = updated
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def connected(n, edges):
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    queue = [0]
    while queue:
        u = queue.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen) == n


def bipartition(n, edges):
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    colour = {0: 0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in colour:
                colour[v] = 1 - colour[u]
                queue.append(v)
            elif colour[v] == colour[u]:
                return None
    return tuple(colour[i] for i in range(n))


def dot(row, vector):
    return sum(Fraction(value) * vector[j] for j, value in row.items())


def propagate_kernel(n, labelled_edges):
    """Return the normalized right-kernel vector, or None on bad holonomy.

    labelled_edges contains (u,v,a,b), representing a*X_u+b*X_v.
    All coefficients are required nonzero.
    """
    adjacency = [[] for _ in range(n)]
    for u, v, a, b in labelled_edges:
        a, b = Fraction(a), Fraction(b)
        require(a and b, "binomial coefficient vanished")
        adjacency[u].append((v, -a / b))
        adjacency[v].append((u, -b / a))
    values = {0: Fraction(1)}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v, transition in adjacency[u]:
            candidate = transition * values[u]
            if v not in values:
                values[v] = candidate
                queue.append(v)
            elif values[v] != candidate:
                return None
    require(len(values) == n, "labelled graph is disconnected")
    return tuple(values[i] for i in range(n))


def graph_census():
    histogram = Counter()
    total = 0
    for n in range(2, 7):
        universe = tuple(combinations(range(n), 2))
        for mask in range(1 << len(universe)):
            if mask.bit_count() < n - 1:
                continue
            edges = tuple(universe[i] for i in range(len(universe))
                          if mask & (1 << i))
            if not connected(n, edges):
                continue
            total += 1
            rows = [{u: 1, v: 1} for u, v in edges]
            actual_rank = rank(rows, n)
            sides = bipartition(n, edges)
            expected_rank = n - 1 if sides is not None else n
            require(actual_rank == expected_rank,
                    ("signless incidence rank", n, edges,
                     actual_rank, expected_rank))
            if sides is not None:
                functional = tuple(Fraction(1 if side == 0 else -1)
                                   for side in sides)
                require(all(dot(row, functional) == 0 for row in rows),
                        ("alternating functional", n, edges))
                histogram[(n, "bipartite", actual_rank)] += 1
            else:
                histogram[(n, "nonbipartite", actual_rank)] += 1
    return total, histogram


def rational_packets():
    # Compatible packets are built from a prescribed nonzero kernel vector.
    # Breaking one coefficient on a non-tree edge destroys compatibility and
    # gives full column rank.
    packets = []
    graphs = (
        ((0, 1), (1, 2), (2, 3)),
        ((0, 1), (1, 2), (2, 0)),
        ((0, 1), (1, 2), (2, 3), (3, 0)),
        ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)),
    )
    for index, edges in enumerate(graphs):
        n = 1 + max(max(edge) for edge in edges)
        kernel = tuple(Fraction((i + 2) * (index + 1), i + 1)
                       * (-1 if i % 2 else 1) for i in range(n))
        labelled = []
        for edge_index, (u, v) in enumerate(edges):
            a = Fraction(edge_index + 2, edge_index + 1)
            b = -a * kernel[u] / kernel[v]
            labelled.append((u, v, a, b))
        rows = [{u: a, v: b} for u, v, a, b in labelled]
        propagated = propagate_kernel(n, labelled)
        require(propagated is not None, ("compatible packet", index))
        normalized = tuple(value / propagated[0] for value in propagated)
        expected = tuple(value / kernel[0] for value in kernel)
        require(normalized == expected, ("kernel propagation", index))
        require(rank(rows, n) == n - 1, ("compatible rank", index))
        require(all(dot(row, propagated) == 0 for row in rows),
                ("compatible annihilator", index))

        if len(edges) >= n:
            broken = list(labelled)
            u, v, a, b = broken[-1]
            broken[-1] = (u, v, a, b + 1)
            require(propagate_kernel(n, broken) is None,
                    ("broken holonomy survived", index))
            broken_rows = [{x: c, y: d} for x, y, c, d in broken]
            require(rank(broken_rows, n) == n,
                    ("broken holonomy rank", index))
        packets.append((n, len(edges)))
    return tuple(packets)


def four_site_core_charge():
    # Columns are the three K4 matchings U,V,W.  Two available routes form
    # a path.  The sole cokernel functional assigns alternating signs.
    rows = (
        {0: 1, 1: 1},  # U+V
        {1: 1, 2: 1},  # V+W
    )
    charge = (Fraction(1), Fraction(-1), Fraction(1))
    require(rank(rows, 3) == 2, "K4 path rank")
    require(all(dot(row, charge) == 0 for row in rows),
            "K4 path charge")
    missing_route = {0: 1, 2: 1}
    full_uncrossed = {0: 1, 1: 1, 2: 1}
    require(dot(missing_route, charge) == 2,
            "missing K4 route did not carry charge two")
    require(dot(full_uncrossed, charge) == 1,
            "uncrossed hafnian did not carry charge one")
    require(rank(rows + (missing_route,), 3) == 3,
            "K4 triangle lost determinant-two closure")
    return {
        "path_rank": 2,
        "charge": tuple(int(value) for value in charge),
        "missing_route_charge": 2,
        "full_uncrossed_charge": 1,
        "triangle_determinant_abs": 2,
    }


def main():
    graph_total, graph_histogram = graph_census()
    packet_ledger = rational_packets()
    core = four_site_core_charge()
    ledger = {
        "connected_simple_graphs_n2_to_n6": graph_total,
        "graph_histogram": sorted((str(key), value)
                                  for key, value in graph_histogram.items()),
        "rational_packets": packet_ledger,
        "four_site_core": core,
        "theorem": (
            "connected binomial SCC: bad signed holonomy gives full rank; "
            "otherwise the cokernel is the propagated one-dimensional charge"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger digest", digest))
    print("OO binomial SCC holonomy/cokernel: PASS")
    print(f"connected simple graphs audited: {graph_total}")
    print("four-site core charge: (1,-1,1); missing route=2; top=1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
