#!/usr/bin/env python3
"""Exact direct-free rank certificates on CCB, CBC, and BCC.

Finite-field points in this file select response-row bases only.  Every
determinant and every localized unit-ideal test is reconstructed over QQ.
"""

from __future__ import annotations

import argparse

import sympy as sp

import explore_live_three_zero_minimal_three_extra_ccb as discovery
import explore_live_three_zero_minimal_three_extra_response as response


DEFAULT_PRIME = 1_000_003
ACTUAL_NAMES = ("a", "b", "c", "d", "e", "f")
ACTUAL = sp.symbols("a b c d e f")
ACTUAL_BY_NAME = dict(zip(ACTUAL_NAMES, ACTUAL))
x, y, z, u, v = sp.symbols("x y z u v")
STANDARD = (x, y, z, u, v)
STANDARD_NAMES = ("x", "y", "z", "u", "v")
STANDARD_BY_NAME = dict(zip(STANDARD_NAMES, STANDARD))
R = sp.Rational


CELL_SPECS = {
    "CCB": {
        "charts": ("01", "01", "12"),
        "names": {"x": "a", "y": "b", "z": "c", "u": "d", "v": "e"},
        "structural": {"f": 0},
    },
    "CBC": {
        "charts": ("01", "12", "01"),
        "names": {"x": "a", "y": "b", "z": "e", "u": "f", "v": "c"},
        "structural": {"d": 0},
    },
    "BCC": {
        "charts": ("12", "01", "01"),
        "names": {"x": "c", "y": "d", "z": "e", "u": "f", "v": "a"},
        "structural": {"b": 0},
    },
}


SIMPLE_MODULAR_POINTS = {
    "y=-1": (
        (17, (0, 0, 7, 0)), (17, (0, 0, 16, 9)),
        (17, (0, 15, 14, 0)), (17, (1, 2, 2, 0)),
        (17, (1, 5, 7, 0)), (17, (1, 13, 7, 3)),
        (17, (4, 10, 7, 0)), (17, (5, 0, 9, 1)),
        (17, (5, 0, 14, 1)), (17, (5, 0, 16, 1)),
        (17, (14, 0, 16, 0)), (17, (15, 0, 14, 0)),
        (17, (15, 0, 16, 0)), (19, (1, 12, 0, 0)),
        (19, (1, 12, 4, 0)), (19, (6, 10, 18, 10)),
    ),
    "u=-1": (
        (17, (0, 7, 0, 0)), (17, (0, 10, 4, 12)),
        (17, (0, 14, 1, 7)), (17, (0, 14, 8, 10)),
        (17, (0, 14, 15, 0)), (17, (0, 16, 0, 9)),
        (17, (0, 16, 14, 0)), (17, (1, 7, 13, 3)),
        (17, (1, 14, 2, 0)), (17, (4, 7, 10, 0)),
        (17, (4, 16, 10, 0)), (17, (15, 14, 0, 0)),
        (17, (0, 16, 15, 0)),
        (19, (1, 0, 12, 0)), (19, (1, 2, 12, 0)),
        (19, (6, 16, 10, 7)), (19, (6, 18, 10, 10)),
    ),
    "T": (
        (17, (11, 16, 16, 0)), (17, (14, 0, 14, 0)),
        (17, (14, 0, 14, 14)), (17, (14, 0, 16, 0)),
        (17, (14, 0, 16, 14)), (19, (0, 1, 18, 1)),
    ),
    "Q": (
        (17, (0, 1, 0, 0)), (17, (0, 1, 0, 1)),
        (17, (0, 1, 15, 0)), (17, (0, 7, 0, 0)),
        (17, (0, 15, 15, 0)), (17, (1, 7, 0, 7)),
        (17, (1, 7, 13, 3)), (17, (1, 15, 2, 0)),
        (17, (3, 2, 11, 5)), (17, (4, 1, 10, 0)),
        (17, (5, 7, 0, 0)), (17, (11, 0, 14, 0)),
        (17, (14, 7, 0, 0)), (17, (15, 7, 0, 0)),
        (17, (0, 16, 5, 0)), (17, (0, 16, 10, 13)),
        (17, (0, 16, 14, 0)), (17, (0, 16, 15, 0)),
        (19, (1, 0, 12, 0)), (19, (1, 7, 12, 0)),
        (19, (7, 12, 3, 0)), (19, (6, 1, 10, 10)),
    ),
}


