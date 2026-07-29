#!/usr/bin/env python3
"""Search the residual one-exceptional-edge charts over F_4 exactly.

The complex obstruction for these charts ends in ``2r=0``.  Thus it is
important not to assume that it survives in characteristic two.  Every
listed support coordinate is required to be nonzero.  We write it as
``omega**e`` with ``e in Z/3``, where ``omega**2+omega+1=0`` in F_4.
Matching monomial exponents are linear modulo three, and each coefficient
equation is checked by the two F_2 coordinates of its exact F_4 sum.

This is a finite-extension discovery tool, not an obstruction over the
algebraic closure when it returns UNSAT.
"""

from __future__ import annotations

import argparse

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from analyze_one_exceptional_edge import CHARTS, chart_data


PRIMITIVE_POLYNOMIALS = {
    2: 0b111,    # x^2+x+1
    3: 0b1011,   # x^3+x+1
    4: 0b10011,  # x^4+x+1
}


def field_powers(degree):
    """Coordinates of successive powers of a primitive field element."""
    polynomial = PRIMITIVE_POLYNOMIALS[degree]
    order = (1 << degree) - 1
    answer = []
    value = 1
    for _ in range(order):
        answer.append(tuple((value >> bit) & 1 for bit in range(degree)))
        value <<= 1
        if value & (1 << degree):
            value ^= polynomial
    assert value == 1 and len(set(answer)) == order
    return tuple(answer)


def exactly_one(cnf, literals):
    cnf.append(list(literals))
    for index, first in enumerate(literals):
        for second in literals[index + 1 :]:
            cnf.append([-first, -second])


def add_mod(cnf, pool, left, right, modulus, tag):
    """Return a one-hot variable for the sum of two cyclic exponents."""
    output = tuple(pool.id(("sum", tag, value)) for value in range(modulus))
    exactly_one(cnf, output)
    for a in range(modulus):
        for b in range(modulus):
            cnf.append([-left[a], -right[b], output[(a + b) % modulus]])
    return output


def monomial_exponent(cnf, pool, variables, exponent, modulus, tag):
    factors = []
    for index, multiplicity in enumerate(exponent):
        factors.extend([variables[index]] * multiplicity)
    assert factors
    total = factors[0]
    for step, factor in enumerate(factors[1:], 1):
        total = add_mod(cnf, pool, total, factor, modulus, (tag, step))
    return total


def xor_gate(cnf, pool, left, right, tag):
    output = pool.id(("xor", tag))
    cnf.extend(
        (
            [left, right, -output],
            [-left, -right, -output],
            [left, -right, output],
            [-left, right, output],
        )
    )
    return output


def require_xor(cnf, pool, literals, target, tag):
    assert literals
    parity = literals[0]
    for step, literal in enumerate(literals[1:], 1):
        parity = xor_gate(cnf, pool, parity, literal, (tag, step))
    cnf.append([parity if target else -parity])


def search(chart_name, degree, solver_name):
    keys, fibers = chart_data(chart_name)
    powers = field_powers(degree)
    modulus = len(powers)
    pool = IDPool()
    cnf = CNF()
    variables = []
    for index, key in enumerate(keys):
        one_hot = tuple(
            pool.id(("variable", index, value)) for value in range(modulus)
        )
        exactly_one(cnf, one_hot)
        variables.append(one_hot)

    for fiber_index, (coloring, monomials, target) in enumerate(fibers):
        terms = tuple(
            monomial_exponent(
                cnf,
                pool,
                variables,
                exponent,
                modulus,
                (fiber_index, term_index),
            )
            for term_index, exponent in enumerate(monomials)
        )
        # Convert each exponent one-hot value to field-coordinate bits, then
        # impose the coefficient equation by bitwise XOR.
        for bit in range(degree):
            term_bits = []
            for term_index, term in enumerate(terms):
                bit_variable = pool.id(("field-bit", fiber_index, term_index, bit))
                term_bits.append(bit_variable)
                for value in range(modulus):
                    cnf.append(
                        [-term[value], bit_variable if powers[value][bit] else -bit_variable]
                    )
            require_xor(
                cnf,
                pool,
                term_bits,
                target=(target == 1 and bit == 0),
                tag=(fiber_index, bit),
            )

    print(
        f"{chart_name}/F_{1 << degree}: coordinates={len(keys)} variables={pool.top} "
        f"clauses={len(cnf.clauses)}",
        flush=True,
    )
    with Solver(name=solver_name, bootstrap_with=cnf) as solver:
        satisfiable = solver.solve()
        print(f"{chart_name}/F_{1 << degree}: SAT={satisfiable}", flush=True)
        if not satisfiable:
            return None
        model = {literal for literal in solver.get_model() if literal > 0}
    assignment = {
        key: next(
            value for value in range(modulus) if variables[index][value] in model
        )
        for index, key in enumerate(keys)
    }

    # Independent exact F_4 audit from exponent vectors.
    for coloring, monomials, target in fibers:
        exponents = [
            sum(
                coefficient * assignment[key]
                for key, coefficient in zip(keys, monomial)
            )
            % modulus
            for monomial in monomials
        ]
        field_sum = tuple(
            sum(powers[exponent][bit] for exponent in exponents) % 2
            for bit in range(degree)
        )
        assert field_sum == (target,) + (0,) * (degree - 1), (
            coloring,
            exponents,
            target,
        )
    print(f"{chart_name}: assignment={assignment}")
    print(f"{chart_name}: independent exact finite-field audit passed")
    return assignment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", choices=tuple(CHARTS), default="same")
    parser.add_argument("--degree", type=int, choices=tuple(PRIMITIVE_POLYNOMIALS), default=2)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    search(args.chart, args.degree, args.solver)


if __name__ == "__main__":
    main()
