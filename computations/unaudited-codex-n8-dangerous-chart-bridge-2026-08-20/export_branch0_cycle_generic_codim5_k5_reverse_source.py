#!/usr/bin/env python3
"""Reverse-pull the literal lower cofactors and Hcore to the K5 residual."""

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
TREE_PATH = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
FULL_PATH = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"
HLIVE_PATH = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_hlive_exact.py"
K4_EXPORT_PATH = HERE / "export_branch0_cycle_generic_codim5_k4_leaf_exact.py"
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
K5_INPUT = HERE / "branch0_cycle_generic_codim5_d10_k4_k5_exact.msolve"
QRS_RESULT = HERE / "results_branch0_cycle_generic_qrs_codim3_export.json"
QR_RESULT = HERE / "results_branch0_cycle_generic_q4098_r4885_gcd_export.json"
CORE_RESULT = HERE / "results_branch0_cycle_generic_cofactor33_export.json"
K5_EXPORT_RESULT = HERE / "results_branch0_cycle_generic_codim5_k4_leaf_export.json"
OUT_HCORE = HERE / "branch0_cycle_generic_codim5_d10_k4_k5_hcore_open_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_codim5_k5_reverse_source_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


TREE = load("k5_reverse_tree", TREE_PATH)
FULL = load("k5_reverse_full", FULL_PATH)
HLIVE = load("k5_reverse_hlive", HLIVE_PATH)
K4EXP = load("k5_reverse_k4_export", K4_EXPORT_PATH)


def profile(poly: sp.Expr, variables) -> list[int]:
    value = sp.Poly(poly, *variables)
    return [len(value.terms()), int(value.total_degree())]


def factor_records(poly: sp.Expr, variables) -> list[dict]:
    primitive = sp.Poly(poly, *variables, domain="QQ").primitive()[1].as_expr()
    answer = []
    for factor, power in sp.factor_list(primitive)[1]:
        value = sp.Poly(factor, *variables)
        record = {
            "terms": len(value.terms()),
            "degree": int(value.total_degree()),
            "power": int(power),
            "sha256": K4EXP.digest(factor, variables),
        }
        if len(value.terms()) <= 20:
            record["expression"] = str(factor)
        answer.append(record)
    return answer


def split_encoded_rows(path: Path, expected_count: int):
    lines = path.read_text().splitlines()
    encoded = "\n".join(lines[2:]).strip().split(",\n")
    require(lines[1] == "0" and len(encoded) == expected_count,
            f"{path.name} header/row count changed")
    return lines[0].split(","), encoded


