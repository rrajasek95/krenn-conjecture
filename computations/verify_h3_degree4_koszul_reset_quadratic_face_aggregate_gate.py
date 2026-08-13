#!/usr/bin/env python3
"""Classify the five quadratic faces of the h=3 degree-four reset cell.

For the internal mixed word 12112, the selected denominator face at deleted
site v is the four-site hafnian h_v.  The five h_v have fifteen disjoint
matching monomials.  This checker computes:

* the raw mixed/pure polynomial face ranks;
* the first graded syzygies of (h_1,...,h_5);
* the exact conditional repeated cap quotient by
  b_(v,N)=-Omega_v+Q_(v,N); and
* the further cyclic Cartan quotient.

After a source-valid common-tail/Rees lift, the reset faces induce 3*I_5 on
the primitive cap coordinates lambda_v.  Physical Cartan/Hasse comparison
then fills the saturated standard lattice, so one primitive aggregate
remains.  Neither the lift nor that aggregate cell is constructed here.
"""

from __future__ import annotations

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py":
        "7308d9b55740644affedbda04c8085517bcc2a0881eb5a8c839fc6cdee5547e5",
    "computations/verify_h3_single_koszul_cell_face_star_no_go.py":
        "5b94a8b213213ce64dd8536baf638e619a4773a2dfc4a2318e1820742f8f8165",
    "computations/verify_h3_jd_normalized_cube_physical_cap_homology.py":
        "2488998937c4aac2915a9335c48d40398b419ee654092d9a9942157abd04b9e3",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_c6_e14_two_cell_unit_frontier.py":
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
    "computations/verify_h3_c6_e14_three_cell_top_degree_boundary.py":
        "ac4ae4b8e2a351f4666cc2e196073663da94634ed4aac4c3f4e6b5dd92169313",
}
EXPECTED_LEDGER_SHA256 = "c6a3e6df4b74ae52478bd2c32c3e61483751f8c879ad4832824da0d99a82ec3f"

SITES = (1, 2, 3, 4, 5)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)
CYCLE = (1, 3, 5, 2, 4)
EDGES = tuple(combinations(SITES, 2))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def face_polynomials(colouring):
    answer = {}
    for deleted in SITES:
        terms = []
        remaining = tuple(site for site in SITES if site != deleted)
        for matching in perfect_matchings(remaining):
            terms.append(tuple(sorted(
                (left, right, colouring[left - 1], colouring[right - 1])
                for left, right in matching
            )))
        require(len(terms) == len(set(terms)) == 3,
                ("four-site hafnian changed", deleted, terms))
        answer[deleted] = tuple(sorted(terms))
    return answer


def raw_face_audit():
    mixed = face_polynomials(MIXED)
    pure = face_polynomials(PURE)
    mixed_terms = {term for face in mixed.values() for term in face}
    pure_terms = {term for face in pure.values() for term in face}
    require(len(mixed_terms) == len(pure_terms) == 15
            and mixed_terms.isdisjoint(pure_terms),
            "the mixed/pure quadratic supports stopped being disjoint")
    basis = tuple(sorted(mixed_terms | pure_terms))
    lookup = {term: index for index, term in enumerate(basis)}

    def column(terms):
        result = [Q(0)] * len(basis)
        for term in terms:
            result[lookup[term]] += 1
        return tuple(result)

    pure_columns = tuple(column(pure[site]) for site in SITES)
    mixed_columns = tuple(column(mixed[site]) for site in SITES)
    require(rank(mixed_columns) == rank(pure_columns) == 5
            and rank(pure_columns + mixed_columns) == 10,
            "the raw mixed/pure face ranks changed")
    return {
        "mixed_word": "".join(map(str, MIXED)),
        "pure_word": "".join(map(str, PURE)),
        "mixed_quadrics": {
            str(site): [
                ["q_%d%d^%d%d" % term for term in monomial]
                for monomial in mixed[site]
            ] for site in SITES
        },
        "mixed_matching_monomials": len(mixed_terms),
        "pure_matching_monomials": len(pure_terms),
        "mixed_face_rank": rank(mixed_columns),
        "pure_face_rank": rank(pure_columns),
        "combined_mixed_pure_rank": rank(pure_columns + mixed_columns),
        "raw_mixed_pure_cancellation": False,
    }, mixed


