#!/usr/bin/env python3
"""Exact source-faithful closure of the Au=0 Delta-cycle subbranch.

We work in the branch-0, four-cycle chart and reuse the literal row parser
from ``audit_branch0_cycle_delta_zero_linear_interface.py``.  On Delta=0
and Bplus=b1+d1 nonzero, the four upper cofactors solve p3,p4 and leave the
two equations U,V.  If the coefficient ``Au`` of d4 in U vanishes, then
U forces b0=-d1 and x=b3/b1=d1^-2; V then forces

    d4 = -d1^3(d1+1)/(d1-1).

The remaining seven literal rows form a small linear packet.  Exact
resultants close its generic solve branch.  Both possible zero solve-
coefficient exceptions are also closed in the localized interior chart:
the t012 exception contains b1^2(d1+1), while the only nonunit t013
exception contains p1+1.  All of these are live factors.
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
OUT = HERE / "results_branch0_cycle_delta_au_zero.json"
INTERFACE_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTERFACE = load("n8_cycle_delta_au_interface", INTERFACE_PATH)
SOURCE = INTERFACE.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(poly):
    return sha256(str(sp.expand(poly)).encode("ascii")).hexdigest()


def top(poly):
    return sp.cancel(poly).as_numer_denom()[0]


def derive(rows, terminal_checks=True):
    p1, p2, p3, p4 = SOURCE.P
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    ratio = {b3: x*b1, d3: -x*d1*d4}

    upper = [sp.factor(rows[f"cofactor_{edge}_0"].subs(ratio))
             for edge in range(1, 5)]
    p3_p4 = sp.solve([upper[2], upper[3]], [p4, p3], dict=True,
                     simplify=False)[0]
    u = sp.factor(-sp.cancel(upper[0].subs(p3_p4))/d4)
    v = sp.factor(sp.cancel(upper[1].subs(p3_p4))
                  /(b1**2*d1*d4*x))
    expected_u = (b0**2*d1*x-b0**2*x-b0*d1*d4*x-b0*d1*x
                  -b0*d4*x+b0-d1*d4*x-d4)
    expected_v = (b0**2*d1*x+b0**2*x-b0*d1*d4*x**2-b0*d1*x
                  +b0*d4*x**2-b0-d1*d4*x**2+d4*x)
    require(sp.expand(u-expected_u) == 0 and sp.expand(v-expected_v) == 0,
            "the literal U,V reduction changed")

    au = sp.factor(sp.diff(u, d4))
    require(au == -b0*d1*x-b0*x-d1*x-1,
            "the Au coefficient changed")
    require(sp.factor(sp.resultant(au, u, x)) == -2*b0*(b0+d1),
            "Au,U no longer force b0=-d1")
    branch = {b0: -d1, x: 1/d1**2,
              d4: -d1**3*(d1+1)/(d1-1)}
    require(sp.cancel(au.subs(branch)) == 0
            and sp.cancel(u.subs(branch)) == 0
            and sp.cancel(v.subs(branch)) == 0,
            "the Au=U=V branch parametrization changed")

    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    reduced = {label: sp.cancel(rows[label].subs(ratio).subs(p3_p4))
               for label in labels}
    a0_row = sp.cancel(reduced["cofactor_5_0"].subs(branch))
    a0_value = sp.solve(a0_row, a0, dict=True, simplify=False)[0][a0]
    current = {label: sp.cancel(value.subs(branch).subs(a0, a0_value))
               for label, value in reduced.items()
               if label != "cofactor_5_0"}
    unknowns = (p1, p2, a5)
    linear_terms = {}
    for label, value in current.items():
        require(all(sp.diff(value, left, right) == 0
                    for left in unknowns for right in unknowns),
                f"{label} ceased to be linear")
        entries = [sp.cancel(sp.diff(value, variable))
                   for variable in unknowns]
        entries.append(sp.cancel(value.subs({variable: 0
                                             for variable in unknowns})))
        linear_terms[label] = [len(sp.Poly(top(entry), b1, d1).terms())
                               if entry else 0 for entry in entries]
    if not terminal_checks:
        return {"current": current, "linear_terms": linear_terms}
    require(linear_terms == {
        "t_012": [9, 0, 0, 8], "t_013": [0, 5, 0, 11],
        "t_023": [2, 2, 2, 3], "t_123": [8, 8, 8, 12],
        "cofactor_0_0": [8, 8, 3, 12],
        "cofactor_0_3": [12, 12, 5, 13]},
        "the six-row linear packet changed")
    solved = {}
    solve_coefficients = {}
    for label, variable in (("t_012", p1), ("t_013", p2),
                            ("t_023", a5)):
        row = sp.cancel(current[label].subs(solved))
        solve_coefficients[label] = sp.factor(sp.diff(row, variable))
        solved[variable] = sp.cancel(sp.solve(
            row, variable, dict=True, simplify=False)[0][variable]
            .subs(solved))
    require(sp.factor(solve_coefficients["t_023"])
            == b1*d1*(b1+d1),
            "the always-live a5 solve coefficient changed")

    finals = []
    for label in ("t_123", "cofactor_0_0", "cofactor_0_3"):
        value = top(current[label].subs(solved))
        core = max((factor for factor, _ in sp.factor_list(value)[1]),
                   key=lambda factor: sp.Poly(factor, b1, d1).total_degree())
        finals.append(core)
    pair_resultants = [
        sp.factor(sp.resultant(finals[left], finals[right], b1))
        for left, right in ((0, 1), (0, 2), (1, 2))]
    common = sp.factor(sp.gcd(sp.gcd(pair_resultants[0],
                                     pair_resultants[1]),
                              pair_resultants[2]))
    q_i = d1**2+1
    q_2 = d1**2+2*d1-1
    q_23 = d1**2+3*d1-1
    q_3 = d1**3+2*d1-1
    expected_common = (32*d1**22*(d1-1)**3*(d1+1)**9*(3*d1-1)
                       *q_i*q_2*q_23*q_3)
    require(common == expected_common,
            "the generic terminal common resultant changed")

    candidate_bases = {}
    for factor in (3*d1-1, q_i, q_2, q_23, q_3):
        gb = sp.groebner([factor, *finals], b1, d1, order="lex")
        candidate_bases[str(factor)] = [sp.factor(poly.as_expr())
                                        for poly in gb.polys]
    require(candidate_bases[str(3*d1-1)] == [3*b1+1, 3*d1-1],
            "the linear generic candidate changed")
    require(candidate_bases[str(q_i)] == [sp.Integer(1)]
            and candidate_bases[str(q_2)] == [sp.Integer(1)],
            "the two generic unit candidates changed")
    require(candidate_bases[str(q_23)] == [13*b1-3*d1+2, q_23],
            "the q23 generic candidate changed")
    require(candidate_bases[str(q_3)] == [b1+d1, q_3],
            "the cubic generic candidate changed")

    # q23 is where both first triangle solve coefficients vanish.  Use the
    # original unsolved six rows, so no division by those coefficients occurs.
    b1_q23 = (3*d1-2)/13
    q23_rows = [top(value.subs(b1, b1_q23)) for value in current.values()]
    q23_gb = sp.groebner([q_23, *q23_rows], p1, p2, a5, d1,
                         order="lex")
    require(any(poly.as_expr() == 1 for poly in q23_gb.polys),
            "the unsolved q23 exception ceased to be a unit")

    # t012 coefficient zero: the full unsolved ideal contains the Laurent
    # unit b1^2(d1+1).  This is an exact membership check, not a dimension
    # inference.
    packet_tops = [top(value) for value in current.values()]
    c012 = top(sp.diff(current["t_012"], p1))
    gb012 = sp.groebner([c012, *packet_tops], p1, p2, a5, b1, d1,
                        order="grevlex")
    target012 = b1**2*(d1+1)
    require(sp.expand(gb012.reduce(target012)[1]) == 0,
            "the t012-exception live target left the ideal")

    # t013 coefficient zero: coefficient and constant can meet only on q2
    # or q3 after live factors are removed.  q2 forces p1+1=0 (an interior
    # selected-term contradiction); q3 is an outright exact unit.
    c013 = top(sp.diff(current["t_013"], p2))
    k013 = top(current["t_013"].subs(p2, 0))
    r013 = sp.factor(sp.resultant(c013, k013, b1))
    expected_r013 = 8*d1**10*(d1+1)**2*q_2*q_3
    require(r013 == expected_r013,
            "the t013 coefficient/constant resultant changed")
    gb013_q2 = sp.groebner([q_2, c013, *packet_tops],
                           p1, p2, a5, b1, d1, order="grevlex")
    require(sp.expand(gb013_q2.reduce(p1+1)[1]) == 0,
            "the q2 t013 exception no longer forces p1=-1")
    gb013_q3 = sp.groebner([q_3, c013, *packet_tops],
                           p1, p2, a5, b1, d1, order="grevlex")
    require(any(poly.as_expr() == 1 for poly in gb013_q3.polys),
            "the q3 t013 exception ceased to be a unit")

    return {
        "au": au, "branch": branch, "linear_terms": linear_terms,
        "finals": finals, "common": common,
        "candidate_bases": candidate_bases,
        "q23_unit_basis_size": len(q23_gb.polys),
        "t012_basis_size": len(gb012.polys),
        "t012_live_target": target012,
        "t013_resultant": r013,
        "t013_q2_basis": [sp.factor(poly.as_expr())
                           for poly in gb013_q2.polys],
        "t013_q3_basis_size": len(gb013_q3.polys),
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
    require(mutated["current"]["cofactor_0_3"]
            != derive(rows, terminal_checks=False)["current"]["cofactor_0_3"],
            "the literal cofactor mutation did not fire")

    result = {
        "status": "UNAUDITED exact closure of Au=0 in Delta=0,Bplus!=0",
        "assumptions": [
            "branch0 four-cycle interior chart", "Delta=0",
            "Bplus=b1+d1 nonzero", "Au=0",
            "b1,d1,d4 and d1-1 are nonzero",
            "all four selected-term factors p_i+1 are nonzero"],
        "forced_branch": {str(key): str(value)
                          for key, value in derived["branch"].items()},
        "linear_packet_terms": derived["linear_terms"],
        "generic_common_resultant": str(derived["common"]),
        "generic_final_digests": [digest(value)
                                  for value in derived["finals"]],
        "generic_candidate_bases": {
            factor: [str(value) for value in basis]
            for factor, basis in derived["candidate_bases"].items()},
        "q23_unsolved_unit_basis_size": derived["q23_unit_basis_size"],
        "t012_exception": {
            "basis_size": derived["t012_basis_size"],
            "live_target_in_ideal": str(derived["t012_live_target"])},
        "t013_exception": {
            "coefficient_constant_resultant": str(
                derived["t013_resultant"]),
            "q2_basis": [str(value) for value
                          in derived["t013_q2_basis"]],
            "q2_live_target_in_ideal": "p1 + 1",
            "q3_unit_basis_size": derived["t013_q3_basis_size"]},
        "scope": (
            "This closes the entire Au=0 subbranch of Delta=0 with "
            "Bplus nonzero in the both-selected-terms-live cycle interior. "
            "The complementary Au!=0 Delta branch remains open."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au=0 exact closure: PASS")
    print("linear packet:", result["linear_packet_terms"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
