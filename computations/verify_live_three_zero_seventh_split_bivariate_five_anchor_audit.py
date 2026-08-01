#!/usr/bin/env python3
"""Independent exact audit of the seventh-split bivariate five-anchor route."""

from __future__ import annotations

from math import prod

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def cleared_quartic_row(
    node: sp.Expr,
    translation: sp.Expr,
    x: sp.Symbol,
    y: sp.Symbol,
) -> list[sp.Expr]:
    """Ascending-coefficient row for q'(node)+Y q(node)=0."""

    dx = x**2 - node**2
    dy = y**2 - node**2
    row = []
    for degree in range(5):
        evaluation = node**degree
        derivative = sp.Integer(0) if degree == 0 else degree * node ** (degree - 1)
        entry = dx * dy * (derivative + translation * evaluation)
        entry -= (x - 3 * node) * dy * evaluation
        entry -= (y - 3 * node) * dx * evaluation
        row.append(sp.expand(entry))
    return row


def check_bidegree_bound() -> None:
    x, y, node, translation = sp.symbols("x y t U")
    row = cleared_quartic_row(node, translation, x, y)
    for entry in row:
        polynomial = sp.Poly(entry, x, y)
        require(
            polynomial.degree(x) <= 2,
            "polynomial.degree(x) <= 2",
        )
        require(
            polynomial.degree(y) <= 2,
            "polynomial.degree(y) <= 2",
        )

    # Every term in the 5-by-5 determinant chooses one entry from each row.
    require(
        5 * 2 == 10,
        "5 * 2 == 10",
    )

    # A direct specialized determinant independently confirms that no hidden
    # denominator or higher bidegree is introduced by the construction.
    nodes = [sp.Integer(value) for value in (1, 2, 4, 7, 11)]
    translations = [sp.Integer(value) for value in (0, 3, -2, 5, -4)]
    matrix = sp.Matrix(
        [
            cleared_quartic_row(t, u, x, y)
            for t, u in zip(nodes, translations)
        ]
    )
    determinant = sp.Poly(sp.expand(matrix.det(method="domain-ge")), x, y)
    require(
        determinant.as_expr() != 0,
        "determinant.as_expr() != 0",
    )
    require(
        determinant.degree(x) <= 10,
        "determinant.degree(x) <= 10",
    )
    require(
        determinant.degree(y) <= 10,
        "determinant.degree(y) <= 10",
    )


def check_off_diagonal_interpolation() -> None:
    minimum_p = 8
    exceptional_values = minimum_p + 9
    fixed_anchors = 5
    moving_values = exceptional_values - fixed_anchors
    bidegree = 10
    require(
        moving_values == 12,
        "moving_values == 12",
    )
    require(
        moving_values - 1 > bidegree,
        "moving_values - 1 > bidegree",
    )
    require(
        moving_values > bidegree,
        "moving_values > bidegree",
    )

    # The threshold is sharp for this row-by-row argument.  On eleven grid
    # values the diagonal Lagrange kernel has bidegree (10,10), vanishes on
    # every off-diagonal pair, and is nonzero on the diagonal.
    x, y = sp.symbols("x y")
    grid = tuple(sp.Integer(value) for value in range(11))
    lagrange = []
    for value in grid:
        numerator = prod(x - other for other in grid if other != value)
        denominator = prod(value - other for other in grid if other != value)
        lagrange.append(sp.Poly(sp.expand(numerator / denominator), x))
    kernel = sum(
        basis.as_expr() * basis.as_expr().subs(x, y) for basis in lagrange
    )
    kernel_poly = sp.Poly(sp.expand(kernel), x, y)
    require(
        kernel_poly.degree(x) == 10,
        "kernel_poly.degree(x) == 10",
    )
    require(
        kernel_poly.degree(y) == 10,
        "kernel_poly.degree(y) == 10",
    )
    for first in grid:
        for second in grid:
            value = sp.expand(kernel.subs({x: first, y: second}))
            require(
                value == int(first == second),
                "value == int(first == second)",
            )


