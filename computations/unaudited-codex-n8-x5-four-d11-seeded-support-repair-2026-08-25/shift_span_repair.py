#!/usr/bin/env python3
"""Search the exact 362-dimensional variable-shift span of a D10 dual."""
import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import time

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

import support_restricted_repair as support

T = 361
DEGREE = 11

def load_integer(path):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header == ["KRENN_X5_BLOCKER_D10_PRIMITIVE_INTEGER_DUAL_V1", str(len(lines) - 1), "1"]
    answer = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(value)
        assert kind == "ROW" and len(row) == 10 and row == tuple(sorted(row)) and row not in answer
        assert value and abs(value) <= 2
        answer[row] = value
    assert answer[(T,) * 10] == 1
    return answer

def pairing(generators, column, dual, prime):
    return sum(coefficient * dual.get(row, 0) for row, coefficient in support.materialize(generators, column)) % prime

def solve_coefficients(equations, prime):
    equations = [(dict(row), rhs) for row, rhs in equations]
    frequency = defaultdict(int)
    for row, _rhs in equations:
        for variable in row:
            frequency[variable] += 1
    order = sorted(range(T + 1), key=lambda variable: (frequency.get(variable, 0), variable))
    rank = {variable: index for index, variable in enumerate(order)}
    basis = {}
    for equation, rhs in equations:
        while equation:
            pivot = min(equation, key=rank.__getitem__)
            value = equation[pivot]
            if pivot in basis:
                record, record_rhs = basis[pivot]
                for variable, coefficient in record.items():
                    updated = (equation.get(variable, 0) - value * coefficient) % prime
                    if updated:
                        equation[variable] = updated
                    else:
                        equation.pop(variable, None)
                rhs = (rhs - value * record_rhs) % prime
                continue
            inverse = pow(value, prime - 2, prime)
            equation = {variable: coefficient * inverse % prime for variable, coefficient in equation.items()}
            basis[pivot] = (equation, rhs * inverse % prime)
            break
        else:
            if rhs:
                return None, len(basis)
    candidate = {}
    for pivot in sorted(basis, key=rank.__getitem__, reverse=True):
        record, rhs = basis[pivot]
        value = rhs
        for variable, coefficient in record.items():
            if variable != pivot:
                value = (value - coefficient * candidate.get(variable, 0)) % prime
        if value:
            candidate[pivot] = value
    return candidate, len(basis)

def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--d10-dual", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selected", type=Path, required=True)
    parser.add_argument("--dual", type=Path, required=True)
    parser.add_argument("--prime", type=int, choices=(1073741827, 1000000007), required=True)
    parser.add_argument("--column-cap", type=int, required=True)
    parser.add_argument("--wall-seconds", type=int, required=True)
    args = parser.parse_args()
    assert args.branch in {"direct", "triangle_endpoint_colour", "third_colour", "cap_endpoint_colour"}
    assert args.column_cap == 500000 and 0 < args.wall_seconds <= 175
    for path in (args.output, args.selected, args.dual):
        assert not path.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    generators = support.load_provider(args.input, args.prime)
    d10 = load_integer(args.d10_dual)
    shifts = []
    column_equations = defaultdict(dict)
    union_support = set()
    incident_sum = 0
    for variable in range(T + 1):
        shifted = {tuple(sorted(row + (variable,))): value % args.prime for row, value in d10.items()}
        shifts.append(shifted)
        union_support.update(shifted)
        columns = support.incident_columns(generators, shifted)
        incident_sum += len(columns)
        for column in columns:
            value = pairing(generators, column, shifted, args.prime)
            if value:
                column_equations[column][variable] = value
        if variable % 16 == 0 and time.monotonic() - started >= args.wall_seconds:
            raise RuntimeError("native wall cap during shift construction")
    assert len(column_equations) <= args.column_cap
    equations = [(row, 0) for _column, row in sorted(column_equations.items())]
    equations.append(({T: 1}, 1))
    coefficients, rank = solve_coefficients(equations, args.prime)
    if coefficients is None:
        result = {"schema": "KRENN_X5_D11_SHIFT_SPAN_RESULT_V1", "status": "INCOMPLETE_SHIFT_SPAN_INCONSISTENT",
                  "branch": args.branch, "prime": args.prime, "degree": DEGREE,
                  "candidate_shifts": T + 1, "union_support": len(union_support),
                  "incident_column_sum": incident_sum, "nonzero_equation_columns": len(column_equations),
                  "coefficient_rank": rank, "elapsed_seconds": time.monotonic() - started,
                  "degree_twelve_launched": False}
        atomic_json(args.output, result)
        raise SystemExit(3)
    assert coefficients.get(T) == 1
    candidate = defaultdict(int)
    for variable, scalar in coefficients.items():
        for row, value in shifts[variable].items():
            candidate[row] = (candidate[row] + scalar * value) % args.prime
    candidate = {row: value for row, value in candidate.items() if value}
    global_columns = support.incident_columns(generators, candidate)
    assert len(global_columns) <= args.column_cap
    failures = [(column, pairing(generators, column, candidate, args.prime)) for column in global_columns]
    failures = [(column, value) for column, value in failures if value]
    assert not failures and candidate[(T,) * DEGREE] == 1
    selected_lines = ["KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1"]
    selected_lines.extend(f"COL\t{g}\t{generators[g][0]}\t{','.join(map(str, m))}" for g, m in global_columns)
    args.selected.write_text("\n".join(selected_lines) + "\n")
    dual_lines = [f"KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1\t{args.prime}\t{len(candidate)}\t1"]
    dual_lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(candidate.items()))
    args.dual.write_text("\n".join(dual_lines) + "\n")
    result = {"schema": "KRENN_X5_D11_SHIFT_SPAN_RESULT_V1", "status": "COMPLETE_MODULAR_DUAL_DIAGNOSTIC",
              "branch": args.branch, "prime": args.prime, "degree": DEGREE, "target": "t^11",
              "candidate_shifts": T + 1, "nonzero_shift_coefficients": len(coefficients),
              "shift_coefficients": {str(k): v for k, v in sorted(coefficients.items())},
              "union_support": len(union_support), "incident_column_sum": incident_sum,
              "nonzero_equation_columns": len(column_equations), "coefficient_rank": rank,
              "selected_columns": len(global_columns), "dual_support": len(candidate),
              "global_modular_dual": True, "column_cap": args.column_cap,
              "elapsed_seconds": time.monotonic() - started, "degree_twelve_launched": False}
    atomic_json(args.output, result)

if __name__ == "__main__":
    main()
