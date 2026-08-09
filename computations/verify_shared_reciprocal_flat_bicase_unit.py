#!/usr/bin/env python3
"""Uniform unit for both flat shared-rank-one star cases.

The shared p-factors of two rank-one arms pq,pr are either proportional or
independent.  Flatness gives a common residual star in the first case and
zero residual stars in the second.  With distinct outer target lines, every
equal-colour q,r slice forces the chord qr in both cases.  The same ordinary
three-row unit from the coordinate-flat checker therefore applies without
budget, site-cover, support, or characteristic hypotheses.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import verify_shared_reciprocal_budget13_overlap_frontier as overlap
import verify_shared_reciprocal_coordinate_flat_unit as coordinate


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
SITES = tuple(range(8))
P, Q, R = 0, 1, 2
COMMON = tuple(range(3, 8))
RESIDUAL = (P,) + COMMON
CASES = ("proportional", "independent")
PINNED_COORDINATE_SHA256 = (
    "01726b46ffdbbc4be5966150879bda788b43978bea57e8e102eb532285d39866"
)
EXPECTED_LEDGER_SHA256 = (
    "f35f3089eec64c65ccef345ce6b434f79699612257094affad9dcfaf03dcfef6"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependency():
    path = ROOT / "computations/verify_shared_reciprocal_coordinate_flat_unit.py"
    require(sha256(path.read_bytes()).hexdigest() == PINNED_COORDINATE_SHA256,
            "the coordinate-flat unit dependency changed")


def head_rows(case):
    if case == "proportional":
        return tuple(
            (a, c, b, b)
            for a in COLORS for c in COLORS if a != c
            for b in COLORS
        )
    require(case == "independent", "unknown flat-star case")
    return tuple(
        (a, c, b, d)
        for a in COLORS for c in COLORS if a != c
        for b in COLORS for d in COLORS if b != d
    )


def unrestricted_support(case, head):
    a, c, b, d = head
    require(a != c, "the outer target lines are not distinct")
    require((case == "proportional") == (b == d),
            "the head does not match its shared-factor case")
    support = set()
    for left in SITES:
        for right in SITES:
            if left >= right:
                continue
            for left_color in COLORS:
                for right_color in COLORS:
                    cell = (left, right, left_color, right_color)
                    if (left, right) == (P, Q):
                        allowed = (left_color, right_color) == (b, a)
                    elif (left, right) == (P, R):
                        allowed = (left_color, right_color) == (d, c)
                    elif left == Q and right in COMMON:
                        allowed = (case == "proportional"
                                   and left_color == a)
                    elif left == R and right in COMMON:
                        allowed = (case == "proportional"
                                   and left_color == c)
                    else:
                        allowed = True
                    if allowed:
                        support.add(cell)
    return frozenset(support)


def cell_monomial(case, head, cell):
    left, right, left_color, right_color = cell
    a, c, b, d = head
    if (left, right) == (P, Q):
        require((left_color, right_color) == (b, a),
                "the pq cell left its head")
        return ("L",)
    if (left, right) == (P, R):
        require((left_color, right_color) == (d, c),
                "the pr cell left its head")
        return ("M",)
    if left == Q and right in COMMON:
        require(case == "proportional" and left_color == a,
                "a forbidden q-C cell was substituted")
        return ("L", f"z{right}_{right_color}")
    if left == R and right in COMMON:
        require(case == "proportional" and left_color == c,
                "a forbidden r-C cell was substituted")
        return ("M", f"z{right}_{right_color}")
    return (f"x{left}{right}_{left_color}{right_color}",)


def generator(case, head, support, word):
    polynomial = Counter()
    for matching in overlap.MATCHINGS:
        cells = tuple((left, right, word[left], word[right])
                      for left, right in matching)
        if not set(cells) <= support:
            continue
        monomial = ()
        for cell in cells:
            monomial += cell_monomial(case, head, cell)
        coordinate.add_term(polynomial, monomial)
    if len(set(word)) == 1:
        coordinate.add_term(polynomial, (), -1)
    return polynomial


def residual_hafnian(case, head, support, color):
    polynomial = Counter()
    for matching in overlap.perfect_matchings(RESIDUAL):
        cells = tuple((left, right, color, color)
                      for left, right in matching)
        require(set(cells) <= support,
                "the unrestricted residual envelope lost an edge")
        monomial = ()
        for cell in cells:
            monomial += cell_monomial(case, head, cell)
        coordinate.add_term(polynomial, monomial)
    require(len(polynomial) == 15,
            "the six-site residual hafnian changed")
    return polynomial


def factor_and_certificate(case, head, first_color, second_color):
    support = unrestricted_support(case, head)
    first_residual = residual_hafnian(
        case, head, support, first_color
    )
    second_residual = residual_hafnian(
        case, head, support, second_color
    )
    first_word = (first_color,) * 8
    second_word = (second_color,) * 8
    mixed_word = tuple(
        first_color if site in (Q, R) else second_color
        for site in SITES
    )
    first_generator = generator(case, head, support, first_word)
    second_generator = generator(case, head, support, second_word)
    mixed_generator = generator(case, head, support, mixed_word)
    first_diagonal = coordinate.monomial_polynomial(
        f"x{Q}{R}_{first_color}{first_color}"
    )
    second_diagonal = coordinate.monomial_polynomial(
        f"x{Q}{R}_{second_color}{second_color}"
    )
    expected_first = coordinate.add_polynomials(
        (coordinate.multiply(first_diagonal, first_residual), 1),
        (coordinate.monomial_polynomial(), -1),
    )
    expected_second = coordinate.add_polynomials(
        (coordinate.multiply(second_diagonal, second_residual), 1),
        (coordinate.monomial_polynomial(), -1),
    )
    expected_mixed = coordinate.multiply(
        first_diagonal, second_residual
    )
    require(first_generator == expected_first,
            f"{case}: first equal-colour slice did not force qr")
    require(second_generator == expected_second,
            f"{case}: second equal-colour slice did not force qr")
    require(mixed_generator == expected_mixed,
            f"{case}: mixed residual slice did not force qr")

    inner = coordinate.add_polynomials(
        (coordinate.multiply(second_diagonal, mixed_generator), 1),
        (coordinate.multiply(first_diagonal, second_generator), -1),
    )
    certificate = coordinate.add_polynomials(
        (coordinate.multiply(first_residual, inner), 1),
        (first_generator, -1),
    )
    require(certificate == coordinate.monomial_polynomial(),
            f"{case}: ordinary three-row unit failed")
    return sha256(json.dumps(
        (
            coordinate.serial_polynomial(first_generator),
            coordinate.serial_polynomial(mixed_generator),
            coordinate.serial_polynomial(second_generator),
        ),
        separators=(",", ":"),
    ).encode()).hexdigest()


def direct_route_audit(case, head):
    """Audit the only possible non-chord uses, including pq and pr."""

    a, c, _b, _d = head
    checked = 0
    for color in COLORS:
        for matching in overlap.MATCHINGS:
            if (Q, R) in matching:
                continue
            q_partner = next(
                right if left == Q else left
                for left, right in matching if Q in (left, right)
            )
            r_partner = next(
                right if left == R else left
                for left, right in matching if R in (left, right)
            )
            require(q_partner != r_partner,
                    "a matching used one partner twice")
            if case == "independent":
                q_possible = q_partner == P and color == a
                r_possible = r_partner == P and color == c
            else:
                q_possible = color == a
                r_possible = color == c
            require(not (q_possible and r_possible),
                    f"{case}: a non-chord equal-colour route survived")
            checked += 1
    return checked


def complete_system(case, head):
    support = unrestricted_support(case, head)
    rows = []
    histogram = Counter()
    variables = set()
    for word in product(COLORS, repeat=8):
        polynomial = generator(case, head, support, word)
        histogram[len(polynomial)] += 1
        serial = coordinate.serial_polynomial(polynomial)
        rows.append((word, serial))
        for monomial in polynomial:
            variables.update(monomial)
    payload = json.dumps(rows, separators=(",", ":"))
    return {
        "cells": len(support),
        "variables": len(variables),
        "term_histogram": dict(sorted(histogram.items())),
        "row_sha256": sha256(payload.encode()).hexdigest(),
    }


def main():
    pin_dependency()
    system_rows = (
        ("proportional", (0, 1, 0, 0)),
        ("independent", (0, 1, 0, 1)),
    )
    systems = [
        {"case": case, **complete_system(case, head)}
        for case, head in system_rows
    ]
    certificates = Counter()
    route_checks = Counter()
    source_hashes = set()
    for case in CASES:
        heads = head_rows(case)
        certificates[case] = 0
        for head in heads:
            route_checks[case] += direct_route_audit(case, head)
            for first_color in COLORS:
                for second_color in COLORS:
                    if first_color == second_color:
                        continue
                    source_hashes.add(factor_and_certificate(
                        case, head, first_color, second_color
                    ))
                    certificates[case] += 1

    require(certificates == {"proportional": 108, "independent": 216},
            f"the bi-case certificate census changed: {certificates}")
    require(route_checks == {"proportional": 4860, "independent": 9720},
            f"the direct-route audit census changed: {route_checks}")

    ledger = {
        "pinned_coordinate_sha256": PINNED_COORDINATE_SHA256,
        "unrestricted_n8_systems": systems,
        "head_counts": {
            case: len(head_rows(case)) for case in CASES
        },
        "ordered_color_certificates": dict(certificates),
        "nonchord_matching_route_checks": dict(route_checks),
        "certificate_source_hashes": sorted(source_hashes),
        "unit": "1=F_i*(D_jj*G_i_given_j-D_ii*G_j)-G_i",
        "uses_budget_or_site_cover": False,
        "support_deletion_stable": True,
        "even_order_scope": "all_even_N_at_least_4",
        "palette_scope": "all_d_at_least_2",
        "coefficient_survivors": 0,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"the flat bi-case ledger changed: {digest}")
    print("shared reciprocal flat bi-case unit: PASS")
    print("unrestricted complete systems: 2 x 6561 rows")
    print("head refinements:", {case: len(head_rows(case)) for case in CASES})
    print("ordinary certificates:", dict(certificates))
    print("nonchord direct-route checks:", dict(route_checks))
    print("coefficient survivors: 0")
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()