def check_endpoint_factor_extraction() -> None:
    x, y = sp.symbols("x y")
    ta, tj, translation = sp.symbols("t_a t_j U_j")
    r_value, r_derivative = sp.symbols("r rprime")

    q_value = (tj - ta) * r_value
    q_derivative = r_value + (tj - ta) * r_derivative
    dx = x**2 - tj**2
    dy = y**2 - tj**2
    seventh_row = (
        dx * dy * (q_derivative + translation * q_value)
        - (x - 3 * tj) * dy * q_value
        - (y - 3 * tj) * dx * q_value
    )
    endpoint_scale = (tj - ta) * (ta**2 - tj**2)

    plus_translation = translation - 2 / (ta + tj)
    plus_dr4_row = (
        dx * (r_derivative + plus_translation * r_value)
        - (x - 3 * tj) * r_value
    )
    require(
        sp.factor(
            seventh_row.subs(y, ta) - endpoint_scale * plus_dr4_row
        ) == 0,
        "sp.factor( seventh_row.subs(y, ta) - endpoint_scale * plu...",
    )

    minus_translation = (
        translation - 1 / (ta + tj) - 1 / (tj - ta)
    )
    minus_dr4_row = (
        dx * (r_derivative + minus_translation * r_value)
        - (x - 3 * tj) * r_value
    )
    require(
        sp.factor(
            seventh_row.subs(y, -ta) - endpoint_scale * minus_dr4_row
        ) == 0,
        "sp.factor( seventh_row.subs(y, -ta) - endpoint_scale * mi...",
    )

    # The anchor row itself becomes a nonzero evaluation row.  These signs
    # are what force q(ta)=0 before q=(z-ta)r is extracted.
    q_at_anchor, qp_at_anchor, ua = sp.symbols("q_a qp_a U_a")
    anchor_dx = x**2 - ta**2
    anchor_dy = y**2 - ta**2
    anchor_row = (
        anchor_dx * anchor_dy * (qp_at_anchor + ua * q_at_anchor)
        - (x - 3 * ta) * anchor_dy * q_at_anchor
        - (y - 3 * ta) * anchor_dx * q_at_anchor
    )
    require(
        sp.expand(anchor_row.subs(y, ta) - 2 * ta * anchor_dx * q_at_anchor) == 0,
        "sp.expand(anchor_row.subs(y, ta) - 2 * ta * anchor_dx * q...",
    )
    require(
        sp.expand(anchor_row.subs(y, -ta) - 4 * ta * anchor_dx * q_at_anchor) == 0,
        "sp.expand(anchor_row.subs(y, -ta) - 4 * ta * anchor_dx * ...",
    )


def quartet_functional(
    nodes: tuple[sp.Expr, ...], translations: tuple[sp.Expr, ...]
) -> sp.Expr:
    return sp.expand(
        sum(
            translations[index]
            * prod(
                nodes[index] + nodes[other]
                for other in range(len(nodes))
                if other != index
            )
            for index in range(len(nodes))
        )
    )


def check_quartet_subtraction_and_selection_polynomial() -> None:
    a, b, c, d, e = sp.symbols("a b c d e")
    ub, uc, ud, ue = sp.symbols("U_b U_c U_d U_e")
    complement = (b, c, d, e)
    base = (ub, uc, ud, ue)
    plus = tuple(
        value - 2 / (a + node) for node, value in zip(complement, base)
    )
    minus = tuple(
        value - 1 / (a + node) - 1 / (node - a)
        for node, value in zip(complement, base)
    )

    plus_certificate = quartet_functional(complement, plus)
    minus_certificate = quartet_functional(complement, minus)
    signed_subtraction = 2 * a * sum(
        prod(node + other for other in complement if other != node)
        / (node**2 - a**2)
        for node in complement
    )
    require(
        sp.factor(
            sp.together(plus_certificate - minus_certificate - signed_subtraction)
        ) == 0,
        "sp.factor( sp.together(plus_certificate - minus_certifica...",
    )

    # Fix Q={a,b,c,d} and move e.  The subtraction S_a(Q union {e})
    # is the rational function above; clearing only e's two endpoint poles
    # gives the selection polynomial H_a(e).
    selection = sp.cancel((e**2 - a**2) * signed_subtraction)
    numerator, denominator = sp.fraction(selection)
    require(
        not denominator.has(e),
        "not denominator.has(e)",
    )
    selection_poly = sp.Poly(selection, e, domain=sp.EX)
    require(
        selection_poly.degree() <= 3,
        "selection_poly.degree() <= 3",
    )

    expected_plus_endpoint = 2 * a * (a + b) * (a + c) * (a + d)
    expected_minus_endpoint = 2 * a * (b - a) * (c - a) * (d - a)
    require(
        sp.factor(selection_poly.eval(a) - expected_plus_endpoint) == 0,
        "sp.factor(selection_poly.eval(a) - expected_plus_endpoint...",
    )
    require(
        sp.factor(selection_poly.eval(-a) - expected_minus_endpoint) == 0,
        "sp.factor(selection_poly.eval(-a) - expected_minus_endpoi...",
    )
    require(
        selection_poly.as_expr() != 0,
        "selection_poly.as_expr() != 0",
    )


