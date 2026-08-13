#!/usr/bin/env python3
"""Audit the frame-circuit shapes in the anchored support-minimality theorem.

The theorem proved in the accompanying note is conceptual.  If an exact
source is support-minimal while twelve selected pure-anchor cells are kept
nonzero, Stiemke's alternative gives a strictly positive dependence among
all occupied non-anchor characters modulo the anchor characters.  A
conformal oriented-matroid decomposition then puts every occupied
non-anchor cell in a primitive circuit of the unsigned port-incidence
matrix, with every negative circuit edge an anchor.

Primitive circuits of an unsigned graph-incidence matrix are exactly even
cycles and odd handcuffs (including the parallel two-cycle).  This checker
exhausts every simple graph on at most six vertices, reconstructs every
minimal dependent edge set over Q, and verifies precisely those shapes and
their primitive coefficients.  Six vertices are the first size containing
two vertex-disjoint odd cycles joined by a path.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/combinatorial-route.md":
        "612ffb3569a8c107d52959f8485315d94da91ef5e9124586acdfa703c6011018",
    "notes/n8-anchored-germ-target-torus-accessibility-no-go.md":
        "826b06c3f8a7fb735e7abd41d6733159811d016228350f45678c36fc3b7f1306",
    "notes/oo-zero-holonomy-schur-interference-reduction.md":
        "fbacb885c979cc4be6a0b765aab9a0bc1b3ffccf6f8013cd20abd111bd97ec3f",
}
EXPECTED_LEDGER_SHA256 = (
    "25fa80c17f9a5488d2f7883d76b39cb8579a281be33afba6d0a92673e15ce82e"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    if not work:
        return 0
    height, width = len(work), len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right
                         for left, right in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def incidence(vertex_count, edges):
    return [
        [int(vertex in edge) for edge in edges]
        for vertex in range(vertex_count)
    ]


def primitive_kernel(vertex_count, edges):
    """Return the primitive one-dimensional kernel of unsigned incidence."""
    matrix = incidence(vertex_count, edges)
    width = len(edges)
    work = [[Q(value) for value in row] for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, vertex_count)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(vertex_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right
                         for left, right in zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    free = [column for column in range(width) if column not in pivots]
    require(len(free) == 1, "circuit kernel is not one-dimensional")
    vector = [Q(0)] * width
    vector[free[0]] = Q(1)
    for row in range(len(pivots) - 1, -1, -1):
        column = pivots[row]
        vector[column] = -sum(
            work[row][other] * vector[other] for other in range(column + 1, width)
        )
    denominators = [entry.denominator for entry in vector]
    lcm = 1
    for denominator in denominators:
        a, b = lcm, denominator
        while b:
            a, b = b, a % b
        lcm = lcm * denominator // a
    integers = [int(entry * lcm) for entry in vector]
    gcd = 0
    for value in integers:
        a, b = gcd, abs(value)
        while b:
            a, b = b, a % b
        gcd = a
    integers = [value // gcd for value in integers]
    if next(value for value in integers if value) < 0:
        integers = [-value for value in integers]
    require(all(
        sum(int(vertex in edge) * value for edge, value in zip(edges, integers, strict=True)) == 0
        for vertex in range(vertex_count)
    ), "primitive kernel reconstruction failed")
    return tuple(integers)


def connected_vertices(edges):
    vertices = {vertex for edge in edges for vertex in edge}
    if not vertices:
        return False
    seen = {min(vertices)}
    stack = list(seen)
    while stack:
        vertex = stack.pop()
        for edge in edges:
            if vertex not in edge:
                continue
            other = edge[0] if edge[1] == vertex else edge[1]
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return seen == vertices


def bipartite(edges):
    adjacency = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    colours = {}
    for root in adjacency:
        if root in colours:
            continue
        colours[root] = 0
        queue = [root]
        for vertex in queue:
            for other in adjacency[vertex]:
                if other not in colours:
                    colours[other] = 1 - colours[vertex]
                    queue.append(other)
                elif colours[other] == colours[vertex]:
                    return False
    return True


def bridges(edges):
    answer = []
    for index in range(len(edges)):
        reduced = edges[:index] + edges[index + 1:]
        if not connected_vertices(reduced):
            answer.append(edges[index])
    return tuple(answer)


def classify_shape(edges):
    degree = {}
    for left, right in edges:
        degree[left] = degree.get(left, 0) + 1
        degree[right] = degree.get(right, 0) + 1
    if bipartite(edges):
        require(all(value == 2 for value in degree.values()),
                "minimal bipartite circuit is not an even cycle")
        return "even_cycle"
    degree_multiset = sorted(degree.values())
    if degree_multiset.count(4) == 1:
        require(all(value in (2, 4) for value in degree_multiset),
                "tight handcuff degree pattern changed")
        return "tight_odd_handcuff"
    require(degree_multiset.count(3) == 2
            and all(value in (2, 3) for value in degree_multiset),
            "loose handcuff degree pattern changed")
    require(bridges(edges), "nonbipartite theta graph survived circuit minimality")
    return "loose_odd_handcuff"


def audit_simple_graphs(max_vertices=6):
    counts = {"even_cycle": 0, "tight_odd_handcuff": 0,
              "loose_odd_handcuff": 0}
    coefficient_profiles = set()
    total_subsets = 0
    for vertex_count in range(2, max_vertices + 1):
        complete = tuple(combinations(range(vertex_count), 2))
        for mask in range(1, 1 << len(complete)):
            total_subsets += 1
            edges = tuple(complete[index] for index in range(len(complete))
                          if mask & (1 << index))
            if len(edges) <= 1 or not connected_vertices(edges):
                continue
            matrix = incidence(vertex_count, edges)
            if rank(matrix) == len(edges):
                continue
            if any(rank(incidence(vertex_count, edges[:index] + edges[index + 1:]))
                   < len(edges) - 1 for index in range(len(edges))):
                continue
            shape = classify_shape(edges)
            kernel = primitive_kernel(vertex_count, edges)
            absolute = tuple(sorted(abs(value) for value in kernel))
            if shape == "even_cycle":
                require(set(absolute) == {1}, "even-cycle coefficient changed")
            else:
                require(set(absolute).issubset({1, 2}) and 1 in absolute,
                        "handcuff coefficient changed")
                if shape == "loose_odd_handcuff":
                    require(2 in absolute, "loose handcuff lost doubled path")
            counts[shape] += 1
            coefficient_profiles.add((shape, absolute))
    require(all(counts.values()), "one frame-circuit shape was not exercised")
    return total_subsets, counts, coefficient_profiles


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    total_subsets, counts, profiles = audit_simple_graphs()

    # Parallel edges are the remaining primitive frame circuit.  Their two
    # equal incidence columns have primitive kernel (1,-1).
    parallel = ((0, 1), (0, 1))
    require(primitive_kernel(2, parallel) == (1, -1),
            "parallel two-cycle coefficient changed")

    ledger = {
        "pins": PINS,
        "simple_graph_subsets_audited": total_subsets,
        "simple_frame_circuit_counts_through_six_vertices": counts,
        "coefficient_profiles": sorted(
            (shape, list(profile)) for shape, profile in profiles
        ),
        "parallel_two_cycle": [1, -1],
        "support_minimality_theorem": (
            "minimum aggregate support among exact sources retaining three "
            "selected pure matching anchors implies a strictly positive "
            "dependence of every occupied nonanchor port character modulo "
            "the anchor characters"
        ),
        "cellwise_consequence": (
            "every occupied nonanchor cell belongs to a sign-conformal "
            "primitive unsigned-incidence circuit whose negative edges are "
            "selected anchors"
        ),
        "topological_consequence": (
            "the primitive circuit is a parallel/even cycle or an odd "
            "handcuff; loose-handcuff connector edges have coefficient two"
        ),
        "scope": (
            "the circuit is a port-multidegree/source-resolution object; it "
            "need not be one squarefree perfect-matching coefficient or a "
            "literal complete-row exchange without an additional source lift"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("anchored frame-circuit ledger changed", digest))
    print("anchored minimum-support frame-circuit cover: PASS")
    print("simple graph subsets audited:", total_subsets)
    print("frame circuit counts:", counts)
    print("parallel two-cycle: (1,-1)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
