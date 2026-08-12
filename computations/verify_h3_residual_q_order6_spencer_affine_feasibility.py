#!/usr/bin/env python3
"""Test whether the order-six residual affine space has a flat first face.

The pinned order-six missing-face block contains 8,580 quadratic-
coefficient sixth-order operators.  The canonical sparse solution kills the
three quadratic source generators and has the required ``-delta`` pair
shadow, but its first coefficient-prolonging (Spencer) faces are nonzero.

This checker asks the stronger invariant question: is there *any* vector in
the same complete order-six block which simultaneously

  * kills all three quadratic source generators literally;
  * has pair shadow ``-delta``; and
  * has every singleton Spencer face equal to zero literally?

The initial pass is exact over a large prime.  If the augmented rank rises,
the desired flat representative does not exist over Q either.  This is a
bounded operator-space verdict, not a no-go for a relative mapping-cone or
higher Spencer generator.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections import deque
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import factorial
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULUS = 1_000_003
PINS = {
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = (
    "f1c28deafd72892f58f1d7a0f9e8d14c30b16725297f7344e388f65389651985"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot load", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def exact_derivatives_of_order(system, order):
    """Return all derivatives of the requested order on the three products."""
    table = defaultdict(Counter)
    for product_index, polynomial in enumerate(system["products"]):
        for monomial, base_coefficient in polynomial.items():
            available = Counter(monomial)
            seen = set()
            for positions in combinations(range(8), order):
                directions = tuple(sorted(monomial[index]
                                          for index in positions))
                if directions in seen:
                    continue
                seen.add(directions)
                needed = Counter(directions)
                coefficient = base_coefficient
                remainder = list(monomial)
                for cell, count in needed.items():
                    coefficient *= factorial(available[cell]) // factorial(
                        available[cell] - count
                    )
                    for _unused in range(count):
                        remainder.remove(cell)
                table[(product_index, directions)][tuple(sorted(remainder))] += (
                    coefficient
                )
    return table


def tail_colour_swap(cell):
    left, right, left_colour, right_colour = cell
    if left in (2, 5) and left_colour in (1, 2):
        left_colour = 3 - left_colour
    if right in (2, 5) and right_colour in (1, 2):
        right_colour = 3 - right_colour
    return left, right, left_colour, right_colour


def endpoint_composition_antisymmetric(metadata):
    """Return twice E o (theta-tau(theta))/2 for one theta term."""
    coefficient, directions = metadata
    source_xv = (0, 1, 1, 1)
    source_pq = (6, 7, 1, 1)
    target_xv = (0, 1, 0, 1)
    target_pq = (6, 7, 2, 2)
    composition = Counter()

    leading_coefficient = tuple(sorted(coefficient +
                                       (target_xv, target_pq)))
    leading_directions = tuple(sorted(directions +
                                      (source_xv, source_pq)))
    composition[(leading_coefficient, leading_directions)] += 1

    counts = Counter(coefficient)
    for source, other_source in ((source_xv, source_pq),
                                 (source_pq, source_xv)):
        if not counts[source]:
            continue
        remainder = list(coefficient)
        remainder.remove(source)
        new_coefficient = tuple(sorted(remainder + [target_xv, target_pq]))
        new_directions = tuple(sorted(directions + (other_source,)))
        composition[(new_coefficient, new_directions)] += counts[source]
    if counts[source_xv] and counts[source_pq]:
        remainder = list(coefficient)
        remainder.remove(source_xv)
        remainder.remove(source_pq)
        new_coefficient = tuple(sorted(remainder + [target_xv, target_pq]))
        composition[(new_coefficient, directions)] += (
            counts[source_xv] * counts[source_pq]
        )

    antisymmetric = Counter(composition)
    for (term_coefficient, term_directions), value in composition.items():
        swapped = (
            tuple(sorted(tail_colour_swap(cell)
                         for cell in term_coefficient)),
            tuple(sorted(tail_colour_swap(cell)
                         for cell in term_directions)),
        )
        antisymmetric[swapped] -= value
    return Counter({term: value for term, value in antisymmetric.items()
                    if value})


def reduce_mod(vector, basis):
    vector = {row: value % MODULUS for row, value in vector.items()
              if value % MODULUS}
    while vector:
        pivot = min(vector)
        if pivot not in basis:
            return vector
        coefficient = vector[pivot]
        for row, value in basis[pivot].items():
            result = (vector.get(row, 0) - coefficient * value) % MODULUS
            if result:
                vector[row] = result
            else:
                vector.pop(row, None)
    return vector


def rank_mod2_constraints(columns, shadow_kind):
    rows = sorted({row for _metadata, column in columns for row, value in
                   column.items() if row[0] < shadow_kind and value % 2})
    row_index = {row: index for index, row in enumerate(rows)}
    basis = {}
    for _metadata, column in columns:
        vector = 0
        for row, value in column.items():
            if row[0] < shadow_kind and value % 2:
                vector ^= 1 << row_index[row]
        while vector:
            pivot_bit = vector & -vector
            pivot = pivot_bit.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector
                break
            vector ^= basis[pivot]
    return len(basis), len(rows)


def row_rank_mod_p(columns, target, modulus):
    equations = defaultdict(dict)
    for column_index, (_metadata, column) in enumerate(columns):
        for row, value in column.items():
            residue = value % modulus
            if residue:
                equations[row][column_index] = residue
    for row in target:
        equations.setdefault(row, {})
    ordered_rows = sorted(equations, key=lambda row: len(equations[row]))

    def rank(with_target):
        basis = {}
        special = len(columns)
        for row in ordered_rows:
            vector = dict(equations[row])
            if with_target and target.get(row, 0) % modulus:
                vector[special] = target[row] % modulus
            while vector:
                pivot = min(vector)
                if pivot not in basis:
                    inverse = pow(vector[pivot], modulus - 2, modulus)
                    basis[pivot] = {
                        column: value * inverse % modulus
                        for column, value in vector.items()
                    }
                    break
                coefficient = vector[pivot]
                for column, value in basis[pivot].items():
                    result = (vector.get(column, 0)
                              - coefficient * value) % modulus
                    if result:
                        vector[column] = result
                    else:
                        vector.pop(column, None)
        return len(basis), special in basis

    plain_rank, _unused = rank(False)
    augmented_rank, inconsistent_pivot = rank(True)
    return plain_rank, augmented_rank, inconsistent_pivot, len(equations)


def exact_row_solution(columns, target):
    equations = defaultdict(dict)
    for column_index, (_metadata, column) in enumerate(columns):
        for row, value in column.items():
            if value:
                equations[row][column_index] = Q(value)
    for row in target:
        equations.setdefault(row, {})
    occurrence = Counter(column for vector in equations.values()
                         for column in vector)
    ordered_rows = sorted(equations, key=lambda row: len(equations[row]))
    basis = {}
    insertion_order = []
    for row_number, row in enumerate(ordered_rows, start=1):
        vector = dict(equations[row])
        rhs = Q(target.get(row, 0))
        while True:
            old_pivots = set(vector) & set(basis)
            if not old_pivots:
                break
            pivot = min(old_pivots, key=lambda column:
                        (occurrence[column], column))
            coefficient = vector[pivot]
            basis_vector, basis_rhs = basis[pivot]
            for column, value in basis_vector.items():
                result = vector.get(column, Q(0)) - coefficient * value
                if result:
                    vector[column] = result
                else:
                    vector.pop(column, None)
            rhs -= coefficient * basis_rhs
        if not vector:
            require(not rhs, ("inconsistent exact Spencer equation", row))
            continue
        pivot = min(vector, key=lambda column: (occurrence[column], column))
        inverse = Q(1) / vector[pivot]
        vector = {column: inverse * value for column, value in vector.items()}
        rhs *= inverse
        basis[pivot] = (vector, rhs)
        insertion_order.append(pivot)
        if row_number % 100 == 0:
            print("exact row elimination", row_number, len(basis), flush=True)

    solution = {}
    for pivot in reversed(insertion_order):
        vector, rhs = basis[pivot]
        value = rhs - sum(coefficient * solution.get(column, Q(0))
                          for column, coefficient in vector.items()
                          if column != pivot)
        if value:
            solution[pivot] = value

    reconstruction = defaultdict(Q)
    for column_index, coefficient in solution.items():
        for row, value in columns[column_index][1].items():
            reconstruction[row] += coefficient * value
    require(all(reconstruction.get(row, Q(0)) == Q(target.get(row, 0))
                for row in set(reconstruction) | set(target)),
            "exact Spencer affine reconstruction failed")
    return solution, len(basis)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "spencer_affine_order6",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "spencer_affine_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "spencer_affine_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "spencer_affine_base",
    )
    system = repair.build_system(base, commutator)
    sixth = order6.build_exact_sixth_derivatives(system)
    fourth = exact_derivatives_of_order(system, 4)
    fifth = exact_derivatives_of_order(system, 5)
    seventh = exact_derivatives_of_order(system, 7)
    include_second_spencer = any(argument in sys.argv for argument in (
        "--second-row-elim", "--second-block-elim",
    ))
    shadow_kind = 3 if include_second_spencer else 2
    missing = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))
    metadata = set()
    for _product_index, directions in sixth:
        if not missing.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns_by_shift = defaultdict(list)
    source_rows = set()
    spencer_rows = set()
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for product_index in range(3):
            for remainder, value in sixth.get(
                    (product_index, directions), {}).items():
                row = (0, product_index, tuple(sorted(remainder + coefficient)))
                column[row] += value
                source_rows.add(row)
        for (composed_coefficient, composed_directions), composed_weight in (
                endpoint_composition_antisymmetric(
                    (coefficient, directions)).items()):
            for selected, multiplicity in Counter(
                    composed_directions).items():
                remaining = list(composed_directions)
                remaining.remove(selected)
                remaining = tuple(remaining)
                derivative_table = {5: fifth, 6: sixth, 7: seventh}.get(
                    len(remaining))
                require(derivative_table is not None,
                        "the endpoint composition acquired another order")
                for product_index in range(3):
                    for remainder, value in derivative_table.get(
                            (product_index, remaining), {}).items():
                        row = (1, product_index, selected, tuple(sorted(
                            remainder + composed_coefficient)))
                        column[row] += (composed_weight * multiplicity * value)
                        spencer_rows.add(row)
            if include_second_spencer:
                removed_faces = Counter()
                for positions in combinations(range(len(composed_directions)),
                                              2):
                    removed = tuple(sorted(composed_directions[position]
                                           for position in positions))
                    remaining = tuple(composed_directions[position]
                                      for position in range(
                                          len(composed_directions))
                                      if position not in positions)
                    removed_faces[(removed, remaining)] += 1
                for (removed, remaining), multiplicity in (
                        removed_faces.items()):
                    derivative_table = {4: fourth, 5: fifth, 6: sixth}.get(
                        len(remaining))
                    require(derivative_table is not None,
                            "a second endpoint face acquired another order")
                    for product_index in range(3):
                        for remainder, value in derivative_table.get(
                                (product_index, remaining), {}).items():
                            row = (2, product_index, removed, tuple(sorted(
                                remainder + composed_coefficient)))
                            column[row] += (
                                composed_weight * multiplicity * value
                            )
        for left, right in combinations(range(6), 2):
            pair = tuple(sorted((directions[left], directions[right])))
            column[(shadow_kind, pair)] += 1
        shift = repair.degree_subtract(
            repair.colour_degree(coefficient),
            repair.colour_degree(directions),
        )
        columns_by_shift[shift].append(((coefficient, directions), {
            row: value for row, value in column.items() if value
        }))

    if any(argument.startswith("--emit-singular") for argument in sys.argv):
        argument = next(argument for argument in sys.argv
                        if argument.startswith("--emit-singular"))
        characteristic = (argument.split("=", 1)[1]
                          if "=" in argument else "1000003")
        columns = [column for _shift, block in sorted(
            columns_by_shift.items(), key=repr) for _metadata, column in block]
        target = {(shadow_kind, pair): int(value) for pair, value in
                  commutator.expected_second_shadow().items()}
        rows = sorted({row for column in columns for row in column} |
                      set(target))
        row_index = {row: index + 1 for index, row in enumerate(rows)}

        def vector_expression(vector):
            terms = []
            for row, value in sorted(vector.items(), key=lambda item:
                                     row_index[item[0]]):
                if not value:
                    continue
                terms.append(f"({value})*gen({row_index[row]})")
            return "+".join(terms) if terms else "0"

        print(f"ring r={characteristic},(x),dp;")
        print("option(redSB);")
        print("module M=" + ",\n".join(
            vector_expression(column) for column in columns) + ";")
        print("module G=std(M);")
        print("vector T=" + vector_expression(target) + ";")
        print('print("BEGIN_SPENCER_RESULT");')
        print("print(size(G));")
        print("print(reduce(T,G));")
        print('print("END_SPENCER_RESULT");')
        print("quit;")
        return {"emitted_singular": True}

    if "--probe-private" in sys.argv:
        private_row = (
            1, 2, (3, 7, 1, 1),
            tuple(sorted((
                (0, 1, 0, 1), (2, 7, 2, 1), (3, 4, 1, 1),
                (3, 5, 1, 2), (6, 7, 2, 2),
            ))),
        )
        owners = []
        for shift, block in sorted(columns_by_shift.items(), key=repr):
            for metadata_entry, column in block:
                if column.get(private_row):
                    owners.append({
                        "shift": list(shift),
                        "metadata": repr(metadata_entry),
                        "coefficient": column[private_row],
                        "source_support": sum(row[0] == 0 for row in column),
                        "singleton_support": sum(row[0] == 1 for row in column),
                        "shadow": sorted((repr(row[1]), value)
                                         for row, value in column.items()
                                         if row[0] == 2),
                    })
        print(json.dumps({
            "private_row": repr(private_row),
            "owner_count": len(owners),
            "owners": owners,
        }, sort_keys=True))
        return {"private_probe": True}

    if ("--row-elim" in sys.argv
            or "--second-row-elim" in sys.argv):
        columns = [entry for _shift, block in sorted(
            columns_by_shift.items(), key=repr) for entry in block]
        target = {(shadow_kind, pair): int(value) for pair, value in
                  commutator.expected_second_shadow().items()}
        plain_rank, augmented_rank, inconsistent, equation_count = (
            row_rank_mod_p(columns, target, MODULUS)
        )
        result = {
            "eligible_order6_columns": len(columns),
            "equations": equation_count,
            "row_rank_mod_p": plain_rank,
            "augmented_row_rank_mod_p": augmented_rank,
            "target_in_image_mod_p": not inconsistent,
            "modulus": MODULUS,
            "spencer_layers_forced_zero": (
                2 if include_second_spencer else 1
            ),
        }
        print(json.dumps(result, sort_keys=True))
        return result

    diagnostic_flags = {
        "--row-elim", "--second-row-elim", "--second-block-elim",
        "--mod2-only",
        "--probe-private",
    }
    exact_default = not any(
        argument in diagnostic_flags or argument.startswith("--emit-singular")
        for argument in sys.argv[1:]
    )
    if "--exact-row-elim" in sys.argv or exact_default:
        indexed_columns = [(_shift, entry) for _shift, block in sorted(
            columns_by_shift.items(), key=repr) for entry in block]
        columns = [entry for _shift, entry in indexed_columns]
        target = {(2, pair): int(value) for pair, value in
                  commutator.expected_second_shadow().items()}
        solution, rank = exact_row_solution(columns, target)
        encoded = sorted((str(value), repr(columns[index][0]))
                         for index, value in solution.items())
        endpoint_operator = Counter()
        shadow_by_fine_shift = defaultdict(Counter)
        for index, value in solution.items():
            fine_shift = indexed_columns[index][0]
            for row, row_value in columns[index][1].items():
                if row[0] == 2:
                    shadow_by_fine_shift[fine_shift][row[1]] += (
                        value * row_value
                    )
            for term, term_value in endpoint_composition_antisymmetric(
                    columns[index][0]).items():
                endpoint_operator[term] += value * term_value / 2
        endpoint_operator = Counter({term: value for term, value in
                                     endpoint_operator.items() if value})

        derivative_tables = {4: fourth, 5: fifth, 6: sixth, 7: seventh}

        def coefficient_face_output(removed_size):
            output = Counter()
            for (coefficient, directions), operator_weight in (
                    endpoint_operator.items()):
                for positions in combinations(range(len(directions)),
                                              removed_size):
                    removed = tuple(sorted(directions[position]
                                           for position in positions))
                    remaining = tuple(directions[position]
                                      for position in range(len(directions))
                                      if position not in positions)
                    table = derivative_tables.get(len(remaining))
                    require(table is not None,
                            "a prolonged endpoint face left orders four--seven")
                    for product_index in range(3):
                        for remainder, derivative_value in table.get(
                                (product_index, remaining), {}).items():
                            row = (product_index, removed,
                                   tuple(sorted(remainder + coefficient)))
                            output[row] += operator_weight * derivative_value
            return Counter({row: value for row, value in output.items()
                            if value})

        singleton_output = coefficient_face_output(1)
        doubleton_output = coefficient_face_output(2)
        require(not singleton_output,
                "the exact affine solution retained a singleton Spencer face")
        nonzero_shift_shadows = {
            shift: Counter({pair: value for pair, value in shadow.items()
                            if value})
            for shift, shadow in shadow_by_fine_shift.items()
        }
        nonzero_shift_shadows = {
            shift: shadow for shift, shadow in nonzero_shift_shadows.items()
            if shadow
        }
        result = {
            "eligible_order6_columns": len(columns),
            "exact_row_rank": rank,
            "exact_solution_terms": len(solution),
            "exact_solution_denominators": sorted({
                value.denominator for value in solution.values()
            }),
            "exact_solution_sha256": sha256(json.dumps(
                encoded, separators=(",", ":")).encode()).hexdigest(),
            "endpoint_antisymmetric_operator_terms": len(endpoint_operator),
            "first_spencer_face_support": len(singleton_output),
            "second_spencer_face_support": len(doubleton_output),
            "second_spencer_face_l1": str(sum(
                abs(value) for value in doubleton_output.values())),
            "second_spencer_face_sha256": sha256(json.dumps(
                sorted((repr(row), str(value)) for row, value in
                       doubleton_output.items()),
                separators=(",", ":"),
            ).encode()).hexdigest(),
            "nonzero_fine_shift_shadow_count": len(nonzero_shift_shadows),
            "fine_shift_shadows": [
                {
                    "shift": repr(shift),
                    "support": len(shadow),
                    "l1": str(sum(abs(value) for value in shadow.values())),
                    "sha256": sha256(json.dumps(
                        sorted((repr(pair), str(value)) for pair, value in
                               shadow.items()),
                        separators=(",", ":"),
                    ).encode()).hexdigest(),
                }
                for shift, shadow in sorted(nonzero_shift_shadows.items(),
                                            key=lambda item: repr(item[0]))
            ],
        }
        require(result["eligible_order6_columns"] == 8580
                and result["exact_row_rank"] == 1328
                and result["exact_solution_terms"] == 343,
                "the exact first-Spencer-flat affine solution changed")
        return result

    # Source and singleton rows in different fine shifts are disjoint.  Only
    # the forgotten-grade pair shadow is common.  Eliminate each block first
    # and retain only the shadow images of its constraint kernel; this avoids
    # artificial cross-grade fill-in.
    block_records = []
    kernel_shadow_vectors = []
    for block_index, (shift, columns) in enumerate(sorted(
            columns_by_shift.items(), key=repr)):
        # Iteratively delete a column hit by a private literal source or
        # singleton row.  Such a row forces that coefficient to zero in
        # every constraint-kernel vector.  This is exact over every field.
        row_to_columns = defaultdict(set)
        constraint_rows_by_column = []
        for column_index, (_metadata, column) in enumerate(columns):
            rows = tuple(row for row in column if row[0] < shadow_kind)
            constraint_rows_by_column.append(rows)
            for row in rows:
                row_to_columns[row].add(column_index)
        active = set(range(len(columns)))
        private_queue = deque(row for row, owners in row_to_columns.items()
                              if len(owners) == 1)
        while private_queue:
            row = private_queue.popleft()
            owners = row_to_columns[row] & active
            if len(owners) != 1:
                continue
            column_index = next(iter(owners))
            active.remove(column_index)
            for incident in constraint_rows_by_column[column_index]:
                remaining = row_to_columns[incident] & active
                if len(remaining) == 1:
                    private_queue.append(incident)
        peeled = len(columns) - len(active)
        surviving_columns = [columns[index] for index in sorted(active)]
        print("peeled fine-shift block", block_index + 1, len(columns),
              peeled, len(surviving_columns), flush=True)

        mod2_rank, mod2_rows = rank_mod2_constraints(
            surviving_columns, shadow_kind
        )
        full_column_rank_mod2 = mod2_rank == len(surviving_columns)
        print("mod2 constraint rank", block_index + 1, mod2_rank,
              len(surviving_columns), mod2_rows, flush=True)

        if full_column_rank_mod2:
            block_records.append({
                "shift": list(shift),
                "columns": len(columns),
                "private_face_peeled_columns": peeled,
                "two_core_columns": len(surviving_columns),
                "constraint_rows_mod2": mod2_rows,
                "constraint_rank_mod2": mod2_rank,
                "full_column_rank_mod2": True,
                "combined_rank": len(columns),
                "kernel_shadow_rank": 0,
            })
            continue
        if "--mod2-only" in sys.argv:
            block_records.append({
                "shift": list(shift),
                "columns": len(columns),
                "private_face_peeled_columns": peeled,
                "two_core_columns": len(surviving_columns),
                "constraint_rows_mod2": mod2_rows,
                "constraint_rank_mod2": mod2_rank,
                "full_column_rank_mod2": False,
                "combined_rank": None,
                "kernel_shadow_rank": None,
            })
            continue

        basis = {}
        shadow_rank = 0
        for _metadata, column in surviving_columns:
            vector = reduce_mod(column, basis)
            if not vector:
                continue
            pivot = min(vector)
            inverse = pow(vector[pivot], MODULUS - 2, MODULUS)
            vector = {row: value * inverse % MODULUS
                      for row, value in vector.items()}
            basis[pivot] = vector
            if pivot[0] == shadow_kind:
                require(all(row[0] == shadow_kind for row in vector),
                        "a kernel-shadow pivot retained a constraint row")
                kernel_shadow_vectors.append(vector)
                shadow_rank += 1
        block_records.append({
            "shift": list(shift),
            "columns": len(columns),
            "private_face_peeled_columns": peeled,
            "two_core_columns": len(surviving_columns),
            "constraint_rows_mod2": mod2_rows,
            "constraint_rank_mod2": mod2_rank,
            "full_column_rank_mod2": False,
            "combined_rank": len(basis),
            "kernel_shadow_rank": shadow_rank,
        })
        print("finished fine-shift block", block_index + 1,
              len(columns), len(basis), shadow_rank, flush=True)

    shadow_basis = {}
    for vector in kernel_shadow_vectors:
        reduced = reduce_mod(vector, shadow_basis)
        if not reduced:
            continue
        pivot = min(reduced)
        inverse = pow(reduced[pivot], MODULUS - 2, MODULUS)
        shadow_basis[pivot] = {
            row: value * inverse % MODULUS for row, value in reduced.items()
        }

    target = {(shadow_kind, pair): int(value) % MODULUS
              for pair, value in commutator.expected_second_shadow().items()}
    remainder = reduce_mod(target, shadow_basis)
    target_in_image = not remainder

    result = {
        "eligible_order6_columns": sum(len(columns) for columns in
                                        columns_by_shift.values()),
        "fine_shift_blocks": block_records,
        "literal_source_rows": len(source_rows),
        "singleton_spencer_rows": len(spencer_rows),
        "kernel_shadow_rank": len(shadow_basis),
        "minus_delta_in_source_plus_singleton_plus_shadow_image_mod_p":
            target_in_image,
        "modulus": MODULUS,
        "target_remainder_support": len(remainder),
        "first_target_remainder": repr(next(iter(remainder.items())))
            if remainder else None,
    }
    print(json.dumps(result, sort_keys=True))
    return result


def main():
    result = audit()
    if sys.argv[1:]:
        payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
        print("h3 order-six Spencer affine diagnostic: PASS")
        print("ledger_sha256=" + sha256(payload.encode()).hexdigest())
        return
    ledger = {
        "theorem": "first-Spencer-flat endpoint-recoloured order-six lift",
        "audit": result,
        "scope": (
            "the complete 8,580-column quadratic/order-six missing-face "
            "block on the three quadratic source products.  The theorem "
            "constructs a rational representative with zero first "
            "coefficient-prolonging faces; it does not kill its second "
            "Spencer layer, type the physical repeated grade, or construct "
            "the eta/sigma terminal comparison"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("first-Spencer-flat ledger changed", digest))
    print("h3 order-six Spencer affine feasibility: PASS")
    print("exact rational representative: 343 terms")
    print("first Spencer face: zero")
    print("second Spencer face support:",
          result["second_spencer_face_support"])
    print("nonzero fine-shift shadows:",
          result["nonzero_fine_shift_shadow_count"])
    for record in result["fine_shift_shadows"]:
        print("fine-shift shadow:", record)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
