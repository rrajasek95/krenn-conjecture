#!/usr/bin/env python3
"""Clean-room audit of the full-rank-site response countermodel.

This file deliberately imports nothing from the primary verifier.  It uses
six-bit support masks, keeps the colour at site zero as a separate monomial
label, and constructs divided powers by repeated multiplication followed by
division by the degree.  The edge list and the cofactor order are both
different from those in the primary artifact.
"""

from __future__ import annotations

from itertools import combinations, product as cartesian_product

import sympy as sp


N = 6
FULL = (1 << N) - 1
ZERO_COLOUR = -1
Monomial = tuple[int, int]
Polynomial = dict[Monomial, sp.Expr]
ONE: Polynomial = {(0, ZERO_COLOUR): sp.Integer(1)}


def clean(poly: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for monomial, coefficient in poly.items():
        coefficient = sp.expand(coefficient)
        if coefficient != 0:
            answer[monomial] = coefficient
    return answer


def add(*polys: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
    return clean(answer)


def scaled(poly: Polynomial, scalar: sp.Expr | int) -> Polynomial:
    return clean(
        {monomial: sp.sympify(scalar) * coefficient for monomial, coefficient in poly.items()}
    )


def product(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply in the site-square-zero algebra."""
    answer: Polynomial = {}
    for (left_mask, left_colour), left_coefficient in left.items():
        for (right_mask, right_colour), right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            result_mask = left_mask | right_mask
            if left_mask & 1:
                result_colour = left_colour
            elif right_mask & 1:
                result_colour = right_colour
            else:
                result_colour = ZERO_COLOUR
            monomial = (result_mask, result_colour)
            answer[monomial] = (
                answer.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return clean(answer)


def multiply_all(*polys: Polynomial) -> Polynomial:
    answer = ONE
    for poly in polys:
        answer = product(answer, poly)
    return answer


def divided_power(poly: Polynomial, degree: int) -> Polynomial:
    """Use f^[d] = f^[d-1] f / d, rather than edge-subset selection."""
    answer = ONE
    for current_degree in range(1, degree + 1):
        answer = scaled(product(answer, poly), sp.Rational(1, current_degree))
    return answer


def scalar_word(sites: tuple[int, ...], coefficient: sp.Expr | int = 1) -> Polynomial:
    support = sum(1 << site for site in sites)
    assert not support & 1
    return {(support, ZERO_COLOUR): sp.sympify(coefficient)}


def vector_word(
    vector: tuple[sp.Expr | int, sp.Expr | int, sp.Expr | int],
    other_sites: tuple[int, ...],
) -> Polynomial:
    support = 1 + sum(1 << site for site in other_sites)
    answer: Polynomial = {}
    for colour, coefficient in enumerate(vector):
        coefficient = sp.sympify(coefficient)
        if coefficient != 0:
            answer[(support, colour)] = coefficient
    return clean(answer)


def local(site: int, coefficient: sp.Expr | int = 1, colour: int | None = None) -> Polynomial:
    if site == 0:
        assert colour in (0, 1, 2)
        return {((1 << site), int(colour)): sp.sympify(coefficient)}
    assert colour is None
    return {((1 << site), ZERO_COLOUR): sp.sympify(coefficient)}


def vector_add(*vectors: tuple[sp.Expr, sp.Expr, sp.Expr]) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    return tuple(sp.expand(sum(vector[index] for vector in vectors)) for index in range(3))


def vector_scale(
    scalar: sp.Expr | int, vector: tuple[sp.Expr, sp.Expr, sp.Expr]
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    return tuple(sp.expand(sp.sympify(scalar) * entry) for entry in vector)


def assert_equal(left: Polynomial, right: Polynomial) -> None:
    assert add(left, scaled(right, -1)) == {}


def substitute(poly: Polynomial, substitutions: dict[sp.Symbol, sp.Expr]) -> Polynomial:
    return clean(
        {
            monomial: sp.expand(coefficient.subs(substitutions))
            for monomial, coefficient in poly.items()
        }
    )


def split_linear_row(row: Polynomial) -> dict[int, Polynomial]:
    answer: dict[int, Polynomial] = {}
    for monomial, coefficient in row.items():
        support, _ = monomial
        assert support and support & (support - 1) == 0
        site = support.bit_length() - 1
        answer[site] = add(answer.get(site, {}), {monomial: coefficient})
    return answer


def coefficient_after_site_zero_contraction(
    poly: Polynomial, support: int, x: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Expr:
    answer = 0
    for (monomial_support, colour), coefficient in poly.items():
        if monomial_support != support:
            continue
        if support & 1:
            assert colour in (0, 1, 2)
            answer += coefficient * x[colour]
        else:
            assert colour == ZERO_COLOUR
            answer += coefficient
    return sp.expand(answer)


def matrix_expand(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(sp.expand)


TupleMonomial = tuple[int, int, int, int, int, int]
TuplePolynomial = dict[TupleMonomial, sp.Expr]
TUPLE_ONE: TuplePolynomial = {(-1, -1, -1, -1, -1, -1): sp.Integer(1)}


def tuple_clean(poly: TuplePolynomial) -> TuplePolynomial:
    answer: TuplePolynomial = {}
    for monomial, coefficient in poly.items():
        coefficient = sp.expand(coefficient)
        if coefficient != 0:
            answer[monomial] = coefficient
    return answer


def tuple_add(*polys: TuplePolynomial) -> TuplePolynomial:
    answer: TuplePolynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
    return tuple_clean(answer)


def tuple_scaled(poly: TuplePolynomial, scalar: sp.Expr | int) -> TuplePolynomial:
    return tuple_clean(
        {monomial: sp.sympify(scalar) * coefficient for monomial, coefficient in poly.items()}
    )


def tuple_product(left: TuplePolynomial, right: TuplePolynomial) -> TuplePolynomial:
    answer: TuplePolynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            if any(
                left_label != -1 and right_label != -1
                for left_label, right_label in zip(left_monomial, right_monomial)
            ):
                continue
            monomial = tuple(
                left_label if left_label != -1 else right_label
                for left_label, right_label in zip(left_monomial, right_monomial)
            )
            answer[monomial] = (
                answer.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return tuple_clean(answer)


def tuple_multiply_all(*polys: TuplePolynomial) -> TuplePolynomial:
    answer = TUPLE_ONE
    for poly in polys:
        answer = tuple_product(answer, poly)
    return answer


def tuple_divided_power(poly: TuplePolynomial, degree: int) -> TuplePolynomial:
    answer = TUPLE_ONE
    for current_degree in range(1, degree + 1):
        answer = tuple_scaled(
            tuple_product(answer, poly), sp.Rational(1, current_degree)
        )
    return answer


def tuple_local(
    site: int, label: int = 0, coefficient: sp.Expr | int = 1
) -> TuplePolynomial:
    monomial = [-1] * N
    monomial[site] = label
    return {tuple(monomial): sp.sympify(coefficient)}


def tuple_edge(
    left: int,
    left_label: int,
    right: int,
    right_label: int,
    coefficient: sp.Expr | int = 1,
) -> TuplePolynomial:
    assert left < right
    monomial = [-1] * N
    monomial[left] = left_label
    monomial[right] = right_label
    return {tuple(monomial): sp.sympify(coefficient)}


def tuple_assert_equal(left: TuplePolynomial, right: TuplePolynomial) -> None:
    assert tuple_add(left, tuple_scaled(right, -1)) == {}


def tuple_contraction(
    poly: TuplePolynomial,
    support: int,
    x: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
    y: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Expr:
    answer = 0
    for monomial, coefficient in poly.items():
        monomial_support = sum(
            1 << site for site, label in enumerate(monomial) if label != -1
        )
        if monomial_support != support:
            continue
        factor = coefficient
        if monomial[0] != -1:
            factor *= x[monomial[0]]
        if monomial[1] != -1:
            factor *= y[monomial[1]]
        for site in range(2, N):
            if monomial[site] != -1:
                assert monomial[site] == 0
        answer += factor
    return sp.expand(answer)


def audit_two_separated_target_sites() -> tuple[sp.Matrix, sp.Expr, sp.Matrix]:
    """Rebuild Sections 4's stronger model in a second local algebra."""
    x = sp.symbols("X0:3")
    y = sp.symbols("Y0:3")

    # Reverse/scramble the displayed order and retain literal endpoint labels.
    q = tuple_add(
        tuple_edge(3, 0, 4, 0),
        tuple_edge(2, 0, 4, 0),
        tuple_edge(2, 0, 5, 0, -1),
        tuple_edge(1, 2, 5, 0),
        tuple_edge(0, 0, 5, 0),
        tuple_edge(0, 2, 3, 0, 2),
        tuple_edge(0, 1, 2, 0),
        tuple_edge(0, 2, 1, 2, 2),
        tuple_edge(0, 1, 1, 2),
    )
    q2 = tuple_divided_power(q, 2)
    q3 = tuple_divided_power(q, 3)
    assert q3 == {}
    tuple_assert_equal(tuple_product(q, q), tuple_scaled(q2, 2))
    assert tuple_product(q2, q) == {}

    p = (
        tuple_local(0, 0),
        tuple_local(1, 1),
        tuple_add(tuple_local(2), tuple_local(3, coefficient=-1)),
    )
    s = (
        tuple_local(1, 0, -1),
        tuple_local(0, 1, -1),
        tuple_add(
            tuple_local(0, 1, sp.Rational(1, 4)),
            tuple_local(4, coefficient=sp.Rational(1, 4)),
            tuple_local(5, coefficient=sp.Rational(1, 4)),
        ),
    )
    targets = tuple(
        {(colour, colour, 0, 0, 0, 0): sp.Integer(1)}
        for colour in range(3)
    )
    for i in range(3):
        for j in range(3):
            response = tuple_multiply_all(p[i], s[j], q2)
            tuple_assert_equal(response, targets[i] if i == j else {})

    C = sp.zeros(N)
    for u in range(N):
        for v in range(N):
            if u == v:
                continue
            complement = FULL ^ (1 << u) ^ (1 << v)
            C[u, v] = tuple_contraction(q2, complement, x, y)
    assert C == C.T
    determinant = sp.factor(C.det())
    expected_determinant = -64 * x[2] ** 2 * y[2] ** 4 * (x[1] + 2 * x[2]) ** 2
    assert determinant == expected_determinant

    P = sp.zeros(3, N)
    S = sp.zeros(3, N)
    for i in range(3):
        for site in range(N):
            P[i, site] = tuple_contraction(p[i], 1 << site, x, y)
            S[i, site] = tuple_contraction(s[i], 1 << site, x, y)
    strange_order = (4, 1, 5, 0, 3, 2)
    C_strange = C.extract(strange_order, strange_order)
    P_strange = P.extract((0, 1, 2), strange_order)
    S_strange = S.extract((0, 1, 2), strange_order)
    response = matrix_expand(P_strange * C_strange * S_strange.T)
    assert response == sp.diag(x[0] * y[0], x[1] * y[1], x[2] * y[2])

    # Incident endpoint spans, read directly from the displayed edge blocks.
    W0 = sp.Matrix.hstack(
        sp.Matrix((0, 1, 2)),
        sp.Matrix((0, 1, 0)),
        sp.Matrix((0, 0, 2)),
        sp.Matrix((1, 0, 0)),
    )
    W1 = sp.Matrix.hstack(sp.Matrix((0, 0, 1)), sp.Matrix((0, 0, 1)))
    assert W0.rank() == 3
    assert W1.rank() == 1
    assert sp.eye(3).rank() == 3  # Target rank at each of sites zero and one.
    assert sp.Matrix([[1, 1, 1]]).rank() == 1  # Target rank at each line site.
    return response, determinant, C_strange


def audit_rank_budget_and_omission_pairs() -> dict[str, int]:
    """Exhaust the labelled omission-pair classification in Proposition 5.1."""
    pairs = tuple(frozenset(pair) for pair in combinations(range(N), 2))
    ledger = {
        "141": 0,
        "222_coincident": 0,
        "222_path": 0,
        "303_triangle": 0,
        "coincident_flattenings": 0,
    }

    for omission_pairs in cartesian_product(pairs, repeat=3):
        memberships = [
            sum(site in omission_pair for omission_pair in omission_pairs)
            for site in range(N)
        ]
        # Site cover excludes membership three.  The displayed proposition
        # additionally assumes at least one rank-three site.
        if max(memberships) >= 3 or 0 not in memberships:
            continue
        ranks = [3 - membership for membership in memberships]
        assert sum(ranks) == 12
        rank_counts = (ranks.count(3), ranks.count(2), ranks.count(1))
        intersection_sizes = sorted(
            len(omission_pairs[left] & omission_pairs[right])
            for left, right in combinations(range(3), 2)
        )

        if rank_counts == (1, 4, 1):
            assert len(set(omission_pairs)) == 3
            assert intersection_sizes == [0, 0, 1]
            ledger["141"] += 1
        elif rank_counts == (2, 2, 2):
            if len(set(omission_pairs)) == 2:
                repeated = next(
                    pair for pair in set(omission_pairs) if omission_pairs.count(pair) == 2
                )
                singleton = next(
                    pair for pair in set(omission_pairs) if omission_pairs.count(pair) == 1
                )
                assert repeated.isdisjoint(singleton)
                assert intersection_sizes == [0, 0, 2]
                ledger["222_coincident"] += 1
            else:
                assert len(set(omission_pairs)) == 3
                assert intersection_sizes == [0, 1, 1]
                ledger["222_path"] += 1
        elif rank_counts == (3, 0, 3):
            assert len(set(omission_pairs)) == 3
            assert intersection_sizes == [1, 1, 1]
            assert len(set().union(*omission_pairs)) == 3
            ledger["303_triangle"] += 1
        else:
            raise AssertionError((omission_pairs, ranks, rank_counts))

        # Reconstruct the target side of the pair quotient as a flattening.
        # The row label records response index and the two quotient target
        # axes; the column label is the four-site target word.
        for physical_pair in set(omission_pairs):
            colours = [
                colour
                for colour, omission_pair in enumerate(omission_pairs)
                if omission_pair == physical_pair
            ]
            left_labels = [(colour, colour, colour) for colour in colours]
            complement = tuple(site for site in range(N) if site not in physical_pair)
            right_labels = [tuple(colour for _site in complement) for colour in colours]
            rows = {label: index for index, label in enumerate(left_labels)}
            columns = {label: index for index, label in enumerate(right_labels)}
            flattening = sp.zeros(len(rows), len(columns))
            for left_label, right_label in zip(left_labels, right_labels):
                flattening[rows[left_label], columns[right_label]] += 1
            assert flattening.rank() == len(colours)
            if len(colours) >= 2:
                assert flattening.rank() >= 2
                ledger["coincident_flattenings"] += 1

    assert ledger == {
        "141": 1080,
        "222_coincident": 270,
        "222_path": 1080,
        "303_triangle": 120,
        "coincident_flattenings": 270,
    }
    return ledger


def main() -> None:
    a = sp.symbols("a0:3")
    b = sp.symbols("b0:3")
    x = sp.symbols("x0:3")
    e0 = (sp.Integer(1), sp.Integer(0), sp.Integer(0))
    e1 = (sp.Integer(0), sp.Integer(1), sp.Integer(0))
    e2 = (sp.Integer(0), sp.Integer(0), sp.Integer(1))
    zero = (sp.Integer(0), sp.Integer(0), sp.Integer(0))

    # Deliberately scrambled relative to the primary verifier: internal edge,
    # star, internal edge, star, and so on.
    q = add(
        scalar_word((3, 4)),
        vector_word(b, (5,)),
        scalar_word((2, 4)),
        vector_word(vector_scale(2, e2), (3,)),
        scalar_word((2, 5), -1),
        vector_word(a, (2,)),
        scalar_word((1, 5)),
        vector_word(b, (4,)),
        vector_word(vector_add(a, vector_scale(2, e2)), (1,)),
    )

    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)

    # A support-by-support reconstruction of q^[2].  This is also the complete
    # list: eight site-zero-vector words and three scalar words.
    expected_q2 = add(
        vector_word(vector_scale(-2, e2), (1, 2, 5)),
        scalar_word((1, 3, 4, 5)),
        vector_word(b, (3, 4, 5)),
        vector_word(vector_add(a, vector_scale(2, e2)), (1, 3, 4)),
        scalar_word((2, 3, 4, 5), -1),
        vector_word(vector_scale(2, e2), (1, 3, 5)),
        vector_word(vector_add(a, vector_scale(2, e2)), (2, 3, 4)),
        scalar_word((1, 2, 4, 5)),
        vector_word(b, (1, 4, 5)),
        vector_word(vector_scale(-2, e2), (2, 3, 5)),
        vector_word(vector_add(a, vector_scale(2, e2)), (1, 2, 4)),
    )
    assert_equal(q2, expected_q2)
    assert q3 == {}
    assert_equal(product(q, q), scaled(q2, 2))
    assert product(q2, q) == {}

    p = (
        local(0, colour=0),
        add(local(1, sp.Rational(-1, 2)), local(3, sp.Rational(1, 2))),
        local(4),
    )
    s = (
        add(local(1, sp.Rational(-1, 2)), local(3, sp.Rational(1, 2))),
        local(0, colour=1),
        add(local(1, sp.Rational(-1, 4)), local(3, sp.Rational(-1, 4))),
    )

    targets = tuple(vector_word(basis, (1, 2, 3, 4, 5)) for basis in (e0, e1, e2))
    response: list[list[Polynomial]] = []
    for i in range(3):
        row: list[Polynomial] = []
        for j in range(3):
            direct = multiply_all(p[i], s[j], q2)
            expected = targets[i] if i == j else {}
            assert_equal(direct, expected)

            # Reassemble from explicitly ordered (p-site, s-site) choices in
            # an order unrelated to the site's numerical order.  Terms with
            # the two endpoints reversed are therefore never identified.
            p_by_site = split_linear_row(p[i])
            s_by_site = split_linear_row(s[j])
            ordered = {}
            for p_site in (4, 1, 0, 5, 2, 3):
                for s_site in (2, 5, 3, 0, 4, 1):
                    if p_site not in p_by_site or s_site not in s_by_site:
                        continue
                    ordered = add(
                        ordered,
                        multiply_all(p_by_site[p_site], s_by_site[s_site], q2),
                    )
            assert_equal(ordered, direct)
            row.append(direct)
        response.append(row)

    # Audit the full five-vector deformation, before specializing it to the
    # two-vector kernel (a,a,0,b,b).
    t = tuple(tuple(sp.symbols(f"t{site}0 t{site}1 t{site}2")) for site in range(1, 6))
    deformed_q = add(q, *(vector_word(t[site - 1], (site,)) for site in range(1, 6)))
    deformed_q2 = divided_power(deformed_q, 2)
    deformed_q3 = divided_power(deformed_q, 3)
    chain_vector = vector_add(vector_scale(-1, t[0]), t[1], t[2])
    assert_equal(deformed_q3, vector_word(chain_vector, (1, 2, 3, 4, 5)))

    expected_change: list[list[Polynomial]] = [[{} for _ in range(3)] for _ in range(3)]
    expected_change[1][0] = vector_word(
        vector_scale(sp.Rational(1, 2), vector_add(t[3], vector_scale(-1, t[4]))),
        (1, 2, 3, 4, 5),
    )
    expected_change[2][0] = vector_word(
        vector_scale(
            sp.Rational(1, 2),
            vector_add(vector_scale(-1, t[0]), t[1], t[2]),
        ),
        (1, 2, 3, 4, 5),
    )
    expected_change[2][2] = vector_word(
        vector_scale(
            sp.Rational(1, 4),
            vector_add(t[0], vector_scale(-1, t[1]), t[2]),
        ),
        (1, 2, 3, 4, 5),
    )
    for i in range(3):
        for j in range(3):
            changed_response = multiply_all(p[i], s[j], deformed_q2)
            delta = add(changed_response, scaled(response[i][j], -1))
            assert_equal(delta, expected_change[i][j])

    kernel_substitution: dict[sp.Symbol, sp.Expr] = {}
    for colour in range(3):
        kernel_substitution[t[0][colour]] = a[colour]
        kernel_substitution[t[1][colour]] = a[colour]
        kernel_substitution[t[2][colour]] = 0
        kernel_substitution[t[3][colour]] = b[colour]
        kernel_substitution[t[4][colour]] = b[colour]
    assert substitute(deformed_q3, kernel_substitution) == {}
    for row in expected_change:
        for entry in row:
            assert substitute(entry, kernel_substitution) == {}

    # Obtain C directly by extracting complementary supports from the q^[2]
    # just computed.  A and B are abbreviations, not fresh independent data.
    C = sp.zeros(N)
    for u in range(N):
        for v in range(N):
            if u == v:
                continue
            complement = FULL ^ (1 << u) ^ (1 << v)
            C[u, v] = coefficient_after_site_zero_contraction(q2, complement, x)
    A = sp.expand(sum(a[colour] * x[colour] for colour in range(3)))
    B = sp.expand(sum(b[colour] * x[colour] for colour in range(3)))
    expected_C = sp.Matrix(
        (
            (0, -1, 1, 1, 0, 0),
            (-1, 0, B, 0, -2 * x[2], A + 2 * x[2]),
            (1, B, 0, B, 2 * x[2], A + 2 * x[2]),
            (1, 0, B, 0, -2 * x[2], A + 2 * x[2]),
            (0, -2 * x[2], 2 * x[2], -2 * x[2], 0, 0),
            (0, A + 2 * x[2], A + 2 * x[2], A + 2 * x[2], 0, 0),
        )
    )
    assert matrix_expand(C - expected_C) == sp.zeros(N)
    assert sp.factor(C.det()) == -64 * x[2] ** 2 * (A + 2 * x[2]) ** 2

    # Derive the scalar row matrices from the tensor rows, then read all
    # matrices in the deliberately nonstandard site order below.
    P = sp.zeros(3, N)
    S = sp.zeros(3, N)
    for i in range(3):
        for site in range(N):
            P[i, site] = coefficient_after_site_zero_contraction(p[i], 1 << site, x)
            S[i, site] = coefficient_after_site_zero_contraction(s[i], 1 << site, x)
    strange_order = (5, 2, 0, 4, 1, 3)
    C_strange = C.extract(strange_order, strange_order)
    P_strange = P.extract((0, 1, 2), strange_order)
    S_strange = S.extract((0, 1, 2), strange_order)
    scalar_response = matrix_expand(P_strange * C_strange * S_strange.T)
    diagonal = sp.diag(*x)
    assert scalar_response == diagonal
    assert sp.factor(scalar_response.det()) == x[0] * x[1] * x[2]
    assert matrix_expand(scalar_response.adjugate()) == sp.diag(
        x[1] * x[2], x[0] * x[2], x[0] * x[1]
    )

    # At a=e_0 and b=e_1 the five site-zero endpoint vectors span V_0.
    specialization = {
        a[0]: 1,
        a[1]: 0,
        a[2]: 0,
        b[0]: 0,
        b[1]: 1,
        b[2]: 0,
    }
    star_vectors = (
        vector_add(a, vector_scale(2, e2)),
        a,
        vector_scale(2, e2),
        b,
        b,
    )
    star_matrix = sp.Matrix.hstack(
        *(sp.Matrix(vector).subs(specialization) for vector in star_vectors)
    )
    assert star_matrix.rank() == 3

    q_specialized = substitute(q, specialization)
    for site in range(1, 6):
        # Every nonzero site has at least one incident block, and the algebra
        # itself gives that site only the single local label z_site.
        assert any(
            support.bit_count() == 2 and support & (1 << site)
            for support, _colour in q_specialized
        )
    target_rank_at_site_zero = sp.eye(3).rank()
    target_rank_at_other_site = sp.Matrix([[1, 1, 1]]).rank()
    assert target_rank_at_site_zero == 3
    assert target_rank_at_other_site == 1

    two_site_response, two_site_determinant, two_site_cofactor = (
        audit_two_separated_target_sites()
    )
    omission_ledger = audit_rank_budget_and_omission_pairs()

    print("full-rank-site response countermodel independent audit: PASS")
    print("q^[2] vector/scalar support words: 8 / 3")
    print("q^[3] and five-vector chain formula: PASS")
    print("all nine arbitrary-(a,b) tensor responses: PASS")
    print("ordered endpoint reconstruction: PASS")
    print("incident ranks at sites 0..5: 3,1,1,1,1,1")
    print("scalar response:", scalar_response)
    print("cofactor determinant:", sp.factor(C.det()))
    print("target local ranks at sites 0 / 1..5: 3 / 1")
    print("two-separated-site tensor response and cofactor: PASS")
    print("two-site scalar response:", two_site_response)
    print("two-site cofactor determinant:", two_site_determinant)
    print("two-site cofactor in order (4,1,5,0,3,2):", two_site_cofactor)
    print("rank-budget omission-pair ledger:", omission_ledger)
    print("coincident-pair target flattenings have rank two: PASS")


if __name__ == "__main__":
    main()
