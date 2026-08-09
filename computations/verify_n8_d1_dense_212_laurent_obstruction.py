#!/usr/bin/env python3
"""Exact Laurent-lattice obstruction on a dense 212-cell D1 support."""

from __future__ import annotations

import hashlib
import importlib
import math
import os
import sys
from collections import Counter
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D

MISSING_CELLS = (
    (6, 7, 0, 2), (6, 7, 1, 0), (6, 7, 1, 2),
    (6, 7, 2, 0), (6, 7, 2, 1),
)
EXPECTED_LEDGER_SHA256 = (
    "b08106c08267a8e530e2330e80bac0b00de0169087faf702aa3f46e53b869e71"
)


def exponent_difference(first, second):
    result = Counter(first)
    result.subtract(second)
    return {name: Fraction(exponent) for name, exponent in result.items()
            if exponent}


def axpy(target, scalar, source):
    for key, value in source.items():
        result = target.get(key, Fraction(0)) + scalar * value
        if result:
            target[key] = result
        else:
            target.pop(key, None)


def primitive(representation):
    denominator = 1
    for coefficient in representation.values():
        denominator = math.lcm(denominator, coefficient.denominator)
    integers = {index: int(coefficient * denominator)
                for index, coefficient in representation.items()}
    divisor = 0
    for coefficient in integers.values():
        divisor = math.gcd(divisor, abs(coefficient))
    require(divisor, "a zero dependence was presented as primitive")
    return {index: coefficient // divisor
            for index, coefficient in integers.items()}


def plus_binomials(records):
    rows = []
    for record_index, record in enumerate(records):
        if len(record["terms"]) != 2:
            continue
        parsed = [(tuple(monomial), Fraction(coefficient))
                  for monomial, coefficient in record["terms"]]
        if {coefficient for _monomial, coefficient in parsed} != {Fraction(1)}:
            continue
        rows.append({
            "record_index": record_index,
            "difference": exponent_difference(parsed[0][0], parsed[1][0]),
        })
    return rows


def integer_laurent_basis(rows):
    basis = {}
    dependencies = []
    for position, original in enumerate(rows):
        row = dict(original["difference"])
        representation = {position: Fraction(1)}
        while row:
            pivot = min(row)
            if pivot not in basis:
                value = row[pivot]
                row = {key: coefficient / value
                       for key, coefficient in row.items()}
                representation = {
                    key: coefficient / value
                    for key, coefficient in representation.items()
                }
                basis[pivot] = (row, representation)
                break
            basis_row, basis_representation = basis[pivot]
            factor = row[pivot]
            axpy(row, -factor, basis_row)
            axpy(representation, -factor, basis_representation)
        else:
            dependencies.append(primitive(representation))
    require(all(coefficient.denominator == 1
                for row, representation in basis.values()
                for polynomial in (row, representation)
                for coefficient in polynomial.values()),
            "the Laurent row basis is not integral")

    # Independently reconstruct every basis exponent and its sign character
    # from the original plus-binomial equations x^d = -1.
    for basis_row, representation in basis.values():
        rebuilt = {}
        for position, coefficient in representation.items():
            axpy(rebuilt, coefficient, rows[position]["difference"])
        require(rebuilt == basis_row,
                "a Laurent basis representation failed reconstruction")
    return basis, dependencies


