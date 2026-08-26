#!/usr/bin/env python3
"""Exact closure of the generic Bplus=0 part of the Delta=0 cycle.

This continues the source-faithful linear interface from
``audit_branch0_cycle_delta_zero_linear_interface.py``.  Put
``b1=-d1`` and retain ``x=b3/b1 != 1``.  The literal t023 row forces W=0.
After the W substitution, the U,V resultant splits into a selected-term
contradiction and one bivariate factor P.  On P, a subresultant solves b0;
away from the two displayed triangle solve coefficients, the remaining
two cofactor equations have incompatible exact univariate resultants.

The two zero-coefficient branches are also empty: coefficient/constant
resultants share only ``d1^2+1``, which is incompatible with P.  Thus the
entire ``Bplus=0,x!=1`` branch is closed.
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
OUT = HERE / "results_branch0_cycle_delta_bplus_generic.json"
INTERFACE_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTERFACE = load("n8_cycle_delta_bplus_interface", INTERFACE_PATH)
SOURCE = INTERFACE.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(poly):
    return sha256(str(sp.expand(poly)).encode("ascii")).hexdigest()


def core_factor(poly, variables):
    factors = sp.factor_list(poly)[1]
    return max((factor for factor, _ in factors),
               key=lambda factor: sp.Poly(factor, *variables).total_degree())


def derive(rows, terminal_checks=True):
    a0, a5 = SOURCE.A0, SOURCE.A5
    p1, p2, p3, p4 = SOURCE.P
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    ratio = {b3: x*b1, d3: -x*d1*d4}
    minus = {b1: -d1}
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    upper_minus = [sp.factor(row.subs(ratio).subs(minus)) for row in upper]
    p1_p2 = sp.solve([upper_minus[2], upper_minus[3]], [p2, p1],
                     dict=True, simplify=False)[0]

    u = (b0**2*d1*x - b0**2*x - b0*d1*d4*x - b0*d1*x
         - b0*d4*x + b0 - d1*d4*x - d4)
    v = (b0**2*d1*x + b0**2*x - b0*d1*d4*x**2 - b0*d1*x
         + b0*d4*x**2 - b0 - d1*d4*x**2 + d4*x)
    require(sp.factor(sp.cancel(upper_minus[0].subs(p1_p2)) + d4*u) == 0
            and sp.factor(sp.cancel(upper_minus[1].subs(p1_p2))
                          - d1**3*d4*x*v) == 0,
            "the Bplus=0 U,V reduction changed")

    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    reduced = {label: sp.cancel(rows[label].subs(ratio).subs(minus)
                                .subs(p1_p2))
               for label in labels}
    a0_row = reduced["cofactor_5_0"]
    a0_value = sp.solve(a0_row, a0, dict=True, simplify=False)[0][a0]
    after_a0 = {label: sp.cancel(value.subs(a0, a0_value))
                for label, value in reduced.items()
                if label != "cofactor_5_0"}

    w = d1**2*x - d1*x + d1 + 1
    require(sp.cancel(after_a0["t_023"]/(b0*d1*w/(d4*x))) == 1,
            "the literal W row changed")
    x_value = -(d1 + 1)/(d1*(d1 - 1))
    u_w = sp.cancel(u.subs(x, x_value)).as_numer_denom()[0]
    v_w = sp.cancel(v.subs(x, x_value)).as_numer_denom()[0]
    qplus = d1**2 + 2*d1 - 1
    p_big = (
        d1**6*d4**2 + 4*d1**6*d4 + 4*d1**6
        + 4*d1**5*d4**2 + 16*d1**5*d4
        + 7*d1**4*d4**2 + 16*d1**4*d4 + 4*d1**4
        + 8*d1**3*d4**2 + 7*d1**2*d4**2 - 4*d1**2*d4
        + 4*d1*d4**2 + d4**2)
    require(sp.factor(sp.resultant(u_w, v_w, b0)) ==
            2*d1*d4*(d1 - 1)*(d1 + 1)*qplus*p_big,
            "the W/U/V resultant changed")

    # The qplus branch has b0=-(d1+2)d4 and makes p2=-1.
    b0_qplus = -(d1 + 2)*d4
    p2_plus_one = sp.cancel(p1_p2[p2].subs(
        {x: x_value, b0: b0_qplus}) + 1)
    p2_top = p2_plus_one.as_numer_denom()[0]
    require(sp.rem(sp.Poly(p2_top, d1), sp.Poly(qplus, d1)).is_zero,
            "the qplus p2=-1 contradiction changed")

    # On P, the linear subresultant has coefficient A.  A cannot vanish,
    # because its constant term is a chart unit, so it solves b0.
    subresultant = sp.factor(sp.subresultants(u_w, v_w, b0)[-2]
                            / ((d1 - 1)*(d1 + 1)))
    a_lead = (d1**4*d4 + 2*d1**4 + 4*d1**3*d4
              + 4*d1**2*d4 + 2*d1**2 - d4)
    constant = 4*d1**2*d4*(d1 + 1)
    require(sp.expand(subresultant - (a_lead*b0 + constant)) == 0,
            "the P-branch linear subresultant changed")
    b0_value = -constant/a_lead

    branch = {x: x_value, b0: b0_value}
    a5_row = sp.cancel(after_a0["t_123"].subs(branch))
    a5_value = sp.solve(a5_row, a5, dict=True, simplify=False)[0][a5]
    branch[a5] = a5_value
    p3_row = sp.cancel(after_a0["t_012"].subs(branch))
    p4_row = sp.cancel(after_a0["t_013"].subs(branch))

    # If either triangle solve coefficient vanishes, its constant must also
    # vanish.  Eliminating d4 against P shows that the two resultant pairs
    # share only d1^2+1 (apart from Laurent units).  P is nonzero there.
    exception_data = {}
    qi = d1**2 + 1
    for name, row, variable, expected_terms, expected_powers in (
            ("D3", p3_row, p3, (26, 40), (20, 10)),
            ("D4", p4_row, p4, (24, 36), (16, 8))):
        coefficient_top = sp.cancel(sp.diff(row, variable)) \
            .as_numer_denom()[0]
        constant_top = sp.cancel(row.subs(variable, 0)) \
            .as_numer_denom()[0]
        require((len(sp.Poly(coefficient_top, d1, d4).terms()),
                 len(sp.Poly(constant_top, d1, d4).terms()))
                == expected_terms,
                f"the {name} exceptional row sizes changed")
        coefficient_resultant = sp.factor(
            sp.resultant(p_big, coefficient_top, d4))
        constant_resultant = sp.factor(
            sp.resultant(p_big, constant_top, d4))
        common = sp.factor(sp.gcd(coefficient_resultant,
                                  constant_resultant))
        expected_common = (4096*d1**expected_powers[0]
                           *(d1 + 1)**expected_powers[1]*qi**3)
        require(common == expected_common,
                f"the {name} exceptional resultant gcd changed")
        exception_data[name] = {
            "coefficient_terms": expected_terms[0],
            "constant_terms": expected_terms[1],
            "common_resultant": common,
        }

    p3_value = sp.solve(p3_row, p3, dict=True, simplify=False)[0][p3]
    p4_value = sp.solve(p4_row, p4, dict=True, simplify=False)[0][p4]
    branch[p3] = p3_value
    branch[p4] = p4_value

    d3_core = core_factor(sp.cancel(p3_value).as_numer_denom()[1],
                          (d1, d4))
    d4_core = core_factor(sp.cancel(p4_value).as_numer_denom()[1],
                          (d1, d4))
    d3_terms = len(sp.Poly(d3_core, d1, d4).terms())
    d4_terms = len(sp.Poly(d4_core, d1, d4).terms())
    require(d3_terms == 17 and d4_terms == 24,
            f"the two triangle solve coefficients changed: "
            f"{d3_terms},{d4_terms}")

    final = {}
    for label in ("cofactor_0_0", "cofactor_0_3"):
        final[label] = sp.cancel(after_a0[label].subs(branch)) \
            .as_numer_denom()[0]
    if not terminal_checks:
        return {"final": final}
    require([len(sp.Poly(final[label], d1, d4).terms())
             for label in final] == [111, 150],
            "the final cofactor numerator sizes changed")
    resultants = {label: sp.factor(sp.resultant(p_big, value, d4))
                  for label, value in final.items()}
    factors0 = sp.factor_list(resultants["cofactor_0_0"])[1]
    factors3 = sp.factor_list(resultants["cofactor_0_3"])[1]
    r18 = next(factor for factor, _ in factors0
               if sp.Poly(factor, d1).degree() == 18)
    r22 = next(factor for factor, _ in factors3
               if sp.Poly(factor, d1).degree() == 22)
    require(sp.gcd(sp.Poly(r18, d1), sp.Poly(r22, d1)).degree() == 0,
            "the degree-18/22 terminal factors acquired a common root")
    p_mod_qi = sp.rem(sp.Poly(p_big, d1, domain="EX"),
                      sp.Poly(qi, d1, domain="EX")).as_expr()
    require(sp.factor(p_mod_qi) == 16*d4*(d1 + 1),
            "the d1^2+1 leading degeneration changed")

    return {
        "W": w, "P": p_big, "A": a_lead,
        "D3": d3_core, "D4": d4_core,
        "exceptions": exception_data,
        "final": final, "R18": r18, "R22": r22,
        "p_mod_qi": p_mod_qi,
    }


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    derived = derive(rows)

    mutated_raw = dict(raw["cofactor_0_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["cofactor_0_3"] = SOURCE.expression(mutated_raw)
    mutated = derive(mutated_rows, terminal_checks=False)
    require(mutated["final"]["cofactor_0_3"]
            != derived["final"]["cofactor_0_3"],
            "the literal Cof(0,3) mutation did not fire")

    result = {
        "status": "UNAUDITED exact closure of full Bplus=0 Delta branch",
        "assumptions": [
            "Delta=0", "b1+d1=0", "x=b3/b1 != 1",
            "all Laurent and selected-term factors live"],
        "forced_W": str(derived["W"]),
        "bivariate_P": str(derived["P"]),
        "b0_solve_coefficient": str(derived["A"]),
        "triangle_solve_factors": {
            "D3_terms": len(sp.Poly(derived["D3"], *SOURCE.PARAMETERS[3:6:2]).terms()),
            "D3_sha256": digest(derived["D3"]),
            "D4_terms": len(sp.Poly(derived["D4"], *SOURCE.PARAMETERS[3:6:2]).terms()),
            "D4_sha256": digest(derived["D4"]),
        },
        "triangle_zero_exceptions": {
            name: {key: (str(value) if key == "common_resultant" else value)
                   for key, value in data.items()}
            for name, data in derived["exceptions"].items()
        },
        "final_cofactor_terms": {
            label: len(sp.Poly(value, SOURCE.PARAMETERS[3],
                               SOURCE.PARAMETERS[5]).terms())
            for label, value in derived["final"].items()},
        "terminal_univariates": {
            "R18": str(derived["R18"]),
            "R22": str(derived["R22"]),
            "gcd": "1",
            "P_mod_d1^2_plus_1": str(derived["p_mod_qi"]),
        },
        "scope": (
            "This closes all of Bplus=0,x!=1, including D3=0 and D4=0. "
            "Together with the companion x=1 unit, the entire Bplus=0 "
            "Delta branch is empty. The Bplus!=0 Delta matrix remains open."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Bplus=0 full closure: PASS")
    print("final terms:", result["final_cofactor_terms"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
