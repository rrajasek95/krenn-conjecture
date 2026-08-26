#!/usr/bin/env python3
"""Compare literal omitted lower cofactors on the generic cycle Cramer chart."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
GENERIC = HERE.parent / "unaudited-codex-root-integration-2026-08-20" / \
    "discover_branch0_k4_cycle_cramer_generic.py"


def load(path: Path):
    spec = importlib.util.spec_from_file_location("cycle_generic_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(GENERIC)


def primitive(poly: sp.Expr) -> sp.Expr:
    poly = sp.expand(poly)
    common = sp.gcd_list(list(sp.Poly(poly, *SOURCE.PARAMETERS).terms()))
    del common  # SymPy's primitive operation below is the intended normalization.
    return sp.primitive(sp.Poly(poly, *SOURCE.PARAMETERS))[1].as_expr()


def main() -> None:
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]

    c50 = SOURCE.numerator(rows["cofactor_5_0"], p_solution)
    a0_solution = sp.solve(c50, SOURCE.A0, dict=True, simplify=False)[0]
    t023 = SOURCE.numerator(
        SOURCE.numerator(rows["t_023"], p_solution), a0_solution)
    a5_solution = sp.solve(t023, SOURCE.A5, dict=True, simplify=False)[0]

    delta = SOURCE.PARAMETERS[1] * SOURCE.PARAMETERS[4] \
        + SOURCE.PARAMETERS[2] * SOURCE.PARAMETERS[3] * SOURCE.PARAMETERS[5]
    for edge in range(1, 6):
        label = f"cofactor_{edge}_3"
        value = SOURCE.numerator(rows[label], p_solution)
        value = SOURCE.numerator(value, a0_solution)
        value = SOURCE.numerator(value, a5_solution)
        delta_power = 0
        while sp.rem(sp.Poly(value, *SOURCE.PARAMETERS),
                     sp.Poly(delta, *SOURCE.PARAMETERS)) == 0:
            value = sp.cancel(value / delta)
            delta_power += 1
        value = sp.primitive(sp.Poly(value, *SOURCE.PARAMETERS))[1].as_expr()
        polynomial = sp.Poly(value, *SOURCE.PARAMETERS)
        factors = sp.factor_list(value)[1]
        print(label, "terms", len(polynomial.terms()),
              "degree", polynomial.total_degree(),
              "delta_removed", delta_power,
              "factor_degrees", [sp.Poly(f, *SOURCE.PARAMETERS).total_degree()
                                  for f, _ in factors],
              "small_factors", [str(f) for f, _ in factors
                                  if sp.Poly(f, *SOURCE.PARAMETERS).total_degree() <= 2])


if __name__ == "__main__":
    main()
