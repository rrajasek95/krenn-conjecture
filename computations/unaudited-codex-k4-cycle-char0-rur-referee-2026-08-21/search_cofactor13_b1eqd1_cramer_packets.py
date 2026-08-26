#!/usr/bin/env python3
"""Search Cramer packets detecting Cof(1,3) on the branch b1=d1.

The previously frozen packet (rows 2,3,4) gives an obstruction divisible
by b1-d1, hence says nothing on this branch.  This script independently
rebuilds the six-row affine packet, imposes b1=d1 and the exact U-solve for
d4, and tests all 20 three-row Cramer homogenizations.  Every retained
polynomial is a necessary consequence even when its Cramer determinant
vanishes; only Laurent monomial content in the declared-live b0,d1,x is
removed.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
DANGER = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
AUDIT_PATH = DANGER / "audit_branch0_cycle_delta_au_open_generic.py"
RESULT = HERE / "results_cofactor13_b1eqd1_cramer_packets.json"
ROWS = HERE / "cofactor13_b1eqd1_cramer_packets.jsonl"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("cofactor13_b1eqd1_packet_audit", AUDIT_PATH)
SOURCE = AUDIT.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial_sha(poly, variables):
    logical = [[[int(value) for value in exponent], str(coefficient)]
               for exponent, coefficient in sp.Poly(poly, *variables).terms()]
    return sha256(json.dumps(logical, separators=(",", ":")).encode()).hexdigest()


def strip_live_monomial(poly, variables):
    p = sp.Poly(poly, *variables)
    content = tuple(min(monomial[index] for monomial, _ in p.terms())
                    for index in range(len(variables)))
    divisor = sp.prod(variable**power
                      for variable, power in zip(variables, content))
    return p.exquo(sp.Poly(divisor, *variables)).as_expr(), content


def derive():
    raw_rows, _ = SOURCE.SOURCE.data()
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    interface = AUDIT.INTERFACE.derive(rows)
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    y = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    variables = (b0, d1, x)
    ratio = {b3: x*b1, d3: -x*d1*d4}

    literal = sp.cancel(rows["cofactor_1_3"].subs(ratio)
                        .subs(interface[3]).subs(SOURCE.A0, interface[4]))
    cleared = literal.as_numer_denom()[0]
    literal_poly = sp.Poly(cleared, *y)
    require(max(sum(m) for m, _ in literal_poly.terms()) == 2,
            "Cof(1,3) degree changed")

    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row])
               for entry in entries]
              for row, entries in enumerate(interface[6])]
    u = interface[1]
    d4_value = sp.cancel(-u.subs(d4, 0)/sp.diff(u, d4))
    branch_subs = {b1: d1, d4: d4_value.subs(b1, d1)}
    matrix = [[sp.cancel(entry.subs(branch_subs)) for entry in row]
              for row in matrix]
    cleared = sp.cancel(cleared.subs(branch_subs)).as_numer_denom()[0]
    literal_poly = sp.Poly(cleared, *y)

    q = (
        b0**2*d1**2*x**3-b0**2*d1**2*x**2
        -2*b0**2*d1*x**3-2*b0**2*d1*x**2
        +b0**2*x**3-b0**2*x**2-d1**2*x**3+d1**2*x**2
        +2*d1*x**2+2*d1*x-x+1)
    n_symbols = sp.symbols("n0 n1 n2")
    d_symbol = sp.Symbol("D")
    template = 0
    for monomial, scalar in literal_poly.terms():
        degree = sum(monomial)
        term = scalar*d_symbol**(2-degree)
        for variable, exponent in zip(n_symbols, monomial, strict=True):
            term *= variable**exponent
        template += term

    records = []
    retained = []
    labels = interface[5]
    # The first exploratory pass found these two compact nonzero packets.
    # Keep this bounded and replayable; this is not advertised as a census
    # of all twenty packets.
    packets = ((0, 1, 2), (0, 1, 4))
    for selected in packets:
        coefficient = sp.Matrix([[matrix[row][column]
                                  for column in range(3)]
                                 for row in selected])
        right = sp.Matrix([-matrix[row][3] for row in selected])
        determinant = sp.cancel(coefficient.det())
        numerators = coefficient.adjugate()*right
        if determinant == 0:
            records.append({"row_indices": list(selected),
                            "row_labels": [labels[i] for i in selected],
                            "status": "zero determinant"})
            continue
        value = sp.cancel(template.subs({
            d_symbol: determinant,
            **{symbol: numerator for symbol, numerator
               in zip(n_symbols, numerators, strict=True)}}))
        numerator = value.as_numer_denom()[0]
        remainder = sp.rem(sp.Poly(numerator, b0, domain="QQ(d1,x)"),
                           sp.Poly(q, b0, domain="QQ(d1,x)")).as_expr()
        remainder = sp.cancel(remainder).as_numer_denom()[0]
        if remainder == 0:
            records.append({"row_indices": list(selected),
                            "row_labels": [labels[i] for i in selected],
                            "status": "zero modulo Q"})
            continue
        core, monomial = strip_live_monomial(remainder, variables)
        p = sp.Poly(core, *variables)
        record = {
            "row_indices": list(selected),
            "row_labels": [labels[i] for i in selected],
            "status": "nonzero",
            "removed_live_monomial_b0_d1_x": list(monomial),
            "terms": len(p.terms()),
            "degrees_b0_d1_x": [p.degree(v) for v in variables],
            "sha256": polynomial_sha(core, variables),
        }
        records.append(record)
        retained.append((record, core))
        print(selected, record["terms"], record["degrees_b0_d1_x"])

    retained.sort(key=lambda item: (item[0]["terms"],
                                    sum(item[0]["degrees_b0_d1_x"])))
    ROWS.write_text("\n".join(json.dumps({
        "row_indices": record["row_indices"],
        "row_labels": record["row_labels"],
        "polynomial": str(sp.expand(poly)).replace("**", "^")},
        separators=(",", ":")) for record, poly in retained) + "\n")
    result = {
        "status": "UNAUDITED exact b1=d1 alternate Cramer packet export",
        "branch": "b1-d1=0",
        "declared_live_removed": ["b0", "d1", "x"],
        "Q": str(q),
        "records": records,
        "retained_rows_path": ROWS.name,
        "retained_rows_sha256": sha256(ROWS.read_bytes()).hexdigest(),
        "searched_packets": [list(value) for value in packets],
        "scope": ("Each nonzero row is a necessary exact consequence of "
                  "the displayed three source rows and Cof(1,3)=0 on the "
                  "b1=d1 chart, including the zero-determinant locus. It "
                  "does not by itself close the branch, and this bounded "
                  "export is not a census of all 20 row triples."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("retained", len(retained), "of", len(packets))
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    derive()
