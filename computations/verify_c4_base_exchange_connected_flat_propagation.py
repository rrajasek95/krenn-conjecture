#!/usr/bin/env python3
"""Audit connected flat C4 propagation and its sharp connectivity guard.

The positive theorem is linear: on a connected graph of nonzero matching
evaluation vectors, vanishing all edge 2-minors makes every vector a scalar
multiple of one root vector.  If the graph exhausts all bases of complete
one-star response columns, those columns are proportional and the pinned
nu-safe finite deletion applies.

The physical guard has four perfect matchings on eight sites.  Their typed
C4 graph has two components.  Each component cancels coefficientwise, but
the two component tensors are independent, so common-q provenance and local
flatness do not force graph connectivity or one complete-column line.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c4_torus_flat_transport_vertex_gauge.py":
        "7208712c580847c61cafcd009cb124b44d0060c0d66c4fdf2b7470e78193be57",
    "notes/c4-torus-flat-transport-vertex-gauge.md":
        "b81661d33b8f008b69891acfb3cb4e4c47e5e790ec37559a72165789b87015b9",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "notes/h3-axis-target-coloop-proportional-nu-safe-reduction.md":
        "8e9ba2c477be06a022f1c86f334d45a95b1ff7d9393b7134c6f38aa21d797f14",
    "computations/verify_uniform_axis_k3_minor_common_tail_boundary.py":
        "6a4454c324744d68457579b7aa613d026ea17457d95746d14743766a12a5710e",
    "notes/uniform-axis-k3-minor-common-tail-boundary.md":
        "19e2293461893fd6275335dc19564cd68050c44eab2e386429720a079317cf96",
}
EXPECTED_LEDGER_SHA256 = (
    "925fc1258cdde853c23b016f64f4c3c034c395193e0ddb49a4f3e488cc89da15"
)
COLOURS = range(3)
SITES = tuple(range(8))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def rank(vectors):
    matrix = [list(map(Q, vector)) for vector in vectors]
    if not matrix:
        return 0
    rows, columns = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [old - value * new
                           for old, new in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def all_minors_zero(left, right):
    pivot = next((index for index, value in enumerate(left) if value), None)
    if pivot is None:
        return not any(right)
    scalar = right[pivot] / left[pivot]
    return tuple(scalar * value for value in left) == tuple(right)


def ratio(left, right):
    """Return scalar with right=scalar*left, for nonzero proportional rows."""
    pivot = next(index for index, value in enumerate(left) if value)
    scalar = right[pivot] / left[pivot]
    require(tuple(scalar * value for value in left) == tuple(right),
            "edge vectors are not proportional")
    return scalar


def connected_potentials(vectors, edges, root=0):
    adjacency = {vertex: [] for vertex in range(len(vectors))}
    for left, right in edges:
        require(all_minors_zero(vectors[left], vectors[right]),
                "a purported flat edge has curvature")
        scalar = ratio(vectors[left], vectors[right])
        adjacency[left].append((right, scalar))
        adjacency[right].append((left, Q(1) / scalar))
    potentials = {root: Q(1)}
    queue = [root]
    while queue:
        left = queue.pop(0)
        for right, scalar in adjacency[left]:
            candidate = potentials[left] * scalar
            if right in potentials:
                require(potentials[right] == candidate,
                        "actual flat vectors acquired nontrivial holonomy")
            else:
                potentials[right] = candidate
                queue.append(right)
    require(len(potentials) == len(vectors),
            "the matching-base graph is not connected")
    require(all(tuple(potentials[index] * value for value in vectors[root])
                == tuple(vector)
                for index, vector in enumerate(vectors)),
            "the connected potentials do not reconstruct every base")
    return potentials


def audit_connected_theorem():
    root = tuple(map(Q, (1, 2, 3, 5)))
    scalars = tuple(map(Q, (2, -3, 5, 7, -11)))
    vectors = tuple(tuple(scalar * value for value in root)
                    for scalar in scalars)
    edges = ((0, 1), (1, 2), (1, 3), (3, 4))
    potentials = connected_potentials(vectors, edges)
    groups = ((0, 2, 4), (1, 3))
    columns = tuple(tuple(sum(vectors[index][coordinate] for index in group)
                          for coordinate in range(len(root)))
                    for group in groups)
    require(rank(columns) == 1 and all(columns),
            "exhaustive flat base groups stopped giving dependent columns")
    deletion_scalar = ratio(columns[0], columns[1])
    deleted = tuple(columns[1][index]
                    - deletion_scalar * columns[0][index]
                    for index in range(len(root)))
    require(not any(deleted), "the finite one-column deletion stopped working")
    return {
        "vertices": len(vectors),
        "flat_typed_C4_edges": edges,
        "root_potentials": {str(key): str(value)
                            for key, value in sorted(potentials.items())},
        "complete_column_groups": groups,
        "complete_column_rank": rank(columns),
        "finite_deletion_scalar": str(deletion_scalar),
    }


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return answer


def is_c4(left, right):
    return len(set(left) ^ set(right)) == 4


def edge_table(left_factor, right_factor, scalar=Q(1)):
    return tuple(tuple(scalar * left_factor[a] * right_factor[b]
                       for b in COLOURS) for a in COLOURS)


def matching_vector(matching, tables):
    values = []
    for word in itertools.product(COLOURS, repeat=len(SITES)):
        value = Q(1)
        for left, right in matching:
            value *= tables[(left, right)][word[left]][word[right]]
        values.append(value)
    return tuple(values)


def audit_disconnected_physical_guard():
    A = ((0, 1), (2, 3), (4, 5), (6, 7))
    B = ((0, 1), (2, 3), (4, 6), (5, 7))
    K = ((0, 1), (2, 4), (3, 7), (5, 6))
    L = ((0, 1), (2, 7), (3, 4), (5, 6))
    bases = (A, B, K, L)
    supported_edges = set().union(*(set(base) for base in bases))
    induced = tuple(matching for matching in perfect_matchings(SITES)
                    if set(matching) <= supported_edges)
    require(set(induced) == set(bases) and len(induced) == 4,
            "the physical guard acquired an extra perfect matching")
    graph_edges = tuple((left, right)
                        for left in range(len(bases))
                        for right in range(left + 1, len(bases))
                        if is_c4(bases[left], bases[right]))
    require(graph_edges == ((0, 1), (2, 3)),
            f"the two-component C4 graph changed: {graph_edges}")

    common01 = tuple(map(Q, (2, 3, 5)))
    family_one = {site: tuple(map(Q, (7 + site, 11 + site, 17 + site)))
                  for site in range(2, 8)}
    family_two = {site: tuple(map(Q, (19 + 2 * site,
                                     23 + 3 * site,
                                     29 + 5 * site)))
                  for site in range(2, 8)}
    tables = {(0, 1): edge_table(common01, common01)}
    # Component A/B uses one vertex-factor family.
    for edge in set(A) | set(B):
        if edge == (0, 1):
            continue
        scalar = Q(-1) if edge == (4, 6) else Q(1)
        tables[edge] = edge_table(family_one[edge[0]],
                                  family_one[edge[1]], scalar)
    # Component K/L uses an independent family.  The two components share
    # only physical edge 01, so this is one literal common quadratic.
    for edge in set(K) | set(L):
        if edge == (0, 1):
            continue
        scalar = Q(-1) if edge == (3, 4) else Q(1)
        tables[edge] = edge_table(family_two[edge[0]],
                                  family_two[edge[1]], scalar)
    require(set(tables) == supported_edges,
            "the common-q table inventory changed")
    vectors = tuple(matching_vector(base, tables) for base in bases)
    require(vectors[1] == tuple(-value for value in vectors[0])
            and vectors[3] == tuple(-value for value in vectors[2]),
            "one of the flat C4 components stopped cancelling")
    require(rank((vectors[0], vectors[2])) == 2,
            "the two disconnected gauge lines became dependent")
    total = tuple(sum(vector[index] for vector in vectors)
                  for index in range(len(vectors[0])))
    require(not any(total), "the literal common-q zero row stopped vanishing")
    require(all(all_minors_zero(vectors[left], vectors[right])
                for left, right in graph_edges),
            "a local C4 component acquired curvature")
    return {
        "physical_sites": len(SITES),
        "supported_physical_edges": len(supported_edges),
        "supported_perfect_matchings": len(induced),
        "matching_bases": bases,
        "typed_C4_graph_edges": graph_edges,
        "connected_components": ((0, 1), (2, 3)),
        "local_flatness": "B=-A and L=-K coefficientwise",
        "component_tensor_rank": rank((vectors[0], vectors[2])),
        "common_q_top": "A+B+K+L=0 coefficientwise",
        "scope": (
            "genuine common-q zero row with unit-valued supported edge "
            "tables; unary target and four response normalizations absent"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    ledger = {
        "connected_exhaustive_propagation": audit_connected_theorem(),
        "disconnected_common_q_guard": audit_disconnected_physical_guard(),
        "exact_dichotomy": (
            "on a source-exhaustive connected graph of certified typed-C4 "
            "edges, a nonzero edge minor is the pinned active curvature; "
            "if every edge minor vanishes, all matching bases lie on one "
            "line and all complete one-star columns are dependent"
        ),
        "missing_source_lemma": (
            "the unary and four response companions must connect every "
            "flat matching-base component by a certified typed C4, or route "
            "the first C6/C8/changed-tail separator to active/Hall"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"connected C4 propagation ledger changed: {digest}")
    print("C4 connected flat base propagation: PASS")
    print("connected+exhaustive closes; common-q alone permits two components")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
