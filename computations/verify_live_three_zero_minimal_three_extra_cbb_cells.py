#!/usr/bin/env python3
"""Exact direct-free rank certificates on all three CBB cells.

For each placement, x,y are the parameters of the central (01-chart)
plane and u,v are the free parameters of the two boundary (12-chart)
planes.  The structural second parameters of the boundary charts vanish.
The checker covers the six factors of one initial maximal minor and audits
all localizations exactly over QQ.
"""

from __future__ import annotations

import argparse

import sympy as sp

import explore_live_three_zero_minimal_three_extra_response as response


DEFAULT_PRIME = 1_000_003
PARAMETER_NAMES = ("a", "b", "c", "d", "e", "f")
ACTUAL_SYMBOLS = sp.symbols("a b c d e f")
ACTUAL_BY_NAME = dict(zip(PARAMETER_NAMES, ACTUAL_SYMBOLS))
x, y, u, v = sp.symbols("x y u v")
STANDARD_SYMBOLS = (x, y, u, v)
R = sp.Rational

CELL_SPECS = {
    "CBB": {
        "charts": ("01", "12", "12"),
        "names": {"x": "a", "y": "b", "u": "c", "v": "e"},
        "structural": {"d": 0, "f": 0},
    },
    "BCB": {
        "charts": ("12", "01", "12"),
        "names": {"x": "c", "y": "d", "u": "a", "v": "e"},
        "structural": {"b": 0, "f": 0},
    },
    "BBC": {
        "charts": ("12", "12", "01"),
        "names": {"x": "e", "y": "f", "u": "a", "v": "c"},
        "structural": {"b": 0, "d": 0},
    },
}

SAMPLE_POINTS = (
    (0, 0, 0),
    (-3, -1, -3),
    (-3, -2, -3),
    (-3, -3, -3),
    (-3, -3, R(-1, 2)),
    (R(2, 5), -3, -3),
    (2, -3, -3),
    (1, -1, 0),
    (1, -2, 0),
    (1, -3, 0),
    (-2, 0, 0),
    (0, -1, 1),
    (-2, -1, 1),
    (0, -2, 1),
    (-2, -2, 1),
    (0, -3, 1),
    (-2, -3, 1),
    (0, 0, R(-1, 2)),
    (-2, 0, R(-1, 2)),
    (-2, -3, 0),
    (-3, -3, 0),
    (0, -1, 0),
    (0, -1, R(-1, 2)),
    (0, -2, 0),
    (0, -2, R(-1, 2)),
    (0, -3, 0),
    (0, -3, R(-1, 2)),
)

CURVE_POINTS = (
    (0, 1), (-1, 1), (-2, 1), (-3, 1),
    (0, -1), (0, -2), (0, -3), (-1, -1), (-2, -2), (-3, -3),
    (1, 1), (R(-1, 2), R(-1, 2)), (1, R(-1, 2)),
    (-2, R(-1, 2)),
)

Y_BRANCH_MODULAR_POINTS = {
    -1: (
        (101, (30, 35, 52)),
        (101, (30, 52, 35)),
        (101, (63, 1, 57)),
        (101, (63, 57, 1)),
        (101, (98, 0, 0)),
        (101, (98, 0, 50)),
        (101, (98, 50, 0)),
        (103, (63, 51, 85)),
        (103, (63, 85, 51)),
    ),
    -2: (
        (101, (3, 8, 8)),
        (101, (8, 63, 50)),
        (101, (90, 48, 48)),
        (101, (98, 0, 0)),
        (101, (98, 0, 50)),
        (101, (98, 50, 0)),
        (103, (64, 51, 37)),
        (103, (94, 51, 23)),
    ),
}


def modular_value(value, prime):
    value = R(value)
    return int(value.p) * pow(int(value.q), prime - 2, prime) % prime


def actual_name(spec, standard_name):
    return spec["names"][standard_name]


def standard_to_actual_substitution(spec):
    return {
        ACTUAL_BY_NAME[actual_name(spec, name)]: symbol
        for name, symbol in zip(("x", "y", "u", "v"), STANDARD_SYMBOLS)
    }


def full_actual_values(spec, standard_values):
    values = {name: R(value) for name, value in spec["structural"].items()}
    values.update(
        {
            actual_name(spec, name): R(value)
            for name, value in zip(("x", "y", "u", "v"), standard_values)
        }
    )
    return tuple(values[name] for name in PARAMETER_NAMES)


