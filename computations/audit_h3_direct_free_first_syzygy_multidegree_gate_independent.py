#!/usr/bin/env python3
"""Independent exact audit of the first h=3 direct-free reset syzygy gate.

No code or computed data are imported from the primary checker.  The audit
uses a bit-mask matching recursion, a 24-coordinate fine grading, and a
separate sparse-polynomial implementation.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json


F = Fraction
ZERO = F(0)
ONE = F(1)
SITES = tuple(range(8))
ODD_SITES = (1, 2, 3, 4, 5)
PURE_WORD = (0, 0, 0, 0, 0, 0, 0, 0)
MIXED_WORD = (0, 1, 2, 1, 1, 2, 2, 2)
ODD_WORD = MIXED_WORD[1:6]
U_VAR = ("u",)
EXPECTED_DIGEST = "7c083defb48358d17679f94743eba3bac17dcd52a874a31f78042b00b20f1f34"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(site_a, site_b, color_a, color_b):
    require(site_a != site_b, "edge loop requested")
    if site_a < site_b:
        return ("w", site_a, site_b, color_a, color_b)
    return ("w", site_b, site_a, color_b, color_a)


def matching_edge_sets(mask):
    """Return perfect matchings as tuples by deleting the least set bit."""
    if mask == 0:
        return ((),)
    require(mask.bit_count() % 2 == 0, "odd matching mask")
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    answer = []
    partners = rest
    while partners:
        second_bit = partners & -partners
        second = second_bit.bit_length() - 1
        for tail in matching_edge_sets(rest ^ second_bit):
            answer.append(((first, second),) + tail)
        partners ^= second_bit
    return tuple(answer)


def monomial(*variables):
    return tuple(sorted(variables))


def hafnian(vertices, word):
    mask = sum(1 << site for site in vertices)
    result = {}
    for matching in matching_edge_sets(mask):
        term = monomial(*(
            edge(site_a, site_b, word[site_a], word[site_b])
            for site_a, site_b in matching
        ))
        result[term] = result.get(term, ZERO) + ONE
    return result


def polynomial_add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for term, coefficient in polynomial.items():
            result[term] = result.get(term, ZERO) + coefficient
            if result[term] == ZERO:
                del result[term]
    return result


def polynomial_scale(scalar, polynomial):
    return {
        term: scalar * coefficient
        for term, coefficient in polynomial.items()
        if scalar * coefficient != ZERO
    }


def polynomial_product(left, right):
    result = {}
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            term = monomial(*(left_term + right_term))
            result[term] = (
                result.get(term, ZERO)
                + left_coefficient * right_coefficient
            )
            if result[term] == ZERO:
                del result[term]
    return result


def polynomial_variables(polynomial):
    return {
        variable
        for term in polynomial
        for variable in term
    }


def word_degree(word):
    degree = [0] * 24
    for site, color in enumerate(word):
        degree[3 * site + color] += 1
    return tuple(degree)


def edge_monomial_degree(term):
    degree = [0] * 24
    for variable in term:
        require(variable[0] == "w", "non-edge in edge degree")
        _, site_a, site_b, color_a, color_b = variable
        degree[3 * site_a + color_a] += 1
        degree[3 * site_b + color_b] += 1
    return tuple(degree)


def degree_max(left, right):
    return tuple(max(a, b) for a, b in zip(left, right))


def degree_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def degree_subtract(left, right):
    difference = tuple(a - b for a, b in zip(left, right))
    require(all(entry >= 0 for entry in difference), "negative fine degree")
    return difference


def degree_weight(degree):
    return sum(degree)


def expected_defect_terms():
    colors = dict(zip(ODD_SITES, ODD_WORD))

    def e(site_a, site_b):
        return edge(site_a, site_b, colors[site_a], colors[site_b])

    return {
        1: {
            monomial(e(2, 3), e(4, 5)),
            monomial(e(2, 4), e(3, 5)),
            monomial(e(2, 5), e(3, 4)),
        },
        2: {
            monomial(e(1, 3), e(4, 5)),
            monomial(e(1, 4), e(3, 5)),
            monomial(e(1, 5), e(3, 4)),
        },
        3: {
            monomial(e(1, 2), e(4, 5)),
            monomial(e(1, 4), e(2, 5)),
            monomial(e(1, 5), e(2, 4)),
        },
        4: {
            monomial(e(1, 2), e(3, 5)),
            monomial(e(1, 3), e(2, 5)),
            monomial(e(1, 5), e(2, 3)),
        },
        5: {
            monomial(e(1, 2), e(3, 4)),
            monomial(e(1, 3), e(2, 4)),
            monomial(e(1, 4), e(2, 3)),
        },
    }


def guard_word_edge_values():
    """Direct-free guard's internal q restricted to the word 12112."""
    colors = dict(zip(ODD_SITES, ODD_WORD))
    values = {}
    for site_a, site_b in combinations(ODD_SITES, 2):
        variable = edge(site_a, site_b, colors[site_a], colors[site_b])
        values[variable] = ONE if (site_a, site_b) in {(1, 2), (1, 4)} else ZERO
    return values


