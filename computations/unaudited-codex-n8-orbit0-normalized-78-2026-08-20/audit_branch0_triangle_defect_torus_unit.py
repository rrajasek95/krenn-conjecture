#!/usr/bin/env python3
"""Exact torus-normalized unit for the branch-zero triangle defect stratum.

The defect support is the triangle {01,02,12}, edge indices {0,1,3}.
The anchor-preserving four-site torus first sets b03=b13=b23=1 and then,
over the algebraic closure, d01=1.  Three literal cofactor rows give two
linear relations, allowing d12 and b02 to be eliminated.  The resulting
13-row ideal is the unit ideal over Q after localizing only the genuinely
live b entries and diagonal permanent terms.  The pure Hafnian is not
localized: the whole triangle defect stratum is empty.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_nonaligned_defect_strata.py"
OUT = HERE / "results_branch0_triangle_defect_torus_unit.json"
SUPPORT = (0, 1, 3)
EXPECTED_REDUCED_LABELS = (6, 7, 8, 9, 10, 11, 12, 13,
                           14, 15, 17, 19, 21)


def load():
    spec = importlib.util.spec_from_file_location("n8_triangle_defect_probe",
                                                  PROBE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROBE = load()
CHART = PROBE.Chart(SUPPORT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


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
                term = CHART.multiply(
                    term, power(replacements[index], multiplicity))
        answer = CHART.add(answer, term)
    return answer


def gauge_rows():
    rows, _, _ = CHART.rows_and_hafnian()
    one = CHART.one
    gauge = {index: CHART.variable(index) for index in range(CHART.n)}
    for index in (8, 10, 11):  # b2=b4=b5=1
        gauge[index] = one
    gauge[CHART.d_index[0]] = one  # d0=1
    gauged = {index: substitute_poly(poly, gauge)
              for index, poly, _ in rows}

    # Literal short cofactor ledger before the two eliminations.
    r12, r16, r20 = gauged[12], gauged[16], gauged[20]
    d0 = one
    d1 = CHART.variable(CHART.d_index[1])
    d3 = CHART.variable(CHART.d_index[3])
    b0, b1 = CHART.variable(6), CHART.variable(7)
    sum_d = CHART.add(d0, d1, d3)
    ledger_one = CHART.add(r12, CHART.scale(r20, -1),
                           CHART.multiply(b0, r16),
                           CHART.scale(CHART.multiply(b0, sum_d), 2))
    require(ledger_one == {}, "three-cofactor d-sum ledger changed")
    expected_r16 = CHART.add(CHART.multiply(CHART.add(b1,
                                                     CHART.scale(one, -1)), d0),
                             CHART.multiply(CHART.add(b0,
                                                     CHART.scale(one, -1)), d1))
    require(r16 == expected_r16, "short b-relation cofactor changed")
    return rows, gauged


def reduced_system():
    rows, gauged = gauge_rows()
    one = CHART.one
    d1 = CHART.variable(CHART.d_index[1])
    b0 = CHART.variable(6)
    replacements = {index: CHART.variable(index)
                    for index in range(CHART.n)}
    # Consequences of the three short cofactor rows after d0=1.
    replacements[CHART.d_index[3]] = CHART.add(
        CHART.scale(one, -1), CHART.scale(d1, -1))
    replacements[7] = CHART.add(
        one, d1, CHART.scale(CHART.multiply(b0, d1), -1))

    reduced, seen = [], set()
    for index, _, _ in rows:
        value = substitute_poly(gauged[index], replacements)
        if not value:
            continue
        encoded = CHART.singular(value)
        if encoded in seen:
            continue
        seen.add(encoded)
        reduced.append((index, value, encoded))
    require(tuple(index for index, _, _ in reduced) == EXPECTED_REDUCED_LABELS,
            "reduced distinct source-row labels changed")

    # The six original b's become b0, b1=1+d1-b0*d1, b3 and three units.
    b_live = CHART.multiply(b0, replacements[7], CHART.variable(9))
    # a0*d0*a1*d1*a3*d3, with d0=1.
    both_live = CHART.multiply(
        CHART.variable(0), CHART.variable(1), CHART.variable(3),
        d1, replacements[CHART.d_index[3]])
    return reduced, b_live, both_live


def singular_status(characteristic, include_rows=True):
    rows, b_live, both_live = reduced_system()
    names = ",".join(CHART.names + ["z", "w"])
    generators = ([encoded for _, _, encoded in rows] if include_rows else [])
    generators += [f"z*({CHART.singular(b_live)})-1",
                   f"w*({CHART.singular(both_live)})-1"]
    command = (
        f"ring R={characteristic},({names}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=15, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"Singular characteristic {characteristic} failed")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    require(len(body) == 3, "Singular status output changed")
    return tuple(body)


def main():
    rows, b_live, both_live = reduced_system()
    exact = singular_status(0)
    require(exact == ("0", "1", "-1"),
            "triangle defect exact unit certificate failed")
    modular = {str(prime): singular_status(prime)
               for prime in (1009, 1013)}
    require(all(status == ("0", "1", "-1")
                for status in modular.values()),
            "triangle defect modular control changed")
    # Must-fire: localizers alone are not a contradiction; the literal
    # specialized source rows are essential to the unit computation.
    no_source_rows = singular_status(0, include_rows=False)
    require(no_source_rows[0] != "0",
            "source-row deletion must-fire control did not fire")

    result = {
        "status": "UNAUDITED exact torus-normalized triangle defect unit",
        "branch_mask": 0,
        "defect_support_edge_indices": list(SUPPORT),
        "defect_support_edges": [[0, 1], [0, 2], [1, 2]],
        "torus_action": (
            "at supervertex i use diag(t_i,t_i^-1); then "
            "a_ij->t_i*t_j*a_ij, b_ij->t_i/t_j*b_ij, "
            "c_ij->t_j/t_i*c_ij, d_ij->d_ij/(t_i*t_j)"
        ),
        "lossless_gauge": (
            "b03=b13=b23=1; the remaining common torus sets d01=1 "
            "over the algebraic closure"
        ),
        "cofactor_elimination": [
            "R12-R20+b0*R16=-2*b0*(d0+d1+d3)",
            "R16=(b1-1)*d0+(b0-1)*d1",
            "therefore d3=-1-d1 and b1=1+d1-b0*d1",
        ],
        "reduced_distinct_source_row_indices": list(EXPECTED_REDUCED_LABELS),
        "reduced_source_row_count": len(rows),
        "localized_after_gauge": [CHART.singular(b_live),
                                  CHART.singular(both_live)],
        "pure_H_localized": False,
        "exact_status_remainder_basis_size_dimension": list(exact),
        "modular_statuses": {prime: list(status)
                             for prime, status in modular.items()},
        "must_fire_without_source_rows": list(no_source_rows),
        "consequence": (
            "the entire branch-zero triangle both-term stratum is empty; "
            "this is stronger than exclusion of its H-live part"
        ),
        "scope": (
            "exact aligned-to-nonaligned defect stratum only; the unit is a "
            "Groebner certificate, not yet a serialized source multiplier lift"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-zero triangle defect torus unit: PASS")
    print("reduced rows / exact unit:", len(rows), exact)
    print("H localizer used / must-fire:", False, no_source_rows)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
