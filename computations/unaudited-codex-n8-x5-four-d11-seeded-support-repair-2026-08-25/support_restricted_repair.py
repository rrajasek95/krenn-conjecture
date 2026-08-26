#!/usr/bin/env python3
"""Exact support-restricted D11 repair from a transported D10 certificate."""
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
import os
from pathlib import Path
import time

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

T = 361
DEGREE = 11

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def signed_terms(line):
    line = line.rstrip("\n,")
    answer, begin, sign = [], 0, 1
    if line[0] in "+-":
        sign, begin = (-1 if line[0] == "-" else 1), 1
    for index in range(begin, len(line)):
        if line[index] in "+-":
            answer.append((sign, line[begin:index]))
            sign, begin = (-1 if line[index] == "-" else 1), index + 1
    answer.append((sign, line[begin:]))
    return answer

def load_provider(path, prime):
    with path.open() as stream:
        variables = stream.readline().rstrip("\n").split(",")
        assert len(variables) == 361 and int(stream.readline()) == prime
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw, maximum = [], 0
            for coefficient, token in signed_terms(line):
                ids = () if token == "1" else tuple(sorted(names[x] for x in token.split("*")))
                maximum = max(maximum, len(ids))
                raw.append((ids, coefficient))
            combined = defaultdict(int)
            for ids, coefficient in raw:
                combined[tuple(sorted(ids + (T,) * (maximum - len(ids))))] += coefficient
            generators.append((maximum, tuple((row, c) for row, c in sorted(combined.items()) if c)))
    assert len(generators) == 6571
    return tuple(generators)

def quotient(row, divisor):
    answer, cursor = [], 0
    for value in row:
        if cursor < len(divisor) and value == divisor[cursor]:
            cursor += 1
        else:
            answer.append(value)
    return tuple(answer) if cursor == len(divisor) else None

