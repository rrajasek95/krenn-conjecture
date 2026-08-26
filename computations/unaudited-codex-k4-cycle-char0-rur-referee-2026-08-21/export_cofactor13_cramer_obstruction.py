#!/usr/bin/env python3
"""Export a denominator-free Cof(1,3) obstruction on the all-minor chart.

After the Delta/Bplus source reduction, the six retained literal rows are
affine-linear in y=(p1,p2,a5), whereas Cof(1,3) is quadratic in y.  For the
three rows (t023,t123,Cof(0,0)), write C*y=b, D=det(C), N=adj(C)*b.  If a
literal packet solution exists then N=D*y, so the degree-two homogenization

    G = D^2 * cleared_Cof13(N/D)

vanishes without any assumption that D is nonzero.  Substitute the exact
d4 solve, reduce modulo Q, and remove only a chart-live monomial to obtain
the four-variable obstruction exported here.
"""

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
DANGER = (HERE.parent /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
AUDIT_PATH = DANGER / "audit_branch0_cycle_delta_au_open_generic.py"
SOURCE_P1 = DANGER / "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve"
SOURCE_P2 = DANGER / "branch0_cycle_delta_au_open_all_minors_p1073741789.msolve"
OUT_P1 = HERE / "cofactor13_all_minors_p1073741827.msolve"
OUT_P2 = HERE / "cofactor13_all_minors_p1073741789.msolve"
LABELS = HERE / "cofactor13_all_minors_labels.json"
RESULT = HERE / "results_cofactor13_cramer_obstruction.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("k4_cofactor13_export_audit", AUDIT_PATH)
SOURCE = AUDIT.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def polynomial_sha(poly):
    return sha256(encode(poly).encode("ascii")).hexdigest()


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def read_input(path):
    lines = path.read_text().splitlines()
    variables = tuple(value.strip() for value in lines[0].split(","))
    characteristic = int(lines[1])
    rows = tuple(value.strip() for value in
                 "\n".join(lines[2:]).split(",") if value.strip())
    return variables, characteristic, rows


def write_input(path, characteristic, rows):
    path.write_text("b0,b1,d1,x\n" + str(characteristic) + "\n" +
                    ",\n".join(rows) + "\n")


def derive_core():
    raw_rows, _ = SOURCE.SOURCE.data()
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in raw_rows}
    interface = AUDIT.INTERFACE.derive(rows)
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    y = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    ratio = {b3: x*b1, d3: -x*d1*d4}

    literal = sp.cancel(rows["cofactor_1_3"].subs(ratio)
                        .subs(interface[3]).subs(SOURCE.A0, interface[4]))
    cleared, literal_denominator = literal.as_numer_denom()
    require(sp.factor(literal_denominator) ==
            b0*(b1+d1)**2*(x-1),
            "the Cof(1,3) clearing denominator changed")
    literal_poly = sp.Poly(cleared, *y)
    y_degree = max(sum(monomial) for monomial, _ in literal_poly.terms())
    require(y_degree == 2,
            "the reduced Cof(1,3) ceased to be quadratic")

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
            "the selected Cramer determinant changed")

    n_symbols = sp.symbols("n0 n1 n2")
    d_symbol = sp.Symbol("D")
    homogenized_template = 0
    for monomial, scalar in literal_poly.terms():
        degree = sum(monomial)
        term = scalar*d_symbol**(2-degree)
        for variable, exponent in zip(n_symbols, monomial, strict=True):
            term *= variable**exponent
        homogenized_template += term
    replay = sp.expand(homogenized_template.subs(
        {d_symbol: determinant,
         **{symbol: determinant*variable for symbol, variable
            in zip(n_symbols, y, strict=True)}}))
    require(sp.expand(replay-determinant**2*cleared) == 0,
            "Cramer homogenization identity failed")
    homogenized = sp.expand(homogenized_template.subs(
        {d_symbol: determinant,
         **{symbol: numerator for symbol, numerator
            in zip(n_symbols, numerators, strict=True)}}))
    require(len(sp.Poly(homogenized, b0, b1, x, d1, d4).terms())
            == 1383, "Cramer homogenization term count changed")
    u = interface[1]
    d4_value = sp.cancel(-u.subs(d4, 0)/sp.diff(u, d4))
    q = (
        b0**2*d1**2*x**3-b0**2*d1**2*x**2
        -2*b0**2*d1*x**3-2*b0**2*d1*x**2
        +b0**2*x**3-b0**2*x**2-d1**2*x**3+d1**2*x**2
        +2*d1*x**2+2*d1*x-x+1)
    substituted = sp.cancel(homogenized.subs(d4, d4_value))
    substituted_numerator = substituted.as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(substituted_numerator, b0, domain="QQ(b1,d1,x)"),
        sp.Poly(q, b0, domain="QQ(b1,d1,x)")).as_expr()
    remainder = sp.cancel(remainder).as_numer_denom()[0]
    remainder_poly = sp.Poly(remainder, b0, b1, d1, x)
    content = tuple(min(monomial[index]
                        for monomial, _ in remainder_poly.terms())
                    for index in range(4))
    require(content == (0, 5, 3, 0),
            "the chart-live remainder monomial changed")
    monomial = b0**content[0]*b1**content[1]*d1**content[2]*x**content[3]
    core = remainder_poly.exquo(
        sp.Poly(monomial, b0, b1, d1, x)).as_expr()
    core_poly = sp.Poly(core, b0, b1, d1, x)
    require(len(core_poly.terms()) == 7264,
            "the reduced Cof(1,3) obstruction term count changed")
    core_degrees = [core_poly.degree(variable)
                    for variable in (b0, b1, d1, x)]
    require(core_degrees == [1, 8, 31, 26],
            f"the reduced Cof(1,3) obstruction degree changed: "
            f"{core_degrees}")
    return core, {
        "source_label": "cofactor_1_3",
        "linear_packet_row_indices": list(selected),
        "linear_packet_row_labels": [
            interface[5][index] for index in selected],
        "literal_clearing_denominator": str(sp.factor(literal_denominator)),
        "literal_y_degree": y_degree,
        "cramer_determinant_terms": 10,
        "homogenized_terms": 1383,
        "d4_value": str(d4_value),
        "Q": str(q),
        "removed_chart_live_monomial_exponents_b0_b1_d1_x": list(content),
        "core_terms": len(core_poly.terms()),
        "core_degrees_b0_b1_d1_x": core_degrees,
        "core_sha256": polynomial_sha(core),
    }


