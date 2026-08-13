#!/usr/bin/env python3
"""Assemble the five physical face separators across the cyclic edge lattice.

Each repeated face component has a primitive six-term covector, and the
canonical face calculation identifies its pure marker with minus physical
anchor incidence.  Normalize the five facewise covectors to take value one
on their desired boundary-zero anchors.  The covariance-Spencer bridge
orbit consists of the five oriented C5 incidence columns.  Therefore the
sum of the face covectors kills all edge comparisons.  The only remaining
cyclic direction is the primitive aggregate (1,1,1,1,1), on which it reads
five.  Over characteristic zero, a physical aggregate relative cell either
normalizes to the required generator or, if absent/killed, leaves the summed
physical separator.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_repeated_component_six_term_separators.py":
        "b8c3eff88b44a9a12d45f61b44449ac8a0b3a4c3e9a6d351a50ef19293ce2d25",
    "computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py":
        "01d4d504c0d5d9ac8fd643e06a38b35d75962c859e41908bff3161d10c7cbc13",
    "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py":
        "d1b545f25603930a6247a286c5be70c7d16e20caab053401eeeb650bb53559d6",
}
EXPECTED_LEDGER_SHA256 = "3175a867a20de2a9cdf7ba2214f42b7b19709d831bc2f506310204fd3b28af51"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def rank(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(rows)]
    pivot = 0
    for column in range(len(columns)):
        hit = next((row for row in range(pivot, rows)
                    if work[row][column]), None)
        if hit is None:
            continue
        work[pivot], work[hit] = work[hit], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [value / scale for value in work[pivot]]
        for row in range(rows):
            if row == pivot or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right for left, right in
                         zip(work[row], work[pivot], strict=True)]
        pivot += 1
    return pivot


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
    physical = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "cyclic_physical_separator_face",
    )
    six = load(
        "computations/verify_h3_repeated_component_six_term_separators.py",
        "cyclic_physical_separator_six",
    )
    orbit = load(
        "computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py",
        "cyclic_physical_separator_orbit",
    )
    absolute = load(
        "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py",
        "cyclic_physical_separator_absolute",
    )
    require(physical.EXPECTED_LEDGER_SHA256
            == "bd41b41fdef28c5a2cfcf2d1c187e7145eb5c1c54a3015be7cbd0d61b3760bbd",
            "canonical physical separator ledger pin changed")
    require(six.EXPECTED_LEDGER_SHA256
            == "6063daed9a1759d2051996230a6b6906a9c7136380593476f7fd6e8c352e6497",
            "five six-term dual ledger pin changed")
    require(orbit.EXPECTED_LEDGER_SHA256
            == "7f46d103e1f06a6573a56631de15114b80dfdb8fb51b9b42d334e9cf274b74fc",
            "cyclic bridge ledger pin changed")
    require(absolute.EXPECTED_LEDGER_SHA256
            == "ae3c65f9ed33f96a568621f35df250fb5885d5ef650edcdcdd0bd456ca0c4c63",
            "absolute exhaustivity ledger pin changed")

    cycle_ledger = orbit.audit()
    columns = [tuple(record["face_boundary"])
               for record in cycle_ledger["bridge_orbit"]]
    aggregate = (1, 1, 1, 1, 1)
    require(rank(columns) == 4, "cyclic edge rank changed")
    edge_pairings = [sum(left * right for left, right in
                         zip(aggregate, column, strict=True))
                     for column in columns]
    require(set(edge_pairings) == {0},
            "summed physical separator sees a cyclic edge")
    aggregate_value = sum(aggregate)
    require(aggregate_value == 5,
            "summed physical separator lost primitive aggregate value")
    normalized_generator_scale = Q(1, aggregate_value)
    require(normalized_generator_scale * aggregate_value == 1,
            "characteristic-zero aggregate normalization failed")

    return {
        "theorem": "cyclic physical separator or aggregate generator",
        "face_order": list(orbit.CYCLE),
        "facewise_covectors": [
            "Lambda_v=sum six private matching rows in face grade v - ainc_v"
            for _ in orbit.CYCLE
        ],
        "facewise_normalization_on_desired_anchor": [1] * 5,
        "cyclic_edge_columns": [list(column) for column in columns],
        "cyclic_edge_rank": rank(columns),
        "summed_separator_pairing_on_edges": edge_pairings,
        "primitive_aggregate": list(aggregate),
        "summed_separator_pairing_on_aggregate": aggregate_value,
        "aggregate_generator_normalization": str(normalized_generator_scale),
        "alternative": {
            "relative_aggregate_cell_exists": (
                "its nonzero value 5 normalizes over characteristic zero to "
                "the physical relative-generator branch"
            ),
            "relative_aggregate_cell_absent_or_killed": (
                "the sum of the five physical face covectors descends across "
                "the whole rank-four cyclic comparison lattice"
            ),
        },
        "absolute_source_status": (
            "each face covector already kills its complete absolute "
            "source/bar/Tate component"
        ),
        "remaining_physical_check": (
            "the genuinely relative aggregate generator family and the "
            "identification of the descended summed covector with the final "
            "rootless/pentagon terminal"
        ),
        "scope": (
            "exact C5 incidence assembly of the five componentwise physical "
            "covectors.  Physical realization of the four symbolic edge "
            "comparisons, arbitrary relative terminal corrections, and "
            "transverse rank landing are not asserted"
        ),
    }


def main():
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("cyclic physical separator ledger changed", digest))
    print("h3 cyclic physical separator/aggregate generator: PASS")
    print("sum Lambda_v kills all five cyclic edges")
    print("aggregate pairing: 5; normalized generator scale: 1/5")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
