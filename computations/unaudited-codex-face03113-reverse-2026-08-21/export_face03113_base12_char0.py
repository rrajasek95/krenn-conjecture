#!/usr/bin/env python3
"""Export the canonical characteristic-zero base12+C Rabinowitsch system.

Every row is rebuilt from the frozen literal face chart, expanded over Z,
and printed with numeric coefficients before symbolic factors.  The final
row is the explicit Rabinowitsch equation

  s*a5*b3*b4*(1+a0)*(1+a2*d2)*(1+a3*d3)-1.

No H or both-live a*d factor is localized.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE = (HERE.parent /
          "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
          "results_recursive_face_charts.json")
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "face03113_base12_c_char0.msolve"
LABELS = HERE / "face03113_base12_c_char0_labels.json"
RESULT = HERE / "results_face03113_base12_char0_export.json"
KEY = "0:31:13"
KEPT = (7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)
VARIABLE_NAMES = ("a0", "a1", "a2", "a3", "a4", "a5",
                  "b3", "b4", "b5", "d2", "d3", "s")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MSOLVE_IO = load("face03113_char0_msolve_io", TOOLKIT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def extract_factor(record, label):
    value = record["localizers"][label]
    require(value.endswith("-1") and "*(" in value,
            f"unexpected {label} encoding")
    return value[value.index("*(")+1:-2]


def encode(poly, symbols):
    polynomial = sp.Poly(sp.expand(poly), *symbols)
    require(polynomial.domain == sp.ZZ, "export row left Z")
    pieces = []
    for position, (monomial, coefficient) in enumerate(polynomial.terms()):
        coefficient = int(coefficient)
        sign = "-" if coefficient < 0 else "+"
        factors = []
        magnitude = abs(coefficient)
        symbolic = [(symbol, exponent) for symbol, exponent in
                    zip(symbols, monomial, strict=True) if exponent]
        if magnitude != 1 or not symbolic:
            factors.append(str(magnitude))
        factors.extend(str(symbol) + (f"^{exponent}" if exponent != 1 else "")
                       for symbol, exponent in symbolic)
        term = "*".join(factors)
        if position == 0:
            pieces.append(("-" if coefficient < 0 else "") + term)
        else:
            pieces.append(sign + term)
    require(pieces, "zero source row")
    return "".join(pieces)


def main():
    payload = json.loads(SOURCE.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    raw = {row["raw_index"]: row for row in record["rows"]}
    symbols = sp.symbols(" ".join(VARIABLE_NAMES))
    locals_map = dict(zip(VARIABLE_NAMES, symbols, strict=True))
    labelled = []
    source_profiles = []
    for index in KEPT:
        expression = raw[index]["polynomial"]
        poly = sp.sympify(expression.replace("^", "**"), locals=locals_map)
        encoded = encode(poly, symbols)
        labelled.append((f"raw_{index}_{raw[index]['label']}", encoded))
        source_profiles.append({
            "raw_index": index, "label": raw[index]["label"],
            "source_expression_sha256": sha256(expression.encode()).hexdigest(),
            "expanded_polynomial_sha256":
                MSOLVE_IO.polynomial_sha256(encoded),
            "terms": len(sp.Poly(poly, *symbols).terms()),
        })
    selected = sp.sympify(extract_factor(record, "selected_base_terms"),
                          locals=locals_map)
    c_factor = sp.sympify(extract_factor(
        record, "both_live_c_numerators"), locals=locals_map)
    a0, a1, a2, a3, a4, a5, b3, b4, b5, d2, d3, s = symbols
    require(sp.expand(c_factor-(1+a0)*(1+a2*d2)*(1+a3*d3)) == 0,
            "remaining-C factorization changed")
    require(sp.expand(selected-a5*b3*b4) == 0,
            "selected-base factor changed")
    rab = encode(sp.expand(s*selected*c_factor-1), symbols)
    labelled.append(("RAB_selected_base_times_C", rab))

    INPUT.write_text(",".join(VARIABLE_NAMES) + "\n0\n" +
                     ",\n".join(poly for _, poly in labelled) + "\n")
    LABELS.write_text(json.dumps({"labels": [label for label, _ in labelled]},
                                 indent=2) + "\n")
    parsed = MSOLVE_IO.read_msolve_input(
        INPUT, strict=True, allow_characteristic_zero=True)
    require(parsed.variables == VARIABLE_NAMES and parsed.characteristic == 0
            and len(parsed.polynomials) == 13,
            "strict characteristic-zero parse changed")
    # Coefficient-first and expansion guards are enforced by the strict
    # parser.  A hostile source coefficient mutation must alter exactly row0.
    first_poly = sp.Poly(sp.sympify(labelled[0][1].replace("^", "**"),
                                    locals=locals_map), *symbols)
    terms = first_poly.terms()
    mutated = first_poly.as_dict()
    mutated[terms[0][0]] = -mutated[terms[0][0]]
    mutated_encoded = encode(sp.Poly.from_dict(mutated, symbols).as_expr(),
                             symbols)
    require(MSOLVE_IO.polynomial_sha256(mutated_encoded)
            != parsed.polynomial_sha256[0]
            and tuple(parsed.polynomial_sha256[1:]) ==
                tuple(MSOLVE_IO.polynomial_sha256(poly)
                      for _, poly in labelled[1:]),
            "hostile literal-row mutation did not fire locally")
    result = {
        "status": "UNAUDITED exact source/export replay PASS",
        "face": KEY, "characteristic": 0,
        "variables": list(VARIABLE_NAMES),
        "kept_raw_rows": list(KEPT),
        "source_profiles": source_profiles,
        "rabinowitsch_label": labelled[-1][0],
        "rabinowitsch_expanded": rab,
        "rabinowitsch_terms": len(sp.Poly(
            sp.sympify(rab.replace("^", "**"), locals=locals_map),
            *symbols).terms()),
        "localized_factors": ["a5", "b3", "b4", "1+a0",
                              "1+a2*d2", "1+a3*d3"],
        "not_localized": ["H", "a0*a2*a3*d2*d3"],
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "input_path": INPUT.name,
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "labels_path": LABELS.name,
        "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        "must_fire": "negating row0's leading coefficient changes only row0",
        "scope_guard": ("A characteristic-zero msolve [-1] on this explicit "
                        "Rabinowitsch system closes only face (0,31,13) on "
                        "the selected-base and remaining-C open set."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03113 char0 export: PASS")
    print("row terms", [row["terms"] for row in source_profiles],
          "rab", result["rabinowitsch_terms"])
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
