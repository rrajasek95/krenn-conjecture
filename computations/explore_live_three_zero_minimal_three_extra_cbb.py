#!/usr/bin/env python3
"""Discover exact branch certificates on the representative CBB cell."""

from __future__ import annotations

import argparse
import subprocess

import numpy as np
import sympy as sp

import explore_live_three_zero_minimal_three_extra_response as response


CHARTS = ("01", "12", "12")
DEFAULT_PRIME = 1_000_003
PARAMETER_NAMES = "abcdef"
SYMBOLS = sp.symbols("a b c d e f")
LOCAL_MAP = {str(symbol): symbol for symbol in SYMBOLS}
R = sp.Rational

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

BRANCHES = {
    "b-1": ({"b": -1, "d": 0, "f": 0}, (0, 2, 4)),
    "b-2": ({"b": -2, "d": 0, "f": 0}, (0, 2, 4)),
    "c-half": ({"c": R(-1, 2), "d": 0, "f": 0}, (0, 1, 4)),
    "e-half": ({"e": R(-1, 2), "d": 0, "f": 0}, (0, 1, 2)),
}

CURVE_POINTS = (
    (0, 1), (-1, 1), (-2, 1), (-3, 1),
    (0, -1), (0, -2), (0, -3), (-1, -1), (-2, -2), (-3, -3),
    (1, 1), (R(-1, 2), R(-1, 2)), (1, R(-1, 2)),
    (-2, R(-1, 2)),
)


def labels_at(values, prime=DEFAULT_PRIME, raw_modular=False):
    response.PRIME = prime
    modular = tuple(
        int(value) % prime if raw_modular else modular_value(value, prime)
        for value in values
    )
    selected = response.select_labels(
        CHARTS, modular, excluded_sources=((0, 1),)
    )
    assert len(selected) == 19
    return tuple(label for _row_support, label in selected)


def rational_support(labels, substitutions, free_names):
    variables = tuple(SYMBOLS[PARAMETER_NAMES.index(name)] for name in free_names)
    determinant, _multiplier = response.flint_rational_restriction(
        CHARTS, labels, substitutions, free_names
    )
    return support(determinant, variables)


def modular_value(value, prime):
    value = R(value)
    return int(value.p) * pow(int(value.q), prime - 2, prime) % prime


def support(determinant, variables):
    product = sp.S.One
    for factor, _multiplicity in determinant.factor()[1]:
        product *= sp.sympify(
            str(factor).replace("^", "**"), locals=LOCAL_MAP
        )
    return sp.Poly(
        product, *variables, domain=sp.QQ
    ).sqf_part().monic().as_expr()


def add_point(polynomials, fixed, ordered_indices, point, prime, raw_modular):
    response.PRIME = prime
    values = [0] * 6
    for name, value in fixed.items():
        values[PARAMETER_NAMES.index(name)] = modular_value(value, prime)
    for index, value in zip(ordered_indices, point):
        values[index] = (
            int(value) % prime
            if raw_modular
            else modular_value(value, prime)
        )
    selected = response.select_labels(
        CHARTS, tuple(values), excluded_sources=((0, 1),)
    )
    assert len(selected) == 19
    labels = tuple(label for _row_support, label in selected)
    determinant = response.flint_restricted_determinant(
        CHARTS, labels, fixed
    )
    variables = tuple(SYMBOLS[index] for index in ordered_indices)
    polynomial = support(determinant, variables)
    if polynomial not in polynomials:
        polynomials.append(polynomial)


def finite_field_zeros(basis, variables, prime):
    polynomials = []
    for polynomial in basis.polys:
        integral = sp.Poly(
            polynomial.as_expr(), *variables, domain=sp.QQ
        ).clear_denoms()[1]
        polynomials.append(
            sp.Poly(integral.as_expr(), *variables, modulus=prime)
        )

    coordinate = np.arange(prime, dtype=np.int64)
    powers = []
    for variable_index in range(3):
        maximum = max(
            monomial[variable_index]
            for polynomial in polynomials
            for monomial, _coefficient in polynomial.terms()
        )
        table = [np.ones(prime, dtype=np.int64)]
        for _degree in range(maximum):
            table.append(table[-1] * coordinate % prime)
        powers.append(table)

    mask = np.ones((prime, prime, prime), dtype=bool)
    shapes = ((prime, 1, 1), (1, prime, 1), (1, 1, prime))
    for polynomial in polynomials:
        values = np.zeros(mask.shape, dtype=np.int64)
        for monomial, coefficient in polynomial.terms():
            term = int(coefficient) % prime
            for variable_index, degree in enumerate(monomial):
                if degree:
                    term = (
                        term
                        * powers[variable_index][degree].reshape(
                            shapes[variable_index]
                        )
                        % prime
                    )
            values = (values + term) % prime
        mask &= values == 0
    return np.argwhere(mask)


