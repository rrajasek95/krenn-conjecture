#!/usr/bin/env python3
r"""Universal endpoint-typed quotient of the normalized C5 tail occurrences.

After the target-preserving C5 normalization, every deleted face has

    h_v = 1 + R_v,

where R_v is the sum of two off-cycle matching occurrences.  This checker
keeps the ten occurrences distinct and audits every complete coefficient of
the unary row and the four response tensors which literally contains one of
them.  Every such term has positive endpoint-use grade: a q-spoke for the
unary row, or an oriented p_i/s_j endpoint pair for a response row.  Hence
the universal polynomial rows have zero projection to the bare-tail grade.

The five cyclic differences R_v-R_next have rank four.  Therefore their
universal typed quotient is Q^4.  This is a source-typing theorem, not a
full-source counterexample: localizing an active endpoint bracket is exactly
the additional hypothesis used by the conditional attachment theorem.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "f5998c8c56459323e0fb9f56158d0785ba1841654b7737415748407cb84c675d"
PINS = {
    "computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py":
        "02c2cc44c4d849e9db5d98c3c28882e93772dcc01cab286bba7d94cf8a8502be",
    "notes/h3-rootless-target-preserving-c5-etale-gauge.md":
        "da6d5d3658b8dfe005f47f8e859342f1f98dfb0d1d8c40ca3b0b596b365726cb",
    "computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py":
        "ef235f2e17b7f62a7160bdc9fccd18efae5842c00ae2fc4ae7d900de34255f0d",
    "notes/h3-rootless-c5-first-unmatched-tail-attachment-boundary.md":
        "b26b97ecda76037fd6f73a2e6a37823e6cffc75d5917485da5a07e29c0d18d50",
}

X = 0
ODD = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))
FACE_ORDER = (1, 3, 5, 2, 4)
RESPONSES = ((1, 1), (1, 2), (2, 1), (2, 2))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def perfect_matchings(vertices: tuple[int, ...]):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted(((first, second),) + tail)))
    return tuple(result)


def decorated_edge(edge: tuple[int, int]):
    left, right = edge
    return left, right, MIDDLE[left], MIDDLE[right]


def monomial_text(matching) -> str:
    return "*".join(
        f"q{left}{right}^{MIDDLE[left]}{MIDDLE[right]}"
        for left, right in matching
    )


def rank(columns: list[list[int]]) -> int:
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
        if pivot_row == height:
            break
    return pivot_row


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def tail_basis():
    occurrences = []
    faces = {}
    for deleted in ODD:
        face = tuple(site for site in ODD if site != deleted)
        matchings = perfect_matchings(face)
        selected = tuple(matching for matching in matchings
                         if set(matching) <= CYCLE)
        residual = tuple(matching for matching in matchings
                         if matching not in selected)
        require(len(matchings) == 3 and len(selected) == 1
                and len(residual) == 2,
                "a deleted C5 face lost its 1+2 split")
        indices = []
        for local_index, matching in enumerate(residual):
            occurrence = {
                "basis_index": len(occurrences),
                "label": f"t_{deleted},{local_index}",
                "deleted_face": deleted,
                "face_word": "".join(str(MIDDLE[site]) for site in face),
                "matching": [list(edge) for edge in matching],
                "decorated_tail": [list(decorated_edge(edge))
                                   for edge in matching],
                "monomial": monomial_text(matching),
                "target_readout": 0,
                "bare_endpoint_use_grade": [],
            }
            indices.append(len(occurrences))
            occurrences.append(occurrence)
        faces[deleted] = {
            "selected_matching": [list(edge) for edge in selected[0]],
            "residual_indices": indices,
        }
    require(len(occurrences) == 10, "the ten-tail basis changed")
    require(len({item["monomial"] for item in occurrences}) == 10,
            "two labelled off-cycle tail monomials collided")
    return occurrences, faces


def tail_difference_module(occurrences, faces):
    dimension = len(occurrences)
    face_sums = {}
    for deleted in ODD:
        vector = [0] * dimension
        for index in faces[deleted]["residual_indices"]:
            vector[index] = 1
        face_sums[deleted] = vector

    differences = []
    for position, left in enumerate(FACE_ORDER):
        right = FACE_ORDER[(position + 1) % len(FACE_ORDER)]
        differences.append([
            a - b for a, b in zip(face_sums[left], face_sums[right], strict=True)
        ])
    require(rank(differences) == 4,
            "the cyclic C5 tail differences lost rank four")
    require([sum(column[index] for column in differences)
             for index in range(dimension)] == [0] * dimension,
            "the five cyclic differences stopped summing to zero")
    require(rank(differences[:4]) == 4,
            "the first four cyclic differences stopped being a basis")

    # Integral sparse representatives: lambda_k uses one occurrence in each
    # of the first k+1 faces.  Symmetric face-potential representatives put
    # 1/2 on both occurrences in those faces.  Both restrict to the same
    # primitive functional on the difference lattice.
    integral_duals = []
    symmetric_duals = []
    for k in range(4):
        integral = [Q(0)] * dimension
        symmetric = [Q(0)] * dimension
        for deleted in FACE_ORDER[:k + 1]:
            first, second = faces[deleted]["residual_indices"]
            integral[first] = Q(1)
            symmetric[first] = symmetric[second] = Q(1, 2)
        integral_duals.append(integral)
        symmetric_duals.append(symmetric)
    expected_pairing = [[Q(int(row == column)) for column in range(4)]
                        for row in range(4)]
    for duals in (integral_duals, symmetric_duals):
        pairing = [[dot(dual, boundary) for boundary in differences[:4]]
                   for dual in duals]
        require(pairing == expected_pairing,
                ("a sparse face-potential dual changed", pairing))
        require([dot(dual, differences[4]) for dual in duals] == [-1] * 4,
                "the closing-edge dual values changed")

    def sparse(vector):
        return {occurrences[index]["label"]: str(value)
                for index, value in enumerate(vector) if value}

    return {
        "ambient_tail_rank": dimension,
        "difference_columns": differences,
        "difference_rank": 4,
        "basis_edges": [[FACE_ORDER[k], FACE_ORDER[k + 1]] for k in range(4)],
        "closing_edge": [FACE_ORDER[4], FACE_ORDER[0]],
        "unique_relation": "sum of the five oriented differences is zero",
        "integral_sparse_duals": [sparse(vector) for vector in integral_duals],
        "symmetric_face_potential_duals": [sparse(vector)
                                            for vector in symmetric_duals],
    }


def complete_typed_rows(occurrences, faces):
    occurrence_by_pair = {
        (item["deleted_face"], tuple(tuple(edge) for edge in item["matching"])):
            item["basis_index"]
        for item in occurrences
    }

    # The unary word is x followed by m=12112.  Its 15 perfect matchings
    # split uniquely as the spoke (x,v) times one of the three face PMs.
    unary_word = "0" + "".join(str(MIDDLE[site]) for site in ODD)
    unary_terms = []
    unary_off_cycle = []
    for matching in perfect_matchings((X,) + ODD):
        spoke = next(edge for edge in matching if X in edge)
        deleted = spoke[1]
        tail = tuple(edge for edge in matching if edge != spoke)
        endpoint_grade = (("q_spoke", X, deleted, 0, MIDDLE[deleted]),)
        term = {
            "deleted_face": deleted,
            "tail_matching": [list(edge) for edge in tail],
            "endpoint_grade": [list(item) for item in endpoint_grade],
            "target_readout": 0,
        }
        unary_terms.append(term)
        key = (deleted, tail)
        if key in occurrence_by_pair:
            term["tail_basis_index"] = occurrence_by_pair[key]
            unary_off_cycle.append(term)
    require(len(unary_terms) == 15 and len(unary_off_cycle) == 10,
            "the unary word lost its 15/10 occurrence split")
    require(unary_word == "012112", "the normalized unary word changed")

    response_coefficients = []
    response_off_cycle = []
    bracket_count = 0
    orientation_count = 0
    for deleted in ODD:
        face = tuple(site for site in ODD if site != deleted)
        require(len(set(MIDDLE[site] for site in face)) == 2,
                "a response face became a pure target word")
        for i, j in RESPONSES:
            terms = []
            for orientation in ((X, deleted), (deleted, X)):
                p_site, s_site = orientation
                endpoint_grade = tuple(sorted((
                    ("p", i, p_site), ("s", j, s_site)
                )))
                for tail in perfect_matchings(face):
                    term = {
                        "orientation": [p_site, s_site],
                        "tail_matching": [list(edge) for edge in tail],
                        "endpoint_grade": [list(item) for item in endpoint_grade],
                        "target_readout": 0,
                    }
                    terms.append(term)
                    key = (deleted, tail)
                    if key in occurrence_by_pair:
                        term["tail_basis_index"] = occurrence_by_pair[key]
                        response_off_cycle.append(term)
                        orientation_count += 1
            require(len(terms) == 6,
                    "a complete response-hole coefficient lost a term")
            response_coefficients.append({
                "row": f"G{i}{j}",
                "deleted_face": deleted,
                "endpoint_word": f"p{i}@0,s{j}@{deleted};p{i}@{deleted},s{j}@0",
                "tail_word": "".join(str(MIDDLE[site]) for site in face),
                "target_readout": 0,
                "terms": terms,
            })
            bracket_count += 2  # two off-cycle tails, one bracket each

    require(len(response_coefficients) == 20,
            "the four-response coefficient inventory changed")
    require(all(len(row["terms"]) == 6 for row in response_coefficients),
            "a response row is incomplete")
    require(bracket_count == 40 and orientation_count == 80,
            "the 40-bracket/80-orientation count changed")

    # Every literal occurrence has a nonempty endpoint grade.  Projection to
    # the bare ten-tail summand is therefore identically zero.  Polynomial
    # multiplication only adds nonnegative endpoint degree and cannot alter
    # this statement.  Inverting a spoke/bracket is localization, not part of
    # the universal polynomial module.
    all_off_cycle = unary_off_cycle + response_off_cycle
    require(len(all_off_cycle) == 90,
            "the complete rows lost an off-cycle occurrence")
    require(all(term["endpoint_grade"] for term in all_off_cycle),
            "a complete-row occurrence entered the bare-tail grade")
    endpoint_degree_histogram = Counter(
        len(term["endpoint_grade"]) for term in all_off_cycle
    )
    require(endpoint_degree_histogram == Counter({1: 10, 2: 80}),
            "the endpoint-use degree histogram changed")

    return {
        "unary": {
            "complete_word": unary_word,
            "complete_term_count": len(unary_terms),
            "off_cycle_occurrence_count": len(unary_off_cycle),
            "missing_spoke_columns": 10,
            "target_readout": 0,
        },
        "responses": {
            "complete_equations": [f"G{i}{j}" for i, j in RESPONSES],
            "relevant_hole_coefficients": len(response_coefficients),
            "terms_per_coefficient": 6,
            "complete_term_count": sum(len(row["terms"])
                                       for row in response_coefficients),
            "off_cycle_oriented_occurrences": orientation_count,
            "missing_endpoint_brackets": bracket_count,
            "bracket_formula": "B_ij^(xv)=p_i@x*s_j@v+p_i@v*s_j@x",
            "target_readout": 0,
        },
        "all_relevant_complete_coefficients": 1 + len(response_coefficients),
        "all_complete_terms": len(unary_terms) + sum(
            len(row["terms"]) for row in response_coefficients),
        "off_cycle_endpoint_degree_histogram": dict(endpoint_degree_histogram),
        "bare_tail_projection_rank": 0,
        "polynomial_multiplication_preserves_separation": True,
        "localization_can_break_separation": True,
    }


def audit():
    pin_dependencies()
    occurrences, faces = tail_basis()
    difference = tail_difference_module(occurrences, faces)
    typed = complete_typed_rows(occurrences, faces)
    routed_rank = typed["bare_tail_projection_rank"]
    quotient_rank = difference["difference_rank"] - routed_rank
    require((routed_rank, quotient_rank) == (0, 4),
            "the universal typed tail quotient changed")
    ledger = {
        "pins": PINS,
        "tail_occurrences": occurrences,
        "face_aggregates": {
            str(deleted): [occurrences[index]["label"]
                           for index in faces[deleted]["residual_indices"]]
            for deleted in ODD
        },
        "cyclic_difference_module": difference,
        "complete_unary_four_response_typing": typed,
        "J_tail_universal_routed_rank": routed_rank,
        "Q_tail_rank_over_Q": quotient_rank,
        "missing_physical_columns": {
            "unary_spokes": 10,
            "response_brackets": 40,
            "oriented_response_columns": 80,
            "bracket_formula": "(p_i@x*s_j@v+p_i@v*s_j@x)*N",
        },
        "verdict": (
            "Q_tail=span_Q{R_v-R_next}/im(J_tail)=Q^4 in the universal "
            "endpoint-typed polynomial module; every literal unary/response "
            "occurrence has positive endpoint-use grade, so no complete row "
            "projects to a bare tail without an active localization"
        ),
        "scope": (
            "finite exact h=3 normalized-C5 source-typing theorem; not a "
            "full-source counterexample, not a proof that every endpoint "
            "bracket is dark, and compatible with the conditional active-"
            "hole routing theorem pinned above"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"universal ten-tail quotient ledger changed: {digest}")
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    typed = ledger["complete_unary_four_response_typing"]
    print("h3 rootless C5 universal ten-tail typed quotient: PASS")
    print("tails=10 cyclic_difference_rank=4 J_tail_routed_rank=0 Q_tail_rank=4")
    print("complete_coefficients=21 complete_terms=135")
    print("missing=10 unary spokes + 40 brackets / 80 orientations")
    print("endpoint-grade separation: exact before localization")
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()
