#!/usr/bin/env python3
"""Exact audit of the rootless h=3 weighted-normal triple-root boundary.

The checker is dependency-free and uses explicit failures, including under
``python -O``.  It audits three independent layers: the completed-label
selector quotient, the weighted K6 four-cycle normal, and the residual
binary Macaulay quotient at ``f=v^3``.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


Matrix = tuple[tuple[F, ...], ...]
Vector = tuple[F, ...]


def matrix(rows) -> Matrix:
    return tuple(tuple(F(value) for value in row) for row in rows)


def madd(left: Matrix, right: Matrix) -> Matrix:
    require(len(left) == len(right), "matrix height mismatch")
    require(all(len(a) == len(b) for a, b in zip(left, right)),
            "matrix width mismatch")
    return tuple(tuple(a + b for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def mscale(value, item: Matrix) -> Matrix:
    value = F(value)
    return tuple(tuple(value * entry for entry in row) for row in item)


def msub(left: Matrix, right: Matrix) -> Matrix:
    return madd(left, mscale(-1, right))


def diagonal(*entries) -> Matrix:
    return tuple(tuple(F(entries[i]) if i == j else F(0)
                       for j in range(len(entries)))
                 for i in range(len(entries)))


def det2(item: Matrix) -> F:
    require(len(item) == 2 and all(len(row) == 2 for row in item),
            "det2 needs a 2-by-2 matrix")
    return item[0][0] * item[1][1] - item[0][1] * item[1][0]


def det3(item: Matrix) -> F:
    require(len(item) == 3 and all(len(row) == 3 for row in item),
            "det3 needs a 3-by-3 matrix")
    return (
        item[0][0] * (item[1][1] * item[2][2] - item[1][2] * item[2][1])
        - item[0][1] * (item[1][0] * item[2][2] - item[1][2] * item[2][0])
        + item[0][2] * (item[1][0] * item[2][1] - item[1][1] * item[2][0])
    )


def exact_rank(vectors: list[Vector]) -> int:
    if not vectors:
        return 0
    work = [list(vector) for vector in vectors]
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged rank input")
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b
                         for a, b in zip(work[row], work[rank])]
        rank += 1
        if rank == len(work):
            break
    return rank


def omega(direct: Matrix, response: Matrix) -> F:
    """Coordinate on Mat_2/(diagonals + span(direct))."""
    return direct[1][0] * response[0][1] - direct[0][1] * response[1][0]


def audit_two_anchor_crossed_packet() -> F:
    direct = matrix(((1, 1), (1, 2)))
    forward = matrix(((0, 1), (0, 0)))
    reverse = matrix(((0, 0), (2, 0)))
    edge_sum = madd(forward, reverse)
    crossed = msub(forward, reverse)
    curvature_forward = msub(direct, forward)
    curvature_reverse = msub(direct, reverse)

    require(det2(direct) == 1, "direct square is not invertible")
    require(det2(forward) == 0 and forward != matrix(((0, 0), (0, 0))),
            "forward assignment is not nonzero rank one")
    require(det2(reverse) == 0 and reverse != matrix(((0, 0), (0, 0))),
            "reverse assignment is not nonzero rank one")
    require(madd(msub(curvature_forward, curvature_reverse), crossed)
            == matrix(((0, 0), (0, 0))),
            "crossed Bianchi identity failed")
    require(madd(curvature_forward, curvature_reverse)
            == msub(mscale(2, direct), edge_sum),
            "curvature-sum identity failed")

    edge_class = omega(direct, edge_sum)
    crossed_class = omega(direct, crossed)
    require(edge_class == -1, "weighted edge class should be -1")
    require(crossed_class == 3, "crossed row should have nonzero class 3")

    # This is the exact static transport:
    # B = -(1/3)J + (4/3)d + diag(-4/3,-8/3).
    transported = madd(
        madd(mscale(F(-1, 3), crossed), mscale(F(4, 3), direct)),
        diagonal(F(-4, 3), F(-8, 3)),
    )
    require(transported == edge_sum,
            "two anchors plus crossed row did not transport the edge class")

    # Formal completed full-nine top maps on two chart copies.  Coordinates
    # are (Q, X_0, X_1, X_2); the cap symbols themselves are independent.
    direct3 = matrix(((1, 1, 0), (1, 2, 0), (0, 0, 1)))
    for _chart in range(2):
        for i in range(3):
            for j in range(3):
                cap_image = [F(-direct3[i][j]), F(0), F(0), F(0)]
                if i == j:
                    cap_image[1 + i] = F(1)
                lhs = list(cap_image)
                lhs[0] += direct3[i][j]
                target = [F(0), F(0), F(0), F(0)]
                if i == j:
                    target[1 + i] = F(1)
                require(lhs == target,
                        f"formal full-row identity failed at {(i, j)}")

    # Mutation: the familiar opposite sign makes the crossed row class
    # vanish while the edge class survives.  Our packet is strictly past
    # that already-known static obstruction.
    reverse_mutation = matrix(((0, 0), (-1, 0)))
    mutated_sum = madd(forward, reverse_mutation)
    mutated_crossed = msub(forward, reverse_mutation)
    require(omega(direct, mutated_crossed) == 0,
            "crossed-class mutation was not detected")
    require(omega(direct, mutated_sum) == 2,
            "crossed-class mutation also killed the edge class")
    return edge_class


Edge = tuple[int, int]
FourSet = tuple[int, int, int, int]


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def matching_product_map(beta: dict[Edge, F], q: dict[Edge, F]) -> dict[FourSet, F]:
    out = {}
    for vertices in combinations(range(6), 4):
        vertex_set = set(vertices)
        value = F(0)
        for chosen in combinations(vertices, 2):
            chosen_edge = edge(*chosen)
            complement = tuple(sorted(vertex_set - set(chosen)))
            complement_edge = edge(*complement)
            value += beta.get(chosen_edge, F(0)) * q[complement_edge]
        out[vertices] = value
    return out


def dot(left: dict, right: dict) -> F:
    return sum((value * right.get(key, F(0)) for key, value in left.items()), F(0))


def audit_weighted_k6_normal(expected_normal: F) -> None:
    edges = tuple(edge(*pair) for pair in combinations(range(6), 2))
    four_sets = tuple(tuple(vertices) for vertices in combinations(range(6), 4))
    q = {item: F(1) for item in edges}
    cycle = {
        edge(0, 1): F(1),
        edge(2, 3): F(1),
        edge(0, 3): F(-1),
        edge(1, 2): F(-1),
    }
    weighted_cycle = {item: cycle.get(item, F(0)) for item in edges}
    complementary_cut = {}
    for vertices in four_sets:
        missing = tuple(sorted(set(range(6)) - set(vertices)))
        complementary_cut[vertices] = cycle.get(edge(*missing), F(0))

    # Audit mu^T T_q = lambda^T on every edge basis vector, not only on
    # the chosen correction.
    for selected in edges:
        basis = {item: F(item == selected) for item in edges}
        left = dot(complementary_cut, matching_product_map(basis, q))
        right = weighted_cycle[selected]
        require(left == right,
                f"weighted K6 transport failed on edge {selected}")

    correction = {item: F(0) for item in edges}
    correction[edge(0, 1)] = F(-1)
    normal = dot(weighted_cycle, correction)
    transported = dot(complementary_cut, matching_product_map(correction, q))
    require(normal == transported == expected_normal,
            "finite correction did not carry the selected weighted normal")

    # The displayed rectangle is Q+R = ((0,1),(1,1)), of determinant -1.
    finite_rectangle = matrix(((0, 1), (1, 1)))
    require(det2(finite_rectangle) == expected_normal,
            "finite determinant did not equal the linearized normal")

    radial_normal = dot(weighted_cycle, q)
    require(radial_normal == 0,
            "radial mutation should be killed by the four-cycle normal")


def pmul(left: Vector, right: Vector) -> Vector:
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return tuple(out)


QUADRATIC_BASIS = (
    (F(1), F(0), F(0)),  # u^2
    (F(0), F(1), F(0)),  # uv
    (F(0), F(0), F(1)),  # v^2
)


def residual_columns(cubic: Vector) -> list[Vector]:
    require(len(cubic) == 4, "expected a binary cubic")
    # For f=v^3, f*S_2 is exactly the last three monomial coordinates in
    # S_5.  Q_f has basis u^5,u^4v,u^3v^2.
    return [pmul(cubic, quadratic)[:3] for quadratic in QUADRATIC_BASIS]


def audit_triple_root_macaulay() -> None:
    f = (F(0), F(0), F(0), F(1))  # v^3
    f_columns = [pmul(f, quadratic) for quadratic in QUADRATIC_BASIS]
    require(exact_rank(f_columns) == 3, "the exposed f-block lost rank")

    probes = (
        (F(1), F(0), F(0), F(0)),
        (F(2), F(-3), F(5), F(7)),
        (F(-4, 3), F(2, 5), F(-7, 2), F(11, 6)),
        (F(0), F(1), F(2), F(3)),
    )
    for cubic in probes:
        a, b, c, _d = cubic
        columns = residual_columns(cubic)
        expected = [
            (a, b, c),
            (F(0), a, b),
            (F(0), F(0), a),
        ]
        require(columns == expected, "residual triangular matrix is wrong")
        column_matrix = tuple(tuple(columns[column][row] for column in range(3))
                              for row in range(3))
        require(det3(column_matrix) == a ** 3,
                "residual determinant is not the cube of g(1,0)")

    # The rootless packet: f=v^3 and g=u^3 have no common projective root,
    # and the one residual channel fills all of Q_f.
    g = (F(1), F(0), F(0), F(0))
    g_columns = residual_columns(g)
    require(exact_rank(g_columns) == 3,
            "u^3 did not fill the residual quotient")
    require(exact_rank(f_columns + [pmul(g, quadratic)
                                    for quadratic in QUADRATIC_BASIS]) == 6,
            "the full h=3 Macaulay map should be surjective")

    # Sharp mutation: deleting only [u^3]g makes evaluation at [1:0]
    # annihilate every residual column and drops the rank to at most two.
    boundary = (F(0), F(1), F(2), F(3))
    boundary_columns = residual_columns(boundary)
    evaluation = (F(1), F(0), F(0))
    require(all(sum((a * b for a, b in zip(evaluation, column)), F(0)) == 0
                for column in boundary_columns),
            "evaluation at [1:0] did not annihilate the boundary image")
    require(exact_rank(boundary_columns) == 2,
            "the leading-coefficient mutation should give the sharp rank-two boundary")


def main() -> None:
    normal = audit_two_anchor_crossed_packet()
    audit_weighted_k6_normal(normal)
    audit_triple_root_macaulay()
    print(
        "rootless h=3 weighted-normal triple-root boundary: PASS; "
        "static crossed transport, K6 normal, and sharp Macaulay coefficient audited"
    )


if __name__ == "__main__":
    main()
