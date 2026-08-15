#!/usr/bin/env python3
"""Audit the tail-stable permanent-triangle unit lemma.

The local source packet has two row sites, three column sites and one hub.
One colour supports the K_2,3 matrix and a second colour supports the three
hub spokes.  Any number of disjoint, forced decorated tail edges may be
adjoined.  The three mixed coefficient rows are the three 2-by-2 permanents
times their forced spoke and common tail.  Their universal syzygy has twice
a support monomial on the right.

The checker also freezes a sharp contamination counterguard: merely
containing the K_2,3 support minor is insufficient.  Adding one extra
same-colour matching to one of the three word fibres gives a torus point at
which all three contaminated rows vanish.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import json


EXPECTED_LEDGER_SHA256 = "fc6821a5ff6140cc76e2769916c17c7115445fa1419a9bd708c6e7abd70f6176"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def normalize(source):
    return {tuple(sorted(monomial)): coefficient
            for monomial, coefficient in source.items() if coefficient}


def monomial(*variables):
    return {tuple(sorted(variables)): 1}


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return normalize(answer)


def scale(coefficient, polynomial):
    return normalize({term: coefficient * value
                      for term, value in polynomial.items()})


def multiply(*polynomials):
    answer = {(): 1}
    for polynomial in polynomials:
        following = Counter()
        for left, left_value in answer.items():
            for right, right_value in polynomial.items():
                following[tuple(sorted(left + right))] += (
                    left_value * right_value)
        answer = normalize(following)
    return answer


def evaluate(polynomial, values):
    return sum(coefficient
               * product_values(tuple(values[name] for name in term))
               for term, coefficient in polynomial.items())


def product_values(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def hafnian_coefficient(word, support):
    """Exact sparse hafnian coefficient in one literal output word."""

    memo = {(): {(): 1}}

    def recurse(vertices):
        vertices = tuple(vertices)
        if vertices in memo:
            return memo[vertices]
        pivot = vertices[0]
        answer = {}
        for position in range(1, len(vertices)):
            partner = vertices[position]
            if word[pivot] != word[partner]:
                continue
            cell = support.get((edge(pivot, partner), word[pivot]))
            if cell is None:
                continue
            rest = vertices[1:position] + vertices[position + 1:]
            answer = add(answer,
                         multiply(monomial(cell), recurse(rest)))
        memo[vertices] = answer
        return answer

    return recurse(tuple(range(len(word))))


def clean_packet(order):
    require(order >= 6 and order % 2 == 0, order)
    r, s, x, y, z, hub = range(6)
    support = {
        (edge(r, x), 0): "a",
        (edge(r, y), 0): "b",
        (edge(r, z), 0): "c",
        (edge(s, x), 0): "d",
        (edge(s, y), 0): "e",
        (edge(s, z), 0): "f",
        (edge(hub, x), 1): "p_x",
        (edge(hub, y), 1): "p_y",
        (edge(hub, z), 1): "p_z",
    }
    tail_variables = []
    for index, left in enumerate(range(6, order, 2)):
        name = f"t_{index}"
        support[edge(left, left + 1), 2] = name
        tail_variables.append(name)

    pairs = ((x, y, z), (x, z, y), (y, z, x))
    words = []
    rows = []
    for first, second, omitted in pairs:
        word = [2] * order
        for vertex in (r, s, first, second):
            word[vertex] = 0
        for vertex in (hub, omitted):
            word[vertex] = 1
        words.append(tuple(word))
        rows.append(hafnian_coefficient(tuple(word), support))

    tau = monomial(*tail_variables)
    u_xy = multiply(tau, monomial("p_z"))
    u_xz = multiply(tau, monomial("p_y"))
    u_yz = multiply(tau, monomial("p_x"))
    expected = (
        multiply(u_xy, add(monomial("a", "e"), monomial("b", "d"))),
        multiply(u_xz, add(monomial("a", "f"), monomial("c", "d"))),
        multiply(u_yz, add(monomial("b", "f"), monomial("c", "e"))),
    )
    require(tuple(rows) == expected, (order, rows, expected))

    first, second, third = rows
    lhs = add(
        multiply(monomial("c"), u_xz, u_yz, first),
        multiply(monomial("b"), u_xy, u_yz, second),
        scale(-1, multiply(monomial("a"), u_xy, u_xz, third)),
    )
    rhs = scale(2, multiply(
        monomial("b", "c", "d"), u_xy, u_xz, u_yz))
    require(lhs == rhs and len(rhs) == 1, (order, lhs, rhs))
    rhs_term, rhs_coefficient = next(iter(rhs.items()))
    require(rhs_coefficient == 2, (order, rhs))

    return {
        "order": order,
        "common_tail_edges": (order - 6) // 2,
        "row_term_counts": [len(row) for row in rows],
        "row_monomial_degrees": [len(next(iter(row))) for row in rows],
        "words": ["".join(map(str, word)) for word in words],
        "certificate_rhs_coefficient": rhs_coefficient,
        "certificate_rhs_degree": len(rhs_term),
    }


def generic_identity():
    first = add(monomial("a", "e"), monomial("b", "d"))
    second = add(monomial("a", "f"), monomial("c", "d"))
    third = add(monomial("b", "f"), monomial("c", "e"))
    lhs = add(multiply(monomial("c"), first),
              multiply(monomial("b"), second),
              scale(-1, multiply(monomial("a"), third)))
    rhs = scale(2, monomial("b", "c", "d"))
    require(lhs == rhs, (lhs, rhs))
    return {
        "identity": "c(ae+bd)+b(af+cd)-a(bf+ce)=2bcd",
        "matrix_variables": 6,
        "minor_rows": 3,
        "active_sites_with_completion_hub": 6,
        "valid_characteristic": "not 2",
    }


def contamination_counterguard():
    # A K_2,3 support minor by itself does not isolate the three source rows.
    # Give the first minor a third compatible matching g*k.  The following
    # all-unit assignment kills the three contaminated rows exactly.
    r, s, x, y, z, hub = range(6)
    support = {
        (edge(r, x), 0): "a", (edge(r, y), 0): "b",
        (edge(r, z), 0): "c", (edge(s, x), 0): "d",
        (edge(s, y), 0): "e", (edge(s, z), 0): "f",
        (edge(hub, x), 1): "p_x", (edge(hub, y), 1): "p_y",
        (edge(hub, z), 1): "p_z",
        (edge(r, s), 0): "g", (edge(x, y), 0): "k",
    }
    words = (
        (0, 0, 0, 0, 1, 1),
        (0, 0, 0, 1, 0, 1),
        (0, 0, 1, 0, 0, 1),
    )
    literal_rows = tuple(hafnian_coefficient(word, support) for word in words)
    expected_rows = (
        multiply(monomial("p_z"), add(
            monomial("a", "e"), monomial("b", "d"),
            monomial("g", "k"))),
        multiply(monomial("p_y"), add(
            monomial("a", "f"), monomial("c", "d"))),
        multiply(monomial("p_x"), add(
            monomial("b", "f"), monomial("c", "e"))),
    )
    require(literal_rows == expected_rows, (literal_rows, expected_rows))

    values = {
        "a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": -1,
        "g": 1, "k": -2, "p_x": 1, "p_y": 1, "p_z": 1,
    }
    row_names = ("E_xy_contaminated", "E_xz", "E_yz")
    rows = {name: evaluate(row, values)
            for name, row in zip(row_names, literal_rows, strict=True)}
    require(all(value != 0 for value in values.values()), values)
    require(set(rows.values()) == {0}, rows)
    return {
        "extra_matching_monomial": "g*k in the xy word",
        "literal_source_words": ["".join(map(str, word)) for word in words],
        "literal_row_term_counts": [len(row) for row in literal_rows],
        "all_unit_solution": values,
        "row_values": rows,
        "conclusion": (
            "an uncoloured K_2,3/theta minor or terminal ear does not force "
            "the unit; word-filtered two-occurrence isolation is essential"
        ),
    }


def doubled_k4_support28_instance():
    # Canonical support-28 variables, with row sites 0,3; column sites
    # 1,2,5; completion hub 4; and physical tail edge 67.  The tail edge is
    # common physically but its source decoration is allowed to vary by row.
    a, b, c = "x_01^1", "x_02^1", "x_05^1"
    d, e, f = "x_13^1", "x_23^1", "x_35^1"
    u_xy = monomial("x_45^0", "x_67^2")
    u_xz = monomial("x_24^2", "x_67^0")
    u_yz = monomial("x_14^0", "x_67^2")
    rows = (
        multiply(u_xy, add(monomial(a, e), monomial(b, d))),
        multiply(u_xz, add(monomial(a, f), monomial(c, d))),
        multiply(u_yz, add(monomial(b, f), monomial(c, e))),
    )
    lhs = add(
        multiply(monomial(c), u_xz, u_yz, rows[0]),
        multiply(monomial(b), u_xy, u_yz, rows[1]),
        scale(-1, multiply(monomial(a), u_xy, u_xz, rows[2])),
    )
    rhs = scale(2, multiply(monomial(b, c, d), u_xy, u_xz, u_yz))
    require(lhs == rhs and len(rhs) == 1, (lhs, rhs))
    return {
        "row_sites": [0, 3],
        "column_sites": [1, 2, 5],
        "completion_hub": 4,
        "physical_tail_edge": [6, 7],
        "words": ["11110022", "11212100", "10110122"],
        "tail_decorations_may_vary": True,
        "row_term_counts": [len(row) for row in rows],
        "certificate_rhs_coefficient": next(iter(rhs.values())),
    }


def audit():
    orders = tuple(range(6, 16, 2))
    ledger = {
        "theorem": "tail-stable source-labelled permanent-triangle unit",
        "generic_identity": generic_identity(),
        "literal_clean_packets": [clean_packet(order) for order in orders],
        "arbitrary_order_schema": {
            "orders": "N=6+2q for every q>=0",
            "common_tail": (
                "a forced decorated perfect-matching monomial tau on the "
                "2q spectator sites"
            ),
            "three_row_form": [
                "F_xy=tau*p_z*(a*e+b*d)",
                "F_xz=tau*p_y*(a*f+c*d)",
                "F_yz=tau*p_x*(b*f+c*e)",
            ],
            "certificate": (
                "c*U_xz*U_yz*F_xy + b*U_xy*U_yz*F_xz "
                "- a*U_xy*U_xz*F_yz = "
                "2*b*c*d*U_xy*U_xz*U_yz"
            ),
        },
        "support28_doubled_K4_instance": doubled_k4_support28_instance(),
        "forcing_hypotheses": {
            "bright_core": (
                "six nonzero same-colour cells form K_2,3 between two "
                "row sites and three column sites"
            ),
            "completion": (
                "one hub has a nonzero compatible spoke to each omitted "
                "column, and the remaining even sites have a common "
                "decorated perfect-matching tail"
            ),
            "mixedness": "each of the three completed output words is mixed",
            "word_isolation": (
                "in each completed word the only supported perfect matchings "
                "are the two K_2,2 pairings times the forced spoke and tail"
            ),
            "unit_localization": "every displayed core, spoke and tail cell is nonzero",
        },
        "counterguard": contamination_counterguard(),
        "scope": (
            "the lemma is uniform and source-labelled, but terminality or an "
            "uncoloured theta/K_2,3 minor alone does not imply word isolation; "
            "a private-tail/cofactor-isolation theorem is the exact forcing datum"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
        return
    print("uniform permanent-triangle common-tail lemma: PASS")
    print("orders", [row["order"] for row in ledger["literal_clean_packets"]])
    print("row term counts", ledger["literal_clean_packets"][-1]
          ["row_term_counts"])
    print("contaminated-minor torus counterguard", ledger["counterguard"]
          ["row_values"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