def incident_columns(generators, support):
    term_index = defaultdict(set)
    for generator, (_degree, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient:
                term_index[term].add(generator)
    columns = set()
    for row in support:
        for degree in (2, 3, 4):
            for positions in itertools.combinations(range(DEGREE), degree):
                divisor = tuple(row[index] for index in positions)
                multiplier = quotient(row, divisor)
                for generator in term_index.get(divisor, ()):
                    columns.add((generator, multiplier))
    return tuple(sorted(columns))

def materialize(generators, column):
    generator, multiplier = column
    return tuple((tuple(sorted(term + multiplier)), coefficient) for term, coefficient in generators[generator][1])

def load_selected(path, generators):
    lines = path.read_text().splitlines()
    assert lines and lines[0] == "KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1"
    answer = []
    for line in lines[1:]:
        kind, raw_generator, raw_degree, raw_multiplier = line.split("\t")
        generator, degree = int(raw_generator), int(raw_degree)
        multiplier = tuple(map(int, raw_multiplier.split(","))) if raw_multiplier else ()
        assert kind == "COL" and generators[generator][0] == degree
        assert len(multiplier) + degree == DEGREE and multiplier == tuple(sorted(multiplier))
        answer.append((generator, multiplier))
    assert answer == sorted(set(answer))
    return tuple(answer)

def load_dual(path, prime):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header == ["KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1", str(prime), str(len(lines) - 1), "1"]
    answer = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(value)
        assert kind == "ROW" and len(row) == DEGREE and row == tuple(sorted(row)) and row not in answer
        assert 0 < value < prime
        answer[row] = value
    assert answer[(T,) * DEGREE] == 1
    return answer

def inverse(value, prime):
    return pow(value, prime - 2, prime)

def solve_restricted(generators, columns, allowed, seed, prime):
    target = (T,) * DEGREE
    equations = []
    frequency = defaultdict(int)
    for column in columns:
        equation = defaultdict(int)
        for row, coefficient in materialize(generators, column):
            if row in allowed and row != target:
                equation[row] = (equation[row] + coefficient) % prime
        equation = {row: value for row, value in equation.items() if value}
        target_coefficient = sum(c for row, c in materialize(generators, column) if row == target) % prime
        rhs = (-target_coefficient) % prime
        if equation or rhs:
            equations.append((equation, rhs))
            for row in equation:
                frequency[row] += 1
    order = sorted(allowed - {target}, key=lambda row: (frequency.get(row, 0), row))
    rank = {row: index for index, row in enumerate(order)}
    basis = {}
    for raw, raw_rhs in equations:
        equation, rhs = dict(raw), raw_rhs
        while equation:
            pivot = min(equation, key=rank.__getitem__)
            value = equation[pivot]
            if pivot in basis:
                record, record_rhs = basis[pivot]
                for row, coefficient in record.items():
                    updated = (equation.get(row, 0) - value * coefficient) % prime
                    if updated:
                        equation[row] = updated
                    else:
                        equation.pop(row, None)
                rhs = (rhs - value * record_rhs) % prime
                continue
            inv = inverse(value, prime)
            equation = {row: coefficient * inv % prime for row, coefficient in equation.items()}
            rhs = rhs * inv % prime
            basis[pivot] = (equation, rhs)
            break
        else:
            if rhs:
                return None, len(equations), len(basis)
    candidate = {row: value for row, value in seed.items() if row in allowed}
    candidate[target] = 1
    for pivot in basis:
        candidate.pop(pivot, None)
    for pivot in sorted(basis, key=rank.__getitem__, reverse=True):
        record, rhs = basis[pivot]
        value = rhs
        for row, coefficient in record.items():
            if row != pivot:
                value = (value - coefficient * candidate.get(row, 0)) % prime
        if value:
            candidate[pivot] = value
    candidate = {row: value for row, value in candidate.items() if value}
    assert candidate[target] == 1
    return candidate, len(equations), len(basis)

def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--resume-selected", type=Path, required=True)
    parser.add_argument("--resume-dual", type=Path, required=True)
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
    generators = load_provider(args.input, args.prime)
    seed_columns = load_selected(args.resume_selected, generators)
    seed = load_dual(args.resume_dual, args.prime)
    allowed = set(seed)
    for column in seed_columns:
        allowed.update(row for row, coefficient in materialize(generators, column) if coefficient)
    columns = incident_columns(generators, allowed)
    assert len(columns) <= args.column_cap and time.monotonic() - started < args.wall_seconds
    candidate, equation_count, basis_rank = solve_restricted(generators, columns, allowed, seed, args.prime)
    if candidate is None:
        result = {"schema": "KRENN_X5_D11_SUPPORT_RESTRICTED_RESULT_V1", "status": "INCOMPLETE_SUPPORT_RESTRICTED_INCONSISTENT",
                  "branch": args.branch, "prime": args.prime, "degree": DEGREE, "allowed_rows": len(allowed),
                  "incident_columns": len(columns), "equations": equation_count, "basis_rank": basis_rank,
                  "elapsed_seconds": time.monotonic() - started, "degree_twelve_launched": False}
        atomic_json(args.output, result)
        raise SystemExit(3)
    global_columns = incident_columns(generators, candidate)
    failures = []
    for column in global_columns:
        pairing = sum(coefficient * candidate.get(row, 0) for row, coefficient in materialize(generators, column)) % args.prime
        if pairing:
            failures.append((column, pairing))
    assert not failures and len(global_columns) <= len(columns)
    selected_lines = ["KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1"]
    selected_lines.extend(f"COL\t{g}\t{generators[g][0]}\t{','.join(map(str, m))}" for g, m in columns)
    dual_lines = [f"KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1\t{args.prime}\t{len(candidate)}\t1"]
    dual_lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(candidate.items()))
    args.selected.write_text("\n".join(selected_lines) + "\n")
    args.dual.write_text("\n".join(dual_lines) + "\n")
    result = {"schema": "KRENN_X5_D11_SUPPORT_RESTRICTED_RESULT_V1", "status": "COMPLETE_MODULAR_DUAL_DIAGNOSTIC",
              "branch": args.branch, "prime": args.prime, "degree": DEGREE, "target": "t^11",
              "transported_seed_loaded": True, "seed_violation_columns": len(seed_columns),
              "allowed_rows": len(allowed), "selected_columns": len(columns), "equations": equation_count,
              "basis_rank": basis_rank, "dual_support": len(candidate), "global_incident_columns": len(global_columns),
              "global_modular_dual": True, "column_cap": args.column_cap,
              "elapsed_seconds": time.monotonic() - started, "degree_twelve_launched": False}
    atomic_json(args.output, result)

if __name__ == "__main__":
    main()