def specialize(polynomial, values):
    answer = ZERO
    for term, coefficient in polynomial.items():
        term_value = coefficient
        for variable in term:
            term_value *= values.get(variable, ZERO)
        answer += term_value
    return answer


def display_variable(variable):
    _, site_a, site_b, color_a, color_b = variable
    return f"w{site_a}{site_b}^{color_a}{color_b}"


def display_term(term):
    return "*".join(display_variable(variable) for variable in term)


def main():
    pure_degree = word_degree(PURE_WORD)
    mixed_degree = word_degree(MIXED_WORD)
    common_degree_floor = degree_max(pure_degree, mixed_degree)
    pure_deficit = degree_subtract(common_degree_floor, pure_degree)
    mixed_deficit = degree_subtract(common_degree_floor, mixed_degree)

    agreements = tuple(
        site for site in SITES if PURE_WORD[site] == MIXED_WORD[site]
    )
    require(agreements == (0,), "the global words' agreement sites changed")
    require(
        degree_weight(common_degree_floor) == 15,
        "fine componentwise LCM no longer has 15 slots",
    )
    require(
        degree_weight(pure_deficit) == degree_weight(mixed_deficit) == 7,
        "fine LCM deficits are no longer seven slots",
    )

    # An edge-degree d multiplier contributes exactly 2d fine slots.  Every
    # common homogeneous degree dominates the componentwise LCM, so 2d >= 7.
    excluded_degrees = tuple(
        degree for degree in range(4) if 2 * degree < 7
    )
    require(excluded_degrees == (0, 1, 2, 3), "parity lower bound changed")

    first_common_degree = degree_add(pure_degree, mixed_degree)
    coefficient_on_pure_degree = degree_subtract(
        first_common_degree, pure_degree
    )
    coefficient_on_mixed_degree = degree_subtract(
        first_common_degree, mixed_degree
    )
    require(
        degree_weight(coefficient_on_pure_degree)
        == degree_weight(coefficient_on_mixed_degree)
        == 8,
        "first realized coefficient degree is not four edges",
    )

    pure_hafnian = hafnian(SITES, PURE_WORD)
    mixed_hafnian = hafnian(SITES, MIXED_WORD)
    require(
        len(pure_hafnian) == len(mixed_hafnian) == 105,
        "eight-site perfect-matching count changed",
    )
    require(
        all(len(term) == 4 for term in pure_hafnian | mixed_hafnian),
        "a global hafnian term does not have four edges",
    )
    require(
        all(
            edge_monomial_degree(term) == pure_degree
            for term in pure_hafnian
        ),
        "pure hafnian is not fine homogeneous",
    )
    require(
        all(
            edge_monomial_degree(term) == mixed_degree
            for term in mixed_hafnian
        ),
        "mixed hafnian is not fine homogeneous",
    )

    pure_variables = polynomial_variables(pure_hafnian) | {U_VAR}
    mixed_variables = polynomial_variables(mixed_hafnian)
    require(
        pure_variables.isdisjoint(mixed_variables),
        "the two homogenized rows do not have separated variables",
    )
    # Since each row is a nonconstant polynomial in a variable set disjoint
    # from the other, any common divisor has degree zero in both sets.  This
    # is the coprimality certificate used by the two-row syzygy lemma.
    require(
        len(pure_variables) > 1 and len(mixed_variables) > 1,
        "coprimality certificate became vacuous",
    )

    u = {(U_VAR,): ONE}
    pure_row = polynomial_add(pure_hafnian, polynomial_scale(-ONE, u))
    mixed_row = mixed_hafnian
    coefficient_on_pure_row = mixed_row
    coefficient_on_mixed_row = polynomial_scale(-ONE, pure_row)
    koszul_boundary = polynomial_add(
        polynomial_product(coefficient_on_pure_row, pure_row),
        polynomial_product(coefficient_on_mixed_row, mixed_row),
    )
    require(koszul_boundary == {}, "two-row Koszul boundary is nonzero")

    # K = H_m r_0 + (u-H_0) r_m.  After u=1, the unique edge-degree-zero
    # term in the coefficient of r_m is +1.
    require(
        coefficient_on_mixed_row.get((U_VAR,)) == ONE,
        "the lowest mixed-row symbol has the wrong sign",
    )
    require(
        all(
            coefficient == -ONE
            for term, coefficient in coefficient_on_mixed_row.items()
            if term != (U_VAR,)
        ),
        "the quartic correction on the mixed row changed sign",
    )
    reset_scale = F(1, 4)
    require(
        reset_scale * coefficient_on_mixed_row[(U_VAR,)] == F(1, 4),
        "normalized lowest reset symbol is not +1/4",
    )

    expected = expected_defect_terms()
    all_defect_terms = set()
    defects = {}
    colors = dict(zip(ODD_SITES, ODD_WORD))
    for deleted_site in ODD_SITES:
        remaining = tuple(
            site for site in ODD_SITES if site != deleted_site
        )
        defect = hafnian(remaining, colors)
        require(
            set(defect) == expected[deleted_site],
            f"site {deleted_site}: universal defect monomials changed",
        )
        require(
            len(defect) == 3
            and all(coefficient == ONE for coefficient in defect.values()),
            f"site {deleted_site}: universal defect is not a three-term quadric",
        )
        require(
            all_defect_terms.isdisjoint(defect),
            f"site {deleted_site}: defect supports are no longer disjoint",
        )
        all_defect_terms.update(defect)
        expected_degree = [0] * 24
        for site in remaining:
            expected_degree[3 * site + colors[site]] = 1
        require(
            all(
                edge_monomial_degree(term) == tuple(expected_degree)
                for term in defect
            ),
            f"site {deleted_site}: defect has the wrong fine degree",
        )
        defects[deleted_site] = defect

    # The other ten denominator columns have the wrong exposed color and
    # therefore coefficient zero at the selected word.
    nonzero_denominator_columns = tuple(
        (site, color)
        for site in ODD_SITES
        for color in range(3)
        if color == colors[site]
    )
    require(
        nonzero_denominator_columns
        == ((1, 1), (2, 2), (3, 1), (4, 1), (5, 2)),
        "the five potentially nonzero denominator columns changed",
    )

    guard_values = guard_word_edge_values()
    supported_guard_edges = {
        variable for variable, value in guard_values.items() if value != ZERO
    }
    require(
        supported_guard_edges
        == {
            edge(1, 2, 1, 2),
            edge(1, 4, 1, 1),
        },
        "direct-free odd-word support changed",
    )
    guard_defect_values = {
        site: specialize(defect, guard_values)
        for site, defect in defects.items()
    }
    require(
        all(value == ZERO for value in guard_defect_values.values()),
        "a universal denominator defect survives on the direct-free guard",
    )

    # The guard evaluation is a non-flat specialization.  For example the
    # nonzero universal variable below maps to zero.  Multiplication by it is
    # injective in the polynomial domain but becomes the zero map after base
    # change, so exactness need not be preserved at the left end.
    nonflat_witness = edge(2, 3, 2, 1)
    require(
        nonflat_witness in polynomial_variables(defects[1]),
        "chosen non-flat witness left the denominator defects",
    )
    require(
        guard_values[nonflat_witness] == ZERO,
        "chosen non-flat witness is not killed by specialization",
    )

    ledger = {
        "agreement_sites": list(agreements),
        "fine_lcm_slots": degree_weight(common_degree_floor),
        "fine_lcm_deficits": [
            degree_weight(pure_deficit), degree_weight(mixed_deficit)
        ],
        "excluded_edge_degrees": list(excluded_degrees),
        "first_edge_degree": 4,
        "hafnian_terms": [len(pure_hafnian), len(mixed_hafnian)],
        "separated_variable_coprime": True,
        "koszul_boundary_terms": len(koszul_boundary),
        "lowest_mixed_row_symbol": "+u",
        "normalized_reset_symbol": "+1/4",
        "defects": {
            str(site): sorted(display_term(term) for term in defect)
            for site, defect in defects.items()
        },
        "defect_supports_pairwise_disjoint": True,
        "nonzero_denominator_columns": [
            list(column) for column in nonzero_denominator_columns
        ],
        "guard_defect_values": {
            str(site): str(value)
            for site, value in guard_defect_values.items()
        },
        "nonflat_witness": display_variable(nonflat_witness),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"independent ledger digest: {digest}")
    print("independent h=3 first-syzygy multidegree audit: PASS")
    print("fine parity gate: edge degrees 0--3 excluded; degree 4 attained")
    print("coprime two-row Koszul cell: unique up to scalar, lowest symbol +r_m")
    print("universal reset: five disjoint nonzero quadratic denominator defects")
    print("direct-free guard kills all five; specialization is non-flat")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