def main():
    core, metadata = derive_core()
    variables1, prime1, rows1 = read_input(SOURCE_P1)
    variables2, prime2, rows2 = read_input(SOURCE_P2)
    require(variables1 == variables2 == ("b0", "b1", "d1", "x")
            and prime1 == 1073741827 and prime2 == 1073741789
            and len(rows1) == len(rows2) == 17,
            "frozen all-minor inputs changed")
    # The two inputs differ only in their characteristic line.
    require(rows1 == rows2, "the two-prime integer row lists diverged")
    encoded_core = encode(core)
    output_rows = (*rows1[:-1], encoded_core, rows1[-1])
    labels = (["Q"] +
              ["minor_" + "".join(map(str, selected))
               for selected in __import__("itertools").combinations(
                   range(6), 4)] +
              ["cofactor_1_3_cramer_homogenized", "live_saturator"])
    require(len(labels) == len(output_rows) == 18,
            "extended input row count changed")
    write_input(OUT_P1, prime1, output_rows)
    write_input(OUT_P2, prime2, output_rows)
    LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")
    result = {
        "status": "UNAUDITED exact Cof(1,3) necessary obstruction export",
        **metadata,
        "prime_inputs": [
            {"prime": prime1, "path": OUT_P1.name, "sha256": sha(OUT_P1)},
            {"prime": prime2, "path": OUT_P2.name, "sha256": sha(OUT_P2)},
        ],
        "labels_path": LABELS.name,
        "labels_sha256": sha(LABELS),
        "scope": (
            "The exported core is necessary for a literal Cof(1,3)-zero "
            "packet on the displayed Delta/Bplus/Au chart. Cramer "
            "homogenization makes the implication valid even when the "
            "selected determinant vanishes. Modular UNIT is discovery "
            "only; an exact-Q certificate is still required."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Cof(1,3) Cramer obstruction export: PASS")
    print("core terms/degrees:", metadata["core_terms"],
          metadata["core_degrees_b0_b1_d1_x"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
