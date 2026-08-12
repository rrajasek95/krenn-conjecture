#!/usr/bin/env python3
"""Compute the literal primitive face of the endpoint-recoloured class.

This is the physical grading audit omitted by the unrecoloured bridge probe.
It antisymmetrizes the exact order-six class under the tail-colour Weyl
involution, performs the endpoint recolouring with its Weyl correction,
removes the primitive 07:11 and 24:11 directions, and evaluates the remaining
operator on all three quadratic source products.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    "computations/verify_h3_order6_to_repeated_grade_bridge.py":
        "30c5df97584a01dfcf121cd48affa8525c058e00a69f8806b6ae81492fff9cda",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
}
EXPECTED_LEDGER_SHA256 = "bee8fafb4de176d1049c816f0726870a9f001a44271cdde28c695c10ff533369"
PRIMITIVE_PAIR = ((0, 7, 1, 1), (2, 4, 1, 1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def swap_tail(cell):
    left, right, a, b = cell
    if left in (2, 5) and a in (1, 2):
        a = 3 - a
    if right in (2, 5) and b in (1, 2):
        b = 3 - b
    return left, right, a, b


def endpoint_compose(operator):
    source_xv = (0, 1, 1, 1)
    source_pq = (6, 7, 1, 1)
    target_xv = (0, 1, 0, 1)
    target_pq = (6, 7, 2, 2)
    answer = Counter()
    for (coefficient, directions), weight in operator.items():
        answer[(tuple(sorted(coefficient + (target_xv, target_pq))),
                tuple(sorted(directions + (source_xv, source_pq))))] += weight
        for position, cell in enumerate(coefficient):
            if cell != source_xv:
                continue
            remainder = coefficient[:position] + coefficient[position + 1:]
            answer[(tuple(sorted(remainder + (target_xv, target_pq))),
                    tuple(sorted(directions + (source_pq,))))] += weight
    return +answer


def degree(monomial):
    result = [0] * 24
    for left, right, a, b in monomial:
        result[3 * left + a] += 1
        result[3 * right + b] += 1
    return tuple(result)


def site_profile(value):
    return tuple(sum(value[3 * site:3 * site + 3]) for site in range(8))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    hasse = load(
        "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py",
        "endpoint_face_hasse",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "endpoint_face_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "endpoint_face_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "endpoint_face_base",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "endpoint_face_complete",
    )
    bridge = load(
        "computations/verify_h3_order6_to_repeated_grade_bridge.py",
        "endpoint_face_bridge",
    )
    terms, pair_shadow = hasse.exact_solution_terms()
    require(pair_shadow[tuple(sorted(PRIMITIVE_PAIR))] == 1,
            "primitive pair normalization changed")
    theta = Counter({(coefficient, directions): weight
                     for weight, coefficient, directions in terms})
    swapped = Counter()
    for (coefficient, directions), weight in theta.items():
        swapped[(tuple(sorted(map(swap_tail, coefficient))),
                 tuple(sorted(map(swap_tail, directions))))] += weight
    antisymmetric = Counter(theta)
    for term, value in swapped.items():
        antisymmetric[term] -= value
    antisymmetric = Counter({term: value / 2 for term, value in
                             antisymmetric.items() if value})
    composition = endpoint_compose(antisymmetric)

    system = repair.build_system(base, commutator)
    outputs = []
    output_polynomials = {}
    output_degrees = []
    for product_index, source_product in enumerate(system["products"]):
        output = Counter()
        used_operators = 0
        for (coefficient, directions), weight in composition.items():
            remaining = list(directions)
            if not all(cell in remaining for cell in PRIMITIVE_PAIR):
                continue
            for cell in PRIMITIVE_PAIR:
                remaining.remove(cell)
            used_operators += 1
            for tail, value in repair.derivatives(
                    source_product, tuple(remaining)).items():
                output[tuple(sorted(coefficient + tail))] += weight * value
        output = +output
        degrees = sorted({degree(monomial) for monomial in output})
        outputs.append({
            "product": product_index,
            "operators_with_primitive_pair": used_operators,
            "support": len(output),
            "l1": str(sum(abs(value) for value in output.values())),
            "fine_degree_count": len(degrees),
            "site_profiles": [list(site_profile(value)) for value in degrees],
            "fine_degrees": [list(value) for value in degrees],
        })
        for index, value in enumerate(degrees):
            output_polynomials[(product_index, index)] = Counter({
                monomial: coefficient for monomial, coefficient in output.items()
                if degree(monomial) == value
            })
        output_degrees.extend((product_index, index, value)
                              for index, value in enumerate(degrees))

    repeated = []
    repeated_raw = []
    for component, (left, right, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        value = complete.degree_add(
            base.lambda_degree(left),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        repeated.append({
            "component": component,
            "faces": [left, right],
            "site_profile": list(site_profile(value)),
            "fine_degree": list(value),
        })
        repeated_raw.append((component, left, right, value))

    bridge_records = []
    for product_index, fine_index, source_degree in output_degrees:
        for component, left, right, target_degree in repeated_raw:
            fixed = bridge.one_edge_difference(source_degree, target_degree)
            transported = bridge.transported_one_edge_bridges(
                source_degree, target_degree)
            differential = bridge.arm_contraction_two_edge_bridges(
                source_degree, target_degree, complete, base)
            covariance = bridge.covariance_arm_contraction_bridges(
                source_degree, target_degree, complete, base)
            if fixed is not None or transported or differential or covariance:
                bridge_records.append({
                    "primitive": [product_index, fine_index],
                    "component": component,
                    "faces": [left, right],
                    "fixed_one_edge": list(fixed) if fixed is not None else None,
                    "transported_one_edge_count": len(transported),
                    "fixed_arm_contraction_count": len(differential),
                    "covariance_arm_contraction_count": len(covariance),
                    "first_covariance_arm_contraction": (
                        covariance[0] if covariance else None
                    ),
                })

    require(len(bridge_records) == 2
            and {tuple(record["primitive"]) for record in bridge_records}
            == {(1, 0), (2, 0)}
            and {record["component"] for record in bridge_records} == {1}
            and {record["covariance_arm_contraction_count"]
                 for record in bridge_records} == {192},
            "endpoint-recoloured normalized bridge classification changed")
    canonical = bridge_records[0]["first_covariance_arm_contraction"]
    require(canonical["contracted_arm"] == [0, 7, 0, 1]
            and canonical["inserted_two_edge_tail"]
            == [[1, 3, 0, 0], [4, 5, 0, 0]]
            and canonical["colour_permutations_source_to_target"]
            == [[1, 0, 2], [0, 1, 2], [1, 0, 2], [0, 1, 2],
                [0, 1, 2], [0, 1, 2], [1, 2, 0], [1, 2, 0]],
            "endpoint-recoloured canonical bridge representative changed")

    component_one_degree = repeated_raw[1][3]
    component_one = complete.component(base, component_one_degree)
    literal = []
    for key in ((1, 0), (2, 0)):
        transformed, hit_terms = bridge.transform_primitive_face(
            output_polynomials[key], canonical, base)
        membership, remainder = bridge.full_component_membership(
            component_one, transformed)
        literal.append({
            "primitive": list(key),
            "terms_containing_the_abstract_contracted_edge": hit_terms,
            "transformed_support": len(transformed),
            "in_old_repeated_component": membership["in_span"],
            "remainder_support": membership["remainder_support"],
        })

    require([(record["operators_with_primitive_pair"], record["support"],
              record["l1"], record["fine_degree_count"])
             for record in outputs]
            == [(168, 21, "663", 1), (168, 54, "961/2", 2),
                (168, 32, "444", 1)],
            "endpoint-recoloured literal output census changed")
    require(all(record["site_profiles"]
                == [[2, 1, 2, 1, 2, 1, 1, 2]]
                * record["fine_degree_count"] for record in outputs),
            "endpoint-recoloured site profile changed")
    require(all(record["terms_containing_the_abstract_contracted_edge"] == 0
                and record["transformed_support"] == 0
                for record in literal),
            "abstract covariance contraction became a literal edge derivative")

    return {
        "theorem": "literal endpoint-recoloured primitive face grading",
        "antisymmetric_order6_terms": len(antisymmetric),
        "endpoint_recoloured_terms": len(composition),
        "outputs": outputs,
        "first_repeated_components": repeated,
        "normalized_bridge_records": bridge_records,
        "literal_contracted_edge_test": literal,
        "conclusion": (
            "the endpoint-recoloured physical primitive face has the same "
            "site profile and one normalized stub-level covariance-Spencer "
            "degree bridge to the faces-3/5 component, but the abstract "
            "contracted edge 07:01 occurs in no literal term; the bridge is "
            "a principal-parts/site-colour contraction, not an edge "
            "derivative or an old-column identity"
        ),
        "scope": (
            "literal endpoint-recoloured antisymmetric order-six primitive "
            "face on the three quadratic source products; no relative "
            "boundary, augmented comparison, or rank landing asserted"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint primitive grade ledger changed", digest))
    print("h3 endpoint-recoloured primitive face grading")
    print("outputs:", [(record["support"], record["fine_degree_count"],
                        record["site_profiles"]) for record in ledger["outputs"]])
    print("output records:", ledger["outputs"])
    print("normalized bridge records:", ledger["normalized_bridge_records"])
    print("literal contracted-edge test:", ledger["literal_contracted_edge_test"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
