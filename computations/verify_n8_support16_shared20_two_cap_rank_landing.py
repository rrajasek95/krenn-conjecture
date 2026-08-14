#!/usr/bin/env python3
"""Two-cap rank landing for the sparsest support-16 directed orbit.

For representative B of degree sequence (6,4^5,3^2), the shared directed
source block X20 is invisible in its minimum cap-27 tensor but occurs in the
literal cap-23 and cap-25 responses.  In the exceptional anchor chart, those
responses split into two X20 terms and a 2x2 permanent on the complementary
anchor colours.

This checker proves a denominator-cleared rank-two construction.  If the
near vector w of X20 has nonzero direct-colour coordinate A, it constructs K
with w^T K=0, all three diagonal readouts nonzero, and the complementary
2x2 permanent zero.  The direct colours at caps 23 and 25 are distinct, so a
noncoordinate w has a nonzero direct coordinate for at least one cap.  Hence
one of the two independently typed cap covectors is actively clean.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "a97ff705d10246af9966732fe6e95f3e2b557fbdd1a68271327f80ed16b8f73d"
COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ORBIT = load_local(
    "n8_support16_source_orbits_for_shared20",
    "verify_n8_support16_directed_incidence_response_orbits.py",
)


def zero():
    return {}


def constant(value):
    return {} if value == 0 else {(0, 0, 0): value}


def variable(index):
    exponent = [0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): 1}


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def scale(polynomial, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        next_answer = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                monomial = tuple(a + b for a, b in zip(left, right))
                next_answer[monomial] += left_coefficient * right_coefficient
        answer = {monomial: coefficient
                  for monomial, coefficient in next_answer.items()
                  if coefficient}
    return answer


def rank_two_matrix(direct, first, second, chart):
    """Return the denominator-cleared matrix on A*w_chart != 0.

    Coordinates are A=w_direct, B=w_first, C=w_second.  The complementary
    2x2 block has diagonal entries D, upper entry D and lower entry -D, so
    its permanent is zero.  The direct column is completed so w^T K=0.
    """
    require((direct, first, second) in set(permutations(COLORS)),
            ("colour order is not a permutation", direct, first, second))
    require(chart in (first, second), ("bad localization chart", chart))
    w = tuple(variable(index) for index in COLORS)
    a, b, c = w[direct], w[first], w[second]
    matrix = [[zero() for _column in COLORS] for _row in COLORS]

    if chart == first:
        denominator = multiply(a, b)
        matrix[direct][direct] = denominator
        matrix[first][direct] = scale(multiply(a, a), -1)
        matrix[second][direct] = zero()
        matrix[direct][first] = multiply(b, add(c, scale(b, -1)))
        matrix[first][first] = denominator
        matrix[second][first] = scale(denominator, -1)
        matrix[direct][second] = scale(multiply(b, add(b, c)), -1)
        matrix[first][second] = denominator
        matrix[second][second] = denominator
    else:
        denominator = multiply(a, c)
        matrix[direct][direct] = denominator
        matrix[first][direct] = zero()
        matrix[second][direct] = scale(multiply(a, a), -1)
        matrix[direct][first] = multiply(c, add(c, scale(b, -1)))
        matrix[first][first] = denominator
        matrix[second][first] = scale(denominator, -1)
        matrix[direct][second] = scale(multiply(c, add(b, c)), -1)
        matrix[first][second] = denominator
        matrix[second][second] = denominator

    return matrix, denominator


def audit_symbolic_rank_construction():
    ledgers = []
    w = tuple(variable(index) for index in COLORS)
    for direct, first, second in permutations(COLORS):
        for chart in (first, second):
            matrix, denominator = rank_two_matrix(
                direct, first, second, chart
            )
            left_kernel = tuple(
                add(*(multiply(w[row], matrix[row][column])
                      for row in COLORS))
                for column in COLORS
            )
            require(left_kernel == (zero(), zero(), zero()),
                    ("w^T K did not vanish", direct, first, second, chart,
                     left_kernel))
            require(tuple(matrix[index][index] for index in COLORS)
                    == (denominator, denominator, denominator),
                    ("active diagonal readouts changed", direct, first,
                     second, chart, matrix))
            permanent = add(
                multiply(matrix[first][first], matrix[second][second]),
                multiply(matrix[first][second], matrix[second][first]),
            )
            require(permanent == zero(),
                    ("complementary permanent did not vanish", direct,
                     first, second, chart, permanent))
            require(matrix[direct][direct] == denominator,
                    ("direct scalar is not localized unit", direct, chart))
            ledgers.append({
                "direct_colour": direct,
                "complementary_colours": (first, second),
                "chart_coordinate": chart,
                "localized_diagonal": denominator,
                "left_kernel": left_kernel,
                "permanent": permanent,
            })
    require(len(ledgers) == 12,
            ("rank chart count changed", len(ledgers)))
    return tuple(ledgers)


def physical_shared20_pair():
    records = ORBIT.terminal_two_rrx_records()
    record = records[1]
    edges = tuple(record["representative_edges"])
    adjacency = ORBIT.adjacency_from_edges(edges)
    target = (2, (0, 2))
    occurrences = ORBIT.response_occurrences(adjacency, edges)[target]
    caps = tuple(sorted({item[0] for item in occurrences}))
    require(caps == ((2, 3), (2, 5)),
            ("literal shared20 cap pair changed", caps))

    faces = []
    for cap_edge in caps:
        expanded = ORBIT.expanded_response_monomials(
            adjacency, edges, cap_edge
        )
        through_target = tuple(
            item for item in expanded
            if ORBIT.contains_directed_star(item, target)
        )
        residue = tuple(
            item for item in expanded
            if not ORBIT.contains_directed_star(item, target)
        )
        require((len(expanded), len(through_target), len(residue)) == (4, 2, 2),
                ("shared20 response split changed", cap_edge, expanded))
        faces.append({
            "cap_edge": cap_edge,
            "factor_level_terms": tuple(
                ORBIT.monomial_names(term)
                for term in ORBIT.response_terms(adjacency, edges, cap_edge)
            ),
            "expanded_count": len(expanded),
            "through_X20": len(through_target),
            "companion_residue": len(residue),
        })
    return {
        "degree_sequence": record["degree_sequence"],
        "representative_edges": edges,
        "directed_source_incidence": target,
        "faces": tuple(faces),
    }


def enumerate_exceptional_anchor_completions(edges):
    """Enumerate the chart where only X02 and X35 are nonanchors.

    Fix colour zero on X23 to remove the three choices for that direct
    anchor.  Every other vertex must see all three coordinate anchor colours.
    """
    wildcards = {(0, 2), (3, 5)}
    anchor_edges = tuple(edge for edge in edges if edge not in wildcards)
    incident = {
        vertex: tuple(edge for edge in anchor_edges if vertex in edge)
        for vertex in range(8)
    }
    states = {(2, 3): 0}
    free_edges = tuple(edge for edge in anchor_edges if edge != (2, 3))
    completions = []

    def recurse(index):
        for vertex in range(8):
            seen = {states[edge] for edge in incident[vertex]
                    if edge in states}
            remaining = sum(edge not in states for edge in incident[vertex])
            if 3 - len(seen) > remaining:
                return
        if index == len(free_edges):
            if all({states[edge] for edge in incident[vertex]}
                   == set(COLORS) for vertex in range(8)):
                completions.append(tuple(sorted(states.items())))
            return
        edge = free_edges[index]
        for colour in COLORS:
            states[edge] = colour
            recurse(index + 1)
        del states[edge]

    recurse(0)
    require(len(completions) == 104,
            ("exceptional anchor completion count changed", len(completions)))

    face_ledgers = []
    for completion in completions:
        state = dict(completion)
        direct23 = state[(2, 3)]
        direct25 = state[(2, 5)]
        require(direct23 != direct25,
                ("two cap direct colours collided", completion))
        require({state[(2, 5)], state[(2, 7)]}
                == set(COLORS) - {direct23},
                ("cap23 row complement changed", completion))
        require({state[(0, 3)], state[(3, 6)]}
                == set(COLORS) - {direct23},
                ("cap23 column complement changed", completion))
        require({state[(2, 3)], state[(2, 7)]}
                == set(COLORS) - {direct25},
                ("cap25 row complement changed", completion))
        require({state[(0, 5)], state[(4, 5)]}
                == set(COLORS) - {direct25},
                ("cap25 column complement changed", completion))
        face_ledgers.append((direct23, direct25))
    direct_pair_histogram = Counter(face_ledgers)
    require(direct_pair_histogram == Counter({(0, 1): 52, (0, 2): 52}),
            ("direct cap-colour histogram changed", direct_pair_histogram))
    return {
        "fixed_direct_edge": ((2, 3), 0),
        "completion_count": len(completions),
        "direct_pair_histogram": tuple(sorted(direct_pair_histogram.items())),
        "first_completion": completions[0],
    }


def audit_two_cap_support_logic():
    """Check every noncoordinate support mask against two direct colours."""
    ledgers = []
    for direct_left, direct_right in permutations(COLORS, 2):
        for mask in range(1 << len(COLORS)):
            support = frozenset(
                colour for colour in COLORS if (mask >> colour) & 1
            )
            if len(support) < 2:
                continue
            usable = tuple(
                colour for colour in (direct_left, direct_right)
                if colour in support
            )
            require(usable,
                    ("noncoordinate vector missed both direct colours",
                     direct_left, direct_right, support))
            chosen = usable[0]
            complement = tuple(
                colour for colour in COLORS if colour != chosen
            )
            charts = tuple(colour for colour in complement if colour in support)
            require(charts,
                    ("chosen direct chart lost noncoordinate companion",
                     chosen, support))
            ledgers.append((
                (direct_left, direct_right), tuple(sorted(support)),
                chosen, charts[0],
            ))
    require(len(ledgers) == 24,
            ("two-cap support-mask count changed", len(ledgers)))
    return tuple(ledgers)


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    physical = physical_shared20_pair()
    ledger = canonical({
        "physical_shared20_pair": physical,
        "symbolic_rank_charts": audit_symbolic_rank_construction(),
        "exceptional_anchor_completions":
            enumerate_exceptional_anchor_completions(
                physical["representative_edges"]
            ),
        "two_cap_support_logic": audit_two_cap_support_logic(),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("shared20 two-cap rank ledger changed", digest))

    print("N=8 support-16 shared20 two-cap rank landing: PASS")
    print("  literal cap pair: 23 / 25")
    print("  each response: 2 X20 + 2 companion monomials")
    print("  denominator-cleared active rank charts: 12")
    print("  exceptional mutual-anchor completions: 104")
    print("  noncoordinate support masks closed: 24 / 24")
    print("  surviving local counterguard: none")


if __name__ == "__main__":
    main()
