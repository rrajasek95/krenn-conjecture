#!/usr/bin/env python3
"""Factor the exact left covariants used by the compact mate certificate."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_left_slices_export_mate.py"
OUT = HERE / "results_left_localizers_exact.json"
COFACTOR_INDICES = (1, 2, 6, 10, 14, 18, 21, 22)
LEFT_Q_INDICES = (0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 15)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("generic_cycle_localizer_audit", AUDIT_PATH)


def raw_to_sympy(poly, entries):
    result = sp.Integer(0)
    for monomial, coefficient in poly.items():
        term = sp.Rational(coefficient)
        for index in monomial:
            term *= entries[index]
        result += term
    return sp.cancel(result)


def describe(expression, variables):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    numerator = sp.factor(numerator)
    denominator = sp.factor(denominator)
    return {
        "numerator": str(numerator),
        "denominator": str(denominator),
        "numerator_terms": len(sp.Poly(sp.expand(numerator), *variables).terms()),
        "numerator_total_degree": sp.Poly(sp.expand(numerator), *variables).total_degree(),
    }


def main() -> None:
    variables, entries = AUDIT.raw_left_expressions()
    h = AUDIT.CORE.pure_hafnian()
    cofactors = tuple(AUDIT.PROBE.derivative(h, index) for index in range(24))
    q_polys = tuple(AUDIT.CORE.q_orientation(tuple(
        (index >> (3-site)) & 1 for site in range(4))) for index in range(16))
    cofactor_records = {
        str(index): describe(raw_to_sympy(cofactors[index], entries), variables)
        for index in COFACTOR_INDICES
    }
    q_records = {
        str(index): describe(raw_to_sympy(q_polys[index], entries), variables)
        for index in LEFT_Q_INDICES
    }
    result = {
        "status": "UNAUDITED exact-Q left-localizer factor export PASS",
        "variables": [str(variable) for variable in variables],
        "cofactor_localizers": cofactor_records,
        "left_Q_localizers": q_records,
        "scope_guard": (
            "These are exact rational functions on the frozen solved chart before "
            "reduction by the remaining A=B=0 source ideal. A factor is chart-forced "
            "only if its numerator is a product of declared live factors modulo that ideal."
        ),
        "source_sha256": sha256(AUDIT_PATH.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("left localizer exact factor export PASS")
    for family in (cofactor_records, q_records):
        for index, record in family.items():
            print(index, record["numerator_terms"], record["numerator_total_degree"],
                  record["numerator"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
