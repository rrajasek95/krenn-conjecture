#!/usr/bin/env python3
"""Exact 112-variable coordinate audit for the 560 P_(3,3,2) quartics.

For every physical edge use the four difference-plane coordinates

    a=D(r,r), b=D(s,s), c=D(s-r,s-r), h=D(r,s)-D(s,r),

where r=e0-e1 and s=e0-e2.  The nine ordered bilinear forms between
r,s,s-r then have coefficients in (1/2) Z[a,b,c,h].  We store twice each
form, so sixteen times every quartic P_sigma is integral.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_p332_coordinate_interface.json"

N = 8
DIRECTIONS = (0, 1, 2)  # r, s, s-r
# Coefficients of 2 D(direction_left,direction_right) in (a,b,c,h).
TWICE_FORM = {
    (0, 0): (2, 0, 0, 0),
    (1, 1): (0, 2, 0, 0),
    (2, 2): (0, 0, 2, 0),
    (0, 1): (1, 1, -1, 1),
    (1, 0): (1, 1, -1, -1),
    (0, 2): (-1, 1, -1, 1),
    (2, 0): (-1, 1, -1, -1),
    (1, 2): (-1, 1, 1, 1),
    (2, 1): (-1, 1, 1, -1),
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in matchings(rest):
            yield ((u, v),) + tail


PM8 = tuple(matchings())
EDGES = tuple((u, v) for u in range(N) for v in range(u + 1, N))
EDGE_ID = {edge: i for i, edge in enumerate(EDGES)}


def variable(edge, coordinate):
    return 4 * EDGE_ID[edge] + coordinate


def quartic(assignment):
    """Return 16 P_sigma as an integral sparse polynomial."""
    answer = Counter()
    for matching in PM8:
        partial = Counter({(): 1})
        for edge in matching:
            form = TWICE_FORM[(assignment[edge[0]], assignment[edge[1]])]
            updated = Counter()
            for monomial, coefficient in partial.items():
                for coordinate, scalar in enumerate(form):
                    if scalar:
                        updated[tuple(sorted(monomial +
                                             (variable(edge, coordinate),)))] += (
                            coefficient * scalar
                        )
            partial = updated
        answer.update(partial)
    return Counter({row: value for row, value in answer.items() if value})


def raw_source_words(assignment):
    """The literal 256 mixed H_w rows and their signed coefficients."""
    vectors = ((1, -1, 0), (1, 0, -1), (0, 1, -1))
    words = Counter({(): 1})
    for direction in assignment:
        updated = Counter()
        for word, coefficient in words.items():
            for colour, scalar in enumerate(vectors[direction]):
                if scalar:
                    updated[word + (colour,)] += coefficient * scalar
        words = updated
    require(len(words) == 256, "raw source support is not 256")
    require(all(len(set(word)) > 1 for word in words),
            "a raw P332 source word is pure")
    return words


def evaluate(poly, values):
    return sum(coefficient
               * product(values[cell] for cell in monomial)
               for monomial, coefficient in poly.items())


def product(values):
    result = 1
    for value in values:
        result *= value
    return result


def direct_polarized_value(assignment, values):
    total = 0
    for matching in PM8:
        term = 1
        for edge in matching:
            form = TWICE_FORM[(assignment[edge[0]], assignment[edge[1]])]
            term *= sum(form[i] * values[variable(edge, i)]
                        for i in range(4))
        total += term
    return total


def main() -> None:
    require(len(PM8) == 105 and len(EDGES) == 28,
            "matching/edge census changed")
    require(set(TWICE_FORM) == set((i, j) for i in DIRECTIONS
                                   for j in DIRECTIONS),
            "bilinear table is incomplete")

    assignments = sorted(set(permutations((0, 0, 0, 1, 1, 1, 2, 2))))
    require(len(assignments) == 560, "P332 assignment orbit changed")
    probe_values = tuple(((17 * i + 5) % 23) - 11 for i in range(112))
    support_histogram = Counter()
    coefficient_histogram = Counter()
    polynomial_digests = []
    raw_digests = []
    raw_sign_histogram = Counter()
    for assignment in assignments:
        poly = quartic(assignment)
        raw = raw_source_words(assignment)
        require(evaluate(poly, probe_values)
                == direct_polarized_value(assignment, probe_values),
                "expanded quartic differs from direct bilinear evaluation")
        support_histogram[len(poly)] += 1
        coefficient_histogram.update(poly.values())
        raw_sign_histogram.update(raw.values())
        polynomial_digests.append(sha256(repr(sorted(poly.items())).encode()).hexdigest())
        raw_digests.append(sha256(repr(sorted(raw.items())).encode()).hexdigest())

    require(len(set(polynomial_digests)) == 560,
            "two labelled P332 assignments gave the same quartic")
    require(raw_sign_histogram == {-1: 71_680, 1: 71_680},
            "raw 256-row sign census changed")

    base = assignments[0]
    base_poly = quartic(base)
    mutated = base_poly.copy()
    mutated[min(mutated)] += 1
    require(evaluate(mutated, probe_values)
            != direct_polarized_value(base, probe_values),
            "coefficient mutation did not fire")

    result = {
        "status": "UNAUDITED exact 112-variable P332 coordinate interface",
        "coordinate_count": 112,
        "edge_count": 28,
        "coordinate_order_per_edge": ["a", "b", "c", "h"],
        "coordinate_definition": (
            "a=D(r,r), b=D(s,s), c=D(s-r,s-r), "
            "h=D(r,s)-D(s,r), r=e0-e1, s=e0-e2"
        ),
        "twice_bilinear_form_table": {
            f"{i}{j}": list(TWICE_FORM[(i, j)])
            for i in DIRECTIONS for j in DIRECTIONS
        },
        "generator_scaling": "stored quartic is 16*P_sigma",
        "generator_count": len(assignments),
        "generator_support_histogram": {
            str(k): v for k, v in sorted(support_histogram.items())
        },
        "all_generator_coefficient_histogram": {
            str(k): v for k, v in sorted(coefficient_histogram.items())
        },
        "raw_source_rows_per_generator": 256,
        "raw_source_sign_histogram": {
            str(k): v for k, v in sorted(raw_sign_histogram.items())
        },
        "distinct_generator_digests": len(set(polynomial_digests)),
        "generator_digest": sha256("".join(polynomial_digests).encode()).hexdigest(),
        "raw_source_digest": sha256("".join(raw_digests).encode()).hexdigest(),
        "probe_values_digest": sha256(repr(probe_values).encode()).hexdigest(),
        "direct_evaluation_checks": len(assignments),
        "coefficient_mutation_fires": True,
        "scope": (
            "Each generator is a signed combination of 256 literal mixed "
            "H_w rows, so J332 is a subideal of I_mix. A positive ideal "
            "certificate in these coordinates lifts after substituting the "
            "four linear contrast coordinates on every physical edge."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("P332 coordinate interface: PASS")
    print("support histogram:", dict(sorted(support_histogram.items())))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
