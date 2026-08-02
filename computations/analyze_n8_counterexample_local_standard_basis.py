#!/usr/bin/env python3
"""Experimental automatic m-adic normal form at the n=8 mixed torus.

This propagates literal mixed-equation corrections degree by degree.  It is
an analyzer until a stable stopping order and frozen ledger are selected.
"""

from collections import defaultdict
from fractions import Fraction
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_counterexample_local_mod_m5_membership.py"
SPEC = importlib.util.spec_from_file_location("n8_mod_m5", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)

CUBIC = SOURCE.CUBIC
FACTOR = SOURCE.FACTOR
SECOND = SOURCE.SECOND
THIRD = SOURCE.THIRD
FOURTH = SOURCE.FOURTH
QQ = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial_degree(polynomial):
    degrees = {len(monomial) for monomial in polynomial}
    require(len(degrees) <= 1, "multiplier is not homogeneous")
    return next(iter(degrees), 0)


class LocalReducer:
    def __init__(self):
        self.rows = CUBIC.mixed_rows()
        self.jacobian_pivots = CUBIC.echelon_with_representatives(self.rows)
        CUBIC.reconstruct_echelon_rows(self.rows, self.jacobian_pivots)
        self.data = SOURCE.obstruction_data()
        self.simple_obstructions = {
            pivot: row for pivot, (row, _representative)
            in self.data["obstruction_pivots"].items()
        }
        self.free_columns = self.data["free_columns"]
        self.free_position = {
            coordinate: position
            for position, coordinate in enumerate(self.free_columns)
        }
        self._functional_hasse_cache = {}
        self._jacobian_functionals = {}
        self._obstruction_functionals = {}
        self.corrections = []

    def jacobian_functional(self, pivot):
        if pivot not in self._jacobian_functionals:
            functional = {}
            for row_index, coefficient in self.jacobian_pivots[pivot][1].items():
                word = self.rows[row_index][0]
                functional[THIRD.MIXED_WORD_INDEX[word]] = coefficient
            self._jacobian_functionals[pivot] = functional
        return self._jacobian_functionals[pivot]

    def obstruction_functional(self, pivot):
        if pivot not in self._obstruction_functionals:
            row, representative = self.data["obstruction_pivots"][pivot]
            functional = SOURCE.literal_cokernel_lift(
                representative, self.data
            )
            quadratic = self.functional_hasse(functional, 2)
            require(
                CUBIC.tangent_restriction(
                    quadratic, self.data["tangent_basis"]
                ) == row,
                "literal obstruction lift lost its tangent leading form",
            )
            self._obstruction_functionals[pivot] = functional
        return self._obstruction_functionals[pivot]

    def functional_hasse(self, functional, degree):
        key = tuple(sorted(functional.items())), degree
        if key not in self._functional_hasse_cache:
            self._functional_hasse_cache[key] = (
                SOURCE.represented_literal_hasse(functional, degree)
                if 0 <= degree <= 4 else {}
            )
        return self._functional_hasse_cache[key]

    def add_correction(self, multiplier, functional, kind):
        require(multiplier, "zero multiplier correction")
        self.corrections.append({
            "multiplier": dict(multiplier),
            "degree": polynomial_degree(multiplier),
            "functional": dict(functional),
            "kind": kind,
        })

    def residual(self, pure_word, degree):
        answer = CUBIC.hasse_form(pure_word, degree) if degree <= 4 else {}
        for correction in self.corrections:
            equation_degree = degree - correction["degree"]
            if not 0 <= equation_degree <= 4:
                continue
            equation_part = self.functional_hasse(
                correction["functional"], equation_degree
            )
            CUBIC.add_scaled(
                answer,
                CUBIC.multiply_polynomials(
                    correction["multiplier"], equation_part
                ),
                -1,
            )
        return answer

    def normal_reduce(self, polynomial, degree, stage):
        quotients, remainder, steps = (
            SOURCE.fast_divide_by_echelon_linear_forms(
                polynomial, self.jacobian_pivots
            )
        )
        replay = CUBIC.reconstruct_division(
            quotients, self.jacobian_pivots
        )
        CUBIC.add_scaled(replay, remainder)
        require(replay == polynomial, f"degree {degree} {stage}: replay")
        for pivot, multiplier in quotients.items():
            self.add_correction(
                multiplier, self.jacobian_functional(pivot),
                f"degree_{degree}_{stage}_normal",
            )
        return remainder, len(quotients), sum(map(len, quotients.values())), steps

    def tangent_polynomial(self, ambient_free_polynomial):
        return {
            tuple(sorted(self.free_position[index] for index in monomial)):
            coefficient
            for monomial, coefficient in ambient_free_polynomial.items()
        }

    def ambient_free_polynomial(self, tangent_polynomial):
        return {
            tuple(sorted(self.free_columns[index] for index in monomial)):
            coefficient
            for monomial, coefficient in tangent_polynomial.items()
        }

    def reduce_degree(self, pure_word, degree):
        incoming = self.residual(pure_word, degree)
        first_remainder, nf1, nt1, ns1 = self.normal_reduce(
            incoming, degree, "first"
        )
        tangent = self.tangent_polynomial(first_remainder)
        obstruction_quotients, obstruction_remainder, obstruction_steps = (
            FOURTH.reduce_by_quadratic_obstructions(
                tangent, self.simple_obstructions
            )
        )
        if obstruction_remainder:
            return {
                "degree": degree,
                "incoming_terms": len(incoming),
                "first_normal_factors": nf1,
                "first_normal_terms": nt1,
                "first_normal_steps": ns1,
                "tangent_terms": len(tangent),
                "obstruction_terms": len(obstruction_quotients),
                "obstruction_steps": obstruction_steps,
                "unreduced_tangent_terms": len(obstruction_remainder),
                "unreduced_tangent": obstruction_remainder,
                "complete": False,
            }

        require(
            FOURTH.reconstruct_obstruction_division(
                obstruction_quotients, self.simple_obstructions
            ) == tangent,
            f"degree {degree}: obstruction division did not replay",
        )

        lifted = {}
        for (pivot, multiplier), coefficient in obstruction_quotients.items():
            ambient_multiplier = SOURCE.convert_tangent_multiplier(
                multiplier, coefficient, self.free_columns
            )
            functional = self.obstruction_functional(pivot)
            self.add_correction(
                ambient_multiplier, functional,
                f"degree_{degree}_obstruction",
            )
            CUBIC.add_scaled(
                lifted,
                CUBIC.multiply_polynomials(
                    ambient_multiplier,
                    self.functional_hasse(functional, 2),
                ),
            )
        second_input = dict(first_remainder)
        CUBIC.add_scaled(second_input, lifted, -1)
        require(
            not CUBIC.tangent_restriction(
                second_input, self.data["tangent_basis"]
            ),
            f"degree {degree}: obstruction lift left tangent terms",
        )
        second_remainder, nf2, nt2, ns2 = self.normal_reduce(
            second_input, degree, "second"
        )
        require(not second_remainder,
                f"degree {degree}: final normal remainder")
        return {
            "degree": degree,
            "incoming_terms": len(incoming),
            "first_normal_factors": nf1,
            "first_normal_terms": nt1,
            "first_normal_steps": ns1,
            "tangent_terms": len(tangent),
            "obstruction_terms": len(obstruction_quotients),
            "obstruction_steps": obstruction_steps,
            "unreduced_tangent_terms": 0,
            "second_normal_input_terms": len(second_input),
            "second_normal_factors": nf2,
            "second_normal_terms": nt2,
            "second_normal_steps": ns2,
            "complete": True,
        }


