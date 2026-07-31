#!/usr/bin/env python3
"""Exact audits for physical scalar-unit target-jet constraints.

The companion note proves the uniform carrier-factorization/localization
statement.  This dependency-free checker works in the literal
site-square-zero algebra over ``Fraction`` and verifies two minimal h=3
guards:

* an eight-of-nine-row clean guard whose sole failed row is ``(c,c)``;
* a clean exceptional-row guard with a rank-two physical target jet.

All failures are explicit, so ``python -O`` leaves every check active.
"""

from fractions import Fraction
from itertools import product
from math import factorial


F = Fraction
SITES = tuple(range(6))
LABELS = (0, 1, 2)
A, B, C = LABELS


def require(condition, message):
    """Raise explicitly under normal and optimized Python."""

    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            answer[monomial] = answer.get(monomial, F(0)) + coefficient
    return clean(answer)


def scale(poly, coefficient):
    coefficient = F(coefficient)
    return clean({monomial: coefficient * value
                  for monomial, value in poly.items()})


def neg(poly):
    return scale(poly, -1)


def mul(left, right):
    """Multiply in the commutative algebra with each physical site square zero."""

    answer = {}
    for left_monomial, left_coefficient in left.items():
        left_sites = {site for site, _colour in left_monomial}
        for right_monomial, right_coefficient in right.items():
            right_sites = {site for site, _colour in right_monomial}
            if left_sites & right_sites:
                continue
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, F(0))
                + left_coefficient * right_coefficient
            )
    return clean(answer)


def product_poly(*polys):
    answer = {(): F(1)}
    for poly in polys:
        answer = mul(answer, poly)
    return answer


def power(poly, exponent):
    require(exponent >= 0, "negative power")
    answer = {(): F(1)}
    for _ in range(exponent):
        answer = mul(answer, poly)
    return answer


def divided_power(poly, exponent):
    return scale(power(poly, exponent), F(1, factorial(exponent)))


def coordinate(site, colour, coefficient=1):
    coefficient = F(coefficient)
    if not coefficient:
        return {}
    return {((site, colour),): coefficient}


def cell(left_site, left_colour, right_site, right_colour, coefficient=1):
    return scale(
        mul(coordinate(left_site, left_colour),
            coordinate(right_site, right_colour)),
        coefficient,
    )


def target(colour):
    return product_poly(*(coordinate(site, colour) for site in SITES))


TARGETS = tuple(target(colour) for colour in LABELS)


