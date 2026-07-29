#!/usr/bin/env python3
"""Discover exact branch certificates on the representative CCB cell."""

from __future__ import annotations

import argparse
import subprocess

import numpy as np
import sympy as sp
from flint import nmod_mpoly_ctx

import explore_live_three_zero_minimal_three_extra_response as response
import verify_live_three_zero_minimal_three_extra_boundary_low_cells as low
from explore_live_three_zero_minimal_three_extra_remaining_cells import (
    FIVE_POINTS,
    FOUR_POINTS,
    finite_field_zeros,
    values_at_points,
)


CHARTS = ("01", "01", "12")
DEFAULT_PRIME = 1_000_003
PARAMETER_NAMES = ("a", "b", "c", "d", "e", "f")
SYMBOLS = sp.symbols("a b c d e f")
SYMBOL_BY_NAME = dict(zip(PARAMETER_NAMES, SYMBOLS))
R = sp.Rational


# Exact-support selectors discovered by ``close_p_branch`` over F_17.  Their
# determinants are reconstructed over QQ for the final certificate; the same
# list can also be reconstructed directly over F_17 to audit the whole
# algebraic-closure fibre (rather than only its F_17-rational points).
P_MODULAR_POINTS = (
    (1, 15, 2, 2, 16),
    (8, 2, 0, 15, 7),
    (10, 5, 7, 12, 8),
    (16, 14, 7, 3, 4),
    (16, 15, 0, 14, 6),
    (0, 2, 16, 15, 2),
    (11, 15, 6, 1, 0),
    (16, 0, 0, 5, 11),
    (0, 4, 16, 15, 15),
    (0, 8, 16, 11, 0),
    (15, 4, 16, 11, 1),
    (0, 14, 16, 14, 14),
    (0, 2, 0, 15, 5),
    (1, 10, 13, 7, 0),
    (16, 4, 0, 13, 0),
    (7, 14, 16, 2, 4),
    (0, 15, 14, 2, 0),
    (16, 2, 2, 8, 0),
    (0, 15, 0, 5, 5),
    (15, 7, 0, 7, 8),
    (15, 7, 0, 11, 15),
    (0, 5, 15, 11, 0),
    (16, 0, 16, 0, 16),
    (0, 1, 0, 15, 5),
    (15, 0, 0, 0, 15),
    (0, 14, 5, 15, 0),
    (16, 0, 15, 0, 0),
    (10, 0, 16, 0, 14),
    (16, 15, 0, 14, 0),
    (0, 15, 0, 2, 0),
    (0, 2, 0, 15, 0),
    (4, 8, 10, 9, 0),
    (16, 13, 2, 0, 0),
    (0, 15, 0, 15, 1),
    (0, 15, 0, 15, 11),
    (0, 14, 15, 15, 0),
    (0, 14, 14, 15, 0),
    (14, 9, 0, 14, 0),
    (0, 4, 0, 15, 0),
    (0, 15, 0, 4, 0),
    (0, 15, 0, 15, 0),
)


