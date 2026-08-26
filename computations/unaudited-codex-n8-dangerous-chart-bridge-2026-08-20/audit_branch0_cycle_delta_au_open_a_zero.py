#!/usr/bin/env python3
"""Exact source-derived unit closure of A=0 in the Au-open Delta chart.

For Q=b0^2*x^2*A+C, the divisor A=0 and Q=0 forces either
q_i=d1^2+1=0 or q_2=d1^2+2*d1-1=0.  On the two branches x=-1 and
x=2*d1+5 respectively.  Substitute the exact U-solve for d4 into the
six-row augmented packet, retain all four selected-term localizers, and
compute an exact-Q Groebner basis.  Both ideals are units; no pure Hafnian
row or localization is used.  A sparse source lift is not claimed.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_delta_au_open_a_zero.json"
INTERFACE_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTERFACE = load("n8_cycle_delta_a_zero_interface", INTERFACE_PATH)
SOURCE = INTERFACE.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def singular(poly):
    return str(sp.expand(poly)).replace("**", "^")


def reduce_d1(poly, q, d1, coefficient_variables):
    domain = "QQ[" + ",".join(map(str, coefficient_variables)) + "]"
    return sp.rem(sp.Poly(sp.expand(poly), d1, domain=domain),
                  sp.Poly(q, d1, domain=domain)).as_expr()


def branch_packet(normalized, p3_p4, branch, symbols):
    (p1, p2, p3, p4, a5, b0, b1, x, d1, d4) = symbols
    q = branch["q"]
    x_value = branch["x"]
    numerator = branch["d4_numerator"]
    denominator = branch["d4_denominator"]
    coefficient_variables = (b0, b1, p1, p2, a5)

    matrix = []
    for row in normalized:
        power = max(sp.Poly(entry, d4).degree() if entry else 0
                    for entry in row)
        specialized = []
        for entry in row:
            value = sp.cancel(sp.expand(
                entry.subs(x, x_value).subs(d4, numerator/denominator)
                * denominator**power)).as_numer_denom()[0]
            specialized.append(reduce_d1(
                value, q, d1, coefficient_variables))
        matrix.append(specialized)

    equations = [sp.expand(row[0]*p1 + row[1]*p2
                           + row[2]*a5 + row[3])
                 for row in matrix]
    selected_numerators = [p1+1, p2+1]
    for variable in (p3, p4):
        value = sp.cancel(p3_p4[variable].subs(
            {x: x_value, d4: numerator/denominator}) + 1)
        selected_numerators.append(reduce_d1(
            value.as_numer_denom()[0], q, d1,
            coefficient_variables))

    au = -b0*d1*x-b0*x-d1*x-1
    au_value = reduce_d1(au.subs(x, x_value), q, d1,
                         coefficient_variables)
    live_factors = [*selected_numerators, b0, b1, b1+d1,
                    numerator, denominator, au_value]
    live = sp.expand(sp.prod(live_factors))
    z = sp.Symbol("z")
    generators = [q, *equations, z*live-1]
    return matrix, selected_numerators, live_factors, generators, (z,)


def exact_unit(name, generators, ring_variables):
    program = (
        f"ring R=0,({','.join(map(str, ring_variables))}),dp;"
        "option(redSB);"
        f"ideal I={','.join(singular(value) for value in generators)};"
        "ideal G=slimgb(I);"
        "if(size(G)!=1 || G[1]!=1 || dim(G)!=-1)"
        '{print("UNIT_BASIS_FAILED");exit(1);}'
        'print("UNIT_BASIS_PASS");print(size(G));print(dim(G));quit;'
    )
    completed = subprocess.run(
        ["Singular", "-q", "--no-warn"], input=program, text=True,
        capture_output=True, timeout=180, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"{name}: Singular failed: {completed.stderr[-1000:]}")
    require("UNIT_BASIS_PASS\n1\n-1" in completed.stdout,
            f"{name}: exact unit-basis guard failed: {completed.stdout[-1000:]}")
    return {
        "exact_Q_unit_basis": True,
        "basis_size": 1,
        "basis_dimension": -1,
        "source_lift": "not frozen; liftstd and targeted lift timed out",
    }


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    derived = INTERFACE.derive(rows)
    normalized = derived[6]
    p3_p4 = derived[3]
    p1, p2, p3, p4 = SOURCE.P
    a5 = SOURCE.A5
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")

    # Rebuild the exact A,C divisor split from Q.
    u, v = derived[1], derived[2]
    q_full = sp.factor(sp.resultant(u, v, d4)/b0)
    a = sp.Poly(q_full, b0).coeff_monomial(b0**2)/x**2
    c = sp.Poly(q_full, b0).coeff_monomial(1)
    split = sp.factor(sp.resultant(a, c, x))
    require(split == 16*d1**2*(d1**2+1)*(d1**2+2*d1-1),
            "the A=0 divisor split changed")

    branches = [
        {"name": "qi", "q": d1**2+1, "x": -1,
         "d4_numerator": -b0*(b0*d1-b0-d1-1),
         "d4_denominator": -b0*d1-b0-d1+1,
         "expected_terms": [2, 32, 32, 9, 68, 14, 34, 1333]},
        {"name": "q2", "q": d1**2+2*d1-1, "x": 2*d1+5,
         "d4_numerator": -b0*(b0*d1+3*b0+d1+1),
         "d4_denominator": 3*b0*d1+7*b0+d1+3,
         "expected_terms": [3, 32, 32, 11, 72, 24, 69, 1405]},
    ]
    records = []
    symbols = (p1, p2, p3, p4, a5, b0, b1, x, d1, d4)
    for branch in branches:
        matrix, selected, live_factors, generators, inverses = branch_packet(
            normalized, p3_p4, branch, symbols)
        ring_variables = (p1, p2, a5, b0, b1, d1, *inverses)
        terms = [len(sp.Poly(value, *ring_variables).terms())
                 for value in generators]
        require(terms == branch["expected_terms"],
                f"{branch['name']}: generator census changed: {terms}")
        unit = exact_unit(branch["name"], generators, ring_variables)
        records.append({
            "name": branch["name"],
            "minimal_polynomial": str(branch["q"]),
            "x": str(branch["x"]),
            "d4_numerator": str(branch["d4_numerator"]),
            "d4_denominator": str(branch["d4_denominator"]),
            "generator_terms": terms,
            "selected_numerator_terms": [
                len(sp.Poly(value, p1, p2, a5, b0, b1, d1).terms())
                for value in selected],
            "live_factor_terms": [len(sp.Poly(
                value, p1, p2, a5, b0, b1, d1).terms())
                for value in live_factors],
            **unit,
        })

    # Literal source mutation: only Cof(0,3)'s normalized row changes.
    mutated_raw = dict(raw["cofactor_0_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["cofactor_0_3"] = SOURCE.expression(mutated_raw)
    mutated_normalized = INTERFACE.derive(mutated_rows)[6]
    require(normalized[:-1] == mutated_normalized[:-1]
            and normalized[-1] != mutated_normalized[-1],
            "the literal Cof(0,3) mutation did not fire")

    result = {
        "status": "UNAUDITED exact source-derived unit closure of A=0 divisor",
        "assumptions": [
            "branch0 four-cycle interior chart", "Delta=0",
            "Bplus nonzero", "Au nonzero", "A=0",
            "all four selected-term factors nonzero",
            "displayed solve/chart factors nonzero"],
        "A": str(a),
        "A_C_resultant": str(split),
        "records": records,
        "uses_pure_H": False,
        "scope": (
            "This closes all of the quadratic-leading divisor A=0 in the "
            "Au-open Delta chart. It does not close the remaining proper "
            "resultant-norm divisor on A!=0."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au-open A=0 closure: PASS")
    print("unit bases:", [(record["name"], record["basis_size"])
                          for record in records])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