def polynomial_relation_matrix(faces, multiplier_degree):
    multipliers = tuple(combinations_with_replacement(
        tuple((left, right, MIXED[left - 1], MIXED[right - 1])
              for left, right in EDGES),
        multiplier_degree,
    ))
    columns = []
    output_terms = set()
    column_terms = []
    for site in SITES:
        for multiplier in multipliers:
            terms = tuple(tuple(sorted(multiplier + face_term))
                          for face_term in faces[site])
            column_terms.append(terms)
            output_terms.update(terms)
    output_terms = tuple(sorted(output_terms))
    lookup = {term: index for index, term in enumerate(output_terms)}
    for terms in column_terms:
        column = [Q(0)] * len(output_terms)
        for term in terms:
            column[lookup[term]] += 1
        columns.append(tuple(column))
    return tuple(columns), multipliers


def graded_syzygy_audit(faces):
    records = {}
    degree_two_columns = None
    degree_two_multipliers = None
    for degree in (0, 1, 2):
        columns, multipliers = polynomial_relation_matrix(faces, degree)
        current_rank = rank(columns)
        kernel = len(columns) - current_rank
        records[degree] = {
            "coefficient_degree": degree,
            "columns": len(columns),
            "rank": current_rank,
            "kernel_dimension": kernel,
        }
        if degree == 2:
            degree_two_columns = columns
            degree_two_multipliers = multipliers
    require(records[0]["kernel_dimension"] == 0
            and records[1]["kernel_dimension"] == 0
            and records[2]["kernel_dimension"] == 10,
            ("first syzygy dimensions changed", records))

    require(degree_two_columns is not None
            and degree_two_multipliers is not None,
            "degree-two relation matrix missing")
    multiplier_index = {
        tuple(sorted(multiplier)): index
        for index, multiplier in enumerate(degree_two_multipliers)
    }
    multiplier_count = len(degree_two_multipliers)
    koszul = []
    for left, right in combinations(SITES, 2):
        vector = [Q(0)] * (len(SITES) * multiplier_count)
        for term in faces[right]:
            vector[(left - 1) * multiplier_count
                   + multiplier_index[tuple(sorted(term))]] += 1
        for term in faces[left]:
            vector[(right - 1) * multiplier_count
                   + multiplier_index[tuple(sorted(term))]] -= 1
        image = [
            sum(column[row] * coefficient
                for column, coefficient in
                zip(degree_two_columns, vector, strict=True))
            for row in range(len(degree_two_columns[0]))
        ]
        require(not any(image),
                ("pairwise Koszul vector stopped being a syzygy", left, right))
        koszul.append(tuple(vector))
    require(rank(tuple(koszul)) == 10,
            "the ten pairwise Koszul syzygies lost independence")
    return {
        "graded_search": records,
        "first_nonzero_syzygy_coefficient_degree": 2,
        "first_total_polynomial_degree": 4,
        "first_syzygy_dimension": 10,
        "first_syzygy_basis": "h_w*e_v-h_v*e_w for 1<=v<w<=5",
        "extra_non_Koszul_syzygies_in_first_degree": 0,
        "consequence": (
            "the smallest polynomial relations compare face quadrics only "
            "after multiplying by another quadratic; they do not provide a "
            "unit or primitive aggregate nullhomotopy"
        ),
    }


