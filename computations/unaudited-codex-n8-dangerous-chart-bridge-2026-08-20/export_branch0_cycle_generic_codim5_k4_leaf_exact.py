#!/usr/bin/env python3
"""Export sound exact-Q gates for the two apparent K4 leaves.

The D10/K4 intersection has a useful identity which must be used before the
tempting b1 solve.  On K4=0, after clearing the d3 pivot denominator,

    b0*(b0+d4)*D10 = -d1*d4*(b1+d1)*K5.

Thus the original Bplus-open chart forces K5=0.  In particular the N14 leaf
away from K5 is already empty, while on K5 both coefficients of the affine
D10 equation in b1 vanish.  Cancelling them to obtain b1=-d1 would therefore
be unsound (and would also contradict Bplus!=0).  The K5 gate consequently
retains b1 and eliminates only d3 through the K4 pivot.
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
TREE_PATH = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
OUT_K5 = HERE / "branch0_cycle_generic_codim5_d10_k4_k5_exact.msolve"
OUT_N14 = HERE / "branch0_cycle_generic_codim5_d10_k4_n14_off_k5_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_codim5_k4_leaf_export.json"


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


TREE = load("codim5_k4_leaf_tree", TREE_PATH)


def primitive(poly: sp.Expr, variables) -> sp.Expr:
    return sp.Poly(sp.expand(poly), *variables, domain="ZZ").primitive()[1].as_expr()


def encode(poly: sp.Expr, variables) -> str:
    value = sp.Poly(sp.expand(poly), *variables, domain="ZZ")
    pieces = []
    for monomial, coefficient in value.terms():
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for variable, power in zip(variables, monomial, strict=True):
            if power:
                factors.append(str(variable) if power == 1
                               else f"{variable}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def digest(poly: sp.Expr, variables) -> str:
    return sha256(encode(primitive(poly, variables), variables).encode("ascii")).hexdigest()


def profile(poly: sp.Expr, variables) -> list[int]:
    value = sp.Poly(poly, *variables)
    return [len(value.terms()), int(value.total_degree())]


def evaluate_at_linear_root(poly: sp.Expr, variable: sp.Symbol,
                            leading: sp.Expr, constant: sp.Expr) -> sp.Expr:
    """Return leading^degree*poly(variable=-constant/leading)."""
    source = sp.Poly(poly, variable)
    degree = source.degree()
    return sp.expand(sum(
        coefficient*(-constant)**power*leading**(degree-power)
        for (power,), coefficient in source.terms()))


def reduce_by_leaf(poly: sp.Expr, leaf: sp.Expr, variables) -> sp.Expr:
    quotients, remainder = sp.reduced(
        sp.Poly(poly, *variables, domain="QQ"),
        [sp.Poly(leaf, *variables, domain="QQ")])
    require(sp.expand(poly-quotients[0].as_expr()*leaf-remainder.as_expr()) == 0,
            "leaf reduction identity failed")
    return primitive(remainder.as_expr(), variables)


def write_msolve(path: Path, variables, equations) -> None:
    path.write_text(
        ",".join(map(str, variables)) + "\n0\n"
        + ",\n".join(encode(poly, variables) for poly in equations) + "\n")
    body = path.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "canonical msolve syntax guard failed")


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    require(lines[:2] == ["b0,b1,d1,d3,d4,z", "0"],
            "corrected exact source header changed")
    require(sha256(SOURCE.read_bytes()).hexdigest()
            == "067c27ddc22af9c62472427d15be58aecb89eb6196f53b65e2a82f0caae63d0d",
            "corrected exact source bytes changed")
    b0, b1, d1, d3, d4, source_z = sp.symbols(lines[0].replace(",", " "))
    source_variables = (b0, b1, d1, d3, d4)
    local = {str(v): v for v in (*source_variables, source_z)}
    encoded_rows = "\n".join(lines[2:]).strip().split(",\n")
    require(len(encoded_rows) == 10, "corrected exact source row count changed")
    rows = [sp.sympify(row.replace("^", "**"), locals=local)
            for row in encoded_rows[:9]]
    row_labels = ["P851", "P1342", "P324", "P1846", "Q4098",
                  "R4885", "S4331", "T4750", "U3217"]
    require([len(sp.Poly(row, *source_variables).terms()) for row in rows]
            == [851, 1342, 324, 1846, 4098, 4885, 4331, 4750, 3217],
            "literal retained row profiles changed")

    core_rows, _, _ = TREE.SOURCE.derive()
    tb0, tb1, b3, td1, td3, td4 = TREE.SOURCE.SOURCE.PARAMETERS
    require((tb0, tb1, td1, td3, td4) == source_variables,
            "tree/source variable identity changed")
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        core_rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1), strict=True)]
    pivot = compact[1]
    pivot_leading = sp.diff(pivot, b3)
    pivot_constant = sp.expand(pivot.subs(b3, 0))
    aa = sp.cancel(pivot_leading/(2*b0))
    bb = sp.cancel(pivot_constant/2)

    d0 = d1*d4+d3
    bplus = b1+d1
    d10 = (b0**2*b1*d1*d4 + 2*b0**2*b1*d3
           - b0**2*d1**2*d4 - b0*b1*d1*d4 + b0*b1*d3*d4
           - b0*d1**2*d4 - b0*d1*d3*d4 + 2*b1*d1*d4**2
           + b1*d3*d4 + d1*d3*d4)
    k4_leading = b0*(b0+d4)
    k4_constant = d1*d4*(b0**2+d4)
    k4 = sp.expand(k4_leading*d3+k4_constant)
    k5 = (b0**4+b0**3+2*b0**2*d4-b0*d4**2+d4**2)
    n14 = (b0**6*d1+b0**6-b0**5*d1+2*b0**5*d4-b0**5
           -b0**4*d1*d4-b0**3*d1*d4**2-b0**3*d1*d4
           +3*b0**3*d4**2-3*b0**2*d1*d4**2+b0**2*d4**2
           -b0*d1*d4**3+2*b0*d4**3-d1*d4**3)

    quotient_variables = (b0, b1, d1, d4)
    cleared_d10 = evaluate_at_linear_root(
        d10, d3, k4_leading, k4_constant)
    require(sp.expand(cleared_d10+d1*d4*bplus*k5) == 0,
            "K4/D10/K5 structural identity changed")
    require(sp.expand(evaluate_at_linear_root(
        k4, d3, k4_leading, k4_constant)) == 0,
        "K4 root substitution ceased to vanish")

    # The b1 solve becomes 0/0 exactly on K5.  Audit this explicitly rather
    # than cancelling to the spurious root b1=-d1.
    d10_poly = sp.Poly(d10, b1)
    l6 = d10_poly.coeff_monomial(b1)
    c4 = d10_poly.coeff_monomial(1)
    cleared_l6 = evaluate_at_linear_root(l6, d3, k4_leading, k4_constant)
    cleared_c4 = evaluate_at_linear_root(c4, d3, k4_leading, k4_constant)
    require(sp.expand(cleared_l6+d1*d4*k5) == 0
            and sp.expand(cleared_c4+d1**2*d4*k5) == 0,
            "D10 affine coefficients on K4 changed")

    raw_mapped_rows = [evaluate_at_linear_root(
        row, d3, k4_leading, k4_constant) for row in rows]
    reduced_k5_rows = [reduce_by_leaf(
        row, k5, quotient_variables) for row in raw_mapped_rows]

    live_source_factors = [b0, b1, d1, d3, d4, d0, bplus, aa, bb]
    live_source_labels = ["b0", "b1", "d1", "d3", "d4", "D0",
                          "Bplus", "A", "B"]
    mapped_live = [primitive(evaluate_at_linear_root(
        factor, d3, k4_leading, k4_constant), quotient_variables)
        for factor in live_source_factors]
    # The K4 pivot coefficient itself must be live for this parametrization.
    # b0 is already present; b0+d4 is added explicitly.
    mapped_live.append(b0+d4)
    mapped_live_labels = [*live_source_labels, "K4_d3_pivot_b0_plus_d4"]
    require(all(factor != 0 for factor in mapped_live),
            "a declared live factor vanished under the K4 solve")
    live_product = sp.expand(sp.prod(mapped_live))

    z = sp.Symbol("z")
    out_variables = (*quotient_variables, z)
    localizer_k5 = sp.expand(z*live_product-1)
    equations_k5 = (*reduced_k5_rows, k5, localizer_k5)
    write_msolve(OUT_K5, out_variables, equations_k5)

    # N14 away from K5 is empty already from D10=0 and the live factors
    # d1,d4,Bplus,K5.  Keep the literal mapped retained rows in this small
    # gate nonetheless, so its source coverage is identical to the K5 gate.
    live_product_n14 = sp.expand(live_product*k5)
    localizer_n14 = sp.expand(z*live_product_n14-1)
    reduced_n14_rows = [reduce_by_leaf(
        row, n14, quotient_variables) for row in raw_mapped_rows]
    equations_n14 = (*reduced_n14_rows, n14, cleared_d10, localizer_n14)
    write_msolve(OUT_N14, out_variables, equations_n14)

    # The omitted K4-pivot companion is also exactly empty.  With b0 live,
    # b0+d4=0 and K4=0 imply d4=-b0 and b0=1; D10 then equals
    # 2*d1*(b1+d1), contradicting the live d1 and Bplus factors.
    exceptional_k4 = sp.factor(k4.subs(d4, -b0))
    exceptional_d10 = sp.factor(d10.subs({b0: 1, d4: -1}))
    require(exceptional_k4 == -b0**2*d1*(b0-1)
            and exceptional_d10 == 2*d1*bplus,
            "K4 pivot-companion unit identity changed")

    row_records = []
    for label, source_row, raw, reduced in zip(
            row_labels, rows, raw_mapped_rows, reduced_k5_rows, strict=True):
        row_records.append({
            "label": label,
            "source_sha256": digest(source_row, source_variables),
            "mapped_raw_profile": profile(raw, quotient_variables),
            "mapped_raw_sha256": digest(raw, quotient_variables),
            "mapped_mod_K5_profile": profile(reduced, quotient_variables),
            "mapped_mod_K5_sha256": digest(reduced, quotient_variables),
        })

    result = {
        "status": "UNAUDITED exact-Q sound K4 leaf export",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "source_row_labels": row_labels,
        "source_row_count": len(rows),
        "row_records": row_records,
        "d3_solve": "d3=-d1*d4*(b0^2+d4)/(b0*(b0+d4))",
        "d3_solve_denominator_factors": ["b0", "b0+d4"],
        "structural_identity": (
            "b0*(b0+d4)*D10 mod K4 = -d1*d4*(b1+d1)*K5"),
        "D10_b1_coefficients_on_K4": {
            "cleared_L6": "-d1*d4*K5",
            "cleared_C4": "-d1^2*d4*K5",
            "warning": "b1=-d1 is an invalid 0/0 cancellation on K5",
        },
        "K5": str(k5),
        "K5_sha256": digest(k5, quotient_variables),
        "N14": str(n14),
        "N14_sha256": digest(n14, quotient_variables),
        "K5_input": OUT_K5.name,
        "K5_input_sha256": sha256(OUT_K5.read_bytes()).hexdigest(),
        "K5_input_bytes": OUT_K5.stat().st_size,
        "K5_equation_count": len(equations_k5),
        "N14_off_K5_input": OUT_N14.name,
        "N14_off_K5_input_sha256": sha256(OUT_N14.read_bytes()).hexdigest(),
        "N14_off_K5_input_bytes": OUT_N14.stat().st_size,
        "N14_off_K5_equation_count": len(equations_n14),
        "localized_source_factors": mapped_live_labels,
        "N14_additional_localized_factor": "K5",
        "live_product_profile": profile(live_product, quotient_variables),
        "K4_pivot_companion": {
            "condition": "b0+d4=0",
            "K4_after_d4_minus_b0": str(exceptional_k4),
            "consequence_on_live_chart": "b0=1,d4=-1",
            "D10_after_consequence": str(exceptional_d10),
            "status": "exact unit from d1*(b1+d1) live",
        },
        "scope": (
            "Exact reduced nine-row A/B-open interface on D10=K4=0. "
            "TrueDelta is intentionally not localized because D10=0. The "
            "K5 gate covers the only possible K4 leaf on the original "
            "Bplus-open chart; the N14 gate covers N14 away from K5 and is "
            "structurally unit. The d3-pivot companion is separately unit."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("sound K4 leaf exact export: PASS")
    print("K5 bytes/profile:", OUT_K5.stat().st_size,
          result["live_product_profile"])
    print("N14-off-K5 bytes:", OUT_N14.stat().st_size)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