def rank(rows):
    work = [list(map(F, row)) for row in rows]
    if not work:
        return 0
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged rank matrix")
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work))
             if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [entry / divisor for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                x - multiplier * y
                for x, y in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


COORDINATES = tuple((site, colour)
                    for site in SITES for colour in LABELS)


def linear_vector(linear):
    return [linear.get((coordinate_key,), F(0))
            for coordinate_key in COORDINATES]


def star_rank(stars):
    return rank([linear_vector(stars[label]) for label in LABELS])


def response_table(p_stars, s_stars):
    return {
        (i, j): mul(p_stars[i], s_stars[j])
        for i, j in product(LABELS, repeat=2)
    }


def target_matrix(packet, colour, complement=(B, C)):
    target_monomial = next(iter(TARGETS[colour]))
    return [
        [packet[i, j].get(target_monomial, F(0)) for j in complement]
        for i in complement
    ]


def matrix_rank_2(matrix):
    return rank(matrix)


def determinant_2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def require_target_only(packet, name):
    target_monomials = {next(iter(value)) for value in TARGETS}
    for key, value in packet.items():
        impure = [monomial for monomial in value
                  if monomial not in target_monomials]
        require(not impure, f"{name} {key} has an impure top word")


def linear_terms(linear):
    for monomial, coefficient_value in linear.items():
        require(len(monomial) == 1, "expected a one-site linear form")
        yield monomial[0], coefficient_value


def localized_four_star_sum(pj, sa, pa, sk, carrier, top_word):
    """Expand one coefficient before the four-star carrier is contracted."""

    total = F(0)
    nonzero_terms = []
    for x, px in linear_terms(pj):
        for y, sy in linear_terms(sa):
            for z, pz in linear_terms(pa):
                for w, sw in linear_terms(sk):
                    if len({x[0], y[0], z[0], w[0]}) != 4:
                        continue
                    stars = tuple(sorted((x, y, z, w)))
                    star_sites = {site for site, _colour in stars}
                    for carrier_monomial, carrier_coefficient in carrier.items():
                        if star_sites & {site for site, _colour in carrier_monomial}:
                            continue
                        if tuple(sorted(stars + carrier_monomial)) != top_word:
                            continue
                        term = px * sy * pz * sw * carrier_coefficient
                        total += term
                        if term:
                            nonzero_terms.append((stars, carrier_monomial, term))
    return total, nonzero_terms


def audit_segre_and_localization(p_stars, s_stars, carrier, packet, keys):
    responses = response_table(p_stars, s_stars)
    selected = A
    for i, j in product(LABELS, repeat=2):
        require(
            mul(responses[i, j], responses[selected, selected])
            == mul(responses[i, selected], responses[selected, j]),
            f"Segre square failed at {(i, j)}",
        )

    top_word = next(iter(TARGETS[B]))
    for key in keys:
        i, j = key
        expected = packet[key].get(top_word, F(0))
        total, terms = localized_four_star_sum(
            p_stars[i], s_stars[A], p_stars[A], s_stars[j],
            carrier, top_word,
        )
        require(total == expected, f"localized sum mismatch at {key}")
        require(expected and terms, f"no nonzero localized term at {key}")
        require(
            all(len({site for site, _colour in stars}) == 4
                for stars, _carrier_monomial, _term in terms),
            f"site collision survived localization at {key}",
        )


def eight_row_guard():
    """Audit the clean good-star guard missing exactly the (c,c) row."""

    q = add(
        cell(0, A, 1, A),
        cell(2, A, 3, A),
        cell(4, A, 5, A),
        cell(1, B, 4, B),
        cell(3, B, 5, B),
    )
    p_stars = {
        A: coordinate(1, B),
        B: coordinate(0, B),
        C: coordinate(1, C),
    }
    s_stars = {
        A: coordinate(4, B),
        B: coordinate(2, B),
        C: coordinate(3, C),
    }
    responses = response_table(p_stars, s_stars)
    r = responses[A, A]
    g = add(q, r)

    require(star_rank(p_stars) == 3, "left stars are not good")
    require(star_rank(s_stars) == 3, "right stars are not good")
    require(divided_power(q, 3) == TARGETS[A], "guard q^[3] is wrong")
    require(mul(r, divided_power(q, 2)) == {}, "exceptional response is nonzero")
    require(divided_power(g, 3) == TARGETS[A], "unary cap is not clean")

    theta = add(divided_power(g, 2), neg(divided_power(q, 2)))
    carrier = add(q, scale(r, F(1, 2)))
    require(theta == mul(r, carrier), "Theta != R_aa H_a")
    require(theta == mul(r, q), "square-zero simplification of Theta failed")

    passed = []
    failed = []
    for i, j in product(LABELS, repeat=2):
        left = mul(responses[i, j], divided_power(q, 2))
        if (i, j) == (A, A):
            left = add(divided_power(q, 3), left)
        right = TARGETS[i] if i == j else {}
        if left == right:
            passed.append((i, j))
        else:
            failed.append(((i, j), add(left, neg(right))))
    require(
        passed == [(A, A), (A, B), (A, C), (B, A),
                   (B, B), (B, C), (C, A), (C, B)],
        "the eight-row pass list changed",
    )
    require(
        failed == [((C, C), neg(TARGETS[C]))],
        "the sole failed row is not exactly 0 = X_c",
    )

    complement = (B, C)
    z_packet = {
        (i, j): mul(responses[i, j], theta)
        for i, j in product(complement, repeat=2)
    }
    require_target_only(z_packet, "eight-row Z")
    require(z_packet[B, B] == TARGETS[B], "wrong surviving eight-row jet")
    require(
        all(z_packet[key] == {} for key in ((B, C), (C, B), (C, C))),
        "an unintended eight-row jet entry survived",
    )

    transformed = {
        (i, j): mul(responses[i, j], divided_power(g, 2))
        for i, j in product(complement, repeat=2)
    }
    require_target_only(transformed, "eight-row transformed response")
    require(transformed[B, B] == scale(TARGETS[B], 2), "wrong doubled b row")
    require(
        all(transformed[key] == {}
            for key in ((B, C), (C, B), (C, C))),
        "unexpected transformed complementary entry",
    )

    matrices = tuple(target_matrix(transformed, colour) for colour in LABELS)
    require(matrix_rank_2(matrices[A]) == 0, "A_a should vanish")
    require(matrix_rank_2(matrices[B]) == 1, "A_b should have rank one")
    require(matrix_rank_2(matrices[C]) == 0, "A_c should have rank zero")
    require(
        determinant_2([[matrices[B][i][j] + matrices[C][i][j]
                        for j in range(2)] for i in range(2)]) == 0,
        "nonabsorbable determinant unexpectedly became nonzero",
    )

    audit_segre_and_localization(
        p_stars, s_stars, carrier, z_packet, ((B, B),),
    )
    return passed, failed, matrices


def rank_two_guard():
    """Audit a physical rank-two target jet with clean unary and aa row."""

    q = add(
        cell(0, A, 1, A),
        cell(2, A, 3, A),
        cell(4, A, 5, A),
        cell(0, B, 5, B, -2),
        cell(2, B, 5, B),
        cell(3, B, 5, B),
    )
    p_stars = {
        A: coordinate(1, B, -1),
        B: coordinate(0, B),
        C: coordinate(4, B),
    }
    s_stars = {
        A: coordinate(3, B),
        B: coordinate(0, B),
        C: coordinate(4, B),
    }
    responses = response_table(p_stars, s_stars)
    r = responses[A, A]
    g = add(q, r)

    require(star_rank(p_stars) == 3, "rank-two left stars are not good")
    require(star_rank(s_stars) == 3, "rank-two right stars are not good")
    require(divided_power(q, 3) == TARGETS[A], "rank-two q^[3] is wrong")
    require(mul(r, divided_power(q, 2)) == {}, "rank-two aa response is nonzero")
    require(divided_power(g, 3) == TARGETS[A], "rank-two unary cap is not clean")

    theta = add(divided_power(g, 2), neg(divided_power(q, 2)))
    carrier = add(q, scale(r, F(1, 2)))
    require(theta == mul(r, carrier), "rank-two Theta factorization failed")
    require(theta == mul(r, q), "rank-two R^[2] should vanish")

    complement = (B, C)
    z_packet = {
        (i, j): mul(responses[i, j], theta)
        for i, j in product(complement, repeat=2)
    }
    require_target_only(z_packet, "rank-two Z")
    require(z_packet[B, C] == neg(TARGETS[B]), "wrong bc rank-two jet")
    require(z_packet[C, B] == neg(TARGETS[B]), "wrong cb rank-two jet")
    require(z_packet[B, B] == z_packet[C, C] == {}, "rank-two diagonal survived")

    transformed = {
        (i, j): mul(responses[i, j], divided_power(g, 2))
        for i, j in product(complement, repeat=2)
    }
    require(transformed == z_packet, "rank-two transformed packet changed")
    matrix_b = target_matrix(transformed, B)
    require(matrix_b == [[F(0), F(-1)], [F(-1), F(0)]],
            "wrong physical rank-two coefficient matrix")
    require(matrix_rank_2(matrix_b) == 2, "physical target jet lost rank two")
    require(determinant_2(matrix_b) == -1, "wrong rank-two determinant")

    # The exceptional full-nine row is exact, although the other rows are
    # deliberately not asserted in this weaker guard.
    require(
        add(divided_power(q, 3),
            mul(responses[A, A], divided_power(q, 2))) == TARGETS[A],
        "rank-two exceptional row failed",
    )
    audit_segre_and_localization(
        p_stars, s_stars, carrier, z_packet, ((B, C), (C, B)),
    )
    return matrix_b


def mutation_checks():
    """Reject the two normalizations most likely to be silently altered."""

    # Use a carrier with nonzero square here; both main guards deliberately
    # use a one-cell R, on which the 1/2 coefficient is invisible after
    # multiplication by R.
    p = add(coordinate(0, B), coordinate(2, B))
    s = add(coordinate(1, B), coordinate(3, B))
    r_test = mul(p, s)
    theta_test = divided_power(r_test, 2)
    require(
        theta_test == mul(r_test, scale(r_test, F(1, 2))),
        "correct H coefficient failed on the mutation packet",
    )
    require(
        theta_test != mul(r_test, r_test),
        "wrong H coefficient survived",
    )

    q = add(
        cell(0, A, 1, A), cell(2, A, 3, A), cell(4, A, 5, A),
        cell(1, B, 4, B), cell(3, B, 5, B),
    )
    r = cell(1, B, 4, B)
    wrong_direct_row = add(scale(divided_power(q, 3), 2),
                           mul(r, divided_power(q, 2)))
    require(wrong_direct_row != TARGETS[A], "direct-row coefficient mutation survived")


def main():
    passed, failed, matrices = eight_row_guard()
    matrix_b = rank_two_guard()
    mutation_checks()
    require(len(passed) == 8 and len(failed) == 1, "row census mutation")
    require(matrix_rank_2(matrix_b) == 2, "final rank-two mutation")
    require(matrix_rank_2(matrices[C]) == 0, "final eight-row mutation")
    print(
        "scalar-unit physical target-jet constraints: PASS; "
        "h=3 eight-of-nine clean good-star guard has sole residual -X_c; "
        "rank-two physical jet det=-1; four-site carrier localization exact"
    )


if __name__ == "__main__":
    main()