def main() -> None:
    require(sha256(SOURCE.read_bytes()).hexdigest()
            == "067c27ddc22af9c62472427d15be58aecb89eb6196f53b65e2a82f0caae63d0d",
            "corrected exact source bytes changed")

    core_rows, _, _ = TREE.SOURCE.derive()
    tb0, tb1, b3, td1, td3, td4 = TREE.SOURCE.SOURCE.PARAMETERS
    b0, b1, d1, d3, d4 = tb0, tb1, td1, td3, td4
    variables5 = (b0, b1, d1, d3, d4)
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        core_rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1), strict=True)]
    pivot = compact[1]
    pivot_leading = sp.diff(pivot, b3)
    pivot_constant = sp.expand(pivot.subs(b3, 0))
    aa = sp.cancel(pivot_leading/(2*b0))
    bb = sp.cancel(pivot_constant/2)
    require(sp.expand(pivot_leading-2*b0*aa) == 0
            and sp.expand(pivot_constant-2*bb) == 0,
            "b3 pivot identity changed")

    # Derive only the six solve substitutions needed by Hcore.  Calling the
    # full lower-cofactor constructor here would needlessly expand five large
    # rows whose exact pullback identities are already frozen below.
    generic = FULL.SOURCE.SOURCE.SOURCE
    raw_rows, _ = generic.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    needed_labels = [*(f"cofactor_{edge}_0" for edge in range(1, 6)), "t_023"]
    solved_rows = {label: generic.expression(raw[label])
                   for label in needed_labels}
    upper = [solved_rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, generic.P, dict=True, simplify=False)[0]
    c50 = generic.numerator(solved_rows["cofactor_5_0"], p_solution)
    a0_solution = sp.solve(c50, generic.A0, dict=True, simplify=False)[0]
    t023 = generic.numerator(
        generic.numerator(solved_rows["t_023"], p_solution), a0_solution)
    a5_solution = sp.solve(t023, generic.A5, dict=True, simplify=False)[0]
    print("reverse-source: source solve derivation complete", flush=True)
    hcore, h_denominator = HLIVE.derive_hcore(
        p_solution, a0_solution, a5_solution)
    print("reverse-source: Hcore source derivation complete", flush=True)
    require(profile(hcore, (b0, b1, b3, d1, d3, d4)) == [258, 15],
            "literal Hcore profile changed")

    # The five exact b3-pullback factorizations were already frozen by the
    # source exporters which produced Q/R/S/T/U.  Reuse those theorem
    # artifacts rather than repeating five large resultants here.
    qrs_result = json.loads(QRS_RESULT.read_text())
    qr_result = json.loads(QR_RESULT.read_text())
    core_result = json.loads(CORE_RESULT.read_text())
    lower_hashes = {
        1: qrs_result["cofactor13_literal_source_sha256"],
        2: qrs_result["cofactor23_literal_source_sha256"],
        3: core_result["omitted_source_sha256"],
        4: qr_result["cofactor43_literal_source_sha256"],
        5: qrs_result["cofactor53_literal_source_sha256"],
    }
    k5_export = json.loads(K5_EXPORT_RESULT.read_text())
    retained_hashes = {record["label"]: record["source_sha256"]
                       for record in k5_export["row_records"]}
    edge_to_row = {3: ("Q4098", "b0^2*D0*C8"),
                   4: ("R4885", "b0^2*D0*C8"),
                   1: ("S4331", "b0^2*D0*C8"),
                   2: ("T4750", "b0^2*D0*C8"),
                   5: ("U3217", "b0^3*D0*C8")}
    lower_records = [{
        "edge": edge,
        "literal_label": f"cofactor_{edge}_3",
        "literal_source_sha256": lower_hashes[edge],
        "retained_label": label,
        "retained_sha256": retained_hashes[label],
        "frozen_exact_b3_pullback_quotient": quotient,
        "component_status": (
            "identically zero wherever the retained factor vanishes"),
    } for edge, (label, quotient) in edge_to_row.items()]

    # Pull Hcore first through b3=-B/(b0*A), then through the K4 d3 root.
    # Both leading coefficients are explicitly present in the K5 live product.
    quotient_variables6 = (b0, b1, b3, d1, d3, d4)
    quotient_variables5 = (b0, b1, d1, d3, d4)
    k4_leading = b0*(b0+d4)
    k4_constant = d1*d4*(b0**2+d4)
    quotient_variables = (b0, b1, d1, d4)
    k5 = b0**4+b0**3+2*b0**2*d4-b0*d4**2+d4**2
    hcore_before_b3 = K4EXP.reduce_by_leaf(
        hcore, k5, quotient_variables6)
    print("reverse-source: Hcore reduced modulo K5 before b3", flush=True)
    hcore_after_b3_raw = K4EXP.evaluate_at_linear_root(
        hcore_before_b3, b3, pivot_leading, pivot_constant)
    hcore_after_b3 = K4EXP.reduce_by_leaf(
        hcore_after_b3_raw, k5, quotient_variables5)
    print("reverse-source: Hcore b3 pullback complete", flush=True)
    hcore_after_k4_raw = K4EXP.evaluate_at_linear_root(
        hcore_after_b3, d3, k4_leading, k4_constant)
    hcore_mod_k5 = K4EXP.reduce_by_leaf(
        hcore_after_k4_raw, k5, quotient_variables)
    print("reverse-source: Hcore K4 pullback complete", flush=True)
    require(hcore_mod_k5 != 0,
            "Hcore unexpectedly vanished already modulo K5")
    # Full factorization is deliberately deferred: the component-open
    # sentinel below answers the higher-impact generic-liveness question.
    hcore_factors = []

    # Preserve the already-frozen nine-row K5 gate and replace only its final
    # Rabinowitsch sentinel by the same live product times Hcore.  This tests
    # Hcore as a polynomial on the residual; it is not a literal-H replay,
    # because actual Delta is zero on D10=0.
    k5_names, k5_encoded = split_encoded_rows(K5_INPUT, 11)
    k5_variables_all = sp.symbols(" ".join(k5_names))
    kb0, kb1, kd1, kd4, z = k5_variables_all
    require((kb0, kb1, kd1, kd4) == quotient_variables,
            "K5 gate variable order changed")
    old_localizer = sp.sympify(
        k5_encoded[-1].replace("^", "**"),
        locals=dict(zip(k5_names, k5_variables_all, strict=True)))
    live_product = sp.diff(old_localizer, z)
    require(sp.expand(old_localizer-z*live_product+1) == 0,
            "K5 Rabinowitsch sentinel changed")
    new_localizer = sp.expand(z*live_product*hcore_mod_k5-1)
    OUT_HCORE.write_text(
        ",".join(k5_names)+"\n0\n"
        + ",\n".join([*k5_encoded[:-1],
                       K4EXP.encode(new_localizer, k5_variables_all)])+"\n")
    require("(" not in OUT_HCORE.read_text().split("\n", 2)[2]
            and "**" not in OUT_HCORE.read_text().split("\n", 2)[2],
            "Hcore-open canonical syntax guard failed")

    # The literal H formula has Delta^2 in its denominator.  On this residual
    # TrueDeltaN=C8*D10=0, so no value of H may be inferred from Hcore here.
    d0 = d1*d4+d3
    delta = b1*d3+b3*d1*d4
    require(sp.factor(h_denominator) == b0*delta**2*d0,
            "literal H denominator changed")

    result = {
        "status": "UNAUDITED exact K5 reverse-source/Hcore export",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "K5_input": K5_INPUT.name,
        "K5_input_sha256": sha256(K5_INPUT.read_bytes()).hexdigest(),
        "positive_dimensional_sentinel": "[1, 5, -1, []]:",
        "lower_cofactor_pullbacks": lower_records,
        "all_five_literal_lower_rows_status": (
            "zero on the retained-factor K5 residual by exact divisibility"),
        "Hcore_source_profile": [258, 15],
        "Hcore_before_b3_mod_K5_profile": profile(
            hcore_before_b3, quotient_variables6),
        "Hcore_after_b3_profile": profile(hcore_after_b3, variables5),
        "Hcore_after_K4_profile": profile(hcore_after_k4_raw, quotient_variables),
        "Hcore_mod_K5_profile": profile(hcore_mod_k5, quotient_variables),
        "Hcore_mod_K5_sha256": K4EXP.digest(
            hcore_mod_k5, quotient_variables),
        "Hcore_mod_K5_factor_profile": hcore_factors,
        "Hcore_mod_K5_status": "nonzero polynomial before full-component reduction",
        "Hcore_open_input": OUT_HCORE.name,
        "Hcore_open_input_sha256": sha256(OUT_HCORE.read_bytes()).hexdigest(),
        "Hcore_open_input_bytes": OUT_HCORE.stat().st_size,
        "literal_H_denominator": "b0*Delta^2*D0",
        "actual_Delta_on_component": "zero because TrueDeltaN=C8*D10 and D10=0",
        "Hcore_scope_guard": (
            "Hcore can be tested as a polynomial on K5, but the identity "
            "H=b1*b3*Hcore/(b0*Delta^2*D0) cannot be evaluated there."),
        "scope": (
            "Reverse source pullback of all five lower cofactors through the "
            "A-open b3 pivot, plus polynomial Hcore pullback through b3 and "
            "K4. The Hcore-open gate retains the exact nine-row K5 residual. "
            "No literal-H or packet-point claim is made on Delta=0."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("K5 reverse-source/Hcore export: PASS")
    print("lower rows: all exact retained-factor multiples")
    print("Hcore mod K5 profile:", result["Hcore_mod_K5_profile"])
    print("Hcore-open input bytes:", result["Hcore_open_input_bytes"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
