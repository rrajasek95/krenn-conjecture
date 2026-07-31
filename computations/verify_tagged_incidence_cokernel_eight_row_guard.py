#!/usr/bin/env python3
"""Exact all-word audit of the tagged incidence-cokernel eight-row guard."""

from fractions import Fraction
from itertools import combinations, product


N = 6
COLORS = range(3)
LABELS = range(3)
ZERO = Fraction(0)
ONE = Fraction(1)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    x = vertices[0]
    for pos in range(1, len(vertices)):
        y = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((x, y),) + matching


MATCHINGS = {
    tuple(vertices): tuple(perfect_matchings(vertices))
    for size in range(0, N + 1, 2)
    for vertices in combinations(range(N), size)
}


# Internal residual edges of the binary C8 source after deleting p,q.
Q = {
    (2, 3, 0, 0): ONE,
    (4, 5, 0, 0): ONE,
    (1, 2, 1, 1): ONE,
    (3, 4, 1, 1): ONE,
}

# Endpoint-star rows.  The third-label edges are physically present but
# have zero q^[2]-cofactor.  The q-endpoint label of s_2 is 2, while its
# residual endpoint has physical color 0.
P = {
    (0, 0, 0): ONE,
    (1, 5, 1): ONE,
    (2, 2, 2): ONE,
}
S = {
    (0, 1, 0): ONE,
    (1, 0, 1): ONE,
    (2, 4, 0): ONE,
}


def q_coeff(x, cx, y, cy):
    if x > y:
        x, y, cx, cy = y, x, cy, cx
    return Q.get((x, y, cx, cy), ZERO)


def hafnian(word, vertices=tuple(range(N))):
    total = ZERO
    for matching in MATCHINGS[tuple(vertices)]:
        term = ONE
        for x, y in matching:
            term *= q_coeff(x, word[x], y, word[y])
        total += term
    return total


def response(i, j, word):
    total = ZERO
    for x, y in combinations(range(N), 2):
        edge = (
            P.get((i, x, word[x]), ZERO) * S.get((j, y, word[y]), ZERO)
            + P.get((i, y, word[y]), ZERO) * S.get((j, x, word[x]), ZERO)
        )
        if not edge:
            continue
        complement = tuple(z for z in range(N) if z not in (x, y))
        total += edge * hafnian(word, complement)
    return total


def direct(i, j):
    return ONE if (i, j) == (0, 2) else ZERO


def lhs(i, j, word):
    return direct(i, j) * hafnian(word) + response(i, j, word)


def target(i, j, word):
    if i != j or i == 2:
        return ZERO
    return ONE if all(color == i for color in word) else ZERO