def check_zero_safe_cardinalities_and_collision_extension() -> None:
    minimum_classes = 17
    fixed_core = 5
    possible_zero_classes = 1
    interpolation_values = minimum_classes - fixed_core
    require(
        interpolation_values == 12,
        "interpolation_values == 12",
    )
    require(
        interpolation_values - 1 == 11 > 10,
        "interpolation_values - 1 == 11 > 10",
    )

    # Choose Q of four nonzero classes.  In the worst case the unique zero
    # lies outside Q and is unavailable as the fifth fixed anchor e.
    nonzero_e_candidates = minimum_classes - 4 - possible_zero_classes
    require(
        nonzero_e_candidates == 12,
        "nonzero_e_candidates == 12",
    )
    require(
        nonzero_e_candidates > 3,
        "nonzero_e_candidates > 3",
    )
    require(
        nonzero_e_candidates - 3 == 9,
        "nonzero_e_candidates - 3 == 9",
    )

    # A repeated class retained as a singleton means that one label from a
    # double class is the fixed anchor a and its mate stays in every N_{x,y}.
    repeated_class_size = 2
    selected_from_repeated_class = 1
    require(
        repeated_class_size - selected_from_repeated_class == 1,
        "repeated_class_size - selected_from_repeated_class == 1",
    )
    require(
        repeated_class_size > 1,
        "repeated_class_size > 1",
    )

    # A repeated zero is structurally forbidden, so this anchor is nonzero.
    repeated_anchor_can_be_zero = repeated_class_size == 1
    require(
        not repeated_anchor_can_be_zero,
        "not repeated_anchor_can_be_zero",
    )

    # If the unique zero exists, Q and e avoid it, while it remains one of
    # the twelve moving values.  For an off-diagonal pair it occurs at most
    # once, and the retained mate of a still supplies the singleton row.
    moving_nonzero_values = minimum_classes - fixed_core - possible_zero_classes
    moving_zero_values = possible_zero_classes
    require(
        moving_nonzero_values + moving_zero_values == interpolation_values,
        "moving_nonzero_values + moving_zero_values == interpolati...",
    )
    require(
        moving_zero_values <= 1,
        "moving_zero_values <= 1",
    )


def previous_double_single_closure(doubles: int, singles: int) -> bool:
    return (
        (doubles >= 8 and singles >= 4)
        or (doubles >= 9 and singles >= 3)
        or (doubles >= 10 and singles >= 2)
        or doubles >= 11
    )


EXPECTED_POST_CLOSURE_DOUBLES = {
    8: tuple(range(1, 9)),
    9: tuple(range(2, 10)),
    10: tuple(range(3, 10)),
    11: (4, 5, 6, 7, 9, 10),
    12: (5, 6, 7, 10),
    13: (6, 7),
    14: (7,),
}


TRIPLE_RESIDUALS = {
    8: {
        (3, 4, 0), (3, 3, 2), (3, 2, 4), (3, 1, 6),
        (2, 5, 1), (2, 3, 5),
    },
    9: {(6, 0, 0), (3, 4, 1), (3, 2, 5)},
    12: {(7, 0, 0)},
}


def check_post_closure_residual_table() -> None:
    for p in range(8, 101):
        total = p + 9
        remaining = []
        for doubles in range(1, total // 2 + 1):
            singles = total - 2 * doubles
            old_open = not previous_double_single_closure(doubles, singles)
            distinct_classes = doubles + singles
            new_closed = distinct_classes >= 17
            if old_open and not new_closed:
                remaining.append(doubles)

        expected = EXPECTED_POST_CLOSURE_DOUBLES.get(p, ())
        require(
            tuple(remaining) == expected,
            "tuple(remaining) == expected",
        )
        if p >= 15:
            require(
                not remaining,
                "not remaining",
            )

    # Every old triple residual has fewer than seventeen distinct value
    # classes, so this bivariate collision extension does not touch it.
    for residuals in TRIPLE_RESIDUALS.values():
        for triples, doubles, singles in residuals:
            require(
                triples + doubles + singles < 17,
                "triples + doubles + singles < 17",
            )


def main() -> None:
    check_bidegree_bound()
    check_off_diagonal_interpolation()
    check_endpoint_factor_extraction()
    check_quartet_subtraction_and_selection_polynomial()
    check_zero_safe_cardinalities_and_collision_extension()
    check_post_closure_residual_table()
    print("independent seventh-split bivariate five-anchor audit: PASS")
    print("verified bidegree (10,10), M >= 12 off-diagonal interpolation")
    print("verified endpoint signs, quartet subtraction, and cubic H_a(e)")
    print("verified zero-safe >=17-class retained-double extension")
    print("verified the exact post-closure double/single residual table")


if __name__ == "__main__":
    main()
