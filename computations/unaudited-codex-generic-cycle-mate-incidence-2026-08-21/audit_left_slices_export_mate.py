#!/usr/bin/env python3
"""Replay generic A=B=0 slices and export arbitrary-mate incidence ideals."""

from __future__ import annotations

import ast
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys

from flint import nmod_poly
import sympy as sp


HERE = Path(__file__).resolve().parent
BUILDER_PATH = HERE / "build_left_generic_slice.py"
SOURCE_DIR = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
CORE_PATH = SOURCE_DIR / "audit_polarized_superpair_core_identity.py"
PROBE_PATH = SOURCE_DIR / "probe_cofactor_orientation_classes.py"
PRIMES = (1073741827, 1073741789)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BUILDER = load("generic_cycle_mate_slice_builder", BUILDER_PATH)
CORE = load("generic_cycle_mate_core", CORE_PATH)
PROBE = load("generic_cycle_mate_probe", PROBE_PATH)
FULL = BUILDER.SOURCE


def inverse(value, modulus, prime):
    gcd, coefficient, _ = value.xgcd(modulus)
    require(gcd.degree() == 0 and int(gcd[0]) % prime,
            "declared denominator is nonunit on slice component")
    return (coefficient*pow(int(gcd[0]), -1, prime)) % modulus


def compile_expr(expression, variables):
    poly = sp.Poly(expression, *variables, domain=sp.QQ)
    terms = []
    for monomial, coefficient in poly.terms():
        terms.append((monomial, int(coefficient.p), int(coefficient.q)))
    return terms


def evaluate_terms(terms, values, modulus, prime):
    answer = nmod_poly([], prime)
    for monomial, numerator, denominator in terms:
        coefficient = numerator*pow(denominator, -1, prime) % prime
        term = nmod_poly([coefficient], prime)
        for value, exponent in zip(values, monomial):
            if exponent:
                term = term*value.pow_mod(exponent, modulus) % modulus
        answer = (answer+term) % modulus
    return answer


def evaluate_rational(expression, variables, values, modulus, prime):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    top = evaluate_terms(compile_expr(numerator, variables), values,
                         modulus, prime)
    bottom = evaluate_terms(compile_expr(denominator, variables), values,
                            modulus, prime)
    return top*inverse(bottom, modulus, prime) % modulus


def evaluate_raw(poly, values, modulus, prime):
    answer = nmod_poly([], prime)
    for monomial, coefficient in poly.items():
        numerator = int(coefficient.numerator)
        denominator = int(coefficient.denominator)
        term = nmod_poly([numerator*pow(denominator, -1, prime) % prime],
                         prime)
        for variable in monomial:
            term = term*values[variable] % modulus
        answer = (answer+term) % modulus
    return answer


def parse_slice(prime):
    path = HERE / f"left_AB0_slice2_p{prime}.param.out"
    encoded = path.read_text().strip()
    require(encoded.endswith(":"), "slice RUR delimiter changed")
    envelope = ast.literal_eval(encoded[:-1])
    payload = envelope[1]
    require(payload[0] == prime and payload[1:4] == [7, 4,
            ["b0", "b1", "b3", "d1", "d3", "d4", "z"]],
            "slice RUR header changed")
    require(payload[4] == [0, 0, 0, 0, 0, 0, 1],
            "z ceased to be slice separating variable")
    data = payload[5][1]
    eliminant = nmod_poly(data[0][1], prime)
    require(eliminant.degree() == 4 and data[1] == [0, [1]],
            "slice eliminant/common denominator changed")
    unit, factors = eliminant.factor()
    require(int(unit) == 1 and all(exponent == 1 for _, exponent in factors),
            "slice eliminant stopped being monic squarefree")
    ordered = sorted((factor for factor, _ in factors),
                     key=lambda factor: (factor.degree(),
                                         tuple(int(factor[i])
                                               for i in range(len(factor)))))
    modulus = ordered[0]
    parameter = nmod_poly([0, 1], prime) % modulus
    numerators = [nmod_poly(record[0][1], prime) for record in data[2]]
    require(len(numerators) == 6, "slice coordinate count changed")
    values = tuple((-numerator) % modulus for numerator in numerators)
    return path, eliminant, tuple(ordered), modulus, (*values, parameter)