def direct_free_guard_linearization_audit():
    """Linearize the five uncoloured quadrics at q12=a, q14=b."""
    edge_index = {edge: index for index, edge in enumerate(EDGES)}
    uncoloured = {
        site: perfect_matchings(tuple(value for value in SITES
                                      if value != site))
        for site in SITES
    }
    a = Q(2)
    b = Q(3)
    point = {edge: Q(0) for edge in EDGES}
    point[(1, 2)] = a
    point[(1, 4)] = b
    jacobian = []
    for site in SITES:
        row = [Q(0)] * len(EDGES)
        for first, second in uncoloured[site]:
            row[edge_index[first]] += point[second]
            row[edge_index[second]] += point[first]
        jacobian.append(tuple(row))
    jacobian = tuple(jacobian)

    def sparse(row):
        return {str(edge): str(row[index]) for edge, index in edge_index.items()
                if row[index]}

    require(sparse(jacobian[0]) == {}
            and sparse(jacobian[1]) == {"(3, 5)": str(b)}
            and sparse(jacobian[2])
                == {"(2, 5)": str(b), "(4, 5)": str(a)}
            and sparse(jacobian[3]) == {"(3, 5)": str(a)}
            and sparse(jacobian[4])
                == {"(2, 3)": str(b), "(3, 4)": str(a)},
            ("direct-free Jacobian formulas changed",
             [sparse(row) for row in jacobian]))
    require(rank(jacobian) == 3,
            "direct-free quadratic Jacobian rank changed")

    k1 = (Q(1), Q(0), Q(0), Q(0), Q(0))
    k2 = (Q(0), a, Q(0), -b, Q(0))
    for vector in (k1, k2):
        image = tuple(sum(vector[site] * jacobian[site][edge]
                          for site in range(5))
                      for edge in range(len(EDGES)))
        require(not any(image), ("dark face combination changed", vector))
    require(rank((k1, k2)) == 2,
            "direct-free dark face kernel changed")
    zero_sum_dark = tuple((b - a) * k1[index] + k2[index]
                          for index in range(5))
    require(sum(zero_sum_dark, Q(0)) == 0
            and rank((zero_sum_dark,)) == 1,
            "dark standard line changed")

    # Both dark generators begin in the two-new-cell layer.  The dependent
    # opposite-face combination cancels the shared first-order x35 term.
    supported = {(1, 2), (1, 4)}

    def guard_expand(site):
        result = {}
        for term in uncoloured[site]:
            absent = tuple(edge for edge in term if edge not in supported)
            coefficient = Q(1)
            for edge in term:
                if edge in supported:
                    coefficient *= point[edge]
            result[absent] = result.get(absent, Q(0)) + coefficient
        return result

    h1_terms = guard_expand(1)
    combo = {}
    for coefficient, site in ((a, 2), (-b, 4)):
        for term, value in guard_expand(site).items():
            key = tuple(sorted(term))
            combo[key] = combo.get(key, Q(0)) + coefficient * value
            if not combo[key]:
                combo.pop(key)
    require(len(h1_terms) == 3 and len(combo) == 4
            and all(len(term) == 2
                    for term in tuple(h1_terms) + tuple(combo)),
            ("dark second-order supports changed", h1_terms, combo))
    return {
        "guard_supported_edges": {"q12": str(a), "q14": str(b)},
        "jacobian_rows": {
            f"dh_{site}": sparse(jacobian[site - 1]) for site in SITES
        },
        "jacobian_rank": rank(jacobian),
        "first_order_bright_rank": 3,
        "first_order_dark_kernel_rank": 2,
        "dark_kernel_basis": [
            "e1",
            f"{a}*e2-{b}*e4",
        ],
        "dark_standard_intersection": [
            str(value) for value in zero_sum_dark
        ],
        "dark_standard_intersection_rank": 1,
        "dark_aggregate_quotient_rank": 1,
        "h1_second_order_terms": [
            [list(edge) for edge in term] for term in sorted(h1_terms)
        ],
        "opposite_face_second_order_terms": {
            repr(term): str(value) for term, value in sorted(combo.items())
        },
        "every_dark_leading_monomial_uses_two_new_cells": True,
        "unit_theorem_handoff": (
            "after a source-valid Rees/initial-form lift isolates a dark "
            "leading support, the pinned E14 two-cell theorem gives a "
            "literal source unit; any cubic proper face is covered by the "
            "pinned three-cell theorem.  Those finite theorems do not "
            "construct or terminate the Rees lift because their witnessing "
            "zero row varies with the support."
        ),
    }


