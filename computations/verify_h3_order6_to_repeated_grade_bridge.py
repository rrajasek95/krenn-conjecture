#!/usr/bin/env python3
"""Locate the first multigraded bridge from the primitive order-six face.

The literal primitive face has polynomial degree six.  The five first
rootless collision components have polynomial degree seven.  This audit
reconstructs every fine degree of the primitive face and every cyclic
P3+K2 target degree, then tests whether the latter is obtained from the
former by one decorated physical edge in the fixed labelling.

The result is deliberately only the first grading test.  If no fixed-label
edge exists, a physical comparison must include a labelled covariance/site
transport before the one-edge promotion; it cannot be an unlabelled common
multiplier assertion.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_primitive_face_literal_boundary.py":
        "5fbb2458dd98cf4d647ef72eff7a7b58e4dcfb2a7281bc4c433db7f75b020c4c",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = "f31903449a1c8b4a343b95b9399fbe4677be22eb2050e2f5a5c4fc46f3a5adef"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def degree_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def site_profile(degree):
    return tuple(sum(degree[3 * site:3 * site + 3]) for site in range(8))


def one_edge_difference(left, right):
    difference = tuple(b - a for a, b in zip(left, right, strict=True))
    if any(value < 0 for value in difference) or sum(difference) != 2:
        return None
    slots = [index for index, value in enumerate(difference) for _ in range(value)]
    if len(slots) != 2:
        return None
    sites = [slot // 3 for slot in slots]
    if sites[0] == sites[1]:
        return None
    return tuple(slots)


COLOUR_PERMUTATIONS = tuple(permutations(range(3)))


def colour_transport(source, target):
    """Return one source-colour -> target-colour permutation, if it exists."""
    for permutation in COLOUR_PERMUTATIONS:
        if all(source[colour] == target[permutation[colour]]
               for colour in range(3)):
            return permutation
    return None


def role_preserving_site_permutations():
    """Fix x=0, permute residual sites, and preserve the endpoint set 6,7."""
    for residual in permutations(range(1, 6)):
        for endpoints in ((6, 7), (7, 6)):
            yield (0,) + residual + endpoints


def transported_one_edge_bridges(source_degree, target_degree):
    """All bridges modulo normalized physical site and local-colour gauges."""
    records = []
    for left in range(8):
        for right in range(left + 1, 8):
            for left_colour in range(3):
                for right_colour in range(3):
                    extended = list(source_degree)
                    extended[3 * left + left_colour] += 1
                    extended[3 * right + right_colour] += 1
                    for site_permutation in role_preserving_site_permutations():
                        colour_permutations = []
                        for source_site, target_site in enumerate(site_permutation):
                            source_local = tuple(
                                extended[3 * source_site + colour]
                                for colour in range(3)
                            )
                            target_local = tuple(
                                target_degree[3 * target_site + colour]
                                for colour in range(3)
                            )
                            transport = colour_transport(source_local, target_local)
                            if transport is None:
                                break
                            colour_permutations.append(transport)
                        else:
                            records.append({
                                "source_edge": [left, right, left_colour,
                                                right_colour],
                                "target_edge": [
                                    site_permutation[left],
                                    site_permutation[right],
                                    colour_permutations[left][left_colour],
                                    colour_permutations[right][right_colour],
                                ],
                                "site_permutation_source_to_target":
                                    list(site_permutation),
                                "colour_permutations_source_to_target": [
                                    list(value) for value in colour_permutations
                                ],
                            })
    return records


def arm_contraction_two_edge_bridges(source_degree, target_degree, complete, base):
    """Bridges of the form (two-edge coefficient)*partial_(07:a,b)."""
    records = []
    for left_colour in range(3):
        for right_colour in range(3):
            if (source_degree[3 * 0 + left_colour] == 0
                    or source_degree[3 * 7 + right_colour] == 0):
                continue
            remainder = [b - a for a, b in zip(
                source_degree, target_degree, strict=True
            )]
            remainder[3 * 0 + left_colour] += 1
            remainder[3 * 7 + right_colour] += 1
            if any(value < 0 for value in remainder) or sum(remainder) != 4:
                continue
            stubs = tuple(sorted(
                (site, colour)
                for site in range(8)
                for colour in range(3)
                for _ in range(remainder[3 * site + colour])
            ))
            pairings = complete.multiplier_pairings(base, stubs)
            for pairing in pairings:
                require(len(pairing) == 2,
                        ("arm bridge stopped having two coefficient edges", pairing))
                records.append({
                    "contracted_arm": [0, 7, left_colour, right_colour],
                    "inserted_two_edge_tail": [list(cell) for cell in pairing],
                    "inserted_tail_site_profile": list(site_profile(remainder)),
                })
    return records


def covariance_arm_contraction_bridges(source_degree, target_degree, complete, base):
    """Arm contraction/two-edge insertion followed by sitewise colour transport."""
    records = []
    source_profile = site_profile(source_degree)
    target_profile = site_profile(target_degree)
    for left_colour in range(3):
        for right_colour in range(3):
            if (source_degree[left_colour] == 0
                    or source_degree[3 * 7 + right_colour] == 0):
                continue
            site_remainder = [b - a for a, b in zip(
                source_profile, target_profile, strict=True
            )]
            site_remainder[0] += 1
            site_remainder[7] += 1
            if any(value < 0 for value in site_remainder) or sum(site_remainder) != 4:
                continue
            site_stubs = tuple(sorted(
                site for site, count in enumerate(site_remainder)
                for _ in range(count)
            ))
            undecorated_pairings = set()
            if site_stubs:
                first = site_stubs[0]
                for position, second in enumerate(site_stubs[1:], start=1):
                    if first == second:
                        continue
                    rest = site_stubs[1:position] + site_stubs[position + 1:]
                    require(len(rest) == 2, "two-edge site stub count changed")
                    if rest[0] == rest[1]:
                        continue
                    undecorated_pairings.add(tuple(sorted(
                        ((first, second), (rest[0], rest[1]))
                    )))
            for pairing in sorted(undecorated_pairings):
                incident_sites = tuple(site for edge in pairing for site in edge)
                for colours in product(range(3), repeat=4):
                    extended = list(source_degree)
                    extended[left_colour] -= 1
                    extended[3 * 7 + right_colour] -= 1
                    decorated = []
                    for edge_index, (left, right) in enumerate(pairing):
                        a = colours[2 * edge_index]
                        b = colours[2 * edge_index + 1]
                        extended[3 * left + a] += 1
                        extended[3 * right + b] += 1
                        decorated.append(base.edge(left, right, a, b))
                    colour_permutations = []
                    for site in range(8):
                        transport = colour_transport(
                            tuple(extended[3 * site:3 * site + 3]),
                            tuple(target_degree[3 * site:3 * site + 3]),
                        )
                        if transport is None:
                            break
                        colour_permutations.append(transport)
                    else:
                        records.append({
                            "contracted_arm": [0, 7, left_colour, right_colour],
                            "inserted_two_edge_tail": [list(cell) for cell in decorated],
                            "inserted_tail_sites": list(incident_sites),
                            "colour_permutations_source_to_target": [
                                list(value) for value in colour_permutations
                            ],
                        })
    return records


def primitive_degrees(primitive):
    hasse = primitive.load(
        "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py",
        "bridge_hasse",
    )
    repair = primitive.load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "bridge_repair",
    )
    commutator = primitive.load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "bridge_commutator",
    )
    base = primitive.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "bridge_primitive_base",
    )
    system = repair.build_system(base, commutator)
    terms, pair_shadow = hasse.exact_solution_terms()
    require(pair_shadow[tuple(sorted(primitive.PRIMITIVE_PAIR))] == 1,
            "primitive pair coefficient changed")

    answer = []
    outputs = {}
    for product_index, source_product in enumerate(system["products"]):
        output = Counter()
        for weight, coefficient, directions in terms:
            remaining = list(directions)
            for selected in primitive.PRIMITIVE_PAIR:
                require(selected in remaining,
                        ("primitive direction missing", selected))
                remaining.remove(selected)
            for tail, value in repair.derivatives(
                    source_product, tuple(remaining)).items():
                output[tuple(sorted(coefficient + tail))] += weight * value
        output = +output
        degrees = sorted({primitive.degrees(monomial)[1] for monomial in output})
        for index, degree in enumerate(degrees):
            answer.append((product_index, index, degree))
            outputs[(product_index, index)] = Counter({
                monomial: value for monomial, value in output.items()
                if primitive.degrees(monomial)[1] == degree
            })
    return answer, outputs


def repeated_degrees(complete, base):
    answer = []
    for component, (left_face, right_face, left_cell, right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        left = complete.degree_add(
            base.lambda_degree(left_face),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        right = complete.degree_add(
            base.lambda_degree(right_face),
            complete.cell_degree(complete.CYCLE_CELLS[right_cell]),
        )
        require(left == right, ("repeated component degree mismatch", component))
        answer.append((component, left_face, right_face, left))
    return answer


def transform_primitive_face(polynomial, bridge, base):
    contracted = tuple(bridge["contracted_arm"])
    tail = tuple(tuple(cell) for cell in bridge["inserted_two_edge_tail"])
    transports = tuple(tuple(value) for value in
                       bridge["colour_permutations_source_to_target"])
    answer = Counter()
    hit_terms = 0
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(contracted)
        if not multiplicity:
            continue
        hit_terms += 1
        remaining = list(monomial)
        remaining.remove(contracted)
        transformed = []
        for left, right, left_colour, right_colour in tuple(remaining) + tail:
            transformed.append(base.edge(
                left, right,
                transports[left][left_colour],
                transports[right][right_colour],
            ))
        answer[tuple(sorted(transformed))] += multiplicity * coefficient
    return +answer, hit_terms


def subtract_sparse(target, source, coefficient):
    for row, value in source.items():
        updated = target.get(row, Q(0)) - coefficient * value
        if updated:
            target[row] = updated
        else:
            target.pop(row, None)


def full_component_membership(component, target):
    basis = {}
    for column_index, (_word, _multiplier, boundary) in enumerate(
            component["columns"]):
        vector = {monomial: Q(1) for monomial in boundary}
        expression = {column_index: Q(1)}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = (
                    {row: inverse * value for row, value in vector.items()},
                    {index: inverse * value
                     for index, value in expression.items()},
                )
                break
            basis_vector, basis_expression = basis[pivot]
            coefficient = vector[pivot]
            subtract_sparse(vector, basis_vector, coefficient)
            subtract_sparse(expression, basis_expression, coefficient)

    remainder = {row: Q(value) for row, value in target.items() if value}
    expression = {}
    while remainder:
        pivot = min(remainder)
        if pivot not in basis:
            break
        basis_vector, basis_expression = basis[pivot]
        coefficient = remainder[pivot]
        subtract_sparse(remainder, basis_vector, coefficient)
        for index, value in basis_expression.items():
            expression[index] = expression.get(index, Q(0)) + coefficient * value
            if not expression[index]:
                expression.pop(index)
    return ({
        "in_span": not remainder,
        "component_rank": len(basis),
        "target_support": len(target),
        "expression_support": len(expression) if not remainder else None,
        "remainder_support": len(remainder),
        "first_remainder": repr(min(remainder)) if remainder else None,
        "first_remainder_coefficient": (
            str(remainder[min(remainder)]) if remainder else None
        ),
    }, remainder)


def sparse_pair_rank(left, right):
    if not left:
        return int(bool(right))
    if not right:
        return 1
    pivot = min(left)
    if pivot not in right:
        return 2
    ratio = right[pivot] / left[pivot]
    keys = set(left) | set(right)
    return 1 if all(right.get(key, 0) == ratio * left.get(key, 0)
                    for key in keys) else 2


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    primitive = load(
        "computations/verify_h3_order6_primitive_face_literal_boundary.py",
        "bridge_primitive",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "bridge_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "bridge_base",
    )
    primitive_records, primitive_outputs = primitive_degrees(primitive)
    repeated_records = repeated_degrees(complete, base)

    bridges = []
    transported_bridges = []
    differential_bridges = []
    covariance_differential_bridges = []
    comparisons = []
    for product_index, fine_index, source_degree in primitive_records:
        for component, left_face, right_face, target_degree in repeated_records:
            edge = one_edge_difference(source_degree, target_degree)
            comparisons.append({
                "primitive": [product_index, fine_index],
                "component": component,
                "site_profile_difference": [
                    right - left for left, right in zip(
                        site_profile(source_degree), site_profile(target_degree),
                        strict=True)
                ],
                "one_edge": list(edge) if edge is not None else None,
            })
            if edge is not None:
                bridges.append({
                    "primitive": [product_index, fine_index],
                    "component": component,
                    "faces": [left_face, right_face],
                    "edge_slots": list(edge),
                    "edge": [edge[0] // 3, edge[1] // 3,
                             edge[0] % 3, edge[1] % 3],
                })
            transported = transported_one_edge_bridges(
                source_degree, target_degree)
            if transported:
                transported_bridges.append({
                    "primitive": [product_index, fine_index],
                    "component": component,
                    "faces": [left_face, right_face],
                    "count": len(transported),
                    "first": transported[0],
                })
            differential = arm_contraction_two_edge_bridges(
                source_degree, target_degree, complete, base)
            if differential:
                differential_bridges.append({
                    "primitive": [product_index, fine_index],
                    "component": component,
                    "faces": [left_face, right_face],
                    "count": len(differential),
                    "records": differential,
                })
            covariance_differential = covariance_arm_contraction_bridges(
                source_degree, target_degree, complete, base)
            if covariance_differential:
                covariance_differential_bridges.append({
                    "primitive": [product_index, fine_index],
                    "component": component,
                    "faces": [left_face, right_face],
                    "count": len(covariance_differential),
                    "first": covariance_differential[0],
                })

    unique_primitive_degrees = {record[2] for record in primitive_records}
    require(len(primitive_records) == 4 and len(unique_primitive_degrees) == 2,
            "primitive fine-degree multiplicities changed")
    require(not bridges and not transported_bridges and not differential_bridges,
            "a simpler fixed-label or one-edge bridge appeared")
    require(len(covariance_differential_bridges) == 2
            and {tuple(record["primitive"])
                 for record in covariance_differential_bridges}
            == {(1, 0), (2, 0)}
            and {record["component"]
                 for record in covariance_differential_bridges} == {1}
            and {record["count"]
                 for record in covariance_differential_bridges} == {48},
            "canonical covariance/Spencer bridge classification changed")
    canonical = covariance_differential_bridges[0]["first"]
    require(canonical["contracted_arm"] == [0, 7, 1, 1]
            and canonical["inserted_two_edge_tail"]
            == [[1, 3, 0, 0], [4, 5, 0, 0]]
            and canonical["colour_permutations_source_to_target"]
            == [[1, 0, 2], [0, 1, 2], [1, 0, 2], [0, 1, 2],
                [0, 1, 2], [0, 1, 2], [1, 0, 2], [1, 0, 2]],
            "canonical bridge representative changed")

    component_one_degree = next(
        degree for component, _left, _right, degree in repeated_records
        if component == 1
    )
    component_one = complete.component(base, component_one_degree)
    literal_lifts = []
    lift_remainders = []
    for key in ((1, 0), (2, 0)):
        transformed, hit_terms = transform_primitive_face(
            primitive_outputs[key], canonical, base)
        if transformed:
            require({primitive.degrees(monomial)[1] for monomial in transformed}
                    == {component_one_degree},
                    ("transformed primitive left the repeated degree", key))
        membership, remainder = full_component_membership(
            component_one, transformed)
        lift_remainders.append(remainder)
        literal_lifts.append({
            "primitive": list(key),
            "primitive_terms_divisible_by_07_11": hit_terms,
            "transformed_support": len(transformed),
            "transformed_l1": str(sum(abs(value)
                                       for value in transformed.values())),
            "complete_component_membership": membership,
        })
    literal_quotient_rank = sparse_pair_rank(*lift_remainders)
    require([record["primitive_terms_divisible_by_07_11"]
             for record in literal_lifts] == [27, 16]
            and [record["transformed_support"]
                 for record in literal_lifts] == [27, 16]
            and [record["transformed_l1"]
                 for record in literal_lifts] == ["182/3", "82"]
            and not any(record["complete_component_membership"]["in_span"]
                        for record in literal_lifts)
            and [record["complete_component_membership"]["remainder_support"]
                 for record in literal_lifts] == [186, 104]
            and literal_quotient_rank == 2,
            "literal canonical Spencer quotient changed")

    return {
        "theorem": "first multigraded order-six to repeated-component bridge",
        "primitive_fine_degrees": [
            {
                "product": product_index,
                "fine_index": fine_index,
                "site_profile": list(site_profile(degree)),
                "degree": list(degree),
            }
            for product_index, fine_index, degree in primitive_records
        ],
        "repeated_degrees": [
            {
                "component": component,
                "faces": [left_face, right_face],
                "site_profile": list(site_profile(degree)),
                "degree": list(degree),
            }
            for component, left_face, right_face, degree in repeated_records
        ],
        "fixed_label_one_edge_bridges": bridges,
        "role_and_colour_transport_one_edge_bridges": transported_bridges,
        "endpoint_arm_contraction_two_edge_bridges": differential_bridges,
        "covariance_endpoint_arm_contraction_bridges":
            covariance_differential_bridges,
        "literal_canonical_spencer_face": literal_lifts,
        "literal_canonical_spencer_quotient_rank": literal_quotient_rank,
        "comparisons": comparisons,
        "conclusion": (
            "no common multiplier or role-preserving one-edge promotion exists; "
            "the unique normalized bridge type is the mixed primitive degree to "
            "the faces-3/5 repeated component by the formal shift "
            "q13:00*q45:00*partial_(07:11), followed by local 0<->1 colour "
            "transport at sites 0,2,6,7"
        ),
        "scope": (
            "fine-degree equality, complete normalized bridge census, and the "
            "literal derivative/multiplier/colour-transport membership test in "
            "the old linear full-row component.  The audit does not construct "
            "the higher bar/Tate boundary required by the two independent "
            "quotient classes, or check the augmented "
            "W/target/anchor/eta/sigma rows"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("order-six/repeated bridge ledger changed", digest))
    print("h3 order-six to repeated-grade bridge audit")
    print("primitive fine degrees:", len(ledger["primitive_fine_degrees"]))
    print("repeated degrees:", len(ledger["repeated_degrees"]))
    print("fixed-label one-edge bridges:",
          len(ledger["fixed_label_one_edge_bridges"]))
    print("transported bridge pairs:",
          len(ledger["role_and_colour_transport_one_edge_bridges"]))
    print("endpoint-arm contraction bridge pairs:",
          len(ledger["endpoint_arm_contraction_two_edge_bridges"]))
    print("covariance arm-contraction bridge pairs:",
          len(ledger["covariance_endpoint_arm_contraction_bridges"]))
    print("canonical bridge: q13:00*q45:00*partial_(07:11), colour transport "
          "0<->1 at sites 0,2,6,7, into repeated component faces 3/5")
    print("literal transformed face membership:", [
        record["complete_component_membership"]["in_span"]
        for record in ledger["literal_canonical_spencer_face"]
    ])
    print("literal transformed quotient rank:",
          ledger["literal_canonical_spencer_quotient_rank"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
