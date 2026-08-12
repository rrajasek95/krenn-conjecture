#!/usr/bin/env python3
"""Audit ambient coefficient cells in the residual-q order-five repair.

The committed order-five solve allowed the linear coefficient of x*d_T only
when x occurred in one of the two complete source generators.  This checker
removes that restriction: for every admissible fifth derivative direction,
it tries all nine colour decorations on the forced physical coefficient
edge, including the direct-free edge omitted from both generators.

It asks whether any new ambient term has one of the two required commutator
fine shifts.  A positive answer would be the first polynomial-kernel place
where eta/sigma terminal data could enter.  A negative answer proves that
the terminal correction requires a genuinely shifted relative module.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "notes/h3-residual-q-order5-generator-repair.md":
        "ac43ca7c2f44151c6386743e5d1af30f0809e294e0c11185731234de9fac9e3d",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = "d662ae2571dc6c47a62cb76847709ef9f06f14e9aa02116a7ec297f5d2defb60"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def sparse_rank(columns):
    pivots = {}
    for source in columns:
        column = {row: Q(value) for row, value in source.items() if value}
        while column:
            pivot = min(column, key=repr)
            value = column[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in column.items()
                }
                break
            for row, coefficient in pivots[pivot].items():
                updated = column.get(row, Q(0)) - value * coefficient
                if updated:
                    column[row] = updated
                else:
                    column.pop(row, None)
    return len(pivots)


def quotient_separator(columns, target):
    """Return a rational left separator for target outside column span."""
    pivots = {}

    def reduce(column):
        column = {row: Q(value) for row, value in column.items() if value}
        for pivot in sorted(pivots, key=repr):
            value = column.get(pivot, Q(0))
            if not value:
                continue
            for row, coefficient in pivots[pivot].items():
                updated = column.get(row, Q(0)) - value * coefficient
                if updated:
                    column[row] = updated
                else:
                    column.pop(row, None)
        return column

    for source in columns:
        remainder = reduce(source)
        if not remainder:
            continue
        pivot = min(remainder, key=repr)
        value = remainder[pivot]
        new_basis = {
            row: coefficient / value
            for row, coefficient in remainder.items()
        }
        # Maintain reduced pivot columns so quotient reduction is linear and
        # independent of the order in which nonpivot rows appear.
        for old_pivot, old_basis in list(pivots.items()):
            factor = old_basis.get(pivot, Q(0))
            if not factor:
                continue
            updated_basis = dict(old_basis)
            for row, coefficient in new_basis.items():
                updated = updated_basis.get(row, Q(0)) - factor * coefficient
                if updated:
                    updated_basis[row] = updated
                else:
                    updated_basis.pop(row, None)
            pivots[old_pivot] = updated_basis
        pivots[pivot] = new_basis

    target_remainder = reduce(target)
    require(target_remainder, "separator target entered the column span")
    quotient_row = min(target_remainder, key=repr)
    normalizer = target_remainder[quotient_row]
    all_rows = set(target)
    for source in columns:
        all_rows.update(source)
    functional = {}
    for row in all_rows:
        value = reduce({row: 1}).get(quotient_row, Q(0)) / normalizer
        if value:
            functional[row] = value
    require(sum(functional.get(row, Q(0)) * Q(value)
                for row, value in target.items()) == 1,
            "separator target normalization changed")
    require(all(sum(functional.get(row, Q(0)) * Q(value)
                    for row, value in source.items()) == 0
                for source in columns),
            "left separator stopped killing the source columns")
    return functional, target_remainder


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(expected == "TO_BE_HASHED" or actual == expected,
                ("pinned dependency changed", relative, actual))

    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "ambient_order5_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "ambient_order5_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "ambient_order5_base",
    )
    system = repair.build_system(base, commutator)
    old_terms = set(system["columns"])
    corner_shifts = tuple(
        tuple(-value for value in repair.colour_degree(corner))
        for corner in commutator.CORNERS
    )

    eligible = set()
    all_ambient = set()
    eligible_by_shift = Counter()
    ambient_by_shift = Counter()
    direct_free_ambient = set()
    direct_free_eligible = set()
    direct_free_pair = tuple(sorted(base.DIRECT_FREE_PAIR))

    for polynomial in system["products"]:
        for monomial, base_coefficient in polynomial.items():
            require(base_coefficient, "a zero product monomial survived")
            for positions in combinations(range(8), 5):
                directions = tuple(sorted(monomial[position]
                                          for position in positions))
                # Replay the exact multiplicity factor as a guard that this
                # is the same operator census as the source repair.
                derivative_factor = base_coefficient
                for count in Counter(directions).values():
                    derivative_factor *= factorial(count)
                require(derivative_factor, "a fifth derivative vanished")
                degree = repair.endpoint_degrees(directions)
                doubled = tuple(site for site, value in enumerate(degree)
                                if value == 2)
                if (len(doubled) != 2
                        or any(value not in (1, 2) for value in degree)):
                    continue
                left, right = sorted(doubled)
                for left_colour, right_colour in product(range(3), repeat=2):
                    coefficient = (left, right, left_colour, right_colour)
                    metadata = (coefficient, directions)
                    all_ambient.add(metadata)
                    shift = repair.degree_subtract(
                        repair.colour_degree((coefficient,)),
                        repair.colour_degree(directions),
                    )
                    ambient_by_shift[shift] += 1
                    if (left, right) == direct_free_pair:
                        direct_free_ambient.add(metadata)
                    if shift in corner_shifts:
                        eligible.add(metadata)
                        eligible_by_shift[corner_shifts.index(shift)] += 1
                        if (left, right) == direct_free_pair:
                            direct_free_eligible.add(metadata)

    new_eligible = eligible - old_terms
    missing_old = old_terms - eligible
    old_coefficients = {item[0] for item in old_terms}
    new_coefficients = sorted({item[0] for item in new_eligible}
                              - old_coefficients)
    # Counts in the Counters above include repeated generation of a metadata
    # term.  The theorem uses the unique term sets.
    unique_by_shift = Counter()
    for coefficient, directions in eligible:
        shift = repair.degree_subtract(
            repair.colour_degree((coefficient,)),
            repair.colour_degree(directions),
        )
        unique_by_shift[corner_shifts.index(shift)] += 1

    # The only new coefficient cell is absent from every generator, so its
    # output rows are disjoint from the committed block.  Determine whether
    # its 180 eligible operators contain any source cycle.
    direct_metadata = sorted(direct_free_eligible, key=repr)
    direct_columns = []
    for coefficient, directions in direct_metadata:
        column = Counter()
        for product_index, polynomial in enumerate(system["products"]):
            for remainder, value in repair.derivatives(
                    polynomial, directions).items():
                output = tuple(sorted(remainder + (coefficient,)))
                column[(product_index, output)] += value
        direct_columns.append(dict(column))
    direct_rank = sparse_rank(direct_columns)
    direct_rows = {row for column in direct_columns for row in column}
    require(all(any(cell[:2] == direct_free_pair for cell in monomial)
                for _product, monomial in direct_rows),
            "a direct-free coefficient column lost its direct cell")

    def rank_with_terminal(functionals):
        augmented = []
        for column_index, column in enumerate(direct_columns):
            output = dict(column)
            for name, values in functionals.items():
                value = values[column_index]
                if value:
                    output[("terminal", name)] = value
            augmented.append(output)
        return sparse_rank(augmented)

    ones = [1] * len(direct_metadata)
    shift_parity = []
    corner_hits = [[] for _corner in commutator.CORNERS]
    for coefficient, directions in direct_metadata:
        shift = repair.degree_subtract(
            repair.colour_degree((coefficient,)),
            repair.colour_degree(directions),
        )
        shift_index = corner_shifts.index(shift)
        shift_parity.append(1 if shift_index == 0 else -1)
        multiplicities = Counter(directions)
        for corner_index, corner in enumerate(commutator.CORNERS):
            corner_count = Counter(corner)
            corner_hits[corner_index].append(int(all(
                multiplicities[cell] >= count
                for cell, count in corner_count.items()
            )))
    alpha_corner = [
        sum(int(commutator.ALPHA[corner]) * corner_hits[corner][index]
            for corner in range(4))
        for index in range(len(direct_metadata))
    ]
    second_shadow = commutator.expected_second_shadow()
    second_shadow_pairing = []
    for _coefficient, directions in direct_metadata:
        value = 0
        for left, right in combinations(range(len(directions)), 2):
            value += second_shadow.get(tuple(sorted(
                (directions[left], directions[right])
            )), 0)
        second_shadow_pairing.append(value)
    terminal_audits = {}
    for name, values in {
        "all_ones": ones,
        "pure_minus_mixed_shift": shift_parity,
        "alpha_corner_containment": alpha_corner,
        "codimension_two_minus_delta_shadow": second_shadow_pairing,
    }.items():
        augmented_rank = rank_with_terminal({name: values})
        terminal_audits[name] = {
            "augmented_rank": augmented_rank,
            "nonzero_on_source_kernel": augmented_rank > direct_rank,
            "nonzero_entries": sum(bool(value) for value in values),
        }
    four_corner_rank = rank_with_terminal({
        f"corner_{index}": values
        for index, values in enumerate(corner_hits)
    })
    all_candidate_rank = rank_with_terminal({
        "all_ones": ones,
        "pure_minus_mixed_shift": shift_parity,
        **{f"corner_{index}": values
           for index, values in enumerate(corner_hits)},
        "codimension_two_minus_delta_shadow": second_shadow_pairing,
    })

    # Since the shadow raises rank by one, solve exactly for a source cycle
    # normalized to shadow value one.
    terminal_row = (3, ("terminal_codimension_two_minus_delta_shadow",))
    augmented_columns = []
    for metadata, column, terminal in zip(
            direct_metadata, direct_columns, second_shadow_pairing,
            strict=True):
        augmented = dict(column)
        if terminal:
            augmented[terminal_row] = int(terminal)
        augmented_columns.append((metadata, augmented))
    picked = repair.select_modular_basis(augmented_columns)
    require(len(picked) == direct_rank + 1,
            "the residual shadow rank jump changed")
    solution, picked_metadata = repair.exact_solution(
        augmented_columns, picked, {terminal_row: 1}
    )
    source_reconstruction = Counter()
    shadow_reconstruction = Q(0)
    encoded_solution = []
    for local_index, coefficient in solution.items():
        metadata = picked_metadata[local_index]
        original_index = direct_metadata.index(metadata)
        for row, value in direct_columns[original_index].items():
            source_reconstruction[row] += coefficient * value
        shadow_reconstruction += (
            coefficient * second_shadow_pairing[original_index]
        )
        encoded_solution.append((str(coefficient), repr(metadata)))
    require(not +source_reconstruction and shadow_reconstruction == 1,
            "the normalized direct-edge residual cycle changed")
    solution_digest = sha256(json.dumps(
        sorted(encoded_solution), separators=(",", ":")
    ).encode()).hexdigest()

    # Stronger vector-valued test: does a direct-edge source cycle have the
    # entire 16-coordinate codimension-two shadow, not merely nonzero pairing
    # with it?
    shadow_columns = []
    for metadata, column in zip(direct_metadata, direct_columns, strict=True):
        _coefficient, directions = metadata
        augmented = dict(column)
        for left, right in combinations(range(len(directions)), 2):
            pair = tuple(sorted((directions[left], directions[right])))
            row = (3, pair)
            augmented[row] = augmented.get(row, 0) + 1
        shadow_columns.append((metadata, augmented))
    shadow_target = {
        (3, pair): int(value) for pair, value in second_shadow.items()
    }
    shadow_picked = repair.select_modular_basis(shadow_columns)
    shadow_with_target_rank = len(repair.select_modular_basis(
        shadow_columns + [("target", shadow_target)]
    ))
    exact_shadow_solvable = shadow_with_target_rank == len(shadow_picked)
    shadow_only_columns = [
        (metadata, {row: value for row, value in column.items()
                    if row[0] == 3})
        for metadata, column in shadow_columns
    ]
    shadow_only_picked = repair.select_modular_basis(shadow_only_columns)
    shadow_only_with_target_rank = len(repair.select_modular_basis(
        shadow_only_columns + [("target", shadow_target)]
    ))
    shadow_only_target_solvable = (
        shadow_only_with_target_rank == len(shadow_only_picked)
    )
    shadow_only_separator = None
    if not shadow_only_target_solvable:
        shadow_only_separator, _shadow_only_remainder = quotient_separator(
            [column for _metadata, column in shadow_only_columns],
            shadow_target,
        )
    missing_face = (3, tuple(sorted((
        (0, 7, 1, 1),
        (2, 4, 1, 1),
    ))))
    require(shadow_only_separator == {missing_face: Q(1)},
            "the primitive one-face separator changed")
    exact_shadow_solution_terms = None
    if exact_shadow_solvable:
        shadow_solution, _shadow_metadata = repair.exact_solution(
            shadow_columns, shadow_picked, shadow_target
        )
        exact_shadow_solution_terms = len(shadow_solution)
    shadow_separator = None
    shadow_remainder = None
    if not exact_shadow_solvable:
        shadow_separator, shadow_remainder = quotient_separator(
            [column for _metadata, column in shadow_columns], shadow_target
        )
    separator_source_rows = {
        row: value for row, value in (shadow_separator or {}).items()
        if row[0] < 3
    }
    separator_shadow_rows = {
        row: value for row, value in (shadow_separator or {}).items()
        if row[0] == 3
    }

    return {
        "ambient_physical_coefficient_cells": 28 * 9,
        "unique_ambient_order5_terms": len(all_ambient),
        "committed_source_terms": len(old_terms),
        "fine_shift_eligible_terms": len(eligible),
        "eligible_unique_shift_split": dict(sorted(unique_by_shift.items())),
        "new_fine_shift_eligible_terms": len(new_eligible),
        "new_fine_shift_coefficient_cells": [list(cell)
                                              for cell in new_coefficients],
        "committed_terms_missing_from_ambient_replay": len(missing_old),
        "direct_free_edge": list(direct_free_pair),
        "direct_free_ambient_terms": len(direct_free_ambient),
        "direct_free_fine_shift_eligible_terms": len(direct_free_eligible),
        "direct_free_eligible_column_rank": direct_rank,
        "direct_free_eligible_kernel_dimension":
            len(direct_columns) - direct_rank,
        "direct_free_output_rows": len(direct_rows),
        "direct_free_terminal_functionals": terminal_audits,
        "four_corner_augmented_rank": four_corner_rank,
        "all_candidate_terminal_augmented_rank": all_candidate_rank,
        "normalized_residual_cycle": {
            "nonzero_operator_terms": len(solution),
            "coefficient_denominators": sorted({
                coefficient.denominator for coefficient in solution.values()
            }),
            "source_boundary_terms": len(+source_reconstruction),
            "codimension_two_minus_delta_shadow":
                str(shadow_reconstruction),
            "solution_sha256": solution_digest,
            "operator_terms": sorted(encoded_solution),
        },
        "full_codimension_two_shadow_test": {
            "source_plus_shadow_column_rank": len(shadow_picked),
            "rank_after_adjoining_exact_minus_delta": shadow_with_target_rank,
            "exact_minus_delta_shadow_solvable": exact_shadow_solvable,
            "shadow_only_column_rank": len(shadow_only_picked),
            "shadow_only_rank_after_target": shadow_only_with_target_rank,
            "shadow_only_target_solvable": shadow_only_target_solvable,
            "shadow_only_separator_support": len(shadow_only_separator or {}),
            "shadow_only_separator_coordinates": [
                [repr(row[1]), str(value)]
                for row, value in sorted(
                    (shadow_only_separator or {}).items(),
                    key=lambda item: repr(item[0]),
                )
            ],
            "exact_solution_terms": exact_shadow_solution_terms,
            "quotient_remainder_terms": len(shadow_remainder or {}),
            "left_separator_source_support": len(separator_source_rows),
            "left_separator_shadow_support": len(separator_shadow_rows),
            "left_separator_source_coordinates": [
                [repr(row), str(value)]
                for row, value in sorted(separator_source_rows.items(),
                                         key=lambda item: repr(item[0]))
            ],
            "left_separator_shadow_coordinates": [
                [repr(row[1]), str(value)]
                for row, value in sorted(separator_shadow_rows.items(),
                                         key=lambda item: repr(item[0]))
            ],
        },
        "eligible_coefficient_variables": len({item[0] for item in eligible}),
        "eligible_has_colour_zero_cell": any(
            0 in coefficient[2:] for coefficient, _directions in eligible
        ),
        "eligible_has_marked_p_or_x_colour2_cell": any(
            ((coefficient[0] in (0, 6) and coefficient[2] == 2)
             or (coefficient[1] in (0, 6) and coefficient[3] == 2))
            for coefficient, _directions in eligible
        ),
        "verdict": (
            "the ambient replay adds one direct-free 11 coefficient and a "
            "large source kernel.  A two-term integral cycle is detected by "
            "the minus-delta scalar pairing, but the full 16-coordinate "
            "minus-delta shadow is not in the source-plus-shadow image.  "
            "Already the shadow-only projection misses the single face "
            "07:11 wedge 24:11; all natural eta/sigma character rows remain "
            "zero"
        ),
    }


def main():
    ledger = {
        "theorem": "ambient order-five terminal-shift boundary",
        "audit": audit(),
        "scope": (
            "all linear-coefficient fifth-order differential operators on "
            "the two pair generators, with all 252 ambient decorated physical "
            "cells.  This does not enumerate separately shifted relative or "
            "mapping-cone generators"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ambient order-five ledger changed: {digest}")
    print("h3 residual-q ambient order-five terminal shift: AUDIT")
    audit_result = ledger["audit"]
    print(json.dumps({
        "ambient_physical_coefficient_cells":
            audit_result["ambient_physical_coefficient_cells"],
        "unique_ambient_order5_terms":
            audit_result["unique_ambient_order5_terms"],
        "new_fine_shift_coefficient_cells":
            audit_result["new_fine_shift_coefficient_cells"],
        "direct_free_eligible_column_rank":
            audit_result["direct_free_eligible_column_rank"],
        "direct_free_eligible_kernel_dimension":
            audit_result["direct_free_eligible_kernel_dimension"],
        "full_codimension_two_shadow_test": {
            key: value for key, value in
            audit_result["full_codimension_two_shadow_test"].items()
            if not key.endswith("_coordinates")
        },
    }, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