def rank(matrix):
    a = [[Fraction(entry) for entry in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [entry / scale for entry in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not a[r][col]:
                continue
            scale = a[r][col]
            a[r] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(a[r], a[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def audit_all_words():
    supplied_rows = [
        (i, j) for i in LABELS for j in LABELS if (i, j) != (2, 2)
    ]
    checked = 0
    for word in product(COLORS, repeat=N):
        require(hafnian(word) == 0, ("q^[3] became nonzero", word))
        for i, j in supplied_rows:
            require(
                lhs(i, j, word) == target(i, j, word),
                ("supplied all-word row failure", word, i, j),
            )
            checked += 1
    require(checked == 8 * 729, ("supplied coefficient count", checked))

    # Relative to the full-nine target, exactly one coefficient is missing.
    ninth_residuals = []
    for word in product(COLORS, repeat=N):
        wanted = ONE if all(color == 2 for color in word) else ZERO
        residual = lhs(2, 2, word) - wanted
        if residual:
            ninth_residuals.append((word, residual))
    require(
        ninth_residuals == [((2,) * N, -ONE)],
        ("ninth-row residual ledger changed", ninth_residuals),
    )


def audit_goodness_and_cokernel():
    p_rows = [
        [P.get((i, site, color), ZERO) for i in LABELS]
        for site in range(N)
        for color in COLORS
    ]
    s_rows = [
        [S.get((j, site, color), ZERO) for j in LABELS]
        for site in range(N)
        for color in COLORS
    ]
    require(rank(p_rows) == 3, "first star is not good")
    require(rank(s_rows) == 3, "second star is not good")
    p_selector = [
        [P.get((i, site, color), ZERO) for i in LABELS]
        for site, color in ((0, 0), (5, 1), (2, 2))
    ]
    s_selector = [
        [S.get((j, site, color), ZERO) for j in LABELS]
        for site, color in ((1, 0), (0, 1), (4, 0))
    ]
    identity = [[ONE if i == j else ZERO for j in LABELS] for i in LABELS]
    require(p_selector == identity, "first coordinate selector changed")
    require(s_selector == identity, "second coordinate selector changed")
    require(direct(0, 2) == 1, "selected d_02 orientation changed")
    require(direct(2, 0) == 0, "direct block was accidentally transposed")
    require(
        sum(direct(i, j) != 0 for i in LABELS for j in LABELS) == 1,
        "direct block is not exactly E_02",
    )

    # For selected (a,b,c)=(0,2,0), beta_0(c)=z_4^0 and q has no edge at 0.
    coords0 = [(site, color) for site in range(1, N) for color in COLORS]
    beta0 = [ONE if coord == (4, 0) else ZERO for coord in coords0]
    q0_columns = [
        [
            q_coeff(0, input_color, site, output_color)
            for site, output_color in coords0
        ]
        for input_color in COLORS
    ]
    require(rank(q0_columns) == 0, "Q_0 is no longer zero")
    require(rank(q0_columns + [beta0]) == 1, "beta_0 lost its cokernel class")

    # The other response endpoint gives beta_4(0)=z_0^0, outside im Q_4.
    coords4 = [
        (site, color)
        for site in range(N)
        if site != 4
        for color in COLORS
    ]
    beta4 = [ONE if coord == (0, 0) else ZERO for coord in coords4]
    q4_columns = [
        [
            q_coeff(4, input_color, site, output_color)
            for site, output_color in coords4
        ]
        for input_color in COLORS
    ]
    require(rank(q4_columns) == 2, "Q_4 incidence rank changed")
    require(rank(q4_columns + [beta4]) == 3, "beta_4 lost its cokernel class")


def response_quadratic(i, j):
    result = {}
    for x, y in combinations(range(N), 2):
        for cx in COLORS:
            for cy in COLORS:
                value = (
                    P.get((i, x, cx), ZERO) * S.get((j, y, cy), ZERO)
                    + P.get((i, y, cy), ZERO) * S.get((j, x, cx), ZERO)
                )
                if value:
                    result[((x, cx), (y, cy))] = value
    return result


def multiply_quadratics(left, right):
    result = {}
    for monomial_left, coefficient_left in left.items():
        sites_left = {site for site, _ in monomial_left}
        for monomial_right, coefficient_right in right.items():
            if sites_left.intersection(site for site, _ in monomial_right):
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            result[monomial] = (
                result.get(monomial, ZERO) + coefficient_left * coefficient_right
            )
    return {monomial: value for monomial, value in result.items() if value}


def audit_literal_segre_and_mutations():
    responses = {
        (i, j): response_quadratic(i, j) for i in LABELS for j in LABELS
    }
    for i in LABELS:
        for k in LABELS:
            for j in LABELS:
                for ell in LABELS:
                    left = multiply_quadratics(responses[i, j], responses[k, ell])
                    right = multiply_quadratics(responses[i, ell], responses[k, j])
                    require(
                        left == right,
                        ("literal Segre rectangle failed", i, k, j, ell),
                    )

    # Mutation guard 1: deleting the 23 color-zero cofactor edge destroys X0.
    key = (2, 3, 0, 0)
    saved = Q.pop(key)
    try:
        require(
            lhs(0, 0, (0,) * N) == 0,
            "deleted color-zero cofactor edge was not detected",
        )
    finally:
        Q[key] = saved
    require(lhs(0, 0, (0,) * N) == 1, "cofactor restoration failed")

    # Mutation guard 2: moving s_2 from the dark even site 4 to site 3
    # activates the selected 02 row on a concrete mixed word.
    mutated_word = (0, 1, 1, 0, 0, 0)
    saved_s2 = S.pop((2, 4, 0))
    S[(2, 3, 0)] = saved_s2
    try:
        require(
            lhs(0, 2, mutated_word) == 1,
            "mutated selected response did not acquire its mixed cofactor",
        )
    finally:
        S.pop((2, 3, 0))
        S[(2, 4, 0)] = saved_s2
    require(lhs(0, 2, mutated_word) == 0, "dark endpoint restoration failed")

    # Mutation guard 3: removing either dead third-label star keeps the
    # eight tensors but destroys the corresponding goodness certificate.
    p_without_third = [
        [P.get((i, site, color), ZERO) for i in LABELS]
        for site in range(N)
        for color in COLORS
        if (site, color) != (2, 2)
    ]
    s_without_third = [
        [S.get((j, site, color), ZERO) for j in LABELS]
        for site in range(N)
        for color in COLORS
        if (site, color) != (4, 0)
    ]
    require(rank(p_without_third) == 2, "p_2 deletion mutation was not detected")
    require(rank(s_without_third) == 2, "s_2 deletion mutation was not detected")


def main():
    audit_all_words()
    audit_goodness_and_cokernel()
    audit_literal_segre_and_mutations()
    print(
        "PASS: all 8*729 supplied coefficients; sole residual -X2; "
        "d=E_02; coordinate selectors/good Segre stars; "
        "beta_0(0), beta_4(0) cokernels; "
        "mutation guards"
    )


if __name__ == "__main__":
    main()
