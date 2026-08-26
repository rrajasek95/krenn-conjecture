#!/usr/bin/env python3
"""Exact generic closure of Delta=0,Bplus!=0,Au!=0.

This is deliberately a generic theorem, not a closure of every parameter
divisor.  Over K=Q(d1,x), the U equation solves d4 and V gives a quadratic
relation Q for b0.  Two literal 4x4 consistency minors of the remaining
six-row linear packet have no common b1-root over K[b0]/(Q).  Hence the
Au-open chart has no generic component; any survivor is confined to the
proper parameter divisor given by their resultant norm (plus displayed
solve denominators).

The nonvanishing of the resultant class is certified without printing its
large symbolic norm: specialize (d1,x)=(2,3), where Q=-2(27*b0^2+13), and
replay the exact nonzero linear resultant remainder in that quadratic
field.  A zero rational-function class would specialize to zero here.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import itertools
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
OUT = HERE / "results_branch0_cycle_delta_au_open_generic.json"
INTERFACE_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTERFACE = load("n8_cycle_delta_au_open_interface", INTERFACE_PATH)
SOURCE = INTERFACE.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(poly):
    return sha256(str(sp.expand(poly)).encode("ascii")).hexdigest()


def determinant4(matrix, rows):
    value = 0
    for permutation in itertools.permutations(range(4)):
        inversions = sum(permutation[left] > permutation[right]
                         for left in range(4)
                         for right in range(left+1, 4))
        value += ((-1)**inversions
                  * sp.prod(matrix[rows[row]][permutation[row]]
                            for row in range(4)))
    return sp.expand(value)


def minor_core(matrix, rows, d4, d4_value, q, b0, b1, x, d1):
    value = sp.cancel(determinant4(matrix, rows).subs(d4, d4_value)) \
        .as_numer_denom()[0]
    # Reduce in the generic quadratic coefficient extension.  Clearing the
    # resulting coefficient-field denominator is valid over Q(d1,x).
    value = sp.rem(sp.Poly(value, b0, domain="QQ(b1,x,d1)"),
                   sp.Poly(q, b0, domain="QQ(b1,x,d1)")).as_expr()
    value = sp.cancel(value).as_numer_denom()[0]
    b1_power = min(monomial[1]
                   for monomial, _ in sp.Poly(value, b0, b1, x, d1).terms())
    require(b1_power == 2, f"minor {rows} lost its live b1^2 factor")
    return sp.Poly(value, b0, b1, x, d1).exquo(
        sp.Poly(b1**2, b0, b1, x, d1)).as_expr()


def derive(rows):
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    interface = INTERFACE.derive(rows)
    variables, u, v = interface[:3]
    normalized = interface[6]
    require(tuple(variables) == (b0, b1, x, d1, d4),
            "the Delta interface variable order changed")
    au = sp.factor(sp.diff(u, d4))
    d4_value = sp.cancel(-u.subs(d4, 0)/au)
    q = sp.factor(sp.resultant(u, v, d4)/b0)
    expected_q = (
        b0**2*d1**2*x**3-b0**2*d1**2*x**2
        -2*b0**2*d1*x**3-2*b0**2*d1*x**2
        +b0**2*x**3-b0**2*x**2-d1**2*x**3+d1**2*x**2
        +2*d1*x**2+2*d1*x-x+1)
    require(sp.expand(q-expected_q) == 0, "the 12-term Q changed")

    # Only explicitly chart-live monomial row factors are removed.  No
    # arbitrary polynomial content is divided out.
    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row]) for entry in entries]
              for row, entries in enumerate(normalized)]
    left_rows = (2, 3, 4, 5)
    right_rows = (0, 2, 3, 4)
    left = minor_core(matrix, left_rows, d4, d4_value,
                      q, b0, b1, x, d1)
    right = minor_core(matrix, right_rows, d4, d4_value,
                       q, b0, b1, x, d1)
    left_shape = (len(sp.Poly(left, b0, b1, x, d1).terms()),
                  sp.Poly(left, b1).degree())
    right_shape = (len(sp.Poly(right, b0, b1, x, d1).terms()),
                   sp.Poly(right, b1).degree())
    require(left_shape == (938, 5),
            f"the first reduced minor changed: {left_shape}")
    require(right_shape == (1526, 4),
            f"the second reduced minor changed: {right_shape}")

    # Q is irreducible over Q(d1,x): its square ratio has the irreducible
    # odd-valuation factor A in the denominator, and gcd(A,C)=1.
    a = sp.Poly(q, b0).coeff_monomial(b0**2)/x**2
    c = sp.Poly(q, b0).coeff_monomial(1)
    require(sp.expand(a-((d1-1)**2*x-(d1+1)**2)) == 0,
            "the Q leading factor A changed")
    require(sp.gcd(sp.Poly(a, d1, x), sp.Poly(c, d1, x)).as_expr() == 1,
            "A and C acquired a common factor")
    require(sp.factor(sp.resultant(a, c, x))
            == 16*d1**2*(d1**2+1)*(d1**2+2*d1-1),
            "the A,C coprimality witness changed")

    specialization = {d1: 2, x: 3}
    q_special = sp.factor(q.subs(specialization))
    resultant = sp.resultant(left.subs(specialization),
                             right.subs(specialization), b1)
    remainder = sp.factor(sp.rem(sp.Poly(resultant, b0),
                                 sp.Poly(q_special, b0)).as_expr())
    scale = -69518224795925593323989958561245179702282019772505893371904
    slope = 131219100251472764329632105369604839
    intercept = 116938404104448695432512512100744501
    expected_remainder = scale*(slope*b0-intercept)
    require(sp.expand(q_special+2*(27*b0**2+13)) == 0,
            "the exact quadratic specialization changed")
    require(sp.expand(remainder-expected_remainder) == 0,
            "the exact specialized resultant remainder changed")
    require(sp.gcd(sp.Poly(27*b0**2+13, b0),
                   sp.Poly(slope*b0-intercept, b0)).degree() == 0,
            "the specialized resultant became zero in the quadratic field")
    return {
        "au": au, "d4_value": d4_value, "q": q,
        "left": left, "right": right,
        "q_special": q_special, "remainder": remainder,
        "a": a, "c": c,
    }


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    derived = derive(rows)

    # Hostile literal mutation stays local and changes the first minor's
    # source row.  The heavy resultant need not be rerun for this guard.
    mutated_raw = dict(raw["cofactor_0_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["cofactor_0_3"] = SOURCE.expression(mutated_raw)
    original_matrix = INTERFACE.derive(rows)[6]
    mutated_matrix = INTERFACE.derive(mutated_rows)[6]
    require(original_matrix[:-1] == mutated_matrix[:-1]
            and original_matrix[-1] != mutated_matrix[-1],
            "the literal Cof(0,3) mutation did not fire")

    b0, b1, _, d1, _, _ = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    result = {
        "status": "UNAUDITED exact generic closure of Delta Au-open branch",
        "assumptions": [
            "branch0 four-cycle interior chart", "Delta=0",
            "Bplus=b1+d1 nonzero", "Au nonzero",
            "b1*d1*d4*x nonzero", "all selected-term factors nonzero"],
        "Au": str(derived["au"]),
        "d4": str(derived["d4_value"]),
        "Q": str(derived["q"]),
        "Q_irreducibility": {
            "A": str(derived["a"]),
            "gcd_A_C": "1",
            "resultant_A_C_x": str(sp.factor(sp.resultant(
                derived["a"], derived["c"], x)))},
        "minor_rows": [[2, 3, 4, 5], [0, 2, 3, 4]],
        "minor_terms": [
            len(sp.Poly(derived["left"], b0, b1, x, d1).terms()),
            len(sp.Poly(derived["right"], b0, b1, x, d1).terms())],
        "minor_b1_degrees": [5, 4],
        "minor_sha256": [digest(derived["left"]),
                          digest(derived["right"])],
        "exact_nonzero_specialization": {
            "d1": 2, "x": 3,
            "Q": str(derived["q_special"]),
            "resultant_remainder": str(derived["remainder"])},
        "scope": (
            "The Au-open locus has no component dominating the (d1,x) "
            "parameter plane. This does not close special parameter "
            "divisors: the symbolic resultant norm and all denominator "
            "divisors must still be split and checked."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au-open generic closure: PASS")
    print("minor terms/degrees:", result["minor_terms"],
          result["minor_b1_degrees"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
