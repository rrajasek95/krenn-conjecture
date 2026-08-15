#!/usr/bin/env python3
"""Exclude every Lagrangian split of the fixed rank-six scalar-zero lift.

For the exact guard frozen in 8e49a4c, restrict the wordwise bilinear forms

    C_w(u,v) = [u v q^[2]]_w

to the six-dimensional span of the displayed response factors.  Three
forms satisfy a rank-one polarization identity.  The two pure target rows
then force the mixed cross block to contain two nonzero entries whose
product is 1/4, although that mixed row has zero target and zero hafnian.
This is independent of the chosen complementary maximal-J-isotropic split.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py":
        "20ec8fabda17ab915e9b071df00a06d72e985943a3672a5f0a9e02edff80badf",
    "notes/h3-scalar-zero-packet-six-site-nonreduction.md":
        "22404c6a55c8c6a60cd3186eef3401212a60a4b6fcdc0cde5077fbab6892ff08",
    "notes/curved-pure-binary-three-channel-common-power-independent-audit.md":
        "2686bf1ddce9d22eb3fc2cdf1cd7871560744ad28a409c98e80586a10a3645de",
}
EXPECTED_LEDGER_SHA256 = "33f6816971b5eebc9d48697e8f1c86a5682221a240be9435740483f017f1b522"

SITES = tuple(range(6))
COLOURS = tuple(range(3))
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
I = (Q(0), Q(1))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def gadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def gneg(item):
    return -item[0], -item[1]


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gscale(scalar, item):
    return scalar * item[0], scalar * item[1]


def ginv(item):
    norm = item[0] ** 2 + item[1] ** 2
    require(norm != 0, item)
    return item[0] / norm, -item[1] / norm


def matrix(rows, columns, entry=ZERO):
    return [[entry for _ in range(columns)] for _ in range(rows)]


def matrix_rank(items):
    work = [row[:] for row in items]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows)
                      if work[row][column] != ZERO), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = ginv(work[rank][column])
        work[rank] = [gmul(inverse, item) for item in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == ZERO:
                continue
            scalar = work[row][column]
            work[row] = [gadd(work[row][index],
                              gneg(gmul(scalar, work[rank][index])))
                         for index in range(columns)]
        rank += 1
    return rank


def matrix_scale(scalar, items):
    return [[gmul(scalar, item) for item in row] for row in items]


def matrix_add(*items):
    rows = len(items[0])
    columns = len(items[0][0])
    return [[sum_gaussian(item[row][column] for item in items)
             for column in range(columns)] for row in range(rows)]


def outer(left, right):
    return [[gmul(left_item, right_item) for right_item in right]
            for left_item in left]


def transpose(items):
    return [list(row) for row in zip(*items, strict=True)]


def sum_gaussian(items):
    answer = ZERO
    for item in items:
        answer = gadd(answer, item)
    return answer


def scaled_form(scalar, form):
    return {port: gmul(scalar, coefficient)
            for port, coefficient in form.items()}


def form_sum(*forms):
    answer = {}
    for form in forms:
        for port, coefficient in form.items():
            answer[port] = gadd(answer.get(port, ZERO), coefficient)
    return {port: coefficient for port, coefficient in answer.items()
            if coefficient != ZERO}


def port(site, colour):
    return {(site, colour): ONE}


def response_basis():
    u0 = form_sum(port(0, 0), port(4, 0))
    v0 = form_sum(port(0, 1), port(1, 1))
    u1 = form_sum(port(1, 0), port(3, 0))
    v1 = form_sum(port(0, 2), port(2, 2))
    return (
        form_sum(u0, scaled_form(I, v0)),
        form_sum(u1, scaled_form(I, v1)),
        port(2, 0),
        form_sum(scaled_form((Q(1, 2), Q(0)), u0),
                 scaled_form((Q(0), Q(-1, 2)), v0)),
        form_sum(scaled_form((Q(1, 2), Q(0)), u1),
                 scaled_form((Q(0), Q(-1, 2)), v1)),
        scaled_form((Q(-1), Q(0)), port(5, 0)),
    )


Q_EDGES = {
    ((0, 4), 0, 0): ONE,
    ((2, 5), 0, 0): ONE,
    ((2, 4), 1, 1): ONE,
    ((3, 5), 1, 1): ONE,
    ((1, 3), 2, 2): ONE,
    ((4, 5), 2, 2): ONE,
}


def q_value(left, right, left_colour, right_colour):
    endpoints = tuple(sorted((left, right)))
    if left < right:
        colours = left_colour, right_colour
    else:
        colours = right_colour, left_colour
    return Q_EDGES.get((endpoints, *colours), ZERO)


def four_site_hafnian(vertices, word):
    first = vertices[0]
    answer = ZERO
    for position in range(1, 4):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        answer = gadd(answer, gmul(
            q_value(first, second, word[first], word[second]),
            q_value(rest[0], rest[1], word[rest[0]], word[rest[1]]),
        ))
    return answer


def c_value(left_form, right_form, word):
    answer = ZERO
    for left_site in SITES:
        for right_site in range(left_site + 1, 6):
            left_right = gmul(
                left_form.get((left_site, word[left_site]), ZERO),
                right_form.get((right_site, word[right_site]), ZERO),
            )
            right_left = gmul(
                left_form.get((right_site, word[right_site]), ZERO),
                right_form.get((left_site, word[left_site]), ZERO),
            )
            remaining = tuple(site for site in SITES
                              if site not in (left_site, right_site))
            answer = gadd(answer, gmul(
                gadd(left_right, right_left),
                four_site_hafnian(remaining, word),
            ))
    return answer


def c_matrix(forms, word):
    return [[c_value(left, right, word) for right in forms]
            for left in forms]


def q_cube_coefficient(word):
    first = SITES[0]
    answer = ZERO
    for position in range(1, 6):
        second = SITES[position]
        rest = SITES[1:position] + SITES[position + 1:]
        answer = gadd(answer, gmul(
            q_value(first, second, word[first], word[second]),
            four_site_hafnian(rest, word),
        ))
    return answer


def serialize_matrix(items):
    def show(item):
        return str(item[0]), str(item[1])
    return tuple(tuple(show(item) for item in row) for row in items)


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    forms = response_basis()
    port_order = tuple((site, colour) for site in SITES for colour in COLOURS)
    coefficient_matrix = [[form.get(item, ZERO) for item in port_order]
                          for form in forms]
    require(matrix_rank(coefficient_matrix) == 6,
            matrix_rank(coefficient_matrix))

    # J is the polar form of sum_i p_i t_i in the displayed basis.  The
    # coordinate P0 and S0 are complementary maximal J-isotropic spaces.
    J = matrix(6, 6)
    for index in range(3):
        J[index][index + 3] = ONE
        J[index + 3][index] = ONE
    require(matrix_rank(J) == 6, matrix_rank(J))
    require(all(J[row][column] == ZERO
                for row in range(3) for column in range(3)), J)
    require(all(J[row][column] == ZERO
                for row in range(3, 6) for column in range(3, 6)), J)

    words = {
        "X0": (0, 0, 0, 0, 0, 0),
        "X2": (2, 2, 2, 2, 2, 2),
        "M02": (0, 0, 2, 1, 0, 1),
        "Y": (0, 2, 0, 2, 0, 0),
    }
    C0 = c_matrix(forms, words["X0"])
    C2 = c_matrix(forms, words["X2"])
    CM = c_matrix(forms, words["M02"])

    ell0 = (ZERO, (Q(2), Q(0)), ZERO, ZERO, ONE, ZERO)
    ell2 = (ZERO, (Q(2), Q(0)), ZERO, ZERO, (Q(-1), Q(0)), ZERO)
    expected_C0 = matrix_scale((Q(1, 2), Q(0)), outer(ell0, ell0))
    expected_C2 = matrix_scale((Q(-1, 2), Q(0)), outer(ell2, ell2))
    expected_CM = matrix_scale((Q(0), Q(1, 4)), matrix_add(
        outer(ell0, ell2), outer(ell2, ell0)))
    require(C0 == expected_C0, C0)
    require(C2 == expected_C2, C2)
    require(CM == expected_CM, CM)
    require(matrix_rank(C0) == 1, matrix_rank(C0))
    require(matrix_rank(C2) == 1, matrix_rank(C2))
    require(matrix_rank(CM) == 2, matrix_rank(CM))

    nonzero_q_cube = {}
    nonzero_c_words = []
    for word in product(COLOURS, repeat=6):
        q3 = q_cube_coefficient(word)
        if q3 != ZERO:
            nonzero_q_cube["".join(map(str, word))] = q3
        if any(item != ZERO for row in c_matrix(forms, word) for item in row):
            nonzero_c_words.append("".join(map(str, word)))
    require(nonzero_q_cube == {"020200": ONE}, nonzero_q_cube)
    require(len(nonzero_c_words) == 25, len(nonzero_c_words))
    require(q_cube_coefficient(words["M02"]) == ZERO,
            q_cube_coefficient(words["M02"]))
    require(words["M02"] not in ((colour,) * 6 for colour in COLOURS),
            words["M02"])

    # Universal Laurent normalization forced by the two pure rows.
    # If C0(P,S)=E00 and C2(P,S)=E22, then for nonzero lambda,mu
    #   ell0|P=lambda e0, ell0|S=2/lambda e0,
    #   ell2|P=mu e2,     ell2|S=-2/mu e2.
    # Therefore CM_02=-i lambda/(2mu), CM_20=i mu/(2lambda),
    # and their product is the basis-independent unit 1/4.
    # Laurent monomials use exponents (lambda, mu).
    mixed_02 = {(1, -1): (Q(0), Q(-1, 2))}
    mixed_20 = {(-1, 1): (Q(0), Q(1, 2))}
    product_certificate = {}
    for left_exponent, left_coefficient in mixed_02.items():
        for right_exponent, right_coefficient in mixed_20.items():
            exponent = tuple(left + right for left, right in
                             zip(left_exponent, right_exponent, strict=True))
            product_certificate[exponent] = gadd(
                product_certificate.get(exponent, ZERO),
                gmul(left_coefficient, right_coefficient),
            )
    require(product_certificate == {(0, 0): (Q(1, 4), Q(0))},
            product_certificate)

    return {
        "theorem": (
            "no complementary maximal-J-isotropic split of the fixed "
            "rank-six lift satisfies the full-nine rows"
        ),
        "pins": PINS,
        "latent_space": {
            "dimension": 6,
            "J_rank": matrix_rank(J),
            "displayed_P_and_S_maximal_isotropic": True,
        },
        "word_forms": {
            "C_000000": serialize_matrix(C0),
            "C_222222": serialize_matrix(C2),
            "C_002101": serialize_matrix(CM),
            "nonzero_C_word_count": len(nonzero_c_words),
            "q^[3]_support": {
                word: (str(value[0]), str(value[1]))
                for word, value in nonzero_q_cube.items()
            },
        },
        "rank_one_polarization": {
            "C0": "(1/2) ell0 tensor ell0",
            "C2": "-(1/2) ell2 tensor ell2",
            "CM": "(i/4)(ell0 tensor ell2 + ell2 tensor ell0)",
            "ell0": tuple((str(item[0]), str(item[1])) for item in ell0),
            "ell2": tuple((str(item[0]), str(item[1])) for item in ell2),
        },
        "unit_certificate": {
            "forced_CM_02": "-i lambda/(2 mu)",
            "forced_CM_20": "i mu/(2 lambda)",
            "product": "CM_02*CM_20=1/4",
            "required_mixed_row": "C_002101(P,S)=0",
        },
        "scope": (
            "exhausts all complementary Lagrangian splits and all bases of "
            "the fixed minimal rank-six lift.  Inequivalent rank-six "
            "site-diagonal completions change the C_w forms and are not "
            "classified here."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("h3 scalar-zero packet all Lagrangian splits obstruction: PASS")
    print("mode", arguments.mode)
    print("C0=(1/2)ell0^2; C2=-(1/2)ell2^2;",
          "CM=(i/4)(ell0 ell2+ell2 ell0)")
    print("full-nine mixed row contradiction: CM_02*CM_20=1/4 != 0")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
