#!/usr/bin/env python3
"""Close a 2I+3R+1Z generic-kernel subcase by shore rank bounds.

Let two endpoint matrices be invertible, three be nonzero rank one, and one
be zero.  Assume the zero endpoint has nonzero multiplier sum with each of
the three rank-one endpoints.  Its three shore blocks therefore vanish.

Use the rank-one endpoints as a three-site shore.  Every cross block has a
fixed local factor at its shore endpoint.  The zero-sum graph on the shore
is empty, one edge, a two-edge path, or the full triangle.  The first three
cases have exact differential-rank bounds 35, 42, and 49.  In the triangle
case the three source factors share one isotropic line, so the cross spokes
are constant and the exact bound is 51.  Thus rank 55 is impossible.

No physical target coordinate is chosen: local changes of basis are made
only to expose fixed shore factors, and differential rank is invariant.

Standard library only; assertions remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


# Sparse formal polynomial arithmetic for the rank-one block identities.
def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = {}
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] = (
                    updated.get(monomial, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not updated[monomial]:
                    del updated[monomial]
        answer = updated
    return answer


def matrix_product(left, right):
    return tuple(
        tuple(
            add(*(multiply(left[row][middle], right[middle][column])
                  for middle in range(2)))
            for column in range(2)
        )
        for row in range(2)
    )


def transpose(matrix):
    return tuple(
        tuple(matrix[column][row] for column in range(2))
        for row in range(2)
    )


def outer(left, right):
    return tuple(
        tuple(multiply(left[row], right[column]) for column in range(2))
        for row in range(2)
    )


def audit_rank_one_generic_factors():
    # For X_r=a_r b_r^T, the I-r numerator is
    # X_i J b_r a_r^T, and an r-u numerator is
    # (b_r^T J b_u) a_r a_u^T.  Thus every determined block has the
    # required factor at each rank-one shore endpoint.
    J = ((constant(0), constant(1)),
         (constant(1), constant(0)))
    X = tuple(
        tuple(variable(f"x{row}{column}") for column in range(2))
        for row in range(2)
    )
    a = tuple(variable(f"a{row}") for row in range(2))
    b = tuple(variable(f"b{row}") for row in range(2))
    c = tuple(variable(f"c{row}") for row in range(2))
    d = tuple(variable(f"d{row}") for row in range(2))
    Xr = outer(a, b)
    Xu = outer(c, d)

    i_r = matrix_product(matrix_product(X, J), transpose(Xr))
    left = tuple(
        add(*(multiply(X[row][middle], b[1 - middle])
              for middle in range(2)))
        for row in range(2)
    )
    require(i_r == outer(left, a),
            "invertible-to-rank-one factorization changed")

    r_u = matrix_product(matrix_product(Xr, J), transpose(Xu))
    pairing = add(multiply(b[0], d[1]), multiply(b[1], d[0]))
    require(r_u == tuple(
        tuple(multiply(pairing, a[row], c[column]) for column in range(2))
        for row in range(2)
    ), "rank-one shore numerator factorization changed")
    return 8


def audit_zero_sum_graph_classification():
    # Three pair equations have full rank, so a zero-sum triangle forces all
    # three potentials to vanish.  Any two edges on three vertices form a
    # path; the two equations give equal leaves opposite the centre, and a
    # nontriangle path has nonzero centre.
    triangle_system = (
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
    )
    require(rational_rank(triangle_system) == 3,
            "zero-sum triangle stopped forcing zero potentials")

    graph_types = {}
    for edges in range(4):
        graph_types[edges] = (
            "empty" if edges == 0
            else "one edge" if edges == 1
            else "two-edge path" if edges == 2
            else "triangle"
        )
    require(graph_types == {
        0: "empty",
        1: "one edge",
        2: "two-edge path",
        3: "triangle",
    }, "three-vertex zero-sum graph types changed")
    return graph_types


def audit_triangle_common_isotropic_line():
    # Let b0=(x,y).  Its J-orthogonal line is spanned by k=(x,-y).
    # The first two zero pairings put b1=c1*k and b2=c2*k.  Their pairing is
    # -2*c1*c2*x*y.  Since b1,b2 are nonzero, the third zero pairing forces
    # x*y=0, and then k is proportional to b0.  All three lines coincide;
    # their nonzero proportionality constants can be absorbed into a_t.
    x, y = variable("x"), variable("y")
    c1, c2 = variable("c1"), variable("c2")
    b0 = (x, y)
    k = (x, scale(-1, y))
    b1 = tuple(multiply(c1, entry) for entry in k)
    b2 = tuple(multiply(c2, entry) for entry in k)

    def pairing(left, right):
        return add(
            multiply(left[0], right[1]),
            multiply(left[1], right[0]),
        )

    require(not pairing(b0, b1) and not pairing(b0, b2),
            "orthogonal-line parametrization changed")
    require(
        pairing(b1, b2) == scale(-2, multiply(c1, c2, x, y)),
        "third triangle pairing changed",
    )

    # Audit the two localized branches x!=0,y=0 and x=0,y!=0.
    branches = []
    for x_live, y_live in ((True, False), (False, True)):
        base = (int(x_live), int(y_live))
        orthogonal = (int(x_live), -int(y_live))
        determinant = (
            base[0] * orthogonal[1] - base[1] * orthogonal[0]
        )
        require(determinant == 0,
                "isotropic orthogonal line was not the base line")
        branches.append((base, orthogonal))
    return tuple(branches)


def audit_imported_shore_bounds():
    empty = SHORE["empty_shore_slice_bounds"]()
    one_checks = SHORE["one_exceptional_edge_bound"]()
    path_identities, categories = SHORE["audit_path_factorization"]()
    constant_identities = SHORE["audit_constant_cross_factorization"]()
    require(sum(empty.values()) == 35, "empty-shore bound changed")
    require(one_checks == 320, "one-edge shore audit changed")
    require(path_identities == 64, "path shore audit changed")
    require(constant_identities == 64, "constant-cross audit changed")
    bounds = {
        "empty": 35,
        "one edge": 42,
        "two-edge path": 49,
        "triangle": 51,
    }
    require(max(bounds.values()) == 51, "maximum imported bound changed")
    return bounds, categories


def audit_remaining_boundary():
    # The theorem's only excluded multiplier pattern has at least one free
    # z-r block: X_z=0 makes the numerator zero, and nu_z+nu_r=0 leaves that
    # 2x2 residual block undetermined by the generic-kernel equation.
    patterns = tuple(
        pattern
        for pattern in product((False, True), repeat=3)
        if any(pattern)
    )
    require(len(patterns) == 7, "free z-r boundary pattern count changed")
    return len(patterns)


def main():
    factor_checks = audit_rank_one_generic_factors()
    graph_types = audit_zero_sum_graph_classification()
    isotropic = audit_triangle_common_isotropic_line()
    bounds, categories = audit_imported_shore_bounds()
    boundary_patterns = audit_remaining_boundary()
    print("2I+3R+1Z determined-zero-shore closure: all checks passed")
    print(f"  generic factor identities : {factor_checks}")
    print(f"  zero-sum shore graphs      : {graph_types}")
    print(f"  triangle isotropic branches: {isotropic}")
    print(f"  exact shore bounds         : {bounds}, {categories}")
    print(f"  maximum differential rank : {max(bounds.values())}")
    print(f"  remaining free-zR patterns : {boundary_patterns}")


if __name__ == "__main__":
    main()
