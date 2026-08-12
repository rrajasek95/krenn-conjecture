#!/usr/bin/env python3
"""Probe the first quadratic/order-six route to the missing residual face.

The linear/order-five ambient module misses the singleton lower face
07:11 wedge 24:11.  This checker enumerates every correctly graded
quadratic-coefficient sixth-order operator whose derivative directions
contain that face.  It then asks whether the restricted block already has a
literal source cycle with nonzero missing-face augmentation.

The selected block is then augmented by every codimension-two lower face.
It turns out to contain an exact chain with zero literal source boundary and
the complete sixteen-coordinate ``-delta`` shadow.  This is still not the
complete order-six Spencer tower: source cancellation is restricted to
columns which themselves contain the missing face, and higher proper faces
and eta/sigma terminals are not imposed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_residual_q_order5_ambient_terminal_shift_boundary.py":
        "e58f91c166f0c94b7155b2f43bb26d9e085cb9f4e0062241e8c946dba37f068d",
}
EXPECTED_LEDGER_SHA256 = "78fabcce9541b559b3778cf06f70f207c802dbf615cd19262afc50866cb92bad"


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


def oriented_edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def four_site_matchings(sites):
    left, middle_left, middle_right, right = sorted(sites)
    return (
        ((left, middle_left), (middle_right, right)),
        ((left, middle_right), (middle_left, right)),
        ((left, right), (middle_left, middle_right)),
    )


def build_exact_sixth_derivatives(system):
    """Return exact product derivatives indexed by (product, directions)."""
    table = defaultdict(Counter)
    for product_index, polynomial in enumerate(system["products"]):
        for monomial, base_coefficient in polynomial.items():
            available = Counter(monomial)
            seen = set()
            for positions in combinations(range(8), 6):
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
                table[(product_index, directions)][
                    tuple(sorted(remainder))
                ] += coefficient
    return table


def eligible_coefficients(repair, commutator, directions):
    """Generate the forced quadratic coefficients in the four corner shifts."""
    endpoint_degree = repair.endpoint_degrees(directions)
    if (any(value not in (1, 2) for value in endpoint_degree)
            or any(value < 1 for value in endpoint_degree)):
        return set()
    doubled = tuple(site for site, value in enumerate(endpoint_degree)
                    if value == 2)
    if len(doubled) != 4:
        return set()

    direction_colour_degree = repair.colour_degree(directions)
    answer = set()
    for corner in commutator.CORNERS:
        corner_degree = repair.colour_degree(corner)
        required = tuple(left - right for left, right in
                         zip(direction_colour_degree, corner_degree,
                             strict=True))
        if any(value not in (0, 1) for value in required) or sum(required) != 4:
            continue
        colours = {}
        valid = True
        for site in range(8):
            occupied = [colour for colour in range(3)
                        if required[3 * site + colour]]
            if site in doubled:
                if len(occupied) != 1:
                    valid = False
                    break
                colours[site] = occupied[0]
            elif occupied:
                valid = False
                break
        if not valid:
            continue
        for matching in four_site_matchings(doubled):
            coefficient = tuple(sorted(
                oriented_edge(left, right, colours[left], colours[right])
                for left, right in matching
            ))
            answer.add(coefficient)
    return answer


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(expected == "TO_BE_HASHED" or actual == expected,
                ("pinned dependency changed", relative, actual))

    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "order6_probe_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "order6_probe_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "order6_probe_base",
    )
    system = repair.build_system(base, commutator)
    derivatives = build_exact_sixth_derivatives(system)

    missing_face = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))
    metadata = set()
    for _product_index, directions in derivatives:
        if not missing_face.issubset(directions):
            continue
        for coefficient in eligible_coefficients(repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns = []
    shadow_columns = []
    source_rows = set()
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for product_index in range(3):
            for remainder, value in derivatives.get(
                    (product_index, directions), {}).items():
                row = (product_index, tuple(sorted(remainder + coefficient)))
                column[row] += value
                source_rows.add(row)
        source_column = {
            row: value for row, value in column.items() if value
        }
        columns.append(((coefficient, directions), source_column))
        shadow_column = dict(source_column)
        for left, right in combinations(range(6), 2):
            row = (3, tuple(sorted((directions[left], directions[right]))))
            shadow_column[row] = shadow_column.get(row, 0) + 1
        shadow_columns.append(((coefficient, directions), shadow_column))

    source_basis = repair.select_modular_basis(columns)
    shadow_basis = repair.select_modular_basis(shadow_columns)
    shadow_target = {
        (3, pair): int(value)
        for pair, value in commutator.expected_second_shadow().items()
    }
    shadow_target_rank = len(repair.select_modular_basis(
        shadow_columns + [("target", shadow_target)]
    ))
    exact_shadow_solvable = shadow_target_rank == len(shadow_basis)
    require(exact_shadow_solvable,
            "the complete order-six block stopped carrying -delta")
    solution, picked_metadata = repair.exact_solution(
        shadow_columns, shadow_basis, shadow_target
    )
    encoded = sorted(
        (str(coefficient), repr(picked_metadata[index]))
        for index, coefficient in solution.items()
    )
    exact_solution_digest = sha256(json.dumps(
        encoded, separators=(",", ":")
    ).encode()).hexdigest()

    reconstruction = Counter()
    solution_metadata = []
    for index, coefficient in solution.items():
        metadata_entry = picked_metadata[index]
        original_index = next(
            position for position, (entry, _column) in enumerate(shadow_columns)
            if entry == metadata_entry
        )
        _metadata, column = shadow_columns[original_index]
        solution_metadata.append((coefficient, metadata_entry))
        for row, value in column.items():
            reconstruction[row] += coefficient * value
    reconstruction = Counter({row: value for row, value in
                              reconstruction.items() if value})
    require(reconstruction == Counter(shadow_target),
            "the exact order-six -delta reconstruction changed")

    denominators = sorted({coefficient.denominator
                           for coefficient in solution.values()})
    coefficient_cells = [cell for _weight, (coefficient, _directions)
                         in solution_metadata for cell in coefficient]
    colour_zero_cells = sum(
        cell[2] == 0 or cell[3] == 0 for cell in coefficient_cells
    )
    marked_colour_two_cells = sum(
        ((cell[0] in (0, 6) and cell[2] == 2)
         or (cell[1] in (0, 6) and cell[3] == 2))
        for cell in coefficient_cells
    )

    require(metadata and solution,
            "the order-six residual chain disappeared")
    return {
        "exact_sixth_derivative_keys": len(derivatives),
        "eligible_missing_face_operators": len(metadata),
        "literal_source_rows": len(source_rows),
        "modular_source_rank": len(source_basis),
        "source_plus_shadow_rank": len(shadow_basis),
        "rank_after_exact_minus_delta": shadow_target_rank,
        "source_kernel_dimension_lower_bound": len(columns) - len(source_basis),
        "exact_minus_delta_solvable": exact_shadow_solvable,
        "exact_normalized_cycle_terms": len(solution),
        "exact_normalized_cycle_sha256": exact_solution_digest,
        "exact_solution_denominators": denominators,
        "solution_coefficient_colour_zero_cells": colour_zero_cells,
        "solution_marked_colour_two_cells": marked_colour_two_cells,
        "source_boundary_terms": sum(
            row[0] < 3 for row in reconstruction
        ),
        "shadow_reconstruction_terms": sum(
            row[0] == 3 for row in reconstruction
        ),
        "missing_face": "07:11 wedge 24:11",
        "verdict": (
            "the first quadratic/order-six missing-face block contains an "
            "exact zero-source chain whose complete codimension-two shadow "
            "is minus-delta.  Higher proper faces, eta/sigma, and full "
            "relative typing remain untested"
        ),
    }


def main():
    ledger = {
        "theorem": "quadratic order-six missing-face source-shadow lift",
        "audit": audit(),
        "scope": (
            "all correctly graded quadratic-coefficient sixth-order operators "
            "which themselves contain 07:11 wedge 24:11; this is not the "
            "complete order-six source/Spencer totalization"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"order-six missing-face ledger changed: {digest}")
    print("h3 residual-q order-six missing face: SOURCE-SHADOW PASS")
    print(json.dumps(ledger["audit"], sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