def modular_value(value, prime):
    value = R(value)
    return int(value.p) * pow(int(value.q), prime - 2, prime) % prime


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
    labels = tuple(label for _row_support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    return labels


def support(value, variables):
    return low.squarefree_support(value, variables)


def primitive_support(value, variables):
    """Squarefree support with an integral normalization for modular use."""
    local_map = {str(symbol): symbol for symbol in SYMBOLS}
    product = sp.S.One
    for factor, _multiplicity in value.factor_squarefree()[1]:
        product *= sp.sympify(
            str(factor).replace("^", "**"), locals=local_map
        )
    integral = sp.Poly(
        product, *variables, domain=sp.QQ
    ).clear_denoms()[1].primitive()[1]
    return integral.as_expr()


def fixed_support(labels, substitutions, variables):
    determinant = response.flint_restricted_determinant(
        CHARTS, labels, substitutions
    )
    return support(determinant, variables)


def fixed_primitive_support(labels, substitutions, variables):
    determinant = response.flint_restricted_determinant(
        CHARTS, labels, substitutions
    )
    return primitive_support(determinant, variables)


def rational_support(labels, substitutions, free_names):
    variables = tuple(SYMBOL_BY_NAME[name] for name in free_names)
    determinant, _multiplier = response.flint_rational_restriction(
        CHARTS, labels, substitutions, free_names
    )
    return support(determinant, variables)


def singular_status(polynomials, variables, localizer=None):
    generators = []
    for polynomial in polynomials:
        integral = sp.Poly(
            polynomial, *variables, domain=sp.QQ
        ).clear_denoms()[1].as_expr()
        generators.append(str(sp.expand(integral)).replace("**", "^"))
    names = list(map(str, variables))
    if localizer is not None:
        names.append("tau")
        generators.append(
            "1-tau*("
            + str(sp.expand(localizer)).replace("**", "^")
            + ")"
        )
    script = (
        'LIB "modstd.lib";\n'
        + f"ring r=0,({','.join(names)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        + "ideal G=modStd(I,1);\n"
        + 'if (size(G)==1 && deg(G[1])==0) { "UNIT"; } '
        + 'else { "NONUNIT"; dim(G); size(G); }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=900,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def modular_restricted_support(labels, substitutions, variables, prime):
    """Reconstruct one determinant directly in F_p[variables]."""
    parameters, matrix = response.symbolic_response_matrix(CHARTS, labels)
    parameter_by_name = {str(parameter): parameter for parameter in parameters}
    restricted = matrix.subs(
        {
            parameter_by_name[name]: value
            for name, value in substitutions.items()
        }
    )
    context = nmod_mpoly_ctx.get(tuple(map(str, variables)), prime)

    def convert(expression):
        polynomial = sp.Poly(
            sp.expand(expression), *variables, domain=sp.QQ
        )
        terms = {}
        for monomial, coefficient in polynomial.terms():
            numerator, denominator = map(int, coefficient.as_numer_denom())
            terms[monomial] = (
                numerator * pow(denominator % prime, prime - 2, prime)
            ) % prime
        return context.from_dict(terms)

    entries = [
        [convert(restricted[row, column]) for column in range(restricted.cols)]
        for row in range(restricted.rows)
    ]
    sign = 1
    previous = context.constant(1)
    size = len(entries)
    for pivot_index in range(size - 1):
        if not entries[pivot_index][pivot_index]:
            swap_index = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if entries[row][pivot_index]
                ),
                None,
            )
            if swap_index is None:
                swap_column = next(
                    (
                        column
                        for column in range(pivot_index + 1, size)
                        if any(
                            entries[row][column]
                            for row in range(pivot_index, size)
                        )
                    ),
                    None,
                )
                if swap_column is None:
                    return context.constant(0)
                for row in range(size):
                    entries[row][pivot_index], entries[row][swap_column] = (
                        entries[row][swap_column], entries[row][pivot_index]
                    )
                sign = -sign
                swap_index = next(
                    row
                    for row in range(pivot_index, size)
                    if entries[row][pivot_index]
                )
            entries[pivot_index], entries[swap_index] = (
                entries[swap_index], entries[pivot_index]
            )
            if swap_index != pivot_index:
                sign = -sign
        pivot = entries[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    pivot * entries[row][column]
                    - entries[row][pivot_index] * entries[pivot_index][column]
                )
                entries[row][column] = (
                    numerator if pivot_index == 0 else numerator // previous
                )
            entries[row][pivot_index] = context.constant(0)
        previous = pivot
    determinant = sign * entries[-1][-1]
    assert determinant
    product = context.constant(1)
    _unit, factors = determinant.factor_squarefree()
    for factor, _multiplicity in factors:
        product *= factor
    return product


