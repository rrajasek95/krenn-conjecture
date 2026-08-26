#!/usr/bin/env python3
"""Independent exact audit of the rep1 guard-minor quotient design."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import random
from fractions import Fraction
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load_generator():
    specification = importlib.util.spec_from_file_location("rep1_minor_generator", HERE / "generate_minor_quotient.py")
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def matvec(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)]


def partner(A13, A35, y, z):
    return [sum(A13[j][i] * y[j] + A35[i][j] * z[j] for j in range(3)) for i in range(3)]


def replay(record, rng):
    coordinate, p, q, r, kind, s, a, b = record
    c = next(item for item in range(3) if item not in (a, b))
    while True:
        w = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        w[r] = 1
        v = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        if v[q] == 0:
            v[q] = 1
        d = w[a] * v[b] - w[b] * v[a]
        if d:
            break
    abar = Fraction(rng.choice((-5, -3, -1, 1, 2, 4)))
    beta = Fraction(rng.choice((-4, -2, -1, 1, 3, 5)))
    t = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    A06 = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        reduced = abar * int(i == coordinate) - t[i] * w[c]
        A06[i][a] = reduced * v[b] + w[b] * t[i] * v[c]
        A06[i][b] = -(w[a] * t[i] * v[c] + reduced * v[a])
        A06[i][c] = d * t[i]
    alpha = d * abar
    x = [value / alpha for value in w]
    target = [Fraction(int(i == coordinate)) for i in range(3)]
    assert matvec(A06, v) == [Fraction(0)] * 3
    assert matvec(A06, x) == target

    qy = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    qz = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    (qy if kind == "y" else qz)[s] = 1
    A13 = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    A35 = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    if kind == "y":
        for i in range(3):
            A13[s][i] = beta * int(i == coordinate) - sum(A13[j][i] * qy[j] for j in range(3) if j != s) - sum(A35[i][j] * qz[j] for j in range(3))
    else:
        for i in range(3):
            A35[i][s] = beta * int(i == coordinate) - sum(A13[j][i] * qy[j] for j in range(3)) - sum(A35[i][j] * qz[j] for j in range(3) if j != s)
    y = [value / beta for value in qy]
    z = [value / beta for value in qz]
    assert partner(A13, A35, y, z) == target
    assert v[q] != 0 and d != 0 and abar != 0 and beta != 0


def validate(result):
    assert result["schema"] == "KRENN_X5_REP1_GUARD_MINOR_QUOTIENT_AUDIT_V1"
    assert result["status"] == "PASS_STRICTLY_SMALLER_EXACT_QUOTIENT_DESIGN"
    assert result["chart_union"] == {"raw": 972, "orbits": 162, "y_orbits": 81, "z_orbits": 81, "all_equal_y_orbits": 1, "complete": True}
    assert result["counts"] == {"variables": 91, "generators": 6577, "A06_entries_solved": 9, "partner_entries_solved": 3, "tautological_guard_equations_removed": 3}
    assert result["scope"] == {"launches": 0, "rep1_closed": False, "D12_reads": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    generator = load_generator()
    metadata = json.loads((HERE / "minor_quotient_metadata.json").read_text())
    assert metadata["status"] == "PASS_STRICTLY_SMALLER_EXACT_QUOTIENT_DESIGN"
    assert metadata["counts"]["minor_quotient_variables"] == 91
    assert metadata["counts"]["minor_quotient_generators"] == 6577
    raw, groups = generator.orbit_ledger()
    assert len(raw) == 972 and len(groups) == 162
    assert metadata["chart_census"]["complete"] is True
    assert metadata["chart_census"]["orbits_by_partner_kind"] == {"y": 81, "z": 81}
    source = HERE / metadata["materialized_input"]["path"]
    program = generator.build_program(generator.load_base(), generator.TINY)
    assert hashlib.sha256(program.encode()).hexdigest() == sha256(source) == metadata["materialized_input"]["sha256"]
    ring_line = next(line for line in program.splitlines() if line.startswith("ring r="))
    variables = ring_line.split(",(", 1)[1].split("),dp;", 1)[0].split(",")
    assert len(variables) == len(set(variables)) == 91
    assert not any(name.startswith("a06_") for name in variables)
    assert all(f"t{i}" in variables for i in range(3))
    body = program.split("ideal I=", 1)[1].split(";\nprint(", 1)[0]
    equations = body.split(",\n")
    assert len(equations) == len(set(equations)) == 6577 and "0" not in equations
    assert "abar*beta*a47_00*(a47_01-(xn1*a47_00))*sat-1" in program

    rng = random.Random(0xA060047)
    representatives = sorted(groups)
    for index in range(257):
        replay(representatives[index % len(representatives)], rng)

    result = {
        "schema": "KRENN_X5_REP1_GUARD_MINOR_QUOTIENT_AUDIT_V1",
        "status": "PASS_STRICTLY_SMALLER_EXACT_QUOTIENT_DESIGN",
        "metadata_sha256": sha256(HERE / "minor_quotient_metadata.json"),
        "input_sha256": sha256(source),
        "chart_union": {"raw": 972, "orbits": 162, "y_orbits": 81, "z_orbits": 81, "all_equal_y_orbits": 1, "complete": True},
        "counts": {"variables": 91, "generators": 6577, "A06_entries_solved": 9, "partner_entries_solved": 3, "tautological_guard_equations_removed": 3},
        "exact_fraction_replays": 257,
        "alternate_carrier_audit": metadata["alternate_carrier_audit"],
        "scope": {"launches": 0, "rep1_closed": False, "D12_reads": False},
    }
    validate(result)
    tests = {
        "drop_minor_chart": hostile(result, lambda item: item["chart_union"].__setitem__("complete", False)),
        "variable_overclaim": hostile(result, lambda item: item["counts"].__setitem__("variables", 90)),
        "launch_injection": hostile(result, lambda item: item["scope"].__setitem__("launches", 1)),
        "closure_overclaim": hostile(result, lambda item: item["scope"].__setitem__("rep1_closed", True)),
        "D12_scope_mutation": hostile(result, lambda item: item["scope"].__setitem__("D12_reads", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_design_audit.json")
    print(json.dumps({"status": result["status"], "replays": 257, "launches": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