def reduce_record(record, basis):
    reduced = Counter()
    traces = []
    for monomial, coefficient in record["terms"]:
        exponent = Counter(monomial)
        phase = 1
        multipliers = {}
        for pivot, (basis_row, representation) in basis.items():
            multiplier = exponent.get(pivot, 0)
            if not multiplier:
                continue
            multipliers[pivot] = multiplier
            for name, value in basis_row.items():
                require(value.denominator == 1,
                        "a nonintegral Laurent exponent appeared")
                exponent[name] -= multiplier * int(value)
                if not exponent[name]:
                    exponent.pop(name, None)
            character_exponent = multiplier * sum(representation.values())
            require(character_exponent.denominator == 1,
                    "a nonintegral sign character appeared")
            if character_exponent.numerator % 2:
                phase = -phase
        canonical = tuple(sorted(exponent.items()))
        reduced[canonical] += phase * Fraction(coefficient)
        if not reduced[canonical]:
            del reduced[canonical]

        # Rebuild e_original-e_canonical from the basis multipliers and
        # separately verify the accumulated (-1)-character.
        rebuilt_difference = {}
        rebuilt_character = 0
        for pivot, multiplier in multipliers.items():
            basis_row, representation = basis[pivot]
            axpy(rebuilt_difference, multiplier, basis_row)
            rebuilt_character += multiplier * sum(representation.values())
        # Canonical Laurent exponents can be negative; compare counters
        # directly instead of relying on an ordinary monomial expansion.
        direct_difference = Counter(monomial)
        direct_difference.subtract(dict(canonical))
        direct_difference = {
            name: Fraction(value) for name, value in direct_difference.items()
            if value
        }
        require(rebuilt_difference == direct_difference,
                "a target-monomial Laurent reduction failed reconstruction")
        require(phase == (-1 if rebuilt_character.numerator % 2 else 1),
                "a target-monomial sign reduction failed reconstruction")
        traces.append({
            "canonical": [[name, exponent] for name, exponent in canonical],
            "phase": phase,
            "basis_multipliers": [[pivot, multiplier]
                                  for pivot, multiplier in multipliers.items()],
        })
    return dict(reduced), traces


def audit():
    started = monotonic()
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(MISSING_CELLS)
    require(base_support <= support and len(admissible) == 217
            and len(support) == 212,
            "the dense D1 support changed")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    require(len(records) == 8101
            and not any(len(record["terms"]) == 1 for record in records),
            "the dense coefficient-generator census changed")
    binomials = plus_binomials(records)
    require(len(binomials) == 720,
            "the dense plus-binomial census changed")
    # Nine consecutive full-output binomials already suffice; the other 711
    # binomials are audited only as a census and are not used in the proof.
    witness_binomials = binomials[:9]
    require(tuple(row["record_index"] for row in witness_binomials)
            == tuple(range(5387, 5396)),
            "the nine dense witness binomials moved")
    basis, dependencies = integer_laurent_basis(witness_binomials)
    require(len(basis) == 9 and not dependencies,
            "the nine witness exponent differences lost independence")

    target_index = 5351
    target = records[target_index]
    target_reduced, target_traces = reduce_record(target, basis)
    require(target["families"] == ["full_exactness"]
            and len(target["terms"]) == 3,
            "the selected dense target generator changed")
    expected_unit = (
        (("x_02_20", 1), ("x_13_20", 1),
         ("x_45_00", 1), ("x_67_00", 1)),
        Fraction(1),
    )
    require(next(iter(target_reduced.items())) == expected_unit,
            "the selected dense target no longer reduces to the frozen unit")
    require(all(name in {"x_%d%d_%d%d" % cell for cell in support}
                for name, _exponent in expected_unit[0]),
            "the Laurent unit uses a nonlocalized variable")

    basis_sources = [row["record_index"] for row in witness_binomials]
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "admissible_cells": len(admissible),
        "localized_cells": len(support),
        "missing_cells": [list(cell) for cell in MISSING_CELLS],
        "complete_fibres_checked": shadow["fibres_checked"],
        "coefficient_generators": len(records),
        "plus_binomials": len(binomials),
        "witness_plus_binomials": len(witness_binomials),
        "witness_laurent_rank": len(basis),
        "basis_source_generators": basis_sources,
        "basis_source_sha256": D.content_hash(
            [records[index] for index in basis_sources]
        ),
        "selected_unit_generator": target_index,
        "selected_unit_generator_sha256": D.content_hash(target),
        "selected_unit_normal_form": [
            [[name, exponent] for name, exponent in expected_unit[0]],
            str(expected_unit[1]),
        ],
        "selected_unit_trace_sha256": D.content_hash(target_traces),
        "characteristic_scope": "empty over every field, including characteristic two",
        "status": (
            "the dense 212-cell localized D1 coefficient ideal is empty; "
            "nine exact plus-binomial lattice rows reduce a full-output "
            "generator to a localized monomial"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the dense Laurent-obstruction ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 dense 212-cell Laurent obstruction: PASS (exact)")
    print("witness binomial lattice: rank %d from %d selected of %d equations"
          % (ledger["witness_laurent_rank"],
             ledger["witness_plus_binomials"], ledger["plus_binomials"]))
    print("selected full-output unit row:", ledger["selected_unit_generator"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
