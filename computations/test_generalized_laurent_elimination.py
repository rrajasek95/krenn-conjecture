#!/usr/bin/env python3
"""Adversarial exact tests for generalized Laurent elimination.

The tests use explicit synthetic fibers, not the support SAT encoding.  They
exercise extraction of rational power relations, compatible and incompatible
dependencies, sign-character inconsistencies, equal exponents with unequal
values, a nonprimitive lattice that must be declined, and unimodular changes
of ambient exponent coordinates.
"""

from __future__ import annotations

import random
from fractions import Fraction

import generalized_laurent_elimination as laurent
import search_f5_support_sat as base


MIXED = tuple(coloring for coloring in base.COLORINGS if len(set(coloring)) > 1)


def explicit_data(exponent_fibers):
    fibers = {}
    signatures = {}
    for coloring, exponents in exponent_fibers:
        assert coloring not in fibers
        assert len(exponents) <= len(base.MATCHINGS)
        fibers[coloring] = tuple(range(len(exponents)))
        for index, exponent in enumerate(exponents):
            signatures[coloring, index] = tuple(exponent)
    return signatures, fibers


def transform(exponent, shear):
    # Row-vector action by a determinant-one integral shear.
    first, second = exponent
    return first, shear * first + second


def inconsistent_power_fibers(shear=0):
    # x=-1; then 1+x^2+y=0 gives y=-2, while
    # x+x^3+y^2=0 gives y^2=2.  These force 4=2.
    raw = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 0), (2, 0), (0, 1))),
        (MIXED[2], ((1, 0), (3, 0), (0, 2))),
    )
    return tuple(
        (coloring, tuple(transform(exponent, shear) for exponent in exponents))
        for coloring, exponents in raw
    )


def test_power_dependency_from_fibers():
    signatures, fibers = explicit_data(inconsistent_power_fibers())
    answer = laurent.generalized_laurent_conflict_from_fibers(signatures, fibers)
    assert answer is not None
    assert answer.kind == "multiplicative-power"
    assert len(answer.power_relations) == 2
    # Lexicographic exponent normalization reverses both powers here.
    assert {relation.value for relation in answer.power_relations} == {
        Fraction(-1, 2),
        Fraction(1, 2),
    }
    assert answer.scalar != 1


def test_compatible_power_dependency_is_retained():
    # x=-1; the first mixed fiber gives y=-2.  Four negative x-odd
    # terms and y^2 give y^2=4, exactly the compatible square relation.
    signatures, fibers = explicit_data(
        (
            (MIXED[0], ((1, 0), (0, 0))),
            (MIXED[1], ((0, 0), (2, 0), (0, 1))),
            (
                MIXED[2],
                ((1, 0), (3, 0), (5, 0), (7, 0), (0, 2)),
            ),
        )
    )
    assert (
        laurent.generalized_laurent_conflict_from_fibers(signatures, fibers)
        is None
    )


def test_equal_exponent_unequal_values():
    # Two fibers independently demand y=-2 and y=-3.
    signatures, fibers = explicit_data(
        (
            (MIXED[0], ((1, 0), (0, 0))),
            (MIXED[1], ((0, 0), (2, 0), (0, 1))),
            (MIXED[2], ((0, 0), (2, 0), (4, 0), (0, 1))),
        )
    )
    answer = laurent.generalized_laurent_conflict_from_fibers(signatures, fibers)
    assert answer is not None
    assert answer.kind == "equal-exponent-values"
    assert answer.scalar != 1


def test_single_surviving_class():
    # x=y=-1 makes 1+x+y=-1, not zero.
    signatures, fibers = explicit_data(
        (
            (MIXED[0], ((1, 0), (0, 0))),
            (MIXED[1], ((0, 1), (0, 0))),
            (MIXED[2], ((0, 0), (1, 0), (0, 1))),
        )
    )
    answer = laurent.generalized_laurent_conflict_from_fibers(signatures, fibers)
    assert answer is not None
    assert answer.kind == "single-laurent-class"
    assert answer.class_sums == (-1,)


def test_redundant_sign_character_conflict():
    # x=-1 and y=-1 imply xy=+1, contradicting a third fiber xy=-1.
    signatures, fibers = explicit_data(
        (
            (MIXED[0], ((1, 0), (0, 0))),
            (MIXED[1], ((0, 1), (0, 0))),
            (MIXED[2], ((1, 1), (0, 0))),
        )
    )
    answer = laurent.generalized_laurent_conflict_from_fibers(signatures, fibers)
    assert answer is not None
    assert answer.kind == "odd-binomial"


def test_nonprimitive_lattice_is_declined():
    # The quotient routine must not replace <(2,0)> by its saturation <(1,0)>.
    signatures, fibers = explicit_data(
        (
            (MIXED[0], ((2, 0), (0, 0))),
            (MIXED[1], ((0, 0), (1, 0), (0, 1))),
        )
    )
    assert (
        laurent.generalized_laurent_conflict_from_fibers(signatures, fibers)
        is None
    )


def test_random_unimodular_coordinate_changes():
    rng = random.Random(20260724)
    for _trial in range(40):
        signatures, fibers = explicit_data(
            inconsistent_power_fibers(rng.randint(-20, 20))
        )
        answer = laurent.generalized_laurent_conflict_from_fibers(
            signatures, fibers
        )
        assert answer is not None
        assert answer.kind == "multiplicative-power"
        assert answer.scalar != 1


def main() -> None:
    tests = sorted(
        (
            (name, value)
            for name, value in globals().items()
            if name.startswith("test_") and callable(value)
        ),
        key=lambda item: item[0],
    )
    for name, test in tests:
        test()
        print(f"PASS {name}")
    print(f"generalized Laurent adversarial audit passed ({len(tests)} tests)")


if __name__ == "__main__":
    main()
