#!/usr/bin/env python3
"""Exact normal form for aligned survivor (branch 1, term mask 12)."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "audit_aligned_survivor_1_38_normal_form.py"
OUT = HERE / "results_aligned_survivor_1_12_normal_form.json"
BRANCH = 1
TERM_MASK = 12
EXPECTED_GROEBNER = (
    "a5^2*b3^2+2*a4*a5*b3-a4^2",
    "a5^2*b2^2+2*a1*a5*b2-a1^2",
    "a0^2*a1*a4*z+1",
    "b5", "b4", "b1", "b0", "a3", "a2",
    "a0^3*a5*b3*z+2*a0^3*a4*z-b3",
    "a0^2*a1^2*b3*z+b2",
    "a1^2*b3^2+2*a0*a1*b3-a0^2",
    "a4*b2-a1*b3",
    "2*a0^3*a1*b3*z-a0^4*z-b2*b3",
    "a0^3*a4*a5*z+2*a5*b3-a4",
    "a0^3*a1*a5*z+2*a5*b2-a1",
    "a0^4*a5*z-2*a1*b3-5*a0",
    "a5*b2*b3+a0",
    "2*a1*a5*b3-a1*a4-a0*a5",
    "a1*a4*b3+a0*a5*b3+2*a0*a4",
    "a0*a5*b2+a1^2*b3+2*a0*a1",
    "a0^3*a4^2*z-a5*b3^2",
    "a0^4*a4*z+a1*b3^2+2*a0*b3",
    "a0^3*a1^2*z-a5*b2^2",
    "a0^4*a1*z+a1*b2*b3+2*a0*b2",
    "2*a0*a5^2*b3+a1*a4^2+5*a0*a4*a5",
    "a1^2*a4^2+6*a0*a1*a4*a5+a0^2*a5^2",
    "a0^5*z+2*a1*b2*b3^2+5*a0*b2*b3",
)


def load_core():
    spec = importlib.util.spec_from_file_location("n8_1_12_core", CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()
SCREEN = CORE.SCREEN
SUPPORT6 = CORE.SUPPORT6


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def aligned_entries():
    entries = []
    for edge in range(6):
        a_value, b_value = CORE.variable(edge), CORE.variable(6 + edge)
        if TERM_MASK & (1 << edge):
            entries.extend((a_value, b_value,
                            CORE.variable(6 + edge, -1, -1), {}))
        else:
            entries.extend((a_value, b_value, {},
                            CORE.variable(edge, -1, -1)))
    return tuple(entries)


ENTRIES = aligned_entries()


def substitute(raw_poly):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = CORE.scale(CORE.ONE, coefficient)
        for raw_variable in monomial:
            term = CORE.multiply(term, ENTRIES[raw_variable])
        answer = CORE.add(answer, term)
    return answer


def exact_groebner():
    equations, _ = SCREEN.PROBE.equations(SCREEN.branch_bits(BRANCH))
    rows = [CORE.clear_denominators(substitute(raw)) for raw in equations
            if substitute(raw)]
    variables = ",".join([f"a{index}" for index in range(6)]
                         + [f"b{index}" for index in range(6)] + ["z"])
    command = (
        f"ring R=0,({variables}),dp;"
        f"ideal I={','.join(CORE.singular(row) for row in rows)},"
        "z*a0*a1*b2*b3*a4*a5-1;ideal G=slimgb(I);"
        'print("BEGIN");G;print("END");print(dim(G));quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular exact normal form failed")
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    basis = tuple(line.split("=", 1)[1] for line in lines[begin + 1:end])
    require(basis == EXPECTED_GROEBNER and int(lines[end + 1]) == 3,
            "(1,12) Groebner normal form changed")
    return rows, basis


def concrete_entries():
    zero = CORE.K_ZERO
    one = CORE.K_ONE
    r = CORE.K_R
    return (
        one, zero, zero, (F(-1), F(0)),
        r, zero, zero, (F(-2), F(-1)),
        zero, one, (F(-1), F(0)), zero,
        zero, one, (F(-1), F(0)), zero,
        r, zero, zero, (F(-2), F(-1)),
        (F(-1), F(0)), zero, zero, one,
    )


def act_mask(mask, count, action_function, action):
    return sum(1 << action_function(index, *action)
               for index in range(count) if mask & (1 << index))


def main():
    rows, basis = exact_groebner()
    entries = concrete_entries()
    base, hafnian_poly = SCREEN.PROBE.equations(SCREEN.branch_bits(BRANCH))
    require(all(CORE.evaluate(poly, entries) == CORE.K_ZERO for poly in base),
            "literal base replay failed")
    require(CORE.evaluate(hafnian_poly, entries) == (F(4), F(0)),
            "pure Hafnian changed")
    q_values = tuple(CORE.evaluate(SCREEN.q_poly(index), entries)
                     for index in range(16))
    q_mask = sum((value != CORE.K_ZERO) << index
                 for index, value in enumerate(q_values))
    require(tuple(index for index in range(16) if q_mask & (1 << index))
            == (0, 3, 5, 10, 12, 15), "Q support changed")
    cofactors = tuple(CORE.evaluate(SCREEN.PROBE.derivative(hafnian_poly, index),
                                    entries) for index in range(24))
    x_mask = sum((value != CORE.K_ZERO) << index
                 for index, value in enumerate(entries))
    c_mask = sum((value != CORE.K_ZERO) << index
                 for index, value in enumerate(cofactors))
    require(tuple(index for index in range(24) if c_mask & (1 << index))
            == (9, 10, 13, 14), "cofactor support changed")
    orbit = frozenset((
        act_mask(x_mask, 24, SUPPORT6.entry_action, action),
        act_mask(c_mask, 24, SUPPORT6.entry_action, action),
        act_mask(q_mask, 16, SCREEN.act_index, action),
    ) for action in SCREEN.ACTIONS)
    old_orbit = frozenset((
        act_mask(6710886, 24, SUPPORT6.entry_action, action),
        act_mask(26112, 24, SUPPORT6.entry_action, action),
        act_mask(5736, 16, SCREEN.act_index, action),
    ) for action in SCREEN.ACTIONS)
    require(len(orbit) == 24 and orbit == old_orbit,
            "support-six joint orbit equivalence failed")
    result = {
        "status": "UNAUDITED exact aligned-survivor normal form",
        "joint_chart": [BRANCH, TERM_MASK],
        "derived_base_row_count": len(rows),
        "saturated_groebner_size": len(basis),
        "saturated_dimension": 3,
        "normal_form": (
            "free units A=a0,U=b2,V=b3; r=a1*b3/a0, r^2+2r-1=0; "
            "a1=A*r/V,a4=A*r/U,a5=-A/(U*V); "
            "a2=a3=b0=b1=b4=b5=0"
        ),
        "H": "4",
        "Q_nonzero_indices": [index for index in range(16)
                              if q_mask & (1 << index)],
        "X_nonzero_indices": [index for index in range(24)
                              if x_mask & (1 << index)],
        "cofactor_nonzero_indices": [index for index in range(24)
                                     if c_mask & (1 << index)],
        "joint_X_C_Q_orbit_size": len(orbit),
        "equals_frozen_weight0_support6_joint_orbit": True,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("aligned survivor (1,12) normal form: PASS")
    print("Groebner size / dim:", len(basis), 3)
    print("H / Q support:", 4, result["Q_nonzero_indices"])
    print("joint orbit equality / size:", True, len(orbit))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
