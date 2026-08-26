#!/usr/bin/env python3
"""Four-row normal form for aligned survivor (branch 11, term 21).

Four literal specialized source rows force the pure Hafnian to be exactly 4
on this aligned chart.  The exact component on which all but the six smallest
Q coordinates vanish is also replayed and identified with the already frozen
weight-zero support-six joint (X, cofactor, Q) orbit.

This is only an aligned zero-cell boundary-chart statement.  It is not a
classification of the corresponding full 24-variable permanent-term chart.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "audit_aligned_survivor_1_38_normal_form.py"
OUT = HERE / "results_aligned_survivor_11_21_four_row_normal_form.json"
BRANCH = 11
TERM_MASK = 21
LOW_Q_SUPPORT = (1, 4, 7, 8, 11, 14)
EXPECTED_LOW_Q_BASIS_SHA256 = (
    "64f4202498b09e404727b3e223d2d3cb0a761b62b8a06f6a4ccdfc1a814d9fca"
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_11_21_core", CORE_PATH)
SCREEN = CORE.SCREEN
SUPPORT6 = CORE.SUPPORT6


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def chart_entries():
    answer = []
    for edge in range(6):
        a_value, b_value = CORE.variable(edge), CORE.variable(6 + edge)
        if TERM_MASK & (1 << edge):
            answer.extend((a_value, b_value,
                           CORE.variable(6 + edge, -1, -1), {}))
        else:
            answer.extend((a_value, b_value, {},
                           CORE.variable(edge, -1, -1)))
    return tuple(answer)


ENTRIES = chart_entries()


def substitute(raw_poly):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = CORE.scale(CORE.ONE, coefficient)
        for raw_variable in monomial:
            term = CORE.multiply(term, ENTRIES[raw_variable])
        answer = CORE.add(answer, term)
    return answer


def raw_labels():
    labels = ["e_01", "e_02", "e_03", "e_12", "e_13", "e_23"]
    labels += ["t_012", "t_013", "t_023", "t_123"]
    for edge, bit in enumerate(SCREEN.branch_bits(BRANCH)):
        for position in ((1, 2) if bit else (0, 3)):
            labels.append(f"cofactor_{edge}_{position}")
    return tuple(labels)


def derived_rows():
    equations, hafnian_raw = SCREEN.PROBE.equations(
        SCREEN.branch_bits(BRANCH))
    rows = {}
    cleared_rows = []
    seen = set()
    for label, raw in zip(raw_labels(), equations):
        specialized = substitute(raw)
        if not specialized:
            continue
        rows[label] = specialized
        cleared = CORE.clear_denominators(specialized)
        encoded = CORE.singular(cleared)
        if encoded not in seen:
            seen.add(encoded)
            cleared_rows.append((label, cleared))
    require(len(cleared_rows) == 15, "derived source-row count changed")
    return rows, tuple(cleared_rows), substitute(hafnian_raw)


def monomial(exponents, coefficient=1):
    return {tuple(exponents): F(coefficient)}


def param_variable(index, exponent=1, coefficient=1):
    return CORE.variable(index, exponent, coefficient)


def parameter_substitutions():
    # Parameter slots: A,B,C,x,y,z in indices 0,...,5.  They encode
    # a1=A, b0=B, b2=C, a3=xA/B, b4=yC/B, a5=zA/C.
    zero = {}
    return (
        zero,
        param_variable(0),
        zero,
        monomial((1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)),
        zero,
        monomial((1, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0)),
        param_variable(1),
        zero,
        param_variable(2),
        zero,
        monomial((0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0)),
        zero,
    )


PARAMS = parameter_substitutions()


def monomial_power(poly, power):
    require(len(poly) == 1, "parameter substitution is not monomial")
    exponent, coefficient = next(iter(poly.items()))
    return monomial(tuple(power * value for value in exponent),
                    coefficient ** power)


def parameterize(poly):
    answer = {}
    for exponent, coefficient in poly.items():
        term = CORE.scale(CORE.ONE, coefficient)
        killed = False
        for index, power in enumerate(exponent):
            if not power:
                continue
            replacement = PARAMS[index]
            if not replacement:
                require(power > 0,
                        "zero parameter was used with a negative exponent")
                killed = True
                break
            term = CORE.multiply(term, monomial_power(replacement, power))
        if not killed:
            answer = CORE.add(answer, term)
    return answer


def replace_y_by_x(poly):
    answer = {}
    for exponent, coefficient in poly.items():
        updated = list(exponent)
        updated[3] += updated[4]
        updated[4] = 0
        answer = CORE.add(answer, {tuple(updated): coefficient})
    return answer


def replay_four_row_identity(rows, literal_hafnian):
    a1, a3 = CORE.variable(1), CORE.variable(3)
    b0, b2, b4, b5 = (CORE.variable(6), CORE.variable(8),
                       CORE.variable(10), CORE.variable(11))
    c11 = CORE.clear_denominators(rows["cofactor_1_1"])
    c31 = CORE.clear_denominators(rows["cofactor_3_1"])
    difference = CORE.add(c11, CORE.scale(c31, -1))
    require(difference == CORE.scale(CORE.multiply(b2, b5), 2),
            "two-cofactor b5 identity changed")

    A, C = param_variable(0), param_variable(2)
    x, y, z = param_variable(3), param_variable(4), param_variable(5)
    fx = CORE.add(CORE.ONE, CORE.scale(x, -2),
                  CORE.scale(CORE.multiply(x, x), -1))
    g = CORE.add(CORE.multiply(x, y), x, y, CORE.scale(CORE.ONE, -1))
    require(parameterize(CORE.clear_denominators(rows["t_012"])) ==
            CORE.multiply(A, A, fx), "triangle x identity changed")
    require(parameterize(CORE.clear_denominators(rows["cofactor_5_0"])) ==
            CORE.scale(CORE.multiply(A, C, g), -1),
            "bridge identity changed")

    # (x+1)(x-y)+g=-fx and (x+1)^2=2-fx: over Q, fx=g=0
    # forces x=y.  Replay both identities literally.
    x_plus_one = CORE.add(x, CORE.ONE)
    x_minus_y = CORE.add(x, CORE.scale(y, -1))
    require(CORE.add(CORE.multiply(x_plus_one, x_minus_y), g, fx) == {},
            "x=y bridge ledger changed")
    require(CORE.add(CORE.multiply(x_plus_one, x_plus_one), fx,
                     CORE.scale(CORE.ONE, -2)) == {},
            "x+1 unit ledger changed")

    parameter_h = replace_y_by_x(parameterize(literal_hafnian))
    z2_plus = CORE.add(CORE.multiply(z, z), CORE.scale(z, 2),
                        CORE.scale(CORE.ONE, -1))
    correction = CORE.multiply(
        fx, z2_plus, param_variable(5, -1), param_variable(3, -1))
    expected_h = CORE.add(CORE.scale(CORE.ONE, 4), correction)
    require(parameter_h == expected_h,
            "raw pure-H four-row normal form changed")
    return {
        "rows": ["cofactor_1_1", "cofactor_3_1", "t_012",
                 "cofactor_5_0"],
        "ratios": {"x": "a3*b0/a1", "y": "b0*b4/b2",
                   "z": "a5*b2/a1"},
        "ledger": [
            "cofactor_1_1-cofactor_3_1=2*b2*b5, hence b5=0",
            "t_012/a1^2=fx=1-2*x-x^2",
            "cofactor_5_0/(-a1*b2)=g=x*y+x+y-1",
            "(x+1)(x-y)+g=-fx and (x+1)^2=2-fx, hence x=y",
            "H-4=fx*(z^2+2*z-1)/(z*x) after b5=0 and y=x",
        ],
        "conclusion": "literal H=4",
    }


def live_product():
    return "*".join(("b" if TERM_MASK & (1 << edge) else "a")
                    + str(edge) for edge in range(6))


def low_q_groebner(characteristic, cleared_rows):
    q_rows = []
    for index in range(16):
        if index in LOW_Q_SUPPORT:
            continue
        specialized = substitute(SCREEN.q_poly(index))
        if specialized:
            q_rows.append(CORE.clear_denominators(specialized))
    variables = ",".join([f"a{index}" for index in range(6)]
                         + [f"b{index}" for index in range(6)] + ["z"])
    generators = [CORE.singular(poly) for _, poly in cleared_rows]
    generators += [CORE.singular(poly) for poly in q_rows]
    command = (
        f"ring R={characteristic},({variables}),dp;"
        f"ideal I={','.join(generators)},z*{live_product()}-1;"
        'ideal G=slimgb(I);print("BEGIN");G;print("END");print(dim(G));quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"low-Q Singular run failed in characteristic {characteristic}")
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    basis = tuple(line.split("=", 1)[1] for line in lines[begin + 1:end])
    dimension = int(lines[end + 1])
    require(basis != ("1",) and dimension == 3,
            "low-Q component existence/dimension changed")
    return basis, len(q_rows)


def concrete_entries():
    zero, one, r = CORE.K_ZERO, CORE.K_ONE, CORE.K_R
    inverse_r = (F(2), F(1))
    values = (zero, one, zero, r, zero, r,
              one, zero, one, zero, r, zero)
    answer = []
    for edge in range(6):
        a_value, b_value = values[edge], values[6 + edge]
        if TERM_MASK & (1 << edge):
            inverse = one if b_value == one else inverse_r
            answer.extend((a_value, b_value, CORE.k_mul((-1, 0), inverse),
                           zero))
        else:
            inverse = one if a_value == one else inverse_r
            answer.extend((a_value, b_value, zero,
                           CORE.k_mul((-1, 0), inverse)))
    return tuple(answer)


def act_mask(mask, count, action_function, action):
    return sum(1 << action_function(index, *action)
               for index in range(count) if mask & (1 << index))


def concrete_orbit_check():
    entries = concrete_entries()
    base, hafnian_raw = SCREEN.PROBE.equations(SCREEN.branch_bits(BRANCH))
    require(all(CORE.evaluate(poly, entries) == CORE.K_ZERO for poly in base),
            "literal low-Q point failed a base row")
    require(CORE.evaluate(hafnian_raw, entries) == (F(4), F(0)),
            "literal low-Q point no longer has H=4")
    q_values = tuple(CORE.evaluate(SCREEN.q_poly(index), entries)
                     for index in range(16))
    q_mask = sum((value != CORE.K_ZERO) << index
                 for index, value in enumerate(q_values))
    require(tuple(index for index in range(16) if q_mask & (1 << index)) ==
            LOW_Q_SUPPORT, "literal low-Q support changed")
    cofactors = tuple(CORE.evaluate(SCREEN.PROBE.derivative(hafnian_raw, index),
                                    entries) for index in range(24))
    x_mask = sum((value != CORE.K_ZERO) << index
                 for index, value in enumerate(entries))
    c_mask = sum((value != CORE.K_ZERO) << index
                 for index, value in enumerate(cofactors))
    require((x_mask, c_mask, q_mask) == (9868950, 38400, 18834),
            "literal low-Q joint support record changed")
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
            "low-Q support-six joint orbit equivalence failed")
    return x_mask, c_mask, q_mask, len(orbit)


def main():
    rows, cleared_rows, literal_hafnian = derived_rows()
    four_row = replay_four_row_identity(rows, literal_hafnian)
    exact_basis, added_q_rows = low_q_groebner(0, cleared_rows)
    exact_sha = sha256("\n".join(exact_basis).encode("ascii")).hexdigest()
    require(len(exact_basis) == 29 and exact_sha == EXPECTED_LOW_Q_BASIS_SHA256,
            "exact low-Q Groebner basis changed")
    modular_sizes = {}
    for prime in (1009, 1013):
        basis, modular_added = low_q_groebner(prime, cleared_rows)
        require(modular_added == added_q_rows,
                "modular low-Q source count changed")
        modular_sizes[str(prime)] = len(basis)
    x_mask, c_mask, q_mask, orbit_size = concrete_orbit_check()
    result = {
        "status": "UNAUDITED exact aligned-survivor four-row normal form",
        "joint_chart": [BRANCH, TERM_MASK],
        "scope": "only the aligned zero-cell boundary chart",
        "derived_source_row_count": len(cleared_rows),
        "four_row_normal_form": four_row,
        "low_Q_component": {
            "Q_nonzero_indices": list(LOW_Q_SUPPORT),
            "added_zero_Q_row_count": added_q_rows,
            "exact_saturated_basis_size": len(exact_basis),
            "exact_saturated_dimension": 3,
            "exact_basis_sha256": exact_sha,
            "modular_basis_sizes": modular_sizes,
            "literal_X_C_Q_masks": [x_mask, c_mask, q_mask],
            "joint_orbit_size": orbit_size,
            "equals_frozen_weight0_support6_joint_orbit": True,
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("aligned survivor (11,21) four-row normal form: PASS")
    print("literal H / low-Q support:", 4, list(LOW_Q_SUPPORT))
    print("low-Q GB size/dim / old orbit equality:",
          len(exact_basis), 3, True)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
