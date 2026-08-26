#!/usr/bin/env python3
"""Audit exact chart-union equivalence and the representative tiny input."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
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
    specification = importlib.util.spec_from_file_location("rep1_pivot_generator", HERE / "generate_quotient.py")
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def matvec(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)]


def partner(A13, A35, y, z):
    return [sum(A13[j][i] * y[j] + A35[i][j] * z[j] for j in range(3)) for i in range(3)]


def exact_replay(chart, rng):
    coordinate, _, _, r, kind, s = chart
    alpha = Fraction(rng.choice((-5, -3, -2, 1, 2, 4)))
    beta = Fraction(rng.choice((-4, -3, -1, 1, 3, 5)))
    xnorm = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    xnorm[r] = 1
    qy = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    qz = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
    (qy if kind == "y" else qz)[s] = 1
    A06 = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        A06[i][r] = alpha * int(i == coordinate) - sum(A06[i][j] * xnorm[j] for j in range(3) if j != r)
    A13 = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    A35 = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    if kind == "y":
        for i in range(3):
            A13[s][i] = beta * int(i == coordinate) - sum(A13[j][i] * qy[j] for j in range(3) if j != s) - sum(A35[i][j] * qz[j] for j in range(3))
    else:
        for i in range(3):
            A35[i][s] = beta * int(i == coordinate) - sum(A13[j][i] * qy[j] for j in range(3)) - sum(A35[i][j] * qz[j] for j in range(3) if j != s)
    x = [value / alpha for value in xnorm]
    y = [value / beta for value in qy]
    z = [value / beta for value in qz]
    target = [Fraction(int(i == coordinate)) for i in range(3)]
    assert matvec(A06, x) == target
    assert partner(A13, A35, y, z) == target


def validate(result):
    assert result["schema"] == "KRENN_X5_REP1_INCIDENCE_PIVOT_QUOTIENT_AUDIT_V1"
    assert result["status"] == "PASS_EXACT_CONTRACTION_DESIGN"
    assert result["chart_union"] == {"raw": 486, "orbits": 82, "y_orbits": 41, "z_orbits": 41, "complete": True}
    assert result["contraction"] == {"variables_before": 100, "variables_after": 94, "generators_before": 6586, "generators_after": 6580, "equivalent_on_each_chart": True}
    assert result["scope"] == {"rep1_closed": False, "tiny_diagnostic_coverage": False, "D12_reads": False}


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
    metadata = json.loads((HERE / "quotient_metadata.json").read_text())
    assert metadata["status"] == "PASS_EXACT_CONTRACTION_DESIGN"
    assert metadata["counts"] == {"parent_variables": 100, "quotient_variables": 94, "variables_removed": 6, "parent_generators": 6586, "quotient_generators": 6580, "generators_removed": 6, "solved_block_entries": 6, "explicit_incidence_equations": 0}
    raw, groups = generator.orbit_ledger()
    assert len(raw) == metadata["chart_census"]["raw_charts"] == 486
    assert len(groups) == metadata["chart_census"]["s3_orbits"] == 82
    assert metadata["chart_census"]["orbits_by_partner_kind"] == {"y": 41, "z": 41}
    assert metadata["equivalence"]["chart_union_complete"] is True
    program = generator.build_program(generator.TINY)
    source = HERE / metadata["tiny_diagnostic"]["input"]
    assert hashlib.sha256(program.encode()).hexdigest() == sha256(source) == metadata["tiny_diagnostic"]["input_sha256"]
    first_line = next(line for line in program.splitlines() if line.startswith("ring r="))
    variables = first_line.split(",(", 1)[1].split("),dp;", 1)[0].split(",")
    assert len(variables) == len(set(variables)) == 94
    assert "a06_00" not in variables and "a06_10" not in variables and "a06_20" not in variables
    assert "a13_00" not in variables and "a13_01" not in variables and "a13_02" not in variables
    assert "alpha*beta*a47_00*sat-1" in program

    rng = random.Random(0xA0613)
    representatives = sorted(groups)
    for index in range(257):
        exact_replay(representatives[index % len(representatives)], rng)

    result = {
        "schema": "KRENN_X5_REP1_INCIDENCE_PIVOT_QUOTIENT_AUDIT_V1",
        "status": "PASS_EXACT_CONTRACTION_DESIGN",
        "metadata_sha256": sha256(HERE / "quotient_metadata.json"),
        "tiny_input_sha256": sha256(source),
        "chart_union": {"raw": 486, "orbits": 82, "y_orbits": 41, "z_orbits": 41, "complete": True},
        "contraction": {"variables_before": 100, "variables_after": 94, "generators_before": 6586, "generators_after": 6580, "equivalent_on_each_chart": True},
        "exact_fraction_replays": 257,
        "scope": {"rep1_closed": False, "tiny_diagnostic_coverage": False, "D12_reads": False},
    }
    validate(result)
    tests = {
        "drop_chart": hostile(result, lambda item: item["chart_union"].__setitem__("orbits", 81)),
        "equivalence_overclaim": hostile(result, lambda item: item["contraction"].__setitem__("equivalent_on_each_chart", False)),
        "closure_overclaim": hostile(result, lambda item: item["scope"].__setitem__("rep1_closed", True)),
        "diagnostic_overclaim": hostile(result, lambda item: item["scope"].__setitem__("tiny_diagnostic_coverage", True)),
        "D12_scope_mutation": hostile(result, lambda item: item["scope"].__setitem__("D12_reads", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_design_audit.json")
    print(json.dumps({"status": result["status"], "orbits": 82, "fraction_replays": 257}, sort_keys=True))


if __name__ == "__main__":
    main()