def physical_cap_audit():
    companions = tuple((site, matching)
                       for site in SITES for matching in range(3))
    omega_index = {site: index for index, site in enumerate(SITES)}
    q_index = {item: len(SITES) + index
               for index, item in enumerate(companions)}
    ambient = len(SITES) + len(companions)

    routes = []
    for site, matching in companions:
        column = [Q(0)] * ambient
        column[omega_index[site]] = -1
        column[q_index[(site, matching)]] = 1
        routes.append(tuple(column))
    routes = tuple(routes)

    lambdas = []
    for site in SITES:
        row = [Q(0)] * ambient
        row[omega_index[site]] = 1
        for matching in range(3):
            row[q_index[(site, matching)]] = 1
        lambdas.append(tuple(row))
    lambdas = tuple(lambdas)
    require(rank(routes) == 15 and rank(lambdas) == 5
            and all(dot(value, column) == 0
                    for value in lambdas for column in routes),
            "the physical route/lambda complex changed")

    reset_faces = []
    for site in SITES:
        column = [Q(0)] * ambient
        for matching in range(3):
            column[q_index[(site, matching)]] = 1
        reset_faces.append(tuple(column))
    reset_faces = tuple(reset_faces)
    induced = tuple(tuple(dot(row, column) for column in reset_faces)
                    for row in lambdas)
    require(induced == tuple(
        tuple(Q(3) if row == column else Q(0)
              for column in range(5)) for row in range(5)
    ), ("reset face matrix on lambda changed", induced))

    face_index = {site: index for index, site in enumerate(SITES)}
    quotient_edges = []
    cartan_lifts = []
    for index, site in enumerate(CYCLE):
        successor = CYCLE[(index + 1) % len(CYCLE)]
        edge = [Q(0)] * 5
        edge[face_index[site]] = -1
        edge[face_index[successor]] = 1
        quotient_edges.append(tuple(edge))

        # This is a convenient representative of the induced physical
        # Cartan class.  The pinned theorem constructs the physical chain;
        # only its lambda image is used here.
        lift = [Q(0)] * ambient
        lift[omega_index[site]] = -1
        lift[omega_index[successor]] = 1
        cartan_lifts.append(tuple(lift))
    quotient_edges = tuple(quotient_edges)
    cartan_lifts = tuple(cartan_lifts)
    aggregate = (Q(1),) * 5
    require(rank(quotient_edges) == 4
            and all(dot(aggregate, edge) == 0 for edge in quotient_edges),
            "the cyclic Cartan standard lattice changed")
    require(rank(routes + cartan_lifts) == 19,
            "route plus Cartan cap rank changed")

    aggregate_dual = tuple(sum(row[index] for row in lambdas)
                           for index in range(ambient))
    require(all(dot(aggregate_dual, column) == 0
                for column in routes + cartan_lifts)
            and all(dot(aggregate_dual, face) == 3
                    for face in reset_faces),
            "the primitive aggregate detector changed")

    primitive = [Q(0)] * ambient
    primitive[q_index[(CYCLE[0], 0)]] = -1
    primitive = tuple(primitive)
    require(dot(aggregate_dual, primitive) == -1
            and rank(routes + cartan_lifts + (primitive,)) == ambient,
            "one primitive reduced cap stopped completing the complex")
    for face in reset_faces:
        require(rank(routes + cartan_lifts + (primitive,))
                == rank(routes + cartan_lifts + (primitive, face)),
                "a reset face was not filled after primitive attachment")

    return {
        "physical_word": "01211222",
        "residual_denominator_word": "12112",
        "raw_quadratic_face": "h_v=sum_N q_(v,N)",
        "common_tail_transport": "Q_(v,N)=t_v*q_(v,N)",
        "raw_to_repeated_Q_chain_map_constructed": False,
        "transport_gate": (
            "the matrix below is the exact induced cap matrix after a "
            "source-valid common-tail/Rees lift.  Bare multiplication by "
            "t_v has product-rule faces and is not itself that lift."
        ),
        "route_rows": ["Omega_v"] + ["Q_(v,N)"],
        "route_formula": "b_(v,N)=-Omega_v+Q_(v,N)",
        "route_matrix_shape": [ambient, len(routes)],
        "route_rank": rank(routes),
        "route_cokernel_rank": ambient - rank(routes),
        "primitive_coordinates": "lambda_v=Omega_v+sum_N Q_(v,N)",
        "transported_reset_face_matrix_on_lambda": [
            [int(value) for value in row] for row in induced
        ],
        "reset_face_rank_after_routes": rank(reset_faces),
        "cartan_cycle_order": list(CYCLE),
        "cartan_standard_matrix": [
            [int(value) for value in column] for column in quotient_edges
        ],
        "cartan_standard_rank": rank(quotient_edges),
        "cartan_standard_lattice": "saturated ker(sum:Z^5->Z)",
        "rank_after_routes_and_cartan": rank(routes + cartan_lifts),
        "remaining_cokernel_rank": ambient - rank(routes + cartan_lifts),
        "aggregate_covector": "epsilon=sum_v lambda_v",
        "epsilon_on_each_reset_face": 3,
        "primitive_reduced_cap": "-Q_(1,N0), epsilon=-1",
        "rank_after_primitive_cap": rank(
            routes + cartan_lifts + (primitive,)
        ),
        "all_five_transported_reset_faces_filled_after_one_primitive_cap":
            True,
        "raw_quadratic_faces_filled_without_transport": False,
    }


