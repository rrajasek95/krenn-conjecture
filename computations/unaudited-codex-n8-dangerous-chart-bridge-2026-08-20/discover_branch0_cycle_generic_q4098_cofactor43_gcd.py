#!/usr/bin/env python3
"""Exact/modular gcd probe for Q4098 and the Cof(4,3) b3 resultant."""

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
TREE = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
FULL = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("q4098_tree_source", TREE)
FULL_SOURCE = load("q4098_full_source", FULL)


def main() -> None:
    started = time.monotonic()
    rows, labels, _ = SOURCE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    variables = (b0, b1, d1, d3, d4)
    live_monomials = (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1)
    compact = [sp.cancel(poly/factor)
               for poly, factor in zip(rows, live_monomials, strict=True)]
    pivot = compact[1]
    leading = sp.diff(pivot, b3)
    constant = sp.expand(pivot.subs(b3, 0))
    aa = sp.cancel(leading/(2*b0))
    bb = sp.cancel(constant/2)
    dn = sp.expand(b0*aa*b1*d3-bb*d1*d4)
    print("A/B/DeltaN profiles",
          (len(sp.Poly(aa, *variables).terms()), sp.Poly(aa, *variables).total_degree()),
          (len(sp.Poly(bb, *variables).terms()), sp.Poly(bb, *variables).total_degree()),
          (len(sp.Poly(dn, *variables).terms()), sp.Poly(dn, *variables).total_degree(),
           [(len(sp.Poly(f,*variables).terms()),sp.Poly(f,*variables).total_degree(),int(e)) for f,e in sp.factor_list(dn)[1]]), flush=True)
    r33 = SOURCE.linear_resultant(compact[5], b3, leading, constant)
    primitive33 = sp.Poly(r33, *variables).primitive()[1].as_expr()
    factors33 = sp.factor_list(primitive33)[1]
    q4098 = next(factor for factor, power in factors33
                 if len(sp.Poly(factor, *variables).terms()) == 4098)
    print("Q4098 ready", time.monotonic()-started)

    lower, *_ = FULL_SOURCE.derive_lower_cofactors()
    cofactor43 = lower[4]
    r43 = SOURCE.linear_resultant(cofactor43, b3, leading, constant)
    primitive43 = sp.Poly(r43, *variables).primitive()[1].as_expr()
    factors43 = sp.factor_list(primitive43)[1]
    print("R43 profile", len(sp.Poly(primitive43, *variables).terms()),
          sp.Poly(primitive43, *variables).total_degree(),
          [(len(sp.Poly(f, *variables).terms()),
            sp.Poly(f, *variables).total_degree(), int(e))
           for f, e in factors43], time.monotonic()-started)

    r13 = SOURCE.linear_resultant(lower[1], b3, leading, constant)
    primitive13 = sp.Poly(r13, *variables).primitive()[1].as_expr()
    factors13 = sp.factor_list(primitive13)[1]
    print("R13 profile", len(sp.Poly(primitive13, *variables).terms()),
          sp.Poly(primitive13, *variables).total_degree(),
          [(len(sp.Poly(f, *variables).terms()),
            sp.Poly(f, *variables).total_degree(), int(e))
           for f, e in factors13], time.monotonic()-started, flush=True)

    r23 = SOURCE.linear_resultant(lower[2], b3, leading, constant)
    primitive23 = sp.Poly(r23, *variables).primitive()[1].as_expr()
    factors23 = sp.factor_list(primitive23)[1]
    print("R23 profile", len(sp.Poly(primitive23, *variables).terms()),
          sp.Poly(primitive23, *variables).total_degree(),
          [(len(sp.Poly(f, *variables).terms()),
            sp.Poly(f, *variables).total_degree(), int(e))
           for f, e in factors23], time.monotonic()-started, flush=True)

    r53 = SOURCE.linear_resultant(lower[5], b3, leading, constant)
    primitive53 = sp.Poly(r53, *variables).primitive()[1].as_expr()
    factors53 = sp.factor_list(primitive53)[1]
    print("R53 profile", len(sp.Poly(primitive53, *variables).terms()),
          sp.Poly(primitive53, *variables).total_degree(),
          [(len(sp.Poly(f, *variables).terms()),
            sp.Poly(f, *variables).total_degree(), int(e))
           for f, e in factors53], time.monotonic()-started, flush=True)

    for prime in (1073741827, 1073741789):
        q = sp.Poly(q4098, *variables, modulus=prime)
        r = sp.Poly(primitive43, *variables, modulus=prime)
        gcd = sp.gcd(q, r)
        print("prime gcd", prime, len(gcd.terms()), gcd.total_degree(),
              gcd.as_expr(), time.monotonic()-started)
    exact = sp.gcd(sp.Poly(q4098, *variables, domain="QQ"),
                   sp.Poly(primitive43, *variables, domain="QQ"))
    print("exact gcd", len(exact.terms()), exact.total_degree(), exact.as_expr(),
          time.monotonic()-started)


if __name__ == "__main__":
    main()
