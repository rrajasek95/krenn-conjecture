#!/usr/bin/env python3
"""One exact linear-elimination tree for the generic cycle core."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import time

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_cycle_generic_cofactor33_core.py"


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_b3_resultant_source", path)
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
        answer += coefficient * (-constant)**power * leading**(degree-power)
    return sp.expand(answer)


def main() -> None:
    started = time.monotonic()
    rows, labels, _ = SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.PARAMETERS
    live_monomials = (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1)
    compact = [sp.cancel(poly/factor)
               for poly, factor in zip(rows, live_monomials, strict=True)]
    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    require_linear = sp.expand(pivot-(leading*b3+constant))
    if require_linear != 0:
        raise RuntimeError("t_013 is no longer linear in b3")
    leading_reduced = sp.cancel(leading/(2*b0))
    if not sp.Poly(leading_reduced, b0, b1, d1, d3, d4).is_irreducible:
        raise RuntimeError("the special b3 pivot divisor unexpectedly factors")
    print("pivot special divisor terms/degree:",
          len(sp.Poly(leading_reduced, b0, b1, d1, d3, d4).terms()),
          sp.Poly(leading_reduced, b0, b1, d1, d3, d4).total_degree())
    print("pivot constant terms/degree:",
          len(sp.Poly(constant/2, b0, b1, d1, d3, d4).terms()),
          sp.Poly(constant/2, b0, b1, d1, d3, d4).total_degree())
    for index, (label, poly) in enumerate(zip(labels, compact, strict=True)):
        if index in (1, 6):
            continue
        result = linear_resultant(poly, b3, leading, constant)
        value = sp.Poly(result, b0, b1, d1, d3, d4).primitive()[1]
        factors = sp.factor_list(value.as_expr())[1]
        profile = [(len(sp.Poly(factor, b0, b1, d1, d3, d4).terms()),
                    sp.Poly(factor, b0, b1, d1, d3, d4).total_degree(), power)
                   for factor, power in factors]
        print(label, "resultant terms/degree", len(value.terms()),
              value.total_degree(), "factor profile", profile,
              "small factors", [(str(factor), power) for factor, power in factors
                                  if len(sp.Poly(factor, b0, b1, d1, d3, d4).terms()) <= 8],
              "elapsed", round(time.monotonic()-started, 3))


if __name__ == "__main__":
    main()
