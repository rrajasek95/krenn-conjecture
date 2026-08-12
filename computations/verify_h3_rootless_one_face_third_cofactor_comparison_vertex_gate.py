#!/usr/bin/env python3
"""One-face third-cofactor attempt at the rootless comparison vertex.

Fix v=1 and the selected C5 complement N=23|45.  Coarsely, the formal
third-cofactor proper-face tail has rows (-lower,-anchor,0,0,0), while the
target-normalized unary lift x has (+lower,-anchor,0,0,0).  Their half-sum
is therefore a formal primitive relative generator.

This checker shows why it is not the physical base C_v-x.  The selected
fourth operator sends the mixed source equation to 1 but sends the pure
unary equation underlying x to 0.  The physical/zero-endpoint bridge leaves
the primitive ridge

  Omega_1=(a67_22-a67_00)-(a01_01-a01_00).

Even granting a clean adjacent comparison edge, no scalar multiple of the
edge C_1-C_3 kills Omega_1: cancelling its Omega_1 entry leaves the rootless
r_1-r_3 entries and Omega_3.  Before homogenizing, the formal Hasse cube is
squarefree (4K2) whereas the adjacent edge is repeated-site P3+K2.  After
polynomial homogenization the literal source words still differ, so the
unit/descent obstruction remains.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "21ad8ab579d066f20260df7e7a93dadabd72133a5e16ebe81e70d777465d7f7f"
PINS = {
    "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py":
        "7abab46d3ae648dd309c2fec3266e70dec5b95c5fd150fea2c8c6035840e9bd3",
    "computations/verify_h3_rootless_cyclic_comparison_target_normalized_transfer_gate.py":
        "532d9d84cc1e4410d32e904d9ad36ec5c3c56b83a39f0d43641b19a085c02570",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
}

SITES = tuple(range(8))
X = 0
V = 1
P = 6
Q_SITE = 7
PHYSICAL_WORD = (0, 1, 2, 1, 1, 2, 2, 2)
PURE_WORD = (0,) * 8
CHART_WORD = (0, 0, 2, 1, 1, 2, 0, 0)
N = ((2, 3), (4, 5))
FORBIDDEN = (3, 6)
AUG_ROWS = ("lower", "ainc", "W", "target", "ores")
RIDGE_ROWS = ("Omega_1", "r_1", "Omega_3", "r_3")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(*columns):
    return tuple(sum(column[index] for column in columns)
                 for index in range(len(columns[0])))


def scale(coefficient, column):
    coefficient = Q(coefficient)
    return tuple(coefficient * Q(value) for value in column)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        edge = tuple(sorted((first, second)))
        rest = tuple(site for site in vertices if site not in edge)
        for tail in perfect_matchings(rest):
            answer.append((edge,) + tail)
    return tuple(answer)


def cell(edge, word):
    left, right = edge
    return f"a{left}{right}_{word[left]}{word[right]}"


def hafnian_monomials(word):
    answer = set()
    for matching in perfect_matchings(SITES):
        if FORBIDDEN in matching:
            continue
        answer.add(tuple(sorted(cell(edge, word) for edge in matching)))
    return answer


def derivative(monomials, variables):
    variables = tuple(variables)
    answer = set()
    for monomial in monomials:
        terms = list(monomial)
        for variable in variables:
            if variable not in terms:
                break
            terms.remove(variable)
        else:
            answer.add(tuple(terms))
    return answer


def site_profile(edges):
    answer = [0] * 8
    for left, right in edges:
        answer[left] += 1
        answer[right] += 1
    return tuple(answer)


def canonical_cube_and_unit():
    physical = hafnian_monomials(PHYSICAL_WORD)
    pure = hafnian_monomials(PURE_WORD)
    chart = hafnian_monomials(CHART_WORD)
    require(len(physical) == len(pure) == len(chart) == 90,
            "direct-free hafnian term count changed")

    edges = ((P, Q_SITE), (X, V), *N)
    physical_marked = tuple(cell(edge, PHYSICAL_WORD) for edge in edges)
    chart_marked = tuple(cell(edge, CHART_WORD) for edge in edges)
    expected_physical = ("a67_22", "a01_01", "a23_21", "a45_12")
    expected_chart = ("a67_00", "a01_00", "a23_21", "a45_12")
    require(physical_marked == expected_physical,
            ("physical marked cells changed", physical_marked))
    require(chart_marked == expected_chart,
            ("chart marked cells changed", chart_marked))

    unit = {()}
    require(derivative(physical, physical_marked) == unit,
            "selected fourth derivative of H_m stopped being 1")
    require(derivative(chart, chart_marked) == unit,
            "zero-endpoint chart top stopped being the same unit")
    require(not derivative(pure, physical_marked),
            "physical fourth operator stopped killing the pure unary row")

    # The two internal ridges agree.  The two endpoint ridges give Omega_1.
    physical_ridges = []
    chart_ridges = []
    for omitted in range(4):
        p_variables = tuple(variable for index, variable in
                            enumerate(physical_marked) if index != omitted)
        c_variables = tuple(variable for index, variable in
                            enumerate(chart_marked) if index != omitted)
        p_ridge = derivative(physical, p_variables)
        c_ridge = derivative(chart, c_variables)
        require(p_ridge == {(physical_marked[omitted],)}
                and c_ridge == {(chart_marked[omitted],)},
                ("codimension-one ridge changed", omitted))
        physical_ridges.append(physical_marked[omitted])
        chart_ridges.append(chart_marked[omitted])
    require(physical_ridges[2:] == chart_ridges[2:],
            "internal matching ridges stopped agreeing")
    omega = {
        physical_ridges[0]: 1,
        chart_ridges[0]: -1,
        physical_ridges[1]: -1,
        chart_ridges[1]: 1,
    }
    require(omega == {
        "a67_22": 1, "a67_00": -1,
        "a01_01": -1, "a01_00": 1,
    }, "Omega_1 labels/signs changed")

    return {
        "face": V,
        "matching": [list(edge) for edge in N],
        "physical_word": "".join(map(str, PHYSICAL_WORD)),
        "zero_endpoint_chart_word": "".join(map(str, CHART_WORD)),
        "pure_unary_word": "".join(map(str, PURE_WORD)),
        "physical_marked_cells": list(physical_marked),
        "chart_marked_cells": list(chart_marked),
        "fourth_operator_on_H_m": 1,
        "fourth_operator_on_H_0_minus_u": 0,
        "primitive_bridge": omega,
    }


def coarse_candidate():
    # Formal tail: d=-Eq and physical anchor -1.  Target-normalized x:
    # d=+Eq and physical anchor -1.  Only after forgetting source word,
    # fine Hasse degree, and descent may they be added.
    tail = (Q(-1), Q(-1), Q(0), Q(0), Q(0))
    x = (Q(1), Q(-1), Q(0), Q(0), Q(0))
    candidate = scale(Q(1, 2), add(tail, x))
    require(candidate == (Q(0), Q(-1), Q(0), Q(0), Q(0)),
            "coarse half-sum stopped having the primitive signature")

    # The selected fourth-operator connecting value is linear.  It is 1 on
    # the formal tail and zero on x and every honest source-chain edge.
    descent_values = {"formal_tail": Q(1), "x": Q(0),
                      "one_adjacent_edge": Q(0)}
    candidate_descent = Q(1, 2) * (
        descent_values["formal_tail"] + descent_values["x"]
    )
    require(candidate_descent == Q(1, 2),
            "source-ideal unit unexpectedly cancelled")
    return {
        "row_order": list(AUG_ROWS),
        "formal_tail": [str(value) for value in tail],
        "target_normalized_x": [str(value) for value in x],
        "formal_half_sum": [str(value) for value in candidate],
        "coarse_signature_is_desired": True,
        "source_valid": False,
        "selected_fourth_operator_value": str(candidate_descent),
        "reason": (
            "x and a source-valid adjacent edge have connecting value zero; "
            "they cannot cancel Psi_I(H_m)=1 from the formal tail"
        ),
    }


def one_adjacent_edge_gate():
    # In the most favorable strict quotient, the candidate leaves +Omega_1.
    # A clean edge is C_1-C_3=(Omega_1-r_1)-(Omega_3-r_3).
    candidate = (Q(1), Q(0), Q(0), Q(0))
    edge = (Q(1), Q(-1), Q(-1), Q(1))

    # Solve candidate + alpha*edge=0.  Omega_1 forces alpha=-1, after which
    # three primitive coordinates remain.
    alpha = Q(-1)
    remainder = add(candidate, scale(alpha, edge))
    require(remainder == (Q(0), Q(1), Q(1), Q(-1)),
            ("one-edge transfer remainder changed", remainder))
    require(any(remainder), "one adjacent edge killed a single vertex")
    return {
        "row_order": list(RIDGE_ROWS),
        "candidate_bridge": [int(value) for value in candidate],
        "clean_adjacent_edge_C1_minus_C3": [int(value) for value in edge],
        "coefficient_for_Omega1_cancellation": str(alpha),
        "remaining_rows": [int(value) for value in remainder],
        "interpretation": (
            "the edge transfers the defect to Omega_3 and leaves r_1-r_3; "
            "it is a difference, not a vertex nullhomotopy"
        ),
        "literal_physical_edge_has_additional_pure_Eq_defect": True,
    }


def fine_grade_and_word_gate():
    marked_edges = ((6, 7), (0, 1), (2, 3), (4, 5))
    hasse_profile = site_profile(marked_edges)
    require(hasse_profile == (1,) * 8,
            "selected Hasse top stopped being squarefree 4K2")

    first_tor_edges = ((1, 2), (2, 3), (4, 5))
    first_tor_profile = site_profile(first_tor_edges)
    require(first_tor_profile[1:6] == (1, 2, 1, 1, 1),
            "adjacent C1-C3 edge stopped having P3+K2 profile")

    # Homogenize the selected internal N=bd to M=abcde by ace.  The cell
    # multidegrees can then be matched by also multiplying x by pq:22,xv:01,
    # but polynomial multiplication never changes the source equation word.
    cycle_edges = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))
    common_tail_profile = site_profile(((6, 7), (0, 1), *cycle_edges))
    require(common_tail_profile == (1, 3, 2, 2, 2, 2, 1, 1),
            "common homogenized cell profile changed")
    require(len({PHYSICAL_WORD, CHART_WORD, PURE_WORD}) == 3,
            "physical/chart/pure source words collided")
    return {
        "formal_Hasse_top_type": "4K2, squarefree on all eight sites",
        "formal_Hasse_site_profile": list(hasse_profile),
        "adjacent_first_Tor_type": "P3+K2 on odd sites",
        "adjacent_first_Tor_odd_profile": list(first_tor_profile[1:6]),
        "polynomial_common_multiple_exists": True,
        "common_multiplier_profile": list(common_tail_profile),
        "word_labels_after_homogenization": {
            "mixed_H_m": "01211222",
            "zero_endpoint_chart": "00211200",
            "pure_unary_x": "00000000",
        },
        "word_change_supplied_by_multiplication_or_adjacent_edge": False,
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    ledger = {
        "theorem": "one-face third-cofactor comparison-vertex gate",
        "canonical_literal_cube": canonical_cube_and_unit(),
        "coarse_formal_candidate": coarse_candidate(),
        "single_adjacent_edge": one_adjacent_edge_gate(),
        "fine_grade_and_source_word": fine_grade_and_word_gate(),
        "complete_response_alternative": {
            "bar_boundary": "-Omega_1+q_(1,N)",
            "q_(1,N)": "a23_21*a45_12",
            "clean_minus_Omega_only_in_current_literal_module": False,
        },
        "verdict": (
            "the half-sum of x and the formal Hasse tail has the desired "
            "coarse anchor signature, but is not physical.  It retains the "
            "primitive selected-fourth-operator value 1/2, the endpoint "
            "ridge Omega_1, and a mixed source-word label.  One adjacent "
            "edge merely transfers Omega_1 to face 3 and adds rootless ridge "
            "rows; the complete colour-bar route instead leaves q_(1,N)"
        ),
        "smallest_new_datum": (
            "a source-labelled same-word comparison at one face which kills "
            "both the fourth-operator connecting class and Omega_1 while "
            "retaining/cancelling its all-D companion in the repeated grade"
        ),
        "scope": (
            "one canonical face v=1,N=23|45; cyclic symmetry gives the other "
            "faces, but no cyclic averaging is used in the proof"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless one-face third-cofactor comparison: OBSTRUCTED")
    print("coarse half-sum (x+tail)/2 has primitive anchor signature: YES")
    print("source descent: NO (Psi_I(H_m)=1/2)")
    print("one adjacent edge kills Omega_1: NO (transfers to face 3)")
    print("first exact residual: unit + endpoint ridge + source-word label")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
