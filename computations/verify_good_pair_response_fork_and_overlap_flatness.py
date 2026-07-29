#!/usr/bin/env python3
"""Small exact guards for the good-pair response fork.

This intentionally checks only finite combinatorial identities used in the
proof note.  It is dependency-free and is not an exhaustive source search.
"""

from fractions import Fraction
from itertools import combinations


def edge(i, j):
    return (i, j) if i < j else (j, i)


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    i = vertices[0]
    for position in range(1, len(vertices)):
        j = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in matchings(rest):
            yield (edge(i, j),) + matching


def matching_weight(matching, q):
    value = 1
    for ij in matching:
        value *= q[ij]
    return value


def hafnian(vertices, q):
    return sum(matching_weight(matching, q) for matching in matchings(vertices))


def deterministic_q(n, seed):
    return {
        (i, j): ((i + 2) * (j + 3) + 3 * seed) % 11 - 5
        for i, j in combinations(range(n), 2)
    }


def audit_even_gauge_identity():
    ledgers = 0
    for n in (2, 4, 6, 8):
        for seed in range(4):
            q = deterministic_q(n, seed)
            alpha = [((i + 1) * (seed + 2)) % 9 - 4 for i in range(n)]
            lhs = 0
            for matching in matchings(range(n)):
                lhs += matching_weight(matching, q) * sum(
                    alpha[i] + alpha[j] for i, j in matching
                )
            rhs = sum(alpha) * hafnian(range(n), q)
            assert lhs == rhs
            ledgers += 1
    return ledgers


def odd_gauge_insertion(vertices, q, alpha, linear):
    """Coefficient of Z^alpha * linear * q^[t-2] on an odd full support."""
    total = 0
    for i in vertices:
        rest = tuple(j for j in vertices if j != i)
        for matching in matchings(rest):
            total += linear[i] * matching_weight(matching, q) * sum(
                alpha[a] + alpha[b] for a, b in matching
            )
    return total


def linear_times_near_hafnian(vertices, q, linear):
    return sum(
        linear[i] * hafnian(tuple(j for j in vertices if j != i), q)
        for i in vertices
    )


def audit_odd_identity_and_transition():
    ledgers = 0
    for n in (3, 5, 7):
        vertices = tuple(range(n))
        for seed in range(5):
            q = deterministic_q(n, seed)
            alpha = [((i + 3) * (seed + 1)) % 13 - 6 for i in vertices]
            linear = [((2 * i + 1) * (seed + 3)) % 17 - 8 for i in vertices]
            weighted = [alpha[i] * linear[i] for i in vertices]
            lhs = odd_gauge_insertion(vertices, q, alpha, linear)
            rhs = (
                sum(alpha) * linear_times_near_hafnian(vertices, q, linear)
                - linear_times_near_hafnian(vertices, q, weighted)
            )
            assert lhs == rhs

            # Full triple cancellation with h the deleted coordinate:
            # a=-(sum alpha+h), L_i=(alpha_i+h)T_i.
            h = seed - 2
            direct = -(sum(alpha) + h)
            transition = [(alpha[i] + h) * linear[i] for i in vertices]
            pair_linear = [direct * linear[i] + transition[i] for i in vertices]
            residual = linear_times_near_hafnian(vertices, q, pair_linear) + lhs
            assert residual == 0
            ledgers += 1
    return ledgers


def rational_rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(value) for value in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [value / scale for value in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][col]:
                continue
            scale = a[r][col]
            a[r] = [x - scale * y for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def defect_count(n, edges):
    adjacency = [set() for _ in range(n)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    seen = set()
    defects = 0
    for start in range(n):
        if start in seen:
            continue
        stack = [(start, 0)]
        colors = {}
        bipartite = True
        while stack:
            vertex, color = stack.pop()
            if vertex in colors:
                bipartite &= colors[vertex] == color
                continue
            colors[vertex] = color
            seen.add(vertex)
            stack.extend((other, 1 - color) for other in adjacency[vertex])
        if not adjacency[start] or bipartite:
            defects += 1
    return defects


def audit_signless_incidence():
    graphs = 0
    for n in range(1, 6):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [ij for bit, ij in enumerate(possible) if mask & (1 << bit)]
            incidence = [
                [int(vertex == i or vertex == j) for vertex in range(n)]
                for i, j in edges
            ]
            nullity = n - rational_rank(incidence)
            assert nullity == defect_count(n, edges)
            graphs += 1
    return graphs


def audit_noncomplex_guard_and_restriction():
    # G_3 has only 01.  The 02 block is nonzero of rank one.
    zeta = (1, -1, 0, 0)
    assert zeta[0] + zeta[1] == 0
    assert sum(zeta) == 0
    assert zeta[0] + zeta[2] == 1  # (Z^zeta)_02 is the nonzero 02 block.

    # Every gauge on an odd overlap extends to a zero-sum chart gauge.
    for gamma in ((2, -3, 5), (0, 0, 0), (-7, 4, 1)):
        extension = gamma + (-sum(gamma),)
        assert sum(extension) == 0
        assert extension[:-1] == gamma

    # The constant choice in the augmented-to-usual E1 identification.
    for t in (1, 2, 3, 5):
        for direct in (-7, 0, 11):
            beta = [Fraction(-direct, 2 * t)] * (2 * t)
            assert sum(beta) == -direct
            assert beta[0] + beta[1] == Fraction(-direct, t)


def main():
    even_ledgers = audit_even_gauge_identity()
    odd_ledgers = audit_odd_identity_and_transition()
    graphs = audit_signless_incidence()
    audit_noncomplex_guard_and_restriction()
    print(
        "PASS "
        f"graphs={graphs} even_matching_ledgers={even_ledgers} "
        f"odd_transition_ledgers={odd_ledgers}"
    )


if __name__ == "__main__":
    main()
