#!/usr/bin/env python3
"""Certify that the orbit transfer is not yet a single-chart localization."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TAIL_PATH = HERE / "verify_n8_root_plateau_transferred_tail.py"
SPEC = importlib.util.spec_from_file_location("n8_root_transfer_guard", TAIL_PATH)
TAIL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TAIL)
SOURCE = TAIL.SOURCE
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "edfcf65d948469317b5cac65a443e09879572cf536aa52e8704504ad0b45bb7c"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    roots = tuple(sorted(SOURCE.target_orbit_rows()))
    root_index = {row: index for index, row in enumerate(roots)}
    columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in roots
    ))))
    column_index = {column: index for index, column in enumerate(columns)}
    incident_roots = [set() for _column in columns]
    for root_number, row in enumerate(roots):
        for column in SOURCE.incident_columns(row):
            incident_roots[column_index[column]].add(root_number)

    top_columns = []
    fibre_orbit_sizes = []
    fibre_multiplicity_histogram = Counter()
    for column in columns:
        entries = Counter(SOURCE.column_outputs(column))
        fibre_orbit_sizes.append(len(entries))
        fibre_multiplicity_histogram.update(entries.values())
        top_columns.append({
            root_index[row]: QQ(coefficient)
            for row, coefficient in entries.items() if row in root_index
        })

    pivots = {}
    pivot_representatives = {}
    zero_representatives = {}
    for column_number, source in enumerate(top_columns):
        vector = dict(source)
        representative = {column_number: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                pivot_representatives[pivot] = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                break
            TAIL.add_scaled(vector, pivots[pivot], -value)
            TAIL.add_scaled(representative, pivot_representatives[pivot], -value)
        if not vector:
            require(not TAIL.replay(top_columns, representative),
                    "root-kernel representative did not replay")
            zero_representatives[column_number] = representative

    require(len(zero_representatives) == 7,
            "root plateau kernel dimension changed")
    records = []
    for source_column, representative in sorted(zero_representatives.items()):
        support = tuple(sorted(representative))
        common = set(range(len(roots)))
        touched = set()
        for column in support:
            common &= incident_roots[column]
            touched |= incident_roots[column]
        records.append({
            "kernel_source_column": source_column + 1,
            "representative_support_columns": [column + 1 for column in support],
            "representative_support_size": len(support),
            "touched_root_charts": [root + 1 for root in sorted(touched)],
            "common_incident_root_charts": [root + 1 for root in sorted(common)],
        })
    require(all(not record["common_incident_root_charts"] for record in records),
            "a root-kernel representative unexpectedly stayed in one chart")
    require(any(value > 1 for value in fibre_multiplicity_histogram),
            "orbit compression unexpectedly became labelled-injective")

    ledger = {
        "root_orbits": len(roots),
        "support_column_orbits": len(columns),
        "root_kernel_dimension": len(records),
        "root_kernel_chart_provenance": records,
        "kernel_representatives_with_common_incident_chart": 0,
        "full_fibre_labelled_terms_per_column": 105,
        "canonical_output_orbit_count_histogram": dict(sorted(Counter(
            fibre_orbit_sizes
        ).items())),
        "canonical_output_multiplicity_histogram": dict(sorted(
            fibre_multiplicity_histogram.items()
        )),
        "individual_chart_localization_certificate": False,
        "missing_lift": (
            "a labelled Macaulay relation within one P_j localization, or "
            "an explicit multiplication by that chart's anchor product "
            "giving a common-denominator lift of every cross-chart column"
        ),
        "scope_guard": (
            "the transferred relations are exact in the S8xS3 "
            "orbit-compressed incidence module only; orbit-kernel provenance "
            "does not certify P_j-localized ideal membership"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "orbit-transfer localization guard changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
