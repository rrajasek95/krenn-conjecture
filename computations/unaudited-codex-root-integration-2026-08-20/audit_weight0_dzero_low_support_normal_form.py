#!/usr/bin/env python3
"""Exact low-Q normal form on the weight-zero d=0 cofactor chart.

This is deliberately a chart theorem, not a theorem about all diagonal
packet points.  In the branch-51 Laurent chart

    M_e = [[a_e,b_e],[-1/b_e,0]],  all b_e != 0,

the six permanent and four triangle rows reduce the b-ratios to one
quadratic extension.  The remaining base quotient is affine four-space,
with four Laurent-unit-scaled Q coordinates as coordinates and Q_0 a single
explicit quadratic form.  This classifies every point of this chart with at
most eight nonzero Q coordinates.  It also checks the full X/cofactor/Q
orbit obstruction for the only support-eight class which has a support-level
mate.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys
import sysconfig

# ``-S`` omits the site initialization which normally exposes SymPy.  Add
# only the interpreter's configured purelib path so the exact checker remains
# replayable in the hostile ``-I -S`` mode used by the audit suite.
PURELIB = sysconfig.get_paths().get("purelib")
VENV_PURELIB = (Path(sys.executable).parent.parent / "lib" /
                f"python{sys.version_info.major}.{sys.version_info.minor}" /
                "site-packages")
for package_path in (PURELIB, str(VENV_PURELIB)):
    if package_path and package_path not in sys.path:
        sys.path.append(package_path)
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHART_PATH = (ROOT / "computations" /
              "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
              "analyze_weight0_dzero_lowq_chart.py")
COMPONENT_PATH = (ROOT / "computations" /
                  "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
                  "audit_weight0_support6_char0_component.py")
RAW_PATH = (ROOT / "computations" /
            "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
            "audit_diagonal_cofactor_branch_orbits.py")
OUT = HERE / "results_weight0_dzero_low_support_normal_form.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CHART = load("root_dzero_chart", CHART_PATH)
COMPONENT = load("root_support6_component", COMPONENT_PATH)
RAW = load("root_dzero_raw", RAW_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


r, s, t = sp.symbols("r s t")
y1, y2, y4, y8 = sp.symbols("y1 y2 y4 y8")
T = sp.symbols("T")
ROOT_POLY = sp.Poly(r * r + 2 * r - 1, r)


def reduce_r(expression):
    expression = sp.cancel(expression)
    numerator, denominator = sp.fraction(expression)
    numerator = sp.rem(sp.Poly(sp.expand(numerator), r), ROOT_POLY).as_expr()
    denominator = sp.rem(sp.Poly(sp.expand(denominator), r), ROOT_POLY).as_expr()
    inverse = sp.invert(sp.Poly(denominator, r), ROOT_POLY).as_expr()
    return sp.factor(sp.rem(sp.Poly(sp.expand(numerator * inverse), r),
                           ROOT_POLY).as_expr())


def chart_expression(poly, variables):
    answer = 0
    for exponent, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for variable, power in zip(variables, exponent):
            term *= variable ** power
        answer += term
    return sp.expand(answer)


def raw_evaluate(poly, entries):
    answer = 0
    for monomial, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for variable in monomial:
            term *= entries[variable]
        answer += term
    return reduce_r(answer)


def derivative(poly, variable):
    answer = {}
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable)
            reduced = tuple(reduced)
            answer[reduced] = answer.get(reduced, 0) + coefficient * multiplicity
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def bit_mask(indices):
    return sum(1 << index for index in indices)


def q_complement(mask):
    return sum(1 << (15 - index) for index in range(16)
               if mask & (1 << index))


def main():
    # After writing b0=r*u/v, b1=s*u/w, b2=u, b3=t*v/w,
    # b4=v, b5=w, the eight nonduplicate b-only equations have these
    # ratio parts.  Their exact Groebner basis is triangular and radical.
    ratio_equations = (
        r * r * t * t + 2 * r * s * t - s * s,
        r * r + 2 * r - 1,
        s * s + 2 * s - 1,
        t * t + 2 * t - 1,
        s * t + s + t - 1,
        r * t - r - t - 1,
        r * s * t - r * t - s * s - s,
        r * r * t + r * s + r * t - s,
    )
    ratio_basis = sp.groebner(ratio_equations, s, t, r, order="lex")
    expected_ratio_basis = (r + s + 2, r + t + 2,
                            r * r + 2 * r - 1)
    require(tuple(sp.factor(poly.as_expr()) for poly in ratio_basis.polys)
            == expected_ratio_basis, "b-ratio Groebner basis changed")

    # Gauge u=v=w=1.  The other conjugate root is already represented by
    # r^2+2r-1; zero patterns are unchanged by the discarded Laurent units.
    b_values = (r, -r - 2, 1, -r - 2, 1, 1)
    c_values = (-r - 2, r, -1, r, -1, -1)
    a_values = (
        (13*r*y1 + 13*r*y2 - r*y4 - 7*r*y8
         + 27*y1 - y2 - 9*y4 - 13*y8) / 40,
        -(13*r*y1 + 9*r*y2 - r*y4 - 7*r*y8
          - y1 - y2 - 13*y4 - y8) / 40,
        -(3*r*y2 + y1 + 3*y4 + y8) / 10,
        (-r*y2 + 3*y1 - y4 + 3*y8) / 10,
        -(r*y1 + r*y2 - 7*r*y4 + r*y8
          + 9*y1 + 13*y2 - 13*y4 - 11*y8) / 40,
        (r*y1 + 13*r*y2 + 13*r*y4 + r*y8
         - 7*y1 - 7*y2 - y4 + 13*y8) / 40,
    )
    chart_variables = sp.symbols("a0:6") + sp.symbols("b0:6")
    chart_substitution = dict(zip(chart_variables, a_values + b_values))
    base_values = tuple(reduce_r(chart_expression(poly, chart_variables)
                                 .subs(chart_substitution))
                        for poly in CHART.BASE)
    require(not any(base_values), "a purported base equation is nonzero")

    cleared_q_values = tuple(
        reduce_r(chart_expression(CHART.clear_denominators(poly),
                                  chart_variables).subs(chart_substitution))
        if poly else sp.Integer(0)
        for poly in CHART.Q_POLYS
    )
    q0 = -(6*r*y1*y2 + 22*r*y2*y2 + 18*r*y2*y4 + 6*r*y2*y8
           + 11*y1*y1 + 6*y1*y4 - 18*y1*y8 - 11*y2*y2
           - 11*y4*y4 + 6*y4*y8 + 11*y8*y8) / 80
    expected_q = (q0, y1, y2, -2*(r+2), y4, -2, 2, 0,
                  y8, 2, 2, 0, -2*(r+2), 0, 0, 0)
    require(cleared_q_values == tuple(map(reduce_r, expected_q)),
            "Q-coordinate normal form changed")

    raw_entries = []
    for edge in range(6):
        raw_entries.extend((a_values[edge], b_values[edge],
                            c_values[edge], sp.Integer(0)))
    raw_hafnian = RAW.matching_poly(tuple(range(8)))
    require(raw_evaluate(raw_hafnian, raw_entries) == 4,
            "raw pure Hafnian is not the constant four")
    raw_cofactors = tuple(derivative(raw_hafnian, variable)
                          for variable in range(24))
    generic_cofactor_values = tuple(raw_evaluate(poly, raw_entries)
                                    for poly in raw_cofactors)
    require(frozenset(index for index, value
                      in enumerate(generic_cofactor_values) if value != 0)
            == {3, 7, 9, 10, 13, 14, 19, 23},
            "generic cofactor support changed")

    fixed = frozenset((3, 5, 6, 9, 10, 12))
    y_indices = (1, 2, 4, 8)
    diagonal_coefficients = tuple(
        reduce_r(sp.expand(q0).coeff(variable, 2))
        for variable in (y1, y2, y4, y8)
    )
    require(all(value != 0 for value in diagonal_coefficients),
            "a one-coordinate Q0 coefficient vanished")

    # On every two-coordinate Q0=0 section, the four scale-dependent
    # cofactors C3,C7,C19,C23 remain nonzero.  A zero would give a common
    # projective root of a binary quadratic and a linear form; their exact
    # resultants are all nonzero in Q[r]/(r^2+2r-1).
    q0_numerator = sp.fraction(sp.cancel(q0))[0]
    variable_cofactor_indices = (3, 7, 19, 23)
    two_y_cofactor_resultants = {}
    y_variables = (y1, y2, y4, y8)
    for left_position, right_position in combinations(range(4), 2):
        left_variable = y_variables[left_position]
        right_variable = y_variables[right_position]
        zero_substitution = {
            variable: 0 for position, variable in enumerate(y_variables)
            if position not in (left_position, right_position)
        }
        binary_q0 = sp.expand(q0_numerator.subs(zero_substitution))
        pair_key = f"Q{y_indices[left_position]}_Q{y_indices[right_position]}"
        pair_record = {}
        for cofactor_index in variable_cofactor_indices:
            linear_cofactor = sp.expand(
                generic_cofactor_values[cofactor_index]
                .subs(zero_substitution)
            )
            resultant = reduce_r(sp.resultant(binary_q0, linear_cofactor,
                                               left_variable))
            require(resultant != 0,
                    f"C{cofactor_index} meets the {pair_key} Q0 conic")
            pair_record[f"C{cofactor_index}"] = str(resultant)
        two_y_cofactor_resultants[pair_key] = pair_record

    # Therefore support <=8 has exactly three forms: y=0 (support six),
    # one y nonzero (Q0 is also nonzero), or two y nonzero with Q0=0.
    support6 = fixed
    one_y_supports = tuple(fixed | {0, index} for index in y_indices)
    two_y_supports = tuple(fixed | set(pair)
                           for pair in combinations(y_indices, 2))
    require(all(len(row) == 8 for row in one_y_supports + two_y_supports),
            "low-support census changed")

    # Build literal X/cofactor/Q masks for each one-y line.  Every nonzero
    # entry/cofactor is a nonzero constant times T^0 or T^1, so its mask is
    # stable on the punctured line.
    one_y_records = []
    for position, index in enumerate(y_indices):
        substitution = {variable: (T if offset == position else 0)
                        for offset, variable in enumerate((y1, y2, y4, y8))}
        entries = tuple(reduce_r(sp.sympify(value).subs(substitution))
                        for value in raw_entries)
        cofactors = tuple(raw_evaluate(poly, entries)
                          for poly in raw_cofactors)
        for value in entries + cofactors:
            polynomial = sp.Poly(value, T)
            require(value == 0 or len(polynomial.terms()) == 1,
                    "a punctured-line support has an exceptional scale")
        q_values = tuple(raw_evaluate(RAW.q_poly(q_index), entries)
                         for q_index in range(16))
        entry_mask = bit_mask(i for i, value in enumerate(entries)
                              if value != 0)
        cofactor_mask = bit_mask(i for i, value in enumerate(cofactors)
                                 if value != 0)
        q_mask = bit_mask(i for i, value in enumerate(q_values)
                          if value != 0)
        require(frozenset(i for i in range(16) if q_mask & (1 << i))
                == one_y_supports[position], "one-y raw Q support changed")
        one_y_records.append((entry_mask, cofactor_mask, q_mask))

    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))

    def joint_orbit(record):
        entry_mask, cofactor_mask, q_mask = record
        return frozenset((
            COMPONENT.act_mask(entry_mask, 24,
                               COMPONENT.entry_action, action),
            COMPONENT.act_mask(cofactor_mask, 24,
                               COMPONENT.entry_action, action),
            COMPONENT.act_mask(q_mask, 16, CHART.SCREEN.act_index, action),
        ) for action in actions)

    one_y_orbits = tuple(joint_orbit(record) for record in one_y_records)
    require(all(len(orbit) == 192 for orbit in one_y_orbits),
            "one-y joint orbit size changed")

    support6_result = json.loads(
        COMPONENT.OUT.read_text()
    )
    support6_record = (
        bit_mask(support6_result["entry_nonzero_indices"]),
        bit_mask(support6_result["cofactor_nonzero_indices"]),
        bit_mask(support6_result["Q_support"]),
    )
    support6_orbit = joint_orbit(support6_record)
    require(len(support6_orbit) == 24, "support-six joint orbit changed")

    # The two-y class has no support-level mate at all.  The support-six and
    # one-y classes do, but every such pair already fails each direction of
    # the entry/cofactor equations.
    support_actions = lambda seed: frozenset(
        COMPONENT.act_mask(bit_mask(seed), 16, CHART.SCREEN.act_index, action)
        for action in actions
    )
    support_orbits = {
        "six": support_actions(support6),
        "one_y": support_actions(one_y_supports[0]),
        "two_y": support_actions(two_y_supports[0]),
    }
    require(tuple(map(len, support_orbits.values())) == (8, 64, 96),
            "support-orbit sizes changed")
    support_compatibility = {}
    for left_name, left_orbit in support_orbits.items():
        for right_name, right_orbit in support_orbits.items():
            support_compatibility[f"{left_name}_to_{right_name}"] = sum(
                not (left & q_complement(right))
                for left in left_orbit for right in right_orbit
            )
    require(support_compatibility == {
        "six_to_six": 32, "six_to_one_y": 64, "six_to_two_y": 0,
        "one_y_to_six": 64, "one_y_to_one_y": 64,
        "one_y_to_two_y": 0, "two_y_to_six": 0,
        "two_y_to_one_y": 0, "two_y_to_two_y": 0,
    }, "support compatibility census changed")

    directional = {"Q_compatible": 0, "left_X_right_C": 0,
                   "right_X_left_C": 0, "full": 0}
    left_union = frozenset().union(support6_orbit, *one_y_orbits)
    right_union = left_union
    for left in left_union:
        for right in right_union:
            q_ok = not (left[2] & q_complement(right[2]))
            left_ok = not (left[0] & right[1])
            right_ok = not (right[0] & left[1])
            directional["Q_compatible"] += q_ok
            directional["left_X_right_C"] += q_ok and left_ok
            directional["right_X_left_C"] += q_ok and right_ok
            directional["full"] += q_ok and left_ok and right_ok
    require(directional["Q_compatible"] > 0
            and directional["left_X_right_C"] == 0
            and directional["right_X_left_C"] == 0
            and directional["full"] == 0,
            "the low-support cofactor obstruction changed")

    result = {
        "status": "UNAUDITED exact weight-zero d=0 low-support normal form",
        "chart": "branch51 M_e=[[a_e,b_e],[-1/b_e,0]], all b_e nonzero",
        "b_ratio_groebner_basis": [str(value)
                                    for value in expected_ratio_basis],
        "raw_H": 4,
        "fixed_live_Q": sorted(fixed),
        "affine_coordinates": ["Q1", "Q2", "Q4", "Q8"],
        "Q0_quadratic": str(sp.factor(q0)),
        "Q0_diagonal_coefficients": [str(value)
                                      for value in diagonal_coefficients],
        "generic_cofactor_values": {
            str(index): str(value) for index, value
            in enumerate(generic_cofactor_values) if value != 0
        },
        "two_y_Q0_conic_cofactor_resultants": two_y_cofactor_resultants,
        "support_at_most_8_classification": {
            "support6": [sorted(support6)],
            "one_y_support8": [sorted(row) for row in one_y_supports],
            "two_y_Q0_zero_support8": [sorted(row)
                                        for row in two_y_supports],
            "support7_exists": False,
        },
        "support_orbit_sizes": {name: len(orbit)
                                for name, orbit in support_orbits.items()},
        "support_compatibility": support_compatibility,
        "one_y_signatures": [
            {
                "coordinate": f"Q{index}",
                "entry_nonzero_indices": [i for i in range(24)
                                           if record[0] & (1 << i)],
                "cofactor_nonzero_indices": [i for i in range(24)
                                              if record[1] & (1 << i)],
                "Q_nonzero_indices": [i for i in range(16)
                                       if record[2] & (1 << i)],
            }
            for index, record in zip(y_indices, one_y_records)
        ],
        "one_y_joint_orbit_sizes": [len(orbit) for orbit in one_y_orbits],
        "low_support6_one_y_joint_directional_census": directional,
        "scope": (
            "Exact on the localized weight-zero d=0 chart only.  It proves "
            "there is no support-seven stratum there and that all of its "
            "support-six/one-y transformed copies fail the full packet, but "
            "does not classify mate components in other cofactor charts."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight-zero d=0 low-support normal form: PASS")
    print("support orbits:", result["support_orbit_sizes"])
    print("joint directional census:", directional)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
