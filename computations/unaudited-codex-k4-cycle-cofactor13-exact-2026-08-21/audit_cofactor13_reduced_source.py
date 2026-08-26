#!/usr/bin/env python3
"""Independent exact-source replay of Volta's reduced Cof(1,3) core.

This starts from the 16 literal p-coordinate source rows, reconstructs the
Delta/Bplus/Au reduction, and independently checks the fraction-free Cramer
obstruction used in the four-parameter all-minor input.  No modular or
characteristic-zero Groebner output is trusted here.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
VOLTA = HERE.parent / "unaudited-codex-k4-cycle-char0-rur-referee-2026-08-21"
DANGER = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
AUDIT_PATH = DANGER / "audit_branch0_cycle_delta_au_open_generic.py"
INPUTS = (
    VOLTA / "cofactor13_all_minors_p1073741827.msolve",
    VOLTA / "cofactor13_all_minors_p1073741789.msolve",
)
LABELS = VOLTA / "cofactor13_all_minors_labels.json"
OUT = HERE / "results_cofactor13_reduced_source_audit.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("k4_cofactor13_independent_source", AUDIT_PATH)
SOURCE = AUDIT.SOURCE
sp = AUDIT.sp


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def poly_sha(poly):
    return sha256(encode(poly).encode("ascii")).hexdigest()


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read_input(path):
    lines = path.read_text().splitlines()
    variables = tuple(value.strip() for value in lines[0].split(","))
    characteristic = int(lines[1])
    rows = tuple(value.strip() for value in
                 "\n".join(lines[2:]).split(",") if value.strip())
    return variables, characteristic, rows


def exact_core(rows):
    derived = AUDIT.derive(rows)
    interface = AUDIT.INTERFACE.derive(rows)
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    unknowns = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    ratio = {b3: x*b1, d3: -x*d1*d4}

    literal = sp.cancel(rows["cofactor_1_3"].subs(ratio)
                        .subs(interface[3]).subs(SOURCE.A0, interface[4]))
    cleared, denominator = literal.as_numer_denom()
    require(sp.factor(denominator) == b0*(b1+d1)**2*(x-1),
            "literal Cof(1,3) clearing denominator changed")
    cleared_poly = sp.Poly(cleared, *unknowns)
    expected_support = {
        (1, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)}
    require({monomial for monomial, _ in cleared_poly.terms()}
            == expected_support, "Cof(1,3) unknown support changed")

    # Keep precisely the source-labelled rows t023,t123,Cof(0,0).  The
    # divisions below are the same six row monomials already proved live by
    # the source interface; no polynomial pivot is divided out.
    row_factors = (b1**2*d1**2*x, 1, 1,
                   d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/row_factors[row])
               for entry in entries]
              for row, entries in enumerate(interface[6])]
    selected = (2, 3, 4)
    coefficient = sp.Matrix([[matrix[row][column] for column in range(3)]
                             for row in selected])
    right = sp.Matrix([-matrix[row][3] for row in selected])
    determinant = sp.expand(coefficient.det(method="domain-ge"))
    numerators = coefficient.adjugate()*right
    require(len(sp.Poly(determinant, b0, b1, x, d1, d4).terms()) == 10,
            "Cramer determinant term count changed")

    ns = sp.symbols("n0 n1 n2")
    ds = sp.Symbol("D")
    homogeneous = 0
    for monomial, scalar in cleared_poly.terms():
        term = scalar*ds**(2-sum(monomial))
        for variable, exponent in zip(ns, monomial, strict=True):
            term *= variable**exponent
        homogeneous += term
    source_replay = sp.expand(homogeneous.subs(
        {ds: determinant,
         **{symbol: determinant*variable for symbol, variable
            in zip(ns, unknowns, strict=True)}}))
    require(sp.expand(source_replay-determinant**2*cleared) == 0,
            "fraction-free source replay failed at the pivot-zero boundary")
    obstruction = sp.expand(homogeneous.subs(
        {ds: determinant,
         **{symbol: numerator for symbol, numerator
            in zip(ns, numerators, strict=True)}}))
    require(len(sp.Poly(obstruction, b0, b1, x, d1, d4).terms()) == 1383,
            "fraction-free obstruction term count changed")

    d4_value = sp.cancel(-interface[1].subs(d4, 0)
                         / sp.diff(interface[1], d4))
    require(sp.cancel(d4_value-derived["d4_value"]) == 0,
            "independent d4 solve disagrees with source audit")
    substituted = sp.cancel(obstruction.subs(d4, d4_value))
    substituted_numerator = substituted.as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(substituted_numerator, b0, domain="QQ(b1,d1,x)"),
        sp.Poly(derived["q"], b0, domain="QQ(b1,d1,x)")).as_expr()
    remainder = sp.cancel(remainder).as_numer_denom()[0]
    remainder_poly = sp.Poly(remainder, b0, b1, d1, x)
    content = tuple(min(monomial[index]
                        for monomial, _ in remainder_poly.terms())
                    for index in range(4))
    require(content == (0, 5, 3, 0),
            "removed chart-live monomial changed")
    monomial = b1**5*d1**3
    core = remainder_poly.exquo(
        sp.Poly(monomial, b0, b1, d1, x)).as_expr()
    core_poly = sp.Poly(core, b0, b1, d1, x)
    require(len(core_poly.terms()) == 7264
            and [core_poly.degree(variable)
                 for variable in (b0, b1, d1, x)] == [1, 8, 31, 26],
            "reduced Cof(1,3) core profile changed")
    return core, {
        "literal_clearing_denominator": str(sp.factor(denominator)),
        "literal_unknown_support": [list(value)
                                    for value in sorted(expected_support)],
        "selected_linear_row_indices": list(selected),
        "selected_linear_row_labels": [interface[5][index]
                                       for index in selected],
        "cramer_determinant_terms": 10,
        "homogeneous_obstruction_terms": 1383,
        "source_identity": "G(D,D*y)=D^2*cleared_Cof13(y)",
        "removed_live_monomial_b0_b1_d1_x": list(content),
        "core_terms": len(core_poly.terms()),
        "core_degrees_b0_b1_d1_x": [core_poly.degree(variable)
                                     for variable in (b0, b1, d1, x)],
        "core_sha256": poly_sha(core),
    }


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    core, metadata = exact_core(rows)
    expected_labels = (["Q"] +
                       ["minor_" + "".join(map(str, selected))
                        for selected in itertools.combinations(range(6), 4)] +
                       ["cofactor_1_3_cramer_homogenized",
                        "live_saturator"])
    frozen_labels = json.loads(LABELS.read_text())["labels"]
    require(frozen_labels == expected_labels,
            "frozen source label ordering changed")
    inputs = []
    common_rows = None
    for path, expected_prime in zip(INPUTS,
                                    (1073741827, 1073741789), strict=True):
        variables, prime, input_rows = read_input(path)
        require(variables == ("b0", "b1", "d1", "x")
                and prime == expected_prime and len(input_rows) == 18,
                "frozen extended input header changed")
        require(input_rows[16] == encode(core),
                "frozen reduced Cof(1,3) row differs byte-for-byte")
        if common_rows is None:
            common_rows = input_rows
        else:
            require(input_rows == common_rows,
                    "two-prime exact integer row ledgers diverged")
        inputs.append({"prime": prime, "path": path.name,
                       "file_sha256": file_sha(path),
                       "core_row_sha256": sha256(
                           input_rows[16].encode("ascii")).hexdigest()})

    # A hostile source mutation must already change the exact cleared
    # Cof(1,3) polynomial, before any Cramer or quotient manipulation.
    mutated_raw = dict(raw["cofactor_1_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["cofactor_1_3"] = SOURCE.expression(mutated_raw)
    original_interface = AUDIT.INTERFACE.derive(rows)
    mutated_interface = AUDIT.INTERFACE.derive(mutated_rows)
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    ratio = {b3: x*b1, d3: -x*d1*d4}
    original_literal = sp.cancel(
        rows["cofactor_1_3"].subs(ratio).subs(original_interface[3])
        .subs(SOURCE.A0, original_interface[4])).as_numer_denom()[0]
    mutated_literal = sp.cancel(
        mutated_rows["cofactor_1_3"].subs(ratio).subs(mutated_interface[3])
        .subs(SOURCE.A0, mutated_interface[4])).as_numer_denom()[0]
    require(sp.expand(original_literal-mutated_literal) != 0,
            "literal Cof(1,3) mutation did not fire")

    result = {
        "status": "UNAUDITED independent exact source replay PASS",
        **metadata,
        "source_row": "cofactor_1_3",
        "input_labels_sha256": file_sha(LABELS),
        "inputs": inputs,
        "must_fire": (
            "Negating the lex-first raw Cof(1,3) coefficient changes the "
            "cleared source polynomial before Cramer reduction."),
        "scope": (
            "This proves the exported four-variable row is a necessary "
            "exact consequence on the declared localized Delta/Bplus/Au "
            "chart, including the selected Cramer pivot-zero boundary. It "
            "does not prove the extended ideal is a unit over Q."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("independent Cof(1,3) reduced-source audit: PASS")
    print("core terms/degrees:", result["core_terms"],
          result["core_degrees_b0_b1_d1_x"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
