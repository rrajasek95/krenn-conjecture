#!/usr/bin/env python3
"""Seek a constant-coefficient tensor contraction on the smallest pair01 chart."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATLAS = HERE / "verify_simultaneous_pivots.py"
PRIME = 32003


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Poly:
    __slots__ = ("terms",)

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, int):
            self.terms = {} if value % PRIME == 0 else {(): value % PRIME}
        else:
            raise TypeError(value)

    @classmethod
    def variable(cls, name):
        answer = cls()
        answer.terms[(name,)] = 1
        return answer

    def __add__(self, other):
        other = Poly(other)
        answer = Poly(self)
        for monomial, coefficient in other.terms.items():
            value = (answer.terms.get(monomial, 0) + coefficient) % PRIME
            if value:
                answer.terms[monomial] = value
            else:
                answer.terms.pop(monomial, None)
        return answer

    __radd__ = __add__

    def __neg__(self):
        answer = Poly()
        answer.terms = {monomial: (-coefficient) % PRIME for monomial, coefficient in self.terms.items()}
        return answer

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        other = Poly(other)
        answer = Poly()
        for left, lc in self.terms.items():
            for right, rc in other.terms.items():
                monomial = tuple(sorted(left + right))
                answer.terms[monomial] = (answer.terms.get(monomial, 0) + lc * rc) % PRIME
                if answer.terms[monomial] == 0:
                    del answer.terms[monomial]
        return answer

    __rmul__ = __mul__


def chart_equations():
    atlas = load("simultaneous_atlas", ATLAS)
    incidence = atlas.load_module(
        "sealed_incidence_for_span",
        atlas.INC_DIR / "generate_incidence_pivot_charts.py",
    )
    helper = incidence.load_helper()
    module = helper.load_core()
    words = incidence.stage_words("pair01")
    equations = [
        f"({module.amplitude(word)})-1" if len(set(word)) == 1 else module.amplitude(word)
        for word in words
    ]
    a67 = incidence.adjoint_replacements(module)
    incidence_sub, incidence_inverse, _ = incidence.incidence_replacements(0, "sigma", 0)
    guard_sub, guard_inverse, _ = atlas.guard_replacements(module, 0, 0)
    equations = [atlas.token_replace(value, a67) for value in equations]
    equations = [atlas.token_replace(value, guard_sub) for value in equations]
    equations = [atlas.token_replace(value, incidence_sub) for value in equations]
    equations = [atlas.token_replace(value, {"u0": "1"}) for value in equations]
    equations += incidence_inverse + guard_inverse
    assert len(equations) == 261
    return equations


def main():
    texts = chart_equations()
    names = sorted(set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", "\n".join(texts))))
    namespace = {name: Poly.variable(name) for name in names}
    polynomials = [eval(text, {"__builtins__": {}}, namespace) for text in texts]
    distinct_monomials = set().union(*(poly.terms for poly in polynomials))

    # Constant-coefficient row span only.  This is a bounded tensor-contraction
    # search, not a Groebner computation or polynomial-multiplier search.
    basis = {}
    rank = 0
    for index, poly in enumerate(polynomials):
        row = dict(poly.terms)
        while row:
            pivot = max(row)
            if pivot not in basis:
                scale = pow(row[pivot], PRIME - 2, PRIME)
                row = {term: coefficient * scale % PRIME for term, coefficient in row.items()}
                basis[pivot] = (row, index)
                rank += 1
                break
            known, _ = basis[pivot]
            multiple = row[pivot]
            for term, coefficient in known.items():
                value = (row.get(term, 0) - multiple * coefficient) % PRIME
                if value:
                    row[term] = value
                else:
                    row.pop(term, None)

    target = {(): 1}
    while target:
        pivot = max(target)
        if pivot not in basis:
            break
        known, _ = basis[pivot]
        multiple = target[pivot]
        for term, coefficient in known.items():
            value = (target.get(term, 0) - multiple * coefficient) % PRIME
            if value:
                target[term] = value
            else:
                target.pop(term, None)
    status = "FOUND_LINEAR_UNIT_CONTRACTION" if not target else "NO_CONSTANT_COEFFICIENT_UNIT_CONTRACTION"
    print({
        "status": status,
        "prime": PRIME,
        "chart": "u0_v0_w0_rho0_sigma0",
        "equations": len(polynomials),
        "variables": len(names),
        "distinct_monomials": len(distinct_monomials),
        "constant_span_rank": rank,
        "target_remainder_terms": len(target),
        "scope": "constant coefficients only; no polynomial multipliers and no Groebner basis",
    })


if __name__ == "__main__":
    main()
