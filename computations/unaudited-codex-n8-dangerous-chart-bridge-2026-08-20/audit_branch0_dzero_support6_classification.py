#!/usr/bin/env python3
"""Exact classification of the branch-0, d=0 chart as support-six points."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
DZERO_PATH = SOURCE / "analyze_weight0_dzero_lowq_chart.py"
SUPPORT6_PATH = HERE / "audit_support6_component_pairwise_obstruction.py"
OUT = HERE / "results_branch0_dzero_support6_classification.json"
BRANCH_MASK = 0
GAUGE = {2: 1, 4: 1, 5: 1}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


DZERO = load("n8_branch0_dzero", DZERO_PATH)
S6 = load("n8_branch0_s6", SUPPORT6_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def singular_census(base, cleared_h):
    variables = ",".join([f"a{i}" for i in range(6)]
                         + [f"b{i}" for i in range(6)] + ["u"])
    ideal = ",".join(DZERO.singular(poly) for poly in base)
    gauge = ",".join(f"b{index}-{value}"
                     for index, value in sorted(GAUGE.items()))
    reductions = ";".join(
        f'poly ra{index}=reduce(a{index},G);'
        f'if(ra{index}==0){{print("A{index}_ZERO");}}'
        f'else{{print("A{index}_NONZERO");}}'
        for index in range(6)
    )
    command = (
        f"ring R=0,({variables}),dp; ideal I={ideal},{gauge},"
        f"u*({DZERO.singular(cleared_h)})-1; ideal G=std(I); "
        'print("BEGIN"); print(dim(G)); print(vdim(G)); '
        f"{reductions}; print(\"END\"); quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular census failed: " + completed.stderr[-1000:])
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = lines[begin + 1:end]
    require(body[:2] == ["0", "6"],
            f"dimension/vector-dimension changed: {body[:2]}")
    require(body[2:] == [f"A{index}_ZERO" for index in range(6)],
            "an a-coordinate survived the exact quotient")
    return {"dimension": 0, "vector_space_dimension": 6,
            "all_a_reduce_to_zero": True}


def main():
    equations, raw_h = DZERO.SCREEN.PROBE.equations(
        DZERO.SCREEN.branch_bits(BRANCH_MASK))
    base = tuple(DZERO.clear_denominators(DZERO.substitute(poly))
                 for poly in equations if DZERO.substitute(poly))
    cleared_h = DZERO.clear_denominators(DZERO.substitute(raw_h))
    require(len(base) == 10, "branch-0 surviving row count changed")
    quotient = singular_census(base, cleared_h)

    roots = (S6.Z, -S6.Z - 2)
    allowed_root_choices = ((0, 0, 0), (0, 0, 1), (0, 1, 1),
                            (1, 0, 0), (1, 1, 0), (1, 1, 1))
    x_support = frozenset(4 * edge + position
                          for edge in range(6) for position in (1, 2))
    q_support = frozenset((3, 5, 6, 9, 10, 12))
    canonical_record = (x_support, frozenset((9, 10, 13, 14)), q_support)
    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))
    canonical_orbit = frozenset(
        (S6.act_support(canonical_record[0], S6.raw_action_index, *action),
         S6.act_support(canonical_record[1], S6.raw_action_index, *action),
         S6.act_support(canonical_record[2], S6.q_action_index, *action))
        for action in actions
    )
    points = []
    records = set()
    for choices in allowed_root_choices:
        b = (roots[choices[0]], roots[choices[1]], S6.ONE,
             roots[choices[2]], S6.ONE, S6.ONE)
        c = (roots[1 - choices[0]], roots[1 - choices[1]], -S6.ONE,
             roots[1 - choices[2]], -S6.ONE, -S6.ONE)
        blocks = tuple((S6.ZERO, b[edge], c[edge], S6.ZERO)
                       for edge in range(6))
        require(all(S6.ONE + S6.permanent(block) == S6.ZERO
                    for block in blocks), "a permanent row failed")
        triangle_rows = tuple(
            S6.ONE
            + S6.permanent(blocks[S6.EDGE_INDEX[(i, j)]])
            + S6.permanent(blocks[S6.EDGE_INDEX[(i, k)]])
            + S6.permanent(blocks[S6.EDGE_INDEX[(j, k)]])
            + S6.triangle(blocks, i, j, k)
            for i, j, k in __import__("itertools").combinations(range(4), 3)
        )
        require(not any(triangle_rows), "a triangle row failed")
        h_value = S6.hafnian_on(blocks, range(8))
        require(h_value == S6.as_k(4), "pure H ceased to be 4")
        cofactors = tuple(S6.cofactor(blocks, index)
                          for index in range(24))
        selected = tuple(4 * edge + position for edge in range(6)
                         for position in (0, 3))
        require(not any(cofactors[index] for index in selected),
                "a branch-0 selected cofactor is nonzero")
        qs = tuple(S6.q_value(blocks, value) for value in range(16))
        actual_q = frozenset(index for index, value in enumerate(qs) if value)
        c_support = frozenset(index for index, value in enumerate(cofactors)
                              if value)
        record = (x_support, c_support, actual_q)
        require(actual_q == q_support and record in canonical_orbit,
                "a classified point left the support-six joint orbit")
        records.add(record)
        points.append({
            "root_choices_b0_b1_b3": list(choices),
            "H": 4,
            "Q_support": sorted(actual_q),
            "cofactor_support": sorted(c_support),
        })
    require(len(points) == quotient["vector_space_dimension"],
            "listed distinct-point count does not exhaust quotient length")

    result = {
        "status": "UNAUDITED exact branch-0 d=0 classification",
        "localized_chart": "M_e=[[a_e,b_e],[-1/b_e,0]], all b_e nonzero",
        "branch_mask": BRANCH_MASK,
        "gauge": "b2=b4=b5=1",
        "number_field_for_points": "Q(z), z^2+2z-1=0",
        "surviving_literal_row_count": len(base),
        "exact_quotient": quotient,
        "classified_points": points,
        "distinct_point_count": len(points),
        "joint_support_record_count": len(records),
        "support6_orbit_size": len(canonical_orbit),
        "completeness_argument": (
            "The saturated gauge quotient has vector-space dimension six. "
            "The six displayed points are distinct and all satisfy it, so "
            "the quotient is reduced and consists exactly of these points."
        ),
        "conclusion": (
            "Every point on this chart is a B4 transform of the exact "
            "support-six component already excluded by the global fixed-left "
            "partner Nullstellensatz."
        ),
        "scope": (
            "This classifies branch mask 0 on the uniform d=0 chart, modulo "
            "the stated nonzero-b gauge."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 d=0 support-six classification: PASS")
    print("quotient dimension / length / points:", quotient["dimension"],
          quotient["vector_space_dimension"], len(points))
    print("joint records / support-six orbit:", len(records),
          len(canonical_orbit))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
