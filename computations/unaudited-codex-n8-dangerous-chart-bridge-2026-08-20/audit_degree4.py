#!/usr/bin/env python3
"""Exact K-degree-four lift for dangerous pure-matching charts 25--28.

This is a separate checker because closing the literal degree-four incidence
component is materially larger than the anchor/degree-two/three audit.  It
imports that audit by pinned local path, reconstructs every component, finds
an integer lower-filtration solution by modular discovery, and accepts the
solution only after a literal characteristic-zero replay.

The conclusion ``H0 H1 H2 in I_mix + K^5`` is filtered-boundary progress.
It is not a full localized-chart identity and not an N=8 proof.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("dangerous_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_degree4.json"
PRIME = 1009
EXPECTED = {
    25: ((17610, 75900), 126, (201, 44, 1713, 1958)),
    26: ((16332, 64628), 0, (171, 9, 1541, 1721)),
    27: ((17578, 75720), 190, (440, 64, 3289, 3793)),
    28: ((16300, 64190), 2, (199, 19, 1753, 1971)),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def build_components(matchings):
    anchors = BASE.anchor_ids(matchings)
    anchor_row = bytes(sorted(anchors))
    seeds = BASE.seed_columns(matchings)

    target2 = BASE.filtered_target(matchings, 2)
    start2 = set(target2)
    for column in seeds:
        start2.update(row for row in BASE.column_rows(column)
                      if BASE.row_degree(row, anchors) == 2)
    rows2, columns2 = BASE.close_exact_degree(start2, anchors, 2)
    lower2 = seeds + tuple(sorted(columns2, key=repr))

    target3 = BASE.filtered_target(matchings, 3)
    start3 = set(target3)
    for column in lower2:
        start3.update(row for row in BASE.column_rows(column)
                      if BASE.row_degree(row, anchors) == 3)
    rows3, columns3 = BASE.close_exact_degree(start3, anchors, 3)
    lower3 = lower2 + tuple(sorted(columns3, key=repr))

    target4 = BASE.filtered_target(matchings, 4)
    start4 = set(target4)
    for column in lower3:
        start4.update(row for row in BASE.column_rows(column)
                      if BASE.row_degree(row, anchors) == 4)
    rows4, columns4 = BASE.close_exact_degree(start4, anchors, 4)
    return {
        "anchors": anchors,
        "anchor_row": anchor_row,
        "targets": {2: target2, 3: target3, 4: target4},
        "rows": {2: rows2, 3: rows3, 4: rows4},
        "columns": {0: seeds, 2: columns2, 3: columns3, 4: columns4},
        "lower3": lower3,
    }


def modular_integer_solution(rows, columns, target):
    """Discover mod PRIME, center residues, then require exact Z replay."""
    row_index = {row: index for index, row in enumerate(rows)}
    vectors = []
    basis = {}
    for number, column in enumerate(columns):
        raw = Counter(row_index[row] for row in BASE.column_rows(column)
                      if row in row_index)
        vectors.append(raw)
        vector = {i: value % PRIME for i, value in raw.items()
                  if value % PRIME}
        combination = {number: 1}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, PRIME)
                vector = {i: entry * inverse % PRIME
                          for i, entry in vector.items()}
                combination = {i: entry * inverse % PRIME
                               for i, entry in combination.items()}
                basis[pivot] = (vector, combination)
                break
            base_vector, base_combination = basis[pivot]
            for i, entry in base_vector.items():
                new = (vector.get(i, 0) - value * entry) % PRIME
                if new:
                    vector[i] = new
                else:
                    vector.pop(i, None)
            for i, entry in base_combination.items():
                new = (combination.get(i, 0) - value * entry) % PRIME
                if new:
                    combination[i] = new
                else:
                    combination.pop(i, None)
        if len(basis) == len(rows):
            break
    require(len(basis) == len(rows),
            "augmented lower-degree matrix is not full row rank mod PRIME")

    residual = {row_index[row]: value % PRIME
                for row, value in target.items() if value % PRIME}
    solution_mod = {}
    while residual:
        pivot = min(residual)
        value = residual[pivot]
        require(pivot in basis, "modular target left the discovered image")
        base_vector, base_combination = basis[pivot]
        for i, entry in base_vector.items():
            new = (residual.get(i, 0) - value * entry) % PRIME
            if new:
                residual[i] = new
            else:
                residual.pop(i, None)
        for i, entry in base_combination.items():
            new = (solution_mod.get(i, 0) + value * entry) % PRIME
            if new:
                solution_mod[i] = new
            else:
                solution_mod.pop(i, None)
    solution = {
        index: value if value <= PRIME // 2 else value - PRIME
        for index, value in solution_mod.items()
    }
    replay = Counter()
    for index, coefficient in solution.items():
        for row, multiplicity in vectors[index].items():
            replay[row] += coefficient * multiplicity
    replay = Counter({row: value for row, value in replay.items() if value})
    expected = Counter({row_index[row]: value
                        for row, value in target.items() if value})
    require(replay == expected,
            "centered modular solution is not an exact integer solution")
    return tuple((Fraction(coefficient), columns[index])
                 for index, coefficient in sorted(solution.items()))


def exact_degree4_certificate(chart, matchings):
    data = build_components(matchings)
    anchors = data["anchors"]
    anchor_row = data["anchor_row"]
    target2, target3, target4 = (data["targets"][d] for d in (2, 3, 4))
    rows2, rows3, rows4 = (data["rows"][d] for d in (2, 3, 4))
    columns4 = data["columns"][4]
    lower = data["lower3"]

    singleton = {}
    triple = []
    covered4 = set()
    leading_histogram = Counter()
    for column in sorted(columns4, key=repr):
        outputs = tuple(row for row in BASE.column_rows(column)
                        if BASE.row_degree(row, anchors) == 4)
        require(len(outputs) in (1, 3),
                "degree-four leading term count left {1,3}")
        leading_histogram[len(outputs)] += 1
        covered4.update(outputs)
        if len(outputs) == 1:
            singleton.setdefault(outputs[0], column)
        else:
            triple.append((outputs, column))
    hard = tuple(sorted(set(rows4) - covered4))
    lower_rows = (
        (anchor_row,) + tuple(sorted(rows2)) + tuple(sorted(rows3)) + hard
    )
    lower_target = Counter({anchor_row: 1})
    lower_target.update(target2)
    lower_target.update(target3)
    lower_target.update({row: target4[row] for row in hard})
    lower_certificate = list(modular_integer_solution(
        lower_rows, lower, lower_target
    ))

    current4 = Counter()
    for coefficient, column in lower_certificate:
        for row in BASE.column_rows(column):
            if BASE.row_degree(row, anchors) == 4:
                current4[row] += coefficient
    residual = {
        row: Fraction(target4[row]) - current4[row]
        for row in set(target4) | set(current4)
        if Fraction(target4[row]) - current4[row]
    }
    require(not (set(residual) & set(hard)),
            "lower solution did not kill the hard degree-four quotient")

    non_singleton = set(rows4) - set(singleton)
    triple_pivot = {}
    for outputs, column in triple:
        projected = tuple(row for row in outputs if row in non_singleton)
        require(len(projected) <= 1,
                "triple column couples two non-singleton quotient rows")
        if projected:
            triple_pivot.setdefault(projected[0], column)
    triple_certificate = []
    for row in sorted(set(residual) & non_singleton):
        require(row in triple_pivot,
                "degree-four residual has no triple quotient pivot")
        coefficient = residual[row]
        column = triple_pivot[row]
        triple_certificate.append((coefficient, column))
        for output in BASE.column_rows(column):
            if BASE.row_degree(output, anchors) == 4:
                value = residual.get(output, Fraction(target4[output])
                                     - current4[output]) - coefficient
                if value:
                    residual[output] = value
                else:
                    residual.pop(output, None)
    require(not (set(residual) & non_singleton),
            "triple pivots left a non-singleton residual")

    singleton_certificate = []
    for row, coefficient in sorted(residual.items()):
        require(row in singleton, "degree-four singleton pivot missing")
        singleton_certificate.append((coefficient, singleton[row]))
    certificate = (
        tuple(lower_certificate) + tuple(triple_certificate)
        + tuple(singleton_certificate)
    )
    replay = Counter()
    for coefficient, column in certificate:
        for row in BASE.column_rows(column):
            degree = BASE.row_degree(row, anchors)
            if degree in (0, 2, 3, 4):
                replay[row] += coefficient
    replay = Counter({row: value for row, value in replay.items() if value})
    expected = Counter({anchor_row: Fraction(1)})
    expected.update({row: Fraction(value) for row, value in target2.items()})
    expected.update({row: Fraction(value) for row, value in target3.items()})
    expected.update({row: Fraction(value) for row, value in target4.items()})
    require(replay == expected, "exact degree-four certificate replay failed")
    negative = next(((coefficient, column)
                     for coefficient, column in certificate
                     if coefficient < 0), None)
    require(negative is not None, "degree-four certificate has no negative term")
    mutation = Counter(replay)
    coefficient, column = negative
    for row in BASE.column_rows(column):
        if BASE.row_degree(row, anchors) in (0, 2, 3, 4):
            mutation[row] -= 2 * coefficient
    mutation = Counter({row: value for row, value in mutation.items() if value})
    require(mutation != expected, "negative degree-four sign mutation did not fire")

    coefficient_histogram = Counter(str(value) for value, _column in certificate)
    certificate_ledger = []
    for coefficient, (word, multiplier) in certificate:
        certificate_ledger.append({
            "coefficient": str(coefficient),
            "word": BASE.word_name(word),
            "multiplier": [BASE.cell_name(BASE.CELLS[cell])
                           for cell in multiplier],
            "minimum_K_degree": BASE.column_minimum_degree(
                (word, multiplier), anchors
            ),
        })
    frozen = (
        (len(rows4), len(columns4)),
        len(hard),
        (
            len(lower_certificate), len(triple_certificate),
            len(singleton_certificate), len(certificate),
        ),
    )
    require(frozen == EXPECTED[chart],
            "frozen degree-four component/certificate census changed")
    return {
        "chart": chart,
        "legacy_one_based_chart": chart + 3,
        "K": "the 240 cells outside the twelve named pure anchors",
        "component": {
            "degree_two_rows_columns": [len(rows2), len(data["columns"][2])],
            "degree_three_rows_columns": [len(rows3), len(data["columns"][3])],
            "degree_four_rows_columns": [len(rows4), len(columns4)],
            "degree_four_leading_term_histogram": {
                str(k): value for k, value in sorted(leading_histogram.items())
            },
            "singleton_pivot_rows": len(singleton),
            "hard_rows_not_hit_by_any_min_degree_four_column": len(hard),
        },
        "certificate": {
            "lower_filtration_terms": len(lower_certificate),
            "triple_pivot_terms": len(triple_certificate),
            "singleton_pivot_terms": len(singleton_certificate),
            "total_terms": len(certificate),
            "coefficient_histogram": dict(sorted(coefficient_histogram.items())),
            "denominator_lcm": 1,
            "literal_replay": True,
            "negative_sign_mutation_fired": True,
            "terms": certificate_ledger,
        },
        "conclusion": "H0*H1*H2 belongs to I_mix + K^5 over Q",
        "full_localized_chart_controlled": False,
        "scope": (
            "exact filtered identity through K-degree four only; terms of "
            "K-degree five and higher remain uncontrolled"
        ),
    }


def audit():
    base_result = json.loads(BASE.OUT.read_text())
    require(base_result["result_sha256"]
            == "49226ce09479fb174221cb02d64b53d77e3574ea462dee5fa06f05f196dd02f5",
            "pinned degree-three result changed")
    charts = {}
    for chart, matchings in BASE.CHARTS.items():
        charts[str(chart)] = exact_degree4_certificate(chart, matchings)
        record = charts[str(chart)]
        print(
            f"milestone chart {chart}: "
            f"d4={record['component']['degree_four_rows_columns']}, "
            f"hard={record['component']['hard_rows_not_hit_by_any_min_degree_four_column']}, "
            f"certificate={record['certificate']['total_terms']}",
            flush=True,
        )
    core = {
        "status": "UNAUDITED exact K-adic lift; full chart remains open",
        "base_result_sha256": base_result["result_sha256"],
        "charts": charts,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("dangerous-chart degree-four audit: PASS")
    for chart, record in result["charts"].items():
        component = record["component"]
        certificate = record["certificate"]
        print(
            f"chart {chart} (legacy {record['legacy_one_based_chart']}): "
            f"d4 rows/cols={component['degree_four_rows_columns']}, "
            f"hard={component['hard_rows_not_hit_by_any_min_degree_four_column']}, "
            f"certificate={certificate['total_terms']}"
        )
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