def raw_left_expressions():
    generic = FULL.SOURCE.SOURCE.SOURCE
    lower, _, _, p_solution, a0_solution, a5_solution = \
        FULL.derive_lower_cofactors()
    del lower
    b0, b1, b3, d1, d3, d4 = generic.PARAMETERS
    a = [a0_solution[generic.A0],
         p_solution[generic.P[0]]/d1,
         p_solution[generic.P[1]],
         p_solution[generic.P[2]]/d3,
         p_solution[generic.P[3]]/d4,
         a5_solution[generic.A5]]
    b = [b0, b1, sp.Integer(1), b3, sp.Integer(1), sp.Integer(1)]
    d = [sp.Integer(0), d1, sp.Integer(1), d3, d4, sp.Integer(0)]
    c = [sp.cancel(-(1+a[index]*d[index])/b[index])
         for index in range(6)]
    entries = tuple(value for edge in range(6)
                    for value in (a[edge], b[edge], c[edge], d[edge]))
    return generic.PARAMETERS, entries


def clean(poly):
    return {tuple(monomial): int(coefficient)
            for monomial, coefficient in poly.items() if coefficient}


def specialize(poly, zero_cells):
    return clean({monomial: coefficient
                  for monomial, coefficient in poly.items()
                  if not any(variable in zero_cells for variable in monomial)})


def encode(poly, variables):
    if not poly:
        return "0"
    pieces = []
    for monomial, coefficient in sorted(poly.items()):
        factors = [variables[index] for index in monomial]
        magnitude = abs(int(coefficient))
        if magnitude != 1 or not factors:
            factors.insert(0, str(magnitude))
        body = "*".join(factors)
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces)


def export_mate(prime, support_record):
    zero_cells = frozenset(support_record["cofactor_support"])
    remaining = tuple(index for index in range(24) if index not in zero_cells)
    variable_names = tuple(f"x{index}" for index in remaining)
    old_to_new = {old: new for new, old in enumerate(remaining)}

    def renumber(poly):
        specialized = specialize(poly, zero_cells)
        answer = Counter()
        for monomial, coefficient in specialized.items():
            answer[tuple(old_to_new[index] for index in monomial)] += coefficient
        return clean(answer)

    hafnian = CORE.pure_hafnian()
    rows = []
    rows.extend(("mate_e_"+"".join(map(str, edge)),
                 renumber(CORE.e_pair(*edge)))
                for edge in CORE.SUPER_EDGES)
    rows.extend(("mate_t_"+"".join(map(str, triple)),
                 renumber(CORE.t_triple(*triple)))
                for triple in combinations(range(4), 3))
    rows.extend((f"mate_cofactor_{index}",
                 renumber(PROBE.derivative(hafnian, index)))
                for index in support_record["entry_support"])
    rows.extend((f"mate_Q_{15-index}", renumber(CORE.q_orientation(tuple(
        ((15-index) >> (3-site)) & 1 for site in range(4)))))
                for index in support_record["Q_support"])
    # Exact dedupe after specialization, retaining provenance aliases.
    unique = []
    aliases = []
    seen = {}
    for label, poly in rows:
        key = tuple(sorted(poly.items()))
        if not poly:
            continue
        if key in seen:
            aliases[seen[key]].append(label)
        else:
            seen[key] = len(unique)
            unique.append((label, poly))
            aliases.append([label])
    h_specialized = renumber(hafnian)
    require(h_specialized, "mate Hafnian vanished structurally")
    all_rows = [poly for _, poly in unique] + [h_specialized]
    out = HERE / f"mate_incidence_p{prime}.msolve"
    out.write_text(
        ",".join(variable_names)+f"\n{prime}\n"
        + ",\n".join(encode(poly, variable_names) for poly in all_rows)+"\n")
    body = out.read_text().split("\n", 2)[2]
    require("(" not in body and "**" not in body,
            "mate msolve syntax regression")
    return {
        "input": out.name,
        "input_sha256": sha256(out.read_bytes()).hexdigest(),
        "remaining_variables": list(variable_names),
        "zero_cells_from_left_cofactors": sorted(zero_cells),
        "ordinary_generator_count_before_dedupe": len(rows),
        "ordinary_generator_count_after_dedupe": len(unique),
        "generator_aliases": aliases,
        "final_saturator": "mate_H",
        "total_input_rows": len(all_rows),
        "constant_unit_present": any(poly == {(): 1} for _, poly in unique),
    }


