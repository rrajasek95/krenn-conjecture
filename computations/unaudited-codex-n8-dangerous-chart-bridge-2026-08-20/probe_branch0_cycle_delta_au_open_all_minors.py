#!/usr/bin/env python3
"""Census all literal consistency minors on the Delta/Au-open quotient.

Discovery only: this identifies the smallest fourth packet determinant to add
to the already frozen three-minor modular interface.  It makes no closure
claim.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_all_minor_audit", AUDIT_PATH)
sp = AUDIT.sp
SOURCE = AUDIT.SOURCE


def open_core(matrix, selected, derived, b0, b1, d1, d4, x):
    value = sp.cancel(AUDIT.determinant4(matrix, selected).subs(
        d4, derived["d4_value"])).as_numer_denom()[0]
    value = sp.rem(sp.Poly(value, b0, domain="QQ(b1,d1,x)"),
                   sp.Poly(derived["q"], b0,
                           domain="QQ(b1,d1,x)")).as_expr()
    value = sp.cancel(value).as_numer_denom()[0]
    poly = sp.Poly(value, b0, b1, d1, x)
    content = tuple(min(monomial[index] for monomial, _ in poly.terms())
                    for index in range(4))
    monomial = b0**content[0]*b1**content[1]*d1**content[2]*x**content[3]
    return poly.exquo(sp.Poly(monomial, b0, b1, d1, x)).as_expr(), content


def main():
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    derived = AUDIT.derive(rows)
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    normalized = AUDIT.INTERFACE.derive(rows)[6]
    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row])
               for entry in entries]
              for row, entries in enumerate(normalized)]
    known = {(2, 3, 4, 5), (0, 2, 3, 4), (1, 2, 3, 4)}
    for selected in itertools.combinations(range(6), 4):
        started = time.monotonic()
        minor, content = open_core(
            matrix, selected, derived, b0, b1, d1, d4, x)
        poly = sp.Poly(minor, b0, b1, d1, x)
        print(selected, "known" if selected in known else "new",
              "content", content,
              "terms", len(poly.terms()), "degrees", poly.degree_list(),
              "elapsed", round(time.monotonic()-started, 3), flush=True)


if __name__ == "__main__":
    main()
