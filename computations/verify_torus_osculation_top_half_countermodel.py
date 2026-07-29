#!/usr/bin/env python3
"""Exact audits for the uniform torus-osculation top-half boundary."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


def edge(u, v):
    return (u, v) if u < v else (v, u)


def all_perfect_matchings(n):
    return supported_perfect_matchings(n, frozenset(combinations(range(n), 2)))


def supported_perfect_matchings(n, support):
    adjacency = {v: set() for v in range(n)}
    for u, v in support:
        adjacency[u].add(v)
        adjacency[v].add(u)

    @lru_cache(maxsize=None)
    def recurse(remaining):
        if not remaining:
            return ((),)
        u = remaining[0]
        answer = []
        remaining_set = set(remaining)
        for v in sorted(adjacency[u] & remaining_set):
            tail_vertices = tuple(x for x in remaining if x not in (u, v))
            for tail in recurse(tail_vertices):
                answer.append(tuple(sorted((edge(u, v),) + tail)))
        return tuple(answer)

    return recurse(tuple(range(n)))


def connected(n, support):
    adjacency = {v: set() for v in range(n)}
    for u, v in support:
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            frontier.append(neighbor)
    return len(seen) == n


def factors(m):
    """The three pairwise-Hamilton factors used in the uniform family."""

    n = 2 * m
    p0 = tuple((2 * j, 2 * j + 1) for j in range(m))
    p1 = tuple(
        sorted(edge(2 * j + 1, (2 * j + 2) % n) for j in range(m))
    )
    p2 = (
        (edge(0, 2),)
        + tuple(edge(2 * j - 1, 2 * j + 2) for j in range(1, m - 1))
        + (edge(2 * m - 3, 2 * m - 1),)
    )
    return tuple(sorted(p0)), tuple(sorted(p1)), tuple(sorted(p2))


def independent_subsets(path_vertices):
    path_vertices = tuple(path_vertices)
    answer = []
    for mask in range(1 << len(path_vertices)):
        chosen = tuple(
            path_vertices[position]
            for position in range(len(path_vertices))
            if mask & (1 << position)
        )
        if all(right - left > 1 for left, right in zip(chosen, chosen[1:])):
            answer.append(chosen)
    return tuple(answer)


def fibonacci(index):
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def matching_coloring(matching, factors_by_color, n):
    coloring = [-1] * n
    edge_color = {
        selected_edge: color
        for color, matching_factor in enumerate(factors_by_color)
        for selected_edge in matching_factor
    }
    assert len(edge_color) == 3 * (n // 2)
    for u, v in matching:
        color = edge_color[(u, v)]
        coloring[u] = color
        coloring[v] = color
    assert -1 not in coloring
    return tuple(coloring)


def hafnian(vertices, weights):
    vertices = tuple(sorted(vertices))

    @lru_cache(maxsize=None)
    def recurse(remaining):
        if not remaining:
            return Fraction(1)
        u = remaining[0]
        answer = Fraction(0)
        for position, v in enumerate(remaining[1:], 1):
            selected_weight = weights.get(edge(u, v), Fraction(0))
            if not selected_weight:
                continue
            tail = remaining[1:position] + remaining[position + 1 :]
            answer += selected_weight * recurse(tail)
        return answer

    return recurse(vertices)


def verify_uniform_top_half_family(max_m=14):
    records = []
    for m in range(3, max_m + 1):
        n = 2 * m
        p0, p1, p2 = factors(m)
        factor_sets = tuple(frozenset(p) for p in (p0, p1, p2))
        assert all(not (factor_sets[i] & factor_sets[j]) for i in range(3) for j in range(i))

        # Contracting either factor in a pair leaves a connected 2-regular
        # graph, so every pairwise union is one Hamilton cycle.
        for left, right in combinations(factor_sets, 2):
            union = left | right
            degrees = {v: sum(v in selected_edge for selected_edge in union) for v in range(n)}
            assert set(degrees.values()) == {2}
            assert connected(n, union)
            assert set(supported_perfect_matchings(n, union)) == {tuple(sorted(left)), tuple(sorted(right))}

        support = frozenset().union(*factor_sets)
        matchings = supported_perfect_matchings(n, support)
        p2_index = {selected_edge: index for index, selected_edge in enumerate(p2)}
        independent = set(independent_subsets(range(1, m - 1)))
        observed_independent = set()
        fibre_terms = defaultdict(list)

        for matching in matchings:
            coloring = matching_coloring(matching, (p0, p1, p2), n)
            fibre_terms[coloring].append(matching)
            if matching in (p0, p1, p2):
                continue
            chosen_p2 = tuple(sorted(p2_index[e] for e in matching if e in factor_sets[2]))
            assert chosen_p2
            assert 0 not in chosen_p2 and m - 1 not in chosen_p2
            assert all(right - left > 1 for left, right in zip(chosen_p2, chosen_p2[1:]))
            color_edge_counts = tuple(
                len(set(matching) & factor_set) for factor_set in factor_sets
            )
            assert color_edge_counts == (
                len(chosen_p2),
                m - 2 * len(chosen_p2),
                len(chosen_p2),
            )
            observed_independent.add(chosen_p2)

        assert observed_independent == independent - {()}
        assert len(matchings) == fibonacci(m) + 2
        assert len(fibre_terms) == len(matchings)
        assert all(len(terms) == 1 for terms in fibre_terms.values())

        pure_colorings = {(color,) * n for color in range(3)}
        assert pure_colorings <= fibre_terms.keys()
        mixed_exponents = [
            coloring.count(2)
            for coloring in fibre_terms
            if coloring not in pure_colorings
        ]
        assert mixed_exponents
        assert min(mixed_exponents) == 2
        assert max(mixed_exponents) == 2 * ((m - 1) // 2)
        assert max(mixed_exponents) < m
        expected_reverse_contact = m + 1 if m % 2 else m + 2
        assert min(2 * m - exponent for exponent in mixed_exponents) == expected_reverse_contact

        # With c supported on P2, its two-hole cofactor is one exactly on a
        # P2 edge.  Since a is supported on disjoint P0/P1 edges and b=0,
        # the first two top osculating equations vanish termwise.
        c_weights = {selected_edge: Fraction(1) for selected_edge in p2}
        assert hafnian(range(n), c_weights) == 1
        for i, k in combinations(range(n), 2):
            cofactor = hafnian((v for v in range(n) if v not in (i, k)), c_weights)
            assert cofactor == (1 if edge(i, k) in factor_sets[2] else 0)
            if edge(i, k) in factor_sets[0] | factor_sets[1]:
                assert cofactor == 0

        records.append(
            (m, len(matchings), len(matchings) - 3, max(mixed_exponents), expected_reverse_contact)
        )
    return tuple(records)


def full_coefficient(n, cell_weights, coloring):
    answer = Fraction(0)
    for matching in all_perfect_matchings(n):
        term = Fraction(1)
        for u, v in matching:
            term *= cell_weights.get((u, v, coloring[u], coloring[v]), Fraction(0))
        answer += term
    return answer


def dense_scalar_endpoint(n):
    """A rational dense scalar graph of hafnian one and nonzero cofactors."""

    def odd_double_factorial(value):
        answer = 1
        for factor in range(value, 0, -2):
            answer *= factor
        return answer

    two_hole_count = odd_double_factorial(n - 3)
    exceptional = Fraction(1, two_hole_count) - (n - 2)
    weights = {selected_edge: Fraction(1) for selected_edge in combinations(range(n), 2)}
    weights[(0, 1)] = exceptional
    assert hafnian(range(n), weights) == 1
    return weights


def verify_dense_first_two_lift(n=8):
    """Audit the exact cofactor-row classification and second lift."""

    c_weights = dense_scalar_endpoint(n)
    vertices = tuple(range(n))

    def cofactor(*deleted):
        return hafnian((v for v in vertices if v not in deleted), c_weights)

    h2 = {(i, k): cofactor(i, k) for i, k in combinations(vertices, 2)}
    assert all(value for value in h2.values())
    for i in vertices:
        euler_row = sum(
            (c_weights[edge(i, j)] * h2[edge(i, j)] for j in vertices if j != i),
            Fraction(0),
        )
        assert euler_row == 1

    # b[r,i,j] is the cell with binary color r at i and z at j.  Every
    # (r,i)-row uses a two-coordinate vector orthogonal to its cofactor row.
    b = defaultdict(Fraction)
    for r in (0, 1):
        for i in vertices:
            destinations = [j for j in vertices if j != i]
            if r == 1:
                destinations.reverse()
            j, k = destinations[:2]
            b[(r, i, j)] = h2[edge(i, k)]
            b[(r, i, k)] = -h2[edge(i, j)]
            tangent = sum(
                (b[(r, i, destination)] * h2[edge(i, destination)] for destination in vertices if destination != i),
                Fraction(0),
            )
            assert tangent == 0

    # If h_ik is nonzero, the second equation independently determines the
    # four binary endpoint cells on ik.
    a = {}
    for i, k in combinations(vertices, 2):
        for r, s in product((0, 1), repeat=2):
            pairing = Fraction(0)
            for j in vertices:
                if j in (i, k):
                    continue
                for ell in vertices:
                    if ell in (i, k, j):
                        continue
                    pairing += b[(r, i, j)] * b[(s, k, ell)] * cofactor(i, k, j, ell)
            a[(i, k, r, s)] = -pairing / h2[(i, k)]
            assert a[(i, k, r, s)] * h2[(i, k)] + pairing == 0

    # Independently rebuild the 3x3 cell assignment and enumerate all
    # one- and two-binary-hole fibres.
    cells = {}
    for i, k in combinations(vertices, 2):
        cells[(i, k, 2, 2)] = c_weights[(i, k)]
        for r, s in product((0, 1), repeat=2):
            cells[(i, k, r, s)] = a[(i, k, r, s)]
    for (r, i, j), value in b.items():
        if not value:
            continue
        occurrence = (i, j, r, 2) if i < j else (j, i, 2, r)
        assert occurrence not in cells
        cells[occurrence] = value

    assert full_coefficient(n, cells, (2,) * n) == 1
    for i in vertices:
        for r in (0, 1):
            coloring = [2] * n
            coloring[i] = r
            assert full_coefficient(n, cells, tuple(coloring)) == 0
    for i, k in combinations(vertices, 2):
        for r, s in product((0, 1), repeat=2):
            coloring = [2] * n
            coloring[i] = r
            coloring[k] = s
            assert full_coefficient(n, cells, tuple(coloring)) == 0

    return 2 * n * (n - 2), len(a), len([value for value in b.values() if value])


def verify_six_site_cancellation_endpoint():
    """A non-one-factor c with cancellation passes the same top half."""

    n = 6
    rows = (
        ((0, 1, 1), (2, 3, 1), (4, 5, Fraction(1, 2)), (2, 4, 1), (3, 5, Fraction(1, 2))),
        ((3, 4, 1), (0, 2, 1), (1, 5, Fraction(1, 2)), (0, 5, 1), (1, 2, Fraction(1, 2))),
        ((2, 5, 1), (0, 3, 1), (1, 4, Fraction(1, 2)), (0, 4, 1), (1, 3, Fraction(1, 2))),
    )
    cells = {}
    for color, row in enumerate(rows):
        for u, v, value in row:
            u, v = edge(u, v)
            cells[(u, v, color, color)] = Fraction(value)

    coefficients = {}
    for coloring in product(range(3), repeat=n):
        value = full_coefficient(n, cells, coloring)
        if value:
            coefficients[coloring] = value
    for color in range(3):
        assert coefficients[(color,) * n] == 1
    assert all(
        len(set(coloring)) == 1 or len(set(coloring)) == 3
        for coloring in coefficients
    )
    mixed = {coloring: value for coloring, value in coefficients.items() if len(set(coloring)) == 3}
    assert len(mixed) == 9
    assert all(coloring.count(2) == 2 for coloring in mixed)

    c_weights = {
        (u, v): value
        for u, v, color_left, color_right in cells
        if color_left == color_right == 2
        for value in (cells[(u, v, color_left, color_right)],)
    }
    assert len(c_weights) == 5
    c_matchings = [
        matching
        for matching in all_perfect_matchings(n)
        if all(selected_edge in c_weights for selected_edge in matching)
    ]
    assert len(c_matchings) == 2
    assert hafnian(range(n), c_weights) == 1
    return len(mixed), len(c_matchings)


def main():
    records = verify_uniform_top_half_family()
    tangent_dimension, lifted_cells, active_b = verify_dense_first_two_lift()
    six_mixed, six_pure_terms = verify_six_site_cancellation_endpoint()
    print("verified uniform pairwise-Hamilton top-half counterfamily for 3 <= m <= 14")
    print(f"last audit row (m, PMs, errors, max t-degree, reverse contact): {records[-1]}")
    print(
        "verified dense c first/second lift at n=8: "
        f"tangent dimension {tangent_dimension}, {lifted_cells} determined a-cells, {active_b} active b-cells"
    )
    print(
        "verified rational n=6 cancellation endpoint: "
        f"{six_pure_terms} pure-c terms and {six_mixed} genuinely ternary errors"
    )


if __name__ == "__main__":
    main()
