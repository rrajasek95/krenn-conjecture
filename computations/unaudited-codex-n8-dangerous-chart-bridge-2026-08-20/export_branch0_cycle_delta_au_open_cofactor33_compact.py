#!/usr/bin/env python3
"""Compact denominator-free Cof(3,3) obstruction for the cycle residual."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
REFEREE = (HERE.parent /
           "unaudited-codex-k4-cycle-char0-rur-referee-2026-08-21" /
           "export_cofactor13_cramer_obstruction.py")
SOURCE_P1 = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve"
SOURCE_P2 = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741789.msolve"
OUT_P1 = HERE / "branch0_cycle_delta_au_open_cofactor33_p1073741827.msolve"
OUT_P2 = HERE / "branch0_cycle_delta_au_open_cofactor33_p1073741789.msolve"
OUT_Q = HERE / "branch0_cycle_delta_au_open_cofactor33_char0.msolve"
RESULT = HERE / "results_branch0_cycle_delta_au_open_cofactor33_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("n8_cycle_cofactor33_compact_base", REFEREE)
SOURCE = BASE.SOURCE
AUDIT = BASE.AUDIT
require = BASE.require


def derive_core():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    interface = AUDIT.INTERFACE.derive(rows)
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    y = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    ratio = {b3: x*b1, d3: -x*d1*d4}

    literal = sp.cancel(rows["cofactor_3_3"].subs(ratio)
                        .subs(interface[3]).subs(SOURCE.A0, interface[4]))
    cleared, literal_denominator = literal.as_numer_denom()
    require(sp.factor(literal_denominator) == (b1+d1)*(x-1),
            "the compact Cof(3,3) clearing denominator changed")
    literal_poly = sp.Poly(cleared, *y)
    require(literal_poly.total_degree() == 2
            and len(literal_poly.terms()) == 5,
            "the compact omitted cofactor changed shape")

    # Hostile source mutation must change the literal reduced row before any
    # Cramer or quotient operation.
    mutated_raw = dict(raw["cofactor_3_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated = SOURCE.expression(mutated_raw)
    mutated = sp.cancel(mutated.subs(ratio).subs(interface[3])
                        .subs(SOURCE.A0, interface[4]))
    require(sp.cancel(mutated-literal) != 0,
            "the Cof(3,3) source mutation did not fire")

    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row])
               for entry in entries]
              for row, entries in enumerate(interface[6])]
    selected = (2, 3, 4)
    coefficient = sp.Matrix(
        [[matrix[row][column] for column in range(3)]
         for row in selected])
    right = sp.Matrix([-matrix[row][3] for row in selected])
    determinant = sp.expand(coefficient.det())
    numerators = coefficient.adjugate()*right
    require(len(sp.Poly(determinant, b0, b1, x, d1, d4).terms()) == 10,
            "the compact Cramer determinant changed")

    n_symbols = sp.symbols("n0 n1 n2")
    d_symbol = sp.Symbol("D")
    template = 0
    for monomial, scalar in literal_poly.terms():
        term = scalar*d_symbol**(2-sum(monomial))
        for variable, exponent in zip(n_symbols, monomial, strict=True):
            term *= variable**exponent
        template += term
    replay = sp.expand(template.subs(
        {d_symbol: determinant,
         **{symbol: determinant*variable for symbol, variable
            in zip(n_symbols, y, strict=True)}}))
    require(sp.expand(replay-determinant**2*cleared) == 0,
            "the compact Cramer homogenization identity failed")
    homogenized = sp.expand(template.subs(
        {d_symbol: determinant,
         **{symbol: numerator for symbol, numerator
            in zip(n_symbols, numerators, strict=True)}}))
    require(len(sp.Poly(homogenized, b0, b1, x, d1, d4).terms()) == 1306,
            "the compact homogenized term count changed")

    u = interface[1]
    d4_value = sp.cancel(-u.subs(d4, 0)/sp.diff(u, d4))
    q = AUDIT.derive(rows)["q"]
    substituted = sp.cancel(homogenized.subs(d4, d4_value))
    numerator = substituted.as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(numerator, b0, domain="QQ(b1,d1,x)"),
        sp.Poly(q, b0, domain="QQ(b1,d1,x)")).as_expr()
    remainder = sp.cancel(remainder).as_numer_denom()[0]
    remainder_poly = sp.Poly(remainder, b0, b1, d1, x)
    content = tuple(min(monomial[index]
                        for monomial, _ in remainder_poly.terms())
                    for index in range(4))
    require(content == (0, 5, 3, 0),
            "the compact chart-live monomial changed")
    monomial = b0**content[0]*b1**content[1]*d1**content[2]*x**content[3]
    core = remainder_poly.exquo(
        sp.Poly(monomial, b0, b1, d1, x)).as_expr()
    core_poly = sp.Poly(core, b0, b1, d1, x)
    degrees = [core_poly.degree(variable)
               for variable in (b0, b1, d1, x)]
    require(len(core_poly.terms()) == 4031
            and degrees == [1, 7, 24, 19],
            "the compact Cof(3,3) quotient profile changed")
    return core, {
        "source_label": "cofactor_3_3",
        "source_row_sha256": sha256(str(raw["cofactor_3_3"])
                                     .encode("ascii")).hexdigest(),
        "linear_packet_row_indices": list(selected),
        "linear_packet_row_labels": [interface[5][index]
                                      for index in selected],
        "literal_clearing_denominator": str(sp.factor(literal_denominator)),
        "cramer_determinant_terms": 10,
        "homogenized_terms": 1306,
        "d4_value": str(d4_value),
        "removed_chart_live_monomial_exponents_b0_b1_d1_x": list(content),
        "core_terms": len(core_poly.terms()),
        "core_degrees_b0_b1_d1_x": degrees,
        "core_sha256": BASE.polynomial_sha(core),
    }


def main():
    core, metadata = derive_core()
    variables1, prime1, rows1 = BASE.read_input(SOURCE_P1)
    variables2, prime2, rows2 = BASE.read_input(SOURCE_P2)
    require(variables1 == variables2 == ("b0", "b1", "d1", "x")
            and prime1 == 1073741827 and prime2 == 1073741789
            and rows1 == rows2 and len(rows1) == 17,
            "the frozen two-prime all-minor inputs changed")
    encoded = BASE.encode(core)
    output_rows = (*rows1[:-1], encoded, rows1[-1])
    BASE.write_input(OUT_P1, prime1, output_rows)
    BASE.write_input(OUT_P2, prime2, output_rows)
    b0, b1, d1, x, z = sp.symbols("b0 b1 d1 x z")
    live_expression = sp.sympify(rows1[-1].replace("^", "**"), locals={
        "b0": b0, "b1": b1, "d1": d1, "x": x})
    rabinowitsch = sp.expand(z*live_expression-1)
    require(sp.expand(sp.diff(rabinowitsch, z)-live_expression) == 0
            and sp.expand(rabinowitsch.subs(z, 0)+1) == 0,
            "the compact characteristic-zero Rabinowitsch row failed")
    OUT_Q.write_text("b0,b1,d1,x,z\n0\n" + ",\n".join(
        (*output_rows[:-1], BASE.encode(rabinowitsch))) + "\n")
    result = {
        "status": "UNAUDITED compact exact Cof(3,3) necessary export",
        **metadata,
        "prime_inputs": [
            {"prime": prime1, "path": OUT_P1.name,
             "sha256": sha256(OUT_P1.read_bytes()).hexdigest()},
            {"prime": prime2, "path": OUT_P2.name,
             "sha256": sha256(OUT_P2.read_bytes()).hexdigest()},
            {"prime": 0, "path": OUT_Q.name,
             "sha256": sha256(OUT_Q.read_bytes()).hexdigest()}],
        "scope": (
            "Every literal full-source packet on the declared Delta/Bplus/"
            "Au-open chart kills this polynomial. Fraction-free Cramer "
            "homogenization retains the determinant-zero boundary. Modular "
            "UNIT is discovery only; no exact-Q claim is made."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("compact Cof(3,3) export: PASS")
    print("core terms/degrees:", metadata["core_terms"],
          metadata["core_degrees_b0_b1_d1_x"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
