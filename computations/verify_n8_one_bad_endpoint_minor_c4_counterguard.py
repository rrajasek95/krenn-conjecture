#!/usr/bin/env python3
"""Exact common-q guard to endpoint-minor => alternating-C4 activation.

The four binary one-bad response rows do not by themselves force the two
endpoint rows to be proportional.  More sharply, a literal common-q packet
has rank-two endpoint port matrices while every nonzero coloured-port minor
is invisible to its corresponding hafnian cofactor.  Thus the first
alternating-C4 term in the private-site identity is absent.

The packet is the exact eight-of-nine guard from the multisite-cap audit.  It
is not a full one-bad packet: q^[3]=0 rather than X0, and a response-invisible
star component is removable.  The point of this checker is only to pin the
third, cofactor-invisible branch which a source-valid dichotomy must exclude
using the unary top or a minimum-support/source modification argument.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_hafnian_private_site_matching_bijection_lemma.py":
        "310167f3f51cdbf7619497662b29b267f2d34de4c7e67c00110dba55d4c77efc",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = (
    "bd6e7d90aacd2b7592dc467c0f612b6108176868769c310db1d15b85eb578eea"
)

SITES = tuple(range(8))
COLOURS = tuple(range(3))
P_ENDPOINT = 6
Q_ENDPOINT = 7
Port = tuple[int, int]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_guard():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")
    path = ROOT / "computations/verify_n8_one_bad_multisite_permanent_null_defect.py"
    spec = spec_from_file_location("multisite_guard", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_packet(module):
    q_cells = Counter({
        module.source_cell(2, 4, 1, 1): Fraction(1),
        module.source_cell(3, 5, 1, 1): Fraction(1),
        module.source_cell(0, 5, 2, 2): Fraction(1),
        module.source_cell(1, 4, 2, 2): Fraction(1),
    })
    e1 = (Fraction(0), Fraction(1), Fraction(0))
    e2 = (Fraction(0), Fraction(0), Fraction(1))
    stars = {
        "p1": {0: e1, 5: e1},
        "p2": {2: e2},
        "s1": {1: e1},
        "s2": {3: e2},
    }
    blocks = Counter(q_cells)
    for name, label, endpoint in (
            ("p1", 1, P_ENDPOINT), ("p2", 2, P_ENDPOINT),
            ("s1", 1, Q_ENDPOINT), ("s2", 2, Q_ENDPOINT)):
        for site, vector in stars[name].items():
            for colour, value in enumerate(vector):
                if value:
                    blocks[module.source_cell(
                        endpoint, site, label, colour
                    )] += value
    return q_cells, stars, blocks


def port_row(module, blocks, endpoint, label):
    other_sites = tuple(site for site in SITES if site != endpoint)
    return {
        (site, colour): blocks.get(
            module.source_cell(endpoint, site, label, colour), Fraction(0)
        )
        for site in other_sites for colour in COLOURS
    }


def nonzero_minors(left, right):
    ports = tuple(sorted(left))
    answer = []
    for index, first in enumerate(ports):
        for second in ports[index + 1:]:
            determinant = (left[first] * right[second]
                           - right[first] * left[second])
            if determinant:
                answer.append((first, second, determinant))
    return tuple(answer)


def visible_cofactor_terms(module, blocks, endpoint, reference, alternate):
    """C_alternate terms compatible with the fixed colour at reference."""
    reference_site, reference_colour = reference
    alternate_site, _alternate_colour = alternate
    vertices = tuple(site for site in SITES
                     if site not in (endpoint, alternate_site))
    tensor = module.matching_tensor(blocks, vertices)
    reference_position = vertices.index(reference_site)
    visible = Counter({
        word: coefficient for word, coefficient in tensor.items()
        if word[reference_position] == reference_colour
    })
    return vertices, tensor, visible


def oriented_minor_audit(module, blocks, endpoint, left, right):
    minors = nonzero_minors(left, right)
    oriented = []
    for first, second, determinant in minors:
        for reference, alternate, signed in (
                (first, second, determinant),
                (second, first, -determinant)):
            vertices, cofactor, visible = visible_cofactor_terms(
                module, blocks, endpoint, reference, alternate
            )
            require(not visible,
                    "a nonzero endpoint minor acquired an active cofactor")
            oriented.append({
                "reference_port": list(reference),
                "alternate_port": list(alternate),
                "minor": str(signed),
                "cofactor_vertices": list(vertices),
                "cofactor_words": {
                    "".join(map(str, word)): str(coefficient)
                    for word, coefficient in sorted(cofactor.items())
                },
                "reference_colour_compatible_terms": 0,
            })
    return minors, oriented


def rank_two(row1, row2):
    columns = tuple(sorted(row1))
    matrix = [[row1[column] for column in columns],
              [row2[column] for column in columns]]
    return 2 if any(
        matrix[0][i] * matrix[1][j] - matrix[1][i] * matrix[0][j]
        for i in range(len(columns)) for j in range(i + 1, len(columns))
    ) else (1 if any(matrix[0]) or any(matrix[1]) else 0)


def main():
    module = load_guard()
    q_cells, stars, blocks = source_packet(module)

    # These are literal common-q cofactors, not independent formal tensors.
    rows = module.response_rows({
        "a": stars["p1"], "b": stars["p2"],
        "c": stars["s1"], "d": stars["s2"],
    }, q_cells)
    pure1 = module.pure(1)
    pure2 = module.pure(2)
    require(rows == {"11": pure1, "12": Counter(),
                     "21": Counter(), "22": pure2},
            "the four common-q response rows changed")
    require(module.matching_tensor(q_cells, tuple(range(6))) == Counter(),
            "the exact missing unary top unexpectedly appeared")
    full_tensor = module.matching_tensor(blocks, SITES)
    require(full_tensor == Counter({(1,) * 8: Fraction(1),
                                    (2,) * 8: Fraction(1)}),
            "the eight-site partial source tensor changed")

    p1 = port_row(module, blocks, P_ENDPOINT, 1)
    p2 = port_row(module, blocks, P_ENDPOINT, 2)
    s1 = port_row(module, blocks, Q_ENDPOINT, 1)
    s2 = port_row(module, blocks, Q_ENDPOINT, 2)
    p_minors, p_oriented = oriented_minor_audit(
        module, blocks, P_ENDPOINT, p1, p2
    )
    s_minors, s_oriented = oriented_minor_audit(
        module, blocks, Q_ENDPOINT, s1, s2
    )
    require(rank_two(p1, p2) == rank_two(s1, s2) == 2,
            "an endpoint port matrix lost rank two")
    require(p_minors == (
        ((0, 1), (2, 2), Fraction(1)),
        ((2, 2), (5, 1), Fraction(-1)),
    ), f"the P endpoint minor list changed: {p_minors}")
    require(s_minors == (
        ((1, 1), (3, 2), Fraction(1)),
    ), f"the Q endpoint minor list changed: {s_minors}")
    require(len(p_oriented) + len(s_oriented) == 6,
            "the oriented determinant census changed")

    # The canonical permanent-null cap is not clean on the unreduced packet.
    old_guard = module.exact_response_guard()
    require(old_guard["cap_sectors"]["R^[2]*q"] == {"111211": "2"},
            "the exact repeated-label cap defect changed")
    incidence = old_guard["eight_site_incidence_audit"]
    require(not any(pair == [3, 3]
                    for pair in incidence["deleted_star_rank_pairs"].values()),
            "the guard unexpectedly acquired a doubly-good arm")
    require(incidence["arm_activity"]["6-5"] is False,
            "the response-invisible defect arm became active")

    ledger = {
        "dependencies": PINS,
        "literal_packet": {
            "common_q_cells": 4,
            "endpoint_star_cells": 5,
            "responses": {"11": "X1", "12": "0",
                          "21": "0", "22": "X2"},
            "unary_top": "q^[3]=0 (the required X0 row is absent)",
            "eight_site_tensor": "X1+X2",
        },
        "endpoint_port_ranks": {"P": 2, "Q": 2},
        "nonzero_unordered_minors": {
            "P": [[list(first), list(second), str(value)]
                  for first, second, value in p_minors],
            "Q": [[list(first), list(second), str(value)]
                  for first, second, value in s_minors],
        },
        "oriented_private_site_tests": {
            "P": p_oriented, "Q": s_oriented,
        },
        "first_c4_verdict": (
            "all six orientations of the three nonzero coloured-port "
            "minors have zero compatible common cofactor; hence no literal "
            "alternating-C4 term is active"
        ),
        "canonical_cap": {
            "raw_repeated_label_defect": "R^[2]q=2*[111211]",
            "doubly_good_arms": 0,
            "inactive_defect_arm": "P5",
        },
        "structural_dichotomy": (
            "four common-q response rows have a third branch: endpoint "
            "minors may be nonzero but cofactor-invisible.  Therefore "
            "crossed-zero plus diagonal targets alone do not imply "
            "proportional stars or an active alternating-C4/OO overlap"
        ),
        "scope": (
            "exact ordinary common-q source packet for all four binary "
            "responses, but not a full one-bad packet or Krenn source; the "
            "sole failed full-nine row is q^[3]=X0, and deleting the "
            "response-invisible P5 component restores the clean-cap branch"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"endpoint-minor/C4 ledger changed: {digest}")

    print("N=8 one-bad endpoint-minor/C4 counterguard: PASS")
    print("four common-q responses: exact")
    print("endpoint port ranks: P=2, Q=2; nonzero minors: 3")
    print("active compatible alternating-C4 cofactors: 0/6 orientations")
    print("missing full-nine row: q^[3]=X0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