NONCOORDINATE_POINTS = (
    (17, (16, 5, 1, 12, 8)),
    (17, (7, 3, 16, 14, 4)),
    (17, (16, 9, 16, 9, 10)),
    (17, (2, 6, 1, 11, 8)),
    (17, (8, 0, 5, 12, 3)),
    (17, (1, 7, 2, 7, 8)),
    (17, (16, 11, 8, 11, 11)),
    (17, (1, 4, 2, 10, 15)),
    (17, (1, 13, 2, 2, 15)),
)


E0_POINTS = (
    (19, (1, 0, 12, 4)),
    (19, (1, 4, 12, 4)),
)


def modular_value(value, prime):
    value = R(value)
    return int(value.p) * pow(int(value.q), prime - 2, prime) % prime


def actual_name(spec, standard_name):
    return spec["names"][standard_name]


def actual_values(spec, standard_values):
    values = {name: R(value) for name, value in spec["structural"].items()}
    values.update(
        {
            actual_name(spec, name): R(value)
            for name, value in zip(STANDARD_NAMES, standard_values)
        }
    )
    return tuple(values[name] for name in ACTUAL_NAMES)


def selected_labels(spec, standard_values, prime=DEFAULT_PRIME, raw=False):
    response.PRIME = prime
    values = actual_values(spec, standard_values)
    modular = tuple(
        int(value) % prime if raw else modular_value(value, prime)
        for value in values
    )
    selected = response.select_labels(
        spec["charts"], modular, excluded_sources=((0, 1),)
    )
    assert len(selected) == 19
    labels = tuple(label for _support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    return labels


def normalized(polynomial, variables):
    return sp.Poly(
        polynomial, *variables, domain=sp.QQ
    ).sqf_part().monic().as_expr()


def fixed_support(spec, labels, fixed, free_names):
    substitutions = dict(spec["structural"])
    substitutions.update(
        {actual_name(spec, name): value for name, value in fixed.items()}
    )
    actual_variables = tuple(
        ACTUAL_BY_NAME[actual_name(spec, name)] for name in free_names
    )
    determinant = response.flint_restricted_determinant(
        spec["charts"], labels, substitutions
    )
    if not determinant:
        return None
    polynomial = discovery.primitive_support(determinant, actual_variables)
    rename = {
        ACTUAL_BY_NAME[actual_name(spec, name)]: STANDARD_BY_NAME[name]
        for name in free_names
    }
    variables = tuple(STANDARD_BY_NAME[name] for name in free_names)
    return normalized(polynomial.xreplace(rename), variables)


def rational_support(spec, labels, substitutions, free_names):
    standard_to_actual = {
        STANDARD_BY_NAME[name]: ACTUAL_BY_NAME[actual_name(spec, name)]
        for name in STANDARD_NAMES
    }
    actual_substitutions = dict(spec["structural"])
    actual_substitutions.update(
        {
            actual_name(spec, name): sp.sympify(value).xreplace(standard_to_actual)
            for name, value in substitutions.items()
        }
    )
    actual_free_names = tuple(actual_name(spec, name) for name in free_names)
    actual_variables = tuple(ACTUAL_BY_NAME[name] for name in actual_free_names)
    determinant, _denominator = response.flint_rational_restriction(
        spec["charts"], labels, actual_substitutions, actual_free_names
    )
    if not determinant:
        return None
    polynomial = discovery.primitive_support(determinant, actual_variables)
    rename = {
        ACTUAL_BY_NAME[actual_name(spec, name)]: STANDARD_BY_NAME[name]
        for name in free_names
    }
    variables = tuple(STANDARD_BY_NAME[name] for name in free_names)
    return normalized(polynomial.xreplace(rename), variables)


def append_distinct(polynomials, polynomial):
    if polynomial is not None and polynomial not in polynomials:
        polynomials.append(polynomial)


def assert_unit(name, polynomials, variables, localizer=None):
    status = discovery.singular_status(polynomials, variables, localizer)
    assert "UNIT" in status and "NONUNIT" not in status, (name, status)
    print(name, "PASS", flush=True)


def origin_polynomial(spec):
    labels = selected_labels(spec, (0, 0, 0, 0, 0))
    origin = fixed_support(spec, labels, {}, STANDARD_NAMES)
    factors = sp.factor_list(origin)[1]
    p_polynomial = max(
        (factor for factor, _multiplicity in factors), key=sp.total_degree
    )
    t_polynomial = x*(2*v+1)+2
    q_polynomial = y*u+3*y+3*u+6
    expected = (y+1)*(u+1)*t_polynomial*q_polynomial*p_polynomial
    assert normalized(origin, STANDARD) == normalized(expected, STANDARD)
    assert sp.degree(p_polynomial, z) == 1
    return normalized(p_polynomial, STANDARD)


def fixed_branch(
    spec, name, fixed, free_names, point_to_full, discover=False
):
    variables = tuple(STANDARD_BY_NAME[item] for item in free_names)
    polynomials = []
    for point in discovery.FOUR_POINTS:
        labels = selected_labels(spec, point_to_full(point))
        append_distinct(
            polynomials, fixed_support(spec, labels, fixed, free_names)
        )
    for prime, point in SIMPLE_MODULAR_POINTS[name]:
        labels = selected_labels(
            spec, point_to_full(point), prime=prime, raw=True
        )
        append_distinct(
            polynomials, fixed_support(spec, labels, fixed, free_names)
        )
    if discover:
        def add_at(point, prime):
            labels = selected_labels(
                spec, point_to_full(point), prime=prime, raw=True
            )
            return fixed_support(spec, labels, fixed, free_names)

        discovery.modular_finish(polynomials, variables, add_at)
    else:
        assert_unit(name, polynomials, variables)


def rational_branch(
    spec, name, substitution, free_names, denominator, point_to_full,
    discover=False,
):
    variables = tuple(STANDARD_BY_NAME[item] for item in free_names)
    polynomials = []
    for point in discovery.FOUR_POINTS:
        full = point_to_full(point, None)
        if full is None:
            continue
        labels = selected_labels(spec, full)
        append_distinct(
            polynomials,
            rational_support(spec, labels, substitution, free_names),
        )
    for prime, point in SIMPLE_MODULAR_POINTS[name]:
        full = point_to_full(point, prime)
        labels = selected_labels(spec, full, prime=prime, raw=True)
        append_distinct(
            polynomials,
            rational_support(spec, labels, substitution, free_names),
        )
    if discover:
        def add_at(point, prime):
            full = point_to_full(point, prime)
            labels = selected_labels(spec, full, prime=prime, raw=True)
            return rational_support(
                spec, labels, substitution, free_names
            )

        discovery.modular_finish(
            polynomials, variables, add_at, localizer=denominator
        )
    else:
        assert_unit(name, polynomials, variables, denominator)


def assert_simple_branches(spec, only=None, discover=False):
    if only in (None, "y=-1"):
        fixed_branch(
        spec, "y=-1", {"y": -1}, ("x", "z", "u", "v"),
        lambda point: (point[0], -1, point[1], point[2], point[3]),
        discover=discover,
        )
    if only in (None, "u=-1"):
        fixed_branch(
        spec, "u=-1", {"u": -1}, ("x", "y", "z", "v"),
        lambda point: (point[0], point[1], point[2], -1, point[3]),
        discover=discover,
        )

    denominator = 2*v+1

    def t_full(point, prime):
        yvalue, zvalue, uvalue, vvalue = point
        if prime is None:
            if denominator.subs(v, vvalue) == 0:
                return None
            xvalue = -R(2)/denominator.subs(v, vvalue)
        else:
            xvalue = -2*pow((2*vvalue+1) % prime, prime-2, prime) % prime
        return (xvalue, yvalue, zvalue, uvalue, vvalue)

    if only in (None, "T"):
        rational_branch(
            spec, "T", {"x": -2/denominator},
            ("y", "z", "u", "v"), denominator, t_full,
            discover=discover,
        )

    denominator = y+3

    def q_full(point, prime):
        xvalue, yvalue, zvalue, vvalue = point
        if prime is None:
            if denominator.subs(y, yvalue) == 0:
                return None
            uvalue = -R(3)*(yvalue+2)/denominator.subs(y, yvalue)
        else:
            uvalue = (
                -3*(yvalue+2)*pow((yvalue+3) % prime, prime-2, prime)
                % prime
            )
        return (xvalue, yvalue, zvalue, uvalue, vvalue)

    if only in (None, "Q"):
        rational_branch(
            spec, "Q", {"u": -3*(y+2)/denominator},
            ("x", "y", "z", "v"), denominator, q_full,
            discover=discover,
        )


def p_selector_bases(spec):
    labels = [
        selected_labels(spec, point) for point in discovery.FIVE_POINTS[:8]
    ]
    labels.extend(
        selected_labels(spec, point, prime=17, raw=True)
        for point in discovery.P_MODULAR_POINTS
    )
    return tuple(labels)


def component_data(name, p_polynomial, base_localizer):
    if name == "y2-z0":
        return {"y": -2, "z": 0}, ("x", "u", "v"), (), base_localizer.subs({y: -2, z: 0}), ()
    if name == "y2-v1":
        return {"y": -2, "v": -1}, ("x", "z", "u"), (), base_localizer.subs({y: -2, v: -1}), ()
    if name == "y2-F":
        quotient = sp.cancel(-p_polynomial.subs(y, -2)/(z*(u+1)*(v+1)))
        assert sp.denom(quotient) == 1
        return {"y": -2}, ("x", "z", "u", "v"), (sp.expand(quotient),), base_localizer.subs(y, -2)*z*(v+1), ((19, (1, -2, 12, 10, 0)),)
    if name == "u2-x0":
        return {"u": -2, "x": 0}, ("y", "z", "v"), (), base_localizer.subs({u: -2, x: 0}), ()
    if name == "u2-v1":
        return {"u": -2, "v": -1}, ("x", "y", "z"), (), base_localizer.subs({u: -2, v: -1}), ()
    if name == "u2-G":
        quotient = sp.cancel(-p_polynomial.subs(u, -2)/(x*(y+1)*(v+1)))
        assert sp.denom(quotient) == 1
        return {"u": -2}, ("x", "y", "z", "v"), (sp.expand(quotient),), base_localizer.subs(u, -2)*x*(v+1), ((19, (12, 10, 1, -2, 0)),)
    raise ValueError(name)


def assert_p_fixed_components(spec, p_polynomial, base_localizer):
    selector_bases = p_selector_bases(spec)
    for name in ("y2-z0", "y2-v1", "y2-F", "u2-x0", "u2-v1", "u2-G"):
        fixed, free_names, equations, localizer, extras = component_data(
            name, p_polynomial, base_localizer
        )
        variables = tuple(STANDARD_BY_NAME[item] for item in free_names)
        polynomials = list(equations)
        for labels in selector_bases:
            append_distinct(
                polynomials, fixed_support(spec, labels, fixed, free_names)
            )
        for prime, point in extras:
            labels = selected_labels(spec, point, prime=prime, raw=True)
            append_distinct(
                polynomials, fixed_support(spec, labels, fixed, free_names)
            )
        assert_unit(name, polynomials, variables, sp.expand(localizer))


def coordinate_data(name, p_polynomial, complement_localizer):
    if name == "x0":
        equation = sp.cancel(p_polynomial.subs(x, 0)/((u+1)*(u+2)))
        return {"x": 0}, ("y", "z", "u", "v"), equation, complement_localizer.subs(x, 0), ()
    if name == "z0":
        equation = sp.cancel(p_polynomial.subs(z, 0)/((y+1)*(y+2)))
        return {"z": 0}, ("x", "y", "u", "v"), equation, complement_localizer.subs(z, 0)*x, ()
    if name == "v0":
        return {"v": 0}, ("x", "y", "z", "u"), p_polynomial.subs(v, 0), complement_localizer.subs(v, 0)*x*z, E0_POINTS
    raise ValueError(name)


def assert_p_complement(spec, p_polynomial, base_localizer):
    complement_localizer = base_localizer*(y+2)*(u+2)
    for name in ("x0", "z0", "v0"):
        fixed, free_names, equation, localizer, extras = coordinate_data(
            name, p_polynomial, complement_localizer
        )
        assert sp.denom(equation) == 1
        variables = tuple(STANDARD_BY_NAME[item] for item in free_names)
        polynomials = [sp.expand(equation)]

        def full(point):
            values = dict(zip(free_names, point))
            values.update(fixed)
            return tuple(values[item] for item in STANDARD_NAMES)

        for point in discovery.FOUR_POINTS:
            labels = selected_labels(spec, full(point))
            append_distinct(
                polynomials, fixed_support(spec, labels, fixed, free_names)
            )
        for prime, point in extras:
            labels = selected_labels(spec, full(point), prime=prime, raw=True)
            append_distinct(
                polynomials, fixed_support(spec, labels, fixed, free_names)
            )
        assert_unit(name, polynomials, variables, sp.expand(localizer))

    polynomials = [p_polynomial]
    for point in discovery.FIVE_POINTS[:8]:
        labels = selected_labels(spec, point)
        append_distinct(
            polynomials, fixed_support(spec, labels, {}, STANDARD_NAMES)
        )
    for prime, point in NONCOORDINATE_POINTS:
        labels = selected_labels(spec, point, prime=prime, raw=True)
        append_distinct(
            polynomials, fixed_support(spec, labels, {}, STANDARD_NAMES)
        )
    assert_unit(
        "noncoordinate", polynomials, STANDARD,
        sp.expand(complement_localizer*x*z*v),
    )


def assert_cell(cell, section=None):
    spec = CELL_SPECS[cell]
    p_polynomial = origin_polynomial(spec)
    t_polynomial = x*(2*v+1)+2
    q_polynomial = y*u+3*y+3*u+6
    base_localizer = (y+1)*(u+1)*t_polynomial*q_polynomial
    print(cell, "origin PASS", flush=True)
    if section in (None, "simple"):
        assert_simple_branches(spec)
    if section in (None, "p-fixed"):
        assert_p_fixed_components(spec, p_polynomial, base_localizer)
    if section in (None, "p-complement"):
        assert_p_complement(spec, p_polynomial, base_localizer)
    if section is None:
        print(cell, "PASS", flush=True)
    else:
        print(cell, section, "section PASS", flush=True)
    return p_polynomial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", choices=tuple(CELL_SPECS))
    parser.add_argument(
        "--simple-branch", choices=("y=-1", "u=-1", "T", "Q")
    )
    parser.add_argument("--discover", action="store_true")
    parser.add_argument(
        "--section", choices=("simple", "p-fixed", "p-complement")
    )
    args = parser.parse_args()
    if args.simple_branch:
        assert args.cell
        spec = CELL_SPECS[args.cell]
        try:
            origin_polynomial(spec)
            assert_simple_branches(
                spec, only=args.simple_branch, discover=args.discover
            )
        finally:
            response.PRIME = DEFAULT_PRIME
        return
    cells = (args.cell,) if args.cell else tuple(CELL_SPECS)
    reference = None
    try:
        for cell in cells:
            p_polynomial = assert_cell(cell, section=args.section)
            if reference is None:
                reference = p_polynomial
            else:
                assert sp.expand(p_polynomial-reference) == 0
    finally:
        response.PRIME = DEFAULT_PRIME
    if args.cell is None and args.section is None:
        print("minimal three-extra CCB orbit: PASS")
        print("CCB, CBC, BCC: exact localized branch covers over QQ")
        print("all selected rows direct-free; arbitrary B_01 scale allowed")


if __name__ == "__main__":
    main()
