#!/usr/bin/env python3
"""Reduce the seven exceptional left-Q divisors by the exact A=B basis."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_left_Q_exception_hlive.py"
BASIS_PATH = HERE / "left_AB0_exact_full.gb.out"
OUT = HERE / "results_Q_exceptions_mod_exact_basis.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


EXPORT = load("generic_cycle_Q_exception_export", EXPORT_PATH)


def parse_basis(variables):
    text = BASIS_PATH.read_text()
    start = text.index("[", text.index("#---", text.index("#---")+3))
    end = text.rindex("]:")
    encoded = text[start:end+1].replace("^", "**")
    parsed = sp.sympify(encoded, locals={str(v): v for v in variables})
    if not isinstance(parsed, (list, tuple)) or len(parsed) != 18:
        raise RuntimeError("exact basis parse changed")
    return tuple(parsed)


def raw_to_sympy(poly, entries):
    result = sp.Integer(0)
    for monomial, coefficient in poly.items():
        term = sp.Rational(coefficient)
        for index in monomial:
            term *= entries[index]
        result += term
    return sp.cancel(result)


def main():
    variables, _, _, _ = EXPORT.BUILDER.derive()
    parameters, entries = EXPORT.AUDIT.raw_left_expressions()
    basis = parse_basis(variables)
    gb = sp.groebner(basis, *variables, order="grevlex", domain=sp.QQ)
    if len(gb.polys) != 18:
        raise RuntimeError("exact basis reconstruction changed")
    q_polys = tuple(EXPORT.AUDIT.CORE.q_orientation(tuple(
        (index >> (3-site)) & 1 for site in range(4))) for index in range(16))
    records = []
    for index in range(16):
        expression = raw_to_sympy(q_polys[index], entries)
        numerator = expression.as_numer_denom()[0]
        remainder = sp.factor(gb.reduce(numerator)[1])
        profile = sp.Poly(sp.expand(remainder), *variables)
        records.append({
            "left_Q_index": index,
            "remainder": str(remainder),
            "remainder_terms": len(profile.terms()),
            "remainder_total_degree": profile.total_degree(),
            "zero_mod_component": remainder == 0,
        })
    result = {
        "status": "UNAUDITED exact-Q exceptional-divisor reduction PASS",
        "basis_length": 18,
        "basis_sha256": sha256(BASIS_PATH.read_bytes()).hexdigest(),
        "records": records,
        "scope": (
            "Exact normal forms modulo the reduced grevlex basis of the full "
            "A=B=0 source chart with the original nine live factors. A "
            "nonzero remainder is not itself proof that its divisor survives; "
            "the dedicated H-live divisor gates decide that question."
        ),
        "source_sha256": sha256(EXPORT_PATH.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q exceptions exact-basis reduction PASS")
    for record in records:
        print(record["left_Q_index"], record["remainder_terms"],
              record["remainder_total_degree"], record["remainder"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
