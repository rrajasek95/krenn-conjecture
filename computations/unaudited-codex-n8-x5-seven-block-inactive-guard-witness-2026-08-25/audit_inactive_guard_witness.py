#!/usr/bin/env python3
"""Exact triangle-inactive guard witness and surviving star route at seven blocks."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/results_seven_block_support_boundary.json"
PARENT_RESULT_SHA256 = "b3951e07149e4b831a5d3d3548284afb27f04154d805585468ba69bdb09b2f19"
REFEREE = HERE.parent / "unaudited-codex-n8-x5-support-induction-boundary-referee-2026-08-25/FINAL_MANIFEST.sha256"
REFEREE_SHA256 = "583bea191a1be0adb8d197270c22f9dd7b7ba0494b9d1f95b963213a19f23f61"
FIVE_SOURCE = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/audit_five_block_support_cap.py"
FIVE_SOURCE_SHA256 = "4a686fe5bbf80559283d993245166764d5b52d8b4bd33b144017f26f5f2c1f45"
CENSUS_SOURCE = HERE.parent / "unaudited-codex-n8-x5-single-offfamily-block-2026-08-25/audit_single_offfamily_block.py"
CENSUS_SOURCE_SHA256 = "2084fde03f78b9c535cda1d546c597ff79e967453560c17c1afdaefe710f7dc5"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(REFEREE) == REFEREE_SHA256
assert sha256(FIVE_SOURCE) == FIVE_SOURCE_SHA256
assert sha256(CENSUS_SOURCE) == CENSUS_SOURCE_SHA256

spec = importlib.util.spec_from_file_location("five_block", FIVE_SOURCE)
assert spec is not None and spec.loader is not None
five = importlib.util.module_from_spec(spec)
spec.loader.exec_module(five)
spec = importlib.util.spec_from_file_location("carrier_census", CENSUS_SOURCE)
assert spec is not None and spec.loader is not None
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)

STUCK_ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)))
STUCK_VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
SUPPORT = five.FIXED | STUCK_VARIABLE | STUCK_ADDED

# Stored-block convention A_uv with u<v: (row, column, coefficient).
MATRIX_UNITS = {
    (0, 4): (2, 0, +1),
    (0, 6): (1, 0, +1),
    (1, 2): (0, 0, -1),
    (1, 3): (1, 1, -1),
    (1, 7): (1, 2, -1),
    (2, 4): (1, 2, -1),
    (2, 6): (2, 1, -1),
    (3, 5): (2, 2, +1),
    (5, 6): (2, 2, -1),
    (5, 7): (2, 1, -1),
    (6, 7): (0, 1, -1),
}


def matrix_unit(row, column, coefficient):
    matrix = five.zero_matrix()
    matrix[row][column] = coefficient
    return matrix


def build_source():
    source = {}
    for edge in five.FIXED:
        five.install_block(source, edge, five.identity_matrix())
    for edge, coordinates in MATRIX_UNITS.items():
        five.install_block(source, edge, matrix_unit(*coordinates))
    return source


def matrix_strings(matrix):
    return [[str(value) for value in row] for row in matrix]


def response_terms(source, p, q, a, b, covector):
    direct = five.zero_matrix()
    switched = five.zero_matrix()
    for alpha, beta in itertools.product(five.core.COLORS, repeat=2):
        direct[alpha][beta] = sum(
            covector[i][j]
            * five.core.get(source, p, a, i, alpha)
            * five.core.get(source, q, b, j, beta)
            for i, j in itertools.product(five.core.COLORS, repeat=2)
        )
        switched[alpha][beta] = sum(
            covector[i][j]
            * five.core.get(source, p, b, i, beta)
            * five.core.get(source, q, a, j, alpha)
            for i, j in itertools.product(five.core.COLORS, repeat=2)
        )
    return direct, switched


def add_matrices(left, right):
    return [[left[i][j] + right[i][j] for j in five.core.COLORS] for i in five.core.COLORS]


def carrier_record(source, cap, internal_edges, carrier, label):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    forbidden = tuple(
        edge for edge in itertools.combinations(residual, 2)
        if edge not in internal_edges
    )
    columns = []
    for left, right in itertools.product(five.core.COLORS, repeat=2):
        K = census.basis_matrix(left, right)
        vector = []
        for a, b in forbidden:
            response = five.core.response(source, p, q, a, b, K)
            vector.extend(response[i][j] for i, j in itertools.product(five.core.COLORS, repeat=2))
        columns.append(vector)
    response_rows = [list(row) for row in zip(*columns)]
    response_rank = census.matrix_rank(columns)
    activities = [
        [int((left, right) == (colour, colour))
         for left, right in itertools.product(five.core.COLORS, repeat=2)]
        for colour in five.core.COLORS
    ]
    activities.append([
        five.core.get(source, p, q, left, right)
        for left, right in itertools.product(five.core.COLORS, repeat=2)
    ])
    activity_live = [
        census.matrix_rank(response_rows + [activity]) == response_rank + 1
        for activity in activities
    ]
    return {
        "cap": five.edge_string(cap),
        "carrier": label,
        "defining_sites": list(carrier),
        "forbidden_pairs": list(map(five.edge_string, forbidden)),
        "response_rank": response_rank,
        "kernel_dimension": 9 - response_rank,
        "activity_live": {
            "K00": activity_live[0],
            "K11": activity_live[1],
            "K22": activity_live[2],
            "cap_pairing": activity_live[3],
        },
        "active": response_rank < 9 and all(activity_live),
    }


def all_carriers(source):
    triangles = []
    stars = []
    for cap in itertools.combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in cap)
        for triangle in itertools.combinations(residual, 3):
            internal = set(itertools.combinations(triangle, 2))
            triangles.append(carrier_record(source, cap, internal, triangle, "triangle"))
        for center in residual:
            internal = {tuple(sorted((center, other))) for other in residual if other != center}
            stars.append(carrier_record(source, cap, internal, (center,), "star"))
    assert len(triangles) == 560 and len(stars) == 168
    return triangles, stars


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    unresolved = parent["exact_variable_stratum_classification"]["unresolved_orbit_records"]
    canonical = {
        (tuple(member["added"]), tuple(member["nonzero_variable_blocks"]))
        for orbit in unresolved for member in orbit["members"]
    }
    expected_key = (
        tuple(map(five.edge_string, sorted(STUCK_ADDED))),
        tuple(map(five.edge_string, sorted(STUCK_VARIABLE))),
    )
    assert expected_key in canonical
    assert set(MATRIX_UNITS) == (STUCK_ADDED | STUCK_VARIABLE)

    source = build_source()
    assert all(any(five.core.get(source, *edge, i, j) != 0
                   for i, j in itertools.product(five.core.COLORS, repeat=2))
               for edge in SUPPORT)

    outside = tuple(
        edge for edge in itertools.combinations(range(6), 2)
        if not set(edge) <= five.TRIANGLE
    )
    guard_records = []
    nontrivial_guard_equations = 0
    for edge in outside:
        direct, switched = response_terms(source, 6, 7, *edge, five.identity_matrix())
        total = add_matrices(direct, switched)
        assert total == five.zero_matrix()
        nontrivial = direct != five.zero_matrix() or switched != five.zero_matrix()
        if nontrivial:
            nontrivial_guard_equations += 1
            assert direct != five.zero_matrix() and switched != five.zero_matrix()
            assert direct == [[-value for value in row] for row in switched]
        guard_records.append({
            "response_pair": five.edge_string(edge),
            "direct_term": matrix_strings(direct),
            "switched_term": matrix_strings(switched),
            "sum": matrix_strings(total),
            "nontrivial_cancellation": nontrivial,
        })
    assert nontrivial_guard_equations == 2

    triangles, stars = all_carriers(source)
    assert not any(record["active"] for record in triangles)
    active_stars = [record for record in stars if record["active"]]
    assert [(record["cap"], record["defining_sites"]) for record in active_stars] == [
        ("16", [2]), ("45", [2])
    ]
    triangle_rank_census = Counter(record["response_rank"] for record in triangles)
    star_rank_census = Counter(record["response_rank"] for record in stars)
    triangle_failure_census = Counter(
        "rank9" if record["response_rank"] == 9 else
        (",".join(name for name, live in record["activity_live"].items() if not live) or "active")
        for record in triangles
    )
    star_failure_census = Counter(
        "rank9" if record["response_rank"] == 9 else
        (",".join(name for name, live in record["activity_live"].items() if not live) or "active")
        for record in stars
    )

    pure_amplitudes = [five.core.amplitude(source, (colour,) * 8) for colour in five.core.COLORS]
    assert pure_amplitudes == [1, 1, 1]
    residual_records = []
    for a, b in itertools.permutations(five.core.COLORS, 2):
        word = (a, b, b, a, a, a, b, b)
        residual_records.append({
            "word": "".join(map(str, word)),
            "amplitude": five.core.amplitude(source, word),
            "terms": [
                {"matching": five.core.matching_string(matching), "coefficient": value}
                for matching, value in five.core.amplitude_terms(source, word)
            ],
        })
    assert [record["amplitude"] for record in residual_records] == [1, 1, 1, 1, 1, 2]

    mixed = []
    amplitude_census = Counter()
    profile_census = Counter()
    for word in itertools.product(five.core.COLORS, repeat=8):
        value = five.core.amplitude(source, word)
        if len(set(word)) > 1 and value:
            mixed.append(("".join(map(str, word)), value))
            amplitude_census[value] += 1
            profile_census[five.core.profile(word)] += 1
    assert len(mixed) == 114

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_TRIANGLE_INACTIVE_GUARD_WITNESS_V1",
        "status": "PASS_TRIANGLE_INACTIVE_GUARD_WITNESS_STAR_ROUTE_SURVIVES_AND_FULL_X5_FAILS",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "referee_manifest_sha256": REFEREE_SHA256,
        "support": {
            "added": list(map(five.edge_string, sorted(STUCK_ADDED))),
            "nonzero_variable_blocks": list(map(five.edge_string, sorted(STUCK_VARIABLE))),
            "fixed_identity_blocks": list(map(five.edge_string, sorted(five.FIXED))),
            "all_15_blocks_nonzero": True,
            "minimal_relative_to_support_calculus": "parent closes every <=6-added-block support",
        },
        "source": {
            "fixed_blocks": "A03=A16=A27=A45=I3",
            "matrix_units": {
                five.edge_string(edge): {
                    "row": row, "column": column, "coefficient": coefficient
                }
                for edge, (row, column, coefficient) in sorted(MATRIX_UNITS.items())
            },
            "coefficient_ring": "Z",
        },
        "formal_guard": {
            "cap": "67",
            "triangle": "012",
            "K": "I3",
            "outside_response_equations": guard_records,
            "outside_equations": len(guard_records),
            "nontrivial_direct_switched_cancellations": nontrivial_guard_equations,
            "all_zero": True,
        },
        "activity_census": {
            "triangle_carriers": len(triangles),
            "active_triangle_carriers": 0,
            "triangle_response_rank_census": {str(k): v for k, v in sorted(triangle_rank_census.items())},
            "triangle_failure_census": dict(sorted(triangle_failure_census.items())),
            "triangle_records_sha256": hashlib.sha256(
                json.dumps(triangles, sort_keys=True).encode()
            ).hexdigest(),
            "star_carriers_supplementary": len(stars),
            "active_star_carriers": len(active_stars),
            "active_star_records": active_stars,
            "star_response_rank_census": {str(k): v for k, v in sorted(star_rank_census.items())},
            "star_failure_census": dict(sorted(star_failure_census.items())),
            "star_records_sha256": hashlib.sha256(
                json.dumps(stars, sort_keys=True).encode()
            ).hexdigest(),
            "exact_rational_rank_and_activity_replay": True,
        },
        "full_X5_test": {
            "pure_amplitudes": pure_amplitudes,
            "pure_normalization_pass": True,
            "six_residuals": residual_records,
            "six_residual_common_zero": False,
            "first_false_equation": residual_records[0],
            "nonzero_mixed_amplitudes": len(mixed),
            "amplitude_census": {str(k): v for k, v in sorted(amplitude_census.items())},
            "profile_census": dict(sorted(profile_census.items())),
            "mixed_ledger_sha256": hashlib.sha256(
                json.dumps(mixed, sort_keys=True).encode()
            ).hexdigest(),
            "is_full_X5_point": False,
        },
        "theorem_verdict": {
            "guard_plus_pure_forces_block_zero_or_active_triangle": False,
            "counterexample_scope": "exact integer matrix-unit source on canonical minimal stuck support",
            "guard_plus_pure_forces_block_zero_or_active_triangle_or_star": "NOT_REFUTED; two active stars survive",
            "guard_plus_full_X5_forces_block_zero_or_active_cap": "OPEN; witness fails six residuals and 114 mixed rows",
            "referee_complete_switched_rectangle_lemma": "NOT_REFUTED_IF_FULL_EQUATIONS_ARE_HYPOTHESES",
            "coefficient_minor_boundary_is_genuine": True,
        },
        "scope": {
            "exact_canonical_stuck_support": True,
            "all_560_triangle_carriers": True,
            "all_168_star_carriers_supplementary": True,
            "formal_guard": True,
            "pure_normalization": True,
            "full_X5": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_inactive_guard_witness.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_inactive_guard_witness.json")
    print(json.dumps({
        "status": result["status"],
        "guard_equations": len(guard_records),
        "nontrivial_guard_cancellations": nontrivial_guard_equations,
        "active_triangles": 0,
        "active_stars": len(active_stars),
        "pures": pure_amplitudes,
        "six_residuals": [record["amplitude"] for record in residual_records],
        "mixed": len(mixed),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
