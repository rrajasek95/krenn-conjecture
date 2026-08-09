#!/usr/bin/env python3
"""Exact tangent space of the anchored N=8 three-cut cylinder locus."""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_boundary_shear():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_old_source_two_cell_shear.py"
    )
    spec = importlib.util.spec_from_file_location("boundary_shear", path)
    require(spec is not None and spec.loader is not None, "cannot load shear")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sparse_add(*terms):
    answer = {}
    for scalar, vector in terms:
        for key, value in vector.items():
            total = answer.get(key, Q(0)) + Q(scalar) * value
            if total:
                answer[key] = total
            else:
                answer.pop(key, None)
    return answer


def independent_indices(module, columns):
    selected = []
    basis = {}
    for index, column in enumerate(columns):
        candidate = module.rational_basis(list(basis.values()) + [column])
        if len(candidate) > len(basis):
            selected.append(index)
            basis = candidate
    return tuple(selected)


def column_coordinate_solver(columns):
    """Return a pivot basis carrying expressions in the original columns."""
    basis = {}
    expressions = {}
    for index, source in enumerate(columns):
        vector = dict(source)
        expression = {index: Q(1)}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = vector[pivot]
                vector = {key: value / scale for key, value in vector.items()}
                expression = {
                    key: value / scale for key, value in expression.items()
                }
                basis[pivot] = vector
                expressions[pivot] = expression
                break
            coefficient = vector[pivot]
            vector = sparse_add((Q(1), vector), (-coefficient, basis[pivot]))
            expression = sparse_add(
                (Q(1), expression), (-coefficient, expressions[pivot])
            )
        else:
            raise RuntimeError("selected columns became dependent")
    return basis, expressions


def solve_coordinates(source, basis, expressions):
    vector = dict(source)
    coefficients = {}
    while vector:
        pivot = min(vector)
        require(pivot in basis, "base residual left its cylinder")
        coefficient = vector[pivot]
        vector = sparse_add((Q(1), vector), (-coefficient, basis[pivot]))
        coefficients = sparse_add(
            (Q(1), coefficients), (coefficient, expressions[pivot])
        )
    return coefficients


def affine_minor_polynomial(dependence, columns, derivatives, rows):
    require(len(columns) == len(rows), "affine minor is not square")
    values = []
    for parameter in range(len(rows) + 1):
        matrix = tuple(
            tuple(
                columns[column].get(row, Q(0))
                + Q(parameter) * derivatives[column].get(row, Q(0))
                for column in range(len(columns))
            )
            for row in rows
        )
        values.append(dependence.determinant(matrix))
    return dependence.interpolate_at_integers(values)


def kernel_relations(columns):
    """Exact nullspace basis for a sparse column map with hashable row keys."""
    basis = {}
    expressions = {}
    kernel = []
    for index, source in enumerate(columns):
        vector = dict(source)
        expression = {index: Q(1)}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in basis:
                scale = vector[pivot]
                basis[pivot] = {
                    key: value / scale for key, value in vector.items()
                }
                expressions[pivot] = {
                    key: value / scale for key, value in expression.items()
                }
                break
            coefficient = vector[pivot]
            vector = sparse_add((Q(1), vector), (-coefficient, basis[pivot]))
            expression = sparse_add(
                (Q(1), expression), (-coefficient, expressions[pivot])
            )
        if not vector:
            kernel.append(expression)
    return tuple(kernel), len(basis)


def all_old_coordinates():
    return tuple(
        (left, right, left_colour, right_colour)
        for left in range(8)
        for right in range(left + 1, 8)
        for left_colour in range(3)
        for right_colour in range(3)
    )


def occupied_weights(base):
    return {
        (left, right, left_colour, right_colour): weight
        for (left, right), entries in base.items()
        for left_colour, right_colour, weight in entries
        if weight
    }


