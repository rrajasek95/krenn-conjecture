#!/usr/bin/env python3
"""Exact Laurent reduction of sparse mixed coefficient fibers.

Binomial zero fibers give ``x^d=-1``.  When their exponent lattice has a
unimodular coordinate minor, every monomial has an exact canonical Laurent
normal form, including its forced sign.  Reducing an arbitrary mixed fiber
can then yield

* one nonzero Laurent class, an immediate contradiction; or
* two classes, hence a power relation ``x^e=r`` with ``r in Q^*``.

The latter relations are row-reduced over Q with provenance.  Any exact
integer dependency among their exponent vectors must have scalar product
one.  A different rational product (for example ``1=2^k`` or ``1=-1``) is
a sound multiplicative contradiction.

This module is a reusable checker.  It trusts neither a floating-point
solver nor a saturated lattice: the unimodular minor, every normal form,
every exponent dependency, and the final rational scalar are audited with
exact Python/SymPy arithmetic.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from fractions import Fraction

import sympy as sp

import search_f5_support_sat as base
import verify_f3_toric_obstruction as toric


@dataclass(frozen=True)
class PowerRelation:
    exponent: tuple[int, ...]
    value: Fraction
    coloring: tuple[int, ...]
    supported: tuple[int, ...]
    class_sums: tuple[int, int]


@dataclass(frozen=True)
class LaurentConflict:
    kind: str
    used_fibers: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
    coloring: tuple[int, ...] | None
    class_sums: tuple[int, ...] | None
    power_relations: tuple[PowerRelation, ...]
    coefficients: tuple[int, ...]
    scalar: Fraction


class BinomialQuotient:
    def __init__(self, relations):
        self.relations = tuple(relations)
        if not self.relations:
            raise ValueError("at least one binomial relation is required")
        relation_matrix = sp.Matrix(
            [relation.difference for relation in self.relations]
        )
        _rref, basis_indices = relation_matrix.T.rref()
        self.basis_indices = tuple(basis_indices)
        self.basis = relation_matrix[list(self.basis_indices), :]
        _rref, coordinate_columns = self.basis.rref()
        self.coordinate_columns = tuple(coordinate_columns)
        minor = self.basis[:, list(self.coordinate_columns)]
        if abs(int(minor.det())) != 1:
            raise ValueError("binomial lattice has no selected unimodular minor")
        self.inverse_minor = minor.inv()
        assert all(value.q == 1 for value in self.inverse_minor)
        self.basis_relations = tuple(
            self.relations[index] for index in self.basis_indices
        )

    def coordinates(self, vector):
        row = sp.Matrix(1, len(vector), vector)
        coefficients = row[:, list(self.coordinate_columns)] * self.inverse_minor
        assert all(value.q == 1 for value in coefficients)
        return tuple(int(value) for value in coefficients)

    def reduce(self, vector):
        coordinates = self.coordinates(vector)
        row = sp.Matrix(1, len(vector), vector)
        remainder = row - sp.Matrix(1, len(coordinates), coordinates) * self.basis
        assert all(remainder[0, column] == 0 for column in self.coordinate_columns)
        reconstructed = remainder + sp.Matrix(1, len(coordinates), coordinates) * self.basis
        assert reconstructed == row
        sign = toric.relation_character(self.basis_relations, coordinates)
        return tuple(int(value) for value in remainder), sign, coordinates

    def audit_binomial_character(self):
        for relation in self.relations:
            remainder, sign, _coordinates = self.reduce(relation.difference)
            if any(remainder) or sign != relation.value:
                return relation
        return None


def supported_fibers(pool, model):
    return {
        coloring: tuple(
            index
            for index in range(len(base.MATCHINGS))
            if pool.id(("monomial", coloring, index)) in model
        )
        for coloring in base.COLORINGS
    }


def binomial_relations_from_fibers(signatures, fibers, term_signs=None):
    """Collect exact two-term relations from an explicit fiber dictionary."""
    if term_signs is None:
        term_signs = (1,) * len(base.MATCHINGS)
    term_signs = tuple(term_signs)
    assert len(term_signs) == len(base.MATCHINGS)
    assert all(value in (-1, 1) for value in term_signs)
    by_relation = {}
    for coloring in base.COLORINGS:
        if len(set(coloring)) == 1:
            continue
        supported = tuple(fibers.get(coloring, ()))
        if len(supported) != 2:
            continue
        first, second = supported
        difference = tuple(
            a - b
            for a, b in zip(
                signatures[coloring, first],
                signatures[coloring, second],
                strict=True,
            )
        )
        value = -term_signs[second] * term_signs[first]
        by_relation.setdefault(
            (difference, value),
            toric.BinomialRelation(difference, coloring, supported, value),
        )
    return tuple(by_relation.values())


def reduce_fiber(quotient, exponents, coefficients=None):
    if coefficients is None:
        coefficients = (1,) * len(exponents)
    assert len(coefficients) == len(exponents)
    classes = {}
    reductions = []
    for exponent, coefficient in zip(exponents, coefficients, strict=True):
        remainder, sign, coordinates = quotient.reduce(exponent)
        classes[remainder] = classes.get(remainder, 0) + coefficient * sign
        reductions.append((remainder, sign, coordinates))
    classes = {remainder: value for remainder, value in classes.items() if value}
    return classes, tuple(reductions)


def normalize_power(exponent, value):
    opposite = tuple(-entry for entry in exponent)
    if opposite < exponent:
        return opposite, Fraction(1, 1) / value
    return exponent, value


def multiply_powers(values, coefficients):
    answer = Fraction(1)
    for value, coefficient in zip(values, coefficients, strict=True):
        answer *= value**coefficient
    return answer


def primitive_integer_combination(combo):
    denominators = [value.denominator for value in combo.values() if value]
    multiple = math.lcm(*denominators) if denominators else 1
    integers = {index: int(value * multiple) for index, value in combo.items() if value}
    divisor = math.gcd(*(abs(value) for value in integers.values())) if integers else 1
    integers = {index: value // divisor for index, value in integers.items()}
    if integers and next(iter(integers.values())) < 0:
        integers = {index: -value for index, value in integers.items()}
    return integers


def dependency_conflict(power_relations):
    """Return one exact multiplicative dependency, if inconsistent."""
    pivots = {}
    for index, relation in enumerate(power_relations):
        vector = {
            coordinate: Fraction(value)
            for coordinate, value in enumerate(relation.exponent)
            if value
        }
        combination = {index: Fraction(1)}
        while vector:
            pivot = min(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                inverse = Fraction(1, 1) / coefficient
                vector = {key: value * inverse for key, value in vector.items()}
                combination = {
                    key: value * inverse for key, value in combination.items()
                }
                pivots[pivot] = (vector, combination)
                break
            pivot_vector, pivot_combination = pivots[pivot]
            for key, value in pivot_vector.items():
                updated = vector.get(key, 0) - coefficient * value
                if updated:
                    vector[key] = updated
                else:
                    vector.pop(key, None)
            for key, value in pivot_combination.items():
                updated = combination.get(key, 0) - coefficient * value
                if updated:
                    combination[key] = updated
                else:
                    combination.pop(key, None)
        else:
            integer_combination = primitive_integer_combination(combination)
            if not integer_combination:
                continue
            exact_exponent = [0] * len(relation.exponent)
            for relation_index, coefficient in integer_combination.items():
                for coordinate, value in enumerate(
                    power_relations[relation_index].exponent
                ):
                    exact_exponent[coordinate] += coefficient * value
            assert not any(exact_exponent)
            coefficients = tuple(
                integer_combination.get(position, 0)
                for position in range(len(power_relations))
            )
            scalar = multiply_powers(
                [relation.value for relation in power_relations], coefficients
            )
            if scalar != 1:
                return coefficients, scalar
    return None


def generalized_laurent_conflict_from_fibers(
    signatures, fibers, term_signs=None
):
    """Check explicit exact fiber supports for a Laurent contradiction."""
    if term_signs is None:
        term_signs = (1,) * len(base.MATCHINGS)
    term_signs = tuple(term_signs)
    relations = binomial_relations_from_fibers(
        signatures, fibers, term_signs
    )
    if not relations:
        return None
    try:
        quotient = BinomialQuotient(relations)
    except ValueError:
        return None

    bad_binomial = quotient.audit_binomial_character()
    if bad_binomial is not None:
        used = {relation.coloring: relation.supported for relation in quotient.basis_relations}
        used[bad_binomial.coloring] = bad_binomial.supported
        return LaurentConflict(
            "odd-binomial",
            tuple(sorted(used.items())),
            bad_binomial.coloring,
            None,
            (),
            (),
            Fraction(-1),
        )

    powers = []
    seen_powers = {}
    pending_single = None
    for coloring, supported in fibers.items():
        is_constant = len(set(coloring)) == 1
        if (is_constant and len(supported) < 2) or (
            not is_constant and len(supported) < 3
        ):
            continue
        exponents = [signatures[coloring, index] for index in supported]
        coefficients = [term_signs[index] for index in supported]
        classes, _reductions = reduce_fiber(
            quotient, exponents, coefficients
        )
        if is_constant:
            # The target constant coordinate is nonzero.  If all of its
            # Laurent classes cancel under exact mixed-binomial relations,
            # the chart instead forces that coordinate to vanish.
            if not classes:
                used = {
                    relation.coloring: relation.supported
                    for relation in quotient.basis_relations
                }
                used[coloring] = supported
                return LaurentConflict(
                    "zero-constant-fiber",
                    tuple(sorted(used.items())),
                    coloring,
                    (),
                    (),
                    (),
                    Fraction(0),
                )
            continue
        if len(classes) == 1:
            class_sums = tuple(classes.values())
            if pending_single is None:
                used = {
                    relation.coloring: relation.supported
                    for relation in quotient.basis_relations
                }
                used[coloring] = supported
                pending_single = LaurentConflict(
                    "single-laurent-class",
                    tuple(sorted(used.items())),
                    coloring,
                    class_sums,
                    (),
                    (),
                    Fraction(class_sums[0]),
                )
            continue
        if len(classes) != 2:
            continue
        ordered = sorted(classes.items())
        (first_exponent, first_coefficient), (second_exponent, second_coefficient) = ordered
        exponent = tuple(
            second - first
            for first, second in zip(first_exponent, second_exponent, strict=True)
        )
        value = Fraction(-first_coefficient, second_coefficient)
        exponent, value = normalize_power(exponent, value)
        power = PowerRelation(
            exponent,
            value,
            coloring,
            supported,
            (first_coefficient, second_coefficient),
        )
        key = exponent
        if key in seen_powers and seen_powers[key].value != value:
            other = seen_powers[key]
            used = {relation.coloring: relation.supported for relation in quotient.basis_relations}
            used[other.coloring] = other.supported
            used[coloring] = supported
            return LaurentConflict(
                "equal-exponent-values",
                tuple(sorted(used.items())),
                coloring,
                None,
                (other, power),
                (1, -1),
                other.value / value,
            )
        seen_powers.setdefault(key, power)

    powers = tuple(seen_powers.values())
    dependency = dependency_conflict(powers)
    if dependency is None:
        return pending_single
    coefficients, scalar = dependency
    used = {relation.coloring: relation.supported for relation in quotient.basis_relations}
    selected_powers = []
    selected_coefficients = []
    for power, coefficient in zip(powers, coefficients, strict=True):
        if not coefficient:
            continue
        used[power.coloring] = power.supported
        selected_powers.append(power)
        selected_coefficients.append(coefficient)
    # Independent final audit.
    exact_exponent = [0] * len(selected_powers[0].exponent)
    for power, coefficient in zip(selected_powers, selected_coefficients, strict=True):
        for coordinate, value in enumerate(power.exponent):
            exact_exponent[coordinate] += coefficient * value
    assert not any(exact_exponent)
    assert multiply_powers(
        [power.value for power in selected_powers], selected_coefficients
    ) == scalar != 1
    return LaurentConflict(
        "multiplicative-power",
        tuple(sorted(used.items())),
        None,
        None,
        tuple(selected_powers),
        tuple(selected_coefficients),
        scalar,
    )


def generalized_laurent_conflict(
    pool, signatures, model, term_signs=None
):
    """Compatibility wrapper for the SAT support-model audit."""
    return generalized_laurent_conflict_from_fibers(
        signatures, supported_fibers(pool, model), term_signs
    )


def synthetic_audit():
    """Dependency engine audit: x^u=-2 and x^(2u)=2 are inconsistent."""
    first = PowerRelation((1, 0), Fraction(-2), (0,) * 6, (0, 1, 2), (1, 2))
    second = PowerRelation((2, 0), Fraction(2), (1,) * 6, (0, 1, 2), (1, -2))
    result = dependency_conflict((first, second))
    assert result is not None
    coefficients, scalar = result
    assert not any(
        sum(
            coefficient * relation.exponent[coordinate]
            for relation, coefficient in zip((first, second), coefficients, strict=True)
        )
        for coordinate in range(2)
    )
    assert scalar != 1
    print(
        f"verified generalized Laurent dependency: coefficients={coefficients}, "
        f"scalar={scalar}"
    )


if __name__ == "__main__":
    synthetic_audit()
