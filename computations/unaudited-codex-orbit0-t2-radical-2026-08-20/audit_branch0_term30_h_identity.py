#!/usr/bin/env python3
"""Exact nine-row H identity on aligned joint chart (branch 0, term 30)."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ALIGNED_PATH = HERE / "audit_joint_aligned_zero_chart_census.py"
OUT = HERE / "results_branch0_term30_h_identity.json"
BRANCH = 0
TERM_MASK = 30


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ALIGNED = load("n8_b0_term30_aligned", ALIGNED_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parse_polynomial(text):
    """Parse deterministic Singular dp output in a0..a5,b0..b5."""
    answer = Counter()
    for raw_term in re.findall(r"[+-]?[^+-]+", text.replace(" ", "")):
        if not raw_term:
            continue
        sign = -1 if raw_term.startswith("-") else 1
        body = raw_term[1:] if raw_term[:1] in "+-" else raw_term
        coefficient = Fraction(sign)
        exponent = [0] * 12
        for factor in body.split("*"):
            match = re.fullmatch(r"([ab])(\d)(?:\^(\d+))?", factor)
            if match:
                index = int(match.group(2)) + (6 if match.group(1) == "b" else 0)
                exponent[index] += int(match.group(3) or 1)
            else:
                coefficient *= Fraction(factor)
        answer[tuple(exponent)] += coefficient
    return ALIGNED.clean(answer)


def serialize(poly):
    return [{"exponents_a0_a5_b0_b5": list(exponent),
             "coefficient": [coefficient.numerator, coefficient.denominator]}
            for exponent, coefficient in sorted(poly.items())]


def singular_lift(rows, hafnian):
    variables = ",".join([f"a{index}" for index in range(6)]
                         + [f"b{index}" for index in range(6)])
    ideal = ",".join(encoded for _, _, encoded in rows)
    program = (
        f"ring R=0,({variables}),dp;ideal I={ideal};"
        f"poly h={ALIGNED.singular(hafnian)};matrix L=lift(I,ideal(h));"
        "matrix MI[1][size(I)]=I;print(\"BEGIN_CHECK\");"
        "print(string((MI*L)[1,1]-h));print(\"END_CHECK\");"
        "for(int i=1;i<=nrows(L);i++){if(L[i,1]!=0){"
        "print(\"BEGIN_MULT\");print(i);print(string(L[i,1]));"
        "print(\"END_MULT\");}};"
    )
    completed = subprocess.run(["Singular", "-q"], input=program,
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular H lift failed: " + completed.stderr[-500:])
    lines = [line.strip() for line in completed.stdout.splitlines()]
    begin, end = lines.index("BEGIN_CHECK"), lines.index("END_CHECK")
    require("".join(lines[begin + 1:end]) == "0",
            "Singular H lift did not replay")
    answer = []
    cursor = 0
    labels = [label for label, _, _ in rows]
    while "BEGIN_MULT" in lines[cursor:]:
        begin = lines.index("BEGIN_MULT", cursor)
        end = lines.index("END_MULT", begin)
        index = int(lines[begin + 1]) - 1
        text = "".join(lines[begin + 2:end])
        answer.append((labels[index], parse_polynomial(text), text))
        cursor = end + 1
    return tuple(answer)


def main():
    rows = ALIGNED.derived_rows(BRANCH, TERM_MASK, deduplicate=False)
    require(len(rows) == 16 and [label for label, _, _ in rows[:4]] ==
            ["t_012", "t_013", "t_023", "t_123"],
            "branch0/term30 raw row ledger changed")
    entries = ALIGNED.aligned_entries(TERM_MASK)
    hafnian = ALIGNED.clear_denominators(ALIGNED.substitute(
        ALIGNED.PROBE.CORE.pure_hafnian(), entries))
    lift = singular_lift(rows, hafnian)
    expected_labels = ("t_012", "t_013", "t_023",
                       "cofactor_1_0", "cofactor_2_0", "cofactor_2_3",
                       "cofactor_3_3", "cofactor_4_3", "cofactor_5_0")
    require(tuple(label for label, _, _ in lift) == expected_labels,
            "nine-row H certificate support changed")
    row_map = {label: poly for label, poly, _ in rows}
    replay = ALIGNED.add(*(ALIGNED.multiply(multiplier, row_map[label])
                           for label, multiplier, _ in lift))
    require(replay == hafnian, "independent sparse H replay failed")

    last_label, last_multiplier, _ = lift[-1]
    mutation = ALIGNED.add(replay, ALIGNED.scale(
        ALIGNED.multiply(last_multiplier, row_map[last_label]), -1))
    require(mutation != hafnian, "nine-row deletion mutation did not fire")

    result = {
        "status": "UNAUDITED exact branch0/term30 aligned H identity",
        "joint_chart": {
            "cofactor_branch_mask": BRANCH,
            "permanent_term_mask": TERM_MASK,
            "permanent_term_bits_01_02_03_12_13_23":
                list(ALIGNED.branch_bits(TERM_MASK)),
            # term30 has bits (0,1,1,1,1,0) in edge order
            # 01,02,03,12,13,23.  A zero bit uses the diagonal-live
            # chart (cell 2 is zero), while a one bit uses the
            # antidiagonal-live chart (cell 3 is zero).
            "aligned_zero_cells": [2, 7, 11, 15, 19, 22],
            "blocks": (
                "term bit1: [[a,b],[-1/b,0]]; term bit0: "
                "[[a,b],[0,-1/a]]"
            ),
        },
        "raw_surviving_rows": [label for label, _, _ in rows],
        "identity": "H = sum of nine displayed cleared source-row multiples",
        "source_terms": [
            {"label": label, "multiplier": serialize(multiplier),
             "singular_multiplier": text,
             "cleared_source_row": serialize(row_map[label])}
            for label, multiplier, text in lift
        ],
        "source_row_count": len(lift),
        "cleared_H": serialize(hafnian),
        "independent_sparse_replay": True,
        "deletion_mutation_fired": True,
        "H_live_Q_X_C_strata": [],
        "conclusion": (
            "The specialized pure H lies in the ideal of nine literal "
            "cleared base/cofactor rows. Hence this entire aligned chart has "
            "no H-live point, so no arbitrary-partner analysis is needed."
        ),
        "scope": (
            "This closes only the aligned zero-cell chart (branch0,term30). "
            "It does not close the surrounding 24-variable term open chart."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch0/term30 H identity: PASS")
    print("raw / used / H terms:", len(rows), len(lift), len(hafnian))
    print("labels:", expected_labels)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
