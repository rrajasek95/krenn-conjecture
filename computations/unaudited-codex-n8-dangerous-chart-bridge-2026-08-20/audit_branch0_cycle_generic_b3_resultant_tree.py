#!/usr/bin/env python3
"""Exact one-level b3 resultant tree for the generic cycle core."""

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
EXPORTER = HERE / "export_branch0_cycle_generic_cofactor33_core.py"
RESULT = HERE / "results_branch0_cycle_generic_b3_resultant_tree.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_b3_tree_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(EXPORTER)


def linear_resultant(poly: sp.Expr, variable: sp.Symbol,
                     leading: sp.Expr, constant: sp.Expr) -> sp.Expr:
    source = sp.Poly(poly, variable)
    degree = source.degree()
    answer = 0
    for (power,), coefficient in source.terms():
        answer += coefficient*(-constant)**power*leading**(degree-power)
    answer = sp.expand(answer)
    # For A*x+B, this is the defining closed formula
    # Res_x(A*x+B,f)=A^deg(f) f(-B/A); no division is performed.
    require(answer != 0, "fraction-free linear resultant vanished")
    return answer


def encode(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> str:
    value = sp.Poly(poly, *variables, domain="QQ").primitive()[1]
    pieces = []
    for monomial, coefficient in value.terms():
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for variable, power in zip(variables, monomial, strict=True):
            if power:
                factors.append(str(variable) if power == 1
                               else f"{variable}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else "")) + body)
    return "".join(pieces)


def sha(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> str:
    return sha256(encode(poly, variables).encode("ascii")).hexdigest()


def main() -> None:
    rows, labels, export_metadata = SOURCE.derive()
    require(export_metadata["omitted_source_label"] == "cofactor_3_3",
            "generic source provenance changed")
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.PARAMETERS
    variables = (b0, b1, d1, d3, d4)
    live_monomials = (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1)
    compact = [sp.cancel(poly/factor)
               for poly, factor in zip(rows, live_monomials, strict=True)]
    for poly, factor, original in zip(compact, live_monomials, rows, strict=True):
        require(sp.expand(poly*factor-original) == 0,
                "live-monomial normalization failed")

    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    require(sp.expand(pivot-leading*b3-constant) == 0,
            "t_013 is no longer affine in b3")
    pivot_divisor = sp.cancel(leading/(2*b0))
    pivot_constant = sp.cancel(constant/2)
    require(len(sp.Poly(pivot_divisor, *variables).terms()) == 19
            and sp.Poly(pivot_divisor, *variables).total_degree() == 6,
            "pivot divisor profile changed")
    require(len(sp.Poly(pivot_constant, *variables).terms()) == 44
            and sp.Poly(pivot_constant, *variables).total_degree() == 7,
            "pivot constant profile changed")

    expected = {
        "t_012": [(2, 2, 1), (1, 1, 2), (851, 18, 1)],
        "t_123": [(1, 1, 1), (1342, 20, 1)],
        "cofactor_0_0": [(1, 1, 1), (324, 15, 1)],
        "cofactor_0_3": [(1, 1, 1), (1846, 21, 1)],
        "literal_cofactor_3_3_cleared": [
            (2, 2, 1), (1, 1, 2), (8, 4, 1), (4098, 26, 1)],
    }
    records = []
    small_quartic = None
    for index, (label, poly) in enumerate(zip(labels, compact, strict=True)):
        if index in (1, 6):
            continue
        resultant = linear_resultant(poly, b3, leading, constant)
        primitive = sp.Poly(resultant, *variables).primitive()[1].as_expr()
        scalar, factors = sp.factor_list(primitive)
        replay = sp.expand(scalar*sp.prod(factor**power
                                          for factor, power in factors))
        require(sp.expand(replay-primitive) == 0,
                f"{label} exact factor replay failed")
        profile = [(len(sp.Poly(factor, *variables).terms()),
                    sp.Poly(factor, *variables).total_degree(), power)
                   for factor, power in factors]
        require(profile == expected[label], f"{label} factor profile changed")
        factor_records = []
        for factor, power in factors:
            item = {
                "terms": len(sp.Poly(factor, *variables).terms()),
                "degree": sp.Poly(factor, *variables).total_degree(),
                "power": int(power),
                "sha256": sha(factor, variables),
            }
            if item["terms"] <= 8:
                item["expression"] = str(factor)
            factor_records.append(item)
            if label == "literal_cofactor_3_3_cleared" \
                    and item["terms"] == 8:
                small_quartic = factor
        records.append({
            "label": label,
            "resultant_terms": len(sp.Poly(primitive, *variables).terms()),
            "resultant_degree": sp.Poly(primitive, *variables).total_degree(),
            "resultant_sha256": sha(primitive, variables),
            "factors": factor_records,
        })
    require(small_quartic is not None, "small quartic split was not found")

    result = {
        "status": "UNAUDITED exact generic-cycle b3 resultant tree",
        "source_export_result_sha256": export_metadata["omitted_sha256"],
        "pivot_label": "t_013",
        "pivot_identity": "t_013_normalized = 2*b0*(A*b3+B)",
        "pivot_divisor_A": str(pivot_divisor),
        "pivot_divisor_terms_degree": [19, 6],
        "pivot_divisor_sha256": sha(pivot_divisor, variables),
        "pivot_constant_terms_degree": [44, 7],
        "pivot_constant_sha256": sha(pivot_constant, variables),
        "resultants": records,
        "smallest_new_split": {
            "source": "Res_b3(t_013,Cof(3,3))/(b0^2*D0)",
            "left_terms_degree": [8, 4],
            "left_expression": str(small_quartic),
            "left_sha256": sha(small_quartic, variables),
            "right_terms_degree": [4098, 26],
        },
        "scope": (
            "On the frozen b0*b1*b3*d1*d3*d4*Delta*D0*Bplus-open generic "
            "cycle branch, split first at A=0. On A!=0 eliminate b3 exactly. "
            "The Cof(3,3) resultant then splits into the displayed quartic "
            "or a degree-26 factor after removing only live b0^2*D0. No "
            "emptiness is claimed on either residual branch."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic b3 resultant tree: PASS")
    print("small quartic:", small_quartic)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