def singular_localized_unit(polynomials, variables, localizer):
    names = ",".join(map(str, variables)) + ",tau"
    generators = []
    for polynomial in polynomials:
        integral = sp.Poly(
            polynomial, *variables, domain=sp.QQ
        ).clear_denoms()[1].as_expr()
        generators.append(str(sp.expand(integral)).replace("**", "^"))
    generators.append(
        "1-tau*(" + str(sp.expand(localizer)).replace("**", "^") + ")"
    )
    script = (
        f"ring r=0,({names}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=std(I);\n"
        'if (size(G)==1 && G[1]==1) { "UNIT"; } '
        'else { "NONUNIT"; }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"),
        input=script,
        text=True,
        capture_output=True,
        check=True,
        timeout=300,
    )
    if "?" in result.stdout:
        raise RuntimeError("Singular rejected the localization input:\n" + result.stdout)
    return "UNIT" in result.stdout and "NONUNIT" not in result.stdout


def close_half_curve(which):
    a, b, c, d, e, f = SYMBOLS
    if which == "c-curve":
        free_names = ("b", "e")
        variables = (b, e)
        substitutions = {"a": -1/e, "c": R(-1, 2), "d": 0, "f": 0}

        def full_values(bvalue, other):
            return (-R(1)/other, bvalue, R(-1, 2), 0, other, 0)

        residual_fixed = {
            "a": -2, "c": R(-1, 2), "d": 0, "e": R(1, 2), "f": 0
        }
        residual_values = (-2, -1, R(-1, 2), 0, R(1, 2), 0)
    else:
        free_names = ("b", "c")
        variables = (b, c)
        substitutions = {"a": -1/c, "d": 0, "e": R(-1, 2), "f": 0}

        def full_values(bvalue, other):
            return (-R(1)/other, bvalue, other, 0, R(-1, 2), 0)

        residual_fixed = {
            "a": -2, "c": R(1, 2), "d": 0, "e": R(-1, 2), "f": 0
        }
        residual_values = (-2, -1, R(1, 2), 0, R(-1, 2), 0)

    polynomials = []
    for bvalue, other in CURVE_POINTS:
        labels = labels_at(full_values(bvalue, other))
        polynomial = rational_support(labels, substitutions, free_names)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    basis = sp.groebner(
        polynomials, *variables, order="grevlex", domain=sp.QQ
    )
    print(
        which,
        "supports",
        len(polynomials),
        "basis",
        [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
        flush=True,
    )

    labels = labels_at(residual_values)
    determinant = response.flint_restricted_determinant(
        CHARTS, labels, residual_fixed
    )
    print(which, "residual determinant", determinant.factor(), flush=True)


def close_t_branch():
    a, b, c, d, e, f = SYMBOLS
    denominator = 2*c + 2*e + 1
    substitutions = {"a": -2/denominator, "d": 0, "f": 0}
    variables = (b, c, e)
    polynomials = []
    for bvalue, cvalue, evalue in SAMPLE_POINTS:
        if denominator.subs({c: cvalue, e: evalue}) == 0:
            continue
        avalue = -R(2) / denominator.subs({c: cvalue, e: evalue})
        labels = labels_at((avalue, bvalue, cvalue, 0, evalue, 0))
        polynomial = rational_support(
            labels, substitutions, ("b", "c", "e")
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    basis = sp.groebner(
        polynomials, *variables, order="grevlex", domain=sp.QQ
    )
    print(
        "t-branch",
        "supports",
        len(polynomials),
        "basis",
        [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
        flush=True,
    )


def close_r_line_branch():
    a, b, c, d, e, f = SYMBOLS
    substitutions = {"a": 0, "d": 0, "e": -R(3, 4)-c, "f": 0}
    variables = (b, c)
    points = (
        (0, 0), (-1, 0), (-2, 0), (-3, 0),
        (0, -1), (0, -2), (0, -3), (-1, -1), (-2, -2), (-3, -3),
        (1, 1), (R(-1, 2), R(-1, 2)),
        (0, R(-3, 4)), (-1, R(-3, 4)), (-2, R(-3, 4)),
        (-3, R(-3, 4)),
    )
    polynomials = []
    for bvalue, cvalue in points:
        labels = labels_at((0, bvalue, cvalue, 0, -R(3, 4)-cvalue, 0))
        polynomial = rational_support(
            labels, substitutions, ("b", "c")
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    basis = sp.groebner(
        polynomials, *variables, order="grevlex", domain=sp.QQ
    )
    print(
        "r-line before target",
        len(polynomials),
        [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
        flush=True,
    )
    targets = []
    for bvalue in (0, -2):
        labels = labels_at(
            (0, bvalue, R(-1, 2), 0, R(-1, 4), 0)
        )
        targets.append(
            rational_support(labels, substitutions, ("b", "c"))
        )
    basis = sp.groebner(
        polynomials + targets, *variables, order="grevlex", domain=sp.QQ
    )
    print(
        "r-line targets",
        [sp.factor(target) for target in targets],
        "unit",
        basis.reduce(sp.S.One)[1] == 0,
        flush=True,
    )


def close_r_special_branch():
    a, b, c, d, e, f = SYMBOLS
    fixed = {"c": R(-3, 8), "d": 0, "e": R(-3, 8), "f": 0}
    variables = (a, b)
    points = (
        (0, 0), (-2, 0), (0, -3), (0, -1), (-2, -3),
        (-2, -1), (1, 1), (-1, -2), (R(-1, 2), 0),
    )
    polynomials = []
    for avalue, bvalue in points:
        labels = labels_at((avalue, bvalue, R(-3, 8), 0, R(-3, 8), 0))
        polynomial = support(
            response.flint_restricted_determinant(CHARTS, labels, fixed),
            variables,
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    basis = sp.groebner(
        polynomials, *variables, order="grevlex", domain=sp.QQ
    )
    print(
        "r-special before target",
        len(polynomials),
        [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
        flush=True,
    )
    targets = []
    for avalue, bvalue in ((4, -1), (0, -2)):
        labels = labels_at(
            (avalue, bvalue, R(-3, 8), 0, R(-3, 8), 0)
        )
        targets.append(
            support(
                response.flint_restricted_determinant(
                    CHARTS, labels, fixed
                ),
                variables,
            )
        )
    basis = sp.groebner(
        polynomials + targets, *variables, order="grevlex", domain=sp.QQ
    )
    print(
        "r-special targets",
        [sp.factor(target) for target in targets],
        "unit",
        basis.reduce(sp.S.One)[1] == 0,
        flush=True,
    )


def close_r_open_branch(scan_primes=True):
    a, b, c, d, e, f = SYMBOLS
    variables = (b, c, e)
    coefficient = (
        2*c**2 - 4*c*e - 4*c + 2*e**2 - 4*e - 3
    )
    numerator = 8*c + 8*e + 6
    a_restriction = numerator / coefficient
    line = 4*c + 4*e + 3
    coefficient_poly = sp.Poly(coefficient, *variables, domain=sp.QQ)
    line_poly = sp.Poly(line, *variables, domain=sp.QQ)

    def restricted_support(labels):
        determinant, _multiplier = response.flint_rational_restriction(
            CHARTS,
            labels,
            {"a": a_restriction, "d": 0, "f": 0},
            ("b", "c", "e"),
        )
        polynomial = sp.Poly(
            support(determinant, variables),
            *variables,
            domain=sp.QQ,
        )
        polynomial = polynomial.exquo(
            sp.gcd(polynomial, coefficient_poly)
        )
        return polynomial.monic()

    polynomials = []
    response.PRIME = DEFAULT_PRIME
    for bvalue, cvalue, evalue in SAMPLE_POINTS:
        denominator = coefficient.subs({c: cvalue, e: evalue})
        if denominator == 0:
            continue
        avalue = R(8*cvalue + 8*evalue + 6) / denominator
        values = (
            modular_value(avalue, DEFAULT_PRIME),
            modular_value(bvalue, DEFAULT_PRIME),
            modular_value(cvalue, DEFAULT_PRIME),
            0,
            modular_value(evalue, DEFAULT_PRIME),
            0,
        )
        selected = response.select_labels(
            CHARTS, values, excluded_sources=((0, 1),)
        )
        labels = tuple(label for _row_support, label in selected)
        polynomial = restricted_support(labels)
        assert polynomial.rem(line_poly) == 0
        quotient = polynomial.exquo(line_poly).monic().as_expr()
        if quotient not in polynomials:
            polynomials.append(quotient)

    # First residual point, found modulo 43.  Keeping it as a deterministic
    # seed makes later exploratory runs reproducible.
    response.PRIME = 43
    bvalue, cvalue, evalue = (5, 40, 41)
    denominator = int(coefficient.subs({c: cvalue, e: evalue})) % 43
    avalue = (
        int(numerator.subs({c: cvalue, e: evalue}))
        * pow(denominator, 41, 43)
        % 43
    )
    selected = response.select_labels(
        CHARTS,
        (avalue, bvalue, cvalue, 0, evalue, 0),
        excluded_sources=((0, 1),),
    )
    seeded = restricted_support(
        tuple(label for _row_support, label in selected)
    ).as_expr()
    if seeded not in polynomials:
        polynomials.append(seeded)

    if not scan_primes:
        basis = sp.groebner(
            polynomials, *variables, order="grevlex", domain=sp.QQ
        )
        print(
            "r-open residual basis",
            [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
            flush=True,
        )
        return

    localizer = coefficient * line
    # The residual may have no rational point modulo an inert prime.  Scan a
    # healthy collection of small splitting primes; modular points are used
    # only to choose row sets, while every added polynomial is recomputed over
    # QQ and the final unit-ideal check is exact.
    primes = (
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
        163, 167, 173, 179, 181, 191, 193, 197, 199,
    )
    for prime in primes:
        basis = sp.groebner(
            polynomials, *variables, order="grevlex", domain=sp.QQ
        )
        unit = singular_localized_unit(
            [polynomial.as_expr() for polynomial in basis.polys],
            variables,
            localizer,
        )
        print(
            "r-open",
            "prime",
            prime,
            "supports",
            len(polynomials),
            "localized_unit",
            unit,
            flush=True,
        )
        if unit:
            return
        assert basis.is_zero_dimensional
        try:
            zeros = finite_field_zeros(basis, variables, prime)
        except (ValueError, ZeroDivisionError):
            print("bad reduction", prime, flush=True)
            continue
        useful = []
        response.PRIME = prime
        for bvalue, cvalue, evalue in zeros:
            denominator = int(
                coefficient.subs({c: int(cvalue), e: int(evalue)})
            ) % prime
            line_value = int(
                line.subs({c: int(cvalue), e: int(evalue)})
            ) % prime
            if denominator == 0 or line_value == 0:
                continue
            avalue = (
                int(numerator.subs({c: int(cvalue), e: int(evalue)}))
                * pow(denominator, prime - 2, prime)
                % prime
            )
            values = (
                avalue,
                int(bvalue),
                int(cvalue),
                0,
                int(evalue),
                0,
            )
            selected = response.select_labels(
                CHARTS, values, excluded_sources=((0, 1),)
            )
            labels = tuple(label for _row_support, label in selected)
            polynomial = restricted_support(labels).as_expr()
            if polynomial not in polynomials:
                polynomials.append(polynomial)
            useful.append(tuple(map(int, (bvalue, cvalue, evalue))))
        print("useful zeros", useful, flush=True)
    print(
        "r-open residual basis",
        [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
        flush=True,
    )
    raise AssertionError("r-open")


def close_fixed_branch(branch):
    fixed, ordered_indices = BRANCHES[branch]
    variables = tuple(SYMBOLS[index] for index in ordered_indices)
    polynomials = []
    for point in SAMPLE_POINTS:
        add_point(
            polynomials,
            fixed,
            ordered_indices,
            point,
            DEFAULT_PRIME,
            raw_modular=False,
        )

    for prime in (101, 103, 107, 109, 127, 131, 137, 139, 149):
        basis = sp.groebner(
            polynomials, *variables, order="grevlex", domain=sp.QQ
        )
        is_unit = basis.reduce(sp.S.One)[1] == 0
        print(
            branch,
            "prime",
            prime,
            "supports",
            len(polynomials),
            "basis",
            len(basis.polys),
            "zero_dimensional",
            basis.is_zero_dimensional,
            "unit",
            is_unit,
            flush=True,
        )
        if is_unit:
            return
        if not basis.is_zero_dimensional:
            print(
                "positive-dimensional basis",
                [sp.factor(polynomial.as_expr()) for polynomial in basis.polys],
                flush=True,
            )
            return
        zeros = finite_field_zeros(basis, variables, prime)
        print("zeros", [tuple(map(int, point)) for point in zeros], flush=True)
        for point in zeros:
            add_point(
                polynomials,
                fixed,
                ordered_indices,
                point,
                prime,
                raw_modular=True,
            )
    raise AssertionError(branch)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "branch",
        choices=tuple(BRANCHES)
        + (
            "c-curve", "e-curve", "t-branch", "r-open", "r-basis",
            "r-line", "r-special",
        ),
    )
    args = parser.parse_args()
    try:
        if args.branch in ("c-curve", "e-curve"):
            close_half_curve(args.branch)
        elif args.branch == "t-branch":
            close_t_branch()
        elif args.branch in ("r-open", "r-basis"):
            close_r_open_branch(scan_primes=args.branch == "r-open")
        elif args.branch == "r-line":
            close_r_line_branch()
        elif args.branch == "r-special":
            close_r_special_branch()
        else:
            close_fixed_branch(args.branch)
    finally:
        response.PRIME = DEFAULT_PRIME


if __name__ == "__main__":
    main()
