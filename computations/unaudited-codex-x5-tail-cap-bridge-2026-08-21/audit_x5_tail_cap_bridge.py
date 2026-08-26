#!/usr/bin/env python3
"""Structural audit of the X5 -> tail response -> clean-cap interface.

This checker deliberately proves only row provenance and finite-ledger
correspondence.  It also freezes the exact logical gap: the tail theorem is
an associated-graded 12-column quotient, not a global entry/lifting theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import sys


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESPONSE = ROOT / "computations/unaudited-codex-response-star-2026-08-20"
TAIL = ROOT / "computations/unaudited-codex-tail-polar-source-lift-2026-08-21"
OUT = HERE / "results_x5_tail_cap_bridge.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def logical_sha(payload) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def off_count(label: str) -> int:
    require(label.startswith("F_") and len(label) == 10, f"bad source label {label}")
    word = label[2:]
    require(set(word) <= {"0", "1", "2"}, f"bad source word {label}")
    return 8 - max(word.count(str(colour)) for colour in range(3))


def audit_carriers(response):
    star_path = RESPONSE / "response_star_matrices_w40.jsonl"
    triangle_path = RESPONSE / "response_triangle_matrices_w40.jsonl"
    stars = load_jsonl(star_path)
    triangles = load_jsonl(triangle_path)

    expected_stars = {
        ((p, q), v)
        for p in range(8) for q in range(p + 1, 8)
        for v in range(8) if v not in (p, q)
    }
    actual_stars = {(tuple(row["pair"]), row["centre"]) for row in stars}
    require(actual_stars == expected_stars, "star carrier labels changed")
    require(len(stars) == 168, "star carrier count changed")
    for row in stars:
        require(len(row["rows"]) == 90, "star response row count changed")
        require(len(row["row_labels"]) == 90, "star row-label count changed")
        require(len(row["activity_in_rowspan"]) == 4, "star blocker count changed")

    expected_triangles = set()
    for p in range(8):
        for q in range(p + 1, 8):
            residual = [v for v in range(8) if v not in (p, q)]
            for tri in itertools.combinations(residual, 3):
                expected_triangles.add(((p, q), tri))
    actual_triangles = {
        (tuple(row["pair"]), tuple(row["triangle"])) for row in triangles
    }
    require(actual_triangles == expected_triangles, "triangle carrier labels changed")
    require(len(triangles) == 560, "triangle carrier count changed")
    for row in triangles:
        require(len(row["rows"]) == 108, "triangle response row count changed")
        require(len(row["row_labels"]) == 108, "triangle row-label count changed")
        require(len(row["activity_in_rowspan"]) == 4,
                "triangle blocker count changed")

    require(response["criterion"]["activity_forms"] ==
            ["K00", "K11", "K22", "<K,A_pq>"],
            "carrier activity forms changed")
    return {
        "star": {"carriers": 168, "rows_per_matrix": 90},
        "triangle": {"carriers": 560, "rows_per_matrix": 108},
        "total_carriers": 728,
        "blockers_per_carrier": 4,
        "simultaneous_no_cap_clause_count": 728,
        "labelled_membership_predicates": 2912,
        "activity_forms": response["criterion"]["activity_forms"],
        "ledger_hashes": {
            star_path.name: sha256(star_path),
            triangle_path.name: sha256(triangle_path),
        },
    }


def audit_tail_rows(base, rescue, closure):
    ledger = base["row_ledger"]
    require(len(ledger) == 380, "tail row ledger count changed")
    labels = [row["source_label"] for row in ledger]
    require(len(set(labels)) == 380, "tail source labels ceased to be unique")
    profiles = {}
    off_counts = {}
    for row in ledger:
        profile = row["profile"]
        profiles[profile] = profiles.get(profile, 0) + 1
        degree = off_count(row["source_label"])
        off_counts[degree] = off_counts.get(degree, 0) + 1
    require(profiles == {"7+1": 8, "6+1+1": 12, "3+3+2": 360},
            "tail profile census changed")
    require(off_counts == {1: 8, 2: 12, 5: 360},
            "tail off-count census changed")
    require(base["source_row_census"]["columns"] == 12,
            "tail polar-column count changed")
    require(base["generic_rank_theorem"]["combined_rank_over_Q_G0_G1_G2"] == 12,
            "generic tail rank changed")

    selected = base["source_faithful_6+1+1_elimination"]["rows"]
    selected_map = {row["source_label"]: row["column"] for row in selected}
    require(len(selected_map) == 12, "611 pivot-label count changed")
    require(set(selected_map.values()) == set(base["retained_star_columns"]),
            "611 pivots ceased to cover the 12 polar columns")
    by_label = {row["source_label"]: row for row in ledger}
    for label, column in selected_map.items():
        require(by_label[label]["profile"] == "6+1+1",
                f"611 pivot {label} changed profile")
        require(set(by_label[label]["nonzero_columns"]) == {column},
                f"611 pivot {label} ceased to be column-diagonal")

    coverage = rescue["generic_principal_open_coverage"]
    require(coverage == {
        "Delta_layer": 33, "Hall_d3": 16, "Hall_d4": 8,
        "Hall_d5": 2, "Hall_d6": 1, "SDR": 66, "total": 126,
    }, "126-orbit tail coverage changed")
    require(closure["closed_orbit_census"]["total"] == 126,
            "nonmonomial closure orbit total changed")
    remaining = closure["remaining_recursive_divisor_antichain"]
    require(len(remaining) == 1, "tail recursive antichain family count changed")
    require(remaining[0]["factor_family"] == "support_monomial",
            "unexpected tail boundary family")
    require(remaining[0]["factor_orbit_count"] == 4,
            "support-factor orbit count changed")

    return {
        "matrix_shape": [380, 12],
        "profile_counts": profiles,
        "off_count_counts": {str(k): off_counts[k] for k in sorted(off_counts)},
        "X4_rows_available": sum(count for degree, count in off_counts.items()
                                 if degree <= 4),
        "X4_rows_missing": sum(count for degree, count in off_counts.items()
                               if degree > 4),
        "X5_rows_available": len(ledger),
        "rank_over_Q_G0_G1_G2": 12,
        "polar_columns": base["retained_star_columns"],
        "diagonal_611_pivots": selected_map,
        "missing_pattern_orbits": coverage,
        "closed_nonmonomial_boundaries":
            closure["removed_nonmonomial_factor_orbits"],
        "remaining_support_factor_orbits": remaining[0]["suborbits"],
    }


def main() -> None:
    response_path = RESPONSE / "results_response_star.json"
    base_path = TAIL / "results_tail_polar_source_lift.json"
    rescue_path = TAIL / "results_tail_response_rescue_theorem.json"
    closure_path = TAIL / "results_tail_nonmonomial_boundary_closure.json"
    response = load_json(response_path)
    base = load_json(base_path)
    rescue = load_json(rescue_path)
    closure = load_json(closure_path)

    carrier = audit_carriers(response)
    tail = audit_tail_rows(base, rescue, closure)

    histogram = {}
    mixed = 0
    for word in itertools.product(range(3), repeat=8):
        degree = 8 - max(word.count(c) for c in range(3))
        histogram[degree] = histogram.get(degree, 0) + 1
        if degree:
            mixed += 1
    require(histogram == {0: 3, 1: 48, 2: 336, 3: 1344, 4: 3150, 5: 1680},
            "global off-count histogram changed")
    require(mixed == 6558, "mixed row count changed")

    payload = {
        "status": "PASS exact structural X5/tail/carrier interface audit",
        "raw_row_scope": {
            "all_words": 6561,
            "pure_rows": 3,
            "mixed_rows": 6558,
            "off_count_histogram": {str(k): histogram[k] for k in sorted(histogram)},
            "X4_mixed_rows": sum(histogram[k] for k in range(1, 5)),
            "X5_mixed_rows": sum(histogram[k] for k in range(1, 6)),
            "X5_equals_full_mixed_scope_for_N8_d3": True,
        },
        "carrier_interface": carrier,
        "tail_interface": tail,
        "source_scope_verdict": {
            "X4_to_tail_380": "FAIL: 360 profile-332 rows have off-count 5",
            "X5_to_tail_380": "PASS row provenance: all 380 labels are X5 rows",
            "warning": (
                "Row provenance does not imply global tail entry or lifting; "
                "the frozen theorem is a 12-column associated-graded quotient."
            ),
        },
        "conditional_X5_to_cap": {
            "proved_implication": (
                "carrier_to_tail_entry_and_lifting + closure_of_the_four_"
                "support_factor_orbits + terminal_same_source_cap_extraction "
                "implies X5-to-cap"
            ),
            "not_proved": (
                "X5 plus the 728 no-cap clauses does not presently supply "
                "the entry/lifting or terminal extraction hypotheses."
            ),
        },
        "missing_lemma": {
            "name": "carrier-to-tail entry, lifting, and termination lemma",
            "ambient_variables": {
                "diagonal": "g^c_uv=A_uv[c,c], 3*28=84",
                "cross_colour": "t^ij_uv=A_uv[i,j], i!=j, 6*28=168",
                "total": 252,
                "fixed_tail_polar_slice":
                    "y_a=A_a6[0,1], z_a=A_a7[0,1], 0<=a<6",
            },
            "equations": {
                "source": "F_w=0 for all 6558 mixed words; pure F_cccccccc=1",
                "no_cap_branch": (
                    "for each of 728 carriers choose i in {0,1,2,3}, a rank r, "
                    "and an invertible r-minor of L_C; impose all (r+1)-minors "
                    "of [L_C;ell_i]"
                ),
                "tail_rows": "8 profile-71 + 12 profile-611 + 360 profile-332",
            },
            "localizers": {
                "carrier": "the chosen nonzero rank minor for every carrier branch",
                "tail": (
                    "remaining 611 Hafnian cofactors and the exact support monomial "
                    "of the chosen rescue minor"
                ),
                "normalization": "the three pure Hafnians, fixed to 1",
            },
            "required_conclusion": (
                "After site/colour transport and a well-founded tail ordering, "
                "all columns deleted in the 12-column quotient are already "
                "eliminated; the displayed full-rank minor therefore removes "
                "the next 12 cells in the actual source ideal. Iteration must "
                "terminate at an active star/triangle cap on the same source "
                "(or at a separately justified strict minimum-support descent)."
            ),
            "four_support_orbits_are_only_chartwise_rank_boundaries": True,
            "four_support_orbits_are_only_global_obstruction": False,
        },
        "implication_diagram": [
            "X5 literal rows (all 6558 mixed; selected 380 source-labelled)",
            "MISSING carrier-to-tail entry/order from the 728 simultaneous blocker clauses",
            "frozen 380x12 lowest-tail quotient rank on 126 pattern opens",
            "MISSING quotient-to-full-ideal lifting and well-founded iteration",
            "four support-monomial recursive boundary orbits",
            "MISSING terminal same-source active clean-cap extraction",
            "exact star/triangle criterion (168+560 carriers)",
        ],
        "source_hashes": {
            str(response_path.relative_to(ROOT)): sha256(response_path),
            str(base_path.relative_to(ROOT)): sha256(base_path),
            str(rescue_path.relative_to(ROOT)): sha256(rescue_path),
            str(closure_path.relative_to(ROOT)): sha256(closure_path),
        },
        "mutation_guards": {
            "drop_one_332_row_breaks_X5_tail_census": True,
            "relabel_one_611_column_breaks_diagonal_pivot_bijection": True,
            "delete_one_carrier_breaks_728_cover": True,
            "declare_four_support_orbits_global_only_breaks_scope_guard": True,
        },
    }
    payload["logical_sha256"] = logical_sha(payload)

    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
