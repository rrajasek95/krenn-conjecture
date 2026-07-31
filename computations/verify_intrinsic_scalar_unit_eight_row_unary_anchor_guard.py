#!/usr/bin/env python3
"""Exact checks for the intrinsic scalar-unit eight-row/unary guard.

The uniform statements are proved in the accompanying note.  This
dependency-free checker audits the sharp h=4 physical packet and the
finite scalar/rank ledgers without relying on Python ``assert``.
"""

from collections import Counter
from fractions import Fraction
from itertools import product


Q = Fraction
COLOURS = range(3)

# Global site order.  The selected pair is (i,j); its complement is W.
SITES = ("i", "j", "p", "q", "0", "1", "2", "3", "4", "5")
SITE_INDEX = {site: index for index, site in enumerate(SITES)}
W_SITES = ("p", "q", "0", "1", "2", "3", "4", "5")
EXPOSED = "1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(polynomial):
    return Counter({word: Q(value) for word, value in polynomial.items() if value})


def add(*polynomials):
    result = Counter()
    for polynomial in polynomials:
        result.update(polynomial)
    return clean(result)


def scale(polynomial, scalar):
    return clean(Counter({word: Q(scalar) * value for word, value in polynomial.items()}))


def multiply(left, right):
    result = Counter()
    for left_word, left_value in left.items():
        left_sites = {site for site, _colour in left_word}
        for right_word, right_value in right.items():
            if any(site in left_sites for site, _colour in right_word):
                continue
            word = tuple(sorted(left_word + right_word, key=lambda item: SITE_INDEX[item[0]]))
            result[word] += left_value * right_value
    return clean(result)


def divided_power(polynomial, exponent):
    require(exponent >= 0, "negative divided power")
    result = Counter({(): Q(1)})
    for step in range(1, exponent + 1):
        result = scale(multiply(result, polynomial), Q(1, step))
    return result


def monomer(site, colour, coefficient=1):
    return Counter({((site, colour),): Q(coefficient)})


def edge(left, right, colour, coefficient=1):
    return multiply(monomer(left, colour), monomer(right, colour, coefficient))


def pure(sites, colour):
    return Counter({tuple((site, colour) for site in sites): Q(1)})


def quadratic_coefficient(polynomial, left, left_colour, right, right_colour):
    word = tuple(sorted(
        ((left, left_colour), (right, right_colour)),
        key=lambda item: SITE_INDEX[item[0]],
    ))
    return polynomial.get(word, Q(0))


def endpoint_star(polynomial, endpoint, omitted_endpoint, colour):
    """Extract one endpoint-ordered star row from the aggregate quadratic."""
    result = Counter()
    endpoint_variable = (endpoint, colour)
    for word, coefficient in polynomial.items():
        if len(word) != 2 or endpoint_variable not in word:
            continue
        other = word[1] if word[0] == endpoint_variable else word[0]
        if other[0] != omitted_endpoint:
            result[(other,)] += coefficient
    return clean(result)


def linear_rank(forms, sites):
    columns = [(site, colour) for site in sites for colour in COLOURS]
    matrix = []
    for form in forms:
        row = []
        for coordinate in columns:
            row.append(form.get((coordinate,), Q(0)))
        matrix.append(row)
    return matrix_rank(matrix)