def gauge_directions(coordinates, occupied):
    coordinate_index = {coordinate: index for index, coordinate in enumerate(coordinates)}
    directions = []
    for colour in range(3):
        for vertex in range(7):
            direction = {}
            for coordinate, weight in occupied.items():
                left, right, left_colour, right_colour = coordinate
                exponent = Q(
                    (left == vertex and left_colour == colour)
                    + (right == vertex and right_colour == colour)
                    - (left == 7 and left_colour == colour)
                    - (right == 7 and right_colour == colour)
                )
                if exponent:
                    direction[coordinate_index[coordinate]] = weight * exponent
            directions.append(direction)
    return tuple(directions)


def main() -> None:
    boundary_shear = load_boundary_shear()
    dependence = boundary_shear.load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    module = data["module"]
    one_cell = data["one_cell"]
    unit_gate = one_cell.load_unit_gate()
    base = data["base"]
    coordinates = all_old_coordinates()
    require(len(coordinates) == 252, "old-coordinate count changed")

    cut_data = {}
    for cut in unit_gate.THREE_CUTS:
        u_set = tuple(vertex for vertex in module.S if vertex != cut)
        c_set = (cut, 6, 7)
        columns = one_cell.insertion_columns(module, u_set, base)
        selected = independent_indices(module, columns)
        require(len(selected) == 14, f"base cut-{cut} rank changed")
        selected_columns = tuple(columns[index] for index in selected)
        basis, expressions = column_coordinate_solver(selected_columns)
        rows = module.flatten_rows(
            one_cell.residual_tensor(module, base), c_set, u_set
        )
        row_coefficients = {
            word: solve_coordinates(rows.get(word, {}), basis, expressions)
            for word in product(range(3), repeat=3)
        }
        one_rows = module.flatten_rows(
            module.sector(c_set, 1, base), c_set, u_set
        )
        one_row_coefficients = {
            word: solve_coordinates(one_rows.get(word, {}), basis, expressions)
            for word in product(range(3), repeat=3)
        }
        cut_data[cut] = (
            u_set,
            c_set,
            columns,
            selected,
            selected_columns,
            module.rational_basis(list(selected_columns)),
            rows,
            row_coefficients,
            one_rows,
            one_row_coefficients,
        )

    base_tensor = module.matching_tensor(module.B, base)
    tangent_columns = []
    tensor_derivative_columns = []
    for coordinate in coordinates:
        changed = one_cell.add_parameter(module, base, coordinate, Q(1))
        changed_tensor = module.matching_tensor(module.B, changed)
        signature = {}
        for colour in range(3):
            word = (colour,) * 8
            derivative = changed_tensor.get(word, Q(0)) - base_tensor.get(word, Q(0))
            if derivative:
                signature[("pure", colour)] = derivative
        tensor_derivative_columns.append(
            {
                word: changed_tensor.get(word, Q(0)) - base_tensor.get(word, Q(0))
                for word in set(base_tensor) | set(changed_tensor)
                if changed_tensor.get(word, Q(0)) != base_tensor.get(word, Q(0))
            }
        )

        for cut, record in cut_data.items():
            (
                u_set,
                c_set,
                columns0,
                selected,
                _selected_columns,
                quotient_basis,
                rows0,
                row_coefficients,
                one_rows0,
                one_row_coefficients,
            ) = record
            columns1 = one_cell.insertion_columns(module, u_set, changed)
            derivatives = tuple(
                sparse_add((Q(1), columns1[index]), (-Q(1), columns0[index]))
                for index in selected
            )
            rows1 = module.flatten_rows(
                one_cell.residual_tensor(module, changed), c_set, u_set
            )
            one_rows1 = module.flatten_rows(
                module.sector(c_set, 1, changed), c_set, u_set
            )
            for family, family_rows0, family_rows1, family_coefficients in (
                ("combined", rows0, rows1, row_coefficients),
                ("one-cross", one_rows0, one_rows1, one_row_coefficients),
            ):
                for word in product(range(3), repeat=3):
                    row_derivative = sparse_add(
                        (Q(1), family_rows1.get(word, {})),
                        (-Q(1), family_rows0.get(word, {})),
                    )
                    adjusted = dict(row_derivative)
                    for index, coefficient in family_coefficients[word].items():
                        adjusted = sparse_add(
                            (Q(1), adjusted), (-coefficient, derivatives[index])
                        )
                    remainder = data["two_cell"].quotient_remainder(
                        adjusted, quotient_basis
                    )
                    for row, value in remainder.items():
                        signature[("cut", family, cut, word, row)] = value
        tangent_columns.append(signature)

    kernel, constraint_rank = kernel_relations(tangent_columns)
    require(
        len(kernel) + constraint_rank == len(coordinates),
        "tangent rank-nullity changed",
    )
    occupied = occupied_weights(base)
    gauges = gauge_directions(coordinates, occupied)
    coordinate_index = {coordinate: index for index, coordinate in enumerate(coordinates)}
    boundary = tuple(
        {coordinate_index[coordinate]: Q(1)}
        for coordinate in dependence.ADMISSIBLE_DIRECTIONS
    )
    expected_basis = module.rational_basis(list(gauges) + list(boundary))
    kernel_basis = module.rational_basis(list(kernel))
    expected_inside = sum(
        module.rational_member(vector, kernel_basis)
        for vector in expected_basis.values()
    )
    tangent_inside_expected = sum(
        module.rational_member(vector, expected_basis)
        for vector in kernel_basis.values()
    )
    complement = []
    enlarged_basis = dict(expected_basis)
    for vector in kernel_basis.values():
        if module.rational_member(vector, enlarged_basis):
            continue
        complement.append(vector)
        enlarged_basis = module.rational_basis(
            list(enlarged_basis.values()) + [vector]
        )
    require(
        len(enlarged_basis) == len(expected_basis) + len(complement),
        "tangent complement bookkeeping changed",
    )
    named_complement = tuple(
        tuple(
            (coordinates[index], coefficient)
            for index, coefficient in sorted(vector.items())
        )
        for vector in complement
    )

    full_fibre_columns = tuple(
        sparse_add(
            (Q(1), tangent_columns[index]),
            (
                Q(1),
                {
                    ("full-tensor", word): coefficient
                    for word, coefficient in tensor_derivative_columns[index].items()
                },
            ),
        )
        for index in range(len(coordinates))
    )
    full_fibre_kernel, full_fibre_rank = kernel_relations(full_fibre_columns)
    expected_vectors = tuple(expected_basis.values())
    expected_tensor_images = tuple(
        sparse_add(
            *tuple(
                (coefficient, tensor_derivative_columns[index])
                for index, coefficient in vector.items()
            )
        )
        if vector
        else {}
        for vector in expected_vectors
    )
    expected_fibre_relations, _expected_tensor_rank = kernel_relations(
        expected_tensor_images
    )
    expected_fibre_vectors = tuple(
        sparse_add(
            *tuple(
                (coefficient, expected_vectors[index])
                for index, coefficient in relation.items()
            )
        )
        for relation in expected_fibre_relations
    )
    full_fibre_basis = module.rational_basis(list(full_fibre_kernel))
    expected_fibre_basis = module.rational_basis(list(expected_fibre_vectors))
    expected_fibre_inside = sum(
        module.rational_member(vector, full_fibre_basis)
        for vector in expected_fibre_basis.values()
    )
    full_fibre_inside_expected = sum(
        module.rational_member(vector, expected_fibre_basis)
        for vector in full_fibre_basis.values()
    )
    require(constraint_rank == 225 and len(kernel) == 27, "tangent dimensions changed")
    require(len(module.rational_basis(list(gauges))) == 12, "gauge rank changed")
    require(
        len(expected_basis) == 26 and expected_inside == 26,
        "gauge-boundary tangent inclusion changed",
    )
    require(
        named_complement == ((((2, 3, 2, 1), Q(1)),),),
        "tangent quotient representative changed",
    )
    require(
        full_fibre_rank == 245
        and len(full_fibre_kernel) == 7
        and len(expected_fibre_basis) == 7
        and expected_fibre_inside == 7
        and full_fibre_inside_expected == 7,
        "fixed-full-tensor tangent intersection changed",
    )

    quotient_jet_records = []
    jet_length_census = Counter()
    frame_polynomials = []
    target_polynomials = []
    full_tensor_derivative = None
    parameter_cut_status = None
    if complement:
        representative = complement[0]
        require(len(representative) == 1, "quotient representative support changed")
        representative_changed = one_cell.add_parameter(
            module,
            base,
            coordinates[next(iter(representative))],
            next(iter(representative.values())),
        )
        representative_tensor = module.matching_tensor(
            module.B, representative_changed
        )
        full_tensor_derivative = tuple(
            sorted(
                (word, representative_tensor.get(word, Q(0)) - base_tensor.get(word, Q(0)))
                for word in set(base_tensor) | set(representative_tensor)
                if representative_tensor.get(word, Q(0)) != base_tensor.get(word, Q(0))
            )
        )
        parameter_cut_status = tuple(
            (
                parameter,
                tuple(
                    unit_gate.active_complete(
                        module.cut_record(
                            cut,
                            one_cell.add_parameter(
                                module,
                                base,
                                coordinates[next(iter(representative))],
                                parameter * next(iter(representative.values())),
                            ),
                        )
                    )
                    for cut in unit_gate.THREE_CUTS
                ),
            )
            for parameter in (-2, -1, 1, 2)
        )
        for cut, record in cut_data.items():
            (
                u_set,
                c_set,
                columns0,
                selected,
                _selected_columns,
                quotient_basis,
                rows0,
                row_coefficients,
                one_rows0,
                one_row_coefficients,
            ) = record
            column_derivatives = [dict() for _index in selected]
            row_derivatives = {"combined": {}, "one-cross": {}}
            for coordinate_index_value, coefficient in representative.items():
                changed = one_cell.add_parameter(
                    module, base, coordinates[coordinate_index_value], Q(1)
                )
                columns1 = one_cell.insertion_columns(module, u_set, changed)
                for local_index, full_index in enumerate(selected):
                    column_derivatives[local_index] = sparse_add(
                        (Q(1), column_derivatives[local_index]),
                        (
                            coefficient,
                            sparse_add(
                                (Q(1), columns1[full_index]),
                                (-Q(1), columns0[full_index]),
                            ),
                        ),
                    )
                rows1 = module.flatten_rows(
                    one_cell.residual_tensor(module, changed), c_set, u_set
                )
                one_rows1 = module.flatten_rows(
                    module.sector(c_set, 1, changed), c_set, u_set
                )
                for family, family_rows0, family_rows1 in (
                    ("combined", rows0, rows1),
                    ("one-cross", one_rows0, one_rows1),
                ):
                    for word in product(range(3), repeat=3):
                        row_derivatives[family][word] = sparse_add(
                            (Q(1), row_derivatives[family].get(word, {})),
                            (
                                coefficient,
                                sparse_add(
                                    (Q(1), family_rows1.get(word, {})),
                                    (-Q(1), family_rows0.get(word, {})),
                                ),
                            ),
                        )
            basis, expressions = column_coordinate_solver(
                tuple(record[4])
            )
            frame_rows = tuple(sorted(quotient_basis))
            frame_polynomial = affine_minor_polynomial(
                dependence,
                tuple(record[4]),
                tuple(column_derivatives),
                frame_rows,
            )
            frame_polynomials.append((cut, frame_polynomial))
            base_cut_record = module.cut_record(cut, base)
            target_colour = next(
                colour
                for colour, member in enumerate(base_cut_record["constant_members"])
                if not member
            )
            target_column = {
                module.WORD5_INDEX[(target_colour,) * 5]: Q(1)
            }
            augmented_columns = tuple(record[4]) + (target_column,)
            augmented_derivatives = tuple(column_derivatives) + ({},)
            augmented_basis = module.rational_basis(list(augmented_columns))
            require(len(augmented_basis) == 15, "target witness rank changed")
            target_polynomial = affine_minor_polynomial(
                dependence,
                augmented_columns,
                augmented_derivatives,
                tuple(sorted(augmented_basis)),
            )
            target_polynomials.append((cut, target_colour, target_polynomial))
            for family, family_coefficients in (
                ("combined", row_coefficients),
                ("one-cross", one_row_coefficients),
            ):
                for word in product(range(3), repeat=3):
                    first_adjusted = dict(row_derivatives[family][word])
                    for index, coefficient in family_coefficients[word].items():
                        first_adjusted = sparse_add(
                            (Q(1), first_adjusted),
                            (-coefficient, column_derivatives[index]),
                        )
                    first_coefficients = solve_coordinates(
                        first_adjusted, basis, expressions
                    )
                    previous = first_coefficients
                    jet_length = 1 if previous else 0
                    for order in range(2, 31):
                        obstruction = {}
                        for index, coefficient in previous.items():
                            obstruction = sparse_add(
                                (Q(1), obstruction),
                                (coefficient, column_derivatives[index]),
                            )
                        remainder = data["two_cell"].quotient_remainder(
                            obstruction, quotient_basis
                        )
                        if remainder:
                            quotient_jet_records.append(
                                (
                                    family,
                                    cut,
                                    word,
                                    order,
                                    tuple(sorted(remainder.items())),
                                )
                            )
                            break
                        following = solve_coordinates(
                            sparse_add((-Q(1), obstruction)), basis, expressions
                        )
                        if not following:
                            jet_length_census[(family, jet_length)] += 1
                            break
                        previous = following
                        jet_length = order
                    else:
                        raise RuntimeError("quotient coefficient jet did not terminate")

    require(not quotient_jet_records, "occupied modulus acquired a higher cylinder obstruction")
    require(
        jet_length_census
        == Counter(
            {
                ("combined", 0): 77,
                ("combined", 1): 4,
                ("one-cross", 0): 77,
                ("one-cross", 1): 4,
            }
        ),
        "occupied-modulus cylinder jets changed",
    )
    require(
        frame_polynomials
        == [(2, (-Q(1),)), (3, (Q(1),)), (4, (-Q(1),))],
        "cofactor-frame minors changed",
    )
    require(
        target_polynomials
        == [
            (2, 1, (Q(1),)),
            (3, 2, (Q(1),)),
            (4, 1, (-Q(1),)),
        ],
        "target-defect minors changed",
    )
    require(
        full_tensor_derivative
        == (
            ((0, 0, 2, 1, 0, 0, 0, 0), Q(1)),
            ((0, 0, 2, 1, 0, 0, 1, 2), -Q(1)),
        ),
        "occupied-modulus full-tensor derivative changed",
    )

    print("N=8 anchored three-cut exactness tangent: exact frontier")
    print(f"old coordinates: {len(coordinates)}")
    print(f"linearized constraint rank: {constraint_rank}")
    print(f"full-cylinder-plus-anchor tangent dimension: {len(kernel)}")
    print(f"gauge directions/rank: {len(gauges)}/{len(module.rational_basis(list(gauges)))}")
    print(f"gauge-plus-boundary expected rank: {len(expected_basis)}")
    print(f"expected directions inside tangent: {expected_inside}/{len(expected_basis)}")
    print(f"tangent basis inside expected span: {tangent_inside_expected}/{len(kernel_basis)}")
    print(f"tangent quotient dimension: {len(complement)}")
    print(f"first quotient representative: {named_complement[0] if named_complement else None}")
    print(f"sample cut status of quotient representative: {parameter_cut_status}")
    print(f"nonzero higher cylinder jets: {len(quotient_jet_records)}")
    print(
        "first quadratic jet: "
        f"{quotient_jet_records[0] if quotient_jet_records else None}"
    )
    print(f"terminating coefficient-jet lengths: {dict(sorted(jet_length_census.items()))}")
    print(f"cofactor-frame minors: {frame_polynomials}")
    print(f"target-defect minors: {target_polynomials}")
    print(f"full-tensor mixed derivative: {full_tensor_derivative}")
    print(
        "fixed-full-tensor tangent rank/dimension: "
        f"{full_fibre_rank}/{len(full_fibre_kernel)}"
    )
    print(
        "expected-span fixed-fibre rank / containments: "
        f"{len(expected_fibre_basis)} / "
        f"{expected_fibre_inside}/{len(expected_fibre_basis)}, "
        f"{full_fibre_inside_expected}/{len(full_fibre_basis)}"
    )
    print("scope: combined residual and one-cross cylinders plus pure anchors")


if __name__ == "__main__":
    main()