def audit():
    pin_dependencies()
    raw, mixed_faces = raw_face_audit()
    ledger = {
        "theorem": "degree-four Koszul reset quadratic-face aggregate gate",
        "pins": PINS,
        "raw_quadratic_faces": raw,
        "first_polynomial_syzygies":
            graded_syzygy_audit(mixed_faces),
        "direct_free_guard_linearization":
            direct_free_guard_linearization_audit(),
        "physical_cap_quotient": physical_cap_audit(),
        "verdict": (
            "the reset has five independent quadratic faces.  Bare "
            "matching/Bianchi rows do not fill their cross-face standard "
            "directions, and the first bare polynomial "
            "syzygies occur in total degree four and are only the ten "
            "pairwise Koszul relations.  After granting a source-valid "
            "common-tail/Rees transport into the repeated Q_(v,N) packet, "
            "the induced cap matrix is 3*I_5 and the pinned physical "
            "Cartan/Hasse orbit fills the saturated rank-four standard "
            "lattice, leaving exactly one primitive aggregate.  Neither the "
            "transport nor the primitive cell is constructed here."
        ),
        "guard_refinement": (
            "at the direct-free q12/q14 guard the first derivative has rank "
            "three.  The two dark directions are h1 and the dependent h2/h4 "
            "combination; their intersection with the Cartan standard "
            "lattice is one-dimensional, leaving the same one aggregate "
            "second-order direction.  Its monomials are all two-new-cell "
            "E14 supports, so the pinned two-/three-cell unit theorems are "
            "a terminal handoff only after a source-valid Rees lift."
        ),
        "smallest_open_physical_cell": (
            "one source-valid seven-occurrence relative total cell in word "
            "01211222 and the labelled repeated P3+K2 grade, with induced "
            "aggregate epsilon=+/-1 and the protected readouts required by "
            "the pinned primitive-cap theorem"
        ),
        "scope": (
            "exact universal quadratic face algebra and exact conditional "
            "induced cap quotient.  The physical standard edge cells are "
            "reused from the pinned Cartan source-orbit theorem only after "
            "the raw faces enter its repeated grade.  No raw-to-repeated "
            "Rees lift, primitive aggregate source cell, or terminal "
            "comparison is constructed here."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("degree-four reset face ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 degree-four reset faces: RAW RANK 5")
    print("conditional repeated-cap quotient: 3*I_5")
    print("Cartan/Hasse standard directions: RANK 4 SATURATED")
    print("remaining physical cap: ONE PRIMITIVE AGGREGATE")
    print("first polynomial syzygies: degree 4, ten Koszul pairs only")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
