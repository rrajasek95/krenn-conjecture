#!/usr/bin/env python3
"""Export the exact Delta-open, selected-pivot-zero R0=R1 gate."""

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
DELTA_SCOPE = HERE / "results_d0_pivot_zero_delta_scope.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load():
    spec = importlib.util.spec_from_file_location("d0_R0_R1_literal_source", GENERIC)
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
    interface = json.loads(INTERFACE.read_text())
    interface_hash = interface.pop("logical_sha256")
    require(logical_hash(interface) == interface_hash, "interface digest mismatch")
    delta_scope = json.loads(DELTA_SCOPE.read_text())
    delta_hash = delta_scope.pop("logical_sha256")
    require(logical_hash(delta_scope) == delta_hash, "Delta-scope digest mismatch")

    source = P.SOURCE
    raw_rows, _ = source.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    expressions = {label: source.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = source.A0, source.A5
    b0, b1, b3, d1, d3, d4 = source.PARAMETERS
    variables = (b0, d1, d4, a0, a5)
    base_variables = (b0, d1, d4)
    c0 = b0**2+d4**2
    r_records = interface["coefficient_pivot"]["C0_open_residual_factors"]
    R = [sp.sympify(record["polynomial"].replace("^", "**"))
         for record in r_records]
    R0, R1, _, R3 = R

    upper = [expressions[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    upper_matrix, _ = sp.linear_eq_to_matrix(upper, source.P)
    delta = b1*d3+b3*d1*d4
    require(sp.expand(upper_matrix.det() -
        4*b0**2*b1*b3*d1*d3*d4*delta**2) == 0,
        "upper Cramer determinant changed")
    p_solution = sp.solve(upper, source.P, dict=True, simplify=False)[0]
    d0 = {d3: -d1*d4}

    def endpoint_core(label):
        top = sp.cancel(expressions[label].subs(p_solution).subs(d0)) \
            .as_numer_denom()[0]
        return max((factor for factor, _ in sp.factor_list(top)[1]),
                   key=lambda value:
                   len(sp.Poly(value, b0, b1, b3, d1, d4).terms()))

    endpoint_rows = [endpoint_core(label)
                     for label in ("cofactor_0_0", "cofactor_5_0")]
    endpoint_matrix, _ = sp.linear_eq_to_matrix(endpoint_rows, [b1, b3])
    require(sp.factor(endpoint_matrix.det()) == -2*b0*d1*c0,
            "endpoint determinant changed")
    endpoint = sp.solve(endpoint_rows, [b1, b3], dict=True,
                        simplify=False)[0]
    delta_reduced = sp.cancel(delta.subs(d0).subs(endpoint))
    require(sp.cancel(delta_reduced-d4*R3/(2*b0*c0)) == 0,
            "Delta=R3 relation changed")

    rational_field, _, _, _, _, _ = P.field("b0,d1,d4,a0,a5", P.QQ)
    substitutions = {**d0, **endpoint}
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(substitutions))) for variable in source.P]
    values += [rational_field.from_expr(a0), rational_field.from_expr(a5)]
    values += [rational_field.from_expr(sp.cancel(
        substitutions.get(variable, variable)))
        for variable in source.PARAMETERS]

    declared = [b0, d1, d4, c0, R3]
    declared_monic = [sp.Poly(value, *base_variables).monic() for value in declared]

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
        factors = []
        for factor, multiplicity in sp.factor_list(denominator)[1]:
            monic = sp.Poly(factor, *base_variables).monic()
            require(any(monic == known for known in declared_monic),
                    f"undeclared denominator in {label}: {factor}")
            factors.append({"factor": encode(sp, factor),
                            "multiplicity": int(multiplicity)})
        return numerator, factors

    residual_labels = ("t_012", "t_013", "t_023", "t_123",
                       *(f"cofactor_{edge}_3" for edge in range(6)))
    residual, denominator_records = [], {}
    for label in residual_labels:
        value, factors = evaluate(label)
        residual.append(value)
        denominator_records[label] = factors

    # Six-row crosscheck against the frozen pre-selected-pivot packet.
    _, frozen_rows, frozen_c0 = P.derive()
    frozen_rows = dict(frozen_rows)
    require(sp.expand(frozen_c0-c0) == 0, "C0 crosscheck failed")
    for label in ("t_012", "t_013", "t_023", "t_123",
                  "cofactor_0_3", "cofactor_5_3"):
        value = residual[residual_labels.index(label)]
        require(sp.Poly(value, *variables).monic() ==
                sp.Poly(frozen_rows[label], *variables).monic(),
                f"literal packet crosscheck failed: {label}")

    z = sp.Symbol("z")
    guaranteed_live = sp.expand(b0*d1*d4*c0*R3)
    localizer = sp.expand(z*guaranteed_live-1)
    rows = [R0, R1, *residual, localizer]
    labels = ["R0", "R1", *residual_labels,
              "z*b0*d1*d4*C0*R3-1"]
    input_path = HERE / "d0_pivot_zero_R0_R1_char0.msolve"
    input_path.write_text("z,b0,d1,d4,a0,a5\n0\n" +
                          ",\n".join(encode(sp, value) for value in rows) + "\n")
    result = {
        "status": "exact Delta-open pre-pivot R0=R1 gate export PASS",
        "input": input_path.name, "input_sha256": digest(input_path),
        "labels": labels,
        "profiles": [profile(sp, value, (z, *variables)) for value in rows],
        "denominator_records": denominator_records,
        "guaranteed_live_product": encode(sp, guaranteed_live),
        "guaranteed_live_profile": profile(sp, guaranteed_live, base_variables),
        "explicit_nonlocalization": ["R2"],
        "interface_logical_sha256": interface_hash,
        "delta_scope_logical_sha256": delta_hash,
        "source": {"path": str(GENERIC), "sha256": digest(GENERIC)},
        "scope": ("Corrected O1 representative R0=R1=0 in the Delta-open, "
                  "D0=0,C0!=0 selected-pivot-zero branch. Only guaranteed "
                  "b0*d1*d4*C0*R3 is localized; R2 is not localized."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_R0_R1_gate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero R0/R1 export PASS", result["logical_sha256"])
    print("input", input_path.stat().st_size, "bytes", result["input_sha256"])
    print("terms", [record["terms"] for record in result["profiles"]])


if __name__ == "__main__":
    main()
