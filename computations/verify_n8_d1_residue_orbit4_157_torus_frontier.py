#!/usr/bin/env python3
"""Freeze the first torus-consistent two-class O4 coefficient frontier."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_DIRECT_BATCH_SHA256 = (
    "8bed466723fe37da34136f4c10f5d49e866984effddcb69b56dbdf0bbde6335e"
)
SOURCE = os.path.join(HERE,
                      "verify_n8_d1_residue_orbit4_158_direct_batch.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_DIRECT_BATCH_SHA256,
            "the pinned O4 Laurent source changed")
B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
E, Q, C, D = B.E, B.Q, B.C, B.D

MISSING = (
    (0, 1, 1, 0), (0, 3, 0, 1),
    (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
    (0, 7, 0, 1), (0, 7, 0, 2),
    (1, 2, 1, 0), (1, 3, 1, 0), (1, 3, 1, 2),
    (1, 4, 0, 1), (1, 4, 1, 0),
    (1, 5, 0, 1), (1, 5, 1, 0),
    (1, 6, 0, 1), (1, 6, 1, 0),
    (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
    (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
    (2, 6, 2, 0), (2, 6, 2, 1),
    (2, 7, 1, 0), (2, 7, 1, 2), (2, 7, 2, 0),
    (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
    (3, 7, 2, 0), (3, 7, 2, 1),
)
GENERATOR_SHA256 = (
    "00839fab040697522574a57f3529eb2968247eaa0b2ab49d2eadaf4795cf17d4"
)
INITIAL_HISTOGRAM_SHA256 = (
    "27c569af5b7a8b09e79fa1b17943d44728b40a71aa47df9f5d579dc448b085ff"
)
FINAL_HISTOGRAM_SHA256 = (
    "5f7c3104e03a67a358bfb2074847cae34c96ccb768d43e849c8a7743d35d3390"
)
DERIVED_RECORDS = (
    114,
    2228, 2229, 2230, 2234, 2235, 2236, 2240, 2241, 2242,
    2799, 2802, 2805, 2871, 2874, 2877, 2943, 2946, 2949,
)
EXPECTED_LEDGER_SHA256 = (
    "55572b97ff5a8bb421d81a9c8e32e1a29f2308e19602ea217ff48d56ccf77360"
)


def rational_power(value, exponent):
    require(exponent.denominator == 1,
            "a torus parameter exponent is not integral")
    integer = exponent.numerator
    return value ** integer if integer >= 0 else Fraction(1, value ** -integer)


def complete_parametrization(basis, rows):
    """Solve the unit-pivot echelon character basis in free torus variables."""
    pivots = set(basis)
    resolved = {}
    for pivot in reversed(sorted(basis)):
        basis_row, representation = basis[pivot]
        require(basis_row[pivot] == 1,
                "the character lattice has a nonunit pivot")
        coefficient = E.row_character(representation, rows)
        exponents = Counter()
        for name, value in basis_row.items():
            if name != pivot:
                exponents[name] -= value
        for name in sorted(tuple(exponents), reverse=True):
            power = exponents.pop(name)
            if name not in pivots:
                exponents[name] += power
                continue
            require(name in resolved,
                    "the echelon parametrization is not triangular")
            substitution_coefficient, substitution_exponent = resolved[name]
            coefficient *= rational_power(substitution_coefficient, power)
            for free_name, free_power in substitution_exponent.items():
                exponents[free_name] += power * free_power
                if not exponents[free_name]:
                    exponents.pop(free_name)
        require(not (set(exponents) & pivots),
                "a solved pivot still depends on a pivot")
        resolved[pivot] = (coefficient, dict(exponents))

    # Substitute into every character equation independently.
    for pivot, (basis_row, representation) in basis.items():
        coefficient = Fraction(1)
        exponents = Counter()
        for name, power in basis_row.items():
            if name in resolved:
                sub_coefficient, sub_exponent = resolved[name]
                coefficient *= rational_power(sub_coefficient, power)
                for free_name, free_power in sub_exponent.items():
                    exponents[free_name] += power * free_power
            else:
                exponents[name] += power
        require(not {name: value for name, value in exponents.items() if value}
                and coefficient == E.row_character(representation, rows),
                "the explicit torus parametrization failed substitution")
    return [[
        pivot,
        str(resolved[pivot][0]),
        [[name, exponent.numerator]
         for name, exponent in sorted(resolved[pivot][1].items())],
    ] for pivot in sorted(resolved)]


def frontier_input():
    support = Q.allowed_support() - set(MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 157 and len(records) == 4321
            and D.content_hash(records) == GENERATOR_SHA256,
            "the torus-consistent 157-cell input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 72 and len(basis) == 25
            and len(dependencies) == 47
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the torus frontier initial character changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    seen = {E.canonical_row(row["difference"], row["constant"])
            for row in rows}
    derived = []
    initial_histogram = Counter()
    for record_index, record in enumerate(records):
        reduced, _traces, _parents = E.reduce_record(
            record, basis, basis_characters
        )
        initial_histogram[len(reduced)] += 1
        if len(reduced) != 2:
            continue
        (first, first_coefficient), (second, second_coefficient) = sorted(
            reduced.items()
        )
        difference = E.exponent_difference(first, second)
        constant = -second_coefficient / first_coefficient
        key = E.canonical_row(difference, constant)
        if key in seen:
            continue
        seen.add(key)
        derived.append({
            "difference": difference,
            "constant": constant,
            "source_record": record_index,
        })
    require(D.content_hash({str(classes): count for classes, count
                            in sorted(initial_histogram.items())})
            == INITIAL_HISTOGRAM_SHA256
            and tuple(row["source_record"] for row in derived)
                == DERIVED_RECORDS
            and all(row["constant"] == 1 for row in derived),
            "the torus frontier two-class rows changed")

    augmented = rows + derived
    augmented_basis, augmented_dependencies = E.L.integer_laurent_basis(
        augmented
    )
    require(len(augmented) == 91 and len(augmented_basis) == 36
            and len(augmented_dependencies) == 55
            and all(E.row_character(dependency, augmented) == 1
                    for dependency in augmented_dependencies),
            "the full two-class character system stopped being consistent")
    parametrization = complete_parametrization(augmented_basis, augmented)
    support_names = {"x_%d%d_%d%d" % cell for cell in support}
    pivot_names = set(augmented_basis)
    free_parameters = sorted(support_names - pivot_names)
    require(len(parametrization) == 36 and len(free_parameters) == 121,
            "the torus dimension changed")

    augmented_characters = {
        pivot: E.row_character(representation, augmented)
        for pivot, (_basis_row, representation) in augmented_basis.items()
    }
    final_histogram = Counter()
    terminal = None
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(
            record, augmented_basis, augmented_characters
        )
        final_histogram[len(reduced)] += 1
        if record_index == 343:
            terminal = {
                "source_record": record_index,
                "classes": len(reduced),
                "normal_form": E.polynomial_trace(reduced),
                "parents": sorted(parents),
                "trace_sha256": D.content_hash(traces),
            }
    require(D.content_hash({str(classes): count for classes, count
                            in sorted(final_histogram.items())})
            == FINAL_HISTOGRAM_SHA256,
            "the residual class histogram changed")
    require(terminal == {
        "source_record": 343,
        "classes": 3,
        "normal_form": [
            [[
                ["x_02_01", 1], ["x_13_01", 1], ["x_23_11", -1],
                ["x_27_01", 1], ["x_34_01", 1], ["x_56_21", 1],
                ["x_57_12", 1], ["x_57_22", -1],
            ], "1"],
            [[
                ["x_02_01", 1], ["x_13_01", 1], ["x_23_11", -1],
                ["x_27_01", 1], ["x_35_01", 1], ["x_47_12", 1],
                ["x_56_21", 1], ["x_57_22", -1],
            ], "-1"],
            [[
                ["x_02_01", 1], ["x_13_01", 1], ["x_23_11", -1],
                ["x_27_01", 1], ["x_36_01", 1], ["x_45_11", 1],
            ], "1"],
        ],
        "parents": [0, 1, 2, 3, 4, 5, 6, 9, 18, 20, 22, 24, 72],
        "trace_sha256":
            "9bc92a3630ad7e26995df44554ffc23038cb0fde3b0d21d4f0087890a91ca32a",
    }, "the selected three-class residual changed")
    return (support, records, rows, augmented, augmented_basis,
            augmented_dependencies, parametrization, free_parameters,
            terminal)


def audit():
    started = monotonic()
    (support, records, rows, augmented, augmented_basis,
     augmented_dependencies, parametrization, free_parameters,
     terminal) = frontier_input()
    ledger = {
        "pinned_direct_batch_sha256": PINNED_DIRECT_BATCH_SHA256,
        "missing_cells": [list(cell) for cell in MISSING],
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "initial_character": {
            "rows": len(rows), "rank": 25, "dependencies": 47,
        },
        "two_class_character": {
            "rows": len(augmented), "rank": len(augmented_basis),
            "dependencies": len(augmented_dependencies),
            "inconsistent_dependencies": 0,
        },
        "free_torus_parameters": free_parameters,
        "pivot_parametrization": parametrization,
        "residual_histogram_sha256": FINAL_HISTOGRAM_SHA256,
        "selected_three_class_residual": terminal,
        "status": (
            "first exact O4 frontier whose complete one/two-class character "
            "system is torus-consistent; higher-class equations remain open"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the 157-cell torus-frontier ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("two-class torus rank / dimension: %d / %d" % (
        ledger["two_class_character"]["rank"],
        len(ledger["free_torus_parameters"]),
    ))
    print("selected residual classes:", ledger[
        "selected_three_class_residual"
    ]["classes"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()
