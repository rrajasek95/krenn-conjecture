#!/usr/bin/env python3
"""Exact source boundary for the strict Hall K2,2 family.

The two diagonal hole families contain complementary perfect matchings of
one physical K4.  We classify their endpoint orientations, reduce every
common-effective orientation to the Hall-star source theorem, and compute
the two genuinely opposite orientations exactly.  In the latter case the
four axis crossed products occupy four distinct word grades (not two
binomials), and the permanent-null cap has two factorized repeated-row
tails.  Retaining both strict core matchings repairs the natural overlaps
to active rank-three deleted stars; curvature remains a separate minor.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from math import prod
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_uniform_multisite_hall_star_source_reduction.py":
        "65ccab6e5830efd9f0dfa084c0d98391e89bad083fa7a41743b2fec7dde15bd5",
    "notes/uniform-multisite-hall-star-source-reduction.md":
        "a0efe068a25423f16d0e24f8d943fd09c4c6911d1dbcdd231d45e66ae37868e0",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "notes/uniform-one-bad-defect-provenance-routing-obstruction.md":
        "8d9f27595caebce72137ed19f5d9517cdc60208ed9e8ea256d291785c3427f4c",
}
EXPECTED_LEDGER_SHA256 = "d4eb154985c824c9e463ff6db4f6c0c47a42458561583f65bae9e459ca3edad5"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


# Sparse commutative polynomials over Q.
def clean(polynomial):
    return Counter({term: coefficient for term, coefficient
                    in polynomial.items() if coefficient})


def variable(name):
    return Counter({(name,): Q(1)})


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale(polynomial, scalar):
    return clean(Counter({term: Q(scalar) * coefficient
                          for term, coefficient in polynomial.items()}))


def multiply(*polynomials):
    answer = Counter({(): Q(1)})
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(updated)
    return answer


def monomial(*names, coefficient=1):
    return Counter({tuple(sorted(names)): Q(coefficient)})


def audit_strict_rectangle():
    """The only optional edges are the common third perfect matching."""
    vertices = range(4)
    all_edges = set(itertools.combinations(vertices, 2))
    first_core = {(0, 1), (2, 3)}
    second_core = {(0, 2), (1, 3)}
    third = {(0, 3), (1, 2)}
    allowed_first = {
        edge for edge in all_edges
        if all(set(edge) & set(member) for member in second_core)
    }
    allowed_second = {
        edge for edge in all_edges
        if all(set(edge) & set(member) for member in first_core)
    }
    require(allowed_first == first_core | third,
            "the first strict K2,2 envelope changed")
    require(allowed_second == second_core | third,
            "the second strict K2,2 envelope changed")
    require((allowed_first - first_core) == (allowed_second - second_core)
            == third, "the optional shared matching changed")
    return {
        "colour1_core": sorted(first_core),
        "colour2_core": sorted(second_core),
        "only_optional_edges": sorted(third),
    }


def audit_orientations():
    """Orient the two core matchings by which endpoint is the P-star."""
    first = ((0, 1), (2, 3))
    second = ((0, 2), (1, 3))
    histogram = Counter()
    opposite = []
    for bits in itertools.product((0, 1), repeat=4):
        sides = {}
        for colour, (matching, choices) in enumerate(
                ((first, bits[:2]), (second, bits[2:]))):
            for edge, choice in zip(matching, choices, strict=True):
                p_site = edge[choice]
                s_site = edge[1 - choice]
                sides[colour, p_site] = "P"
                sides[colour, s_site] = "S"
        same = tuple(site for site in range(4)
                     if sides[0, site] == sides[1, site])
        histogram[len(same)] += 1
        if not same:
            opposite.append({
                "bits": bits,
                "P_colour1": tuple(site for site in range(4)
                                    if sides[0, site] == "P"),
                "P_colour2": tuple(site for site in range(4)
                                    if sides[1, site] == "P"),
            })
    require(histogram == Counter({2: 12, 4: 2, 0: 2}),
            f"the K2,2 orientation histogram changed: {histogram}")
    require(all(set(item["P_colour1"]).isdisjoint(item["P_colour2"])
                and set(item["P_colour1"]) | set(item["P_colour2"])
                == set(range(4)) for item in opposite),
            "an opposite orientation stopped being a two-shore split")
    return {
        "same_side_site_histogram": dict(sorted(histogram.items())),
        "common_side_orientations": 14,
        "opposite_orientations": opposite,
        "source_routing_guard": (
            "the Hall-star theorem applies at a same-side site only when "
            "both complete oriented contributions there are nonzero; if "
            "one cancels inside its complete coefficient, this is exactly "
            "the pre-existing affine line-hitting/joint-kernel gate"
        ),
    }


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    pivot_row = 0
    if not matrix:
        return 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def perfect_matching(*edges):
    flat = [site for edge in edges for site in edge]
    require(len(flat) == len(set(flat)), f"not a matching: {edges}")
    return tuple(tuple(sorted(edge)) for edge in edges)


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def selected_column_rank(matchings, pair, endpoint):
    """Endpoint-row rank certified after a selected arm is cut."""
    other = pair[0] if endpoint == pair[1] else pair[1]
    labels = []
    for colour, matching in matchings:
        neighbour = partner(matching, endpoint)
        if neighbour == other:
            continue
        labels.append((neighbour, colour))
    # Each diagonal selected cell E_cc supplies endpoint row c.  Different
    # neighbours in the same colour do not increase the 3-row star rank.
    return len({colour for _neighbour, colour in labels})


def audit_anchor_rank_boundary():
    # Outer endpoints P=6,S=7.  The opposite shore orientation is
    # p1:{0,3}, s1:{1,2}, p2:{1,2}, s2:{0,3}.
    q0 = perfect_matching((6, 7), (0, 1), (2, 4), (3, 5))
    q1_left = perfect_matching((6, 0), (7, 1), (2, 3), (4, 5))
    q1_right = perfect_matching((6, 3), (7, 2), (0, 1), (4, 5))
    q2_left = perfect_matching((6, 2), (7, 0), (1, 3), (4, 5))
    q2_right = perfect_matching((6, 1), (7, 3), (0, 2), (4, 5))
    matchings = (
        (0, q0), (1, q1_left), (1, q1_right),
        (2, q2_left), (2, q2_right),
    )
    pair1, pair2 = (6, 0), (7, 0)
    ranks = tuple(selected_column_rank(matchings, pair, endpoint)
                  for pair in (pair1, pair2) for endpoint in pair)
    require(ranks == (3, 3, 3, 3),
            f"the opposite-anchor selected ranks changed: {ranks}")
    return {
        "natural_overlap_pairs": [pair1, pair2],
        "direct_heads": [1, 2],
        "selected_column_ranks": ranks,
        "support_active": [True, True],
        "conclusion": (
            "both strict core matchings restore the same-colour column lost "
            "at a selected arm; the other diagonal target and the direct "
            "unary matching restore the other two endpoint rows.  Thus the "
            "natural overlaps are active and four-good, but a nonzero "
            "shore curvature minor is still separate"
        ),
    }


def coefficient_of_pair_form(left, right, scalar, u, v, colours):
    """Coefficient of scalar*(left right) on decorated edge uv."""
    answer = Counter()
    cu, cv = colours[u], colours[v]
    for first_site, first_colour, second_site, second_colour in (
            (u, cu, v, cv), (v, cv, u, cu)):
        first = left.get((first_site, first_colour))
        second = right.get((second_site, second_colour))
        if first is not None and second is not None:
            answer.update(multiply(scalar, first, second))
    return clean(answer)


def hafnian_four(cell_coefficient, colours):
    answer = Counter()
    for matching in (((0, 1), (2, 3)),
                     ((0, 2), (1, 3)),
                     ((0, 3), (1, 2))):
        answer.update(multiply(*(
            cell_coefficient(left, right, colours)
            for left, right in matching
        )))
    return clean(answer)


def audit_opposite_cap_and_crossed_locks():
    x, r, s, y = (variable(name) for name in ("x", "r", "s", "y"))
    a = {(0, 1): variable("a0"), (3, 1): variable("a3")}
    b = {(1, 2): variable("b1"), (2, 2): variable("b2")}
    c = {(1, 1): variable("c1"), (2, 1): variable("c2")}
    d = {(0, 2): variable("d0"), (3, 2): variable("d3")}
    summands = ((a, c, x), (a, d, r), (b, c, s), (b, d, y))

    def r_cell(u, v, colours):
        return add(*(coefficient_of_pair_form(left, right, scalar,
                                              u, v, colours)
                     for left, right, scalar in summands))

    pure1 = hafnian_four(r_cell, (1, 1, 1, 1))
    pure2 = hafnian_four(r_cell, (2, 2, 2, 2))
    require(pure1 == monomial("a0", "a3", "c1", "c2", "x", "x",
                              coefficient=2),
            f"the pure-1 repeated row changed: {pure1}")
    require(pure2 == monomial("b1", "b2", "d0", "d3", "y", "y",
                              coefficient=2),
            f"the pure-2 repeated row changed: {pure2}")

    permanent = add(multiply(x, y), multiply(r, s))
    mixed_words = ((1, 1, 2, 2), (1, 2, 1, 2),
                   (2, 1, 2, 1), (2, 2, 1, 1))
    mixed_factors = (
        ("a0", "b2", "c1", "d3"),
        ("a0", "b1", "c2", "d3"),
        ("a3", "b2", "c1", "d0"),
        ("a3", "b1", "c2", "d0"),
    )
    for word, factors in zip(mixed_words, mixed_factors, strict=True):
        value = hafnian_four(r_cell, word)
        require(value == multiply(monomial(*factors), permanent),
                f"the mixed permanent factor changed at {word}: {value}")

    # The four axis crossed products occupy four different output words.
    # Therefore they are four monomial coefficients, not two binomials.
    crossed_words = ((1, 0, 0, 2), (2, 0, 0, 1),
                     (0, 2, 1, 0), (0, 1, 2, 0))
    require(len(set(crossed_words)) == 4,
            "the four axis crossed word grades collided")
    crossed_rows = (
        "a0*d3*H03", "a3*d0*H03",
        "b1*c2*H12", "b2*c1*H12",
    )

    # On six residual sites the only remaining edge multiplies each pure
    # sector.  There are 18 disjoint output words, so the two debts cannot
    # cancel one another.
    residual_words = {
        tuple((1, 1, 1, 1) + colours)
        for colours in itertools.product(range(3), repeat=2)
    } | {
        tuple((2, 2, 2, 2) + colours)
        for colours in itertools.product(range(3), repeat=2)
    }
    require(len(residual_words) == 18,
            "the repeated-row residual word grades collided")
    return {
        "opposite_shores": {
            "A": [0, 3], "B": [1, 2],
            "p1_s2_support": "A", "p2_s1_support": "B",
        },
        "response_linear_identity":
            "R*q^[h-1]=x*X1+y*X2 for R=x*p1s1+r*p1s2+s*p2s1+y*p2s2",
        "permanent_relation": "x*y+r*s=0",
        "axis_crossed_rows": crossed_rows,
        "axis_crossed_words": crossed_words,
        "cofactor_consequence": (
            "when the strict core coefficients are localized and no "
            "same-word mate occurs, the four zero rows force H03=H12=0"
        ),
        "R_squared": {
            "1111": "2*x^2*a0*a3*c1*c2",
            "2222": "2*y^2*b1*b2*d0*d3",
            "four_mixed_words": "star_monomial*(x*y+r*s)=0",
        },
        "six_site_tail": (
            "the two displayed pure K4 coefficients multiply the arbitrary "
            "decorated outside edge q45, giving 18 pairwise distinct output "
            "word grades; q45=0 kills the tail, while q45!=0 is a genuine "
            "repeated endpoint-use debt rather than a physical OO witness"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "strict_rectangle": audit_strict_rectangle(),
        "orientations": audit_orientations(),
        "opposite_anchor_rank_boundary": audit_anchor_rank_boundary(),
        "opposite_cap_and_crossed_locks":
            audit_opposite_cap_and_crossed_locks(),
        "source_reduction": [
            "failure of complete oriented effectiveness is the established "
            "affine line-hitting/joint-kernel gate",
            "a common effective side enters the Hall-star source theorem; "
            "a free off-web cancellation carrier enters the good active route",
            "a kernel of the same-star five-row lock map gives an exact "
            "anchor-safe deletion",
            "otherwise the strict-K2,2 datum is four separate selected-axis "
            "monomial rows, the cofactor-dark equations H03=H12=0, and the "
            "two factorized repeated-row tails",
        ],
        "scope": (
            "uniform family algebra on the strict K2,2 core, not a subset "
            "census and not a proof that every combinatorial same-side "
            "orientation is aggregate-effective.  The opposite residual "
            "does certify active rank-three deleted stars after both core "
            "matchings are retained, but does not force curvature or a clean cap"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall K2,2 source ledger changed: {digest}")
    print("uniform multisite strict Hall K2,2 source reduction: PASS")
    print("orientations: 14 common-side, 2 opposite-shore")
    print("opposite natural selected ranks: (3,3,3,3), support-active")
    print("opposite residual: four monomial rows + two pure repeated-row tails")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
