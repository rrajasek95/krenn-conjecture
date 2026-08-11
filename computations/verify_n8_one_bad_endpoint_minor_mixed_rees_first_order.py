#!/usr/bin/env python3
"""First mixed-q Rees order around the arbitrary pure unary chart.

Adjoin every off-diagonal decorated residual q cell with a common factor tau,
every endpoint-star correction with factor tau, and the four binary direct
corrections with factor tau.  Expand q^[3] and all four response tensors
exactly modulo tau^2.  The two crossed equations already have unit initial
forms in degree zero by the pure-chart ideal certificate, so no positive-
filtration mixed or endpoint correction can produce a formal completion.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_endpoint_minor_arbitrary_pure_unary_completion.py":
        "f77b99d56d817689e55f4790e000799bc34c9b6960d2b9f035300d407562f20a",
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = (
    "2a1b18e49a659c6d074624243f44506609f2afaaee041e36d00e928066dab7c6"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
TAU = "tau"
PURE0 = (0,) * 6
CROSS12_WORD = tuple(map(int, "100200"))
CROSS21_WORD = tuple(map(int, "012000"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def variable(*names):
    return Counter({tuple(sorted(names)): Fraction(1)})


def poly_add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def poly_mul(left, right, max_tau=1):
    answer = defaultdict(Fraction)
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            term = tuple(sorted(left_term + right_term))
            if term.count(TAU) <= max_tau:
                answer[term] += left_coefficient * right_coefficient
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def matching_tensor(module, cells, vertices):
    vertices = tuple(sorted(vertices))
    output = defaultdict(Counter)
    for matching in module.perfect_matchings(vertices):
        choices = [tuple(
            (left_colour, right_colour, polynomial)
            for (cell_edge, left_colour, right_colour), polynomial
            in cells.items() if cell_edge == edge and polynomial
        ) for edge in matching]
        if any(not choice for choice in choices):
            continue

        def visit(index, word, coefficient):
            if index == len(matching):
                output[tuple(word[site] for site in vertices)].update(
                    coefficient
                )
                return
            left, right = matching[index]
            for left_colour, right_colour, polynomial in choices[index]:
                next_coefficient = poly_mul(coefficient, polynomial)
                if not next_coefficient:
                    continue
                next_word = list(word)
                next_word[left], next_word[right] = left_colour, right_colour
                visit(index + 1, next_word, next_coefficient)

        visit(0, [-1] * len(SITES), Counter({(): Fraction(1)}))
    return {
        word: Counter({term: coefficient for term, coefficient
                       in polynomial.items() if coefficient})
        for word, polynomial in output.items() if polynomial
    }


def star_product(module, left_star, right_star, q_cells):
    output = defaultdict(Counter)
    for (left_site, left_colour), left_polynomial in left_star.items():
        for (right_site, right_colour), right_polynomial in right_star.items():
            if left_site == right_site:
                continue
            remaining = tuple(site for site in SITES
                              if site not in (left_site, right_site))
            cofactor = matching_tensor(module, q_cells, remaining)
            star_factor = poly_mul(left_polynomial, right_polynomial)
            if not star_factor:
                continue
            for cofactor_word, polynomial in cofactor.items():
                word = [-1] * len(SITES)
                word[left_site] = left_colour
                word[right_site] = right_colour
                for site, colour in zip(remaining, cofactor_word, strict=True):
                    word[site] = colour
                output[tuple(word)].update(poly_mul(star_factor, polynomial))
    return {
        word: Counter({term: coefficient for term, coefficient
                       in polynomial.items() if coefficient})
        for word, polynomial in output.items() if polynomial
    }


def tau_part(polynomial, degree):
    answer = Counter()
    for term, coefficient in polynomial.items():
        if term.count(TAU) != degree:
            continue
        reduced = list(term)
        for _ in range(degree):
            reduced.remove(TAU)
        answer[tuple(reduced)] += coefficient
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def tensor_statistics(tensor):
    return {
        "degree0_words": sum(bool(tau_part(polynomial, 0))
                             for polynomial in tensor.values()),
        "degree0_terms": sum(len(tau_part(polynomial, 0))
                             for polynomial in tensor.values()),
        "degree1_words": sum(bool(tau_part(polynomial, 1))
                             for polynomial in tensor.values()),
        "degree1_terms": sum(len(tau_part(polynomial, 1))
                             for polynomial in tensor.values()),
    }


def serial_polynomial(polynomial):
    return {
        "*".join(term) if term else "1": str(coefficient)
        for term, coefficient in sorted(polynomial.items())
    }


def main():
    pin_dependencies()
    pure = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_arbitrary_pure_unary_completion")
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    q_cells = {
        module.source_cell(2, 4, 1, 1): variable("A"),
        module.source_cell(3, 5, 1, 1): variable("B"),
        module.source_cell(0, 5, 2, 2): variable("C"),
        module.source_cell(1, 4, 2, 2): variable("D"),
    }
    for left in SITES:
        for right in SITES[left + 1:]:
            q_cells[module.source_cell(left, right, 0, 0)] = variable(
                f"z{left}{right}"
            )
            for left_colour in COLOURS:
                for right_colour in COLOURS:
                    if left_colour == right_colour:
                        continue
                    q_cells[module.source_cell(
                        left, right, left_colour, right_colour
                    )] = variable(
                        TAU, f"m{left}{right}_{left_colour}{right_colour}"
                    )
    mixed_q_variables = 15 * 6
    require(sum(
        any(name.startswith("m") for name in term)
        for polynomial in q_cells.values() for term in polynomial
    ) == mixed_q_variables, "the mixed q direction count changed")

    def star(name, base):
        row = {}
        for site in SITES:
            for colour in COLOURS:
                correction = variable(TAU, f"d{name}{site}_{colour}")
                if (site, colour) in base:
                    row[(site, colour)] = poly_add(
                        variable(base[(site, colour)]), correction
                    )
                else:
                    row[(site, colour)] = correction
        return row

    stars = {
        "p1": star("p1", {(0, 1): "p0", (5, 1): "p5"}),
        "p2": star("p2", {(2, 2): "p2"}),
        "s1": star("s1", {(1, 1): "s1"}),
        "s2": star("s2", {(3, 2): "s2"}),
    }
    endpoint_star_directions = 4 * 6 * 3
    require(sum(
        any(name.startswith("d") for name in term)
        for row in stars.values() for polynomial in row.values()
        for term in polynomial
    ) == endpoint_star_directions,
            "the endpoint-star direction count changed")

    top = matching_tensor(module, q_cells, SITES)
    responses = {}
    for left, right, label in (
            ("p1", "s1", "11"), ("p1", "s2", "12"),
            ("p2", "s1", "21"), ("p2", "s2", "22")):
        response = star_product(module, stars[left], stars[right], q_cells)
        direct = variable(TAU, f"dd{label}")
        for word, polynomial in top.items():
            response[word] = poly_add(
                response.get(word, Counter()), poly_mul(direct, polynomial)
            )
        responses[label] = response

    cofactor_03 = pure.pure_zero_cofactor(
        completion, module,
        {cell: tau_part(polynomial, 0)
         for cell, polynomial in q_cells.items() if tau_part(polynomial, 0)},
        frozenset((0, 3)))
    cofactor_12 = pure.pure_zero_cofactor(
        completion, module,
        {cell: tau_part(polynomial, 0)
         for cell, polynomial in q_cells.items() if tau_part(polynomial, 0)},
        frozenset((1, 2)))
    initial_12 = tau_part(responses["12"][CROSS12_WORD], 0)
    initial_21 = tau_part(responses["21"][CROSS21_WORD], 0)
    require(initial_12 == poly_mul(variable("p0", "s2"), cofactor_03),
            "the degree-zero 12 crossed initial changed")
    require(initial_21 == poly_mul(variable("p2", "s1"), cofactor_12),
            "the degree-zero 21 crossed initial changed")

    # Mixed-q directions cannot even enter these two selected words at first
    # order: their residual four-site word is pure 0.  Endpoint corrections
    # do enter, but only in tau degree one and hence cannot cancel a unit
    # constant coefficient.
    linear_12 = tau_part(responses["12"][CROSS12_WORD], 1)
    linear_21 = tau_part(responses["21"][CROSS21_WORD], 1)
    require(not any(name.startswith("m") for term in linear_12 for name in term)
            and not any(name.startswith("m") for term in linear_21
                        for name in term),
            "a mixed q direction entered a pure crossed word at order one")
    require(linear_12 and linear_21,
            "the endpoint correction layer unexpectedly vanished")

    # Import the exact pure-chart quotient statement.  Modulo the eight
    # degree-zero mixed-top rows and haf(z)=1:
    #   C03=z12*z45, C12=z03*z45, z03*z12*z45=1.
    # The star factors p0,s2,p2,s1 are units by the diagonal response anchors.
    ledger = {
        "dependencies": PINS,
        "rees_variables": {
            "offdiagonal_mixed_q": mixed_q_variables,
            "endpoint_star": endpoint_star_directions,
            "binary_direct": 4,
            "truncation": "mod tau^2",
        },
        "top_statistics": tensor_statistics(top),
        "response_statistics": {
            label: tensor_statistics(tensor)
            for label, tensor in responses.items()
        },
        "first_nonzero_associated_graded": {
            "order": 0,
            "12@100200": serial_polynomial(initial_12),
            "21@012000": serial_polynomial(initial_21),
            "pure_chart_reductions": {
                "C03": "z12*z45 (unit)",
                "C12": "z03*z45 (unit)",
                "unary": "z03*z12*z45=1",
            },
        },
        "order1_selected_words": {
            "12_terms": len(linear_12),
            "21_terms": len(linear_21),
            "mixed_q_terms": 0,
            "endpoint_or_direct_terms": len(linear_12) + len(linear_21),
        },
        "verdict": (
            "the two crossed response germs have unit tau-initial forms at "
            "degree zero, so the positive-filtration mixed-q, endpoint-star, "
            "and direct corrections cannot define a formal completion"
        ),
        "scope": (
            "all 90 offdiagonal residual q directions, all 72 endpoint-star "
            "directions, and four binary direct directions through tau order "
            "one around the arbitrary pure chart; new same-colour 11/22 q "
            "directions or negative-valuation/reselected charts are excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the mixed Rees ledger changed: {digest}")

    print("N=8 endpoint-minor mixed Rees first order: PASS")
    print("directions: mixed q 90, endpoint-star 72, binary direct 4")
    print("first nonzero crossed initials occur at tau order 0 and are units")
    print("mixed-q contributions to selected crossed words at order 1: 0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
