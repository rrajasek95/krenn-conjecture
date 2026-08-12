#!/usr/bin/env python3
"""Test the repeated-grade bridge on the exact first-Spencer-flat lift.

The sparse endpoint-recoloured representative has literal 07:11 faces, but
their normalized bridge orbit is not contained in the old repeated
component.  The proof-relevant representative is instead the exact 343-term
affine solution with source=0, singleton Spencer face=0, and D2=-delta.

This checker reconstructs that solution from the complete 8,580-column
operator block, forms its endpoint-antisymmetric operator, evaluates the
primitive 07:11 wedge 24:11 face on all three source products, and tests all
normalized covariance/Spencer bridge presentations against every repeated
P3+K2 component.  It then solves the simultaneous source/first-face/bridge
system with the physical pure-row aggregate retained.  The zero-normalized
system is feasible, but an exact rational elimination proves that no kernel
direction changes the pure aggregate.  Thus the old repeated source module
cannot supply the primitive anchor; the missing object is genuinely
relative rather than another polynomial full-nine correction.
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
PINS = {
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_order6_to_repeated_grade_bridge.py":
        "30c5df97584a01dfcf121cd48affa8525c058e00a69f8806b6ae81492fff9cda",
    "computations/verify_h3_endpoint_recoloured_primitive_face_grade.py":
        "1c5ed6f5488fb1c4ec8c26d618f312dc1dfeeb5215f2fa24271154d0bcdea0c0",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
}
EXPECTED_LEDGER_SHA256 = "de8151738fe609f857e4e5917c3555067b2a9681018567fd11236c706316d997"
PRIMITIVE_PAIR = ((0, 7, 1, 1), (2, 4, 1, 1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add_scaled(target, source, scalar=Q(1)) -> None:
    for key, value in source.items():
        updated = target.get(key, Q(0)) + scalar * value
        if updated:
            target[key] = updated
        else:
            target.pop(key, None)


def sparse_rank(vectors) -> int:
    basis = {}
    for source in vectors:
        vector = {key: Q(value) for key, value in source.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {key: inverse * value
                                for key, value in vector.items()}
                break
            coefficient = vector[pivot]
            add_scaled(vector, basis[pivot], -coefficient)
    return len(basis)


def reconstruct_first_flat_operator(affine, order6, repair, commutator, base,
                                    system):
    sixth = order6.build_exact_sixth_derivatives(system)
    fifth = affine.exact_derivatives_of_order(system, 5)
    seventh = affine.exact_derivatives_of_order(system, 7)
    missing = frozenset(PRIMITIVE_PAIR)
    metadata = set()
    for _product_index, directions in sixth:
        if not missing.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns_by_shift = defaultdict(list)
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for product_index in range(3):
            for remainder, value in sixth.get(
                    (product_index, directions), {}).items():
                column[(0, product_index,
                        tuple(sorted(remainder + coefficient)))] += value
        for (composed_coefficient, composed_directions), composed_weight in (
                affine.endpoint_composition_antisymmetric(
                    (coefficient, directions)).items()):
            for selected, multiplicity in Counter(
                    composed_directions).items():
                remaining = list(composed_directions)
                remaining.remove(selected)
                remaining = tuple(remaining)
                derivative_table = {5: fifth, 6: sixth, 7: seventh}.get(
                    len(remaining))
                require(derivative_table is not None,
                        "endpoint singleton left orders five--seven")
                for product_index in range(3):
                    for remainder, value in derivative_table.get(
                            (product_index, remaining), {}).items():
                        column[(1, product_index, selected, tuple(sorted(
                            remainder + composed_coefficient)))] += (
                                composed_weight * multiplicity * value
                            )
        for left, right in combinations(range(6), 2):
            pair = tuple(sorted((directions[left], directions[right])))
            column[(2, pair)] += 1
        shift = repair.degree_subtract(
            repair.colour_degree(coefficient),
            repair.colour_degree(directions),
        )
        columns_by_shift[shift].append(((coefficient, directions), {
            row: value for row, value in column.items() if value
        }))

    indexed = [(_shift, entry) for _shift, block in sorted(
        columns_by_shift.items(), key=repr) for entry in block]
    columns = [entry for _shift, entry in indexed]
    target = {(2, pair): int(value) for pair, value in
              commutator.expected_second_shadow().items()}
    solution, exact_rank = affine.exact_row_solution(columns, target)
    require(len(columns) == 8_580 and exact_rank == 1_328
            and len(solution) == 343,
            "first-flat affine solution changed")

    endpoint_operator = Counter()
    for index, value in solution.items():
        for term, term_value in affine.endpoint_composition_antisymmetric(
                columns[index][0]).items():
            endpoint_operator[term] += value * term_value / 2
    endpoint_operator = +endpoint_operator
    return (endpoint_operator, solution, exact_rank, indexed, columns,
            {5: fifth, 6: sixth, 7: seventh})


def primitive_outputs(operator, system, repair, endpoint):
    outputs = []
    derivative_cache = {}
    for product_index, source_product in enumerate(system["products"]):
        polynomial = Counter()
        for (coefficient, directions), weight in operator.items():
            remaining = list(directions)
            if not all(cell in remaining for cell in PRIMITIVE_PAIR):
                continue
            for cell in PRIMITIVE_PAIR:
                remaining.remove(cell)
            remaining = tuple(remaining)
            cache_key = product_index, remaining
            if cache_key not in derivative_cache:
                derivative_cache[cache_key] = repair.derivatives(
                    source_product, remaining
                )
            for tail, value in derivative_cache[cache_key].items():
                polynomial[tuple(sorted(coefficient + tail))] += weight * value
        polynomial = +polynomial
        degrees = sorted({endpoint.degree(monomial) for monomial in polynomial})
        outputs.append({
            "product": product_index,
            "support": len(polynomial),
            "l1": str(sum(abs(value) for value in polynomial.values())),
            "fine_degree_count": len(degrees),
            "site_profiles": [list(endpoint.site_profile(value))
                              for value in degrees],
            "pieces": [Counter({
                monomial: value for monomial, value in polynomial.items()
                if endpoint.degree(monomial) == degree
            }) for degree in degrees],
            "degrees": degrees,
        })
    return outputs


def exact_base_and_pure_aggregate(augmented_columns, operator_column_count,
                                  base_target):
    """Solve q=0 and test q=1 in one exact row elimination."""
    selected_columns = []
    for metadata, column in augmented_columns:
        selected_columns.append((metadata, {
            row: value for row, value in column.items()
            if row[0] != 4 or row[1] == "pure_aggregate"
        }))
    targets = [dict(base_target), dict(base_target)]
    targets[1][(4, "pure_aggregate")] = 1
    equations = defaultdict(dict)
    for column_index, (_metadata, column) in enumerate(selected_columns):
        for row, value in column.items():
            if value:
                equations[row][column_index] = Q(value)
    for target in targets:
        for row in target:
            equations.setdefault(row, {})
    occurrence = Counter(column for vector in equations.values()
                         for column in vector)
    ordered_rows = sorted(equations, key=lambda row: len(equations[row]))
    basis = {}
    basis_parents = {}
    insertion_order = []
    inconsistent_rows = [None, None]
    aggregate_eliminations = None
    for row_number, row in enumerate(ordered_rows, start=1):
        vector = dict(equations[row])
        rhs = [Q(target.get(row, 0)) for target in targets]
        eliminations = []
        while True:
            old_pivots = set(vector) & set(basis)
            if not old_pivots:
                break
            pivot = min(old_pivots, key=lambda column:
                        (occurrence[column], column))
            coefficient = vector[pivot]
            eliminations.append((pivot, coefficient))
            basis_vector, basis_rhs = basis[pivot]
            for column, value in basis_vector.items():
                result = vector.get(column, Q(0)) - coefficient * value
                if result:
                    vector[column] = result
                else:
                    vector.pop(column, None)
            for target_index in range(2):
                rhs[target_index] -= coefficient * basis_rhs[target_index]
        if not vector:
            if row == (4, "pure_aggregate"):
                aggregate_eliminations = tuple(eliminations)
            for target_index, value in enumerate(rhs):
                if value and inconsistent_rows[target_index] is None:
                    inconsistent_rows[target_index] = row
            continue
        pivot = min(vector, key=lambda column: (occurrence[column], column))
        inverse = Q(1) / vector[pivot]
        vector = {column: inverse * value for column, value in vector.items()}
        rhs = [inverse * value for value in rhs]
        basis[pivot] = (vector, rhs)
        basis_parents[pivot] = (
            row,
            inverse,
            tuple((old_pivot, -inverse * coefficient)
                  for old_pivot, coefficient in eliminations),
        )
        insertion_order.append(pivot)
        if row_number % 2000 == 0:
            print("exact simultaneous bridge elimination", row_number,
                  len(basis), flush=True)

    require(inconsistent_rows[0] is None,
            ("zero-normalized exact bridge became inconsistent",
             inconsistent_rows[0]))
    require(inconsistent_rows[1] == (4, "pure_aggregate"),
            ("pure aggregate exact separator changed", inconsistent_rows[1]))
    require(aggregate_eliminations,
            "pure aggregate row lost its exact dependency")

    expanded_cache = {}

    def expand(pivot):
        if pivot in expanded_cache:
            return expanded_cache[pivot]
        row, row_coefficient, ancestors = basis_parents[pivot]
        result = Counter({row: row_coefficient})
        for ancestor, coefficient in ancestors:
            add_scaled(result, expand(ancestor), coefficient)
        expanded_cache[pivot] = result
        return result

    aggregate_dependency = Counter()
    for pivot, coefficient in aggregate_eliminations:
        add_scaled(aggregate_dependency, expand(pivot), coefficient)
    reconstructed_aggregate_row = defaultdict(Q)
    for row, coefficient in aggregate_dependency.items():
        for column, value in equations[row].items():
            reconstructed_aggregate_row[column] += coefficient * value
    require({column: value for column, value in
             reconstructed_aggregate_row.items() if value}
            == equations[(4, "pure_aggregate")],
            "exact pure aggregate dependency failed reconstruction")
    require(sum(coefficient * Q(base_target.get(row, 0))
                for row, coefficient in aggregate_dependency.items()) == 0,
            "aggregate dependency stopped killing the normalized target")

    dependency_monomials = tuple(
        row[1] for row in aggregate_dependency if row[0] == 3
    )

    def local_count(monomial, site, colour):
        return sum((left == site and a == colour)
                   + (right == site and b == colour)
                   for left, right, a, b in monomial)

    dependency_degrees = {
        tuple(local_count(monomial, site, colour)
              for site in range(8) for colour in range(3))
        for monomial in dependency_monomials
    }
    require(len(dependency_degrees) == 1,
            "aggregate dependency left one physical fine degree")

    stabilizer_fields = {
        **{f"eta_p0_minus_{site}0": ((6, 0, 1), (site, 0, -1))
           for site in range(1, 6)},
        **{f"left_x0_minus_{site}0": ((0, 0, 1), (site, 0, -1))
           for site in range(1, 6)},
        "external_p2_minus_x2": ((6, 2, 1), (0, 2, -1)),
        "external_x0_minus_p0": ((0, 0, 1), (6, 0, -1)),
    }
    stabilizer_weights = {}
    for label, field in stabilizer_fields.items():
        weights = tuple(
            sum(weight * local_count(monomial, site, colour)
                for site, colour, weight in field)
            for monomial in dependency_monomials
        )
        require(set(weights) == {0},
                ("aggregate dual sees a known physical stabilizer", label,
                 weights))
        stabilizer_weights[label] = list(weights)
    solution = {}
    for pivot in reversed(insertion_order):
        vector, rhs = basis[pivot]
        value = rhs[0] - sum(
            coefficient * solution.get(column, Q(0))
            for column, coefficient in vector.items() if column != pivot
        )
        if value:
            solution[pivot] = value
    reconstruction = defaultdict(Q)
    for column_index, coefficient in solution.items():
        for row, value in selected_columns[column_index][1].items():
            reconstruction[row] += coefficient * value
    require(all(reconstruction.get(row, Q(0))
                == Q(targets[0].get(row, 0))
                for row in set(reconstruction) | set(targets[0])),
            "zero-normalized exact bridge reconstruction failed")
    repeated_pure_sum = sum(
        value for index, value in solution.items()
        if index >= operator_column_count
        and selected_columns[index][0][2] == (0,) * 8
    )
    return {
        "matrix_rank_over_Q": len(basis),
        "zero_normalized_target_in_image_over_Q": True,
        "zero_normalized_solution_terms": len(solution),
        "zero_normalized_operator_terms": sum(
            index < operator_column_count for index in solution
        ),
        "zero_normalized_repeated_completion_terms": sum(
            index >= operator_column_count for index in solution
        ),
        "zero_normalized_repeated_pure_sum": str(repeated_pure_sum),
        "zero_normalized_solution_denominators": sorted({
            value.denominator for value in solution.values()
        }),
        "zero_normalized_solution_sha256": sha256(json.dumps(sorted(
            (index, str(value)) for index, value in solution.items()
        ), separators=(",", ":")).encode()).hexdigest(),
        "primitive_pure_aggregate_in_image_over_Q": False,
        "primitive_pure_aggregate_inconsistent_row": repr(
            inconsistent_rows[1]
        ),
        "exact_aggregate_dependency_support": len(aggregate_dependency),
        "exact_aggregate_dependency_support_by_row_kind": {
            str(kind): sum(row[0] == kind for row in aggregate_dependency)
            for kind in range(4)
        },
        "exact_aggregate_dependency_denominators": sorted({
            value.denominator for value in aggregate_dependency.values()
        }),
        "exact_aggregate_dependency": [
            [repr(row), str(value)] for row, value in
            sorted(aggregate_dependency.items(), key=lambda item: repr(item[0]))
        ],
        "exact_aggregate_dependency_sha256": sha256(json.dumps(sorted(
            (repr(row), str(value)) for row, value in
            aggregate_dependency.items()
        ), separators=(",", ":")).encode()).hexdigest(),
        "dependency_single_physical_fine_degree": list(
            next(iter(dependency_degrees))
        ),
        "known_physical_stabilizer_weights_on_six_features":
            stabilizer_weights,
        "consequence": (
            "the pure aggregate kills the exact homogeneous kernel of the "
            "source/first-Spencer/bridge matrix and hence factors through "
            "its output; it is not supplied by an old repeated source row"
        ),
    }


def augmented_bridge_feasibility(affine, indexed, columns, derivative_tables,
                                 target_degree, source_degree, presentation,
                                 repeated_component, system, repair, bridge,
                                 endpoint, base, commutator, complete):
    derivative_cache = {}
    augmented_columns = []
    bridge_nonzero_columns = 0
    bridge_feature_count = set()
    for (_shift, (metadata, old_column)) in indexed:
        coefficient, directions = metadata
        bridge_polynomial = Counter()
        for (composed_coefficient, composed_directions), weight in (
                affine.endpoint_composition_antisymmetric(metadata).items()):
            remaining = list(composed_directions)
            if not all(cell in remaining for cell in PRIMITIVE_PAIR):
                continue
            for cell in PRIMITIVE_PAIR:
                remaining.remove(cell)
            remaining = tuple(remaining)
            cache_key = remaining
            if cache_key not in derivative_cache:
                table = derivative_tables.get(len(remaining))
                if table is None:
                    derivative_cache[cache_key] = {}
                else:
                    derivative_cache[cache_key] = table.get((1, remaining), {})
            for tail, value in derivative_cache[cache_key].items():
                monomial = tuple(sorted(composed_coefficient + tail))
                if endpoint.degree(monomial) == source_degree:
                    bridge_polynomial[monomial] += weight * value / 2
        bridge_polynomial = +bridge_polynomial
        transformed, _hits = bridge.transform_primitive_face(
            bridge_polynomial, presentation, base
        )
        column = dict(old_column)
        if transformed:
            bridge_nonzero_columns += 1
            for monomial, value in transformed.items():
                column[(3, monomial)] = column.get((3, monomial), Q(0)) + value
                bridge_feature_count.add(monomial)
        augmented_columns.append((metadata, column))

    cycle_cells = frozenset(tuple(cell) for cell in complete.CYCLE_CELLS)
    cycle_pure_indices = []
    for column_index, (word, multiplier, boundary) in enumerate(
            repeated_component["columns"]):
        column = {(3, monomial): Q(-1) for monomial in boundary}
        bridge_feature_count.update(boundary)
        if word == (0,) * 8:
            column[(4, "pure_aggregate")] = Q(1)
            if set(multiplier).issubset(cycle_cells):
                cycle_pure_indices.append(column_index)
                column[(4, "cycle_pure_vertex")] = Q(1)
        augmented_columns.append((("repeated", column_index, word, multiplier),
                                  column))
    require(len(cycle_pure_indices) == 1,
            ("canonical cycle-supported pure column changed",
             cycle_pure_indices))
    modulus = affine.MODULUS
    base_target = {(2, pair): int(value) for pair, value in
                   commutator.expected_second_shadow().items()}

    def solve(label, markers=()):
        selected_columns = []
        for metadata, column in augmented_columns:
            selected_columns.append((metadata, {
                row: value for row, value in column.items()
                if row[0] != 4 or row[1] in markers
            }))
        modular_columns = []
        for metadata, column in selected_columns:
            modular = {}
            for row, value in column.items():
                value = Q(value)
                residue = (value.numerator
                           * pow(value.denominator, modulus - 2,
                                 modulus)) % modulus
                if residue:
                    modular[row] = residue
            modular_columns.append((metadata, modular))
        target = dict(base_target)
        for marker in markers:
            target[(4, marker)] = 1
        plain_rank, augmented_rank, inconsistent, equations = (
            affine.row_rank_mod_p(modular_columns, target, modulus)
        )
        return {
            "label": label,
            "normalization_markers": list(markers),
            "equations": equations,
            "row_rank_mod_p": plain_rank,
            "augmented_row_rank_mod_p": augmented_rank,
            "target_in_image_mod_p": not inconsistent,
        }

    tests = [
        solve("unnormalized"),
        solve("primitive pure aggregate", ("pure_aggregate",)),
        solve("cycle vertex with zero pure aggregate", ("cycle_pure_vertex",)),
        solve("canonical primitive pure vertex",
              ("pure_aggregate", "cycle_pure_vertex")),
    ]
    exact_certificate = exact_base_and_pure_aggregate(
        augmented_columns, len(columns), base_target
    )
    return {
        "operator_columns": len(columns),
        "operator_columns_with_nonzero_bridge_face": bridge_nonzero_columns,
        "repeated_completion_columns": len(repeated_component["columns"]),
        "bridge_features": len(bridge_feature_count),
        "modulus": modulus,
        "canonical_cycle_pure_repeated_column": cycle_pure_indices[0],
        "normalization_tests": tests,
        "exact_pure_aggregate_certificate": exact_certificate,
        "readout_scope": (
            "a repeated pure-row coefficient contributes physical target +1 "
            "and anchor incidence -1.  These tests construct a source-typed "
            "nonzero repeated boundary, not yet a target-zero relative anchor"
        ),
    }


def audit() -> dict[str, object]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    affine = load(
        "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py",
        "first_flat_affine",
    )
    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "first_flat_order6",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "first_flat_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "first_flat_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "first_flat_base",
    )
    endpoint = load(
        "computations/verify_h3_endpoint_recoloured_primitive_face_grade.py",
        "first_flat_endpoint",
    )
    bridge = load(
        "computations/verify_h3_order6_to_repeated_grade_bridge.py",
        "first_flat_bridge",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "first_flat_complete",
    )
    system = repair.build_system(base, commutator)
    (operator, solution, exact_rank, indexed, columns,
     derivative_tables) = reconstruct_first_flat_operator(
        affine, order6, repair, commutator, base, system
    )
    outputs = primitive_outputs(operator, system, repair, endpoint)

    repeated = []
    for component, (left, right, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        target_degree = complete.degree_add(
            base.lambda_degree(left),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        repeated.append((component, left, right, target_degree,
                         complete.component(base, target_degree)))

    bridge_records = []
    all_remainders = []
    for output in outputs:
        for fine_index, (degree, polynomial) in enumerate(zip(
                output["degrees"], output["pieces"], strict=True)):
            for component, left, right, target_degree, target_component in repeated:
                presentations = bridge.covariance_arm_contraction_bridges(
                    degree, target_degree, complete, base
                )
                if not presentations:
                    continue
                tests = []
                for presentation in presentations:
                    transformed, hit_terms = bridge.transform_primitive_face(
                        polynomial, presentation, base
                    )
                    membership, remainder = bridge.full_component_membership(
                        target_component, transformed
                    )
                    if transformed:
                        all_remainders.append(Counter(remainder))
                    tests.append((presentation, transformed, hit_terms,
                                  membership, remainder))
                nonzero = [test for test in tests if test[1]]
                bridge_records.append({
                    "primitive": [output["product"], fine_index],
                    "component": component,
                    "faces": [left, right],
                    "presentations": len(presentations),
                    "literal_nonzero_presentations": len(nonzero),
                    "literal_in_old_component": sum(
                        test[3]["in_span"] for test in nonzero
                    ),
                    "minimum_remainder_support": min(
                        (len(test[4]) for test in nonzero), default=0
                    ),
                    "first_nonzero": ({
                        "contracted_arm": nonzero[0][0]["contracted_arm"],
                        "inserted_tail": nonzero[0][0][
                            "inserted_two_edge_tail"
                        ],
                        "hit_terms": nonzero[0][2],
                        "transformed_support": len(nonzero[0][1]),
                        "remainder_support": len(nonzero[0][4]),
                        "first_remainder": nonzero[0][3]["first_remainder"],
                    } if nonzero else None),
                })

    serial_outputs = [{key: value for key, value in output.items()
                       if key not in ("pieces", "degrees")}
                      for output in outputs]

    source_degree = outputs[1]["degrees"][0]
    target_degree = repeated[1][3]
    repeated_component = repeated[1][4]
    presentation_key = {
        "contracted_arm": [0, 7, 1, 1],
        "inserted_two_edge_tail": [[1, 3, 0, 0], [4, 5, 0, 0]],
        "colour_permutations_source_to_target": [
            [0, 1, 2], [0, 1, 2], [1, 0, 2], [0, 1, 2],
            [0, 1, 2], [0, 1, 2], [1, 2, 0], [1, 2, 0],
        ],
    }
    presentation = next((record for record in
                         bridge.covariance_arm_contraction_bridges(
                             source_degree, target_degree, complete, base)
                         if all(record[key] == value for key, value in
                                presentation_key.items())), None)
    require(presentation is not None,
            "physical canonical bridge presentation changed")
    feasibility = augmented_bridge_feasibility(
        affine, indexed, columns, derivative_tables, target_degree,
        source_degree, presentation, repeated_component, system, repair,
        bridge, endpoint, base, commutator,
        complete,
    )
    normalization = {
        record["label"]: record for record in
        feasibility["normalization_tests"]
    }
    require(normalization["unnormalized"]["target_in_image_mod_p"],
            "zero-normalized simultaneous bridge lost feasibility")
    require(not normalization["primitive pure aggregate"][
                "target_in_image_mod_p"]
            and feasibility["exact_pure_aggregate_certificate"][
                "primitive_pure_aggregate_inconsistent_row"]
            == repr((4, "pure_aggregate")),
            "primitive pure aggregate entered the flat bridge image")
    require(not normalization["cycle vertex with zero pure aggregate"][
                "target_in_image_mod_p"]
            and not normalization["canonical primitive pure vertex"][
                "target_in_image_mod_p"],
            "canonical pure vertex normalization changed")
    return {
        "theorem": "first-Spencer-flat endpoint bridge classification",
        "eligible_columns": 8_580,
        "exact_rank": exact_rank,
        "solution_terms": len(solution),
        "endpoint_operator_terms": len(operator),
        "primitive_outputs": serial_outputs,
        "bridge_records": bridge_records,
        "nonzero_bridge_quotient_rank": sparse_rank(all_remainders),
        "simultaneous_bridge_feasibility": feasibility,
        "scope": (
            "the exact first-Spencer-flat order-six representative and all "
            "normalized covariance/arm-contraction presentations, followed "
            "by the complete old repeated full-nine component and its pure "
            "row aggregate.  No new relative comparison cell, physical "
            "terminal, or transverse-rank conclusion is asserted"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("first-flat bridge ledger changed", digest))
    print("h3 first-Spencer-flat endpoint bridge")
    print("primitive outputs:", ledger["primitive_outputs"])
    print("bridge records:", ledger["bridge_records"])
    print("quotient rank:", ledger["nonzero_bridge_quotient_rank"])
    print("simultaneous feasibility:",
          ledger["simultaneous_bridge_feasibility"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
