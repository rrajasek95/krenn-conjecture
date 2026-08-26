#!/usr/bin/env python3
"""Export the exact pre-pivot D0 gate on R0=R3=0."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "probe_branch0_cycle_d0_c0_generic.py")
INTERFACE = HERE / "results_d0_pivot_zero_interface.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load():
    spec = importlib.util.spec_from_file_location("d0_R0_R3_prepivot_source", GENERIC)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    require(spec.loader is not None, "missing source loader")
    spec.loader.exec_module(module)
    return module


def encode(sp, value):
    return str(sp.expand(value)).replace("**", "^")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def profile(sp, value, variables):
    poly = sp.Poly(value, *variables)
    return {"terms": len(poly.terms()), "total_degree": int(poly.total_degree()),
            "multidegree": [int(poly.degree(variable)) for variable in variables],
            "sha256": sha256(encode(sp, poly.as_expr()).encode()).hexdigest()}


def primitive(sp, value, variables):
    return sp.primitive(sp.Poly(value, *variables))[1].as_expr()


def main():
    P = load()
    sp = P.sp
    source = P.SOURCE
    raw_rows, _ = source.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    expressions = {label: source.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = source.A0, source.A5
    b0, b1, b3, d1, d3, d4 = source.PARAMETERS
    variables = (b0, d1, d4, a0, a5)
    base_variables = (b0, d1, d4)
    c0 = b0**2 + d4**2

    upper_labels = tuple(f"cofactor_{edge}_0" for edge in range(1, 5))
    upper = [expressions[label] for label in upper_labels]
    p_solution = sp.solve(upper, source.P, dict=True, simplify=False)[0]
    d0 = {d3: -d1*d4}

    def endpoint_core(label):
        top = sp.cancel(expressions[label].subs(p_solution).subs(d0)) \
            .as_numer_denom()[0]
        return max((factor for factor, _ in sp.factor_list(top)[1]),
                   key=lambda value:
                   len(sp.Poly(value, b0, b1, b3, d1, d4).terms()))

    endpoint_labels = ("cofactor_0_0", "cofactor_5_0")
    endpoint_rows = [endpoint_core(label) for label in endpoint_labels]
    endpoint_matrix, _ = sp.linear_eq_to_matrix(endpoint_rows, [b1, b3])
    endpoint_determinant = sp.factor(endpoint_matrix.det())
    require(endpoint_determinant == -2*b0*d1*c0,
            "endpoint determinant changed")
    endpoint = sp.solve(endpoint_rows, [b1, b3], dict=True, simplify=False)[0]

    rational_field, _, _, _, _, _ = P.field("b0,d1,d4,a0,a5", P.QQ)
    substitutions = {**d0, **endpoint}
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(substitutions))) for variable in source.P]
    values += [rational_field.from_expr(a0), rational_field.from_expr(a5)]
    values += [rational_field.from_expr(sp.cancel(
        substitutions.get(variable, variable)))
        for variable in source.PARAMETERS]

    declared_denominators = {encode(sp, value) for value in (b0, d1, d4, c0)}

    def evaluate(label):
        answer = rational_field.zero
        for exponents, coefficient in raw[label].items():
            term = rational_field.from_expr(sp.Rational(
                coefficient.numerator, coefficient.denominator))
            for value, power in zip(values, exponents, strict=True):
                term *= value**power
            answer += term
        numerator = primitive(sp, answer.numer.as_expr(), variables)
        denominator = primitive(sp, answer.denom.as_expr(), base_variables)
        denominator_factors = []
        for factor, multiplicity in sp.factor_list(denominator)[1]:
            encoded = encode(sp, factor)
            require(encoded in declared_denominators,
                    f"undeclared pre-pivot denominator in {label}: {encoded}")
            denominator_factors.append({"factor": encoded,
                                        "multiplicity": int(multiplicity)})
        return numerator, denominator_factors

    residual_labels = ("t_012", "t_013", "t_023", "t_123",
                       *(f"cofactor_{edge}_3" for edge in range(6)))
    residual = []
    denominator_records = {}
    for label in residual_labels:
        value, denominators = evaluate(label)
        residual.append(value)
        denominator_records[label] = denominators

    # Crosscheck the six previously frozen pre-pivot rows up to a rational
    # unit; the remaining four are independently evaluated here before any
    # selected-pivot Cramer solve.
    old_variables, old_residual, old_c0 = P.derive()
    old = dict(old_residual)
    require(sp.expand(old_c0-c0) == 0, "C0 crosscheck failed")
    for label in ("t_012", "t_013", "t_023", "t_123",
                  "cofactor_0_3", "cofactor_5_3"):
        new = residual[residual_labels.index(label)]
        require(sp.Poly(new, *variables).monic() ==
                sp.Poly(old[label], *variables).monic(),
                f"pre-pivot row crosscheck failed: {label}")

    interface = json.loads(INTERFACE.read_text())
    frozen_interface = interface.pop("logical_sha256")
    require(logical_hash(interface) == frozen_interface,
            "pivot-zero interface digest mismatch")
    r_records = interface["coefficient_pivot"]["C0_open_residual_factors"]
    R0 = sp.sympify(r_records[0]["polynomial"].replace("^", "**"))
    R3 = sp.sympify(r_records[3]["polynomial"].replace("^", "**"))
    z = sp.Symbol("z")
    base_live = sp.expand(b0*d1*d4*c0)
    localizer = sp.expand(z*base_live - 1)
    rows = [R0, R3, *residual, localizer]
    labels = ["R0", "R3", *residual_labels, "z*b0*d1*d4*C0-1"]
    input_path = HERE / "d0_pivot_zero_R0_R3_char0.msolve"
    input_path.write_text("z,b0,d1,d4,a0,a5\n0\n" +
                          ",\n".join(encode(sp, value) for value in rows) + "\n")
    result = {
        "status": "exact pre-pivot R0=R3 gate export PASS",
        "input": input_path.name,
        "input_sha256": digest(input_path),
        "labels": labels,
        "profiles": [profile(sp, value, (z, *variables)) for value in rows],
        "denominator_records": denominator_records,
        "endpoint_determinant": encode(sp, endpoint_determinant),
        "base_live_product": encode(sp, base_live),
        "interface_logical_sha256": frozen_interface,
        "source": {"path": str(GENERIC), "sha256": digest(GENERIC)},
        "scope": ("D0=0,C0!=0 pre-pivot literal system, R0=R3=0; "
                  "only b0*d1*d4*C0 is localized. No complementary R factor "
                  "and no selected coefficient pivot is localized."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_R0_R3_gate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero R0/R3 export PASS", result["logical_sha256"])
    print("input", input_path.stat().st_size, "bytes", result["input_sha256"])
    print("row terms", [record["terms"] for record in result["profiles"]])


if __name__ == "__main__":
    main()
