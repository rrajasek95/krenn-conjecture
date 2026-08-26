#!/usr/bin/env python3
"""Exact combinatorial guards for the singular normal-cone Gram system.

This does not solve the system.  It verifies the literal site/colour Euler
identity, the four-root blocker selector, and the unavoidable mixed-output
cokernel dimension used in REPORT.md.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_singular_normal_cone_gram_system.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def lagrange_delta(index, value):
    answer = Fraction(1)
    for other in range(4):
        if other != index:
            answer *= Fraction(value - other, index - other)
    return answer


def selector_guard():
    table = []
    for value in range(4):
        deltas = [lagrange_delta(index, value) for index in range(4)]
        require(deltas == [Fraction(index == value) for index in range(4)],
                (value, deltas))
        polynomial = value * (value - 1) * (value - 2) * (value - 3)
        require(polynomial == 0, (value, polynomial))
        table.append([int(item) for item in deltas])
    return {
        "selector_polynomial": "sigma(sigma-1)(sigma-2)(sigma-3)",
        "lagrange_delta_table": table,
        "auxiliary_selector_variables_per_carrier": 1,
        "gram_variables_per_carrier": 9,
    }


def site_colour_euler_guard():
    n = 8
    q = 3
    matchings = tuple(perfect_matchings(range(n)))
    require(len(matchings) == 105, len(matchings))
    words = tuple(product(range(q), repeat=n))
    checked_monomials = 0
    checked_weights = 0
    for word in words:
        for matching in matchings:
            selected = []
            for u, v in matching:
                selected.append((u, v, word[u], word[v]))
            require(len(selected) == 4, selected)
            checked_monomials += 1
            for site in range(n):
                incident = [cell for cell in selected
                            if cell[0] == site or cell[1] == site]
                require(len(incident) == 1, (word, matching, site, incident))
                u, v, i, j = incident[0]
                endpoint_colour = i if u == site else j
                for colour in range(q):
                    exponent = int(endpoint_colour == colour)
                    expected = int(word[site] == colour)
                    require(exponent == expected,
                            (word, matching, site, colour, exponent, expected))
                    checked_weights += 1

    # At the exact GHZ target, the vector selected by the (site, colour)
    # weighted Euler derivative is exactly the corresponding pure word.
    for site in range(n):
        for colour in range(q):
            nonzero = []
            for word in words:
                target = int(len(set(word)) == 1)
                coefficient = int(word[site] == colour) * target
                if coefficient:
                    nonzero.append(word)
            require(nonzero == [(colour,) * n], (site, colour, nonzero))

    return {
        "sites": n,
        "colours": q,
        "perfect_matchings": len(matchings),
        "output_words": len(words),
        "matching_monomials_checked": checked_monomials,
        "site_colour_weights_checked": checked_weights,
        "weighted_euler_target": (
            "D Phi_A[g_(v,c)(A)] has coordinate "
            "1_(w_v=c) Phi(A)_w and equals e_(c^8) on GHZ"
        ),
    }


def dimension_guard():
    source = 28 * 9
    output = 3 ** 8
    mixed = output - 3
    lower = mixed - source
    require((source, output, mixed, lower) == (252, 6561, 6558, 6306),
            (source, output, mixed, lower))
    return {
        "complex_source_dimension": source,
        "mixed_output_coordinates": mixed,
        "mixed_only_left_cokernel_lower_bound": lower,
        "conclusion": (
            "ker(J_mix^*) has dimension at least 6306 at every source; "
            "the alpha=0 output-multiplier branch remains tautological "
            "even after all three pure multiplier coordinates are removed"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-selector", action="store_true")
    args = parser.parse_args()

    selector = selector_guard()
    if args.mutate_selector:
        selector["lagrange_delta_table"][0][0] = 0
    require(selector["lagrange_delta_table"][0][0] == 1, selector)

    payload = {
        "status": "PASS exact Euler/selector/cokernel guards",
        "selector": selector,
        "site_colour_euler": site_colour_euler_guard(),
        "singular_multiplier_dimension": dimension_guard(),
        "scope": (
            "Combinatorial and linear-algebra guards only; no claim that the "
            "normal-cone plus blocker Gram system is inconsistent."
        ),
    }
    payload["logical_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("matchings", payload["site_colour_euler"]["perfect_matchings"])
    print("weights", payload["site_colour_euler"]["site_colour_weights_checked"])
    print("mixed cokernel lower bound",
          payload["singular_multiplier_dimension"]["mixed_only_left_cokernel_lower_bound"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
