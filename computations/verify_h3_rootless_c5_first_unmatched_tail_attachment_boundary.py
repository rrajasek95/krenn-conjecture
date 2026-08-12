#!/usr/bin/env python3
"""First-unmatched-tail attachment boundary for normalized rootless C5.

The normalized off-cycle companions have ten distinct literal monomials.
For an active endpoint product at the forced hole (x,v), the complete
six-term response coefficient gives an exact unit/same-tail/C4 partition.
The C5 tail equations alone do not force that endpoint activity: a rational
normalized chord point has nonzero R_v-R_w while every endpoint product at
the relevant holes is zero.  Thus response-hole accessibility is the first
missing hypothesis, before rank landing.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py":
        "02c2cc44c4d849e9db5d98c3c28882e93772dcc01cab286bba7d94cf8a8502be",
    "notes/h3-rootless-target-preserving-c5-etale-gauge.md":
        "da6d5d3658b8dfe005f47f8e859342f1f98dfb0d1d8c40ca3b0b596b365726cb",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_h3_c6_e14_pure11_unary_unit.py":
        "07160a67a4a16885fe481265ce67a372117b323dea82819e220cbe79e131df2d",
    "computations/verify_h3_c6_e14_two_cell_unit_frontier.py":
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
}
EXPECTED_LEDGER_SHA256 = (
    "7d0d402c01bd9862235b568068a418009220f344247d48ca4c8f48b683c12578"
)
ODD = (1, 2, 3, 4, 5)
X = 0
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))
FACE_ORDER = (1, 3, 5, 2, 4)
CHORD_NAME = {
    (1, 3): "A", (1, 4): "B", (2, 4): "C",
    (2, 5): "D", (3, 5): "E",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices
                          if site not in (first, second))
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def normalized_monomial(matching):
    return tuple(sorted(CHORD_NAME[edge]
                        for edge in matching if edge not in CYCLE))


def polynomial_value(polynomial, values):
    return sum(Q(coefficient) * __import__("math").prod(
        values[variable] for variable in monomial
    ) for monomial, coefficient in polynomial.items())


def tail_algebra():
    faces = {}
    occurrences = []
    for deleted in ODD:
        face = tuple(site for site in ODD if site != deleted)
        matchings = perfect_matchings(face)
        selected = [matching for matching in matchings
                    if set(matching) <= CYCLE]
        require(len(matchings) == 3 and len(selected) == 1,
                "a C5 deletion face lost its 1+2 matching split")
        residual = tuple(matching for matching in matchings
                         if matching not in selected)
        monomials = tuple(normalized_monomial(matching)
                          for matching in residual)
        require(all(monomials), "an off-cycle tail became the selected route")
        faces[deleted] = {
            "selected_matching": selected[0],
            "residual_matchings": residual,
            "R_monomials": monomials,
        }
        occurrences.extend((deleted, matching, monomial)
                           for matching, monomial in zip(
                               residual, monomials, strict=True))

    require(len(occurrences) == 10
            and len({monomial for _v, _n, monomial in occurrences}) == 10,
            "the ten C5 residual monomials stopped being literal unmatched tails")
    degree_histogram = Counter(len(monomial)
                               for _v, _n, monomial in occurrences)
    require(degree_histogram == Counter({1: 5, 2: 5}),
            f"the linear/quadratic tail split changed: {degree_histogram}")

    expected = {
        1: {("C", "E"): 1, ("D",): 1},
        2: {("A",): 1, ("B", "E"): 1},
        3: {("B", "D"): 1, ("C",): 1},
        4: {("E",): 1, ("A", "D"): 1},
        5: {("A", "C"): 1, ("B",): 1},
    }
    actual = {deleted: {monomial: 1
                        for monomial in record["R_monomials"]}
              for deleted, record in faces.items()}
    require(actual == expected, f"the normalized R_v algebra changed: {actual}")

    boundaries = []
    for index, left in enumerate(FACE_ORDER):
        right = FACE_ORDER[(index + 1) % len(FACE_ORDER)]
        left_support = set(actual[left])
        right_support = set(actual[right])
        require(left_support.isdisjoint(right_support),
                "an adjacent C5 boundary acquired a common literal tail")
        polynomial = {monomial: 1 for monomial in left_support}
        polynomial.update({monomial: -1 for monomial in right_support})
        require(len(polynomial) == 4,
                "an R_v-R_w boundary stopped having four unmatched terms")
        boundaries.append({
            "faces": [left, right],
            "positive_monomials": sorted(left_support),
            "negative_monomials": sorted(right_support),
        })
    return faces, occurrences, boundaries, degree_histogram


def complete_response_partition(faces, occurrences):
    records = []
    route_counts = Counter()
    for deleted, selected_tail, monomial in occurrences:
        all_tails = perfect_matchings(
            tuple(site for site in ODD if site != deleted)
        )
        terms = tuple((orientation, tail)
                      for orientation in ((X, deleted), (deleted, X))
                      for tail in all_tails)
        require(len(terms) == 6,
                "a forced-hole complete response coefficient lost six terms")
        selected_term = ((X, deleted), selected_tail)
        require(selected_term in terms,
                "the chosen tail lost its literal endpoint orientation")
        opposite = [term for term in terms
                    if term[0] == (deleted, X) and term[1] == selected_tail]
        switched = [term for term in terms if term[1] != selected_tail]
        require(len(opposite) == 1 and len(switched) == 4,
                "the complete response mate partition changed")
        require(all(len(set(tail) ^ set(selected_tail)) == 4
                    for _orientation, tail in switched),
                "a different-tail mate stopped being one literal C4 switch")

        # Exact exhaustive alternatives after localizing the selected term.
        alternatives = {
            "no_active_mate": "ordinary localized source unit",
            "opposite_orientation_same_tail": (
                "same-tail endpoint columns: proportional finite deletion "
                "or a nonzero Fitting minor"
            ),
            "different_tail_C4": (
                "an edge outside the selected anchor web is an offanchor "
                "attachment; otherwise the C4 enters the anchor Hall/lock gate"
            ),
        }
        route_counts.update({"same_tail_opposite_orientation": 1,
                             "different_tail_C4_terms": 4})
        records.append({
            "deleted_face": deleted,
            "forced_response_hole": [X, deleted],
            "tail_matching": [list(edge) for edge in selected_tail],
            "normalized_tail_monomial": list(monomial),
            "complete_term_count": len(terms),
            "opposite_same_tail_count": len(opposite),
            "different_tail_C4_count": len(switched),
            "conditional_alternatives": alternatives,
        })
    require(route_counts == Counter({
        "same_tail_opposite_orientation": 10,
        "different_tail_C4_terms": 40,
    }), f"the ten-tail complete-row partition changed: {route_counts}")
    return records, route_counts


def response_dark_counterguard(boundaries):
    # A=2 and B=C=D=E=1 is a nonzero normalized chord-torus point.
    # It has a nonzero R3-R5 and R4-R1 tail boundary, while setting every
    # endpoint product at all forced holes (x,v) to zero removes every
    # complete-column attachment.  This is a counterguard to deriving
    # attachment from normalized C5 tail data alone, not a full-source point.
    values = {"A": Q(2), "B": Q(1), "C": Q(1),
              "D": Q(1), "E": Q(1)}
    polynomials = {
        1: {("C", "E"): 1, ("D",): 1},
        2: {("A",): 1, ("B", "E"): 1},
        3: {("B", "D"): 1, ("C",): 1},
        4: {("E",): 1, ("A", "D"): 1},
        5: {("A", "C"): 1, ("B",): 1},
    }
    r_values = {deleted: polynomial_value(polynomial, values)
                for deleted, polynomial in polynomials.items()}
    differences = {
        f"{left}-{right}": r_values[left] - r_values[right]
        for left, right in (record["faces"] for record in boundaries)
    }
    require(any(differences.values()),
            "the response-dark chord point lost its nonzero tail boundary")
    endpoint_products = {f"hole_0{deleted}": Q(0) for deleted in ODD}
    require(not any(endpoint_products.values()),
            "the response-dark guard acquired an endpoint attachment")
    return {
        "normalized_chord_values": {key: str(value)
                                    for key, value in values.items()},
        "R_values": {str(key): str(value)
                     for key, value in r_values.items()},
        "adjacent_R_differences": {key: str(value)
                                   for key, value in differences.items()},
        "all_forced_hole_endpoint_products": {
            key: str(value) for key, value in endpoint_products.items()
        },
        "meaning": (
            "normalized C5 internal-tail data do not force an active "
            "endpoint product at the unique response hole (x,v)"
        ),
        "scope": (
            "formal source-typing counterguard only; the omitted full unary "
            "and four-response target rows may forbid it, and proving that "
            "is exactly the missing spoke-to-hole accessibility lemma"
        ),
    }


def audit():
    pin_dependencies()
    faces, occurrences, boundaries, degrees = tail_algebra()
    attachment, route_counts = complete_response_partition(faces, occurrences)
    dark = response_dark_counterguard(boundaries)
    ledger = {
        "pins": PINS,
        "normalized_R_polynomials": {
            "R1": "C*E+D", "R2": "A+B*E", "R3": "B*D+C",
            "R4": "E+A*D", "R5": "A*C+B",
        },
        "literal_tail_occurrence_count": len(occurrences),
        "tail_degree_histogram": dict(sorted(degrees.items())),
        "adjacent_boundaries": boundaries,
        "complete_response_attachment_records": attachment,
        "complete_response_route_counts": dict(sorted(route_counts.items())),
        "response_dark_counterguard": dark,
        "conditional_first_unmatched_tail_lemma": (
            "if a literal R_v tail has a nonzero endpoint product at its "
            "forced hole (x,v), its complete response coefficient gives an "
            "ordinary unit, an opposite-orientation same-tail endpoint "
            "column (proportional deletion or Fitting carrier), or a C4 "
            "mate (offanchor attachment or anchor Hall/lock gate)"
        ),
        "earliest_obstruction": (
            "response-hole accessibility: the normalized internal C5 "
            "equations alone do not force any endpoint product at (x,v). "
            "The first missing full-source row must turn a response-dark "
            "tail into a hole hit, an offanchor carrier, or Hall incidence"
        ),
        "rank_scope": (
            "same-tail nonproportionality yields a Fitting carrier only; "
            "four-good/clean rank landing and termination remain separate"
        ),
        "local_evidence_scope": (
            "e35b24c and 414f4c6 kill one- and two-cell contaminations on "
            "the canonical E14 fibre, but do not imply C5 response-hole "
            "accessibility and are used only as pinned local evidence"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C5 unmatched-tail attachment ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 rootless C5 first-unmatched-tail attachment: PASS (exact)")
    print(f"literal_tails={ledger['literal_tail_occurrence_count']}")
    print(f"tail_degrees={ledger['tail_degree_histogram']}")
    print(f"complete_routes={ledger['complete_response_route_counts']}")
    print("earliest_obstruction=response-dark forced hole (x,v)")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