def analyze(colour, maximum_degree):
    reducer = LocalReducer()
    selected = SECOND.MIXED_WORD_0 if colour == 0 else SECOND.MIXED_WORD_1
    pure = SECOND.PURE_WORD_0 if colour == 0 else SECOND.PURE_WORD_1
    reducer.add_correction(
        {(): QQ(1)},
        {THIRD.MIXED_WORD_INDEX[selected]: QQ(1)},
        "selected_mixed_coefficient",
    )
    ledger = []
    for degree in range(1, maximum_degree + 1):
        record = reducer.reduce_degree(pure, degree)
        ledger.append(record)
        print(
            f"colour={colour} degree={degree} incoming={record['incoming_terms']} "
            f"tangent={record['tangent_terms']} "
            f"unreduced={record['unreduced_tangent_terms']} "
            f"corrections={len(reducer.corrections)}",
            flush=True,
        )
        if not record["complete"]:
            break
    return ledger, reducer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--colour", type=int, choices=(0, 1), required=True)
    parser.add_argument("--max-degree", type=int, default=6)
    args = parser.parse_args()
    ledger, reducer = analyze(args.colour, args.max_degree)
    last = ledger[-1]
    print(
        f"STOP colour={args.colour} degree={last['degree']} "
        f"complete={last['complete']} corrections={len(reducer.corrections)}"
    )


if __name__ == "__main__":
    main()
