#!/usr/bin/env python3
r"""Exact order-five repair of the residual-q commutator on two generators.

Let A0 and A1 be the complete direct-free rows in words 11111111 and
11211211.  The signed fourth-order operator D4 from the covariance-curvature
commutator annihilates A0 and A1, but not their pair products.  This checker
constructs, by exact rational elimination, a linear-coefficient order-five
operator D5 such that

    (D4+D5)(A0^2) = (D4+D5)(A0*A1) = (D4+D5)(A1^2) = 0.

D5 annihilates each quartic generator for degree reasons, so the proved
fourth symbol -delta is unchanged.  This is the generator-level condition
needed by the R-linear Hasse totalization.  It is not the stronger
coefficient-prolonging assertion D(I^2) subset I for arbitrary multipliers,
and it does not construct the physical eta/sigma comparison.
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
EXPECTED_LEDGER_SHA256 = "f0d1edf01a9a01a0fcfd971f114474a4c0a23ae4e0d76a5ea53345081163d88c"
PINS = {
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
MODULUS = 1_000_003


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


def polynomial_multiply(left, right):
    output = defaultdict(int)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            output[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def derivatives(polynomial, directions):
    directions = Counter(directions)
    output = {}
    for monomial, coefficient in polynomial.items():
        multiplicities = Counter(monomial)
        if not all(multiplicities[cell] >= count
                   for cell, count in directions.items()):
            continue
        value = coefficient
        remainder = list(monomial)
        for cell, count in directions.items():
            available = multiplicities[cell]
            for offset in range(count):
                value *= available - offset
            for _ in range(count):
                remainder.remove(cell)
        output[tuple(remainder)] = value
    return output


def apply_fourth(commutator, polynomial):
    output = defaultdict(int)
    for coefficient, directions in zip(
            commutator.ALPHA, commutator.CORNERS, strict=True):
        for monomial, value in derivatives(polynomial, directions).items():
            output[monomial] += int(coefficient) * value
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def endpoint_degrees(directions):
    degree = [0] * 8
    for left, right, _left_colour, _right_colour in directions:
        degree[left] += 1
        degree[right] += 1
    return tuple(degree)


def subtract_multiple(target, source, coefficient):
    for row, value in source.items():
        result = target.get(row, Q(0)) - coefficient * value
        if result:
            target[row] = result
        else:
            target.pop(row, None)


def build_system(base, commutator):
    words = (commutator.PURE_WORD, commutator.MIXED_WORD)
    generators = tuple(
        {monomial: 1 for monomial in base.full_row(word)}
        for word in words
    )
    products = (
        polynomial_multiply(generators[0], generators[0]),
        polynomial_multiply(generators[0], generators[1]),
        polynomial_multiply(generators[1], generators[1]),
    )
    variables = sorted(set().union(*(
        {cell for monomial in generator for cell in monomial}
        for generator in generators
    )))
    variables_by_endpoints = defaultdict(list)
    for variable in variables:
        variables_by_endpoints[variable[:2]].append(variable)

    row_index = {}
    row_keys = []

    def index(key):
        if key not in row_index:
            row_index[key] = len(row_keys)
            row_keys.append(key)
        return row_index[key]

    # A term x*d_T has degree shift -4 precisely when |T|=5 and x is
    # linear.  Generate every term capable of landing in site degree 1^8.
    columns = defaultdict(lambda: defaultdict(int))
    for product_index, polynomial in enumerate(products):
        for monomial, base_coefficient in polynomial.items():
            for positions in combinations(range(8), 5):
                directions = tuple(sorted(monomial[position]
                                          for position in positions))
                derivative_factor = base_coefficient
                for count in Counter(directions).values():
                    derivative_factor *= factorial(count)
                degree = endpoint_degrees(directions)
                doubled_sites = tuple(site for site, value in enumerate(degree)
                                      if value == 2)
                if (len(doubled_sites) != 2
                        or any(value not in (1, 2) for value in degree)):
                    continue
                remainder = tuple(monomial[position]
                                  for position in range(8)
                                  if position not in positions)
                for coefficient_variable in variables_by_endpoints[
                        doubled_sites]:
                    output_monomial = tuple(sorted(
                        remainder + (coefficient_variable,)
                    ))
                    columns[(coefficient_variable, directions)][index(
                        (product_index, output_monomial)
                    )] += derivative_factor

    # Retain complete source-row columns as an audit: the exact solution
    # below turns out to use none of them, so the three pair products vanish
    # outright rather than merely modulo the source ideal.
    ideal_columns = []
    seen_word_blocks = set()
    for product_index, output_monomial in tuple(row_keys):
        colours = [None] * 8
        for left, right, left_colour, right_colour in output_monomial:
            colours[left] = left_colour
            colours[right] = right_colour
        word = tuple(colours)
        key = product_index, word
        if key in seen_word_blocks:
            continue
        seen_word_blocks.add(key)
        ideal_columns.append((key, {
            index((product_index, monomial)): 1
            for monomial in base.full_row(word)
        }))

    target = {}
    fourth_defect_supports = []
    for product_index, polynomial in enumerate(products):
        defect = apply_fourth(commutator, polynomial)
        fourth_defect_supports.append(len(defect))
        for monomial, coefficient in defect.items():
            target[index((product_index, monomial))] = -coefficient

    all_columns = list(columns.items()) + [
        (("ideal",) + metadata, column)
        for metadata, column in ideal_columns
    ]
    return {
        "generators": generators,
        "products": products,
        "variables": variables,
        "columns": columns,
        "ideal_columns": ideal_columns,
        "all_columns": all_columns,
        "row_keys": row_keys,
        "target": target,
        "fourth_defect_supports": fourth_defect_supports,
        "word_blocks": seen_word_blocks,
    }


def select_modular_basis(all_columns):
    basis = {}
    picked = []

    def reduce(vector):
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

    for column_index, (_metadata, column) in enumerate(all_columns):
        vector = reduce(column)
        if not vector:
            continue
        pivot = min(vector)
        inverse = pow(vector[pivot], MODULUS - 2, MODULUS)
        basis[pivot] = {
            row: value * inverse % MODULUS
            for row, value in vector.items()
        }
        picked.append(column_index)
    return picked


def exact_solution(all_columns, picked, target):
    basis_vectors = {}
    basis_representations = {}
    picked_metadata = []

    def reduce(vector, representation=None):
        vector = {row: Q(value) for row, value in vector.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis_vectors:
                return vector, representation
            coefficient = vector[pivot]
            subtract_multiple(vector, basis_vectors[pivot], coefficient)
            if representation is not None:
                subtract_multiple(
                    representation, basis_representations[pivot], coefficient
                )
        return vector, representation

    for local_index, column_index in enumerate(picked):
        metadata, column = all_columns[column_index]
        vector, representation = reduce(column, {local_index: Q(1)})
        require(vector, ("modular basis became rationally dependent", metadata))
        pivot = min(vector)
        inverse = Q(1) / vector[pivot]
        vector = {row: inverse * value for row, value in vector.items()}
        representation = {
            index: inverse * value for index, value in representation.items()
        }
        basis_vectors[pivot] = vector
        basis_representations[pivot] = representation
        picked_metadata.append(metadata)

    remainder, representation = reduce(target, {})
    require(not remainder, ("order-five repair has rational remainder",
                            remainder))
    solution = {
        local_index: -coefficient
        for local_index, coefficient in representation.items()
        if coefficient
    }

    reconstruction = defaultdict(Q)
    for local_index, coefficient in solution.items():
        _metadata, column = all_columns[picked[local_index]]
        for row, value in column.items():
            reconstruction[row] += coefficient * value
    require(all(reconstruction.get(row, Q(0)) == target.get(row, Q(0))
                for row in set(reconstruction) | set(target)),
            "exact order-five reconstruction failed")
    return solution, picked_metadata


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(expected == "TO_BE_HASHED" or actual == expected,
                ("pinned dependency changed", relative, actual))
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "order5_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "order5_base",
    )
    system = build_system(base, commutator)
    require(system["fourth_defect_supports"] == [60, 96, 60],
            "fourth-order pair-generator defect changed")
    require(len(system["variables"]) == 40
            and len(system["columns"]) == 31_008
            and len(system["row_keys"]) == 1_080
            and len(system["ideal_columns"]) == 12,
            "order-five system census changed")

    # The fourth symbol kills both generators; every fifth derivative does
    # so by degree.  Hence the repair leaves the principal -delta symbol.
    require(not apply_fourth(commutator, system["generators"][0])
            and not apply_fourth(commutator, system["generators"][1]),
            "fourth commutator stopped killing its two generators")
    require(all(not derivatives(generator, metadata[1])
                for metadata in system["columns"]
                for generator in system["generators"]),
            "an order-five direction acted on a quartic generator")

    picked = select_modular_basis(system["all_columns"])
    require(len(picked) == 706, "order-five source rank changed")
    solution, metadata = exact_solution(
        system["all_columns"], picked, system["target"]
    )
    ideal_terms = sum(metadata[index][0] == "ideal" for index in solution)
    operator_terms = len(solution) - ideal_terms
    require(operator_terms == 248 and ideal_terms == 0,
            "canonical exact repair sparsity changed")
    denominators = sorted({coefficient.denominator
                           for coefficient in solution.values()})
    require(denominators == [1, 2, 3, 4, 6, 12, 127, 254, 508, 1016],
            "canonical repair denominators changed")

    encoded_solution = [
        [str(solution[index]), repr(metadata[index])]
        for index in sorted(solution)
    ]
    solution_digest = sha256(json.dumps(
        encoded_solution, separators=(",", ":")
    ).encode()).hexdigest()
    ledger = {
        "theorem": "residual-q order-five generator-level source repair",
        "source_words": ["11111111", "11211211"],
        "complete_row_terms_each": 90,
        "fourth_operator": {
            "corner_coefficients": [-1, 1, 1, -1],
            "on_generators": [0, 0],
            "pair_generator_defect_supports":
                system["fourth_defect_supports"],
            "first_surviving_symbol": "-delta",
        },
        "linear_coefficient_order5_system": {
            "ring_variables": len(system["variables"]),
            "candidate_operator_columns": len(system["columns"]),
            "literal_coordinates": len(system["row_keys"]),
            "source_word_blocks": len(system["word_blocks"]),
            "audited_ideal_columns": len(system["ideal_columns"]),
            "exact_rank": len(picked),
            "augmented_rank": len(picked),
        },
        "canonical_exact_repair": {
            "nonzero_order5_terms": operator_terms,
            "source_ideal_columns_used": ideal_terms,
            "denominators": denominators,
            "maximum_absolute_numerator": max(
                abs(coefficient.numerator) for coefficient in solution.values()
            ),
            "solution_sha256": solution_digest,
        },
        "exact_identities": {
            "D(A0)": 0,
            "D(A1)": 0,
            "D(A0^2)": 0,
            "D(A0*A1)": 0,
            "D(A1^2)": 0,
            "D": "D4 + linear-coefficient D5",
        },
        "consequence": (
            "the covariance-curvature fourth symbol admits a complete "
            "generator-level lower-face repair on the two selected source "
            "rows; the private source-boundary obstruction is not a "
            "generator-level impossibility"
        ),
        "scope": (
            "exact R-linear/generator-level two-row Hasse repair only; does "
            "not prove the coefficient-prolonging condition D(I^2) subset I "
            "for arbitrary polynomial multipliers, does not identify the "
            "248-term correction with the physical repeated-grade relative "
            "source image, and does not supply eta/sigma or rank landing"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    system = ledger["linear_coefficient_order5_system"]
    repair = ledger["canonical_exact_repair"]
    print("h=3 residual-q order-five generator repair: CONSTRUCTED")
    print("system rank/augmented rank:", system["exact_rank"], "/",
          system["augmented_rank"])
    print("exact repair terms:", repair["nonzero_order5_terms"])
    print("pair-generator residuals after repair: 0 / 0 / 0")
    print("physical eta/sigma comparison: still required")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
