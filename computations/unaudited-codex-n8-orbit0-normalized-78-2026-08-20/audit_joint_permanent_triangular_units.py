#!/usr/bin/env python3
"""Joint cofactor/permanent chart census and two triangular-chart units.

The 64 cofactor orientations and 64 choices of a nonzero permanent term are
quotiented simultaneously by B4.  For two high-symmetry complementary joint
charts this checker then sets one entry of the *opposite* permanent term to
zero and solves the selected term exactly.  Two/three raw cofactor rows give
Laurent units, proving these closed triangular subcharts empty in char 0.

This does not prove the surrounding 18-variable permanent charts empty.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCREEN_PATH = HERE / "screen_lowq_joint_branch_orbits.py"
OUT = HERE / "results_joint_permanent_triangular_units.json"
VARIABLE_COUNT = 12
ONE = {(0,) * VARIABLE_COUNT: 1}


def load_screen():
    spec = importlib.util.spec_from_file_location("n8_joint_triangular_core",
                                                  SCREEN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCREEN = load_screen()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {exponent: coefficient for exponent, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, scalar):
    return clean({exponent: scalar * coefficient
                  for exponent, coefficient in poly.items()})


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                exponent = tuple(left[index] + right[index]
                                 for index in range(VARIABLE_COUNT))
                updated[exponent] += left_coefficient * right_coefficient
        answer = clean(updated)
    return answer


def variable(index, exponent=1):
    powers = [0] * VARIABLE_COUNT
    powers[index] = exponent
    return {tuple(powers): 1}


def triangular_entries(permanent_mask):
    entries = []
    denominators = []
    for edge in range(6):
        a_value = variable(2 * edge)
        b_value = variable(2 * edge + 1)
        if permanent_mask & (1 << edge):
            # Anti term b*c=-1 is selected; set d=0 and c=-1/b.
            entries.extend((a_value, b_value,
                            scale(variable(2 * edge + 1, -1), -1), {}))
            denominators.append(2 * edge + 1)
        else:
            # Diagonal term a*d=-1 is selected; set c=0 and d=-1/a.
            entries.extend((a_value, b_value, {},
                            scale(variable(2 * edge, -1), -1)))
            denominators.append(2 * edge)
    return tuple(entries), tuple(denominators)


def substitute(raw_poly, entries):
    answer = {}
    for monomial, integer_coefficient in raw_poly.items():
        term = scale(ONE, integer_coefficient)
        for raw_variable in monomial:
            term = multiply(term, entries[raw_variable])
        answer = add(answer, term)
    return answer


def cofactor_rows(branch_mask, permanent_mask):
    entries, denominators = triangular_entries(permanent_mask)
    raw_hafnian = SCREEN.CORE.pure_hafnian()
    rows = {}
    for edge in range(6):
        branch_bit = (branch_mask >> edge) & 1
        positions = (1, 2) if branch_bit else (0, 3)
        for position in positions:
            raw = SCREEN.PROBE.derivative(raw_hafnian, 4 * edge + position)
            rows[f"c{edge}_{position}"] = substitute(raw, entries)
    return rows, denominators


def joint_chart_census():
    rows = []
    expected = {0: (48, 11), 1: (8, 28), 11: (48, 11)}
    for branch in (0, 1, 11):
        stabilizer = tuple(action for action in SCREEN.ACTIONS
                           if SCREEN.act_branch_mask(branch, *action) == branch)
        seen = set()
        representatives = []
        for permanent in range(64):
            if permanent in seen:
                continue
            orbit = {SCREEN.act_branch_mask(permanent, *action)
                     for action in stabilizer}
            seen.update(orbit)
            representatives.append(min(orbit))
        representatives.sort()
        require((len(stabilizer), len(representatives)) == expected[branch],
                "joint chart census changed")
        rows.append({
            "cofactor_branch_representative": branch,
            "stabilizer_size": len(stabilizer),
            "permanent_chart_representatives": representatives,
            "joint_chart_count": len(representatives),
        })
    require(sum(row["joint_chart_count"] for row in rows) == 50,
            "total joint chart count changed")
    return rows


def main():
    census = joint_chart_census()

    # Weight-two branch, complementary permanent chart.
    rows2, denominators2 = cofactor_rows(1, 62)
    f30 = rows2["c3_0"]
    f40 = rows2["c4_0"]
    unit2 = scale(multiply(variable(3), variable(11),
                           variable(0, -1)), -2)
    identity2 = add(f40, multiply(variable(11), f30), scale(unit2, -1))
    require(not identity2, "weight-two Laurent unit identity failed")
    require({0, 3, 11}.issubset(denominators2),
            "weight-two RHS ceased to be a Laurent unit")
    mutation2 = add(f40, multiply(variable(11), f30),
                    multiply(variable(3), variable(11), variable(0, -1)))
    require(mutation2, "weight-two coefficient mutation did not fire")

    # Weight-four branch, complementary permanent chart.
    rows4, denominators4 = cofactor_rows(11, 52)
    f20 = rows4["c2_0"]
    f40_weight4 = rows4["c4_0"]
    f50 = rows4["c5_0"]
    unit4 = scale(multiply(variable(5), variable(9),
                           variable(0, -1), variable(11, -1)), 2)
    identity4 = add(
        f50,
        scale(multiply(variable(9), variable(11, -1), f40_weight4), -1),
        scale(multiply(variable(5), variable(11, -1), f20), -1),
        scale(unit4, -1),
    )
    require(not identity4, "weight-four Laurent unit identity failed")
    require({0, 5, 9, 11}.issubset(denominators4),
            "weight-four RHS ceased to be a Laurent unit")
    mutation4 = add(
        f50,
        scale(multiply(variable(9), variable(11, -1), f40_weight4), -1),
        scale(multiply(variable(5), variable(11, -1), f20), -1),
        scale(multiply(variable(5), variable(9),
                       variable(0, -1), variable(11, -1)), -1),
    )
    require(mutation4, "weight-four coefficient mutation did not fire")

    result = {
        "status": "UNAUDITED exact joint-chart census and Laurent identities",
        "joint_chart_census": census,
        "total_joint_chart_orbits": 50,
        "weight2_triangular_unit": {
            "cofactor_branch": 1,
            "permanent_term_chart": 62,
            "localized_variable_indices": list(denominators2),
            "raw_cofactor_rows": ["c3_0", "c4_0"],
            "identity": "c4_0+x11*c3_0=-2*x3*x11/x0",
            "rhs_unit_variable_indices": [0, 3, 11],
        },
        "weight4_triangular_unit": {
            "cofactor_branch": 11,
            "permanent_term_chart": 52,
            "localized_variable_indices": list(denominators4),
            "raw_cofactor_rows": ["c2_0", "c4_0", "c5_0"],
            "identity": (
                "c5_0-(x9/x11)c4_0-(x5/x11)c2_0="
                "2*x5*x9/(x0*x11)"
            ),
            "rhs_unit_variable_indices": [0, 5, 9, 11],
        },
        "triangular_substitution": (
            "per edge: selected anti => d=0,c=-1/b; selected diagonal => "
            "c=0,d=-1/a; localize only b or a respectively"
        ),
        "scope": (
            "These identities exclude one canonical closed triangular "
            "sublocus of each indicated joint chart.  They do not exclude "
            "the surrounding 18-variable permanent-term chart or other "
            "zero-entry choices."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("joint permanent triangular units: PASS")
    print("joint charts / branches:", 50, [row["joint_chart_count"]
                                           for row in census])
    print("weight2 / weight4 row counts:", 2, 3)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
