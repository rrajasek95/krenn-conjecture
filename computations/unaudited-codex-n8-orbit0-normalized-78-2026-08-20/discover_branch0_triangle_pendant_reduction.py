#!/usr/bin/env python3
"""Discovery helper for branch-zero triangle-plus-pendant defect support.

Support edge indices are {2,3,4,5}; the torus gauge is
b2=b4=b5=d2=1.  This file only prints/factors the specialized literal rows
and runs small elimination probes.  It makes no closure claim.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import argparse
import time


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_nonaligned_defect_strata.py"


def load():
    spec = importlib.util.spec_from_file_location("n8_defect_probe", PROBE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROBE = load()
CHART = PROBE.Chart((2, 3, 4, 5))


def power(poly, exponent):
    answer = CHART.one
    for _ in range(exponent):
        answer = CHART.multiply(answer, poly)
    return answer


def substitute_poly(poly, replacements):
    answer = {}
    for exponent, coefficient in poly.items():
        term = CHART.scale(CHART.one, coefficient)
        for index, multiplicity in enumerate(exponent):
            if multiplicity:
                term = CHART.multiply(term, power(replacements[index], multiplicity))
        answer = CHART.add(answer, term)
    return answer


def inverse_monomial(*indices):
    exponent = [0] * CHART.n
    for index in indices:
        exponent[index] -= 1
    return {tuple(exponent): PROBE.F(1)}


def gauged_rows():
    rows, _, hafnian = CHART.rows_and_hafnian()
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    for index in (8, 10, 11, CHART.d_index[2]):
        replacements[index] = CHART.one
    return [(label, substitute_poly(poly, replacements))
            for label, poly, _ in rows], substitute_poly(hafnian, replacements)


def solve_a0_a3():
    """Use literal rows R20 and R14 over the already localized torus."""
    rows, hafnian = gauged_rows()
    row_map = dict(rows)
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    b0, b1, b3 = (CHART.variable(index) for index in (6, 7, 9))
    d3 = CHART.variable(CHART.d_index[3])
    d4 = CHART.variable(CHART.d_index[4])
    d5 = CHART.variable(CHART.d_index[5])
    a0_numerator = CHART.add(
        d3, CHART.multiply(b1, d4),
        CHART.scale(CHART.multiply(b0, d3), -1),
        CHART.scale(CHART.multiply(b0, b3, d4), -1),
        CHART.scale(CHART.multiply(b0, b1), -1),
        CHART.scale(CHART.multiply(b0, b0, b3), -1))
    a3_numerator = CHART.add(
        CHART.scale(CHART.multiply(b1, d5), -1),
        CHART.multiply(b1, b3, d4), CHART.multiply(b1, b3, d3),
        CHART.multiply(b0, b3, d5), CHART.multiply(b0, b3, d3),
        CHART.multiply(b0, b3, b3, d4))
    replacements[0] = CHART.multiply(a0_numerator, inverse_monomial(6, CHART.d_index[3]))
    replacements[3] = CHART.multiply(a3_numerator, inverse_monomial(7, CHART.d_index[3],
                                                                    CHART.d_index[5]))
    reduced = []
    for label, poly in rows:
        value = CHART.clear_denominators(substitute_poly(poly, replacements))
        if value:
            reduced.append((label, value))
    assert 14 not in dict(reduced) and 20 not in dict(reduced)
    return reduced, CHART.clear_denominators(substitute_poly(hafnian, replacements)), replacements


def solve_a0_a3_a1():
    """Additionally solve literal R6 for a1; R18 then carries the d-relation."""
    rows, hafnian, first_replacements = solve_a0_a3()
    row_map = dict(rows)
    r6 = row_map[6]
    constant, coefficient = {}, {}
    for exponent, value in r6.items():
        exponent = list(exponent)
        power_a1 = exponent[1]
        assert power_a1 in (0, 1)
        if power_a1:
            exponent[1] = 0
            coefficient[tuple(exponent)] = value
        else:
            constant[tuple(exponent)] = value
    assert len(coefficient) == 1
    coefficient_monomial, coefficient_scalar = next(iter(coefficient.items()))
    inverse = tuple(-power for power in coefficient_monomial)
    a1_value = CHART.scale(
        CHART.multiply(constant, {inverse: PROBE.F(1)}),
        -PROBE.F(1) / coefficient_scalar)
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    replacements[1] = a1_value
    reduced = []
    for label, poly in rows:
        value = CHART.clear_denominators(substitute_poly(poly, replacements))
        if value:
            reduced.append((label, value))
    assert 6 not in dict(reduced)
    return reduced, CHART.clear_denominators(substitute_poly(hafnian, replacements)), (
        first_replacements, replacements)


def use_derived_d_relation():
    """Substitute d3=-b1*d4-b0*d5 using the localized R6/R18 ledger."""
    rows, hafnian = gauged_rows()
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    replacements[CHART.d_index[3]] = CHART.scale(CHART.add(
        CHART.multiply(CHART.variable(7), CHART.variable(CHART.d_index[4])),
        CHART.multiply(CHART.variable(6), CHART.variable(CHART.d_index[5]))), -1)
    reduced, seen = [], set()
    for label, poly in rows:
        value = substitute_poly(poly, replacements)
        if not value:
            continue
        encoded = CHART.singular(value)
        if encoded in seen:
            continue
        seen.add(encoded)
        reduced.append((label, value))
    return reduced, substitute_poly(hafnian, replacements), replacements


def solve_a0_a3_use_d_relation():
    """Solve a0/a3 first, then apply the derived linear d3 relation."""
    rows, hafnian, first_replacements = solve_a0_a3()
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    replacements[CHART.d_index[3]] = CHART.scale(CHART.add(
        CHART.multiply(CHART.variable(7), CHART.variable(CHART.d_index[4])),
        CHART.multiply(CHART.variable(6), CHART.variable(CHART.d_index[5]))), -1)
    reduced, seen = [], set()
    for label, poly in rows:
        value = CHART.clear_denominators(substitute_poly(poly, replacements))
        if not value:
            continue
        encoded = CHART.singular(value)
        if encoded in seen:
            continue
        seen.add(encoded)
        reduced.append((label, value))
    live_replacements = {index: CHART.variable(index)
                         for index in range(CHART.n)}
    live_replacements[3] = CHART.clear_denominators(
        substitute_poly(first_replacements[3], replacements))
    live_replacements[CHART.d_index[3]] = replacements[CHART.d_index[3]]
    return reduced, CHART.clear_denominators(
        substitute_poly(hafnian, replacements)), live_replacements


def solve_row_variable(rows, hafnian, row_label, variable_index):
    """Solve a literal linear row whose coefficient is a Laurent monomial."""
    row_map = dict(rows)
    pivot = row_map[row_label]
    constant, coefficient = {}, {}
    for exponent, value in pivot.items():
        exponent = list(exponent)
        degree = exponent[variable_index]
        assert degree in (0, 1), (row_label, variable_index, degree)
        if degree:
            exponent[variable_index] = 0
            coefficient[tuple(exponent)] = value
        else:
            constant[tuple(exponent)] = value
    assert len(coefficient) == 1, (row_label, len(coefficient))
    coefficient_monomial, coefficient_scalar = next(iter(coefficient.items()))
    inverse = tuple(-power for power in coefficient_monomial)
    value = CHART.scale(CHART.multiply(constant, {inverse: PROBE.F(1)}),
                        -PROBE.F(1) / coefficient_scalar)
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    replacements[variable_index] = value
    reduced, seen = [], set()
    for label, poly in rows:
        result = CHART.clear_denominators(substitute_poly(poly, replacements))
        if not result:
            continue
        encoded = CHART.singular(result)
        if encoded in seen or CHART.singular(CHART.scale(result, -1)) in seen:
            continue
        seen.add(encoded)
        reduced.append((label, result))
    return reduced, CHART.clear_denominators(
        substitute_poly(hafnian, replacements)), value


def solve_b0_a3_a1():
    """Use E for b0, then literal R14 for a3 and R6 for a1."""
    rows, hafnian = gauged_rows()
    b1 = CHART.variable(7)
    d3 = CHART.variable(CHART.d_index[3])
    d4 = CHART.variable(CHART.d_index[4])
    d5 = CHART.variable(CHART.d_index[5])
    b0_numerator = CHART.scale(CHART.add(d3, CHART.multiply(b1, d4)), -1)
    b0_value = CHART.multiply(b0_numerator,
                              inverse_monomial(CHART.d_index[5]))
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    replacements[6] = b0_value
    first_rows = [(label, CHART.clear_denominators(
        substitute_poly(poly, replacements))) for label, poly in rows]
    first_h = CHART.clear_denominators(substitute_poly(hafnian, replacements))
    second_rows, second_h, a3_value = solve_row_variable(
        first_rows, first_h, 14, 3)
    third_rows, third_h, a1_value = solve_row_variable(
        second_rows, second_h, 6, 1)
    live_replacements = {index: CHART.variable(index)
                         for index in range(CHART.n)}
    live_replacements[6] = CHART.clear_denominators(b0_value)
    live_replacements[3] = CHART.clear_denominators(a3_value)
    return third_rows, third_h, live_replacements, (b0_value, a3_value, a1_value)


def solve_a0_a3_a2():
    """Solve R20/R14, derive E, then solve R16+a2*E for a2."""
    rows, hafnian, first_replacements = solve_a0_a3()
    e_relation = CHART.add(
        CHART.variable(CHART.d_index[3]),
        CHART.multiply(CHART.variable(7), CHART.variable(CHART.d_index[4])),
        CHART.multiply(CHART.variable(6), CHART.variable(CHART.d_index[5])))
    updated = []
    for label, poly in rows:
        if label == 16:
            poly = CHART.add(poly, CHART.multiply(CHART.variable(2), e_relation))
        updated.append((label, poly))
    reduced, reduced_h, a2_value = solve_row_variable(updated, hafnian, 16, 2)
    reduced.append((100, e_relation))
    live_replacements = {index: CHART.variable(index)
                         for index in range(CHART.n)}
    live_replacements[2] = CHART.clear_denominators(a2_value)
    live_replacements[3] = CHART.clear_denominators(first_replacements[3])
    return reduced, reduced_h, live_replacements, (first_replacements, a2_value)


def solve_a0_a3_a2_a1():
    """Continue the localized chain by solving reduced R6 for a1."""
    rows, hafnian, live_replacements, prior = solve_a0_a3_a2()
    rows, hafnian, a1_value = solve_row_variable(rows, hafnian, 6, 1)
    # R18=-2*b3*d5*E after this reduction, and E itself is synthetic row100.
    rows = [(label, poly) for label, poly in rows if label != 18]
    return rows, hafnian, live_replacements, prior + (a1_value,)


def solve_full_chain_use_e():
    """Finally use monic E to remove d3 after all Laurent substitutions."""
    rows, hafnian, live_replacements, prior = solve_a0_a3_a2_a1()
    replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    replacements[CHART.d_index[3]] = CHART.scale(CHART.add(
        CHART.multiply(CHART.variable(7), CHART.variable(CHART.d_index[4])),
        CHART.multiply(CHART.variable(6), CHART.variable(CHART.d_index[5]))), -1)
    reduced, seen = [], set()
    for label, poly in rows:
        value = substitute_poly(poly, replacements)
        if not value:
            continue
        encoded = CHART.singular(value)
        negative = CHART.singular(CHART.scale(value, -1))
        if encoded in seen or negative in seen:
            continue
        seen.add(encoded)
        reduced.append((label, value))
    final_live = {index: substitute_poly(poly, replacements)
                  for index, poly in live_replacements.items()}
    return reduced, substitute_poly(hafnian, replacements), final_live, prior


def singular_probe(characteristic, order_names, split_localizers, timeout,
                   solve_linear=False, include_h=True, solve_a1=False,
                   use_d_relation=False, solve_linear_use_d=False,
                   solve_b0_chain=False, include_c=False, c_edges=(2, 3, 4, 5),
                   algorithm="slimgb", localizers_first=False,
                   term_order="dp", solve_a2_chain=False,
                   localizer_scheme="two", solve_a1_after_a2=False,
                   protocol=False, use_e_after_chain=False):
    if use_e_after_chain:
        rows, hafnian, replacements, _ = solve_full_chain_use_e()
    elif solve_a1_after_a2:
        rows, hafnian, replacements, _ = solve_a0_a3_a2_a1()
    elif solve_a2_chain:
        rows, hafnian, replacements, _ = solve_a0_a3_a2()
    elif solve_b0_chain:
        rows, hafnian, replacements, _ = solve_b0_a3_a1()
    elif solve_linear_use_d:
        rows, hafnian, replacements = solve_a0_a3_use_d_relation()
    elif use_d_relation:
        rows, hafnian, replacements = use_derived_d_relation()
    elif solve_a1:
        rows, hafnian, replacement_pair = solve_a0_a3_a1()
        first_replacements, second_replacements = replacement_pair
        replacements = {index: CHART.variable(index)
                        for index in range(CHART.n)}
        # Only a3 occurs in the defect live product.  Its denominator is a
        # product of already-live b/d variables, so localizing its cleared
        # numerator is equivalent and avoids Laurent substitution.
        replacements[3] = CHART.clear_denominators(first_replacements[3])
    elif solve_linear:
        rows, hafnian, replacements = solve_a0_a3()
    else:
        rows, hafnian = gauged_rows()
        replacements = {index: CHART.variable(index) for index in range(CHART.n)}
    live_b = CHART.multiply(replacements[6], replacements[7],
                            replacements[9])
    live_a = CHART.one
    live_d = CHART.one
    live_c = CHART.one
    for edge in (2, 3, 4, 5):
        live_a = CHART.multiply(live_a, replacements[edge])
        if edge != 2:
            live_d = CHART.multiply(
                live_d, replacements[CHART.d_index[edge]])
        d_value = (CHART.one if edge == 2 else
                   replacements[CHART.d_index[edge]])
        if edge in c_edges:
            live_c = CHART.multiply(live_c, CHART.add(
                CHART.one, CHART.multiply(replacements[edge], d_value)))
    if split_localizers:
        if localizer_scheme == "individual":
            require_factors = [replacements[6], replacements[7], replacements[9],
                               replacements[2], replacements[3],
                               replacements[4], replacements[5],
                               replacements[CHART.d_index[3]],
                               replacements[CHART.d_index[4]],
                               replacements[CHART.d_index[5]]]
            locator_names = [f"u{index}" for index in range(len(require_factors))]
            if include_h:
                locator_names = ["uh"] + locator_names
        else:
            locator_names = (["u"] if include_h else []) + ["z", "w"]
        if localizer_scheme == "three":
            locator_names += ["v"]
        variables = ((locator_names + order_names) if localizers_first else
                     (order_names + locator_names))
        if localizer_scheme == "individual":
            localizers = ([f"uh*({CHART.singular(hafnian)})-1"]
                          if include_h else [])
            localizers += [f"u{index}*({CHART.singular(factor)})-1"
                           for index, factor in enumerate(require_factors)]
        else:
            localizers = ([f"u*({CHART.singular(hafnian)})-1"]
                          if include_h else [])
            localizers += [f"z*({CHART.singular(live_b)})-1"]
        if localizer_scheme == "three":
            localizers += [f"w*({CHART.singular(live_a)})-1",
                           f"v*({CHART.singular(CHART.multiply(live_d, live_c) if include_c else live_d)})-1"]
        elif localizer_scheme == "two":
            live_ad = CHART.multiply(live_a, live_d)
            localizers += [f"w*({CHART.singular(CHART.multiply(live_ad, live_c) if include_c else live_ad)})-1"]
    else:
        variables = (["u"] + order_names if localizers_first else
                     order_names + ["u"])
        factors = tuple([hafnian] if include_h else []) + (live_b, live_a, live_d)
        if include_c:
            factors += (live_c,)
        live = CHART.multiply(*factors)
        localizers = [f"u*({CHART.singular(live)})-1"]
    generators = [CHART.singular(poly) for _, poly in rows] + localizers
    library = 'LIB "modstd.lib";' if algorithm in ("modStd", "modGB") else ""
    algorithm_call = ('modGB("slimgb",I,1)' if algorithm == "modGB"
                      else f"{algorithm}(I)")
    command = (
        library +
        f"ring R={characteristic},({','.join(variables)}),{term_order};"
        + ("option(prot);" if protocol else "") +
        f"ideal I={','.join(generators)};"
        f'ideal G={algorithm_call};print("BEGIN");print(string(reduce(1,G)));'
        'print(size(G));print(dim(G));print("END");quit;')
    started = time.monotonic()
    try:
        singular_args = (["Singular", "--cpus=1", "--threads=1", "-q", "-c", command]
                         if algorithm in ("modStd", "modGB") else
                         ["Singular", "-q", "-c", command])
        completed = subprocess.run(singular_args,
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return time.monotonic() - started, stdout + "\nTIMEOUT", stderr


def c2_nilpotence_probe(characteristic, timeout):
    rows, _ = gauged_rows()
    live_b = CHART.multiply(CHART.variable(6), CHART.variable(7),
                            CHART.variable(9))
    live_ad = CHART.one
    for edge in (2, 3, 4, 5):
        live_ad = CHART.multiply(live_ad, CHART.variable(edge))
        if edge != 2:
            live_ad = CHART.multiply(live_ad,
                                     CHART.variable(CHART.d_index[edge]))
    names = ["a0", "a1", "a2", "a3", "a4", "a5", "b0", "b1", "b3",
             "d3", "d4", "d5", "z", "w"]
    generators = [CHART.singular(poly) for _, poly in rows]
    generators += [f"z*({CHART.singular(live_b)})-1",
                   f"w*({CHART.singular(live_ad)})-1"]
    tests = ";".join(
        f'print("POWER {power}");print(string(reduce((1+a2)^{power},G)))'
        for power in range(1, 9))
    command = (f"ring R={characteristic},({','.join(names)}),dp;"
               f"ideal I={','.join(generators)};ideal G=slimgb(I);"
               f'{tests};print("SIZE");print(size(G));quit;')
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired:
        return time.monotonic() - started, "TIMEOUT", ""


def homogeneous_probe(characteristic, timeout, modular):
    rows, _ = gauged_rows()
    live_b = CHART.multiply(CHART.variable(6), CHART.variable(7),
                            CHART.variable(9))
    live_a = CHART.one
    live_d = CHART.one
    for edge in (2, 3, 4, 5):
        live_a = CHART.multiply(live_a, CHART.variable(edge))
        if edge != 2:
            live_d = CHART.multiply(live_d,
                                     CHART.variable(CHART.d_index[edge]))
    names = ["z", "w", "a0", "a1", "a2", "a3", "a4", "a5",
             "b0", "b1", "b3", "d3", "d4", "d5", "t"]
    generators = [CHART.singular(poly) for _, poly in rows]
    generators += [f"z*({CHART.singular(live_b)})-1",
                   f"w*({CHART.singular(CHART.multiply(live_a, live_d))})-1"]
    algorithm = 'modGB("slimgb",J)' if modular else "slimgb(J)"
    library = 'LIB "modstd.lib";' if modular else ""
    tests = ";".join(
        f'print("POWER {power}");print(string(reduce(t^{power},G)))'
        for power in range(1, 31))
    command = (library +
               f"ring R={characteristic},({','.join(names)}),Dp;"
               f"ideal I={','.join(generators)};ideal J=homog(I,t);"
               f"ideal G={algorithm};print(\"SIZE\");print(size(G));"
               f"{tests};quit;")
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired:
        return time.monotonic() - started, "TIMEOUT", ""


def homogeneous_chain_probe(characteristic, timeout, modular):
    rows, _, replacements, _ = solve_a0_a3_a2_a1()
    live_b = CHART.multiply(replacements[6], replacements[7], replacements[9])
    live_a = CHART.one
    live_d = CHART.one
    for edge in (2, 3, 4, 5):
        live_a = CHART.multiply(live_a, replacements[edge])
        if edge != 2:
            live_d = CHART.multiply(live_d,
                                     replacements[CHART.d_index[edge]])
    names = ["z", "w", "a4", "a5", "b0", "b1", "b3",
             "d3", "d4", "d5", "t"]
    generators = [CHART.singular(poly) for _, poly in rows]
    generators += [f"z*({CHART.singular(live_b)})-1",
                   f"w*({CHART.singular(CHART.multiply(live_a, live_d))})-1"]
    algorithm = 'modGB("slimgb",J)' if modular else "slimgb(J)"
    library = 'LIB "modstd.lib";' if modular else ""
    tests = ";".join(
        f'print("POWER {power}");print(string(reduce(t^{power},G)))'
        for power in range(1, 61))
    command = (library +
               f"ring R={characteristic},({','.join(names)}),Dp;"
               f"ideal I={','.join(generators)};ideal J=homog(I,t);"
               f"ideal G={algorithm};print(\"SIZE\");print(size(G));"
               f"{tests};quit;")
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired:
        return time.monotonic() - started, "TIMEOUT", ""


def sequential_saturation_probe(characteristic, timeout, reverse=False):
    rows, _, replacements, _ = solve_a0_a3_a2_a1()
    names = ["a4", "a5", "b0", "b1", "b3", "d3", "d4", "d5"]
    factors = ["b0", "b1", "b3", "d3", "d4", "d5", "a4", "a5",
               CHART.singular(replacements[2]),
               CHART.singular(replacements[3])]
    if reverse:
        factors = list(reversed(factors))
    generators = [CHART.singular(poly) for _, poly in rows]
    commands = ['LIB "elim.lib";',
                f"ring R={characteristic},({','.join(names)}),Dp;",
                f"ideal I={','.join(generators)};"]
    for index, factor in enumerate(factors):
        commands += [f"I=sat(I,ideal({factor}));",
                     f'print("STEP {index}");print(size(I));print(dim(I));']
    commands += ['print("BEGIN");print(string(reduce(1,I)));',
                 'print(size(I));print(dim(I));print("END");quit;']
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", "".join(commands)],
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return time.monotonic() - started, stdout + "\nTIMEOUT", stderr


def reduced_lift_probe(characteristic, timeout):
    rows, _, replacements, _ = solve_a0_a3_a2_a1()
    live_b = CHART.multiply(replacements[6], replacements[7], replacements[9])
    live_a = CHART.one
    live_d = CHART.one
    for edge in (2, 3, 4, 5):
        live_a = CHART.multiply(live_a, replacements[edge])
        if edge != 2:
            live_d = CHART.multiply(live_d,
                                     replacements[CHART.d_index[edge]])
    names = ["z", "w", "a4", "a5", "b0", "b1", "b3",
             "d3", "d4", "d5"]
    generators = [CHART.singular(poly) for _, poly in rows]
    generators += [f"z*({CHART.singular(live_b)})-1",
                   f"w*({CHART.singular(CHART.multiply(live_a, live_d))})-1"]
    command = (
        f"ring R={characteristic},({','.join(names)}),Dp;"
        f"ideal I={','.join(generators)};ideal T=1;matrix L=lift(I,T);"
        'poly check=1;int terms=0;int maxd=0;int dd;'
        'for(int i=1;i<=nrows(L);i++){check=check-L[i,1]*I[i];'
        'terms=terms+size(L[i,1]);dd=deg(L[i,1])+deg(I[i]);'
        'if(dd>maxd){maxd=dd;}'
        'print("ENTRY");print(i);print(size(L[i,1]));print(deg(L[i,1]));}'
        'print("BEGIN");print(string(check));print(nrows(L));print(terms);'
        'print(maxd);print("END");quit;')
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return time.monotonic() - started, stdout + "\nTIMEOUT", stderr


def split_linear(poly, indices=(4, 5)):
    constant, coefficients = {}, {index: {} for index in indices}
    for exponent, value in poly.items():
        degrees = [exponent[index] for index in indices]
        if sum(degrees) > 1 or any(degree not in (0, 1) for degree in degrees):
            raise RuntimeError(("not jointly linear", degrees))
        target = constant
        if sum(degrees) == 1:
            index = indices[degrees.index(1)]
            target = coefficients[index]
            exponent = list(exponent)
            exponent[index] = 0
            exponent = tuple(exponent)
        target[exponent] = value
    return constant, coefficients[indices[0]], coefficients[indices[1]]


def cramer_pair_census():
    rows, _, _, _ = solve_a0_a3_a2_a1()
    linear = {label: split_linear(poly) for label, poly in rows if label != 100}
    census = []
    labels = sorted(linear)
    for left_index, left in enumerate(labels):
        for right in labels[left_index + 1:]:
            _, l4, l5 = linear[left]
            _, r4, r5 = linear[right]
            determinant = CHART.add(CHART.multiply(l4, r5),
                                    CHART.scale(CHART.multiply(l5, r4), -1))
            census.append((len(determinant),
                           max([sum(exponent) for exponent in determinant] + [-1]),
                           left, right, determinant))
    census.sort(key=lambda item: item[:4])
    return linear, census


def cramer_e_factor_summary(limit=55):
    """Factor Cramer determinants after imposing the proved monic row E=0.

    The output deliberately records only factor degrees/term counts, except for
    short factors.  This keeps the discovery ledger readable while allowing us
    to see whether a determinant is a product of already-localized factors.
    """
    _, census = cramer_pair_census()
    e_replacements = {index: CHART.variable(index)
                      for index in range(CHART.n)}
    e_replacements[CHART.d_index[3]] = CHART.scale(CHART.add(
        CHART.multiply(CHART.variable(7),
                       CHART.variable(CHART.d_index[4])),
        CHART.multiply(CHART.variable(6),
                       CHART.variable(CHART.d_index[5]))), -1)
    # Numerator of the previously solved/live a3.  Its specialization modulo E
    # is a legitimate coefficient-field localizer in the six-to-five-variable
    # Cramer calculation.
    _, _, first_replacements, _ = solve_a0_a3_a2_a1()
    a3_numerator = CHART.clear_denominators(first_replacements[3])
    a3_e = substitute_poly(a3_numerator, e_replacements)
    names = ["b0", "b1", "b3", "d4", "d5"]
    command = f"ring R=0,({','.join(names)}),dp;"
    command += (f'poly liveA3={CHART.singular(a3_e)};'
                'list lf=factorize(liveA3);print("LIVE_A3");'
                'for(int k=1;k<=size(lf[1]);k++)'
                '{print("F");print(lf[2][k]);print(size(lf[1][k]));'
                'print(deg(lf[1][k]));if(size(lf[1][k])<=12)'
                '{print(string(lf[1][k]));}}')
    selected = []
    for raw_terms, raw_degree, left, right, determinant in census[:limit]:
        determinant_e = substitute_poly(determinant, e_replacements)
        if not determinant_e:
            selected.append((left, right, raw_terms, raw_degree, 0, -1))
            continue
        selected.append((left, right, raw_terms, raw_degree,
                         len(determinant_e),
                         max(sum(exponent) for exponent in determinant_e)))
        command += (f'poly p={CHART.singular(determinant_e)};'
                    f'list f=factorize(p);print("PAIR {left} {right}");'
                    'print(size(p));print(deg(p));'
                    'for(int k=1;k<=size(f[1]);k++)'
                    '{print("F");print(f[2][k]);print(size(f[1][k]));'
                    'print(deg(f[1][k]));if(size(f[1][k])<=12)'
                    '{print(string(f[1][k]));}}')
    command += "quit;"
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               check=False, timeout=120)
    return selected, completed.stdout, completed.stderr


def divide_common_monomial(poly):
    """Remove scalar/content-free common monomial (all remaining variables live)."""
    if not poly:
        return poly
    exponents = list(poly)
    common = tuple(min(exponent[index] for exponent in exponents)
                   for index in range(CHART.n))
    first_coefficient = next(iter(poly.values()))
    return {tuple(exponent[index] - common[index]
                  for index in range(CHART.n)): coefficient / first_coefficient
            for exponent, coefficient in poly.items()}


def exact_divide(dividend, divisor):
    """Exact multivariate division in graded-lex order."""
    quotient, remainder = {}, dict(dividend)
    divisor_lead = max(divisor, key=lambda exponent: (sum(exponent), exponent))
    divisor_coefficient = divisor[divisor_lead]
    while remainder:
        lead = max(remainder, key=lambda exponent: (sum(exponent), exponent))
        if not all(lead[index] >= divisor_lead[index]
                   for index in range(CHART.n)):
            raise RuntimeError(("nonzero remainder", CHART.singular(remainder)))
        exponent = tuple(lead[index] - divisor_lead[index]
                         for index in range(CHART.n))
        coefficient = remainder[lead] / divisor_coefficient
        term = {exponent: coefficient}
        quotient = CHART.add(quotient, term)
        remainder = CHART.add(
            remainder, CHART.scale(CHART.multiply(term, divisor), -1))
    return quotient


def divide_live_factor_power(poly, factor):
    """Cancel every exact power of a previously localized polynomial."""
    exponent = 0
    while poly:
        try:
            quotient = exact_divide(poly, factor)
        except RuntimeError:
            break
        poly = quotient
        exponent += 1
    return poly, exponent


def cramer_branch_system(left=7, right=12):
    """Build the E=0 Cramer open chart and determinant-zero boundary.

    Returns polynomial systems only.  The open chart is equivalent after
    localizing the reduced determinant and the transported live factors; the
    closed chart keeps a4,a5 and adds the reduced determinant equation.
    """
    rows, _, live_replacements, _ = solve_a0_a3_a2_a1()
    e_replacements = {index: CHART.variable(index)
                      for index in range(CHART.n)}
    live_d3 = CHART.add(
        CHART.multiply(CHART.variable(7),
                       CHART.variable(CHART.d_index[4])),
        CHART.multiply(CHART.variable(6),
                       CHART.variable(CHART.d_index[5])))
    e_replacements[CHART.d_index[3]] = CHART.scale(live_d3, -1)
    # Rescale the two remaining unknowns by Laurent units:
    # x=d4*a4 and y=d4*d5*a5.  This exposes the common d4*d3 factor
    # in all three Cramer numerators and cuts it before elimination.
    e_replacements[4] = CHART.multiply(
        CHART.variable(4), inverse_monomial(CHART.d_index[4]))
    e_replacements[5] = CHART.multiply(
        CHART.variable(5),
        inverse_monomial(CHART.d_index[4], CHART.d_index[5]))
    e_rows = [(label, divide_common_monomial(CHART.clear_denominators(
        substitute_poly(poly, e_replacements))))
              for label, poly in rows if label != 100]
    linear = {label: split_linear(poly) for label, poly in e_rows}
    lc, la, lb = linear[left]
    rc, ra, rb = linear[right]
    determinant_raw = CHART.add(CHART.multiply(la, rb),
                                CHART.scale(CHART.multiply(lb, ra), -1))
    numerator_a4_raw = CHART.add(CHART.multiply(lb, rc),
                                 CHART.scale(CHART.multiply(lc, rb), -1))
    numerator_a5_raw = CHART.add(CHART.multiply(lc, ra),
                                 CHART.scale(CHART.multiply(la, rc), -1))
    common_cramer = CHART.multiply(
        CHART.variable(CHART.d_index[4]), live_d3)
    determinant = exact_divide(determinant_raw, common_cramer)
    numerator_a4 = exact_divide(numerator_a4_raw, common_cramer)
    numerator_a5 = exact_divide(numerator_a5_raw, common_cramer)
    delta = determinant
    open_rows = []
    for label, (constant, coefficient_a4, coefficient_a5) in linear.items():
        if label in (left, right):
            continue
        value = CHART.add(
            CHART.multiply(constant, determinant),
            CHART.multiply(coefficient_a4, numerator_a4),
            CHART.multiply(coefficient_a5, numerator_a5))
        if value:
            value = divide_common_monomial(value)
            value, _ = divide_live_factor_power(value, live_d3)
            open_rows.append((label, value))
    # Transport A2's live numerator through the same Cramer substitution.
    live_a2_e = CHART.clear_denominators(substitute_poly(
        live_replacements[2], e_replacements))
    a2_constant, a2_a4, a2_a5 = split_linear(live_a2_e)
    live_a2_numerator = divide_common_monomial(CHART.add(
        CHART.multiply(a2_constant, determinant),
        CHART.multiply(a2_a4, numerator_a4),
        CHART.multiply(a2_a5, numerator_a5)))
    live_a2_numerator, _ = divide_live_factor_power(
        live_a2_numerator, live_d3)
    live_a3 = divide_common_monomial(CHART.clear_denominators(substitute_poly(
        live_replacements[3], e_replacements)))
    live_b = CHART.multiply(*(CHART.variable(index) for index in (6, 7, 9)))
    live_d = CHART.multiply(CHART.variable(CHART.d_index[4]),
                            CHART.variable(CHART.d_index[5]), live_d3)
    open_live_factors = [CHART.multiply(live_b, live_d), live_a3, delta,
                         numerator_a4, numerator_a5, live_a2_numerator]
    closed_rows = e_rows + [(101, delta)]
    closed_live_factors = [CHART.multiply(live_b, live_d), live_a3,
                           live_a2_e, CHART.variable(4), CHART.variable(5)]
    return {
        "open_rows": open_rows,
        "open_live_factors": open_live_factors,
        "closed_rows": closed_rows,
        "closed_live_factors": closed_live_factors,
        "determinant": determinant,
        "delta": delta,
        "common_cramer": common_cramer,
        "numerator_a4": numerator_a4,
        "numerator_a5": numerator_a5,
        "live_a2_numerator": live_a2_numerator,
    }


def cramer_branch_probe(characteristic, timeout, left=7, right=12,
                        branch="open", algorithm="slimgb"):
    data = cramer_branch_system(left, right)
    if branch == "open":
        factors = data["open_live_factors"]
        names = [f"z{index}" for index in range(len(factors))]
        names += ["b0", "b1", "b3", "d4", "d5"]
        generators = [CHART.singular(poly)
                      for _, poly in data["open_rows"]]
        generators += [f'z{index}*({CHART.singular(factor)})-1'
                       for index, factor in enumerate(factors)]
    else:
        factors = data["closed_live_factors"]
        names = [f"z{index}" for index in range(len(factors))]
        names += ["a4", "a5", "b0", "b1", "b3", "d4", "d5"]
        generators = [CHART.singular(poly)
                      for _, poly in data["closed_rows"]]
        generators += [f'z{index}*({CHART.singular(factor)})-1'
                       for index, factor in enumerate(factors)]
    command = (f"ring R={characteristic},({','.join(names)}),dp;"
               f"ideal I={','.join(generators)};"
               f"ideal G={algorithm}(I);"
               'print("BEGIN");print(size(G));print(dim(G));'
               'print(string(reduce(1,G)));print("END");quit;')
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=timeout)
        return time.monotonic() - started, completed.stdout, completed.stderr, data
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return time.monotonic() - started, stdout + "\nTIMEOUT", stderr, data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--characteristic", type=int, default=7)
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--split", action="store_true")
    parser.add_argument("--solve-linear", action="store_true")
    parser.add_argument("--solve-a1", action="store_true")
    parser.add_argument("--use-d-relation", action="store_true")
    parser.add_argument("--solve-linear-use-d", action="store_true")
    parser.add_argument("--solve-b0-chain", action="store_true")
    parser.add_argument("--solve-a2-chain", action="store_true")
    parser.add_argument("--solve-a1-after-a2", action="store_true")
    parser.add_argument("--use-e-after-chain", action="store_true")
    parser.add_argument("--include-c", action="store_true")
    parser.add_argument("--c-edges", default="2,3,4,5")
    parser.add_argument("--c2-nilpotence", action="store_true")
    parser.add_argument("--homogeneous", action="store_true")
    parser.add_argument("--modular-homogeneous", action="store_true")
    parser.add_argument("--homogeneous-chain", action="store_true")
    parser.add_argument("--modular-homogeneous-chain", action="store_true")
    parser.add_argument("--sequential-saturation", action="store_true")
    parser.add_argument("--reverse-saturation", action="store_true")
    parser.add_argument("--reduced-lift", action="store_true")
    parser.add_argument("--cramer-census", action="store_true")
    parser.add_argument("--cramer-e-factors", action="store_true")
    parser.add_argument("--cramer-branch", choices=("open", "closed"))
    parser.add_argument("--cramer-left", type=int, default=7)
    parser.add_argument("--cramer-right", type=int, default=12)
    parser.add_argument("--algorithm", choices=("slimgb", "std", "modStd", "modGB"), default="slimgb")
    parser.add_argument("--localizers-first", action="store_true")
    parser.add_argument("--term-order", choices=("dp", "Dp", "lp"), default="dp")
    parser.add_argument("--localizer-scheme", choices=("two", "three", "individual"), default="two")
    parser.add_argument("--protocol", action="store_true")
    parser.add_argument("--no-h", action="store_true")
    parser.add_argument("--print-solved", action="store_true")
    parser.add_argument("--print-solved-d", action="store_true")
    parser.add_argument("--print-b0-chain", action="store_true")
    parser.add_argument("--factor-solved-d", action="store_true")
    parser.add_argument("--factor-a2-chain", action="store_true")
    parser.add_argument("--print-full-chain", action="store_true")
    parser.add_argument("--order", default="natural",
                        choices=("natural", "d-first", "b-first", "a-reverse",
                                 "linear-first"))
    args = parser.parse_args()
    rows, hafnian = gauged_rows()
    if args.c2_nilpotence:
        elapsed, stdout, stderr = c2_nilpotence_probe(
            args.characteristic, args.timeout)
        print("c2-nilpotence:", args.characteristic, round(elapsed, 3))
        print(stdout[-10000:])
        print(stderr[-1000:])
        return
    if args.homogeneous or args.modular_homogeneous:
        elapsed, stdout, stderr = homogeneous_probe(
            args.characteristic, args.timeout, args.modular_homogeneous)
        print("homogeneous:", args.characteristic, args.modular_homogeneous,
              round(elapsed, 3))
        print(stdout[-20000:])
        print(stderr[-1000:])
        return
    if args.homogeneous_chain or args.modular_homogeneous_chain:
        elapsed, stdout, stderr = homogeneous_chain_probe(
            args.characteristic, args.timeout,
            args.modular_homogeneous_chain)
        print("homogeneous-chain:", args.characteristic,
              args.modular_homogeneous_chain, round(elapsed, 3))
        print(stdout[-30000:])
        print(stderr[-1000:])
        return
    if args.sequential_saturation:
        elapsed, stdout, stderr = sequential_saturation_probe(
            args.characteristic, args.timeout, args.reverse_saturation)
        print("sequential-saturation:", args.characteristic,
              args.reverse_saturation, round(elapsed, 3))
        print(stdout[-30000:])
        print(stderr[-1000:])
        return
    if args.reduced_lift:
        elapsed, stdout, stderr = reduced_lift_probe(
            args.characteristic, args.timeout)
        print("reduced-lift:", args.characteristic, round(elapsed, 3))
        print(stdout[-30000:])
        print(stderr[-1000:])
        return
    if args.cramer_census:
        linear, census = cramer_pair_census()
        names = ["b0", "b1", "b3", "d3", "d4", "d5"]
        command = f"ring R=0,({','.join(names)}),dp;"
        for terms, degree, left, right, determinant in census[:20]:
            print("PAIR", left, right, "terms", terms, "degree", degree)
            print(CHART.singular(determinant))
            command += (f'print("PAIR {left} {right}");'
                        f'factorize({CHART.singular(determinant)});')
        command += "quit;"
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=30)
        print(completed.stdout)
        print(completed.stderr)
        return
    if args.cramer_e_factors:
        selected, stdout, stderr = cramer_e_factor_summary()
        print("SELECTED", selected)
        print(stdout)
        print(stderr)
        return
    if args.cramer_branch:
        elapsed, stdout, stderr, data = cramer_branch_probe(
            args.characteristic, args.timeout, args.cramer_left,
            args.cramer_right, args.cramer_branch, args.algorithm)
        print("CRAMER", args.cramer_branch, args.cramer_left,
              args.cramer_right, args.characteristic, round(elapsed, 3))
        print("delta", len(data["delta"]), CHART.singular(data["delta"]))
        print("open row terms", [(label, len(poly))
                                 for label, poly in data["open_rows"]])
        print("live factor terms", [len(poly)
                                    for poly in data["open_live_factors"]])
        print(stdout[-30000:])
        print(stderr[-1000:])
        return
    if args.print_solved:
        solved, solved_h, _ = solve_a0_a3()
        print("solved H terms:", len(solved_h))
        for label, poly in solved:
            print("SOLVED", label, CHART.singular(poly))
        return
    if args.print_solved_d:
        solved, solved_h, _ = solve_a0_a3_use_d_relation()
        print("solved-d H terms:", len(solved_h))
        for label, poly in solved:
            print("SOLVED-D", label, len(poly), CHART.singular(poly))
        return
    if args.print_b0_chain:
        solved, solved_h, _, _ = solve_b0_a3_a1()
        print("b0-chain H terms:", len(solved_h))
        for label, poly in solved:
            print("B0-CHAIN", label, len(poly), CHART.singular(poly))
        return
    if args.factor_solved_d:
        solved, _, _ = solve_a0_a3_use_d_relation()
        names = ["a1", "a2", "a4", "a5", "b0", "b1", "b3", "d4", "d5"]
        command = f"ring R=0,({','.join(names)}),dp;"
        for label, poly in solved:
            command += f'print("ROW {label}");factorize({CHART.singular(poly)});'
        command += "quit;"
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=30)
        print(completed.stdout)
        print(completed.stderr)
        return
    if args.factor_a2_chain:
        solved, _, _, _ = solve_a0_a3_a2()
        names = ["a1", "a4", "a5", "b0", "b1", "b3", "d3", "d4", "d5"]
        command = f"ring R=0,({','.join(names)}),dp;"
        for label, poly in solved:
            print("A2-CHAIN", label, len(poly))
            if len(poly) <= 60:
                command += f'print("ROW {label}");factorize({CHART.singular(poly)});'
        command += "quit;"
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   check=False, timeout=30)
        print(completed.stdout)
        print(completed.stderr)
        return
    if args.print_full_chain:
        solved, solved_h, _, _ = solve_a0_a3_a2_a1()
        print("full-chain H terms:", len(solved_h))
        for label, poly in solved:
            print("FULL-CHAIN", label, len(poly),
                  CHART.singular(poly) if len(poly) <= 10 else "")
        return
    active = [index for index in range(CHART.n)
              if index not in (8, 10, 11, CHART.d_index[2])]
    names = [CHART.names[index] for index in active]
    print("active:", ",".join(names))
    print("H terms:", len(hafnian))
    for label, poly in rows:
        print(label, CHART.singular(poly))

    if args.probe:
        orders = {
            "natural": names,
            "d-first": ["d3", "d4", "d5", "b0", "b1", "b3"]
                       + [f"a{i}" for i in range(6)],
            "b-first": ["b0", "b1", "b3", "d3", "d4", "d5"]
                       + [f"a{i}" for i in range(6)],
            "a-reverse": [f"a{i}" for i in reversed(range(6))]
                         + ["b3", "b1", "b0", "d5", "d4", "d3"],
            "linear-first": ["a0", "a3", "a1", "a2", "a4", "a5",
                             "d3", "b0", "b1", "b3", "d4", "d5"],
        }
        if args.solve_linear or args.solve_a1 or args.solve_linear_use_d:
            for key in orders:
                orders[key] = [name for name in orders[key]
                               if name not in ("a0", "a3")]
        if args.solve_a1:
            for key in orders:
                orders[key] = [name for name in orders[key] if name != "a1"]
        if args.use_d_relation or args.solve_linear_use_d:
            for key in orders:
                orders[key] = [name for name in orders[key] if name != "d3"]
        if args.solve_b0_chain:
            for key in orders:
                orders[key] = [name for name in orders[key]
                               if name not in ("b0", "a3", "a1")]
        if args.solve_a2_chain or args.solve_a1_after_a2:
            for key in orders:
                orders[key] = [name for name in orders[key]
                               if name not in ("a0", "a3", "a2")]
        if args.solve_a1_after_a2:
            for key in orders:
                orders[key] = [name for name in orders[key] if name != "a1"]
        if args.use_e_after_chain:
            for key in orders:
                orders[key] = [name for name in orders[key]
                               if name not in ("a0", "a1", "a2", "a3", "d3")]
        elapsed, stdout, stderr = singular_probe(
            args.characteristic, orders[args.order], args.split, args.timeout,
            args.solve_linear, not args.no_h, args.solve_a1,
            args.use_d_relation, args.solve_linear_use_d,
            args.solve_b0_chain, args.include_c,
            tuple(int(value) for value in args.c_edges.split(",") if value),
            args.algorithm, args.localizers_first, args.term_order,
            args.solve_a2_chain, args.localizer_scheme,
            args.solve_a1_after_a2, args.protocol, args.use_e_after_chain)
        print("probe:", args.characteristic, args.order, args.split,
              round(elapsed, 3))
        print(stdout[-2000:])
        print(stderr[-1000:])
        return

    ring_names = ",".join(names)
    commands = [f"ring R=0,({ring_names}),dp;"]
    for label, poly in rows:
        commands.append(f'print("ROW {label}");factorize({CHART.singular(poly)});')
    commands.append("quit;")
    completed = subprocess.run(
        ["Singular", "-q", "-c", "".join(commands)],
        text=True, capture_output=True, check=False, timeout=20)
    print(completed.stdout)
    print(completed.stderr)


if __name__ == "__main__":
    main()
