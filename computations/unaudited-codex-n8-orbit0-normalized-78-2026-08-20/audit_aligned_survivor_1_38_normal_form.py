#!/usr/bin/env python3
"""Exact normal form for aligned survivor (branch 1, term mask 38).

The saturated aligned chart has a 17-row Groebner basis and a three-parameter
normal form over Q(r), r^2+2r-1=0.  Its literal (X,cofactor,Q) support orbit is
the same 24-record orbit as the previously frozen weight-zero support-six
component, so it is not a new fixed-left packet type.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SCREEN_PATH = HERE / "screen_lowq_joint_branch_orbits.py"
SUPPORT6_PATH = HERE / "audit_weight0_support6_char0_component.py"
OUT = HERE / "results_aligned_survivor_1_38_normal_form.json"
F = Fraction
VARIABLE_COUNT = 12
ONE = {(0,) * VARIABLE_COUNT: F(1)}
BRANCH = 1
TERM_MASK = 38
EXPECTED_GROEBNER = (
    "b1^2*b5^2+2*b1*b2*b5-b2^2",
    "a0^3*b5*z+1",
    "b4", "b3", "b0", "a5", "a2", "a1",
    "a4^2*b5^2+2*a3*a4*b5-a3^2",
    "a3*b2-a0*b5",
    "a3*b1+a4*b2+2*a0",
    "a0^4*z-a4*b1",
    "a4*b2^2+a0*b1*b5+2*a0*b2",
    "a4*b1*b5+a0",
    "a4^2*b2*b5+2*a0*a4*b5-a0*a3",
    "a0^3*b2^2*z+b1^2*b5+2*b1*b2",
    "a0^3*a3^2*z+a4^2*b5+2*a3*a4",
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCREEN = load("n8_1_38_screen", SCREEN_PATH)
SUPPORT6 = load("n8_1_38_support6", SUPPORT6_PATH)


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


def scale(poly, coefficient):
    return clean({exponent: F(coefficient) * value
                  for exponent, value in poly.items()})


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                exponent = tuple(a + b for a, b in zip(left, right))
                updated[exponent] += left_coefficient * right_coefficient
        answer = clean(updated)
    return answer


def variable(index, exponent=1, coefficient=1):
    powers = [0] * VARIABLE_COUNT
    powers[index] = exponent
    return {tuple(powers): F(coefficient)}


def aligned_entries():
    entries = []
    for edge in range(6):
        a_value, b_value = variable(edge), variable(6 + edge)
        if TERM_MASK & (1 << edge):
            entries.extend((a_value, b_value,
                            variable(6 + edge, -1, -1), {}))
        else:
            entries.extend((a_value, b_value, {},
                            variable(edge, -1, -1)))
    return tuple(entries)


ENTRIES = aligned_entries()


def substitute(raw_poly):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = scale(ONE, coefficient)
        for raw_variable in monomial:
            term = multiply(term, ENTRIES[raw_variable])
        answer = add(answer, term)
    return answer


def clear_denominators(poly):
    shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                  for index in range(VARIABLE_COUNT))
    return {tuple(exponent[index] + shift[index]
                  for index in range(VARIABLE_COUNT)): coefficient
            for exponent, coefficient in poly.items()}


def singular(poly):
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = []
        for index, power in enumerate(exponent):
            if power:
                name = ("a" if index < 6 else "b") + str(index % 6)
                factors.append(name + (f"^{power}" if power != 1 else ""))
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        prefix = "-" if coefficient < 0 else ("+" if pieces else "")
        pieces.append(prefix + body)
    return "".join(pieces) if pieces else "0"


def exact_groebner():
    equations, _ = SCREEN.PROBE.equations(SCREEN.branch_bits(BRANCH))
    rows = []
    for raw in equations:
        specialized = substitute(raw)
        if specialized:
            rows.append(clear_denominators(specialized))
    variables = ",".join([f"a{index}" for index in range(6)]
                         + [f"b{index}" for index in range(6)] + ["z"])
    live_product = "a0*b1*b2*a3*a4*b5"
    command = (
        f"ring R=0,({variables}),dp;"
        f"ideal I={','.join(singular(row) for row in rows)},"
        f"z*{live_product}-1;ideal G=slimgb(I);"
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
    dimension = int(lines[end + 1])
    require(basis == EXPECTED_GROEBNER and dimension == 3,
            "(1,38) Groebner normal form changed")
    return rows, basis, dimension


K_ZERO = (F(0), F(0))
K_ONE = (F(1), F(0))
K_R = (F(0), F(1))


def k_add(*values):
    return (sum(value[0] for value in values),
            sum(value[1] for value in values))


def k_mul(left, right):
    return (left[0] * right[0] + left[1] * right[1],
            left[0] * right[1] + left[1] * right[0]
            - 2 * left[1] * right[1])


def evaluate(raw_poly, entries):
    answer = K_ZERO
    for monomial, coefficient in raw_poly.items():
        term = (F(coefficient), F(0))
        for raw_variable in monomial:
            term = k_mul(term, entries[raw_variable])
        answer = k_add(answer, term)
    return answer


def concrete_entries():
    # Free units a0=b1=b5=1; b2=r+2, a3=r, a4=-1.
    return (
        K_ONE, K_ZERO, K_ZERO, (F(-1), F(0)),
        K_ZERO, K_ONE, (F(-1), F(0)), K_ZERO,
        K_ZERO, (F(2), F(1)), (F(0), F(-1)), K_ZERO,
        K_R, K_ZERO, K_ZERO, (F(-2), F(-1)),
        (F(-1), F(0)), K_ZERO, K_ZERO, K_ONE,
        K_ZERO, K_ONE, (F(-1), F(0)), K_ZERO,
    )


def act_mask(mask, count, action_function, action):
    return sum(1 << action_function(index, *action)
               for index in range(count) if mask & (1 << index))


def main():
    rows, basis, dimension = exact_groebner()
    entries = concrete_entries()
    base, hafnian_poly = SCREEN.PROBE.equations(SCREEN.branch_bits(BRANCH))
    require(all(evaluate(poly, entries) == K_ZERO for poly in base),
            "literal base replay failed")
    hafnian = evaluate(hafnian_poly, entries)
    require(hafnian == (F(4), F(0)), "pure Hafnian changed")
    q_values = tuple(evaluate(SCREEN.q_poly(index), entries)
                     for index in range(16))
    q_mask = sum((value != K_ZERO) << index
                 for index, value in enumerate(q_values))
    require(tuple(index for index in range(16) if q_mask & (1 << index))
            == (1, 2, 7, 8, 13, 14), "Q support changed")
    cofactors = tuple(evaluate(SCREEN.PROBE.derivative(hafnian_poly, index),
                               entries) for index in range(24))
    x_mask = sum((value != K_ZERO) << index
                 for index, value in enumerate(entries))
    c_mask = sum((value != K_ZERO) << index
                 for index, value in enumerate(cofactors))
    require(x_mask == sum(1 << index for index in
                           (0, 3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22)),
            "X support changed")
    require(c_mask == sum(1 << index for index in (0, 3, 21, 22)),
            "cofactor support changed")

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
    require(len(orbit) == len(old_orbit) == 24 and orbit == old_orbit,
            "support-six joint orbit equivalence failed")

    result = {
        "status": "UNAUDITED exact aligned-survivor normal form",
        "joint_chart": [BRANCH, TERM_MASK],
        "derived_base_row_count": len(rows),
        "saturated_groebner_size": len(basis),
        "saturated_dimension": dimension,
        "normal_form": (
            "free units A=a0,U=b1,V=b5; r=b1*b5/b2, r^2+2r-1=0; "
            "b2=U*V/r, a3=A*r/U, a4=-A/(U*V); "
            "a1=a2=a5=b0=b3=b4=0"
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
        "consequence": (
            "Aligned survivor (1,38) is not a new fixed-left packet type; "
            "any global unit proved for the frozen support-six orbit applies."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("aligned survivor (1,38) normal form: PASS")
    print("Groebner size / dim:", len(basis), dimension)
    print("H / Q support:", 4, result["Q_nonzero_indices"])
    print("joint orbit equality / size:", True, len(orbit))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
