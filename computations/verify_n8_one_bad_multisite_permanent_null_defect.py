#!/usr/bin/env python3
"""Exact repeated-label defect of the one-bad permanent-null cap.

Put a=p1, b=p2, c=s1, d=s2 and

    R = ac + ad - bc + bd = a(c+d) + b(d-c).

For arbitrary multi-site one-forms the permanent-zero cancellation removes
only the abcd sector of R^[2].  This checker verifies the complete formal
R^[2], R^[3] formulas and a literal six-site common-q^[2] response packet
where one response-invisible extra p1 component creates a nonzero R^[2]q
defect.  The extra component is removable, so the packet is a guard to an
activity/minimality-free argument, not a counterexample to the normalized
one-bad branch.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_direct_permanent_null_descent.py":
        "4d7ea4e4e992142780ffd58f685177d1e3c958f5eec5c1bab2afd4404feb1043",
    "computations/verify_n8_lemma_e_unary_top_channel_synchronization.py":
        "822c9ff2b0839f3c91fe317218b5ddf4861bd737f912a9b85e9b51e324db243e",
    "notes/centered-rank-one-two-star-pure-response-obstruction.md":
        "685d76abf57ed21249196e5c22d20875460f6fdb6793c688ee54b4c6dedc21ee",
}
EXPECTED_LEDGER_SHA256 = (
    "b9af9a967bc46195a6c0494ede3dbcd0adeb370188f80a077a54e7fc0c0d92e6"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
Monomial = tuple[int, int, int, int]
Polynomial = dict[Monomial, Fraction]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def poly_add(*polynomials: Polynomial) -> Polynomial:
    out = defaultdict(Fraction)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in out.items()
            if coefficient}


def poly_scale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    out = defaultdict(Fraction)
    for lm, lc in left.items():
        for rm, rc in right.items():
            out[tuple(x + y for x, y in zip(lm, rm, strict=True))] += lc * rc
    return {monomial: coefficient for monomial, coefficient in out.items()
            if coefficient}


def poly_power(polynomial: Polynomial, exponent: int) -> Polynomial:
    answer = {(0, 0, 0, 0): Fraction(1)}
    for _ in range(exponent):
        answer = poly_mul(answer, polynomial)
    return answer


def formal_defect():
    a = {(1, 0, 0, 0): Fraction(1)}
    b = {(0, 1, 0, 0): Fraction(1)}
    c = {(0, 0, 1, 0): Fraction(1)}
    d = {(0, 0, 0, 1): Fraction(1)}
    u = poly_add(c, d)
    v = poly_add(d, poly_scale(c, Fraction(-1)))
    r = poly_add(poly_mul(a, u), poly_mul(b, v))

    r2 = poly_scale(poly_power(r, 2), Fraction(1, 2))
    r3 = poly_scale(poly_power(r, 3), Fraction(1, 6))
    expected_r2 = poly_add(
        poly_scale(poly_mul(poly_power(a, 2), poly_power(u, 2)),
                   Fraction(1, 2)),
        poly_mul(poly_mul(a, b), poly_mul(u, v)),
        poly_scale(poly_mul(poly_power(b, 2), poly_power(v, 2)),
                   Fraction(1, 2)),
    )
    expected_r3 = poly_add(
        poly_scale(poly_mul(poly_power(a, 3), poly_power(u, 3)),
                   Fraction(1, 6)),
        poly_scale(poly_mul(poly_mul(poly_power(a, 2), b),
                            poly_mul(poly_power(u, 2), v)), Fraction(1, 2)),
        poly_scale(poly_mul(poly_mul(a, poly_power(b, 2)),
                            poly_mul(u, poly_power(v, 2))), Fraction(1, 2)),
        poly_scale(poly_mul(poly_power(b, 3), poly_power(v, 3)),
                   Fraction(1, 6)),
    )
    require(r2 == expected_r2, "the compact R^[2] defect formula changed")
    require(r3 == expected_r3, "the compact R^[3] defect formula changed")

    # The abcd coefficient is the 2x2 permanent and vanishes.  Every
    # surviving quadratic monomial repeats a row or a column label.
    require(r2.get((1, 1, 1, 1), 0) == 0,
            "the permanent-null sector returned")
    require(len(r2) == 8, "the repeated-label R^[2] support changed")
    require(all(max(monomial) >= 2 for monomial in r2),
            "R^[2] acquired a non-repeated label sector")
    # Quotient by a^2=b^2=c^2=d^2=0.  This is the exact algebraic form of
    # concentrating each global star row at at most one physical site.  Four
    # distinct sites are not required: collisions only kill more products.
    square_zero_r2 = {monomial: coefficient for monomial, coefficient
                      in r2.items() if max(monomial) < 2}
    square_zero_r3 = {monomial: coefficient for monomial, coefficient
                      in r3.items() if max(monomial) < 2}
    require(not square_zero_r2 and not square_zero_r3,
            "the four-self-square-zero cap acquired a higher defect")
    return r2, r3


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def source_cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right), left_colour, right_colour


def matching_tensor(cells, vertices):
    vertices = tuple(sorted(vertices))
    answer = Counter()
    for matching in perfect_matchings(vertices):
        choices = []
        for edge in matching:
            choices.append(tuple(
                (left_colour, right_colour, coefficient)
                for (cell_edge, left_colour, right_colour), coefficient
                in cells.items()
                if cell_edge == edge and coefficient
            ))
        for selected in product(*choices):
            word = {}
            coefficient = Fraction(1)
            for edge, (left_colour, right_colour, value) in zip(
                    matching, selected, strict=True):
                word[edge[0]] = left_colour
                word[edge[1]] = right_colour
                coefficient *= value
            answer[tuple(word[site] for site in vertices)] += coefficient
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def star_product(left_star, right_star, q_cells):
    answer = Counter()
    for left_site, left_vector in left_star.items():
        for right_site, right_vector in right_star.items():
            if left_site == right_site:
                continue
            remaining = tuple(site for site in SITES
                              if site not in (left_site, right_site))
            cofactor = matching_tensor(q_cells, remaining)
            for left_colour, left_value in enumerate(left_vector):
                for right_colour, right_value in enumerate(right_vector):
                    if not left_value or not right_value:
                        continue
                    for cofactor_word, coefficient in cofactor.items():
                        word = [-1] * len(SITES)
                        word[left_site] = left_colour
                        word[right_site] = right_colour
                        for site, colour in zip(remaining, cofactor_word,
                                                strict=True):
                            word[site] = colour
                        answer[tuple(word)] += (
                            left_value * right_value * coefficient
                        )
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def build_insertion(stars):
    coefficients = {
        ("a", "c"): Fraction(1),
        ("a", "d"): Fraction(1),
        ("b", "c"): Fraction(-1),
        ("b", "d"): Fraction(1),
    }
    insertion = defaultdict(Fraction)
    for (left_name, right_name), scalar in coefficients.items():
        for left_site, left_vector in stars[left_name].items():
            for right_site, right_vector in stars[right_name].items():
                if left_site == right_site:
                    continue
                for left_colour, left_value in enumerate(left_vector):
                    for right_colour, right_value in enumerate(right_vector):
                        if not left_value or not right_value:
                            continue
                        key = source_cell(
                            left_site, right_site, left_colour, right_colour
                        )
                        insertion[key] += (
                            scalar * left_value * right_value
                        )
    return Counter({cell: coefficient for cell, coefficient
                    in insertion.items() if coefficient})


def top_by_insertion_count(q_cells, insertion):
    answer = [Counter() for _ in range(4)]
    for matching in perfect_matchings(SITES):
        def visit(index, word, coefficient, insertion_count):
            if index == len(matching):
                answer[insertion_count][tuple(word)] += coefficient
                return
            edge = matching[index]
            for is_insertion, cells in ((False, q_cells),
                                        (True, insertion)):
                for (cell_edge, left_colour, right_colour), value in cells.items():
                    if cell_edge != edge or not value:
                        continue
                    next_word = list(word)
                    next_word[edge[0]] = left_colour
                    next_word[edge[1]] = right_colour
                    visit(index + 1, next_word, coefficient * value,
                          insertion_count + int(is_insertion))
        visit(0, [-1] * len(SITES), Fraction(1), 0)
    return tuple(Counter({word: coefficient for word, coefficient
                          in tensor.items() if coefficient})
                 for tensor in answer)


def pure(colour):
    return Counter({(colour,) * len(SITES): Fraction(1)})


def rational_rank(matrix):
    matrix = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [value - scale * pivot_entry
                           for value, pivot_entry
                           in zip(matrix[row], matrix[rank], strict=True)]
        rank += 1
    return rank


def eight_site_incidence_audit(q_cells, stars):
    """Test the precise activity/goodness hypotheses of the OO gate."""
    p_endpoint, q_endpoint = 6, 7
    vertices = tuple(range(8))
    blocks = Counter(q_cells)
    for name, label, endpoint in (
            ("a", 1, p_endpoint), ("b", 2, p_endpoint),
            ("c", 1, q_endpoint), ("d", 2, q_endpoint)):
        for site, vector in stars[name].items():
            for colour, value in enumerate(vector):
                if value:
                    blocks[source_cell(endpoint, site, label, colour)] += value

    full_tensor = matching_tensor(blocks, vertices)
    require(full_tensor == Counter({(1,) * 8: Fraction(1),
                                    (2,) * 8: Fraction(1)}),
            "the eight-site partial target changed")

    def entry(u, v, i, j):
        return blocks.get(source_cell(u, v, i, j), Fraction(0))

    def star_rank(endpoint, deleted_neighbor):
        columns = [(site, colour) for site in vertices
                   if site not in (endpoint, deleted_neighbor)
                   for colour in COLOURS]
        return rational_rank([
            [entry(endpoint, site, row_colour, colour)
             for site, colour in columns]
            for row_colour in COLOURS
        ])

    arms = ((p_endpoint, 0), (p_endpoint, 5), (p_endpoint, 2),
            (q_endpoint, 1), (q_endpoint, 3))
    activity = {}
    ranks = {}
    for left, right in arms:
        complement = tuple(site for site in vertices
                           if site not in (left, right))
        activity[f"{left}-{right}"] = bool(
            matching_tensor(blocks, complement)
        )
        ranks[f"{left}-{right}"] = [
            star_rank(left, right), star_rank(right, left)
        ]
    require(activity == {
        "6-0": True, "6-5": False, "6-2": True,
        "7-1": True, "7-3": True,
    }, "the response guard activity pattern changed")
    require(ranks == {
        "6-0": [2, 1], "6-5": [2, 2], "6-2": [1, 1],
        "7-1": [1, 1], "7-3": [1, 1],
    }, "the response guard good-star ranks changed")

    # Both repeated-row defect matchings use inactive P--5.  The shared
    # P--0/P--5 rank-one fan is moreover the flat pair E11/E11.
    require(entry(6, 0, 1, 1) == entry(6, 5, 1, 1) == 1,
            "the flat repeated-row fan changed")
    require(all(entry(6, site, i, j) == (1 if (i, j) == (1, 1) else 0)
                for site in (0, 5) for i in COLOURS for j in COLOURS),
            "the repeated-row fan stopped being E11/E11")
    return {
        "full_matching_tensor": ["X1", "X2"],
        "missing_full_nine_anchor": "X0",
        "arm_activity": activity,
        "deleted_star_rank_pairs": ranks,
        "defect_arm_provenance": [
            ["P0", "Q1", "P5", "Q3", "q24"],
            ["P0", "Q3", "P5", "Q1", "q24"],
        ],
        "oo_gate_failure": (
            "both defect matchings use inactive P5; no displayed arm is "
            "doubly good (rank pair 3,3), and the P0/P5 rank-one fan is "
            "the flat common-factor pair E11/E11"
        ),
    }


def response_rows(stars, q_cells):
    return {
        "11": star_product(stars["a"], stars["c"], q_cells),
        "12": star_product(stars["a"], stars["d"], q_cells),
        "21": star_product(stars["b"], stars["c"], q_cells),
        "22": star_product(stars["b"], stars["d"], q_cells),
    }


def exact_response_guard():
    # The committed silent P3+P3 common-cofactor packet, with one additional
    # response-invisible colour-1 component at site 5 in p1=a.
    q_cells = Counter({
        source_cell(2, 4, 1, 1): Fraction(1),
        source_cell(3, 5, 1, 1): Fraction(1),
        source_cell(0, 5, 2, 2): Fraction(1),
        source_cell(1, 4, 2, 2): Fraction(1),
    })
    e1 = (Fraction(0), Fraction(1), Fraction(0))
    e2 = (Fraction(0), Fraction(0), Fraction(1))
    stars = {
        "a": {0: e1, 5: e1},
        "b": {2: e2},
        "c": {1: e1},
        "d": {3: e2},
    }
    rows = response_rows(stars, q_cells)
    require(rows == {"11": pure(1), "12": Counter(),
                     "21": Counter(), "22": pure(2)},
            "the exact 2x2 response guard changed")
    require(matching_tensor(q_cells, SITES) == Counter(),
            "the response guard acquired the unary top")

    insertion = build_insertion(stars)
    sectors = top_by_insertion_count(q_cells, insertion)
    defect_word = (1, 1, 1, 2, 1, 1)
    require(sectors[0] == Counter(), "q^[3] changed")
    require(sectors[1] == pure(1) + pure(2), "Rq^[2] changed")
    require(sectors[2] == Counter({defect_word: Fraction(2)}),
            "the repeated-row R^[2]q defect changed")
    require(sectors[3] == Counter(), "R^[3] changed")

    # Deleting the extra component preserves all four response equations and
    # removes the defect.  Thus maximum-anchor/minimum-support is genuinely
    # load-bearing; this example does not survive that normalization.
    reduced = {name: dict(components) for name, components in stars.items()}
    del reduced["a"][5]
    require(response_rows(reduced, q_cells) == rows,
            "the extra p1 component stopped being response-invisible")
    reduced_sectors = top_by_insertion_count(
        q_cells, build_insertion(reduced)
    )
    require(reduced_sectors[1] == pure(1) + pure(2)
            and reduced_sectors[2] == Counter()
            and reduced_sectors[3] == Counter(),
            "minimum-support deletion stopped cleaning the cap")

    # The two-star line-hitting conclusion is already present: p1,p2 have
    # target lines e1 at site 0 (also 5) and e2 at site 2; s1,s2 have e1 at
    # site 1 and e2 at site 3.  It does not see the removable repeated row.
    line_sites = {
        "p_e1": [0, 5], "p_e2": [2],
        "s_e1": [1], "s_e2": [3],
    }
    incidence = eight_site_incidence_audit(q_cells, stars)
    return {
        "q_cells": [list(edge) + [left, right, str(value)]
                    for (edge, left, right), value in sorted(q_cells.items())],
        "stars": {
            name: {str(site): [str(value) for value in vector]
                   for site, vector in sorted(components.items())}
            for name, components in stars.items()
        },
        "response_rows": {"11": "X1", "12": "0", "21": "0", "22": "X2"},
        "q_cubed": "0",
        "cap_sectors": {
            "R*q^[2]": ["X1", "X2"],
            "R^[2]*q": {"111211": "2"},
            "R^[3]": {},
        },
        "two_star_target_line_sites": line_sites,
        "minimum_support_audit": (
            "deleting p1's site-5 component preserves every response row "
            "and removes the repeated-label defect"
        ),
        "eight_site_incidence_audit": incidence,
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main():
    pin_dependencies()
    r2, r3 = formal_defect()
    guard = exact_response_guard()
    ledger = {
        "pins": PINS,
        "canonical_cap": "R=ac+ad-bc+bd=a(c+d)+b(d-c)",
        "formal_identity": {
            "R^[2]": (
                "a^2(c+d)^2/2 + ab(d^2-c^2) + b^2(d-c)^2/2"
            ),
            "R^[3]": (
                "a^3(c+d)^3/6 + a^2b(c+d)^2(d-c)/2 + "
                "ab^2(c+d)(d-c)^2/2 + b^3(d-c)^3/6"
            ),
            "R2_monomials": len(r2),
            "R3_monomials": len(r3),
            "distinct_row_column_abcd_coefficient": "0=perm(K)",
            "clean_cap_criterion": (
                "a^2=b^2=c^2=d^2=0; equivalently each star row has "
                "support on at most one physical site"
            ),
        },
        "exact_full_response_counterguard": guard,
        "verdict": (
            "permanent zero alone leaves precisely the repeated-row/column "
            "defect; the full response tensor and two-star line-hitting "
            "conclusion do not annihilate it"
        ),
        "remaining_gap": (
            "the displayed defect cell is individually removable, so it is "
            "excluded by minimum support; no full q^[3]=X0 one-bad "
            "counterguard or concentration/descent theorem is claimed; "
            "nonzero second fundamental form does not by itself imply the "
            "active doubly-good OO gate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"multisite permanent-null ledger changed: {digest}")
    print("N=8 one-bad multisite permanent-null defect: PASS")
    print("formal R^[2] support: 8 repeated-label monomials; abcd sector: 0")
    print("exact full-response guard: R^[2]q = 2*[111211]")
    print("unary top of guard: q^[3]=0")
    print("minimum-support deletion: preserves responses and kills defect")
    print("full minimum-support one-bad packet: OPEN")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