def singular_modular_status(polynomials, variables, prime, localizer=None):
    names = list(map(str, variables))
    generators = [str(polynomial).replace("**", "^") for polynomial in polynomials]
    if localizer is not None:
        names.append("tau")
        generators.append(
            "1-tau*(" + str(sp.expand(localizer)).replace("**", "^") + ")"
        )
    script = (
        f"ring r={prime},({','.join(names)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=std(I);\n"
        + 'if (size(G)==1 && deg(G[1])==0) { "UNIT"; } '
        + 'else { "NONUNIT"; dim(G); size(G); }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=900,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def modular_finish(polynomials, variables, add_at, localizer=None):
    added = []
    for prime in (17, 19, 23, 29, 31):
        zeros = finite_field_zeros(polynomials, variables, prime)
        if localizer is not None and len(zeros):
            zeros = zeros[
                values_at_points(localizer, variables, zeros, prime) != 0
            ]
        print("prime", prime, "open zeros", len(zeros), flush=True)
        bad_reduction = False
        while len(zeros):
            point = tuple(map(int, zeros[0]))
            polynomial = add_at(point, prime)
            if polynomial not in polynomials:
                polynomials.append(polynomial)
            values = values_at_points(polynomial, variables, zeros, prime)
            target_value = values_at_points(
                polynomial,
                variables,
                np.asarray((point,), dtype=np.int64),
                prime,
            )[0]
            if target_value == 0:
                print("bad reduction", prime, point, flush=True)
                bad_reduction = True
                break
            zeros = zeros[values == 0]
            added.append((prime, point))
            print("add", prime, point, "remaining", len(zeros), flush=True)
        if bad_reduction:
            continue
        status = singular_status(polynomials, variables, localizer)
        print("exact", status, flush=True)
        if "UNIT" in status and "NONUNIT" not in status:
            print("MODULAR_POINTS", tuple(added), flush=True)
            return
    print("MODULAR_POINTS", tuple(added), flush=True)
    raise AssertionError("branch remains")


def close_fixed(branch, modular=False):
    a, b, c, d, e, f = SYMBOLS
    if branch == "b-1":
        substitutions = {"b": -1, "f": 0}
        variables = (a, c, d, e)

        def values(point):
            avalue, cvalue, dvalue, evalue = point
            return (avalue, -1, cvalue, dvalue, evalue, 0)
    else:
        substitutions = {"d": -1, "f": 0}
        variables = (a, b, c, e)

        def values(point):
            avalue, bvalue, cvalue, evalue = point
            return (avalue, bvalue, cvalue, -1, evalue, 0)

    polynomials = []
    for index, point in enumerate(FOUR_POINTS):
        print(branch, index + 1, flush=True)
        polynomial = fixed_support(
            labels_at(values(point)), substitutions, variables
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    if not modular:
        print(branch, "supports", len(polynomials), singular_status(polynomials, variables))
        return

    def add_at(point, prime):
        return fixed_support(
            labels_at(values(point), prime=prime, raw_modular=True),
            substitutions,
            variables,
        )

    print(branch, "supports", len(polynomials), flush=True)
    modular_finish(polynomials, variables, add_at)


def close_rational(branch, modular=False):
    a, b, c, d, e, f = SYMBOLS
    if branch == "t":
        denominator = 2*e + 1
        substitutions = {"a": -2/denominator, "f": 0}
        free_names = ("b", "c", "d", "e")
        variables = (b, c, d, e)

        def values(point):
            bvalue, cvalue, dvalue, evalue = point
            denominator_value = denominator.subs(e, evalue)
            if denominator_value == 0:
                return None
            return (-R(2)/denominator_value, bvalue, cvalue, dvalue, evalue, 0)
    else:
        denominator = b + 3
        substitutions = {"d": -3*(b+2)/denominator, "f": 0}
        free_names = ("a", "b", "c", "e")
        variables = (a, b, c, e)

        def values(point):
            avalue, bvalue, cvalue, evalue = point
            denominator_value = denominator.subs(b, bvalue)
            if denominator_value == 0:
                return None
            dvalue = -R(3)*(bvalue+2)/denominator_value
            return (avalue, bvalue, cvalue, dvalue, evalue, 0)

    polynomials = []
    for index, point in enumerate(FOUR_POINTS):
        actual_values = values(point)
        if actual_values is None:
            continue
        print(branch, index + 1, flush=True)
        polynomial = rational_support(
            labels_at(actual_values), substitutions, free_names
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    if modular:
        def add_at(point, prime):
            if branch == "t":
                bvalue, cvalue, dvalue, evalue = point
                denominator_value = (2*evalue + 1) % prime
                avalue = -2*pow(denominator_value, prime-2, prime) % prime
                actual_values = (
                    avalue, bvalue, cvalue, dvalue, evalue, 0
                )
            else:
                avalue, bvalue, cvalue, evalue = point
                denominator_value = (bvalue + 3) % prime
                dvalue = (
                    -3*(bvalue+2)*pow(denominator_value, prime-2, prime)
                    % prime
                )
                actual_values = (
                    avalue, bvalue, cvalue, dvalue, evalue, 0
                )
            return rational_support(
                labels_at(actual_values, prime=prime, raw_modular=True),
                substitutions,
                free_names,
            )

        print(branch, "supports", len(polynomials), flush=True)
        modular_finish(polynomials, variables, add_at, denominator)
        return
    print(
        branch,
        "supports",
        len(polynomials),
        singular_status(polynomials, variables, denominator),
    )


def p_branch_zeros(p_polynomial, polynomials, localizer, prime):
    a, b, c, d, e, f = SYMBOLS
    free_variables = (a, b, d, e)
    grid = np.indices((prime,) * 4, dtype=np.int64).reshape(4, -1).T
    coefficient = sp.diff(p_polynomial, c)
    constant = p_polynomial.subs(c, 0)
    coefficient_values = values_at_points(
        coefficient, free_variables, grid, prime
    )
    constant_values = values_at_points(constant, free_variables, grid, prime)

    regular_free = grid[coefficient_values != 0]
    regular_coefficient = coefficient_values[coefficient_values != 0]
    regular_constant = constant_values[coefficient_values != 0]
    regular_c = np.asarray(
        [
            -int(value)*pow(int(coefficient_value), prime-2, prime) % prime
            for value, coefficient_value in zip(
                regular_constant, regular_coefficient
            )
        ],
        dtype=np.int64,
    )
    regular = np.column_stack(
        (
            regular_free[:, 0], regular_free[:, 1], regular_c,
            regular_free[:, 2], regular_free[:, 3],
        )
    )

    special_free = grid[(coefficient_values == 0) & (constant_values == 0)]
    if len(special_free):
        repeated = np.repeat(special_free, prime, axis=0)
        special_c = np.tile(np.arange(prime, dtype=np.int64), len(special_free))
        special = np.column_stack(
            (
                repeated[:, 0], repeated[:, 1], special_c,
                repeated[:, 2], repeated[:, 3],
            )
        )
        points = np.vstack((regular, special))
    else:
        points = regular

    mask = values_at_points(localizer, (a, b, c, d, e), points, prime) != 0
    for polynomial in polynomials:
        mask &= values_at_points(
            polynomial, (a, b, c, d, e), points, prime
        ) == 0
        if not mask.any():
            break
    return points[mask]


def p_branch_cut(zeros, prime):
    sample_indices = np.linspace(
        0, len(zeros)-1, min(96, len(zeros)), dtype=int
    )
    candidates = []
    response.PRIME = prime
    for index in sample_indices:
        point = tuple(map(int, zeros[index]))
        selected = response.select_labels(
            CHARTS, (*point, 0), excluded_sources=((0, 1),)
        )
        if len(selected) == 19:
            candidates.append(
                (sum(size for size, _label in selected), point, selected)
            )
    assert candidates

    # Estimate exact matrix complexity on the numerically sparsest options.
    ranked = []
    for numeric_complexity, point, selected in sorted(candidates)[:8]:
        labels = tuple(label for _size, label in selected)
        _parameters, matrix = response.symbolic_response_matrix(CHARTS, labels)
        restricted = matrix.subs(SYMBOL_BY_NAME["f"], 0)
        symbolic_complexity = sum(
            len(sp.Poly(entry, *SYMBOLS[:5]).terms())
            for entry in restricted
            if entry != 0
        )
        ranked.append(
            (symbolic_complexity, numeric_complexity, point, labels)
        )
    symbolic_complexity, numeric_complexity, point, labels = min(ranked)
    print(
        "p cut", prime, point,
        "complexity", (numeric_complexity, symbolic_complexity),
        flush=True,
    )
    return point, labels


def close_p_branch():
    a, b, c, d, e, f = SYMBOLS
    variables = (a, b, c, d, e)
    origin = fixed_primitive_support(
        labels_at((0, 0, 0, 0, 0, 0)), {"f": 0}, variables
    )
    factors = sp.factor_list(origin)[1]
    p_polynomial = max(
        (factor for factor, _multiplicity in factors), key=sp.total_degree
    )
    t_polynomial = a*(2*e+1)+2
    q_polynomial = b*d+3*b+3*d+6
    localizer = (b+1)*(d+1)*t_polynomial*q_polynomial
    assert sp.degree(p_polynomial, c) == 1

    polynomials = []
    for index, point in enumerate(FIVE_POINTS[:8]):
        print("p base", index + 1, point, flush=True)
        labels = labels_at((*point, 0))
        polynomial = fixed_primitive_support(labels, {"f": 0}, variables)
        if polynomial not in polynomials:
            polynomials.append(polynomial)

    added = []
    for prime in (17, 19, 23, 29):
        zeros = p_branch_zeros(
            p_polynomial, polynomials, localizer, prime
        )
        print("p prime", prime, "open zeros", len(zeros), flush=True)
        while len(zeros):
            point, labels = p_branch_cut(zeros, prime)
            polynomial = fixed_primitive_support(
                labels,
                {"f": 0},
                variables,
            )
            if polynomial not in polynomials:
                polynomials.append(polynomial)
            values = values_at_points(polynomial, variables, zeros, prime)
            target_value = values_at_points(
                polynomial,
                variables,
                np.asarray((point,), dtype=np.int64),
                prime,
            )[0]
            if target_value == 0:
                print("p bad reduction", prime, point, flush=True)
                break
            zeros = zeros[values == 0]
            added.append((prime, point))
            print("p add", prime, point, "remaining", len(zeros), flush=True)
        else:
            status = singular_status(
                [p_polynomial] + polynomials, variables, localizer
            )
            print("p exact", status, flush=True)
            if "UNIT" in status and "NONUNIT" not in status:
                print("P_MODULAR_POINTS", tuple(added), flush=True)
                return
    print("P_MODULAR_POINTS", tuple(added), flush=True)
    raise AssertionError("p branch")


def close_p_complement(noncoordinate=False):
    """Close the P branch away from the exact b=-2 and d=-2 strata."""
    a, b, c, d, e, f = SYMBOLS
    variables = (a, b, c, d, e)
    origin = fixed_primitive_support(
        labels_at((0, 0, 0, 0, 0, 0)), {"f": 0}, variables
    )
    p_polynomial = max(
        (factor for factor, _multiplicity in sp.factor_list(origin)[1]),
        key=sp.total_degree,
    )
    t_polynomial = a*(2*e+1)+2
    q_polynomial = b*d+3*b+3*d+6
    localizer = (
        (b+1)*(d+1)*t_polynomial*q_polynomial*(b+2)*(d+2)
    )
    if noncoordinate:
        localizer *= a*c*e
    prefix = "p noncoordinate" if noncoordinate else "p complement"

    polynomials = []
    for index, point in enumerate(FIVE_POINTS[:8]):
        print(prefix, "base", index + 1, point, flush=True)
        labels = labels_at((*point, 0))
        polynomial = fixed_primitive_support(
            labels, {"f": 0}, variables
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)

    added = []
    for prime in (17, 19, 23, 29):
        zeros = p_branch_zeros(
            p_polynomial, polynomials, localizer, prime
        )
        print(prefix, "prime", prime, "open zeros", len(zeros), flush=True)
        while len(zeros):
            point, labels = p_branch_cut(zeros, prime)
            polynomial = fixed_primitive_support(
                labels, {"f": 0}, variables
            )
            if polynomial not in polynomials:
                polynomials.append(polynomial)
            values = values_at_points(polynomial, variables, zeros, prime)
            target_value = values_at_points(
                polynomial,
                variables,
                np.asarray((point,), dtype=np.int64),
                prime,
            )[0]
            if target_value == 0:
                print(prefix, "bad reduction", prime, point, flush=True)
                break
            zeros = zeros[values == 0]
            added.append((prime, point))
            print(
                prefix, "add", prime, point,
                "remaining", len(zeros), flush=True,
            )
        else:
            status = singular_status(
                [p_polynomial] + polynomials, variables, localizer
            )
            print(prefix, "exact", status, flush=True)
            if "UNIT" in status and "NONUNIT" not in status:
                print(
                    "P_NONCOORDINATE_POINTS"
                    if noncoordinate else "P_COMPLEMENT_POINTS",
                    tuple(added), flush=True,
                )
                return
    print(
        "P_NONCOORDINATE_POINTS"
        if noncoordinate else "P_COMPLEMENT_POINTS",
        tuple(added), flush=True,
    )
    raise AssertionError(prefix)


def close_p_coordinate_plane(plane):
    """Close one disjoint coordinate-plane piece of the P complement."""
    a, b, c, d, e, f = SYMBOLS
    all_variables = (a, b, c, d, e)
    origin = fixed_primitive_support(
        labels_at((0, 0, 0, 0, 0, 0)), {"f": 0}, all_variables
    )
    p_polynomial = max(
        (factor for factor, _multiplicity in sp.factor_list(origin)[1]),
        key=sp.total_degree,
    )
    t_polynomial = a*(2*e+1)+2
    q_polynomial = b*d+3*b+3*d+6
    base_localizer = (
        (b+1)*(d+1)*t_polynomial*q_polynomial*(b+2)*(d+2)
    )

    if plane == "a0":
        substitutions = {"a": 0, "f": 0}
        variables = (b, c, d, e)
        equation = sp.cancel(
            p_polynomial.subs(a, 0) / ((d+1)*(d+2))
        )
        localizer = base_localizer.subs(a, 0)

        def actual(point):
            bvalue, cvalue, dvalue, evalue = point
            return (0, bvalue, cvalue, dvalue, evalue, 0)
    elif plane == "c0":
        substitutions = {"c": 0, "f": 0}
        variables = (a, b, d, e)
        equation = sp.cancel(
            p_polynomial.subs(c, 0) / ((b+1)*(b+2))
        )
        localizer = base_localizer.subs(c, 0)*a

        def actual(point):
            avalue, bvalue, dvalue, evalue = point
            return (avalue, bvalue, 0, dvalue, evalue, 0)
    elif plane == "e0":
        substitutions = {"e": 0, "f": 0}
        variables = (a, b, c, d)
        equation = p_polynomial.subs(e, 0)
        localizer = base_localizer.subs(e, 0)*a*c

        def actual(point):
            avalue, bvalue, cvalue, dvalue = point
            return (avalue, bvalue, cvalue, dvalue, 0, 0)
    else:
        raise ValueError(plane)
    assert sp.denom(equation) == 1

    polynomials = [sp.expand(equation)]
    for index, point in enumerate(FOUR_POINTS):
        print("p plane", plane, "base", index + 1, flush=True)
        labels = labels_at(actual(point))
        determinant = response.flint_restricted_determinant(
            CHARTS, labels, substitutions
        )
        if not determinant:
            continue
        polynomial = primitive_support(determinant, variables)
        if polynomial not in polynomials:
            polynomials.append(polynomial)

    def add_at(point, prime):
        labels = labels_at(
            actual(point), prime=prime, raw_modular=True
        )
        determinant = response.flint_restricted_determinant(
            CHARTS, labels, substitutions
        )
        assert determinant
        return primitive_support(determinant, variables)

    print("p plane", plane, "supports", len(polynomials), flush=True)
    modular_finish(
        polynomials, variables, add_at,
        localizer=sp.expand(localizer),
    )


def close_p_gf17():
    """Audit the selected P-branch ideal over the algebraic closure of F_17."""
    a, b, c, d, e, f = SYMBOLS
    variables = (a, b, c, d, e)
    prime = 17
    origin = fixed_primitive_support(
        labels_at((0, 0, 0, 0, 0, 0)), {"f": 0}, variables
    )
    p_polynomial = max(
        (factor for factor, _multiplicity in sp.factor_list(origin)[1]),
        key=sp.total_degree,
    )
    t_polynomial = a*(2*e+1)+2
    q_polynomial = b*d+3*b+3*d+6
    localizer = (b+1)*(d+1)*t_polynomial*q_polynomial

    polynomials = [sp.Poly(p_polynomial, *variables, modulus=prime).as_expr()]
    for index, point in enumerate(FIVE_POINTS[:8]):
        print("p gf17 base", index + 1, point, flush=True)
        labels = labels_at((*point, 0))
        polynomial = modular_restricted_support(
            labels, {"f": 0}, variables, prime
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    for index, point in enumerate(P_MODULAR_POINTS):
        print("p gf17 cut", index + 1, point, flush=True)
        labels = labels_at((*point, 0), prime=prime, raw_modular=True)
        polynomial = modular_restricted_support(
            labels, {"f": 0}, variables, prime
        )
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    print("p gf17 supports", len(polynomials), flush=True)
    print(
        "p gf17 exact",
        singular_modular_status(
            polynomials, variables, prime, localizer=localizer
        ),
        flush=True,
    )


def p_selector_labels():
    """Return the rational-base and F_17 selector bases for the P branch."""
    labels = [labels_at((*point, 0)) for point in FIVE_POINTS[:8]]
    labels.extend(
        labels_at((*point, 0), prime=17, raw_modular=True)
        for point in P_MODULAR_POINTS
    )
    return tuple(labels)


def close_p_fixed_component(component, modular=False):
    """Check the exact factor branches induced by b=-2 or d=-2."""
    a, b, c, d, e, f = SYMBOLS
    all_variables = (a, b, c, d, e)
    origin = fixed_primitive_support(
        labels_at((0, 0, 0, 0, 0, 0)), {"f": 0}, all_variables
    )
    p_polynomial = max(
        (factor for factor, _multiplicity in sp.factor_list(origin)[1]),
        key=sp.total_degree,
    )
    t_polynomial = a*(2*e+1)+2
    q_polynomial = b*d+3*b+3*d+6
    base_localizer = (b+1)*(d+1)*t_polynomial*q_polynomial

    if component == "b2-c0":
        substitutions = {"b": -2, "c": 0, "f": 0}
        variables = (a, d, e)
        equations = ()
        localizer = base_localizer.subs({b: -2, c: 0})
    elif component == "b2-em1":
        substitutions = {"b": -2, "e": -1, "f": 0}
        variables = (a, c, d)
        equations = ()
        localizer = base_localizer.subs({b: -2, e: -1})
    elif component == "b2-f":
        substitutions = {"b": -2, "f": 0}
        variables = (a, c, d, e)
        quotient = sp.cancel(
            -p_polynomial.subs(b, -2) / (c*(d+1)*(e+1))
        )
        assert sp.denom(quotient) == 1
        equations = (sp.expand(quotient),)
        localizer = base_localizer.subs(b, -2)*c*(e+1)
    elif component == "d2-a0":
        substitutions = {"d": -2, "a": 0, "f": 0}
        variables = (b, c, e)
        equations = ()
        localizer = base_localizer.subs({d: -2, a: 0})
    elif component == "d2-em1":
        substitutions = {"d": -2, "e": -1, "f": 0}
        variables = (a, b, c)
        equations = ()
        localizer = base_localizer.subs({d: -2, e: -1})
    elif component == "d2-g":
        substitutions = {"d": -2, "f": 0}
        variables = (a, b, c, e)
        quotient = sp.cancel(
            -p_polynomial.subs(d, -2) / (a*(b+1)*(e+1))
        )
        assert sp.denom(quotient) == 1
        equations = (sp.expand(quotient),)
        localizer = base_localizer.subs(d, -2)*a*(e+1)
    else:
        raise ValueError(component)

    polynomials = list(equations)
    for index, labels in enumerate(p_selector_labels()):
        print(component, "selector", index + 1, flush=True)
        determinant = response.flint_restricted_determinant(
            CHARTS, labels, substitutions
        )
        if not determinant:
            continue
        polynomial = primitive_support(determinant, variables)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    print(component, "supports", len(polynomials), flush=True)
    if modular:
        assert component in ("b2-f", "d2-g")

        def add_at(point, prime):
            if component == "b2-f":
                avalue, cvalue, dvalue, evalue = point
                actual = (avalue, -2, cvalue, dvalue, evalue, 0)
            else:
                avalue, bvalue, cvalue, evalue = point
                actual = (avalue, bvalue, cvalue, -2, evalue, 0)
            labels = labels_at(
                actual, prime=prime, raw_modular=True
            )
            determinant = response.flint_restricted_determinant(
                CHARTS, labels, substitutions
            )
            assert determinant
            return primitive_support(determinant, variables)

        modular_finish(
            polynomials, variables, add_at,
            localizer=sp.expand(localizer),
        )
        return
    print(
        component,
        "exact",
        singular_status(polynomials, variables, sp.expand(localizer)),
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "branch",
        choices=(
            "b-1", "d-1", "t", "q", "p", "p-gf17",
            "p-complement", "p-noncoordinate",
            "p-a0", "p-c0", "p-e0",
            "b2-c0", "b2-em1", "b2-f",
            "d2-a0", "d2-em1", "d2-g",
        ),
    )
    parser.add_argument("--modular", action="store_true")
    args = parser.parse_args()
    try:
        if args.branch == "p":
            close_p_branch()
        elif args.branch == "p-complement":
            close_p_complement()
        elif args.branch == "p-noncoordinate":
            close_p_complement(noncoordinate=True)
        elif args.branch in ("p-a0", "p-c0", "p-e0"):
            close_p_coordinate_plane(args.branch[2:])
        elif args.branch == "p-gf17":
            close_p_gf17()
        elif args.branch in (
            "b2-c0", "b2-em1", "b2-f",
            "d2-a0", "d2-em1", "d2-g",
        ):
            close_p_fixed_component(args.branch, modular=args.modular)
        elif args.branch in ("b-1", "d-1"):
            close_fixed(args.branch, modular=args.modular)
        else:
            close_rational(args.branch, modular=args.modular)
    finally:
        response.PRIME = DEFAULT_PRIME


if __name__ == "__main__":
    main()