def main():
    parameters, entry_expressions = raw_left_expressions()
    full_variables, reduced_rows, _, _ = BUILDER.derive()
    b0, b1, b3, d1, d3, d4, z = full_variables
    slices = (
        b0+2*b1+3*b3+5*d1+7*d3+11*d4-13,
        17*b0+19*b1+23*b3+29*d1+31*d3+37*d4-41,
    )
    raw_h = CORE.pure_hafnian()
    raw_cofactors = tuple(PROBE.derivative(raw_h, index)
                          for index in range(24))
    records = []
    for prime in PRIMES:
        path, eliminant, factors, modulus, rur_values = parse_slice(prime)
        parameter_values = rur_values[:6]
        # Replay every reduced source row, the live inverse, and both slices.
        reduced_values = tuple(evaluate_rational(
            expression, full_variables, rur_values, modulus, prime)
            for expression in (*reduced_rows, *slices))
        require(all(not len(value) for value in reduced_values),
                f"reduced source/slice replay failed at p{prime}")
        entries = tuple(evaluate_rational(expression, parameters,
                                          parameter_values, modulus, prime)
                        for expression in entry_expressions)
        e_values = tuple(evaluate_raw(CORE.e_pair(*edge), entries,
                                      modulus, prime)
                         for edge in CORE.SUPER_EDGES)
        t_values = tuple(evaluate_raw(CORE.t_triple(*triple), entries,
                                      modulus, prime)
                         for triple in combinations(range(4), 3))
        cofactor_values = tuple(evaluate_raw(poly, entries, modulus, prime)
                                for poly in raw_cofactors)
        selected_cofactor_values = tuple(cofactor_values[4*edge+position]
                                         for edge in range(6)
                                         for position in (0, 3))
        q_values = tuple(evaluate_raw(CORE.q_orientation(tuple(
            (index >> (3-site)) & 1 for site in range(4))), entries,
            modulus, prime) for index in range(16))
        h_value = evaluate_raw(raw_h, entries, modulus, prime)
        require(not any(len(value) for value in
                        (*e_values, *t_values, *selected_cofactor_values)),
                f"literal full-source replay failed at p{prime}")
        entry_support = [index for index, value in enumerate(entries)
                         if len(value)]
        cofactor_support = [index for index, value in enumerate(cofactor_values)
                            if len(value)]
        q_support = [index for index, value in enumerate(q_values) if len(value)]
        record = {
            "prime": prime,
            "rur": path.name,
            "rur_sha256": sha256(path.read_bytes()).hexdigest(),
            "eliminant_coefficients": [int(eliminant[index])
                                        for index in range(len(eliminant))],
            "factor_degrees": [factor.degree() for factor in factors],
            "selected_factor_coefficients": [int(modulus[index])
                                               for index in range(len(modulus))],
            "selected_factor_degree": modulus.degree(),
            "entry_support": entry_support,
            "cofactor_support": cofactor_support,
            "Q_support": q_support,
            "left_H_nonzero_diagnostic_only": bool(len(h_value)),
            "source_replay": {
                "reduced_rows_and_two_slices": True,
                "six_permanent_rows": True,
                "four_triangle_rows": True,
                "twelve_selected_cofactor_rows": True,
            },
        }
        record["mate_export"] = export_mate(prime, record)
        records.append(record)
    require(records[0]["entry_support"] == records[1]["entry_support"]
            and records[0]["cofactor_support"] == records[1]["cofactor_support"]
            and records[0]["Q_support"] == records[1]["Q_support"],
            "two generic slices have different incidence supports")
    result = {
        "status": "UNAUDITED two-prime generic-cycle left-slice/mate export PASS",
        "component_dimension_discovery": 2,
        "slice_codimension": 2,
        "slice_degree": 4,
        "records": records,
        "fixed_certificate_search": (
            "No existing fixed-left/global generic-cycle certificate was "
            "found. The support-six and branch1 fixed-partner certificates "
            "have different frozen left presentations."),
        "scope": (
            "Full-source generic-cycle A=B=0 with the original nine chart "
            "factors live. Left H is evaluated only as a diagnostic and is "
            "not localized or used. Each mate ideal imposes mate e/t, both "
            "directional X*C consequences, complement Q, and mate H only."),
        "source_hashes": {
            "builder": sha256(BUILDER_PATH.read_bytes()).hexdigest(),
            "core": sha256(CORE_PATH.read_bytes()).hexdigest(),
            "probe": sha256(PROBE_PATH.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    (HERE / "results_generic_cycle_left_slices_mate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("generic-cycle left slices/mate export PASS")
    for record in records:
        print(record["prime"], len(record["entry_support"]),
              len(record["cofactor_support"]), len(record["Q_support"]),
              record["mate_export"]["ordinary_generator_count_after_dedupe"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
