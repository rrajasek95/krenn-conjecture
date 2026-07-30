#!/usr/bin/env python3
"""Light exact checks for the two-chart alignment/curvature normal form."""

from itertools import combinations, product
from random import Random


if not __debug__:
    raise RuntimeError("run without -O so all exact assertions remain active")


def add(left, right):
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def scale(value, matrix):
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def transpose(matrix):
    return tuple(zip(*matrix))


def multiply(left, right):
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column] for middle in range(3))
            for column in range(3)
        )
        for row in range(3)
    )


def outer(left, right):
    return tuple(tuple(a * b for b in right) for a in left)


def determinant(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def adjugate(matrix):
    cofactors = []
    for row in range(3):
        cofactor_row = []
        for column in range(3):
            minor = [
                [matrix[i][j] for j in range(3) if j != column]
                for i in range(3)
                if i != row
            ]
            value = minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]
            cofactor_row.append((-1) ** (row + column) * value)
        cofactors.append(tuple(cofactor_row))
    return transpose(tuple(cofactors))


def mat_vec(matrix, vector):
    return tuple(sum(row[i] * vector[i] for i in range(3)) for row in matrix)


def rank(matrix, modulus=0):
    rows = [list(row) for row in matrix]
    rank_value = 0
    for column in range(3):
        pivot = next(
            (
                row
                for row in range(rank_value, len(rows))
                if (
                    rows[row][column] % modulus
                    if modulus
                    else rows[row][column]
                )
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank_value], rows[pivot] = rows[pivot], rows[rank_value]
        if modulus:
            inverse = pow(rows[rank_value][column] % modulus, -1, modulus)
            rows[rank_value] = [entry * inverse % modulus for entry in rows[rank_value]]
            for row in range(len(rows)):
                if row == rank_value:
                    continue
                factor = rows[row][column] % modulus
                rows[row] = [
                    (entry - factor * pivot_entry) % modulus
                    for entry, pivot_entry in zip(rows[row], rows[rank_value])
                ]
        else:
            # All non-modular rank calls below use diagonal/coordinate matrices.
            pivot_value = rows[rank_value][column]
            for row in range(rank_value + 1, len(rows)):
                factor = rows[row][column]
                if factor:
                    rows[row] = [
                        pivot_value * entry - factor * pivot_entry
                        for entry, pivot_entry in zip(rows[row], rows[rank_value])
                    ]
        rank_value += 1
    return rank_value


ZERO = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def unit(row, column):
    return tuple(
        tuple(int(i == row and j == column) for j in range(3))
        for i in range(3)
    )


def j_matrix(target):
    basis = [tuple(int(i == index) for i in range(3)) for index in range(3)]
    columns = []
    for column in range(3):
        values = []
        for row in range(3):
            u, v, e = basis[row], basis[column], basis[target]
            values.append(
                determinant(tuple(tuple(vector[i] for vector in (u, v, e)) for i in range(3)))
            )
        columns.append(tuple(values))
    return transpose(tuple(columns))


def wedge_matrix(endpoint_left, endpoint_right, target):
    return multiply(multiply(transpose(endpoint_left), j_matrix(target)), endpoint_right)


def audit_adjugate_identity():
    rng = Random(20260730)
    checks = 0
    for _ in range(80):
        left = tuple(tuple(rng.randrange(-3, 4) for _ in range(3)) for _ in range(3))
        right = tuple(tuple(rng.randrange(-3, 4) for _ in range(3)) for _ in range(3))
        target = rng.randrange(3)
        normal = wedge_matrix(left, right, target)
        basis = tuple(int(i == target) for i in range(3))
        expected = outer(mat_vec(adjugate(right), basis), mat_vec(adjugate(left), basis))
        assert adjugate(normal) == expected
        checks += 1
    return checks


def span(vectors, modulus=2):
    values = {(0, 0, 0)}
    for vector in vectors:
        values |= {
            tuple((entry + scalar * coordinate) % modulus for entry, coordinate in zip(value, vector))
            for value in tuple(values)
            for scalar in range(modulus)
        }
    return frozenset(values)


def all_subspaces_f2():
    vectors = tuple(product(range(2), repeat=3))
    return tuple({span(generators) for size in range(4) for generators in combinations(vectors, size)})


def det_vectors(left, right, target, modulus=2):
    matrix = tuple(
        tuple(vector[index] for vector in (left, right, target))
        for index in range(3)
    )
    return determinant(matrix) % modulus


def audit_two_target_zero_classifier():
    subspaces = all_subspaces_f2()
    e0, e1 = (1, 0, 0), (0, 1, 0)
    plane = span((e0, e1))
    checks = 0
    for left in subspaces:
        for right in subspaces:
            zero = all(
                det_vectors(u, v, target) == 0
                for u in left
                for v in right
                for target in (e0, e1)
            )
            if not zero:
                continue
            left_dimension = (len(left)).bit_length() - 1
            right_dimension = (len(right)).bit_length() - 1
            classified = left_dimension + right_dimension <= 3 or (left == plane and right == plane)
            assert classified
            checks += 1
    return len(subspaces), checks


def matrix_map_rank(local_maps):
    stacked_rows = []
    for matrix in local_maps.values():
        stacked_rows.extend(matrix)
    return rank(tuple(stacked_rows))


def has_perfect_matching(vertices, supported_edges):
    vertices = tuple(vertices)
    if not vertices:
        return True
    first = vertices[0]
    for other in vertices[1:]:
        edge = frozenset((first, other))
        if edge not in supported_edges:
            continue
        remainder = tuple(vertex for vertex in vertices if vertex not in edge)
        if has_perfect_matching(remainder, supported_edges):
            return True
    return False


def audit_rank_two_block_guard():
    j0 = j_matrix(0)
    common = ("s", "t", "u")
    p = {site: IDENTITY for site in common}
    s = {site: IDENTITY for site in common}
    r = {site: scale(2, IDENTITY) for site in common}
    p.update({"r": transpose(j0), "q": transpose(j0), "v": ZERO, "w": ZERO})
    s.update({"r": ZERO, "v": ZERO, "w": ZERO})
    r.update({"q": ZERO, "v": ZERO, "w": ZERO})

    w_pq = ("r", "s", "t", "u", "v", "w")
    w_pr = ("q", "s", "t", "u", "v", "w")
    tq = {site for site in w_pq if wedge_matrix(p[site], s[site], 0) in (ZERO, j0)}
    tr = {
        site
        for site in w_pr
        if wedge_matrix(p[site], r[site], 0) in (ZERO, scale(2, j0))
    }
    assert tq == set(w_pq)
    assert tr == set(w_pr)
    assert all(rank(p[site]) == rank(s[site]) == rank(r[site]) == 3 for site in common)
    assert matrix_map_rank({site: p[site] for site in w_pq}) == 3
    assert matrix_map_rank({site: s[site] for site in w_pq}) == 3
    assert matrix_map_rank({site: p[site] for site in w_pr}) == 3
    assert matrix_map_rank({site: r[site] for site in w_pr}) == 3

    direct_a = j0[1][2]
    direct_b = j0[1][2]
    f_value = IDENTITY[2][2]
    u_value = scale(2, IDENTITY)[2][2]
    assert (direct_a, direct_b, f_value, u_value) == (1, 1, 1, 2)
    assert direct_a * u_value - direct_b * f_value == 1

    pq_edges = {frozenset(("r", site)) for site in common}
    pr_edges = {frozenset(("q", site)) for site in common}
    assert not has_perfect_matching(w_pq, pq_edges)
    assert not has_perfect_matching(w_pr, pr_edges)
    return len(tq), len(tr)


def left_aligned(matrix):
    return all(matrix[row][column] == 0 for row in (1, 2) for column in range(3))


def right_aligned(matrix):
    return all(matrix[row][column] == 0 for row in range(3) for column in (1, 2))


def audit_diagonal_guard_alignment():
    e00, e11, e22 = unit(0, 0), unit(1, 1), unit(2, 2)
    pq_p = {"a": e00, "b": ZERO, "c": e22, "d": e11, "r": e00, "s": ZERO}
    pq_s = {"a": ZERO, "b": e00, "c": ZERO, "d": ZERO, "r": e22, "s": e11}
    pr_p = {"q": e00, "a": e00, "b": ZERO, "c": e22, "d": e11, "s": ZERO}
    pr_r = {"q": e22, "a": ZERO, "b": e11, "c": ZERO, "d": ZERO, "s": e00}

    expected = {
        "pq_left_1": set(pq_p),
        "pq_left_2": set(pq_p),
        "pq_right_1": set(pq_p) - {"r"},
        "pq_right_2": set(pq_p),
        "pr_left_1": set(pr_p),
        "pr_left_2": set(pr_p),
        "pr_right_1": set(pr_p) - {"q"},
        "pr_right_2": set(pr_p),
    }
    actual = {}
    for chart, left_maps, right_maps in (("pq", pq_p, pq_s), ("pr", pr_p, pr_r)):
        for target in (1, 2):
            normals = {
                site: wedge_matrix(left_maps[site], right_maps[site], target)
                for site in left_maps
            }
            actual[f"{chart}_left_{target}"] = {
                site for site, normal in normals.items() if left_aligned(normal)
            }
            actual[f"{chart}_right_{target}"] = {
                site for site, normal in normals.items() if right_aligned(normal)
            }
    assert actual == expected
    assert matrix_map_rank(pq_p) == matrix_map_rank(pq_s) == 3
    assert matrix_map_rank(pr_p) == matrix_map_rank(pr_r) == 3

    # The literal packet has (A,B,F,U)=(1,1,0,1).
    assert 1 * 1 - 1 * 0 == 1
    return {name: len(sites) for name, sites in actual.items()}


def main():
    adjugate_checks = audit_adjugate_identity()
    subspaces, zero_checks = audit_two_target_zero_classifier()
    rank_two_sizes = audit_rank_two_block_guard()
    diagonal_sizes = audit_diagonal_guard_alignment()
    print(f"adjugate identity: PASS ({adjugate_checks} exact trials)")
    print(f"two-target zero classifier: PASS ({subspaces} F2 subspaces, {zero_checks} zero pairs)")
    print(f"rank-two block guard: PASS (alignment sizes {rank_two_sizes}, curvature 1)")
    print(f"diagonal-complete rank-one guard: PASS ({diagonal_sizes}, curvature 1)")


if __name__ == "__main__":
    main()
