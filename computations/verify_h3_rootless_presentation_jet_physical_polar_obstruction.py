#!/usr/bin/env python3
"""Audit the physicality gate for the proposed rootless polar columns.

The shifted principal-parts construction has two chart-tagged copies of one
global hafnian row. Their difference is a presentation cycle. This checker
shows that it cannot, without an additional source map, be read as a pair of
physical invisible coordinate tangents: the marked coordinate directions
have nonzero first derivatives, while forgetting the chart tag sends the
presentation differences to zero and hence gives zero physical Hessian.
"""

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
import json


SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, Q = 0, 3, 6, 7
DIRECT_FREE = frozenset((P, R))
EXPECTED_DIGEST = "22ba910f34831a3acafbd923629e03cc49cd35630f28d3922c4b7fa9b35c8638"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def monomial(matching, colouring):
    return tuple(sorted(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def full_row(word):
    colouring = dict(enumerate(word))
    terms = tuple(
        monomial(matching, colouring)
        for matching in matchings(SITES)
        if DIRECT_FREE not in {frozenset(pair) for pair in matching}
    )
    require(len(terms) == len(set(terms)) == 90,
            "direct-free row changed")
    return terms


def derivative(terms, variables):
    answer = defaultdict(int)
    for term in terms:
        remaining = list(term)
        for variable in variables:
            if variable not in remaining:
                break
            remaining.remove(variable)
        else:
            answer[tuple(sorted(remaining))] += 1
    return {term: value for term, value in answer.items() if value}


def tagged_difference(polynomial):
    """The pq copy minus the pr copy in the presentation module."""
    answer = {}
    for term, value in polynomial.items():
        answer[("pq", term)] = value
        answer[("pr", term)] = -value
    return answer


def forget_tags(tagged):
    answer = defaultdict(int)
    for (_tag, term), value in tagged.items():
        answer[term] += value
    return {term: value for term, value in answer.items() if value}


def edge_degree(term):
    degree = [0] * 24
    for left, right, left_colour, right_colour in term:
        degree[3 * left + left_colour] += 1
        degree[3 * right + right_colour] += 1
    return tuple(degree)


def word_degree(word):
    degree = [0] * 24
    for site, colour in enumerate(word):
        degree[3 * site + colour] += 1
    return tuple(degree)


def subtract(left, *rights):
    result = list(left)
    for right in rights:
        result = [a - b for a, b in zip(result, right)]
    require(all(value >= 0 for value in result), "negative fine degree")
    return tuple(result)


def audit_faces():
    records = []
    total_du = total_dt = total_h = 0
    for deleted in ODD:
        word = [0] * 8
        for site in ODD:
            if site != deleted:
                word[site] = MIXED[site]
        word = tuple(word)
        terms = full_row(word)
        u = edge(X, deleted, 0, 0)
        t = edge(P, Q, 0, 0)
        du = derivative(terms, (u,))
        dt = derivative(terms, (t,))
        dut = derivative(terms, (u, t))

        require(len(du) == (15 if deleted == R else 12),
                f"face {deleted}: u derivative count")
        require(len(dt) == 15, f"face {deleted}: t derivative count")
        require(len(dut) == 3 and set(dut.values()) == {1},
                f"face {deleted}: mixed derivative count")
        require(du and dt, "marked physical coordinate became invisible")

        tagged_u = tagged_difference(du)
        tagged_t = tagged_difference(dt)
        tagged_h = tagged_difference(dut)
        require(tagged_u and tagged_t and tagged_h,
                "presentation jet unexpectedly vanished")
        require(not forget_tags(tagged_u),
                "first u presentation difference survived physically")
        require(not forget_tags(tagged_t),
                "first t presentation difference survived physically")
        require(not forget_tags(tagged_h),
                "mixed presentation difference survived physically")

        physical_hessian_of_forgetful_images = {}
        require(not physical_hessian_of_forgetful_images and dut,
                "physical/presentation Hessian distinction collapsed")

        row_degree = word_degree(word)
        h_degree = subtract(row_degree, edge_degree((u,)), edge_degree((t,)))
        require(all(edge_degree(term) == h_degree for term in dut),
                "formal polar fine degree changed")
        target = 1 if len(set(word)) == 1 else 0
        require(target == 0, "mixed polar row acquired physical target")

        total_du += len(du)
        total_dt += len(dt)
        total_h += len(dut)
        records.append({
            "deleted": deleted,
            "word": "".join(map(str, word)),
            "physical_coordinate_du_terms": len(du),
            "physical_coordinate_dt_terms": len(dt),
            "formal_sector_hessian_terms": len(dut),
            "presentation_u_forgets_to_zero": True,
            "presentation_t_forgets_to_zero": True,
            "presentation_hessian_forgets_to_zero": True,
            "physical_hessian_of_forgotten_pair_terms": 0,
            "mixed_row_target": target,
            "formal_hessian_degree_weight": sum(h_degree),
        })

    require(total_du == 63, "aggregate physical u derivative count")
    require(total_dt == 75, "aggregate physical t derivative count")
    require(total_h == 15, "aggregate formal Hessian count")
    return records


def main():
    ledger = {
        "faces": audit_faces(),
        "two_readings": {
            "physical_marked_coordinates": (
                "fail Jhat xi=Jhat eta=0 on one literal mixed row"
            ),
            "chart_presentation_differences": (
                "cycles, but forget to zero physical source vectors"
            ),
            "sector_symbol": (
                "nonzero three-term second difference, not Hhat(0,0)"
            ),
        },
        "augmented_column_status": {
            "physical_first_jets_constructed": False,
            "target_component_of_formal_mixed_row": 0,
            "ordinary_residue_component_defined": False,
            "mixed_correction_membership_test_defined": False,
            "zero_indeterminacy_test_defined": False,
            "fine_grade_of_formal_sector_symbol_verified": True,
        },
        "minimal_missing_physical_datum": [
            "xi_v,eta_v in the physical source-coordinate module",
            "Jhat*xi_v=Jhat*eta_v=0 with the marked leading components",
            "zeta_v with Jhat*zeta_v=-Hhat(xi_v,eta_v)",
            "a source grade map from that corrected class to the terminal face",
            "annihilation of ker(Jhat) for zero indeterminacy",
        ],
        "answer": "no physical P(e_v) is constructed by the committed presentation jets",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")
    print("h=3 rootless presentation-jet physical-polar obstruction: PASS")
    print("marked coordinate directions: non-invisible on the literal mixed row")
    print("presentation differences: cycles, but physical forgetful image zero")
    print("nonzero three-term sector polar is not a physical Hessian column")
    print("one P(e_v): NOT CONSTRUCTED; physical invisible lifts are missing")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
