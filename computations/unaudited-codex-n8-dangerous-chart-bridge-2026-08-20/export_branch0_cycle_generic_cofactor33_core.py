#!/usr/bin/env python3
"""Fraction-free necessary core for the generic k4-cycle interior chart."""

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
GENERIC = HERE.parent / "unaudited-codex-root-integration-2026-08-20" / \
    "discover_branch0_k4_cycle_cramer_generic.py"
OUT = HERE / "branch0_cycle_generic_cofactor33_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_generic_cofactor33_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_cofactor33_export.json"
PRIME = 1073741827


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("cycle_generic_export_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(GENERIC)


def encode(poly: sp.Expr) -> str:
    value = sp.Poly(sp.expand(poly), *SOURCE.PARAMETERS, domain="ZZ")
    pieces: list[str] = []
    for monomial, coefficient in value.terms():
        magnitude = abs(int(coefficient))
        factors = [str(magnitude)] if magnitude != 1 else []
        for variable, power in zip(SOURCE.PARAMETERS, monomial, strict=True):
            if power:
                factors.append(str(variable) if power == 1
                               else f"{variable}^{power}")
        body = "*".join(factors) or "1"
        if not pieces:
            pieces.append(("-" if coefficient < 0 else "") + body)
        else:
            pieces.append(("-" if coefficient < 0 else "+") + body)
    return "".join(pieces) or "0"


def polynomial_sha(poly: sp.Expr) -> str:
    return sha256(encode(poly).encode("ascii")).hexdigest()


def derive():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    compatibility, _ = SOURCE.derive()
    profiles = [(label, len(sp.Poly(poly, *SOURCE.PARAMETERS).terms()),
                 sp.Poly(poly, *SOURCE.PARAMETERS).total_degree())
                for label, poly in compatibility]
    require(profiles == [
        ("t_012", 63, 13), ("t_013", 63, 9), ("t_123", 44, 11),
        ("cofactor_0_0", 72, 12), ("cofactor_0_3", 73, 10)],
        "generic compatibility profile changed")

    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
    c50 = SOURCE.numerator(rows["cofactor_5_0"], p_solution)
    a0_solution = sp.solve(c50, SOURCE.A0, dict=True, simplify=False)[0]
    t023 = SOURCE.numerator(
        SOURCE.numerator(rows["t_023"], p_solution), a0_solution)
    a5_solution = sp.solve(t023, SOURCE.A5, dict=True, simplify=False)[0]

    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    delta = b1*d3 + b3*d1*d4
    d0 = d1*d4 + d3
    bplus = b1 + d1
    denominators = [sp.factor(value.as_numer_denom()[1])
                    for value in p_solution.values()]
    require(denominators == [2*b0*d3*delta, 2*b0*d4*delta,
                             2*b0*d1*delta, 2*b0*delta],
            "upper Cramer denominators changed")
    require(sp.factor(a0_solution[SOURCE.A0].as_numer_denom()[1]) == b0*d0,
            "a0 solve denominator changed")
    require(sp.factor(a5_solution[SOURCE.A5].as_numer_denom()[1])
            == 2*b0*b1*d1*d3*d4*bplus*delta,
            "a5 solve denominator changed")

    literal = SOURCE.numerator(rows["cofactor_3_3"], p_solution)
    literal = SOURCE.numerator(literal, a0_solution)
    literal = SOURCE.numerator(literal, a5_solution)
    literal_poly = sp.Poly(literal, *SOURCE.PARAMETERS)
    require(literal_poly.rem(sp.Poly(delta, *SOURCE.PARAMETERS)).is_zero,
            "omitted cofactor lost Delta factor")
    literal_poly = literal_poly.exquo(sp.Poly(delta, *SOURCE.PARAMETERS))
    require(literal_poly.rem(sp.Poly(b1, *SOURCE.PARAMETERS)).is_zero,
            "omitted cofactor lost chart-live b1 factor")
    omitted = literal_poly.exquo(sp.Poly(b1, *SOURCE.PARAMETERS)).primitive()[1].as_expr()
    omitted_poly = sp.Poly(omitted, *SOURCE.PARAMETERS)
    require(len(omitted_poly.terms()) == 472 and omitted_poly.total_degree() == 15,
            "compact omitted Cof(3,3) profile changed")

    # Hostile literal-source mutation must change the cleared reduced row.
    mutated_raw = dict(raw["cofactor_3_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated = SOURCE.expression(mutated_raw)
    mutated = SOURCE.numerator(mutated, p_solution)
    mutated = SOURCE.numerator(mutated, a0_solution)
    mutated = SOURCE.numerator(mutated, a5_solution)
    require(sp.expand(mutated-literal) != 0,
            "literal Cof(3,3) mutation did not fire")

    # Only actual solve/chart factors are localized. Omitting p_i and 1+p_i
    # makes a UNIT result stronger than the true both-term-live interior claim.
    live_factors = (b0, b1, b3, d1, d3, d4, delta, d0, bplus)
    saturator = sp.expand(sp.prod(live_factors))
    rows_out = [poly for _, poly in compatibility] + [omitted, saturator]
    labels = [label for label, _ in compatibility] + [
        "literal_cofactor_3_3_cleared", "generic_solve_denominator_product"]
    return rows_out, labels, {
        "compatibility_profiles": profiles,
        "omitted_source_label": "cofactor_3_3",
        "omitted_source_sha256": sha256(str(raw["cofactor_3_3"]).encode("ascii")).hexdigest(),
        "omitted_terms": len(omitted_poly.terms()),
        "omitted_total_degree": omitted_poly.total_degree(),
        "omitted_sha256": polynomial_sha(omitted),
        "removed_factors": ["Delta", "b1"],
        "live_factors": [str(factor) for factor in live_factors],
        "saturator_terms": len(sp.Poly(saturator, *SOURCE.PARAMETERS).terms()),
    }


def main() -> None:
    rows, labels, metadata = derive()
    body = ",\n".join(encode(poly) for poly in rows)
    OUT.write_text(",".join(map(str, SOURCE.PARAMETERS)) + f"\n{PRIME}\n" + body + "\n")
    LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")
    result = {
        "status": "UNAUDITED one-prime generic cycle omitted-cofactor export",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "labels": LABELS.name,
        **metadata,
        "scope": (
            "Necessary source core on Delta*D0*Bplus*b0*b1*b3*d1*d3*d4 != 0. "
            "No p_i or 1+p_i localization is used, so UNIT is stronger than the "
            "true both-term-live interior. Modular output remains discovery only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic Cof(3,3) export: PASS")
    print("omitted terms/degree:", metadata["omitted_terms"], metadata["omitted_total_degree"])
    print("input sha256:", result["input_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
