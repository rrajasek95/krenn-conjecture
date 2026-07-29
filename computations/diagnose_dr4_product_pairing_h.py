#!/usr/bin/env python3
"""Find an exact toric H certificate on the DR4 product-pairing locus."""

from collections import defaultdict
from itertools import combinations, combinations_with_replacement

import sympy as sp
from sympy.polys.domains import QQ


K = QQ.frac_field("a", "b")
a, b = K.gens
anchors = (K.one, a, b, a * b)
subsets = tuple(
    subset
    for degree in range(1, 5)
    for subset in combinations(range(4), degree)
)


def endpoint_rows():
    rows = []
    for i, ti in enumerate(anchors):
        complement = tuple(j for j in range(4) if j != i)
        for sign in (1, -1):
            diagonal = {}
            for j in complement:
                derivative = sum(
                    (1 / (anchors[j] - anchors[k]) for k in complement if k != j),
                    K.zero,
                )
                shift = (
                    -2 / (anchors[j] + ti)
                    if sign == 1
                    else -1 / (anchors[j] + ti) - 1 / (anchors[j] - ti)
                )
                diagonal[j] = derivative + shift

            coefficients = {tuple(complement): K.one}
            for pair in combinations(complement, 2):
                remaining = next(j for j in complement if j not in pair)
                coefficients[pair] = diagonal[remaining]
            for j in complement:
                k, ell = (h for h in complement if h != j)
                coefficients[(j,)] = (
                    diagonal[k] * diagonal[ell]
                    + 1 / (anchors[k] - anchors[ell]) ** 2
                )
            rows.append([coefficients.get(subset, K.zero) for subset in subsets])
            multiplied = {
                tuple(sorted((i,) + subset)): value
                for subset, value in coefficients.items()
            }
            rows.append([multiplied.get(subset, K.zero) for subset in subsets])
    return rows


def kernel_of_fourteen(rows, omitted=(0, 1)):
    matrix = [row[:] for index, row in enumerate(rows) if index not in omitted]
    pivot_columns = []
    pivot_row = 0
    for column in range(15):
        selected = next(
            (row for row in range(pivot_row, 14) if matrix[row][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(14):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                value - multiple * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == 14:
            break
    assert len(pivot_columns) == 14
    free_column = next(column for column in range(15) if column not in pivot_columns)
    kernel = [K.zero] * 15
    kernel[free_column] = K.one
    for row, column in reversed(tuple(enumerate(pivot_columns))):
        kernel[column] = -sum(
            (matrix[row][j] * kernel[j] for j in range(column + 1, 15)),
            K.zero,
        )
    return kernel, pivot_columns, free_column


def main():
    rows = endpoint_rows()
    kernel, pivots, free = kernel_of_fourteen(rows, omitted=(0, 2))
    for row in rows:
        assert not sum((x * y for x, y in zip(row, kernel, strict=True)), K.zero)

    h = (a + 1) ** 2 * (b + 1) ** 2 - 16 * a * b
    candidates = []
    for first, second in combinations(range(4, 10), 2):
        i, j = subsets[first]
        k, ell = subsets[second]
        value = kernel[first] * kernel[k] * kernel[ell]
        value -= kernel[second] * kernel[i] * kernel[j]
        if not value:
            continue
        numerator_raw, denominator_raw = sp.together(
            value.as_expr()
        ).as_numer_denom()
        numerator = sp.factor(numerator_raw)
        denominator = sp.factor(denominator_raw)
        quotient = sp.factor(numerator / h.as_expr())
        if sp.denom(quotient) == 1:
            candidates.append((first, second, numerator, denominator, quotient))

    assert candidates

    # Search every homogeneous quadratic toric relation
    # v_S v_T-v_A v_B with identical exponent sum.
    grouped = defaultdict(list)
    for first, second in combinations_with_replacement(range(15), 2):
        exponent = tuple(
            int(vertex in subsets[first]) + int(vertex in subsets[second])
            for vertex in range(4)
        )
        grouped[exponent].append((first, second))

    quadratic = []
    for pairs in grouped.values():
        if len(pairs) < 2:
            continue
        baseline = pairs[0]
        for other in pairs[1:]:
            value = kernel[baseline[0]] * kernel[baseline[1]]
            value -= kernel[other[0]] * kernel[other[1]]
            if not value:
                continue
            numerator, denominator = sp.together(
                value.as_expr()
            ).as_numer_denom()
            numerator = sp.factor(numerator)
            quotient = sp.factor(numerator / h.as_expr())
            if sp.denom(quotient) == 1:
                quadratic.append(
                    (baseline, other, numerator, sp.factor(denominator), quotient)
                )

    assert quadratic
    best = min(quadratic, key=lambda item: sp.count_ops(item[4]))
    baseline, other, numerator, denominator, quotient = best
    print("pivots", pivots, "free", free)
    print(
        "best quadratic",
        (subsets[baseline[0]], subsets[baseline[1]]),
        (subsets[other[0]], subsets[other[1]]),
    )
    print("numerator =", numerator)
    print("denominator =", denominator)
    print("numerator/H factors =", sp.factor_list(quotient))
    gcd = sp.Poly(quadratic[0][2], sp.Symbol("a"), sp.Symbol("b"))
    for relation in quadratic[1:]:
        gcd = sp.gcd(
            gcd,
            sp.Poly(relation[2], sp.Symbol("a"), sp.Symbol("b")),
        )
    print("quadratic numerator gcd =", sp.factor(gcd.as_expr()))
    structural = {
        sp.factor(value)
        for value in (
            sp.Symbol("a"),
            sp.Symbol("b"),
            sp.Symbol("a") - 1,
            sp.Symbol("a") + 1,
            sp.Symbol("b") - 1,
            sp.Symbol("b") + 1,
            sp.Symbol("a") - sp.Symbol("b"),
            sp.Symbol("a") + sp.Symbol("b"),
            sp.Symbol("a") * sp.Symbol("b") - 1,
            sp.Symbol("a") * sp.Symbol("b") + 1,
        )
    }
    residual_examples = {}
    for baseline, other, numerator, denominator, quotient in quadratic:
        constant, factors = sp.factor_list(quotient)
        residual = sp.Integer(constant)
        for factor, exponent in factors:
            if sp.factor(factor) not in structural:
                residual *= factor**exponent
        residual = sp.factor(residual)
        residual_examples.setdefault(residual, (baseline, other))
    for residual, (baseline, other) in sorted(
        residual_examples.items(), key=lambda item: sp.count_ops(item[0])
    ):
        print(
            "residual",
            residual,
            "from",
            (subsets[baseline[0]], subsets[baseline[1]]),
            (subsets[other[0]], subsets[other[1]]),
        )


if __name__ == "__main__":
    main()