def selected_labels(spec, standard_values, prime=DEFAULT_PRIME, raw=False):
    actual_values = full_actual_values(spec, standard_values)
    response.PRIME = prime
    modular = tuple(
        int(value) % prime if raw else modular_value(value, prime)
        for value in actual_values
    )
    selected = response.select_labels(
        spec["charts"], modular, excluded_sources=((0, 1),)
    )
    assert len(selected) == 19
    labels = tuple(label for _row_support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    return labels


def squarefree_support(value, variables):
    if isinstance(value, sp.Integer):
        assert value != 0
        return sp.S.One
    local_map = {str(symbol): symbol for symbol in ACTUAL_SYMBOLS}
    product = sp.S.One
    for factor, _multiplicity in value.factor()[1]:
        product *= sp.sympify(
            str(factor).replace("^", "**"), locals=local_map
        )
    return sp.Poly(product, *variables, domain=sp.QQ).sqf_part().monic().as_expr()


def fixed_support(spec, labels, fixed_standard, free_standard):
    substitutions = dict(spec["structural"])
    substitutions.update(
        {
            actual_name(spec, name): value
            for name, value in fixed_standard.items()
        }
    )
    actual_variables = tuple(
        ACTUAL_BY_NAME[actual_name(spec, name)] for name in free_standard
    )
    determinant = response.flint_restricted_determinant(
        spec["charts"], labels, substitutions
    )
    polynomial = squarefree_support(determinant, actual_variables)
    rename = {
        ACTUAL_BY_NAME[actual_name(spec, name)]: STANDARD_SYMBOLS[
            ("x", "y", "u", "v").index(name)
        ]
        for name in free_standard
    }
    standard_variables = tuple(
        STANDARD_SYMBOLS[("x", "y", "u", "v").index(name)]
        for name in free_standard
    )
    return sp.Poly(
        polynomial.xreplace(rename), *standard_variables, domain=sp.QQ
    ).monic().as_expr()


def rational_support(spec, labels, standard_substitutions, free_standard):
    substitutions = dict(spec["structural"])
    actual_rename = standard_to_actual_substitution(spec)
    inverse_rename = {standard: actual for actual, standard in actual_rename.items()}
    substitutions.update(
        {
            actual_name(spec, name): sp.sympify(value).xreplace(inverse_rename)
            for name, value in standard_substitutions.items()
        }
    )
    free_actual_names = tuple(actual_name(spec, name) for name in free_standard)
    actual_variables = tuple(ACTUAL_BY_NAME[name] for name in free_actual_names)
    determinant, _multiplier = response.flint_rational_restriction(
        spec["charts"], labels, substitutions, free_actual_names
    )
    polynomial = squarefree_support(determinant, actual_variables)
    rename = {
        ACTUAL_BY_NAME[actual_name(spec, name)]: STANDARD_SYMBOLS[
            ("x", "y", "u", "v").index(name)
        ]
        for name in free_standard
    }
    standard_variables = tuple(
        STANDARD_SYMBOLS[("x", "y", "u", "v").index(name)]
        for name in free_standard
    )
    return sp.Poly(
        polynomial.xreplace(rename), *standard_variables, domain=sp.QQ
    ).monic().as_expr()


def unit_ideal(polynomials, variables):
    basis = sp.groebner(
        polynomials, *variables, order="grevlex", domain=sp.QQ
    )
    return basis.reduce(sp.S.One)[1] == 0


def assert_origin_cover(spec):
    labels = selected_labels(spec, (0, 0, 0, 0))
    polynomial = fixed_support(spec, labels, {}, ("x", "y", "u", "v"))
    denominator = 2*u + 2*v + 1
    coefficient = 2*u**2 - 4*u*v - 4*u + 2*v**2 - 4*v - 3
    expected = (
        (y + 1) * (y + 2) * (2*u + 1) * (2*v + 1)
        * (x*denominator + 2)
        * (x*coefficient - 8*u - 8*v - 6)
    )
    variables = (x, y, u, v)
    assert sp.Poly(polynomial, *variables, domain=sp.QQ).monic() == sp.Poly(
        expected, *variables, domain=sp.QQ
    ).monic()


def assert_y_branch(spec, yvalue):
    polynomials = []
    for xvalue, uvalue, vvalue in SAMPLE_POINTS:
        labels = selected_labels(spec, (xvalue, yvalue, uvalue, vvalue))
        polynomial = fixed_support(
            spec, labels, {"y": yvalue}, ("x", "u", "v")
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    for prime, point in Y_BRANCH_MODULAR_POINTS[yvalue]:
        xvalue, uvalue, vvalue = point
        labels = selected_labels(
            spec, (xvalue, yvalue, uvalue, vvalue), prime=prime, raw=True
        )
        polynomial = fixed_support(
            spec, labels, {"y": yvalue}, ("x", "u", "v")
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    assert unit_ideal(polynomials, (x, u, v))


def assert_half_branch(spec, half_name):
    other = "v" if half_name == "u" else "u"
    other_symbol = v if other == "v" else u
    fixed = {half_name: R(-1, 2)}
    polynomials = []
    for xvalue, yvalue, other_value in SAMPLE_POINTS:
        values = {"x": xvalue, "y": yvalue, half_name: R(-1, 2), other: other_value}
        labels = selected_labels(
            spec, tuple(values[name] for name in ("x", "y", "u", "v"))
        )
        polynomial = fixed_support(
            spec, labels, fixed, ("x", "y", other)
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    basis = sp.groebner(
        polynomials, x, y, other_symbol, order="grevlex", domain=sp.QQ
    )
    expected = x*other_symbol + 1
    assert len(basis.polys) == 1
    assert sp.Poly(basis.polys[0].as_expr(), x, y, other_symbol).monic() == sp.Poly(
        expected, x, y, other_symbol
    ).monic()

    curve_polynomials = []
    for yvalue, other_value in CURVE_POINTS:
        values = {
            "x": -1/R(other_value),
            "y": yvalue,
            half_name: R(-1, 2),
            other: other_value,
        }
        labels = selected_labels(
            spec, tuple(values[name] for name in ("x", "y", "u", "v"))
        )
        polynomial = rational_support(
            spec,
            labels,
            {"x": -1/other_symbol, half_name: R(-1, 2)},
            ("y", other),
        )
        if polynomial not in curve_polynomials:
            curve_polynomials.append(polynomial)

    # The relation x*other+1 itself excludes other=0.  One additional row
    # set is nonzero at the only residual point other=1/2; after adjoining
    # it, the exact curve-minor ideal is simply supported at other=0.
    values = {
        "x": -2,
        "y": -1,
        half_name: R(-1, 2),
        other: R(1, 2),
    }
    labels = selected_labels(
        spec, tuple(values[name] for name in ("x", "y", "u", "v"))
    )
    curve_polynomials.append(
        rational_support(
            spec,
            labels,
            {"x": -1/other_symbol, half_name: R(-1, 2)},
            ("y", other),
        )
    )
    tau = sp.symbols("tau")
    assert unit_ideal(
        curve_polynomials + [1-tau*other_symbol],
        (y, other_symbol, tau),
    )


def assert_t_branch(spec):
    denominator = 2*u + 2*v + 1
    polynomials = []
    for yvalue, uvalue, vvalue in SAMPLE_POINTS:
        denominator_value = denominator.subs({u: uvalue, v: vvalue})
        if denominator_value == 0:
            continue
        xvalue = -R(2) / denominator_value
        labels = selected_labels(spec, (xvalue, yvalue, uvalue, vvalue))
        polynomial = rational_support(
            spec,
            labels,
            {"x": -2/denominator},
            ("y", "u", "v"),
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    tau = sp.symbols("tau")
    assert unit_ideal(polynomials + [1-tau*denominator], (y, u, v, tau))


def assert_r_open_branch(spec):
    coefficient = 2*u**2 - 4*u*v - 4*u + 2*v**2 - 4*v - 3
    line = 4*u + 4*v + 3
    coefficient_poly = sp.Poly(coefficient, y, u, v, domain=sp.QQ)
    line_poly = sp.Poly(line, y, u, v, domain=sp.QQ)
    polynomials = []

    def add(labels):
        polynomial = sp.Poly(
            rational_support(
                spec,
                labels,
                {"x": 2*line/coefficient},
                ("y", "u", "v"),
            ),
            y, u, v, domain=sp.QQ,
        )
        polynomial = polynomial.exquo(sp.gcd(polynomial, coefficient_poly))
        assert polynomial.rem(line_poly) == 0
        quotient = polynomial.exquo(line_poly).monic().as_expr()
        if quotient not in polynomials:
            polynomials.append(quotient)

    for yvalue, uvalue, vvalue in SAMPLE_POINTS:
        coefficient_value = coefficient.subs({u: uvalue, v: vvalue})
        if coefficient_value == 0:
            continue
        xvalue = R(2) * line.subs({u: uvalue, v: vvalue}) / coefficient_value
        add(selected_labels(spec, (xvalue, yvalue, uvalue, vvalue)))

    prime = 43
    yvalue, uvalue, vvalue = (5, 40, 41)
    coefficient_value = int(coefficient.subs({u: uvalue, v: vvalue})) % prime
    line_value = int(line.subs({u: uvalue, v: vvalue})) % prime
    xvalue = 2*line_value*pow(coefficient_value, prime-2, prime) % prime
    add(
        selected_labels(
            spec, (xvalue, yvalue, uvalue, vvalue), prime=prime, raw=True
        )
    )

    basis = sp.groebner(
        polynomials, y, u, v, order="grevlex", domain=sp.QQ
    )
    assert basis.is_zero_dimensional
    tau = sp.symbols("tau")
    assert unit_ideal(
        [polynomial.as_expr() for polynomial in basis.polys]
        + [1-tau*coefficient*line],
        (y, u, v, tau),
    )


def assert_r_line_branch(spec):
    substitutions = {"x": 0, "v": -R(3, 4)-u}
    points = (
        (0, 0), (-1, 0), (-2, 0), (-3, 0),
        (0, -1), (0, -2), (0, -3), (-1, -1), (-2, -2), (-3, -3),
        (1, 1), (R(-1, 2), R(-1, 2)),
        (0, R(-3, 4)), (-1, R(-3, 4)), (-2, R(-3, 4)),
        (-3, R(-3, 4)),
    )
    polynomials = []
    for yvalue, uvalue in points:
        labels = selected_labels(
            spec, (0, yvalue, uvalue, -R(3, 4)-uvalue)
        )
        polynomial = rational_support(
            spec, labels, substitutions, ("y", "u")
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    for yvalue, uvalue in (
        (0, R(-1, 2)),
        (-2, R(-1, 2)),
        (-1, R(-1, 2)),
        (-1, R(-1, 4)),
    ):
        labels = selected_labels(
            spec, (0, yvalue, uvalue, -R(3, 4)-uvalue)
        )
        polynomials.append(
            rational_support(spec, labels, substitutions, ("y", "u"))
        )
    assert unit_ideal(polynomials, (y, u))


def assert_r_special_branch(spec):
    fixed = {"u": R(-3, 8), "v": R(-3, 8)}
    points = (
        (0, 0), (-2, 0), (0, -3), (0, -1), (-2, -3),
        (-2, -1), (1, 1), (-1, -2), (R(-1, 2), 0),
        (4, -1), (0, -2),
    )
    polynomials = []
    for xvalue, yvalue in points:
        labels = selected_labels(
            spec, (xvalue, yvalue, R(-3, 8), R(-3, 8))
        )
        polynomial = fixed_support(spec, labels, fixed, ("x", "y"))
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    assert unit_ideal(polynomials, (x, y))


def assert_cell(cell):
    spec = CELL_SPECS[cell]
    assert_origin_cover(spec)
    assert_y_branch(spec, -1)
    assert_y_branch(spec, -2)
    assert_half_branch(spec, "u")
    assert_half_branch(spec, "v")
    assert_t_branch(spec)
    assert_r_open_branch(spec)
    assert_r_line_branch(spec)
    assert_r_special_branch(spec)
    print(cell, "PASS", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", choices=tuple(CELL_SPECS), action="append")
    args = parser.parse_args()
    cells = tuple(args.cell) if args.cell else tuple(CELL_SPECS)
    try:
        for cell in cells:
            assert_cell(cell)
    finally:
        response.PRIME = DEFAULT_PRIME

    print("minimal three-extra CBB orbit: PASS")
    print("CBB, BCB, BBC: exact localized branch covers")
    print("all selected rows direct-free; arbitrary B_01 scale allowed")


if __name__ == "__main__":
    main()
