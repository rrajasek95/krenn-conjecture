#!/usr/bin/env python3
"""Exact degree-six local-web tests on single-perfect-matching sources.

At one site, the multilinear ``SL(3)`` invariants in six copy slots form the
five-dimensional Specht module ``[2,2,2]``.  We realize it by products of two
epsilon brackets.  For a tensor which factors along a vertex perfect
matching, a degree-six web factors edgewise through the Gram matrix of these
five local brackets.  This script asks whether the value on the diagonal
target is already a linear combination of those perfect-matching
restrictions.

All calculations are integral apart from a final Gaussian elimination over
a displayed prime.  A modular inconsistency proves rational inconsistency;
a modular solution is reported only as exploratory evidence.
"""

from __future__ import annotations

import itertools
from math import prod

import numpy as np
import sympy as sp


N = 6
Q = 3
PRIME = 1_000_003


def sign3(values: tuple[int, int, int]) -> int:
    if len(set(values)) < 3:
        return 0
    inversions = sum(values[i] > values[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inversions % 2 else 1


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def local_brackets():
    assignments = tuple(itertools.product(range(Q), repeat=6))
    candidates = []
    labels = []
    # Each unordered 3+3 partition has a unique shore containing slot zero.
    for pair in itertools.combinations(range(1, 6), 2):
        left = (0,) + pair
        right = tuple(x for x in range(6) if x not in left)
        values = tuple(sign3(tuple(a[x] for x in left)) * sign3(tuple(a[x] for x in right)) for a in assignments)
        candidates.append(values)
        labels.append((left, right))

    # Greedily select an exact independent basis modulo PRIME.  Since the
    # selected 5-by-5 minor is nonzero modulo PRIME, it is nonzero over Q.
    pivots: dict[int, dict[int, int]] = {}
    chosen = []
    for j, vector in enumerate(candidates):
        row = {i: z % PRIME for i, z in enumerate(vector) if z % PRIME}
        while row:
            i = min(row)
            a = row[i]
            if i not in pivots:
                inv = pow(a, PRIME - 2, PRIME)
                pivots[i] = {k: z * inv % PRIME for k, z in row.items()}
                chosen.append(j)
                break
            pivot = pivots[i]
            for k, z in pivot.items():
                w = (row.get(k, 0) - a * z) % PRIME
                if w:
                    row[k] = w
                else:
                    row.pop(k, None)
    assert len(chosen) == 5
    return assignments, tuple(labels[j] for j in chosen), tuple(candidates[j] for j in chosen)


def tensor_index(indices: tuple[int, ...]) -> int:
    answer = 0
    for i in indices:
        answer = 5 * answer + i
    return answer


def build_vectors():
    assignments, labels, brackets = local_brackets()
    gram = tuple(tuple(sum(x * y for x, y in zip(a, b)) for b in brackets) for a in brackets)

    size = 5**N
    target = [0] * size
    for k, assignment in enumerate(assignments):
        local = tuple(brackets[i][k] for i in range(5))
        support = tuple(i for i, z in enumerate(local) if z)
        for indices in itertools.product(support, repeat=N):
            target[tensor_index(indices)] += prod(local[i] for i in indices)

    matching_vectors = []
    matchings = tuple(perfect_matchings(tuple(range(N))))
    for matching in matchings:
        vector = [0] * size
        for indices in itertools.product(range(5), repeat=N):
            vector[tensor_index(indices)] = prod(gram[indices[u]][indices[v]] for u, v in matching)
        matching_vectors.append(vector)
    return assignments, labels, brackets, gram, matchings, matching_vectors, target


def tuple_web_vector(bracket_array: np.ndarray, matching_tuple):
    """Return all 5^6 web contractions for six identity matching tensors."""
    slots_by_edge = {}
    for copy, matching in enumerate(matching_tuple):
        for u, v in matching:
            edge = tuple(sorted((u, v)))
            slots_by_edge.setdefault(edge, []).append(copy)

    adjacency = {v: set() for v in range(N)}
    for u, v in slots_by_edge:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert all(1 <= len(adjacency[v]) <= 2 for v in range(N))

    components = []
    unseen = set(range(N))
    while unseen:
        start = min(unseen)
        if len(adjacency[start]) == 1:
            neighbor = next(iter(adjacency[start]))
            component = (start, neighbor)
        else:
            component_list = [start]
            previous = None
            current = start
            while True:
                choices = sorted(adjacency[current] - ({previous} if previous is not None else set()))
                nxt = choices[0]
                if nxt == start:
                    break
                component_list.append(nxt)
                previous, current = current, nxt
            component = tuple(component_list)
        unseen.difference_update(component)
        components.append(component)

    result = np.asarray(1, dtype=np.int64)
    vertex_order = []
    for component in components:
        if len(component) == 2:
            u, v = component
            assert slots_by_edge[tuple(sorted((u, v)))] == list(range(6))
            tensor = np.tensordot(
                bracket_array,
                bracket_array,
                axes=(tuple(range(1, 7)), tuple(range(1, 7))),
            )
        else:
            # Contract a cycle as a matrix-product trace.  Rotate it so the
            # closing super-edge has minimal dimension, keeping intermediates
            # below 5^6 * 3^3 in the worst 3+3 split.
            edge_sizes = [
                len(slots_by_edge[tuple(sorted((component[j], component[(j + 1) % len(component)])))])
                for j in range(len(component))
            ]
            closing = min(range(len(component)), key=lambda j: edge_sizes[j])
            component = component[closing + 1 :] + component[: closing + 1]

            factors = []
            for j, vertex in enumerate(component):
                previous = component[j - 1]
                following = component[(j + 1) % len(component)]
                left = slots_by_edge[tuple(sorted((vertex, previous)))]
                right = slots_by_edge[tuple(sorted((vertex, following)))]
                assert sorted(left + right) == list(range(6))
                permutation = (0,) + tuple(1 + k for k in left) + tuple(1 + k for k in right)
                factors.append(
                    bracket_array.transpose(permutation).reshape(
                        5, 3 ** len(left), 3 ** len(right)
                    )
                )
            tensor = factors[0]
            for factor in factors[1:]:
                tensor = np.tensordot(tensor, factor, axes=([-1], [1]))
            tensor = np.trace(tensor, axis1=1, axis2=-1)
            assert tensor.shape == (5,) * len(component)

        result = np.tensordot(result, tensor, axes=0)
        vertex_order.extend(component)

    assert sorted(vertex_order) == list(range(N))
    permutation = tuple(vertex_order.index(v) for v in range(N))
    return result.transpose(permutation).reshape(-1)


def two_matching_coefficient_vectors(brackets, first, second):
    bracket_array = np.asarray(brackets, dtype=np.int64).reshape((5,) + (3,) * 6)
    answer = [np.zeros(5**N, dtype=np.int64) for _ in range(7)]
    cache = {}
    # The contraction depends on the set of copy slots assigned to ``second``.
    # Complementary subsets need not agree because the local bracket basis is
    # slot-sensitive, so retain all 64 exact contractions.
    for mask in range(64):
        matching_tuple = tuple(second if (mask >> copy) & 1 else first for copy in range(6))
        vector = tuple_web_vector(bracket_array, matching_tuple)
        answer[mask.bit_count()] += vector
    return [v.tolist() for v in answer]


def modular_membership(columns: list[list[int]], target: list[int]):
    # Row-reduce the transpose: columns and target are short (15+1 vectors),
    # while the ambient coordinate space has only 5^6 entries.
    pivots: dict[int, list[int]] = {}
    for coordinate in range(len(target)):
        row = [column[coordinate] % PRIME for column in columns]
        rhs = target[coordinate] % PRIME
        for pivot, equation in pivots.items():
            if not row[pivot]:
                continue
            a = row[pivot]
            row = [(x - a * y) % PRIME for x, y in zip(row, equation[:-1])]
            rhs = (rhs - a * equation[-1]) % PRIME
        if not any(row):
            if rhs:
                return False, len(pivots), coordinate
            continue
        pivot = next(i for i, x in enumerate(row) if x)
        inv = pow(row[pivot], PRIME - 2, PRIME)
        normalized = [x * inv % PRIME for x in row] + [rhs * inv % PRIME]
        pivots[pivot] = normalized
    return True, len(pivots), None


def modular_column_basis(columns):
    pivots = []
    basis_indices = []
    for column_index, column in enumerate(columns):
        vector = np.asarray(column, dtype=np.int64) % PRIME
        for coordinate, pivot_vector in pivots:
            coefficient = int(vector[coordinate])
            if coefficient:
                vector = (vector - coefficient * pivot_vector) % PRIME
        support = np.flatnonzero(vector)
        if not len(support):
            continue
        coordinate = int(support[0])
        vector = vector * pow(int(vector[coordinate]), PRIME - 2, PRIME) % PRIME
        pivots.append((coordinate, vector))
        basis_indices.append(column_index)
    return basis_indices, [coordinate for coordinate, _ in pivots]


def exact_span_certificate(columns, target):
    basis_indices, pivot_rows = modular_column_basis(columns)
    matrix = sp.Matrix([[columns[j][r] for j in basis_indices] for r in pivot_rows])
    rhs = sp.Matrix([target[r] for r in pivot_rows])
    assert matrix.det() != 0
    solution = matrix.inv() * rhs
    for r in range(len(target)):
        value = sum(solution[k] * columns[j][r] for k, j in enumerate(basis_indices))
        assert value == target[r], (r, value, target[r])
    nonzero = [(basis_indices[k], z) for k, z in enumerate(solution) if z]
    max_num = max(abs(int(z.p)) for _, z in nonzero)
    max_den = max(int(z.q) for _, z in nonzero)
    print(
        f"exact Q-span certificate: basis_rank={len(basis_indices)}, "
        f"nonzero_coefficients={len(nonzero)}, "
        f"max_numerator_bits={max_num.bit_length()}, "
        f"max_denominator_bits={max_den.bit_length()}"
    )
    print(f"exact nonzero column coefficients={nonzero}")
    return nonzero


def main():
    assignments, labels, brackets, gram, matchings, columns, target = build_vectors()
    inside, rank, witness_coordinate = modular_membership(columns, target)
    print(f"local bracket basis={labels}")
    print(f"Gram={gram}")
    print(f"perfect matchings={len(matchings)}, span rank={rank} over GF({PRIME})")
    print(f"target in single-matching restriction span={inside}")
    if witness_coordinate is not None:
        print(f"first inconsistent coordinate={witness_coordinate}")

    # Add the coefficient vectors of H=M+(lambda)N for every unordered pair
    # of vertex matchings.  This closes the two cycle types under every vertex
    # relabeling, which is essential because our five bracket coordinates are
    # tied to fixed copy slots while the ambient tensor coordinates are tied
    # to fixed vertices.
    enlarged = list(columns)
    type_counts = {0: 0, 1: 0}
    for pair_index, (first, second) in enumerate(itertools.combinations(matchings, 2), 1):
        common = len(set(first) & set(second))
        assert common in type_counts
        type_counts[common] += 1
        coeffs = two_matching_coefficient_vectors(brackets, first, second)
        enlarged.extend(coeffs)
        if pair_index % 15 == 0 or pair_index == 105:
            inside, rank, witness_coordinate = modular_membership(enlarged, target)
            print(
                f"two-matching pairs={pair_index}/105, type_counts={type_counts}, "
                f"columns={len(enlarged)}, rank={rank}, target_in_span={inside}"
            )
            if inside:
                exact_span_certificate(enlarged, target)
                break


if __name__ == "__main__":
    main()
