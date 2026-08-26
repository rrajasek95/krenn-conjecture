#!/usr/bin/env python3
"""Add literal Cof(4,3) to the exact generic-cycle A=B=0 core."""

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
BASE = HERE / "export_branch0_cycle_generic_azero_bzero_exact.py"
OUT = HERE / "branch0_cycle_generic_azero_bzero_cofactor43_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_azero_bzero_cofactor43_export.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_ab_cof43_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(BASE)


def derive_cofactor43() -> tuple[sp.Expr, str]:
    generic = SOURCE.SOURCE.SOURCE
    raw_rows, _ = generic.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: generic.expression(poly) for label, poly, _ in raw_rows}
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, generic.P, dict=True, simplify=False)[0]
    c50 = generic.numerator(rows["cofactor_5_0"], p_solution)
    a0_solution = sp.solve(c50, generic.A0, dict=True, simplify=False)[0]
    t023 = generic.numerator(
        generic.numerator(rows["t_023"], p_solution), a0_solution)
    a5_solution = sp.solve(t023, generic.A5, dict=True, simplify=False)[0]
    value = generic.numerator(rows["cofactor_4_3"], p_solution)
    value = generic.numerator(value, a0_solution)
    value = generic.numerator(value, a5_solution)
    b0, b1, b3, d1, d3, d4 = generic.PARAMETERS
    delta = b1*d3+b3*d1*d4
    poly = sp.Poly(value, *generic.PARAMETERS)
    require(poly.rem(sp.Poly(delta, *generic.PARAMETERS)).is_zero,
            "Cof(4,3) Delta factor changed")
    poly = poly.exquo(sp.Poly(delta, *generic.PARAMETERS))
    require(poly.rem(sp.Poly(b1, *generic.PARAMETERS)).is_zero,
            "Cof(4,3) live b1 factor changed")
    reduced = poly.exquo(sp.Poly(b1, *generic.PARAMETERS)).primitive()[1].as_expr()
    profile = sp.Poly(reduced, *generic.PARAMETERS)
    require(len(profile.terms()) == 472 and profile.total_degree() == 16,
            "Cof(4,3) reduced profile changed")
    # Literal source mutation must change the reduced numerator before use.
    mutated_raw = dict(raw["cofactor_4_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated = generic.expression(mutated_raw)
    mutated = generic.numerator(mutated, p_solution)
    mutated = generic.numerator(mutated, a0_solution)
    mutated = generic.numerator(mutated, a5_solution)
    require(sp.expand(mutated-value) != 0, "literal Cof(4,3) mutation did not fire")
    return reduced, sha256(str(raw["cofactor_4_3"]).encode("ascii")).hexdigest()


def main() -> None:
    rows, labels, metadata = SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    a_divisor = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    b_polynomial = sp.cancel(normalized_t013.subs(b3, 0)/2)
    cofactor43, source_sha = derive_cofactor43()
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    z = sp.Symbol("z")
    variables = (*SOURCE.SOURCE.SOURCE.PARAMETERS, z)
    generators = (*source_rows, a_divisor, b_polynomial, cofactor43,
                  sp.expand(z*live-1))
    OUT.write_text(
        ",".join(map(str, variables)) + "\n0\n"
        + ",\n".join(SOURCE.encode(poly, variables) for poly in generators) + "\n")
    body = OUT.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "canonical msolve syntax guard failed")
    result = {
        "status": "UNAUDITED exact-Q A=B=0 plus Cof(4,3) export",
        "input": OUT.name,
        "input_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "source_row_labels": labels[:6],
        "source_omitted_cofactor33_sha256": metadata["omitted_sha256"],
        "added_literal_row": "cofactor_4_3",
        "added_literal_source_sha256": source_sha,
        "added_row_terms_degree": [472, 16],
        "added_row_sha256": sha256(SOURCE.encode(cofactor43, variables).encode("ascii")).hexdigest(),
        "localized_factors": ["b0", "b1", "b3", "d1", "d3", "d4",
                              "Delta", "D0", "Bplus"],
        "scope": (
            "Necessary A=B=0 generic-cycle core with the next literal omitted "
            "Cof(4,3) row added. This is not a full packet point test; other "
            "omitted lower cofactors and Q4098 remain out of scope."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A=B=0 + Cof(4,3) exact export: PASS")
    print("input sha256:", result["input_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
