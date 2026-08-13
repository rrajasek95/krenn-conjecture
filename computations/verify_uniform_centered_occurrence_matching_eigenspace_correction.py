#!/usr/bin/env python3
"""Identify and kill the first centered-transfer matching eigenspace.

The 0/1 debt in the full-endpoint transfer is the centered edge-incidence
module E_1=[2h-2,2] of the perfect-matching switch graph.  Its adjacency
eigenvalue is lambda_h=h^2-3h+1, while constants have degree h(h-1).
Thus (A_h-lambda_h I)/(2h-1) is the rational constant projector on
1+E_1; its integral numerator kills the coefficient-one debt.

Applied fibrewise to the negative Gram row of the full endpoint transfer,
this produces an integral centered candidate which is constant on every
ordered-endpoint fibre and keeps a nonzero marked coefficient.  It is not
the full occurrence projector: different endpoint fibres still carry
different constants.  Moreover A_h is currently a coefficient switch, not
a source-valid Hasse cell; its two-edge product-rule commutator is the next
physical obligation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / (
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py"
)
BASE_SPEC = importlib.util.spec_from_file_location(
    "verify_uniform_centered_occurrence_full_endpoint_transfer_gate",
    BASE_PATH,
)
if BASE_SPEC is None or BASE_SPEC.loader is None:
    raise RuntimeError(("cannot load base transfer checker", BASE_PATH))
BASE = importlib.util.module_from_spec(BASE_SPEC)
BASE_SPEC.loader.exec_module(BASE)

PINS = {
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py":
        "6f5686298143b584a4edcb350145bf9d648277972aa96b90443c4ce254cb1d30",
    "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py":
        "c52cec702336ecdd821617ba21c66538cdbbdf2fc964b3d1637dfaf25c9bae6b",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
}
EXPECTED_LEDGER_SHA256 = "19fae004aa82be477cd91354387ad9e49473e481d7aefb764b5b709ee9607b97"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(vectors) -> int:
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right
                          for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def switch_neighbors(matching):
    matching = tuple(matching)
    answer = []
    for left_index, right_index in combinations(range(len(matching)), 2):
        a, b = matching[left_index]
        c, d = matching[right_index]
        untouched = tuple(
            value for index, value in enumerate(matching)
            if index not in (left_index, right_index)
        )
        answer.append(tuple(sorted(untouched + (
            BASE.edge(a, c), BASE.edge(b, d)
        ))))
        answer.append(tuple(sorted(untouched + (
            BASE.edge(a, d), BASE.edge(b, c)
        ))))
    require(len(answer) == len(set(answer)),
            ("switch graph acquired repeated neighbors", matching))
    return tuple(answer)


def matching_eigenspace_audit():
    records = {}
    for h in range(3, 6):
        vertices = tuple(range(2 * h))
        matchings = tuple(BASE.perfect_matchings(vertices))
        lookup = {value: index for index, value in enumerate(matchings)}
        degree = h * (h - 1)
        eigenvalue = h * h - 3 * h + 1
        require(eigenvalue != 0 and degree - eigenvalue == 2 * h - 1,
                ("switch eigenvalue arithmetic changed", h))

        adjacency = []
        for matching in matchings:
            neighbors = switch_neighbors(matching)
            require(len(neighbors) == degree
                    and all(value in lookup for value in neighbors),
                    ("switch graph degree changed", h, matching))
            adjacency.append(tuple(lookup[value] for value in neighbors))

        edges = tuple(combinations(vertices, 2))
        centered_incidence = []
        for selected_edge in edges:
            phi = tuple(Q(int(selected_edge in matching))
                        for matching in matchings)
            observed = tuple(sum(phi[index] for index in neighbors)
                             for neighbors in adjacency)
            expected = tuple(Q(1) + eigenvalue * value for value in phi)
            require(observed == expected,
                    ("edge-incidence eigenidentity changed", h, selected_edge))
            centered = tuple(value - Q(1, 2 * h - 1) for value in phi)
            observed_centered = tuple(
                sum(centered[index] for index in neighbors)
                for neighbors in adjacency
            )
            require(observed_centered == tuple(
                eigenvalue * value for value in centered
            ), ("centered edge eigenspace changed", h, selected_edge))
            centered_incidence.append(centered)

        e1_dimension = rank(centered_incidence)
        require(e1_dimension == h * (2 * h - 3),
                ("E1 dimension changed", h, e1_dimension))

        fixed = matchings[0]
        common_edge = tuple(Q(len(set(fixed) & set(matching)))
                            for matching in matchings)
        switched = tuple(sum(common_edge[index] for index in neighbors)
                         for neighbors in adjacency)
        require(switched == tuple(
            Q(h) + eigenvalue * value for value in common_edge
        ), ("common-edge radial eigenidentity changed", h))
        numerator = tuple(left - eigenvalue * right
                          for left, right in zip(
                              switched, common_edge, strict=True
                          ))
        require(numerator == (Q(h),) * len(matchings),
                ("integral constant projection changed", h))

        records[h] = {
            "perfect_matchings": len(matchings),
            "switch_degree": degree,
            "E1_partition": f"[{2*h-2},2]",
            "E1_dimension": e1_dimension,
            "E1_eigenvalue": eigenvalue,
            "constant_minus_E1_eigenvalue": 2 * h - 1,
            "integral_identity": "(A-lambda I)t_f=h*1",
        }

    # lambda_h cannot vanish at an integer h: its discriminant is 5.
    require(all(h * h - 3 * h + 1 for h in range(3, 501)),
            "switch E1 eigenvalue acquired an integer zero")
    return {
        "eigenspace": "centered edge incidence E1=[2h-2,2]",
        "dimension": "h(2h-3)",
        "switch_degree": "d_h=h(h-1)",
        "switch_eigenvalue": "lambda_h=h^2-3h+1 (nonzero for integer h)",
        "rational_projector_on_1_plus_E1": "(A_h-lambda_h I)/(2h-1)",
        "integral_numerator": "A_h-lambda_h I",
        "bounded_exact_checks": records,
    }


def full_gram_row(h: int):
    big_occurrences, fibres = BASE.chart_fibres(h)
    marked = BASE.marked_occurrence(h)
    gram = Counter()
    for _chart, image in fibres:
        multiplicity = image.get(marked, 0)
        if not multiplicity:
            continue
        for occurrence, value in image.items():
            gram[occurrence] += multiplicity * value
    return big_occurrences, marked, gram


def endpoint_constant(marked, endpoint_pair, h: int):
    marked_p, marked_s, marked_matching = marked
    p_site, s_site = endpoint_pair
    q_value = sum(
        int(p_site not in selected and s_site not in selected)
        for selected in marked_matching
    )
    if p_site == marked_p and s_site == marked_s:
        constant = 4 * h * h + 4 * h
    elif p_site == marked_p or s_site == marked_s:
        constant = 2 * h - 1
    else:
        constant = 0
    return q_value, constant


def matching_flat_candidate_audit():
    h = 3
    big_occurrences, marked, gram = full_gram_row(h)
    small_count = BASE.occurrence_count(h)
    raw_marked_mass = 7 * h * small_count
    eigenvalue = h * h - 3 * h + 1
    normalization = 2 * h - 1

    flat_numerator = {}
    fibres = defaultdict(list)
    occurrence_set = set(big_occurrences)
    for occurrence in big_occurrences:
        p_site, s_site, matching = occurrence
        neighbors = (
            (p_site, s_site, neighbor)
            for neighbor in switch_neighbors(matching)
        )
        adjacency_value = sum(gram[value] for value in neighbors
                              if value in occurrence_set)
        flat_numerator[occurrence] = adjacency_value - eigenvalue * gram[occurrence]
        fibres[(p_site, s_site)].append(occurrence)

    endpoint_values = {}
    for endpoint_pair, values in fibres.items():
        observed = {flat_numerator[value] for value in values}
        require(len(observed) == 1,
                ("matching filter did not flatten endpoint fibre",
                 endpoint_pair, observed))
        q_value, constant = endpoint_constant(marked, endpoint_pair, h)
        expected = q_value + normalization * constant
        require(observed == {expected},
                ("flattened endpoint coefficient changed",
                 endpoint_pair, observed, expected))
        endpoint_values[endpoint_pair] = expected

    require(sum(flat_numerator.values())
            == normalization * sum(gram.values()),
            "matching filter changed total mass incorrectly")
    integral_candidate = {
        occurrence: normalization * raw_marked_mass
        * int(occurrence == marked) - flat_numerator[occurrence]
        for occurrence in big_occurrences
    }
    require(sum(integral_candidate.values()) == 0,
            "integral matching-flat candidate stopped being centered")
    marked_coefficient = integral_candidate[marked]
    require(marked_coefficient > 0,
            ("matching-flat filter killed the marked occurrence",
             marked_coefficient))

    reversed_endpoints = (marked[1], marked[0])
    require(endpoint_values[reversed_endpoints] == h,
            "coefficient-one reversed-endpoint debt was not flattened")
    reversed_coefficients = {
        integral_candidate[value] for value in fibres[reversed_endpoints]
    }
    require(reversed_coefficients == {-h},
            ("reversed endpoint fibre did not become constant",
             reversed_coefficients))

    nonmarked_fibre_constants = {
        integral_candidate[values[0]]
        for endpoint_pair, values in fibres.items()
        if endpoint_pair != (marked[0], marked[1])
    }
    require(len(nonmarked_fibre_constants) > 1,
            "endpoint debt unexpectedly vanished with matching filter")

    return {
        "exact_step": "h=3 to h=4 selected response",
        "rational_filter": "Pi_match=(A-lambda I)/(2h-1)",
        "integral_candidate": (
            "K_match^Z=(2h-1)(7hN_h)e_f-(A-lambda I)k_f"
        ),
        "marked_coefficient": marked_coefficient,
        "reversed_endpoint_fibre_coefficient": -h,
        "matching_variation_remaining": False,
        "number_of_endpoint_fibre_constants": len(set(endpoint_values.values())),
        "endpoint_fibre_variation_remaining": True,
        "full_centered_projector_constructed": False,
    }


def product_rule_face_audit():
    higher = (ROOT / (
        "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py"
    )).read_text()
    ridge = (ROOT / (
        "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py"
    )).read_text()
    require("Reynolds product witness lost its 1/3 commutator" in higher
            and "matching/Bianchi differences enlarged the complete module"
            in ridge,
            "physical matching-switch commutator scope changed")
    records = {}
    for h in range(3, 31):
        degree = h * (h - 1)
        eigenvalue = h * h - 3 * h + 1
        require(degree - eigenvalue == 2 * h - 1,
                ("face normalization changed", h))
        records[h] = {
            "two_switch_neighbors_per_matching": degree,
            "integral_identity_coefficient": -eigenvalue,
            "constant_normalization": 2 * h - 1,
            "new_pair_factors_per_switch_term": 2,
        }
    return {
        "coefficient_operator": (
            "A_h replaces two residual edges ab|cd by the two switches "
            "ac|bd and ad|bc"
        ),
        "formal_local_product_face": (
            "d(q_ac q_bd+q_ad q_bc) has the four one-derivative terms; "
            "the -lambda_h identity term carries the old-edge faces"
        ),
        "known_physical_switches_suffice": False,
        "reason": (
            "existing matching/Bianchi switches are differences of already "
            "coupled ridge/response columns and do not enlarge that physical "
            "image; the Reynolds audit independently shows nonzero Leibniz "
            "commutators.  A_h is therefore only a coefficient operator "
            "until an augmented two-edge Hasse/Spencer cell is supplied"
        ),
        "possible_order_covariant": (
            "each corrected induction step has a quadratic two-edge face, "
            "the numerical degree needed to build order 2h-6 after h-3 "
            "steps, but its clean-line Sym^2 type, target/residue/q typing, "
            "and common-Hankel compatibility are unproved"
        ),
        "first_physical_obligation": (
            "lift A_h-lambda_h I to a source-valid word/fine/repeated-grade "
            "two-switch cell whose product-rule commutator is killed or "
            "typed terminal; then solve the remaining ordered-endpoint "
            "association classes"
        ),
        "orders_audited": records,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "uniform centered occurrence matching eigenspace correction",
        "pins": PINS,
        "matching_eigenspace": matching_eigenspace_audit(),
        "matching_flat_candidate": matching_flat_candidate_audit(),
        "product_rule_faces": product_rule_face_audit(),
        "verdict": (
            "The coefficient-one residual is exactly the E1=[2h-2,2] "
            "matching-incidence sector.  The rational projector "
            "(A-lambda I)/(2h-1), or its integral numerator with scaled "
            "marked mass, kills it uniformly and leaves a centered, "
            "matching-flat candidate.  It does not finish the occurrence "
            "projector: ordered-endpoint fibre constants remain.  Physical "
            "use also requires a new augmented two-edge product-rule cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("matching eigenspace correction ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("coefficient-one residual: E1=[2h-2,2]")
    print("switch eigenvalue: h^2-3h+1 (NONZERO)")
    print("matching-flat integral centered candidate: CONSTRUCTED")
    print("remaining endpoint classes + physical two-switch face: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