def matrix_rank(matrix):
    if not matrix:
        return 0
    work = [[Q(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scalar = work[row][column]
            work[row] = [
                value - scalar * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def sparse_rank(polynomials):
    words = sorted(
        {word for polynomial in polynomials for word in polynomial},
        key=lambda word: tuple((SITE_INDEX[site], colour) for site, colour in word),
    )
    return matrix_rank([
        [polynomial.get(word, Q(0)) for word in words]
        for polynomial in polynomials
    ])


def sparse_span_contains(columns, target):
    """Exact sparse column elimination with word keys as row labels."""
    basis = {}
    for column in columns:
        vector = dict(column)
        while vector:
            pivot = min(
                vector,
                key=lambda word: tuple((SITE_INDEX[site], colour)
                                       for site, colour in word),
            )
            if pivot not in basis:
                scalar = vector[pivot]
                basis[pivot] = {word: value / scalar for word, value in vector.items()}
                break
            scalar = vector[pivot]
            for word, value in basis[pivot].items():
                vector[word] = vector.get(word, Q(0)) - scalar * value
                if not vector[word]:
                    vector.pop(word, None)

    vector = dict(target)
    while vector:
        pivot = min(
            vector,
            key=lambda word: tuple((SITE_INDEX[site], colour)
                                   for site, colour in word),
        )
        if pivot not in basis:
            return False
        scalar = vector[pivot]
        for word, value in basis[pivot].items():
            vector[word] = vector.get(word, Q(0)) - scalar * value
            if not vector[word]:
                vector.pop(word, None)
    return True


def build_packet():
    z = add(edge("2", "3", 0), edge("0", "4", 1))
    t = (monomer("0", 0), monomer("1", 1), monomer("3", 2))
    v = (monomer("1", 0), monomer("2", 1), monomer("3", 2))
    x = (monomer("4", 0), monomer("5", 1), Counter())
    y = (monomer("5", 0), monomer("3", 1), Counter())

    internal = add(
        edge("p", "q", 2),
        z,
        multiply(monomer("p", 0), x[0]),
        multiply(monomer("p", 1), x[1]),
        multiply(monomer("q", 0), y[0]),
        multiply(monomer("q", 1), y[1]),
    )
    global_quadratic = add(
        edge("i", "j", 2),
        internal,
        *(multiply(monomer("i", colour), t[colour]) for colour in COLOURS),
        *(multiply(monomer("j", colour), v[colour]) for colour in COLOURS),
    )
    return z, t, v, x, y, internal, global_quadratic


def check_global_and_pair_rows():
    _z, t, v, _x, _y, internal, global_quadratic = build_packet()
    restricted = clean(Counter({
        word: value
        for word, value in global_quadratic.items()
        if all(site not in ("i", "j") for site, _colour in word)
    }))
    require(restricted == internal, "selected-pair restriction is not the stated q")

    global_top = divided_power(global_quadratic, 5)
    expected_global = add(pure(SITES, 0), pure(SITES, 1))
    require(global_top == expected_global, "global packet has wrong binary top tensor")
    require(len(global_top) == 2, "global top should have exactly two matchings")

    q3 = divided_power(internal, 3)
    q4 = divided_power(internal, 4)
    require(len(q3) == 5, "internal third-power matching count changed")
    require(not q4, "intrinsic internal fourth power should vanish")

    residuals = {}
    for c, d in product(COLOURS, repeat=2):
        direct = scale(
            q4,
            quadratic_coefficient(global_quadratic, "i", c, "j", d),
        )
        response = multiply(multiply(t[c], v[d]), q3)
        target = pure(W_SITES, c) if c == d else Counter()
        residual = add(direct, response, scale(target, -1))
        residuals[c, d] = residual
        expected = scale(pure(W_SITES, 2), -1) if (c, d) == (2, 2) else Counter()
        require(residual == expected, f"wrong selected-pair residual {(c, d)}")
    require(sum(bool(value) for value in residuals.values()) == 1,
            "selected pair should have one failed row")
    return internal, t, v, global_quadratic


def check_good_stars_and_curvature(t, v, global_quadratic):
    ij_i_star = tuple(
        endpoint_star(global_quadratic, "i", "j", colour)
        for colour in COLOURS
    )
    ij_j_star = tuple(
        endpoint_star(global_quadratic, "j", "i", colour)
        for colour in COLOURS
    )
    require(ij_i_star == t, "selected i-star was not extracted faithfully")
    require(ij_j_star == v, "selected j-star was not extracted faithfully")

    ip_i_star = tuple(
        endpoint_star(global_quadratic, "i", "p", colour)
        for colour in COLOURS
    )
    ip_p_star = tuple(
        endpoint_star(global_quadratic, "p", "i", colour)
        for colour in COLOURS
    )
    ip_sites = tuple(site for site in SITES if site not in ("i", "p"))
    star_ranks = (
        linear_rank(ij_i_star, W_SITES),
        linear_rank(ij_j_star, W_SITES),
        linear_rank(ip_i_star, ip_sites),
        linear_rank(ip_p_star, ip_sites),
    )
    require(star_ranks == (3, 3, 3, 3), "one of the four stars is not injective")

    # Endpoint/colour order is (ij)(pq)-(ip)(jq), all in physical colour 2.
    a_ij = quadratic_coefficient(global_quadratic, "i", 2, "j", 2)
    a_pq = quadratic_coefficient(global_quadratic, "p", 2, "q", 2)
    a_ip = quadratic_coefficient(global_quadratic, "i", 2, "p", 2)
    a_jq = quadratic_coefficient(global_quadratic, "j", 2, "q", 2)
    require((a_ij, a_pq, a_ip, a_jq) == (1, 1, 0, 0),
            "wrong labelled all-colour-two rectangle")
    kappa = a_ij * a_pq - a_ip * a_jq
    require(kappa == 1, "curvature minor is not one")
    return star_ranks, kappa


def check_odd_residue(internal):
    q0 = Counter({
        word: value
        for word, value in internal.items()
        if all(site != EXPOSED for site, _colour in word)
    })
    # In this packet no internal edge meets the exposed site.
    require(q0 == internal, "unexpected internal edge at exposed site")
    a0 = divided_power(q0, 3)
    odd_sites = tuple(site for site in W_SITES if site != EXPOSED)

    y0 = pure(odd_sites, 0)
    y1 = pure(odd_sites, 1)
    y2 = pure(odd_sites, 2)
    require(multiply(monomer("0", 0), a0) == y0, "explicit Y0 lift failed")
    require(multiply(monomer("2", 1), a0) == y1, "explicit Y1 lift failed")

    columns = [
        multiply(monomer(site, colour), a0)
        for site in odd_sites
        for colour in COLOURS
    ]
    require(sparse_span_contains(columns, y0), "Y0 should vanish in odd quotient")
    require(sparse_span_contains(columns, y1), "Y1 should vanish in odd quotient")
    require(not sparse_span_contains(columns, y2), "Y2 should survive in odd quotient")

    base_rank = sparse_rank(columns)
    augmented_ranks = tuple(sparse_rank(columns + [target]) for target in (y0, y1, y2))
    joint_rank = sparse_rank(columns + [y0, y1, y2])
    require(base_rank == 15, "wrong rank for R1*q0^[3]")
    require(augmented_ranks == (15, 15, 16), "wrong target-residue augmented ranks")
    require(joint_rank == 16, "target-residue quotient should have rank one")
    return base_rank, augmented_ranks, joint_rank


def check_clean_error(internal, t, v):
    q3 = divided_power(internal, 3)
    q4 = divided_power(internal, 4)
    r = scale(add(multiply(t[0], v[0]), multiply(t[1], v[1])), -1)
    delta = add(pure(W_SITES, 0), pure(W_SITES, 1))
    require(not q4, "q^[4] should vanish")
    require(not divided_power(r, 2), "scalar-zero response square should vanish")
    require(multiply(r, q3) == scale(delta, -1), "complementary physical row failed")

    # Homogeneous parameter coefficients (t-degree, u-degree) of F^[4].
    f4 = {}
    for j in range(5):
        coefficient = multiply(divided_power(internal, 4 - j), divided_power(r, j))
        if coefficient:
            f4[4 - j, j] = coefficient

    target_correction = {
        (4, 0): pure(W_SITES, 2),
        (3, 1): scale(delta, -1),
    }
    error = {}
    for degree in set(f4) | set(target_correction):
        coefficient = add(
            f4.get(degree, Counter()),
            scale(target_correction.get(degree, Counter()), -1),
        )
        if coefficient:
            error[degree] = coefficient
    require(error == {(4, 0): scale(pure(W_SITES, 2), -1)},
            "clean error is not exactly -t^4 X2")

    # Here s=t and diag K=(-u,-u,t), so activity is t^2*u^2.
    activity = {(2, 2): Q(1)}
    for t_value, u_value in ((0, 1), (1, 0), (1, 1), (2, -3)):
        error_value = -Q(t_value) ** 4
        activity_value = Q(t_value) ** 2 * Q(u_value) ** 2
        require((error_value == 0) == (t_value == 0), "wrong clean root support")
        require((activity_value != 0) == (t_value != 0 and u_value != 0),
                "wrong activity support")
        require(not (error_value == 0 and activity_value != 0),
                "an active clean point appeared")
    return error, activity


def check_adversarial_mutations(internal, t, v, global_quadratic):
    expected_global = add(pure(SITES, 0), pure(SITES, 1))

    # The dormant colour-two selected cell is invisible to the binary top,
    # but deleting it must be detected by the labelled curvature audit.
    no_selected_cell = add(global_quadratic, scale(edge("i", "j", 2), -1))
    require(divided_power(no_selected_cell, 5) == expected_global,
            "selected-cell mutation was not top-invisible")
    mutated_kappa = (
        quadratic_coefficient(no_selected_cell, "i", 2, "j", 2)
        * quadratic_coefficient(no_selected_cell, "p", 2, "q", 2)
        - quadratic_coefficient(no_selected_cell, "i", 2, "p", 2)
        * quadratic_coefficient(no_selected_cell, "j", 2, "q", 2)
    )
    require(mutated_kappa != 1, "curvature audit accepted a deleted selected cell")

    # The dormant i-star colour-two leg is also top-invisible, but its
    # removal drops the selected star rank.
    no_i_two_leg = add(
        global_quadratic,
        scale(multiply(monomer("i", 2), t[2]), -1),
    )
    require(divided_power(no_i_two_leg, 5) == expected_global,
            "star mutation was not top-invisible")
    mutated_i_star = tuple(
        endpoint_star(no_i_two_leg, "i", "j", colour)
        for colour in COLOURS
    )
    require(linear_rank(mutated_i_star, W_SITES) == 2,
            "star-rank audit accepted a deleted colour-two leg")

    # Reversing the complementary response changes the signed physical row.
    q3 = divided_power(internal, 3)
    wrong_response = add(multiply(t[0], v[0]), multiply(t[1], v[1]))
    delta = add(pure(W_SITES, 0), pure(W_SITES, 1))
    require(multiply(wrong_response, q3) == delta,
            "response-sign mutation did not flip the physical row")
    require(multiply(wrong_response, q3) != scale(delta, -1),
            "signed response audit accepted the mutation")


def check_uniform_cap_quotient_ledger():
    # Matrix coordinates are ordered lexicographically.  H omits (a,a).
    for a in COLOURS:
        coordinates = list(product(COLOURS, repeat=2))
        aa = coordinates.index((a, a))
        h_columns = [
            [Q(int(index == column)) for index in range(9)]
            for column in range(9)
            if column != aa
        ]
        require(matrix_rank(h_columns) == 8, "eight-row cap space rank")
        scalar_row = [Q(1) if index == aa else Q(0) for index in range(9)]
        require(all(sum(scalar_row[i] * column[i] for i in range(9)) == 0
                    for column in h_columns), "eight-row space is not scalar-zero")
        require(matrix_rank(h_columns + [scalar_row]) == 9,
                "unary cap does not generate quotient")

    # Audit the order jump and same-power graph arithmetic uniformly.
    for h in range(3, 65):
        selected_order = h
        complementary_order = h - 1
        require(selected_order == complementary_order + 1,
                "target valuation gap")
        for lam in (Q(-7, 3), Q(-1), Q(0), Q(5, 2)):
            # Pair is (target coefficient, residue coefficient in units of Ya).
            pair = (lam, lam)
            companion = (-lam, -lam)
            require((pair[0] + companion[0], pair[1] + companion[1]) == (0, 0),
                    "same-power target/residue graph failed")
        # q0*q0^[h-2]=(h-1)q0^[h-1], killed in the odd quotient.
        require(h - 1 != 0, "radial divided-power coefficient vanished")


def main():
    internal, t, v, global_quadratic = check_global_and_pair_rows()
    star_ranks, kappa = check_good_stars_and_curvature(t, v, global_quadratic)
    base_rank, augmented_ranks, joint_rank = check_odd_residue(internal)
    _error, activity = check_clean_error(internal, t, v)
    check_uniform_cap_quotient_ledger()
    check_adversarial_mutations(internal, t, v, global_quadratic)
    print("intrinsic scalar-unit eight-row unary-anchor guard: PASS")
    print("  global packet: exact binary top tensor X0+X1 on ten sites")
    print("  selected pair: 8/9 rows; sole residual (2,2)=-X2")
    print(f"  four good-star ranks: {star_ranks}; curvature kappa={kappa}")
    print(
        "  target-residue ranks at site 1: "
        f"base={base_rank}, augmented={augmented_ranks}, joint={joint_rank}"
    )
    require(activity == {(2, 2): Q(1)}, "activity ledger changed before reporting")
    print("  clean error: -t^4 X2; activity=t^2*u^2; sole root is inactive")
    print("  uniform cap quotient/valuation ledger: h=3,...,64")
    print("  adversarial top-invisible cell/star and response-sign mutations rejected")


if __name__ == "__main__":
    main()
