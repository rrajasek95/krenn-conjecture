#!/usr/bin/env python3
"""Discovery probe for the two branch-1, d=0 one-parameter components."""

from __future__ import annotations

from fractions import Fraction as F
import importlib.util
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
CORE_PATH = (HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
             / "audit_polarized_superpair_core_identity.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b1_probe_core", CORE_PATH)


def derivative(poly, variable):
    answer = {}
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        reduced = list(monomial)
        reduced.remove(variable)
        reduced = tuple(reduced)
        answer[reduced] = answer.get(reduced, 0) + multiplicity * coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


class Quadratic:
    def __init__(self, p, q=1):
        self.p = F(p)
        self.q = F(q)
        self.zero = (F(0), F(0))
        self.one = (F(1), F(0))
        self.z = (F(0), F(1))

    def add(self, *values):
        return (sum(value[0] for value in values),
                sum(value[1] for value in values))

    def neg(self, value):
        return (-value[0], -value[1])

    def scale(self, value, scalar):
        scalar = F(scalar)
        return (scalar * value[0], scalar * value[1])

    def mul(self, left, right):
        return (left[0] * right[0] + self.q * left[1] * right[1],
                left[0] * right[1] + left[1] * right[0]
                + self.p * left[1] * right[1])

    def inv(self, value):
        # (a+bz)(a+bp-bz)=a^2+abp-b^2q.
        conjugate = (value[0] + self.p * value[1], -value[1])
        norm = value[0] * conjugate[0] - self.q * value[1] * value[1]
        if not norm:
            raise ZeroDivisionError
        return self.scale(conjugate, 1 / norm)

    def power(self, value, exponent):
        answer = self.one
        while exponent:
            if exponent & 1:
                answer = self.mul(answer, value)
            value = self.mul(value, value)
            exponent //= 2
        return answer

    def polynomial(self, coefficients):
        return self.add(*(self.scale(self.power(self.z, degree), coefficient)
                          for degree, coefficient in enumerate(coefficients)))


def pt_clean(poly, field):
    return {degree: value for degree, value in poly.items()
            if value != field.zero}


def pt_add(field, *polys):
    answer = {}
    for poly in polys:
        for degree, value in poly.items():
            answer[degree] = field.add(answer.get(degree, field.zero), value)
    return pt_clean(answer, field)


def pt_mul(field, *polys):
    answer = {0: field.one}
    for poly in polys:
        updated = {}
        for left_degree, left in answer.items():
            for right_degree, right in poly.items():
                degree = left_degree + right_degree
                updated[degree] = field.add(
                    updated.get(degree, field.zero), field.mul(left, right))
        answer = pt_clean(updated, field)
    return answer


def evaluate(field, poly, entries):
    answer = {}
    for monomial, integer in poly.items():
        term = {0: field.scale(field.one, integer)}
        for variable in monomial:
            term = pt_mul(field, term, entries[variable])
        answer = pt_add(field, answer, term)
    return answer


def component(p):
    k = Quadratic(p)
    # Coefficients are in increasing powers of z.
    b0 = k.scale(k.polynomial((-41, 105, 35, -3)), F(1, 20))
    b1 = k.scale(k.polynomial((-97, -5, 15, -1)), F(1, 40))
    b = (b0, b1, k.one, b1, k.one, k.one)
    alpha = (
        k.scale(k.polynomial((-97, -5, 15, -1)), F(1, 25)),
        k.scale(k.polynomial((-109, -61, 19, -1)), F(1, 80)),
        k.scale(k.polynomial((-347, 677, 277, -23)), F(1, 80)),
        k.scale(k.polynomial((-641, 215, 175, -13)), F(1, 400)),
        k.scale(k.polynomial((-343, -3455, -1175, 101)), F(1, 400)),
        k.one,
    )
    entries = []
    for edge in range(6):
        entries.extend((({1: alpha[edge]} if alpha[edge] != k.zero else {}),
                        {0: b[edge]},
                        {0: k.neg(k.inv(b[edge]))}, {}))
    h = CORE.pure_hafnian()
    base = [CORE.e_pair(*edge) for edge in CORE.SUPER_EDGES]
    base += [CORE.t_triple(*triple)
             for triple in __import__("itertools").combinations(range(4), 3)]
    bits = (1, 0, 0, 0, 0, 0)
    for edge, bit in enumerate(bits):
        for position in ((1, 2) if bit else (0, 3)):
            base.append(derivative(h, 4 * edge + position))
    values = [evaluate(k, poly, entries) for poly in base]
    if any(values):
        raise RuntimeError((p, [(i, value) for i, value in enumerate(values)
                               if value]))
    h_value = evaluate(k, h, entries)
    q_values = [evaluate(k, CORE.q_orientation(tuple(
        (value >> (3 - site)) & 1 for site in range(4))), entries)
                for value in range(16)]
    cofactor_values = [evaluate(k, derivative(h, variable), entries)
                       for variable in range(24)]
    return {
        "p": p,
        "b": b,
        "alpha": alpha,
        "H": h_value,
        "Q": q_values,
        "C": cofactor_values,
    }


def main():
    for row in (component(14), component(-2)):
        print("COMPONENT p", row["p"], "H", row["H"])
        print("b", row["b"])
        print("alpha", row["alpha"])
        print("Q support", [i for i, value in enumerate(row["Q"]) if value])
        for i, value in enumerate(row["Q"]):
            if value:
                print(" Q", i, value)
        print("C support", [i for i, value in enumerate(row["C"]) if value])
        for i, value in enumerate(row["C"]):
            if value:
                print(" C", i, value)


if __name__ == "__main__":
    main()
